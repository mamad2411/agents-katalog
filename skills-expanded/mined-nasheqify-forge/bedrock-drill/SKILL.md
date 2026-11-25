---
name: bedrock-drill
aliases: [rfp]
description: >
  Recursive first-principles drill with bottom-up synthesis.
  Decomposes problems down to axiom level (physics / logic /
  values), then builds answers from the bottom up.
  Domain-independent — technical design as well as strategy, career,
  consulting, learning or everyday decisions.
  Triggers when a problem must be decomposed to axiom level before synthesis: a question is stuck, goals or values conflict, a recurring pattern is unclear, repeated why-questions lead to unexamined assumptions, or first principles are asked for explicitly (also frame step 2, solve override); NOT for simple factual questions, rewording, summaries, clearly specified execution or routine analysis with a known frame.
status: active
relevant_for: ["solution-expert"]
invocation:
  primary: sub-skill
  secondary: [user-facing, workflow-step]
disable-model-invocation: false
modes: [focused, broad, exhaustive]
uses: [_protocols/analysis-mode-gate]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.
Without Buddy (plugin): if this session holds no Buddy boot entry, run `python3 <root>/scripts/forge_setup.py offer-check` once, as its own call (`<root>`: two levels above this skill's folder); if it prints a line, pass that offer to the user in one sentence, then continue with this skill.


# Skill: bedrock_drill

A recursive deep-drill tool. Decomposes a problem into assumptions,
drills the load-bearing one further until bedrock (physics / logic
/ chosen values) is reached. Then builds the answer layer by layer
from the bottom up. Complement to `frame` (breadth), not a
replacement. Detail mechanics: `REFERENCE.md`.

## Standalone boundary

Supplied problem/context suffice; no Git/user repository, development workflow,
task or durable destination is required. Return the report inline with uncertainty.
The caller owns optional persistence through continuity; a proposed conclusion is
not a user decision. Independent review, when selected, uses caller-owned private
temporary transport per `skills/_protocols/dispatch-template.md`. Existing modes,
max_depth and output_format remain unchanged. Development references below apply
only when that caller is explicitly selected.

## Who runs it

Buddy (primary). v0.2.0: standalone + as step 2 inside `frame`.
- **Solve context:** ALWAYS (focused as default mode, upgrade for
  foundation / cross-layer).
- **Deep mode (frame):** MUST invoke.
- **User-explicit:** callable standalone at any time.

## Input

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| problem | yes | Raw problem description | — |
| context | no | Additional context | — |
| max_depth | no | Maximum recursion depth | 5 |
| mode | no | `focused` \| `broad` \| `exhaustive` | focused |
| output_format | no | `narrative` \| `tree` | narrative |

## Output: axiom-tree report

5 sections: (1) **Axiom tree** — nodes with core label, status,
score. (2) **Bedrock map** — axioms typed; values marked as "YOUR
CHOICE". (3) **Blind spots (user input)** — required prompt for
assumptions structurally invisible to the LLM. (4) **Bottom-up
derivation** — per layer "Given X → Y because Z", with an
integrity check. (5) **Axiom alternatives** — at least one "What if
the value were different?" with a partial re-run.

## Contract

### INPUT
- **Required:** raw problem description.
- **Optional:** context — additional context.
- **Optional:** max_depth — maximum recursion depth (default: 5).
- **Optional:** mode — focused | broad | exhaustive (default:
  focused).
- **Optional:** output_format — narrative | tree (default:
  narrative).
- **Context:** primarily called from `frame` step 2. Standalone
  use is also allowed.

### OUTPUT
**DELIVERS:**
- Axiom tree: nodes with core label, status (bedrock / drilled /
  pruned), score.
- Bedrock map: axioms typed (physics / logic / value); values
  marked as YOUR CHOICE.
- Blind spots: required prompt to the user for LLM-invisible
  assumptions.
- Bottom-up derivation: per layer "Given X → Y because Z" with a
  3-question integrity check.
- Axiom alternatives: ≥1 "What if the value were different?" with
  a partial re-run.

**DOES NOT DELIVER:**
- No solution — only decomposition down to bedrock.
- No action recommendation — that is `frame`'s job.
- No broad solution space — focused depth, not breadth.

**ENABLES:**
- `frame` step 2: full drill as a required sub-invoke (solve
  context + deep mode).
- Solve phase 1: axioms in place before frames are built on top.
- Build specify: bedrock map for foundation specs (via `frame`
  deep mode).
- Spec authoring: bedrock map as the constraint source for
  foundation specs.
- Board review: bedrock map as context for reviewers (assumptions
  UNDER the spec).

### DONE
- All 4 phases executed (decomposition, bedrock presentation,
  bottom-up derivation, axiom questioning).
- Bedrock map ≥1 node.
- Derivation per layer has the integrity check with 3 questions.
- Phase 4 has ≥1 alternative when value axioms are present.
- Output ≤ 200 lines (focused) or cost preview accepted (broad /
  exhaustive).

### FAIL
- **Retry:** integrity check FAIL → re-formulate Y; re-run all 3
  (max 2 revisions per layer).
- **Escalate:** 3rd FAIL on the integrity check → user escalation.
  High stakes → council escalation recommended.
- **Abort:** max_depth reached without bedrock → report honestly,
  do not assert false axioms.

## Flow — 4 phases

### Phase 1: recursive decomposition

Reformulate → assign a core label (3-5 words) → cycle check (label
already on the path?) → identify assumptions (≥2) → per assumption:
bedrock classification (IF-THEN rules, `REFERENCE.md` §Bedrock,
analysis-mode-gate) OR invalidation potential scored (uncertainty
+ impact, ordinal low / med / high, `REFERENCE.md` §Scoring) →
relevance check ("new info on the original problem?") → pruning
(focused: top-1, broad: top-2, exhaustive: all) → recurse if
depth < max_depth. **User override** allowed at any point.

### Phase 2: bedrock presentation

Collect all bedrock nodes → type them with a one-sentence
decision-rule rationale → mark value-type as **"YOUR CHOICE"** →
bedrock map sorted by type, then tree depth → **Unseen-Assumptions
Prompt (required):** "Which assumptions are missing because they
look too self-evident?" — addressed to the user, dedicated section.
Phase 1 is bounded by what the LLM can see; training-corpus
defaults stay invisible.

### Phase 3: bottom-up derivation

From leaves upward: "Given [X] → [Y] because [Z]" per layer.
**Derivation integrity check (required):** 3 hard-coded questions
(Q1: logical link? Q2: contradiction with another branch? Q3:
concrete counter-reason why Y might not follow from X, and whether it is
refutable?), each PASS / FAIL + a one-sentence
rationale. 1 FAIL → revision (re-formulate Y, re-run all 3, max 2
per layer). 3rd FAIL → user escalation. **Limitation:**
self-critique, no independent verifier. High stakes → council
escalation recommended.

### Phase 4: axiom questioning

Per value axiom (max 3): "What if it were different / inverted?"
→ phase 3 **partially** (only the direct path upward to the root).
Name the cross-branch limitation when visible. No verdict — the
user decides.

## Modes

| Mode | Branching | Cost (all phases) | Cap |
|-------|-----------|-------------------|-----|
| focused | 1/level | ~13 passes | — |
| broad | top-2/level | ~68 passes | Soft: max_depth ≤ 4 |
| exhaustive | all | ~280 passes | Hard: max_depth ≤ 3 |

**Cost preview from broad onwards:** required before drill start.

## Gate

The skill is done when: (1) all 4 phases executed, (2) bedrock
map ≥1 node, (3) per-layer derivation has the integrity check
with 3 questions, (4) phase 4 has ≥1 alternative when value
axioms are present, (5) output ≤ 200 lines (focused) or cost
preview accepted (broad / exhaustive).

## Boundary

- Not single-pass analysis → `frame`. Not code review →
  `spec_board`.
- Not a known solution space → `scoping`. Not a knowledge gap →
  `research`.
- **Trigger:** the surface options are compromises; "Why?" can be
  asked more than once.

## Anti-patterns

- **NOT** skipping phase 4 because "no value axioms".
  **INSTEAD** check the bedrock classification. **Because:**
  almost every problem has values.
- **NOT** pruning without scoring. **INSTEAD** score the
  invalidation potential + offer a user override. **Because:**
  wrong branch = wrong drill.
- **NOT** treating the integrity check as "yeah, fits". **INSTEAD**
  3 questions with rationale. **Because:** without rationale, no
  check.
- **NOT** claiming bedrock at max_depth. **INSTEAD** report
  honestly. **Because:** false axioms propagate upward.

## References

| Topic | SoT |
|-------|-----|
| Algorithm, scoring, bedrock rules, examples | `REFERENCE.md` |
| frame (complement) | `skills/frame/SKILL.md` |
