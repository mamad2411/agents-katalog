---
name: agents-md-setup
description: Create or improve AGENTS.md or CLAUDE.md when the user wants persistent instructions, better project context, or an AI that understands how they work.
---

# AGENTS.md Setup

## Two Modes

- **Create:** no instruction file exists yet. Run the interview below and write it.
- **Optimize:** a file already exists. Read it first, then audit it: flag lines that are generic (any AI does this by default), missing boundaries, stale facts, and gaps the interview questions below would fill. Propose the edits, apply on approval, and keep what already works.

## The Job

Most people use powerful AI agents that know nothing about them. Every session starts from zero: wrong tone, wrong assumptions, wrong priorities, re-explaining the same context. The fix is a written working context: a short instruction file the agent reads before it starts working.

This skill interviews the user, writes that file, installs it where their agent reads it, and verifies it works.

## Step 1: Find Out Where It Will Live

Ask which AI tool they mainly use, then target the right file:

| Tool | File the agent reads |
|---|---|
| Claude Code | `CLAUDE.md` in the project folder, or `~/.claude/CLAUDE.md` for everything |
| Codex | `AGENTS.md` in the project folder, or `~/.codex/AGENTS.md` for everything |
| ChatGPT | Custom instructions (settings), pasted text |
| Claude apps | Project instructions or preferences, pasted text |
| Other or several | Write one canonical Markdown file; the user pastes or links it per tool |

If they use more than one tool, write one source file and produce a copy or paste-block for each surface. Do not invent file locations for tools you are not sure about; say what you verified and what they should check in that tool's docs.

Before writing, separate the scope:

| Scope | Put here | Keep out |
|---|---|---|
| Global | Identity, communication preferences, common tools, standing approval boundaries, and rules that apply across work | Project commands, temporary priorities, current build status, or facts that belong to one repository |
| Project | Purpose, audience, stack, commands, file conventions, verification steps, project-specific constraints, and local approval boundaries | Unrelated personal context or preferences already covered globally |

If the user needs both, propose a global file and a project file rather than duplicating everything. Explain which facts belong in each before writing.

## Step 2: The Interview

Ask in two short rounds, not one giant questionnaire. Skip anything already known from the conversation or workspace.

For a global file, ask:

1. What do you do, in one or two sentences? (role, business, or job)
2. Who do you do it for? (clients, audience, employer, yourself)
3. What are the two or three tasks you'll use AI for most?
4. How should the AI talk to you? (short and direct, detailed, casual, formal; anything that annoys you)
5. What should it always know? (tools you use, constraints, working hours, budget realities, quality bars)
6. What must it never do without asking? (send things, spend money, delete things, contact people, publish)
7. Any recurring formats? (how you like documents, reports, code, or posts structured)

For a project file, ask only what the workspace does not already show:

1. What is this project for, and who is it for?
2. What commands, tools, files, or workflows should the agent use?
3. What counts as finished and how should it be verified?
4. What project-specific actions require approval?
5. Which current facts are durable enough to record, and which are temporary status that should stay out?

If an answer is vague, reflect it back sharper and confirm: "So: you run a bookkeeping practice, mostly write client emails and monthly reports, and you want short answers unless you ask for detail. Right?"

## Step 3: Write the File

Structure the file in this order, using the user's own words wherever possible:

```markdown
# Working with [name]

## Who I am
[2-4 lines: role, who they serve, what they're building]

## What I use AI for
[the 2-3 main jobs, each one line]

## How to work with me
[tone, length, format preferences, pet peeves]

## Always know
[tools, constraints, standing facts the AI should never re-ask]

## Never without asking
[the hard boundaries: sending, spending, deleting, publishing, contacting]
```

For a project file, replace the personal sections with: Project purpose, how this project works, commands and tools, quality and verification, durable project facts, and approval boundaries.

Rules:

- Keep it under 60 lines. Agents follow short files better than long ones.
- Every line must be something the AI would otherwise get wrong. Cut anything generic ("be helpful") that any AI does by default.
- Keep global preferences and project facts in their correct scope. Do not copy the same context into both files without a concrete reason.
- Boundaries go in as absolutes ("never send an email without showing me first"), not preferences.
- No secrets: no passwords, API keys, or account numbers in this file, ever. If the user offers them, refuse and explain the file is plain text.

## Step 4: Install and Verify

1. Save the file in the right location for their tool (or give the paste-block for settings-based tools).
2. Verify with a live test: have the user start a fresh session and ask something the file should change, for example "draft a reply to a client who's late paying." Check the response uses their tone, their constraints, and their boundaries.
3. If the test misses, fix the file, not the prompt: the line the agent ignored is usually too vague or buried. Sharpen it and retest.

## Step 5: Teach the Maintenance Habit

End with this advice, in plain words: the file is alive. Whenever the AI gets something wrong twice, that is a missing line. Add one sentence to the file instead of correcting the same thing in every chat.

## Capability Contract

- Reads: only what the user tells it and files the user points to.
- Writes: creates or edits the instruction file, with the user's confirmation of the location, only where the host supports file writes. On chat-only surfaces, delivers the finished file as a copy-paste block.
- Network: none.
- External actions: none.

## Boundaries

- Never overwrite an existing CLAUDE.md or AGENTS.md without showing the user what is already there and merging deliberately.
- Never put credentials or private third-party information (client names with sensitive details) in the file without flagging that anyone with file access can read it.
- If the user's tool is not one this skill knows, say so and produce the canonical Markdown version rather than guessing that tool's file conventions.

## Completion Checklist

- The file exists in the verified location (or the paste-block is delivered)
- It is under 60 lines and every line changes agent behavior
- Hard boundaries are stated as absolutes
- A fresh-session live test passed
- The user knows the one-sentence maintenance habit
