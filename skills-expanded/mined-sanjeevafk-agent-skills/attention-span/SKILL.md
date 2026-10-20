---
name: attention-span
description: ADHD-friendly output styles and attention-kind conciseness rules for AI agents (Claude Code, Codex, Antigravity, Cursor, Windsurf, Copilot). Provides Attention-kind, Spartan, and Rundown output styles for scannable, token-efficient agent communication.
license: AGPL-3.0
metadata:
  origin: alexgreensh/attention-span
  version: 0.6.0
tools: Read, Write, Edit, Bash, Grep, Glob
---

# Attention Span Skill

A collection of ADHD-friendly output styles and conciseness guidelines for AI coding agents that optimize for reader scannability and attention retention without compromising engineering quality.

## When to Activate

- Asking an agent to format responses for maximum scannability and plain-English clarity
- Configuring or switching agent output styles (`Attention-kind`, `Spartan`, `Rundown`)
- Reducing token verbosity and eliminating AI fluff/preambles in agent responses
- Setting up global or project-level output style rules across AI agents (Claude Code, Codex, Antigravity CLI, Cursor, Windsurf, Copilot)

## Available Output Styles

| Style | Description | Ideal For |
|---|---|---|
| **Attention-kind** | ADHD-friendly, front-loaded answers, heavy bolding, arrow markers (`→`), spaced out blocks | General pair programming, deep focus, preventing wall-of-text fatigue |
| **Spartan** | Zero-warmth, blunt, imperative, maximum signal-to-noise ratio | Heads-down work, rapid execution, quick technical answers |
| **Rundown** | Briefing style with TL;DR, status checklist (`✅`/`🟡`/`⬜`), action items tagged with emoji | Standups, status updates, progress reports |

---

## Core Guidelines & Principles

### 1. Attention-Kind Principles
- **Lead with the bottom line in line 1.** The first sentence contains the direct answer.
- **Say the least that fully answers.** Eliminate preambles ("Great question!", "Sure thing!"), restating questions, or closing restatements.
- **Build for scanning:**
  - Mark key points with `**→ Lead-in.**` on a new line with blank lines between paragraphs.
  - **Bold the main takeaway and key terms/numbers** so skimming only the bold text yields the complete answer.
- **Preserve critical details:** Never cut a warning, caveat, exact threshold, or scoped condition to save words.
- **Depth requests suspend brevity:** If the user asks to "explain deeply", "walk me through it", or "give full context", brevity constraints are suspended for that turn.

### 2. Spartan Principles
- **Imperative & direct:** Strip all warmth, transitions, and conversational fluff.
- **Deliverable purity:** When asked for code, a commit message, or a document, return *only* the requested artifact without wrapping text.
- **One idea per paragraph block.**

### 3. Rundown Principles
- **Open with `TL;DR:`** carrying the complete summary.
- **State checklist:** `☑️ Done`, `🟡 In Progress`, `⬜ Not Started`.
- **Group next choices under `Your move:`** with relevant emoji markers.
- **Never invent status:** Report only verified facts.

---

## Multi-Agent Configuration

### Claude Code
Output styles can be selected via `/style`:
```bash
# Global output styles directory
mkdir -p ~/.claude/output-styles ~/.claude/commands
cp output-styles/*.md ~/.claude/output-styles/
cp commands/style.md ~/.claude/commands/
```
To set as default in `~/.claude/settings.json`:
```json
{
  "outputStyle": "Attention-kind"
}
```

### Codex
Append the body of the desired output style to `~/.codex/AGENTS.md` (idempotent block):
```markdown
<!-- attention-span:start -->
[Attention-kind instructions body]
<!-- attention-span:end -->
```

### Antigravity CLI (agy)
Append the style body to `GEMINI.md` in the current project or home directory:
```markdown
<!-- attention-span:start -->
[Attention-kind instructions body]
<!-- attention-span:end -->
```

### Windsurf / Devin / Cursor
For Windsurf/Devin global memories:
`~/.codeium/windsurf/memories/attention-kind.md`
For Cursor global rules:
`~/.cursor/rules/attention-kind.mdc` or `~/.cursor/rules/`

---

## Repository & Links

- Source Repository: [github.com/alexgreensh/attention-span](https://github.com/alexgreensh/attention-span)
- License: AGPL-3.0
