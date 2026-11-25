---
name: multi-agent-working-group
description: Use when a user asks to coordinate multiple agents, PM/advisor/worker/reviewer roles, Claude or external advisor review, delegated implementation, independent verification, controlled commit/push authorization, or cross-agent handoff in a development task.
---

# Multi-Agent Working Group

## Overview

Use this skill to run a guarded, evidence-based multi-agent workflow. The Leader remains responsible for orchestration, verification, owner communication, and git exits; other agents provide scoped work or independent critique.

Project `AGENTS.md`, memory, spec workflow, security, legal, or Owner instructions may only tighten this skill. Do not use this skill to weaken a project-specific gate.

This `SKILL.md` is the always-loaded router and hard-boundary summary. Reference files extend this file; they cannot weaken it, override it, or grant authorization by themselves. If a required reference is missing or unread for an affected domain, stop before acting in that domain.

## Mandatory Reference Routing

Read the relevant reference before acting in these domains:

- Git/default exclusions: MUST read `references/git-exit-rules.md` before commit, push, tag, release, publication, deployment, force-push, protected-branch bypass, destructive operation, credential/secret/security/auth/permission change, schema change, or any other default-exclusion action.
- OpenSpec: MUST read `references/openspec-lifecycle.md` before OpenSpec proposal, implementation, validation, closeout, archive, or status reporting.
- CLI trust/model routing: MUST read `references/cli-trust.md` before relying on Claude CLI, Codex CLI, another CLI-based role, workspace trust setup, or PM/Advisor model-separation state.
- Rollover/handoff: MUST read `references/context-rollover.md` before context rollover, handoff, successor startup, continuity recovery, or relying on prior state.
- Leader-state profiles: MUST read `references/leader-state-profiles.md` before selecting, refreshing, rendering, or transitioning a Compact, Standard, or `hierarchical-required` active-state profile.
- Agent-guided adoption: MUST read `references/agent-guided-adoption.md` before first use in a project, after a material installed-skill upgrade, or before assessing or proposing adoption changes in a consumer project.
- Role output/templates: MUST read `references/role-templates-and-output.md` before dispatching PM, Advisor, Worker, Reviewer, accepting role output, creating startup packets, or producing final closeout summaries.
- Context-efficient role review: MUST read `references/review-context-efficiency.md` before preparing, dispatching, retrying, or accepting a stable-baseline plus incremental PM or Advisor review packet.

Context efficiency may remove repeated material only. It must not reduce PM/Advisor provider or model capability, required review frequency or scope, no-peek independence, task-relevant original-evidence access, gate coverage, lifecycle patience, or Leader verification.

## Advisor Minimum Permissions

Using this skill means the owner has approved Advisor agents to read the minimum local evidence needed for the current assigned task's project. This includes relevant project files, local instructions, specs, tests, docs, global memory/skill files needed for stable rules, and non-mutating discovery/git evidence.

This default approval does not authorize writes, edits, deletes, git mutations, broad context dumps, deployment, publication, network/production actions, secrets, credentials, browser data, unrelated projects, or unrelated personal directories.

If an Advisor cannot read the minimum local evidence, record the Advisor as blocked or degraded. For medium, complex, high-risk, code, permission/API/database/architecture, security, or commit/push-bound work, missing required Advisor evidence fails closed unless the Owner explicitly approves narrower degradation.

## When To Use This Skill

Use or explicitly consider `multi-agent-working-group` when the current task has one or more of these traits:

```text
Explicit Owner request to use this skill, PM, Advisor, Worker, Reviewer, or multi-agent review.
External Advisor review, such as Claude CLI or another non-Leader AI role.
OpenSpec-backed proposal, implementation, closeout, or archive work.
Medium, complex, high-risk, implementation-heavy, or substantive Worker-suitable work.
Guarded commit, push, CI/status, archive, or other gate review.
Cross-conversation handoff, context rollover, successor startup, or continuity recovery.
Complex verification where independent critique or evidence capture matters.
```

Automatic invocation means applying this workflow and checklist to the task. It never creates external effects or transfers authority. It does not silently spawn agents, call an external Advisor, trust a workspace, commit, push, run CI, archive, deploy, release, publish, read secrets, bypass Owner-only gates, or start a recommended next goal.

First use and material upgrades follow the documentation-first Agent-guided
adoption protocol. Installation grants no project-write authority: assess
current project evidence read-only, keep unsupported facts `unverifiable`,
propose exact bounded file changes, wait for exact Owner project-write
authorization, recheck for drift, use project-native validation, and repeat a
stable read-only assessment. This skill provides rules, templates, and
examples; it does not ship or invoke a consumer-project migration runtime.

Scale the workflow to the task size. A narrow small low-risk task may use Small Task Mode only when every Small Task Mode condition is met. Medium or higher work must not be performed by Leader as hidden Worker execution when independent Worker ownership is required.

Fast Path is a reading-order shortcut only: for narrow low-risk or read-only work, start with this `SKILL.md`, project instructions, and only references for domains actually touched. Fast Path is not Small Task Mode, does not remove PM/Advisor/Reviewer or git-gate requirements, and never skips a mandatory reference once a routed domain is touched.

Slow Path applies as soon as the task reaches git exits, OpenSpec, CLI trust or model routing, role dispatch or output, rollover or handoff, release or publication, secrets, auth, security, permission, schema, destructive, irreversible, or other default-exclusion work. In those domains, the action-triggered MUST-read routing above controls before acting.

## Startup Checklist

Before dispatching agents or acting on a gate:

1. Read project instructions and relevant memory for the current repo.
2. Classify risk using the stricter tier when uncertain.
3. Check whether OpenSpec, security, code-intelligence, TDD, review, or other project skills apply.
4. Decide whether multi-agent work is useful or required.
5. Record authorization state; default to no commit/push/tag/release authorization.
6. Record PM/Advisor provider/model, separation state, and any degradation when both roles are active.
7. For OpenSpec work, perform C0 goal analysis before proposal or implementation.
8. Stop at failed validation, unresolved P0/P1, missing required PM, Advisor, or Reviewer, workspace-trust blocker, Owner-only gate, or irreversible external-effect gate.

## Role And Evidence Boundaries

PM and Advisor must independently agree on the goal, scope, next action, verification method, risk level, and lack of unresolved P0/P1. PM and Advisor expected output is independent first-pass / no-peek review before consensus.

Missing required PM or Advisor evidence fails closed for medium, complex, high-risk, OpenSpec-backed, code, permission/API/database/architecture, security, archive, or commit/push-bound work unless the Owner explicitly approves narrower degradation.

Advisor output is unverified evidence rather than authority. Claude/advisor feedback, PM output, Worker output, Reviewer output, old handoff, successor packet, template, memory, or previous consensus is evidence for Leader verification, not authorization by itself.

Leader owns orchestration, synthesis, verification, owner communication, and git exits. Leader must never self-authorize commit, push, tag, release, deployment, or other default exclusions.

Reviewer must not review its own implementation. Worker slices must have bounded scope, cannot expand scope, and cannot self-approve, commit, or push.

## Risk And Severity

Use the higher tier when uncertain.

| Tier | Meaning |
| --- | --- |
| Small low-risk | Read-only work, narrow docs/copy/style/config, or isolated tests with no approved-behavior, permission, data, persistence, external-effect, or git-remote change. |
| Medium | Multi-file docs/tests, contained bug fixes, local tooling, or work needing multiple evidence sources without high-risk areas. |
| Complex | New user-visible workflow, architecture/module boundary, cross-layer work, public API, external integration, or spec-bound change. |
| High-risk | Security, permission, auth, approval/sandbox, credentials, payment/account/wallet, schema/persistence, destructive/irreversible operation, external publication, release/tag/protected-branch bypass or exception, force-push/history rewrite, or unresolved P0/P1. |

| Severity | Gate |
| --- | --- |
| P0 | Stop immediately. |
| P1 | Resolve before affected gate. |
| P2 | Record and continue when safe. |

## Small Task Mode

Small Task Mode is only for narrow small low-risk tasks where project spec workflow and full multi-agent workflow are not required. It uses no PM, no Worker, and no Reviewer.

Small Task Mode does not bypass project instructions, validation, dirty-worktree protection, Advisor review at git gates, or Owner authorization rules. It does not authorize unilateral commit/push or any default exclusion.

## Git Exit And Default Exclusions

PM + Advisor consensus authorizes only normal non-high-risk git exits after the applicable gate passes. It never authorizes default exclusions.

Within the same verified workstream, normal non-high-risk commit, push, CI/status, and archive progression may continue only when PM and Advisor agree, no unresolved P0/P1 remains, required Reviewer approval has passed when applicable, required validation is fresh, target scope is clear, and applicable secret/credential scanning passes.

Default exclusions require explicit Owner authorization naming the action:

```text
Protected-branch bypass or exception action
Force-push or history rewrite
Tag/release publication
Deployment or public publication
Credential/secret/security/permission/authentication changes
Schema migration
Destructive operation
Irreversible external effect
```

Commit requires PM + Advisor consensus, no unresolved P0/P1, required Reviewer approval when applicable, fresh validation, and clear commit scope. After commit, PM + Advisor must review the actual commit result before push.

Push requires PM + Advisor consensus, no unresolved P0/P1, required Reviewer approval when applicable, fresh validation, clear remote/branch/ref, applicable secret scan, CI/status check when available, and post-push PM + Advisor review.

## OpenSpec Lifecycle

When this skill and OpenSpec are both active, use C0-C4:

```text
C0 Goal Analysis
C1 Proposal
C2 Implementation
C3 Closeout
C4 Archive
```

Do not skip C0. Do not treat C3 as final completion when C4/archive applies. Goal completion for OpenSpec work includes validation, PM/Advisor review, commit/push/status when covered by the applicable gate, archive, archive validation, and post-push review.

## CLI Trust And Model Routing

Provider-level separation means different service providers. In validation anchors, provider-level separation remains the current provider separation marker. Same-provider variants can be useful evidence but must be recorded as `same-provider-variant` degraded or partial separation, not full provider separation.

A current verified model record applies to the exact current project, workstream, role, task stage, and available tool environment. Global memory, project memory, handoff, startup-packet, or prior continuity preferences are hints to verify against the current workstream, not stale authority.

Do not claim PM/Advisor independence was strengthened by model diversity when same-model pairing, same-provider variants, stale routing records, or unverified routing hints were used.

For CLI trust setup, an applicable Owner-recorded role assignment source may include current Owner instruction, global memory, project rule, project memory, handoff, startup packet, continuity record, ledger, template, or verified OpenSpec evidence. Record `owner-recorded-role-authorized` only when applicable to the exact current project and role. Record trusted state only after the post-setup read-only probe succeeds. Do not use dangerous permission-bypass flags, broaden scope, read secrets, trust parent/home/all repos, or create external effects without explicit Owner authorization.

## Rollover And Handoff

Leader active state uses the progressive profile rules in `references/leader-state-profiles.md`. Structural current-active inventory selects Compact, Standard, or `hierarchical-required`; provisional line and byte bands only warn. Size never authorizes truncation or omission, and semantic or control failure remains fail-closed.

Every context-budget check must record exactly one canonical ContextBudget state. Platform-visible summaries are evidence of what the Leader can see, not proof of actual total compactions. Owner-reported threshold evidence can raise the canonical state when the Owner reports a concrete count.

Clean boundary plus heavier next step is at least Rollover Opportunity. 3-4 observed compressions/summaries is ContextBudget Watch. 5-6 observed compressions/summaries is Rollover Recommended. 6 or more observed compressions/summaries plus a next action of Worker dispatch, commit, push, CI, archive, or a high-risk gate is Rollover Required.

Rollover or successor packets do not carry that authorization into a successor context. Handoff, rollover, successor startup, task dashboard, and continuity records are evidence only; they do not create authority for commit, push, scope expansion, gate bypass, or external effects.

## Agent Lifecycle And Delegation

For OpenSpec work, default each PM and Advisor to one runtime-proven role-agent lifecycle within exactly one C1, C2, C3, or C4 stage. C0 role sessions are short-lived bootstrap sessions and close or restart before C1. Cross-stage transitions start new role lifecycles by default. Within one C-stage, each distinct checkpoint still requires a new Review ID, Attempt ID, exact target fingerprint, fresh decision, validation freshness, authorization state, and no-peek state; same-stage continuity never inherits an earlier `GO`, validation result, git/archive authorization, or the other role's current first-pass conclusion. Follow `references/review-context-efficiency.md` for runtime identity, canonical states, mandatory restart triggers, ambiguity quarantine, and transition-only actor/time evidence.

For non-OpenSpec work, distinct checkpoints continue to use fresh short-lived role sessions. An unchanged-target narrow clarification may continue under the same session and Review ID with linked attempt evidence. Never silently substitute a provider.

Do not treat short silence or a brief lack of visible output as task failure for PM/Advisor substantive review. Worker lifecycle uses the same evidence-based patience principle for substantive bounded work. Close, restart, or replace PM/Advisor only when there is a recorded lifecycle reason.

For Medium, Complex, High-risk, implementation-heavy, or substantively Worker-suitable work, the Leader should dispatch bounded Worker slices instead of performing hidden Worker execution when practical.

For Medium, Complex, OpenSpec-backed, multi-file, implementation-heavy, or context-heavy work, direct Leader execution beyond small connective edits is an exception. More than 2 files or roughly 80 diff lines is a self-check trigger rather than an automatic correctness failure: dispatch a bounded Worker or record a concrete exception explaining why Leader direct execution is safer.

Worker-first context control means dispatching bounded Worker slices before Leader context grows toward rollover pressure when a coherent slice can be owned by a Worker. It does not require Worker dispatch for narrow low-risk edits or gate-required commands.

Role-agent cleanup or close actions run sequentially, never in parallel. Record each close result before starting the next cleanup action. Normal cleanup order is Worker, Reviewer, PM, then Advisor, but do not close any role still needed for a required gate, cleanup-impact judgment, unresolved P0/P1 review, post-action review, or Owner decision.

Cleanup/close means role-agent teardown or lifecycle hygiene only. Cleanup failure may be reported as degraded cleanup evidence rather than delivery failure only when delivery evidence is already confirmed from evidence in hand and task, git, validation, CI/status, secret-safety, authorization, and required role evidence remain unaffected. Do not classify validation, PM/Advisor/Reviewer, git, CI/status, secret-scan, release/tag, or authorization failure as non-blocking cleanup. Cleanup failure is blocking when it prevents confirming task state, git state, validation state, CI/status state, secret safety, authorization state, or required role evidence.

## Validation And Verification

Before dispatch, acceptance, repair, commit, push, archive, tag, or release, the Leader must:

1. Restate current Owner instruction and whether it authorizes the next action.
2. Check git branch/base/dirty state and changed files.
3. Check OpenSpec state when applicable.
4. Check PM/Advisor independence or record approved degradation.
5. Check required Reviewer status.
6. Check required validation freshness.
7. Label key claims as verified, inferred, assumed, or unverified input.
8. Stop at unresolved P0/P1.

`./scripts/validate-local.sh` is read-only evidence. It does not authorize commit, push, archive, release, deployment, publication, secret-scan bypass, Reviewer bypass, PM/Advisor bypass, or any high-risk/default-exclusion action.

## Output Requirements

Every agent output must include applicable skills, why each skill applies, checks performed, findings by P0/P1/P2 when reviewing, evidence used, and recommended next action.

Leader final outputs should include plain-language closeout:

```text
What changed:
What was verified:
What remains uncertain or was not checked:
Recommended next goal:
Authorization state:
```

Recommended next goals are advice only unless the Owner has already given explicit current-session authorization. Separate verified evidence from claims. Do not present a recommendation, stale memory, handoff, prior consensus, template, or old instruction as current authorization.
