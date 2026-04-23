"""
Configuration management for Business Decision Agent.
Handles environment variables, defaults, and validation.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class LLMConfig:
    """LLM API Configuration"""
    provider: str = os.getenv("LLM_PROVIDER", "openai")
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = os.getenv("OPENAI_MODEL", "gpt-4")
    temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    max_tokens: int = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
    
    def validate(self) -> None:
        """Validate LLM configuration"""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        if self.temperature < 0 or self.temperature > 1:
            raise ValueError("Temperature must be between 0 and 1")


@dataclass
class DataConfig:
    """Data Processing Configuration"""
    max_chunk_size: int = int(os.getenv("MAX_CHUNK_SIZE", "10000"))
    missing_value_threshold: float = float(os.getenv("MISSING_VALUE_THRESHOLD", "0.5"))
    duplicate_check_enabled: bool = os.getenv("DUPLICATE_CHECK_ENABLED", "True").lower() == "true"
    
    def validate(self) -> None:
        """Validate data configuration"""
        if self.missing_value_threshold < 0 or self.missing_value_threshold > 1:
            raise ValueError("Missing value threshold must be between 0 and 1")


@dataclass
class AnalysisConfig:
    """Analysis Engine Configuration"""
    min_segment_size: int = int(os.getenv("MIN_SEGMENT_SIZE", "50"))
    trend_window_days: int = int(os.getenv("TREND_WINDOW_DAYS", "30"))
    anomaly_sensitivity: float = float(os.getenv("ANOMALY_SENSITIVITY", "0.95"))
    
    def validate(self) -> None:
        """Validate analysis configuration"""
        if self.min_segment_size < 1:
            raise ValueError("Minimum segment size must be >= 1")
        if self.anomaly_sensitivity < 0 or self.anomaly_sensitivity > 1:
            raise ValueError("Anomaly sensitivity must be between 0 and 1")


@dataclass
class PriorityConfig:
    """Priority Engine Configuration"""
    impact_weight: float = float(os.getenv("IMPACT_WEIGHT", "0.4"))
    effort_weight: float = float(os.getenv("EFFORT_WEIGHT", "0.3"))
    value_weight: float = float(os.getenv("VALUE_WEIGHT", "0.3"))
    min_priority_score: float = float(os.getenv("MIN_PRIORITY_SCORE", "6.0"))
    
    def validate(self) -> None:
        """Validate priority engine configuration"""
        total_weight = self.impact_weight + self.effort_weight + self.value_weight
        if abs(total_weight - 1.0) > 0.01:  # Allow small floating point errors
            raise ValueError(f"Weights must sum to 1.0, got {total_weight}")
        if self.min_priority_score < 0 or self.min_priority_score > 10:
            raise ValueError("Minimum priority score must be between 0 and 10")


@dataclass
class OutputConfig:
    """Output Configuration"""
    ceo_summary_length: int = int(os.getenv("CEO_SUMMARY_LENGTH", "300"))
    include_visualizations: bool = os.getenv("INCLUDE_VISUALIZATIONS", "True").lower() == "true"
    output_format: str = os.getenv("OUTPUT_FORMAT", "json")
    
    def validate(self) -> None:
        """Validate output configuration"""
        if self.output_format not in ["json", "csv", "markdown"]:
            raise ValueError(f"Invalid output format: {self.output_format}")


@dataclass
class Config:
    """Master Configuration Class"""
    llm: LLMConfig = None
    data: DataConfig = None
    analysis: AnalysisConfig = None
    priority: PriorityConfig = None
    output: OutputConfig = None
    
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    def __post_init__(self):
        """Initialize sub-configs if not provided"""
        if self.llm is None:
            self.llm = LLMConfig()
        if self.data is None:
            self.data = DataConfig()
        if self.analysis is None:
            self.analysis = AnalysisConfig()
        if self.priority is None:
            self.priority = PriorityConfig()
        if self.output is None:
            self.output = OutputConfig()
    
    def validate(self) -> None:
        """Validate all configurations"""
        self.llm.validate()
        self.data.validate()
        self.analysis.validate()
        self.priority.validate()
        self.output.validate()


# Global config instance
config = Config()

# Validate on import
try:
    config.validate()
except ValueError as e:
    if not os.getenv("DEBUG"):
        raise
    print(f"Configuration Warning: {e}")
