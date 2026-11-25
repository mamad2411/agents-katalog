---
name: pre-build-spec-audit
description: >
  Mine pre-MVP / pre-build specs for methodology, architecture, and pattern
  ideas worth carrying into the current build scope (a concept harvest, NOT
  a compliance check against old specs). Use when a build's source set
  includes older specs that may carry reusable ideas. NOT for checking the
  build against an old spec's requirements.
status: active
invocation:
  primary: workflow-step
  secondary: [user-facing, sub-skill]
disable-model-invocation: false
uses: [council, _protocols/context-isolation, _protocols/dispatch-template]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: pre-build-spec-audit

Concept and architecture mining across pre-existing specs against
a concrete build / task. Prevents pre-thought methodology from
being lost during MVP construction AND prevents obsolete pre-MVP
pictures from being misread as a prescription.

## Guiding principle

**Foundation builds can't be over-thought.** Pre-MVP specs are
not prescriptions — they are a thinking source from a larger
(often post-MVP) picture. The skill is a depth tool, not a
compliance check.

## When to call

Required on:

- **Foundation build** (knowledge store, memory, intake pipeline,
  knowledge graph, auth layer, etc.) — where "not quite right"
  is expensive later.
- **Cross-domain construction** (>2 domain boundaries) —
  pre-MVP specs likely thought through cross-cutting patterns.
- **Repo with a large spec history** (>20 specs from older
  iterations).
- **Retroactive after a code-review FAIL** with spec-drift
  findings — is the drift class a pre-MVP picture or a real
  build bug?
- **User question** "was that already thought through?" —
  immediately this skill.

Optional on smaller builds when the cross-spec relationship is
unclear.

## Boundary against related skills

| Skill | Scope | When |
|-------|-------|------|
| **spec_board** | Single-spec review (NEW spec) | A new spec is reviewed |
| **spec_corpus_review** | Full corpus, milestone gate | Before milestone release, all specs together |
| **sectional_deep_review** | One large spec, sectional | Foundation spec >1000 lines |
| **spec_amendment_verification** | Code vs spec post-build | Verify code follows the spec (spec=SoT) |
| **retroactive_spec_update** | Code → spec (fix drift) | Code is SoT, the spec is adapted |
| **pre-build-spec-audit (this)** | Concept mining + MVP reconciliation | What did pre-MVP think through — what of it is viable? |

Other skills treat specs as SoT.
**This skill treats specs as a thinking corpus.**

## Phase 0–2 — pre-conditions, inventory and concept extraction

Before Phase 1, and before dispatching the Phase 1b foundation re-inventory or a Phase 2 / 2b concept-extraction
round: read and follow `skills/pre_build_spec_audit/inventory-and-extraction.md` (Phase 0 pre-conditions, STOP
without a sharp MVP boundary; Phase 1 inventory + relevance scoring with the task lens; Phase 1b re-inventory with
the foundation lens, CONDITIONAL; Phase 2 parallel concept extraction with the 5-class MVP assessment and its prompt
skeletons).

## Phase 3–4 — synthesis, triage and conditional council

When the Phase 2 returns are in, before the synthesis and the user dialog, and before spawning a council on a
NEW-METHODOLOGY entry: read and follow `skills/pre_build_spec_audit/synthesis-and-council.md` (Phase 3 synthesis +
triage across the 5 classes, Buddy direct with the user dialog, no autonomous decision; Phase 4 conditional council
on NEW-METHODOLOGY with the briefing content). When the synthesis shows imminent foundation decisions, return to
Phase 1b above.

## Output paths

```
docs/reviews/audits/
  {date}-{task-id}-pre-build-audit-phase1.md         # inventory
  {date}-{task-id}-pre-build-audit-phase2-{spec}.md  # 1 per HIGH spec
  {date}-{task-id}-pre-build-audit-synthesis.md      # triage + user dialog
  # if phase 4 was triggered:
  docs/reviews/council/{date}-{task-id}-pre-build-audit-{role}.md
```

## Contract

### INPUT

- **Required:** build / task ID + module list + pattern list +
  decisions list.
- **Required:** **MVP boundary** (what is in, what is post-MVP)
  — explicit.
- **Required:** `docs/specs/` directory with pre-existing specs.
- **Optional:** frame report from `frame` (shortens
  inventory).
- **Context:** task file `docs/tasks/{task-id}.md` with build
  notes.

### OUTPUT

**DELIVERS:**
- Inventory table (every spec with a relevance score).
- Phase-2 concept-extraction files (1 per HIGH spec).
- Synthesis file with the 5 triage classes.
- User-dialog questions (instead of autonomous decisions).
- Recommendation to Buddy / user per class (pass-fix /
  backlog / council / spec maintenance).

**DOES NOT DELIVER:**
- No spec edits — triage shows what; `retroactive_spec_update`
  does the editing.
- No code edits — found MVP-INTEGRATEs are fixed in the next
  pass loop.
- No ADR entries — phase-4 council may recommend an ADR.
- No autonomous triage decisions — the user chooses per class.

**ENABLES:**
- Next code-review pass with the MVP-INTEGRATE fix set.
- Follow-up tasks (post-MVP backlog, `retroactive_spec_update`
  for MATCH).
- Council spawn on NEW-METHODOLOGY.
- Spec cleanup on PRE-MVP-OBSOLETE.

### DONE

- Phase 1 inventory persisted.
- Phase 2 every HIGH spec concept-extracted.
- Phase 3 synthesis + triage persisted.
- The user has decided per triage class.
- Phase 4 (if triggered) council decision documented.

### FAIL

- **Retry:** phase 1 finds > 20 HIGH specs → build scope too
  broad, sub-tasking, the skill runs again per sub-task.
- **Escalate:** phase 3 finds > 3 NEW-METHODOLOGY with
  substantial architecture implication → build pause; council
  spawn unavoidable; possibly spec authoring for a revised
  architecture.
- **Abort:** the build is withdrawn by the user → the skill
  terminates without synthesis.

## Boundary

- **No single-spec review.** That is `spec_board`.
- **No full-corpus review.** That is `spec_corpus_review`
  (milestone gate).
- **No spec edits.** The synthesis shows what;
  `retroactive_spec_update` or `spec_update` makes the edits.
- **No code edits.** MVP-INTEGRATE findings land in the next
  code-review pass loop.
- **No compliance check.** Pre-MVP specs are a thinking
  corpus, not SoT — for code-vs-spec compliance use
  `spec_amendment_verification`.

## Anti-patterns

- **NOT** treat pre-MVP specs as prescriptions. **INSTEAD** as
  a thinking corpus — many pre-MVP patterns were thought for
  post-MVP (worker, event bus, multi-region) and are not a
  build deficit in MVP but a scope decision. Because: a
  "DRIFT / BLOCKER" framing creates compliance pressure on the
  MVP scope; that is anti-foundation building.

- **NOT** start phase 2 without phase 1 ("read all 45 specs in
  depth"). **INSTEAD** always run phase 1 filter first, then
  read only HIGH-relevance deeply. Because: phase 2 deep on 45
  specs is 30+ agent calls, token burn without value — most
  specs are orthogonal.

- **NOT** dispatch phase 2 sequentially. **INSTEAD** all N
  HIGH-spec agents in the SAME tool block, `run_in_background`
  on N>3. Because: wall-clock advantage is the point of map
  reduce — sequential takes 5x as long.

- **NOT** triage phase 3 autonomously and head into the fix
  loop. **INSTEAD** dialog with the user across the 5 classes
  — foundation builds deserve discussion; autonomous triage
  decisions burn pre-thought concepts. Because: Buddy can't
  draw the MVP boundary finally; the user decides what is
  MVP-viable.

- **NOT** lump everything as POST-MVP-VISION because "the
  pre-MVP picture was different". **INSTEAD** check honestly
  per concept whether the underlying methodology is MVP-viable
  (sometimes the idea is good and only the topology was
  post-MVP). Because: blanket POST-MVP throws away foundation
  maturity.

- **NOT** frame POST-MVP-VISION as a "backlog task" and
  blindly file it via `task_creation`. **INSTEAD** check the
  roadmap mapping — many pre-MVP concepts already have a
  post-MVP milestone slot (e.g. `<area>-mvp` →
  `<area>-worker` → `enterprise-<area>`). Only when no slot
  exists: a new task in the right milestone, not generic
  "backlog". Because: the roadmap topology is lost when
  everything ends up as a generic backlog task.

- **NOT** classify worker-service / NATS / event-bus /
  multi-tenancy concepts as PRE-MVP-DROPPED just because MVP
  doesn't have them. **INSTEAD** that's almost always
  POST-MVP-VISION with an existing roadmap slot. DROPPED is
  the rare class — only when the idea appears neither in the
  current MVP nor in the post-MVP roadmap. Because:
  foundation skipping of post-MVP concepts devalues the
  vision.

- **NOT** trigger NEW-METHODOLOGY council on API diff or
  field-name drift. **INSTEAD** that's MATCH or MVP-INTEGRATE,
  not council. Because: the council is for architectural
  trade-offs, not surgical patches — council inflation
  devalues the instrument.

## Relation to the code-review loop

The skill is a companion to the code-review-board loop:

```
Foundation build planned OR code-review pass N FAIL
  → pre-build-spec-audit (this skill)
  → 5-class triage (MATCH / MVP-INTEGRATE / NEW-METHODOLOGY / POST-MVP-VISION / DROPPED)
  → user dialog per class
  → MVP-INTEGRATE in the next code-review pass
  → NEW-METHODOLOGY potentially council spawn (phase 4)
  → POST-MVP-VISION linked to an existing roadmap milestone or a new task in the right milestone
  → MATCH potentially spec maintenance via retroactive_spec_update
  → DROPPED spec note or archival
  → code-review pass N+1 with a better-thought-through foundation
```

## Relation to spec_corpus_review

| Axis | spec_corpus_review | pre-build-spec-audit |
|------|--------------------|-----------------------|
| Scope | Full corpus, every spec | Subset, task-focused |
| Frame | Specs as SoT, consistency check | Specs as a thinking corpus, concept mining |
| Trigger | Milestone gate | Before / after a build pass |
| Phases | 7+ (phase 0-7) | 4 (1-2-3-4 conditional) |
| Triage | Cross-spec findings | 5-class MVP reconciliation |
| Wall-clock | Days | < 1 hour |
| Output | Cross-spec findings, impl order | Triage list + user dialog |

The two coexist. `corpus_review` is a heavyweight milestone
gate. `pre-build-spec-audit` is lightweight per-build with a
concept-mining focus.
