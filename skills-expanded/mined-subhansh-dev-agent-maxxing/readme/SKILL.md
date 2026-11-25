<div align="center">

#  Agent Maxxing

> **95+ production-ready skills, 19 UI components, and 7 system prompts extracted from the world's best AI agents.** Drop them into any agent — Claude Code, Codex, Cursor, OpenCode — and it instantly becomes elite.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-95+-orange.svg)](#-skills-roster)
[![Components](https://img.shields.io/badge/Components-19-blue.svg)](#-ui-components)
[![System Prompts](https://img.shields.io/badge/System%20Prompts-7-purple.svg)](#-system-prompts)
[![Format](https://img.shields.io/badge/Format-Markdown-white.svg)](#-skills-roster)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)

---

**Think of it as:** Giving your AI agent a brain transplant — it inherits the engineering judgment of GPT-5.5, the reasoning of Claude Fable 5, the frontend taste of Claude Design, and the tool orchestration of Gemini CLI.

</div>

---

## ⚡ Quick Start

### Step 1: Clone the repo

```bash
git clone https://github.com/subhansh-dev/agent-maxxing.git
```

### Step 2: Install for your agent

**Claude Code** (user-wide):
```bash
cp -r agent-maxxing ~/.claude/skills/agent-maxxing
```

**Claude Code** (project-scoped):
```bash
cp -r agent-maxxing .claude/skills/agent-maxxing
```

**Codex CLI** (user-wide):
```bash
cp -r agent-maxxing ~/.codex/skills/agent-maxxing
```

**OpenCode** (user-wide):
```bash
cp -r agent-maxxing ~/.opencode/skills/agent-maxxing
```

**Cursor** (project-scoped):
```bash
cp -r agent-maxxing .cursor/skills/agent-maxxing
```

**Continue** (project-scoped):
```bash
cp -r agent-maxxing .continue/skills/agent-maxxing
```

**Kilo Code** (project-scoped):
```bash
cp -r agent-maxxing .kilocode/skills/agent-maxxing
```

### Step 3: Restart your agent

The agent auto-discovers all `.md` files with YAML frontmatter on next session.

### Step 4: Use the skills

Just describe what you want. The agent picks the right skill automatically:

```
"Build a landing page with glassmorphism"
→ Loads frontend-design + glass-card

"Write a blog post that sounds human"
→ Loads humanizer

"Create a diagram of the system architecture"
→ Loads diagram-maker

"Review my code for security issues"
→ Loads security-review
```

### Step 5: Fine-Tune Your Agent

This is where the magic happens. Your agent can **read these skills and transform its own behavior** — not through weight training, but through context injection. When an agent reads a skill file, it internalizes the patterns for that session and applies them to every task.

**What fine-tuning does:**
- Teaches your agent to avoid AI slop (no "Great question!", no purple gradients)
- Injects engineering judgment from GPT-5.5 and Claude Fable 5
- Adds 8-angle code review methodology
- Installs security review patterns
- Forces the execution protocol (solve it, don't ask about it)
- Makes the agent sound human, not like a press release

**How to do it:**

Add this prompt to your agent's system prompt, `CLAUDE.md`, or `AGENTS.md`:

```markdown
## Self-Fine-Tune Protocol

Before responding to any task, read these files in order:
1. FINE-TUNE-AGENT.md — master instructions
2. system-prompts/01-agent-core-personality.md — personality and tone
3. system-prompts/02-coding-excellence.md — engineering patterns
4. system-prompts/03-reasoning-planning.md — thinking patterns
5. engineering/anti-patterns.md — what to avoid
6. engineering/execution-protocol.md — how to operate
7. content/writing-style.md — how to communicate

After reading, apply these patterns to every response.
Check anti-patterns before shipping code.
Follow the 10 Golden Rules.
Sound human, not like a bot.
```

**Or use the master file:** [`FINE-TUNE-AGENT.md`(FINE-TUNE-AGENT/SKILL.md) — comprehensive step-by-step guide that walks your agent through every skill category.

---

## 🔥 What Makes This Different

| | Agent Maxxing | Generic Skill Packs |
|---|---|---|
| **Source** | Extracted from Claude Fable 5, GPT-5.5, Gemini CLI, Claude Code | Community-written prompts |
| **Depth** | 95+ skills covering engineering, design, writing, security | 5-10 surface-level tips |
| **Components** | 19 production-ready UI patterns with CSS | None |
| **System Prompts** | 7 fine-tuned personality modules | None |
| **Anti-Slop** | Dedicated anti-patterns + writing style guide | "Be helpful" |
| **Compatibility** | Works with 60+ agents via Agent Skills spec | Vendor-locked |

---

## 🛠️ Skills Roster

### 💻 Engineering Division

Building things that work.

| Skill | Description |
|-------|-------------|
| [Execution Protocol](engineering/execution-protocol/SKILL.md) | Solve it don't ask about it — the problem-solving chain |
| [Anti-Patterns](engineering/anti-patterns/SKILL.md) | Code, design, writing anti-patterns to avoid |
| [Code Review Checklist](engineering/code-review-checklist/SKILL.md) | Ship-ready review: correctness, security, performance |
| [Deep Code Review](engineering/deep-code-review/SKILL.md) | 8-angle methodology from Claude Code bundled skills |
| [Security Review](engineering/security-review/SKILL.md) | Senior security engineer review with false-positive filtering |
| [Code Simplify](engineering/code-simplify/SKILL.md) | 4-angle cleanup: reuse, simplify, efficiency, altitude |
| [Runtime Verify](engineering/runtime-verify/SKILL.md) | Run the app don't test it — observation is evidence |
| [Debugging Patterns](engineering/debugging-patterns/SKILL.md) | Systematic methodology, common bug categories |
| [Testing Patterns](engineering/testing-patterns/SKILL.md) | What to test, test structure, test pyramid |
| [API Design](engineering/api-design/SKILL.md) | REST patterns, naming, status codes, pagination |
| [Database Patterns](engineering/database-patterns/SKILL.md) | Schema design, indexing, migrations, query optimization |
| [Performance Patterns](engineering/performance-patterns/SKILL.md) | Lazy loading, caching, memoization, optimization |
| [Code Generator](engineering/05-CODE-GENERATOR/SKILL.md) | Generate code with best practices |
| [Distill](engineering/06-DISTILL/SKILL.md) | Strip to essence by removing complexity |
| [Extract](engineering/07-EXTRACT/SKILL.md) | Extract reusable components and tokens |
| [Harden](engineering/10-HARDEN/SKILL.md) | Error handling, edge cases, resilience |
| [Normalize](engineering/12-NORMALIZE/SKILL.md) | Match your design system |
| [Optimize](engineering/14-OPTIMIZE/SKILL.md) | Loading, rendering, bundle size |
| [Overdrive](engineering/15-OVERDRIVE/SKILL.md) | Push past conventional limits |
| [Quieter](engineering/16-QUIETER/SKILL.md) | Tone down overly bold designs |
| [Node Debugger](engineering/25-NODE-INSPECT-DEBUGGER/SKILL.md) | Node.js debugging with inspect protocol |
| [Python Debugger](engineering/26-PYTHON-DEBUGPY/SKILL.md) | Python remote debugging with debugpy |

### 🎨 Frontend & Design Division

Making it beautiful, usable, and distinctly human.

| Skill | Description |
|-------|-------------|
| [Frontend Design](frontend-design/01-FRONTEND-DESIGN/SKILL.md) | Premium UI patterns, glassmorphism, anti-slop rules |
| [Animate](frontend-design/02-ANIMATE/SKILL.md) | Motion design, micro-interactions, timing |
| [Colorize](frontend-design/03-COLORIZE/SKILL.md) | Color theory, palettes, strategic color |
| [Typeset](frontend-design/04-TYPESET/SKILL.md) | Typography systems, font pairing, hierarchy |
| [Bolder](frontend-design/05-BOLDER/SKILL.md) | Amplify safe designs to make them interesting |
| [Delight](frontend-design/06-DELIGHT/SKILL.md) | Moments of joy and personality |
| [Polish](frontend-design/07-POLISH/SKILL.md) | Final quality pass — alignment, spacing |
| [Critique](frontend-design/08-CRITIQUE/SKILL.md) | Evaluate design from UX perspective |
| [Onboard](frontend-design/13-ONBOARD/SKILL.md) | Onboarding flows and first-time experiences |
| [Artifact Design](frontend-design/artifact-design/SKILL.md) | Deliberate design choices, avoid AI-generated looks |
| [Typography](frontend-design/typography/SKILL.md) | Font pairing, scale, typographic systems |
| [Color & Contrast](frontend-design/color-and-contrast/SKILL.md) | Color theory and accessibility |
| [Interaction Design](frontend-design/interaction-design/SKILL.md) | Micro-interactions, hover states |
| [Motion Design](frontend-design/motion-design/SKILL.md) | Timing, easing, enter/exit patterns |
| [Responsive Design](frontend-design/responsive-design/SKILL.md) | Breakpoints, fluid layouts, mobile-first |
| [Spatial Design](frontend-design/spatial-design/SKILL.md) | Layout, spacing, visual rhythm |

### 📝 Content & Writing Division

Sound human, not like a press release.

| Skill | Description |
|-------|-------------|
| [Humanizer](content/09-HUMANIZER/SKILL.md) | Strip AI-isms, add real voice |
| [Clarify](content/04-CLARIFY/SKILL.md) | Improve unclear UX copy and errors |
| [Writing Style](content/writing-style/SKILL.md) | How to sound human — voice, rhythm, what to avoid |
| [UX Writing](frontend-design/ux-writing/SKILL.md) | Microcopy, error messages, clear interface text |

### 🖼️ Visual Division

Diagrams, memes, and canvas art.

| Skill | Description |
|-------|-------------|
| [Diagram Maker](visual/10-DIAGRAM-MAKER/SKILL.md) | SVG, HTML, or Excalidraw diagrams |
| [Meme Maker](visual/11-MEME-MAKER/SKILL.md) | Generate memes from curated templates |
| [Canvas](visual/12-CANVAS/SKILL.md) | Canvas-based visual creation |
| [Excalidraw Patterns](visual/excalidraw-patterns/SKILL.md) | Hand-drawn diagram patterns |
| [SVG Template](visual/svg-template/SKILL.md) | SVG generation templates |

### 🧠 Agent Meta & Self-Improvement

Make your agent better over time.

| Skill | Description |
|-------|-------------|
| [Self-Improvement](agent-meta/17-SELF-IMPROVEMENT/SKILL.md) | Agent learning loops and evolution |
| [Skill Creator](agent-meta/18-SKILL-CREATOR/SKILL.md) | Create new agent skills from scratch |
| [Skill Vetter](agent-meta/19-SKILL-VETTER/SKILL.md) | Validate and review skills |
| [Find Skills](agent-meta/08-FIND-SKILLS/SKILL.md) | Search and discover available skills |
| [GitHub](agent-meta/09-GITHUB/SKILL.md) | GitHub integration and repo management |
| [Teach Impeccable](agent-meta/24-TEACH-IMPECCABLE/SKILL.md) | Persistent design guidelines setup |
| [Init Project](agent-meta/init-project/SKILL.md) | Create CLAUDE.md by analyzing codebase |

### ⚙️ Workflows & Orchestration

How to manage complex tasks.

| Skill | Description |
|-------|-------------|
| [Batch Orchestration](workflows/batch-orchestration/SKILL.md) | Parallel work with isolated worktrees |
| [Git Workflow](workflows/git-workflow/SKILL.md) | Commits, branching, PRs, conflict resolution |
| [Taskflow](workflows/22-TASKFLOW/SKILL.md) | Structured task management |
| [Taskflow Inbox Triage](workflows/23-TASKFLOW-INBOX-TRIAGE/SKILL.md) | Inbox triage and priority |
| [Spike](workflows/21-SPIKE/SKILL.md) | Quick prototyping and exploration |
| [Healthcheck](workflows/11-HEALTHCHECK/SKILL.md) | System health monitoring |

### 🔄 Adaptation & Learning

Cross-platform and responsive patterns.

| Skill | Description |
|-------|-------------|
| [Adapt](adaptation/01-ADAPT/SKILL.md) | Cross-screen, cross-device adaptation |
| [Arrange](adaptation/02-ARRANGE/SKILL.md) | Layout, spacing, visual rhythm |
| [Audit](adaptation/03-AUDIT/SKILL.md) | Accessibility, performance, theming audit |

---

## 🧩 UI Components

19 production-ready component patterns with CSS. Drop into any project.

| Component | Description |
|-----------|-------------|
| [Glass Card](components/glass-card/SKILL.md) | Glassmorphism with backdrop blur and specular tracking |
| [Gradient Button](components/gradient-button/SKILL.md) | Buttons with hover glow and press feedback |
| [Animated Input](components/animated-input/SKILL.md) | Floating labels and focus animations |
| [Modal Dialog](components/modal-dialog/SKILL.md) | Backdrop blur, spring animation, focus trap |
| [Loading Skeleton](components/loading-skeleton/SKILL.md) | Shimmer placeholders for content |
| [Toast Notification](components/toast-notification/SKILL.md) | Slide-in, auto-dismiss, stacking |
| [Navbar](components/navbar/SKILL.md) | Glass effect, scroll-aware styling |
| [Data Table](components/data-table/SKILL.md) | Sorting, striped rows, hover states |
| [Tooltip](components/tooltip/SKILL.md) | Arrow, delays, smart positioning |
| [Tabs](components/tabs/SKILL.md) | Animated indicator, keyboard nav |
| [Dropdown](components/dropdown/SKILL.md) | Glass styling, keyboard navigation |
| [Avatar](components/avatar/SKILL.md) | Status indicators, initials fallback |
| [Progress Bar](components/progress-bar/SKILL.md) | Animated, gradient, multi-step |
| [Badge & Tag](components/badge-tag/SKILL.md) | Multiple color variants |
| [Toggle Switch](components/toggle-switch/SKILL.md) | Smooth animation, accessible |
| [Accordion](components/accordion/SKILL.md) | Expandable sections, smooth height |
| [Breadcrumb](components/breadcrumb/SKILL.md) | Navigation with separators |
| [Pagination](components/pagination/SKILL.md) | Page numbers, prev/next |

---

## 🧠 System Prompts

Extracted from the leaked system prompts of Claude Fable 5, GPT-5.5 Codex, Gemini CLI, Claude Code, and Cursor. Intelligently curated — not dumped.

| File | Source | What It Improves |
|------|--------|------------------|
| [Fine-Tune](system-prompts/00-FINE-TUNE/SKILL.md) | Master guide | How to use all prompts |
| [Fable 5 Base](system-prompts/01-agent-core-personality/SKILL.md) | Claude Fable 5 | Personality, memory, tone, refusal handling |
| [Coding Excellence](system-prompts/02-coding-excellence/SKILL.md) | Codex GPT-5.5 + Claude Code | Engineering judgment, code quality |
| [Reasoning & Planning](system-prompts/03-reasoning-planning/SKILL.md) | Codex Plan Mode | 3-phase planning, decision-making |
| [Frontend Mastery](system-prompts/04-frontend-mastery/SKILL.md) | Codex GPT-5.5 + Claude Design | UI/UX rules, anti-AI-slop |
| [Agent Orchestration](system-prompts/05-agent-orchestration/SKILL.md) | Claude Code + Gemini CLI | Tool usage, sub-agents, delegation |
| [Tone & Communication](system-prompts/06-tone-communication/SKILL.md) | Fable 5 + Codex + Cursor | How to talk and present |

---

## 📂 File Structure

```
agent-maxxing/
├── FINE-TUNE-AGENT/          ← Start here — master instruction file
│   └── SKILL.md
├── README.md                 ← You are here
├── LICENSE                   ← MIT
│
├── frontend-design/          (16) ← UI, CSS, motion, typography
│   ├── 01-FRONTEND-DESIGN/SKILL.md
│   ├── 02-ANIMATE/SKILL.md
│   └── ...
├── content/                  (3)  ← Writing, humanization
├── visual/                   (6)  ← Diagrams, memes, canvas
├── engineering/              (22) ← Code, security, testing, debugging
├── agent-meta/               (8)  ← Self-improvement, skill creation
├── workflows/                (6)  ← Task management, git, orchestration
├── adaptation/               (3)  ← Cross-platform, responsive
├── components/               (19) ← Reusable UI patterns
└── system-prompts/           (7)  ← Extracted from top AI agents
```

Each skill lives in its own folder as `SKILL.md` — this is the standard naming convention that OpenCode, Claude Code, and other agents use for skill discovery.

**9 folders. 95+ SKILL.md files. Zero dependencies. Just markdown.**

---

## 🔌 Integration Guide

### How Skills Work

Each skill is a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: skill-name
description: One-line description
---

# Skill Name

## When to Use
- Trigger condition 1
- Trigger condition 2

## Instructions
1. Step one
2. Step two

## Rules
- Rule 1
- Rule 2
```

When your agent reads this file, it knows:
- **When** to activate this skill (from `description` and "When to Use")
- **What** to do (from "Instructions")
- **What not** to do (from "Rules")

### Permanent Integration (Recommended)

**If your agent loads `CLAUDE.md` on every session (OpenCode, MimoCode, Claude Code, Cursor, or any agent that reads a config/rules file at startup) — add the integration block there. This is the most reliable method. The agent will know about agent-maxxing on EVERY prompt, no plugin needed.**

Add this to `CLAUDE.md`, `AGENTS.md`, or your agent's equivalent config file:

```markdown
## Agent Maxxing Skills

You have access to 95+ skills at `~/.claude/skills/agent-maxxing/` (adjust path for your agent).

When working on any task, check if a relevant skill exists:

### Frontend Work
- frontend-design/01-FRONTEND-DESIGN/SKILL.md — premium UI, glassmorphism, anti-slop
- frontend-design/02-ANIMATE/SKILL.md — motion design, micro-interactions
- frontend-design/04-TYPESET/SKILL.md — typography systems
- frontend-design/artifact-design/SKILL.md — deliberate design choices

### Code Work
- engineering/execution-protocol/SKILL.md — solve it don't ask about it
- engineering/deep-code-review/SKILL.md — 8-angle code review
- engineering/security-review/SKILL.md — security audit
- engineering/debugging-patterns/SKILL.md — systematic debugging

### Writing Work
- content/writing-style/SKILL.md — how to sound human
- content/09-HUMANIZER/SKILL.md — strip AI-isms

### Always Apply
- engineering/anti-patterns/SKILL.md — what to avoid
- engineering/code-review-checklist/SKILL.md — before shipping
- The 10 Golden Rules (see below)
```

### On-Demand Loading

When working on a specific task, the agent should load the relevant skill:

```
User: "Build a dashboard with charts"
Agent: *reads frontend-design/01-FRONTEND-DESIGN/SKILL.md*
Agent: *reads components/data-table/SKILL.md*
Agent: *builds the dashboard following the skill patterns*
```

### CLAUDE.md Integration (Best Method for Any Agent)

Any agent that loads `CLAUDE.md` on every session — **OpenCode, MimoCode, Claude Code, Cursor, or similar** — should add the integration block there. This ensures the agent starts every session fully maxxed.

Add this to `~/.claude/CLAUDE.md` (Claude Code) or your agent's equivalent config file:

```markdown
## Agent Maxxing Skills

You have 95+ skills at ~/.opencode/skills/agent-maxxing/ (adjust path for your agent).

Before EVERY response:
1. Check if an anti-pattern is present in your output → remove it
2. Check if a relevant skill exists → load it if so
3. Check if you're hedging → remove the hedge
4. Check if you're over-explaining → cut to the point
5. Check if you're asking when you should be doing → just do it

Always apply: engineering/anti-patterns/SKILL.md before writing code.
Always follow: engineering/execution-protocol/SKILL.md (solve it, don't ask about it).
Sound human, not like a bot.

### Quick Skill Reference
- Frontend: frontend-design/01-FRONTEND-DESIGN/SKILL.md
- Code Review: engineering/deep-code-review/SKILL.md
- Writing: content/writing-style/SKILL.md
- Anti-Patterns: engineering/anti-patterns/SKILL.md
- Execution: engineering/execution-protocol/SKILL.md
- Personality: system-prompts/01-agent-core-personality/SKILL.md
- Tone: system-prompts/06-tone-communication/SKILL.md

Golden Rules:
1. Search before answering
2. Read the codebase first
3. Parallel tool calls
4. Match existing patterns
5. Show don't tell
6. Be concise
7. Take ownership
8. Respect user's time
9. Ship working code
10. Sound human
```

This is the most reliable method — the plugin bootstrap is a fallback, but having it in CLAUDE.md means every session starts with the full integration loaded.

### OpenCode / MimoCode / CLAUDE.md Agents

If your agent loads `CLAUDE.md` on every session (OpenCode, MimoCode, Claude Code, Cursor, etc.), it is recommended to integrate agent-maxxing into CLAUDE.md first, then fine-tune. This way the agent knows about all 95+ skills on every prompt without needing a plugin.

### Creating Your Own Skills

Follow the template in [`CONTRIBUTING.md`](CONTRIBUTING.md):

1. Create `category/your-skill/SKILL.md` with YAML frontmatter
2. Include: name, description, when to use, instructions, rules
3. Test with your agent
4. The agent discovers it automatically on next session

### Skill Discovery

Your agent discovers skills by:
1. Scanning for `SKILL.md` files in the skill directory
2. Reading YAML frontmatter for `name` and `description`
3. Matching task descriptions to skill descriptions
4. Loading the relevant skill before acting

No configuration needed — just drop `SKILL.md` files in the right folder.

---

## 🤖 Compatible Agents

Works with **any agent supporting the [Agent Skills specification](https://agentskills.io/specification)**:

| Agent | Install Path |
|-------|-------------|
| **Claude Code** | `~/.claude/skills/` |
| **Codex CLI** | `~/.codex/skills/` |
| **OpenCode** | `~/.opencode/skills/` (needs plugin for auto-injection — see PROMPT-INTEGRATE.md) |
| **Cursor** | `.cursor/skills/` |
| **Continue** | `.continue/skills/` |
| **Kilo** | `.kilocode/skills/` |
| **OpenClaw** | `.openclaw/skills/` |
| **Pi Agent** | `.pi/skills/` |
| **Hermes** | `~/.hermes/skills/` |
| **60+ more** | Any SKILL.md-compatible agent |

---

## 🏆 The Golden Rules

These patterns come from every top agent in this collection:

1. **Search before answering** — Never guess when you can check
2. **Read the codebase first** — Don't assume, investigate
3. **Parallel tool calls** — Independent ops run simultaneously
4. **Match existing patterns** — Follow the repo's conventions
5. **Show, don't tell** — Demonstrate with examples
6. **Be concise** — Short paragraphs, flat lists, no filler
7. **Take ownership** — Fix mistakes, don't deflect
8. **Respect the user's time** — Don't ask what you can figure out
9. **Ship working code** — Not skeletons, not "you'll need to add..."
10. **Sound human** — Not like a press release or corporate blog

---

## 🤝 Contributing

Skills are just markdown files. To add one:

1. Create `category/your-skill.md` with YAML frontmatter
2. Follow the [Agent Skills spec](https://agentskills.io/specification)
3. Include: name, description, trigger conditions, structured instructions
4. Test with Claude Code, Codex, or any compatible agent
5. Open a PR

### Skill Template

```markdown
---
name: your-skill
description: One-line description of what this skill does
---

# Your Skill Name

## When to Use
- Trigger condition 1
- Trigger condition 2

## Instructions
1. Step one
2. Step two

## Rules
- Rule 1
- Rule 2
```

---

## 💡 P.S. — The Lazy Prompt

Don't want to read through all of that? Pick whichever prompt fits your situation:

### Quick Prompt (just reads and internalizes)

```
Deep dive into the agent-maxxing folder at ~/.claude/skills/agent-maxxing (or wherever you installed it). Read every SKILL.md file — every skill, every system prompt, every component, every workflow example. Understand what each file teaches. Then fine-tune yourself: adopt the patterns, internalize the anti-patterns, apply the engineering judgment, use the writing style. Integrate all 95+ skills so you can use them on any task. From now on, before responding to anything, check if a relevant skill exists and apply it. You are no longer a generic agent — you are maxxed.
```

### Fine-Tune Prompt (behavior transformation — the real magic)

**[Open PROMPT-FINE-TUNE.md on GitHub](https://github.com/subhansh-dev/agent-maxxing/blob/main/PROMPT-FINE-TUNE.md)** — copy the prompt from there.

This is NOT an installation prompt. Use this AFTER the skills are already installed. It forces your agent to internalize the patterns and change how it actually operates on every response. 10 steps: read each core file, confirm you loaded it, demonstrate the behavior change.

### Full Integration Prompt (install + configure + internalize)

**[Open PROMPT-INTEGRATE.md on GitHub](https://github.com/subhansh-dev/agent-maxxing/blob/main/PROMPT-INTEGRATE.md)** — copy the prompt from there.

7 phases: detect platform → locate/clone → install skills → configure permanent integration → self-fine-tune → verify → confirm. Works for Claude Code, Codex, OpenCode, Cursor, Continue, and Kilo Code.

### Ultra-Short Prompt (for context-limited agents)

```
Read FINE-TUNE-AGENT/SKILL.md in the agent-maxxing skills folder. Follow its self-fine-tune protocol. Internalize anti-patterns, execution protocol, and writing style. From now on, check for relevant skills before every task.
```

That's it. One prompt. Your agent reads everything, learns the patterns, and starts applying them. It won't be perfect (context windows have limits), but it'll be noticeably better.

---

## 📜 License

MIT License — use these skills anywhere, no restrictions.

---

<div align="center">

**Built for agents, by someone who got tired of generic AI output.**

[![GitHub](https://img.shields.io/badge/GitHub-subhansh--dev-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/subhansh-dev)

</div>
