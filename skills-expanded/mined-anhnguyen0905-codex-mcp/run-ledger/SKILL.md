---
name: run-ledger
description: Append one durable run record per lane and summarize the append-only ledger.
---

# Run ledger (embed into Claude prompts)

## When to append

Append exactly one record when the lane reaches its terminal outcome: `full` after the final
review and delivery gates, `fast-path-analysis` or `fast-path-small` after its result or
escalation, and `brainstorm` after the analysis is accepted, rejected, or parked. Append after
the lane log, using the same run id, request, and session start.

## The call

Use the exact CLI below. `--project` is the absolute project path; `--request-file` may replace
`--request`. `--started` is the run's session-start ISO timestamp. Omit `--language` to let the
helper detect it; pass it only to correct a wrong detection. `--skills` and `--bypasses` are
comma-separated; omit them when empty. Exit 0 means written, exit 2 means usage or validation
error with nothing written, and exit 1 means I/O failure.

```sh
node "${CLAUDE_PLUGIN_ROOT}/scripts/run-ledger.mjs" append --lane <lane> --project <abs-path> --run-id <id> --profile <profile> --profile-mode <m> --evidence-mode <m> --language-mode <m> --domain <text> --request-file <path> --skills <a,b> --fix-rounds <n> --codex-tokens <n> --started <ISO> --owner-gates <n> --bypasses <a,b> --outcome <outcome>
```

Modes come from STATE.md (`profileMode`, `evidenceMode`, `languageMode`); omit them only when STATE.md
lacks these keys. The examples below show legacy/minimal runs whose STATE.md lacks these keys.

Complete calls, one for each lane:

```sh
node "${CLAUDE_PLUGIN_ROOT}/scripts/run-ledger.mjs" append --lane full --project /workspace/app --run-id run-1 --profile code --domain implementation --request "Ship the fix" --fix-rounds 1 --started 2026-11-13T04:41:51Z --owner-gates 2 --outcome accepted
node "${CLAUDE_PLUGIN_ROOT}/scripts/run-ledger.mjs" append --lane fast-path-analysis --project /workspace/app --run-id run-2 --profile data --domain retention --request "Analyze retention" --fix-rounds 0 --started 2026-11-13T04:41:51Z --owner-gates 0 --outcome delivered
node "${CLAUDE_PLUGIN_ROOT}/scripts/run-ledger.mjs" append --lane fast-path-small --project /workspace/app --run-id run-3 --profile code --domain config --request "Update config" --fix-rounds 0 --started 2026-11-13T04:41:51Z --owner-gates 0 --outcome done
node "${CLAUDE_PLUGIN_ROOT}/scripts/run-ledger.mjs" append --lane brainstorm --project /workspace/app --run-id run-4 --profile plan --domain roadmap --request "Choose a roadmap" --fix-rounds 0 --started 2026-11-13T04:41:51Z --owner-gates 1 --outcome parked
```

## Classifying profile and domain

Choose `profile` from the dominant deliverable: `code`, `data`, `design`, `plan`, `content`, or
`mixed`. Choose `domain` as a concise non-empty label (at most 80 characters) for the subject,
such as `retention`, `mobile UI`, or `release planning`; do not invent a second taxonomy.

Count every AskUserQuestion call made by the run as one `ownerGates`. Count each Codex fix round
after the initial execution as one `fixRounds`; review-only turns are not fix rounds.

## Field sources

| Lane | `--run-id` | `--started` | `--codex-tokens` | `--fix-rounds` | `--owner-gates` |
| --- | --- | --- | --- | --- | --- |
| full | report dir name, e.g. `20261113-114151` | PLAN.md `- Session start:` | input + output tokens from the `session-cost.mjs` Totals already produced for `cost.md` | total `codex_continue` fix rounds across tasks and final review | number of AskUserQuestion calls |
| brainstorm | run dir name | FRAME.md provenance session start | omit (null) unless measured | Reason rounds run | number of AskUserQuestion calls |
| fast path | ISO timestamp written on its `fastpath.log` line | time Claude decided the lane; record it at the gate | omit (null) unless measured | `codex_continue` rounds | number of AskUserQuestion calls |

Vietnamese typed without diacritics is detected as `en`; pass `--language vi` to correct it. Ledger
data stays local and is never deleted by the helper (D5); the owner may delete the file by hand.

## Counting

Pass `--codex-tokens` when the run reports it; otherwise omit it. Pass `--bypasses` for each
recorded bypass. Use `--outcome` exactly as one of `accepted`, `rejected`, `parked`, `delivered`,
`done`, `escalated`, `failed`, or `abandoned`.

## Best-effort rule

The ledger is best-effort: report a non-zero exit to the user and continue; never stop a run for it.
One operator writes one append per run; concurrent writers are not supported.

## Reading the ledger

Inspect aggregates with:

```sh
node "${CLAUDE_PLUGIN_ROOT}/scripts/run-ledger.mjs" summary [--project <abs-path>] [--json]
```

The summary reports totals, profile × language × outcome counts, medians, bypass rate, and
malformed-line count. An empty ledger prints `run-ledger: no runs recorded`.
