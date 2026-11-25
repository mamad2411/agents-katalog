---
name: git-pr-generator
description: Create a GitHub pull request using gh CLI with a structured PR template. Use this skill whenever the user wants to create or generate a PR — in English or Korean. Trigger on phrases like "create pr", "make pr", "open pr", "make a pull request", "pr please", "pr 만들어줘", "pr 생성해줘", "풀리퀘 만들어줘", "PR 생성해줘". Always use this skill when the user says anything about creating, making, or generating a PR or pull request.
---

Create a GitHub pull request for the current branch using `gh pr create`.

## Steps

0. **Check prerequisites** — run as a single Bash call:
   ```bash
   git rev-parse --git-dir 2>/dev/null && gh auth status 2>/dev/null
   ```
   If `git rev-parse` fails, tell the user this must be run inside a git repository and stop.
   If `gh auth status` fails, tell the user to run `gh auth login` first and stop.

1. **Gather context** — run as a single Bash call so `$BASE` persists across commands:
   ```bash
   BASE=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name' 2>/dev/null || echo "main") && \
   BRANCH=$(git rev-parse --abbrev-ref HEAD) && \
   echo "branch=$BRANCH base=$BASE" && \
   git log "origin/$BASE..HEAD" --oneline && \
   git diff "origin/$BASE..HEAD" --stat
   ```
   If the branch has no commits ahead of `origin/$BASE`, tell the user and stop.

2. **Craft the PR title** — derive a concise title (under 70 characters) from the branch name and commit messages. Strip the branch type prefix (e.g., `feature/`, `fix/`) to get a human-readable phrase.

3. **Fill in the PR template** — use the template below, replacing the placeholders based on the actual diff and commits.

4. **Create the PR** using exactly this command shape:
   ```bash
   gh pr create \
     --title "<title>" \
     --body "$(cat <<'EOF'
   <filled-template>
   EOF
   )"
   ```
   Do not add `--draft`, `--assignee`, `--label`, or other flags unless the user explicitly asks.

5. **Report the result** — output the PR URL returned by `gh pr create`.

---

## PR Template

Always use this exact structure. Fill in each section from the diff and commit log:

```
## Summary


## Changes
- 


## Test Plan
- [ ] 
```

If there is something meaningful to note (breaking changes, follow-ups, known limitations), append a `## Notes` section after `## Test Plan`. Otherwise omit it entirely — do not include an empty `## Notes` heading.

**Language rule:**
- Default to English for all content.
- If the user explicitly requests a specific language (e.g., "한국어로 써줘", "write in Korean"), write the content of each section in that language — but always keep the section headings (`## Summary`, `## Changes`, etc.) in English.

**Filling guidance:**
- **Summary**: 2-3 sentences — what changed and why.
- **Changes**: One bullet per logical change. Reference file names where helpful. Keep each bullet under one line.
- **Test Plan**: At least one checkbox. Derive from the type of change — a bug fix gets "Reproduce the bug, verify it's gone"; a new feature gets a smoke-test step.
- **Notes**: Only include when there's something genuinely worth calling out (breaking change, known issue, follow-up ticket, deploy steps).

---

## Rules

- Always use `gh pr create` — no alternatives.
- Pass the body via a heredoc (`<<'EOF' ... EOF`), never via a temp file.
- Title must be plain text, no emoji, under 70 characters.
- Base branch is `main` unless detected otherwise.
- Do not explain the gh command output. Just show the PR URL.
