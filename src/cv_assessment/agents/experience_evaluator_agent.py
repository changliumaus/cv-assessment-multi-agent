"""Experience Evaluator Agent - Evaluates work experience relevance."""

import logging

from cv_assessment.agents.base_agent import BaseAgent
from cv_assessment.models.schemas import CVData, ExperienceEvaluation, JobDescription

logger = logging.getLogger(__name__)

EXPERIENCE_EVALUATOR_PROMPT = """You are an expert at evaluating work experience relevance for job positions.

Your task is to:
1. Calculate total years of professional experience
2. Identify relevant experience for the target role
3. Assess experience level (junior/mid/senior/lead)
4. Identify key responsibilities and impact that align with the role
5. Provide an experience match score (0.0-1.0)

**Evaluation Criteria:**
- **Required Experience Match (70% weight)**:
  - Does the candidate meet the years of DIRECTLY RELEVANT experience requirement?
  - Do their actual job titles/positions match the required experience types?
  - Do their responsibilities demonstrate the required competencies?
  - Does their industry/domain experience match requirements?
  - Count only experience that directly aligns with the target role

- **Preferred Experience Match (15% weight)**:
  - Does the candidate have any of the nice-to-have experience?
  - How much additional value do they bring beyond requirements?

- **Experience Quality (15% weight)**:
  - Relevance of previous roles to target position
  - Relevance of previous responsibilities to current role responsibilities
  - Scope of responsibilities and impact
  - Progression and growth in relevant areas


Provide detailed analysis of how experience aligns with job requirements, explicitly noting any missing required experience."""


class ExperienceEvaluatorAgent(BaseAgent):
    """Agent for evaluating work experience."""

    def __init__(self, **llm_kwargs):
        """Initialize the Experience Evaluator agent."""
        super().__init__(
            name="Experience Evaluator",
            system_prompt=EXPERIENCE_EVALUATOR_PROMPT,
            **llm_kwargs,
        )

    def evaluate_experience(
        self, cv_data: CVData, job_description: JobDescription
    ) -> ExperienceEvaluation:
        """
        Evaluate candidate's work experience.

        Args:
            cv_data: Structured CV data
            job_description: Structured job description

        Returns:
            Experience evaluation results
        """
        logger.info("Evaluating candidate experience")

        prompt = f"""Evaluate the candidate's work experience for the target role:

Target Role: {job_description.job_title}

Candidate Work Experience:
{self._format_experience(cv_data)}

Job Requirements & Responsibilities:
{self._format_job_context(job_description)}

**EVALUATION INSTRUCTIONS:**
Apply the evaluation criteria and scoring framework defined in the system prompt above.

**CRITICAL: Role Matching Guidelines**
- DO NOT infer or assume role equivalence between different job titles or domains
- Only count experience as relevant if the job title, responsibilities, and domain match the target role

**CRITICAL SCORING GUIDANCE:**
- REQUIRED EXPERIENCE is mandatory - Missing or insufficient required experience should result in a LOW score (0.5 or below)
- PREFERRED EXPERIENCE is a bonus - Missing preferred experience should have minimal impact on the score
- Candidates who meet all required experience should score 0.7+
- Candidates with both required and preferred experience should score 0.8+

**In your analysis, explicitly state:**
- Which required experiences are MET ✓
- Which required experiences are MISSING ✗
- Which preferred experiences are present (bonus points)
- Final justification for the score based on required experience gaps"""

        result = self.invoke_structured(prompt, ExperienceEvaluation)
        token_count = self.llm.get_num_tokens(prompt)
        logger.info(f"Experience Evaluation  prompt tokens: {token_count}")
        logger.debug(f"Experience Evaluation prompt: {prompt}")
        logger.info(
            f"Experience evaluation: {result.experience_level}, score: {result.experience_score:.2f}"
        )
        return result

    def _format_experience(self, cv_data: CVData) -> str:
        """Format work experience for prompt."""
        if not cv_data.work_experience:
            return "No work experience listed"

        formatted = []
        for exp in cv_data.work_experience:
            duration = (
                f"{exp.duration_months} months"
                if exp.duration_months
                else f"{exp.start_date} - {exp.end_date or 'Present'}"
            )
            formatted.append(f"\n{exp.position} at {exp.company} ({duration})")

            if exp.responsibilities:
                formatted.append("  Responsibilities:")
                for resp in exp.responsibilities[:3]:
                    formatted.append(f"  - {resp}")

        return "\n".join(formatted)

    def _format_job_context(self, job_description: JobDescription) -> str:
        """Format job context for prompt."""
        sections = []

        # Responsibilities
        if job_description.responsibilities:
            sections.append("RESPONSIBILITIES:")
            for resp in job_description.responsibilities[:5]:
                sections.append(f"  - {resp}")

        # Required Experience
        if job_description.necessary_experince:
            sections.append("\nREQUIRED EXPERIENCE:")
            for exp in job_description.necessary_experince:
                sections.append(f"  - {exp}")

        # Preferred Experience
        if job_description.nice_to_have_experience:
            sections.append("\nPREFERRED EXPERIENCE:")
            for exp in job_description.nice_to_have_experience:
                sections.append(f"  - {exp}")

        

        return "\n".join(sections) if sections else "No job context available"
