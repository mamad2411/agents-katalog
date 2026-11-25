---
name: bugfix
description: >-
  Use this skill when investigating, diagnosing, and fixing a reported bug —
  including when the user reports an error message or broken behavior without
  saying "bugfix" — to run an end-to-end bugfix workflow with a mandatory
  DEVELOP → REVIEW → QA pipeline: the Lead orchestrates triage intake,
  environment analysis (`/env-analyze` for local, `/analyze-prod` for
  production), evidence collection, and bug report, then spawns
  developer/reviewer/QA via the Anthropic `Agent` tool to apply, review, and
  verify the fix.
argument-hint: "[bug description or error message]"
---

<!-- ARCHITECTURAL NOTE: no `context: fork` here. Per Anthropic docs, subagents cannot spawn other subagents. The DEV/REVIEW/QA pipeline requires the `Agent` tool, which is only available in the main thread. -->


# Bugfix (Multi-Agent Pipeline)

End-to-end bugfix workflow. The Lead handles intake / env analysis / evidence / bug report in the main thread, then drives a mandatory **DEVELOP → REVIEW → QA** pipeline by spawning named subagents via the **`Agent` tool** for the implementation, review, and verification of the fix.

You are the Lead. Read `@team-protocols` end-to-end before issuing the first spawn — it covers the spawn pattern, role-by-role mapping, conflict prevention, dual-path detection, and the G7 spawn payload + return contract schemas.

> **YOU MUST spawn subagents via `Agent({...})`.** Do not perform Developer / Reviewer / QA work inline with `Bash`/`Read`/`Edit`. Doing so violates the team-protocols hard invariant — the user loses per-role inspection and the pipeline gates collapse. Every fix-apply / review / verify step in this skill is an explicit, executable `Agent({...})` call.

## 1. Receive Bug Report

Gather from the user (Lead, main thread):

- Expected vs actual behavior, error message / stack trace, steps to reproduce
- Environment (local Docker / cloud production / code-only)
- When it started (after deploy / config change / unknown), recent commits
- Severity: P1 (outage), P2 (degraded), P3 (minor), P4 (cosmetic)

For P1/P2 — skip detailed intake and proceed immediately to Step 2.

## 2. Analyze Environment

Based on the environment, delegate to the appropriate diagnostic sub-workflow (these are skills, not subagent spawns — they run inline):

| Environment | Sub-workflow |
|---|---|
| Local Docker / Docker Compose | `/env-analyze` (or `/analyze-local`) |
| Cloud production (GKE/AKS/EKS, managed DB) | `/analyze-prod` |
| Code-only (no infra) | Skip to Step 3 |

The sub-workflow applies the diagnostic role (`Agent(sre-engineer)` / `Agent(devops-engineer)`), collects environment snapshot, and presents diagnosis. **If it resolves the issue at the infra layer** — skip to Step 9 (Summary). **If the root cause is in application code** — continue to Step 3 with the collected evidence.

## 2b. Reading large source files — never blow the 25K-token cap (audit §2.9)

Claude Code's `Read` tool rejects files whose content exceeds **25 000 tokens** (e.g. a 37K-token `design.md` or an 84K-token Monitor stream log). A failed Read costs the round-trip AND can stall the workflow. Before the first `Read` on any large evidence file (logs, stack traces, dumps, design docs > ~1000 lines):

```bash
wc -l <path>            # line count
wc -c <path>            # byte count — divide by ~4 for token estimate
```

If `wc -l` ≥ 1000 OR estimated tokens ≥ 20 000:

1. `grep -n "<symbol or error>" <path>` to locate the relevant span.
2. `Read(<path>, offset=<line>, limit=<window>)` for that span only.
3. For dump or trace files, prefer `tail -n 500` / `head -n 500` via `Bash` rather than full `Read`.

This rule applies to every teammate spawn's `pre_read` list and to the Lead's own evidence-collection reads.

## 3. Detect Stack and Pick Developer Role

Determine the affected service's tech stack to choose the right Developer `subagent_type` for the pipeline:

1. Read `CLAUDE.md` / `AGENTS.md` — tech stack declaration
2. Scan project files (`package.json`, `pom.xml`, `requirements.txt`, `go.mod`)
3. Inspect Step 2 evidence — which language is the stack trace in?

| Stack signal | Developer `subagent_type` |
|---|---|
| Next.js, React, TypeScript, `.tsx` files | `ai-skills:frontend-engineer` |
| Spring Boot, Java, `.java` files | `ai-skills:java-engineer` |
| FastAPI, Python, `.py` files | `ai-skills:python-engineer` |
| Terraform, Dockerfile, Helm, CI/CD | `ai-skills:devops-engineer` |
| ML model, training pipeline, inference | `ai-skills:ml-engineer` |
| Multiple stacks | One Developer per affected stack (sequential per `subagent-isolation.md`) |
| Unknown / general | `ai-skills:software-engineer` |

Announce the selected Developer role(s) to the user.

## 4. Collect Evidence

Gather a structured evidence collection (Lead, main thread). Combine Step 2 environment data with code-level investigation:

- Error output (full message, stack trace, exit code)
- Logs (timestamped) from the affected service
- Reproduction (local? consistent or intermittent?)
- Scope (which endpoints / features / components)
- Timeline + recent commits (`git log -n 20 --oneline`)
- Triggering inputs (request payload, user ID, dataset)
- Production metrics (error rate, latency change, affected users) if relevant
- Related code (files, functions, lines most likely involved)

Identify the **minimal reproduction case** — this becomes the regression-test oracle in Step 7.

## 5. Prepare Bug Report

Compile findings into a structured bug report (Summary, Severity, Environment, Expected/Actual, Steps to reproduce, Evidence, Root cause analysis, Affected components). Present to the user. Wait for confirmation that the diagnosis is correct before committing the fix to the pipeline.

## 6. Choose execution path (ATTEMPT Path B FIRST — literal, mandatory)

Per `@team-protocols/path-selection-rules.md`: Path B (Agent Teams) is MANDATORY default — visual team panel, Shift+↓ context-switching, dedicated transcript per role. Path A (sequential subagents) is fallback-only.

Detection is implicit — go to Path B Step 1 directly, no Bash env-var check. Valid Path A triggers are documented in `@team-protocols/path-selection-rules.md` (env-var unset, lead-in-subagent, whole-team alpha.32, alpha.33-fast-fail). Display-mode, platform, "small bug", "sequential pipeline", "single-stack", "Windows host", or "no tmux" — NEVER valid Path A triggers. **No silent fallback for non-technical reasons** — rationalised downgrades violate alpha.27.

The FIRST sentence when announcing the path MUST be one of:

- "Attempting Path B (Agent Teams) team-create..."
- (after fallback) "Agent Teams API returned: <verbatim error>. Falling back to Path A."

## 7. Mandatory Pipeline — DEV → REVIEW → QA (both paths)

Every fix MUST pass all three stages. Gate semantics are identical regardless of execution path; only the spawn mechanism differs.

### Gate Rules

1. The fix CANNOT enter REVIEW until the Developer's `Agent` call returns a valid G7 contract.
2. The fix CANNOT enter QA until the Reviewer's contract has `verdict: approved`.
3. The fix is NOT COMPLETE until QA returns `qa_verdict: pass`.
4. If the Developer reports "no changes needed" — the Reviewer STILL runs (independent confirmation).
5. If any spawn returns malformed JSON — re-spawn the same role with a corrected prompt; do NOT advance.
6. **The Lead MUST NEVER skip a spawn and do the work inline.**

Optional RALF on the reproduction test (kill-on `oracle-pass`): wrap the DEV spawn in `/ralph` per `ralph-budget.md` for intermittent / environment-dependent / hard-to-converge bugs (race conditions, memory leaks, off-by-ones). Defaults: 6 iter / 300K tokens / 60 min. Skip RALF for trivial bugs where the regression test passes on the first DEV iteration.

## Path B / Path A execution

The full Path B step sequence (team-create → task list → drive/monitor +
liveness watchdog → final cleanup) and the Path A subagents fallback (verbatim
`Agent({...})` templates, reviewer `disallowedTools`, `isolation: worktree`,
loop-on-`changes_requested`/`fail`) live in `pipeline-execution.md`. **Read
`pipeline-execution.md` and apply the steps verbatim before driving the
pipeline** — those mechanics are mandatory. Path B is the MANDATORY default;
Path A is used only when Path B Step 1 returns a technical error.

## 8. Self-Review and Final Verification (Lead, main thread)

After the pipeline returns the final fix:

- Re-read every changed file diff — verify correctness and completeness against the Step 5 bug report
- Run linter on changed files — zero warnings
- Run formatter — zero diffs
- Run the full test suite (or `/run-tests`) one more time — all tests pass
- For production bugs: verify the fix locally first; deploy through normal CI/CD (no direct prod hotfix); after deploy re-run relevant `/analyze-prod` checks; monitor error rates and SLIs

Do NOT declare the bug fixed until every item passes.

## 9. Summary

Present the completed bugfix:

- **Bug** (one sentence) and **severity** (P1–P4)
- **Environment** (local / production) and **roles applied** (developer + reviewer + qa subagent_types)
- **Root cause** (technical explanation)
- **Fix** (files changed, brief description) and **tests added** (count + description)
- **Pipeline trace**: DEV/REVIEW/QA iterations + verdicts (e.g. `DEV-1 → REVIEW changes_requested → DEV-2 → REVIEW approved → QA pass`)
- **Verification** (how it was confirmed fixed)
- **Remaining issues**: NONE (if any remain, go back through the pipeline before reporting)
- **Prevention**: recommendations to avoid similar bugs

## Integration

- **Sub-workflows (inline, not spawns)**: `/env-analyze` (local Docker diagnostic), `/analyze-prod` (production diagnostic), `/ralph` (optional RALF wrap on the DEV spawn for hard-to-converge bugs)
- **Auxiliary multi-agent skill**: `/team-bugfix` (same DEV/REVIEW/QA pipeline applied to a batch of issues from a code-review or audit document — use it when the input is an audit doc rather than a single bug report)
- **Followed by**: `/run-tests` (final test gate), `/pre-commit` (commit gate), `/create-pr` (submit fix)
- **Protocols**: `@team-protocols` (execution model, spawn primitives, agent coordination, G7 contracts)
- **Schemas**: `plugin/schemas/spawn-payload.schema.json`, `plugin/schemas/return-contract.schema.json`
- **Skills**: `code-review` (Reviewer applies), `test-strategy` (QA applies), `worktree-isolation` (multi-Developer isolation)
- **Rules**: `subagent-isolation` (G7 + bounded recursion + sequential code-mod gate), `ralph-budget` (RALF caps), `untrusted-content-wrapping` (G1 wrap on `/env-analyze` + `/analyze-prod` outputs)
