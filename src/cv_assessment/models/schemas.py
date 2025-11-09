"""Data models and schemas for CV assessment."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Skill(BaseModel):
    """Skill information."""

    name: str
    skill_level: str | None = None  # e.g., "beginner", "intermediate", "advanced", "expert"
    years_experience: float | None = None
    category: str | None = None  # e.g., "programming", "soft_skill", "domain"


class WorkExperience(BaseModel):
    """Work experience entry."""

    company: str
    position: str
    start_date: str | None = None
    end_date: str | None = None
    duration_months: int | None = None
    responsibilities: list[str] = Field(default_factory=list)


class Education(BaseModel):
    """Education entry."""

    institution: str
    degree: str
    field_of_study: str | None = None
    graduation_year: int | None = None
    gpa: float | None = None


class CVData(BaseModel):
    """Structured CV data."""

    candidate_name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    summary: str | None = None
    skills: list[Skill] = Field(default_factory=list)
    work_experience: list[WorkExperience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)


class JobDescription(BaseModel):
    """Structured job description."""

    job_title: str
    company: str | None = None
    department: str | None = None
    location: str | None = None
    necessary_experince: list[str] = Field(default_factory=list)
    necessary_skills: list[Skill] = Field(default_factory=list)
    nice_to_have_experience: list[str] = Field(default_factory=list)
    nice_to_have_skills: list[Skill] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    leadership: list[str] = Field(default_factory=list)
    soft_skills_requirement: list[str] = Field(default_factory=list)
    salary_range: str | None = None


class SkillMatchResult(BaseModel):
    """Result of skill matching analysis."""

    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    partial_matches: list[str] = Field(default_factory=list)
    skill_gap_analysis: str
    match_score: float = Field(ge=0.0, le=1.0)


class ExperienceEvaluation(BaseModel):
    """Result of experience evaluation."""

    total_years_experience: float
    relevant_years_experience: float
    relevant_roles: list[str] = Field(default_factory=list)
    experience_level: str  # e.g., "junior", "mid", "senior", "lead"
    key_achievements: list[str] = Field(default_factory=list)
    experience_score: float = Field(ge=0.0, le=1.0)
    analysis: str


class CultureFitAssessment(BaseModel):
    """Result of culture fit assessment."""

    soft_skills_identified: list[str] = Field(default_factory=list)
    leadership_indicators: list[str] = Field(default_factory=list)
    culture_fit_score: float = Field(ge=0.0, le=1.0)
    notes: str


class AssessmentResult(BaseModel):
    """Final assessment result."""

    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    cv_data: CVData
    job_description: JobDescription
    skill_match: SkillMatchResult
    experience_evaluation: ExperienceEvaluation
    culture_fit: CultureFitAssessment
    overall_score: float = Field(ge=0.0, le=1.0)
    recommendation: str  # e.g., "strong_match", "good_match", "weak_match", "no_match"
    strengths: list[str] = Field(default_factory=list)
    concerns: list[str] = Field(default_factory=list)
    summary: str
    timestamp: datetime = Field(default_factory=datetime.now)


