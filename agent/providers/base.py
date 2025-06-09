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
        # Build command with auto-accept if supported
        cmd = ["claude"]
        
        if context.get("auto_accept") and self.supports_auto_accept():
            cmd.extend(["--auto-accept"])
            
        if context.get("continue_session"):
            cmd.extend(["--continue"])
            
        # Add the task as a prompt
        cmd.extend(["--print", task])
        
        # Execute and capture output
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "provider": "claude-code"
        }
    
    def supports_auto_accept(self) -> bool:
        """Claude Code supports auto-accept mode"""
        return True
    
    def get_capabilities(self) -> List[str]:
        return ["file_edit", "file_create", "terminal", "search", "auto_accept"]

class OpenAIProvider(BaseLLMProvider):
    """OpenAI CLI provider (future)"""
    
    def execute_agent_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Placeholder for OpenAI CLI integration
        return {
            "success": False,
            "output": "OpenAI CLI provider not yet implemented",
            "error": "",
            "provider": "openai"
        }
    
    def supports_auto_accept(self) -> bool:
        return False  # TBD based on OpenAI CLI capabilities
    
    def get_capabilities(self) -> List[str]:
        return ["file_edit", "file_create", "search"]

class LLMProviderFactory:
    """Factory for creating LLM providers"""
    
    _providers = {
        "claude-code": ClaudeCodeProvider,
        "openai": OpenAIProvider,
    }
    
    @classmethod
    def create(cls, provider_name: str, config: Dict[str, Any]) -> BaseLLMProvider:
        """Create an LLM provider instance"""
        if provider_name not in cls._providers:
            raise ValueError(f"Unknown provider: {provider_name}")
        
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