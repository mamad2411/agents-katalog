---
name: ai-assisted-engineering-discipline-2026
description: Disciplined AI-assisted engineering workflow based on 2026 best practices from senior practitioners. Covers spec-before-code planning, iterative chunking, context packaging, model selection, multi-agent CLI tools, human-in-the-loop verification, granular version control, and AI behavior customization. Use when designing agentic IDE features, training developers on AI collaboration, or building quality gates for AI-generated code.
---

# AI-Assisted Engineering Discipline 2026

## Overview

AI coding assistants became game-changers in 2025, but harnessing them effectively takes skill and structure. The best results come from applying classic software engineering discipline to AI collaborations—design before coding, write tests, use version control, maintain standards. These practices are even more important when an AI is writing half the code.

This skill provides the structured workflow for "AI-augmented software engineering" rather than "AI-automated software engineering." The human engineer remains the director; the AI is a powerful but over-confident pair programmer.

## When to Use

- Designing agentic IDE features for A-Coder
- Training Builder's Club members on AI-assisted development
- Setting team policies for human-AI collaboration boundaries
- Building quality gates and automation around AI-generated code
- Evaluating which AI coding tools to adopt

## Core Workflow

### 1. Start with a Clear Plan (Specs Before Code)

Do not throw wishes at the LLM. Begin by defining the problem and planning a solution.

**Process:**
1. Describe the idea to the LLM and ask it to iteratively ask questions until requirements and edge cases are fleshed out.
2. Compile into a comprehensive `spec.md` containing requirements, architecture decisions, data models, and testing strategy.
3. Feed the spec into a reasoning-capable model and prompt it to generate a project plan: break implementation into logical, bite-sized tasks or milestones.
4. Iterate on the plan—edit and ask the AI to critique or refine—until it is coherent and complete.
5. Only then proceed to coding.

**Why it matters:** Planning first forces both human and LLM onto the same page and prevents wasted cycles. As Les Orchard put it, it is like doing a "waterfall in 15 minutes."

### 2. Break Work into Small, Iterative Chunks

Scope management is everything. Feed the LLM manageable tasks, not the whole codebase at once.

**Rules:**
- Implement one function, fix one bug, add one feature at a time.
- After each chunk, test it, then move to the next.
- Carry forward context of what has been built and incrementally add to it.
- Use a structured "prompt plan" file containing a sequence of prompts for each task so tools like Cursor can execute them one by one.

**Why it matters:** LLMs do best with focused prompts. If you ask for too much in one go, the model gets confused or produces a "jumbled mess"—"like 10 devs worked on it without talking to each other."

### 3. Provide Extensive Context and Guidance

LLMs are only as good as the context you provide. Show them relevant code, docs, and constraints.

**Context packaging checklist:**
- High-level goals and invariants
- Examples of good solutions in the codebase
- Warnings about approaches to avoid
- Official docs or README for niche libraries or new APIs
- Project lint rules, style preferences, and technical constraints

**Tools:**
- `gitingest` or `repo2txt` to dump relevant codebase parts into a text file for the LLM
- Claude Projects mode to import an entire GitHub repo into context
- Cursor or Copilot auto-include open files
- MCP tools like Context7 for automated context retrieval

**Guidance techniques:**
- Precede code snippets with constraints: "Here is the current implementation of X. We need to extend it to do Y, but be careful not to break Z."
- Tell the AI what not to focus on if something is out of scope (saves tokens).

### 4. Choose the Right Model (and Use Multiple When Needed)

Not all coding LLMs are equal. Pick your tool with intention.

**Guidelines:**
- Use the newest "pro" tier models when possible—quality matters.
- If one model gets stuck or gives mediocre outputs, try another. Copy the same prompt into a different service.
- Each model has its own "personality." Pick the AI pair programmer whose vibe meshes with you.
- Do not hesitate to switch to a second model for code review after the first writes the code.

### 5. Leverage AI Coding Across the Lifecycle

**CLI agents:** Claude Code, OpenAI Codex CLI, Google Gemini CLI—chat directly in your project directory, read files, run tests, multi-step fix issues.

**Asynchronous agents:** Google Jules, GitHub Copilot Agent—clone your repo into a cloud VM, work on tasks in the background, then open a PR.

**Orchestration tools:** Conductor lets you run multiple agents in parallel on different tasks. Some engineers experiment with 3–4 agents at once on separate features.

**Important:** These tools are not infallible. Use them in a supervised way. Let them generate and run code, but keep an eye on each step, ready to intervene when something looks off.

### 6. Keep a Human in the Loop—Verify, Test, and Review Everything

Think of an LLM pair programmer as "over-confident and prone to mistakes" (Simon Willison). It writes code with complete conviction—including bugs or nonsense.

**Cardinal rules:**
- Never blindly trust LLM output. Treat every AI-generated snippet as if it came from a junior developer.
- Read through the code, run it, and test it.
- Weave testing into the workflow: generate a testing plan for each step, instruct the agent to run the test suite after implementing a task, and have it debug failures.
- Do code reviews—both manual and AI-assisted. Spawn a second AI session to critique code produced by the first.
- Only merge or ship code after you have understood it. If the AI generates something convoluted, ask it to add comments or rewrite it in simpler terms.

**Quality gates:**
- Automated tests run on every commit or PR
- Code style checks (ESLint, Prettier) enforced
- Staging deployment available for any new branch
- Include linter output in the prompt: "please address these issues"

### 7. Commit Often and Use Version Control as a Safety Net

Frequent commits are your save points. They let you undo AI missteps and understand changes.

**Habits:**
- Commit early and often—more than in normal hand-coding.
- After each small task or successful automated edit, make a git commit with a clear message.
- Use branches or git worktrees to isolate AI experiments.
- Scan recent commits to brief the AI (or yourself) on what changed.
- LLMs are good at parsing diffs and using `git bisect` to find where a bug was introduced.

### 8. Customize the AI's Behavior with Rules and Examples

You do not have to accept the AI's default style. Influence it heavily with guidelines.

**Techniques:**
- Maintain a `CLAUDE.md` or `GEMINI.md` file with process rules and preferences: coding style, lint rules, functions to avoid, functional vs. OOP preference.
- Use GitHub Copilot and Cursor custom instructions to configure global behavior for your project.
- Provide in-line examples of the output format or approach you want. LLMs are great at mimicry—show them one or two examples and they will continue in that vein.
- Add explicit rules: "If you are unsure about something or the codebase context is missing, ask for clarification rather than making up an answer."

## A-Tech Applications

### A-Coder (IDE)
- Built-in spec.md generation and project plan scaffolding
- One-click "chunked task" execution from plan files
- Automatic context packaging with gitingest/repo2txt integration
- Multi-model support with easy switching
- Granular commit suggestions after each agent edit
- Custom rules file (`.acoder-rules.md`) per project

### Be Practical (Playbooks)
- Chapter: "The Disciplined AI Engineer: A Workflow That Scales"
- Templates: spec.md, plan.md, prompt-plan.md
- Checklist: human-in-the-loop verification steps

### Builder's Club
- Workshop: "From Vibe Coding to Engineering Discipline"
- Shared rulesets and style guides for community projects
- AI-on-AI code review challenge

## Cross-References
- See `developer-experience-and-flow/agentic-coding-workflow` for foundational agentic coding patterns
- See `developer-experience-and-flow/orchestrator-engineer-mindset` for team transformation from implementer to orchestrator
- See `ai-agents-and-workflows/spec-driven-development-framework` for the OpenSpec technical implementation
- See `developer-experience-and-flow/vibe-coding-security-defense` for quality risks of undisciplined AI coding

## Source
Addy Osmani — "My LLM coding workflow going into 2026" (January 2026)
