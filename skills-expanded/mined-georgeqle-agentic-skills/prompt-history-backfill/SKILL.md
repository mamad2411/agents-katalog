---
name: prompt-history-backfill
description: Scan Claude and Codex conversation history for skill invocation prompts missing from repo prompt history and report or backfill them safely
type: analysis
version: v0.2
required_conventions: [alignment-page]
argument-hint: "[--repo <path>] [--skill <slug>] [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--apply] [history/export paths...]"
---

# Prompt History Backfill

Invoke as `$prompt-history-backfill`.

Use this skill when the user wants to audit or backfill `prompts/<skill-slug>/` prompt-history artifacts from local Claude Code and Codex conversation history. The skill identifies visible user prompts that invoked skills, compares them with the target repository's prompt-history convention, and produces a reviewable report by default.

## Inputs

- Default target repository: current working directory.
- Optional `--repo <path>` to target another repository.
- Optional `--skill <slug>` to limit detection and output to one skill.
- Optional `--since YYYY-MM-DD` and `--until YYYY-MM-DD` filters.
- Optional user-provided history files, exported logs, or session directories.
- Default Claude history file: `~/.claude/history.jsonl`.
- Default Codex prompt history file: `~/.codex/history.jsonl`.
- Default Codex rich session root: `~/.codex/sessions/**/*.jsonl`.

## Process

1. Resolve arguments and mode:
   - Default mode is report-only.
   - Do not create, modify, or remove prompt files unless the visible invocation includes explicit `--apply`.
   - In report-only mode, prompt backfill candidates are reviewed but no files under `prompts/<skill-slug>/` are created.

2. Resolve known skills in the target repo:
   - Read active non-archive `SKILL.md` files under `base/`, `packs/`, `.claude/skills/`, and `.codex/skills/` when present.
   - Include existing `prompts/<skill-slug>/` directories as known prompt-history targets.
   - Maintain a hardcoded legacy skill map for slugs that no longer exist as active skills:
     - `run` — renamed → `exec`
     - `review` — renamed → `expert-review`
     - `skill-creator` — split/renamed → `create-agentic-skill` + `create-local-skill`
     - `verify` — never a skill (native tool)
     - `simplify` — never a skill (native tool)
     - `schedule` — never a skill (native tool)
   - Apply `--skill <slug>` before writing or reporting candidate rows when provided.

3. Read conversation history:
   - Read all existing default sources for the selected date range: `~/.claude/history.jsonl`, `~/.codex/history.jsonl`, and `~/.codex/sessions/**/*.jsonl`.
   - Read optional user-provided history/export paths in addition to the defaults unless the user explicitly says to use only those paths.
   - If a source is missing or unreadable, report it and continue with available sources.

4. Normalize records into visible user prompt candidates only:
   - Claude compact history: use visible user-facing fields such as `display`, timestamp, project, session ID, and directly pasted visible context such as `pastedContents`.
   - Codex compact history: use prompt `text`, timestamp, session ID, and cwd/project metadata when available.
   - Codex rich session JSONL: include user `response_item` records only when they are user-authored messages.
   - Exclude hidden system instructions, hidden developer instructions, base prompts, tool output, tool arguments, assistant messages, unavailable model context, and generated summaries.

5. Classify candidate confidence:
   - High confidence: the visible user prompt begins with or clearly invokes `/skill-name`, `$skill-name`, or `You have the <skill> skill installed`.
   - Medium confidence: the visible user prompt names a known skill and asks the agent to use it, but does not use command syntax.
   - Low confidence: the prompt only loosely mentions a skill or workflow. Include it in the report, but never write it even when `--apply` is present.
   - When a candidate's skill slug matches a legacy skill map entry, tag it as `legacy: true` in addition to its confidence level.

6. Compare against existing prompt history:
   - For each high- or medium-confidence candidate, inspect `prompts/<skill-slug>/`.
   - Skip an existing identical prompt file when the preserved visible prompt text and required frontmatter already match.
   - When a timestamp filename collides with different content, add a deterministic short session suffix while preserving the base `skill-prompt-YYYYMMDD-HHMMSS-<short-topic>` filename shape.

7. Block likely secrets before writing:
   - Before any `--apply` write, scan candidate prompt text for likely secrets such as API keys, bearer tokens, private keys, cookie/session tokens, password assignments, credential-bearing URLs, database URLs, and common provider token prefixes.
   - If a candidate contains a likely secret, do not write it. Mark it as blocked in the report and ask the user for a sanitized prompt.

8. Write outputs:
   - In report-only mode, write a review artifact at `alignment/prompt-history-backfill-{topic}.html` following `ALIGNMENT-PAGE.md`, plus a concise chat summary.
   - In `--apply` mode, create missing prompt files under `prompts/<skill-slug>/` for active skills, or under `prompts/legacy/<old-slug>/` for legacy skills.
   - Legacy skill prompt files add `legacy: true` and optional `successor: <new-slug>` to their YAML frontmatter (successor is included when the legacy map has a renamed/split successor).
   - Use this YAML frontmatter exactly for every backfilled prompt file: `skill`, `agent`, `captured_at`, `source`, and `prompt_scope: visible-user-invocation`.
   - Use `source: user-invocation` unless the user explicitly requests a more specific visible source label; put history file paths and session IDs in the report, not in prompt frontmatter.
   - Preserve the exact visible user prompt content after frontmatter without summarizing, redacting, or truncating.

## Output

The report should include:

- Scope: repository, filters, sources read, sources missing, and mode.
- Candidate summary by confidence, skill slug, source agent, timestamp, session ID, and status.
- Missing prompt files that would be created in report-only mode.
- Prompt files created in `--apply` mode.
- Existing identical prompt files skipped.
- Filename collisions and deterministic suffixes used.
- Low-confidence candidates excluded from writes.
- Likely-secret candidates blocked, with a sanitized-prompt request.
- Verification notes proving no hidden system/developer/tool output was used and all prompt writes stayed under `prompts/<skill-slug>/`.

## Constraints

- Report-only is the safe default; `--apply` is the only write mode for prompt files.
- Never write low-confidence candidates.
- Never write likely-secret candidates.
- Never write prompt files outside `prompts/<skill-slug>/` (active skills) or `prompts/legacy/<old-slug>/` (legacy skills).
- `prompts/legacy/<old-slug>/` is the only valid write path for legacy skill prompts; never create top-level `prompts/<old-slug>/` directories for legacy skills.
- Do not summarize, redact, or truncate the visible prompt body in backfilled prompt files.
- Do not include hidden system/developer instructions, tool output, assistant messages, or unavailable model context in prompt files.
- Do not create or modify GitHub Actions workflows.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/prompt-history-backfill-{topic}.html`. By default, report results inline and write only this skill's normal durable artifacts; create an alignment page only when explicitly requested or when a concrete clarification/review need cannot be handled cleanly inline.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
