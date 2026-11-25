---
name: research-proposal
description: Write, diagnose, and fit research or project proposals for fellowships and grants, the document that says what will be done, why, how, how success will be judged, and with what resources, from short institute-fellowship proposals (1~5 pages) to templated project descriptions (Humboldt research outline, MSCA Part B, DFG Walter Benjamin, ERC Part I/II, NSF project description). Rules come from an evidence-based guideline compiled from funders (ERC, DFG, Humboldt Foundation, NSF, MSCA handbooks and annotated templates, Schmidt programmes, Oxford Physics) and "Ten Simple Rules for Getting Grants". Builds a criteria map, a logic chain from gap to deliverable, an objective-to-milestone work plan, and a risk table before prose; Korean working draft, user revision, English final; `scripts/rp_check.py` checks required elements, objective count, length, dashes, hype, weak verbs, placeholders, and citations. Use when the call asks for a research proposal, project proposal, project description, research outline, research plan with work plan, Part B, 제안서, 연구 제안서, 과제 제안서, or 프로젝트 계획서. Use `research-statement` when the call asks for a research statement or statement of research interests, `cover-letter` for letters, `contact-email` for emails to hosts.
---

# Research Proposal

A proposal is a plan someone can fund: a sharp question, objectives that answer it, methods that can deliver them within the period, a way to tell whether they did, and the resources and environment to do it. A research statement argues who the applicant is; a proposal argues what this project will achieve.

## Which skill

Route by the document the call names. "Research statement", "statement of research interests": `research-statement`. "Research/project proposal", "project description", "research outline", "Part B", "work plan": this skill. When a call asks for both, write both and keep them from repeating each other: the statement carries the trajectory and the person, the proposal carries the project.

## Inputs to confirm

Ask only what the call and files cannot answer.
- The call text, template, and evaluation criteria with weights; page or character limits; whether references count toward the limit; required headings; separately scored parts (abstract, Part I vs Part II, data management, ethics).
- Duration and budget of the award, and what it may pay for.
- Host, mentor, or supervisor and what they must provide; host resources relevant to the project.
- The base research material (an existing research statement or earlier proposal), project notes, preliminary results with their scope and publication status.
- Name form and any generative-AI disclosure the call requires.

## Anatomy by length

| Length | Shape |
|---|---|
| 1~2 pages (institute fellowships, short proposals) | title and one-paragraph summary; question and gap; two or three objectives each with approach and deliverable; feasibility and risk in one paragraph; why this host; 3~6 references |
| 3~5 pages (research outlines, fellowship proposals) | the above plus state of the art with the advance beyond it, methods per objective, a timeline or work-plan table, a risk table, expected results and impact |
| Templated (MSCA, DFG, ERC, NSF) | the funder's headings exactly, in order; content placed where the evaluator's checklist expects it; separately scored parts written to stand alone |

## Workflow

1. **Read the call and build a criteria map**: each evaluation criterion and required heading mapped to the section that answers it. Missing a mapped section is the most common avoidable loss (MSCA checklists, NSF and Humboldt return non-compliant applications without review).
2. **Write the logic chain before prose** in `_guide/<name>_plan_vN.md`: gap, central question, objectives (two or three, each answerable), method per objective, deliverable per objective, how success is judged, what changes if it succeeds. Every objective must trace to the question and to the work plan.
3. **Work plan and risk table.** Objectives to work packages or phases to milestones to months, inside the award period, riskier parts later and paired with lower-risk ones. For each major scientific risk, the observable sign and the fallback.
4. **State of the art from verified sources**: what is known, what is not, what this project adds. Use `reference-search` and `bibtex-gen`; never cite from memory.
5. **Draft in Korean** as `<name>_ko_vN.md` with `_guide/<name>_notes_vN.md` mapping each fact to its source and listing open questions. Mark unpublished preliminary results and keep claims inside their proven scope.
6. **Check** with `python3 scripts/rp_check.py DRAFT.md` and the checklist. Write `_guide/<name>_diagnosis_vN.md` with verdicts (○, △, ×) and line numbers, a fix list by impact, and the decisions only the user can make.
7. **Revise with the user**, translate after approval, run the check on the English file with `--strict`, render, and confirm the page count including whatever the call counts.
8. **Cross-check the package**: CV, research statement, letters, and budget tell the same story; the budget and the work plan match line by line.

## Core rules

Short form; quotes and sources in `references/evidence.md`.

1. **Answer the funder's five questions.** What will be done, why, how, how you will know it worked, and what results or benefits follow (NSF). ERC splits them: Part I makes the case for the idea, Part II for its implementation.
2. **A sharp question, not a topic.** One central question, stated early, with the gap it closes. Ambition belongs in the question and the expected advance, not in adjectives.
3. **Two or three objectives that follow from the state of the art**, each specific and verifiable, each with its method and deliverable. Hypothesis- or question-driven beats exploratory.
4. **State of the art that leads somewhere**: brief, current, only what bears on the project, citing the key prior work (including likely reviewers'), ending in what is missing.
5. **Methods tied to questions.** For each objective: why this method can answer it, what exists and what must be developed, what evidence it produces.
6. **Work plan inside the period.** Timeline or work-package table linked to objectives, milestones that show progress, scope matched to time and money; do not propose too much.
7. **Risks with fallbacks.** Real scientific and methodological risks, not generic ones; each with mitigation; high-risk parts combined with safer ones and placed later.
8. **Feasibility from evidence.** Preliminary results with what they imply for each aim, the applicant's matching expertise, access to the resources needed. Where the funder assesses feasibility separately (ERC Part II), keep it out of the idea section.
9. **Environment and host**: why this host and why now, what the host provides that the project needs, what the applicant brings to them.
10. **Resources consistent with the plan.** Every requested resource justified; nothing inflated; the budget and the work plan agree.
11. **Write for generalists and specialists.** Summaries at the top of sections, defined terms, figures or tables for the plan, self-contained text (no reliance on links or appendices the call did not ask for).
12. **Comply exactly.** Headings, limits, fonts, required parts (abstract, data management, ethics, AI disclosure); readable formatting rather than cramming.

## Resolved conflicts between sources

| Issue | Decision |
|---|---|
| Where feasibility goes | Follow the funder: ERC (2026 onward) keeps feasibility out of Part I; most others expect it with the methods |
| Ambition vs over-ambition | Ambitious question and advance; deliverables scoped to the period and budget |
| Length | Shorter than the limit is fine if complete (Ten Simple Rules); never exceed it |
| Own idea vs host input | The proposal is the applicant's own work; develop it with the host or supervisor where the scheme expects that (MSCA), never have them write it (Humboldt) |

## Checklist

- [ ] Criteria map complete: every criterion and required heading has a section.
- [ ] Title and summary state the question, the approach, and the expected advance; the summary stands alone.
- [ ] One central question and the gap it closes, stated on the first page.
- [ ] Two or three objectives, each verifiable, each with method and deliverable, each traceable to the question and the work plan.
- [ ] State of the art: current, focused, verified references, ending in what is missing.
- [ ] Work plan or timeline inside the award period with milestones.
- [ ] Risk table or paragraph: real risks, signs, fallbacks; riskier parts later.
- [ ] Preliminary results marked by status and kept inside scope; applicant's own role clear.
- [ ] Host and environment: specific resources linked to objectives; why now.
- [ ] Resources and budget consistent with the plan (when requested).
- [ ] Expected results and impact concrete and proportionate.
- [ ] Limits, headings, fonts, and required parts obeyed; AI disclosure if asked.
- [ ] Consistent with CV, research statement, and letters; no copied paragraphs.
- [ ] One specialist and one non-specialist have read it.
- [ ] `rp_check.py --strict` passes on the version to submit.

If the project keeps reviews of earlier proposals or statements (e.g. a `_guide/` folder), read them first and add their recurring failures to this checklist for the session.

## scripts/rp_check.py

Standard-library Python 3. For each Markdown file: share of each `## ` section, required elements found or missing (objectives, state of the art, methods, work plan or timeline, risks or fallbacks, expected results; override with `--require`), number of objective headings (warns outside 2~3), em/en dashes, non-Hangul CJK, weak verbs, hype words, placeholders, cited versus listed references, and characters against `--max-chars`. `--strict` exits 1 on missing elements, dashes, CJK, hype, placeholders, citation mismatches, or overflow.

Element detection is keyword matching on the body (Korean and English). A miss means "no explicit wording", which is worth fixing because evaluators skim for it, but a paraphrase can also cause it; confirm by reading before rewriting.

```bash
python3 scripts/rp_check.py proposal_ko_v1.md
python3 scripts/rp_check.py --strict proposal_en.md --max-chars 9000
python3 scripts/rp_check.py proposal_ko_v1.md --require objectives,methods,risks,host
```

## Output layout

```
<application dir>/
  <name>_ko_vN.md                Korean working drafts
  <name>_en.typ | .tex | .pdf    English submission
  _guide/<name>_plan_vN.md       criteria map, logic chain, work plan, risk table
  _guide/<name>_notes_vN.md      claim-to-source map, open questions
  _guide/<name>_diagnosis_vN.md  checklist verdicts and fix list
```

## References

- `references/evidence.md`: each rule with verbatim, string-checked quotes from its sources, and gaps in the evidence.
- `references/sources.md`: the sources with type and URL.
