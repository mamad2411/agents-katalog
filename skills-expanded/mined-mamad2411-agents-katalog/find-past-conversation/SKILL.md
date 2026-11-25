---
name: find-past-conversation
description: "Searches past Claude Code session transcripts under ~/.claude/projects/ to recover a previous conversation by recalled phrase, error string, or topic. Use when the user says 'search your history for', 'find the conversation about', 'look through your past sessions', 'did I ever finish that work on', 'what did we decide about X last week', 'remind me what came out of that session', or otherwise asks you to recall a prior session. Returns session ID, project, date, and a 2-4 sentence summary; on request, also reports the outcome (commit, branch, PR opened or merged). Not for searching the current codebase, current PR comments, or external systems like Slack/Jira — for those, see codebase-analyzer and address-pr-comments."
license: MIT
---

# Find a Past Claude Code Conversation

You are helping the user recall a previous Claude Code session. They remember roughly *what* was discussed, and they want you to find the actual transcript — the session ID, when it happened, a short summary, and (if relevant) what shipped from it.

Claude Code stores every session as a JSON-lines file under `~/.claude/projects/`. This skill tells you how to search those transcripts efficiently without burning context on multi-megabyte log files.

## When to use this skill

Trigger on phrases like:

- "search your history for [topic]"
- "find the conversation we had about [topic]"
- "look through your past sessions for [topic]"
- "did I ever finish that work on [topic]"
- "what did we decide about [topic] last week"
- "remind me what came out of the [topic] session"

Do **not** use this for searching the current codebase, the current PR's comments, or external systems like Slack/Jira — those have their own skills and tools.

## How transcripts are organized

```
~/.claude/projects/
├── -Users-alice-source-acme-api/
│   ├── 06c5c59e-0735-...jsonl          # one session = one file
│   ├── a7e955d8-cf10-...jsonl
│   └── a7e955d8-cf10-.../
│       └── subagents/
│           └── agent-ab42fde6...jsonl  # subagent transcripts
├── -Users-alice-source-acme-worker/
└── ...
```

Important facts:

- **The project folder is the working directory with `/` replaced by `-`.** So a session run in `/Users/alice/source/acme/api` lives under `~/.claude/projects/-Users-alice-source-acme-api/`.
- **The session ID is the filename without `.jsonl`** — e.g. `a7e955d8-cf10-42ec-a36b-0fe2bcb42d45`.
- **Each line in the `.jsonl` is a single JSON message** with a `type` field (`user`, `assistant`, `system`, etc.), a `timestamp`, and content. Lines are not pretty-printed and can be tens of KB each.
- **Subagent transcripts live in `<session-id>/subagents/agent-*.jsonl`.** They're noisy and multiply hits without adding much. Skip them by default.

## The search workflow

### Step 1 — Pick the right project folder

If the user is currently working in a repo and the session they remember was *in that repo*, start there. Compute the project folder from the current working directory:

```bash
ENCODED=$(pwd | sed 's|/|-|g')
ls ~/.claude/projects/$ENCODED/*.jsonl 2>/dev/null | wc -l
```

If the user is fishing across all their work (e.g. "did we ever talk about X anywhere?"), search across every project:

```bash
ls -d ~/.claude/projects/*/
```

When in doubt, ask: *"Was that conversation in this repo, or across all your work?"* — narrowing the search up front saves time and reduces false positives.

### Step 2 — Run a targeted ripgrep

Use `rg` on the project folder(s). Never `cat` whole `.jsonl` files — they routinely run into the megabytes and contain large model-thinking blocks with cryptographic signatures that blow context.

```bash
rg -l -i "<distinctive phrase>" ~/.claude/projects/<project>/*.jsonl
```

`-l` (list-only) is the right first move — you just want the candidate files. Look at content in a second pass once you've narrowed.

**Search-string hygiene matters.** Common words produce noise:

- `auto-approve` → hits every CI workflow with `terraform apply -auto-approve`
- `commit` → hits every git commit message in every session
- `error` → hits every retried bash command

If the user only has a generic word, **ask them for a distinctive phrase** before searching: an error string, a function name, a flag, a file path, a UI label, a person's name. One specific phrase beats five generic ones.

Subagent transcripts live one level deeper (`<project>/<session-id>/subagents/agent-*.jsonl`), so a top-level shell glob like `~/.claude/projects/<project>/*.jsonl` skips them automatically — no extra flag needed for the targeted case:

```bash
rg -l -i "your phrase" ~/.claude/projects/<project>/*.jsonl
```

If you instead recurse with ripgrep across everything (e.g. when you don't know the project), exclude the subagent subtree explicitly — otherwise you'll get duplicate hits:

```bash
rg -l -i "your phrase" ~/.claude/projects \
   --glob '*.jsonl' --glob '!**/subagents/**'
```

### Step 3 — Triage the candidate list

- **0 hits** → tell the user, ask for a more distinctive phrase. Don't keep guessing at synonyms.
- **1-3 hits** → great, examine each.
- **4+ hits** → ask for a second narrowing term, or sort by recency and look at the most recent first (`ls -lt`).

### Step 4 — Extract context, JSON-aware

For each candidate file, pull surrounding context with bounded windows. Two patterns work well:

**Pattern A — grep with line context (fast, rough):**

```bash
rg -i -B 2 -A 5 "your phrase" ~/.claude/projects/<project>/<session>.jsonl | head -100
```

This catches a few hundred lines of raw JSON around each match. Good for a quick visual scan.

**Pattern B — JSON-aware extraction (cleaner):**

```bash
rg -i "your phrase" ~/.claude/projects/<project>/<session>.jsonl | \
  jq -r 'select(.type=="user" or .type=="assistant") |
         "\(.timestamp) [\(.type)] \(.message.content // .content | tostring | .[0:300])"'
```

This filters to user/assistant turns only and prints the timestamp + first 300 characters. Skip `tool_use` and `tool_result` entries unless they're directly relevant to what the user is searching for — they're voluminous and rarely the answer.

### Step 5 — Report the find

For each strong candidate, surface:

- **Session ID** (the filename without `.jsonl`)
- **Project folder** (`~/.claude/projects/<encoded>`)
- **Date / time** (use the timestamp on the matching message, or the file's mtime as a fallback)
- **2-4 sentence summary** of what was discussed and decided

If there are multiple candidates, list each briefly and let the user pick which one to dig into. Don't dump 20 KB of raw JSON into chat — they want a recap, not a re-read.

## Reporting the outcome (optional follow-up)

Often the user's real question is "did we ever ship that?" Once you've located the session, you can scan the transcript for what was actually done:

```bash
# Branches created, commits made, PRs opened
rg -o '"command":"git (commit|push|checkout -b)[^"]*' <session>.jsonl
rg -o 'gh pr create[^"]*' <session>.jsonl
rg -o 'https://github.com/[^"]*pull/[0-9]+' <session>.jsonl | sort -u
```

If you find a PR URL, check the current status:

```bash
gh pr view <N> --repo <owner>/<repo> --json number,title,state,mergedAt,reviewDecision,url
```

Report back: open / merged / closed, current review decision, and whether CI was last green. That's usually the answer the user actually wanted.

## Anti-patterns to avoid

- **Don't `cat` whole `.jsonl` files.** They are huge and contain `signature` blocks, base64 thinking traces, and tool-result payloads. Use `rg` first to find the matching lines, then `jq` or `grep -B/-A` to pull a window.
- **Don't grep for common words without a qualifier.** `approve`, `error`, `fix`, `commit`, `pr` will hit every session. Anchor on something distinctive the user remembers.
- **Don't trust the first match.** Sessions can run for hours; the canonical decision is often in a later turn. Scan the timestamps and prefer matches near the *end* of a session over the *start*.
- **Don't auto-include subagent transcripts.** They duplicate the parent session's content from a different angle and multiply hits. When recursing, exclude with `--glob '!**/subagents/**'`; with a top-level shell glob they're already skipped.
- **Don't paraphrase from memory.** If you're reporting what was discussed, ground every claim in an actual line you extracted from the file — model memory of past sessions is unreliable.
- **Don't search across `~/.claude/projects/*` when the user has clearly named the repo.** Narrow first.

## Failure modes and recovery

- **The search returns nothing.** Ask the user for a more specific phrase (error message, function name, file path, person's name). If they only remember a topic, try 2-3 synonym variants — but stop after that and ask, don't drift into pattern-matching forever.
- **The matching file is in a project you've never seen.** That's fine — the transcript still lives at `~/.claude/projects/<encoded-cwd>/`. The encoded directory name tells you the original cwd; you can `cd` there if you need to inspect the repo.
- **You find the session but can't tell what was decided.** Read the *last few user turns* and the *last assistant turn before a tool-use chain ended*. Decisions usually live in those, not in the middle of long debugging back-and-forth.

## Worked example

User says: *"Find the conversation we had about the bot auto-approving a PR when it finds approvals."*

```bash
# Step 1: across all projects since user didn't name a repo.
# The shell glob `*/[0-9a-f]*.jsonl` only matches top-level session files,
# so subagent transcripts (one dir deeper) are naturally excluded.
rg -l -i "auto.approv" ~/.claude/projects/*/[0-9a-f]*.jsonl
# → too many hits; mostly `terraform apply -auto-approve`. Ask for a distinctive phrase.

# User: "look for 'request changes'"
rg -l -i "request changes" ~/.claude/projects/*/[0-9a-f]*.jsonl
# → narrows to ~10 files. Sort by recency.

ls -lt $(rg -l -i "request changes" ~/.claude/projects/*/[0-9a-f]*.jsonl) | head -5

# Step 4: read context from the most recent candidate
rg -i -B 2 -A 5 "request changes" \
   ~/.claude/projects/-Users-alice-source-acme-api/a7e955d8-*.jsonl | head -60

# Step 5: report — Session a7e955d8-... in acme-api, 2026-05-14, about the review bot
#   posting a plain comment after a REQUEST_CHANGES review (which doesn't clear the
#   block) instead of submitting a new opinionated review.

# Outcome check
rg -o 'https://github.com/[^"]*pull/[0-9]+' \
   ~/.claude/projects/-Users-alice-source-acme-api/a7e955d8-*.jsonl | sort -u
# → https://github.com/acme/api/pull/23
gh pr view 23 --repo acme/api --json state,mergedAt,reviewDecision
# → OPEN, APPROVED, not yet merged
```

The user gets one tight answer: session ID, date, summary, and "PR #23 — approved but not merged."
