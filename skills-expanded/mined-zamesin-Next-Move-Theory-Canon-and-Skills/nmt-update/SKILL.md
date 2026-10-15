---
name: nmt-update
description: >-
  Update an installed Next Move Theory setup to the latest published canon +
  skills by re-running the official one-command installer straight from the
  public GitHub repo (zamesin/Next-Move-Theory-Canon-and-Skills, branch main).
  It refreshes the canon, the nmt-* skills (both Codex and Claude), the marked
  rules block in AGENTS.md / CLAUDE.md, and the README in place. Idempotent and
  safe: it never touches your own files and never deletes unrelated skills. Use
  when the user says "update NMT", "update the skills", "get the latest canon",
  runs $nmt-update, or when another skill reports that a newer version is
  available. Defaults to English.
user-invocable: true
---

# nmt-update — update to the latest canon + skills

Re-runs the official Next Move Theory installer from the **project root**. The
installer clones the public repo
(`zamesin/Next-Move-Theory-Canon-and-Skills`, branch `main`) and refreshes,
**in place**:

- `Next-Move-Theory-Canon/` — the canon
- `.agents/skills/nmt-*` — Codex skills (invoke with `$nmt-…`)
- `.claude/skills/nmt-*` — Claude skills (invoke with `/nmt-…`)
- the `<!-- Next-Move-Theory-Rules:start … end -->` block in `AGENTS.md` and `CLAUDE.md`
- `NextMoveTheory-README.md`

It is **idempotent and safe** — it replaces the canon, skills, marked rules
block, and README in place, leaves your own files untouched (including anything
outside the markers), and does **not** delete unrelated skills already in
`.agents/skills` or `.claude/skills`. Everything it installs is downloaded from
the public GitHub repo.

> **Count this run — optional; policy in `NextMoveTheory-README.md`, section "Updates & telemetry".**
> Skip this entirely if `.nmt-config` (project root) contains a line `update-check: off`, or the environment variable `DO_NOT_TRACK` or `NMT_NO_UPDATE_CHECK` is set.
> Otherwise, as your **first action**, tell the user in one line: "Counting this update run — only this skill's name and the installed version are sent (details: NextMoveTheory-README.md; disable: add `update-check: off` to `.nmt-config`)."
> Then run `v="$(grep -m1 -E '^[0-9]' .nmt-version 2>/dev/null)"; curl -fsSL --max-time 2 "https://nextmovetheory.com/version?skill=nmt-update${v:+&v=$v}" >/dev/null 2>&1 || true` — on any error or timeout, skip and move on; never retry, never block. This ping only counts the run; the update itself always downloads from GitHub.

## Steps

1. **Locate the project root** — the folder that contains `Next-Move-Theory-Canon/`
   and/or `.agents/skills/`. That is where the canon + skills must be refreshed.
   If the current directory is not it, ask the user which directory to update.
   If interactive input is unavailable, use the current directory and say so.
2. **Read the installed and the latest version.** The installed version sits in
   `.nmt-version`; the latest is the top entry of the changelog in the public
   GitHub repo:
   ```bash
   installed="$(grep -m1 -E '^[0-9]' .nmt-version 2>/dev/null)"
   latest="$(curl -fsSL --max-time 3 https://raw.githubusercontent.com/zamesin/Next-Move-Theory-Canon-and-Skills/main/CHANGELOG.md 2>/dev/null \
     | grep -m1 -E '^##[[:space:]]+[0-9]' | sed -E 's/^##[[:space:]]+([^[:space:]]+).*/\1/')"
   echo "installed=${installed:-unknown} latest=${latest:-unknown}"
   ```
   Report the `<installed> → <latest>` gap in one line. **If the fetch fails or
   times out, say so in one line and continue to step 3 anyway** — never block
   the update on the version check. If the two versions already match, say so
   and still run the install (it is idempotent, and it repairs a partial one).
3. **Run the installer** from that directory:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/zamesin/Next-Move-Theory-Canon-and-Skills/main/install.sh | bash
   ```
   (Windows / PowerShell: `irm https://raw.githubusercontent.com/zamesin/Next-Move-Theory-Canon-and-Skills/main/install.ps1 | iex`.)
4. **Report what changed.** Show the installer's final summary. If the project is
   a git repo, run `git status --short` and list which canon files / skill folders
   were added or modified so the user sees exactly what the update pulled in. If
   the changelog was fetched in step 2, add a one-line summary per version newer
   than the one that was installed.
5. **Confirm done.** Tell the user the update is complete and that any
   new/updated skills are available immediately (e.g. `$nmt-diagnose`,
   `$nmt-chat`). No restart is needed.

## Notes

- **Best-effort.** The installer needs `curl` and `git`. If either is missing,
  tell the user to install it, or to install by hand from
  https://github.com/zamesin/Next-Move-Theory-Canon-and-Skills (clone the repo
  and run `bash install.sh --target <your-project-root>`).
- **Non-destructive.** Your own `AGENTS.md` / `CLAUDE.md` content outside the
  `<!-- Next-Move-Theory-Rules:start … end -->` markers is preserved — the
  installer only ever rewrites what sits *between* the markers. Unrelated skills
  are left alone.
- **Renamed skill.** This skill used to be called `nmt-upgrade`. The installer
  removes the old `nmt-upgrade` folder from `.agents/skills` and `.claude/skills`
  and installs `nmt-update` in its place, so you won't end up with both.
- **Source of truth.** What gets installed is always the current `main` of the
  public GitHub repo — the installer clones it fresh on every run, so there is no
  stale cache for the canon or skills.
