---
name: chatlab-analyze
description: Analyze local ChatLab chat records through the chatlab CLI. Use when the user asks an external agent to inspect conversations, find evidence, summarize topics, compare members, or analyze a named relationship from imported ChatLab data.
---

# ChatLab Analyze

Use this skill when the user asks you to analyze local ChatLab chat records, especially when they explicitly write `chatlab-analyze`, ask about a person or group in their chat history, or want evidence from imported conversations.

Example user request:

```text
chatlab-analyze 帮我分析我和小红的聊天记录
```

Install this skill with:

```bash
npx skills add ChatLab/ChatLab --skill chatlab-analyze -g
```

## What ChatLab Provides

`chatlab` is a local CLI for querying chat records imported into ChatLab. Treat it as the source of truth for sessions, members, messages, statistics, topics, and read-only SQL fallback.

The CLI is read-only for this skill. Do not modify ChatLab data, import files, change config, or start long-running services unless the user explicitly asks.

## First Steps

1. Check that the CLI is available:

```bash
chatlab --help
```

2. Load the command contract before deeper work:

```bash
chatlab manifest
```

3. List sessions. If exactly one session is relevant, use it. If multiple sessions may match the user's wording, ask a short clarification or show the likely candidates.

```bash
chatlab sessions list --format json
```

## Privacy Rules

- Always pass `--format` explicitly.
- Use `--format agent` when reading message bodies.
- Use `--format json` for structural scouting such as session lists, member lists, counts, fields, and `--no-content` searches.
- Do not use `--raw`. ChatLab disables raw output by default because the safe path applies the user's desensitization and blacklist rules.
- Do not reveal full chat dumps. Retrieve only the context needed for the user's question.
- Cite evidence with ChatLab message markers such as `[#1021]`, `[#1021*]`, or merged ranges like `[#1021-1024]` when available.

## Common Workflows

### Analyze a One-To-One Relationship

Use this when the user asks about themselves and another person, for example "我和小红".

```bash
chatlab members list --session <session-id> --format json
chatlab messages between --member me --member <member> --session <session-id> --last 90d --format agent
chatlab stats keywords --session <session-id> --member me --last 90d --top 20 --format json
chatlab stats keywords --session <session-id> --member <member> --last 90d --top 20 --format json
```

Then answer with patterns, concrete examples, and limits. If the retrieved time range is narrow, say so and offer the next query you would run.

### Find Who Mentioned Something First

```bash
chatlab messages search "<keyword>" --session <session-id> --sort asc --limit 5 --context 3 --format agent
chatlab messages context --id 1021 --session <session-id> --window 10 --format agent
```

Use the earliest hit and its surrounding context as evidence. The `[#1021*]` marker identifies the matching message.

### Summarize Recent Topics

```bash
chatlab topics list --session <session-id> --last 30d --format agent
chatlab stats keywords --session <session-id> --last 30d --top 20 --format json
chatlab messages list --session <session-id> --last 7d --limit 80 --max-tokens 3000 --format agent
```

Prefer topic summaries first. Use keywords and recent messages to verify or fill gaps.

### Scout Before Pulling Message Bodies

Use JSON scouting before retrieving many message bodies.

```bash
chatlab messages search "<keyword>" --session <session-id> --since 2026-01-01 --no-content --limit 100 --format json
chatlab messages search "<keyword>" --session <session-id> --cursor <meta.nextCursor> --format agent
```

When `meta.hasMore` is true, continue with `--cursor <meta.nextCursor>` using the same query conditions.

### Read-Only SQL Fallback

Only use SQL when dedicated commands cannot answer the question.

```bash
chatlab schema --session <session-id> --format json
chatlab sql "SELECT COUNT(*) AS n FROM message" --session <session-id> --format json
```

SQL output still goes through ChatLab's privacy preprocessing for string values.

## Answering Style

- Start with the direct answer, then give evidence and caveats.
- Name the session and time range you actually queried.
- Separate observed facts from interpretation.
- For relationship analysis, avoid overclaiming emotional intent. Use language like "从这些记录看..." and ground claims in message evidence.
- If member names are ambiguous, stop and ask the user to choose from the candidate ids.
- If ChatLab returns an error envelope, follow `error.hint` and retry only when the correction is clear.

## Useful Command Hints

- Time supports ISO dates, `today`, `yesterday`, and `--last 30d`.
- Members can be ids, exact display names, aliases, or `me`.
- Pagination uses `meta.hasMore` and `meta.nextCursor`.
- Token controls: `--limit`, `--max-messages`, `--max-tokens`, and `--max-chars`.
