---
name: cover-letter
description: Write a one-page cover letter for one specific job posting and hand back the finished PDF (LaTeX, same header as the user's Jake's-template resume) in a single pass. The user's identity comes from tailor-profile.md and their letter style from cover-letter-profile.md, so the skill works for anyone. Use this whenever the user pastes a job description or link and asks for a cover letter — "write a cover letter for this", "make me a cover letter", "/cover-letter" — or asks for edits to a cover letter this workflow produced. Do not use it for resumes (that's resume-tailor).
---

# Cover Letter

Job description in → finished one-page cover letter (`.tex` + `.pdf`) out. **No intermediate check-ins, no version snapshots.** Research, grounding and humanizing happen silently; the user sees the finished letter plus a short note.

## Hard rules (every user, every letter; no profile can override these)

1. **Header format:** `Start Availability: <Month> <Year>` (always with a year), then a line holding **only a length** ("4 months", "16 weeks", "4/8/12 months"). Never a sentence or a date range.
2. **Paragraph 2 is the user's technical background:**
   - It opens by saying how their background fits the company's engineering work.
   - It names the relevant languages and tools as a short prose list, plus any relevant coursework.
   - It shows those skills in use in the user's **current role** (what they build, with which tools).
   - Stories, results and metrics are saved for paragraph 4.
3. **Goodbye:** exactly 2 sentences, using this pattern: "Thank you for your time and consideration." then "I'd welcome the chance to discuss how I could contribute to <Company>, and you can reach me at <email> or <phone>." Nothing else goes in it: no graduation date, no logistics, no employer names, no semicolons. The only exception is a third sentence when the posting requires a transcript ("I've included my transcript with my resume.").
4. **No bold anywhere in the letter.** Bold keywords belong on the resume only.
5. **No employer named in more than 2 paragraphs.** The in-depth job is told in paragraph 4 only.
6. **No invention:**
   - no forced resume keyword claimed as experience
   - no made-up process, reason, decision or story
   - every sentence is backed by the resume, the profile, the repos or the posting
7. **Plain, correct English:** one idea per sentence, no unrelated facts glued together, under ~30 words per sentence, read-aloud checked.
8. **Only the user's own words go into their profile,** never the run's own choices.

These are checked line by line in §5b before every build.

Why this shape: tailored letters get ~31% more callbacks than generic ones (ResumeGo, 7,287 applications). In a study of Canadian co-op students, letters with more **detail, clarity and structure** got more interviews per application (Wingate et al., 2025). Since AI cover-letter tools spread, simply mirroring the posting's keywords lost about half its value, while real specifics and editing effort still pay (arXiv 2509.25054). So every rule below pushes toward *specific, checkable, first-person detail* and away from restating the resume.

## 0. Workspace and profiles

The **workspace** is the folder Claude is working in: the one holding the user's original resume and `tailor-profile.md` (the same folder resume-tailor uses). Everything is read from and written to it.

**Personal information lives only in the user's workspace files, never in this skill.** The skill folder holds rules and blank templates only. Never write a user's name, contact details, employers or letters into any file under the skill folder.

**Workspace layout:** the standard layout in resume-tailor §0 (`checkpoint.md`, `resumes/`, `personal-info/`, `job-tracker/`, `tailored/`). The profile files below live in `personal-info/`, original resumes in `resumes/`, and each letter in `tailored/<posting>/`. If the layout doesn't exist yet, offer to set it up as resume-tailor §0 describes.

Three workspace files in `personal-info/` drive everything personal:

| File | What it holds |
|---|---|
| `tailor-profile.md` → **Identity** section | name, file prefix, phone, email, LinkedIn, GitHub, city, school, degree, graduation date, work authorization |
| `cover-letter-profile.md` | header lines and default availability, sign-off, paragraph structure and word targets, how to introduce each employer, voice rules and corrections, local tie, story bank |
| `cover-letter-examples.md` (optional) | the user's own approved letters, for their voice |

**First run (onboarding).** Check for these files before drafting. Don't create anything silently:
1. **No `tailor-profile.md` (or no Identity section):** follow resume-tailor §0. Offer to create it, pre-fill it from the resume, and ask for the rest in one message.
2. **No `cover-letter-profile.md`:** say something like: *"You don't have a `cover-letter-profile.md` yet. It holds how your letters look and sound: the header, sign-off, structure and how to introduce each employer. Should I create it for you? I'll start from sensible defaults and your resume, then ask a few questions."* On yes:
   - Copy `assets/cover_letter_profile_template.md` to `personal-info/cover-letter-profile.md`. Fill in the sign-off name, the employer-intro table (one row per employer and title on the resume) and the city.
   - Then ask in **one** message, with defaults:
     - the availability header ("Start Availability: <month year>" plus term lengths, or none)
     - the greeting (default "Dear Hiring Manager,")
     - the sign-off (default "Sincerely,")
     - whether the 5-paragraph default structure is fine or they want a different one
     - any phrases they never want
     - a real story or two for paragraph 4 (optional)
   - Write the answers in and show the user the result.
3. If the user declines, write the letter from the defaults in this skill and the Identity details, and ask for anything missing inline, without saving it.

**Keep the profile current.** When the user states a new letter preference or correction, write it into `cover-letter-profile.md` in the same turn, and a new story into its Story bank. When they approve a letter, offer to add it to `cover-letter-examples.md`.

**Only the user's own words go into the profile.** Never record your own choices from a run as preferences or "corrections" (e.g. "header has no year when the posting gives none", "use the <old internship> as a <city> tie"). If a run needs a judgment call, make it for that letter only and mention it in the note.

## 1. Inputs (read, don't ask)

- **The posting.** If `tailored/<Company_Role>/jd.md` exists, use it. Otherwise fetch the posting and save it as `jd.md` in a new `tailored/<Company_Role>/` folder. Note the exact term, location, start date, grad-date requirement, whether a transcript is required, and whether a version of the role in the user's own country exists.
- **The user's ground truth:** the tailored resume in the same folder if there is one, `tailor-profile.md` (confirmed facts, titles), and `personal-info/source-cache.md` (the resume's text + repo facts, see resume-tailor §1). If resume-tailor already read these earlier in this conversation, don't read them again. Fetch a repo only if the cache has nothing on it, then add it to the cache. **Never invent experience, tools, numbers or stories.**

## 2. Research (only if the JD is thin)

If the posting's folder already has `research.md` (from `/apply`) or a research decision in `report.md`, use it and don't search again.

Otherwise apply the thin-JD test from resume-tailor §2 (fewer than ~4 named tools, no duties list, no requirements list, under ~150 words of role content, or a vague title):
- **JD is detailed → no web research.** Build the hook from the JD's own company paragraph and role description: a specific fact the posting states, tied to something the user built. Don't cite anything outside the posting.
- **JD is thin → research**, with sources:
  - **One hook:** a recent, checkable company detail (engineering blog post, launch, benchmark, partnership, new office) that connects to something the user actually built. Read the source; don't cite what you haven't read.
  - **What they hire for:** values page, hiring guide, the team's real stack.
  - **Local tie:** e.g. an office in the user's city, if real.

## 3. Format

Follow `cover-letter-profile.md` for style (header defaults, sign-off, structure, employer intros, voice). Where it's silent, use the defaults below. **The Hard rules at the top of this skill always win, even over a profile that says otherwise.**

**Header:** the resume header (name + one contact line), then exactly these lines, each on its own line, in this exact format:

```
<Mon D, YYYY>                         ← today's date, e.g. Oct 5, 2026
Start Availability: <Month> <YYYY>    ← e.g. Start Availability: September 2027
<length>                              ← ONLY a length, e.g. 4 months · 8 months · 16 weeks · 4/8/12 months
Dear Hiring Manager,
```

- **Line 2 always has a month AND a year.** If the posting gives a month but no year, use the next time that month comes around after today's date. If the posting gives no start at all, use the profile's default.
- **Line 3 is only a length**, never a sentence or a date range. Write "4 months", not "4-month work term, September to December". If the posting's term fits the profile's default list (e.g. 4 months and the default is 4/8/12 months), the profile's default line may be kept. If it doesn't fit, write the posting's length.
- **The term must match the posting.** If the profile's default contradicts it, use the posting's term and say so in the note.
- No company address block unless the profile asks for one.

**Body (default structure):** five paragraphs, ~430–500 words, one page.

| # | Paragraph | Words | Rules |
|---|---|---|---|
| 1 | Hook about the company | 65–80 | Role, location, term. Then one specific company detail tied to something the user built: from the posting when the JD is detailed, from research when it's thin. If the posting checks the graduation date, add it here as its own short sentence ("I graduate in December 2027."). |
| 2 | Technical background | 90–110 | **The pattern** (see `references/examples.md`):<br>(1) "My technical background aligns closely with <Company>'s <area> work."<br>(2) "I have experience with <the posting-relevant languages, frameworks and tools the user actually has>." This is a short prose list.<br>(3) Optionally, relevant coursework or adjacent familiarity, tied to the company's stack ("I also have Haskell coursework experience, which makes <Company>'s backend stack particularly interesting to me.").<br>(4–5) "In my current role as <title> at <Employer>, I build…": what the user builds there day to day, naming the tools, to show the skills in real use.<br>**No stories, results or metrics here;** those are for P4. Only tools the user has actually used. No "I want to learn X". |
| 3 | One project | 100–120 | Opens plainly: "I built <Project>, …". Stack, approach, real numbers from the repo, one thing the user noticed or decided, then the posting task it maps to. |
| 4 | Work experience (most important) | 160–180 | One job told in depth (the most relevant), the others one sentence each. Stories, results and metrics live here. Introduce every employer the way the profile's employer-intro table says. End with curiosity about the company's users. |
| 5 | Goodbye | exactly 2 sentences | "Thank you for your time and consideration." / "I'd welcome the chance to discuss how I could contribute to <Company>, and you can reach me at <email> or <phone>." Add a third sentence only if the posting requires a transcript: "I've included my transcript with my resume." **Nothing else: no graduation date, no logistics, no employer names, no semicolons.** |

## 4. Writing rules (general; the profile can add more)

- **First person, plain openers.** Every paragraph's first sentence has the user as the actor and carries the paragraph's point on its own (readers skim first sentences).
- **Introduce employers with the role,** never a bare company name the reader may not know.
- **No invention: the letter is stricter than the resume.** Every sentence must be backed by the original resume (via the source cache), the profile (confirmed facts, Story bank), the repos, or the posting itself. In particular:
  - **Forced resume keywords never appear in the letter as experience.** If the resume placed a keyword without evidence (marked "forced" in the report), the letter must not claim it ("I used Copilot on those automations" is banned). Leave it out of the letter entirely.
  - **No invented process, reasons or decisions** ("Before building anything, I mapped the steps with staff…"). Only use a reason or decision when the resume, profile, Story bank or repo states it. Otherwise describe what was built and the result.
- **Story slot:** paragraph 4 is strongest with one real incident (a bug fixed, a call made). Use one only if it's in the profile's Story bank or the user gave it. Otherwise write from facts and, in the note, name the sentence a real story would replace.
- **Don't repeat employers.** Each employer is named in at most 2 paragraphs. The in-depth job is told in P4 only. P1 may mention it once in passing; P2 names the current employer once (where the skills are in use); P5 names no employer. If one employer is the only match for the posting, still spread the evidence: use P2 for other employers' skills and P3 for a project.
- **Vary the shape.** Don't reuse the same project and angle as the user's recent letters (check the workspace's `cover-letter-examples.md` and the other `tailored/*/<FilePrefix>_CoverLetter_*.tex` letters).
- **No bold anywhere in the letter.** Bolding keywords is for the resume only. A letter is plain prose.
- **Banned** (plus anything the profile adds): "I am writing to express", "passionate", "proven track record", "detail-oriented", "leverage", em dashes, semicolons, bullet-point skill lists (P2's single prose sentence listing skills is fine), and filler sign-offs like "I look forward to hearing from you".
- Use the company's own names for things (product names, team names) where the user's work matches.
- Job titles match the tailored resume and the title policy in `tailor-profile.md`.

## 5. Humanize

Load and run the `humanizer` skill's checks (Skill tool). It ships alongside this skill. If the optional `structural-humanizer` skill is installed, run it second (theme explicitness, reference specificity, shape convergence vs. the user's previous letters). Fix in place. If either isn't installed, tell the user once, then rely on the banned-phrase list and the read-aloud pass below. Never skip the read-aloud pass.

**Then do a read-aloud pass, sentence by sentence.** The humanizers catch AI vocabulary but not clumsy English, so check every sentence for these:
- **One idea per sentence.** No unrelated facts glued with "and" ("I know <city> from my <old internship> and can be in the office three days a week" fails).
- **It sounds like something a person would say to a hiring manager.** If a sentence sounds odd read aloud, rewrite it plainly.
- **Grammar is correct:** articles, tense agreement, no dangling clauses, no run-ons.
- **No sentence over ~30 words.**
- **No sentence that only restates the posting back to them.**

## 5b. Format compliance check (before building)

Check the draft against §3 and the profile, line by line. Fix anything that fails, then re-check:
- [ ] Header: date / "Start Availability: <Month> <YYYY>" / length only / greeting, each on its own line
- [ ] 5 paragraphs in the profile's order, each within its word range
- [ ] P2 follows the technical-background pattern (alignment line → languages and tools → optional coursework → what they build in the current role), with no stories or metrics
- [ ] No employer named in more than 2 paragraphs; P5 names none
- [ ] P5 is exactly the two-sentence goodbye pattern (3 with a transcript), with no graduation date, no semicolons and nothing glued on
- [ ] No bold, no em dashes, no banned phrases
- [ ] No sentence claims a forced keyword, an invented decision or an invented story
- [ ] Total words within the profile's target

## 6. Build and check

1. Copy `assets/cover_letter_template.tex` and fill every `{{PLACEHOLDER}}` from the profiles and the draft. Save it as `tailored/<Company_Role>/<FilePrefix>_CoverLetter_<JobName>.tex` (JobName = `<Company>_<RoleTag>`, the short name defined in resume-tailor §7, e.g. `Acme_SWEWeb`; use the same JobName as the resume), with the file prefix from Identity. The PDF it compiles to carries the same name. **Use the Write tool, not a shell heredoc:** shells collapse LaTeX's `\\` line breaks into `\`, which glues the header lines together and the sign-off to the name. Escape LaTeX specials (`&`→`\&`, `%`→`\%`).
2. Compile with pdfLaTeX. To find the compiler, see resume-tailor's `references/latex-build.md` (Windows, macOS and Linux). Judge success by `Output written on ... (1 page`. Delete `.aux/.log/.out`.
3. Count body words (`pdftotext`, from the greeting to the sign-off) against the profile's target (default 430–500).
4. Render the page and look at it: one page, the header lines and the sign-off each on their own lines, no bold text, no stray characters, no `{{` left anywhere. Also `grep -c textbf` the `.tex` body (everything after the greeting): it must be 0.
5. Send the PDF to the user (SendUserFile, display render).

## 7. The note back to the user (short)

- Which posting and term it targets (and any availability fix).
- The research decision in one line (skipped because the JD is detailed, or done because it's thin).
- One line per paragraph on what it covers.
- **Inferred claims to check:** anything not word-for-word from the resume or profiles.
- The story-slot sentence, if no real story was available.
- One line on anything saved to `cover-letter-profile.md`.

## References

- `assets/cover_letter_template.tex`: header + layout with `{{PLACEHOLDERS}}`.
- `assets/cover_letter_profile_template.md`: starting point for a new user's `cover-letter-profile.md`.
- `references/examples.md`: an anonymized example letter and the general lessons behind these rules (shape only).
- **`cover-letter-examples.md` in the user's workspace** (if it exists): the user's own approved letters and corrections. Read it every run for their real voice, and use it for the "vary the shape" check. Never copy its contents into this skill folder: it holds personal details.
