---
name: business-brain
description: Implement the Business Brain pattern. Gives every agent skill access to your tone, audience, and positioning without bloating the context window. Use when asked for brand context, voice, or positioning, or when setting up a new project's brain.
version: 1.2.0
---

# Business Brain Pattern

This skill implements the "Business Brain Pattern" for AI coding assistants. It centralizes all shared business and brand knowledge in one location—the "brain"—and allows individual skills or agent queries to reference it selectively rather than duplicating it.

## The Problem

Loading full brand guides, audience profiles, and positioning documents into every skill or prompt bloats the context window. This increases token usage, diffuses the agent's attention from the actual task instructions, and creates a maintenance nightmare when brand guidelines change.

## The Solution

The Business Brain pattern keeps individual skill prompts lean. Each skill loads only the brain sections it actually uses. The brain is organized into modular files by topic.

## Usage

When tasked with retrieving brand context, writing on-brand copy, or answering questions about the project's audience:

1. **Check for a local brain:** Look for an `.agent/brain/` directory (or legacy `brain/`, `.claude/brain/`, `.gemini/brain/`) in the project workspace.
2. **Selective loading:** Use your file reading tools to load **only the specific files needed** for the task.
   - Example: A social media drafting task might only need `brand-voice.md` and `audience-profiles.md`.
   - Example: A technical spec task might only need `content-rules.md`.
3. **DO NOT** load the entire brain directory if only one piece of context is needed. Trust the modular structure.

## Initialization

If the user wants to set up a new Business Brain for their project, run the included scaffolding script to generate the template files:

```bash
bash ~/.agents/skills/business-brain/scripts/init-brain.sh
```
*(Path may vary depending on the agent environment, e.g., `~/.claude/skills/` or `~/.gemini/skills/`)*

This script creates an `.agent/brain/` directory with the following templates:
- `brand-voice.md`
- `audience-profiles.md`
- `positioning.md`
- `content-rules.md`

## Structure of the Brain

A well-built business brain isn't a data dump. It's structured and scannable:

### `brand-voice.md`
- Specify sentence length preferences.
- Define the register (first person, formal "we", conversational "I").
- List words/phrases to always use and never use.
- Describe the energy level.
- Include 2-3 sample paragraphs demonstrating the voice, and examples of off-brand writing.

### `audience-profiles.md`
- Define 2-4 primary audience segments.
- Job title/life situation.
- What they care about most and what they're skeptical of.
- Familiarity level with the topic.
- Language/framing that resonates.

### `positioning.md`
- What the company/product does.
- Who it's for.
- Why someone would choose it over alternatives.
- Explicitly state what you *do not* claim. Keep it focused (200-300 words).

### `content-rules.md`
- Structural preferences across output types.
- Header formatting conventions.
- List vs. prose preferences.
- Length guidelines.
- How to handle calls to action.

## Agentic OS Integration

If the current project root contains an `.agent/` directory, this skill MUST participate in the Agentic OS shared-memory model.

At the end of your execution, check for `.agent/state/last-run.json`. If it exists, append or update the file using its required schema to log your run. Ensure you capture your runtime (`agent_id`), `assigned_skill`, a concise `description`, `decision_log`, and `outcome`. Use `python3 ~/.agents/skills/heartbeat/scripts/heartbeat.py complete <task_id> ...` if completing a task from the queue.
