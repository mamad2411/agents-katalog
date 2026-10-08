---
name: conveyor-setup-bundle
description: Draft, preflight, apply, and inspect Agent Conveyor setup bundles for manager-worker operating cells through a conversational Codex setup flow.
---

# Conveyor Setup Bundle

Use this skill when the operator wants to configure a manager/worker pair or
worker set with explicit planning, loop, PR review, what's-next, derived
permission policy, and evidence policy before launch.

## Rules

- Use `.codex-workers/workerctl.db` under the current project unless the
  operator explicitly provides another path.
- Run `conveyor setup-bundle preview` before `apply`.
- If a required backend is missing, stop. Do not create sessions, bindings, or
  work prompts.
- Ask for explicit operator approval before `conveyor setup-bundle apply`.
- Treat `conveyor setup-bundle show` as the ledger truth for what setup policy
  was approved.
- Do not launch manager or worker sessions until `conveyor setup-bundle show`
  confirms an applied bundle.
- Ask only for settings that can be encoded with current `setup-bundle` flags.
  Manager permissions and worker profile shape are derived from the selected
  preset and must be verified from preview/show output, not customized through
  intake.
- If the operator wants multiple workers, collect that as post-bundle launch
  intent for `conveyor-create-worker-set` after `show` confirms the bundle is
  applied. Do not present worker count/profile as persisted setup-bundle policy.

## Conversation Protocol

Guide setup as a Codex-session conversation, not as a visual app wizard.

1. Confirm or create the Conveyor task.
2. Ask only the missing intake questions needed to build a setup bundle.
3. Translate the answers into `conveyor setup-bundle preview` flags.
4. Show the locked setup summary from the preview JSON.
5. If `preflight.missing_required` is non-empty, stop and tell the operator
   exactly which required skills or plugins need installation.
6. If preflight passes, ask whether to apply this exact setup.
7. Apply only with `--approve`.
8. Run `conveyor setup-bundle show` and report ledger proof.
9. Hand off to launch skills only after the ledger readback proves the bundle is
   applied.

## Intake Questions

Ask these in plain language and skip anything the operator has already answered:

- Setup type: autonomous ship-it, test coverage Ralph Loop, UX Ralph Loop,
  PR/CI/merge Ralph Loop, or custom.
- Planning and goalsetting: direct prompt, `codex_goal`, `goalbuddy`, or custom.
- Review Rigor: off, `codex_review`, `superpowers`, GitHub, security, composite,
  or custom.
- Ralph Loop: none, ship-it, test coverage, UX/visual diff, PR/CI/merge, or
  custom loop preset.
- What's Next Nudging: off, suggest only, or execute bounded.
- What's Next iteration cap: integer max iteration count.
- Post-merge What's Next: whether nudging may continue after a successful merge.
- Manager authority: choose a preset, then verify the derived permissions and
  denied actions from preview/show output.
- Worker launch intent: one pair or a worker set. Treat worker-set details as a
  launch handoff after bundle approval; the current setup bundle records the
  preset-derived worker policy.

## Preset Mapping

Use these defaults unless the operator chooses custom settings:

| Operator intent | Flags |
| --- | --- |
| Autonomous ship-it | `--preset autonomous_ship_it` |
| Test coverage Ralph Loop | `--preset test_coverage_ralph` |
| UX Ralph Loop | `--preset ux_polish_ralph` |
| PR/CI/merge Ralph Loop | `--preset pr_ci_merge_ralph` |
| Custom | `--preset custom` plus explicit backend flags |

## Backend Mapping

Planning flags:

| Choice | Flags |
| --- | --- |
| Direct prompt | `--planning-backend direct_prompt` |
| Codex goal drafter | `--planning-backend codex_goal` |
| GoalBuddy | `--planning-backend goalbuddy --planning-required` |
| Custom | `--planning-backend custom --planning-required --require-skill <skill>` |

Review Rigor flags:

| Choice | Flags |
| --- | --- |
| Off | `--pr-review-backend off` |
| Codex autoreview / closeout review | `--pr-review-backend codex_review --pr-review-required` |
| Superpowers review | `--pr-review-backend superpowers --pr-review-required` |
| GitHub review | `--pr-review-backend github --pr-review-required` |
| Security review | `--pr-review-backend security --pr-review-required` |
| Composite review | `--pr-review-backend composite --pr-review-required` |
| Custom review | `--pr-review-backend custom --pr-review-required --require-skill <skill>` |

Ralph Loop flags:

| Choice | Flags |
| --- | --- |
| None | `--loop-backend none` |
| Ship-it | `--loop-backend ralph_loop --loop-preset ship_it_loop` |
| Test coverage | `--loop-backend ralph_loop --loop-preset test_coverage_loop` |
| UX / visual diff | `--loop-backend ralph_loop --loop-preset visual_diff_loop` |
| PR/CI/merge | `--loop-backend ralph_loop --loop-preset pr_ci_merge_loop` |
| Custom | `--loop-backend custom --loop-preset <preset>` |

What's Next Nudging flags:

| Choice | Flags |
| --- | --- |
| Off | `--whats-next off --whats-next-max-iterations 0` |
| Suggest only | `--whats-next suggest_only --whats-next-max-iterations <n>` |
| Execute bounded | `--whats-next execute_bounded --whats-next-max-iterations <n>` |
| Allow post-merge | add `--whats-next-post-merge` |

## Commands

Create the task when needed:

```bash
TASK="example-task"
LEDGER="$PWD/.codex-workers/workerctl.db"

conveyor tasks --create "$TASK" \
  --goal "Configure an autonomous manager-worker setup before launch." \
  --path "$LEDGER" \
  --json
```

Preview the exact setup:

```bash
conveyor setup-bundle preview "$TASK" \
  --preset autonomous_ship_it \
  --pr-review-backend composite \
  --pr-review-required \
  --planning-backend goalbuddy \
  --planning-required \
  --whats-next execute_bounded \
  --whats-next-max-iterations 1 \
  --whats-next-post-merge \
  --path "$LEDGER" \
  --json
```

If required tools are missing, stop here. Do not run `apply`, do not create
manager/worker sessions, and do not weaken the configured backend silently.

After explicit approval, apply:

```bash
conveyor setup-bundle apply "$TASK" \
  --preset autonomous_ship_it \
  --pr-review-backend composite \
  --pr-review-required \
  --planning-backend goalbuddy \
  --planning-required \
  --whats-next execute_bounded \
  --whats-next-max-iterations 1 \
  --whats-next-post-merge \
  --approve \
  --path "$LEDGER" \
  --json
```

Read back ledger truth:

```bash
conveyor setup-bundle show "$TASK" \
  --path "$LEDGER" \
  --json
```

## Report Format

After `show`, report:

- preset
- planning backend and required skills
- PR review backend, gate, and required skills
- Ralph Loop backend, preset, max iterations, and required evidence
- What's Next mode, max iterations, and post-merge setting
- manager permissions and denied actions
- worker profile summary
- approved hash
- seeded acceptance criteria count, when present
- exact next action

## Handoff

Only after `show` confirms `state: "applied"`:

- Use `conveyor-create-pair` for one manager/worker pair.
- Use `conveyor-create-worker-set` for a manager with multiple workers.
- Use `conveyor-whats-next-nudger` only when the bundle enables What's Next
  nudging.

If `show` returns `blocked`, missing required tools, or no setup bundle, tell the
operator setup is not launch-ready and list the missing proof.
