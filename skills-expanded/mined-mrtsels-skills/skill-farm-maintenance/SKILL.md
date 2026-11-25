---
name: skill-farm-maintenance
description: "Use when organizing skill library: post-flip farm upkeep."
---

# Skill Farm Maintenance (post-2026-08 flip)

Trigger: user asks to 整理/组织/归位 the skill library, or anything touching the layout of `~/.agents/skills`, `~/.hermes/skills`, `~/.claude/skills`, `~/.Codex/skills`.

## Architecture (verify with `git log` before trusting any doc)

- `~/.agents/skills/` — SSOT 真身. Real skill content with Hermes category nesting (`writing/humanizer`, `software-development/<name>`). Git repo (mrtsels/agents-skills). **Since 2026-08-06: tracks ALL skill content (1200+ files)** — the old ignore-all+allowlist mode is retired. `.gitignore` now carries explicit exclusions only (system junk, nested `.git/`, sensitive dirs/files). Stand-in symlinks tracked automatically (mode 120000). See `references/pii-credential-gate.md` for the mandatory pre-commit privacy sweep.
- `~/.hermes/skills/` — **SINCE 2026-08-06 EVENING: NO symlink farm anymore.** Hermes loads the SSOT directly via `skills.external_dirs: [/Users/minimx/.agents/skills]` in `~/.hermes/config.yaml`. The dir now holds only Hermes state (`.archive/`, `.hub/`, `.curator_*`, `.usage.json`, `.bundled_manifest`). No per-skill symlinks to maintain — moving/renaming skills in SSOT is instantly reflected (no farm rebuild).
- `~/.claude/skills/` — symlink farm → `.agents` (Claude Code has no external_dirs; flat names → `../../.agents/skills/<cat>/<name>`; categorized skills link to their category path, e.g. `../../.agents/skills/productivity/docx`). **Must be rebuilt manually after any move.**
- Pre-flip layout (real content in `.hermes`, stand-ins in `.agents`) is OBSOLETE. Older skills may still describe it — cross-check the filesystem and `git log` before acting on them.
- `hermes config set skills.external_dirs '["..."]'` writes a JSON STRING, not a YAML list — the parser rejects it (path with quotes fails `is_dir()`). Edit config.yaml directly to the YAML list form:
  ```yaml
  skills:
    external_dirs:
      - /Users/minimx/.agents/skills
  ```

## skill_manage (agent tool) limitations — verified 2026-08-06

`skill_manage` resolves skills via `_find_skill()` → `Path.rglob("SKILL.md")`, which does NOT follow symlinked dirs (Python 3.13). Consequences in the farm architecture:

- **patch/edit/delete/write_file/remove_file on ANY farm skill** (shell-internal or top-level flat symlink) → error `Skill '<name>' not found in active profile`. `skill_view` still works (uses `os.walk(followlinks=True)`).
- **create → writes a REAL dir** to `~/.hermes/skills/<cat>/<name>` (drift). Must be moved to SSOT + replaced with a relative symlink.

Workaround:
- **Revise existing skills: use file tools** (`read_file`/`patch`/`write_file`) on the real path `~/.agents/skills/<cat>/<name>/…` (writing through the farm symlink also lands in SSOT). Never rely on skill_manage for edits.
- **New skills:** `skill_manage(create)` then immediately move to SSOT + symlink (Maintenance workflow steps 2–3), or write the file directly into `~/.agents/skills/<cat>/` and symlink.
- Upstream fix would be `rglob("SKILL.md", recurse_symlinks=True)` (Py3.13) or `os.walk(followlinks=True)` in `_find_skill`; don't local-patch `~/.hermes/hermes-agent` (wiped/stashed on `hermes update`).

## Maintenance workflow

1. Backup first: `cp -R` affected dirs → `/tmp/skill-reorg-backup-<ts>/`. Ops are destructive (rm -rf real dirs); user wants recoverable.
2. Audit the farms: `python3 scripts/audit_symlink_farms.py` — broken symlinks, real (non-symlink) skill dirs left in farms, duplicate skill names across Hermes load paths.
3. Real dirs in a farm = drift → `diff -rq` against the SSOT copy; identical → replace with a relative symlink.
4. Version drift between farm copy and SSOT: diff both directions. SSOT usually wins (Hermes-adapted frontmatter: short description, `metadata: hermes`, category). BUT watch for botched blanket sed — a Claude→Codex replace corrupted SSOT descriptions ("Codex, Codex" typo in hermes-for-agents) while the `.claude` copy kept the correct original. Fix the SSOT typo in place; never adopt the stale farm copy wholesale.
5. Dedupe reorg `cp -R` copies: latex-debugging existed in BOTH `software-development/` and `latex/`. Keep the git-tracked bundle copy, remove the other + its `.hermes` symlink, verify `hermes skills list | grep -c <name>` == 1.
6. Archive, don't delete: legacy Codex-only skills → `~/.Codex/skills/.archive/` (never touch `.system/` or app-owned symlinks); empty category stubs (only DESCRIPTION.md) → `~/.hermes/skills/.archive/legacy-categories/`.
7. Verify: `hermes skills list` (count + error scan), every farm symlink resolves to a SKILL.md. NOTE: `os.walk` does NOT follow symlinked dirs — to confirm a bundle member (e.g. `latex/latex-debugging`) check the SSOT path directly, not by walking `~/.hermes/skills`.
8. Git: regenerate `skills-manifest.md` (top-level entries + `cat/ (N skills)` lines + symlinks), `git add skills-manifest.md` only (no `git add .`/`-A`), commit, push.
9. **PII/credential gate before any commit** (repo tracks all content now): scan `git ls-files` for user PII (names/emails/passwords/internal IPs), triage false positives, sanitize tracked files in place or add explicit `.gitignore` exclusions — see `references/pii-credential-gate.md`.

## Categorizing flat skills into topic categories (validated 2026-08-06, 211 skills → 20 categories)

When the top level of `.agents/skills` is a flat pile of 200+ standalone skills, migrate them into Hermes category dirs:

1. **Cluster by description, not by name**: read each `SKILL.md` `description:` frontmatter and group by theme. The categories that emerged: finance (new), academic, research, note-taking, data-science, software-development, creative, productivity, autonomous-ai-agents, apple, email, github, resume, infrastructure, devops, workflow, writing.
2. **Watch for bundle duplication BEFORE moving**: ~17 bundle dirs (ai-ml-skills, citation-skills, search-skills, …) contain an index `SKILL.md` AND sub-skill dirs that ALSO exist flat at top level (91 identical duplicates found — `filecmp` verified 32/32 identical). The bundles are aggregation indexes; the flat copies are what Claude Code discovers. Move the FLAT copies into categories; leave the bundle dirs intact (they keep working as indexes).
3. **Move with `shutil.move` per entry, then rebuild every farm symlink** that pointed at the old flat path: `.claude/skills` (flat names → `../../.agents/skills/<cat>/<name>`) and `.hermes/skills` top-level links (→ `../../.agents/skills/<cat>/<name>`). Both farms break en masse otherwise. Depth stays `../../` for flat→category (`.claude` root → `.agents` root), only category-nested links use `../../../`.
4. **Git handles the move as renames**: `git add` the new top-level entries, then `git add -u` stages deletions; `git diff --cached --name-status -M` shows ~100% renames, 0 D/A churn. One commit covers the whole migration.
5. **Update `.gitignore` paths for any sensitive dir that moved** (e.g. `agently-mail/` → `email/agently-mail/`, `kylin-vm-deployment/` → `infrastructure/kylin-vm-deployment/`). Forgetting this silently un-ignores the sensitive dir at its new path.
6. Keep top-level bundles (`latex/`) and their stand-in symlinks in place; `best-practices/` (docs wiki) was deleted 2026-08-06.
7. Verify: `hermes skills list` count DROPS by the number of sensitive skills that stay ignored (181→171 here — expected, they're still local, just untracked); all farm symlinks resolve.

## Merging two overlapping skills (user preference: blend BY TOPIC)

Trigger: user says two skills "应该合并（包括原始的），统一改".

1. **Backup both originals first**: `cp -R <cat>/<a> <cat>/<b> → /tmp/skill-merge-backup-<ts>/`.
2. **Merge into the primary skill** — keep the one that is auto_inject/mandatory/has the trigger; fold the other's content in as sections.
3. **USER PREFERENCE (explicit correction): blend merged content BY TOPIC — do NOT split into "第一部分/第二部分" labeled sections.** Write unified topic sections (Chinese and English rules side by side inside each topic); only the verbatim absorbed original goes to `references/<name>-full.md`.
4. Copy any LICENSE into `references/` and keep attribution (original author, upstream repo, version).
5. Delete the absorbed dir; remove its farm symlinks; regenerate manifest + `.gitignore` exclusions if any.
6. `git add <explicit paths> && git commit && git push`; tell the user the backup location.
7. **Overlap warning:** check for a THIRD overlapping skill (e.g. `ai-writing-humanizer` overlapping humanizer) and flag it — don't merge unprompted.

**Merging narrow siblings INTO an existing umbrella** (github pattern): copy each absorbed SKILL.md → umbrella `references/<name>.md`, add References-table rows, append a compact summary section to the umbrella SKILL.md, then delete the standalone skills (both SSOT and farm symlinks). Example: `install-skill-from-github` + `install-binary-from-github-releases` → `github/` references + a "## N. Install from GitHub" section.

## Pitfalls

- A loaded skill describing the library architecture may lag a recent flip — confirm current layout from `git log` + `ls -la` before acting on it.
- Moving a symlink into a subdir breaks its relative target — recompute depth (`../../` → `../../../`).
- `best-practices/` was a docs wiki (no top-level SKILL.md), NOT a skill — **deleted 2026-08-06** (third-party wiki, its 9 nested example SKILL.md were polluting `hermes skills list`). Don't recreate; flag any future clone instead.
- Not every dir is a skill: bundles (latex, best-practices) and category shells have no top SKILL.md; count sub-skills instead.
- **`for e in *; do git add -- "$e"; done` skips dotfiles** — `.gitignore` changes are NOT staged by the top-level-entry loop. `git add .gitignore` explicitly or the "disable global ignore / add sensitive exclusions" commit silently never lands (happened 2026-08-06: gitignore rewrite was committed separately after the content commit).
- **Sensitive `.gitignore` paths go stale when dirs move categories** — a dir-level ignore (`agently-mail/`) stops matching after `email/agently-mail/`. After any reorg, grep the tracked file list for the sensitive dir names, not the old paths.
- Nested `.git` dirs in cloned bundles (best-practices, consulting-problem-solving) are treated as gitlinks — add `<dir>/.git/` to `.gitignore` so their content tracks instead.
- Skill counts in `hermes skills list` legitimately DROP when sensitive skills stay gitignored — expected, not a regression.
