---
name: autodev
description: Use when the user asks to take a task end-to-end autonomously (e.g. "autodev", "/autodev", "build this on autopilot"). Runs the full chain — plan → implement → review → PR → converge — stopping only at real decisions.
metadata:
  short-description: Autopilot — plan, build, review, PR, converge
---

# Autodev (Codex)

Full-pipeline autopilot, Codex-side. Same workflow as Claude's `/autodev`; this
skill adapts it for a Codex cockpit.

**Canonical procedure:** read `~/.codex/skills/skyhook-skills-commands/autodev.md` and follow it
(chain, modes, plan gate, the `--auto` ceiling, hand-back). Apply these **Codex
translations** wherever it names a Claude command:

| Claude command | Codex equivalent |
|---|---|
| `/plan-loop` | the **plan-loop** skill |
| `/review-loop` | the **review-loop** skill |
| `/cross-review` (cross-model) | the **claude-review** skill — from Codex the secondary reviewer stays Claude (it reviews your work) |
| `/qa` | read the repo's `.claude/commands/qa.md` and follow it (Codex reads it as a file) |
| `/pr` (verify + open/update PR) | inline via `git` + `gh`: run `/qa`, then create/update the PR (stage relevant files only, `--force-with-lease`). **Write the body per `~/.codex/skills/skyhook-skills-commands/pr.md`** — depth proportional to the change, lead with motivation + design, **no review-fix trivia, re-derive don't append**. (Codex especially tends to dump 4 terse bullets — don't.) |
| `/fix-pr-loop` (converge) | inline the reactive loop: wait for CI + bots (`gh pr checks`, `gh pr view --json comments,reviews`), triage each finding skeptically, fix the real ones, push, repeat until settled or capped. **The AI reviewers + failing build/test CI are the primary signal** — wait for those, triage them. **Don't block on CodeQL >~2 min** — it's a secondary scanner; if it's the only laggard, proceed and note `CodeQL pending` |
| `/triage-findings`, `/fix-findings`, `/simple` | no such commands — perform the discipline inline (read the real code, never auto-accept, cite evidence on skips, don't ping-pong, fix confirmed issues) |

**Non-negotiable invariants** (don't let translation lose them):
- **Default mode gates on the plan** — stop for sign-off before code. `--auto`
  logs assumptions to `NOTES.md` and proceeds, but **always stops** for the
  ceiling: prod/deploy/data-migrations · external-publish/money ·
  security/auth/secrets · breaking-public-API/destructive-file-ops.
- **Triage every reviewer skeptically; never auto-accept.** Cross-review only
  when nontrivial.
- **Scenario-sensitive work needs a ledger before "done."** For user-facing copy,
  diagnostics/remediation, detector precision, error classification,
  security/permissions, or UI states, list each scenario with expected final
  behavior/copy, source-of-truth evidence, self-review verdict, Claude status,
  tests/live proof, and open decision. Claude status is either the verdict or
  `skipped: <reason>` when cross-review was intentionally skipped. If review
  happened before later fixes, state whether the final head was re-reviewed.
- **Risk / blast radius belongs in the hand-back.** For nontrivial changes, state
  affected surface, likely failure mode, mitigation/test proof, and residual risk.
  Keep it proportional; low-risk copy/test-only work can be one sentence.
- **Every loop caps and reports** — never loop or proceed-past-a-blocker
  silently.
- **Never** merge, deploy, push to `main`, hard-`--force`, or stage unrelated
  files. PRs are fine; shipping is the user's call.
- **Narrate the run** with the glyph-tagged phase banners and close with the
  end-of-run summary ledger defined in the canonical file (per-step counts, triage
  breakdowns, result line, `--auto` assumptions, open items).
- **Phases are judgment calls, not a fixed sequence** — decide which apply each
  run, and **honor free-text steering in the invocation** (e.g. `consult claude`,
  `no PR`, `plan only`, `quick`, `focus on <area>`) as an override, per the
  canonical file's directives section.
- **UI / product-facing features:** lean toward running visual-test +
  product-review in the review phase, **before opening the PR** (recommended, not
  forced — a skip is fine when small/non-visual, but must be stated). **State
  visual-test and product-review status in the hand-back** (ran/skipped + why),
  never silent. Don't open the PR blind to its own rendered result.
- **Consider a review packet** before handing back, when the work would be hard to
  judge from the PR alone — large or multi-PR, a rendered surface, captured output
  worth showing, or open product calls. Judgement call, not a step; say if skipped.
