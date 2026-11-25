---
name: superpowers
description: Use when planning or executing multi-step engineering work in this project - routes to the vendored Superpowers methodology (brainstorming, writing plans, TDD, subagent-driven development, verification before completion).
---

# Superpowers (vendored)

This project vendors the [obra/superpowers](https://github.com/obra/superpowers) skills framework under `vendor/superpowers/` (MIT, see `vendor/superpowers/LICENSE`). The upstream skills are the source of truth; this adapter only points to them.

## When to use

Use before any non-trivial implementation, planning, review, or completion claim:

- new feature or behaviour change;
- multi-file refactor;
- debugging a failure that is not obviously local;
- declaring work "done", "fixed", "passing", or opening a PR.

## How to use

Read the upstream skill that matches the moment, then follow it exactly:

| Moment | Skill file |
| :--- | :--- |
| Starting a feature, unclear requirements | `vendor/superpowers/skills/brainstorming/SKILL.md` |
| Turning a spec into an implementation plan | `vendor/superpowers/skills/writing-plans/SKILL.md` |
| Executing a plan task-by-task | `vendor/superpowers/skills/executing-plans/SKILL.md` |
| Fresh implementer + fresh reviewer per task | `vendor/superpowers/skills/subagent-driven-development/SKILL.md` |
| Independent work in parallel | `vendor/superpowers/skills/dispatching-parallel-agents/SKILL.md` |
| Writing code test-first | `vendor/superpowers/skills/test-driven-development/SKILL.md` |
| Debugging systematically | `vendor/superpowers/skills/systematic-debugging/SKILL.md` |
| Requesting / receiving review | `vendor/superpowers/skills/requesting-code-review/SKILL.md`, `receiving-code-review/SKILL.md` |
| Before claiming completion | `vendor/superpowers/skills/verification-before-completion/SKILL.md` |
| Finishing a branch | `vendor/superpowers/skills/finishing-a-development-branch/SKILL.md` |

## Project rules that override the framework

1. **Evidence before claims.** No "done" without a command, its output, and an artifact path. See `docs/team/VERIFICATION_PROTOCOL.md`.
2. **A detail without an owner and a test is not planned.** Traceability lives in `docs/team/OWNERSHIP_MATRIX.md`; the checker is `tools/check_team_coverage.py`.
3. **Review is a gate, not a courtesy.** Each task has a spec-compliance reviewer and a quality reviewer; the final review is whole-branch.
4. **Subagents never dispatch their own reviewers.** The controller dispatches review after the report.
5. **No production edits from review agents.** Reviewers write to `docs/team/reviews/` only.

## Attribution

Upstream: https://github.com/obra/superpowers (MIT). Vendored at commit recorded in `vendor/superpowers/README.md`; do not edit vendored skills — adapt via this file or a project-local skill.
