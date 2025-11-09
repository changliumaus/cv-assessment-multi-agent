"""Base agent class."""

import logging
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

from cv_assessment.utils.llm_factory import create_llm

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all agents in the CV assessment system."""

    def __init__(
        self,
        name: str,
        system_prompt: str,
        llm: BaseChatModel | None = None,
        **llm_kwargs: Any,
    ):
        """
        Initialize the base agent.

        Args:
            name: Agent name
            system_prompt: System prompt for the agent
            llm: Optional pre-configured LLM instance
            **llm_kwargs: Additional arguments for LLM creation
        """
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm or create_llm(**llm_kwargs)
        logger.info(f"Initialized agent: {name}")

    def invoke(self, prompt: str) -> str:
        """
        Invoke the agent with a prompt.

        Args:
            prompt: User prompt

        Returns:
            Agent response
        """
        messages = [SystemMessage(content=self.system_prompt), ("user", prompt)]
        response = self.llm.invoke(messages)
        return response.content

    def invoke_structured(
        self, prompt: str, output_model: type[BaseModel]
    ) -> BaseModel:
        """
        Invoke the agent and get structured output.

        Args:
            prompt: User prompt
            output_model: Pydantic model for structured output

        Returns:
            Parsed structured output
        """
        parser = PydanticOutputParser(pydantic_object=output_model)
        format_instructions = parser.get_format_instructions()

        full_prompt = f"{prompt}\n\n{format_instructions}"
        messages = [SystemMessage(content=self.system_prompt), ("user", full_prompt)]

        # Use with_structured_output for better reliability
        structured_llm = self.llm.with_structured_output(output_model)
        response = structured_llm.invoke(messages)

        return response
