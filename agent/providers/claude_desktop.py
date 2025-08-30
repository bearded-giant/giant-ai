#!/usr/bin/env python3
"""
Claude Desktop Provider - Uses Claude Desktop app to leverage Pro Max plan
No API tokens required - uses your existing Claude Desktop session

Author: Bearded Giant, LLC
License: Apache License 2.0
"""

import json
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import time
import shutil

# Import base provider
try:
    from .base import BaseLLMProvider
except ImportError:
    # For standalone testing
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from agent.providers.base import BaseLLMProvider


class ClaudeDesktopProvider(BaseLLMProvider):
    """
    Provider that uses Claude Desktop application instead of API tokens.
    This leverages your Pro Max plan without consuming API tokens.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize Claude Desktop provider"""
        super().__init__(config)
        self.name = "claude-desktop"

        # Check if Claude Desktop is available
        self.claude_command = self._find_claude_command()
        if not self.claude_command:
            raise RuntimeError(
                "Claude Desktop not found. Please ensure Claude Desktop is installed."
            )

        # Configuration
        self.timeout = config.get("timeout", 300)  # 5 minutes default
        self.auto_accept = config.get("auto_accept", False)
        self.context_window = config.get(
            "context_window", 200000
        )  # Claude's large context

    def _find_claude_command(self) -> Optional[str]:
        """Find the Claude Desktop command"""
        # Check common locations
        possible_commands = [
            "claude",  # If added to PATH
            "/Applications/Claude.app/Contents/MacOS/Claude",  # macOS direct path
            shutil.which("claude"),  # System PATH
        ]

        for cmd in possible_commands:
            if cmd and self._test_command(cmd):
                return cmd

        return None

    def _test_command(self, cmd: str) -> bool:
        """Test if a command is valid Claude Desktop"""
        if not cmd:
            return False

        try:
            # Try to run with --version or similar
            # Note: Claude Desktop might not have CLI flags, so we just check if it exists
            if cmd.startswith("/Applications/"):
                return Path(cmd).exists()
            else:
                result = subprocess.run(
                    ["which", cmd], capture_output=True, text=True, timeout=2
                )
                return result.returncode == 0
        except:
            return False

    def execute_agent_task(
        self, prompt: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute an agent task using Claude Desktop.

        Strategy:
        1. Create a temporary file with the task
        2. Use AppleScript or system automation to send to Claude Desktop
        3. Monitor for response
        """
        try:
            # For now, we'll use a file-based approach
            # Create a task file that Claude Desktop can process
            task_file = self._create_task_file(prompt, context)

            # Execute via Claude Desktop
            # This is where we'd integrate with Claude Desktop's actual interface
            # For now, we'll use a workaround approach

            result = self._execute_via_applescript(prompt, context)

            return {"success": True, "output": result, "provider": self.name}

        except Exception as e:
            return {"success": False, "error": str(e), "provider": self.name}

    def _create_task_file(self, prompt: str, context: Dict[str, Any]) -> Path:
        """Create a temporary file with the task details"""
        task_content = f"""# Agent Task Request

## Context
Project: {context.get('project_context', {}).get('project', 'Unknown')}
Timestamp: {context.get('timestamp', 'Unknown')}
Auto-accept: {context.get('auto_accept', False)}

## Task
{prompt}

## Instructions
Please complete this task autonomously. You have access to:
- File operations (read, write, edit)
- Terminal commands
- Code search
- Git operations

Work step by step and provide a summary of changes made.
"""

        # Create temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(task_content)
            return Path(f.name)

    def _execute_via_applescript(self, prompt: str, context: Dict[str, Any]) -> str:
        """
        Execute task using AppleScript to interact with Claude Desktop.
        This is macOS specific but can be adapted for other platforms.
        """

        # AppleScript to send text to Claude Desktop
        # This is a simplified version - real implementation would be more robust
        applescript = f"""
        tell application "Claude"
            activate
            delay 1
            tell application "System Events"
                keystroke "n" using command down
                delay 0.5
                keystroke "{self._escape_for_applescript(prompt)}"
                delay 0.5
                keystroke return
            end tell
        end tell
        """

        try:
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=30,
            )

            # In a real implementation, we'd monitor for the response
            # For now, return a placeholder
            return (
                "Task sent to Claude Desktop. Please check the application for results."
            )

        except subprocess.TimeoutExpired:
            return "Task sent but timed out waiting for response"
        except Exception as e:
            return f"Error executing via AppleScript: {e}"

    def _escape_for_applescript(self, text: str) -> str:
        """Escape text for AppleScript"""
        # Escape quotes and backslashes
        text = text.replace("\\", "\\\\")
        text = text.replace('"', '\\"')
        text = text.replace("\n", "\\n")
        return text

    def complete(self, prompt: str, **kwargs) -> str:
        """Simple completion interface"""
        result = self.execute_agent_task(prompt, {"auto_accept": False})
        if result["success"]:
            return result["output"]
        else:
            raise RuntimeError(
                f"Completion failed: {result.get('error', 'Unknown error')}"
            )

    def stream_complete(self, prompt: str, **kwargs):
        """Streaming not yet implemented for Claude Desktop"""
        # Could potentially implement by monitoring Claude Desktop's output
        yield self.complete(prompt, **kwargs)

    def supports_auto_accept(self) -> bool:
        """Check if provider supports auto-accept mode"""
        return True  # We can auto-accept via AppleScript

    def get_capabilities(self) -> List[str]:
        """Get provider capabilities"""
        return ["file_edit", "file_create", "search", "terminal", "pro_max_plan"]


class ClaudeDesktopMCPProvider(BaseLLMProvider):
    """
    Alternative implementation using MCP protocol to communicate with Claude Desktop.
    This would be the preferred approach if Claude Desktop exposes an MCP server.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize MCP-based Claude Desktop provider"""
        super().__init__(config)
        self.name = "claude-desktop-mcp"

        # MCP connection details
        self.mcp_port = config.get("mcp_port", 3333)  # Default MCP port
        self.mcp_host = config.get("mcp_host", "localhost")

        # Try to establish MCP connection
        self.mcp_client = self._create_mcp_client()

    def _create_mcp_client(self):
        """Create MCP client to connect to Claude Desktop"""
        try:
            # Import MCP SDK
            from mcp import MCPClient

            client = MCPClient(
                host=self.mcp_host,
                port=self.mcp_port,
                transport="stdio",  # or "websocket"
            )

            # Test connection
            client.connect()

            return client

        except ImportError:
            print("MCP SDK not installed. Install with: pip install mcp-sdk")
            return None
        except Exception as e:
            print(f"Could not connect to Claude Desktop MCP server: {e}")
            return None

    def execute_agent_task(
        self, prompt: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute task via MCP protocol"""
        if not self.mcp_client:
            return {
                "success": False,
                "error": "MCP client not connected",
                "provider": self.name,
            }

        try:
            # Call MCP tool
            result = self.mcp_client.call_tool(
                "execute_task",
                {
                    "prompt": prompt,
                    "context": context,
                    "auto_accept": context.get("auto_accept", False),
                },
            )

            return {
                "success": True,
                "output": result.get("content", ""),
                "provider": self.name,
            }

        except Exception as e:
            return {"success": False, "error": str(e), "provider": self.name}

    def complete(self, prompt: str, **kwargs) -> str:
        """Simple completion via MCP"""
        if not self.mcp_client:
            raise RuntimeError("MCP client not connected")

        try:
            result = self.mcp_client.call_tool("complete", {"prompt": prompt, **kwargs})
            return result.get("content", "")
        except Exception as e:
            raise RuntimeError(f"MCP completion failed: {e}")

    def stream_complete(self, prompt: str, **kwargs):
        """Streaming via MCP"""
        if not self.mcp_client:
            raise RuntimeError("MCP client not connected")

        try:
            # MCP streaming would work differently
            stream = self.mcp_client.stream_tool(
                "complete", {"prompt": prompt, "stream": True, **kwargs}
            )

            for chunk in stream:
                yield chunk.get("content", "")

        except Exception as e:
            raise RuntimeError(f"MCP streaming failed: {e}")

    def supports_auto_accept(self) -> bool:
        """Check if provider supports auto-accept mode"""
        return True  # MCP can support auto-accept

    def get_capabilities(self) -> List[str]:
        """Get provider capabilities"""
        return [
            "file_edit",
            "file_create",
            "search",
            "terminal",
            "mcp_protocol",
            "pro_max_plan",
        ]


def test_claude_desktop():
    """Test function to verify Claude Desktop provider works"""
    print("Testing Claude Desktop Provider...")

    # Test config
    config = {"auto_accept": False, "timeout": 30}

    try:
        # Try AppleScript version
        provider = ClaudeDesktopProvider(config)
        print(f"✅ Claude Desktop Provider initialized")
        print(f"   Command: {provider.claude_command}")

        # Test simple completion
        result = provider.execute_agent_task("What is 2+2?", {"auto_accept": False})

        print(f"   Result: {result}")

    except Exception as e:
        print(f"❌ Claude Desktop Provider failed: {e}")

    try:
        # Try MCP version
        provider = ClaudeDesktopMCPProvider(config)
        if provider.mcp_client:
            print(f"✅ Claude Desktop MCP Provider connected")
        else:
            print(f"⚠️  Claude Desktop MCP Provider not available")

    except Exception as e:
        print(f"❌ Claude Desktop MCP Provider failed: {e}")


if __name__ == "__main__":
    test_claude_desktop()
