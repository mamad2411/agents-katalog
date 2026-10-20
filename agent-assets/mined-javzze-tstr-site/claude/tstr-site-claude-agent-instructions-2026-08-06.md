# CLAUDE.md - TSTR.directory Project

> **CRITICAL**: This project is part of the AI_PROJECTS_SPACE continuity system.
> **Global System**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/`
> **Project Context**: Read `TSTR.md` (this directory) for project-specific details.

---

## ⚠️ MANDATORY NOTE: Uncertainty and Certainty

AI agents should make it explicit when they do not know and are guessing. If they present a solution as fact, they should calculate an evidence-based level of certainty or probability that it is correct, and what other potential solutions there may be.

---

## 🚨 CRITICAL: MANDATORY FIRST STEP FOR ALL AGENTS

### ⚠️ ALWAYS RUN GLOBAL BOOTSTRAP BEFORE ANY PROJECT WORK

```bash
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && ./bootstrap_global.sh
```

**This provides:**
- Global system context and learnings
- Cross-project task coordination
- Agent handoff information
- Learning system access for optimal decision making

**Failure to bootstrap may result in:**
- Missing critical context
- Duplicating work already done
- Breaking continuity across agents

---

## 🛑 AUTO-EXECUTION POLICY: REPORT FIRST

**CRITICAL RULE FOR ALL AGENTS: DO NOT AUTOMATICALLY TAKE FURTHER ACTIONS.**
- After completing your designated task or finding an issue, **STOP and report to the user.**
- **NEVER** autonomously continue to the next task, implement unrequested features, or execute further commands without explicit user approval.
- Provide a summary of your work, propose the next logical steps, and **WAIT** for the user's explicit confirmation before proceeding.

---

## Mandatory Protocol for ALL Agents

### 1. Global Bootstrap (MANDATORY - See Above)

### 2. Project Session Start (ALWAYS)

**After global bootstrap, run project-specific bootstrap:**

```bash
./bootstrap_global.sh          # loads MuninnDB memories automatically
muninn-cli bootstrap TSTR      # optional: project-scoped memory filter
```

**Note**: The bootstrap script file is `Link_to_bootstrap_agent.sh` in the project root. Always run project bootstrap after global bootstrap.

This loads:
- **Project-specific learnings** (15 relevant from 90 total)
- **Pending tasks** (filtered to TSTR.directory only)
- **Recent session context** (what was last done)
- **Handoff context** from previous agents
- **Protocol reminders** with absolute paths

**Why bootstrap > resume**:
- resume.sh: Shows ALL learnings (overwhelming)
- bootstrap.sh: Shows TSTR.directory learnings only (manageable)
- Filters by project name in tags AND content
- High confidence only (≥4)

**Symlinks available**: In this folder, just run `./bootstrap.sh TSTR.directory`

### 2. Project Status Protocol (MANDATORY)

**CRITICAL**: All agents MUST read and update `PROJECT_STATUS.md` before/after any work:

#### **Before Starting Work**:
```bash
# Read current project state
cat PROJECT_STATUS.md
```

#### **After Completing Changes**:
1. **Update PROJECT_STATUS.md** with version increment and change details
2. **Commit and push** the updated status document
3. **Document ALL changes** that affect the live website:
   - Code deployments
   - UI/branding changes
   - Infrastructure modifications
   - Content updates
   - Link changes
   - Any successful change affecting tstr.directory

#### **Protocol Requirements**:
- ✅ **ALWAYS** update PROJECT_STATUS.md after successful changes
- ✅ **NEVER** deploy changes without documenting them
- ✅ **READ FIRST** - Check current state before making changes
- ✅ **VERSION BUMP** - Increment version number for each update
- ✅ **TIMESTAMP** - Include date/time and agent attribution

**This is the SINGLE SOURCE OF TRUTH for tstr.directory's current state, structure, and change history.**

### 3. During Work

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
task_id = add_task("TSTR.directory", "Task description", assigned_to="claude")
# ... do work ...
update_task(task_id, "completed", result="Result summary")
PYEOF
```

### 3. Session End or Handoff

```bash
cd "/home/al/AI_PROJECTS_SPACE" && ./handoff.sh <agent> <reason>
```

### 4. Cleanup & Archiving Protocol (MANDATORY)

To maintain a clean environment and reduce token clutter:
1. **Delete Interim Files**: Once work is merged/completed, delete redundant files like `HANDOFF_*.md`, `implementation_plan.md`, or temporary reports.
2. **Archive Historical Context**: If a document (e.g., an old project plan or complex analysis) has historical value but is no longer "active," move it to the `_ARCHIVE/` directory instead of leaving it in the root.
3. **Reference Archives**: Before starting a task that feels like a "retry" or "resumption," proactively search the `_ARCHIVE/` folder for previous context or "forgotten" history.

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
**Database**: Supabase (https://haimjeaetrsaauitrhfy.supabase.co)
**API Keys**:
- Publishable: sb_publishable_*** [REDACTED]
- Service Role: [REDACTED_SECRET] (FOR AGENT USE ONLY)


**MCP Server**: ✅ Configured in `web/tstr-automation/TSTR1.mcp.json`
- Server: @supabase/mcp-server-supabase@latest
- Project Ref: haimjeaetrsaauitrhfy
- Access Token: [REDACTED_PAT]
- Mode: Read-only

**Website**: http://tstr.directory (LIVE - 194 listings as of 2026-02-11)

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

**Deployment:** Live on https://tstr.directory with Cloudflare Pages edge caching

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

### SEO Hybrid Hook Strategy ✅ LIVE (2026-02-11)

**CRITICAL MARKETING PRINCIPLE - READ BEFORE ANY LANDING PAGE WORK**

See `MARKETING_STRATEGY.md` for full documentation.

**Core Concept:**
- H1 = Brand Identity ("[Category] Testers")
- H2 = SEO Traffic ("[Category] Testing Services")
- Title/Meta = Both keywords combined

**Why:**
- "Testers" only = 20% of search traffic
- "Testing Services" only = 80% of search traffic
- Hybrid Hook = 100% coverage (+300-400% traffic increase)

**Implementation:**
```typescript
// Helper function in templates
const getTestingServiceName = (categoryName: string) => {
  return categoryName.replace('Testers', 'Testing');
};
```

**Applied to:**
- `/src/pages/[category]/index.astro` - All category pages
- `/src/pages/[category]/[region]/index.astro` - All region pages
- Works automatically for all 6 categories

**ENFORCEMENT:**
- ⚠️ DO NOT remove H2 elements from landing pages
- ⚠️ DO NOT modify title tag structure
- ⚠️ DO NOT remove "Testing" keywords
- ✅ Preserve dual-targeting strategy in all new pages

**Verification:**
```bash
# Check both keywords present
grep -o 'Testers.*Testing' dist/[category]/index.html
```

**Traffic Impact:** Deployed 2026-02-11, monitor Search Console for keyword performance.

---

**Last Updated**: 2026-02-11
**System Version**: AI_PROJECTS_SPACE v2.0

---

<!-- vibe-flow:start -->
# Vibe Flow — Workflow Guide

Use `/vibe-help` anytime for context-aware guidance on what to do next.

## Analysis

- **`CB`** Create Product Brief — A guided experience to nail down your product idea into an executive brief *(Radar)*
- **`MR`** Market Research — Market analysis, competitive landscape, customer needs and trends *(Radar)*
- **`DR`** Domain Research — Industry domain deep dive, subject matter expertise and terminology *(Radar)*
- **`TR`** Technical Research — Technical feasibility, architecture options and implementation approaches *(Radar)*

## Planning

- **`CP`** Create PRD — Expert led facilitation to produce your Product Requirements Document *(Rhythm)*
- **`VP`** Validate PRD — Validate a Product Requirements Document is comprehensive, lean, well organized and cohesive *(Rhythm)*
- **`EP`** Edit PRD — Update an existing Product Requirements Document *(Rhythm)*
- **`CU`** Create UX Design — Guidance through realizing the plan for your UX to inform architecture and implementation *(Prism)*

## Architecture

- **`CA`** Create Architecture — Guided workflow to document technical decisions to keep implementation on track *(Blueprint)*
- **`CE`** Create Epics & Stories — Create the Epics and Stories Listing — the specs that will drive development *(Rhythm)*
- **`IR`** Implementation Readiness — Ensure the PRD, UX, Architecture, and Epics/Stories are all aligned *(Blueprint)*

## Implementation

- **`DS`** Dev Story — Write the next or specified story's tests and code *(Pulse)*
- **`CR`** Code Review — Comprehensive code review across multiple quality facets *(Pulse)*
- **`SP`** Sprint Planning — Generate or update the record that sequences tasks for the full project *(Tempo)*
- **`CS`** Context Story — Prepare a story with all required context for implementation *(Tempo)*
- **`ER`** Epic Retrospective — Multi-agent review of all work completed across an epic *(Tempo)*
- **`CC`** Course Correction — Determine how to proceed if major need for change is discovered mid implementation *(Tempo)*
- **`SS`** Sprint Status — Review and update sprint progress *(Tempo)*
- **`QA`** Generate Tests — Generate API and E2E tests for existing features *(Signal)*

## Quick Flow

- **`QS`** Quick Spec — Architect a quick but complete technical spec with implementation-ready stories *(Dash)*
- **`QD`** Quick Dev — Implement a story tech spec end-to-end (core of Quick Flow) *(Dash)*
- **`QQ`** Quick Dev New — Unified quick flow — clarify intent, plan, implement, review, present *(Dash)*

## Utility

- **`BP`** Brainstorm — Expert guided facilitation through single or multiple brainstorming techniques *(Radar)*
- **`DP`** Document Project — Analyze an existing project to produce useful documentation for both human and LLM *(Echo)*
- **`GC`** Generate Project Context — Analyze the project and produce a context document for AI agents *(Echo)*
- **`SM`** Squad Mode — Bring multiple agent personas into one session to collaborate and discuss *(Maestro)*

<!-- vibe-flow:end -->


<!-- AI_PROJECTS_SPACE:BIFURCATED_HTML_PROTOCOL:START -->
See: SYSTEM/docs/BIFURCATED_INTERACTIVE_HTML_PROTOCOL.md

Use Markdown/text for machine-facing records, ordinary responses, logs, handoffs, commits, and memory. For complex human-facing plans, audits, comparisons, dashboards, or prioritization workflows where interactivity adds value, create a self-contained HTML artifact under `docs/agent_artifacts/` with an export button when state must carry forward.
<!-- AI_PROJECTS_SPACE:BIFURCATED_HTML_PROTOCOL:END -->
