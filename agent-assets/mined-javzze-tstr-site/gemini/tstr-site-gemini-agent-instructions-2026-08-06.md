# GEMINI.md - TSTR.directory Project

> **CRITICAL**: This project occurs in the context of the AI_PROJECTS_SPACE continuity system.
> **Global System**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/`
> **Project Context**: Read `TSTR.md` (this directory) for project-specific details.

---

## ⚠️ MANDATORY NOTE: Uncertainty and Certainty

AI agents should make it explicit when they do not know and are guessing. If they present a solution as fact, they should calculate an evidence-based level of certainty or probability that it is correct, and what other potential solutions there may be. Always test your assumptions and work before deploying. Make notes of error and successes so all agents can learn from each other and not repeat errors.

---

## 🛑 AUTO-EXECUTION POLICY: REPORT FIRST

**CRITICAL RULE FOR ALL AGENTS: DO NOT AUTOMATICALLY TAKE FURTHER ACTIONS.**
- After completing your designated task or finding an issue, **STOP and report to the user.**
- **NEVER** autonomously continue to the next task, implement unrequested features, or execute further commands without explicit user approval.
- Provide a summary of your work, propose the next logical steps, and **WAIT** for the user's explicit confirmation before proceeding.

---

## 🚨 CRITICAL: Mandatory First Step

### ⚠️ ALWAYS BOOTSTRAP BEFORE STARTING WORK

**Before using Gemini for any task, you MUST run:**

```bash
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && ./bootstrap_global.sh
```

**What this provides:**
- **Project-specific learnings** and context from the continuity system
- **Pending tasks** filtered to relevant projects
- **Session history** and handoff information from other agents
- **Learning system access** that may affect model selection and task routing decisions

**Why mandatory:**
- Gemini is integrated with the multi-agent continuity system
- Bootstrap ensures you have full context and don't duplicate work
- Provides access to accumulated knowledge and task state
- Required for all agents (Claude, Gemini, OpenHands, OpenCode, etc.)

**Failure to bootstrap may result in:**
- Missing important context and learnings
- Duplicating work already done by other agents
- Inefficient task routing and model selection
- Breaking continuity across the multi-agent system

---

## Mandatory Protocol for ALL Agents

### 1. Global Bootstrap (MANDATORY - See Top of Document)
The mandatory global bootstrap step is documented at the top of this file. Always run the global bootstrap first.

### 2. Project-Specific Context (Optional)
After global bootstrap, you may run project-specific bootstrap for additional TSTR.directory context:

```bash
muninn-cli bootstrap TSTR   # Load project memories (PRIMARY)
```

**What this adds:**
- **TSTR.directory-specific learnings** (filtered from global database)
- **Project-focused context** (vs. overwhelming global context)
- **High-confidence learnings only** (≥4 rating)
- **Project-specific task filtering**

**When to use**: For deep TSTR.directory work requiring extensive project history. The global bootstrap provides sufficient context for most tasks.

### 2. During Work

**Checkpoint frequently**:
```bash
cd "/home/al/AI_PROJECTS_SPACE" && ./checkpoint.sh "description of work completed"
```

**Extract learnings** after errors/discoveries:
```bash
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/state" && python3 << 'PYEOF'
from db_utils import add_learning
add_learning(
    "Your learning here",
    "gotcha",  # or "pattern", "optimization", "security"
    confidence=5,
    tags=["TSTR.directory", "relevant-tech", "specific-issue"]
)
PYEOF
```

**Track tasks**:
```bash
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/state" && python3 << 'PYEOF'
from db_utils import add_task, update_task
task_id = add_task("TSTR.directory", "Task description", assigned_to="gemini")
# ... do work ...
update_task(task_id, "completed", result="Result summary")
PYEOF
```

```bash
cd "/home/al/AI_PROJECTS_SPACE" && ./handoff.sh <agent> <reason>
```

### 4. Cleanup & Archiving Protocol (MANDATORY)

To maintain a clean environment and reduce token clutter:
1. **Delete Interim Files**: Once work is merged/completed, delete redundant files like `HANDOFF_*.md`, `implementation_plan.md`, or temporary reports.
2. **Archive Historical Context**: If a document (e.g., an old project plan or complex analysis) has historical value but is no longer "active," move it to the `_ARCHIVE/` directory instead of leaving it in the root.
3. **Reference Archives**: Before starting a task that feels like a "retry" or "resumption," proactively search the `_ARCHIVE/` folder for previous context or "forgotten" history.

---

## Skills System

**Skills Location**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/skills/` - Procedural guidance for specific tasks.

## Architecture & Memory

**MuninnDB**: Primary memory system — 65+ memories, semantic search via `muninn-cli`. Available from any directory. Run `muninn-cli bootstrap TSTR` at session start to load project-relevant memories.

## Gemini / Antigravity Specifics

### Strengths & Capabilities
- **Agentic Workflow**: I excel at breaking down complex tasks using `task_boundary`, `task.md`, and `implementation_plan.md`. I maintain state across long horizons.
- **Browser Subagent**: I have a dedicated `browser_subagent` for verifying UI changes, running end-to-end tests, and interacting with web content visually.
- **Deep Context**: I can process and reason over large amounts of project context, making connections between disparate parts of the codebase.
- **Google Integration**: I have deep knowledge of Google Cloud, Firebase, and related technologies (though note: this project uses Oracle Cloud & Supabase).

### Workflow Preferences
1. **Plan First**: Always start with a clear `task_boundary` and `implementation_plan.md` for any non-trivial task.
2. **Verify Visually**: Use `browser_subagent` to confirm frontend changes actually work as intended.
3. **Artifacts**: Use artifacts to document plans, walkthroughs, and task lists.

---

## Project-Specific Instructions

**Read these files IN ORDER**:

1. **START_HERE.md** - Quick orientation checklist
2. **TSTR.md** - PRIMARY agent instructions (architecture, commands, priorities)
3. **.ai-session.md** - Latest session context and active tasks
4. **PROJECT_STATUS.md** - Deployment status and infrastructure details
5. **HANDOFF_TO_CLAUDE.md** - Current handoff (if exists)

---

## System Tools

Full reference of available system tools: [SYSTEM_TOOLS_REFERENCE.md](../../SYSTEM/docs/SYSTEM_TOOLS_REFERENCE.md)

## Quick Reference

**Project Root**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working`

**Frontend**: `web/tstr-frontend/` (Astro + React + Tailwind)
**Scrapers**: `web/tstr-automation/` (Python, deployed on OCI)
**Database**: Supabase (https://haimjeaetrsaauitrhfy.supabase.co)
**MCP Server**: ✅ Configured in `web/tstr-automation/TSTR1.mcp.json`
- Server: @supabase/mcp-server-supabase@latest
- Project Ref: haimjeaetrsaauitrhfy
- Access Token: [REDACTED_PAT]
- Mode: Read-only

**Website**: http://tstr.directory (LIVE - 579 active listings as of 2026-02-11)

**Git Repo**: https://github.com/JAvZZe/tstr-site.git

---

## Why This Matters

**Token Economics**: Recording learnings prevents repeated mistakes across sessions.
- Repeated error = ~5000 tokens wasted
- Learning recorded once = ~200 tokens
- ROI after 1-2 avoided repetitions

**Continuity**: Without checkpoints/learnings, context is lost between sessions.
- Failed work = wasted time and money
- Checkpoints = instant recovery from failures

**Game Theory**: Using the continuity system is the optimal strategy for long-term project success.

---

## Enforcement

**Self-check compliance**:
```bash
cd "/home/al/AI_PROJECTS_SPACE" && ./SYSTEM/enforcement/protocol_check.sh
```

Should show:
- ✅ Checkpoints created
- ✅ Learnings recorded
- ✅ Tasks tracked

If any fail → fix violations before continuing.

---

## Development Principles

See `TSTR.md` for:
- User profile (non-tech, AuDHD, OODA + Pareto + First Principles)
- Architecture (frontend, scrapers, database)
- Current priorities (P0, P1, P2)
- Code standards
- Common patterns
- Troubleshooting guides

**Remember**: First Principles. OODA Loop. Test before deploy (define success in the beginning). No theater, working code only.

---

### Supabase API Key Migration ✅ COMPLETE
**Old format (deprecated):** JWT tokens (`eyJhbGci...`)
**New format (current):**
- Publishable key: `sb_publishable_*`
- Secret key: `sb_secret_*`

**Environment variables updated:**
- `.env` and `.dev.vars` (local)
- Cloudflare Pages dashboard (production)

**Critical:** Legacy JWT keys were disabled 2025-10-17. All new deployments use new key format.

---

**Last Updated**: 2026-02-11
**System Version**: AI_PROJECTS_SPACE v2.0


<!-- AI_PROJECTS_SPACE:BIFURCATED_HTML_PROTOCOL:START -->
See: SYSTEM/docs/BIFURCATED_INTERACTIVE_HTML_PROTOCOL.md

Use Markdown/text for machine-facing records, ordinary responses, logs, handoffs, commits, and memory. For complex human-facing plans, audits, comparisons, dashboards, or prioritization workflows where interactivity adds value, create a self-contained HTML artifact under `docs/agent_artifacts/` with an export button when state must carry forward.
<!-- AI_PROJECTS_SPACE:BIFURCATED_HTML_PROTOCOL:END -->
