---
name: cover-letter
description: Write, diagnose, and tailor academic cover letters for postdoc, fellowship, and early faculty applications, plus two related forms that follow the same rules, UK supporting statements written against a person specification and European motivation letters. Rules come from an evidence-based guideline compiled from university career offices (Berkeley, Yale, Northwestern, UConn, UC Davis, Cornell, Toronto), UK recruitment guidance (jobs.ac.uk, University of Reading), career columns (Inside Higher Ed, Chronicle), and physicists' own advice. Korean working draft, user revision, English final; `scripts/cl_check.py` checks length, dashes, clichés, hedges, placeholders, and wrong institution names. Use when the user mentions 커버레터, cover letter, covering letter, 지원서 편지, motivation letter, supporting statement, or person specification. Use `research-statement` for the research statement or proposal itself, and `academic-jobs` to find calls.
---

# Cover Letter

A cover letter is a short argument that this applicant fits this position, built from evidence the rest of the file supports. It frames the CV and research statement; it does not repeat them.

## When to use

- A cover letter for an advertised postdoc, research associate, fellowship, or early faculty post.
- A UK supporting statement against a person specification (essential and desirable criteria).
- A motivation letter for a European fellowship or institute.

Not for the research statement itself (`research-statement`), not for reference letters, and not for emails to prospective hosts, mentors, or referees (`contact-email`).

## Inputs to confirm

Ask only for what files and the call cannot answer.
- The call text: title, reference number, where it was posted, addressee, page or character limit, requested documents, and any person specification or explicit questions.
- The research statement and CV that go with this letter; the letter must agree with them and must not copy their sentences.
- Facts the call requires that files may lack: citizenship or work-permit status, start date, PhD date, current position.
- The name form to use (the one on the CV and the one referees will enter in upload portals must match).

## Workflow

1. **Read the call twice.** List every explicit ask (documents, citizenship statement, referee contacts, start date, questions to answer) and every stated priority in the order the call gives them; that order sets the order of the letter. For a UK post, copy the person specification criteria verbatim into the notes.
2. **Choose the form and length.**

   | Form | Length | Shape |
   |---|---|---|
   | PI-group postdoc or research associate | about one page | opening, one research paragraph, one contribution and fit paragraph, logistics, close |
   | Independent fellowship or institute | one to two pages | as above plus the research direction and why this institute |
   | Faculty or senior post | one and a half to two pages | research, future agenda, teaching, service, fit |
   | UK supporting statement | the stated character or word limit | criteria as headings, essential criteria first and in order, one evidence example each |
   | Motivation letter | the stated limit, often two pages | motivation, fit with the programme's aims, career goals, what the applicant brings |

3. **Collect facts from files only.** Contributions as recorded (never inferred from author order), unpublished work marked as such, every date and contact from a file; unknowns stay as `[확인 필요: ...]`.
4. **Draft in Korean** as `<name>_ko_vN.md` with `_guide/<name>_notes_vN.md` mapping each factual sentence to its source and listing open questions. Lead with the questions that block submission (citizenship, name form, referees, dates).
5. **Check** with `python3 scripts/cl_check.py DRAFT.md --expect "<institution>" --forbid "<other institutions>"` and the checklist below. Record verdicts (○ met, △ partial, × missing) with line numbers.
6. **Revise with the user**, then translate to English only after approval. Render the PDF and confirm it fits the limit; sign it and use letterhead if the applicant has one.
7. **Cross-check the set**: the letter, research statement, and CV tell one story, the letter adds what the others cannot (why this post, what the applicant brings, logistics), and no paragraph is copied from the statement.

## Core rules

Short form; quotes and sources in `references/evidence.md`.

1. **Interpret, do not list.** Select one or two results and say why they matter for this post. A paragraph that reads like the CV has no purpose of its own.
2. **Open with the position and a thesis.** First sentence or two: the post (title, sub-field, reference number), the applicant's current role, and the strongest reason for fit.
3. **Explain the research for outsiders.** The question, the applicant's contribution, and why it matters in the wider field, in plain terms. Detail belongs in the research statement; the letter gives direction.
4. **Say what the applicant will contribute, not only what they want.** Concrete skills, results, or a project they would push forward in this group.
5. **Specific fit.** Address the ad's stated needs in its own terms; name a real connection to the group's work, people, or resources; if the profile differs from the ad, explain what transfers and why that is an advantage. A sentence that could go unchanged to five other groups is cut or made specific.
6. **Evidence over adjectives.** Show with facts (results, outputs, numbers, recognition); drop "passionate", "excellent", "uniquely qualified", "perfect fit", "prestigious institution".
7. **Tone of a colleague.** Confident and measured; no hedges ("I will try", "I hope to"), no effusive praise of the institution or of advisers, not every sentence starting with "I".
8. **Honesty.** No exaggeration and no false modesty; state one's own role in collaborative work plainly; state missing qualifications honestly with the closest transferable evidence.
9. **Logistics are part of the letter.** Names, titles, department, and institution correct; addressed to the named person or the search committee; enclosed and separately sent materials listed; availability and any required status stated; signed PDF.
10. **Follow the call.** Its length, questions, and documents override general advice; send nothing that was not requested; check that each tailored letter goes to the right institution.
11. **The applicant's own voice.** Several sources warn that letters written by AI read as generic. Drafts produced with assistance must be revised by the applicant, contain only verified facts, and sound like the applicant.
12. **UK supporting statements are scored criterion by criterion.** Use the criteria as headings, essential first and in the given order, one specific example each (situation, own action, result), then the desirable criteria the applicant meets.

## How much the letter weighs

Readers differ. Some physics search committees barely read cover letters but punish errors in names; career offices for humanities faculty posts call it the most important document. Default for physics and astronomy postdocs: short, specific, and error-free, with the scientific case carried by the research statement and letters of reference.

## Checklist

- [ ] The first two sentences name the post and give the main reason for fit.
- [ ] Every explicit ask in the call is answered (documents, citizenship or status, referee contacts, start date, questions).
- [ ] One or two results, each with the applicant's role and why it matters here; no CV recitation.
- [ ] A paragraph says what the applicant would contribute to this group, with one concrete example.
- [ ] Fit is specific: the ad's own terms, a real connection, and an honest bridge for any mismatch.
- [ ] No clichés, hype, or hedges; claims carry evidence.
- [ ] Reads as a future colleague: no effusive praise, varied sentence openings.
- [ ] Unpublished work marked; nothing beyond proven scope; consistent with CV and research statement, no copied paragraphs.
- [ ] Names, titles, department, institution, reference number, and date correct; the right institution throughout.
- [ ] Within the length limit after rendering; signed; enclosures listed.
- [ ] UK form: every essential criterion has a heading and one example; desirable criteria covered where met.
- [ ] `cl_check.py` reports zero dashes, clichés, hedges, placeholders, and forbidden names in the version meant for submission.

If the project keeps reviews of earlier letters (e.g. a `_guide/` folder), read them first and add their recurring failures to this checklist for the session.

## scripts/cl_check.py

Standard-library Python 3. For each Markdown or text file: word and character counts (body only, before a `## References` or similar heading), em/en dashes, non-Hangul CJK, clichés and hype words, hedges, share of sentences that start with "I", placeholder slots, and institution-name checks (`--expect NAME` must appear, `--forbid NAME` must not). `--strict` exits 1 on dashes, CJK, clichés, hedges, placeholders, missing expected names, or forbidden names.

```bash
python3 scripts/cl_check.py cover_ko_v2.md
python3 scripts/cl_check.py --strict cover_en.md --expect "Example Institute" --forbid "Other University" --forbid "Third Lab" --max-words 600
```

## Output layout

```
<application dir>/
  <name>_ko_vN.md              Korean working drafts
  <name>.typ | .tex, cover.pdf English submission
  _guide/<name>_notes_vN.md    claim-to-source map, open questions
  _guide/<name>_diagnosis_vN.md  checklist verdicts and fix list
```

## References

- `references/evidence.md`: each rule with verbatim, string-checked quotes from its sources, and gaps in the evidence.
- `references/sources.md`: the 17 sources with type and URL.
