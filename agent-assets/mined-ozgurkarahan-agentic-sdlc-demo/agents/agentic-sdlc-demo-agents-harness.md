# AGENTS.md — example repo-wide rule file (EXAMPLE — copy to a target repo root)

> **This is a drop-in EXAMPLE.** In the harness home it lives under `harness/` so it does **not**
> govern that repo. To use it, copy this file to the **root** of a target repo as `AGENTS.md` and
> adapt the bracketed parts (the bootstrap step fills them and removes these EXAMPLE notes). It is
> the **static context** every Copilot coding-agent instance loads — the single highest-leverage
> harness artifact (`Agent = Model + Harness`).
>
> **It does not enforce anything by itself.** Real enforcement comes from rulesets, required checks,
> required reviews, and Environments configured in the target repo (see `README.md` here).

---

## 1. What this repo is

`[One-paragraph description of {{DEMO_APP}} — the service, its boundary, its stack. Example default:
a small REST API service. Replace with the target repo's real service.]`

- **Stack:** `[language / framework / runtime]`
- **Run locally:** `[command]`
- **Test:** `[command]` · **Lint:** `[command]` · **Build:** `[command]`

## Demo operating mode / ownership summary

- The **local/root orchestrator** owns the lifecycle state machine and handoffs, starting from a fresh
  current default-branch workspace and running `workspace-hygiene` before trusting `.harness` artifacts.
- **GitHub** owns durable records and native enforcement: Issues, PRs, required checks, branch protection,
  CODEOWNERS review, and environment/deploy approvals.
- **Copilot cloud agents** are implementation workers for exactly one approved work-unit Issue at a time; launch
  them by GraphQL assignment to the assignable Bot `copilot-swe-agent`, not by an `@copilot` mention.
- **Human gates are hard stops:** plan approval, PR merge/CODEOWNERS review, and deploy/live E2E approval.
- For Teams/M365 intake, use WorkIQ when available; otherwise ask for the pasted Teams message/source text rather
  than guessing.

## 2. The discipline — Enforce → Plan → Validate → Issues → Execute (non-negotiable)

0. **Workspace hygiene first.** Before trusting any local `.harness` artifact, the orchestrator must prove the
   checkout is on the current default-branch tip and that existing `.harness/plan.json` / `dispatch.json` /
   `units/*.json` belongs to the current run. Stale run artifacts are quarantined, not reused.
0a. **Full-tool local orchestrator.** The local/root orchestrator must run with the full harness tool profile
    (`read`, `search`, `edit`, `terminal`, `github`, `actions`, `workiq` or host equivalents). Teams/M365 intake,
    `gh`/`git` polling, local tests, and harness state updates are orchestrator responsibilities; do not offload
    them to the loop/observer because a restricted agent session lacks a tool alias.
1. **Enforce first.** Before any work Issue exists, GitHub-native gates must be **LIVE** on the repo —
   gate workflows in `.github/workflows/`, required status checks, branch protection + **CODEOWNERS** on the
   default branch (prove it with the **`verify-gates`** skill). Ungated Issues produce ungated PRs.
2. **Plan first (locally).** No implementation without an approved plan: each unit specified with acceptance
   criteria, a Definition of Done, a test/eval strategy, declared paths, a required test, and a dependency
   graph — emitted as a **LOCAL, issue-ready artifact** (`.harness/work-plan.md`), not yet GitHub Issues.
3. **Validate the plan.** The plan passes a **rubber-duck / devil's-advocate** review **and** a human
   approval **before any code is written**. This is a hard gate.
4. **Materialize as Issues.** Only the **approved** plan becomes GitHub Issues — one tracking Issue + one
   **work-unit** child per unit — via the **`plan-to-issues`** skill. Issues are the durable work intake the
   pipeline dispatches from (assign each to a dev-fleet agent or **Copilot cloud agent**).
5. **Execute** only against the validated, approved, **Issue-tracked** plan, on an **enforced** repo.

**Never implement an unvalidated plan. Never create Issues before validation + approval + live gates.
Never parallelize dependent units. The human gates (plan-approval · PR-merge · deploy) are HARD STOPS —
the orchestrator must stop and ask, and must never self-approve them or defer with "review later", even
in autopilot.**

## 3. How you (a Development-fleet agent) must work

- You are assigned **exactly one** parallel-safe Issue. Implement **only** that unit.
- Work on your **own branch**; open **one linked PR** that references the Issue.
- **Do not touch files owned by another unit.** If you discover a cross-unit dependency, stop and
  flag it on the Issue — it means the plan needs re-validation, not a workaround.
- Keep the change minimal and scoped to the Issue's DoD. Do not refactor unrelated code.
- Ensure your PR's tests **and** evals pass; do not weaken a check to make it green.
- **Never merge your own PR.** Humans approve via CODEOWNERS / required review.

## 4. Guardrails — "never do" rules

- Never commit secrets, credentials, or `.env` files. (Secret-scanning push protection is on.)
- Never add an unpinned or unverified dependency; watch for **hallucinated / slopsquatted** packages.
- Never disable, skip, or weaken a required check, test, or eval.
- Never deploy on a red gate; never bypass the merge queue.
- Never make architecture-impacting changes without updating the architecture docs/diagrams.

## 5. Conventions

- **Style:** `[link to style guide / formatter config]`. Match existing code; don't reformat
  unrelated lines.
- **Frontend/UI:** For any user-facing web interface unit, invoke
  `.github/skills/frontend-design.skill.md`. Preserve the existing brand/design system unless the
  approved unit authorizes a redesign; implement responsive, accessible, complete interaction states
  and verify them with the required UI tests/E2E flow.
- **Tests:** colocate with `[test convention]`; every behavior change ships with tests **and** evals.
- **Commits/PRs:** small, focused, linked to an Issue; PR description states what + why + how-verified.
- **Docs:** update `README` / API reference when behavior or interfaces change.

## 6. The harness around you (for reference)

> **Enforcement modes.** The agent/prompt/skill markdown below is the thin template a
> target carries. The runnable **checks** (`checks/scripts/*.mjs`) stay in the harness
> **home** and run locally via `<HARNESS_ROOT>` (see `skills/README.md`). The
> **GitHub-phase** files — `workflows/*.yml`, vendored `ci/scripts/*`, `CODEOWNERS` —
> are added only when you wire required-check enforcement on GitHub; they are **not**
> part of the thin local template.

| Role | Where it's defined |
|---|---|
| Orchestrator / Dispatcher | `.github/agents/orchestrator.agent.md` |
| Planning / Requirements | `.github/agents/planning.agent.md` |
| Development fleet (implements one unit) | `.github/agents/dev-fleet.agent.md` |
| Rubber-Duck / Plan-Validation | `.github/agents/rubber-duck.agent.md` |
| Quality / Test | `.github/agents/quality-test.agent.md` |
| Security / Compliance | `.github/agents/security-compliance.agent.md` |
| Code Review | `.github/agents/code-review.agent.md` |
| Deployment / Validation | `.github/agents/deployment.agent.md` |
| Repeatable procedures | `.github/prompts/*.prompt.md` |
| Project-zero bootstrap | `.github/prompts/bootstrap-environment.prompt.md` → produces `.harness/project.json` |
| Skills (procedures agents invoke) | `.github/skills/*.skill.md` (workspace-hygiene · workplace-intake · **frontend-design** · run-tests · check-deps · deploy · **verify-gates** · **plan-to-issues**) |
| Work intake | `.github/ISSUE_TEMPLATE/work-unit.yml` — materialized from the approved plan by **`plan-to-issues`** |
| Safety overlay | `.github/instructions/agent-safety.instructions.md` |
| Verification (GitHub phase — **wired before any Issue**) | `.github/workflows/tests-and-evals.yml` |
| Security gate (GitHub phase — **wired before any Issue**) | `.github/workflows/security-gate.yml` |
| Code ownership (GitHub phase — **wired before any Issue**) | `CODEOWNERS` |

> 🔒 **IF HIGH-ASSURANCE.** Add: mandatory multi-party plan + release approval; a dedicated
> Security/Compliance owner; "all security + eval checks green before merge"; stricter rulesets and
> secret-scanning push protection enforced org-wide.
