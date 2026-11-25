---
name: resume-tailor
description: Use when the user wants to tailor a resume to a job description, convert experience into quantified bullets, improve how a resume parses and scans, fix a resume that gets no responses, or prepare resume evidence for AI-company applications.
---

# Resume Tailor

Rewrite resumes to match a specific job description without inventing anything. A resume must work in two modes: a fast human scan and structured retrieval inside an applicant-tracking system. Exact scan-time and ATS-adoption statistics vary by study and population, so do not repeat them as universal facts. The job is to make the resume parseable, make the first screen land, and make every line survive a follow-up question.

## Before starting, collect

1. The current resume.
2. The full job description.
3. Ask: "Tell me 2-3 things you actually did in that role that aren't on the resume, especially anything with a number attached (scale, latency, cost, users, revenue, time saved)." Most resumes undersell; the raw material lives in the person's head.

Do not generate anything until you have at least items 1 and 2.

## Process

### Step 1: Extract what the JD screens for
List in order of emphasis: hard requirements (named tools, domains; weight what appears early or repeats), the problem behind the role (visible in the responsibilities), and the JD's exact vocabulary. If they say "evals," never write "quality assessment."

### Step 2: Map evidence into three buckets
- **Direct hit**: they did exactly this. Leads the relevant section.
- **Adjacent**: same muscle, different context. Reframe honestly.
- **Gap**: no evidence. Flag it; never fill it with wording. Gaps are handled in the cover letter or interview, not by lying.

### Step 3: Rewrite
- **Design the top third for a fast scan**: target-matching title language, strongest company or project, domain fit, and proof links must be visible before any dense detail.
- **Every bullet becomes evidence, not adjectives**: use the XYZ pattern, "accomplished X, measured by Y, by doing Z." If Y is missing, ask for it; estimates marked with "~" are fine, invented numbers are not.
- **Strip generic AI cadence**: Phrases like "leveraged cutting-edge AI" get cut unless tied to a model, data, eval, or outcome the user actually touched. Tailoring must add relevant evidence, not synthetic polish.
- **Keep it database-readable**: standard section headers, real dates, exact role nouns from the JD, no tables or graphics in the text flow.
- **For AI roles, surface proof links**: GitHub, papers, demos, launches. Ask whether the linked repo shows tests, a clear README, and something deployed; a weak public repo is a risk, not an automatic plus.
- Same length or shorter than the original. Tailoring adds relevance, not volume.

### Step 4: Defensibility pass
Read each rewritten bullet and ask: does this survive two follow-up questions about baselines, trade-offs, and what the user personally did? If not, weaken it or cut it. At AI-native companies every resume line becomes an interview thread.

## Output format

1. **The tailored resume**, full text, ready to paste.
2. **Change log**: what moved, what was rewritten, which JD requirement each change serves.
3. **Gap list**: unmet requirements, each with a one-line plan (cover letter, pre-interview study, or ignore as wishlist).
4. **Resume-to-interview map**: for each of the top 5 bullets, the most likely interview probe and what the user must be ready to say. This is where tailoring becomes interview prep.

## Hard rules (apply at every step, no exceptions)

- Never invent employers, titles, dates, tools, metrics, or outcomes. If the user cannot support a claim when you probe it, it does not go in. This mirrors what AI companies themselves ask of candidates: AI to sharpen true material, never to create experience.
- If the truthful resume does not clear the role's bar, say so plainly and point at the gap. That is more useful than wording tricks.
- One resume per JD. Generic resumes are what got the user here.
