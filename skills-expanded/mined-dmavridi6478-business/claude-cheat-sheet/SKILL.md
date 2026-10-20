---
name: claude-cheat-sheet
description: Quick reference for getting more out of Claude — prompting techniques (zero/one/few-shot, role-based prompting, the role+examples+step-by-step combo), structured prompt frameworks (the 5 C's, SEED, PEEL), what Skills/Hooks/MCP/Projects/Artifacts actually are and how they differ, and a short list of durable pro tips. Use when asked how to write a better prompt, what a Claude concept (skill/hook/MCP/artifact/project) means, or for a general "how do I use Claude well" reference.
---

# Claude Cheat Sheet

Source: prompted by reviewing a social-media "Claude AI Cheat Sheet" infographic that turned out to be unreliable — garbled text throughout, wrong model names, a non-Anthropic URL presented as an official courses link, and mangled tool names in its "tools to use with Claude" table. None of that is repeated here. This skill is written fresh from first-hand knowledge of how these features actually work, kept to the parts that are genuinely stable and checkable rather than product specifics (model lineups, exact UI labels) that change too often to belong in a static reference.

## Prompting techniques

**Shot count** — how many examples a prompt includes:
- **Zero-shot**: just the instruction ("Write 5 CTAs about [topic]"). Fine for simple, well-understood tasks.
- **One-shot**: instruction + one example of the desired output. Useful when format matters more than content.
- **Few-shot**: instruction + 2+ examples, ideally varied ones. More examples generally improve output consistency — but examples should show the *range* of acceptable outputs, not near-duplicates of each other, or the model over-fits to one pattern.

**Prompt shapes** — pick based on what you actually need:
- **Open-ended**: broad exploration when you don't know the shape of the answer yet ("what are the risks here?").
- **Multiple-choice / constrained**: forces a specific, comparable output ("pick the best of these 3 options and say why").
- **Fill-in-the-template**: give the exact structure and have Claude complete it — best when downstream tooling expects a specific format.
- **Comparative**: "compare X vs. Y" — forces explicit trade-offs instead of a one-sided pitch.
- **Scenario / role-play**: "you are reviewing this as a skeptical investor" — useful for stress-testing, not just persona flavor.
- **Instructional**: "explain how to do X" — optimizes for a process, not just an answer.
- **Feedback / critique**: "review this and point out what's wrong" — asking for critique directly gets sharper output than asking for a rewrite and hoping it's better.

**Role-based prompting**: "act as [role]" primes the vocabulary, priorities, and blind spots of that role — most useful when paired with a concrete task and output format, not on its own. A role with no task ("act as a marketer") gets generic output; a role with a specific task and format ("act as a performance marketer, audit this landing page, output a prioritized punch list") gets usable output.

**The reliable combo**: **role + examples + explicit step-by-step instructions** together outperform any one of the three alone. The role sets the lens, the examples set the format/tone, and the step-by-step breakdown keeps a multi-part task from collapsing into a single shallow pass.

## Structured prompt frameworks

Added from a reviewed "How to Prompt AI" infographic — named templates
for when a prompt needs more structure than a single instruction, without
reinventing the shape each time.

**The 5 C's** — the checklist every strong prompt should pass: **C**lear
(say exactly what's needed), **C**ontextual (add relevant background),
**C**omplete (state constraints up front, not as a follow-up correction),
**C**onversational (delegate like briefing a colleague, not issuing a
command to a machine), **C**haracter (assign a role or voice when tone
matters).

**SEED** — for task-execution prompts: **S**cenario ("here is the
situation: [context/data]"), **E**xpertise ("act as a [role]"), **E**xecute
("perform [analysis or task]"), **D**eliverable ("output as [format]").

**PEEL** — for prompts that need a worked example to anchor tone/format:
**P**ersona ("act as a [role]"), **E**xplain ("your task is to
[deliverable]"), **E**xamples ("here are 1-2 style references [links or
snippets]"), **L**imitations ("must follow [length, tone, format,
rules]").

Six advanced techniques from the same source are installed as their own
commands (each takes the task as `$ARGUMENTS`) rather than duplicated here
as text: `/plan-then-answer` (plan silently, output only the final
answer), `/reflect-then-revise` (draft, self-score 1–5, fix anything
under 4), `/self-critique-pass` (three internal drafts, return the best
with why), `/evidence-first-grounding` (answer only from an attached
source, flag anything unverifiable), `/assumptions-and-gaps` (list
assumptions/missing info before answering, state the safest default for
anything critical), `/contrast-few-shot` (match a Good example's traits,
avoid a Not-Good example's).

## Skills, Hooks, MCP, Projects, and Artifacts — what each actually is

These get conflated a lot; they solve different problems:

- **Skills** — a `SKILL.md` file (name + description in frontmatter, instructions in the body) that Claude loads automatically when the description matches what you're doing. Background knowledge/procedure, not something you invoke by name. This repo's `.claude/skills/` is full of examples.
- **Slash commands** — the opposite of a skill: explicitly invoked by typing `/name`, not auto-loaded. See `.claude/commands/` in this repo and the distinction called out in the main README.
- **Hooks** — shell commands the Claude Code harness runs automatically at specific lifecycle points (configured in `settings.json`), not something Claude decides to run. The real lifecycle points are `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Notification`, `Stop`, `SubagentStop`, `PreCompact`, and `SessionEnd` — each fires on an actual event (e.g. `PreToolUse` before a tool call, matchable to specific tools), not on vague categories.
- **MCP (Model Context Protocol)** — an open protocol for connecting an AI application to external tools/data sources through one standard interface, instead of a custom integration per tool. A "connector" (Slack, Notion, Google Drive, etc.) is an MCP server someone already built; you can also point Claude at a custom/self-hosted one. See the `mcp-integration-scout` agent in this repo for checking what's actually connected before assuming.
- **Projects** — a persistent workspace that groups related conversations, holds shared reference files, and can carry custom instructions specific to that context — useful when the same background material (a client's brand voice, a codebase, a research corpus) applies across many conversations.
- **Artifacts** — a distinct, renderable output (code, a document, an interactive React component, a diagram) that lives outside the linear chat flow, can be iterated on directly, and can be shared independent of the conversation that produced it. Not every response needs to be an artifact — reach for one when the output is something the user will look at, edit, or reuse as a standalone thing, not just read once.

## Pro tips that hold up

- Attach real reference material (brand voice doc, prior work, actual data) instead of describing it from memory in the prompt — a Project's file upload or a pasted example beats a paragraph of description every time.
- Ask for a self-critique pass explicitly ("now find the 3 weakest parts of what you just wrote") — Claude reviewing its own prior output on request tends to catch real issues that a first pass alone misses.
- For a multi-part or structured prompt, use explicit section markers (headers, or tags like `<context>`/`<task>`) rather than one dense paragraph — it measurably reduces the model dropping or blending instructions.
- In Claude Code specifically: `CLAUDE.md` is project memory that loads automatically every session — put durable, project-specific instructions there, not one-off task details.

## Related skills in this repo

- **mcp-integration-scout** (agent): does the live version of the MCP section above — checks what's actually connected rather than describing the concept.
- **capability-scout** (agent): finds which of this repo's own skills matches a task, once you know what a skill is from the section above.
- **task-loop-runner**, **multi-agent-orchestrator**, **agentic-researcher**, **memory-keeper** (agents): concrete implementations of agent patterns, if this cheat sheet's overview is the "what," those are the "how."
