---
name: dummyindex-evolve
description: "Improve conventions and skill guidance from cited session evidence. Harvest, diagnose at most five scoped edits, verify exact staged files against existing project tests, then promote or discard with content-bound receipts and recoverable backups. Missing checks are blocked, and project-test qualification does not establish measured model improvement. Use for `/dummyindex-evolve`, `$dummyindex-evolve`, evolve this repo's harness, improve the skills/conventions from evidence, or run an overnight improvement pass."
---

# /dummyindex-evolve / $dummyindex-evolve — evidence → diagnosis → gated edit → decision history

> **Installed from dummyindex `__VERSION__`.** Run `dummyindex --version` to confirm the CLI matches. If they diverge, diagnose with `dummyindex context check --versions`, then run `/dummyindex-update` on Claude or `$dummyindex-update` on Codex to bring the CLI, skills, and this repo's wiring back into sync.

You are the **evolution conductor**. Turn accepted audit findings, human
corrections and verified task outcomes into one supported guidance change.
Closeout handles one bounded reflection automatically; explicit improvement work
uses **harvest → diagnose → exact gate → promote-or-rollback**. Every adoption
keeps its evidence, measured bytes and recoverable originals.

## The deterministic / LLM split (read this first)

Read `harvest.json`, diagnose a supported problem and author the smallest scoped
candidate. The CLI validates scope, executes existing project checks against the
baseline and exact candidate, binds the result to their contents, and owns history,
promotion and rollback. Never manufacture a pass from a summary or missing checks.

## The loop (run it literally)

### 1. Harvest

```
dummyindex context evolve harvest --run <name>
```

Writes `<run>/harvest.json`: audit findings, session-memory corrections, reconcile deltas (`drifted_features` / `unassigned_new_files` / `awaiting_enrichment`), and adoption misses (user turns that had to invoke the context engine manually — stored as counts + projects-root-relative citations only, never message content). Flipped predictions from earlier promotes print here too. Overnight/fleet mode: add `--sleep`; when there is nothing new it exits 0 having written nothing.

### 2. Diagnose (LLM step)

Read `<run>/harvest.json`. Emit **at most 5** candidates, each one JSON line:

```json
{"target_file": ".context/conventions/naming.md", "diagnosis": "...", "evidence": ["audits/<slug>/report.md:L12"], "change_sketch": "...", "prediction": "..."}
```

- `target_file` — one existing file (or an array of 1–5 distinct files): curated `.context/conventions/`, `.context/playbooks/`, `.context/equipment/` markdown, the legacy `.context/equipment.json`, or packaged `dummyindex/skills/**/*.md`. **Never source code, feature specs, decision history or the GC anchor.**
- `evidence[]` — citations that exist: repo-relative `path:Lline` (or `projects/<slug>/<session>.jsonl:L<n>`).
- `prediction` — falsifiable: what should change/stay true once adopted. Later harvests re-check these and flag flips.

Write them to a scratch JSONL file, then validate:

```
dummyindex context evolve diagnose --run <name> --from-file candidates.jsonl
```

The CLI re-validates every candidate (structure, scope guard, citation existence). Fix errors until it accepts.

### 3. Stage the actual files

Write each proposed file to `<run>/staged/<N>/<repo-relative-target>`. For example,
`.context/conventions/naming.md` becomes
`staged/0/.context/conventions/naming.md`. Preserve relative paths: two files named
`SKILL.md` must remain distinct. Select an existing project test that checks the
intended outcome; the candidate must not edit its own acceptance test.

For a managed capability, apply normalizes the staged frontmatter to the next
patch version before checking it. Promotion updates its ownership hash and
registry record in the same recoverable transaction as those measured bytes.

### 4. Apply + gate

```
dummyindex context evolve apply --candidate N --run <name> --tests tests/test_rule.py
```

The CLI runs the same selected pytest checks in isolated copies of the current
baseline and the staged candidate. Without `--tests`, it looks for established
tests matching target path segments. No applicable tests means **blocked**, not
success. The owner checkout stays unchanged.

A failing baseline followed by a passing candidate can qualify a repaired
project check. Candidate failures cannot be overridden; unavailable checks remain
blocked regardless of the other arm.

A passing project test qualifies that checked behavior. It does not prove a model
used the skill, obeyed every instruction or improved on real tasks. Keep actual
outcome evidence distinct from file validity and discovery. Use isolated fixtures;
production live testing is not a proposal-checklist step.

### 5. Promote / rollback / discard

```
dummyindex context evolve promote --candidate N --run <name>
```

A passing verdict adopts the measured files with originals backed up. Changed
candidate, baseline or verification inputs require another apply; an override
cannot bypass identity checks. A **blocked** verdict requires `--override "<reason>"`
for recorded manual adoption, which remains unmeasured. Failed checks cannot be
overridden. Interrupted or failed writes retain recovery information.

- Changed your mind after promoting: `rollback --candidate N --run <name>` restores the backups.
- Not worth keeping: `discard --candidate N --run <name>` drops the staged copy, adopts nothing.

## Falsification round

Each harvest compares fresh evidence paths against open predictions from earlier promotes. A flagged flip means reality contradicted the prediction — read the matched citations, draft a rollback proposal (or a corrective candidate), and say so out loud to the user.

## Discipline (non-negotiable)

- **Never hand-edit `evolution.jsonl`, `gate-*.json`, `harvest.json`, or `candidates.jsonl`.** They are CLI-owned state; hand edits poison the decision history. Corrupt JSONL lines are skipped with a warning on read — report them, don't "fix" them silently.
- **Never show or run a bare `promote` on a blocked verdict** — the refusal is the safety interlock; the override reason must be typed by someone who read why it was blocked.
- **Scope guard is a floor, not a ceiling.** Even where a target is technically allowed, ask whether it belongs to this loop or to a normal plan/reconcile.
- **Evidence over vibes**: every candidate cites existing artifacts; a diagnosis you cannot cite does not get authored.
- **Sleep contract**: fleet runners drive `harvest --sleep` overnight; exit 0 with zero writes means "nothing new" — that is success, not failure.

## Portable host compatibility

This procedure runs identically on Claude Code (`/dummyindex-evolve`) and on any portable host path (`$dummyindex-evolve` through whatever mechanism invokes an installed skill): the CLI verbs above are identical; only who orchestrates the LLM steps differs (native subagents vs. Task dispatch).

## Automatic closeout learning

After an accepted audit/build closeout, handle at most one pending event from
`dummyindex context evolve learning --next` without another user prompt. Inspect
its cited outcome and current source. Reflect once: one narrow verified rule,
or `learning --event ID --no-entry`. Create no lesson merely because the queue
exists; accepted transfers already in place need no rule.

For a supported change, write reflection JSON: `verified: true`, `target`,
`rule_id`, `body`, `expected_sha256` (reviewed whole-document hash), `sources`
(repo-relative), existing project `tests`; optional `supersedes` (old IDs,
same document). Run `learning --event ID --from-file reflection.json`. It
stages one protected rule, runs the exact gate, adopts only passing bytes.
Report pending/prepared/evaluated/applied accurately; blocked checks stay blocked.
Never recursively learn from evolution or experiment output.

`evolve evidence` imports only this project's host evidence; `evolve rules`
reports source-invalid managed rules. Chat corrections go through local probation:
follow [probation-protocol.md](probation-protocol.md). For explicit agent-quality
improvement, use native agents via [native-protocol.md](native-protocol.md):
observe task feedback before authoring general/domain proposals, then
compose from measured outcomes. External executor: [replay-protocol.md](replay-protocol.md).
No trigger-word score or deterministic fixture is evidence of model improvement.

## CLI reference

```
dummyindex context evolve harvest [--since YYYY-MM-DD] [--sleep] [--json] [--run NAME] [--root DIR]
dummyindex context evolve diagnose --run NAME --from-file FILE [--json]
dummyindex context evolve apply --candidate N --run NAME [--tests PATH] [--json]
dummyindex context evolve promote --candidate N --run NAME [--override "REASON"]
dummyindex context evolve rollback --candidate N --run NAME
dummyindex context evolve discard --candidate N --run NAME
dummyindex context evolve evidence [--claude PROJECTS] [--codex SESSIONS] [--state SQLITE --history SQLITE]
dummyindex context evolve learning --next
dummyindex context evolve learning --event ID (--from-file REFLECTION | --no-entry)
dummyindex context evolve attribute (--next | --event ID --verdict attributed|unrelated|unknown [--item ITEM] [--durable] [--retracts])
dummyindex context evolve probation report|promote|demote [--item ID]...
dummyindex context evolve rules
dummyindex context evolve experiment --run NAME --from-file SPECIFICATION
dummyindex context evolve utility
```
