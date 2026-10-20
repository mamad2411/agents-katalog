# Repository Context for Claude

## Repository Purpose

This repository serves **two primary purposes**:

1. **Portfolio Website** (Production) - A live portfolio website showcasing Viresh's work
2. **Job Hunting & Interview Prep** (Personal) - Active materials for job applications and interview preparation

## Directory Structure

```
per_wesite/
├── [WEBSITE - Production Files - DO NOT MODIFY without explicit request]
│   ├── index.html, profile-photo.jpg, package.json, nginx.conf
│   ├── css/, js/, data/, media/
│   ├── certifications/, resume/, scripts/
│   ├── README.md, CONTENT_GUIDE.md, DEPLOYMENT.md
│   └── Docker configuration files
│
├── job-prep/                 [Active job hunting materials]
│   ├── README.md                [Overview and quick links]
│   ├── guides/                  [Job search guides and strategies]
│   ├── applications/            [One folder per application - STRUCTURED SYSTEM]
│   │   ├── README.md            [Master tracker with all applications]
│   │   ├── _template/           [Template for new applications]
│   │   │   ├── job-posting.md   [Job details template]
│   │   │   └── resume-data.json [Resume JSON template]
│   │   ├── _resources/          [Reference materials - guides, templates]
│   │   ├── _archive/            [Old/rejected applications]
│   │   └── {company-role}/      [Active application folders]
│   │       ├── job-posting.md   [Job details + metadata + customization notes]
│   │       ├── resume-data.json [Resume generation data]
│   │       └── resume.pdf       [Latest generated resume]
│   ├── context/                 [Interview Q&A banks and application context]
│   └── archive/                 [Old/completed materials - rarely modified]
│
├── interview-prep/              [Active interview preparation]
│   ├── companies/               [Company-specific prep - ALL materials per company]
│   │   ├── casium/              [Casium: 23 files - DB schema, Python, exercises + README]
│   │   └── woven/               [Woven: Architecture debugging prep]
│   └── mock-interviews/         [General practice interviews by type]
│       ├── code-review/         [Code review practice (3 mocks)]
│       ├── architecture-debugging/ [Architecture debugging (5 practices)]
│       └── assessments/         [Mock assessments (2 files)]
│
└── practice-problems/           [General coding practice - NOT company-specific]
    └── python/
        └── fundamentals/        [Basic Python warmups (3 files)]
```

## Important Files & Usage

### Scratchpad Usage
- **Location:** `scratchpad.txt` (root directory) - **ALWAYS use .txt format, never .md**
- **Purpose:** Active workspace for discussions about job hunting and interview prep
- **Workflow:** User shares ideas → Claude provides feedback → Extract relevant context into organized markdown files
- **Keep:** File exists but content should be cleared after extraction
- **Rule:** When creating or writing to scratchpad, ALWAYS use `scratchpad.txt` format

### Content Management
- **Website content:** Managed via JSON files in `data/` directory
- **Job hunting context:** Organized in `job-prep/` and `interview-prep/`
- **Resume files:** Stored in `resume/` (AI-focused and Robotics-focused versions)

## What NOT to Modify

**Production website files** should only be changed with explicit user request:
- `index.html`, `css/`, `js/`, `data/`
- `package.json`, `nginx.conf`, Docker files
- `profile-photo.jpg`, `media/`

## Where to Add New Materials

| Material Type | Location | Notes |
|---------------|----------|-------|
| **New job application** | `job-prep/applications/{company-role}/` | Copy `_template/` folder, customize, generate resume |
| Job hunting guides/strategies | `job-prep/guides/` | Strategic planning, market research |
| Interview Q&A banks | `job-prep/context/` | Behavioral, technical, leadership questions |
| Company-specific interview prep | `interview-prep/companies/{company-name}/` | DB schema, coding exercises, ALL prep materials |
| Mock interview practice | `interview-prep/mock-interviews/{type}/` | General practice by interview type |
| General Python practice | `practice-problems/python/fundamentals/` | Warmup exercises, NOT company-specific |

🚨 **CRITICAL: RESUME WORKFLOW ENFORCEMENT SYSTEM** 🚨

⚠️ **TRIGGER CONDITION: User mentions job posting, role application, or says "help me apply"**

## MANDATORY WORKFLOW STEPS - NO EXCEPTIONS

### 🛑 STEP 0: IMMEDIATE VALIDATION (DO THIS FIRST)
```
BEFORE any resume work, ask yourself:
"Am I about to start Step 0: FIT ANALYSIS from RESUME_APPLICATION_WORKFLOW.md?"

IF NO: STOP. Start with fit analysis.
IF YES: Proceed with validation checks below.
```

### 📋 PRE-WORKFLOW VALIDATION CHECKLIST
**Load these files in order and validate access:**

1. **Load Role Context** (saves 600 tokens):
   ```
   Read: job-prep/applications/_resources/role-based-context-loading.md
   ```

2. **Load Validation Rules** (prevents violations):
   ```
   Read: job-prep/applications/_resources/VALIDATION_RULES.md
   Read: job-prep/applications/_resources/RESUME_VALIDATION_CHECKLIST.md
   ```

3. **Verify Baseline Access** (source of truth):
   ```
   Read: job-prep/applications/_resources/baseline-resume-data.json
   ```

4. **Load Workflow Document** (mandatory process):
   ```
   Read: job-prep/RESUME_APPLICATION_WORKFLOW.md
   ```

### 🔒 ENFORCEMENT SAFEGUARDS

**LOCKED CONTENT - NEVER MODIFY:**
- 🔒 Freefly bullets 2-4 (LinkedIn verified)
- 🔒 Lumenier bullets 1-2 (both locked)
- 🔒 York bullets 1-2 (both locked)
- 🔒 All job titles, company names, dates
- 🔒 Education section, contact information

**VALIDATION REQUIREMENTS:**
- ✅ 3-4-2-2 bullet count pattern enforced
- ✅ Human approval at 3 checkpoints mandatory
- ✅ JSON draft review before PDF generation
- ✅ Automated validation against baseline required

**CHECKPOINT GATES (user approval required):**
1. **Fit Assessment** - "Does this job match? Proceed?"
2. **Scratchpad Review** - "Does this customization look correct? Approve to generate PDF?"

### ⛔ FAILURE CONDITIONS
**If any of these occur, STOP workflow immediately:**
- Cannot access baseline-resume-data.json
- User skips fit analysis confirmation
- Locked content is modified in any way
- Validation rules are violated
- User doesn't approve at checkpoints

### 🔄 WORKFLOW EXECUTION

**MANDATORY ORDER:**
```
Step 0: FIT ANALYSIS (must complete first)
   ↓
Step 1: CUSTOMIZE RESUME + SCRATCHPAD (if user confirmed)
   ↓
Step 2: USER APPROVES SCRATCHPAD
   ↓
Step 3: GENERATE JSON → VALIDATE → GENERATE PDF
```

**TECHNICAL IMPLEMENTATION:**
- Start from `baseline-resume-data.json` (never from scratch)
- Use role-based context loading for optimization
- Apply format standards from `FORMAT-STANDARDS.md`
- Run `validate-resume.js` checks programmatically
- Generate with proper naming convention

### 🎯 SUCCESS CRITERIA
```markdown
✅ All validation files loaded
✅ Fit analysis completed and confirmed
✅ Scratchpad generated and approved by user
✅ Baseline data used as starting point
✅ Locked content preserved exactly
✅ Validation rules passed
✅ PDF generated with proper naming
✅ Application tracked in system
```

### 📚 COMPLETE REFERENCE SYSTEM
**Full workflow details:** `job-prep/RESUME_APPLICATION_WORKFLOW.md`
**Technical validation:** `job-prep/applications/_resources/VALIDATION_RULES.md`
**Format standards:** `job-prep/applications/_resources/reference/FORMAT-STANDARDS.md`
**Troubleshooting:** See workflow document for common issues and fixes

---

**For Other Use Cases:**

- **Interview prep:** Work normally, no workflow triggered
- **Draft messages:** Work normally
- **Manual tool use:** User can call MCP tools directly anytime
- **Research:** Use tools as needed

**The workflow is ONLY triggered for job applications.**

---

**Company-Specific Interview Prep:**
- ALL materials for ONE company go in `interview-prep/companies/{company-name}/`
- Include: DB schema prep, Python exercises, coding challenges, company research
- NOT scattered in general `practice-problems/`

## User Context

**User:** Viresh Duvvuri
**Background:** Systems engineer transitioning from robotics/embedded systems to AI agent development
**Current Focus:** Actively interviewing for AI Agent Engineer and Robotics Systems Engineer roles
**Tech Stack:** Python, LangChain, RAG systems, PX4, ROS2, embedded systems, LLM integration

### Key Projects
- **GridCOP** (Grid CoOperator) - Agentic AI system for smart grid analytics
- **Drone Log Analysis Tool** (Freefly) - RAG-based diagnostic system for drone crashes
- **PX4 Flight Control** - Real-time embedded systems for autonomous drones

## Repository Workflow

1. **Active Discussions:** Use `scratchpad.txt` for brainstorming and working through ideas
2. **Context Preservation:** Extract valuable content from scratchpad into organized markdown files
3. **Organization:** Keep materials categorized by purpose (job-prep vs interview-prep vs practice)
4. **Portfolio Updates:** Only modify website files when explicitly requested by user
5. **Git Tracking:** Everything is version-controlled; no need for manual .backup files

## Job Application System

**Structured workflow for fast, consistent applications:**

### Quick Apply Process (20 minutes)
1. **Copy template:** `cp -r applications/_template/ applications/{company-role}/`
2. **Fill job-posting.md:** Requirements, fit assessment, customization strategy
3. **Customize resume-data.json:** Summary, highlights, projects tailored for THIS role
4. **Generate resume:** MCP tool → `viresh-duvvuri_YYMMDD-HHMM_position-title.pdf` in application folder
5. **Apply & track:** Update master tracker, network on LinkedIn

### File Organization
- **One folder per application:** `applications/{company-role}/`
- **Three core files:**
  - `job-posting.md` - Job details, metadata, customization notes
  - `resume-data.json` - Resume generation data (for MCP tool)
  - `viresh-duvvuri_YYMMDD-HHMM_position-title.pdf` - Generated resume (timestamped)
- **Resume naming convention (PERMANENT):** `viresh-duvvuri_YYMMDD-HHMM_position-title.pdf`
  - Example: `viresh-duvvuri_251110-1435_ai-agent-developer.pdf`
  - Format: fullname_timestamp_position-title
  - Position title: lowercase, hyphenated (e.g., `ai-agent-developer`)
  - NO generic `resume.pdf` - use timestamped names only
- **Storage location:** All resumes stored INSIDE repo at `applications/{company-role}/`
- **Archive completed apps:** Move to `_archive/` when done

### Resume Customization Strategy
- **Skills-first:** For AI/ML roles (career switcher from embedded)
- **Standard:** For roles aligned with current experience
- **Reorder skills:** Match job posting keywords
- **Select 2-3 projects:** Most relevant to role requirements
- **Quantify impact:** Include metrics from similar domain

### Master Tracker
- **Location:** `applications/README.md`
- **Tracks:** All active applications with status, fit score, next actions
- **Update after:** Every application submission
- **Status workflow:** researching → applied → screening → interview → offer/rejected/archived

### Resources
- **Master resume:** `applications/_resources/master-resume.md` (all content)
- **Customization guide:** `applications/_resources/resume-customization-guide.md`
- **Networking templates:** `applications/_resources/networking-templates.md`
- **Workflow details:** `applications/_resources/application-workflow.md`

## Company-Specific Organization

### Casium (Primary Focus)
**Location:** `interview-prep/companies/casium/`
**Contains:** 23 files + comprehensive README
- Company-specific prep (immigration exercise, satellite exercise, interview guide)
- Database schema materials (9 files: tutorials, practice, exercises)
- Python coding practice (8 files: timed assessments, realistic problems, billing logic)
- Reference solutions (2 files)
- **README.md** - Complete guide explaining every file, learning paths, interview checklist

**Key:** ALL Casium prep materials are in this one folder - DB schema, Python practice, exercises, everything

### Woven
**Location:** `interview-prep/companies/woven/`
**Contains:** Architecture debugging preparation

### Adding New Companies
Create folder at `interview-prep/companies/{company-name}/` and include:
- Company-specific prep docs
- All related practice materials (DB, Python, etc.)
- README.md explaining the materials

## Notes

- User is actively interviewing - materials in `job-prep/` and `interview-prep/` are current
- Archive folder contains completed work but is kept for reference
- Resume has two versions: AI-focused and Robotics-focused (dual-track strategy)
- Scratchpad is the primary collaboration space for job hunting discussions
- **Organization principle:** Company-specific materials stay WITH that company (not scattered in general folders)

## Company-Specific Context Files

For detailed interview preparation context for specific companies, see:
- **Casium:** `interview-prep/companies/casium/onsite-prep/claude.md` (detailed interview prep guide)

**Note:** These are NOT auto-loaded. Use `/casium` slash command to load Casium-specific context.
