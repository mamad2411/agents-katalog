---
name: openspec-superpower-change
description: "Use when a request may modify files or behavior, asks review-and-fix, changes skill/workflow/template files, needs OpenSpec or Direct Change classification or Superpowers routing, decides evidence-based final completion, or asks to archive and distill a session through Project Learning Closeout; also trigger on 开发变更、变更准入、OpenSpec、Review并修复、实施闭环、归档并蒸馏、Skill自演进、OpenSpec 精简模式、OpenSpec 正常模式. 可按用户要求输出 caveman 风格摘要，但不改治理约束。"
---

# OpenSpec + Superpowers Change Gate

Single entry gate for state-changing development work. It classifies the
request, protects approval boundaries, selects implementation discipline, and
owns final review and verification. It does not own standalone prompt wording
or an already-handed-off external batch.

## Governed Caveman Lite output mode

The built-in `governed-caveman-lite` profile does not activate by default.
Enable it with `OpenSpec 精简模式：<任务>`, or send `OpenSpec 精简模式` before the task.
While active, use concise professional full sentences without filler, repetition, fragment-heavy prose, or unexplained abbreviations.

It remains active for the current conversation until disabled or the conversation ends.
Disable it with `OpenSpec 正常模式`.
A new conversation starts in normal output mode and creates no account, repository, or runtime preference.
The latest explicit OpenSpec mode command controls Router prose, so normal mode wins even after a prior Caveman-style instruction.

It is presentation state only, never invokes or delegates to a separate `caveman` skill, and works when one is unavailable.
It does not change routing, approval, evidence, Review, verification, completion, Git, or publication authority.

Compression may shorten ordinary summaries only. Protected content remains structurally complete:

- Gate 0 and mandatory governance/approval fields;
- OpenSpec artifacts and Superpowers implementation plans;
- Handoff/evidence artifacts and canonical state transitions;
- PASS/FAIL/BLOCKED, final verification, and final Review;
- critical commands, rollback instructions, security warnings, destructive confirmations, and sensitive-data handling.

Governance output keeps every required field and ordering constraint present; governance clarity and safety override compression.

## Legacy request-scoped output compatibility

The legacy requests `少 token/更短/更精简/像 caveman 说` and the entry wording `caveman 风格摘要` still request request-scoped compression.
This applies only to the current request.
It does not activate or persist `governed-caveman-lite`.
Only `OpenSpec 精简模式` activates the named conversation profile.
Legacy brevity remains subject to the same protected-surface rules defined above; it cannot omit governance or safety content.

## Mandatory Entry Gate

Before file modification, state-changing commands, proposal creation, or
implementation, complete Gate 0:

1. mode and references read;
2. OpenSpec decision and reason;
3. required Superpowers sub-skills;
4. risk/evidence profile, next action, and confirmation requirement.

For a typo, formatting, or other non-behavioral micro change, one compact line
may carry all four facts. Gate 0 must stay complete but must not make a light
task heavy. Inspection-only reads are allowed before Gate 0 to classify work.

## Routing Boundary

| Request | Primary skill / mode |
|---|---|
| Modify, fix, implement, change behavior, change workflow/template files, or dispatch without a valid Handoff | This skill |
| Review-and-fix, including explicit backend architecture Review plus a fix | This skill / state-changing Router route; specialist output is bounded evidence only |
| Explicit backend architecture Review of a proposal/design, without a fix, including architecture/design, performance/stability, service/module boundaries, API/call chain/transaction boundaries, or over-design | `backend-architecture-review` / read-only bounded evidence |
| Other architecture Review, OpenSpec need, implementation authorization, or whole-task completion evidence | This skill / Review-only |
| Write or refine a task prompt, Brief, or checklist without changing files | `codex-brief-antigravity-review` / standalone |
| Read-only review of a diff, Report, or evidence without fixing it | `codex-brief-antigravity-review` / standalone |
| Execute, resume, or review a batch with a valid Handoff Contract | `codex-brief-antigravity-review` / handed-off |

“Review and fix” is implementation, not Review-only. Review-and-fix remains
state-changing Router work and does not select the specialist by itself. A Direct
Change that uses
an external agent still enters here first; create a profile-appropriate Handoff
Contract before handing execution to the governor. Only work that remains
low-risk may default to `compact`.

When a valid Handoff already exists, its dispatch/resume/review route takes
priority and goes directly to `codex-brief-antigravity-review`.

For already authorized implementation, the complete closed-loop continuation
rule is owned by `references/approved-implementation-workflow.md`. Its four
continuation phrases permit only safe, reversible, same-scope progress; a status
report is progress rather than a confirmation request. This entry reference
points to that owner and does not create a competing approval rule.

For proportional implementation decisions, read `references/approved-implementation-workflow.md`.
Reuse existing mechanisms first; apply current-task TDD and do not widen tests
or machinery without a gate or demonstrated blast radius.

Only explicit backend architecture Review selects
`backend-architecture-review`; generic Bugfix/Diff/Plan/acceptance Review,
including `Review 一下这个 Bugfix 的 Diff` and `Review 当前 Plan`, does not
select the specialist. The specialist returns read-only specialist
evidence as bounded evidence only and cannot mutate or decide Router canonical
state. The existing route remains unchanged; ordinary Review remains unchanged.
Gate, OpenSpec, Handoff, Evidence,
PASS/FAIL/BLOCKED, Completion, and authority remain with this Router.

This skill owns request classification, OpenSpec approval, risk/evidence and
batch profiles, Handoff creation, and final completion. The brief skill owns
Brief/Report/Review attempts only after handoff and returns the final batch to
this router.

Under schema 6, `codex`, `pi`, `antigravity-cli`, and `grok-cli` are equally
eligible for assigned executor or independent-reviewer roles. Their results are
evidence inputs. Only a bound `codex` product with role `control-plane`, profile
`control-plane-high`, matching instance, and canonical contract may accept that
evidence or record a canonical transition. Product names alone grant no
authority; standard/strict executor and reviewer instance IDs must differ.

Every Review request or recommendation states Review purpose, reviewer product,
role, capability, independence, and authority. Preserve an existing canonical
assignment, then an explicitly user-selected eligible product, then recommend
one concrete product; if no required independent instance is available, return
`BLOCKED`. Route the exact contract through
`references/agent-capability-routing.md`.

<!-- ROLE_FIRST_REVIEW_CLASSIFICATION_START -->
Use this exact classification before selecting a product:

- A Review that decides whether implementation, execution, runtime planning,
  promotion, archive, or completion may proceed is gate-bearing: use role
  `independent-reviewer`, profile `control-plane-high`, distinct-instance
  independence, and authority `governed-review-evidence`.
- A standalone Review that explicitly does not decide a gate is advisory:
  preserve any eligible user-selected product, use role `advisory-reviewer`,
  profile `control-plane-high`, advisory-not-gate-bearing independence, and
  authority `advisory-input`.
- `cohesive-medium` and `mechanical-low` are executor/evidence-collection
  profiles, not Review profiles.
- For standalone prompt or recommendation wording, a request to open or name a
  new distinct reviewer instance remains actionable after all six assignment
  concepts are resolved; do not infer unavailability merely because a concrete
  instance ID or open window is not yet supplied.
- Return `BLOCKED` only when the request explicitly says no eligible distinct
  instance exists or insists on reusing an implementation instance.
- When a required distinct reviewer instance is unavailable because the user
  must open or provide one, return `BLOCKED` with `blocker_owner: user` and a
  non-blank resume condition.
<!-- ROLE_FIRST_REVIEW_CLASSIFICATION_END -->

## Reference Read Matrix

Read `SKILL.md` first, then only the matching references:

For state-changing work or a whole-task completion decision, also read
`references/local-instruction-checkpoint.md` and
`references/completion-contract.md`. When correction/Review history or an
archive-and-distill request may require durable project learning, read
`references/project-learning-closeout.md`.

| Task | Required references |
|---|---|
| Review-only / route review | `references/request-modes.md`, `references/response-patterns.md` |
| Implementation / bugfix | `references/request-modes.md`, `references/openspec-decision-rule.md`, `references/step-evidence-gate.md`, `references/superpowers-adapter.md` |
| Direct Change | `references/direct-change-rule.md`, `references/step-evidence-gate.md` |
| Runtime / tool / workflow change | `references/openspec-decision-rule.md`, `references/proposal-workflow.md`, `references/approved-implementation-workflow.md`, `references/superpowers-adapter.md` |
| External execution | `references/approved-implementation-workflow.md`, `references/handoff-contract.md`, `references/agent-capability-routing.md`, `references/confirmation-lease.md` |
| Skill self-evolution | `references/self-evolution-rule.md`, `references/step-evidence-gate.md`, `references/learning-candidate-pipeline.md` |
| Runtime/source sync | `references/sync-checklist.md` |
| Cross-CLI skill/global-rule sync | `references/cross-cli-sync.md`, `references/sync-checklist.md` |

## OpenSpec Boundary

OpenSpec is required for new functionality, architecture or pattern changes,
public/operator-visible behavior, security, migrations, API/schema/data
lifecycle, broad refactors, runtime control flow, routing, or workflow lifecycle.

OpenSpec may be skipped for localized internal restoration of defined behavior,
small config-only changes, typo/comment/formatting updates, non-contractual docs,
or tests for existing behavior. Changing a skill's trigger, routing, required
artifact, state transition, evidence rule, or completion rule is workflow
behavior and requires OpenSpec. Editorial wording that changes none of those
contracts may use Direct Change.

A public/user/operator-visible restoration may use Direct Change only when an
approved existing spec or equivalent project-authoritative contract explicitly
defines the intended behavior, Gate 0 records its exact path, and no contract,
schema, compatibility, or lifecycle behavior changes. Otherwise use OpenSpec.

Do not implement OpenSpec-required work before approval.

## Implementation And Closure

- OpenSpec defines what/why/acceptance; Superpowers defines post-approval
  implementation discipline. Do not create duplicate design approvals.
- TDD applies to feature, bugfix, refactor, and behavior changes. Test-only
  coverage of already-defined behavior uses focused verification and must not
  claim runtime behavior changed.
- Step Evidence Gate signs off complete business slices or risk milestones,
  not every RED/GREEN micro-step.
- `compact` work requires focused verification and an inline diff/self-review.
- `standard` and `strict` inline work requires a distinct Review pass.
- A Handoff-backed external Review is the batch code-review gate; do not add a
  duplicate review for the same batch.
- Before implementation or dispatch, run a current-revision Plan/Brief
  **Preflight Review** under the bounded convergence contract in
  `references/approved-implementation-workflow.md`. First lineage Review is
  `FULL_PREFLIGHT`; only same-reviewer, unchanged-boundary, declared mechanical
  corrections may use `FOCUSED_RECHECK`. Non-convergence returns through
  `CONTROL_PLANE_ADJUDICATION`, not a new state. Preflight authorizes execution
  only; it is not Implementation Review or completion evidence.
- Separate tool/platform permission, scope/workflow authorization, and
  business/production authorization. Reuse an unchanged Confirmation Lease for
  safe commands and same-finding loops; never treat platform permission as a
  business approval.
- For standard/strict work, High Review inspects actual files and the complete
  diff, traces copy/transform/runtime wiring and claims to mechanisms, reruns
  critical evidence, and adds an independent adversarial or business-chain probe.

Every implementation follows:

```text
Plan/Brief Preflight PASS -> Implement -> Verify -> Review
Review FAIL -> Fix same scope -> Verify -> Review again
Review BLOCKED -> Resolve/decide -> refresh evidence -> Review again
Review PASS -> next slice, or final verification when no slice remains
```

Non-converging Review/Fix retries are not an unlimited automatic fix loop. When
repeated evidence shows widening scope or complexity instead of convergence,
follow `references/approved-implementation-workflow.md`: stop the widening retry
and return through existing `BLOCKED` / `control-plane-high` handling.

After implementation Review PASS, whole-task closure leaves this entry workflow
and follows `references/completion-contract.md`. That canonical contract owns
Learning entry and promotion blocking, final evidence, reconciliation, runtime
sync, and the completion decision; this entry does not restate those rules.

The final external batch `PASS` means `awaiting-final-verification`, not task
completion. Whole-task success, fresh final evidence, stop conditions, learning
and OpenSpec reconciliation, portable runtime sync, Git/publication authority,
and residual-risk reporting are owned by
`references/completion-contract.md`. Apply `references/cross-cli-sync.md` when
that contract's portable-file condition is triggered.

## Capability And Evidence Profiles

Capability profiles are independent from process weight:

- `control-plane-high`: architecture, approval/risk decisions, Preflight,
  evidence audit, promotion, archive, completion, and High Review.
- `cohesive-medium`: approved multi-file implementation with no open design or
  authorization decision.
- `mechanical-low`: deterministic edits, commands, tests, and evidence collection;
  ambiguity or authority-boundary work returns `BLOCKED`.

Evidence profiles remain:

- `compact`: low-risk docs, formatting, config, existing-behavior tests, or
  localized restoration; no large plan or Handoff by default.
- `standard`: default multi-file behavior slice; per-slice critical checks plus
  a distinct review; final matrix runs once after the final slice.
- `strict`: security, auth, public API/schema, persistence, migration,
  deployment/rollback, deletion/recovery, or cross-tenant work; real evidence
  cannot be replaced with mocks or unit tests.

## Phase-Aware Superpowers Activation

For governed state-changing work, this change gate performs phase-aware
classification before broad Superpowers metadata selects a sub-skill. Gate 0
selects sub-skills from the current phase, material unresolved decisions, and
implementation risk. Generic create/modify wording does not activate a
Superpowers sub-skill by itself.

Run the Domain Context Check before material-choice classification when affected
terms, actors, boundaries, states, or lifecycle may change. Repository facts
that establish clear language continue without `grill-with-docs`; unresolved or
conflicting domain language invokes it when installed, or the complete portable
Discovery First fallback when unavailable.

- `proposal-only`: inspect repository facts first. If a reviewable contract can
  be drafted with explicit bounded assumptions, create and validate it with no
  implementation sub-skill.
- Invoke brainstorming only for a material unresolved choice affecting scope,
  security, compatibility, data lifecycle, production authority, or testable
  acceptance. Once selected, preserve its complete HARD-GATE. A request to
  choose for the user does not resolve a material choice; invoke brainstorming
  and obtain acceptance before artifact finalization.
- Refresh Gate 0 when approved implementation begins; required planning, TDD,
  Preflight, Review, evidence, and verification then apply normally.

Model identity or version does not grant approval and does not select workflow
weight. Use task facts and stable capability/evidence profiles.

## Superpowers Mapping

| Scenario | Required Superpowers |
|---|---|
| Material unresolved choice after repository inspection | `superpowers:brainstorming` |
| Multi-step approved implementation | `superpowers:writing-plans` |
| Execute a reviewed plan | `superpowers:subagent-driven-development` or `superpowers:executing-plans` |
| Isolate work unless current branch use is explicitly authorized | `superpowers:using-git-worktrees` |
| Feature, bugfix, refactor, behavior change | `superpowers:test-driven-development` |
| Unexplained failure | `superpowers:systematic-debugging` |
| Inline standard/strict implementation review | `superpowers:requesting-code-review` |
| Completion/fixed/passing/ready claim | `superpowers:verification-before-completion` |
| Editing a skill | `superpowers:writing-skills` |
| Complete a branch workflow | `superpowers:finishing-a-development-branch` |

Apply `references/superpowers-adapter.md`. It maps Superpowers artifact and
permission defaults onto this workflow without weakening brainstorming, TDD,
debugging, Review, or verification discipline.

## Self-Evolution

Use Self-Evolution for changes to this skill or its companion's trigger,
routing, templates, validation, evidence, completion, or runtime/source sync.
Major self-evolution requires an approved contract, structured backup,
RED/GREEN forward-test, validation, rollback, final report, and final Review.

For global personal skill edits, short-circuit only unrelated business-project
OpenSpec recursion. Do not short-circuit user approval or any self-evolution
gate. Product behavior published from an OpenSpec-managed repository requires
an approved OpenSpec change.

Portable self-evolution is not complete after updating only the source repository
or Codex runtime. Run the declared cross-CLI target plan/apply/verify sequence;
a missing, stale, undiscoverable, or failed required target is `BLOCKED`.

A user correction or discovered invariant first enters
`references/learning-candidate-pipeline.md`. Candidate capture may be automatic;
Skill modification never is. A global candidate can at most propose a specific
Self-Evolution change after its evidence threshold and cannot bypass approval,
TDD, Review, runtime synchronization, or publication gates.

## Non-Negotiables

- Do not let `CONTEXT.md` replace OpenSpec artifacts.
- Do not let required project learning remain only in chat, Review output, or
  prose-only context when deterministic regression enforcement is practical.
- Do not let OpenSpec `tasks.md` replace a Superpowers implementation plan.
- Do not use Superpowers planning to bypass OpenSpec approval.
- Do not implement OpenSpec-required work before approval.
- Do not gate every TDD micro-step; do not skip the business-slice evidence gate.
- Do not advance with `FAIL`, `BLOCKED`, stale evidence, or unresolved findings.
- Do not claim completion without fresh verification evidence and Review PASS.
- Do not accept empty critical commands, blank blocker details, evidence-free
  external PASS, or an atomic final-verification/final-Review completion update.
- New schema-6 external artifacts carry the exact immutable
  `reviewer_assignment`; schema-2 evidence binds product, instance, role,
  capability profile, result, change, batch, attempt, and source canonical
  revision/SHA-256 back to that parent assignment. Historical schema-4/schema-5
  contracts and their evidence remain immutable legacy history. Runtime
  `complete` validation requires the actual previous status.
- The bound Codex control-plane instance is the only decision owner; executor or
  reviewer output cannot self-authorize a transition or final completion.
- Platform/tool permission never substitutes for OpenSpec, production, archive,
  promotion, release, destructive Git, or another user-owned authorization.
- Do not claim a portable global skill optimization complete while any declared
  required Codex, Pi, Antigravity CLI, or Grok CLI target is stale or unverified.
- Do not duplicate mutable Handoff Contract blocks outside canonical `status.md`.
- Self-evolution cannot weaken approval, evidence, review, verification, or
  user-control boundaries.
- Never run `git add`, `git commit`, `git reset`, or `git clean` unless the user
  explicitly commands it.
- Do not push without explicit user approval.
