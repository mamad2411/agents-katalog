---
name: pre-public-release-check
description: Use before pushing this repository to a public remote (GitHub, etc.) or sharing it as a portfolio link. Audits exactly what git would actually track, greps it for leaked secrets, and verifies .gitignore does what you think it does rather than assuming.
---

# Pre-public-release audit

Don't eyeball `.gitignore` and assume it's correct — verify what git would
*actually* stage, then scan exactly that file set. This is the procedure
used to clear this repo for a public push.

## 1. List exactly what would be committed

```bash
git add -n -A .
```

This respects `.gitignore` for real (no need to reimplement its glob rules
by hand) and shows every file that would be staged. Review the list itself
first — anything unexpected in there (a `.db` file, a `*.user` file, a
`node_modules/`) means `.gitignore` has a gap before you even get to
grepping content.

## 2. Grep that exact file set for secret patterns

Don't grep the whole working tree — grep only the files from step 1, or
you'll get false confidence from files that were never going to be
committed anyway. Check for, at minimum:

- Telegram bot tokens: `\d{8,10}:[A-Za-z0-9_-]{35}`
- Anthropic/OpenAI-style API keys: `sk-[A-Za-z0-9_-]{20,}`
- Any literal value copied from your actual `dotnet user-secrets list` /
  `.env` — pull the real secret values programmatically and grep for the
  literal string, don't rely on pattern-matching alone:

```bash
TOKEN=$(dotnet user-secrets list --project <proj> | grep BotToken | sed -E 's/.*= *//')
git add -n -A . | sed "s/^add '//;s/'\$//" | while read -r f; do
  [ -f "$f" ] && grep -qF "$TOKEN" "$f" && echo "LEAK: $f"
done
```

## 3. Verify .gitignore behaves as intended, per-path, with `git status`

`git check-ignore -v <path>` is misleading for negated patterns — it exits 0
(and prints the matching rule) whenever a path matches *any* rule,
including a `!` un-ignore rule. That looks like "found = ignored" but often
means the opposite. Use `git status --porcelain <path>` instead: `??` means
untracked-and-trackable (visible to git, not ignored); no output at all
means genuinely ignored. Check both directions explicitly — the files that
must stay out (`.env`, `*.mcp.json`, `.claude/settings.local.json`,
`*.db`) and the files that must get in (anything you deliberately carved an
exception for, like `CLAUDE.md`/`AGENTS.md` inside an otherwise-ignored
working directory).

## 4. Check config files for empty-string placeholders, not just missing keys

A shipped `appsettings.json` with `"BotToken": ""` is fine — it's a
placeholder. The same file with a real value pasted in during testing and
never reverted is not. Diff placeholder-shaped configs against what you
remember setting via user secrets / environment variables for local
testing; they should never match.

## 5. Look for leftover scaffold/template artifacts

Not a security issue, but worth a pass before a public link goes out:
grep for template leftovers (`weatherforecast`, `TODO`, default project
names) that reveal the repo was never fully adapted from its starting
template.
