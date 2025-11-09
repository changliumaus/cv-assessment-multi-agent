"""Final Scorer Agent - Aggregates results and provides final recommendation."""

import logging
from datetime import datetime

from pydantic import BaseModel

from cv_assessment.agents.base_agent import BaseAgent
from cv_assessment.models.schemas import (
    AssessmentResult,
    CultureFitAssessment,
    CVData,
    ExperienceEvaluation,
    JobDescription,
    SkillMatchResult,
)

logger = logging.getLogger(__name__)

FINAL_SCORER_PROMPT = """You are an expert hiring manager making final candidate assessments.

Your task is to:
1. Review all assessment components (skills, experience, culture fit)
2. Calculate an overall match score (0.0-1.0)
3. Provide a clear recommendation (strong_match/good_match/weak_match/no_match)
4. Identify key strengths and concerns
5. Write an executive summary

Scoring weights (suggested):
- Skills match: 40%
- Experience: 40%
- Culture fit: 20%

Recommendations:
- strong_match (0.8-1.0): Highly qualified, proceed to interview
- good_match (0.6-0.79): Qualified with some gaps, interview recommended
- weak_match (0.4-0.59): Significant gaps, interview only if no better candidates
- no_match (0.0-0.39): Not qualified for this role

Provide actionable insights and be objective."""


class FinalScorerAgent(BaseAgent):
    """Agent for final assessment and recommendations."""

    def __init__(self, **llm_kwargs):
        """Initialize the Final Scorer agent."""
        super().__init__(
            name="Final Scorer",
            system_prompt=FINAL_SCORER_PROMPT,
            **llm_kwargs,
        )

    def create_final_assessment(
        self,
        cv_data: CVData,
        job_description: JobDescription,
        skill_match: SkillMatchResult,
        experience_eval: ExperienceEvaluation,
        culture_fit: CultureFitAssessment,
    ) -> AssessmentResult:
        """
        Create final assessment and recommendation.

        Args:
            cv_data: Structured CV data
            job_description: Structured job description
            skill_match: Skills matching results
            experience_eval: Experience evaluation
            culture_fit: Culture fit assessment

        Returns:
            Final assessment result
        """
        logger.info("Creating final assessment")

        prompt = f"""Create a final assessment for this candidate:

Candidate: {cv_data.candidate_name}
Position: {job_description.job_title}

Assessment Components:

1. SKILLS MATCH (Score: {skill_match.match_score:.2f})
   Matched: {', '.join(skill_match.matched_skills[:10])}
   Missing: {', '.join(skill_match.missing_skills[:10])}
   Analysis: {skill_match.skill_gap_analysis[:200]}...

2. EXPERIENCE (Score: {experience_eval.experience_score:.2f})
   Level: {experience_eval.experience_level}
   Relevant Experience: {experience_eval.relevant_years_experience} years
   Analysis: {experience_eval.analysis[:200]}...

3. CULTURE FIT (Score: {culture_fit.culture_fit_score:.2f})
   Soft Skills: {', '.join(culture_fit.soft_skills_identified[:10])}
   Notes: {culture_fit.notes[:200]}...

Provide final assessment with overall score, recommendation, strengths, concerns, and executive summary."""

        # Calculate overall score with weights
        overall_score = (
            skill_match.match_score * 0.4
            + experience_eval.experience_score * 0.4
            + culture_fit.culture_fit_score * 0.2
        )

        # Get structured assessment details
        assessment_prompt = f"""{prompt}

Based on the overall score of {overall_score:.2f}, provide:
- Recommendation level (strong_match/good_match/weak_match/no_match)
- 3-5 key strengths
- 3-5 key concerns or areas to probe
- Executive summary (2-3 paragraphs)

Format the response as a structured assessment."""

        class AssessmentDetails(BaseModel):
            recommendation: str
            strengths: list[str]
            concerns: list[str]
            summary: str

        token_count = self.llm.get_num_tokens(prompt)
        logger.info(f"Final scorer prompt tokens: {token_count}")

        details = self.invoke_structured(assessment_prompt, AssessmentDetails)

        # Use model_construct to bypass validation since we already have validated instances
        result = AssessmentResult.model_construct(
            cv_data=cv_data,
            job_description=job_description,
            skill_match=skill_match,
            experience_evaluation=experience_eval,
            culture_fit=culture_fit,
            overall_score=overall_score,
            recommendation=details.recommendation,
            strengths=details.strengths,
            concerns=details.concerns,
            summary=details.summary,
            timestamp=datetime.now(),
        )

        logger.info(
            f"Final assessment complete: {result.recommendation} (score: {overall_score:.2f})"
        )
        return result
