# /apply — Resume Application Workflow

**Job Description:**
$ARGUMENTS

---

If the job description above is empty, respond: "Please paste the job description and I'll run the full fit analysis and resume workflow." Stop here.

---

## PHASE 0: INIT

Load in parallel:
- `job-prep/applications/_resources/resume-profile.json`
- `job-prep/applications/_resources/baseline-resume-data.json`

If either fails, tell the user which file could not be loaded and stop.

Parse the job description to extract company and role. Set:
```
run_id = {role-kebab}_{company-kebab}_{YYMMDD-HHMM}
```

Log:
```bash
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"FILES_LOADED","data":{}}' >> job-prep/applications/_logs/apply-runs.jsonl
```

---

## PHASE 1: FIT ANALYSIS

Calculate the fit score internally using the rubric below. Do not write any files yet.

**Rubric:**

- **Required skills (0–40):** List every required skill from the job description. Mark ✅ HAVE / ❌ MISSING / 🟡 PARTIAL. Score = (fully matched / total required) × 40, rounded.
- **Preferred skills (0–20):** Same approach. Score = (fully matched / total preferred) × 20, rounded.
- **Years of experience (0–20):** Meets/exceeds = 20. Within 1 yr short = 15. 1–2 yrs short = 10. 3+ yrs short = 0.
- **Domain/context (0–20):** Direct match = 20. Same domain different context = 15. Adjacent/transferable = 10. Different domain = 0.

**After calculating, write the following directly to the user as your response — this is your text output for this phase:**

---
## Fit Analysis — {Role} @ {Company}
**Score: {N}/100**

| Category | Score | Notes |
|---|---|---|
| Required skills | {N}/40 | matched {X} of {Y} — missing: {list} |
| Preferred skills | {N}/20 | matched {X} of {Y} |
| Years of experience | {N}/20 | {requirement vs actual} |
| Domain/context | {N}/20 | {reasoning} |

**Gaps:**
- {gap — MINOR / MODERATE / MAJOR}

**Recommendation:** {Strong / Moderate / Weak} Fit

**Proceed with application? (yes / no)**

---

Then log:
```bash
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"FIT_SCORED","data":{"score":<n>,"breakdown":{"required":<n>,"preferred":<n>,"experience":<n>,"domain":<n>},"gaps":[<gaps>]}}' >> job-prep/applications/_logs/apply-runs.jsonl
```

Wait for user response. Do not create any files or continue until the user replies.

**If no:**
```bash
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"CHECKPOINT_FIT","data":{"decision":"rejected"}}' >> job-prep/applications/_logs/apply-runs.jsonl
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"RUN_COMPLETE","data":{"status":"ABORTED_FIT"}}' >> job-prep/applications/_logs/apply-runs.jsonl
```
Stop.

**If yes:**
```bash
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"CHECKPOINT_FIT","data":{"decision":"approved"}}' >> job-prep/applications/_logs/apply-runs.jsonl
```
Continue to Phase 2.

---

## PHASE 2: SETUP + CUSTOMIZATION

Now create the application files and generate customizations.

**2a — Create files:**

Create `job-prep/applications/{run_id}/job-posting.md`:
```markdown
# {Role} @ {Company}
**Date:** {YYYY-MM-DD}

## Fit Analysis
**Score:** {N}/100

| Category | Score | Notes |
|---|---|---|
| Required skills | {N}/40 | {notes} |
| Preferred skills | {N}/20 | {notes} |
| Years of experience | {N}/20 | {notes} |
| Domain/context | {N}/20 | {notes} |

**Gaps:** {gaps}
**Recommendation:** {recommendation}

---
## Job Description
{full raw job description}
```

Create `job-prep/applications/{run_id}/scratchpad.md` with Status: draft and these sections filled in:
```markdown
# {Role} @ {Company}
**Date:** {YYYY-MM-DD HH:MM}
**Fit Score:** {N}/100
**Status:** draft

---

## Summary
{customized summary for this role}

---

## Skills Order
1. {most relevant section}
2. {section}
3. {section}
4. {section}
5. {section}

---

## {Customizable company from resume-profile.json} Bullet 1
{best variation from baseline _variations for this role}

---

## Projects
1. {project name from baseline}
2. {project name from baseline}
3. {project name from baseline}

---

## Notes

```

**Customization rules:**
- Summary: rewrite for this role, lead with most relevant experience, match JD language where accurate
- Skills order: reorder section names to put most relevant categories first (keep all keywords unchanged)
- Bullet: choose or write the best variation from `baseline-resume-data.json` `_variations` for this role
- Projects: select exactly 3 from `baseline-resume-data.json` projects, most relevant to this role

**2b — Write the following directly to the user as your response:**

---
Scratchpad created at `job-prep/applications/{run_id}/scratchpad.md`

Here's what I customized for this role:

**Summary:**
{summary text}

**Skills order:** {section 1} → {section 2} → {section 3} → {section 4} → {section 5}

**{Company} Bullet 1:**
{bullet text}

**Projects:** {project 1}, {project 2}, {project 3}

You can edit `scratchpad.md` directly or tell me what to change. Say **approve** to generate the PDF.

---

Then log:
```bash
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"SCRATCHPAD_WRITTEN","data":{"path":"job-prep/applications/<run_id>/scratchpad.md","iterations":1}}' >> job-prep/applications/_logs/apply-runs.jsonl
```

Wait for user response. Do not generate PDF until the user approves.

**If change requested:** edit only the requested section(s) in `scratchpad.md`, confirm what changed in one sentence, show the updated section, wait again. Increment iterations in the next log entry.

**If approved:** update `scratchpad.md` Status: draft → approved, then log:
```bash
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"CHECKPOINT_SCRATCHPAD","data":{"decision":"approved"}}' >> job-prep/applications/_logs/apply-runs.jsonl
```

**If no / stop:**
```bash
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"CHECKPOINT_SCRATCHPAD","data":{"decision":"rejected"}}' >> job-prep/applications/_logs/apply-runs.jsonl
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"RUN_COMPLETE","data":{"status":"ABORTED_SCRATCHPAD"}}' >> job-prep/applications/_logs/apply-runs.jsonl
```
Stop.

---

## PHASE 3: GENERATION

Read `scratchpad.md`. Extract: Summary, Skills Order, bullet text(s), 3 project names.

**Build resume JSON internally (do not save to disk):**
- Start from `baseline-resume-data.json`
- Replace `basics.summary` with scratchpad Summary
- Reorder `skills` array to match scratchpad Skills Order (keywords unchanged)
- For each `customizable_bullets` entry in `resume-profile.json`: replace `work[company].highlights[index]` with scratchpad bullet
- Replace `projects` with the 3 full project objects from baseline matching scratchpad names (do not rewrite content)
- Strip all keys starting with `_`

**Validate:**

For each `locked_bullets` entry in `resume-profile.json`, compare generated JSON `work[company].highlights[index]` against the same position in `baseline-resume-data.json` verbatim. If any mismatch:
```bash
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"VALIDATION_FAILED","data":{"errors":["<detail>"]}}' >> job-prep/applications/_logs/apply-runs.jsonl
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"RUN_COMPLETE","data":{"status":"FAILED_VALIDATION"}}' >> job-prep/applications/_logs/apply-runs.jsonl
```
Show the exact mismatch to the user. Stop.

Also verify bullet counts match `resume-profile.json` `bullet_counts` exactly.

On pass:
```bash
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"VALIDATION_PASSED","data":{}}' >> job-prep/applications/_logs/apply-runs.jsonl
```

**Generate PDF:**
```
mcp__resume-generator__generate_resume(
  resumeData: <generated JSON>,
  folderPath: "<run_id>",
  filename: "resume_<username>_<role-kebab>"
)
```
`username` from `resume-profile.json`. `role-kebab` = role lowercase hyphenated.

If MCP fails:
```bash
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"PDF_FAILED","data":{"error":"<error>"}}' >> job-prep/applications/_logs/apply-runs.jsonl
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"RUN_COMPLETE","data":{"status":"FAILED_PDF"}}' >> job-prep/applications/_logs/apply-runs.jsonl
```
Fallback: `node generate-resume-standalone.mjs`

On success — update `scratchpad.md` Status: approved → generated, then log:
```bash
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"PDF_GENERATED","data":{"filename":"resume_<username>_<role-kebab>.pdf"}}' >> job-prep/applications/_logs/apply-runs.jsonl
echo '{"ts":"<now>","run_id":"<run_id>","company":"<company>","role":"<role>","folder":"<run_id>","event":"RUN_COMPLETE","data":{"status":"COMPLETED"}}' >> job-prep/applications/_logs/apply-runs.jsonl
```

Write to the user:
```
✅ Done.

  job-prep/applications/{run_id}/
    job-posting.md
    scratchpad.md  (Status: generated)
    resume_{username}_{role-kebab}.pdf

To update: edit scratchpad.md and say "regenerate".
```

---

## Hard Rules

- Always build from `baseline-resume-data.json` — never generate resume content from scratch
- Locked bullets per `resume-profile.json` `locked_bullets` — never modify, validated verbatim
- Job titles, company names, dates — never change
- Education, contact info — never change
- Bullet counts must match `resume-profile.json` `bullet_counts` exactly
- Projects must exist in `baseline-resume-data.json` — never invent projects
- No user approval at Phase 2 = no PDF
