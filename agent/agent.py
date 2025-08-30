#!/usr/bin/env python3
"""
Giant AI Agent Mode - Autonomous coding with safety controls

Author: Bearded Giant, LLC
License: Apache License 2.0
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .providers.base import LLMProviderFactory
from .checkpoint import CheckpointManager


class AgentMode:
    """Autonomous agent mode for AI development"""

    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir).resolve()
        self.config_dir = self.project_dir / ".giant-ai"
        self.checkpoint_manager = CheckpointManager(project_dir)
        self.session_log = []

        self.context = self._load_project_context()
        self.agent_config = self._load_agent_config()
        provider_name = self.agent_config.get("provider", "claude-code")
        self.provider = LLMProviderFactory.create(provider_name, self.agent_config)

    def execute_task(self, task: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute an agent task with safety controls"""
        options = options or {}

        if options.get("checkpoint", True):
            checkpoint_id = self.checkpoint_manager.create_checkpoint(
                f"Before: {task[:50]}"
            )
        else:
            checkpoint_id = None

        task_context = {
            "project_context": self.context,
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "checkpoint_id": checkpoint_id,
            "auto_accept": options.get("auto_accept", False),
            "continue_session": options.get("continue_session", False),
        }

        prompt = self._build_agent_prompt(
            task, options.get("prompt_template", "default")
        )

        print(f"🤖 Executing agent task: {task}")
        print(f"   Provider: {self.provider.name}")
        print(f"   Auto-accept: {task_context['auto_accept']}")

        result = self.provider.execute_agent_task(prompt, task_context)

        self._log_session(task, result, checkpoint_id)

        if result["success"]:
            print("✅ Task completed successfully")

            if options.get("checkpoint_after", False):
                self.checkpoint_manager.create_checkpoint(f"After: {task[:50]}")
        else:
            print("❌ Task failed")

            if checkpoint_id and options.get("auto_restore_on_failure", False):
                print("🔄 Auto-restoring checkpoint due to failure...")
                self.checkpoint_manager.restore_checkpoint(checkpoint_id)

        return result

    def batch_execute(
        self, tasks: List[str], options: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Execute multiple tasks in sequence"""
        options = options or {}
        results = []

        if options.get("checkpoint", True):
            initial_checkpoint = self.checkpoint_manager.create_checkpoint(
                "Batch start"
            )

        for i, task in enumerate(tasks):
            print(f"\n📋 Task {i+1}/{len(tasks)}: {task}")

            # Continue session for subsequent tasks
            task_options = options.copy()
            if i > 0:
                task_options["continue_session"] = True
                task_options["checkpoint"] = False  # Only checkpoint at start

            result = self.execute_task(task, task_options)
            results.append(result)

            # Stop on failure unless specified
            if not result["success"] and not options.get("continue_on_failure", False):
                print("⛔ Stopping batch due to failure")
                break

        return results

    def interactive_mode(self):
        """Interactive agent mode with checkpoint controls"""
        print("🤖 Giant AI - Agent Mode")
        print("Commands: task <description>, checkpoint, restore <id>, list, exit")
        print("-" * 50)

        while True:
            command = input("\nagent> ").strip()

            if command.lower() == "exit":
                break
            elif command.lower() == "checkpoint":
                desc = input("Checkpoint description: ")
                checkpoint_id = self.checkpoint_manager.create_checkpoint(desc)
            elif command.lower().startswith("restore "):
                checkpoint_id = command.split(" ", 1)[1]
                self.checkpoint_manager.restore_checkpoint(checkpoint_id)
            elif command.lower() == "list":
                checkpoints = self.checkpoint_manager.list_checkpoints()
                for cp in checkpoints[:10]:
                    print(
                        f"  {cp['id']} - {cp['description']} ({cp['modified_files']} files)"
                    )
            elif command.lower().startswith("task "):
                task = command[5:]
                auto_accept = input("Enable auto-accept? (y/N): ").lower() == "y"
                self.execute_task(task, {"auto_accept": auto_accept})
            else:
                print("Unknown command. Use: task, checkpoint, restore, list, or exit")

    def _load_project_context(self) -> Dict[str, Any]:
        """Load project context from .giant-ai"""
        context = {}

        # Load context.md
        context_file = self.config_dir / "context.md"
        if context_file.exists():
            context["project_context"] = context_file.read_text()

        # Load conventions.yml
        conventions_file = self.config_dir / "conventions.yml"
        if conventions_file.exists():
            with open(conventions_file) as f:
                context["conventions"] = yaml.safe_load(f)

        return context

    def _load_agent_config(self) -> Dict[str, Any]:
        """Load agent configuration"""
        config_file = self.config_dir / "agent.yml"

        if config_file.exists():
            with open(config_file) as f:
                return yaml.safe_load(f)

        # Default configuration
        return {
            "provider": "claude-code",
            "checkpoint_before_tasks": True,
            "auto_restore_on_failure": False,
            "max_checkpoints": 20,
            "prompt_templates": {
                "default": "agent/prompts/default.md",
                "refactor": "agent/prompts/refactor.md",
                "feature": "agent/prompts/feature.md",
                "debug": "agent/prompts/debug.md",
            },
        }

    def _build_agent_prompt(self, task: str, template_name: str) -> str:
        """Build agent prompt from template"""
        # Load prompt template
        template_path = Path(__file__).parent / "prompts" / f"{template_name}.md"

        if template_path.exists():
            template = template_path.read_text()
        else:
            # Default template
            template = """You are an autonomous AI agent. Your task is to complete the following:

TASK: {task}

Project Context:
{project_context}

Conventions:
{conventions}

Guidelines:
1. Break down the task into clear steps
2. Implement each step carefully
3. Test your changes when possible
4. Follow project conventions
5. Provide clear summaries of changes

Execute this task autonomously, making all necessary file changes and running appropriate commands."""

        # Format template with context
        return template.format(
            task=task,
            project_context=self.context.get("project_context", ""),
            conventions=json.dumps(self.context.get("conventions", {}), indent=2),
        )

    def _log_session(
        self, task: str, result: Dict[str, Any], checkpoint_id: Optional[str]
    ):
        """Log agent session for analysis"""
        session_entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "provider": result.get("provider"),
            "success": result.get("success"),
            "checkpoint_id": checkpoint_id,
            "output_length": len(result.get("output", "")),
        }

        self.session_log.append(session_entry)

        # Save to file
        log_file = self.config_dir / "agent_sessions.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(session_entry) + "\n")
