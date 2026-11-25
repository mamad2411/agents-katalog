---
name: plan-analysis
description: User describes a research question — what they're trying to predict or explain, what variables are involved, and what the study design looks like — and wants a recommended statistical model with a hierarchical test sequence from null to fully specified. Use this skill whenever the user asks which statistical test or model to use, wants to plan an analysis, needs help choosing between ANOVA/regression/mixed effects/CCA/factor analysis, or describes outcome and predictor variables and wants a structured modelling approach.
argument-hint: [outcome variable(s) and predictor description]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob
---

# Skill: plan-analysis

Route a research question to the right statistical family and produce a hierarchical
model sequence — null through fully specified — that the user can run and refine.

Reference files (load as directed below):
- `${CLAUDE_PLUGIN_ROOT}/references/test-selection.md` — decision tree: outcome × predictors × design → method
- `${CLAUDE_PLUGIN_ROOT}/references/model-hierarchy.md` — null → full model patterns and comparison tests (R/Python/Julia)
- `${CLAUDE_PLUGIN_ROOT}/references/anova-family.md` — ANOVA, ANCOVA, RM-ANOVA, MANOVA, MANCOVA
- `${CLAUDE_PLUGIN_ROOT}/references/regression-glm.md` — OLS, logistic, Poisson, ordinal, LME, GLMM
- `${CLAUDE_PLUGIN_ROOT}/references/multivariate.md` — CCA, RDA, PERMANOVA, multivariate regression
- `${CLAUDE_PLUGIN_ROOT}/references/factor-analysis.md` — EFA, CFA, PCA, SEM skeleton
- `${CLAUDE_PLUGIN_ROOT}/../../references/qc-metrics.md` — shared diagnostics and assumption checks

---

## Phase 0: Collect the four intake answers

Parse from `$ARGUMENTS` where possible. Ask only for what is missing.

1. **Outcome(s)** — what is being predicted or explained?
   - How many outcome variables? (one or multiple)
   - What type: continuous, binary (yes/no), count/rate, ordinal (ranked), nominal,
     or "no outcome — I want to find structure in the variables"?

2. **Predictors** — what explains the outcome?
   - Are they categorical (groups, conditions, time points), continuous (scores,
     measurements), or a mix?
   - Is there a variable you want to control for but are not interested in testing
     (a covariate)?

3. **Design** — what is the data structure?
   - Are observations independent, or do subjects contribute multiple rows?
     (repeated measures, longitudinal, subjects nested in sites/families)
   - Is this a designed experiment (randomised groups) or observational?

4. **Language preference** — R (default), Python, or Julia?

If the user already described the question in their message, extract these answers
from context before asking. Only ask about genuinely missing information.

---

## Phase 1: Navigate the decision tree

Load `${CLAUDE_PLUGIN_ROOT}/references/test-selection.md`.

For regression-family analyses, also consult
`${CLAUDE_PLUGIN_ROOT}/references/worked-examples.md` for annotated workflows
covering simple regression, hierarchical ΔR², curvilinear, categorical coding,
and interaction/simple-slopes patterns (R/Python/Julia).

Follow the tree to identify:
- The recommended **statistical family** (e.g., "linear mixed effects regression")
- The corresponding **reference file** to load next
- Any **method-specific questions** flagged by the tree

Tell the user the recommended family in one sentence and why (what features of their
design drove the choice). If two methods are plausible, name both and explain the
deciding factor, then ask the user which fits their intent.

---

## Phase 2: Load the method reference and ask method-specific questions

Load the reference file identified in Phase 1. Read the "Key decisions" section.
Ask only questions whose answers are needed to write the model formula. Examples:

- ANOVA: "What is the reference / baseline group?" "Are any factors within-subject?"
- Regression: "Which predictors are you most interested in testing?" "Should any
  continuous predictors be mean-centred or standardised?"
- Mixed effects: "What is the grouping variable for the random effect?" "Do you
  expect random slopes, or only a random intercept?"
- CCA: "Which variables form Set A (predictors) and Set B (outcomes)?"
- EFA: "Do you have a hypothesis about how many factors there are?"

---

## Phase 3: Confirm the model hierarchy

Load `${CLAUDE_PLUGIN_ROOT}/references/model-hierarchy.md` for the code patterns.

Present the proposed model sequence as a numbered list:

```
Level 0 (null):        outcome ~ 1
Level 1 (covariates):  outcome ~ age + site
Level 2 (main effects): outcome ~ age + site + group + score
Level 3 (interaction):  outcome ~ age + site + group * score
```

For each step, name the comparison test (F-test, likelihood ratio, Pillai's trace,
etc.) and what a significant result means in plain language.

Ask: "Does this sequence match what you want to test? Any levels to add, remove,
or reorder?"

Incorporate corrections before Phase 4.

---

## Phase 4: Emit the model sequence as runnable code stubs

Generate a script skeleton in the user's chosen language. Use the code templates
from the method reference and `model-hierarchy.md`. The output should be:

- One model object per level, with the formula filled in from the confirmed hierarchy
- Comparison tests between adjacent levels (LRT, `anova()`, `car::Anova()`, etc.)
- Calls to the key diagnostic checks from `qc-metrics.md` for this method family
- Comments explaining what each level tests and what to look for in the output

The script is a starting point, not a finished analysis. The user should be able
to copy it, point it at their data, and run it immediately.

---

## Constraints

- **Never recommend a method without explaining why** — the user needs to understand
  the choice, not just receive a label.
- **Never skip the null model.** Every sequence starts at Level 0. Skipping it
  removes the ability to attribute explained variance to specific terms.
- **If the design is ambiguous, ask.** A wrong random-effects structure or a
  misidentified outcome type produces valid-looking but wrong results.
- **Flag assumption violations early.** If the user's description implies likely
  violations (e.g., heavily skewed outcome → mention GLM alternatives; small N
  with many predictors → mention regularisation or dimensionality reduction first),
  name the concern before committing to a model.
- **Point toward a separate skill for complex methods.** SEM with latent paths,
  Bayesian modelling, and machine learning pipelines are out of scope here. Name
  them and say "consider a dedicated skill or workflow for this."
