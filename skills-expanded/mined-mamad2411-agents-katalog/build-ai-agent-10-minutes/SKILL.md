---
name: build-ai-agent-10-minutes
description: 9-step framework from @51ultron for building and running a personal AI agent with Claude Code in 10 minutes — from installation through context, memory, prompt refinement, skills, testing, multi-agent architecture, autopilot routines, and scaling. Distinct from claude-start-business (which covers launching a business); this skill covers building the Claude Code agent system itself.
---

# Build an AI Agent in 10 Minutes

Source: @51ultron
9 steps · build your personal Claude Code agent system

Run steps 1–5 once to set up your agent. Run step 6 continuously. Run steps 7–9 to go beyond a single agent.

---

## Step 1 — Install Claude Code

```
Install Claude Code and confirm it's working.

1. Install: npm install -g @anthropic/claude-code
2. Authenticate: claude login
3. Test: claude "Hello — tell me what you can do"

If on Mac: brew install claude-code
```

---

## Step 2 — Build Context (CLAUDE.md)

Create the foundational context file so your agent always knows who it's working with.

```
Create a CLAUDE.md file for this project that gives my agent permanent context.

Include:
1. WHO I AM — my role, my business, what I'm building
2. WHAT THIS PROJECT IS — one paragraph on the codebase/product
3. MY STACK — languages, frameworks, tools I use
4. MY PREFERENCES — coding style, naming conventions, output format
5. MY GOALS — what I'm optimising for (speed, quality, revenue, learning)
6. WHAT TO NEVER DO — my hard rules and non-negotiables
7. DEFAULT BEHAVIOURS — how to respond when uncertain

Make it specific enough that a new agent session reads CLAUDE.md and acts like we've been working together for months.
```

---

## Step 3 — Build Memory (Save Corrections)

Train your agent to get better over time by saving corrections as persistent memory.

```
I want my agent to remember corrections and preferences across sessions.

Create a system where:
1. Every time I correct a mistake, Claude saves the correction to memory/corrections.md
2. Every time I state a preference, Claude saves it to memory/preferences.md
3. At the start of each session, Claude reads both files

Help me:
a. Create memory/corrections.md and memory/preferences.md with headers
b. Add a rule to CLAUDE.md: "At session start, read memory/corrections.md and memory/preferences.md"
c. Add a rule: "When corrected, save the correction to memory/corrections.md with date"
```

---

## Step 4 — Refine Prompts (Iterative Prompting)

Use structured iteration to get dramatically better outputs.

```
Help me develop a better prompt for [task I keep asking about].

Current prompt I use: [paste your current prompt]
Current output quality: [describe what's wrong or missing]
What I actually want: [describe ideal output]

Using iterative prompting:
1. Analyse why my current prompt produces weak results
2. Identify the 3 most impactful things to change
3. Write an improved prompt
4. Show me the output of the improved prompt
5. Propose 2 further refinements I could test

Return: the best prompt version I can save and reuse.
```

---

## Step 5 — Build Skills (Create SKILL.md)

Package your most useful workflows as reusable skills.

```
Turn this workflow into a reusable Claude Code skill.

Workflow: [describe the thing you do repeatedly]
Inputs: [what information I always need to provide]
Output: [what I want produced]

Create .claude/skills/[skill-name]/SKILL.md with:
- YAML frontmatter: name and description (one sentence)
- Step-by-step prompt for executing this workflow
- Bracketed placeholders for variable inputs
- Usage examples

After creating the skill, show me how to invoke it.
```

---

## Step 6 — Test & Iterate

Continuously improve your agent through structured feedback.

```
Review the output of my last [task type] and give me a structured critique.

Score it 1–10 on:
1. Accuracy — is it correct?
2. Completeness — did it cover everything needed?
3. Format — is it in the right format for my use case?
4. Efficiency — was it produced without unnecessary back-and-forth?

For any score below 8:
- What specifically failed?
- What should I add to CLAUDE.md, memory/, or a skill to prevent this next time?

Return: a concrete list of system improvements to make right now.
```

---

## Step 7 — Build Agents (Multi-Agent Architecture)

Graduate from one agent to a coordinated team: Strategist → Builder → QA Gate.

```
Help me set up a 3-agent architecture for [project]:

STRATEGIST AGENT (Claude Opus)
- Role: architecture decisions, complex reasoning, strategy
- Trigger: I call /strategy before any high-level decision
- System prompt: "You are a strategic advisor. Think in systems, second-order effects, and long-term leverage. Never implement — only recommend."

BUILDER AGENT (Claude Sonnet)
- Role: code generation, implementation, execution
- Trigger: I call /build before any implementation request
- System prompt: "You are a senior engineer. Build it right the first time. Read CLAUDE.md before every task."

QA GATE (Claude Sonnet with critic prompt)
- Role: review all Builder output before it ships
- Trigger: auto-runs after every /build session
- Target: 95/100 quality score before output is accepted
- System prompt: "Review this output against the requirements. Score 1–100. Below 95, list every issue and return to Builder."

Create the CLAUDE.md entries and skill files for each agent role.
```

---

## Step 8 — Run on Autopilot (Claude Routines)

Schedule your agent to run recurring tasks without you.

```
Help me set up Claude Routines to automate [recurring task].

Task: [what needs to happen]
Frequency: [daily/weekly/on trigger]
Input: [what data the routine needs]
Output: [what it should produce or do]

Create:
1. The routine prompt (self-contained — no context assumed)
2. The cron expression for my schedule
3. The claude mcp command to register it as a routine
4. A check: how will I know if it ran and succeeded?

Make it idempotent — running twice should not cause problems.
```

---

## Step 9 — Scale & Deploy

Move from personal agent to a system that can serve others.

```
I want to scale my Claude Code agent system for [use case: team / product / service].

Help me:
1. DOCUMENT — write a setup guide so others can replicate my system
2. PARAMETERISE — identify every hardcoded personal detail that needs to become a variable
3. ONBOARD — create an onboarding prompt that sets up CLAUDE.md for a new user in 5 questions
4. HARDEN — identify the 3 ways this system could break and add guardrails
5. PACKAGE — what would it take to turn this into a Claude Code template others can clone?

Return a deployment checklist I can work through.
```

---

## Usage Guide

Run once (setup):
1. Step 1 — Install
2. Step 2 — CLAUDE.md context
3. Step 3 — Memory system
4. Step 5 — First skill

Run continuously:
- Step 4 — Refine prompts as you work
- Step 6 — Test and iterate every session

Scale up:
- Step 7 — Add multi-agent roles
- Step 8 — Automate with Routines
- Step 9 — Package for others

---

## Variant: Wealth Lab 6-step version

A shorter 6-step variant (Context → Memory → Skills → Agents → Automation) with different prompts, including the agent-team and autopilot prompts, is in `references/wealth-lab-6-step.md`. One-shot command: `/workflow-to-agent`.
