# Quick Start Guide -  Your First Assessment

## Step 1: Install 

```bash
cd cv-assessment-agent
conda create -n cv-assessment python=3.11
conda activate cv-assessment
pip install -e .
```

## Step 2: Configure API Key 

Copy the example environment file and add your API key:
```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```bash
# Choose one provider:
ANTHROPIC_API_KEY=sk-ant-your-key-here
# OR
OPENAI_API_KEY=sk-your-key-here
```

## Step 3: Run Example 

```bash
python tests/run_example.py
```

The default example assesses a Data Scientist CV against a Senior Data Scientist job description.

You should see output like:
```
================================================================================
CV ASSESSMENT EXAMPLE
================================================================================

CV Path: /path/to/examples/sample_cv_data_scientist.txt
Job Path: /path/to/examples/Senior_Data_Scientist.txt

Starting assessment...

[Agent processing logs...]

================================================================================
DETAILED AGENT ANALYSIS
================================================================================

--- 1. SKILLS MATCH ANALYSIS ---
Score: 78.50%

Matched Skills (15):
  ✓ Python
  ✓ Machine Learning
  ✓ Deep Learning
  ✓ SQL
  ... and 11 more

Missing Skills (8):
  ✗ Azure
  ✗ Snowflake
  ✗ Reinforcement Learning
  ... and 5 more

Skill Gap Analysis:
[Detailed analysis of skill matches and gaps]

--- 2. EXPERIENCE EVALUATION ANALYSIS ---
Score: 75.00%
Experience Level: senior
Total Years: 6.0
Relevant Years: 6.0

Relevant Roles:
  - Senior Data Scientist at TechCorp
  - Data Scientist at DataCo
  ...

Experience Analysis:
[Detailed analysis of relevant experience]

--- 3. CULTURE FIT ANALYSIS ---
Score: 80.00%

Soft Skills Identified:
  - Leadership
  - Collaboration
  - Communication
  ...

Leadership Indicators:
  - Led data science team
  - Mentored junior scientists
  ...

Culture Fit Notes:
[Detailed cultural fit analysis]

================================================================================
FINAL RECOMMENDATION
================================================================================

--- Strengths ---
1. Strong technical foundation in ML/DL with 6+ years experience
2. Ph.D. in Computer Science with NLP specialization
3. Proven track record of deploying production ML models
4. Leadership and mentoring experience
5. Strong analytical and problem-solving skills

--- Concerns ---
1. Limited experience with Azure cloud platform (highly desirable)
2. No Snowflake experience mentioned
3. Limited exposure to financial services industry
4. Generative AI experience needs validation

--- Executive Summary ---
Dr. Sarah Chen is a strong candidate for the Senior Data Scientist position...
[Full detailed summary]

================================================================================
ASSESSMENT COMPLETE
================================================================================

Candidate: Dr. Sarah Chen
Position: Senior Data Scientist
Overall Score: 77.80%
Recommendation: GOOD MATCH

--- Recommendation Scale ---
  STRONG MATCH  (80-100%): Highly qualified, proceed to interview
  GOOD MATCH    (60-79%):  Qualified with some gaps, interview recommended
  WEAK MATCH    (40-59%):  Significant gaps, interview only if no better candidates
  NO MATCH      (0-39%):   Not qualified for this role

================================================================================
SCORE BREAKDOWN
================================================================================
Skills Match: 78.50% (Weight: 40%)
Experience: 75.00% (Weight: 40%)
Culture Fit: 80.00% (Weight: 20%)

Results saved to: /path/to/tests/reports/example_result.json
```

## Understanding Results

### Recommendation Levels
- **STRONG MATCH (80-100%)**: Highly qualified, proceed to interview immediately
- **GOOD MATCH (60-79%)**: Qualified with some gaps, interview recommended
- **WEAK MATCH (40-59%)**: Significant gaps, interview only if no better candidates available
- **NO MATCH (0-39%)**: Not qualified for this role

### Score Components
The overall score is calculated using weighted averages:
- **Skills Match**: 40% weight - How well candidate's skills match job requirements
- **Experience**: 40% weight - Relevance and quality of work experience
- **Culture Fit**: 20% weight - Soft skills and cultural alignment

### What to Review
1. **Detailed Agent Analysis**: Each agent's assessment (skills, experience, culture fit)
2. **Strengths**: Key advantages and qualifications of the candidate
4. **Executive Summary**: High-level overview of candidate fit
5. **Score Breakdown**: Individual component scores with weights

### Try Different Candidates

Assess your own CV and job description:
```bash
python tests/run_example.py --cv path/to/your_cv.pdf --job path/to/job_description.txt
```

Supported formats: PDF, DOCX, TXT, JSON

## Interactive Testing with Jupyter Notebook

For interactive exploration and testing of individual agents, use the provided Jupyter notebook:

```bash
# Install Jupyter if not already installed
pip install jupyter

# Launch Jupyter notebook
jupyter notebook tests/test_agents.ipynb
```

**What you can do in the notebook:**

1. **Test each agent individually** - Run agents one at a time to see their specific outputs
2. **Experiment with different inputs** - Easily swap CV and job description files
3. **Inspect intermediate results** - View parsed CV data, job requirements, skill matches, etc.
4. **Debug and iterate** - Modify agent prompts and see results immediately with autoreload
5. **Customize scoring** - Test different scoring thresholds and weights

**Available agent tests:**
- **CV Parser Agent** - Extract structured data from CV text
- **Job Analyzer Agent** - Parse job requirements and categorize skills
- **Skills Matcher Agent** - Compare candidate skills to job requirements
- **Experience Evaluator Agent** - Assess work experience relevance
- **Culture Fit Agent** - Evaluate soft skills and cultural alignment
- **Final Scorer Agent** - Generate overall assessment and recommendation

**Example workflow in notebook:**
```python
# Load custom CV and job description
with open('path/to/your_cv.txt', 'r') as f:
    cv_text = f.read()

# Test individual agent
cv_parser = CVParserAgent()
cv_data = cv_parser.parse_cv(cv_text)

# Inspect results
print(f"Candidate: {cv_data.candidate_name}")
print(f"Skills: {len(cv_data.skills)} found")
```

The notebook includes autoreload, so you can modify agent prompts in `src/cv_assessment/agents/` and see changes immediately without restarting the kernel.

## Next Steps

- Review the full [README.md](README.md) for architecture details
- Check example files in `examples/` directory for reference
- Use [tests/test_agents.ipynb](tests/test_agents.ipynb) for interactive agent testing
- Customize scoring weights in `src/cv_assessment/agents/final_scorer_agent.py`
- Modify agent prompts for domain-specific assessments

