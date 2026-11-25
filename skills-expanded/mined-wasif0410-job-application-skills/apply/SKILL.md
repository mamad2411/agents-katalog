---
name: apply
description: Build a complete application package for one job posting in a single run. It MUST call the /resume-tailor skill and then the /cover-letter skill through the Skill tool every run (never from memory), then adds copy-paste application-form answers, zips everything into one file and logs it in the applications.csv tracker. The user's details come from tailor-profile.md and cover-letter-profile.md, so it works for anyone. Use this when the user types /apply, or pastes a job description/link and says "make the package", "do the full application", "resume and cover letter for this", "get me ready to apply". For a resume alone use resume-tailor; for a letter alone use cover-letter. Also use it to update a posting's status in the tracker ("I applied to X", "X rejected me", "mark X as interviewing").
---

# Apply

> ## ⚠️ MANDATORY: /apply CALLS TWO SKILLS. EVERY RUN. NO EXCEPTIONS.
> 1. **Call `/resume-tailor`** with the Skill tool: `Skill(skill: "resume-tailor", ...)`, at step 3.
> 2. **Call `/cover-letter`** with the Skill tool: `Skill(skill: "cover-letter", ...)`, at step 4.
>
> These are two real tool calls, made in this order, on every `/apply` run. "I already read it earlier", "I remember what it says" and "it's faster to skip" are **not** valid reasons. Writing the resume or letter without these calls is a failed run, even if the files look right. Working from memory is how required end-of-run steps get skipped. If the Skill tool is unavailable, Read each skill's `SKILL.md` in full instead and say so in the hand-off.

One job description in → one application package out, no check-ins along the way.

The two skills it runs stay independent and keep working on their own. This skill only decides the order, makes them share one research decision, checks that they agree with each other, and packages the result.

## 0. Workspace and profiles

- **Personal information lives only in the user's workspace files, never in any skill.** Never write a user's details into a skill folder.
- **Workspace:** the folder Claude is working in, organized in the standard layout from resume-tailor §0:
  ```
  checkpoint.md · resumes/ · personal-info/ (tailor-profile.md, cover-letter-profile.md, cover-letter-examples.md) · job-tracker/applications.csv · tailored/<posting>/
  ```
  Every file named in this skill without a folder lives at the path that table gives.
- **First run (onboarding), before step 1.** Check for:
  - the standard folders and `checkpoint.md`
  - exactly one original resume in `resumes/` (if there are several, ask which one is the ground truth and offer to move the others out)
  - `personal-info/tailor-profile.md` with an Identity section
  - `personal-info/cover-letter-profile.md`
  - `job-tracker/applications.csv`

  If any are missing, tell the user in **one** message: show the layout tree, list what's missing and what each piece is for, and ask: *"Should I set this up and create them for you?"* On yes:
  - Create the folders and `checkpoint.md` (resume-tailor §0, step 0).
  - Offer to move loose resume files into `resumes/`.
  - Create the profiles as resume-tailor §0 and cover-letter §0 describe: pre-fill from the resume, then ask for the rest in one combined message.
  - Create `job-tracker/applications.csv` with the header row from step 8.

  Only start the application once the profiles exist or the user has declined. If they decline, ask for the missing details inline and don't save them.
- **Identity** (name, file prefix, contact, school, degree, graduation date, work authorization, location) comes from the **Identity** section of `tailor-profile.md`. Use it for every file name, form answer and header. **Never hard-code a person's details in this skill.**
- **Letter style** comes from `cover-letter-profile.md`, which the cover-letter skill reads and creates if missing.
- `<Prefix>` below means the Identity file prefix (e.g. `JaneDoe`).
- `<JobName>` means `<Company>_<RoleTag>`, the short name defined in resume-tailor §7 (e.g. `Acme_SWEWeb`, `Globex_SWE`). Every resume and cover letter file carries it: `<Prefix>_Resume_<JobName>.pdf`, `<Prefix>_CoverLetter_<JobName>.pdf`.

## 1. Set up the posting (once)

1. Fetch the posting (or take the pasted text). Save it as `tailored/<Company>_<Role>_<Term-or-ReqID>/jd.md` with the source URL at the top.
2. Pin down the knockouts: exact term and start date, length, location, in-office or hybrid, grad-date rule, work authorization / visa, pay, and required documents (e.g. a transcript). Compare them with the user's Identity: authorization, location and graduation date. If a version of the role in the user's own country exists and fits better (no visa, matching term), use it and say so.
3. If `applications.csv` already has this posting, reuse its folder.

## 2. Research decision (once, shared)

**Research only if the JD is thin**, using the thin-JD test in resume-tailor §2 (fewer than ~4 named tools, no duties list, no requirements list, under ~150 words of role content, or a vague title).

- **JD is detailed → no web research.** Write `research.md` with the decision ("Research: skipped, because the JD is detailed (<why>)"), the knockouts, the stack and duties taken from the JD, and the company facts from the JD's own "About" paragraph. The cover letter's hook comes from those facts.
- **JD is thin → deep research** as in resume-tailor §2 (real stack, product vocabulary, other versions of the posting, values / hiring guide, interview process, past interns), plus the cover letter's hook and any local tie, all with source links.

Both skills read `research.md` instead of searching again, so the resume and letter tell the same story.

## 3. Resume: MANDATORY call to /resume-tailor

**Call the Skill tool now (required):** `skill: "resume-tailor"`, `args: "Called from /apply. Folder: tailored/<folder>/ (jd.md + research.md already there; reuse them). No questions mid-run."` Then follow the loaded skill fully (grounding, keyword mapping, bullets, page fill, verify, report, keyword tables, profile updates), with these changes for this run:
- **No questions mid-run.** Anything resume-tailor would ask (a missing number, a name) goes into the kit's *Questions for you* list instead; write the bullet from what's known. A confirmed fact with no employer attached is placed into the most plausible role, not asked about.
- Its §8 keyword tables are **held for the hand-off** (step 9). They are never dropped. They stay resume-only: no cover letter column.

Output: `resume.tex`, `<Prefix>_Resume_<JobName>.pdf`, `report.md`.

## 4. Cover letter: MANDATORY call to /cover-letter

**Call the Skill tool now (required):** `skill: "cover-letter"`, `args: "Called from /apply. Folder: tailored/<folder>/ (jd.md, research.md and the tailored resume are already there)."` Then follow the loaded skill fully. It reuses `research.md` and must ground itself in **the tailored resume that was just built** as well as the original resumes. The letter can't claim anything the resume doesn't support, and it should lean on the same experiences the resume leads with.

Output: `<Prefix>_CoverLetter_<JobName>.tex`, `<Prefix>_CoverLetter_<JobName>.pdf`.

Always produce the letter, even when the portal has no cover-letter field (note that in the kit; the user decides whether to upload it).

## 5. Cross-check (resume ↔ letter ↔ posting ↔ profile)

Read the text extracted from both final PDFs and confirm:
- [ ] titles, employers, dates and numbers in the letter match the resume exactly
- [ ] every tool named in the letter appears somewhere on the resume
- [ ] the letter's availability and term match the posting, and the resume's graduation date satisfies any grad-date rule
- [ ] the name and contact line are identical on both, and match Identity
- [ ] both are exactly one page, named `<Prefix>_Resume_<JobName>.pdf` and `<Prefix>_CoverLetter_<JobName>.pdf`, with no `{{` placeholders left
- [ ] the letter passes cover-letter §5b:
  - exact header format ("Start Availability: <Month> <Year>" / length only)
  - no bold
  - P2 follows the technical-background pattern (alignment line, languages and tools, current-role work; no stories or metrics)
  - no employer named in more than 2 paragraphs
  - the goodbye is exactly the two-sentence pattern (thanks, then "I'd welcome the chance… reach me at…"), with no graduation date and no semicolons
  - no forced resume keyword claimed as experience in the letter
- [ ] the resume's Technical Skills section is tailored to this posting (posting keywords first, irrelevant skills dropped, each category on one line)

Fix any mismatch in whichever file is wrong, recompile, recheck.

## 6. Application kit

Write `tailored/<folder>/application-kit.md`, the copy-paste sheet for the form. Fill every value from Identity, the posting and the two documents:

```markdown
# Application kit: <Company>, <Role> (<Term>, <Location>)
Posting: <url>   |   Deadline/status: <rolling / date>   |   Pay: <range>

## Form answers
- Name / email / phone: <Identity>
- LinkedIn / GitHub: <Identity>
- School / degree / grad date: <Identity>
- Work authorization: <from Identity, for this posting's country; answer honestly>
- Sponsorship required: <yes/no for this location, from Identity>
- Start date / term: <matches the letter>
- Relocation / in-office: <what the posting requires vs. Identity's location>
- Required documents: <resume, transcript, etc.; flag anything not in the package>
- <each screening question the posting or its form asks, with a suggested answer>

## Short answers (for text boxes)
- Why <Company>? (2–3 sentences, built from the letter's hook, not copied word for word)
- Tell us about a project you're proud of (3–4 sentences, from the letter's project paragraph)

## Before you submit
- Inferred and forced claims to check: <combined list from report.md and the cover-letter note>
- Questions for you: <anything that needed a number/name/story; the sentence it would improve>
- Interview prep: <format and tips; from research if done, otherwise from the JD>
```

## 7. Package

1. Zip the three deliverables into one file in the posting's folder: `<Prefix>_<JobName>_Application.zip`, containing `<Prefix>_Resume_<JobName>.pdf`, `<Prefix>_CoverLetter_<JobName>.pdf` and `application-kit.md`.
   - PowerShell: `Compress-Archive -Path <Prefix>_Resume_<JobName>.pdf,<Prefix>_CoverLetter_<JobName>.pdf,application-kit.md -DestinationPath <zip> -Force`
   - Bash/macOS/Linux: `zip -j <zip> <Prefix>_Resume_<JobName>.pdf <Prefix>_CoverLetter_<JobName>.pdf application-kit.md` (on Windows, MiKTeX ships a `zip`)
2. Delete LaTeX leftovers (`.aux/.log/.out`).

## 8. Tracker

Add (or update) one row in `job-tracker/applications.csv`. Create it with this header if missing:

```
date_prepared,company,role,term,location,req_id,posting_url,folder,status,date_applied,next_step,notes
```

- `status` is one of `prepared`, `applied`, `oa`, `interviewing`, `offer`, `rejected`, `withdrawn`. New packages start as `prepared`.
- Quote any field containing a comma. Dates as YYYY-MM-DD.
- When the user reports progress ("applied to X today", "got an OA from Y"), update that row's `status`, `date_applied` and `next_step`. No package rebuild needed.
- After writing, show the user the row(s) that changed.
- **Update `checkpoint.md`** (workspace root) in the same step: refresh the Status counts (prepared / applied / interviews) from the tracker and add one Log line: "<date>: prepared <Company>, <Role> (<term>)". When the user reports progress, update the counts and log that too.

## 9. Hand-off

Send the resume PDF and the cover letter PDF (SendUserFile, display render), then a short note:
- the posting, term and location targeted (and any switch, e.g. to a home-country version)
- **the research decision**, one line: "Research: skipped, because the JD is detailed (<why>)" or "Research: done, because the JD is thin (<why>)". Only when research was done, add 3–5 bullets on the most valuable insights, with sources.
- **the keyword tables from resume-tailor §8** (always required): Table 1 holds every keyword actually in this JD, each with a quoted JD source, a priority (Mandatory / Critical / Important / Nice-to-have / Soft), Used? ✅🟡❌, and where it sits on the **resume** (resume only, no cover letter column; a keyword only in the letter counts as ❌). Then the JD-only coverage line and the forced-keyword list. Table 2 holds extra keywords from research or the profile, each with its source, or the line "none: research skipped". Check them against the final resume PDF.
- where the zip is
- the **Before you submit** list from the kit
- one line on what was added to `tailor-profile.md` and `cover-letter-profile.md`

Keep the rest short; the details live in `report.md` and `application-kit.md`.

### Done check (run before sending the hand-off)
The run is not finished until every box is true. If one fails, go back and do that step instead of mentioning it as a gap.
- [ ] `resume-tailor` was loaded with a Skill tool call this run
- [ ] `cover-letter` was loaded with a Skill tool call this run
- [ ] every name, contact detail and file prefix came from the Identity section, and no `{{` placeholders remain in either PDF
- [ ] `report.md`, `research.md`, `application-kit.md`, both `.tex` and both PDFs exist in the folder, and both PDFs are 1 page
- [ ] the zip was rebuilt **after** the last edit to any of its three files
- [ ] the tracker row was added or updated and shown to the user, and `checkpoint.md` Status + Log were updated
- [ ] the hand-off contains the keyword tables, the coverage line and the forced-keyword list
- [ ] the thin-JD test was applied and the research decision is stated. If research was done, it covered resume-tailor §2 (including interview process and past interns) and the hand-off lists the key insights
