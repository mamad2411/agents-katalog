# x-post-analyzer

Open-source tool for analyzing X/Twitter posts against the real Twitter algorithm.

## Quick Analysis Skill

When asked to analyze a tweet, run:

```bash
node src/cli.js [options] "tweet text here"
```

### Options
- `--image` / `--video` / `--gif` / `--poll` - specify media type
- `--compare "tweet1" "tweet2"` - compare multiple versions
- `-o report.md` - save report to file
- `-f tweets.txt` - read tweets from file
- `--low-follower` - flag account as low-follower (SpamEasi classifier risk)

### Environment
- `XAI_API_KEY` (optional) — set to enable Grok API integration for banger, safety, and spam classifiers. Falls back to heuristics silently when unset or on error.

### What to Check (Priority Order)

1. **Reply triggers** - Does the tweet ask a question or provoke discussion? Drives reply_score + dwell_time.
2. **Negative-feedback risk** - No excessive hashtags, caps, mentions, or links. Triggers not_interested/block/mute heads.
3. **Media** (2-2.5x boost) - Does it have an image/video? Images also drive photo_expand_score.
4. **Text quality** (75-200 chars optimal for 3-8s dwell window) - Right length, readable formatting.
5. **External links** (penalized) - Links should go in replies, not main tweet.
6. **Banger likelihood** - Score >= 0.4 threshold. Novelty, hook, no cliche density.

### Algorithm Weights Reference

#### Current (xai-org 2026)

Numeric weights are not published upstream. Legacy 2023 numbers shown where known (marked *).

| Action | Category | Weight |
|--------|----------|--------|
| reply | engagement | unpublished (legacy: 13.5*) |
| favorite | engagement | unpublished (legacy: 0.5*) |
| repost | engagement | unpublished (legacy: 1.0*) |
| click | engagement | unpublished (legacy: 11.0*) |
| profile_click | engagement | unpublished (legacy: 12.0*) |
| vqv | media | unpublished (legacy: 0.005*) |
| photo_expand | engagement | unpublished |
| share / share_via_dm / share_via_copy_link | engagement | unpublished |
| dwell | engagement | unpublished |
| quote / quoted_click | engagement | unpublished |
| follow_author | engagement | unpublished |
| not_interested | negative | unpublished (legacy: -74.0*) |
| block_author | negative | unpublished (legacy: -74.0*) |
| mute_author | negative | unpublished (legacy: -74.0*) |
| report | negative | unpublished (legacy: -369.0*) |

#### Legacy (2023)

From the-algorithm-ml README, April 2023. Historical reference only.

| Signal | Weight |
|--------|--------|
| replied | 13.5 |
| replied_and_engaged_by_author | 75.0 |
| good_profile_click | 12.0 |
| good_click | 11.0 |
| retweeted | 1.0 |
| favorited | 0.5 |
| video_playback_50 | 0.005 |
| negative_feedback_v2 | -74.0 |
| report | -369.0 |


---

<!-- dev-team-pack:begin -->
# Dev Team Pack
## Tech Stack

- Node.js (ES modules)
- JavaScript
- No runtime dependencies declared in package.json

## Architecture

Explain folders and patterns.

## Coding Rules

- Use functional React components
- Prefer server components
- Use Tailwind utilities instead of custom CSS
- do not put any comments in!
- only 1 component per file named after the component
- do not use constants for all text, only if there are some arrays, maps or json objects that get used. we do not need text or similar things as a constant

## Design System

- Follow ShadCN patterns

## Commands

`npm run analyze`
`npm test`

The assistant MUST use only the commands listed above for running, building, testing, and linting this project. Do not invoke any other package manager, test runner, or build tool.

# lean-ctx — Context Engineering Layer

PREFER lean-ctx MCP tools over native equivalents for token savings:

| PREFER                      | OVER                     | Why                                                            |
| --------------------------- | ------------------------ | -------------------------------------------------------------- |
| `ctx_read(path)`            | Read / cat / head / tail | Session caching, 8 compression modes, re-reads cost ~13 tokens |
| `ctx_shell(command)`        | Bash (shell commands)    | Pattern-based compression for git, npm, cargo, docker, tsc     |
| `ctx_search(pattern, path)` | Grep / rg                | Compact context, token-efficient results                       |
| `ctx_tree(path, depth)`     | ls / find                | Compact directory maps with file counts                        |

## ctx_read Modes

- `full` — cached read (use for files you will edit)
- `map` — deps + API signatures (use for context-only files)
- `signatures` — API surface only
- `diff` — changed lines only (after edits)
- `aggressive` — syntax stripped
- `entropy` — Shannon + Jaccard filtering
- `lines:N-M` — specific range

## File Editing

Use native Edit/StrReplace when available. If Edit requires Read and Read is unavailable,
use `ctx_edit(path, old_string, new_string)` — it reads, replaces, and writes in one MCP call.
NEVER loop trying to make Edit work. If it fails, switch to ctx_edit immediately.
Write, Delete have no lean-ctx equivalent — use them normally.
<!-- dev-team-pack:end -->
