---
name: rs-assess
description: >
  Assess the quality and situational fitness of an existing skillset.
  Interviews the operator for operational and methodological signal
  about the target skillset, runs agent-autonomous structural checks,
  evaluates fitness functions against the target's current context,
  and selects refinement strategies based on what the assessment
  reveals. Produces a quality assessment with evaluable predicates.
metadata:
  author: monkeypants
  version: "0.2"
  skillset: refine-skillset
  stage: "1"
  freedom: medium
---

# Skillset Quality Assessment

You are assessing the quality and situational fitness of an existing
consulting skillset. This is a diagnostic phase — you are finding
what needs improvement, not making changes yet.

The **target skillset** is whatever skillset the operator wants to
assess (e.g. wardley-mapping, business-model-canvas). You provide
the assessment methodology; the target provides the subject matter.

## References

Load references progressively as needed:
- `references/executive.md` — L0: assessment purpose, 7 pipeline
  coherence criteria. Load first for decision framing.
- `references/domain-model.md` — L1: four dimensions, entities,
  vocabulary. Load for writing assessment artifacts.
- `references/methodology.md` — L2: five-phase process, smell
  catalogue, strategy selection table. Load for execution detail.
- `references/agentskills-way.md` — Skill file quality standard.
  Load during Step 4 (methodological assessment).
- `references/strategies/*.md` — L3 detail. Load on demand based
  on what the assessment reveals (see Step 5).

## Prerequisites

The operator must identify the **target skillset** being assessed.
Check that:

1. The target skillset exists:
   ```bash
   uv run practice skillset show --name {target}
   ```
2. The target has an implemented pipeline (not just a prospectus)
3. Organisation research exists at `resources/index.md` in the
   project directory

Additional context to gather before starting:
- Read any existing decision logs from the target's engagements
  (`clients/{org}/engagements/*/decisions.json`) to understand
  what has been agreed previously
- Read any review documents from prior `review` skill outputs
- Check the target's source: `uv run practice source list` to
  determine whether it is commons, personal, or partnership

If the target skillset does not exist or is not implemented, this
skill cannot proceed.

## Step 1: Structural scan of the target (agent-autonomous)

This step requires no human input. Run mechanical verification
and record findings.

### Conformance tests

Run the conformance tests against the target:

```bash
uv run pytest -m doctrine -v 2>&1 | grep {target_bc_package}
```

Run skill file conformance tests:

```bash
uv run pytest -m doctrine -k TestSkillFileConformance -v
```

### Pipeline mechanics

Check each structural property of the target pipeline:
- Do gates chain correctly (prerequisite of stage N = produces
  of stage N-1)?
- Are stage descriptions unique?
- Does the slug pattern contain `{n}`?

### BC completeness

- Does `__init__.py` export SKILLSETS and PRESENTER_FACTORY?
- Does `presenter.py` implement the ProjectPresenter protocol?
- Does `tests/test_presenter.py` exist with doctrine-marked tests?
- Do skill symlinks exist in `.claude/skills/`?

### Skill file structure

For each skill in the target pipeline:
- Does `.claude/skills/{skill-name}` symlink exist?
- Does SKILL.md have valid frontmatter (name matches dir, ≤64 chars)?
- Is description ≤1024 chars?
- Is SKILL.md under 500 lines?
- Are bash scripts in scripts/ executable?

### Pipeline coherence (mechanically-testable subset)

Apply criteria 1, 2, and 6 from the 7-criteria framework
(see `references/executive.md`):
- **Decision point validity**: Is there a gate at each stage
  boundary? (Mechanical check — whether the decision is genuine
  requires human input in Step 2.)
- **Information timing**: Does each stage's prerequisite gate
  contain the information the stage needs?
- **Feedback integration**: Does the pipeline definition allow
  iteration, or is it strictly one-directional?

Record all findings to `assessment/structural.md`.

**No human gate** — proceed directly to Step 2 regardless of
structural results.

## Step 2: Operational interview about the target (human-primary)

The operator is the primary signal source for this step. Present
structural findings for context, then conduct a structured interview
about the operator's experience using the target skillset.

### Structured probes

Present these questions and record responses verbatim:

1. "Which stages in the target pipeline feel most useful to you?
   Which feel like they're just process?"
2. "Where do you find yourself working around the process — doing
   things the skill file doesn't account for?"
3. "Which gates do you carefully evaluate versus rubber-stamp?"
4. "Has the context this skillset serves changed since it was
   created? Different users, different market, different tools?"
5. "Where does the agent load material that doesn't end up
   helping the work?"
6. "When you use this skillset with clients, where do negotiations
   stall or feel unproductive?"
7. "Are there things you know about this domain that the skill
   files don't capture?"

### Recording

Capture operator responses as close to verbatim as possible. Do
not summarise or interpret at this stage — raw signal is more
valuable than premature synthesis.

Record to `assessment/operational.md`.

## Step 3: Fitness evaluation of the target (human + agent)

Apply the 7 pipeline coherence criteria from `references/executive.md`
against the target, using the operational interview as evidence.

### Criteria evaluation

For each of the 7 criteria:

| # | Criterion | Evidence source | Finding |
|---|-----------|----------------|---------|
| 1 | Decision point validity | Structural scan + interview Q3 | ... |
| 2 | Information timing | Structural scan + interview Q1 | ... |
| 3 | Human leverage | Interview Q1, Q3, Q7 | ... |
| 4 | Cycle time proportionality | Interview Q2 | ... |
| 5 | Situational fit | Interview Q4 | ... |
| 6 | Feedback integration | Structural scan + interview Q6 | ... |
| 7 | Vertical completability | Interview Q2, Q6 | ... |

### Fitness functions

Formulate evaluable predicates about the target's fitness. Use
template functions from `references/strategies/fitness-functions.md`
as starting points, adapted to the specific target.

Each fitness function:
- States a testable predicate
- Specifies the evidence needed to evaluate it
- Returns pass / fail / partial (not a rating scale)
- Cites the evidence for its result

Present proposed fitness functions to the operator. Ask whether
they test the right things — the operator may identify fitness
concerns the criteria don't capture.

Record to `assessment/fitness.md`.

## Step 4: Methodological assessment of the target (collaborative)

Agent reads the target's artifacts; human provides tacit domain
knowledge that artifacts don't capture.

### Artifact review

Read the target skillset's:
- Skill files (SKILL.md for each pipeline stage)
- Reference files (bytecode hierarchy, if any)
- Research and design documents (if from a `new-skillset` project)
- Bash wrapper scripts
- Presenter and test files

### Domain fidelity

- Does the methodology match the domain's actual practices?
- Are domain terms used precisely and consistently across skill files?
- Has the domain evolved since the skillset was created?

Ask the operator: "Is there domain knowledge you rely on when
using this skillset that isn't captured in the skill files?"

### Semantic bytecode quality

If the target has reference files:
- Do they follow the L0-L3 hierarchy?
- Are token budgets respected?
- Does progressive disclosure work (each level adds without
  contradicting)?
- Is vocabulary precise (no ambiguous paraphrasing)?

### Skill file quality

Evaluate each skill file against `references/agentskills-way.md`:
- Does the description enable correct selection?
- Are prerequisites checkable?
- Are steps ordered with named artifacts?
- Is the gate protocol propose-negotiate-agree?
- Are references one level deep?

### Smell detection

Apply the smell catalogue from `references/methodology.md` to the
target's artifacts:
- Structural smells: phantom gate, orphan reference, brittle join
- Methodological smells: parrot methodology, token bloat, vocabulary
  drift
- Operational smells: rubber stamp, negotiation desert, workaround
  prevalence
- Pipeline smells: ceremony debt, horizontal lock, missing feedback
  loop

For each detected smell, record: name, evidence, what it indicates.

### Deliverable quality

For each deliverable the target produces:
- Is the format clearly specified?
- Are quality criteria testable?
- Does the presenter render them correctly?

Record findings to `assessment/methodological.md`.

## Step 5: Select and apply refinement strategies

Based on what Steps 1-4 reveal about the target, select which
strategies from `references/strategies/` are relevant.

### Strategy selection

Consult the strategy selection table in `references/methodology.md`
(L2). Match assessment findings to selection criteria:

| What assessment reveals | Load strategy |
|------------------------|---------------|
| Passes checks but operator reports friction | smell-detection, human-leverage-audit |
| Pipeline designed for different context | situational-scan |
| Process overhead disproportionate to changes | vertical-slice-test |
| Agent performance or context window issues | context-efficiency |
| Conformant but quality uncertain | fitness-functions, outcome-alignment |
| Operator rubber-stamps gates | human-leverage-audit, vertical-slice-test |

Always load `fitness-functions` — it replaces maturity ratings with
evaluable predicates and is applicable to every assessment.

### Strategy execution

For each selected strategy:
1. Read the strategy file from `references/strategies/`
2. Follow its method against the target skillset
3. Record findings in the format the strategy specifies

Strategies are self-contained — each defines its own method,
inputs, and output format. Multiple strategies can be applied to
the same target.

Record all strategy findings to `assessment/strategies.md`, with
one section per strategy applied.

## Step 6: Synthesise assessment of the target

Combine findings from all dimensions into a single assessment
document.

### Assessment template

Write `assessment/assessment.md`:

```markdown
# Quality Assessment: {Target Skillset}

## Summary

{2-3 paragraph overview: what the target does well, where it falls
short, and what the assessment methodology revealed. Frame around
fitness for current purpose, not abstract quality.}

## Fitness Functions

| Predicate | Dimension | Result | Evidence | Confidence |
|-----------|-----------|--------|----------|------------|
| {name} | {structural/fitness/methodological/operational} | Pass/Fail/Partial | {citation} | High/Med/Low |

## Findings by Dimension

### Structural
{Findings from Step 1 — cite specific test results and pipeline
properties.}

### Operational
{Findings from Step 2 — cite operator statements. Preserve the
operator's language.}

### Fitness
{Findings from Step 3 — cite criteria evaluations and fitness
function results.}

### Methodological
{Findings from Step 4 — cite artifact evidence and smell
detections.}

## Strategies Applied

{For each strategy loaded in Step 5, summarise key findings and
reference the full strategy output in assessment/strategies.md.}

## Prioritised Issues

### Critical (blocks effective use)

1. **{Issue}** — {description, evidence, affected fitness functions}

### Important (degrades quality)

1. **{Issue}** — {description, evidence, affected fitness functions}

### Minor (polish)

1. **{Issue}** — {description, evidence}

## Recommendations

{Ordered list of improvements, most impactful first. Each
recommendation references specific issues and fitness functions
above. Frame recommendations as changes that would flip fitness
function results from fail/partial to pass.}
```

Do not use Good/Adequate/Poor ratings. The fitness function table
replaces the scorecard — results are evaluable predicates, not
subjective assessments.

## Step 7: Present and negotiate

Present the assessment to the operator. Ask targeted questions:

1. "Does this assessment match your experience using this skillset?"
2. "Are there findings I've missed — things you know are problems
   that didn't surface in the assessment?"
3. "Do the priority ratings feel right? Should any critical be
   downgraded, or any minor promoted?"
4. "Are there constraints on what we can change (existing projects
   in flight, external dependencies, partnership obligations)?"
5. "Do the fitness functions test the right things? Would you
   change any predicates?"

Incorporate feedback. If the operator identifies new findings,
classify them by dimension and severity. If they challenge fitness
function formulations, revise the predicates.

## Step 8: Iterate and agree

When the operator confirms the assessment is complete:

1. Write `assessment.agreed.md` — the final agreed assessment
2. Record the decision:
   ```
   skillset_engineering/skills/rs-assess/scripts/record-assessment-agreed.sh \
     --client {org} --engagement {engagement} --project {slug} \
     --field "Target={target skillset}" \
     --field "Critical={count}" \
     --field "Important={count}" \
     --field "Minor={count}" \
     --field "Strategies={comma-separated list of strategies applied}" \
     --field "Fitness functions={count pass}/{count total}"
   ```

## Monotonic improvement property

The refine-skillset methodology is designed so that **every iteration
improves quality**. This stage's output is a prioritised issue list
with evaluable fitness functions. The next stage (rs-plan) selects
the highest-impact improvements. The stage after (rs-iterate)
executes them. Even a single iteration cycle must leave the skillset
measurably better — where "measurably" means at least one fitness
function flips from fail/partial to pass.

A vertical slice test (see `references/strategies/vertical-slice-test.md`)
can verify this property: take one finding from identification through
to fix and confirm the corresponding fitness function improves.

## Completion

When `assessment.agreed.md` is written, tell the operator the next
step is `rs-plan` to create an improvement plan targeting the most
impactful issues identified in this assessment.
