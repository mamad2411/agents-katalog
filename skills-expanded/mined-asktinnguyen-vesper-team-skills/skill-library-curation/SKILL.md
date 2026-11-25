---
name: skill-library-curation
description: Curate an agent skill library by finding duplicates, splitting broad skills, improving metadata, syncing installs across apps, and backing up changes.
argument-hint: "Skill library path, app target, or curation goal"
---

# Skill Library Curation

Use when maintaining a collection of agent skills across Hermes, Codex, Vesper, or backup repositories. The goal is a clean, discoverable, synchronized skill library: skills should be easy to trigger, non-overlapping, current, and installed in the right app locations.

## Curation principles

- **One trigger, one skill.** Split skills when they serve different user intents or produce different artifacts.
- **Specific metadata wins.** `name` and `description` are routing surfaces; make descriptions concrete enough for an agent to know when to load the skill.
- **Prefer consolidation over duplication.** Merge near-duplicates into the better maintained skill and keep forwarding notes only when needed.
- **Keep source and install separate.** Runtime app directories are for use; backup repos are for versioned recovery and review.
- **Never bulk-delete blindly.** Archive or mark candidates first unless the user explicitly authorizes removal.

## Workflow

1. **Inventory targets.** Identify relevant skill roots, commonly:
   - Hermes: `~/.hermes/skills/`
   - Codex App: `~/.codex/skills/`
   - Vesper App user skills: `~/.vesper/skills/`
   - Vesper team skills: `~/.vesper/team-skills/`
   - Backup repo: `~/vesper-team-skills/` or the user-specified repo.
2. **Compare by intent.** Group skills by trigger/outcome, not just name. Look for duplicate names, similar descriptions, and overlapping procedures.
3. **Decide action per group.** Choose one:
   - Keep as-is.
   - Improve metadata or instructions.
   - Split into smaller skills.
   - Merge into an umbrella skill.
   - Archive stale/unsafe/unmaintained material.
4. **Apply small, reviewable changes.** Prefer targeted edits or creating clearly named new skill directories. Avoid mixing unrelated cleanups in one commit.
5. **Sync installs.** Copy curated skills to the requested app roots. Preserve resource directories (`references/`, `scripts/`, `templates/`, `assets/`). For cross-app Hermes/Codex/Vesper syncs, consult `references/cross-app-skill-sync.md` for known runtime roots, validation checks, and backup-repo staging discipline. When the task is to pull a source repo and propose which newly available skills to install, use `references/latest-upstream-skill-proposal.md` for the comparison and recommendation pattern.
6. **Validate.** For every changed skill:
   - `SKILL.md` exists.
   - YAML frontmatter includes `name` and `description`.
   - Directory name matches or clearly namespaces the skill name.
   - Links/resources referenced by `SKILL.md` exist locally or are external URLs.
   - For weekly proactive curation, also consult `references/weekly-curation-frontmatter-and-sync.md` for frontmatter pitfalls, backup path staging, and safe sync boundaries.
7. **Backup.** Commit only the intended skill changes to the backup repo and push. Do not stage unrelated dirty work.

## Reporting checklist

Report:

- Skills created/updated/archived.
- Runtime install paths touched.
- Backup repo path, branch, and commit hash.
- Validation command or checks performed.
- Any intentionally skipped dirty files or unrelated repo state.

## Weekly proactive curation lessons

- When this skill itself is installed across apps, verify its support files too: `references/cross-app-skill-sync.md` and `references/weekly-curation-frontmatter-and-sync.md` should exist anywhere `skill-library-curation/SKILL.md` is installed, unless that runtime intentionally strips references.
- Quote YAML `description:` values that contain colons, inline paths, backticks, or long package/workflow labels; unquoted descriptions can parse in one app but fail during full-library validation.
- Treat obvious missing command-skill names as safe metadata fixes. For slash-command skill files such as `commands/skill.md`, add the command name (`name: skill`) rather than reporting it as a vague follow-up.
- If backup repo push is rejected because remote `main` advanced, fetch and rebase before pushing; keep the commit scoped to intentional skill-library changes and re-check `git status --short` after the rebase because new unrelated untracked paths may appear.
- After any fetch/rebase during backup push, re-run the changed-skill validation against both runtime installs and the backup repo. Remote changes can alter inventory counts or nearby files even when the local commit rebases cleanly.
- In backup repos, stage the actual tracked path reported by git. Some command skills are tracked as lowercase files such as `commands/skill.md`, even when runtime skill packages use directory-level `SKILL.md`.
- For scheduled/proactive curation runs, still make a small safe improvement when there is a clear signal; after syncing a skill across runtimes, verify the installed copies by comparing content hashes, not just file existence.
- For repeatable validation during weekly runs, use `references/weekly-curation-validation-pattern.md` for the frontmatter/link/hash checks and report fields.
- When a runtime `SKILL.md` has a broken relative link to a reference that actually lives in a sibling skill package, prefer a minimal relative-link fix such as `../other-skill/references/file.md` over copying the reference file. This preserves ownership and avoids duplicated stale references.
- Treat broad local-reference scans as triage signals, not authoritative findings: Markdown/code examples can look like links. Auto-fix only high-confidence broken references with an obvious existing target; report script/resource gaps and duplicate-name drift as follow-up candidates.
- Treat the user-specified backup repo path as authoritative. If it is missing, inspect a likely adjacent repository only to report the mismatch and its state; do not silently substitute it for commits or pushes unless the user explicitly authorizes the alternate path.
- If an alternate repository is explicitly authorized, record both the requested path and the authorized path, verify the repository identity and remote before staging, and keep the commit limited to the intended skill package.
- For scheduled curation, distinguish inventory evidence from action authority: a nearby repository that appears to be the intended backup is not authorization to use it. Report the mismatch and leave the requested backup path unchanged until explicitly approved.
- When fixing a broken local resource link in a skill synced across runtimes, update only the affected runtime copies, then verify both the target resource exists and the synced `SKILL.md` hashes match. Do not create a backup commit unless the scoped backup repo is present and clean enough to stage only the intended change.
- When broad link validation flags Markdown links inside explicit examples, treat them as high-confidence false positives only if the surrounding text is clearly illustrative (for example, "Examples:" or a pattern snippet) and the target file is not part of the skill package. Prefer converting the example link to inline code over creating empty placeholder files.
- In proactive weekly runs, if the active curation skill itself has newer support files in one runtime than the other app copies, syncing that one package plus hash-verifying every copied support file is a safe small improvement; still skip backup commits when the scoped backup repo path is missing.

## Pitfalls

- Do not confuse a research note with a skill. A skill must change future agent behavior.
- Do not let broad "assistant behavior" skills swallow concrete workflows.
- Do not overwrite local variants without checking whether app-specific additions exist.
- Do not commit unrelated untracked files from a backup repo during curation.
