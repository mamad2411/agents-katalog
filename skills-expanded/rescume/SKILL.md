---
name: rescume
description: "Intelligent resume tailoring system that 'rescues' your resume for specific job applications. Use when user wants to: (1) Tailor their resume for a specific job description, (2) Build a comprehensive resume database from existing resumes, (3) Optimize resume for ATS (Applicant Tracking Systems), (4) Ensure resume fits on one page while covering all required skills, (5) Get feedback on resume quality for a specific role. Works exclusively with DOCX files. Orchestrates specialized subagents (resume-parser, ats-analyzer, coverage-mapper, content-generator, hr-critic, compression-strategist, interview-conductor) to handle the complete workflow from parsing uploaded resumes to delivering a perfectly tailored one-page resume."
---

# Rescume - Rescue Your Resume

**Tagline**: "Rescue My Resume" - An intelligent multi-agent system for tailoring resumes to specific job descriptions.

## Overview

Rescume is a coordinator skill that orchestrates specialized AI subagents to transform your existing resumes into a comprehensive database, then craft perfectly tailored resumes for each job application. The system ensures all required skills are covered while maintaining professional quality and one-page format.

## Core Workflow

### Phase 1: Initial Setup (One-Time)

**Goal**: Build comprehensive resume database from user's existing resumes

1. **User uploads DOCX resumes** (can be multiple, including job-specific versions)
2. **Call `resume-parser` subagent** for each uploaded file
   - Input: DOCX file path
   - Output: Structured JSON (experiences, skills, projects, education)
   - The subagent uses the `docx` skill and `json-database` skill
3. **Call `interview-conductor` subagent** to deepen understanding
   - Input: Current database state
   - Output: Intelligent follow-up questions
   - Mode: `initial_setup`
4. **Present questions to user** and collect answers
5. **Update database** with new information using `json-database` skill
6. **Database ready** for tailoring jobs

**Data structure** created:
```
data/
├── comprehensive_db/
│   ├── experiences.json
│   ├── skills.json
│   ├── projects.json
│   ├── education.json
│   └── metadata.json
└── uploaded_resumes/
    └── *.docx  (style templates)
```

### Phase 2: Tailoring for a Specific Job

**Goal**: Create optimized one-page resume for target role

#### Step 1: Job Analysis

1. **User uploads job description** (text or URL)
2. **Call `ats-analyzer` subagent**
   - Input: Job description text
   - Output: Required skills (must-have vs nice-to-have), ATS keywords, experience requirements
   - Save to: `data/job_applications/[job_id]/jd_analyzed.json`

#### Step 2: Coverage Mapping & Gap Filling

1. **Call `coverage-mapper` subagent**
   - Input: Database + JD requirements
   - Output: Coverage matrix, gap analysis, prioritized experiences
2. **If gaps exist** (coverage < 100%):
   - Call `interview-conductor` subagent in `gap_filling` mode
   - Present gap-filling questions to user
   - Update database with new experiences
   - Re-run `coverage-mapper` subagent
3. **Repeat until** coverage = 100% or user confirms no more experiences

#### Step 3: Content Generation

1. **Select style template**: Choose any uploaded DOCX for formatting reference
2. **Call `content-generator` subagent**
   - Input: Database, coverage matrix, JD analysis, style template
   - Output: Initial draft DOCX (likely >1 page)
   - Note: Content from database, formatting from template
   - Save to: `data/job_applications/[job_id]/working_resume.docx`

#### Step 4: HR Content Critique

1. **Call `hr-critic` subagent** in `comprehensive` mode
   - Input: Initial draft, JD analysis
   - Focus: Content quality (ignore page limit)
   - Output: Bullet scores, improvement suggestions, priority assignments
2. **Apply HR feedback** to improve content
   - Strengthen weak bullets
   - Add quantification
   - Improve action verbs
   - May make resume longer (that's OK)

#### Step 5: Typst Compilation (NEW in v2.0)

**Key principle**: Typst templates with auto-fit logic handle ALL page fitting automatically.

1. **User selects Typst template** (or use default)
   - Available templates: basic-resume, modern-resume
   - Use `list_templates.py` to show options

2. **Call `typst-renderer` skill** to compile
   - Input: content.json (from Step 4), template name
   - Process: JSON → Typst data → Compile with auto-fit
   - Output: Single-page PDF (guaranteed) or overflow error

3. **Auto-fit logic** (handled by typst-renderer):
   ```
   Start at 11pt font
   If content overflows 1 page:
       Reduce font by 0.5pt steps
       Recompile
       Repeat until fits or minimum (9pt) reached
   If still overflows at 9pt:
       Return error with recommendation
   ```

4. **Handle result**:
   - **Success**: PDF created, proceed to Step 6
   - **Overflow**: Ask LLM to trim 2-3 bullets, regenerate JSON, retry compilation

#### Step 6: Quality Check (SIMPLIFIED in v2.0)

1. **Call `hr-critic` subagent** in `comprehensive` mode
   - Input: content.json (evaluate content, not formatting)
   - Output: Content quality scores, improvement suggestions
   - Focus: Bullet impact, keyword coverage, professionalism

2. **If quality issues identified**:
   - Ask content-generator to improve specific bullets
   - Regenerate JSON
   - Recompile with typst-renderer

3. **Call `hr-critic` subagent** in `final_validation` mode
   - Output: APPROVED / NEEDS_REVISION
   - If APPROVED: Proceed to Step 7
   - If NEEDS_REVISION: Iterate

#### Step 7: Deliver PDF

1. **Save final PDF**: `outputs/[job_id]/final_resume.pdf`
2. **Generate coverage report**: Which skills are demonstrated where
3. **Present to user**: PDF for job application submission

**Note**: Output is PDF only. No DOCX in v2.0 (Typst compiles directly to PDF).

## Available Subagents

These specialized AI agents handle specific tasks. Always call subagents for their expertise:

### 1. resume-parser
- **Purpose**: Parse DOCX resume files → structured JSON
- **When to call**: User uploads a resume
- **Tools**: docx skill, json-database skill
- **Input**: DOCX file path
- **Output**: Structured data (experiences, skills, projects, education)

### 2. ats-analyzer
- **Purpose**: Analyze job descriptions to extract requirements
- **When to call**: User uploads a job description
- **Tools**: Text analysis
- **Input**: Job description text
- **Output**: Required skills, keywords, experience requirements (categorized by importance)

### 3. coverage-mapper
- **Purpose**: Map user's experiences to job requirements
- **When to call**: After JD analysis, to check skill coverage
- **Tools**: coverage-tracker skill, json-database skill
- **Input**: Database + JD requirements
- **Output**: Coverage matrix, gap analysis, experience prioritization

### 4. content-generator
- **Purpose**: Generate tailored resume content as structured JSON
- **When to call**: After coverage is complete (100%)
- **Tools**: json-database skill
- **Input**: Database, coverage matrix, JD analysis
- **Output**: Structured JSON content (NOT DOCX) - see content_schema.json
- **Note**: v2.0 changed to JSON output - no formatting decisions, pure content

### 5. hr-critic
- **Purpose**: Evaluate resume CONTENT quality from HR perspective
- **When to call**: After content generation for quality check
- **Modes**:
  - `comprehensive`: Content quality critique (NOT formatting)
  - `final_validation`: Binary APPROVED/NEEDS_REVISION decision
- **Input**: content.json (structured content), JD analysis, mode
- **Output**: Quality scores, content improvement suggestions, hire probability
- **Note**: v2.0 removed `triage` mode (no longer needed)

### 7. interview-conductor
- **Purpose**: Generate intelligent follow-up questions
- **When to call**: After initial parsing, or when gaps are discovered
- **Modes**:
  - `initial_setup`: Deepen understanding after parsing
  - `gap_filling`: Fill specific skill gaps for a job
- **Input**: Database state, context (mode)
- **Output**: List of questions

## Custom Tool Skills

These are reusable tools that subagents and the coordinator use:

### typst-renderer (NEW in v2.0)
- **Purpose**: Compile structured JSON to single-page PDF using Typst templates
- **Usage**: Render final resume with automatic page fitting
- **Input**: content.json, template name
- **Output**: Single-page PDF (guaranteed via auto-fit)
- **Scripts**: compile.py, json_to_typst.py, validate_pdf.py, list_templates.py

### json-database
- **Purpose**: Manage comprehensive resume database
- **Usage**: Read/write structured data (experiences, skills, projects, education)
- **Operations**: Load, update, query

### coverage-tracker
- **Purpose**: Verify skill coverage is maintained
- **Usage**: Check if all required skills are present in resume
- **Output**: Coverage percentage, missing skills

## Built-in Skills (Already Available)

### docx
- **Location**: `/mnt/skills/public/docx/`
- **Purpose**: Read, create, edit Word documents
- **Used by**: resume-parser, content-generator, compression-strategist

### pdf
- **Location**: `/mnt/skills/public/pdf/`
- **Purpose**: Convert DOCX to PDF
- **Used by**: Final export step

## Key Design Principles (v2.0 Updated)

1. **LLM = Content Writer Only**: LLM generates content (JSON), Typst handles all layout
2. **Typst = Layout Engineer**: Templates with auto-fit guarantee single-page output
3. **No Layout Reasoning**: LLM never thinks about fonts, spacing, word counts, or page limits
4. **HR is Authoritative**: HR Critic decides content quality, not formatting
5. **Coverage is Sacred**: Never sacrifice required skills
6. **Subagent Specialization**: Each subagent has one clear purpose
7. **Progressive Workflow**: Setup once (Phase 1), tailor many times (Phase 2)
8. **Deterministic Rendering**: Same content always produces same PDF

## Page Fitting (v2.0)

**Auto-Fit Logic**: Typst templates automatically adjust font size (11pt → 9pt) to fit content on exactly 1 page.

- **No word counting needed** - Typst measures actual rendered content
- **No guessing** - Compilation is deterministic and fast (~50-200ms)
- **Overflow handling** - If content doesn't fit at minimum font (9pt), system provides specific recommendations ("reduce by 2-3 bullets")

**Result**: Guaranteed single-page output or clear guidance for content adjustment.

## File Structure

```
project_root/
├── data/
│   ├── comprehensive_db/
│   │   ├── experiences.json
│   │   ├── skills.json
│   │   ├── projects.json
│   │   ├── education.json
│   │   └── metadata.json
│   │
│   ├── uploaded_resumes/
│   │   └── *.docx                    # For Phase 1 parsing only
│   │
│   └── job_applications/
│       └── [job_id]/
│           ├── jd_original.txt
│           ├── jd_analyzed.json
│           ├── coverage_matrix.json
│           └── content.json          # NEW: structured content (replaces DOCX)
│
├── templates/                         # NEW: Typst templates
│   ├── basic-resume/
│   │   ├── template.typ
│   │   ├── preview.pdf
│   │   └── metadata.json
│   └── modern-resume/
│       ├── template.typ
│       ├── preview.pdf
│       └── metadata.json
│
└── outputs/
    └── [job_id]/
        ├── final_resume.pdf           # NEW: PDF output (no DOCX in v2.0)
        └── coverage_report.json
```

## Usage Examples

### Initial Setup
```
User: "I want to build my resume database from my existing resumes"
Claude: [Uses rescume skill]
Claude: [Calls resume-parser subagent for each uploaded file]
Claude: [Calls interview-conductor subagent]
Claude: "I have some questions to better understand your experience..."
[User answers questions]
Claude: "Your resume database is ready with 5 experiences, 15 skills, and 3 projects"
```

### Tailor for New Job
```
User: "Tailor my resume for this Senior Data Analyst role at PCI Energy"
Claude: [Uses rescume skill]
Claude: [Calls ats-analyzer subagent]
Claude: [Calls coverage-mapper subagent → finds 90% coverage, missing Kubernetes]
Claude: "This role requires Kubernetes. Do you have container orchestration experience?"
User: "Yes, I used Docker extensively at Company X"
Claude: [Updates database, re-runs coverage-mapper → 100%]
Claude: [Calls content-generator subagent]
Claude: [Calls hr-critic subagent → gets feedback]
Claude: [Applies improvements, now 550 words]
Claude: [Calls compression-strategist subagent iteratively]
Claude: "Draft v3 ready (485 words). Please review: does it look like one page?"
User: "Perfect!"
Claude: [Calls hr-critic in final_validation mode → APPROVED]
Claude: "Here's your tailored resume for PCI Energy [DOCX + PDF]"
```

## Error Handling

- **No DOCX uploaded**: Ask user to upload DOCX files (not PDF)
- **Cannot achieve coverage**: Inform user which skills are missing, suggest alternatives
- **Cannot compress to 1 page**: Call hr-critic in triage mode for strategic decisions
- **User rejects final draft**: Iterate based on specific feedback

## Notes

- **DOCX only**: PDF input not supported (no reliable format preservation)
- **Iterative by design**: System expects multiple rounds of feedback
- **Transparent**: Word count tracking and iteration logs show all decisions
- **Growing database**: Each new job enriches the comprehensive database
- **Privacy**: All data stored locally, never transmitted

## Next Steps After Using This Skill

After successfully tailoring a resume, suggest:
1. "Would you like to tailor this for another job?"
2. "Should I update your database with any new skills you've gained?"
3. "Want to review the coverage report to see which experiences were prioritized?"
