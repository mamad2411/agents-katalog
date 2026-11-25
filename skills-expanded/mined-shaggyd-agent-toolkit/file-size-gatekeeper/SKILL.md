---
name: file-size-gatekeeper
description: "Prevent silent context-window pressure and the '18,000 character trap' by enforcing file size discipline on skills, .env, SOUL.md, and config files. Inspired by Andrew's OpenClaw Blueprint series."
version: 1.1.0
author: Dustin Chadwick (@ShaggyD)
source: https://youtu.be/5ec5mh41oig
source_title: "Your OpenClaw AI Agent Is Ignoring Half Its Instructions — The 18,000 Character Trap"
tags: [housekeeping, maintenance, config, skills, performance, context-window]
---

# File Size Gatekeeper

> **Origin:** This skill was created after analyzing [Andrew's OpenClaw Blueprint video](https://youtu.be/5ec5mh41oig) (Video 2 of 8) on the "18,000 character trap."

## Problem

Files grow unchecked and silently degrade agent performance. Every extra character in a loaded file competes for space with the conversation, memory, and tool outputs. Bloated files don't break loudly; they make the agent gradually worse until you notice it's ignoring instructions buried deep in a SKILL.md.

## Built

A skill that enforces file size discipline with four techniques from Andrew's OpenClaw Blueprint: write dense, split files by topic, keep critical info at top and bottom, and audit regularly. Includes on-demand audit commands and threshold-based warnings so you always know which files are getting fat.

## Outcome

Your agent actually reads every instruction because nothing gets truncated or pushed out of context. Files stay lean, the context window stays open for the conversation, and the gradual degradation that creeps in over months is caught before it affects behavior.

## The Problem

Large files silently consume context window space. When a SKILL.md, .env, or reference file exceeds a safe threshold, it may cause:
- Context window pressure (less room for conversation)
- Token waste on content the agent can't effectively use
- Silent degradation — the agent appears to ignore instructions in the middle of bloated files

## Thresholds

| Threshold | Action |
|-----------|--------|
| **< 10,000 chars** | ✅ Safe — no action needed |
| **10,000 – 17,000 chars** | 👀 Caution — review on next edit |
| **> 17,000 chars** | ⚠️ Warning — flag for condense or split |
| **> 18,000 chars** | 🚩 Critical — must condense or split |

## Files to Monitor

- `~/.hermes/.env` — API keys (currently ~17.5k, mostly comments)
- `~/.hermes/SOUL.md` — persona identity
- `~/.hermes/config.yaml` — main config
- `~/.hermes/references/*.md` — reference docs
- `~/.hermes/skills/*/*/SKILL.md` — all skill files
- `~/.hermes/hermes-agent/AGENTS.md` — dev guide (only when working in repo)

## Usage

### On-Demand Audit

When the user asks "check sizes" or "run the gatekeeper":

1. Run: `find ~/.hermes/skills -name "SKILL.md" -exec wc -c {} + | sort -rn`
2. Cross-check against ~/.hermes/references/*.md, ~/.hermes/.env, ~/.hermes/SOUL.md
3. Report which files are over threshold

### After Creating/Editing a Skill

Whenever you create or edit a SKILL.md file:

1. Measure the new file size: `wc -c <path>/SKILL.md`
2. If > 18,000 chars:
   - Suggest splitting into multiple files (e.g., references/ directory within the skill)
   - Offer to condense filler text
   - Consider moving deep-dive content to `references/` sub-dir and trimming SKILL.md
3. If > 17,000 chars (but < 18,000):
   - Note it as "approaching threshold" in the response
   - Offer optional condense

### Condensing a File

To condense an oversized file:

1. Read the file content
2. Strip filler words: "It is important that you remember to..." → "Always..."
3. Remove redundant section headers or transitional text
4. Collapse examples into terse bullet points
5. Move detailed reference material to a linked reference file in the skill's directory
6. Re-measure and confirm under threshold

### Splitting a Skill

For skills that genuinely need more content than fits:

```
skill-name/
├── SKILL.md          # Core instructions (< 18k chars)
├── references/
│   ├── configs.md    # Configuration examples
│   ├── api.md        # Full API reference
│   └── examples.md   # Extended examples
└── templates/        # Template files
```

### Automated Nightly Audit (Cron)

Runs every night via cron to catch files that crept up during the day:

```bash
# Currently configured as:
#   Schedule: every night at 02:00 MT
#   Prompt: Run a file size audit on all SKILL.md files, .env, SOUL.md,
#           config.yaml, and reference files. Report any over 17,000 chars.
#   Deliver: origin (back to the conversation that set it up — usually Discord home)
```

To check or modify: `cronjob(action='list')` and find the `file-size-nightly-audit` job.

## Pitfalls

- **Don't strip useful comments** — some comments in SKILL.md are essential context. Only strip filler.
- **Don't split a skill that works fine** — if it's under threshold and the user is happy, leave it.
- **Watch for symlinks** — `~/.hermes/SOUL.md` is a symlink; resolve it before measuring.
- **Built-in skills are off-limits** unless the user explicitly asks. The hermes-agent shipped skills (in ~/.hermes/hermes-agent/skills/) are pinned/by the maintainers.
- **.env is sensitive** — do NOT show API key values in audit output. Only report character counts.
