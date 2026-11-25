---
name: dummyindex-update
description: "Update or pin dummyindex across the CLI package, selected Claude Code or Codex skill family, current repo wiring, and `.context/` version stamp. Resolves the latest GitHub release with a `main` fallback or accepts an exact version, detects uv tool, pipx, or pip user installation, force-reinstalls that ref, and reruns the host-aware installer. Refreshes deterministic artifacts non-destructively without running the council, reconciling, or replacing curated taxonomy; verifies that every layer moved and surfaces the changelog. Idempotent when already current unless forced. Use for `/dummyindex-update`, `$dummyindex-update`, update dummyindex, upgrade to latest, pin a version, fix version skew, or dummyindex is out of date."
---

# /dummyindex-update / $dummyindex-update [&lt;version|tag&gt;] — Update (or pin) dummyindex

> **Invocation:** Claude Code uses `/dummyindex-update`; Codex uses `$dummyindex-update`. With no argument the skill updates to the latest release; `<version|tag>` pins an exact version (for example, `0.24.0` or `v0.24.0`).

> **Installed from dummyindex `__VERSION__`.** This skill ships with the CLI, so updating also replaces this skill with the new version's copy.

Updating dummyindex by hand is fiddly because three layers drift independently:

| Layer | Where it lives | How it goes stale |
|---|---|---|
| **CLI package** | `dummyindex` on `PATH` (uv tool / pipx / pip `--user`) | A non-editable COPY; repo or GitHub changes never reach it until reinstalled. |
| **Skill family** | Claude: `.claude/skills/dummyindex*/`; Codex: `.agents/skills/dummyindex*/`; user or project scope, plus `.dummyindex_version` and per-file `.dummyindex-files.json` source/ownership records | Copied at install time; stamped with whatever version installed it. |
| **Per-repo wiring** | Claude: managed `CLAUDE.md`, hooks, and commands; Codex: active project instruction file (`AGENTS.override.md`, `AGENTS.md`, or configured fallback); both: `.context/meta.json` `dummyindex_version` | Written by `install` / `ingest`; carries the version that last touched the repo. |

You bring all three to the latest GitHub version in one pass, **non-destructively**, and prove each layer actually moved.

## Hard rules

- **Never** trigger the council, `reconcile`, or a full re-ingest. The only `.context/` write allowed is the deterministic backbone rebuild that `dummyindex install` runs on a git repo. Curated taxonomy (feature names, abstracts, conventions, audits) is left untouched.
- **Never** pass `--break-system-packages` or `sudo`. Match the install method that's already there.
- **Stop on the first failed step** and report the failing command's output. A half-updated install (new CLI, stale skills) is worse than a clean failure.
- **Idempotent.** Stop only when the CLI, every applicable selected host/scope
  skill stamp, and the current repo stamp already equal the target. A current
  CLI with stale skills or wiring continues to repair them. `--force` reinstalls
  anyway (for example, to repair a corrupt copy).

## Procedure

Run these as Bash steps, reading the output of each before the next. `REPO=MullaAhmed/dummyIndex`.

### 1. Resolve the target version

```bash
dummyindex --version            # current, e.g. 0.22.0
```

**If the user passed a version/tag** (e.g. `/dummyindex-update 0.24.0` or `v0.24.0`), use it as `<REF>` **verbatim** — accept it with or without the `v` prefix, **skip** the latest-tag resolution below, and compare the installed version against **that pinned ref** for the idempotency check (not against latest). This is how a session pins an exact version instead of always chasing latest.

**Otherwise** find the latest **release tag** (preferred — stable), falling back to `main` HEAD:

```bash
# Prefer gh; fall back to the public API; final fallback is the main branch.
gh release view --repo MullaAhmed/dummyIndex --json tagName -q .tagName 2>/dev/null \
  || curl -fsSL https://api.github.com/repos/MullaAhmed/dummyIndex/releases/latest 2>/dev/null \
       | grep -m1 '"tag_name"' | sed -E 's/.*"tag_name": *"([^"]+)".*/\1/' \
  || echo main
```

Normalise the tag (a `v` prefix is fine for the pip ref; strip it only when
comparing version numbers). **Do not stop merely because the CLI already equals
the target.** First inventory the selected host/scope skill stamps and the
applicable `.context/meta.json` stamp as described in step 3. Only print
`already up to date (X.Y.Z)` and stop when every applicable selected layer
already equals the target and the user did not pass `--force`. A current CLI
with a stale skill or repo stamp must continue to step 3. When the target is
`main` and has no comparable release version, continue rather than guessing.
`--force` reinstalls every selected layer even when versions match (including a
downgrade to a pinned older ref). For a pinned downgrade, the repo stamp in
`.context/meta.json` moves backwards only when step 3's install runs with
`--force-downgrade` (the same flag already gates rewriting a newer-stamped skill
family). Without it the repo stamp stays at the newer version; report that as
expected, not as skew.

Resolve `<REF>` to one immutable `<COMMIT>` before installing:

```bash
gh api "repos/MullaAhmed/dummyIndex/commits/<REF>" --jq .sha
```

Require a full commit id; if resolution fails, stop with the actual error.
Install that commit, and record the user-facing release/tag separately. Do not
re-fetch a moving branch between updating the CLI and its skills. Version
numbers alone do not establish source equality: run
`dummyindex context check --versions` and inspect the source warnings as well.

### 2. Detect the install method and update the CLI when needed

Probe in order and use the **first** that lists `dummyindex`:

```bash
uv tool list 2>/dev/null | grep -q '^dummyindex'   && echo "method=uv"
pipx list 2>/dev/null    | grep -q 'package dummyindex' && echo "method=pipx"
# else: pip --user (the common default)
```

If the running CLI differs from the comparable target, or the user passed
`--force`, reinstall from the resolved ref (`<REF>` = the tag from step 1, or
`main`):

- **uv tool:** `uv tool install --force "git+https://github.com/MullaAhmed/dummyIndex.git@<COMMIT>"`
- **pipx:** `pipx install --force "git+https://github.com/MullaAhmed/dummyIndex.git@<COMMIT>"`
- **pip --user:** `python3 -m pip install --user --force-reinstall --no-cache-dir --upgrade "dummyindex @ git+https://github.com/MullaAhmed/dummyIndex.git@<COMMIT>"`

If the running CLI sits inside a virtualenv (check `python3 -c 'import sys; print(sys.prefix)'` / `which dummyindex`), reinstall into that environment instead of `--user`. When in doubt, mirror exactly where `which dummyindex` resolves.

If the CLI already equals a release target and this is not `--force`, skip only
the package reinstall only after its installed source matches the resolved commit; continue to step 3 so stale skills or repo wiring are
repaired.

### 3. Refresh the skills + the current repo's wiring

Before the early-exit decision in step 1 and before running the installer,
preserve the host and scope of the skill being updated:

- Claude Code uses `--platform claude`; Codex uses `--platform codex`. Use
  `--platform both` when the user maintains both integrations. Claude AUTO also prepares the canonical `.agents` dependency; that does not add Codex project guidance.
- A family under `~/.claude/skills/` or `~/.agents/skills/` is user-scoped. A
  family under the current repo's `.claude/skills/` or `.agents/skills/` is
  project-scoped and needs `--scope project --dir <repo>`.
- If the user intentionally has different hosts in different scopes, run the
  installer once per host/scope pair instead of moving either family.

From the repo root, run the **newly installed** CLI's installer with the
selected values:

```bash
dummyindex install --platform <claude|codex|both> --scope <user|project> [--dir <repo>] [--force-downgrade]
```

This re-copies the selected skill family (including this update skill),
restamps its `.dummyindex_version`, and — when the target is a git repo —
touches `.context/`. Claude refreshes its managed guidance, commands, and hooks;
Codex refreshes the active project instruction file and does not require
`.claude/` state. **On a
curated index (council-enriched feature names, abstracts, conventions),
`install` takes the non-destructive path: it refreshes only the deterministic
artefacts and advances `.context/meta.json`'s `dummyindex_version` stamp,
leaving the curated taxonomy untouched.** Only a brand-new or
deterministic-only index is full-built. If the target is not a git repo,
`install` skips the per-repo step on its own; that is expected, not an error.

**Context-layout migration.** The same per-repo pass removes retired paths such
as `.context/equipment-evals/` and superseded graph shards. A non-generated file
under a retired path is backed up first. This is part of install's deterministic
`.context/` write, not a separate step. Install prints `removed …`,
`backed up to .context/_doc_backups/retired/<version>/…` and
`warning: migration …` lines; surface them in the final report.

**One shared installation.** AUTO reuses the existing family links where
possible. When Windows cannot create links, Claude gets thin `SKILL.md`
references to the canonical `.agents/skills` family, including its companion
paths. It does not receive another full implementation. Explicit `--copy`
remains the compatibility opt-out.

**Ownership, including same-version updates.** Each family records per-file
hashes and CLI/source fingerprints in `.dummyindex-files.json`. A version
stamp alone never authorizes an overwrite or directory replacement. Refresh
updates only missing files, exact-current files or hash-proven stock files;
unknown companions and edited files are preserved and reported. The bounded
legacy catalog recognizes exact official stock bytes from one prior release;
ambiguous legacy content remains unverified. Do not delete or rebase preserved
files to make a source warning disappear.

**Configuration stays separate.** Existing managed guidance/block and settings
merge rules remain in force. Keep user configuration and project scope. A
same-version source mismatch still needs preparation; a preserved customization
is reported as customized/incomplete, not as a verified update.

For every host, existing equipped projects retain the hash-owned
`equip refresh` path. Only pristine, non-evolved generated capabilities are
refreshed; user-edited/evolved bodies stay intact. This is best-effort and does
not qualify model behavior. The guard is an existing `.context/equipment.json`;
USER_MODIFIED bodies are preserved. If the installed project refresh was skipped,
run `dummyindex context equip refresh --root <PROJECT>` and inspect its report.
This adds no evaluation scaffolding.

### 4. Verify the result

Run the newly installed CLI's `dummyindex context check --versions` and compare:

- CLI version and resolved source commit (distribution `direct_url.json` when
  available); all applicable skill stamps and `.context/meta.json`.
- The running CLI source fingerprint and each selected family's per-file/source
  qualification. Inspect every preserved, incomplete or unverified result.
- Managed project guidance and existing user configuration remain intact.

**A stamp that did not advance is a named failure.** If step 3's output contains
`version stamp not advanced`, a required artifact failed and the repo stamp kept
its old version on purpose. Surface the artifact and the error from that line
(the line reads `warning: <artifact> failed (<error>); version stamp not advanced — …`)
and its fix: `dummyindex context rebuild --changed` after fixing the cause. Do not
re-run step 3 in a loop, and do not report the repo layer as moved.

Report the installed immutable commit, version, scope and any preserved source
mismatch. Never call a partial or customized installation fully coherent merely
because its version stamps agree. A failed required step stops the update;
optional native-adapter limitations remain visible. No council or production
live-test step belongs in this update. Finish with a compact before→after table:

```
dummyindex updated: 0.22.0 → 0.23.0
  CLI package     0.22.0 → 0.23.0  ✓
  skill family    0.22.0 → 0.23.0  ✓  (<host>, <scope>)
  this repo       0.22.0 → 0.23.0  ✓  (.context/ backbone refreshed, curated content untouched)
  context layout  removed N retired file(s), backed up M  (+ any `warning: migration …` verbatim)
```
