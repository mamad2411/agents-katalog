---
name: research-idea-validator
description: Help a CS or AI PhD student turn a rough research idea into a validated next-step decision using the FIVE+C framework. Use this skill whenever the user says they have a research idea, wants to know whether an idea is worth pursuing, needs help choosing between project directions, is preparing to pitch an idea to an advisor or senior student, or feels unsure whether a project is too incremental, too ambitious, already solved, hard to evaluate, or missing resources.
argument-hint: "[idea-notes-or-project-dir] [--area <area>] [--decision pursue|revise|park|kill]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Research Idea Validator

Turn a rough research idea into a decision: pursue, revise, park, or kill. This skill is for early project steering before implementation and heavy experiments.

Use this skill when:

- the user has a research idea and wants to know whether it is worth doing
- a project direction needs a go/no-go decision
- novelty, feasibility, evaluation, or reviewer risk is unclear
- the user is choosing between multiple ideas
- the user wants to prepare an advisor pitch or project proposal
- early results suggest the project may need repositioning

Do not treat this as generic brainstorming. The goal is to decide whether an idea can become a researchable project and publishable paper.

Pair this skill with:

- `research-project-memory` when the decision should persist into a project-level claim, risk, action, or decision board
- `literature-review-sprint` when closest work or novelty risk is unclear
- `algorithm-design-planner` when the idea is promising but the method shape is underspecified
- `experiment-design-planner` when the claim is clear and needs a minimum validation plan
- `paper-reviewer-simulator` only after a draft, proposal, or evidence package exists
- `conference-writing-adapter` after there is enough substance to shape into a venue-specific paper

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── decision-rules.md
    ├── five-plus-c-rubric.md
    ├── memory-guidelines.md
    ├── paper-shapes.md
    └── reviewer-risk-patterns.md
```

## Progressive Loading

- Always read `references/five-plus-c-rubric.md` and `references/decision-rules.md`.
- Read `references/paper-shapes.md` when deciding the contribution type or target paper form.
- Read `references/reviewer-risk-patterns.md` when forecasting rejection risks or advisor objections.
- Read `references/memory-guidelines.md` when saving or reusing idea/project knowledge.
- If the target repo has `memory/` or the user asks for project memory, use `research-project-memory` writeback conventions for decision, risk, and action entries.
- If novelty or current competition matters, verify with current sources using web search or user-provided papers.

## Core Principles

- Separate an interesting idea from a researchable project and a publishable paper.
- Make a decision, not a list of encouragements.
- State the best possible paper claim before judging the idea.
- Identify the closest-work risk early.
- Prefer small falsifying checks over large ambiguous implementations.
- Treat feasibility as scientific: if the needed evidence cannot be produced, the idea is not ready.
- Surface reviewer objections while the project is still cheap to change.
- Keep the output useful even when the decision is `kill`.

## Step 1 - Capture the Idea

Extract or ask for:

- one-sentence idea
- target area and audience
- intended contribution type, if known
- current motivation or pain point
- proposed technical move
- available code, data, compute, collaborators, and time
- known related work
- desired venue or paper type, if any
- current evidence, if any

If the idea is vague, rewrite it into:

```text
We want to solve [problem] for [setting] by [technical move], expecting [measurable benefit] over [baseline/previous approach].
```

If that sentence cannot be written, the likely decision is `revise`.

## Step 2 - Apply FIVE+C

Read `references/five-plus-c-rubric.md`.

Evaluate:

- `Framing`: what problem the idea solves and what claim it could support
- `Importance`: why the problem matters to the field or target venue
- `Validity`: whether the core assumption is plausible and falsifiable
- `Evidence`: what evidence would convince a skeptical reviewer
- `Execution`: whether the user can obtain that evidence with available resources
- `Competition`: closest classic, recent, and concurrent work

Score each dimension qualitatively:

```text
strong / medium / weak / unknown
```

Unknown is a risk, not a neutral value.

## Step 3 - Choose the Paper Shape

Read `references/paper-shapes.md` when the contribution type is unclear.

Classify the best paper form:

- theory
- method
- benchmark
- dataset
- empirical analysis
- systems
- application
- negative result
- position/interpretation
- hybrid

Then state:

- strongest possible paper claim
- weakest unavoidable claim
- what the paper must prove, measure, or demonstrate
- what claims to avoid

If the idea only supports a weak claim, prefer `revise` or `park` over forcing a method paper.

## Step 4 - Forecast Reviewer Attacks

Read `references/reviewer-risk-patterns.md`.

List the most likely reviewer objections:

- novelty too small
- problem not important
- closest work already covers it
- method is a minor engineering tweak
- evaluation does not match the claim
- baseline is weak or under-tuned
- evidence is too expensive to obtain
- assumptions are unrealistic
- failure modes are unaddressed
- contribution type does not fit the target venue

For each major attack, state whether it is:

- fatal unless solved
- fixable by reframing
- fixable by literature review
- fixable by algorithm design
- fixable by experiment design
- acceptable limitation

## Step 5 - Decide

Read `references/decision-rules.md`.

Choose exactly one:

- `pursue`: start building the project now
- `revise`: promising, but must change framing, method, evaluation, or positioning first
- `park`: potentially valuable, but blocked by timing, resources, missing literature clarity, or missing prerequisites
- `kill`: unlikely to become a worthwhile project or paper

Do not choose `pursue` unless there is a plausible minimum viable project and a clear falsification path.

## Step 6 - Define the Minimum Viable Project

For `pursue` or `revise`, define:

- minimal version of the idea
- killer experiment, theorem, analysis, or prototype
- primary baseline or comparison
- first falsification test
- expected time-to-signal
- required resources
- kill criteria

For `park` or `kill`, state what new information would change the decision.

## Step 7 - Route to the Next Skill

Recommend the next skill:

- `literature-review-sprint`: closest work or novelty is uncertain
- `algorithm-design-planner`: method form, assumptions, or mechanism are unclear
- `experiment-design-planner`: claim is clear and needs a validation plan
- `paper-positioning-planner`: evidence exists but the contribution story is unclear
- `run-experiment`: only when the validation experiment is already well specified

If the next skill does not exist yet in this repo, still name the intended function and provide the immediate manual next step.

## Step 8 - Write the Validation Report

Return or save a concise report with:

```markdown
# Research Idea Validation

## One-Sentence Idea

## Intended Contribution Type

## Decision
Decision: pursue / revise / park / kill
Confidence: low / medium / high

## Why This Decision

## FIVE+C Assessment
| Dimension | Rating | Evidence | Risk |
|---|---|---|---|

## Best Possible Paper Claim

## Main Novelty Hypothesis

## Closest Work to Check

## Minimum Viable Project

## Killer Experiment or Analysis

## Reviewer Attack Forecast

## Kill Criteria

## Next 3 Actions

## Recommended Next Skill

## Memory Update
```

If saving to a project and no path is given, use:

```text
docs/ideas/idea_validation_YYYY-MM-DD_<short-name>.md
```

## Step 9 - Write Back to Project Memory

If the project uses `research-project-memory`, update the smallest useful set of entries:

- `memory/decision-log.md`: idea decision, why, alternatives, and revisit trigger
- `memory/claim-board.md`: best possible paper claim as `planned`, `active`, `revised`, `parked`, or `cut`
- `memory/risk-board.md`: novelty, feasibility, evaluation, and reviewer risks
- `memory/action-board.md`: next 3 actions and recommended next skill
- `memory/current-status.md`: current focus if the idea changes the project direction

Use certainty labels:

- `user-stated` for the user's idea and constraints
- `inferred` for reviewer risks and paper-shape diagnosis
- `needs-verification` for closest-work or feasibility assumptions that still need checking

Do not overwrite old idea decisions. Add a new decision entry that supersedes the previous one when the idea changes.

## Final Sanity Check

Before finalizing:

- the idea is rewritten as a testable project sentence
- a single decision is chosen
- the decision follows the explicit rules
- novelty risk and closest-work risk are stated
- the minimum viable project is small enough to run before heavy investment
- reviewer attacks are specific, not generic
- kill criteria are concrete
- next actions are operational
