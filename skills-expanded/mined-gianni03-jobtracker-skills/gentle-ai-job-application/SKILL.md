---
name: gentle-ai-job-application
description: "Trigger: cover letter, cold outreach, adapt resume, adaptar cv, company research, salary, job application, aplicar. Generate adapted resumes, cover letters, outreach, company briefs, salary reference."
license: Apache-2.0
metadata:
  author: "giannipasquinelli"
  version: "2.1"
---

## Activation Contract

Use when the user is applying to a job and needs any of: cover letter, resume adapted to JD keywords, cold outreach to a recruiter, company research brief, why-this-company paragraph, or salary reference. The user provides a JD. The skill produces personalized artifacts from `assets/profile.md`.

If `assets/profile.md` does not exist, run the Setup flow first (see `assets/setup-guide.md`).

## Hard Rules

- **NEVER modify or overwrite the user's original PDF files.** They are read-only source data.
- **Profile is the primary data source**: read `assets/profile.md` before generating any artifact. If it does not exist, run Setup (see `assets/setup-guide.md`).
- **Output language matches JD language.** English JD then English output. Spanish JD then Spanish output.
- **Output folder**: `output/` relative to this skill's directory. Create if needed.
- **File naming**: adapted CVs as `<firstname>_<lastname>_<position>_<company>.{md,docx,pdf}`. All other modes in a single file `<firstname>_<lastname>_application_<company>.md` with each mode as a section.
- **Reverse chronological order**: work experience roles MUST be most-recent-first. Never reorder roles by JD relevance. Only reorder bullets within each role.
- **Clickable links**: contact line MUST use markdown links `[text](url)` for email, portfolio, LinkedIn, GitHub. Projects link to their URLs. `make_docx.py` converts these to clickable hyperlinks.
- **ATS-safe text**: keep `|` as the separator and numerals with symbols ("5+ years", "30%"). Avoid `#` and `*` in prose, but keep exact technology names like `C#`, `C++`, and `.NET`. Write `UI/UX` as `UI UX` and `HTML/CSS` as `HTML and CSS`. Hyphens are allowed in compound words and dates; prefer "August 2025 to Present" for date ranges. Standard bullets are allowed: `make_docx.py` renders `- ` lines as bullets by default. See `assets/ats-rules.md`.
- **Number formatting**: use numerals with symbols, never spell out quantities or percentages. Write "5+ years", "30%", "100+", "90%". Do NOT write "5 plus years" or "30 percent". Numerals with symbols stand out visually during the 6-10 second recruiter scan.
- **Page length**: default to 1 page. Use 2 pages only when the candidate has 5+ years of relevant experience and page 2 is at least about 40% full. Break by complete section. Never let a single line or bullet spill onto the next page. A balanced 2-page resume is acceptable; a sparse or cramped one is not.
- **Proficiency levels**: only "Working proficiency" skills go in CV Skills section. "Learning/In Progress" skills NEVER appear there. When in doubt, omit.
- **No fabrication**: if the JD asks for a skill the user does not have, do not add it. Emphasize adjacent transferable skills.
- **Personalization is mandatory**: every artifact references specifics from the JD, company, and user's achievements. No cliches ("passionate", "team player", "apasionado").
- **No JD parroting**: never copy phrases from the JD into the CV. Use the user's own language to describe their experience. Keywords (technology names) belong in the Skills section. Sentences should sound like the person, not the job description. Exception: mirror the job title in the headline and role line, because ATS and recruiters match titles.
- **Anti-AI voice**: no em dashes. No long sentences chained with commas or semicolons. Short sentences. Direct. Natural rhythm. If a sentence has more than 2 commas, split it.
- **Company research**: use `webfetch` on the company's About/Careers page when available. If webfetch fails, work from JD and flag the gap.
- **Load the playbook** for the requested mode from `assets/playbooks.md` before generating.
- **Interactive mode**: when the user says "interactive", "paso a paso", or "revisar", run adapt-resume section by section with rationale and user approval per section.

## Decision Gates

| User request | Mode | Playbook section |
|---|---|---|
| Generate profile, generar perfil, setup | `setup` | `assets/setup-guide.md` |
| Cover letter, carta de presentacion | `cover-letter` | `# Cover Letter` |
| Adapt resume, adaptar cv, keywords, interactivo | `adapt-resume` | `# Resume Adaptation` |
| Cold outreach, mensaje reclutador, LinkedIn | `cold-outreach` | `# Cold Outreach` |
| Company research, investigar empresa, brief | `company-research` | `# Company Research` |
| Why this company, por que esta empresa | `why-company` | `# Why This Company` |
| Salary reference, negociar, salary, USD | `salary-reference` | `# Salary Reference` |

## Execution Steps

1. Check if `assets/profile.md` exists. If not, run Setup from `assets/setup-guide.md`.
2. Identify which mode(s) the user wants. If ambiguous, ask. Multiple modes can run in one session.
3. Gather inputs: JD text (required), company name, job position, recruiter info, company URL, offered USD amount (all optional depending on mode).
4. Read `assets/profile.md`. If user has a resume PDF, extract URLs with `pdftotext` and the raw byte regex for `/URI` patterns.
5. If company-research, why-company, or cover-letter: optionally `webfetch` the company About/Careers page.
6. Read the playbook section from `assets/playbooks.md`.
7. Generate the artifact following the playbook rules.
8. For adapt-resume: write `.md`, convert to `.docx` with `python3 assets/make_docx.py <input.md> <output.docx>` (add `--plain` for plain paragraphs), convert to `.pdf` with `libreoffice --headless --convert-to pdf`, verify pages (default 1, max 2) with `pdfinfo`.
9. Present results inline. Report saved file path(s).

## Output Contract

- `adapt-resume` generates `.md`, `.docx`, `.pdf` in `output/`.
- All other modes append to a single `<firstname>_<lastname>_application_<company>.md` in `output/`. Each mode is a section. If the file exists, update only that section.
- Present content inline AND report saved file path(s).
- Flag any personalization gaps.

## References

- Profile template: `assets/profile-template.md`
- Setup guide: `assets/setup-guide.md`
- Playbooks: `assets/playbooks.md`
- ATS rules: `assets/ats-rules.md`
- docx converter: `assets/make_docx.py`
