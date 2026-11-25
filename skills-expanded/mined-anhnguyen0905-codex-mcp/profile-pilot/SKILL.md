---
name: profile-pilot
description: Conditional deliverable, evidence and run-language rules.
---

# Profile pilot (multiscope Phase 1)

Load when `profileMode` is `enforce`, `evidenceMode` not `off`, or `languageMode` `on`. Rules replace gates; switches independent. Router applies to confirmed `data`, `design`, `plan` or `content` profiles. For `design`, `plan` or `content`, load `codex-flow:profile-<profile>`; Rubric replaces data list.

**Helpers**: required — profile-router.mjs, evidence-check.mjs, scope-check.mjs, language-check.mjs; helper rule: paths are `scripts/profile-router.mjs`, `scripts/evidence-check.mjs`, `scripts/scope-check.mjs`, `scripts/language-check.mjs`; missing helper → STOP; tell user to reinstall; profile-router.mjs or `scope-check.mjs snapshot` non-zero → surface error; STOP; scope-check task exit 1 is a blocking finding per the scope trip-wire; evidence-check.mjs exit 1 or 2 → Codex.

## Router (enforce, non-code profiles)

| Gate | Replacement |
| --- | --- |
| Known-red test baseline | Snapshot inputs/sources with paths, `du -h` sizes, sha256 for each non-code profile (data: row counts) in PLAN.md Known-red; initialize `--known-red "n/a (<profile> profile)"`. |
| Verify command | Use `evidence-check.mjs` as `verifyCommand` when `evidenceMode` is `enforce`; otherwise omit it and use the `exec-deliverable` Verification block, with Claude re-deriving one figure. |
| Codex review git diff | Run `codex_review` on deliverable, manifest, and rubric. |
| Checkpoint task commits | Approve `--checkpoint-commits no`; record each task's base as the tree id from `node "${CLAUDE_PLUGIN_ROOT}/scripts/scope-check.mjs" snapshot`; scope-check takes it as `--base`. |

Non-code tasks embed `codex-flow:exec-deliverable` blocks instead of coding blocks; these replacements take precedence over generic command steps.

## Profile correction

If confirmed profile is `code` or `mixed` while enforcing, run skipped Phase 0 gates: run the known-red baseline, record it with `flow-state set knownRed "<compact list>"`, note the correction in PLAN.md's Known-red section, then apply normal gates: `verifyCommand`, git-diff review, and the checkpoint question.
If corrected to a non-code profile while enforcing, run `flow-state set profile <p>`, keep the baseline, and apply Router replacements.

## Evidence

Embed the Evidence block and use the checker only when `evidenceMode` is not `off`; with evidence `off`, non-code tasks use the `exec-deliverable` Verification block alone.

```
Evidence block
- Write `evidence.json` beside deliverable with `schemaVersion: 2` (v1 rejected), `deliverable`, `figures` (id, value, command, optional tolerance, timeoutMs, display), `claims` (id,text,sources), optional `tables[]` and `ignoreNumbers`.
- Put `<!--Fn-->` directly after every measured prose number. Copied tables need a `<!--Tn-->` caption and `tables[]` command printing header-first CSV; compare cells exactly; do not anchor the table's numbers.
- Use `ignoreNumbers` only for structural literals: no `.`, `,` or `%`, integers ≤ 100; never a figure value or display.
- Every claim cites at least one figure id. V2 adds `anchor-mismatch`, `anchor-unknown`, `unanchored-number`, `table-unknown`, `table-mismatch`, `table-command`, and `claim-no-figure`; existing findings apply.
- Keep commands portable: use `node`, `duckdb`, or `python3` from manifest directory.
- Run `evidence-check.mjs --manifest evidence.json` before finishing; orchestrator gives absolute path.
```

In shadow, run checker with `--json` after acceptance and record it in reviews.md without blocking. In enforce, command with absolute plugin root is `verifyCommand`. Exit 1 is a finding and exit 2 a manifest error; route either to Codex. evidence.json is executable: commands use operator shell and share verifyCommand trust; review them like code.

## Fast-path analysis lane

When `CODEX_FLOW_EVIDENCE` is `shadow` or `enforce`, write `evidence.json` (v2) beside the deliverable and run checker. In `enforce`, deliver only after exit 0; in `shadow`, put the result in the "what I verified" note. Append `evidence=<pass|fail|off>` to `fastpath.log`.

## Rubric and sampling

For data deliverables, when routing enforces or evidence on, score each item pass/fail with evidence in reviews.md:

- `reproducible`
- `sourced`
- `answers the question`
- `decision-useful`
- `language-consistent`

When evidence is not off, run checker with `--sample 3 --seed <task number>` and ask the owner to verify three claims in ONE AskUserQuestion, one per claim. Record answers in reviews.md. A wrong claim routes back to Codex.

## Run language

When enforcing, first interview question confirms profile; with `languageMode` `on`, it also confirms run language (one AskUserQuestion can carry both). Record corrected profile with `flow-state set profile <p>`. `mixed` resolves to `vi` or `en`; record it with `flow-state set runLanguage <vi|en>`. Every Codex prompt gets this line immediately after the `Run position:` line:

`Deliverable language: <vi|en>`

Write acceptance criteria and reports in that language; this overrides session-report's latest-message rule. Keep code/comments in English.

With `languageMode` `on`, after acceptance run `node "${CLAUDE_PLUGIN_ROOT}/scripts/language-check.mjs" --deliverable <path> --language <runLanguage>` on each deliverable. With `profileMode` `shadow` or `off`, report in reviews.md. With `enforce`, exit 1 (`untranslated-term` or `wrong-language-term`) is a finding routed to the executor. Exit 2 is a usage error: surface it and STOP. With `languageMode` `off`, never run it.

## Ledger

The run-ledger append carries `--profile-mode`, `--evidence-mode`, and `--language-mode` from STATE.md. Missing optional keys in older STATE.md mean `off` for modes and `-` for `profile` and `runLanguage`.
