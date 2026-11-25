---
name: experiment-design
description: Use when a research design has been approved and needs to be broken into executable experiment steps — the research equivalent of an implementation plan
---

# Experiment Design Skill

## Purpose

Break an approved research design into a fully executable experiment plan. Every step must be runnable by someone with zero prior context on the project. No ambiguity, no placeholders, no "check results" without specifying exactly what metric and what threshold.

This is the research equivalent of `writing-plans`: just as that skill breaks a feature into bite-sized TDD tasks with exact file paths and code, this skill breaks a research design into discrete experiment steps with exact data paths, commands, seeds, and success criteria.

## Announce at Start

At the beginning of every session using this skill, state:

> "I'm using the experiment-design skill to create the experiment plan."

## Trigger Conditions

Use this skill when:
- A research design or hypothesis document has been approved (exists in `docs/eureka/designs/`)
- Someone asks to "plan the experiments," "operationalize the design," or "turn this into runnable steps"
- A hypothesis-first output needs to be translated into concrete execution

Do NOT use this skill to:
- Generate hypotheses (use `hypothesis-first`)
- Review completed experiments (use `requesting-research-review`)
- Produce analysis or interpret results

---

## Plan Document Header

Every experiment plan MUST begin with this header, fully filled in — no blanks, no TBDs:

```markdown
# [Study Name] Experiment Plan
**Goal:** [one sentence describing what this plan will determine]
**Design Reference:** [relative path or URL to the approved design doc]
**Registered Hypothesis:** [exact H1 statement, copied verbatim from the design]
**Primary Outcome:** [exact measure, units, and dataset]
**Analysis Plan:** [exact statistical test, correction method, significance threshold]
---
```

If any of these fields cannot be filled in, stop and ask the user to provide the missing information before continuing. An incomplete header is a hard blocker.

---

## Scope Check (Do This First)

Before writing any tasks, examine the approved design for scope:

1. Count the number of independent hypotheses being tested.
2. If there are multiple independent hypotheses (different DV, different population, different intervention), flag this:

   > "This design covers N independent hypotheses. I recommend splitting into N separate experiment plans for traceability. Shall I do that, or keep them in one plan?"

3. If the user confirms a single plan, note the multi-hypothesis scope in the header under a `**Scope Note:**` field.

---

## Contingency Inheritance from Registration (Do This Second)

Before breaking the design into tasks, read the approved registration file at `docs/eureka/registrations/<registration_id>.md`.

**Extract all contingency clauses from the registration:**
- Halt rules ("if X, halt the study")
- Proceed rules ("if X, proceed as pilot"; "if X, proceed without stratification")
- Escalate rules ("if X, amendment required")
- Pre-registered decision rules (analysis branching, correction-method triggers)

**Apply inheritance rules** (see `docs/references/registration-lifecycle.md` section **"Plan ↔ Registration contingency inheritance rules"**):

| Scenario | Allowed? |
|---|---|
| Plan contingency matches registration verbatim | ✓ Yes |
| Plan adds NEW task-level operational contingency (e.g., "restart if GPU OOM") | ✓ Yes — operational, not scientific |
| Plan is STRICTER than registration (e.g., registration says "proceed as pilot if N<300", plan says "halt if N<300") | ✗ No — plan is overriding the registration. Fix plan OR amend registration |
| Plan is WEAKER than registration (e.g., removes a halt rule) | ✗ No — weakening requires a new registration via supersede (not amendment), since it changes the study's risk profile |
| Plan OMITS a registration contingency | ✗ No — silent override; add it back |

**Workflow**:
1. Read registration, extract contingencies verbatim into a scratch list
2. As you write each experiment task, copy applicable contingencies into the task's `Step 4: Verify outputs` or equivalent field
3. If a task-level operational contingency is stricter than what you want to execute, do NOT silently weaken — stop and invoke `eureka:hypothesis-first` amendment workflow
4. The `experiment-plan-reviewer` subagent will check contingency inheritance as a Must-fix-severity dimension

This closes the "plan vs registration contradiction" class of failures (registration says "proceed as pilot if N<300", plan says "halt if N<300" — which wins? Answer: neither should silently win; fix one or amend the other).

---

## Experiment Task Structure

Each experiment is a numbered, named block. Every field is mandatory.

```markdown
### Experiment N: [Descriptive Name]
**Depends on:** [comma-separated list of prior Experiment numbers, or "none"]
**Inputs:**
  - `[exact/relative/path/to/data/file.ext]` — [what this file contains] (version: `<tag or SHA>`, from: `<preprocessing pipeline version>`)
  - `[exact/relative/path/to/another/file.ext]` — [what this file contains] (version: `<tag or SHA>`, from: `<preprocessing pipeline version>`)
**Outputs:**
  - `[exact/relative/path/to/output/file.ext]` — [what this file contains]
**Config:** `[exact/relative/path/to/config.yaml]`
**Seed:** [integer, e.g. 42]
**Expected Runtime:** [rough estimate, e.g. "~5 min on CPU", "~2 hr on GPU"]

- [ ] Step 1: Verify prerequisites
      Confirm all **Inputs** exist and are non-empty. Verify file hash(es) match the version registered in `eureka:hypothesis-first` (SHA256 comparison). Record descriptive statistics of input data (N, mean, std, NaN rate, label distribution) to a log file. If this is the first experiment in the plan, generate Table 1 (demographics / key variables) programmatically. If any check fails, halt and document the gap. See `docs/references/data-checklist.md` for Table 1 template.
- [ ] Step 2: Save config with seed
      Write the config file to **Config** path. Include the seed value, all hyperparameters, and a `generated_at` timestamp. Commit the config before running.
- [ ] Step 3: Run
      [exact shell command with all arguments, e.g.:]
      `python src/models/train.py --config configs/exp_01_baseline.yaml --seed 42 --output results/exp01/`
- [ ] Step 4: Verify outputs
      Confirm **Outputs** exist. Spot-check: [exact check, e.g. "open results/exp01/metrics.json and confirm `val_r2` key is present and finite"].
- [ ] Step 5: Log to experiment record
      Append to `docs/eureka/records/experiment-log.md`:
      - Experiment N name
      - Date/time run
      - Git commit hash of code
      - Config path
      - Primary metric value observed
      - Pass/fail against pre-registered threshold
- [ ] Step 6: Commit results + config
      `git add [config path] [output paths] docs/eureka/records/experiment-log.md`
      `git commit -m "exp N: [name] — primary metric = [value]"`
```

---

## No Placeholders Rule

The same discipline as `writing-plans` applies here. Every vague phrase must be resolved to something executable.

| Vague (not allowed) | Concrete (required) |
|---|---|
| "Run the analysis" | `python src/analysis/run_glm.py --input data/processed/cohort_A.csv --formula "y ~ x1 + x2 + age" --output results/glm_cohort_A.csv` |
| "Check the results" | Open `results/glm_cohort_A/summary.json`, confirm `p_value_x1 < 0.05` and `effect_size_cohen_d > 0.2` |
| "Save the output" | Write to `results/exp02/roc_curve.png` (300 dpi, PNG) and `results/exp02/auc_score.txt` (plain text, one float) |
| "Preprocess the data" | `python src/data/preprocess.py --input data/raw/cohort_2024.csv --output data/processed/cohort_clean.csv --config configs/preprocess_v1.yaml` |
| "Use the cohort data" | `data/processed/cohort_v2.4.0/outcome_baseline.csv` (N=47, version tag v2.4.0, SHA256 `abc1234...`, from preprocessing pipeline `preprocess@v2.4.0`) |
| "Use a reasonable seed" | `--seed 42` |
| "Standard significance" | `alpha = 0.05, two-tailed, Bonferroni correction for N=3 comparisons, corrected threshold = 0.0167` |

If you find yourself writing a placeholder, stop and ask the user for the missing concrete detail.

---

## Self-Review Checklist

After drafting the full plan, run through this checklist and report findings:

### Coverage Check
- [ ] Every hypothesis in the design has at least one experiment that directly tests it
- [ ] Every primary outcome measure has an experiment that produces it
- [ ] Every secondary/exploratory analysis is listed (even if lower priority)
- [ ] Control/baseline conditions are included where needed

### Placeholder Scan
- [ ] No step says "run the analysis" without an exact command
- [ ] No step says "check results" without an exact metric and threshold
- [ ] No step says "save output" without an exact path and format
- [ ] No seed is listed as "TBD" or "any"
- [ ] No input path contains `[...]` unfilled brackets
- [ ] No output path contains `[...]` unfilled brackets

### Path Consistency Check
- [ ] All input paths exist or are clearly documented as "will be created by Experiment M"
- [ ] No two experiments write to the same output path unless intentional (documented)
- [ ] Config paths follow a consistent naming convention (e.g., `configs/exp_NN_<name>.yaml`)

### Reproducibility Check
- [ ] Every experiment has an explicit seed
- [ ] Every experiment has a config file path (not inline parameters)
- [ ] Every experiment has a commit step

Report results as:
```
Self-review complete.
Coverage: [N/N items passed]
Placeholders found: [0 / list any found]
Path issues: [0 / list any found]
Reproducibility: [N/N items passed]
```

If any issues are found, fix them before presenting the final plan.

---

## Dispatching the Experiment Plan Reviewer

After the inline Self-Review Checklist passes, dispatch a fresh subagent reviewer to verify the plan is executable by someone with no prior context. Inline self-review is the writer checking their own work in the same session — a fresh subagent brings fresh eyes and catches placeholder/coverage/buildability issues that the main agent overlooked.

1. Locate the reviewer prompt at `skills/experiment-design/experiment-plan-reviewer-prompt.md`
2. Fill the placeholders:
   - `{PLAN_PATH}` → the path to the plan file you just wrote
   - `{DESIGN_DOC_PATH}` → the approved design document from `research-brainstorming`
   - `{REGISTRATION_PATH}` → the registration file from `hypothesis-first` (if applicable)
3. Dispatch via the Task tool (`general-purpose` subagent) with the filled prompt
4. Wait for the reviewer to return with `Status: Approved` or `Status: Issues Found`

**Acting on the reviewer's response:**

- **`Status: Approved`** → proceed to the Save Location step and report the plan complete to the user
- **`Status: Issues Found`** → address each issue in the plan document (fill missing commands, add seeds, fix paths, add missing experiments for uncovered hypotheses, correct header fields). Re-dispatch the reviewer. Repeat until `Approved`. Do NOT report the plan complete to the user until the reviewer approves.

If the reviewer flags the same issue twice after attempted fixes, escalate to the user: describe the issue and ask for guidance.

---

## Save Location

Save the completed plan to:

```
docs/eureka/plans/YYYY-MM-DD-<topic>-experiments.md
```

Where:
- `YYYY-MM-DD` is today's date
- `<topic>` is a short kebab-case descriptor matching the design doc topic (e.g., `model-baseline-comparison`, `feature-ablation`)

Example: `docs/eureka/plans/2026-04-12-model-baseline-comparison-experiments.md`

After saving, report the path to the user.

---

## Integration

**Called by:** `hypothesis-first` — after a hypothesis is registered and a design is approved, this skill operationalizes it.

**Pairs with:** `requesting-research-review` — after experiments are run, the results log feeds into the review skill for rigor assessment.

**Reference:** `docs/references/data-checklist.md` — input versioning, Table 1 template, preprocessing pipeline requirements.

**Reference:** `docs/references/registration-lifecycle.md` — contingency inheritance rules, amendment workflow when plan needs to differ from registration.

**Workflow position:**
```
hypothesis-first → [design approval] → experiment-design → [execution] → requesting-research-review
```

---

## Example Output (abbreviated)

```markdown
# Model Baseline Comparison Experiment Plan
**Goal:** Determine whether Model B outperforms Model A on outcome Y at 24-month follow-up.
**Design Reference:** docs/eureka/designs/2026-04-10-model-baseline-comparison-design.md
**Registered Hypothesis:** H1: Model B Pearson r with observed outcome Y at 24-month follow-up > Model A Pearson r (one-tailed, alpha=0.05).
**Primary Outcome:** Pearson r between predicted and observed outcome Y at 24 months, held-out test set (N=47).
**Analysis Plan:** Paired t-test on subject-level r values (Model B vs Model A), one-tailed, alpha=0.05, no correction (single comparison).
---

### Experiment 1: Model A Baseline
**Depends on:** none
**Inputs:**
  - `data/processed/cohort_v1/features_train.npy` — training feature matrix, shape (376, 84)
  - `data/processed/cohort_v1/outcome_y_baseline.csv` — baseline outcome per subject, N=47 test subjects
**Outputs:**
  - `results/exp01_modelA/predicted_y_24mo.csv` — predicted outcome per subject
  - `results/exp01_modelA/metrics.json` — per-subject Pearson r and group mean
**Config:** `configs/exp01_modelA_baseline.yaml`
**Seed:** 42
**Expected Runtime:** ~3 min on CPU

- [ ] Step 1: Verify prerequisites
      Confirm `data/processed/cohort_v1/features_train.npy` exists and shape is (376, 84).
      Confirm `data/processed/cohort_v1/outcome_y_baseline.csv` has 47 rows.
- [ ] Step 2: Save config with seed
      Write `configs/exp01_modelA_baseline.yaml` with fields: model=ModelA, seed=42, lr=0.001, epochs=100, generated_at=[timestamp].
      `git add configs/exp01_modelA_baseline.yaml && git commit -m "config: exp01 Model A baseline"`
- [ ] Step 3: Run
      `python src/models/run_model_a.py --config configs/exp01_modelA_baseline.yaml --features data/processed/cohort_v1/features_train.npy --outcome data/processed/cohort_v1/outcome_y_baseline.csv --output results/exp01_modelA/`
- [ ] Step 4: Verify outputs
      Confirm `results/exp01_modelA/metrics.json` exists. Open it and confirm `mean_pearson_r` is a finite float between -1 and 1.
- [ ] Step 5: Log to experiment record
      Append to `docs/eureka/records/experiment-log.md`: Experiment 1, date, git hash, config path, mean_pearson_r value.
- [ ] Step 6: Commit results + config
      `git add results/exp01_modelA/ docs/eureka/records/experiment-log.md`
      `git commit -m "exp01: Model A baseline — mean_pearson_r = [value]"`
```
