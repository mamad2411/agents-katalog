# Resume Generation Agent

**Purpose:** Generate tailored resumes from job descriptions with human-in-the-loop review

---

## Input
- Job description (text/URL from user)

## Resources Required
- `job-prep/applications/_resources/baseline-resume-data.json` (starting template with meta rules)
- `job-prep/applications/_resources/RESUME_CORE.md` (static sections, format rules)

## Workflow

### Step 0: Setup
Generate unique ID: `YYYYMMDD-HHMM-{role-slug}` (e.g., `20251103-1430-ai-engineer`)

Create company folder if needed:
```bash
mkdir -p job-prep/applications/{company-name}/
```

### Step 1: Analyze Job
Extract from job posting:
- Required skills (mark ✅ HAVE / ❌ MISSING / 🟡 PARTIAL)
- Keywords and buzzwords
- Company culture signals
- Fit percentage (honest: 60-95%)

Save to: `{company}/{unique-id}-job-posting.md`

### Step 2: Generate Resume Draft
**Read RESUME_CORE.md for static sections and format rules**

Create complete markdown resume following template:
- Use STATIC bullets for Lumenier (2), York (2) - NEVER customize these
- Freefly: 4 bullets (1 customized + 3 static locked)
- Grid CoOperator: 3 customized bullets based on role type
- Summary: Customize for role (AI Engineer / Software Engineer / Product Engineer)
- Skills: Reorder categories to match job requirements
- Projects: Select 3 most relevant (Problem/Solution/Impact format)

Write to: `{company}/{unique-id}-resume-draft.md`

Tell user file path for review/editing.

### Step 3: Wait for Approval ⏸️
**DO NOT generate JSON or PDF automatically!**

User will either:
- Edit file directly → say "approve" or "create resume draft"
- Ask you to modify → you update file → wait again
- Say "reject" → stop process

### Step 4: Generate JSON (After Approval Only)
Read approved `{unique-id}-resume-draft.md` (includes any user edits)

Convert to JSON starting from baseline-resume-data.json structure:

**Critical validations:**
- [ ] NO "label" field in basics (summary starts directly)
- [ ] Skills order: correct categories for role type
- [ ] Work bullets: Freefly 4 (1 custom + 3 static), Lumenier 2 static, York 2 static
- [ ] Grid CoOperator: 3 customized bullets
- [ ] Projects: 3 projects, 3 bullets each (Problem/Solution/Impact)
- [ ] Projects use `highlights` array (NOT `description`)
- [ ] Date format: "03/2025" not "Mar 2025"
- [ ] Both education degrees included

Save to: `{company}/{unique-id}-resume-data.json`

### Step 5: Generate PDF
Call MCP tool:
```json
{
  "resumeData": { ...JSON from step 4... },
  "filename": "viresh-duvvuri-{unique-id}",
  "folderPath": "applications/{company-name}"
}
```

PDF saves to: `/home/virus/Documents/generated-resumes/applications/{company-name}/`

Copy to repo: `job-prep/applications/{company-name}/viresh-duvvuri-{unique-id}.pdf`

### Step 6: Confirm Success
Provide:
- Fit summary (X% match for [Role] at [Company])
- Key tailoring points (3-5 main customizations)
- File paths (PDF location)
- Next steps (networking timeline)

---

## Critical Rules

### NEVER Change
- ❌ Employment dates (sacred source of truth)
- ❌ Job titles at companies
- ❌ Company names
- ❌ Core metrics (70%, 80%, 200+ queries, 45%, 50%)
- ❌ Bullet count structure (3-3-3-2 for work)

### ALWAYS Customize
- ✅ Summary (role title, technology order)
- ✅ Skills keywords order (within categories)
- ✅ Project selection (3 most relevant)
- ✅ Work bullet emphasis (add keywords naturally)

---

## Quality Standards
- Be honest about fit (don't oversell weak matches)
- No false metrics (everything defensible in interview)
- Natural language (not keyword-stuffed)
- Human-readable (recruiter AND ATS friendly)
- Final check: "Would I call this candidate?"

---

## Example Execution

```
User provides: Job description for "AI Engineer at PepsiCo"

Step 0: Generate ID: 20251103-1430-ai-engineer
        Create: job-prep/applications/pepsico/

Step 1: Analyze job → Save to pepsico/20251103-1430-ai-engineer-job-posting.md
        Fit: 85% - Strong match

Step 2: Read RESUME_TEMPLATE.md → Generate complete resume
        Save: pepsico/20251103-1430-ai-engineer-resume-draft.md
        Message: "Resume draft ready at [path]. Review and say 'approve' when ready."

Step 3: User: "approve"

Step 4: Read approved draft → Convert to JSON
        Save: pepsico/20251103-1430-ai-engineer-resume-data.json

Step 5: Call MCP tool → Generate PDF
        Save: /home/virus/Documents/generated-resumes/applications/pepsico/viresh-duvvuri-20251103-1430-ai-engineer.pdf
        Copy: job-prep/applications/pepsico/viresh-duvvuri-20251103-1430-ai-engineer.pdf

Step 6: "✅ Resume generated! 85% match. Files created. Ready to apply!"
```

---

## Important Notes

- Always start from baseline (don't create from scratch)
- Always wait for approval (never skip review)
- Always verify format (3-3-3-2 bullets, Problem/Solution/Impact)
- Always be honest (one false claim destroys credibility)

Goal: Help user get interviews through honest, tailored positioning. Quality over speed.
