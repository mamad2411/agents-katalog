---
name: llm-chat-librarian
description: "Agent loads when working with raw LLM conversation exports — organizing, summarizing, and extracting value from chat dumps"
---

# LLM Chat Librarian

Tools for turning raw LLM conversation exports into navigable, extractable knowledge. Works with any chat provider's export format (ChatGPT, Claude, Gemini, etc.) in any representation (.md, .json, HAR, mixed).

## Commands

| Command | Phase | What it does |
|---------|-------|--------------|
| `chatlib-digest` | Foundation | Write SUMMARY.md for a directory of messages (single dir or whole tree, bottom-up) |
| `chatlib-survey` | Discovery | Analyze structure, count topics, map conversation tree (reads digested summaries) |
| `chatlib-triage` | Discovery | Assess file type relevance for a given audience |
| `chatlib-segment` | Organization | Split into topical sub-conversations, flatten forks |
| `chatlib-assess` | Evaluation | Rank artifacts by value and dependency order |
| `chatlib-extract` | Extraction | Pull key messages into standalone docs with provenance |
| `chatlib-index` | Navigation | Write top-level SUMMARY.md as latecomer entry point |

Each command is documented in `commands/chatlib-<name>.md`.

## Suggested Workflow: Value Extraction

For turning a raw conversation export into usable project artifacts:

```
1. chatlib-digest     → summarize every directory bottom-up (parallelizable)
2. chatlib-survey     → understand what you have (fast — reads summaries, not raw messages)
3. chatlib-triage     → decide which file types matter
4. chatlib-segment    → split into topical units
5. chatlib-digest     → summarize each segment (same command, different input)
6. chatlib-assess     → identify what's worth extracting
7. chatlib-extract    → pull artifacts with provenance
8. chatlib-index      → create the entry point
```

`chatlib-digest` appears twice: first on the raw tree (step 1), then on the segmented view (step 5). Same command — write a SUMMARY.md for a directory of messages. Step 1 is the foundational pass that makes everything downstream fast. Step 5 adds cross-references between segments.

Steps 2–3 are fast and read-only. Steps 4–5 produce the organized view. Steps 6–8 produce the extractable value.

## When to Skip Steps

- **Already digested?** If SUMMARY.md files exist throughout the tree, skip `chatlib-digest` — go straight to `chatlib-survey`.
- **No forks?** Skip fork-flattening in `chatlib-segment`.
- **Single topic?** Skip `chatlib-segment` — one `chatlib-digest` pass is enough.
- **User already knows what's valuable?** Skip `chatlib-assess` — go straight to `chatlib-extract` with their list.
- **No project context to drift against?** Skip drift analysis in `chatlib-assess` and `chatlib-extract`.

Not every conversation needs all steps. A short, linear conversation might only need `chatlib-digest` + `chatlib-survey`. A large branching conversation with buried design decisions needs the full pipeline.

## Principles

- **Digest first.** The single biggest efficiency gain is creating summaries before doing anything else. Everything downstream reads summaries, not raw messages.
- **Symlink, don't copy.** Organized views point back to source data. Single source of truth.
- **Provenance over prescription.** Every extracted artifact says where it came from, who endorsed it, and what context is lost by reading it standalone.
- **Dependency order over conversation order.** What enables what matters more than what was said first.
- **Ask, don't infer.** When project state is ambiguous, ask the user rather than guessing from repo contents.

## Adapting to Different Formats

The commands assume message files with recognizable naming (numbered, role-tagged). If the input format is different:
- Conversation exports as single files: split first, then proceed.
- HAR files: extract conversation JSON before entering the pipeline.
- API response dumps: identify the message content fields and render to .md before proceeding.

The pipeline is format-agnostic once you have one file per message with readable content.
