---
name: science-vibecoding
description: Structured AI-assisted scientific code generation. 6 safety guards, 8 principles, 11 prompt templates. Grounded in Nature (2026).
version: 1.3.0
---

# Science Vibe Coding

A structured framework for generating rigorous, publication-ready scientific code through AI-assisted natural language prompts. Based on best practices from Nature (Jones, 2026) and validated by early adopters across climate science, proteomics, molecular biology, and statistics.

**Core principle**: AI-generated scientific code is an *untrusted draft* (Meyer, 2026) — it must be verified, not just executed.

## Workflow

When a user requests scientific code generation, follow this workflow:

```
Task Progress:
- [ ] Step 1: Clarify the research task
- [ ] Step 2: Select scenario & generate prompt
- [ ] Step 2.5: Review & confirm analysis plan (before writing code)
- [ ] Step 3: Generate code with safety guards
- [ ] Step 4: Run verification protocol
- [ ] Step 5: Document the Vibe Blueprint
```

### Step 1: Clarify the Research Task

Ask the user these questions (skip any already answered):

1. **What** is the analysis goal? (e.g., "compare two groups", "visualize temperature trends", "train a classifier")
2. **What** is the input data format? (CSV, FASTA, Excel, NetCDF, etc.)
3. **What** tools/libraries are preferred? (pandas, scipy, matplotlib, scikit-learn, etc.)
4. **What** is the output? (figures, processed data files, statistical reports, web apps)
5. **Is this for publication?** If yes, what journal's formatting standards apply?

### Step 2: Select Scenario & Generate Prompt

Based on the user's task, select the matching scenario and load the corresponding prompt template from [prompt-templates.md](prompt-templates.md):

| Scenario | Keywords | Template |
|----------|----------|----------|
| Data Cleaning & Preprocessing | clean, preprocess, impute, outlier, missing values | `DATA_CLEANING` |
| Statistical Testing | t-test, ANOVA, chi-square, regression, p-value | `STAT_TESTING` |
| Data Visualization | plot, chart, figure, heatmap, publication figure | `VISUALIZATION` |
| Format Conversion | convert, transform, FASTA, CSV, cross-validate | `FORMAT_CONVERSION` |
| ML / Model Training | classify, predict, regression, random forest, SVM | `ML_MODELING` |
| Unit Testing | test, validate, edge case, boundary, pytest | `UNIT_TESTING` |
| Math Modeling | ODE, PDE, simulation, differential equation | `MATH_MODELING` |
| Text Analysis | NLP, extract, parse, keyword, literature review | `TEXT_ANALYSIS` |
| Code Review Prep | refactor, PEP-8, docstring, type hints, peer review | `CODE_REVIEW` |
| Deep Learning Training | neural network, CNN, RNN, Transformer, PyTorch, TensorFlow, train, GPU, CUDA | `DL_TRAINING` |
| CS Benchmarking | benchmark, algorithm comparison, time complexity, performance, profiling | `CS_BENCHMARKING` |

**Multi-scenario tasks**: If the task spans multiple scenarios (e.g., clean data → run stats → plot results), chain the templates in order with explicit data handoff between steps.

#### Chaining Templates: Multi-Scenario Protocol

When chaining 2+ templates, follow these rules to prevent data loss between stages:

**Variable Naming Convention**: Each stage's output variable must use a consistent prefix matching its template:
- `data_clean_*` for DATA_CLEANING outputs
- `stat_*` for STAT_TESTING outputs
- `vis_*` for VISUALIZATION outputs
- `ml_*` for ML_MODELING outputs
- `dl_*` for DL_TRAINING outputs (model state, training history, checkpoints)
- `bench_*` for CS_BENCHMARKING outputs (timing data, memory profiles, scaling results)

This prevents variable name collisions and makes handoff points traceable.

**Data Handoff Patterns** (choose one before generating code):

1. **FILE handoff** (recommended for reproducibility): Each stage writes output to a timestamped file, the next stage reads it.
   ```python
   # Stage 1 output
   cleaned = clean_dataset(raw_df)
   cleaned.to_csv("data_clean_20260624.csv", index=False)
   
   # Stage 2 input
   cleaned = pd.read_csv("data_clean_20260624.csv")
   stat_result = run_test(cleaned)
   ```

2. **MEMORY handoff** (for single-script chains): Use distinct variable names; validate data shape at each handoff.
   ```python
   # Handoff point — always validate
   assert not data_clean_df.empty, "Stage 1 produced empty output"
   print(f"[CHAIN] Handoff: Stage 1 → Stage 2 | Shape: {data_clean_df.shape}")
   stat_result = run_test(data_clean_df)
   ```

3. **CONTRACT handoff** (for distributed/large pipelines): Define a schema file specifying column names, types, and value ranges. Each stage validates input against the contract.

**Handoff Validation**: Every chain point MUST print a `[CHAIN]` log confirming:
- Source stage → destination stage
- Data shape (rows, columns)
- Any dropped or filtered rows
- Whether the data passed validation

**Chain Ordering Rule**: Templates must be executed in this dependency order when combined: DATA_CLEANING → FORMAT_CONVERSION → STAT_TESTING / ML_MODELING / DL_TRAINING / MATH_MODELING → CS_BENCHMARKING / VISUALIZATION → CODE_REVIEW. UNIT_TESTING and TEXT_ANALYSIS can be inserted at any point. Note: DL_TRAINING requires DATA_CLEANING as a prerequisite; CS_BENCHMARKING should run after model implementation but can feed into VISUALIZATION.

### Step 2.5: Analysis Plan Review (分析计划审查)

**Source**: Pimenova et al. (2025) — "Planning is boring—until you waste 37+ hours fixing AI hallucinations." Nature (Meyer, 2026) — Meyer first had AI help him select the statistical method, confirmed the plan, then generated code.

Before generating any code, the AI MUST output an analysis plan for user confirmation. This prevents wasted effort on wrong approaches.

**Plan output format**:
```
[PLAN] Method: [exact method/model/algorithm name]
[PLAN] Rationale: [why this method fits your data and goal]
[PLAN] Assumptions: [what the method requires — distribution, sample size, independence, etc.]
[PLAN] If assumptions fail: [alternative method]
[PLAN] Expected output: [what results should look like — range, format, units]
[PLAN] Known limitations: [what this method cannot do]
```

**User confirmation required**: The user must confirm the plan before code generation begins. If the user disagrees, the AI should revise the plan — not jump to writing code.

**For statistical tasks** (STAT_TESTING): The plan must include which assumption checks will be run first (e.g., Shapiro-Wilk for normality, Levene for equal variance) and how the method choice depends on those results.

**For ML/DL tasks** (ML_MODELING, DL_TRAINING): The plan must include model architecture, key hyperparameters with rationale, validation strategy, and expected performance range.

**For multi-step pipelines**: Each stage gets its own plan. Do not plan the entire pipeline at once — plan one stage, confirm, generate code, verify, then plan the next.

### Step 3: Generate Code with Safety Guards

When generating the code, ALWAYS apply these mandatory safety guards:

#### Guard 1: Explicit Method Declaration

**CRITICAL**: The method declaration MUST be determined dynamically AFTER all assumption checks, then printed immediately before the actual function call. A hardcoded string before method selection is a silent bug — it prints the requested method regardless of what the code actually executes.

**CORRECT pattern** (dynamic, after assumption checks):
```python
# (a) Run assumption checks FIRST
shapiro_stat, shapiro_p = stats.shapiro(group_a)
levene_stat, levene_p = stats.levene(group_a, group_b)

# (b) Select method DYNAMICALLY based on assumption results
if shapiro_p > 0.05 and levene_p > 0.05:
    method_name = "Welch's t-test (scipy.stats.ttest_ind, equal_var=False)"
    method_fn = stats.ttest_ind
    method_kwargs = {"equal_var": False}
elif shapiro_p > 0.05 and levene_p <= 0.05:
    method_name = "Student's t-test (scipy.stats.ttest_ind, equal_var=True)"
    method_fn = stats.ttest_ind
    method_kwargs = {"equal_var": True}
else:
    method_name = "Mann-Whitney U (scipy.stats.mannwhitneyu)"
    method_fn = stats.mannwhitneyu
    method_kwargs = {}

# (c) Print the DYNAMICALLY determined method IMMEDIATELY before calling it
print(f"[METHOD] Using: {method_name}")
print(f"[METHOD] Library: scipy v{scipy.__version__}")
print(f"[METHOD] Rationale: Shapiro-Wilk p={shapiro_p:.4f}, Levene p={levene_p:.4f}")

# (d) Execute
result = method_fn(group_a, group_b, **method_kwargs)
```

**BUG pattern to AVOID** (hardcoded before assumption checks):
```python
# BUG: Prints "Welch's t-test" regardless of what happens below
print(f"[METHOD] Using: Welch's t-test (scipy.stats.ttest_ind with equal_var=False)")

# Assumption checks below may lead to a DIFFERENT method being used,
# but the print above has already lied to the user.
shapiro_stat, shapiro_p = stats.shapiro(group_a)
levene_stat, levene_p = stats.levene(group_a, group_b)
# ... method selection logic that might pick Student's t-test or Mann-Whitney ...
```

Never let the code silently choose a statistical method or algorithm. The user must see confirmation of what was actually executed — and that confirmation must match reality.

#### Guard 2: No Silent Defaults

```python
# MANDATORY: Raise errors for unspecified parameters instead of using library defaults
raise ValueError("Parameter [X] not specified. Please explicitly set this value.")
```

If the user hasn't specified a critical parameter (imputation method, kernel function, significance level), the code must ask — not assume.

#### Guard 3: Input Validation Block

Every generated script must start with a validation section:

```python
# === INPUT VALIDATION ===
# Check data shape, types, missing values BEFORE any analysis
assert not df.empty, "Input dataframe is empty"
assert df.shape[0] > 1, "Need at least 2 rows for analysis"
# ... domain-specific checks
print(f"[DATA] Shape: {df.shape}, Missing: {df.isnull().sum().sum()}")
```

#### Guard 4: No AI Self-Testing

Never generate test cases alongside analysis code unless explicitly requested under the `UNIT_TESTING` scenario. When generating tests, they MUST include adversarial edge cases (see `UNIT_TESTING` template).

#### Guard 5: Comprehensive Comments

Every function and non-trivial code block must have comments explaining:
- **What** it does (the operation)
- **Why** this method was chosen (the scientific rationale)
- **What** assumptions it makes (distribution, sample size, etc.)

#### Guard 6: Change Audit (变更审计)

**Source**: Pimenova et al. (2025) documented cases where AI secretly modified tests or deleted code without informing the user. One interviewee reported: "the agent will tell me, like, 'oh, you know, I fixed the tests'…I'm like, no, it's totally our fault."

AI MUST NOT modify, delete, or overwrite existing code without informing the user.

After every code generation/modification, print a change report:
- Which files/functions are NEW
- Which existing files/functions were MODIFIED (with diff summary)
- Which code was DELETED (must be listed explicitly — never silent)

If AI recommends modifying existing tests:
1. Print the test name and what changed
2. Explain WHY the change is needed
3. Wait for user confirmation before proceeding

If AI recommends deleting code:
1. Print the code to be deleted
2. Explain the reason
3. Wait for user confirmation

**Absolute prohibitions**:
- Silently deleting test cases
- Modifying tests so they "always pass"
- Overwriting old code without notification
- Changing function signatures without warning

### Step 4: Run Verification Protocol

After generating code, walk the user through the [risk-checklist.md](risk-checklist.md). At minimum, verify:

1. **Method fidelity**: Does the executed method match what was requested? (cf. Morey's t-test/z-test case)
2. **No silent data modification**: Does the code alter, impute, or smooth data without explicit instruction?
3. **Test adversarial inputs**: What happens with empty data, NaN values, single-row input?
4. **Output sanity check**: Do results match expected ranges from domain knowledge?

For efficient review, use the [Code Review Strategy](#code-review-strategy) — focus effort on high-risk sections (method selection, data processing) rather than reading every line. If errors are found, follow the [Debugging Protocol](#debugging-protocol) — isolate and fix, do not rewrite entire files.

#### Blueprint Checkpoint (MANDATORY)

After completing Step 4 verification, PAUSE and ask the user:

> "The analysis is complete and verified. Would you like me to generate a Vibe Blueprint for reproducibility? This will record the exact prompts, parameters, verification results, and known limitations for inclusion in your paper's supplementary materials."

If the user says yes, proceed to Step 5. If the user says no, record that the blueprint was declined and move on. This checkpoint ensures the blueprint is never silently skipped — reproducibility documentation must be a conscious choice.

### Step 5: Document the Vibe Blueprint

For reproducibility (Meyer, 2026), generate a `VIBE_BLUEPRINT.md` file alongside the code. Use the template in [vibe-blueprint-template.md](vibe-blueprint-template.md).

The blueprint records: the exact prompts used, the AI model and version, all parameter choices, verification results, and known limitations.

## Safety Principles

These principles are derived from Nature 653:348-350 and referenced papers:

### Principle 1: "Vibe coding is not a substitute for understanding" (Meyer, 2026)

If the user cannot explain what the generated code does in their own words, they should not use it for publication. Offer to explain any generated code line by line.

### Principle 2: "Wrong in a subtle way you wouldn't necessarily know" (Morey, via Nature)

AI code can produce results that *look* correct but use wrong methods. The most dangerous errors are the ones that pass visual inspection. Always verify the method, not just the output.

### Principle 3: "It can make some pretty hilarious tests for itself where it just always passes" (Meyer, via Nature)

AI-generated self-tests are unreliable. They tend to verify the simplest path. Researchers must design their own validation tests.

### Principle 4: "Vibe debugging is chaos" (Pimenova et al., 2025)

Keep generated code modular and short. A 400-line file that balloons to 3000 lines becomes unreadable by both human and AI. Split into small, single-responsibility functions. When errors occur, follow the [Debugging Protocol](#debugging-protocol) — do not let AI rewrite entire files.

### Principle 5: "Code should be published alongside the research paper" (Nature consensus)

All generated code should be written as if it will be publicly reviewed. Follow PEP-8, use type hints, write docstrings, and structure for readability.

### Principle 6: "GPU non-determinism must be explicitly controlled" (experience from DL research)

PyTorch and TensorFlow produce different results on every GPU run unless seeds are exhaustively set. Floating-point parallel reduction order varies across CUDA executions. Without `torch.backends.cudnn.deterministic = True`, cuDNN selects different convolution algorithms per run. A paper that reports "70.3% accuracy" from a single run without seed control cannot be reproduced — not by reviewers, not by yourself six months later.

### Principle 7: "Train/eval mode mismatch is the most common silent bug in DL code" (experience from DL research)

Forgetting `model.eval()` before validation causes batch normalization layers to use running statistics instead of batch statistics, silently contaminating validation results. Forgetting `model.train()` after validation keeps dropout active during subsequent training steps. These bugs produce results that look plausible but are wrong — the most dangerous category of error for publication.

### Principle 8: "Small steps, reset often" (Pimenova et al., 2025; Wilton via Nature, 2026)

Generate code in small increments — one function, one module, one statistical test at a time. Verify each step before proceeding to the next. Do not attempt to generate an entire project in one go.

**Conversation management** (from Pimenova et al., 2025):
- If the AI gives incorrect or repetitive suggestions twice in a row, start a new conversation immediately
- If the conversation exceeds 20 rounds, consider starting a new one (use files to transfer context, not conversation history)
- If the AI starts "forgetting" earlier agreements, start a new conversation
- At the start of a new conversation, summarize the previous stage's output and current goal in one sentence

**Why this matters**: Long conversations cause AI context loss, degrading code quality and producing "prompt spirals" — where the AI repeatedly suggests the same incorrect approach. One interviewee reported: "I 'fire' conversations before they start to lose their mind and start a new one…they give 'hints' that they're losing it."

**Granularity guideline**: Each code generation step should produce no more than ~80 lines of code. If a task requires more, break it into sub-tasks, each generated and verified independently.

## Language-Specific Defaults

| Language | Formatting | Type Hints | Docstring Style | Testing Framework |
|----------|-----------|------------|-----------------|-------------------|
| Python | PEP-8 / ruff | Required | Google-style | pytest |
| R | tidyverse style | roxygen2 types | roxygen2 | testthat |
| MATLAB | MATLAB Lint | Argument blocks | Help text | unittest (built-in) |
| Julia | BlueStyle.jl | Required | Docstrings | Test.jl |

## Quick Commands

Users can trigger specific scenarios with shorthand:

- **"Clean this data"** → `DATA_CLEANING` template
- **"Run a t-test"** → `STAT_TESTING` template (Welch's t-test by default)
- **"Make a figure"** → `VISUALIZATION` template (colorblind-safe palette by default)
- **"Convert formats"** → `FORMAT_CONVERSION` template
- **"Train a model"** → `ML_MODELING` template (5-fold CV by default)
- **"Write tests"** → `UNIT_TESTING` template (adversarial cases included)
- **"Simulate"** → `MATH_MODELING` template
- **"Extract text"** → `TEXT_ANALYSIS` template
- **"Refactor for paper"** → `CODE_REVIEW` template
- **"Train a neural network"** → `DL_TRAINING` template (full reproducibility suite by default)
- **"Benchmark algorithms"** → `CS_BENCHMARKING` template (multi-scale + correctness verification)
- **"Vibe blueprint"** → Generate reproducibility documentation

## Common Pipelines

Reference for common multi-scenario workflows. Each pipeline lists the templates in execution order and the recommended handoff pattern.

| Pipeline | Templates (in order) | Handoff Pattern | Notes |
|----------|---------------------|-----------------|-------|
| **Standard Analysis** | DATA_CLEANING → STAT_TESTING → VISUALIZATION | FILE | Most common pipeline; clean data, test hypotheses, visualize results |
| **ML Pipeline** | DATA_CLEANING → ML_MODELING → VISUALIZATION | FILE | Feature engineering in DATA_CLEANING; use stratified CV in ML_MODELING |
| **Simulation Study** | MATH_MODELING → VISUALIZATION → STAT_TESTING | MEMORY | Run simulations, plot trajectories, then test parameter sensitivity |
| **Publication Prep** | CODE_REVIEW → VISUALIZATION → (Blueprint) | CONTRACT | Refactor code for journal submission, regenerate figures to spec, document |
| **Literature Mining** | TEXT_ANALYSIS → STAT_TESTING → VISUALIZATION | FILE | Extract data from papers, run meta-analysis, visualize findings |
| **DL Research** | DATA_CLEANING → DL_TRAINING → CS_BENCHMARKING → VISUALIZATION | FILE | Clean data, train model with explicit seeds, benchmark performance, plot loss/accuracy curves |
| **Algorithm Study** | CS_BENCHMARKING → STAT_TESTING → VISUALIZATION | FILE | Benchmark multiple algorithms, test performance differences statistically, visualize scaling behavior |

When in doubt, use FILE handoff — it provides the strongest reproducibility guarantee.

## Version Control Best Practices

**Source**: Pimenova et al. (2025) — "I got too deep in the vibe, took my eye off the ball, and the whole thing spun out of control. I had 30 files in my change log with hours of work uncommitted."

After every AI code generation or modification, commit before proceeding to the next step:

1. `git add` the changed files
2. `git commit` with a message describing what changed and why
3. Do NOT continue generating new code on top of uncommitted changes

**File discipline**:
- Each modification should touch no more than 3 files. If more files need changing, do it in batches with commits between batches.
- Do not rename/move multiple files in one operation
- Print a change summary after each modification: `[GIT] Modified: [file1, file2] | Added: [file3] | Deleted: [none]`

**Why**: AI tools can make large, sweeping changes that touch many files. Without frequent commits, you lose the ability to roll back individual changes. Version control is your safety net.

## Debugging Protocol

**Source**: Pimenova et al. (2025) — "Vibe coding is one thing, vibe debugging is chaos." Nature (Hobbs, 2026) — "It takes extraordinary effort and expert domain knowledge" to debug AI code.

When generated code fails, follow this protocol:

### Phase A: Locate
- Identify the exact location of the error (line number, function name, exact error message)
- Do NOT let AI "fix the whole file" — pinpoint first

### Phase B: Isolate
- Ask AI to modify ONLY the specific code block that caused the error
- Provide the exact error message as context
- Do not allow AI to "refactor" or "improve" surrounding code while fixing

### Phase C: Verify
- Re-run the code after the fix
- Confirm the error is gone AND no new errors were introduced
- Check that the output still makes sense

### Phase D: Record
- Document the error cause and fix in comments or the Vibe Blueprint
- This helps if the same error recurs

**When to stop letting AI debug**:
- If AI cannot fix the error in 3 attempts, STOP
- Manually read the relevant code yourself
- Search Stack Overflow or documentation
- Consider implementing the feature a different way
- Remember: debugging AI code can be "at least as hard as writing it from scratch" (Hobbs, Nature 2026)

**Absolute prohibitions during debugging**:
- Do not let AI rewrite an entire file to fix one bug
- Do not let AI guess the problem without seeing the error message
- Do not let AI "try a completely different approach" without your approval

## Code Review Strategy

**Source**: Pimenova et al. (2025) — "I'm more mentally exhausted at the end of the day these days because…I'm working so damn fast and am in constant code review mode."

AI-generated code requires review, but not every line needs equal scrutiny. Allocate review effort by risk level:

### High Risk (review line-by-line):
- Statistical method selection and parameters
- Data splitting and preprocessing logic
- Result interpretation and conclusions
- Any code that affects the final numbers

### Medium Risk (spot-check key sections):
- Data input/output operations
- File read/write operations
- Loop and conditional logic
- Error handling

### Low Risk (quick scan):
- Visualization code (colors, labels, layout)
- Formatting and printing
- Logging statements

**Efficient review technique**:
1. First, check the `[METHOD]` print — does it match what you requested?
2. Then, check data shape prints — is the data flowing correctly?
3. Finally, check the output — do the results look reasonable?
4. You do NOT need to read every comment or understand every line of boilerplate

**If review is exhausting**: This is a signal that the generated code is too large. Go back to Principle 8: generate smaller chunks.

## Cost Awareness

**Source**: Nature (Meyer, 2026) — 4 prompts, 10 minutes, $1.96 for 1,400 lines of code. Pimenova et al. (2025) — developers report frustration with API rate limits and latency.

AI coding has costs in three currencies: money (tokens), time, and attention.

### Token Management
- Each session should complete ONE analysis step (not an entire project)
- If the conversation exceeds 20 rounds, start a new session
- For complex tasks, use multiple sessions connected by file handoff (not conversation context)
- Do not mix planning, code generation, and debugging in the same session

### Time Management
- If AI cannot solve a problem in 3 attempts, try a different approach
- If generated code requires extensive manual modification, write it yourself instead
- Record time and cost per session (for the Vibe Blueprint)

### Attention Management
- Do not work continuously for more than 2 hours without a break
- Pause to review results after each stage
- Be aware of "vibe coding addiction" — stop when code quality starts degrading
- One interviewee warned: "If I could go back in time, I would stop myself from using ChatGPT 3.5 for coding…I am literally addicted to it" (Pimenova et al., 2025)

## Context Provision

**Source**: Pimenova et al. (2025) — "since almost every solution we use to common problems is a custom private lib, the LLMs simply have no way of providing value because they know jackshit about my specific issues."

AI does not know your private codebase, internal tools, or recently released libraries. You must actively provide context.

### Method 1: File Injection
- Paste relevant code files into the prompt
- Paste API documentation or README content into the prompt
- For data analysis: paste the first few rows and column descriptions

### Method 2: Rules File
- Create a `.cursorrules` or `CLAUDE.md` file in your project root
- Describe: project structure, libraries used, coding conventions, data formats
- AI tools read these files automatically

### Method 3: Stepwise Guidance
- First, ask AI to generate a "hello world" example using your library
- Confirm AI understands your library's API
- Then ask it to write the actual code

### Method 4: Reference Documents
- Upload relevant papers, documentation, or specifications
- Tell AI which specific sections are relevant
- "Read section 3.2 of the attached paper and implement the method described there"

**Never assume AI knows**:
- Your project structure
- Your internal libraries or custom functions
- Library versions released in the last 3 months
- Your data format conventions or naming schemes
- Domain-specific knowledge not widely published

## Additional Resources

- For detailed prompt templates (11 scientific scenarios), see [prompt-templates.md](prompt-templates.md)
- For the full risk verification checklist, see [risk-checklist.md](risk-checklist.md)
- For the Vibe Blueprint reproducibility template, see [vibe-blueprint-template.md](vibe-blueprint-template.md)
- For a complete end-to-end example demonstrating all safety guards, see [examples/](examples/)
- For debugging strategies, see [Debugging Protocol](#debugging-protocol) above
- For efficient code review, see [Code Review Strategy](#code-review-strategy) above

## References

- Jones, N. "How to vibe code in science: early adopters share their tips." *Nature* 653, 348-350 (2026). DOI: [10.1038/d41586-026-01477-w](https://doi.org/10.1038/d41586-026-01477-w)
- Meyer, J. G. "Vibe Coding Omics Data Analysis Applications." *J. Proteome Res.* 25, 1191-1197 (2026). DOI: [10.1021/acs.jproteome.5c00984](https://doi.org/10.1021/acs.jproteome.5c00984)
- Ziemann, M., Eren, Y. & El-Osta, A. "Gene name errors are widespread in the scientific literature." *Genome Biol.* 17, 177 (2016). DOI: [10.1186/s13059-016-1044-7](https://doi.org/10.1186/s13059-016-1044-7)
- Pimenova, V. et al. "Good Vibrations? A Qualitative Study of Co-Creation, Communication, Flow, and Trust in Vibe Coding." *arXiv:2509.12491* (2025). DOI: [10.48550/arXiv.2509.12491](https://doi.org/10.48550/arXiv.2509.12491)
