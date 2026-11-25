---
name: scout-profile
description: "Use when building, updating, or reviewing your job search profile, master CV, or job preferences. Activates when user wants to set up or modify their professional profile for job hunting."
---

# Scout Profile

Builds and maintains your master professional profile at `~/.scout/profile/`. This profile is the foundation that `/scout-vet` and `/scout-apply` depend on.

## Data Directory

All profile data lives at `~/.scout/profile/`. Create the directory if it doesn't exist.

## Input Mode Detection

Determine mode from context:
- **Profile exists** (`~/.scout/profile/master-profile.md` found) → update mode
- **User provides a file or pasted CV** → parse-and-build mode
- **Nothing provided, no profile exists** → interview mode

## Update Mode

If `master-profile.md` already exists:
1. Read and present the current profile summary to the user.
2. Ask what they want to update: skills, experience, preferences, or something else.
3. Make targeted updates. Never overwrite the entire profile without confirmation.

### Cascading Updates for Contact Information

When updating contact fields (name, email, phone, URLs), changes must propagate to all dependent files:

1. **Always update:** `master-profile.md` and `master-cv.md`.
2. **Update pending applications:** Glob `~/.scout/applications/*/cv.md` and update contact info in each. Then regenerate PDFs for any job whose status is `"materials-ready"` (not yet submitted). Reuse the existing PDF generation script if one was created in the current session.
3. **Warn about submitted applications:** For any job with status `"applied"` or later, inform the user: "Note: your application to [Company] was already submitted with the old [field]. The updated [field] will be used for future applications."
4. **Update cover letters and email drafts** in `~/.scout/applications/*/cover-letter.md` and `~/.scout/applications/*/email-draft.md` if they exist and contain the old value.

## Parse-and-Build Mode

If the user provides an existing CV (file path or pasted text):
1. Parse the document and extract structured data: name, contact info, skills, work history, education.
2. Present what was extracted and ask the user to confirm accuracy.
3. Ask follow-up questions for any gaps — one at a time, prefer multiple choice.
4. Write the three output files (see Output Files below).

## Interview Mode

If no profile exists and no document is provided, conduct an interview — one question at a time, prefer multiple choice where possible:

1. **Professional summary** — What is your current or most recent role? How many years of experience do you have? Give me a 2-3 sentence elevator pitch.
2. **Skills** — What are your top technical skills? Rate each as beginner/intermediate/advanced/expert. What are your key soft skills?
3. **Work history** — For each role (starting with most recent): company, title, dates, 3-5 key achievements. Push for quantified achievements (numbers, percentages, revenue, team size).
4. **Education & certifications** — Degrees, institutions, graduation years. Relevant certifications with dates.
5. **Job preferences** — What roles are you targeting? What industries? What seniority level?
6. **Deal-breakers** — What is your minimum acceptable salary? (Ask for currency and whether annual/monthly.) Location requirements? Remote/hybrid/onsite preference? Company size constraints? Visa sponsorship needs?
7. **Optional extras** — Portfolio URL? LinkedIn? GitHub? Publications? Languages spoken?

## Output Files

### `master-profile.md`

Structured profile with YAML frontmatter. ALL string values must be quoted.

```yaml
---
name: "Jane Doe"
title: "Senior Product Manager"
years_experience: 8
skills:
  - name: "Product Strategy"
    proficiency: "expert"
  - name: "SQL"
    proficiency: "intermediate"
contact:
  email: "jane@example.com"
  phone: "+1-555-0100"
  linkedin: "linkedin.com/in/janedoe"
  portfolio: "janedoe.com"
---

## Summary
[Elevator pitch — 2-3 sentences]

## Work History

### [Job Title] — [Company]
**[Start Date] – [End Date]**

- [Achievement with quantified impact]
- [Achievement with quantified impact]
- [Achievement with quantified impact]

### [Previous Job Title] — [Company]
...

## Education

### [Degree] — [Institution]
**[Graduation Year]**

## Certifications
- [Certification name] ([Year])
```

### `master-cv.md`

A comprehensive, unabridged CV in Markdown containing ALL experience, skills, and achievements. This is the source of truth that `/scout-apply` tailors from. It should include everything — even old or less relevant experience — because different jobs may need different subsets.

Format it as a clean, complete CV document (not a data file). Start with the candidate's name, then contact info, then sections: Summary, Experience, Education, Skills, Certifications.

### `preferences.md`

Structured preferences used by `/scout-vet` for scoring and filtering.

```yaml
---
target_roles:
  - "Product Manager"
  - "Senior Product Manager"
target_industries:
  - "fintech"
  - "healthtech"
seniority: "senior"
location:
  preferred: "Remote"
  acceptable: ["Remote", "Hybrid (NYC)"]
  dealbreaker_if: "fully onsite"
remote_policy:
  preferred: "fully remote"
  acceptable: ["fully remote", "hybrid"]
salary:
  minimum: 150000
  preferred: 180000
  currency: "USD"
  period: "annual"
company_size:
  preferred: "50-500"
  dealbreaker_if: "pre-seed/unfunded"
visa_sponsorship_required: false
dealbreakers:
  - "fully onsite"
  - "pre-seed/unfunded startup"
  - "no salary disclosed and below minimum after negotiation"
---
```

## Completion

After writing all three files, inform the user:

> "Profile created at `~/.scout/profile/`. You can now use `/scout-find` to discover jobs, `/scout-vet` to evaluate them against your profile, or `/scout-apply` to generate tailored application materials."
