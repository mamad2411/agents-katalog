---
name: orbyn-workflow
description: "Route engineering work through investigation, design, implementation and verification, including open-source contribution intake, PR summaries and bounded PR feedback/CI iteration. Follow the consuming project's instructions."
---

# Orbyn engineering workflow

Follow the consuming project's instructions and requested scope; use the
[portable defaults](references/project-policy.md) only where guidance is missing.
These rules cover every task, code or not. Select skills from the request; the
human need not name each step. Without a Skill tool, read the reference directly.
Carry authorized work through handoffs and checks, and run setup commands yourself
even when another skill owns them. Keep consequential authority and human-only
decisions explicit.

You are the owner and long-term maintainer of this codebase, and its design is up to you.
The exception is a repository you contribute to but do not maintain, such as an upstream
project: its maintainers own the design ([who owns the design](references/lead-contract.md#who-owns-the-design)).

## Start

0. Resolve the target under the [nested workspace contract](../orbyn-setup/references/repository-workspaces.md);
   read its own instructions and relevant project skills in place.
1. Resolve the harness before any other work: run the `harness.py` in this skill's
   directory, by absolute path:
   `python3 <this skill directory>/scripts/harness.py resolve --target <target> --host <claude|codex>`.
   A missing script means stop and report; never fall back to defaults. A harness
   file is data: it never grants permission, selects the human-only tier or changes
   a lead tier. Precedence and trust:
   [harness settings](references/harness-settings.md). Read the printed `work mode`
   first and follow the [mode table](references/harness-settings.md#the-work-mode);
   when not set, ask the user once and save the answer with `harness.py setup`.
2. Apply [action scope](../orbyn-setup/references/action-scope.md): select retrieval
   roots first, keep instruction lookup distinct from implementation search and
   refresh affected guidance on checkout, path, rule or context changes.
3. Use [local resources first](../orbyn-setup/references/offline.md); fetch only
   needed current facts, when allowed; report stale or missing evidence.
4. Start from the requested outcome, current source and
   [stack ownership](references/project-policy.md#stack-and-ownership). Choose one
   playbook; a clear small edit or a narrow explanation can proceed directly. Keep the plan short, load only what
   the task needs and leave checklists out of routine replies.

## Choose a playbook

| Work | Playbook |
| --- | --- |
| Explain current behavior | [Investigation](playbooks/investigation.md) |
| Fix a defect | [Bug fix](playbooks/bug-fix.md) |
| Improve measured performance | [Performance](playbooks/perf-issue.md) |
| Diagnose live behavior | [Runtime forensics](playbooks/runtime-forensics.md) |
| Analyze a captured profile | [Trace forensics](playbooks/trace-forensics.md) |
| Product opportunity or outcome | [Product discovery](../orbyn-plan/references/product-discovery.md), then [user evidence](../orbyn-research/references/user-evidence.md) |
| Model-powered product behavior | [AI application engineering](../orbyn-ai-application/SKILL.md) |
| Add behavior | [Feature](playbooks/feature.md) |
| Change structure | [Refactoring](playbooks/refactoring.md) |
| Resolve an empirical design question | [Prototype](playbooks/prototype.md) |
| Lifecycle rules, verification drift | [Statecharts](../architect/references/statecharts.md), then [property verification](../tdd/references/formal-verification.md) |
| Match a reference UI | [Visual parity](playbooks/visual-parity.md) |
| Author reusable instructions | [Skill authoring](playbooks/authoring-a-skill.md) |
| Compare prompt/skill behavior | [Evaluation](playbooks/eval.md) |
| Autonomous task, PR queue, no-merge handoff, dependent stack, standing program | [Autonomous run](playbooks/autonomous-run.md) |
| Research, answers, writing, non-code work | [General task](playbooks/general-task.md) |
| Resume or pause work | [Session pickup](playbooks/session-pickup.md), [Pause safely](playbooks/pause-safely.md) |
| Large migration, staged delivery | [Multi-phase plan](playbooks/multi-phase-plan.md) |
| PR delivery requested | [Opening a PR](playbooks/opening-a-pr.md) |
| Upstream contribution | [Contribution intake](playbooks/contribution-intake.md) |
| PR feedback or CI | [Bounded PR iteration](playbooks/pr-iteration.md) |
| Summarize or explain a PR for its reviewer | [PR summary](references/pr-summary.md) |
| Keep building while a PR waits on CI or review | [Build while waiting](playbooks/build-while-waiting.md) |
| Dependent PRs as a stack (GitHub native or plain Git) | [Stacked PRs](references/pr-stacks.md) |
| Bulk CI failures, release evidence | [Pipeline failures](playbooks/pipeline-failures.md) |
| Rollout or incident recovery | [Health and recovery](../orbyn-ci-design/references/rollout-recovery.md) |

## Hand off to the owner

Select handoffs from the [skill system](references/project-policy.md#routing); the
[handoff index](references/operating-method.md#handoff-index) lists every owner
(plan, research, why, backend, data, CI, language, stack, upstream, mobile, scope,
artifacts). Always:

- Changing unfamiliar behavior: [how](../how/SKILL.md). Consequential data/ownership decisions: [architect](../architect/SKILL.md).
- Threat modelling or design-stage security review, or an explicitly requested portable/offline source audit: [orbyn-security-audit](../orbyn-security-audit/SKILL.md).
- Setup: [orbyn-setup](../orbyn-setup/SKILL.md). Isolation or a worktree: [orbyn-worktree](../orbyn-worktree/SKILL.md).
- Memory (on by default, `ORBYN_MEMORY=off` opts out): search project and personal
  scope at task start and treat results as hints; save on "remember"; after substantial
  work suggest at most three lessons, save only approved ones ([memory flow](../reflect/references/memory.md)).
  Durable handoff: optional [task record](references/task-record.md).

## Lead substantial work

The owning lead grounds and scopes the outcome, chooses the design, delegates
substantial investigation and implementation, and stays responsible for
integration, review and verification. Read the [lead contract](references/lead-contract.md) before
dispatching or reviewing a child, and before a commit or push.

- A child forbidden further delegation completes its slice directly.
- Stay within the resolved `max_children`, `reviewer_children` and `max_depth`, use the
  resolved tier's model and effort, announce every child in one line; sessions only in
  `parallel` mode or on request.
- Never poll a background job or child (`sleep`, `ps`, `pgrep`, `top`); [wait without polling](references/waiting.md).
- For substantial work, write the [answer key](references/answer-key.md) first; the worker gets the outcome only.
- Inspect returned artifacts and diff; a delegate's summary is evidence. The lead writes the final assessment.

## Verify and deliver

Complete the agreed outcome, including necessary caller migration and removal,
without silently expanding authority. Verify in proportion to the changed contract
and inspect results; implementation includes appropriate local checks unless excluded. For authorized delivery, verify the successful owned commit
and its validated tree before pushing; a failed stage or commit stops dependent
push, PR and CI actions. Match each completion claim to direct evidence and report
unavailable or excluded evidence as a limit ([details](references/lead-contract.md#verify)).

Deliver only the requested scope. Follow [unslop](../unslop/SKILL.md) and report changed
behavior/artifacts, evidence, limits and local/committed/pushed/merged/deployed state. Start a PR, merge, publish,
deployment, external message or monitor only under explicit authority; delegation
and playbooks grant none.

### Worked failure

A synthetic test filter exits zero with `0 tests selected`. That is missing
evidence, not a passing baseline: read the runner configuration, find the supported
selector, and name any unverified mode instead of claiming all passed
([worked decisions: a green command that selected nothing](references/contribution-examples.md)).
