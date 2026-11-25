---
name: literature-review-skills
description: "Guide literature reviews from question refinement to evidence-grounded drafting, including journalism and communication, library and information science, and other disciplines. Use for 文献综述、新闻传播、情报学、综述写作、研究空白, or grill me / 追问 / 模拟答辩 about a review."
metadata:
  version: "0.3.0"
---

# Literature Review Skills

This is the entry point for the five literature-review skills in this repository.

Use it when a user wants help with a literature review but has not yet chosen a specific skill. Route the user to the smallest skill that matches the current stage of work.

## Start Here

Read [discipline routing](references/discipline-routing.md), then only the matching discipline profile. Read [review workflow](references/review-workflow.md) for search, extraction, and drafting. Read [research interview](references/research-interview.md) when the user requests grill me, pressure-testing, or has unresolved scope decisions.

Use the user's language. Reuse information already supplied. Establish review type, question, discipline, scope, and available evidence. A scoped conceptual or historical question is valid; do not force causal hypotheses onto every review.

For a complete review, follow the five stages below and then the drafting workflow. With no sources, provide a search plan and outline, not literature findings. With sources, draft thematic synthesis with claim-to-source links and explicit limitations.

## Loading Stage Instructions

Resolve paths relative to this SKILL.md, not the working directory. Open the selected file before executing its workflow; naming a skill is not enough:

| Stage | File to read |
|---|---|
| Question | [refine-literature-question](skills/refine-literature-question/SKILL.md) |
| Structure | [decompose-review-modules](skills/decompose-review-modules/SKILL.md) |
| Methods | [compare-research-methods](skills/compare-research-methods/SKILL.md) |
| Synthesis | [map-literature-contradictions](skills/map-literature-contradictions/SKILL.md) |
| Gap | [locate-review-research-gap](skills/locate-review-research-gap/SKILL.md) |

If an installer omitted these files, report which are missing and request the complete repository or installation of the named stage skills. Do not claim to have loaded absent instructions. Individual stage skills carry their own references and remain usable independently.

## Skill Map

1. `refine-literature-question`
   - Use when the user has a broad topic and needs a sharp one-sentence review question.
2. `decompose-review-modules`
   - Use when the user already has a core question and needs 3-5 review modules.
3. `compare-research-methods`
   - Use when the user needs to justify method choices or compare method routes.
4. `map-literature-contradictions`
   - Use when the user has conflicting findings, notes, claims, or abstracts and needs a structured synthesis.
5. `locate-review-research-gap`
   - Use when the user needs to turn the review ending into a concrete research gap or future study direction.

## Source Integrity

Before starting, check whether real references (full records, abstracts, or notes) are already available. Ask only if this is unresolved and the user has not requested no questions; otherwise record the evidence limit and proceed with a plan. Follow `references/source-integrity.md`: use only sources the user provided or that are verified, tag each with a status (用户提供 / 已核验 / 未核验), and write "未查到" instead of completing authors, year, journal, or pages. If the user has no references yet, say so in the output and give a method framework without literature claims. If that file is not available, still apply these rules.

Read `references/output-contract.md`. Final deliverables end with `## 待核实清单` and `## 给作者的问题`; draft sections use `## 段落草稿（需作者改写并核对来源）` in the position specified by the stage or review workflow. Intermediate interview turns are exempt. In no-question mode, retain the author-question heading with "无（按要求不追加提问）".

## Recommended Sequence

If the user is starting from scratch, use the skills in this order:

```text
refine-literature-question -> decompose-review-modules -> compare-research-methods -> map-literature-contradictions -> locate-review-research-gap
```

Do not treat this workflow as ghostwriting. The skills should help the researcher clarify questions, organize evidence, and test logic. They should not fabricate sources, invent findings, or replace the researcher's academic judgment. Generated paragraphs are drafts for the author to rewrite and check against sources.
