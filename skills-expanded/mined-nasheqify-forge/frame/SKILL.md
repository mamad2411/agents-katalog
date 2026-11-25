---
name: frame
description: >
  Board-style problem-analysis discipline. Forces multi-perspective
  thinking before solutions are developed. Output: a structured
  frame report with reformulated problem, solution space, and
  recommendation in one turn.
  Triggers when a problem needs multi-perspective analysis before solutioning (solve phase 1, build specify interview); NOT when the solution shape is already clear.
status: active
relevant_for: ["solution-expert"]
invocation:
  primary: workflow-step
  secondary: [user-facing, sub-skill]
disable-model-invocation: false
modes: [quick, standard, deep]
uses: [research, bedrock_drill, _protocols/plan-review, _protocols/analysis-mode-gate, _protocols/cross-phase-source-grounding]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.
Without Buddy (plugin): if this session holds no Buddy boot entry, run `python3 <root>/scripts/forge_setup.py offer-check` once, as its own call (`<root>`: two levels above this skill's folder); if it prints a line, pass that offer to the user in one sentence, then continue with this skill.


# Skill: frame

Prevents Buddy from jumping to the first-best solution. Forces a
disciplined analysis of **the problem itself** before solutions are
developed. Detail mechanics (examples, orthogonality-check case
studies, edge cases): `REFERENCE.md`.

## Who runs it

Buddy (primary). Used as a building block in: solve workflow
(phase 1, main call), build workflow (specify interview), scoping
skill (L0 elicitation when problem framing is unclear), council
preparation (solution-candidate input).

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| problem | yes | The user's raw problem description |
| context | no | Additional context (task, spec, existing artifacts) |
| depth | no | quick \| standard \| deep. Default: standard |
| caller | no | solve \| build \| scoping \| standalone. Default: standalone. **Drives the step-2 drill trigger:** solve → full drill always (solve override). Others → per the mode table. MUST be set explicitly by the calling workflow. |

## Standalone boundary

Supplied problem, constraints and evidence are sufficient without a repository or
user scope. Preserve all depth/caller options. Use caller-owned temporary transport
for independent review; `skills/_protocols/dispatch-template.md` defines complete
attributed returns before consolidation. No automatic tasks, ADR, engine or durable
writeback. Missing evidence is a stated limit. Development paths below and in `flow.md` apply only
when the caller explicitly selects that development workflow.

## Output context

- **Inside solve:** the frame report goes into the state-file body
  under `## Phase 1: Frame`.
- **Inside build:** the frame report is inline in the chat AND a
  compact summary (8-12 bullets — decisions + rationales, no full
  prose) is logged to the build state-file phase-log at
  `docs/build/<slug>.md` under `## Gate 1 — interview`. Build has
  a state-file; the chat is transient. Persistent state belongs in
  the state-file. SoT: `workflows/runbooks/build/WORKFLOW.md` gate 1.
  Before the build interview settles scope, read and follow
  `workflows/runbooks/build/lifecycle.md` (conditional stages, UX
  and architecture, with their triggers).
- **Outside solve and build** (scoping, council, standalone): the
  frame report is inline in the chat.

**Scope of the method.** In mixed work, apply this flow to the unresolved
solution space, as selected under `framework/process-map.md` §Workflow routing.
Known mechanical items retain their stated implementation and verification
obligations; do not manufacture alternative designs for them. An embedded defect
uses the existing root-cause-fix primitives and retains its verification
obligation in the parent work artifact. The alternatives, drill and
per-sub-problem requirements below and in `flow.md` apply to the items being framed.

## Flow — 8 sub-steps (binding order)

Once depth and caller are set, before step 1: read and follow `skills/frame/flow.md` in binding order (1 reformulate
the problem; 2 first-principles drill with the full-drill triggers and bedrock-map bind rules; 3 plan + review; 4
source check; 5 constraints; 6 SOTA research, conditional; 7 open the solution space with the orthogonality check
and variation lenses; 8 evaluate + recommend; present all approaches fairly before evaluating).

## Contract

### INPUT
- **Required:** the user's raw problem description.
- **Optional:** context — additional context (task, spec, existing
  artifacts).
- **Optional:** depth — quick | standard | deep (default:
  standard).
- **Optional:** caller — solve | build | scoping | standalone
  (default: standalone). Drives the step-2 drill trigger.
- **Context:** solve context → state file (`docs/solve/*.md`).
  Outside solve → no state file required.

### OUTPUT
**DELIVERS:**
- Frame report: reformulated problem, first-principles result,
  plan + review, repo hits, constraints, solution space (≥3
  approaches with distinguishing axes), context-specific
  recommendation.
- Bedrock map (on full drill — solve context or deep mode): its
  own section in the frame report with typed axioms.
- On decomposition: one frame per unresolved sub-problem in the same report;
  retain known work and defect obligations in the parent scope without another
  frame.

**DOES NOT DELIVER:**
- No solution / implementation — only solution-space analysis.
- No spec — frame is input for spec authoring, not the spec itself.
- No implementation decision — recommendation only; the user
  decides.

**ENABLES:**
- Solve phase 2 (refine): user can challenge and sharpen the
  frame.
- Build specify: frame as the basis for the spec interview.
- Council: solution candidates as input for a structured decision.

### DONE
- All "always" steps (1, 2, 4, 5, 7, 8) executed (step 3 skipped
  on trivial; step 6 skipped with rationale).
- Step 2: ≥1 assumption naming + ≥1 counter-question
  (mechanically checkable).
- Step 2 on full drill: bedrock map as a dedicated section in the
  frame report.
- Step 7: ≥3 approaches (≥2 in quick), each with a distinguishing
  axis; null option checked.
- Recommendation justified context-specifically.
- Output: reformulated problem + first principles + constraints +
  approaches + recommendation.

### FAIL
- **Retry:** problem too large → decompose inline; one frame per
  sub-problem in the same state file.
- **Escalate:** problem not decomposable, or user uncertainty even
  with the frame → invoke council.
- **Abort:** not foreseen — decompose or escalate.

## Gate

Frame is done when:
- All "always" steps (1, 2, 3, 4, 5, 7, 8) are executed (step 3
  skipped on trivial).
- Step 2 has ≥1 assumption naming + ≥1 counter-question
  (mechanical check).
- Step 2 on full drill (solve context or deep): bedrock map as a
  dedicated section `## Bedrock Map` in the frame report MUST be
  present.
- Step 3 has plan block + self-review block + (on non-trivial)
  adversary review block.
- Step 6 executed OR skipped with a one-sentence rationale.
- Step 7 has ≥3 approaches (≥2 in quick), each with a
  distinguishing axis; null option checked.
- Output: reformulated problem + first principles + bedrock map
  (when drill) + plan + review + repo hits + constraints +
  approaches-with-axes + recommendation.
- Recommendation justified context-specifically.

## Modes

| Mode | When | What changes |
|------|------|--------------|
| quick | Small problem, solution space obvious | Step 2 minimum* (1 assumption + 1 counter-question, no skill invoke), SOTA skipped (documented), ≥2 approaches |
| standard | Default | All "always" steps run normally, SOTA conditional, ≥3 approaches. Step 2 minimum* (no skill invoke) |
| deep | Foundation / cross-layer / schema / new subsystem | + SOTA triggered + 4+ approaches + step 2 MUST invoke `bedrock_drill` (full drill, bedrock map required) |

*\*Solve override: in solve context, step 2 ALWAYS fires the full
drill (`bedrock_drill`, focused as default mode), regardless of
mode level. Solve is by definition for uncertain problems — the
drill is proportional. The mode table then only governs the rest
(SOTA trigger, approaches minimum, etc.), not the drill level.*

**Hard gate — auto-upgrade to deep (MUST):**
- Foundation spec (defines constraints that cascade).
- Cross-layer impact (>1 layer / >2 specs affected).
- New subsystem (first time, no predecessor artifact).
- Schema change (DB / API schema definition).

**Soft upgrade to deep (SHOULD, documented skip allowed):**
- Hard to reverse.
- New domain.

Buddy downgrades to quick when: solution space clear from the repo
check, small, reversible. User override wins.

## Boundary

- No feature build (feature already clear) → build workflow.
- No bug fix (reproduction path clear) → fix workflow.
- No spec review (artifact exists) → spec_board / review workflow.
- No knowledge question (answer to be found) → research workflow.
- No objective with spec hierarchy (done state clear) → scoping
  skill.

## Anti-patterns (short)

- **NOT** ticking the template mechanically. **INSTEAD** every step
  delivers substance. Because: a checklist without content = a
  formal gate without value.
- **NOT** favourite-approach-first + strawmen against the rest.
  **INSTEAD** open the space first, then evaluate. Because:
  rationalization blocks real alternatives.
- **NOT** research as default. **INSTEAD** only on a trigger,
  otherwise documented skip. Because: research is expensive; not
  every problem needs SOTA.
- **NOT** skipping first principles because "it's obvious".
  **INSTEAD** drill exactly when the problem looks clear.
  Because: that's where the wrong assumptions hide.
- Do not frame a reproduced malfunction merely to fill the solution-space
  template. Use the existing root-cause-fix primitives; standalone defect work
  routes to Fix, while an embedded defect remains tracked and verified within
  its parent work.

## References

| Topic | SoT |
|-------|-----|
| Detail mechanics, examples, edge cases | `REFERENCE.md` (this directory) |
| Plan + review (step 3) | `skills/_protocols/plan-review.md` |
| Source grounding (step 4) | `agents/buddy/operational.md` §Source-Grounding |
| Research in an explicitly selected development caller (optional integration) | `workflows/runbooks/research/WORKFLOW.md` |
| Use in workflow | `workflows/runbooks/solve/WORKFLOW.md` |
