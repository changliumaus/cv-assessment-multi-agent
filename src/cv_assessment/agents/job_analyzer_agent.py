"""Job Analyzer Agent - Analyzes and structures job descriptions."""

import logging

from cv_assessment.agents.base_agent import BaseAgent
from cv_assessment.models.schemas import JobDescription

logger = logging.getLogger(__name__)

JOB_ANALYZER_PROMPT = """You are an expert job description analyst. Your task is to parse and structure job descriptions.

Extract the following information and categorize carefully:

1. **Basic Information**: Job title, company, desciption, department, location, employment type, salary range

2. **Necessary Experience** (required/must-have experience):
   - Work experience explicitly stated as required, mandatory, or must-have
   - Years of experience in specific roles or domains
   - Industry-specific experience requirements

3. **Necessary Skills** (required/must-have skills):
   - Technical skills explicitly stated as required, mandatory, or must-have
   - Programming languages, tools, frameworks that are critical
   - specify years of skills required if mentioned
   - Certifications or technical competencies marked as required

4. **Nice-to-Have Experience** (preferred/bonus experience):
   - Experience marked as preferred, desired, bonus, or nice-to-have
   - Experience preceded or followed by words like 'ideally', 'preferably', 'optimally'
   - Additional experience that would be beneficial but not required
   - Example: "4+ years experience, ideally in AI" → "4+ years experience" is NECESSARY, "in AI" is NICE-TO-HAVE

5. **Nice-to-Have Skills** (preferred/bonus skills):
   - Skills marked as preferred, desired, bonus, or nice-to-have
   - Skills preceded or followed by words like 'ideally', 'preferably', 'optimally'
   - Additional technical competencies that are beneficial but not required
   - Example: "Proficiency in Python, ideally Django" → "Python" is NECESSARY, "Django" is NICE-TO-HAVE

6. **Responsibilities**: Day-to-day duties and job functions

7. **Education**: Educational requirements, certifications, degrees

8. **Leadership Requirements**: Extract leadership and mentoring expectations for this role:
   - Team leadership responsibilities (e.g., "lead a team of engineers", "manage direct reports")
   - Mentoring and coaching duties (e.g., "mentor junior developers", "provide technical guidance")
   - Project or technical leadership (e.g., "drive architecture decisions", "lead technical initiatives")
   - Cross-team leadership (e.g., "coordinate across teams", "influence stakeholders")

   **Important**: Only include requirements FOR this role, NOT benefits the candidate would receive (e.g., exclude "opportunity to grow leadership skills" or "mentorship from senior staff")

9. **Soft Skills Requirements**: Extract required interpersonal and professional competencies:
   - Communication skills (e.g., "excellent written and verbal communication", "present to stakeholders")
   - Collaboration abilities (e.g., "work cross-functionally", "partner with product teams")
   - Problem-solving approach (e.g., "analytical thinking", "systematic debugging")
   - Ownership and initiative (e.g., "take ownership", "self-starter", "proactive")
   - Adaptability (e.g., "thrive in fast-paced environment", "comfortable with ambiguity")
   - Learning mindset (e.g., "continuous learner", "stay current with technologies")

   **Important**: Extract only what the role REQUIRES from candidates, NOT what the company offers (e.g., exclude "opportunities to learn" or "collaborative team environment")


**Categorization Guidelines**:
- If the job posting uses words like "required", "must have", "essential", "mandatory", categorize as necessary
- If it uses "preferred", "nice to have", "bonus", "a plus", "ideally", "preferably", "optimally", categorize as nice-to-have
- **CRITICAL: When "ideally" appears mid-sentence**, split the requirement:
  - Part BEFORE "ideally" = NECESSARY (e.g., "5 years experience")
  - Part AFTER "ideally" = NICE-TO-HAVE (e.g., "in machine learning")
  - Example: "5+ years in software development, ideally with Python"
    → Necessary: "5+ years in software development"
    → Nice-to-have: "Experience with Python"
- If unclear, consider context: items in "minimum requirements" sections are necessary
- When listing skills, extract specific technologies, languages, frameworks, and tools
- When listing experience, extract specific role types, industries, or domains

Be thorough in identifying both explicit and implicit requirements.
Be careful to distinguish ones are requried vs benefit from joining the role."""


class JobAnalyzerAgent(BaseAgent):
    """Agent for analyzing job descriptions."""

    def __init__(self, **llm_kwargs):
        """Initialize the Job Analyzer agent."""
        super().__init__(
            name="Job Analyzer",
            system_prompt=JOB_ANALYZER_PROMPT,
            **llm_kwargs,
        )

    def analyze_job(self, job_text: str) -> JobDescription:
        """
        Analyze job description text into structured data.

        Args:
            job_text: Raw job description text

        Returns:
            Structured job description
        """
        logger.info("Analyzing job description")

        prompt = f"""Please analyze the following job description and extract all information according to the guidelines provided.

Job Description:
{job_text}



- Look at section headers for additional context.
- Extract all information into the structured format."""

        job_description = self.invoke_structured(prompt, JobDescription)

        logger.info(f"Successfully analyzed job: {job_description.job_title}")
        return job_description
