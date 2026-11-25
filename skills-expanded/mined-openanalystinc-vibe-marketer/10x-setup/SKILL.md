---
name: 10x-setup
description: First-time setup and initialization for 10X Vibe Marketer. Includes an interactive wizard that lets users choose their database, features, marketing focus, visual tools, and tracking preferences. Checks setup.log to determine if setup has already been completed. Run via /setup or auto-triggered on first use.
---

# 10X Vibe Marketer — Interactive Setup Wizard

## FIRST: Check Setup Status

**Before doing ANYTHING, read the setup log file:**

```
Read file: .claude/setup.log
```

### Decision Logic

```
IF STATUS: INITIALIZED AND wizard_completed in user-preferences.json is true
  → Setup done. Show brief status and exit.
  → "10X Vibe Marketer is already set up. Ready to go!"

IF STATUS: NOT_INITIALIZED (or file missing/corrupted)
  → Run WIZARD first, then technical setup.

IF user runs /setup with --force
  → Re-run wizard + setup even if already initialized.

IF user runs /setup with --preferences
  → Re-run wizard only (change preferences without reinstalling).
```

---

## PHASE 1: Interactive Wizard (First Run Only)

The wizard runs BEFORE any technical installation. Every question uses AskUserQuestion with multiple-choice options. The user should feel like they're designing their own marketing agency.

### Wizard Step 1: Welcome & Business Type

Display welcome banner, then ask:

```
AskUserQuestion({
  questions: [{
    question: "What type of business are you building marketing for?",
    header: "Business",
    options: [
      { label: "SaaS / Software", description: "B2B or B2C software product — recurring revenue, feature marketing, demos, free trials" },
      { label: "E-commerce / Online Store", description: "Physical or digital products — product pages, promotions, seasonal campaigns" },
      { label: "Agency / Freelancer", description: "Marketing or creative services — client work, case studies, thought leadership" },
      { label: "Local Business", description: "Brick-and-mortar or service area — local SEO, Google Maps, reviews, community" },
      { label: "Creator / Personal Brand", description: "Content creator, influencer, coach — audience building, courses, sponsorships" },
      { label: "Startup (Pre-revenue)", description: "Early-stage — product-market fit, MVP marketing, investor decks, lean campaigns" },
      { label: "Enterprise / Corporate", description: "Large organization — multi-channel, compliance, brand governance, ABM" }
    ],
    multiSelect: false
  }]
})
```

Save to `user-preferences.json` (in project root): `business.type`

### Wizard Step 2: Database & Storage

```
AskUserQuestion({
  questions: [{
    question: "Where should your marketing intelligence data live? (campaigns, tracking, tactics, brand context)",
    header: "Database",
    options: [
      { label: "DoltgreSQL + Docker (Recommended)", description: "Version-controlled database with full CRM features. Requires Docker Desktop. Richest experience — campaign management, smart tracking, tactics library" },
      { label: "DoltgreSQL Binary", description: "Same features as Docker but installs the DoltgreSQL binary directly. Lighter than Docker, but requires manual install" },
      { label: "File-based only", description: "No database — use local markdown files for tracking. Works instantly, zero setup. Good for quick tasks" },
      { label: "I'll decide later", description: "Skip database setup for now. You can always run /setup --preferences to add it later" }
    ],
    multiSelect: false
  }]
})
```

Save to `user-preferences.json`: `database.provider`

If user chose DoltgreSQL (Docker or Binary), ask about data import:

```
AskUserQuestion({
  questions: [{
    question: "Import pre-built marketing resources into your database?",
    header: "Import",
    options: [
      { label: "Import everything", description: "216 proven marketing tactics + 302 design templates from Canva/Figma. Gives your agents a head start" },
      { label: "Tactics only", description: "Import 216 marketing tactics (ads, SEO, social, funnels, etc.) — skip design templates" },
      { label: "Templates only", description: "Import 302 design template links (Canva/Figma in 3 aspect ratios) — skip tactics" },
      { label: "Start empty", description: "Empty database — agents will build your library from scratch based on your needs" }
    ],
    multiSelect: false
  }]
})
```

Save to `user-preferences.json`: `database.auto_import_tactics`, `database.auto_import_templates`

### Wizard Step 3: Marketing Focus Areas

```
AskUserQuestion({
  questions: [{
    question: "Which marketing areas are your top priorities? (Select up to 4 — these get premium AI models for higher quality)",
    header: "Focus",
    options: [
      { label: "SEO & Organic", description: "Keyword research, technical SEO, content optimization, link building" },
      { label: "Content & Copy", description: "Blog posts, landing pages, email copy, ad creative, content strategy" },
      { label: "Social Media", description: "Platform strategy, post creation, community engagement, influencer outreach" },
      { label: "Paid Ads & PPC", description: "Google Ads, Meta Ads, LinkedIn Ads, budget optimization, ROAS tracking" }
    ],
    multiSelect: true
  }, {
    question: "Any additional focus areas?",
    header: "More Focus",
    options: [
      { label: "Email Marketing", description: "Sequences, newsletters, automation, segmentation, A/B testing" },
      { label: "Branding & Creative", description: "Brand voice, visual identity, messaging, positioning" },
      { label: "Funnel & CRO", description: "Conversion optimization, landing page testing, checkout flows" },
      { label: "Research & Strategy", description: "Market research, competitor analysis, strategic planning" }
    ],
    multiSelect: true
  }]
})
```

Save to `user-preferences.json`: `marketing_focus` (combined array)

### Wizard Step 4: Campaign Style

```
AskUserQuestion({
  questions: [{
    question: "What's your primary marketing approach?",
    header: "Style",
    options: [
      { label: "Product launches", description: "Go-to-market campaigns, feature announcements, release marketing" },
      { label: "Content-driven growth", description: "SEO content, thought leadership, educational marketing" },
      { label: "Lead generation", description: "Landing pages, lead magnets, email funnels, demos" },
      { label: "Brand awareness", description: "Brand building, PR, social presence, community" },
      { label: "E-commerce sales", description: "Product promotions, seasonal campaigns, conversion optimization" },
      { label: "Community growth", description: "Community building, user-generated content, ambassador programs" }
    ],
    multiSelect: false
  }]
})
```

Save to `user-preferences.json`: `campaign_style`

### Wizard Step 5: Visual Reports & Tracking

```
AskUserQuestion({
  questions: [{
    question: "How do you want visual reports and diagrams?",
    header: "Visuals",
    options: [
      { label: "TLDraw Canvas (Recommended)", description: "Rich interactive canvas — strategy maps, funnel diagrams, journey maps. Exports to SVG/PNG" },
      { label: "Mermaid Diagrams", description: "Text-based diagrams rendered in markdown — flowcharts, sequences, mind maps. Lighter" },
      { label: "Both", description: "TLDraw for strategy visuals, Mermaid for quick flowcharts. Best of both worlds" },
      { label: "Text only", description: "No visual generation — use markdown tables and structured text. Fastest" }
    ],
    multiSelect: false
  }, {
    question: "How detailed should activity tracking be?",
    header: "Tracking",
    options: [
      { label: "Full tracking (Recommended)", description: "Track everything — activities, learnings, performance metrics, weekly summaries. Agents learn from history" },
      { label: "Minimal tracking", description: "Track activities only — skip performance analysis and learning system. Lighter" },
      { label: "Off", description: "No tracking at all. Agents work without historical context. Not recommended" }
    ],
    multiSelect: false
  }]
})
```

Save to `user-preferences.json`: `visuals.tool`, `tracking.level`

### Wizard Step 6: Research Preferences

```
AskUserQuestion({
  questions: [{
    question: "Do you want to enable real-time platform research? (Research trending topics, competitors, and audience data across 13 platforms)",
    header: "Research",
    options: [
      { label: "Yes — full research (Recommended)", description: "Enable all 13 platform research agents (LinkedIn, Twitter, Reddit, Instagram, etc.) + web scraping + AI image generation" },
      { label: "Basic research only", description: "WebSearch + WebFetch only — no platform agents, no Chrome extension needed" },
      { label: "Skip research features", description: "Disable platform research agents. Standard market research via research-analyst still works" }
    ],
    multiSelect: false
  }]
})
```

If user chose "Yes — full research":
1. Check if Chrome extension is installed (try detecting Chrome connection)
2. Check if Python is available for research scripts
3. Check if `scripts/research/requirements.txt` deps are installed
4. If Gemini API key is needed, ask user to add it to `scripts/research/.env`
5. Save to `user-preferences.json`: `research.default_platforms`, `research.browser_preference`, `research.chrome_extension_installed`

### Wizard Step 7: Save Preferences

After all questions are answered:

1. Read the current `user-preferences.json` (project root)
2. Update all fields based on wizard answers
3. Set `wizard_completed: true`
4. Write the updated file back
5. Display a summary:

```
╔══════════════════════════════════════════════════════════════╗
║   YOUR MARKETING AGENCY CONFIGURATION                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   Business: {type}                                          ║
║   Database: {provider}                                      ║
║   Focus: {marketing_focus joined}                           ║
║   Style: {campaign_style}                                   ║
║   Visuals: {tool}                                           ║
║   Tracking: {level}                                         ║
║                                                              ║
║   Setting up now...                                          ║
╚══════════════════════════════════════════════════════════════╝
```

Then proceed to PHASE 2.

---

## PHASE 2: Technical Setup (runs after wizard)

### Step 0: Detect Platform

Detect the user's operating system FIRST:

```
┌─────────────────────────────────────────────────────────────┐
│  PLATFORM DETECTION:                                        │
│                                                             │
│  Check process.platform or OS environment:                  │
│  • win32  → Use PowerShell commands, backslash paths       │
│  • darwin → Use bash/zsh commands, forward slash paths      │
│  • linux  → Use bash commands, forward slash paths          │
│                                                             │
│  Store detected platform for all subsequent commands.       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Create Output Directory Structure

Create all output directories for organized deliverable storage.

**Windows (PowerShell):**
```powershell
$dirs = @(
    "output/campaigns",
    "output/content",
    "output/content/blog-posts",
    "output/content/email-sequences",
    "output/content/social-media",
    "output/content/ad-copy",
    "output/content/landing-pages",
    "output/reports",
    "output/reports/seo-audits",
    "output/reports/competitor-analysis",
    "output/reports/analytics",
    "output/strategies",
    "output/visuals",
    "output/visuals/strategy-maps",
    "output/visuals/funnel-diagrams",
    "output/visuals/campaign-flows",
    "output/visuals/org-charts",
    "output/visuals/journey-maps",
    "output/visuals/canvas",
    "output/briefs",
    "output/logs",
    "output/tracking",
    "output/tracking/campaigns",
    "output/tracking/performance",
    "output/tracking/learnings",
    "output/tracking/metrics"
)
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}
Write-Host "Output directories created." -ForegroundColor Green
```

**macOS/Linux (Bash):**
```bash
mkdir -p output/{campaigns,content/{blog-posts,email-sequences,social-media,ad-copy,landing-pages},reports/{seo-audits,competitor-analysis,analytics},strategies,visuals/{strategy-maps,funnel-diagrams,campaign-flows,org-charts,journey-maps,canvas},briefs,logs,tracking/{campaigns,performance,learnings,metrics}}
echo "Output directories created."
```

### Step 2: Install Local Dependencies

**Check user's visual preference from `user-preferences.json`:**
- If `visuals.tool` is `"text_only"` → Skip npm install entirely (TLDraw not needed)
- Otherwise → Install TLDraw SDK

```
┌─────────────────────────────────────────────────────────────┐
│  LOCAL DEPENDENCIES (installed in project node_modules/):   │
│                                                             │
│  REQUIRED (if visuals enabled):                             │
│  • tldraw — TLDraw SDK for canvas/whiteboard creation      │
│  • @tldraw/tldraw — Core TLDraw package                    │
│  • @kitschpatrol/tldraw-cli — Export to SVG/PNG            │
│                                                             │
│  INSTALL COMMAND:                                           │
│  npm install                                                │
│  (reads from package.json in project root)                 │
│                                                             │
│  If npm is not available:                                   │
│  → Warn user to install Node.js from https://nodejs.org/  │
│  → Visual features will use Mermaid fallback               │
│  → Plugin still works for all non-visual features          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**If npm fails, DO NOT block setup.** Continue with remaining steps.

### Step 3: Setup Database (Based on Wizard Choice)

**Check `database.provider` from `user-preferences.json`:**

```
┌─────────────────────────────────────────────────────────────┐
│  DATABASE SETUP (based on user preference):                 │
│                                                             │
│  "doltgresql_docker":                                       │
│  → Run scripts/setup-db.ps1 or setup-db.sh                │
│  → Docker auto-detect, compose up, schema init             │
│  → Configure marketing-db MCP in .mcp.json                 │
│  → If auto_import_tactics: run import-scrapbook.py         │
│  → If auto_import_templates: run import-templates.py       │
│                                                             │
│  "doltgresql_binary":                                       │
│  → Check for doltgresql binary in PATH                     │
│  → Start server, init schema                               │
│  → Configure MCP                                           │
│  → Run imports if selected                                 │
│                                                             │
│  "file_only" or "later":                                    │
│  → Skip database setup entirely                            │
│  → All tracking uses local files in output/tracking/       │
│  → Display: "Using file-based tracking. Run /setup         │
│     --preferences anytime to add a database."              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Step 4: Validate Plugin Structure

Verify all required files exist:

| File | Required | Purpose |
|------|----------|---------|
| `.claude-plugin/plugin.json` | YES | Plugin manifest |
| `.claude/skills/10x-orchestrator/SKILL.md` | YES | CMO brain |
| `.claude/skills/10x-campaigns/SKILL.md` | YES | Campaign templates |
| `.claude/skills/10x-visualizer/SKILL.md` | YES | TLDraw canvas integration |
| `.claude/skills/10x-setup/SKILL.md` | YES | This setup skill |
| `.claude/skills/10x-research/SKILL.md` | YES | Research orchestration |
| `.claude/agents/*.md` | YES | 26 agent definitions (13 dept + 13 platform) |
| `.claude/commands/*.md` | YES | 27 slash commands |
| `CLAUDE.md` | YES | Project configuration |
| `package.json` | YES | Local dependency manifest |
| `user-preferences.json` (project root) | YES | User preferences (wizard output) |

Use `Glob` to check each location. Report any missing files.

### Step 5: Check External Tools

**Check availability of external tools (DO NOT force-install):**

| Tool | Check Command (Win) | Check Command (Unix) | Purpose |
|------|-------------------|---------------------|---------|
| Node.js | `node --version` | `node --version` | Required for TLDraw SDK |
| npm | `npm --version` | `npm --version` | Package manager |
| Docker | `docker --version` | `docker --version` | For DoltgreSQL container |
| Mega CLI | `where mega-ls.bat` | `which mega-ls` | Cloud resource access |

### Step 6: Check Agent Teams Availability (Mac/Linux only)

```
┌─────────────────────────────────────────────────────────────┐
│  AGENT TEAMS CHECK (Mac/Linux only):                        │
│                                                             │
│  Check if agent teams can be enabled:                      │
│  • Platform is darwin or linux                             │
│  • tmux is installed                                       │
│                                                             │
│  If available, offer via AskUserQuestion:                   │
│  "Enable Agent Teams for enhanced multi-agent mode?"       │
│  [Yes] — Enhanced parallel visibility                      │
│  [No] — Use standard subagents                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Step 7: Initialize Tracking System

**Check `tracking.level` from `user-preferences.json`:**

- If `"full"` → Create all tracking files
- If `"minimal"` → Create only `activity-log.md`
- If `"off"` → Skip tracking initialization

```
output/tracking/
├── activity-log.md
├── campaigns/
├── performance/
│   ├── channels.md
│   ├── content-types.md
│   └── strategies.md
├── learnings/
│   ├── what-works.md
│   └── what-doesnt.md
└── metrics/
    └── weekly-summary.md
```

### Step 8: Write Setup Log

**After successful setup, update `.claude/setup.log`:**

```
## 10X Vibe Marketer — Setup Log
## This file tracks setup status. DO NOT DELETE.

STATUS: INITIALIZED
SETUP_DATE: {current date}
PLATFORM: {detected platform}
NODE_VERSION: {node --version or "not_installed"}
NPM_VERSION: {npm --version or "not_installed"}
TLDRAW_SDK: {installed/not_installed/skipped}
DOLTGRESQL: {connected/not_installed/skipped/file_only}
MEGA_CLI: {installed/not_installed}
AGENT_TEAMS: {enabled/disabled}
SKILLS_VALIDATED: 5/5
AGENTS_VALIDATED: 26/26
COMMANDS_VALIDATED: 27/27
RESEARCH_AGENTS: {enabled/disabled}
CHROME_EXTENSION: {installed/not_installed}
PYTHON_RESEARCH: {installed/not_installed}
GEMINI_API: {configured/not_configured}
PLUGIN_MANIFEST: OK
OUTPUT_DIRS: CREATED
TRACKING_SYSTEM: {full/minimal/off}
WIZARD_COMPLETED: true
BUSINESS_TYPE: {from preferences}
DATABASE_PROVIDER: {from preferences}
MARKETING_FOCUS: {from preferences}
CAMPAIGN_STYLE: {from preferences}
VISUALS_TOOL: {from preferences}
```

### Step 9: Display Personalized Welcome

The welcome message adapts to the user's choices:

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   10X VIBE MARKETER — Your Agency is Ready                  ║
║                                                              ║
║   Configured for: {business.type}                           ║
║   Database: {database.provider}                             ║
║   Focus: {marketing_focus}                                  ║
║                                                              ║
║   Recommended Commands for You:                             ║
║   {Show 5 most relevant commands based on preferences}      ║
║                                                              ║
║   Or just describe what you need in plain English.          ║
║   The CMO will assign the right team automatically.         ║
║                                                              ║
║   Platform: {OS} | Skills: 5 | Agents: 26 | Commands: 27  ║
║   Database: {status} | Visuals: {tool} | Tracking: {level} ║
║                                                              ║
║   Developed by 10x.in                                        ║
╚══════════════════════════════════════════════════════════════╝
```

**Personalized command suggestions based on preferences:**

| Business Type | Recommended Commands |
|---------------|---------------------|
| SaaS | `/campaign`, `/content`, `/seo`, `/funnel`, `/ads` |
| E-commerce | `/campaign`, `/ads`, `/social`, `/email`, `/funnel` |
| Agency | `/strategy`, `/research`, `/campaign`, `/brand`, `/report` |
| Local Business | `/seo`, `/social`, `/community`, `/brand`, `/track` |
| Creator | `/content`, `/social`, `/email`, `/brand`, `/community` |
| Startup | `/strategy`, `/research`, `/campaign`, `/content`, `/ads` |
| Enterprise | `/strategy`, `/brand`, `/campaign`, `/research`, `/audit` |

---

## Re-Running Setup

### /setup (when already initialized)

```
AskUserQuestion({
  questions: [{
    question: "10X Vibe Marketer is already set up. What would you like to do?",
    header: "Setup",
    options: [
      { label: "Check status", description: "View current configuration and system health" },
      { label: "Change preferences", description: "Re-run the wizard to update your marketing focus, database, visuals, etc." },
      { label: "Re-run full setup", description: "Force reinstall all dependencies and reconfigure" },
      { label: "Install missing", description: "Only install components that are missing or failed" }
    ],
    multiSelect: false
  }]
})
```

### /setup --preferences

Re-run ONLY the wizard (Phase 1) without reinstalling anything. Updates `user-preferences.json` (project root) and adjusts configuration accordingly.

### /setup --force

Re-run everything: wizard + full technical setup.

### /setup --status

Show current configuration:
- Read `.claude/setup.log` and `user-preferences.json` (project root)
- Display all settings as a formatted dashboard
- Highlight any issues (missing tools, disconnected database, etc.)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "NOT_INITIALIZED" keeps appearing | Delete `.claude/setup.log` and run `/setup` again |
| npm not found | Install Node.js from https://nodejs.org/ |
| Docker not found | Install Docker Desktop from https://docker.com/ |
| DoltgreSQL connection failed | Check `docker compose logs` or port 5432 availability |
| TLDraw not installing | Run `npm install` manually in the project directory |
| Skills not discovered | Verify `.claude/skills/` directory exists with SKILL.md files |
| Mega CLI not found | Install MEGAcmd from https://mega.io/cmd |
| Agent Teams not working | Requires Mac/Linux + tmux |
| Want to change preferences | Run `/setup --preferences` anytime |

---

*Developed by 10x.in*
