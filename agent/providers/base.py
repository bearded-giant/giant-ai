#!/usr/bin/env python3
"""
Giant AI LLM Provider Interface - Base classes for AI provider integration

Author: Bearded Giant, LLC
License: Apache License 2.0
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import subprocess
import json
import os
import requests


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__

    @abstractmethod
    def execute_agent_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an agent task with the provider"""
        pass

    @abstractmethod
    def supports_auto_accept(self) -> bool:
        """Check if provider supports auto-accept mode"""
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of supported capabilities"""
        pass


class ClaudeCodeProvider(BaseLLMProvider):
    """Claude Code CLI provider"""

    def execute_agent_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task using Claude Code CLI"""
        cmd = ["claude"]

        if context.get("auto_accept") and self.supports_auto_accept():
            cmd.extend(["--auto-accept"])

        if context.get("continue_session"):
            cmd.extend(["--continue"])

        cmd.extend(["--print", task])

        result = subprocess.run(cmd, capture_output=True, text=True)

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "provider": "claude-code",
        }

    def supports_auto_accept(self) -> bool:
        """Claude Code supports auto-accept mode"""
        return True

    def get_capabilities(self) -> List[str]:
        return ["file_edit", "file_create", "terminal", "search", "auto_accept"]


class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("openai_api_key") or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable or provide in config."
            )
        self.model = config.get("openai_model", "gpt-4-turbo-preview")
        self.temperature = config.get("openai_temperature", 0.7)
        self.max_tokens = config.get("openai_max_tokens", 4000)

    def execute_agent_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task using OpenAI API"""
        system_prompt = self._build_system_prompt(context)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": task},
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions", headers=headers, json=data
            )
            response.raise_for_status()

            result = response.json()
            output = result["choices"][0]["message"]["content"]

            if "```json" in output:
                json_blocks = self._extract_json_blocks(output)
                if json_blocks:
                    self._execute_file_operations(json_blocks)

            return {
                "success": True,
                "output": output,
                "error": "",
                "provider": "openai",
                "model": self.model,
                "usage": result.get("usage", {}),
            }

        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "provider": "openai",
            }

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build system prompt with project context"""
        prompt = """You are an AI coding assistant helping with software development tasks.
        
When editing or creating files, output JSON blocks in this format:
```json
{
  "action": "create" | "edit" | "delete",
  "file": "path/to/file",
  "content": "file content here" // for create/edit
}
```

Project Context:
"""
        if context.get("project_context"):
            prompt += f"\n{context['project_context']}"

        return prompt

    def _extract_json_blocks(self, text: str) -> List[Dict[str, Any]]:
        """Extract JSON blocks from response"""
        blocks = []
        lines = text.split("\n")
        in_json = False
        json_lines = []

        for line in lines:
            if line.strip() == "```json":
                in_json = True
                json_lines = []
            elif line.strip() == "```" and in_json:
                in_json = False
                try:
                    json_text = "\n".join(json_lines)
                    blocks.append(json.loads(json_text))
                except:
                    pass
            elif in_json:
                json_lines.append(line)

        return blocks

    def _execute_file_operations(self, operations: List[Dict[str, Any]]):
        """Execute file operations from JSON blocks"""
        for op in operations:
            action = op.get("action")
            file_path = op.get("file")
            content = op.get("content", "")

            if action == "create" or action == "edit":
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w") as f:
                    f.write(content)
            elif action == "delete":
                if os.path.exists(file_path):
                    os.remove(file_path)

    def supports_auto_accept(self) -> bool:
        return True  # We handle file operations automatically

    def get_capabilities(self) -> List[str]:
        return ["file_edit", "file_create", "search", "api_based"]


class AnthropicProvider(BaseLLMProvider):
    """Anthropic API provider (Claude via API)"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("anthropic_api_key") or os.environ.get(
            "ANTHROPIC_API_KEY"
        )
        if not self.api_key:
            raise ValueError(
                "Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable or provide in config."
            )
        self.model = config.get("anthropic_model", "claude-3-opus-20240229")
        self.temperature = config.get("anthropic_temperature", 0.7)
        self.max_tokens = config.get("anthropic_max_tokens", 4000)

    def execute_agent_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task using Anthropic API"""
        system_prompt = self._build_system_prompt(context)

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": f"{system_prompt}\n\nTask: {task}"}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages", headers=headers, json=data
            )
            response.raise_for_status()

            result = response.json()
            output = result["content"][0]["text"]

            if "```json" in output:
                json_blocks = self._extract_json_blocks(output)
                if json_blocks:
                    self._execute_file_operations(json_blocks)

            return {
                "success": True,
                "output": output,
                "error": "",
                "provider": "anthropic",
                "model": self.model,
                "usage": result.get("usage", {}),
            }

        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "provider": "anthropic",
            }

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build system prompt with project context"""
        prompt = """You are Claude, an AI coding assistant helping with software development tasks.
        
When editing or creating files, output JSON blocks in this format:
```json
{
  "action": "create" | "edit" | "delete",
  "file": "path/to/file",
  "content": "file content here" // for create/edit
}
```

Project Context:
"""
        if context.get("project_context"):
            prompt += f"\n{context['project_context']}"

        return prompt

    def _extract_json_blocks(self, text: str) -> List[Dict[str, Any]]:
        """Extract JSON blocks from response"""
        blocks = []
        lines = text.split("\n")
        in_json = False
        json_lines = []

        for line in lines:
            if line.strip() == "```json":
                in_json = True
                json_lines = []
            elif line.strip() == "```" and in_json:
                in_json = False
                try:
                    json_text = "\n".join(json_lines)
                    blocks.append(json.loads(json_text))
                except:
                    pass
            elif in_json:
                json_lines.append(line)

        return blocks

    def _execute_file_operations(self, operations: List[Dict[str, Any]]):
        """Execute file operations from JSON blocks"""
        for op in operations:
            action = op.get("action")
            file_path = op.get("file")
            content = op.get("content", "")

            if action == "create" or action == "edit":
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w") as f:
                    f.write(content)
            elif action == "delete":
                if os.path.exists(file_path):
                    os.remove(file_path)

    def supports_auto_accept(self) -> bool:
        return True

    def get_capabilities(self) -> List[str]:
        return ["file_edit", "file_create", "search", "api_based"]


class GeminiProvider(BaseLLMProvider):
    """Google Gemini API provider"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Set GEMINI_API_KEY environment variable or provide in config."
            )
        self.model = config.get("gemini_model", "gemini-pro")
        self.temperature = config.get("gemini_temperature", 0.7)
        self.max_tokens = config.get("gemini_max_tokens", 4000)

    def execute_agent_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task using Gemini API"""
        system_prompt = self._build_system_prompt(context)

        headers = {"Content-Type": "application/json"}

        data = {
            "contents": [{"parts": [{"text": f"{system_prompt}\n\nTask: {task}"}]}],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens,
            },
        }

        try:
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}",
                headers=headers,
                json=data,
            )
            response.raise_for_status()

            result = response.json()
            output = result["candidates"][0]["content"]["parts"][0]["text"]

            if "```json" in output:
                json_blocks = self._extract_json_blocks(output)
                if json_blocks:
                    self._execute_file_operations(json_blocks)

            return {
                "success": True,
                "output": output,
                "error": "",
                "provider": "gemini",
                "model": self.model,
                "usage": result.get("usageMetadata", {}),
            }

        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "provider": "gemini",
            }

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build system prompt with project context"""
        prompt = """You are Gemini, an AI coding assistant helping with software development tasks.
        
When editing or creating files, output JSON blocks in this format:
```json
{
  "action": "create" | "edit" | "delete",
  "file": "path/to/file",
  "content": "file content here" // for create/edit
}
```

Project Context:
"""
        if context.get("project_context"):
            prompt += f"\n{context['project_context']}"

        return prompt

    def _extract_json_blocks(self, text: str) -> List[Dict[str, Any]]:
        """Extract JSON blocks from response"""
        blocks = []
        lines = text.split("\n")
        in_json = False
        json_lines = []

        for line in lines:
            if line.strip() == "```json":
                in_json = True
                json_lines = []
            elif line.strip() == "```" and in_json:
                in_json = False
                try:
                    json_text = "\n".join(json_lines)
                    blocks.append(json.loads(json_text))
                except:
                    pass
            elif in_json:
                json_lines.append(line)

        return blocks

    def _execute_file_operations(self, operations: List[Dict[str, Any]]):
        """Execute file operations from JSON blocks"""
        for op in operations:
            action = op.get("action")
            file_path = op.get("file")
            content = op.get("content", "")

            if action == "create" or action == "edit":
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w") as f:
                    f.write(content)
            elif action == "delete":
                if os.path.exists(file_path):
                    os.remove(file_path)

    def supports_auto_accept(self) -> bool:
        return True

    def get_capabilities(self) -> List[str]:
        return ["file_edit", "file_create", "search", "api_based"]


class OllamaProvider(BaseLLMProvider):
    """Ollama provider for local LLM models"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("ollama_base_url", "http://localhost:11434")
        self.model = config.get("ollama_model", "llama2")
        self.temperature = config.get("ollama_temperature", 0.7)
        self.context_length = config.get("ollama_context_length", 4096)

    def execute_agent_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task using Ollama API"""
        system_prompt = self._build_system_prompt(context)

        # Combine system prompt and task
        full_prompt = f"{system_prompt}\n\nTask: {task}"

        data = {
            "model": self.model,
            "prompt": full_prompt,
            "temperature": self.temperature,
            "stream": False,
            "options": {"num_ctx": self.context_length},
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=data,
                timeout=300,  # Longer timeout for local models
            )
            response.raise_for_status()

            result = response.json()
            output = result.get("response", "")

            if "```json" in output:
                json_blocks = self._extract_json_blocks(output)
                if json_blocks:
                    self._execute_file_operations(json_blocks)

            return {
                "success": True,
                "output": output,
                "error": "",
                "provider": "ollama",
                "model": self.model,
                "total_duration": result.get("total_duration", 0),
                "eval_count": result.get("eval_count", 0),
            }

        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "output": "",
                "error": f"Failed to connect to Ollama at {self.base_url}. Is Ollama running?",
                "provider": "ollama",
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "provider": "ollama",
            }

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build system prompt with project context"""
        prompt = """You are an AI coding assistant helping with software development tasks.
        
When editing or creating files, output JSON blocks in this format:
```json
{
  "action": "create" | "edit" | "delete",
  "file": "path/to/file",
  "content": "file content here" // for create/edit
}
```

Project Context:
"""
        if context.get("project_context"):
            prompt += f"\n{context['project_context']}"

        return prompt

    def _extract_json_blocks(self, text: str) -> List[Dict[str, Any]]:
        """Extract JSON blocks from response"""
        blocks = []
        lines = text.split("\n")
        in_json = False
        json_lines = []

        for line in lines:
            if line.strip() == "```json":
                in_json = True
                json_lines = []
            elif line.strip() == "```" and in_json:
                in_json = False
                try:
                    json_text = "\n".join(json_lines)
                    blocks.append(json.loads(json_text))
                except:
                    pass
            elif in_json:
                json_lines.append(line)

        return blocks

    def _execute_file_operations(self, operations: List[Dict[str, Any]]):
        """Execute file operations from JSON blocks"""
        for op in operations:
            action = op.get("action")
            file_path = op.get("file")
            content = op.get("content", "")

            if action == "create" or action == "edit":
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w") as f:
                    f.write(content)
            elif action == "delete":
                if os.path.exists(file_path):
                    os.remove(file_path)

    def supports_auto_accept(self) -> bool:
        return True

    def get_capabilities(self) -> List[str]:
        return ["file_edit", "file_create", "search", "local", "offline"]


class LLMProviderFactory:
    """Factory for creating LLM providers"""

    _providers = {
        "claude-code": ClaudeCodeProvider,
        "claude-desktop": None,  # Lazy import
        "claude-desktop-mcp": None,  # Lazy import
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "gemini": GeminiProvider,
        "ollama": OllamaProvider,
    }

    @classmethod
    def create(cls, provider_name: str, config: Dict[str, Any]) -> BaseLLMProvider:
        """Create an LLM provider instance"""
        if provider_name not in cls._providers:
            raise ValueError(f"Unknown provider: {provider_name}")

        # Lazy import for Claude Desktop providers
        if provider_name == "claude-desktop" and cls._providers[provider_name] is None:
            from .claude_desktop import ClaudeDesktopProvider

            cls._providers[provider_name] = ClaudeDesktopProvider
        elif (
            provider_name == "claude-desktop-mcp"
            and cls._providers[provider_name] is None
        ):
            from .claude_desktop import ClaudeDesktopMCPProvider

            cls._providers[provider_name] = ClaudeDesktopMCPProvider

        provider_class = cls._providers[provider_name]
        return provider_class(config)

    @classmethod
    def list_providers(cls) -> List[str]:
        """List available providers"""
        return list(cls._providers.keys())

    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """Register a new provider"""
        cls._providers[name] = provider_class
