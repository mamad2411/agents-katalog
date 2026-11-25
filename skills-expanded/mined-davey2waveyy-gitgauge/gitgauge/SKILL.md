---
name: gitgauge
description: Use when a full GitHub repository URL (github.com/owner/repo) appears in conversation, when the user asks to check, review, or analyze a GitHub repo, or when the user runs /gitgauge. Does not trigger on npm packages, file paths, org pages, or issue/PR links.
allowed-tools:
  - Bash
---

# GitGauge

Score GitHub repos for authenticity. Mirrors the GitGauge Chrome extension algorithm exactly.

The GitGauge output line is the announcement — no separate announce needed. Run the scorer first, then engage with the repo.

## When to run

| Trigger | Output mode |
|---------|-------------|
| GitHub URL appears passively in conversation | Compact one-liner, then continue |
| User asks to review / analyze a repo | Compact score + brief breakdown, then review |
| User runs `/gitgauge owner/repo` | Full report: sub-scores, flags, metadata |

**Do not run on:**
- GitHub profile URLs, org pages, gist links, issue links, PR links, or commit links
- npm package references (`@scope/package`), file paths, or bare `owner/repo` with no GitHub URL context
- Repos already scored in the current conversation

## Running the scorer

```bash
python ~/.claude/skills/gitgauge/scripts/score.py owner/repo
# macOS / Linux: use python3 instead of python
```

With a token (removes rate limit):
```bash
python ~/.claude/skills/gitgauge/scripts/score.py owner/repo --token ghp_yourtoken
```

For the full report mode (parse JSON to build structured output):
```bash
python ~/.claude/skills/gitgauge/scripts/score.py owner/repo --json
```

Pass full GitHub URLs too — the script strips the `github.com/` prefix automatically.

## Output formats

### Compact (passive trigger)
```
GitGauge: 🟢 4.1/5.0 — Likely Authentic
```

### Standard (review / analyze trigger)
```
GitGauge: 🟢 4.1/5.0 — Likely Authentic
⭐ 2,400 stars  🍴 310 forks  👁 47 watchers  🐛 18 issues
Fork ratio: 12.9%  |  Watcher ratio: 1.96%  |  Issue ratio: 0.75%
```

### Full report (/gitgauge command)
Use `--json` output. Show score, label, all ratios, sub-scores, flags, and metadata (language, description, topics).

## Score labels

| Score | Label | Emoji |
|-------|-------|-------|
| 1.0–1.4 | Likely Fake | 🔴 |
| 1.5–2.4 | Suspicious | 🟠 |
| 2.5–3.4 | Mixed Signals | 🟡 |
| 3.5–4.4 | Likely Authentic | 🟢 |
| 4.5–5.0 | Highly Authentic | ✅ |

## Warning threshold

If score **< 2.5**, show a soft warning *before* engaging with the repo:

> ⚠️ GitGauge flagged `owner/repo` as **Suspicious (1.8/5.0)** — low engagement relative to star count may indicate star farming or an inactive project. Proceeding anyway.

Never block the user — the score is additive context, not a gate.

## Error handling

| Error | What to show |
|-------|-------------|
| 404 / not found | `GitGauge: ❌ Repo not found or private — skipping score` |
| Rate limited | `GitGauge: ⚠️ Rate limited — pass --token to continue (see Token Setup below)` |
| Unscoreable (< 50 stars) | `GitGauge: ⚪ Unscoreable — fewer than 50 stars` |
| Bad token | `GitGauge: ❌ GitHub token invalid or expired` |

In all error cases: continue engaging with the repo normally.

## Edge case flags

The script returns these flags in output — always surface them:

| Flag | What to tell the user |
|------|-----------------------|
| `is_fork` | "This is a fork — metrics reflect fork activity, not the original repo" |
| `archived` | "Repo is archived — activity metrics are frozen" |
| `low_stars` | "Under 100 stars — signal may not be reliable" |
| `new_repo` | "Under 30 days old — insufficient history for a reliable score" |

**Zero issues + many stars**: Script automatically scores this as 1.5 (Suspicious). Large repos with zero open issues usually have issues disabled, not zero bugs.

## Token setup (optional)

Without a token: 60 GitHub API requests/hour per IP. Sufficient for most sessions.

1. Create a token at https://github.com/settings/tokens — no scopes needed for public repos
2. Pass inline: `--token ghp_yourtoken`
3. Or set `GITHUB_TOKEN` in your environment and update the Bash call to read `$GITHUB_TOKEN`

## Scoring algorithm

Full implementation is in `scripts/score.py` — a direct port of the GitGauge Chrome extension.

- **Minimum threshold**: repos with < 50 stars return unscoreable
- **Fork score** (weight: 35% with watchers, 55% without): forks ÷ stars
- **Watcher score** (weight: 35%, omitted if watchers = 0): watchers ÷ stars
- **Issue score** (weight: 30% with watchers, 45% without): issues ÷ stars
- Final score clamped to [1.0, 5.0], rounded to one decimal

Breakpoints and interpolation logic are defined as constants at the top of `score.py`.

## Quick reference

| Situation | What to do |
|-----------|------------|
| GitHub URL in message | Run scorer → compact one-liner → continue |
| "Review this repo" | Run scorer → standard output → review |
| `/gitgauge owner/repo` | Run scorer with `--json` → full report |
| Score < 2.5 | Show warning before engaging, then proceed |
| Any API error | Show error line, still engage with repo |
| Flag in output | Always mention it to the user |
| Already scored this session | Skip — don't score twice |
