#!/usr/bin/env python3
"""
Giant AI Checkpoint System - Project state management for agent mode

Author: Bearded Giant, LLC
License: Apache License 2.0
"""

import os
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class CheckpointManager:
    """Manage project checkpoints for agent mode"""

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir).resolve()
        self.checkpoint_dir = self.project_dir / ".giant-ai" / "checkpoints"
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def create_checkpoint(self, description: str = "") -> str:
        """Create a checkpoint of current project state"""
        checkpoint_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_path = self.checkpoint_dir / checkpoint_id

        # Create checkpoint metadata
        metadata = {
            "id": checkpoint_id,
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "git_status": self._get_git_status(),
            "modified_files": [],
        }

        # If git repo, use git stash for checkpoint
        if self._is_git_repo():
            # Get list of modified files
            result = subprocess.run(
                ["git", "diff", "--name-only"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                metadata["modified_files"] = result.stdout.strip().split("\n")

            # Create a git stash as checkpoint
            stash_msg = f"AI Agent Checkpoint: {checkpoint_id}"
            subprocess.run(
                ["git", "stash", "push", "-m", stash_msg, "--include-untracked"],
                cwd=self.project_dir,
            )
            metadata["git_stash"] = stash_msg
        else:
            # For non-git projects, create file backups
            checkpoint_path.mkdir(parents=True, exist_ok=True)
            self._backup_project_files(checkpoint_path)
            metadata["backup_path"] = str(checkpoint_path)

        # Save metadata
        metadata_path = self.checkpoint_dir / f"{checkpoint_id}.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"✅ Created checkpoint: {checkpoint_id}")
        return checkpoint_id

    def restore_checkpoint(self, checkpoint_id: str) -> bool:
        """Restore project to a checkpoint state"""
        metadata_path = self.checkpoint_dir / f"{checkpoint_id}.json"

        if not metadata_path.exists():
            print(f"❌ Checkpoint not found: {checkpoint_id}")
            return False

        with open(metadata_path) as f:
            metadata = json.load(f)

        if "git_stash" in metadata:
            # Restore from git stash
            # First, stash current changes
            subprocess.run(
                ["git", "stash", "push", "-m", "Temp stash before restore"],
                cwd=self.project_dir,
            )

            # Find and apply the checkpoint stash
            result = subprocess.run(
                ["git", "stash", "list"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
            )

            stash_list = result.stdout.strip().split("\n")
            for i, stash in enumerate(stash_list):
                if metadata["git_stash"] in stash:
                    subprocess.run(
                        ["git", "stash", "pop", f"stash@{{{i}}}"], cwd=self.project_dir
                    )
                    break
        else:
            # Restore from file backups
            backup_path = Path(metadata["backup_path"])
            if backup_path.exists():
                self._restore_project_files(backup_path)

        print(f"✅ Restored checkpoint: {checkpoint_id}")
        return True

    def list_checkpoints(self) -> List[Dict]:
        """List all available checkpoints"""
        checkpoints = []

        for metadata_file in self.checkpoint_dir.glob("*.json"):
            with open(metadata_file) as f:
                metadata = json.load(f)
                checkpoints.append(
                    {
                        "id": metadata["id"],
                        "timestamp": metadata["timestamp"],
                        "description": metadata["description"],
                        "modified_files": len(metadata.get("modified_files", [])),
                    }
                )

        return sorted(checkpoints, key=lambda x: x["timestamp"], reverse=True)

    def cleanup_old_checkpoints(self, keep_count: int = 10):
        """Remove old checkpoints, keeping the most recent ones"""
        checkpoints = self.list_checkpoints()

        if len(checkpoints) > keep_count:
            for checkpoint in checkpoints[keep_count:]:
                self._remove_checkpoint(checkpoint["id"])

    def _is_git_repo(self) -> bool:
        """Check if project is a git repository"""
        git_dir = self.project_dir / ".git"
        return git_dir.exists() and git_dir.is_dir()

    def _get_git_status(self) -> Optional[str]:
        """Get current git status"""
        if not self._is_git_repo():
            return None

        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=self.project_dir,
            capture_output=True,
            text=True,
        )

        return result.stdout if result.returncode == 0 else None

    def _backup_project_files(self, backup_path: Path):
        """Create file backups for non-git projects"""
        # Simple implementation - can be enhanced
        for item in self.project_dir.iterdir():
            if item.name not in [".giant-ai", "node_modules", ".venv", "__pycache__"]:
                if item.is_file():
                    shutil.copy2(item, backup_path / item.name)
                elif item.is_dir():
                    shutil.copytree(item, backup_path / item.name)

    def _restore_project_files(self, backup_path: Path):
        """Restore files from backup"""
        # Simple implementation - can be enhanced
        for item in backup_path.iterdir():
            dest = self.project_dir / item.name
            if item.is_file():
                shutil.copy2(item, dest)
            elif item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)

    def _remove_checkpoint(self, checkpoint_id: str):
        """Remove a checkpoint"""
        metadata_path = self.checkpoint_dir / f"{checkpoint_id}.json"

        if metadata_path.exists():
            with open(metadata_path) as f:
                metadata = json.load(f)

            # Remove backup files if they exist
            if "backup_path" in metadata:
                backup_path = Path(metadata["backup_path"])
                if backup_path.exists():
                    shutil.rmtree(backup_path)

            # Remove metadata file
            metadata_path.unlink()
