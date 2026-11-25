---
name: bootstrap
description: Project bootstrap wizard — turns any codebase into a fully planned, agent-ready project with coordination docs, debugging guidelines, and parallel execution infrastructure. Use when starting work on a new or unfamiliar project that needs structure.
---

# Project Bootstrap Wizard

You are launching the project bootstrap process. This turns any codebase into a fully planned, deliberated, agent-ready project with coordination docs, debugging guidelines, and parallel execution infrastructure.

---

## Agent Operating Rules (MANDATORY — apply to every phase)

Act like this is your only job:

1. If the task is even slightly unclear or broad → reply ONLY with 2–3 short yes/no or "pick A or B" questions. Nothing else. Stop until answered.
2. For any real work → first reply with a short numbered breakdown of steps and dependencies. Only then do the first step.
3. Use mini versions of yourself for sub-tasks: give each one a 1-sentence goal + exact output format required.
4. When anything fails or is wrong → say exactly what missing rule, check, limit or memory caused it → then add a new permanent rule to prevent it forever.
5. Keep searches tiny: max 3–5 results, very narrow query only.
6. Trim context hard: remove anything not needed right now.
7. End every reply with: Done/created: … | Check: … | Next: … or New rule to add: …

No chit-chat. Follow these rules exactly from now on.

---

## Phase 1: Discovery (Call-and-Response)

Ask the user these questions ONE AT A TIME using AskUserQuestion. Don't dump them all at once. Wait for each answer before proceeding.

### Question 1: Identity
"What is this project? Give me the elevator pitch — what does it do, who is it for, and what makes it different?"

### Question 2: Current State
"What's the current state? Is this greenfield, partially built, or production? What works and what's broken?"

### Question 3: Tech Stack
"What's the tech stack? (Languages, frameworks, databases, APIs, deployment targets)"

### Question 4: Goals
"What are the top 3 things you want to accomplish with this project in the next 2 weeks?"

### Question 5: Pain Points
"What's been frustrating you most? Where do you keep getting stuck or losing time?"

### Question 6: Related Projects
"Does this connect to other projects or services? List them with their locations."

---

## Phase 2: Codebase Exploration

After collecting answers, launch parallel Explore agents:

**Agent 1:** Explore the project structure — files, directories, package.json, configs, README, existing docs. Get the full picture of what exists.

**Agent 2:** Search for existing patterns — how is auth handled? What's the testing setup? Are there CI/CD configs? Existing CLAUDE.md or similar?

**Agent 3 (if related projects exist):** Map the ecosystem — what services are running, what ports, what credentials, what cron jobs.

---

## Phase 3: Deliberation

Launch a deliberation pass before generating documents. If a dedicated deliberation/review agent is available (e.g. a council, architect, or planning agent), use it. Otherwise, run this as a structured self-deliberation or with a general-purpose agent:

"We are deliberating on a new project. Here is what we know:
[Insert all discovery answers + exploration results]

Weigh in on:
1. What is the RIGHT first thing to build? Not the most exciting — the most foundational.
2. What are the biggest risks to this project succeeding?
3. Where should we use sub-agents vs do things directly?
4. What anti-patterns should we watch for given the tech stack and goals?
5. How does this project serve the user's broader goals?"

---

## Phase 4: Generate Project Documents

Based on discovery + exploration + deliberation, create these files:

### 4a: PROJECT_COORDINATION.md
Single source of truth with:
- Project status dashboard (table format)
- Active sub-agents tracker
- Cross-project dependencies (if any)
- Today's priority
- Key file locations
- Lessons/anti-patterns specific to this project

### 4b: CLAUDE.md additions
Add to existing CLAUDE.md (or create one):
- Project ecosystem map (all related projects with paths)
- Debugging guidelines specific to this tech stack
- Automation rules (build commands, test commands, lint commands)
- Anti-patterns from deliberation
- File organization conventions found during exploration

### 4c: Agent Roster
Document which agents are useful for this project:
- Which tasks → which agent type
- Any custom agents needed?
- What skills/slash commands apply?

### 4d: Execution Plan
Phased plan with:
- Week 1 / Week 2 / Week 3 breakdown
- What blocks what (dependency graph)
- Success criteria for each phase
- Verification steps (how to test each phase)

---

## Phase 5: Launch

After documents are created:

1. Set up TodoWrite with the first batch of tasks
2. Launch 2-3 parallel agents for the first actions
3. Report back to user: "Here's what's running, here's what's next"

---

## Key Principles

- **Call-and-response, not monologue.** Ask one question, get the answer, then ask the next. Don't overwhelm.
- **Explore before opining.** Read the code before suggesting architecture.
- **Deliberation is not optional.** Every project gets a risk/direction pass before documents are written.
- **Anti-patterns are project-specific.** Don't just copy generic rules — derive them from the actual codebase and user's pain points.
- **Parallel agents from the start.** The bootstrap should end with agents already working, not with a document that says "next steps."
- **The user's goals override everything.** If they said "I want X done in 2 weeks," plan for X in 2 weeks, not for a perfect architecture that takes 3 months.

---

## Example Output Structure

After bootstrap completes, the project should have:

```
project-root/
├── CLAUDE.md                  (updated with ecosystem, guidelines, anti-patterns)
├── PROJECT_COORDINATION.md    (status dashboard / single source of truth)
├── .claude/
│   └── agents/                (any custom agents created)
├── tasks/
│   └── todo.md                (if applicable)
└── [existing project files unchanged]
```

And in the conversation:
- TodoWrite populated with first tasks
- 2-3 background agents already working
- User knows exactly what's happening and what's next

---

## When NOT to Bootstrap

- Single-file scripts or utilities (just build it)
- Bug fixes where the scope is already clear
- Tasks the user has already fully specified with exact instructions
- Projects where the user explicitly says "just start coding"

Bootstrap is for when you need clarity, not when you already have it.

---

## Installation

Drop this file at `~/.claude/skills/bootstrap/SKILL.md` (global) or `<project>/.claude/skills/bootstrap/SKILL.md` (per-project), then invoke with `/bootstrap` in Claude Code.
