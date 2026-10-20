# AGENTS.md - Development Guidelines for TSTR.directory

## 🚨 CRITICAL: MANDATORY FIRST STEP FOR ALL AGENTS

**⚠️ ALWAYS RUN GLOBAL BOOTSTRAP BEFORE ANY PROJECT WORK:**

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

## 🚀 PROJECT INITIALIZATION (After Global Bootstrap)

**When starting work in this project:**
```bash
./start-agent.sh    # Recommended: Complete project initialization with status
# OR
./bootstrap.sh TSTR-site    # Direct project bootstrap (legacy)
```

**Quick Start Commands:**
```bash
tstr-agent          # Alias for ./start-agent.sh (after ~/.bashrc reload)
./start-agent.sh    # Full project agent initialization
./monitoring/daily_check.sh  # System health check
```

**Note**: The bootstrap script file is `Link_to_bootstrap_agent.sh` in the project root. Always run project initialization after global bootstrap.

This loads:
- Project-specific learnings from database
- Pending tasks for TSTR-site
- Recent session context
- Pending handoffs
- Recent checkpoints

## 🔑 SUPABASE CONFIGURATION

**URL**: https://haimjeaetrsaauitrhfy.supabase.co
**Anon Key**: sb_publishable_nFGCy-22_7FQlVr_SkJ6cQ_mwfYVhA4
**Service Role Key**: [REDACTED_SECRET]

**MCP Server**: ✅ Configured in `web/tstr-automation/TSTR1.mcp.json`
- Server: @supabase/mcp-server-supabase@latest
- Project Ref: haimjeaetrsaauitrhfy
- Access Token: [REDACTED_SECRET]
- Mode: Read-only

## 🔄 DEPLOYMENT NOTES

**Cloudflare Pages Deployment Issues:**
- CSS changes may take 1-2 hours to propagate globally
- Subscription page deployed successfully, account page CSS pending
- Check `ACCOUNT_BUTTON_IMPROVEMENTS_HANDOFF.md` for current status
- Monitor: https://dash.cloudflare.com/pages → tstr-site → Deployments

## 📊 PROJECT STATUS PROTOCOL (MANDATORY)

**CRITICAL**: All agents MUST read and update `PROJECT_STATUS.md` before/after any work:

### **Before Starting Work**:
```bash
# Read current project state
cat PROJECT_STATUS.md
```

### **After Completing Changes**:
1. **Update PROJECT_STATUS.md** with version increment and change details
2. **Commit and push** the updated status document
3. **Document ALL changes** that affect the live website:
   - Code deployments
   - UI/branding changes
   - Infrastructure modifications
   - Content updates
   - Link changes
   - Any successful change affecting tstr.directory

### **Protocol Requirements**:
- ✅ **ALWAYS** update PROJECT_STATUS.md after successful changes
- ✅ **NEVER** deploy changes without documenting them
- ✅ **READ FIRST** - Check current state before making changes
- ✅ **VERSION BUMP** - Increment version number for each update
- ✅ **TIMESTAMP** - Include date/time and agent attribution

**This is the SINGLE SOURCE OF TRUTH for tstr.directory's current state, structure, and change history.**

## AI Agent CLI Functions (v2.0 Integration)

**Available in all bash sessions** (added to ~/.bashrc):

```bash
# Complex reasoning, architecture, review, decisions
ask-arch "your complex query here"

# Continuation when Claude expensive, medium complexity
ask-gemini "continue this task"

# Code generation, batch processing, simple tasks
ask-code "write a Python function for..."
```

**Context Dumping for Agent Handoffs:**
```bash
# Dump current system state to markdown (for external agents)
python3 ../../../SYSTEM/state/db_utils.py --dump > .context_dump/current_state.md

# Add new learnings to the system
python3 ../../../SYSTEM/state/db_utils.py --learn "your learning here"
```

## Commands

### Frontend (Astro + React)
```bash
cd web/tstr-frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Testing
```bash
npm run test          # Run all Playwright tests
npx playwright test tests/example.spec.ts    # Run single test
npx playwright test --grep "test name"      # Run tests by name
```

### Python Scrapers
```bash
cd web/tstr-automation
pip install -r requirements.txt
python scrapers/a2la_materials.py    # Run specific scraper
```

**Scraper Deployment Strategy:**
- **Heavy-duty scrapers** (requiring browser automation like Playwright/Selenium): Run locally due to OCI RAM limitations
- **Lightweight scrapers** (simple HTTP/HTML parsing): Deploy to OCI when resources allow
- **Local Automation**: Available with 40GB RAM - can run automated local scrapers
- **Current OCI instance**: 84.8.139.90 (Oracle Linux 9) - active for lightweight operations
- **Resource decision**: Local execution for any scraper needing >1GB RAM or JavaScript rendering

### Environment Files (.env)
**IMPORTANT**: .env files contain sensitive secrets and are blocked from read/edit tools. Use bash commands instead:
```bash
# Create .env from example
cp web/tstr-frontend/.env.example web/tstr-frontend/.env
cp web/tstr-automation/.env.example web/tstr-automation/.env

# Read .env file
cat web/tstr-frontend/.env

# Edit .env file
nano web/tstr-frontend/.env  # or vim, code, etc.
```

## Code Style

### TypeScript/JavaScript
- Use strict TypeScript config (`extends: "astro/tsconfigs/strict"`)
- Import order: 1) External libs, 2) Internal components, 3) Relative imports
- Use React functional components with hooks
- Error handling with try/catch and proper logging

### Python
- Use type hints (`from typing import Dict, List, Optional`)
- Import order: 1) stdlib, 2) third-party, 3) local imports
- Inherit from `BaseNicheScraper` for all scrapers
- Use logging, not print statements

### Astro
- Use `export const prerender = true` for static pages
- Fetch data in frontmatter with Supabase client
- Use Tailwind CSS classes, avoid inline styles

### Naming
- Files: kebab-case (`my-component.astro`, `scraper_name.py`)
- Components: PascalCase (`MyComponent`)
- Variables/functions: camelCase (JS) or snake_case (Python)
- Constants: UPPER_SNAKE_CASE

### Git Commits
- Format: `[AGENTNAME] Brief description`
- Include context in body for complex changes