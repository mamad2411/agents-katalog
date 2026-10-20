# GEMINI.md - TSTR.directory Project

> **CRITICAL**: This project is part of the AI_PROJECTS_SPACE continuity system.
> **Global System**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/`
> **Project Context**: Read `TSTR.md` (this directory) for project-specific details.

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

## Mandatory Protocol for ALL Agents

### 1. Global Bootstrap (MANDATORY - See Top of Document)

The mandatory global bootstrap step is documented at the top of this file. Always run the global bootstrap first.

### 2. Project-Specific Context (Optional)

After global bootstrap, you may run project-specific bootstrap for additional TSTR.directory context:

```bash
./bootstrap.sh TSTR.directory
```

**What this adds:**

- **TSTR.directory-specific learnings** (filtered from global database)
- **Project-focused context** (vs. overwhelming global context)
- **High-confidence learnings only** (≥4 rating)
- **Project-specific task filtering**

**When to use**: For deep TSTR.site work requiring extensive project history. The global bootstrap provides sufficient context for most tasks.

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

### 3. Session End or Handoff

```bash
cd "/home/al/AI_PROJECTS_SPACE" && ./handoff.sh <agent> <reason>
```

---

## Gemini / Antigravity Specifics

### Strengths & Capabilities

- **Agentic Workflow**: I excel at breaking down complex tasks using `task_boundary`, `task.md`, and `implementation_plan.md`. I maintain state across long horizons.
- **Browser Subagent**: I have a dedicated `browser_subagent` for verifying UI changes, running end-to-end tests, and interacting with web content visually.
- **Deep Context**: I can process and reason over large amounts of project context, making connections between disparate parts of the codebase.
- **Google Integration**: I have deep knowledge of Google Cloud, Firebase, and related technologies (though note: this project uses Oracle Cloud & Supabase).

### Workflow Preferences

1. **Plan First**: Always start with a clear `task_boundary` and `implementation_plan.md` for any non-trivial task. Clarify what success is so that you can verify completion.
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

## Quick Reference

**Project Root**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working`

**Frontend**: `web/tstr-frontend/` (Astro + React + Tailwind)
**Scrapers**: `web/tstr-automation/` (Python, deployed on OCI)
**Database**: Supabase (<https://haimjeaetrsaauitrhfy.supabase.co>)
**MCP Server**: ✅ Configured in `web/tstr-automation/TSTR1.mcp.json`

- Server: @supabase/mcp-server-supabase@latest
- Project Ref: haimjeaetrsaauitrhfy
- Access Token: [REDACTED_SECRET]
- Mode: Read-only

**Website**: <http://tstr.directory> (LIVE - 163 listings as of 2025-11-17)

**Git Repo**: <https://github.com/JAvZZe/tstr-site.git>

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

**Remember**: First Principles. OODA Loop. Test before deploy. No theater, working code only.

---

## Recent Implementation Notes (2025-11-22)

### Category/Region Dynamic Routes ✅ LIVE

**Routes created:**

- `/[category]` - Category overview showing all regions (e.g., `/hydrogen-infrastructure-testing`)
- `/[category]/[region]` - Filtered listings by category + region (e.g., `/hydrogen-infrastructure-testing/global`)

**Files:**

- `src/pages/[category]/index.astro` - Category overview page
- `src/pages/[category]/[region]/index.astro` - Category+region listings page
- Both use `export const prerender = true` for static generation

**Deployment:** Live on <https://tstr.directory> with Cloudflare Pages edge caching

### Sitemap Optimization ✅ LIVE

**Change:** Sitemap now filters out categories with 0 active listings

**Implementation:** `src/pages/sitemap.xml.ts` joins categories with listing counts:

```typescript
const { data: categoryData } = await supabase
  .from('categories')
  .select(`
    slug,
    listings:listings!category_id(count)
  `);

const categories = (categoryData || [])
  .filter(cat => cat.listings && cat.listings[0]?.count > 0)
  .map(cat => ({ slug: cat.slug }));
```

**Result:** Biotech Testing (0 listings) excluded, Pharmaceutical Testing (108 listings) included. Sitemap: 61 URLs (was 63).

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

**Last Updated**: 2025-11-22
**System Version**: AI_PROJECTS_SPACE v2.0
