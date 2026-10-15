---
name: yao-expert-skill
description: Create expert-level learning reports and tutorials from any domain, industry, technology, role, market, product idea, or vague field question. Use when the user wants to quickly build domain expertise, understand an industry, generate a structured expert study report, build a keyword library, design Feynman self-tests, or export the result as Markdown, DOCX, PDF, and HTML. Do not use for short factual answers, pure business model diagnosis, standalone beginner tutorials with no domain-structure research, simple file conversion, or unsourced opinion writing.
metadata:
  author: Yao Team
  maturity_tier: production
  artifact_family: expert-learning-report
---

# Yao Expert Skill

Turn a domain, industry, technology, role, product direction, or fuzzy idea into an expert learning packet: one structured report, one tutorial path, a keyword system, Feynman tests, and four polished export formats.

## Own The Following Job

- Normalize the user's topic into domain, region, purpose, audience, time horizon, output depth, and exclusions.
- Build domain expertise from structure first: boundary, classifications, value chain, actors, demand, supply, competition, lifecycle, policy, technology, capital, risks, and change variables.
- Use authority-first research and separate `fact`, `inference`, `hypothesis`, and `unknown`.
- Generate `50-100` keyword teaching cards. Each keyword must include a plain-language one-liner, concept explanation, bottom logic, real example, practical application, role/effect, related people/companies/institutions when relevant, common misconception, and evidence.
- Explain difficult concepts and underlying logic with simple analogies plus real domain examples, so a newcomer can understand how the field works rather than only memorize terms.
- Begin every report with a reader-facing `导读摘要` that introduces the learning material, highlights, reading path, and structural logic before the formal report sections.
- Write each major module with a natural introductory paragraph and transitions before tables, so the report reads as coherent learning material instead of a hard glossary or matrix dump.
- Generate `10` Feynman questions with reference answers and a scoring rubric.
- Produce Markdown, Word, PDF, and HTML artifacts, with layout checks for tables, borders, overflow, anchors, fixed left-side navigation, and local-path leakage.

## Inputs

Expect one or more of:

- a domain, industry, technology, market, role, company direction, or vague idea
- geography, language, audience, use case, time horizon, and desired depth
- existing notes, links, papers, reports, screenshots, or source constraints
- requested output formats, naming, style, deadline, and privacy constraints

When the user gives only a topic, do not stall. Use the defaults in `references/domain-expert-method.md`, state the assumptions, and continue unless a missing input would materially change the package.

## Do Not Route Here

- one-off factual answers or quick explanations
- generic web research that does not produce an expert learning packet
- pure business model work; use a business model skill instead
- beginner tutorial creation with no industry/domain structure; use a tutorial skill instead
- finished-file conversion with no report or tutorial design
- legal, medical, financial, or safety advice as a final recommendation; keep those as educational research with source and uncertainty notes

## Default Workflow

1. Read `references/domain-expert-method.md`; capture assumptions and the expert-learning brief.
2. Read `references/research-and-source-quality.md`; build a source plan and verify current facts when the domain is time-sensitive.
3. Draft the canonical report in Markdown using `templates/expert-report-template.md`.
4. Add the tutorial path, keyword teaching cards, concept map, representative people/company/case map, Feynman tests, evidence register, and uncertainty log.
5. Read `references/report-and-tutorial-contract.md`; check section coverage, evidence labels, and learning sufficiency.
6. Read `references/export-and-layout-quality.md`; run `scripts/export_expert_report.py` for Markdown, DOCX, PDF, and HTML.
7. Run `scripts/validate_artifacts.py` and fix layout, table, anchor, overflow, citation, and local-path issues before delivery.

## Output Contract

The normal output set is:

- `{basename}.md`: canonical expert learning report and tutorial packet
- `{basename}.docx`: Word document export with readable tables and restrained report styling
- `{basename}.pdf`: PDF export checked for page layout and table overflow risk
- `{basename}.html`: standalone HTML report with a fixed left-side numbered navigation menu and section anchors
- a short delivery note with assumptions, source coverage, uncertainty, validation result, and next learning steps

## Quality Gates

- The topic boundary includes wide, narrow, exclusion, and data/source scope.
- The report begins with `导读摘要`, including introduction, highlights, reading path, and logic overview; Markdown, DOCX, PDF, and HTML exports must all preserve this opening summary.
- Every major module has a reader-facing introduction before dense tables or matrices.
- Key claims are backed by source tier, date, and confidence.
- Every major judgment is labeled as fact, inference, hypothesis, or unknown.
- Keyword teaching cards cover demand, product, technology, value chain, business model, competition, policy, finance, operations, risks, and trends.
- Every keyword teaching card explains: what it means, how to understand it in one sentence, why it exists, how it works, where it appears in the real domain, how to apply it, what role it plays, which people/companies/institutions are associated with it when relevant, and what beginners often misunderstand.
- Representative people, companies, institutions, products, and cases are included as learning anchors, with role labels and source notes rather than unsupported rankings.
- The tutorial can take a beginner from orientation to self-check, not just list terms.
- HTML contains a fixed left-side navigation tree with ordered indices, compact four-character Chinese anchor labels, transparent background, and no standalone sidebar panel styling.
- PDF exports remove the HTML navigation node before printing and hide browser print chrome; no navigation labels, `file://` paths, dates, or browser page footers should appear.
- DOCX/PDF/HTML exports exist and pass `scripts/validate_artifacts.py`, or remaining failures are named precisely.

## Reference Map

- `references/domain-expert-method.md`
- `references/research-and-source-quality.md`
- `references/report-and-tutorial-contract.md`
- `references/export-and-layout-quality.md`
- `templates/expert-report-template.md`
- `templates/expert-report.css`
- `templates/report-html-shell.html`
- `scripts/export_expert_report.py`
- `scripts/validate_artifacts.py`
- `evals/trigger_cases.json`
