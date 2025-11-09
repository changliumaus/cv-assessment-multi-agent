"""LangGraph workflow for CV assessment."""

import logging
from typing import Any

from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict

from cv_assessment.agents import (
    CultureFitAgent,
    CVParserAgent,
    ExperienceEvaluatorAgent,
    FinalScorerAgent,
    JobAnalyzerAgent,
    SkillsMatcherAgent,
)
from cv_assessment.models.schemas import AssessmentResult
from cv_assessment.utils.document_parser import parse_document

logger = logging.getLogger(__name__)


class WorkflowState(TypedDict):
    """State dictionary for LangGraph workflow."""

    cv_file_path: str | None
    job_description_path: str | None
    cv_text: str | None
    job_text: str | None
    cv_data: Any
    job_description: Any
    skill_match: Any
    experience_evaluation: Any
    culture_fit: Any
    assessment_result: Any


class CVAssessmentWorkflow:
    """LangGraph workflow for CV assessment."""

    def __init__(self, **llm_kwargs: Any):
        """
        Initialize the workflow with all agents.

        Args:
            **llm_kwargs: Additional arguments for LLM creation
        """
        self.cv_parser = CVParserAgent(**llm_kwargs)
        self.job_analyzer = JobAnalyzerAgent(**llm_kwargs)
        self.skills_matcher = SkillsMatcherAgent(**llm_kwargs)
        self.experience_evaluator = ExperienceEvaluatorAgent(**llm_kwargs)
        self.culture_fit = CultureFitAgent(**llm_kwargs)
        self.final_scorer = FinalScorerAgent(**llm_kwargs)

        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow with parallel execution."""
        workflow = StateGraph(WorkflowState)

        # Add nodes
        workflow.add_node("load_documents", self._load_documents)
        workflow.add_node("parse_cv", self._parse_cv)
        workflow.add_node("analyze_job", self._analyze_job)
        workflow.add_node("match_skills", self._match_skills)
        workflow.add_node("evaluate_experience", self._evaluate_experience)
        workflow.add_node("assess_culture_fit", self._assess_culture_fit)
        workflow.add_node("create_final_assessment", self._create_final_assessment)

        # Define workflow edges with parallel execution
        workflow.set_entry_point("load_documents")

        # After loading documents, parse CV and analyze job in parallel
        workflow.add_edge("load_documents", "parse_cv")
        workflow.add_edge("load_documents", "analyze_job")

        # After both CV parsing and job analysis complete, run all three evaluation agents in parallel
        workflow.add_edge("parse_cv", "match_skills")
        workflow.add_edge("parse_cv", "evaluate_experience")
        workflow.add_edge("parse_cv", "assess_culture_fit")
        workflow.add_edge("analyze_job", "match_skills")
        workflow.add_edge("analyze_job", "evaluate_experience")
        workflow.add_edge("analyze_job", "assess_culture_fit")

        # After all three evaluations complete, create final assessment
        workflow.add_edge("match_skills", "create_final_assessment")
        workflow.add_edge("evaluate_experience", "create_final_assessment")
        workflow.add_edge("assess_culture_fit", "create_final_assessment")
        workflow.add_edge("create_final_assessment", END)

        return workflow.compile()

    def _load_documents(self, state: WorkflowState) -> dict:
        """Load and parse document files."""
        logger.info("Loading documents")
        try:
            updates = {}

            if state["cv_file_path"]:
                cv_text = parse_document(state["cv_file_path"])
                logger.info(f"Loaded CV: {len(cv_text)} characters")
                updates["cv_text"] = cv_text

            if state["job_description_path"]:
                job_text = parse_document(state["job_description_path"])
                logger.info(f"Loaded job description: {len(job_text)} characters")
                updates["job_text"] = job_text

            return updates

        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            raise

    def _parse_cv(self, state: WorkflowState) -> dict:
        """Parse CV into structured data."""
        logger.info("Parsing CV")
        try:
            cv_text = state.get("cv_text")
            if not cv_text:
                raise ValueError("No CV text available")

            cv_data = self.cv_parser.parse_cv(cv_text)
            logger.info("CV parsing complete")
            return {"cv_data": cv_data}

        except Exception as e:
            logger.error(f"Error parsing CV: {e}")
            raise


    def _analyze_job(self, state: WorkflowState) -> dict:
        """Analyze job description."""
        logger.info("Analyzing job description")
        try:
            job_text = state.get("job_text")
            if not job_text:
                raise ValueError("No job description text available")

            job_description = self.job_analyzer.analyze_job(job_text)
            logger.info("Job analysis complete")
            return {"job_description": job_description}

        except Exception as e:
            logger.error(f"Error analyzing job: {e}")
            raise


    def _match_skills(self, state: WorkflowState) -> dict:
        """Match candidate skills to job requirements."""
        logger.info("Matching skills")
        try:
            cv_data = state.get("cv_data")
            job_description = state.get("job_description")

            if not cv_data or not job_description:
                raise ValueError("CV data or job description not available")

            skill_match = self.skills_matcher.match_skills(
                cv_data, job_description
            )
            logger.info("Skills matching complete")
            return {"skill_match": skill_match}

        except Exception as e:
            logger.error(f"Error matching skills: {e}")
            raise


    def _evaluate_experience(self, state: WorkflowState) -> dict:
        """Evaluate candidate experience."""
        logger.info("Evaluating experience")
        try:
            cv_data = state.get("cv_data")
            job_description = state.get("job_description")

            if not cv_data or not job_description:
                raise ValueError("CV data or job description not available")

            experience_evaluation = self.experience_evaluator.evaluate_experience(
                cv_data, job_description
            )
            logger.info("Experience evaluation complete")
            return {"experience_evaluation": experience_evaluation}

        except Exception as e:
            logger.error(f"Error evaluating experience: {e}")
            raise


    def _assess_culture_fit(self, state: WorkflowState) -> dict:
        """Assess culture fit."""
        logger.info("Assessing culture fit")
        try:
            cv_data = state.get("cv_data")
            job_description = state.get("job_description")

            if not cv_data or not job_description:
                raise ValueError("CV data or job description not available")

            culture_fit = self.culture_fit.assess_culture_fit(
                cv_data, job_description
            )
            logger.info("Culture fit assessment complete")
            return {"culture_fit": culture_fit}

        except Exception as e:
            logger.error(f"Error assessing culture fit: {e}")
            raise


    def _create_final_assessment(self, state: WorkflowState) -> dict:
        """Create final assessment."""
        logger.info("Creating final assessment")
        try:
            cv_data = state.get("cv_data")
            job_description = state.get("job_description")
            skill_match = state.get("skill_match")
            experience_eval = state.get("experience_evaluation")
            culture_fit = state.get("culture_fit")

            if not all([cv_data, job_description, skill_match, experience_eval, culture_fit]):
                raise ValueError("Not all assessment components available")

            assessment_result = self.final_scorer.create_final_assessment(
                cv_data, job_description, skill_match, experience_eval, culture_fit
            )
            logger.info("Final assessment complete")
            return {"assessment_result": assessment_result}

        except Exception as e:
            logger.error(f"Error creating final assessment: {e}")
            raise


    def run(
        self, cv_file_path: str, job_description_path: str
    ) -> AssessmentResult | None:
        """
        Run the complete assessment workflow.

        Args:
            cv_file_path: Path to CV file
            job_description_path: Path to job description file

        Returns:
            Final assessment result or None if errors occurred
        """
        logger.info("Starting CV assessment workflow")

        initial_state: WorkflowState = {
            "cv_file_path": cv_file_path,
            "job_description_path": job_description_path,
            "cv_text": None,
            "job_text": None,
            "cv_data": None,
            "job_description": None,
            "skill_match": None,
            "experience_evaluation": None,
            "culture_fit": None,
            "assessment_result": None,
        }

        try:
            final_state = self.workflow.invoke(initial_state)
            return final_state.get("assessment_result")

        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return None
