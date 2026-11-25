---
name: prompt-builder-architect
description: "Use when breaking down app ideas into modular prompts for v0.dev, Cursor, Replit, and lovable.dev. Creates prompt sets covering UI, backend, and deploy flows tailored by plan tier. Consolidates PromptBuilder Architect V1/V2, Replit Builder, and v0.dev Full Stack App Builder."
version: "1.0"
tags:
  - prompt-engineering
  - v0.dev
  - cursor
  - replit
  - lovable.dev
  - full-stack
  - rapid-prototyping
---

# Prompt Builder Architect

## Overview

Transform a raw app idea into a structured, platform-aware prompt set that targets v0.dev, Cursor, Replit, and lovable.dev. Each platform has unique prompt formats and constraints — this skill generates prompts optimized for each so you can prototype faster across tools.

## When to Use

- A user says "I have an app idea" and wants to start building
- You need to generate v0.dev prompts to scaffold UI components
- You're planning a multi-tool workflow (Cursor for backend, v0 for UI, Replit for deployment)
- A user is evaluating which AI builder best fits their project
- You need tiered prompt sets (free vs. pro plan prompts for each platform)

## How It Works

1. **Idea Intake** — Extract the core concept, target users, key features, and tech preferences.
2. **Platform Mapping** — For each platform, determine what it does best and assign sub-tasks:
   - **v0.dev**: UI components, page layouts, design systems (React/Tailwind/shadcn)
   - **Cursor**: Backend logic, database schemas, API routes, complex business logic
   - **Replit**: Full-stack prototypes, quick deploys, collaborative iteration
   - **lovable.dev**: End-to-end full-stack apps with auth, DB, and deployment
3. **Prompt Generation** — Produce modular prompts for each platform following their specific best practices.
4. **Plan Tiering** — Adapt prompt detail to the user's plan tier (free = concise, pro = comprehensive).

## Steps

### Step 1: Gather Requirements
Ask targeted questions:
- What does the app do? (one-sentence pitch)
- Who is the primary user?
- What are the 3-5 core features?
- Any tech stack preferences? (React, Next.js, TypeScript, etc.)
- Do you have accounts on v0 / Cursor / Replit / lovable?

### Step 2: Select Platforms
Based on the app's complexity and user's access, recommend which platforms to use:
- **Simple UI-heavy apps** → v0.dev first
- **Logic/backend-heavy** → Cursor first
- **Quick full-stack prototype** → Replit or lovable.dev
- **Production-ready full-stack** → Cursor + v0.dev combination

### Step 3: Write Platform Prompts
For each selected platform, craft prompts in their native style:

**v0.dev prompt format:**
```
Create a [component/page] for [app name] that:
- Uses React + Tailwind + shadcn/ui
- [specific layout requirements]
- [state management needs]
- [responsive behavior]
- Match this design tone: [description]
```

**Cursor prompt format:**
```
// File: [path]
// Task: [what to build]
// Context: [relevant project info]
// Constraints: [limits/rules]
// Acceptance: [how to verify it works]
```

**Replit prompt format:**
```
Build a [app type] with:
- Stack: [framework/db/auth]
- Features: [bullet list]
- UI: [design direction]
- Deploy target: [Replit hosting / custom domain]
```

**lovable.dev prompt format:**
```
Full-stack app: [name]
Description: [2-3 sentences]
Core features:
1. [feature with auth requirement]
2. [feature with DB table]
3. [feature with API call]
Tech stack: [Next.js / Supabase / etc.]
```

### Step 4: Tier Adjustments
- **Free tier**: Max 2-3 prompts per platform, concise, one-shot execution
- **Pro tier**: 5-10 prompts, modular files, incremental build steps, error recovery hints

### Step 5: Deliver Prompt Set
Present as a collapsible, numbered list grouped by platform. Include:
- Platform name + purpose
- Copy-paste-ready prompts
- Execution order (what to run first)
- Expected output per prompt
- Tips for fixing common errors per platform

## Common Pitfalls

- **Over-prompting v0.dev**: v0 works best with focused, single-component prompts. Don't ask for an entire app in one prompt.
- **Under-specifying Cursor prompts**: Cursor needs file paths, context, and acceptance criteria to produce good code.
- **Ignoring plan limits**: Free-tier v0 and Replit have message/credits limits. Batch wisely.
- **Wrong platform for the job**: Don't use v0 for database schema design; don't use Cursor for pure UI layout.

## Source

Consolidates: PromptBuilder Architect V1, PromptBuilder Architect V2, Replit Builder GPT, v0.dev Full Stack App Builder GPT.
