# CV Assessment Agent

A multi-agent framework for assessing job applicants' CVs and determining fit for job positions using LangGraph and LLMs.

## Features

- **Multi-Agent Architecture**: Specialized agents for different aspects of CV assessment
- **LangGraph Workflow**: Orchestrated workflow for comprehensive candidate evaluation
- **Structured Output**: Pydantic-validated data models for reliable results
- **Multiple Document Formats**: Support for PDF, DOCX, TXT, and JSON files
- **Comprehensive Analysis**: Skills matching, experience evaluation, and culture fit assessment


## Architecture

### Agent System

The framework consists of 6 specialized agents working in a coordinated workflow:

1. **CV Parser Agent**: Extracts structured information from CV documents
   - Personal information
   - Skills and proficiencies
   - Work experience with achievements
   - Education and certifications

2. **Job Analyzer Agent**: Analyzes and structures job descriptions
   - Requirements categorization (must-have vs nice-to-have)
   - Required Skills and Experience
   - Responsibilities and qualifications

3. **Skills Matcher Agent**: Matches candidate skills to job requirements
   - Exact skill matches
   - Transferable/related skills
   - Skill gap analysis
   - Match score calculation

4. **Experience Evaluator Agent**: Assesses work experience relevance
   - Years of relevant experience
   - Career progression analysis
   - Experience level determination
   - Achievement evaluation

5. **Culture Fit Assessor Agent**: Evaluates soft skills and cultural alignment
   - Leadership indicators
   - Collaboration and teamwork
   - Communication quality assessment
   - Culture fit scoring

6. **Final Scorer Agent**: Aggregates results and provides recommendations
   - Overall match score calculation
   - Hiring recommendation (strong/good/weak/no match)
   - Key strengths and concerns
   - Executive summary

### Workflow

The workflow leverages **LangGraph's parallel execution** for optimal performance:

```
┌─────────────────┐
│ Load Documents  │
└────────┬────────┘
         │
    ┌────┴────┐ (parallel)
    │         │
┌───▼──┐  ┌───▼────┐
│Parse │  │Analyze │
│  CV  │  │  Job   │
└───┬──┘  └───┬────┘
    │         │
    └────┬────┘
         │
    ┌────┴────────┬─────────┐ (parallel)
    │             │         │
┌───▼─────┐  ┌───▼────┐  ┌─▼──────┐
│ Match   │  │Evaluate│  │ Assess │
│ Skills  │  │Experien│  │Culture │
└───┬─────┘  └───┬────┘  └─┬──────┘
    │             │         │
    └─────────┬───┴─────────┘
              │
         ┌────▼─────┐
         │  Final   │
         │ Scoring  │
         └──────────┘
```

**Key Features:**
- CV parsing and job analysis run in parallel
- Skills matching, experience evaluation, and culture fit assessment run in parallel
- Partial state updates enable concurrent execution without conflicts
- Fail-fast error handling with immediate workflow termination on errors

## Installation

### Prerequisites

- Python 3.11 or higher
- Google Gemini API key or Anthropic API key (OpenAI also supported)


### Setup & Quick Start

For a step-by-step guide to get started, see [QUICKSTART.md](QUICKSTART.md).

### Example Script

Run the provided example:
```bash
python tests/run_example.py
```

Or with custom files:
```bash
python tests/run_example.py --cv path/to/cv.pdf --job path/to/job_description.txt
```

This will assess the CV against the job description and save results to `tests/reports/example_result.json`.

### Interactive Testing

Test individual agents interactively using the Jupyter notebook:
```bash
jupyter notebook tests/test_agents.ipynb
```

The notebook allows you to test each agent separately, inspect intermediate results, and iterate on prompts with autoreload enabled.


### Python API

```python
from cv_assessment.workflows.assessment_workflow import CVAssessmentWorkflow

def assess_candidate():
    workflow = CVAssessmentWorkflow()
    result = workflow.run(
        cv_file_path="path/to/cv.pdf",
        job_description_path="path/to/job.txt"
    )

    print(f"Overall Score: {result.overall_score:.2%}")
    print(f"Recommendation: {result.recommendation}")
    print(f"Summary: {result.summary}")

assess_candidate()
```

## Project Structure

```
cv-assessment-agent/
├── src/
│   └── cv_assessment/
│       ├── __init__.py
│       ├── agents/              # Agent implementations
│       │   ├── base_agent.py
│       │   ├── cv_parser_agent.py
│       │   ├── job_analyzer_agent.py
│       │   ├── skills_matcher_agent.py
│       │   ├── experience_evaluator_agent.py
│       │   ├── culture_fit_agent.py
│       │   └── final_scorer_agent.py
│       ├── models/              # Data models
│       │   └── schemas.py
│       ├── utils/               # Utilities
│       │   ├── config.py
│       │   ├── llm_factory.py
│       │   └── document_parser.py
│       └── workflows/          # LangGraph workflows
│           └── assessment_workflow.py
├── tests/                      # Test files and examples
│   ├── run_example.py         # Example script
│   ├── test_agents.ipynb      # Interactive testing notebook
│   └── reports/               # Output reports
├── examples/                   # Sample CV and job files
├── docs/                       # Documentation
├── pyproject.toml             # Project configuration
├── .env.example               # Environment template
├── README.md                  # This file (comprehensive reference)
└── QUICKSTART.md              # 5-minute quick start guide
```

## Configuration

### LLM Provider

The framework supports both OpenAI and Anthropic models. Configure in `.env`:

```bash
# Use Gemini (default)
DEFAULT_LLM_PROVIDER=Gemini
DEFAULT_MODEL=gemini-2.0-flash
OPENAI_API_KEY=your-key

DEFAULT_LLM_PROVIDER=openai
DEFAULT_MODEL=gpt-4o-mini
OPENAI_API_KEY=your-key

# Or use Anthropic
DEFAULT_LLM_PROVIDER=anthropic
DEFAULT_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_API_KEY=your-key
```

### Scoring Weights

The final score is calculated with default weights:
- Skills Match: 40%
- Experience: 40%
- Culture Fit: 20%

These can be customized in [final_scorer_agent.py](src/cv_assessment/agents/final_scorer_agent.py).

### Recommendation Thresholds

- **STRONG MATCH (80-100%)**: Highly qualified, proceed to interview
- **GOOD MATCH (60-79%)**: Qualified with some gaps, interview recommended
- **WEAK MATCH (40-59%)**: Significant gaps, interview only if no better candidates
- **NO MATCH (0-39%)**: Not qualified for this role


## Output Format

The assessment produces a structured result containing:

- **CV Data**: Parsed candidate information
- **Job Description**: Structured job requirements
- **Skill Match**: Detailed skill analysis and score
- **Experience Evaluation**: Experience relevance and score
- **Culture Fit**: Soft skills assessment and score
- **Overall Score**: Weighted average (0.0-1.0)
- **Recommendation**: strong_match | good_match | weak_match | no_match
- **Strengths**: Key candidate advantages
- **Concerns**: Areas requiring attention
- **Summary**: Executive summary of assessment



