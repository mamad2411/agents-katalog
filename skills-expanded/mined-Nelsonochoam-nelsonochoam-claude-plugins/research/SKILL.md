---
name: research
description: Answer research questions by exploring the codebase factually and writing findings to a document.
disable-model-invocation: true
model: opus
---

User's request: $ARGUMENTS

# Research Codebase

You are tasked with answering a set of research questions by exploring the codebase and writing up what you find. You spawn parallel sub-agents to cover the questions efficiently, synthesize their findings, and write the results to a document.

## CRITICAL: YOUR ONLY JOB IS TO DOCUMENT AND EXPLAIN THE CODEBASE AS IT EXISTS TODAY
- DO NOT suggest improvements or changes
- DO NOT infer what the user is trying to build and offer opinions about it
- DO NOT propose future enhancements
- DO NOT critique the implementation or identify problems
- ONLY describe what exists, where it exists, how it works, and how components interact

## Input Resolution

Run feature-discovery (`${CLAUDE_PLUGIN_ROOT}/references/feature-discovery.md`) with current phase `research` to resolve `$FEATURE_PATH`.

**Before reading artifacts**, run prerequisite check per `${CLAUDE_PLUGIN_ROOT}/references/prerequisite-check.md` for phase `research`. If the check halts, stop here.

**Auto-advance**: If `$ARGUMENTS` contains `--autoadvance`, follow the auto-advance protocol in the prerequisite check reference before proceeding. Strip `--autoadvance` from arguments before using them as context.

### Resolve research input

Try to read `$FEATURE_PATH/2-research-questions.md`.

- **If it exists**: use it as the primary input. Do NOT read `1-intent.md` — the research phase stays unbiased about what is being built when research questions have been explicitly defined.
- **If it does not exist**: read `$FEATURE_PATH/1-intent.md` instead. Derive 3–7 focused research questions from the intent — questions that help understand the current codebase state relevant to what the intent describes. These derived questions are internal and ephemeral; do NOT write them to a file. Proceed with these questions as if they came from 2-research-questions.md.

## Steps

### 1. Decompose and Plan

Break the questions into distinct research areas. Read `${CLAUDE_SKILL_DIR}/references/agent-types.md` for the available agent types and assign each area to the right fit.

### 2. Spawn Parallel Sub-agents

Run agents concurrently for independent questions or areas. Give each agent a focused, narrow scope. Remind them: document what exists, no recommendations.

Wait for **all sub-agents to complete** before synthesizing.

### 3. Synthesize

Compile all findings. Organize by question or component area, not by which agent found what. Verify critical claims by reading the relevant file sections yourself. When sources differ, prefer the live codebase.

### 4. Generate Permalinks

Before writing the document, resolve the GitHub permalink base so all file references are clickable:

```bash
REPO=$(gh repo view --json owner,name --jq '"\(.owner.login)/\(.name)"')
SHA=$(git rev-parse HEAD)
```

Every `file:line` reference in the document must be a markdown link using:
`https://github.com/$REPO/blob/$SHA/$FILE_PATH#L$LINE` (or `#L$START-L$END` for ranges).

### 5. Write the Research Document

Read the document format from `${CLAUDE_SKILL_DIR}/references/template.md`. Write findings to `$FEATURE_PATH/3-research.md` (create the directory if needed).

Then say:

```
Written to $FEATURE_PATH/3-research.md — please review.
```

### 6. Iterate Until Confirmed

If the user requests more depth on a question, do a targeted sub-agent lookup and update the file with Edit. Re-prompt for review. Do not reprint the full document to the conversation.

Once the user confirms, say:

```
════════════════════════════════════════
✓ Research confirmed.

Recommended next: /crispy:design
Any phase can follow — each works with whatever artifacts exist.
════════════════════════════════════════
```

## Guidelines

- **Wait for all agents**: Never synthesize partial results
- **Detailed Findings use bullets**: Each bullet is a factual observation with a `file:line` reference
- **Code snippets are selective**: Only include a snippet when prose alone cannot explain the behavior — most findings should be bullet text with a permalink
- **Code References are a flat index**: Every file touched during research should appear here
- **No recommendations**: If you notice something worth flagging, put it in Open Questions — not as a suggestion
