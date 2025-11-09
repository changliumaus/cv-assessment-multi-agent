"""Example script to run CV assessment."""

import argparse
import json
import logging
from pathlib import Path

from cv_assessment.workflows.assessment_workflow import CVAssessmentWorkflow

# Configure logging to see agent activity
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detailed output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    """Run example CV assessment."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run CV assessment on a candidate CV against a job description.')
    parser.add_argument(
        '--cv',
        type=str,
        help='Path to the CV file (default: examples/sample_cv_data_scientist.txt)'
    )
    parser.add_argument(
        '--job',
        type=str,
        help='Path to the job description file (default: examples/Senior_Data_Scientist.txt)'
    )
    args = parser.parse_args()

    # Get file paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    examples_dir = project_root / "examples"

    if args.cv:
        cv_path = Path(args.cv)
    else:
        cv_path = examples_dir / "sample_cv_data_scientist.txt"

    if args.job:
        job_path = Path(args.job)
    else:
        job_path = examples_dir / "Senior_Data_Scientist.txt"

    # Validate files exist
    if not cv_path.exists():
        print(f"[ERROR] CV file not found: {cv_path}")
        return

    if not job_path.exists():
        print(f"[ERROR] Job description file not found: {job_path}")
        return

    print("=" * 80)
    print("CV ASSESSMENT EXAMPLE")
    print("=" * 80)
    print(f"\nCV Path: {cv_path}")
    print(f"Job Path: {job_path}")
    print("\nStarting assessment...\n")

    # Create workflow and run assessment
    workflow = CVAssessmentWorkflow()
    result = workflow.run(str(cv_path), str(job_path))

    if result:
        print("\n" + "=" * 80)
        print("DETAILED AGENT ANALYSIS")
        print("=" * 80)

        # Skills Match Analysis
        print("\n--- 1. SKILLS MATCH ANALYSIS ---")
        print(f"Score: {result.skill_match.match_score:.2%}")
        print(f"\nMatched Skills ({len(result.skill_match.matched_skills)}):")
        for skill in result.skill_match.matched_skills[:10]:
            print(f"  ✓ {skill}")
        if len(result.skill_match.matched_skills) > 10:
            print(f"  ... and {len(result.skill_match.matched_skills) - 10} more")

        print(f"\nMissing Skills ({len(result.skill_match.missing_skills)}):")
        for skill in result.skill_match.missing_skills[:10]:
            print(f"  ✗ {skill}")
        if len(result.skill_match.missing_skills) > 10:
            print(f"  ... and {len(result.skill_match.missing_skills) - 10} more")

        if result.skill_match.partial_matches:
            print(f"\nPartial Matches ({len(result.skill_match.partial_matches)}):")
            for skill in result.skill_match.partial_matches[:5]:
                print(f"  ~ {skill}")

        print(f"\nSkill Gap Analysis:")
        print(result.skill_match.skill_gap_analysis)

        # Experience Evaluation Analysis
        print("\n--- 2. EXPERIENCE EVALUATION ANALYSIS ---")
        print(f"Score: {result.experience_evaluation.experience_score:.2%}")
        print(f"Experience Level: {result.experience_evaluation.experience_level}")
        print(f"Total Years: {result.experience_evaluation.total_years_experience}")
        print(f"Relevant Years: {result.experience_evaluation.relevant_years_experience}")

        if result.experience_evaluation.relevant_roles:
            print(f"\nRelevant Roles:")
            for role in result.experience_evaluation.relevant_roles:
                print(f"  - {role}")

        if result.experience_evaluation.key_achievements:
            print(f"\nKey Achievements:")
            for achievement in result.experience_evaluation.key_achievements[:5]:
                print(f"  - {achievement}")

        print(f"\nExperience Analysis:")
        print(result.experience_evaluation.analysis)

        # Culture Fit Analysis
        print("\n--- 3. CULTURE FIT ANALYSIS ---")
        print(f"Score: {result.culture_fit.culture_fit_score:.2%}")

        if result.culture_fit.soft_skills_identified:
            print(f"\nSoft Skills Identified:")
            for skill in result.culture_fit.soft_skills_identified:
                print(f"  - {skill}")

        if result.culture_fit.leadership_indicators:
            print(f"\nLeadership Indicators:")
            for indicator in result.culture_fit.leadership_indicators:
                print(f"  - {indicator}")

        print(f"\nCulture Fit Notes:")
        print(result.culture_fit.notes)

        print("\n" + "=" * 80)
        print("FINAL RECOMMENDATION")
        print("=" * 80)

        print("\n--- Strengths ---")
        for i, strength in enumerate(result.strengths, 1):
            print(f"{i}. {strength}")

        print("\n--- Concerns ---")
        for i, concern in enumerate(result.concerns, 1):
            print(f"{i}. {concern}")

        print("\n--- Executive Summary ---")
        print(result.summary)

        print("\n" + "=" * 80)
        print("ASSESSMENT COMPLETE")
        print("=" * 80)
        print(f"\nCandidate: {result.cv_data.candidate_name}")
        print(f"Position: {result.job_description.job_title}")
        print(f"Overall Score: {result.overall_score:.2%}")
        print(f"Recommendation: {result.recommendation.upper().replace('_', ' ')}")

        print("\n--- Recommendation Scale ---")
        print("  STRONG MATCH  (80-100%): Highly qualified, proceed to interview")
        print("  GOOD MATCH    (60-79%):  Qualified with some gaps, interview recommended")
        print("  WEAK MATCH    (40-59%):  Significant gaps, interview only if no better candidates")
        print("  NO MATCH      (0-39%):   Not qualified for this role")

        print("\n" + "=" * 80)
        print("SCORE BREAKDOWN")
        print("=" * 80)
        print(f"Skills Match: {result.skill_match.match_score:.2%} (Weight: 40%)")
        print(f"Experience: {result.experience_evaluation.experience_score:.2%} (Weight: 40%)")
        print(f"Culture Fit: {result.culture_fit.culture_fit_score:.2%} (Weight: 20%)")

        # Save results
        output_path = script_dir / "reports" / "example_result.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result.model_dump(mode="json"), f, indent=2, default=str)

        print(f"\n\nResults saved to: {output_path}")
    else:
        print("\n[ERROR] Assessment failed!")


if __name__ == "__main__":
    main()
