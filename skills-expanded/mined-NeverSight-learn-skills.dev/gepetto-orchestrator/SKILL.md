---
name: gepetto-orchestrator
description: "Orchestrates and advises on Gepetto planning sessions. Use when the user wants to plan a feature thoroughly before coding, asks 'should I use Gepetto for this?', wants to create a spec file for Gepetto, or is unsure what to do with Gepetto's output. Helps assess whether Gepetto's full 17-step pipeline is worth the investment, drafts the spec file, guides the user through the workflow, and advises on how to execute the resulting plan (manual, ralph-loop, or Ralphy CLI). Keeps context short — Gepetto itself handles the heavy lifting via subagents."
---

# Gepetto Orchestrator

Gepetto = 17-step planning pipeline: Research → Interview → Spec Synthesis → Plan → External LLM Review → Section Files → Execution Files (ralph-loop prompt + PRD).

**Skill location:** `~/.agents/skills/gepetto/SKILL.md`

---

## Is Gepetto Worth It?

Ask before starting — gepetto is expensive in time and tokens.

**Use Gepetto when:**
- Non-trivial feature (multi-day work, multiple files, architectural impact)
- Requirements are fuzzy and need clarification
- You want external LLM review of the plan (Gemini + Codex)
- You'll hand off to ralph-loop or Ralphy for autonomous execution

**Skip Gepetto when:**
- Task is well-understood and < 1 day
- You already have a clear spec → go straight to `/gsd-plan-phase` or `/ralph-loop`
- You just need a quick implementation → `/gsd-fast` or `/gsd-quick`

---

## Phase 1: Prepare the Spec File

Gepetto requires a `.md` spec file. If the user doesn't have one, help draft it.

A good spec file:
```markdown
# [Feature Name]

## What
[One paragraph: what we're building]

## Why
[Business/technical motivation]

## Scope
- In: [what's included]
- Out: [what's explicitly excluded]

## Known constraints
[Tech stack, performance requirements, existing patterns to follow]

## Open questions
[Things you're unsure about — Gepetto's interview will resolve these]
```

Present the draft and ask: "Does this capture it? Save it as `planning/[feature-name]-spec.md` then run `/gepetto @planning/[feature-name]-spec.md`."

---

## Phase 2: During Gepetto

Gepetto runs mostly autonomously — it spawns its own subagents. Your role during the run:

- **Answer the interview questions** (Step 6) — these are the most important input. Be specific.
- **Review the integrated plan** (Step 12) — gepetto pauses here. Edit `claude-plan.md` if needed.
- **Let external review run** — Gemini + Codex reviews happen automatically.

Keep this chat context clear while gepetto runs. Resume here after Step 17.

---

## Phase 3: After Gepetto — Choose Execution Path

When gepetto finishes, three outputs matter:

| File | Used for |
|------|---------|
| `sections/` | Manual implementation, section by section |
| `claude-ralph-loop-prompt.md` | Autonomous via `/ralph-loop` |
| `claude-ralphy-prd.md` | Autonomous via Ralphy CLI |

### Advise on execution path

| Situation | Recommendation |
|-----------|---------------|
| Complex, want oversight | Manual: read `sections/index.md`, implement in dependency order |
| Want autonomy, have good test coverage | `/ralph-loop @planning/claude-ralph-loop-prompt.md --completion-promise "ALL-SECTIONS-COMPLETE" --max-iterations 100` |
| Using Ralphy CLI | `ralphy --prd planning/claude-ralphy-prd.md` |
| Want GSD tracking alongside | Import plan into GSD with `/gsd-import` |

### Combining with ralph-orchestrator

If using ralph-loop for execution, hand off to `ralph-orchestrator` skill for:
- Prompt quality review before launching
- Monitoring for stuck loops
- Windows hook fix if needed

---

## Status Header

Show at every response:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Gepetto  |  Stage: [spec prep / running / post-planning]
         |  Spec: [filename or "not created yet"]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Resuming a Gepetto Session

Gepetto auto-detects existing files and resumes from the right step. If the user wants to resume:
```
/gepetto @planning/[feature-name]-spec.md
```
It will scan for `claude-research.md`, `claude-interview.md`, etc. and pick up where it left off.
