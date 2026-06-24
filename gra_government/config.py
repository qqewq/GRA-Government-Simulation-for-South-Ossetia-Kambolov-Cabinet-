"""Configuration loading and validation."""

from dataclasses import dataclass, field
from pathlib import Path
import os
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)

@dataclass
class LLMConfig:
    provider: str = "dummy"
    endpoint: str = ""
    api_key_env: str = "LLM_API_KEY"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1024

@dataclass
class LoggingConfig:
    level: str = "INFO"

@dataclass
class ScenarioConfig:
    time_horizon_steps: int = 12
    initial_state: str = "default"

@dataclass
class AppConfig:
    llm: LLMConfig = field(default_factory=LLMConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    scenario: ScenarioConfig = field(default_factory=ScenarioConfig)

    @classmethod
    def from_dict(cls, data: dict) -> "AppConfig":
        """Create config from a dictionary, with fallback defaults."""
        llm_data = data.get("llm", {})
        logging_data = data.get("logging", {})
        scenario_data = data.get("scenario", {})
        return cls(
            llm=LLMConfig(**llm_data),
            logging=LoggingConfig(**logging_data),
            scenario=ScenarioConfig(**scenario_data),
        )

    @classmethod
    def from_yaml(cls, path: Path) -> "AppConfig":
        """Load from a YAML file if PyYAML is available."""
        try:
            import yaml
        except ImportError:
            raise ImportError("PyYAML is required to load YAML config. Install it with `pip install pyyaml`.")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    @classmethod
    def default(cls) -> "AppConfig":
        return cls()
