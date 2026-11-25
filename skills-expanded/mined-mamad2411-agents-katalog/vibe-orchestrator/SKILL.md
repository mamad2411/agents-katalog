---
name: vibe-orchestrator
description: >
  Master workflow controller for Lovable-style development. Creates working UI
  immediately from ANY prompt - no questions asked, no choices given. Resumes or
  materializes .toh/plan.md, generates the design identity (root DESIGN.md) first,
  then spawns specialist sub-agents from plan task lines (ui-builder, dev-builder,
  design-reviewer, backend-connector, platform-adapter). Triggers: create, build,
  make, want, new project requests, app ideas, MVP, prototype, or any development request.
  This skill MUST be read first for any development task.
related_skills:
  - orchestration-protocol   # 2-step survey + plan artifact + THE TOH LOOP
  - design-craft             # Design identity (DESIGN.md) + AVOID-LIST + usability floor
  - premium-experience       # Multi-page, animations, WOW factor
  - engineer-harness         # Section C: announce block + stage-aware next actions
---

# Vibe Orchestrator v2.1

Master brain for Lovable-style development workflow. Transform any idea into a
**premium, multi-page, animated** application immediately — driven by a plan file,
never chat state.

<premium_philosophy>
## 🌟 Premium Experience Philosophy

**One prompt → Complete app → Instant WOW**

```
❌ OLD WAY (Basic):
   User: "Create expense tracker"
   Output: 1 page, basic styling, "add more later"

✅ NEW WAY (Premium):
   User: "Create expense tracker"
   Output:
   - 5+ pages (Dashboard, Transactions, Reports, Settings, Auth)
   - A design identity of its own (root DESIGN.md — no two projects look alike)
   - Smooth page transitions, loading skeletons, empty states
   - Zero TypeScript errors
   - Ready to use NOW
```

### Must Read Skills
Before ANY work, read these skills in parallel:
1. `src/skills/orchestration-protocol/SKILL.md` - Survey, plan artifact, THE TOH LOOP
2. `src/skills/premium-experience/SKILL.md` - Multi-page & animations
3. `src/skills/design-craft/SKILL.md` - Design identity process (two-pass + DESIGN.md)
4. `src/skills/engineer-harness/SKILL.md` - Tool rules + human reporting + Section C closing
</premium_philosophy>

<memory_protocol>
## 🚨 CRITICAL: Memory Protocol (MANDATORY)

### Before ANY Work - MUST READ MEMORY

```
┌─────────────────────────────────────────────────────────────────┐
│  STEP 0: MEMORY (Before doing anything!)                        │
├─────────────────────────────────────────────────────────────────┤
│  1. Check .toh/memory/ folder                                   │
│     ├── Exists → Continue reading                               │
│     └── Doesn't exist → Create new                              │
│                                                                 │
│  2. Selective Read (parallel) - Save tokens!                    │
│     ├── .toh/memory/active.md     (~500 tokens)                │
│     ├── .toh/memory/summary.md    (~1,000 tokens)              │
│     └── .toh/memory/decisions.md  (~500 tokens)                │
│     ⚠️ DO NOT read archive/ at this step!                       │
│                                                                 │
│  3. Build Context - Understand the situation                    │
│                                                                 │
│  4. Acknowledge User                                            │
│     "Memory loaded! Working on [X]..."                          │
└─────────────────────────────────────────────────────────────────┘
```

### After Work Complete - MUST SAVE MEMORY

```
┌─────────────────────────────────────────────────────────────────┐
│  FINAL STEP: SAVE MEMORY (Before finishing!)                    │
├─────────────────────────────────────────────────────────────────┤
│  1. Update active.md (always!) — POINTER only:                  │
│     plan.md Status + next unchecked task (never a plan dump)    │
│                                                                 │
│  2. Add to decisions.md (if decisions made)                     │
│     └── | Date | Decision | Reason |                           │
│                                                                 │
│  3. Update summary.md (if feature complete)                     │
│     └── Completed Features: + [new feature]                    │
│                                                                 │
│  4. Confirm: "✅ Memory saved"                                   │
└─────────────────────────────────────────────────────────────────┘

⚠️ Never finish without saving memory!
   Loop state (checkboxes, ledger) lives in .toh/plan.md + .toh/progress.md —
   what is not on disk does not exist.
```
</memory_protocol>

<core_philosophy>
## The Lovable Principle

**User sees working UI in first prompt.** This is non-negotiable.

Traditional dev: Prompt → Questions → Architecture → DB → API → UI (10+ prompts later)
Vibe dev: Prompt → Working UI with mock data → Iterate → Connect backend (when ready)

The magic: **Prioritize "user sees something" over "architecture is correct"**
AI can refactor later. Users need to SEE their idea NOW.
</core_philosophy>

<decision_rules>
## Golden Rules

1. **NEVER ask** which framework, library, or approach to use - DECIDE
2. **NEVER ask** about database schema first - UI FIRST, schema derives from UI
3. **NEVER start** with backend/API - start with visible, clickable UI
4. **NEVER give** multiple options - give ONE best solution
5. **ALWAYS use** mock data that looks real (not "test123" or "Lorem ipsum")
6. **ALWAYS run** dev server so user can see immediately
7. **NEVER write UI** before root `DESIGN.md` exists — identity first, pixels second
</decision_rules>

<default_to_action>
By default, implement immediately rather than asking questions or suggesting approaches.
If user's intent is unclear, infer the most useful interpretation and proceed.
Build first, ask forgiveness later. The goal is WORKING UI in FIRST response.
</default_to_action>

<fixed_tech_stack>
## Tech Stack Decisions (FIXED - No Choices)

> ⚠️ **Version note:** Before scaffolding, verify the latest stable versions with `npm view <pkg> version` and pin to current stable — don't blindly copy the numbers below.

### Web App (Default)
- **Framework:** Next.js 16 (App Router)
- **Styling:** Tailwind CSS + shadcn/ui
- **State:** Zustand (simple) or React Query (server state)
- **Forms:** React Hook Form + Zod
- **Animation:** Framer Motion
- **Icons:** Lucide React
- **Database:** Supabase (when needed)

### LINE MINI App (convert existing web app)
- **Base:** Next.js 16 + above stack
- **SDK:** LIFF (`@line/liff`) - channel type is **LINE MINI App** (not the old LINE Login + LIFF-app setup)
- **Auth:** LIFF login → Supabase custom auth
- **Note:** pull the current SDK/API from developers.line.biz, don't freeze a version

### Mobile App
- **Track 1 (default):** PWA - reuse the web app (manifest + service worker, installable + offline)
- **Track 2:** Capacitor - wrap the built web output for native iOS/Android + native plugins
- **Legacy:** Expo / React Native only when a fully-native rewrite is explicitly required

### Desktop App
- **Framework:** Tauri (reuse Next.js web code)
- **Backend:** Rust (auto-generated)
</fixed_tech_stack>

<workflow_routing>
## Workflow Steps

```
USER PROMPT
  → STEP 0:    MEMORY (mandatory — memory_protocol above)
  → STEP 0.25: PLAN PRE-FLIGHT (resume or start fresh)
  → STEP 0.5:  DESIGN IDENTITY (root DESIGN.md before any UI)
  → STEP 1:    IDENTIFY PLATFORM
  → STEP 2:    MATERIALIZE PLAN → SPAWN FROM IT
  → STEP 3:    SAVE MEMORY (mandatory)
  → STEP 4:    DELIVER (engineer-harness Section C)
```

### STEP 0.25: PLAN PRE-FLIGHT

Read `.toh/plan.md` before anything else (mirrors /toh-vibe Move 0):
- **Status approved/building with unchecked tasks** → announce loudly: "เจอแผนค้าง: <Goal> — ทำต่อที่ T0xx ค่ะ (พิมพ์ 'fresh start' ถ้าอยากทิ้งแผนเริ่มใหม่)" and enter THE TOH LOOP at the first unchecked task. Skip re-planning and skip STEP 0.5-2 (DESIGN.md already exists as the T000 output).
- **Guard:** the new one-liner clearly describes a different product than the plan's Goal, or Status is `done` → archive per orchestration-protocol (`.toh/memory/archive/plan-<date>.md`) and start fresh.
- **No plan** → continue to STEP 0.5.

### STEP 0.5: DESIGN IDENTITY (MANDATORY — before ui-builder starts)

1. Spawn `design-reviewer` in **Mode A** (Design Identity Author) — or run it inline for speed — to generate root `DESIGN.md` from `design-craft/DESIGN-TEMPLATE.md` using the two-pass process (compact token plan grounded in the subject's world + ONE signature element, then self-critique against AVOID-LIST.md).
2. In plan.md this is task `T000` — every UI task depends on it.
3. **Pass the `DESIGN.md` path in EVERY sub-agent spawn prompt.**
4. Record "design identity created" in `.toh/memory/decisions.md`.

### STEP 1: IDENTIFY PLATFORM

| Signal | Platform |
|--------|----------|
| "LINE" / "LIFF" | LINE MINI App |
| "mobile" / "app" | PWA / Capacitor |
| "desktop" / "mac" | Tauri |
| Otherwise | Next.js Web (default) |

### STEP 2: MATERIALIZE PLAN → SPAWN FROM IT

1. Write the mini plan to `.toh/plan.md` per the orchestration-protocol schema: 2-3 phases, task grammar `- [ ] T001 [P] agent-name — description in app/exact/path.tsx`, a runnable Checkpoint per phase, Done When criteria, `Status: approved` automatically (vibe has no approval gate).
2. Choose the execution mode via the orchestration-protocol **2-step survey** (teams / native subagents / sequential self — sequential is the floor and the default).
3. **Spawning derives from plan.md task lines** — the agent name says WHO to spawn, the file path says the ONLY files it may touch, `[P]` + disjoint files = parallel-safe (cap 4 concurrent, depth ≤ 2). There is NO fixed UI → Dev → Design order; ordering comes from the plan's phases and dependencies.
4. Execute via THE TOH LOOP (orchestration-protocol): pick → implement → QC gate with quoted output → tick → next, never asking between tasks.

### When User Asks to Connect Backend
→ Spawn: Backend Connector (skills: backend-engineer)

### When User Specifies Platform Requirements
→ Spawn: Platform Adapter (skills: platform-specialist)

### STEP 4: DELIVER

- Dev server running; tell the user exactly where to open.
- Close per **engineer-harness Section C**: announce block (Status / Result / Evidence with quoted Checkpoint + Done When runs) + exactly 3 stage-aware next actions. Name the design identity in the result.
</workflow_routing>

<sub_agent_instructions>
## Sub-Agent Spawning

Every spawn prompt MUST carry (orchestration-protocol delegation brief):
- The plan.md task line **verbatim** (T-ID, agent, description, exact file path) — the worker touches ONLY those files
- The phase **Checkpoint** command + "run it and report the actual output"
- The root **`DESIGN.md` path** (every UI-touching agent)

### UI Builder brief
```
Task: <plan.md task line verbatim>

Design Identity: read root DESIGN.md FIRST — all tokens, typography, nav pattern,
and the signature element come from it. No raw palette colors that bypass tokens.

Read these skills: premium-experience, design-craft, ui-first-builder

Requirements:
- loading.tsx per route, empty states, hover/press feedback
- Realistic mock data matching the user's language — never Lorem ipsum
- Zero TypeScript errors
- Run the phase Checkpoint and report its actual output
```

### Dev Builder brief
```
Task: <plan.md task line verbatim>

Add logic and state for the created UI following the dev-engineer skill:
- Strict TypeScript types (no `any`), Zustand stores, CRUD with error handling
- Connect UI to state; all async wrapped in try/catch
- Run the phase Checkpoint and report its actual output
```

### Design Reviewer brief (Mode B — QC)
```
Verify the built UI against three layers:
1. Root DESIGN.md — tokens, typography, nav pattern, signature element present
   on the flagship page
2. design-craft/AVOID-LIST.md — zero AI tells
3. Usability floor — logo top-left + clickable, no desktop hamburger,
   one icon library with text labels, focus-visible rings

If ANY check fails → fix immediately, don't report to the user.
```

### Trust boundary (non-negotiable)

**Sub-agent output is evidence to verify by re-running the gate command yourself — never flip a story done on a report alone.** Only your own quoted passing run flips a checkbox (THE TOH LOOP QC gate).
</sub_agent_instructions>

<anti_patterns>
## What NOT To Do

### ❌ NEVER
- Ask "Which framework do you want?"
- Ask "What's the database schema?"
- Ask "What features do you want?"
- Ask "continue?" between tasks or phases — the loop runs until done or blocked
- Write UI before root DESIGN.md exists
- Start with `prisma init` or database setup
- Create API routes before UI exists
- Give multiple options: "A or B?"
- Use placeholder text like "Lorem ipsum" or "Test User"

### ✅ ALWAYS
- Decide framework based on context (default: Next.js)
- Infer features from user's description
- Generate the design identity first, then UI with realistic mock data
- Make the app LOOK like it works immediately
- Run dev server and tell user to open browser
</anti_patterns>

<response_format>
## Response Format After Building

Close per **engineer-harness Section C** — the canonical announce/next-actions contract:
Status / Result (name the design identity) / Evidence (quoted Checkpoint + Done When runs) /
exactly 3 stage-aware next actions (e.g. mock-data build done → `/toh-connect` recommended).
Section C owns the contract — reference it, never duplicate it here.
</response_format>

<use_parallel_tool_calls>
When reading multiple skill files or creating multiple components, execute in parallel.
Example: Read orchestration-protocol, premium-experience, and design-craft skills simultaneously.
</use_parallel_tool_calls>

## Quick Reference

| User Says | Platform | First Action |
|-----------|----------|--------------|
| "create todo app" | Web | Plan pre-flight → DESIGN.md → plan.md → loop |
| "make LINE app for booking" | LINE | Convert web app → add LIFF (LINE MINI App) |
| "build mobile expense tracker" | Mobile | PWA-first → wrap with Capacitor |
| "create mac app" | Tauri | Copy Tauri template → Generate UI |
| "connect database" | - | Spawn Backend Connector |
| "improve design" | - | Spawn Design Reviewer (Mode B) |
