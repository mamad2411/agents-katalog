---
name: strategy-debate
description: Run a structured Claude + Codex strategy debate for ideas, trade-offs, positioning, or decisions. Use when the user wants both voices, cross-critique, revised positions, a chosen finalizer, and a saved transcript.
argument-hint: "[topic or brief, optional finalizer, optional log file, optional constraints]"
disable-model-invocation: true
---

# Strategy Debate

Use this skill for strategy, product, GTM, positioning, roadmap, research direction, and idea-quality discussions.

Treat `$ARGUMENTS` as the debate brief.

## Non-negotiable rules

1. If Codex is not available in the current Claude Code session, say that explicitly and stop. Do not fabricate Codex output.
2. Show both Claude and Codex contributions in the chat. Do not collapse Codex into a one-line paraphrase.
3. Unless the user opted out of logging, save the full debate transcript to a resolved log path.
4. If logging is enabled, show the exact log path at the start and confirm save success or failure at the end.

## Log file resolution

Accept either `Log File:` or `Save As:` in the user brief.

Resolve the log path with these rules:

0. If the user passes `No Log`, `Log: none`, or `Log File: none`, skip all file writing. Do not resolve a path, do not create directories, do not save anything.
1. If the user provides only a filename such as `smb-vs-enterprise`, save to `.claude/debate-logs/smb-vs-enterprise.md`.
2. If the user provides a filename with `.md`, keep it and save to `.claude/debate-logs/<name>.md`.
3. If the user provides a relative path with folders such as `notes/decisions/smb-vs-enterprise.md`, use it relative to the project root.
4. If the user omits the log path, default to `.claude/debate-logs/${CLAUDE_SESSION_ID}-strategy-debate.md`.
5. Create parent directories if needed.

## Debate protocol

Unless the user explicitly names a finalizer, default to `Claude`.

Run the debate in this exact order:

1. Extract or infer:
   - topic
   - goal of the debate
   - explicit constraints
   - requested finalizer (`Claude` or `Codex`)
   - resolved log path (skip if logging is disabled)
2. Produce `Claude v1` as an independent position.
3. Ask Codex for `Codex v1` as an independent position. Do not ask Codex to merely agree with Claude.
4. Produce `Claude critique of Codex v1`:
   - strongest points
   - weakest points
   - what is missing
5. Ask Codex for `Codex critique of Claude v1`:
   - strongest points
   - weakest points
   - what is missing
6. Produce `Claude v2`, revised after Codex's critique.
7. Ask Codex for `Codex v2`, revised after Claude's critique.
8. Produce `Final synthesis` by the selected finalizer.
9. Produce `Unresolved disagreements`.
10. Produce `Recommendation` and `Confidence`.

## Required chat format

Use these section headings in the visible answer:

- `Log Path` (omit if logging is disabled)
- `Topic`
- `Claude v1`
- `Codex v1`
- `Claude -> Codex Critique`
- `Codex -> Claude Critique`
- `Claude v2`
- `Codex v2`
- `Final Synthesis`
- `Unresolved Disagreements`
- `Recommendation`
- `Confidence`
- `Protocol Summary`

## Protocol summary

After the debate is complete, add a `Protocol Summary` section that contains:

1. A line stating how many stages were completed.
2. A numbered list with a one-line summary of each stage — what was said, what was challenged, what changed.
3. A closing paragraph on the most important disagreement the debate surfaced and how mutual critique resolved it.

Write this section in the same language as the topic. If the topic is mixed-language or unclear, use the primary language of the user's brief.

## Logging requirements

If the user opted out of logging, skip this entire section — do not write any files and do not print log status lines.

Write the same visible debate to the resolved log path.

If the file already exists, append a new debate entry instead of overwriting prior entries, unless the user explicitly asks to replace it.

Each saved entry must contain:

- date or session context if available
- raw user brief
- chosen finalizer
- resolved log path
- every visible section from the answer

After saving, end with one short line:

`Log saved: <path>` or `Log failed: <reason>`.

## Quality bar

- Keep the discussion focused on strategy and trade-offs, not implementation trivia.
- Surface assumptions explicitly.
- Distinguish facts from inferences.
- Prefer disagreement that is useful over false consensus.
- If the debate reaches convergence early, still complete the full structure.

## Example invocation

`/strategy-debate Finalizer: Claude. Log File: smb-vs-enterprise-2027. Topic: Should we position the product for SMB first or enterprise first in 2027? Constraints: team of 6, limited sales capacity, need fast feedback loops.`
