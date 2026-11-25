---
name: generate-cv
description: Generate a tailored CV + interview cheat sheet for a specific role — follows the 11-step resume workflow, saves to output/, and updates the pipeline
argument-hint: <job-url-or-jd> [context]
user-invocable: true
allowed-tools: Read(*), Glob(data/*), Glob(plugins/*), Glob(framework/*), Write(output/**), Write(data/job-pipeline.md), mcp__exa__web_search_exa, mcp__exa__web_fetch_exa, WebFetch, WebSearch, Bash(python3 tools/projects_to_yaml.py:*), Bash(python3 tools/cv_merge_theme.py:*), Bash(~/.local/bin/rendercv render:*), Bash(rendercv render:*), Bash(rm -rf output/**/rendercv_output)
---

# Generate CV — Tailored Resume + Cheat Sheet

Generate a fully tailored CV and companion interview cheat sheet for a specific job posting. Produces ATS-optimised output in the right format for the market and saves both files to `output/`. Quality standards, tailoring rules, and the pre-output checklist are defined in `framework/application-workflow.md`.

## Arguments

- `$ARGUMENTS` (required at minimum a job URL or pasted JD text):
  - **`<job-url-or-jd>`** (required) — a URL to the job posting, or the full pasted job description text
  - **`[context]`** (optional) — additional instructions, e.g. `"emphasize McKinsey"`, `"US resume format"`, `"focus on operations experience"`

Examples:
- `/generate-cv https://jobs.northwind.example.com/cos-role` — fetch and tailor to that posting
- `/generate-cv "Chief of Staff, Northwind..." "emphasize food/FMCG experience"` — pasted JD with context
- `/generate-cv https://example.com/job "US format, keep to 1 page"`

If no arguments provided, display usage:
```
Usage: /generate-cv <job-url-or-jd> [context]

Examples:
  /generate-cv https://company.com/jobs/role
  /generate-cv "Job description text..." "emphasize operations"
  /generate-cv https://company.com/job "US format"
```

## Instructions

### Step 1: Parse Arguments

Parse `$ARGUMENTS`:
1. **Detect URL vs pasted text** — if the first token contains `http` or a recognisable domain pattern, treat it as a URL. Otherwise treat the entire argument (up to any quoted context string) as pasted JD text.
2. **Extract context string** — any quoted string that follows the URL/JD, or text after the job description ends.
3. **If URL detected**: use WebFetch to retrieve the job posting content. If the fetch fails, ask the user to paste the JD text directly.

### Step 2: Load Candidate Context (parallel)

Read all CV-relevant files listed in `framework/application-workflow.md` § Candidate Context Loading (the "CV" column). Skip any that don't exist, never fail.

Derive the company slug from the JD in Step 1 if already parsed, otherwise read `data/company-notes/<company-slug>.md` and the company dossier after Step 3.

Run the **Company Dossier Staleness Check** from `framework/application-workflow.md` § Company Dossier Staleness Check.

### Step 3: Analyse the Role

From the job posting text, extract:

- **Company name** and generate a slug (lowercase, hyphens, e.g. `beacon`)
- **Role title** and a role slug (e.g. `chief-of-staff`)
- **Required skills** (must-haves stated explicitly)
- **Nice-to-have skills** (preferred, bonus, or desirable)
- **Seniority level** (IC, manager, director, VP, C-suite)
- **Top 10 ATS keywords** — the most important terms to appear in the CV for ATS passage. Prioritise: job title words, required skills, industry-specific terms, tools/technologies named.
- **Market** — infer from location mentions or company HQ: `US`, `UK`, `DACH`, or `international`. Default to `US` if unclear.
- **Industry** — infer from company and role context.

### Step 4: Check Plugins

If `data/plugin-activation.md` exists, read it. Glob `plugins/*/plugin.md` and check for any plugin with `scope: cv` or `scope: all`. If found, read those plugin files and apply any instructions they contain for CV generation.

### Step 5: Select Projects & Generate Factual Stubs

1. Read `data/project-index.md` — scan all entries for relevance to the role's required skills, industry, seniority level, and company type.
2. Select **3–6 most relevant projects**. Criteria: skill overlap with required skills > industry/domain match > seniority match > recency.
3. Read the full project files for each selected project from `data/projects/`.
4. **NEVER read or use files from `data/project-background/`** — those are internal-only and must not appear in CVs.
5. Note the rationale for each selected project (will be used in the cheat sheet).
6. **Generate factual EXPERIENCE stubs.** Run:
   ```bash
   PYTHONIOENCODING=utf-8 python3 tools/projects_to_yaml.py --include <slug1>,<slug2>,... --out /tmp/cv-experience-stubs.yaml --json
   ```
   Where `<slug>` matches the filename (no `.md`) of each selected project, in the order they should appear on the CV (most recent first). Read the resulting YAML — it is the **source-of-truth baseline** for company, position, date, location, and highlights. Per lesson #54, every quantified claim on the final CV must trace back to either this stub or directly to `data/projects/<slug>.md`. Tailored phrasing is fine; invented numbers are not.

### Step 6: Generate the CV YAML

The CV is emitted as a **RenderCV YAML** in the same shape as the canonical reference `output/example-ventures/042826-cos-example.yaml`. The design block is NOT included here — it is composed in from the shared theme in Step 9b. Structure:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/rendercv/rendercv/refs/tags/v2.8/schema.json
cv:
  name: NICK MAGNUSON
  location: San Francisco, CA
  email: priya.anand@example.com
  phone: tel:+1-415-555-0148
  social_networks:
    - network: LinkedIn
      username: nicholas-magnuson
  sections:
    SUMMARY:
      - <3–4 line tailored summary>
    EXPERIENCE:
      - <entries from Step 5 stubs, tailored>
    EDUCATION:
      - institution: TUCK SCHOOL OF BUSINESS AT DARTMOUTH
        area: Management Science and Quantitative Methods (STEM)
        degree: MBA
        date: 2020 – 2022
        location: Hanover, NH
      - institution: DUKE UNIVERSITY
        area: Public Policy, Markets and Management Certificate
        degree: BA
        date: 2011 – 2015
        location: Durham, NC
    ADDITIONAL INFORMATION:          # ORDER IS FIXED: Building, Skills, Hobbies. Spec: "Additional Information spec" below.
      - label: Building              # use "Building" NOT "Side project" (Nick: "side project is not what I am")
        details: "(github.com/<github-handle>)\n- <AI-app bullet, 2 lines max>\n- <job-search agent system bullet, exactly 1 full line>"
      - label: Skills
        details: "*Operating:* ... *Data:* ... *Building with AI:* ..."   # exactly 2 rendered lines
      - label: Hobbies
        details: <hobbies line from profile.md>
locale:
  language: english
settings:
  current_date: today
  bold_keywords: []
  pdf_title: Nick Magnuson - CV
```

Apply all **Tailoring Rules** and **CV Quality Standards** from `framework/application-workflow.md`. Key requirements:

- **Professional summary** — 3–4 lines tailored to this specific role. Opens with a hook tied to the company's mission or the role's core challenge. **Voice (Nick, 2026-06-22):** lead with the BUILDER/OPERATOR identity and results ("I get things done, use data, and build the thing that fixes it"), NOT a credential-first opener. Do NOT lead with "McKinsey-trained" or frame Nick as someone who "lands complex change in large organizations" — for early-stage/founder audiences that reads as pedigree-play (and founders hire for agency over credentials). McKinsey + Zuora are SUPPORTING credibility, named mid-summary, not the lead. First-person ("I ...") is acceptable and in voice for the summary.
- **Experience entries** — start from the Step 5 stubs verbatim. Tailor bullet PHRASING for JD relevance (emphasize keywords, lead with most-relevant impact). Do NOT invent quantified claims not present in the stubs or in `data/projects/<slug>.md`. Lesson #54: prior-CV numbers are hypotheses, source files are tests.
- **Experience ordering** — strict reverse-chronological (most recent first). Do NOT reorder by relevance — non-chronological CVs are flagged by ATS systems and confuse recruiters. Tailor through bullet selection and emphasis, not ordering.
- **Skills section: fixed three-group line, exactly two rendered lines (SUPERSEDES the 2026-06-22 framing; Nick, 2026-09-23).** Order and labels are fixed, labels italic, items sentence case:
  `*Operating:* cross-functional stakeholder collaboration, change management, executive presentations. *Data:* SQL, R, Tableau, Looker, Excel. *Building with AI:* Claude Code, multi-agent workflows, cross-model verification, mutation testing.`
  - **Operating goes first and Nick chose these three terms on purpose.** The 2026-06-22 ban on competency phrases is overridden for this group only; do not "fix" it back, and do not add further competency phrases anywhere else. "Stakeholder management" and "cross-functional collaboration" are ONE item ("the same thing" - Nick). Presenting lives here as "executive presentations"; never a separate "Executive decks: PowerPoint" group ("stupid" - Nick).
  - **Building with AI goes LAST** and is sourced from `coaching/coached-answers/how-i-work-with-ai.md` (Nick's record of what he has learned building with AI), not from the product stack. Never list Next.js or Postgres ("not definitive, not important" - Nick). If a term must go for space, cut the least differentiated one first; "Claude and OpenAI APIs" was cut 2026-09-23 because Claude Code already names Claude.
  - Hedge words (`-adjacent`, `exposure`, `familiarity`) stay forbidden. Keep the evidence rule: every tool must trace to `data/skills.md` or a project file.
  - **Superseded 2026-09-23, kept for history:** the 2026-06-22 grouping ("building with AI (Claude Code, Claude/OpenAI APIs, Next.js, Postgres, AI agent workflows), data analysis and financial modeling, executive decks (PowerPoint)") and the blanket ban on "Change Management" / "Stakeholder Management".
- **Additional Information spec (Nick, 2026-09-23). The whole section must render on page 1** (it moves to page 2 as one block, so a one-line overflow anywhere costs the entire section). Trim inside this section first, then elsewhere, before touching design.
  - **Building label line:** `Building:` bold (the label), then the GitHub link (handle from `data/profile.md`) unbolded in parentheses on the same line: `(github.com/<github-handle>)`. **GitHub never goes in the header** (the `-jpg` handle "looks bad" there - Nick). Then two bullets.
  - **RenderCV markup gotcha:** bullets inside a one-line entry need text or a line break BEFORE the first `- `. `details: "- A\n- B"` renders the first item as a literal hyphen. Correct: `details: "(github.com/<github-handle>)\n- A\n- B"`.
  - **Bullet 1, the AI app: two rendered lines MAX, resume register.** Verb-led fragments, no "I", no narrative setup ("What it taught me:" was rejected as not fitting "the rest of the type prose of a resume"). Content = what he built plus the lessons from the Learnings section of that app's project file in `data/projects/`. **Default text lives in `data/profile.md` → `## CV defaults: Building bullets`; use it verbatim and tailor only when Nick asks.**
  - **Bullet 2, job-search agent system: exactly ONE full rendered line that shows scale.** Default text: `Job-search agent system running my search end to end: 180+ scripts, 40 skills, 40+ checks blocking bad output before it ships.` **Recount every time before rendering** (numbers decay): `ls tools/*.py | wc -l` (scripts), `ls .claude/skills | wc -l` (skills), `ls tools/check_*.py | wc -l` (checks). Round down to the stated form. As of 2026-09-23: 182 / 40 / 45.
  - **Verify every number taken from a project file against its live source before it goes on a CV.** On 2026-09-23 a project file said "169 automated test files"; the repo gave 217 at that file's own as-of date and 294 on the day. A project file is a pointer, not a measurement. If the number cannot be reproduced, drop it or recount and update the project file with a dated note.
- **Building entry lives in ADDITIONAL INFORMATION and NEVER in EXPERIENCE (Nick, 2026-08-25).** A deep review will periodically argue for promoting the AI products into EXPERIENCE as a dated entry, usually on the grounds that they are the only evidence of hands-on building or of shipping a fix fast. The argument is reasonable and the answer is still no: these are the Building piece. Do not propose it again, and do not act on a reviewer that does. **Building entry:** label it `Building` (NOT "Side project") and name Nick's AI products (the AI app named in `data/profile.md`; the job-search OS) by what they ARE + capability — see `feedback_dev_jargon_to_ceo_context`. **Exception (Nick, 2026-09-23):** the job-search agent bullet deliberately shows scale with recounted counts (scripts, skills, checks); that is value, not plumbing. Format and default text live in the **Additional Information spec** above, which wins over this sentence.
- **Summary must pass the McKinsey lede test (added 2026-09-14).** Apply `framework/slide-craft-mckinsey.md`
  to the SUMMARY specifically. (a) **Insight lede, not process lede** - the first sentence is a claim the
  reader could disagree with, not a category label or a chronology. (b) **No phase-counting** - "Consultant,
  then operator, now building" enumerates rather than summarizes, which that framework names directly
  ("Counting the sub-bullets is not a summary"). (c) **No empty adjectives or hedge-quantifiers** - "large"
  organization, "mostly" a change problem. (d) **No want-statements** - "that is the part I want to own" is
  a wish, not a claim; the wanting is implied by applying. Nick's word for the failure mode: "it feels fluffy."
- **Rank, do not negate (added 2026-09-14, Nick's own edit).** An absolute contrast asserts the other side out
  of existence and invites an instant rebuttal. "The constraint is behavioral, not technical" tells an
  engineering audience their technical problem does not exist. **"The HARDER constraint is behavioral, not
  technical"** concedes both and ranks them. Prefer the comparative in any X-not-Y construction.
- **Never downgrade a source verb (added 2026-09-14).** If `data/projects/*.md` says "Defined", write
  "Defined". A weaker verb is justified ONLY by a dated correction comment that demands it (e.g. "Supported"
  for the GenAI workshop per `mckinsey.md`, "Facilitated" not "stood up" per lesson #17). Silent conservatism
  reads as hedging and Nick will catch it: "Advised is not a strong word."
- **"Production" requires external users (added 2026-09-14, Nick's call).** The AI app named in `data/profile.md` is production
  (live, real users, a user-reported bug). The job-search OS is a personal system in daily use and is NOT.
  Do not write "two production AI applications". Write "two AI applications".
- **Lane A enterprise-deployment targets get the GenAI workshop bullet (added 2026-09-14, Nick's standing
  instruction).** For any company whose customers are large enterprises adopting AI, include the McKinsey
  GenAI-workshop bullet from `mckinsey.md` "Other Studies". It is the closest thing in the corpus to coaching
  an enterprise executive team on AI adoption. Verb is **"Supported"** per the 2026-07-20 correction (the EM
  led it); never "developed" or "facilitated".
- **One engagement, one bullet (added 2026-09-14).** Do not split a single client engagement across two
  bullets to fit more detail. Merge and cut. A reader scanning bullets reads them as separate achievements.
- **ATS keyword coverage** — verify all 10 extracted keywords appear at least once in the CV text. If a keyword is missing, find a natural place to include it.
- **Achievements over responsibilities** — lead bullets with quantified outcomes where possible (sourced from stubs, not invented).
- **No content from `data/project-background/`** — enforce absolutely.
- **No em dashes** (per CLAUDE.md hard rule) — but the EN DASH (`–`) is used in date ranges per the reference YAML.

### Step 5b: NEVER TEMPLATE OFF A PRIOR CV (added 2026-09-14, the highest-yield rule in this file)

**Generate every bullet from the Step 5 stubs and `data/projects/*.md`. A previous CV is a reference for
SHAPE ONLY (section order, roughly how many bullets, how long a line runs). Never copy its bullet text.**

Why this outranks the individual content rules below: on 2026-09-14 a CV was built by copying the most
recent prior CV and editing it. Four separate defects rode across intact, and **every single one had a
rule already written that would have caught it**:

| Defect that propagated | The rule it violated, which already existed |
|---|---|
| Top-level `BUILDING:` section | This file, Skills section: "Building entry lives in ADDITIONAL INFORMATION and NEVER in EXPERIENCE (Nick, 2026-08-25)" |
| "drove the move to an outcome-based roadmap" | `zuora.md:28`: source verb is "worked with stakeholders"; the pinned comment bans upgrading it into roadmap ownership |
| "making sponsor-level metrics legible to an org built to ship features" | `zuora.md:60`: "The Key Achievements above are what goes on paper" - that clause is Learnings material describing an UNRESOLVED struggle |
| "Advised the AI-in-the-development-lifecycle strategy" | `zuora.md:40`: source verb is "Defined". "Advised" was a silent downgrade with no correction behind it |

**The diagnosis that matters:** no rule was missing. The copy path bypassed all four at once, because a
carried-over sentence never gets checked against the source the way a freshly-written one does. Two of the
four had ALSO shipped in the prior CV, to a live application, two weeks earlier - so copying propagated
defects forward rather than merely repeating them.

**Falsifiable check on this rule:** two other CVs generated in the same period put Building in ADDITIONAL
INFORMATION correctly. Only the one that was copied got it wrong.

**Operationally:** open `data/projects/<slug>.md` for every bullet you write, every time. If you catch
yourself pasting a sentence from `output/<other-company>/*.content.yaml`, stop and rewrite it from source.

### Step 6a-corrections: Reconcile against source corrections (mandatory, BEFORE first render)

Run this against every source project file you drew bullets from in Step 5/6:

```bash
PYTHONIOENCODING=utf-8 python3 tools/source_corrections.py data/projects/<file>.md [more...]
```

Source files carry their honesty history in HTML comments pinned to the bullet they correct. Those comments are invisible while you are reading the claim text you're paraphrasing — which is exactly how this has failed **twice**, both times with the file already read in full in the same session:

- **2026-07-08:** "Ran the operating cadence" / "stood up from scratch" reintroduced the `"facilitated" not "stood up"` overclaim that `zuora.md` had carried a dated correction for since 2026-05-12.
- **2026-08-07:** "built the POC portfolio with our head of engineering" reintroduced an overstatement the same file corrects to "partnered with."

For each correction returned, check the drafted line against the **corrected** wording, not the original claim. A correction that says "keep this wording, but the underlying fact is X" (there is one live example) means the CV line stands and the *cheat sheet* must carry the real fact — do not silently rewrite the bullet.

Also grep the drafted content YAML for `—` before first render. No em dashes, ever (hard project rule). Both fires shipped 3-4 of them in the Summary section.

**Why here and not Step 10b:** both failures were caught only by the 6-agent deep review, after the render. This check costs one command and runs before the expensive pass. Origin: `memory/feedback_cv_em_dash_and_source_verb_regression.md`.

### Step 6b: Inline Quality Review (mandatory — do NOT skip)

Before generating the cheat sheet, run all 18 checks from `framework/application-workflow.md` § CV Quality Checks against the CV you just produced. Fix any issues found **in place** — rewrite the CV, don't just flag problems.

After all fixes, record a QC summary using the template in `framework/application-workflow.md` § QC Summary Template.

### Step 7: Generate Companion Cheat Sheet

Alongside the CV, generate a pre-interview cheat sheet following the structure, quality rules, and markdown template in `framework/application-workflow.md` § Cheat Sheet Structure.

### Step 8: Determine Output Filenames

- Generate date prefix: `MMDDYY` (today's date)
- Use the company slug from Step 3 as the subfolder: `output/<company-slug>/`
- **CV artifacts all use the `MMDDYY-magnuson` stem** (Nick's preference — clean person-named files for submission, no role title in CV filenames):
  - CV YAML (content-only, no design block): `output/<company-slug>/MMDDYY-magnuson.content.yaml`
  - CV YAML (final, design baked in, render-ready and reproducible standalone): `output/<company-slug>/MMDDYY-magnuson.yaml`
  - CV PDF (the artifact you send): `output/<company-slug>/MMDDYY-magnuson.pdf`
  - CV Markdown (rendercv-emitted, used by review skills): `output/<company-slug>/MMDDYY-magnuson.md`
- Cheat sheet **does** include the role slug (it is role-specific, not interchangeable across roles at the same company): `output/<company-slug>/MMDDYY-[role-slug]-cheatsheet.md`
- If a CV file at that path already exists (e.g. two applications at the same company on the same day), append `-v2`, `-v3` etc. to ALL four CV files in the set. The cheat sheet's role-slug already disambiguates it.

### Step 9: Save CV Source YAML

Write the tailored content-only YAML from Step 6 to:
`output/<company-slug>/MMDDYY-magnuson.content.yaml`

The `.content.yaml` MUST NOT contain a `design:` block — design lives in `framework/cv-themes/tuck-mbb.yaml` and is composed in by Step 9a. `tools/cv_merge_theme.py` will error if a design block is already present (that's how the duplication safety net works).

### Step 9a: Compose Theme

Merge the content YAML with the shared design theme:

```bash
PYTHONIOENCODING=utf-8 python3 tools/cv_merge_theme.py \
  --content output/<company-slug>/MMDDYY-magnuson.content.yaml \
  --out     output/<company-slug>/MMDDYY-magnuson.yaml \
  --json
```

The `.yaml` file is now complete and standalone — design + content baked together. Anyone with this single file can re-render the exact PDF months from now, even if the shared theme has changed since.

### Step 9b: Render PDF + Markdown + PNG

```bash
~/.local/bin/rendercv render output/<company-slug>/MMDDYY-magnuson.yaml \
  --pdf-path       MMDDYY-magnuson.pdf \
  --markdown-path  MMDDYY-magnuson.md \
  --output-folder  rendercv_output \
  --dont-generate-html
```

**No `cd`, deliberately.** `--pdf-path` and `--markdown-path` are resolved *relative to the input file* (verified against `rendercv render --help`), so the artifacts land beside the YAML exactly as before. `--output-folder` resolves the same way. **Corrected 2026-09-23:** this note used to say `--output-folder` resolves against the cwd and prescribed `output/<company-slug>/rendercv_output`; in practice that produced a nested `output/<company-slug>/output/<company-slug>/rendercv_output/`. Pass the bare `rendercv_output` and the PNGs land at `output/<company-slug>/rendercv_output/` as the later steps expect. The shell cwd resets between tool calls in this harness, which makes a relative `cd` a latent false-confirmation bug — see `memory/feedback_bash_confirm_must_chain_to_operation.md`.

The PDF is the artifact you send. The markdown is the rendercv-emitted version used by `/review-cv` and `/review-cv-deep`. The PNG (in `rendercv_output/*_1.png`) is for the layout verification in Step 9b-verify — do NOT delete `rendercv_output/` until after that step.

### Step 9b-verify: Render & verify before presenting (mandatory — checks #19, #20)

Per `framework/application-workflow.md` § Render & verify. Do NOT skip — this is where the layout/length defects that otherwise force user iteration get caught.

1. **`Read` the PNG** (`output/<company-slug>/rendercv_output/*_1.png`). Visually confirm: exactly one page for Nick; italics, line breaks, and spacing render cleanly (no stray asterisks, no broken emphasis, no awkward title wraps); page well-filled, not overflowing. Reasoning from the markdown alone misses these — the rendercv gotchas (bare-year → "Jan YYYY"; `\n` breaking position italics) are only visible in the render. **Bare-year fix (Nick, 2026-06-22):** for a single-year role, write the date as an UNQUOTED integer (`date: 2024`) — that renders as "2024". A quoted `date: '2024'` renders as "Jan 2024" (wrong, and it spotlights short stints / the silent gap). Multi-year ranges (`date: 2022 – 2024`) already render verbatim.
2. **Count pages:** `PYTHONIOENCODING=utf-8 python3 -c "from pypdf import PdfReader; print(len(PdfReader('output/<company-slug>/MMDDYY-magnuson.pdf').pages))"`. For Nick this must be 1.
3. **If over one page or layout is off, fix it now and re-render** — trim per § Length & One-Page Verification (tighten summary → merge/cut weakest-oldest bullets → shorten the Building entry → drop filler, before touching design). Never hand over a 2-page CV or one with mechanical layout defects for the user to "edit down."
3b. **Fill the page — don't leave a half-empty CV (Nick, 2026-06-22).** If there is meaningful blank space at the bottom, the CV is under-filled — bump sizing in the FINAL `MMDDYY-magnuson.yaml` design block (NOT the shared theme, so other CVs are unaffected) and re-render: body `11pt` / name `20pt`, `line_spacing: 0.6em`, `sections.space_between_regular_entries: 0.5em`, and `section_titles.space_above: 0.45cm` for clear breaks between SUMMARY / EXPERIENCE / EDUCATION / ADDITIONAL INFORMATION. Re-check it still holds at one page (Step 2). The target is a full, balanced single page, not a top-heavy one.
4. Once verified, `rm -rf output/<company-slug>/rendercv_output/`.

### Step 9c: Save Cheat Sheet

Write the cheat sheet from Step 7 to: `output/<company-slug>/MMDDYY-[role-slug]-cheatsheet.md` (cheat sheets keep the role slug — they are role-specific, not interchangeable across roles at the same company)

### Step 10: Update Pipeline

1. Read `data/job-pipeline.md`.
2. Search for the company name (case-insensitive, fuzzy match — check if the company name from the JD appears as a substring in any active pipeline entry).
3. If found: update that entry's **CV Used** field to the CV output filename (just the filename, not full path).
4. If not found: note in the summary that the company isn't in the pipeline yet and suggest `/pipe add "[Company]" "[Role]"`.

### Step 10b: Run Deep Review (always — do NOT skip)

After saving the CV and updating the pipeline, automatically invoke `/review-cv-deep` against the just-saved CV. This is mandatory, not optional. The deep review produces a six-perspective audit (Recruiter / Hiring Manager / Competitor / Skeptic / Copy Editor / Source Auditor) saved to `output/<company-slug>/MMDDYY-magnuson-DEEP-REVIEW.md`.

**Rationale:** A single-pass inline review (Step 6b) catches surface issues but routinely misses (a) source-data fabrications detectable only by cross-referencing project files, (b) chronology bugs that a structured external-eyes pass surfaces, and (c) high-leverage missed assets documented in source files but absent from the CV. The 6-agent flow is the only reliable way to catch these. Speed is not an acceptable trade-off — every CV gets the same scrutiny.

Pass two arguments to `/review-cv-deep`: the CV filename (just the filename — the skill reads from `output/`) and the JD (pass the URL if provided; otherwise write the JD text to a temp file and pass that path).

Wait for the deep review to complete before proceeding to Step 11. Capture the key verdicts (Recruiter phone-screen decision, Hiring Manager interview decision, Competitor shortlist rank, top 3 CRITICAL/IMPORTANT findings) for the Step 11 summary display.

**Apply the high-confidence quality fixes before presenting — do NOT hand the user a report of cleanup they have to ask for.** After the deep review returns, auto-apply (and re-render + re-verify per Step 9b-verify) the objective, low-risk findings the panel converges on: cut vague/source-unbacked filler bullets, fix skills format/filler, remove a location line from the summary, fix any unevidenced skill or label, resolve layout/one-page defects. Then re-run Step 9b-verify. Leave for the user ONLY the judgment/voice calls (summary phrasing they must stand behind, which optional achievements to include, claim-level decisions). **Surface those in the DECISIONS FOR YOU block, which is the REQUIRED first block of Step 11 and has a mandatory format — see Step 11.** "A short menu" was the prior wording and it produced nothing for three months, because an instruction with no shape does not convert into an artifact. Origin: 2026-06-11 recruiter-channel CV — the deep review flagged filler bullets, the skills grouping, and the summary location line, but they were left for the user to catch, driving ~6 extra rounds.

**Opt-out:** if the user explicitly passes `--no-deep-review` in `[context]`, skip this step and note "Deep review skipped per --no-deep-review flag" in the Step 11 summary. This exists for fast-iteration cases (drafting variants); the default is always-on.

### Step 11: Display Summary

**The DECISIONS FOR YOU block comes FIRST, before the file paths. This is required, not optional.**

**Why it leads:** Nick's read of a finished CV catches a class no reviewer catches. On 2026-09-14 the
six-perspective deep review caught two source-fidelity violations and flagged ZERO of the six things
Nick caught himself: a fluffy summary, a downgraded verb, an overclaimed "production", a misplaced
Building section, a missing Lane-A bullet, and an absolute claim that should have been comparative.
Those are voice, emphasis, and claim-level calls. No agent makes them.

**But handing him a finished PDF makes that pass expensive** — he has to FIND the decisions before he
can make them, and expensive is what gets skipped on a tired day. In his words: "my human QC is an
important step but sometimes I get lazy." The fix is not more discipline from him. It is presenting
the decisions instead of the artifact.

```markdown
## Decisions for you — [N] calls before this ships

1. **[What the CV currently does]** — [the one-line reason it is a judgment call, not a mechanical fix]
   → Alternative: [the specific other option, written out]
   → *Keep / switch?*

2. **[...]**
   → Alternative: [...]
   → *Keep / switch?*
```

**Rules for this block:**
- **3 to 6 items. Never zero.** An empty block means you did not look; every tailored CV contains
  claim-level and emphasis choices someone has to own.
- **Pre-name the alternative.** Nick picks, he does not generate. "Consider revisiting the summary" is
  not a decision, it is homework.
- **Only judgment calls.** Mechanical fixes are already applied per Step 10b. If it has one right
  answer, it does not belong here.
- **Always include, when present:** any verb where you chose more conservative wording than the source
  file permits; any claim whose scope is arguable ("production", scale figures, attributed outcomes);
  what the summary leads with; and which proof carries the argument for this specific role.
- Then, and only then, print the file paths and the rest of the summary below.

```markdown
## CV Generated — [Role Title] at [Company]

**Format:** [US/UK/DACH/international] | **Market:** [market]
**CV PDF (send file):** `output/<company-slug>/MMDDYY-magnuson.pdf`
**CV YAML (source):** `output/<company-slug>/MMDDYY-magnuson.yaml`
**CV Markdown (for review):** `output/<company-slug>/MMDDYY-magnuson.md`
**Cheat sheet:** `output/<company-slug>/MMDDYY-[role-slug]-cheatsheet.md`

### QC Summary (from Step 6b self-review)
- **Keyword coverage:** N/10 matched [list any unfixable gaps]
- **Claims verified:** N checked, N corrected
- **Issues fixed:** [list or "none"]
- **Language consistency:** clean / N items fixed

### Deep Review Verdict (from Step 10b — always runs)
- **Deep review file:** `output/<company-slug>/MMDDYY-magnuson-DEEP-REVIEW.md`
- **Recruiter (phone invite?):** Yes / No / Maybe
- **Hiring Manager (interview?):** Yes / No / Maybe
- **Competitor shortlist rank:** N of 8
- **Top 3 critical/important issues surfaced:** [one-line each]
- **Recommendation:** [one-line — proceed, fix before submitting, or reconsider]

### ATS Keyword Coverage
| Keyword | Present? | Where |
|---------|----------|-------|
| [keyword 1] | ✅ | Professional Summary |
| [keyword 2] | ✅ | Project: [name] |
| [keyword 3] | ⚠️ | Gap — candidate lacks this skill |

**Coverage: N/10 keywords**

### Projects Selected
1. [Project name] — [one-line rationale]
2. ...

### Pipeline
[✅ CV Used field updated in pipeline for [Company]] OR [⚠️ [Company] not in pipeline — add with: `/pipe add "[Company]" "[Role]"`]

### Suggested Next Step
- Review output: `/review-cv output/<company-slug>/MMDDYY-magnuson.md`
- Open the printable PDF: `open output/<company-slug>/MMDDYY-magnuson.pdf`
- When ready to apply: `/pipe update "[Company]" Applied`
- Before interview: `/prep-interview "[Company]"`
```

## Edge Cases

- **URL fetch fails**: Ask user to paste the JD text directly. Do not attempt to reconstruct the JD from partial content.
- **Too few projects**: If fewer than 3 relevant projects exist, use all available. Note in summary: "Only N projects available — consider adding more to `data/projects/`."
- **Missing profile.md**: Proceed without personal details. Omit compensation/availability from cheat sheet. Flag in summary.
- **Missing `coaching/coached-answers/`**: Skip that section of cheat sheet silently. Read the whole directory when present, not a single file.
- **Keywords not coverable**: If a keyword can't be added naturally to the CV (e.g. a technology the candidate genuinely doesn't have), flag it in the ATS coverage table as `⚠️ Gap — omit` and note it in the summary as a genuine skill gap.
- **Multiple roles at same company in pipeline**: Update the most recently active matching entry.
