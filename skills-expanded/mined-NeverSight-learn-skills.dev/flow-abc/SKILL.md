---
name: flow-abc
description: >
  AI-driven frontend development workflow framework. Standardizes how AI assists
  throughout the entire frontend development lifecycle — from requirements analysis
  to code review. Use when: initializing AI rules for a frontend project, developing
  new features with AI assistance, modifying existing features, fixing bugs, reviewing
  code, scanning project components, or auditing project health. Triggers on: init,
  新功能, new feature, modify, bugfix, review, scan, audit, 初始化, 开发, 规范.
license: MIT
metadata:
  author: flow-abc
  version: "2.0.0"
---

# flow-abc — AI Frontend Development Harness

A structured methodology for AI-assisted frontend development. This skill provides
workflows, rules, and context management to ensure AI produces consistent, high-quality
code that follows your project's conventions.

## Core Concept: Three-Layer Harness

```
┌──────────────────────────────────────┐
│  Layer 3: Workflow Harness           │  ← Process: 6-stage development lifecycle
│  ┌──────────────────────────────┐    │
│  │  Layer 2: Eval Harness       │    │  ← Quality: lint + test + AI review
│  │  ┌──────────────────────┐    │    │
│  │  │  Layer 1: Prompt      │    │    │  ← Behavior: rules + context files
│  │  │  Harness              │    │    │
│  │  └──────────────────────┘    │    │
│  └──────────────────────────────┘    │
└──────────────────────────────────────┘
```

- **Prompt Harness**: Rules in `copilot-instructions.md` constrain AI behavior every conversation
- **Eval Harness**: Existing tools (lint/test/type-check) validate AI output
- **Workflow Harness**: Step-by-step workflows ensure consistent development process

## Intent Routing

Based on the user's intent, load the corresponding reference document:

| User Intent | Reference Document | Description |
|---|---|---|
| Initialize AI rules for this project | [references/init-guide.md](references/init-guide.md) | Analyze project, generate `.ai/` directory and rules |
| Develop a new feature / page | [references/workflow-new.md](references/workflow-new.md) | 6-stage workflow: requirements → design → components → code → test → review |
| Modify an existing feature | [references/workflow-modify.md](references/workflow-modify.md) | Locate existing code, understand context, make targeted changes |
| Fix a bug | [references/workflow-bugfix.md](references/workflow-bugfix.md) | Reproduce → locate → fix → verify workflow |
| Review code | [references/review-guide.md](references/review-guide.md) | High signal-to-noise AI review with project rules |
| Scan / refresh components | [references/init-guide.md](references/init-guide.md) §Scan | Re-scan component index and context files |
| Audit project health | [references/init-guide.md](references/init-guide.md) §Audit | One-time architecture and convention analysis |
| Remove AI config from project | [references/init-guide.md](references/init-guide.md) §Clean | Remove `.ai/`, `copilot-instructions.md` (supports sub-project path) |

**How to route**: Read the user's message, identify the primary intent from the table above, then load and follow the corresponding reference document.

## Project Rule File System

After initialization, the target project will have this structure:

### Single-Project Repository

```
.ai/                              # AI configuration directory (source of truth)
├── rules/                        # Behavior rules
│   ├── coding.md                 # Coding conventions (naming, TypeScript, imports)
│   ├── architecture.md           # Architecture constraints (API layer, state, components)
│   ├── testing.md                # Testing conventions
│   └── review.md                 # Review rules (NOT compiled into instructions)
└── context/                      # Project context (loaded on demand)
    ├── project.md                # Project overview, tech stack, architecture
    ├── components.md             # Component index (auto-generated)
    └── api.md                    # API endpoint catalog

.github/copilot-instructions.md  ← Compiled from .ai/rules/ (auto-loaded every conversation)
```

### Monorepo

For monorepos with multiple sub-projects that may have different tech stacks or conventions:

```
.ai/                              # Shared rules (apply to all sub-projects)
├── rules/
│   ├── coding.md                 # Shared coding conventions
│   ├── architecture.md           # Shared architecture constraints
│   ├── testing.md                # Shared testing conventions
│   └── review.md                 # Review rules (NOT compiled)
└── context/
    ├── project.md                # Monorepo overview
    └── components.md             # Shared component index

.ai-<name>/                       # Sub-project specific rules (one per sub-project)
├── rules/
│   ├── coding.md                 # e.g., React-specific or Vue-specific rules
│   └── architecture.md           # Sub-project architecture
└── context/
    ├── components.md             # Sub-project component index
    └── api.md                    # Sub-project API catalog

.github/
├── copilot-instructions.md       ← Compiled from .ai/rules/ (shared rules)
└── instructions/                 ← Path-specific instructions (Copilot native feature)
    ├── <name>.instructions.md    # applyTo: "apps/<name>/**"
    └── <name2>.instructions.md   # applyTo: "packages/<name2>/**"
```

Path-specific instructions use GitHub Copilot's native `applyTo` feature. Each `.instructions.md` file has a frontmatter specifying which files it applies to:

```markdown
---
applyTo: "apps/web/**"
---

[Compiled sub-project rules here]
```

When editing a file, Copilot loads: **shared `copilot-instructions.md`** + **matching path-specific instructions** — both are merged automatically.

### Compilation Rule

All `.ai/rules/*.md` files **except `review.md`** are compiled into `.github/copilot-instructions.md`.

For monorepos, each `.ai-<name>/rules/*.md` is compiled into `.github/instructions/<name>.instructions.md` with the appropriate `applyTo` glob.

- `review.md` is excluded because review rules should only load during review, not during coding
- Context files (`.ai/context/`) are NOT compiled — they are loaded on demand during workflows
- To compile: run `scripts/sync.sh` from this skill, or concatenate manually

### Rule Generation Principle

**Rules are generated by AI (you), not from static templates.** During init:
1. You read and analyze the actual project code
2. You identify real conventions and patterns
3. You generate rules that reflect this specific project
4. You reference [rule-examples/](references/rule-examples/) for formatting style only

## Quick Commands

These are natural language triggers — users just say them in conversation:

- "初始化这个项目的 AI 规范" / "Initialize AI rules" → init workflow
- "开发一个新功能：用户登录" / "Develop: user login feature" → new feature workflow
- "修改搜索功能，增加筛选" / "Modify search to add filters" → modify workflow
- "修复这个 bug" / "Fix this bug" → bugfix workflow
- "review 这段代码" / "Review this code" → review workflow
- "重新扫描组件" / "Rescan components" → scan
- "检查项目规范健康度" / "Audit project health" → audit
- "移除 AI 规范" / "Remove AI config" / "Clean" → clean (支持指定子项目路径)

## Integration with Other Skills

flow-abc manages **project-specific rules**. It works alongside other skills:

- `vercel-react-best-practices` — community React/Next.js best practices
- `web-design-guidelines` — UI/UX audit rules
- Other domain skills

When conflicts arise, project rules in `copilot-instructions.md` take precedence over skill instructions.
