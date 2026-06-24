"""Abstract LLM client interface and a dummy implementation."""

from abc import ABC, abstractmethod
from typing import Optional


class LLMClient(ABC):
    """Abstract base class for language model interaction."""

    @abstractmethod
    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Generate a completion from the LLM."""
        ...


class DummyLLMClient(LLMClient):
    """
    A dummy client that echoes the prompt back.
    Used for testing and demonstration only.
    """

    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        _ = system_prompt, kwargs  # ignored
        return f"[DUMMY LLM RESPONSE] Echo: {prompt[:200]}... (truncated)"
