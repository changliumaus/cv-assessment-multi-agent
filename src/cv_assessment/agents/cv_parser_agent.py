"""CV Parser Agent - Extracts structured information from CVs."""

import logging

from cv_assessment.agents.base_agent import BaseAgent
from cv_assessment.models.schemas import CVData

logger = logging.getLogger(__name__)

CV_PARSER_PROMPT = """You are an expert CV/Resume parser. Your task is to extract structured information from CV text.

Extract the following information accurately:
- Candidate personal information (name, contact details)
- Professional summary
- Skills: For each skill identified, provide:
  * skill_level: Classify as "beginner", "intermediate", "advanced", or "expert" based on context
  * years_experience: Estimate years of experience with this skill
  * category: Use specific, granular categories
  Note: Be as specific as possible with categories. Avoid generic terms like "technical" or "programming".
- Work experience: For each position, extract company, position, dates, and responsibilities
- Education (institution, degree, field, graduation year)
- Certifications
- Languages

Be thorough and accurate. If information is not present, leave it as null/empty.
Infer skill levels and experience duration when possible from context clues like:
- Years mentioned in work experience
- Project complexity and scope
- Leadership roles or mentoring activities
- Publications, certifications, or awards related to the skill"""


class CVParserAgent(BaseAgent):
    """Agent for parsing CV documents into structured data."""

    def __init__(self, **llm_kwargs):
        """Initialize the CV Parser agent."""
        super().__init__(
            name="CV Parser",
            system_prompt=CV_PARSER_PROMPT,
            **llm_kwargs,
        )

    def parse_cv(self, cv_text: str) -> CVData:
        """
        Parse CV text into structured data.

        Args:
            cv_text: Raw CV text

        Returns:
            Structured CV data
        """
        logger.info("Parsing CV text")

        prompt = f"""Please parse the following CV and extract all relevant information:

CV Text:
{cv_text}

Extract all information into the structured format."""

        cv_data = self.invoke_structured(prompt, CVData)

        logger.info(
            f"Successfully parsed CV for candidate: {cv_data.candidate_name or 'Unknown'}"
        )
        return cv_data
