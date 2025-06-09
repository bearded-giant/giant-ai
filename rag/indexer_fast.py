#!/usr/bin/env python3
import json
import click
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
import tree_sitter_python as tspython
from tree_sitter import Language, Parser


class CodebaseRAG:
    def __init__(self, project_path, persist_directory=None):
        self.project_path = Path(project_path).resolve()

        # Use global RAG db location with project-specific collection
        if persist_directory is None:
            self.persist_dir = Path.home() / ".giant-ai" / "rag" / "db"
        else:
            self.persist_dir = Path(persist_directory)

        self.persist_dir.mkdir(parents=True, exist_ok=True)

        # Project identifier for collection name
        self.project_id = self.project_path.name.replace(" ", "_").replace("/", "_")

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.collection = self.client.get_or_create_collection(
            name=f"codebase_{self.project_id}", embedding_function=self.ef
        )

        self.setup_parsers()

    def setup_parsers(self):
        try:
            PY_LANGUAGE = Language(tspython.language(), "python")
            self.parser = Parser()
            self.parser.set_language(PY_LANGUAGE)
        except:
            self.parser = None

    def index_codebase(self, batch_size=100, max_file_size_mb=10, use_chunking=False):
        file_patterns = [
            "*.py",
            "*.js",
            "*.ts",
            "*.tsx",
            "*.jsx",
            "*.rs",
            "*.go",
            "*.java",
            "*.cpp",
            "*.h",
            "*.lua",
            "*.vim",
        ]
        indexed_count = 0

        click.echo(f"Indexing project: {self.project_path}")
        click.echo(f"Collection name: codebase_{self.project_id}")
        click.echo(f"Batch size: {batch_size}, Max file size: {max_file_size_mb}MB")
        click.echo(
            f"Chunking mode: {'enabled' if use_chunking else 'disabled (fast mode)'}"
        )

        # Collect all files to index first
        files_to_index = []
        for pattern in file_patterns:
            for file_path in self.project_path.rglob(pattern):
                if self.should_index_file(file_path, max_file_size_mb):
                    files_to_index.append(file_path)

        click.echo(f"Found {len(files_to_index)} files to index")

        # Process files in batches
        all_docs = []
        all_metas = []
        all_ids = []

        with click.progressbar(
            files_to_index, label="Indexing files", show_pos=True
        ) as bar:
            for file_path in bar:
                if use_chunking:
                    # Original chunking behavior (slower)
                    docs, metas, ids = self.prepare_file_chunks(file_path)
                else:
                    # Fast mode - one document per file
                    doc, meta, doc_id = self.prepare_file_fast(file_path)
                    if doc:
                        docs, metas, ids = [doc], [meta], [doc_id]
                    else:
                        docs, metas, ids = [], [], []

                if docs:
                    all_docs.extend(docs)
                    all_metas.extend(metas)
                    all_ids.extend(ids)
                    indexed_count += 1

                    # Insert in batches
                    if len(all_docs) >= batch_size:
                        try:
                            self.collection.upsert(
                                documents=all_docs, metadatas=all_metas, ids=all_ids
                            )
                            all_docs = []
                            all_metas = []
                            all_ids = []
                        except Exception as e:
                            click.echo(f"\nError during batch insert: {e}", err=True)
                            all_docs = []
                            all_metas = []
                            all_ids = []

        # Insert remaining documents
        if all_docs:
            try:
                self.collection.upsert(
                    documents=all_docs, metadatas=all_metas, ids=all_ids
                )
            except Exception as e:
                click.echo(f"\nError during final batch insert: {e}", err=True)

        click.echo(f"✓ Indexed {indexed_count} files")
        return indexed_count

    def should_index_file(self, file_path, max_file_size_mb=10):
        exclude_dirs = {
            ".git",
            "node_modules",
            "target",
            "build",
            "__pycache__",
            ".claude",
            "venv",
            ".venv",
            "dist",
            ".next",
        }
        if any(part in exclude_dirs for part in file_path.parts):
            return False

        try:
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            if file_size_mb > max_file_size_mb:
                click.echo(
                    f"Skipping large file ({file_size_mb:.1f}MB): {file_path.relative_to(self.project_path)}",
                    err=True,
                )
                return False
        except:
            pass

        return True

    def prepare_file_fast(self, file_path):
        """Fast mode - index entire file as one document with smart context"""
        try:
            content = file_path.read_text(encoding="utf-8")

            # For Python files, extract key components for metadata
            functions = []
            classes = []
            if file_path.suffix == ".py" and self.parser:
                tree = self.parser.parse(bytes(content, "utf8"))
                functions, classes = self.extract_python_symbols(
                    tree.root_node, content
                )

            # Create a single document with rich metadata
            doc_id = str(file_path.relative_to(self.project_path))
            metadata = {
                "file_path": str(file_path.relative_to(self.project_path)),
                "file_type": file_path.suffix,
                "project": str(self.project_path),
                "functions": json.dumps(functions[:20]),  # Limit stored functions
                "classes": json.dumps(classes[:10]),  # Limit stored classes
                "line_count": len(content.split("\n")),
            }

            return content, metadata, doc_id

        except Exception as e:
            click.echo(f"Error preparing {file_path}: {e}", err=True)
            return None, None, None

    def extract_python_symbols(self, node, content):
        """Extract function and class names for metadata"""
        functions = []
        classes = []

        def extract_nodes(node):
            if (
                node.type == "function_definition"
                or node.type == "async_function_definition"
            ):
                # Get function name
                for child in node.children:
                    if child.type == "identifier":
                        functions.append(child.text.decode("utf8"))
                        break
            elif node.type == "class_definition":
                # Get class name
                for child in node.children:
                    if child.type == "identifier":
                        classes.append(child.text.decode("utf8"))
                        break

            for child in node.children:
                extract_nodes(child)

        extract_nodes(node)
        return functions, classes

    def prepare_file_chunks(self, file_path):
        """Original chunking method - kept for compatibility"""
        try:
            content = file_path.read_text(encoding="utf-8")

            if file_path.suffix == ".py" and self.parser:
                chunks = self.parse_python_file(content, file_path)
            else:
                chunks = self.chunk_by_lines(content, file_path)

            batch_docs = []
            batch_metas = []
            batch_ids = []

            for i, chunk in enumerate(chunks):
                doc_id = f"{file_path.relative_to(self.project_path)}:{i}"
                batch_docs.append(chunk["content"])
                batch_metas.append(
                    {
                        "file_path": str(file_path.relative_to(self.project_path)),
                        "chunk_type": chunk["type"],
                        "line_start": chunk.get("line_start", 0),
                        "line_end": chunk.get("line_end", 0),
                        "project": str(self.project_path),
                    }
                )
                batch_ids.append(doc_id)

            return batch_docs, batch_metas, batch_ids

        except Exception as e:
            click.echo(f"Error preparing {file_path}: {e}", err=True)
            return [], [], []

    def parse_python_file(self, content, file_path):
        tree = self.parser.parse(bytes(content, "utf8"))
        chunks = []

        def extract_nodes(node, depth=0):
            if node.type in [
                "function_definition",
                "class_definition",
                "async_function_definition",
            ]:
                start_line = node.start_point[0]
                end_line = node.end_point[0]
                node_content = "\n".join(content.split("\n")[start_line : end_line + 1])

                chunks.append(
                    {
                        "content": node_content,
                        "type": node.type,
                        "line_start": start_line,
                        "line_end": end_line,
                    }
                )

            for child in node.children:
                extract_nodes(child, depth + 1)

        extract_nodes(tree.root_node)

        if chunks and chunks[0]["line_start"] > 5:
            file_header = "\n".join(content.split("\n")[: chunks[0]["line_start"]])
            if file_header.strip():
                chunks.insert(
                    0,
                    {
                        "content": file_header,
                        "type": "module_header",
                        "line_start": 0,
                        "line_end": chunks[0]["line_start"],
                    },
                )

        return chunks or self.chunk_by_lines(content, file_path)

    def chunk_by_lines(self, content, file_path, chunk_size=50):
        lines = content.split("\n")
        chunks = []

        for i in range(0, len(lines), chunk_size):
            chunk_lines = lines[i : i + chunk_size]
            chunks.append(
                {
                    "content": "\n".join(chunk_lines),
                    "type": "text_chunk",
                    "line_start": i,
                    "line_end": min(i + chunk_size, len(lines)),
                }
            )

        return chunks

    def search(self, query, n_results=10):
        results = self.collection.query(query_texts=[query], n_results=n_results)

        return [
            {"content": doc, "metadata": meta, "distance": dist}
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    def clear_project_index(self):
        """Clear the index for this specific project"""
        try:
            self.client.delete_collection(f"codebase_{self.project_id}")
            click.echo(f"Cleared index for project: {self.project_id}")
        except:
            click.echo(f"No existing index found for project: {self.project_id}")


@click.group()
def cli():
    """Claude RAG indexer for codebase semantic search"""
    pass


@cli.command()
@click.argument("project_path", type=click.Path(exists=True), default=".")
@click.option("--clear", is_flag=True, help="Clear existing index before indexing")
@click.option(
    "--batch-size",
    "-b",
    default=100,
    help="Number of documents to insert per batch (default: 100)",
)
@click.option(
    "--chunk", is_flag=True, help="Enable chunking mode (slower but more granular)"
)
@click.option(
    "--max-file-size",
    "-m",
    default=10,
    help="Maximum file size in MB to index (default: 10)",
)
def index(project_path, clear, batch_size, chunk, max_file_size):
    """Index a codebase for semantic search"""
    rag = CodebaseRAG(project_path)

    if clear:
        rag.clear_project_index()

    count = rag.index_codebase(
        batch_size=batch_size, max_file_size_mb=max_file_size, use_chunking=chunk
    )
    click.echo(f"Indexing complete! Processed {count} files.")


@cli.command()
@click.argument("query")
@click.argument("project_path", type=click.Path(exists=True), default=".")
@click.option("--limit", "-n", default=10, help="Number of results to return")
def search(query, project_path, limit):
    """Search the indexed codebase"""
    rag = CodebaseRAG(project_path)
    results = rag.search(query, limit)

    click.echo(f"\nSearch results for '{query}':")
    click.echo("=" * 50)

    for i, result in enumerate(results[:limit], 1):
        click.echo(f"\n{i}. {result['metadata']['file_path']}")
        if "line_start" in result["metadata"]:
            click.echo(
                f"   Lines: {result['metadata']['line_start']}-{result['metadata']['line_end']}"
            )
            click.echo(f"   Type: {result['metadata']['chunk_type']}")
        else:
            click.echo(
                f"   File type: {result['metadata'].get('file_type', 'unknown')}"
            )
            click.echo(f"   Lines: {result['metadata'].get('line_count', 'unknown')}")
        click.echo(f"   Distance: {result['distance']:.4f}")
        click.echo(f"   Preview: {result['content'][:200]}...")
        click.echo("-" * 50)


@cli.command()
def list_projects():
    """List all indexed projects"""
    persist_dir = Path.home() / ".giant-ai" / "rag" / "db"
    if not persist_dir.exists():
        click.echo("No projects indexed yet.")
        return

    client = chromadb.PersistentClient(path=str(persist_dir))
    collections = client.list_collections()

    click.echo("Indexed projects:")
    for collection in collections:
        if collection.name.startswith("codebase_"):
            project_name = collection.name.replace("codebase_", "")
            click.echo(f"  - {project_name}")


if __name__ == "__main__":
    cli()

