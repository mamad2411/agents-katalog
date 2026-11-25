---
name: resume-builder
description: Build, tailor, or revise a resume. Use when the user asks for a resume, either a general version or one tailored to a specific job posting. Produces Markdown, .docx, and .pdf outputs.
---

# Resume Builder

## When to use
Any request to build, tailor, revise, or critique a resume.

## Inputs
- **Source material** — read all that exist before drafting. `$PERSONAL` is the personal-docs sibling directory defined in `CLAUDE.md`; resolve it once at the start of the session.
  - `$PERSONAL/career/impact-doc.md` — always. Primary source of truth for roles, projects, and metrics.
  - `$PERSONAL/career/brag-doc.md` — read if it exists. Contains quantified wins and recognition not always captured in the impact doc. Cross-check metrics here before finalizing any bullet.
  - `$PERSONAL/career/goals.md` — read if it exists. Use to understand target role type, level, and what to emphasize or deprioritize.
  - `$PERSONAL/career/personal-info.md` — read if it exists. Use for the resume header: name, email, phone, location, LinkedIn, GitHub. If the file does not exist, use placeholders and note them explicitly so the user can fill them in.
  - `$PERSONAL/career/current-resume.md` — use as a baseline if it exists; otherwise build from scratch.
- **Target** (one of):
  - A specific job description → tailor to it
  - "General" → produce a strong default version
- **Length preference**: default 1 page. Confirm if I want longer.

## Workflow

### 1. Confirm target
If the target isn't obvious from context, ask:
- Specific Job Description, or general?
- Length preference?
- Any role/company I'm asking you to *deprioritize* (e.g., I don't want my AWS work to dominate)?

### 2. Pull and rewrite bullets
For each role in my career, draft bullets using **XYZ format**:
> Accomplished **X** by doing **Y**, measured by **Z**.

Every bullet must:
- Start with a strong action verb (built, led, shipped, reduced, architected — not "responsible for," "helped with," "worked on")
- Include scope (team size, system scale, dollar impact, user count, request volume — whatever applies)
- Include a quantified outcome where possible

If `$PERSONAL/career/impact-doc.md` is missing the numbers, surface that and ask me to fill them in rather than fabricating.

### 3. Tailor
When a target Job Description is provided:
- Match the Job Description's keyword vocabulary where it's truthful (e.g., if they say "distributed systems," use that phrase if it applies to my work, don't keyword-stuff with terms I haven't used)
- Reorder bullets so the most relevant come first within each role
- Cut bullets that don't reinforce the target — even strong ones
- Adjust the summary/header to mirror the role's framing

### 4. Critique pass
Before finalizing, evaluate every bullet:
- Does it have a number? If not, can I add one?
- Does it lead with action and outcome, or with the situation?
- Could a less impressive engineer write the same bullet? If yes, sharpen it.
- Is the scope clear?

Flag weak bullets explicitly with proposed alternatives.

### 5. Produce outputs
Create three formats in `$PERSONAL/applications/<company>/<role>/` (or `$PERSONAL/career/resumes/<variant>/` for general versions):
- `resume.md` — clean Markdown, the source of truth
- `resume.docx` — using the docx skill
- `resume.pdf` — using the pdf skill

For the .docx and .pdf, use a clean professional template — single column, sans-serif, no graphics, no skill bars, no photo. ATS-friendly.

### 6. Summarize the changes
End with a short summary of:
- What you emphasized and why
- What you cut and why
- Anything you flagged as weak that I should improve at the source (in `$PERSONAL/career/impact-doc.md` or `$PERSONAL/career/brag-doc.md`)

## Anti-patterns
- Don't invent metrics. If the number isn't in my files, ask.
- Don't keyword-stuff. ATS optimization is real, but obvious stuffing reads worse than honest framing.
- Don't include an "Objective" section. Use a one-line professional summary instead, only if it adds signal.
- Don't list every technology I've ever touched. Curate to what matters for the target.
- One page unless explicitly asked otherwise. Senior-level resumes can justify two pages; if I'm targeting staff+, ask.
- **Never use em dashes or en dashes** (— or –) anywhere in the resume. Replace with a comma, colon, period, or parentheses. This applies to bullets, the summary, section headers, and job titles. No exceptions.
- **Use generic, industry-standard terminology, not company-specific or tool-specific jargon.** The reader may not share my team's vocabulary. Translate internal shorthand to widely understood equivalents before it hits the bullet. Examples:
  - "MR review cycle" → "code review cycle" (MR is GitLab-specific; PR is GitHub-specific; "code review" works everywhere)
  - "Cut MR review cycle by 50%" → "Cut code review cycle by 50%"
  - Internal product or team codenames → the public product name, or the generic capability ("checkout service," "payments pipeline")
  - Internal acronyms (CRQ, TPS, OKR-of-the-quarter names) → spelled-out plain English
  - Custom tooling names → the category of tool ("internal deploy tool" rather than the codename)
  If a term is genuinely industry-standard (Kubernetes, Kafka, gRPC, OAuth), keep it. If in doubt, ask whether a reader at a different company would recognize it.
