"""LLM factory for creating language model instances."""

import logging
import os
from typing import Any

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


def create_llm(
    provider: str | None = None,
    model: str | None = None,
    temperature: float | None = None,
    **kwargs: Any,
) -> BaseChatModel:
    """
    Create an LLM instance based on provider and configuration.

    Args:
        provider: LLM provider ("openai", "anthropic", or "gemini")
        model: Model name to use
        temperature: Temperature setting
        **kwargs: Additional arguments to pass to the LLM constructor

    Returns:
        Configured LLM instance

    Raises:
        ValueError: If provider is not supported
    """
    # Get configuration from environment variables with defaults
    provider = provider or os.getenv("DEFAULT_LLM_PROVIDER") or "anthropic"
    model = model or os.getenv("DEFAULT_MODEL") or "claude-3-5-sonnet-latest"

    # Handle temperature - could be passed as arg, env var, or use default
    if temperature is None:
        temp_str = os.getenv("TEMPERATURE")
        temperature = float(temp_str) if temp_str else 0.4

    # Get API keys and other settings with proper None handling
    timeout_str = os.getenv("TIMEOUT_SECONDS")
    timeout_seconds = int(timeout_str) if timeout_str else 60

    max_retries_str = os.getenv("MAX_RETRIES")
    max_retries = int(max_retries_str) if max_retries_str else 3

    # Log which LLM is being created
    logger.info(f"Creating LLM instance: provider={provider}, model={model}, temperature={temperature}")

    if provider == "openai":
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=timeout_seconds,
            max_retries=max_retries,
            **kwargs,
        )
    elif provider == "anthropic":
        return ChatAnthropic(
            model=model,
            temperature=temperature,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            timeout=timeout_seconds,
            max_retries=max_retries,
            **kwargs,
        )
    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            google_api_key=os.getenv("GEMINI_API_KEY"),
            **kwargs,
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
