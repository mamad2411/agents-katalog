---
name: grill-me
description: "Brainstorm engine — interview the user about a plan/design, auto-write PRD and context manifests as answers resolve. Use when the user wants to stress-test a plan, brainstorm a feature, design architecture, or says 'grill me', 'brainstorm', 'let's plan', 'design this', or describes a new feature they want to build. Also use when the workflow phase is 'planning' and a task is active."
---

# Brainstorm Engine (grill-me)

Interview me relentlessly about every aspect of this plan. Walk down each branch of the design tree, resolving dependencies one-by-one. For each question, provide your recommended answer.

Ask questions one at a time. If a question can be answered by exploring the codebase, explore the codebase instead of asking.

## Why this skill writes files during the interview

If the brainstorm stays only in chat, a session timeout or `/compact` loses everything. Writing incrementally means every resolved question is immediately durable — the PRD builds up as you go, and a session crash loses at most the current question. The finalize step at the end cleans up the working draft into a polished document.

## Setup

Before the first question, ensure a task exists:

```bash
# Check for active task
python3 scripts/codex_harness.py task current

# If none exists, create one
python3 scripts/codex_harness.py task create "<title from user's request>"
python3 scripts/codex_harness.py task start <slug>
```

Note the task slug — you'll use it for every command below.

## The interview loop

Each turn of the brainstorm follows this pattern:

1. **Ask one question** with your recommended answer
2. **Wait for the user's answer** (they may accept your recommendation, modify it, or reject it)
3. **Immediately write the decision** — this is the critical step, don't batch these

### What "immediately write" means

After the user answers, run these before asking the next question:

```bash
# Step 1: Record the question (returns an ID like q-1)
python3 scripts/codex_harness.py task question ask <slug> "<your question>" --recommended-answer "<your recommendation>"

# Step 2: Record the user's answer (use the ID from step 1)
python3 scripts/codex_harness.py task question answer <slug> <id> "<their answer>" --decision "<one-line summary for prd.md>"
```

The `--decision` flag auto-appends to prd.md's Decisions section. Beyond that, also update the relevant section of prd.md directly:
- Scope/goal decisions → `## Goal`
- Feature requirements → `## Requirements`
- Implementation choices → `## Technical Approach`
- Quality bar decisions → `## Acceptance Criteria`
- Boundary decisions → `## Out of Scope`

If the decision identifies files the implementer will need:
```bash
python3 scripts/codex_harness.py task add-context <slug> implement "<spec-or-source-path>" "<why>"
```

If it identifies files the reviewer will need:
```bash
python3 scripts/codex_harness.py task add-context <slug> check "<spec-or-source-path>" "<why>"
```

Scan `.codex/spec/project/index.md` to know what specs exist for curation.

### Example turn

> **You**: "Should the keyboard shortcuts be user-configurable, or hardcoded? I'd recommend configurable with a JSON config file."
>
> **User**: "Configurable, but use a plist not JSON since this is a macOS app."
>
> **You**: *(runs `task question ask <slug> "..." --recommended-answer "..."`, gets back id q-1, runs `task question answer <slug> q-1 "Configurable via plist" --decision "Shortcuts: user-configurable via plist"`, updates prd.md Technical Approach, adds playback-state-sync.md to implement.jsonl, then asks next question)*

## Convergence and finalize

The brainstorm converges when you've explored all branches and no new questions are emerging. Typically this is after 5-10 questions. When you sense convergence, say so: "I think we've covered the main decisions. Ready to finalize the PRD?"

When the user confirms:

1. **Rewrite prd.md** as a clean document (replace the working draft entirely):
   - `## Goal` — one paragraph
   - `## Requirements` — numbered list
   - `## Technical Approach` — architecture decisions, key patterns
   - `## Acceptance Criteria` — checkboxes
   - `## Out of Scope` — explicit exclusions
   - `## Decisions` — all Q&A pairs from the brainstorm

2. **Verify manifests**:
   ```bash
   python3 scripts/codex_harness.py task list-context <slug>
   ```

3. **Validate readiness**:
   ```bash
   python3 scripts/codex_harness.py task validate <slug>
   ```

4. **Record to journal**:
   ```bash
   python3 scripts/codex_harness.py record-session --title "Brainstorm: <task-title>" --summary "<one-line summary>"
   ```

5. Announce: "Brainstorm complete. PRD written, manifests curated. Ready for `task start`."
