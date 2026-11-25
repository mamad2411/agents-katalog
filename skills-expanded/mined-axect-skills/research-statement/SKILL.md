---
name: research-statement
description: Write, diagnose, and tailor research statements (statements of research interests, the narrative of what the applicant has done and will pursue) for postdoc, fellowship, and early-career applications, following an evidence-based guideline compiled from funder and university sources (NASA Hubble Fellowship review, DFG Walter Benjamin and proposal tips, MSCA handbooks, Schmidt AI in Science, Schmidt Science Fellows, AAS, Oxford Physics, Cornell, Harvard, Yale, UCLA, and practising physicists). Korean working draft, user revision, then English final. Modes are draft, diagnose (checklist verdicts with line evidence plus `scripts/rs_check.py`), tailor (per call type and per host fit paragraph), and translate. Use when the user mentions 연구계획서, research statement, statement of research interests, "연구계획서 써줘/진단/수정/맞춤", or adapting one statement to a specific call. Use `research-proposal` when the call asks for a research or project proposal, project description, research outline, or work plan (제안서), `academic-jobs` to find and curate calls, `adversarial-review` for hostile audits of paper drafts, and `workshop-paper-review` for reviewing someone else's paper.
---

# Research Statement

Produce research statements that let a busy, partly non-specialist committee answer five questions quickly, and back every structural choice with the guideline in `references/evidence.md`.

## When to use

- Drafting a research statement for a postdoc, fellowship, or early faculty call.
- Diagnosing an existing draft against the checklist before revision.
- Tailoring a base statement to a call type (PI-group postdoc, independent fellowship, AI-for-science fellowship, short 1~2 page statement) or to a specific host.
- Translating an approved Korean draft into the English submission.

Not for project proposals, project descriptions, research outlines, or templated Part B documents (`research-proposal`); route by the document name in the call, and when a call asks for both, keep the statement on the person and trajectory and the proposal on the project. Not for cover letters as such (reuse the fit and "why me" material, but a cover letter has its own job), not for reviewing other people's papers. Once a paragraph's content is settled, use `academic-prose` for the sentence pass (wording, claim strength, referents, real word counts); `rs_check.py` stays the document-level check.

## Inputs to confirm

Ask only for what files and the call text cannot answer.
- The call text or URL. Its page limit, required sections, evaluation criteria, and template headings override every general rule here.
- Call type (table below) and, if known, host group and people.
- Fact sources: CV, publication list, project notes, previous statements and reviews of them.
- Which research axis to lead with when the applicant has several (e.g. physics-led vs method-led variants).
- Output directory. Default: next to the existing statements.

## The five questions

Every paragraph should answer one of these. A reader outside the subfield should be able to answer all five after one read.

1. What problem do you work on, and why does it matter?
2. What have you established, and what was your own contribution?
3. What will you do next, and how?
4. Why are you the person to do it?
5. Why here, and why now?

## Workflow

1. **Read the call.** Extract hard constraints into the notes file: length, fonts, required headings, criteria and their weights, letters, host or mentor requirements. If the call has a template, mirror its headings exactly; evaluators mark by checklist and misplaced content scores zero.
2. **Classify the call** and set the balance:

   | Call type | Past : future | Emphasis |
   |---|---|---|
   | PI-group postdoc | 1 : 1 | record, one or two projects that mesh with the group |
   | Independent theory fellowship | 1 : 2 | own programme, risks and fallbacks, why this institute |
   | AI-for-science fellowship | 1 : 2 | scientific bottleneck first, why AI is needed, validation and reproducibility, both mentors |
   | Short statement (1~2 pages) | 1 : 1 | opening paragraph, one project, no figure |

3. **Collect facts from files only.** Mark unpublished work as unpublished, keep every result inside its proven scope, record each collaborator's role, and never infer contribution from author order. Unknowns stay as explicit `[확인 필요: ...]` slots.
4. **Plan before prose.** One central question. Two or three objectives, each with a verifiable deliverable, a first-year step, and one risk with its fallback. Two or three past results with outcome verbs and the applicant's own role. Three to five state-of-the-art references that show what is new (verify with `reference-search` / `bibtex-gen`; never cite from memory). A "why me" paragraph, a fit paragraph, a closing paragraph.
5. **Draft in Korean** as `<name>_ko_vN.md` plus `_guide/<name>_notes_vN.md` mapping each factual sentence to its source and listing open questions.
6. **Diagnose** with the checklist below and `python3 scripts/rs_check.py DRAFT.md`. Write `_guide/<name>_diagnosis_vN.md`: verdict per item (○ met, △ partial, × missing) with line numbers, a fix list ordered by impact, and the decisions only the user can make. Show the user the table and the decisions; do not silently rewrite.
7. **Revise with the user**, bumping `vN`. Translate to English only after the user approves the Korean version, keeping the user's typesetting template if one exists, then run the check again on the English file and render the PDF to confirm length.
8. **Tailor per call.** Keep a base version per research axis and swap only the fit paragraph, the call-type balance, and terminology the call uses. Check that the statement does not repeat the cover letter sentence for sentence.

## Core rules

Short form; quotes and sources in `references/evidence.md`.

1. **Win the first page.** The opening paragraph states the central question, why it matters, and the applicant's approach. No personal anecdotes.
2. **One programme, not a list.** Pick an overarching theme, give the key project most space, and leave miscellaneous work out. Two aims that only share a section heading read as stapled together.
3. **Past work is evidence.** Two or three results, each with what it showed (not "studied" or "worked on") and the applicant's role. Let the physics carry the weight, not journal names.
4. **The future is the centre.** Two or three verifiable objectives, short, medium, and long horizons, and something to start on immediately. Objectives follow logically from the state of the art.
5. **Feasibility shows.** Preliminary results, risks with alternatives, high-risk parts paired with lower-risk ones and placed later, all inside the funding period.
6. **Independence.** Not an extension of the adviser's or current host's project; say which question is new. Do not jump so far that competence becomes invisible.
7. **Specific fit.** Connect named resources and people to a specific objective, say what the host gains, and say why now. Lists of names and "the institute has X" do not count.
8. **Write for outsiders.** Define terms at first use, give a concrete example before the general statement, use headings, keep the text self-contained (evaluators ignore links).
9. **Interdisciplinary and AI calls.** Lead with the scientific bottleneck, explain why AI is the right tool and how its output is validated, address data quality and reproducibility, and assume a mixed panel. Core AI research alone is out of scope for AI-for-science schemes.
10. **Honesty.** Neither exaggerate nor be falsely modest; cite the key prior work (missing references are noticed at once); separate one's own work from others'; disclose generative-AI use where the call asks.
11. **Format.** Obey the call, first person singular for individual fellowships, a closing paragraph with the overall vision, proofread.
12. **The person is assessed too.** The statement must tell the same story as the CV and the letters.

## Resolved conflicts between sources

| Issue | Decision |
|---|---|
| Which verbs (some guides prefer "investigate" to "explore"; others reject both) | Past work: outcome verbs (showed, proved, measured). Objectives: verbs with a defined product (determine, derive, decide). Avoid explore and study |
| How big to sound ("Go big!" vs penalties for over-ambition) | Big question in the opening, deliverables that fit the funding period |
| Past to future balance | 1 : 2 for independent fellowships, 1 : 1 for PI-group postdocs |
| Distance from the PhD | Large pivots only where the scheme asks for one (Schmidt Science Fellows); otherwise existing methods applied to a new question |

## Checklist

- [ ] The opening paragraph alone gives the central question, its importance, and the approach.
- [ ] Each of the five questions has a paragraph that answers it.
- [ ] Two or three past results, each with an outcome verb and the applicant's own role.
- [ ] Two or three objectives, each with a verifiable deliverable, a first-year step, and a risk with a fallback.
- [ ] The objectives serve one question; one sentence says what each uses from the others.
- [ ] Reads as the applicant's own programme, not the host's or adviser's.
- [ ] The fit paragraph links specific host resources or people to an objective and says what the host gains.
- [ ] Terms defined at first use; a concrete example precedes each general claim; headings present.
- [ ] AI variant: scientific bottleneck first, why AI, validation and reproducibility.
- [ ] Unpublished work marked; no claim beyond proven scope; three to five verified external references.
- [ ] Call limits and headings obeyed; first person singular; no sentences copied from the cover letter.
- [ ] A closing paragraph restates the overall vision.
- [ ] One specialist and one non-specialist have read it and summarised it back.
- [ ] `rs_check.py` reports zero em/en dashes, zero hype words, zero non-Hangul CJK in Korean prose, and no leftover placeholders in a version meant for submission.

If the project keeps reviews of earlier statements (e.g. a `_guide/` folder), read them first and add their recurring failures to this checklist for the session.

## scripts/rs_check.py

Standard-library Python 3. Reports, per Markdown file: share of each `## ` section (whitespace-free characters, references excluded), em/en dash count, non-Hangul CJK count, weak verbs, hype words, placeholder slots, citation markers used versus reference entries. `--strict` exits 1 if dashes, hype words, CJK, or placeholders remain.

```bash
python3 scripts/rs_check.py research_statement_ko_v2.md
python3 scripts/rs_check.py --strict research_statement_en_v1.md
```

The section shares are raw; map them to past, future, and fit yourself, because headings differ between drafts.

## Output layout

```
<statement dir>/
  <name>_ko_vN.md             Korean working drafts
  <name>_en.typ | .tex | .pdf English submission
  _guide/<name>_notes_vN.md   claim-to-source map, open questions
  _guide/<name>_diagnosis_vN.md  checklist verdicts and fix list
```

## References

- `references/evidence.md`: each rule with verbatim quotes from the sources, the call-type table with its basis, and known gaps in the evidence.
- `references/sources.md`: the 24 sources with type and URL.
