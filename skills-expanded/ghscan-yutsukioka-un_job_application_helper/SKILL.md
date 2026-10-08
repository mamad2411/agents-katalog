---
name: apex-cover-letter-pointers
description: Provide 2–3 strategic recommendations for crafting a cover letter tailored to the target role. This is Phase 5 guidance only (not a full letter draft). Focus on narrative theme, evidence selection, gap-addressing, and how to complement (not duplicate) the CV/Admin Profile. Use this skill only when the user asks for cover letter pointers or when building the complete strategy report.
---

# apex-cover-letter-pointers

## Purpose

This skill provides high-leverage guidance for the cover letter narrative:
- what to emphasize,
- which evidence to use,
- how to address gaps diplomatically,
- and how to mirror the JD language without copying the CV.

## Shared definitions

Apply the expert lens, collaboration rules, guardrails, and quality loop
protocol defined in `apex-guardrails`.
Output format profile: `strategy_markdown`.

## Inputs

Required:

- `JOB_DESCRIPTION_TEXT`: to align the cover letter with the role's
  mission and requirements.
- `USER_JOB_HISTORY_TEXT`: to identify standout experiences and
  personal motivations.

Optional (Recommended for higher quality):

- `apex-candidate-evidence-bank` output: to address gaps strategically.
- `apex-star-story-blueprints`: 3–4 STAR story blueprints tied to critical job requirements using the candidate’s evidence.
- `apex-uvp-statement` output: for thematic unity across documents.
- `TERM_EXTRACTOR`: five high-priority terms from a job description with star
  ratings, ATS synonyms, JD-grounded rationale, and resume-ready examples in
  a strict four-line format.
- `JD_KEYWORD_BANK`: an expanded 20–40 phrase keyword bank.

## Output format

Return:

## Cover Letter Integration Pointers

Provide 2–4 short paragraphs or bullets, each focused on one of:

1. **Core Narrative Theme:** Suggest a unifying story or theme that
   ties together motivation, UVP and alignment with the job and
   organization’s mission.
2. **Evidence selection:** Which 1–2 STAR stories to feature and why
3. **Gap Addressing Strategy:** Provide advice on how to proactively
   address any critical gaps identified (e.g. lacking direct
   experience) using transferable skills or a commitment to learn.
4. **Complement, Don’t Repeat:** Remind the user that the cover letter
   should add context and personality, rather than re‑listing CV
   bullet points. Recommend highlighting motivation, cultural fit, or
   values alignment.

## Rules

- Do not draft the cover letter itself. Keep each recommendation
  concise but specific, ideally one short paragraph.
- Ensure suggestions align with the organization’s tone and the
  analysis from earlier phases.
- Use term text only (no star symbols).
- Mention UN Values & Behaviours only when they are credible and
  supported by the candidate's evidence.

## Steps

1. Identify the JD’s top 2–3 requirements and the candidate’s most compelling motivations and relevant experiences.
2. Recommend a narrative theme and which STAR story(ies) to highlight.
3. Identify any gaps and propose ways to address them positively.
4. Provide 2–4 recommendations of concise pointers in the required format.
