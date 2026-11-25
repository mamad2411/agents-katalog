---
name: startup-content-machine
description: Turn what your startup actually built into posts and short-video scripts. Reads your coding-agent session logs (Claude Code, Codex), git history and company docs from the last days, pulls out real moments (shipped features, numbers, decisions, failures, user quotes), and drafts LinkedIn posts, X posts and 30-60 s video scripts you can edit in Compound. Use when a founder asks "what should I post this week?", "turn my work into content", "build in public", or wants a content calendar from their own work.
---

# Startup Content Machine

Your best content already exists: it is in the work you and your agents did this week. This skill finds it, checks it, and drafts it. It never posts.

## 1. Collect (5 minutes)
Run the collector over the last 7 days (change `--days` as needed):
```bash
python3 scripts/collect.py --days 7 --repo . --out content-digest.md
```
It reads, read-only:
- Claude Code sessions `~/.claude/projects/*/*.jsonl` and Codex sessions `~/.codex/sessions/**/*.jsonl`: your requests and the agent's final summaries, not tool noise.
- `git log` of `--repo` (commit subjects, dates, files touched).
- Company context: `README.md`, `CLAUDE.md`, `AGENTS.md`, `CHANGELOG.md`, `docs/` headings.
Secrets are redacted (keys, tokens, emails, phone numbers). Review the digest before using it anywhere else.

## 2. Pick moments
From the digest, list 5 to 10 moments. A moment is one of:
| type | example |
|---|---|
| Shipped | "Launched X. It does Y for Z." |
| Number | a real metric that moved (users, speed, cost, accuracy) |
| Decision | something you stopped, killed or chose, and why |
| Failure | what broke, what you learned |
| User | a real user quote or request |
| Behind the scenes | how the agent and you built it |

For each: one-line claim, the source (log file + line, commit hash, doc), and whether it is public. **No source, no moment.** Never invent numbers, users or quotes. Drop anything about customers, revenue or people that is not already public.

## 3. Draft
For the top 3 moments, write:
- **LinkedIn:** line 1 is the result or the surprising fact in under 12 words, no question opener, no number as the very first character. Short lines, one idea each, normal capitalization, 60 to 180 words, link in the first comment.
- **X:** under 280 characters, same story, link in a reply.
- **Video (30 to 60 s):** frame 0 shows the result, then 3 to 5 beats (what you tried, what happened, the proof), each with the on-screen text and the clip or screen recording it needs. Hand it to Compound to cut: footage in, captions, music, export.
Under every draft add a source map: one line per claim, where it came from.

## 4. Check before you show anyone
- Every claim maps to a source; anything else is cut.
- No secrets, internal URLs, customer names or private numbers.
- No disclaimers, no "game-changer", no em dashes, no stat stacks (max 3 lines with numbers).
- Line 1 read alone: would a stranger understand it?

## 5. Output
`content-week.md`: a 7-day calendar (1 LinkedIn + 1 X per weekday, 1 video), the drafts, the video scripts and the source maps. The founder edits and approves; posting is theirs.
