---
name: screenshots
description: Locate macOS screenshots saved to ~/screenshots/ and route them into downstream workflows — most commonly attaching to GitHub PR/issue/comment bodies via the gh image extension, but also useful for previewing, organizing, copying to clipboard, or feeding into other tools. Use when the user mentions "screenshots", "today's screenshots", "find a screenshot", "attach screenshots", "upload screenshot", "images on machine", or wants to locate, preview, or share a local screenshot.
license: MIT
compatibility: opencode
metadata:
  scope: global
  tools: bash
---

# Screenshots

Local macOS screenshots are saved to `~/screenshots/`. This skill covers locating them and using them in downstream workflows. The most detailed workflow is uploading to GitHub via `gh image`, but the skill also applies to previewing, sharing via other channels, and basic housekeeping.

## One-time setup (per machine)

Verify before assuming:

```bash
# 1. macOS screenshot location is ~/screenshots/ (not Desktop)
defaults read com.apple.screencapture location
# expected: /Users/<you>/screenshots

# If empty or pointing at Desktop, set it once:
mkdir -p ~/screenshots
defaults write com.apple.screencapture location ~/screenshots
killall SystemUIServer

# 2. gh CLI authenticated (for the GitHub workflow below)
gh auth status

# 3. gh-image extension installed (one-time)
gh extension list | grep -q 'drogers0/gh-image' || gh extension install drogers0/gh-image
```

Per-day subdirs are **not** used by default — the filename already embeds the date (`Screenshot 2026-05-21 at 10.38.18.png`), so a flat dir keeps the workflow simple. If sorting ever becomes painful, layer on a Folder Action, launchd watcher, or Hazel rule.

## Finding screenshots

```bash
# Listing (human-readable, today's only)
ls -lt ~/screenshots/ | grep "$(date +%Y-%m-%d)"

# Full paths (for piping into other commands)
ls ~/screenshots/Screenshot\ "$(date +%Y-%m-%d)"*.png

# All recent (last 24h, any filename)
find ~/screenshots/ -type f -mtime -1
```

Filename format is `Screenshot YYYY-MM-DD at HH.MM.SS.png`. Time separator may be `.` (Norwegian locale) or `:` (English locale) — prefer globs that don't depend on it.

## Workflow: attach to a GitHub PR / issue / comment

### The command

```bash
# Run from inside the target repo so origin is auto-detected:
gh image ~/screenshots/Screenshot\ 2026-05-21\ at\ 10.38.18.png \
         ~/screenshots/Screenshot\ 2026-05-21\ at\ 12.23.18.png

# Or pass --repo explicitly:
gh image --repo owner/repo ~/screenshots/...
```

Output is one `![filename](https://github.com/user-attachments/assets/...)` line per upload. Capture stdout and paste into the target body.

### End-to-end: attaching today's screenshots to a PR

1. **Find** the candidate files, newest first:
   ```bash
   ls -t ~/screenshots/Screenshot\ "$(date +%Y-%m-%d)"*.png
   ```
2. **Read every candidate before uploading.** Use the Read tool on each file (start with the most recent — those are usually the "for this PR" captures, while older ones in the same day are often unrelated work). For each one, decide:
   - **Keep** if it shows the change the PR is about (before/after states, mobile/desktop views, the bug being fixed, the feature in action)
   - **Drop** if it's a throwaway: code diffs already visible in Files Changed, scratch debug shots, accidental captures, screenshots from other unrelated work earlier in the day
   - **Label** the keepers with one short phrase (e.g. "Empty state on mobile", "Toast after save") — you'll use these as sub-headings in the PR body

   Never upload blind. An unfiltered batch dump pollutes the PR and forces reviewers to guess what each image is showing.
3. **Upload** only the keepers:
   ```bash
   gh image ~/screenshots/Screenshot\ 2026-05-21\ at\ 12.23.18.png \
            ~/screenshots/Screenshot\ 2026-05-21\ at\ 12.23.44.png
   ```
4. **Fetch** the current PR body, **append** a `## Screenshots` section pairing each label with its returned markdown URL, then write back:
   ```bash
   gh pr view <num> --json body -q .body > /tmp/pr-body.md
   cat >> /tmp/pr-body.md <<'EOF'

   ## Screenshots

   ### <label for image 1>
   ![…](https://github.com/user-attachments/assets/…)

   ### <label for image 2>
   ![…](https://github.com/user-attachments/assets/…)
   EOF
   gh pr edit <num> --body-file /tmp/pr-body.md
   ```

Same flow works for issues (`gh issue view`, `gh issue edit`) and for posting as a comment (`gh pr comment <num> --body-file ...`).

## Other workflows

- **Preview / label** — feed paths to the Read tool to identify content before using them anywhere.
- **Copy path to clipboard** — `echo -n /path/to/file.png | pbcopy` to paste into Slack, Teams, email, or design tools.
- **Cleanup old files** — `find ~/screenshots/ -mtime +30 -name '*.png' -delete` removes screenshots older than 30 days.
- **Pre-process before sharing** — `sips`, ImageMagick, or `pngquant` for cropping, resizing, or compressing.
- **Reference in local markdown** — drop a relative or absolute path into Obsidian / scratch notes.

## Tips

- **Group related shots** with markdown sub-headings (`### Mobile`, `### Desktop`) instead of dumping a raw list.
- **Skip code-diff screenshots** when the diff is already visible in the PR's Files Changed tab — they add noise.
- **Reuse upload URLs.** `gh image` returns CDN-backed URLs that work in any GitHub markdown surface (PRs, issues, comments, gists, Discussions).
- **Filenames with spaces** must be backslash-escaped or quoted — the macOS default format includes spaces.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `gh: image: unknown command` | `gh extension install drogers0/gh-image` |
| `401 / authentication required` | `gh auth login` (the token used by `gh image` is the gh session token, not a PAT) |
| Wrong repo detected | Add `--repo owner/repo` or `cd` into the repo first |
| Filename glob misses today's files | Confirm `defaults read com.apple.screencapture location` matches `~/screenshots/` |
