"""Culture Fit Agent - Assesses soft skills and cultural alignment."""

import logging

from cv_assessment.agents.base_agent import BaseAgent
from cv_assessment.models.schemas import CultureFitAssessment, CVData, JobDescription

logger = logging.getLogger(__name__)

CULTURE_FIT_PROMPT = """You are an expert at assessing cultural fit and soft skills from CV information.

**IMPORTANT: Definition of Soft Skills**
Soft skills are interpersonal and professional attributes, NOT technical skills or domain knowledge.

**Examples of SOFT SKILLS (what to identify):**
- Communication 
- Collaboration 
- Problem-solving approach 
- Initiative and ownership 
- Adaptability
- Learning mindset 
- Interpersonal skills 

**Examples of TECHNICAL SKILLS (DO NOT include in soft skills):**
- Programming languages (Python, Java, JavaScript, etc.)
- Technical domains (full-stack development, machine learning, database optimization)
- Tools and frameworks (React, Django, Kubernetes, etc.)
- Technical activities (API development, code review, system design)

Your task is to:
1. Identify SOFT SKILLS (interpersonal/professional attributes) demonstrated in the CV
2. Assess leadership capabilities and match against leadership requirements
3. Evaluate collaboration and teamwork indicators
4. Assess communication quality (from CV writing and responsibility descriptions)
5. Provide a culture fit score (0.0-1.0)

**Evaluation Criteria:**
- **Leadership Match (40% weight)**:
  - Does leadership requirement align with candidate's experience?
  - Identify candidate's leadership experience from their work history (leading teams, mentoring, project leadership)
  - Compare against job's leadership requirements

- **Soft Skills & Cultural Fit (60% weight)**:
  - Communication skills (written clarity, presentation experience, explaining to stakeholders)
  - Collaboration abilities (cross-functional work, partnering with product/design teams)
  - Problem-solving approach (analytical thinking, systematic approach)
  - Initiative and ownership (self-starter, proactive, taking ownership)
  - Adaptability (fast-paced environment, handling ambiguity, learning new domains)
  - Learning mindset (continuous learning, staying current, professional development)
  - Team collaboration evidence (working with diverse teams, remote collaboration)
  - Community involvement (open source contributions, conference speaking, mentoring others)

Base your assessment on concrete evidence from the CV, not assumptions.
Focus on HOW they work (soft skills), not WHAT technologies they use (technical skills)."""


class CultureFitAgent(BaseAgent):
    """Agent for assessing culture fit and soft skills."""

    def __init__(self, **llm_kwargs):
        """Initialize the Culture Fit agent."""
        super().__init__(
            name="Culture Fit Assessor",
            system_prompt=CULTURE_FIT_PROMPT,
            **llm_kwargs,
        )

    def assess_culture_fit(
        self, cv_data: CVData, job_description: JobDescription
    ) -> CultureFitAssessment:
        """
        Assess candidate's cultural fit.

        Args:
            cv_data: Structured CV data
            job_description: Structured job description

        Returns:
            Culture fit assessment
        """
        logger.info("Assessing culture fit and soft skills")

        # Format job requirements
        leadership_reqs = "\n".join([f"  - {lead}" for lead in job_description.leadership]) if job_description.leadership else "None - This is an individual contributor role"
        soft_skills_reqs = "\n".join([f"  - {skill}" for skill in job_description.soft_skills_requirement]) if job_description.soft_skills_requirement else "Not specified"
        responsibilities = "\n".join([f"  - {resp}" for resp in job_description.responsibilities]) if job_description.responsibilities else "Not specified"

        prompt = f"""Assess the candidate's cultural fit for the role:

CANDIDATE PROFILE:
Name: {cv_data.candidate_name}
Summary: {cv_data.summary or 'Not provided'}

CANDIDATE WORK EXPERIENCE:
{self._format_experience(cv_data)}

CANDIDATE ADDITIONAL INFORMATION:
- Certifications: {', '.join(cv_data.certifications) if cv_data.certifications else 'None'}
- Languages: {', '.join(cv_data.languages) if cv_data.languages else 'None'}

TARGET ROLE: {job_description.job_title}
Company: {job_description.company or 'Not specified'}

JOB RESPONSIBILITIES:
{responsibilities}

JOB LEADERSHIP REQUIREMENTS:
{leadership_reqs}

JOB SOFT SKILLS REQUIREMENTS:
{soft_skills_reqs}

**ASSESSMENT INSTRUCTIONS:**
Apply the assessment criteria and scoring rules defined in the system prompt above.

**CRITICAL SCORING GUIDANCE:**
- **If job REQUIRES leadership** AND **candidate HAS leadership experience** → HIGH score (0.8-1.0)
- **If job REQUIRES leadership** BUT **candidate LACKS leadership experience** → LOW score (0.3-0.5)
- **If job DOES NOT require leadership** → NEUTRAL (no penalty)

- Compare candidate's demonstrated soft skills against job's required soft skills
- Match each required soft skill - missing critical soft skills should lower the score
- Look for concrete evidence in CV, not assumptions

**In your assessment, explicitly state:**
- Leadership match: Does it align? ✓ or misaligned? ✗
- Which soft skills are demonstrated ✓ and which are missing ✗
- Final score justification based on leadership and soft skills alignment"""

        result = self.invoke_structured(prompt, CultureFitAssessment)

        logger.info(f"Culture fit score: {result.culture_fit_score:.2f}")
        return result

    def _format_experience(self, cv_data: CVData) -> str:
        """Format work experience highlighting soft skills indicators."""
        if not cv_data.work_experience:
            return "No work experience listed"

        formatted = []
        for exp in cv_data.work_experience[:3]:
            formatted.append(f"\n{exp.position} at {exp.company}")

            if exp.responsibilities:
                formatted.append("  Key responsibilities:")
                for resp in exp.responsibilities[:3]:
                    formatted.append(f"  - {resp}")

        return "\n".join(formatted)
