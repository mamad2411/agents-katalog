---
name: Operating Framework
description: Task routing, risk assessment, execution modes, and completion standards for meaningful work.
---

# Operating Framework v1.0

Macro-level routing for meaningful work. It classifies lane, risk, mode, required artifacts, evidence, and completion standard. It integrates with existing gates and commands; it does not replace them.

## Triggers

Activate on every meaningful task. Trivial tasks such as a single lookup, file read, or quick answer can bypass the full framework, but safety, verification, and approval gates still apply.

## Session Contract

For non-trivial work, route before acting:

```text
TASK: [one-line description]
LANE: [Explore | Specify | Build | Verify | Ship | Recover]
RISK: [T0 Safe | T1 Local | T2 Shared | T3 Critical]
MODE: [A Founder | B Elite Engineering | C Recovery | D Secure Delivery]
ARTIFACTS: [what this task must produce]
EVIDENCE: [what proves completion]
COUNCIL: [Solo | Lead+Reviewer | Full Council]
DONE WHEN: [measurable completion condition]
```

Use `/start-task` when an explicit header is useful; otherwise route mentally before acting.

## Lane and Risk Rules

| Lane | Use For | Required Standard |
|---|---|---|
| Explore | Vague request, unknown scope, "what if" | Questions, options, or brief before specification |
| Specify | Behavior change or new capability | Spec, acceptance criteria, and plan before build |
| Build | Approved spec or clear plan | Code, tests, docs as needed |
| Verify | Existing work needs validation | Test results and review findings |
| Ship | Verified work ready for delivery | Commit/PR/deploy checklist and evidence |
| Recover | Bug, incident, regression, failure | Root cause before fix, then regression check |

| Risk | Scope | Behavior |
|---|---|---|
| T0 Safe | Local, read-only, reversible | Proceed freely |
| T1 Local | Local workspace writes | Execute narrowly and verify |
| T2 Shared | Shared systems, remotes, data, config | Pause before shared/irreversible action |
| T3 Critical | Production, financial, security, secrets, irreversible | Full review and explicit user approval |

If unsure, escalate one tier. Production is T2+, financial/trading is T3, and security-sensitive work is T2+.

## Operating Modes

| Mode | When | Typical Sequence |
|---|---|---|
| A Founder | Greenfield product or feature | brainstorm -> spec -> architecture -> plan -> build -> verify |
| B Elite Engineering | Approved spec and clear implementation | plan -> test -> build -> review -> document |
| C Recovery | Bug, failure, incident, regression | debug -> review -> test -> reflect |
| D Secure Delivery | Security-sensitive, deployment, infra | security audit -> review -> build |

See [operating-modes.md](references/operating-modes.md) for detailed mode playbooks.

## Decision Tree

1. Vague or exploratory? Use Explore.
2. Behavior change or new capability? Use Specify before Build.
3. Bug, failure, or regression? Use Recover.
4. Production, money, security, secrets, shared state, or irreversible action? Escalate to T2/T3.
5. Multiple domains or high-stakes tradeoff? Convene council.
6. Otherwise use Solo execution with the matching mode.

## Enforcement Rules

- Do not cross lane boundaries without required artifacts.
- Do not claim completion without evidence.
- Do not fix bugs before stating root cause with supporting evidence.
- T2/T3 actions require explicit checkpoint before irreversible or shared action.
- Every review finding gets a disposition: accepted, deferred with reason, or rejected with reason.

## Completion Standard

Every non-trivial task ends with a completion packet or equivalent final report covering:

- Summary.
- Changed files and artifacts.
- Tests or validation run.
- Evidence.
- Risks, rollback path, open questions, and next step when applicable.

See [completion-and-precedence.md](references/completion-and-precedence.md) for the full packet template and skill precedence rules.

## Escape Hatch

If the user explicitly says "just do it", "skip routing", "emergency mode", or "no framework needed", streamline the framework. Never skip:

- No fabrication.
- Security-first behavior.
- Verify before asserting.
- Approval gates for T2/T3, destructive, secret-affecting, production, or irreversible actions.

See [escape-hatch-and-integrations.md](references/escape-hatch-and-integrations.md) for bypass logging and integration points.

## Reference Map

| Need | Read |
|---|---|
| Session contract, lane definitions, risk tiers, decision tree, artifact matrix, enforcement rules | [routing-and-artifacts.md](references/routing-and-artifacts.md) |
| Operating mode detail | [operating-modes.md](references/operating-modes.md) |
| Council compositions and decision format | [councils.md](references/councils.md) |
| Memory promotion and benchmark metrics | [memory-and-metrics.md](references/memory-and-metrics.md) |
| Golden workflows | [golden-workflows.md](references/golden-workflows.md) |
| Completion packet and skill precedence | [completion-and-precedence.md](references/completion-and-precedence.md) |
| Escape hatch and integration points | [escape-hatch-and-integrations.md](references/escape-hatch-and-integrations.md) |
