---
name: lyra-bug-hunter
description: "Adversarial bug hunting focused on runtime behavior: a Recon → Hunter → Skeptic → Referee pipeline that finds, verifies, and optionally fixes real bugs with evidence discipline. Use for bug finding, pre-merge regression checks, behavior-focused PR review, or a security-flavored sweep of a codebase."
compatibility: "No tools required. Optional: git (diff/PR/staged scopes), a test runner (fix verification), gh CLI (PR mode). Composes with lyra-security-appsec, lyra-ci-cd-automation, lyra-de-slop. Version policy: examples target the latest stable release of every tool; minimum supported is the newest LTS (or last maintained major), and features newer than the minimum are flagged inline."
---

# lyra-bug-hunter

## What it does

Runs an adversarial bug hunt where four roles check each other: **Recon** maps the code and ranks it by risk, the **Hunter** hunts for defects with a runtime-behavior checklist, the **Skeptic** tries to kill every finding, and the **Referee** confirms only what survives with evidence. Findings that no one can trigger at runtime don't exist. In fix mode (the default when bugs are confirmed) it repairs one bug at a time on a dedicated branch, verifying after each fix and reverting anything that regresses.

The pipeline is sequential by default and needs no scripts, subagents, or external services — every phase is executed by the agent itself, with phase outputs persisted to `.lyra/bug-hunter/` so large hunts can resume. Add `.lyra/bug-hunter/` to `.gitignore`.

## Scopes

| Invocation           | Scope                                                            |
| -------------------- | ---------------------------------------------------------------- |
| `lyra-bug-hunter`         | Whole project                                                     |
| `lyra-bug-hunter src/`    | A directory or file                                               |
| `--changed [base]`   | Full contents of files this branch changed vs `base` (default: merge-base with main) |
| `--pr [number]`      | Full contents of files a PR touches (`gh pr diff --name-only`)    |
| `--staged`           | Full contents of staged files (pre-commit check)                  |
| `--scan-only`        | Report findings, change nothing                                   |
| `--dry-run`          | Plan fixes as diffs, edit nothing                                 |

The "flags" are **vocabulary, not a CLI**: skills are invoked as `Skill(command="lyra-bug-hunter")` with no argument channel, so modes arrive as words in the user's request ("scan-only", "just the staged files", "--changed") or as the agent's own judgment call — an agent that sees none of them runs the default (whole target, fix mode). Diff scopes scan the **full contents** of changed files, not just the hunks — a change often breaks code it didn't touch. Skip non-source files (docs, lockfiles, assets, generated code, vendored dirs); if nothing scannable remains, say so and stop.

## The pipeline

### 1. Recon — map before hunting

Identify the tech stack, entry points, and trust boundaries. Classify files by risk: **CRITICAL** (auth, payments, permissions, session, crypto, input parsing), **HIGH** (data writes, concurrency, external I/O), **MEDIUM** (business logic), **LOW** (presentation, utils), **CONTEXT-ONLY** (tests — read for intent, don't hunt in them). Write the risk map to `.lyra/bug-hunter/recon.md`. Hunt in risk order so a truncated run still covered what matters.

### 2. Hunter — every finding needs a runtime trigger

For each file, hunt defects that change behavior. A valid finding states: file and lines, the claim, and the **concrete input or state that makes it misbehave**. "This could be cleaner" is not a bug; that belongs to lyra-de-slop or code review. Sweep for:

- Injection and unsanitized input reaching a sink (SQL, shell, path, template, HTML)
- Authorization gaps: missing object-level checks, trust of client-supplied identity
- Async races, unawaited promises, unhandled rejections, TOCTOU
- Off-by-one, boundary conditions, integer precision/overflow, NaN propagation
- Null/undefined flow the types don't actually rule out
- Swallowed errors, catch blocks that hide failures, wrong error paths
- Resource leaks: unclosed handles, listeners, timers, connections
- State-machine violations: operations valid only in states nobody checks
- Timezone, locale, and encoding assumptions

Record findings as `BUG-N` entries in `.lyra/bug-hunter/findings.md`. On large codebases, chunk by directory or service, append per chunk, and note completed chunks so a resumed run skips them.

### 3. Skeptic — try to kill every finding

For each finding, actively look for the reason it's wrong: a guard upstream, a type that forbids the input, a caller that can never pass the bad value, a test that pins the behavior, framework behavior the Hunter forgot. Each finding gets a verdict: **disproved** (with the evidence that kills it) or **stands** (with the strongest objection that failed).

Be honest about what separation you actually have. When the runtime can spawn an isolated sub-agent, run the Skeptic there — it inherits none of the Hunter's framing, which is the strongest form of this phase. When it can't, the Skeptic pass is a *structured self-review*: re-read the surrounding code fresh (never just the Hunter's claim), argue the strongest case *against* each finding before ruling, and record that the pass was self-reviewed. A self-reviewed pass is still mandatory; it just doesn't get to call itself independent.

### 4. Referee — confirm with evidence, report honestly

Only findings that survived the Skeptic reach the Referee. Each becomes **CONFIRMED** (failure scenario is concrete and reachable) or **PLAUSIBLE** (real risk, but reachability unproven — manual review, never auto-fix). **Execute the evidence when a runner exists**: the strongest confirmation is a failing test or reproduction script actually run, not a scenario reasoned about — each CONFIRMED entry records whether its evidence was *executed* or *static*, and static-only confirmations of Critical/High findings **must** be escalated to an executed reproduction before the fix phase touches them (fix-phase step 3 enforces this). Severity is exploitability × impact: Critical / High / Medium / Low. The report lists confirmed bugs first, then plausible items, then dismissed findings with dismissal reasons — transparency is part of the contract. In `--pr` scope, additionally emit findings as SARIF when asked — a SARIF 2.1.0 JSON file (`.lyra/bug-hunter/findings.sarif`, one `result` per confirmed bug with `ruleId` = BUG-N, `level` from severity, and the file/region in `locations`) that GitHub ingests via `github/codeql-action/upload-sarif` to annotate the diff, so the hunt can run as a standing CI gate instead of an on-demand ritual. A clean report is a good result; partial coverage is declared, never papered over ("scanned 40 of 122 files" beats a false "audit complete").

## Fix phase (default when bugs are confirmed; `--scan-only` opts out)

0. **Precondition: a runner exists.** The fix loop is built on executable verification — if the repo has no test runner (or tests can't run in this environment), fix mode degrades to `--dry-run`: plan the fixes as diffs, edit nothing, and say why. Running a repo's test suite is executing that repo's code: on an untrusted repository, do it in a sandbox/container (lyra-security-containers rule 5's escalation ladder), not on the host.
1. **Baseline** — run the test suite; record failures that pre-date the hunt.
2. **Branch** — create `lyra-bug-hunter/fixes-<date>`. A dirty tree stops the phase: report the uncommitted changes and let the user decide (commit, stash, or abort) — never stash someone's work-in-progress silently.
3. **One bug, one commit** — fix in confirmed-severity order, minimal diff, no drive-by refactors. Reference the BUG-N id in the commit message. Critical/High bugs whose confirmation evidence was static-only get their reproduction executed *now*, before the fix — this is a precondition, not a preference.
4. **Verify after each fix** — targeted test (write one that reproduces the bug if none exists), then the full suite against the baseline. New failures ⇒ revert that commit, mark `FIX_REVERTED`, continue with the next bug.
5. **Report** — fixed / reverted / skipped per bug, with the verification evidence.

Only CONFIRMED bugs are auto-fixed. PLAUSIBLE items ship in the report with a suggested fix but no edit.

## Non-negotiables

- **No unchallenged confirmation** — every finding passes through the Skeptic, in an isolated context when the runtime provides one, as a disciplined self-review when it doesn't; the pass is mandatory even when the finding looks obvious.
- **Evidence or it didn't happen** — every confirmed bug carries its failure scenario; every dismissal carries its counter-evidence.
- **A fix that isn't verified is a finding, not a fix.**

---

_Part of the [skill collection](../README.md)._
