#!/usr/bin/env python3
"""
Giant AI RAG Search - Semantic codebase search interface

Author: Bearded Giant, LLC
License: Apache License 2.0
"""
import sys
import json
import click
from pathlib import Path
from indexer import CodebaseRAG


def search_project(project_path, query, limit=10, format="json"):
    """Search a project's indexed codebase"""
    project_path = Path(project_path)

    # Check if project is initialized (has .giant-ai directory)
    giant_ai_dir = project_path / ".giant-ai"
    if not giant_ai_dir.exists():
        if format == "json":
            return json.dumps(
                {
                    "error": "Project not initialized",
                    "message": f"Run 'ai-init-project-smart' in {project_path} to initialize Giant AI first",
                    "query": query,
                    "project": str(project_path),
                    "results": [],
                }
            )
        else:
            return f"Error: Project {project_path} is not initialized.\nRun 'ai-init-project-smart' to initialize Giant AI first."

    rag = CodebaseRAG(project_path)

    # Fast check if project is indexed
    if not rag.has_index():
        if format == "json":
            return json.dumps(
                {
                    "error": "Project not indexed",
                    "message": f"Run 'ai-rag index {project_path}' to index this project first",
                    "query": query,
                    "project": str(project_path),
                    "results": [],
                }
            )
        else:
            return f"Error: Project {project_path} is not indexed.\nRun 'ai-rag index {project_path}' to index this project first."

    results = rag.search(query, limit)

    if format == "json":
        output = {"query": query, "project": str(project_path), "results": results}
        return json.dumps(output, indent=2)
    else:
        # Human readable format
        lines = [f"Search results for '{query}' in {project_path}:"]
        lines.append("=" * 50)

        for i, result in enumerate(results, 1):
            lines.append(f"\n{i}. {result['metadata']['file_path']}")
            lines.append(
                f"   Lines: {result['metadata']['line_start']}-{result['metadata']['line_end']}"
            )
            lines.append(f"   Type: {result['metadata']['chunk_type']}")
            lines.append(f"   Distance: {result['distance']:.4f}")
            lines.append(f"   Preview: {result['content'][:200]}...")
            lines.append("-" * 50)

        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python search.py <query> [project_path] [limit] [format]")
        print("  query: Search query string")
        print("  project_path: Path to project (default: current directory)")
        print("  limit: Number of results (default: 10)")
        print("  format: Output format - 'json' or 'text' (default: json)")
        sys.exit(1)

    query = sys.argv[1]
    project_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    format = sys.argv[4] if len(sys.argv) > 4 else "json"

    try:
        result = search_project(project_path, query, limit, format)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
