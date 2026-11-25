---
name: dotfiles-backup
description: Back up a config/dotfiles directory (e.g. ~/.pi, ~/.config/foo) to a private GitHub repo with a proper secret-aware .gitignore and a restore recipe. Use when the user wants to version their agent/tool/editor config to replicate across machines.
metadata:
  pi:
    category: workflows
---

# Dotfiles / Config Backup to GitHub

## When to Use

User wants to mirror a personal config directory (`~/.pi`, `~/.claude`, `~/.config/<tool>`, shell dotfiles, etc.) to a private GitHub repo so they can clone it on another device.

## Procedure

1. **Survey the directory.** List every file, identify which are:
   - **Portable** (settings, extensions, skills, scripts you wrote, notes).
   - **Secret** (auth tokens, API keys, OAuth refresh tokens, `.env` files).
   - **Machine-local runtime state** (session history, caches, usage counters, PID/lock files, cwd-hash → id mappings).
   Read any `auth.json`/`config.json`/`.env`/`state.json` to know which bucket they're in. Bias to "exclude" when uncertain.

2. **Check repo doesn't exist yet** — `gh repo view OWNER/NAME 2>&1 | head -3`. If "Could not resolve to a Repository", you're clear.

3. **Write `.gitignore` BEFORE `git init`** at the repo root. Critical rules:
   - **No inline comments.** `# comment` must be at column 0. `pattern  # explanation` is parsed as a literal filename with trailing junk and matches nothing.
   - Use one comment line above each rule (or group) for readability.
   - Prefer `**/.env` patterns for nested dotenv files.
   - Trailing-slash patterns (`sessions/`) match directories.

4. **Write `README.md`** with: what's included, what's excluded and why, restore steps, update workflow, secret-rotation warning.

5. **`git init -b main`**, then **`git add -A`**.

6. **Run a guard before committing.** Pipe `git diff --cached --name-only` through `grep -E` for known-sensitive patterns and `exit 1` on any hit. Cheap insurance.

7. **`git commit`**, then `gh repo create OWNER/NAME --private --description "..."`, then `git remote add origin git@github.com:OWNER/NAME.git && git push -u origin main`.

8. **Verify on the remote.** `gh api repos/OWNER/NAME/contents/<sensitive-path> --jq .sha` should 404 for every secret/state file. Don't trust your local view — confirm against GitHub.

## Pitfalls

- **`.gitignore` inline comments silently break patterns.** A line like `agent/auth.json  # tokens` is read as one literal filename. Symptom: ignored files still get staged. Fix: put every `#` at column 0.
- **`git check-ignore` skips tracked files by default.** If you ran `git add -A` once with a broken `.gitignore`, files are now in the index. `check-ignore` will report "not ignored" for them, sending you on a goose chase debugging `.gitignore` syntax that's actually fine. Use `git check-ignore --no-index <path>` to test the patterns themselves, OR fully reset the index with `git rm -rf --cached .` and re-add.
- **`git rm --cached -r . 2>/dev/null || true` can silently no-op.** If the index is empty or the command errors, `|| true` hides it. Drop the `|| true` and check exit code, or run it before `set -e`.
- **`auth.json` may be regenerated on first launch** of the tool on the new machine (e.g. OAuth flows). Make the README say "run the tool, complete auth flow" rather than "copy auth.json across" — it's often a one-shot file.
- **Repo visibility = private** for anything containing personal preference notes (`USER.md`, working-style memories). Even without secrets, those are personal.
- **macOS `xattr com.apple.provenance`** on files written through certain tools is harmless to git. Don't get distracted by `ls -la@`.
- **Don't `git push --force` on dotfiles.** A clean force-push to a freshly-created empty repo is fine, but never on one with history — local config drift across machines is normal and merge-friendly.

## Resetting History (when secrets leaked into an early commit)

If you committed something you shouldn't have and want a clean slate:

```bash
git checkout --orphan fresh        # new branch with no parents
git add -A                          # stage current state
git commit -m "Initial commit"      # parentless commit
git branch -D main                  # drop old main
git branch -m main                  # rename fresh → main
git push --force origin main        # replaces remote history; old commits become unreachable
```

This works without the `delete_repo` gh scope. Prefer it over `gh repo delete && gh repo create` when you only have the `repo` scope. Flip visibility separately with `gh repo edit --visibility public --accept-visibility-change-consequences` (only needs `repo`).

**Caveat**: for actual secrets (API keys, tokens), force-pushing is NOT enough — assume the secret is compromised and rotate it. Force-push removes the public link, but cached clones, forks, and GitHub's internal logs may still contain it.

## Verification

```bash
# Locally: nothing sensitive staged
git diff --cached --name-only | grep -E '<sensitive-pattern>' && echo BAD || echo OK

# Remotely: each sensitive path should 404
for f in path/to/auth.json .env state.json; do
  gh api repos/OWNER/NAME/contents/$f --jq '.sha // "MISSING"'
done
# Expect: "Not Found (HTTP 404)" for each.

# .gitignore patterns themselves work
git check-ignore --no-index -v path/to/auth.json   # should print matching line
```

## Restore Recipe Template (for the README.md)

```bash
# 1. Install the tool (Homebrew/npm/etc.)
# 2. Clone the repo INTO the config location:
git clone git@github.com:OWNER/NAME.git ~/.<tool>
# 3. Run the tool once to regenerate runtime state and auth:
<tool>   # complete any OAuth flow, then quit
# 4. Restore secrets:
~/.tool/bin/<set-secret-helper> <api-key>
# 5. Verify:
<tool> # boots with all config intact
```
