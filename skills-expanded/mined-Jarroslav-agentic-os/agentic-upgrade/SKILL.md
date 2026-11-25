---
name: agentic-upgrade
description: Upgrade a repo's scaffolded agentic-os layer to the currently installed plugin version — per-file three-way reconciliation via the install journal's recorded sha256 (unchanged managed files overwritten, user-modified files diffed and prompted, managed blocks replaced wholesale, generated agents offered regeneration plus re-audit — never a silent overwrite), then doctor re-run and journal stamp bump. Use when the user says "/agentic-upgrade", "upgrade agentic-os", "update the scaffolded agents/hooks", or after updating the agentic-os plugin. Not for: first-time installs (agentic-init) or verification without changes (agentic-doctor).
version: 0.1.0
license: Apache-2.0
---

## Shared contract preflight

Before workflow actions, send this JSON request to the installed plugin's
`runtime/run.py` using Python 3.10+ (resolve the plugin root on the current host):

```json
{"api_version":"1.0.0","operation":"policy.resolve","entrypoint":"agentic-upgrade"}
```

Use the returned policy and `references/runtime-contracts.md` for contract identifiers,
limits and dependency floors. Unknown fields or incompatible versions block startup.
Task envelopes use `contract_version: "1.0.0"` and `task_input`; legacy `raw_input`
is accepted only by the explicit `input.normalize` compatibility adapter with `legacy: true`.
This preflight validates policy; durable lifecycle and host enforcement are separate
capabilities. Never infer those capabilities from a successful policy response.



# agentic-upgrade — scaffold updater

You reconcile the target repo's scaffold with the newer plugin templates.
The **install journal is the third point of the three-way merge**: it records
what agentic-os last wrote (`sha256`), from which template (`template`), and
who owns the file now (`owner`). **Never overwrite silently** — every
destructive choice is either provably safe (hash-identical to what we wrote)
or user-confirmed.

Conventions (`PLUGIN`, `TARGET`, journal shape, rendering rules incl. the
`.json.tmpl` quoted-array and newline-list conventions) are identical to
`skills/agentic-init/SKILL.md` — read its "Conventions" section first.
Like init: never `git add`/`git commit` in the target repo.

When `journal.adoption.mode == "adopt-existing"`, resolve canonical agents,
skills and state from `journal.adoption` and never fall back to hardcoded
`.agentic/` paths. Entries with `origin: "adopted-existing"` are immutable: you
may verify them and report drift, but never render, replace, regenerate,
re-synthesize or delete them — and that covers Codex TOML adapters, hook
registrations and rules as much as agent contracts. Preserve Codex
configuration keys you do not recognise; an upgrade that drops a key it did not
write is indistinguishable from corruption.

## Phase 1 — Version gate

1. Read `TARGET/.agentic/agentic-os/install.json`. Missing ⇒ stop: "no install
   journal — run /agentic-init".
2. `NEW` = `"version"` from `PLUGIN/.claude-plugin/plugin.json`; `OLD` =
   `journal.agentic_os_version`.
3. `NEW == OLD` ⇒ nothing to upgrade; offer a refresh (Phase 2 with
   unchanged-only rules) or just `/agentic-doctor`, then stop.
   `NEW < OLD` ⇒ stop and escalate (plugin downgraded — human decision).
4. Re-load `journal.answers` — every re-render uses the **journaled answers**;
   the upgrade never re-interviews (changing answers is an `/agentic-init`
   re-run).

## Phase 2 — Per-file three-way reconciliation

Every write below goes through the runtime operations in init's "How journal
and file writes happen": **overwrite** an untouched managed file →
`install.apply` (no confirmation needed); **take new** on a user-modified file →
`install.apply` with `expect_sha256` = `CURRENT` and the owner the journal
records (`managed` or `generated`) — the replacement content is ours again;
**accept regeneration** of an `owner: "generated"` file → `install.apply` with
`expect_sha256` = `CURRENT` and `owner: "generated"` (never a plain apply,
which would preserve the file and record it user-owned);
**keep mine** → `install.apply` without a
confirmation (the installer preserves it and records it user-owned);
**merge by hand** → `install.apply` for the `.ao-new` path with
`owner: "user"`, so a later uninstall never deletes it as a managed file; if a
previous upgrade already left that `.ao-new`, send its current sha256 as
`expect_sha256` (with `owner: "user"`) to refresh it — a plain apply is
reported `preserved` and leaves the old render. The journal stamp in
Phase 4 is the `agentic_os_version` field of those requests or
`install.record`.

For every journal entry with a template ID (the destination map lives in
`skills/agentic-init/SKILL.md` Phase 4), compute:
`RECORDED` = journaled sha256, `CURRENT` = sha256 of the file on disk,
`NEWRENDER` = the `NEW` template rendered with `journal.answers` (including
init's installer-side conditionals: the warn-only git-sync patch when
`answers.git_sync_mode` is `warn-only`, migration-notice skip on empty
migrations dir, registry row pruning). Entries with `template: "derived"`
have **no template to render** — handle them in the derived branch below,
never via a template diff.

Then per `owner` / `template`:

**`template: "derived"` (synthesized pointer files —
`.claude/agents/<name>.md` and `.claude/commands/<name>.md` for templated
agents; init Phase 4 step 7)**
- Handle these **after** their canonical contract
  (`.agentic/agents/<name>.md`) has been reconciled.
- Canonical unchanged in this upgrade ⇒ skip the pointer.
- Canonical rewritten/regenerated ⇒ re-synthesize the pointer from the new
  canonical using the same synthesis rule as init (the pointer formats in
  `PLUGIN/generators/agent-generator.md` §2/§3): `CURRENT == RECORDED` →
  overwrite and update the journal sha; `CURRENT != RECORDED`
  (user-modified pointer) → show current → re-synthesized diff and ask
  keep (→ `owner: "user"`) / re-synthesize.

**`owner: "managed"` (regular files)**
- File deleted on disk ⇒ ask: restore from `NEWRENDER` or journal as removed.
- `CURRENT == RECORDED` (untouched since we wrote it) ⇒ **overwrite** with
  `NEWRENDER`, update the journal sha. Report one line per file.
- `CURRENT != RECORDED` (user-modified) ⇒ **show the template-old→new diff
  and ask**. Old render recovery: the plugin installs from a git marketplace,
  so try `git -C PLUGIN_REPO show agentic-os-v<OLD>:<template path>` (where
  `PLUGIN_REPO` = the marketplace clone containing `PLUGIN`; the per-plugin
  tag form `agentic-os-v<OLD>` is the policy since the first release — fall back to
  `v<OLD>` or `<OLD>`), render it with `journal.answers`, and diff old-render
  → new-render — that shows the user exactly what the *template* changed,
  separate from their local edits. If the old version is unrecoverable, fall
  back to diffing `CURRENT` → `NEWRENDER` and say so explicitly (that diff
  mixes their edits with template changes). AskUserQuestion per file:
  **keep mine (default)** → journal flips to `owner: "user"`;
  **take new** → overwrite, stays `managed`;
  **merge by hand** → write `NEWRENDER` to `<path>.ao-new` beside it, journal
  a follow-up, leave the live file alone.

**Managed blocks (`CLAUDE.md`, and `AGENTS.md` when it was installed as an
appended block on a mature repo)**
- A block file the journal records user-owned (it pre-existed install) is
  still refreshed: apply the merged text under init's merge rule
  (`expect_sha256` of its current bytes); it stays user-owned.
- Replace the content between `<!-- agentic-os:begin v… -->` and
  `<!-- agentic-os:end -->` **wholesale** with the newly rendered block (the
  begin marker carries the new version stamp — it is rendered from
  `{{AGENTIC_OS_VERSION}}` in
  `PLUGIN/templates/governance/CLAUDE.section.md.tmpl`). Content outside the
  markers is never touched, even if the user edited inside the markers (the
  markers say "do not edit inside" — still, mention in the report when the
  replaced block had drifted).
- Markers missing entirely (user deleted the block) ⇒ ask before re-appending.

**`owner: "user"`**
- Never touched. If the corresponding template changed between `OLD` and
  `NEW`, add one report line ("template <ID> changed upstream; your file
  <path> is user-owned — diff available on request").

**`owner: "generated"`**
- **Never auto-overwritten.** If the generator inputs changed in `NEW`
  (`PLUGIN/generators/agent-generator.md`, `guide-generator.md`, the matching
  stack profile, or the exemplars) — or unconditionally, as a cheap default —
  **offer regeneration**: re-run init Phase 5 for that slot (same subagent
  prompt assembly, same ≤2-retry audit loop against
  `.agentic/guides/standards/instruction-quality-rubric.md`, same decision-6
  relaxed fallback) and update `docs/audits/instruction-scorecard.json`
  (`content_sha256` + `composite_score`, per-agent `gate_threshold` only when
  relaxed). Declined ⇒ leave the contract, but if its scorecard entry is now
  stale the instruction gate will block its spawn — warn about that
  explicitly.

**Agent registry (`.agentic/guides/agent-registry.md`, `owner: "managed"`,
`template: "governance/agent-registry"`)** — handled specially, **never**
through the plain `owner: "managed"` branch above, even when
`CURRENT == RECORDED`, and **after** every `owner: "generated"` regeneration
decision in this same upgrade pass has been finalized (same "process this
after its dependency" pattern as the `template: "derived"` pointer-file
branch above) — a slot regenerated in this pass needs its row's text
refreshed before this section reconciles the file, not after: this file is a
hybrid of **three** parts, not two. The table row whose first cell is the
literal `<!-- generated-agent-rows -->` marker, and everything above it, is
ordinary template output (the curated preset rows). The **contiguous run of
table rows immediately after** that marker row is orchestrator-appended state
from init Phase 5 step 6 (one row per generated writer/gate agent) — state the
template render has no knowledge of and would silently discard. And everything
below that run — the closing paragraph and the `## Orchestration rules` section
— is template output again. Forgetting that third part is what a two-way split
does, and it truncates the file at the marker row.
- Split `CURRENT` into **three** parts, not two — the file does not end at the
  generated rows, and a two-way split silently discards everything past them:
  - `head_current` = everything through and including the marker row (the
    marker row stays with the head, so it is never duplicated or dropped on
    reassembly);
  - `generated_rows` = the **contiguous run of table rows immediately after**
    the marker row, verbatim, byte-for-byte (empty when nothing has been
    generated yet — a fresh install, or any no-code union);
  - `tail_current` = **everything from the first line after `generated_rows`
    ends, through end of file** (i.e. scanning down from the marker row: the
    first line that is not one of those contiguous table rows; when
    `generated_rows` is empty, the line immediately after the marker row) —
    the closing explanatory paragraph and
    the whole `## Orchestration rules` section. This is ordinary template
    output, exactly like `head_current`, and it is **not** optional: those
    rules (one-owner-per-intent, gates-are-read-only, the escalation ladder)
    are cited from elsewhere in the scaffold.
- Compute `NEWRENDER` from the `NEW` template as usual and split it the same
  way. A bare template render has an **empty** `generated_rows` (nothing has
  been generated in an upgrade-only pass), so its head and tail together are
  the entire file.
- Reconcile **`head_current` vs. `head_newrender`, and `tail_current` vs.
  `tail_newrender`** — both are template output — using the same spirit as the
  `owner: "managed"` diff-and-ask rule above (untouched ⇒ overwrite that
  portion; user-edited ⇒ show diff, ask). Never reconcile `generated_rows`
  against the template: the template has no knowledge of them. The marker row
  is part of the head diff like any other row, so a genuine upstream template
  change to it (should one ever happen) still surfaces normally instead of
  being silently frozen. **One deviation from
  that rule, and it matters**: the "keep mine" outcome must **never** flip
  this file's journal `owner` to `"user"` the way it does for an ordinary
  managed file. This file's `owner` stays `"managed"` /
  `template: "governance/agent-registry"` **permanently**, regardless of how the
  head or tail diff was answered — because `owner: "user"` means "never touched
  again" (see the generic `owner: "user"` rule above), and that would
  silently and permanently stop this file from ever reconciling
  `generated_rows` on every future upgrade too, disabling the very feature
  this whole section exists to provide, with no warning. A declined head or
  tail update just leaves that portion as-is for this pass — the
  same diff is offered again on the next upgrade; that's an acceptable
  minor repetition, not a workaround for a real problem.
- Reassemble **all three parts, in order**: reconciled head (**already ends
  with the marker row** — do not insert it again), **immediately followed by**
  `generated_rows` unchanged, **immediately followed by** the reconciled tail.
  Write that back. Dropping the tail here truncates the file at the marker row
  and destroys the `## Orchestration rules` section. Check 8's structural rules
  (8a–8f) cannot see that damage — the marker row, the table block, and the
  generated rows all survive it, and GitHub still renders a valid table — which
  is exactly why doctor grew **Check 8g** (the tail survived). Do not rely on
  8g to catch your mistake here; it is the last line of defence, not the first.
  Never run the reconciled generated-agent rows through
  `AskUserQuestion` — they are not the user's content to diff against a
  template, they are this feature's own state, already governed by init
  Phase 5 step 6's insert-or-replace-by-path rule.
- **Sanity-check the result before writing.** The invariant is *structural*, not
  textual: the bytes you write below `generated_rows` must be **exactly the
  reconciled tail** — whichever of `tail_current` or `tail_newrender` the
  diff-and-ask settled on — and that tail must be **non-empty**. Nothing else.
  A tail that is empty, or that is neither candidate, means the split was
  computed wrong ⇒ **stop and report; do not write.**
  - Do **not** gate on headings or line count against either `CURRENT` or
    `NEWRENDER`. Both directions produce false aborts on legitimate upgrades: a
    *declined* tail update keeps a tail lacking a heading the new template
    added; an *accepted* one takes a tail in which upstream renamed or removed a
    heading `CURRENT` had. Neither is data loss — both are the diff-and-ask
    working as designed. The only thing worth asserting is that a tail is there
    and is the one the human chose.
  - An **empty `tail_current`** is always damage, never a legitimate state: the
    template unconditionally renders a closing paragraph and an
    `## Orchestration rules` section below the marker row (it did so even before
    the marker row existed). So an empty `tail_current` means this file was
    already truncated by an upgrade run under the old two-way split. Do not pass
    it through vacuously and do not treat it as "the user's tail": say so, and
    reconcile it against the non-empty `tail_newrender` so the diff-and-ask can
    restore the section. **"Keep mine" is not offered here** — an empty tail is
    not content to preserve, and the non-empty-tail rule above would refuse the
    write anyway. Take theirs, or stop and report.
- **Re-stamp both the journal and the scorecard** for this file, same as
  init Phase 5 step 7 — this write changed the file's bytes just as surely
  as an install-time append does, and the failure mode is identical if you
  skip either: journal `sha256` stale ⇒ every future `/agentic-upgrade` sees
  a false "user-modified" and asks needlessly; scorecard `content_sha256`
  stale ⇒ `.claude/hooks/instruction_gate.py` hard-blocks the spawn of
  `dispatcher` (and any other agent citing this guide) with "stale" until a
  human runs `/instruction-auditor` — on the very next spawn after this
  upgrade, not eventually. Scorecard entry stays `composite_score: 100`,
  `source: "template-inherited"` (same rationale as init: the reconciled head
  and tail are template output, the preserved/replaced rows follow a
  strict mechanical format, none needs a fresh audit pass).
- **Same-pass regeneration**: before starting the split above (per the
  ordering rule at the top of this section), for every slot whose canonical
  contract was regenerated in this pass (the `owner: "generated"` branch
  above), re-apply Phase 5 step 6's replace-by-path logic to that slot's row
  in `CURRENT` — so head/`generated_rows`/tail are computed from a
  file whose rows already reflect the regenerated contract's actual
  triggers, not stale text from before this upgrade.
- **Before splitting, require the shape.** If `CURRENT` fails **any** of
  `/agentic-doctor`'s Check 8 shape rules (8a–8d — read them there; they include
  a missing or mangled `| --- |` delimiter, a marker that is a bare comment line
  rather than a table row, a marker in some other table, more than one marker,
  and a blank line breaking the run of generated rows) ⇒ **do not split.** A
  non-contiguous run would silently reclassify the trailing generated rows as
  `tail_current`, where an "overwrite / take theirs" answer destroys them.
  Report the Check 8 failure and stop. Only the case of **no occurrence of the
  marker string anywhere in the file** takes the branch below — a marker present
  as a bare comment line is a shape failure, not a missing marker, and stops
  here.
- **Marker missing from `CURRENT` entirely** (a repo installed under a
  plugin version that predates this marker — every install before this fix
  shipped) ⇒ **do not guess where the split is.** Same rule as the CLAUDE.md
  managed-block's "markers missing entirely" case above: ask before doing
  anything. Show the user `CURRENT` in full and ask whether it contains any
  hand-appended stack-specific rows worth preserving.
  - If **yes**, have them point out which lines. Those lines **must be
    contiguous table rows, and must be the final rows of the routing table**
    (nothing but non-table content may follow them inside the table block). If
    the selection is non-contiguous, is not the tail of the table, or includes a
    curated preset row ⇒ **stop and report; do not write.** Anything else
    silently sweeps curated rows into `generated_rows` — where they are never
    reconciled against the template again, permanently frozen — or drops them
    into `tail_current`, where an "overwrite / take theirs" answer deletes them.
    That is the same destruction the shape precondition above refuses to perform
    on a structurally-detected file; a human pointing at lines does not make it
    safe. On a valid selection: those rows become `generated_rows`, everything
    above them (with the marker row inserted as its new last line) becomes
    `head_current`, and everything below them becomes `tail_current`.
  - If **no rows exist yet**, insert the marker row as the last row of the
    routing table: everything through it is `head_current`, `generated_rows` is
    empty, and the remainder of the file is `tail_current` — the common case for
    a repo that installed before any capability ever applied.

  Either way the marker is retroactively added, so every later upgrade of this
  file takes the fast, unattended path; then proceed with the normal
  reconcile/reassemble steps
  above.

**Guide index (`PATTERNS.md`, `owner: "managed"`, `template: "governance/patterns"`)**
— handled specially, **never** through the plain `owner: "managed"` branch, and
after every `owner: "generated"` decision this pass (the generated-guide set may
have changed). Unlike the agent registry, its generated rows are **fully derived**
from the journal, so they are **regenerated, not preserved** — no three-way split,
no "keep mine", no 8g-class truncation trap. The rebuild is self-healing: it fixes a
marker or rows left malformed by an older install.
- The run of table rows directly below the `<!-- generated-guide-rows -->` marker
  row is orchestrator state (init Phase 5 step 6b); everything above the marker row
  and everything below that run is template output.
- Reconcile the template output — head (through the marker row) and tail (from the
  first non-row line after the run to EOF) — as an ordinary managed diff-and-ask.
  **Never** diff the generated-guide rows against the template; it has none.
- **Rebuild** the run: drop whatever rows are below the marker, then emit one row
  per guide in init Phase 5 step 6b's fixed **Guide path → Label** table whose path
  is present in the journal as an `owner: "generated"` file, in that table's order.
  A guide dropped since last upgrade loses its row; a newly generated one gains one
  — both fall out of the journal automatically, with no diff to answer.
- **Marker missing** (a repo installed before this marker shipped) ⇒ insert the
  marker row as the guide table's last base row, then rebuild. No need to ask about
  hand-appended rows the way the agent registry does: these rows were never the
  user's to edit, so there is nothing to preserve — just regenerate.
- Owner stays `"managed"` / `template: "governance/patterns"` **permanently** (same
  reason as the agent registry: `owner: "user"` would silently disable regeneration
  forever). **Re-stamp journal + scorecard**, same as init Phase 5 step 7.

**New/removed template IDs**
- Template IDs newly present in `NEW`'s preset union (re-resolve the union
  from `journal.answers` presets against `PLUGIN/presets/roles/*.json`) but
  absent from the journal ⇒ scaffold them exactly as init Phase 4 does
  (collision prompts included).
- Journaled IDs no longer shipped ⇒ never auto-delete; list them as
  "orphaned — safe to remove manually".

## Phase 3 — Settings + git hooks refresh

1. Re-run init's settings deep-merge with the `NEW`
   `PLUGIN/templates/hooks/settings-fragment.json.tmpl` (append-if-absent,
   set-union, pruning rule for unscaffolded hook scripts, **diff shown and
   confirmed before write**).
2. If `.githooks/pre-commit` or `scripts/install-git-hooks.sh` was updated in
   Phase 2, re-run `bash scripts/install-git-hooks.sh` (idempotent; chains a
   foreign hook as `pre-commit.local`, never replaces it).

## Phase 4 — Verify and stamp

1. Re-run the `agentic-doctor` skill; it rewrites
   `.agentic/agentic-os/doctor.json`. Fix-or-report any `failures`.
2. Bump the journal: `agentic_os_version` = `NEW`, refresh every touched
   file's `sha256`, append `follow_ups` for merge-by-hand files
   (`<path>.ao-new`), declined regenerations, and orphaned templates.
3. Report: files overwritten / prompted / kept / regenerated / newly
   scaffolded / orphaned, the managed-block version bump, the doctor verdict,
   and the reminder that committing the upgrade diff is the human's call.
