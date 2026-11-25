---
name: skill-manager
description: "Maintain the local .agent-share skill library: source sync, skill lifecycle, manifest provenance/packs, canonical lib copies, always-on links, agent fragments, and consistency audits. Use for any .agent-share or registry mutation. Skill-creator supplies the authoring/evaluation method; skill-manager owns writes, provenance, materialization, and final audit."
---

# Skill Manager

Maintain `.agent-share` skill assets. Execute the requested maintenance
operation; do not use this skill for ordinary project work or to decide whether
a skill should exist.

## Execution model

1. Identify the requested operation: sync upstream, add skill, add custom
   skill, delete skill, modify skill, rename skill, change pack, edit agent
   fragment, runtime activation, or audit.
2. Inspect only the files needed for that operation: usually `manifest.yaml`,
   the relevant `lib/<skill>/`, `sources/<repo>/<path>/`, `skills/`, and
   affected `agents-fragments/`.
3. Follow the matching workflow below. Do not mix workflows unless the user
   requested a compound change.
4. For mutations, clean up stale links or leftover files created by the
   operation. Audits are read-only: report inconsistencies without repairing
   links, syncing sources, installing dependencies, or writing files.
5. Run the audit checklist after every workflow and report only: changed paths,
   audit result, and any unresolved inconsistency requiring a user decision.

## Model

- `sources/`: pristine upstream clones. Sync only; no local normalization edits.
- `lib/<skill>/`: canonical maintained skill copies. Local normalizations live
  here.
- `agents-fragments/AGENT-*.md`: reusable project-instruction fragments
  consumed by `project-setup`; neither skills nor manifest entries.
- `skills/<skill> -> ../lib/<skill>`: materialized discovery view for
  `pack: always-on` only, never a second canonical copy.
- Runtime activation roots live outside this repo. They link installed agents
  to `~/.agent-share/skills/` and never own skill content.
- `manifest.yaml`: sole registry for name, pack, source URL/path, the full
  `source_commit` accepted for each upstream-backed skill, and local
  normalization intent (`notes`). Custom skills omit `source_commit`; this
  repo's Git history versions them. `sources/` HEAD is only a cache state, not
  the installed baseline.

## Rules

- Mutate the narrowest layer that owns the requested change.
- Edit `lib/`, never `sources/`, except when syncing upstream clones.
- Keep `lib/` flat: one directory per skill, no pack folders or non-skill
  support directories. Keep agent fragments in top-level `agents-fragments/`.
- Add or delete only skills the user requested; never import unregistered
  sibling skills from a source repo.
- When authoring, redesigning, or evaluating a skill, load `skill-creator` for
  method; `skill-manager` remains the sole writer, provenance owner, and
  auditor inside `.agent-share`.
- Update `manifest.yaml` before or with any change to provenance, pack
  membership, naming, or normalization intent.
- Use relative symlinks in `skills/` and runtime roots. Resolve bundled
  resources from the canonical skill directory, not a symlink's lexical parent
  or the caller's working directory. Project skill roots use `.agents/skills/`.
- Never copy `always-on` skills into runtime roots; link roots or entries to
  `~/.agent-share/skills`.
- Never create side registries, trash files, transitional docs, or
  compatibility copies unless explicitly requested. Remove stale links and
  leftovers within the maintenance scope.

## Workflows

### Runtime activation

Keep existing global skill directories that work. For new setups, use
`~/.agents/skills` where supported. Use `~/.claude/skills` for Claude Code
and `~/.gemini/antigravity-cli/skills` for `agy`.

Add a relative symlink to `~/.agent-share/skills/<name>` for each `always-on`
skill with no entry. Leave existing files and links untouched.

Report missing or incorrect links for `always-on` skills. List any links for
skills that `manifest.yaml` does not mark as `always-on`.

### Sync upstream

1. Read each affected entry's `source_commit` and `notes`, and diff that exact
   upstream tree against `lib/<name>` to identify the local delta. `notes`
   define intent; a diff is evidence, not permission to preserve every change.
   If the recorded baseline is missing, establish it from Git history and
   source evidence before replacing content; never assume cache HEAD.
2. Verify the source checkout is clean and its remote matches the manifest.
   Fetch, resolve the requested ref (or upstream default branch) to a full
   commit SHA, and inspect changes to selected paths. Fast-forward clean
   checkouts; never reset dirty or diverged branches. Investigate a missing or
   moved source path rather than deleting the skill.
3. Review changed instructions, scripts, dependencies, links, and licensing
   before executing new upstream code. Update only registered skills and
   preserve local-only distribution restrictions.
4. Stage a fresh candidate outside `lib/` from the tracked tree at that exact
   commit, preserving dotfiles, file modes, and symlinks while excluding
   repository internals (`.git`) and runtime caches.
5. Reapply only local normalizations that still serve the skill's intent;
   retire patches superseded upstream or no longer needed. Review the
   candidate's diff against the new pin and update `manifest.yaml.notes`.
6. Check changed entry points and plausible failure modes (using focused
   bundled tests when they cover the change). Replace `lib/<name>/` once
   verified; skip replacement if the incoming tree is identical.
7. Advance `source_commit` with the accepted content, including when a new
   commit has an identical selected tree. Fetching alone never advances this
   field.
8. Remove temporary staging and backup files after success; never store
   generated diffs or a separate patch registry in the repo.

### Add skill

1. Add or update the source repo entry in `manifest.yaml` if needed.
2. Resolve and review an exact upstream commit. Add the manifest entry: `name`,
   `pack`, `source_repo`, `source_path`, full `source_commit`, and optional
   `notes`.
3. Materialize the reviewed tracked tree into `lib/<name>/`, preserving
   dotfiles, file modes, and symlinks while excluding repository internals and
   runtime caches.
4. Apply any local normalizations in `lib/<name>/` and record their intent in
   `manifest.yaml.notes`.
5. If `pack: always-on`, create `skills/<name> -> ../lib/<name>`.

### Add custom skill

1. Load `skill-creator` for capability design, triggering, resources, and
   evaluation.
2. Create `lib/<name>/SKILL.md` and required resources.
3. Add the manifest entry with `source_repo: custom`,
   `source_path: "lib/<name>"`, `pack`, and `notes` when needed.
4. If `pack: always-on`, create `skills/<name> -> ../lib/<name>`.

### Delete skill

1. Remove `skills/<name>` if present.
2. Remove the manifest entry.
3. Remove `lib/<name>/`.
4. Remove the source repo only if unreferenced and explicitly requested.
5. Delete stale references to the removed skill name.

### Modify skill

1. Load `skill-creator` when the change involves capability design, prompt
   quality, triggering, or evaluation.
2. Update `manifest.yaml.notes` first if the change introduces or alters local
   normalization intent.
3. Edit skill content in `lib/<name>/`.

### Rename skill

1. Update `name` in `lib/<old-name>/SKILL.md` frontmatter and in
   `manifest.yaml` (along with `source_path: "lib/<new-name>"` for custom
   skills and any affected `notes`).
2. Rename `lib/<old-name>/` to `lib/<new-name>/`.
3. If `pack: always-on`, replace `skills/<old-name>` with
   `skills/<new-name> -> ../lib/<new-name>`. Note affected per-skill links in
   known runtime roots (directory links to `~/.agent-share/skills` follow
   automatically), and migrate them when runtime sync is in scope.
4. Update or remove stale references to the old name.

### Change pack

1. Update `manifest.yaml.pack`.
2. Entering `always-on`: add `skills/<name> -> ../lib/<name>`.
3. Leaving `always-on`: remove `skills/<name>`.

### Modify agent fragment

1. Edit only the relevant `agents-fragments/AGENT-*.md` file; keep filenames
   descriptive and stable unless a rename was requested.
2. Do not add fragment entries to `manifest.yaml`.
3. If a rename affects target projects, update them through `project-setup`
   rather than hand-editing generated `AGENTS.md`.

## Audit checklist

Run the default audit after any library change (requires Python 3.10+ with
PyYAML; use `.venv/bin/python` when present):

```bash
.venv/bin/python -B lib/skill-manager/scripts/audit.py
```

It checks registry consistency, `SKILL.md` frontmatter (including boolean
`disable-model-invocation`), canonical `lib/` entries, `skills/` links, and
`agents-fragments/`. Add `--runtime <existing-skill-root>` for affected runtime
roots, or `--sources` for a library-wide comparison of `lib/` bytes, executable
bits, and symlink targets against pinned Git trees (review reported diffs
against `notes`).

Run maintenance unit tests (`lib/skill-manager/scripts/test_*.py` and
`lib/skill-creator/scripts/test_*.py`) when audit, validation, or packaging
behavior changes. Keep one-off checks temporary.
