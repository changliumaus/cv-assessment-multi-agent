"""Skills Matcher Agent - Matches candidate skills to job requirements."""

import logging

from cv_assessment.agents.base_agent import BaseAgent
from cv_assessment.models.schemas import CVData, JobDescription, SkillMatchResult

logger = logging.getLogger(__name__)

SKILLS_MATCHER_PROMPT = """You are an expert at matching candidate skills and qualifications to job requirements.

Your task is to:
1. Verify candidate meets required education qualifications
2. Identify which required skills the candidate possesses
3. Identify missing critical skills and qualifications
4. Identify partial matches (related/transferable skills)
5. Provide a skill gap analysis
6. Calculate an overall skill match score (0.0-1.0)

**Evaluation Criteria:**
- **Education Match (10% weight)**:
  - Does candidate's degree level meet requirements (Bachelor's, Master's, PhD)?
  - Does field of study align with job requirements?
  - Does candidate have required certifications or licenses?
  - Consider degree equivalency (PhD > Master's > Bachelor's in same field)
  - Education requirements are often hard requirements that cannot be substituted

- **Required Skills Match (70% weight)**:
  - Exact skill matches
  - Years of experience with each skill
  - Skill proficiency level
  - Similar or equivalent skills (e.g., React vs Vue, Python vs Ruby)
  - Transferable skills

- **Preferred Skills Match (20% weight)**:
  - Nice-to-have skills that add value
  - Bonus points for additional capabilities

Be objective and thorough in your analysis."""


class SkillsMatcherAgent(BaseAgent):
    """Agent for matching candidate skills to job requirements."""

    def __init__(self, **llm_kwargs):
        """Initialize the Skills Matcher agent."""
        super().__init__(
            name="Skills Matcher",
            system_prompt=SKILLS_MATCHER_PROMPT,
            **llm_kwargs,
        )

    def match_skills(
        self, cv_data: CVData, job_description: JobDescription
    ) -> SkillMatchResult:
        """
        Match candidate skills to job requirements.

        Args:
            cv_data: Structured CV data
            job_description: Structured job description

        Returns:
            Skill matching results
        """
        logger.info("Matching candidate skills to job requirements")

        # Format candidate skills with details
        candidate_skills_formatted = []
        for skill in cv_data.skills:
            skill_str = skill.name
            if skill.years_experience:
                skill_str += f" ({skill.years_experience} years)"
            if skill.skill_level:
                skill_str += f" [{skill.skill_level}]"
            candidate_skills_formatted.append(skill_str)

        # Format candidate education
        candidate_education_formatted = []
        for edu in cv_data.education:
            edu_str = f"{edu.degree}"
            if edu.field_of_study:
                edu_str += f" in {edu.field_of_study}"
            if edu.institution:
                edu_str += f" from {edu.institution}"
            if edu.graduation_year:
                edu_str += f" ({edu.graduation_year})"
            candidate_education_formatted.append(edu_str)

        prompt = f"""Analyze the match between candidate qualifications/skills and job requirements:

CANDIDATE EDUCATION:
{chr(10).join(['  - ' + edu for edu in candidate_education_formatted]) if candidate_education_formatted else 'None listed'}

CANDIDATE SKILLS:
{', '.join(candidate_skills_formatted) if candidate_skills_formatted else 'None listed'}

CANDIDATE WORK EXPERIENCE:
{self._format_experience(cv_data)}

JOB REQUIREMENTS:
{self._format_requirements(job_description)}

**EVALUATION INSTRUCTIONS:**
Apply the evaluation criteria and scoring framework defined in the system prompt above.

**CRITICAL SCORING GUIDANCE:**
- REQUIRED EDUCATION is mandatory - Missing required education should result in a LOW score (0.3-0.5)
- Candidates who meet education + all required skills should score 0.8+
- Candidates with education + required + preferred skills should score 0.9+
- REQUIRED SKILLS are critical - Missing required skills significantly penalize score
The penalty should be proportional to the percentage of missing required skills calculated as (number of missing required skills / total number of required skills).
For example, if a candidate misses half of the required skills, the score should be below 0.5
If a candidate misses 1/3 of the required skills, the score should be below 0.6
- PREFERRED SKILLS are bonus - Missing preferred skills should have minimal impact


**In your analysis, explicitly state:**
- Which education requirements are MET ✓ and which are MISSING ✗
- Which required skills are MET ✓ and which are MISSING ✗
- Which preferred skills are present (bonus points)
- Final justification for the score based on education and skill gaps"""

        # Count and log token usage
        token_count = self.llm.get_num_tokens(prompt)
        logger.info(f"Skill match prompt tokens: {token_count}")
        logger.debug(f"Skill match prompt: {prompt}")

        result = self.invoke_structured(prompt, SkillMatchResult)

        logger.info(f"Skill match score: {result.match_score:.2f}")
        return result

    def _format_experience(self, cv_data: CVData) -> str:
        """Format work experience for prompt."""
        if not cv_data.work_experience:
            return "No work experience listed"

        formatted = []
        for exp in cv_data.work_experience[:5]:  # Top 5 most recent
            exp_str = f"- {exp.position} at {exp.company}"

            # Add duration if available
            if exp.duration_months:
                years = exp.duration_months / 12
                if years >= 1:
                    exp_str += f" ({years:.1f} years)"
                else:
                    exp_str += f" ({exp.duration_months} months)"
            elif exp.start_date and exp.end_date:
                exp_str += f" ({exp.start_date} - {exp.end_date})"

            formatted.append(exp_str)

            # Add key responsibilities (max 3)
            if exp.responsibilities:
                for resp in exp.responsibilities[:3]:
                    formatted.append(f"    • {resp}")

        return "\n".join(formatted)

    def _format_requirements(self, job_description: JobDescription) -> str:
        """Format job requirements for prompt."""
        sections = []

        # Necessary Skills (Required)
        if job_description.necessary_skills:
            sections.append("REQUIRED SKILLS:")
            for skill in job_description.necessary_skills:
                skill_info = f"  - {skill.name}"
                if skill.years_experience:
                    skill_info += f" ({skill.years_experience}+ years)"
                if skill.skill_level:
                    skill_info += f" [{skill.skill_level}]"
                sections.append(skill_info)

        # Nice-to-Have Skills (Preferred)
        if job_description.nice_to_have_skills:
            sections.append("\nPREFERRED SKILLS:")
            for skill in job_description.nice_to_have_skills:
                skill_info = f"  - {skill.name}"
                if skill.years_experience:
                    skill_info += f" ({skill.years_experience}+ years)"
                if skill.skill_level:
                    skill_info += f" [{skill.skill_level}]"
                sections.append(skill_info)

        # Education
        if job_description.education:
            sections.append("\nEDUCATION:")
            for edu in job_description.education:
                sections.append(f"  - {edu}")


        return "\n".join(sections) if sections else "No specific requirements listed"
