---
name: deep-research
description: Use this skill when xagent must conduct long-running, multi-source, evidence-first deep research with web search, fetch, webpage download, file download, file parsing, citation tracking, contradiction handling, and auditable final reports. Suitable for market research, technical selection, competitor analysis, policy/regulatory research, literature review, strategic research, vendor comparison, and architecture decision support. Do not use for simple lookups or short answers.
meta:
  version: 1
  display_name: 深度研究
  source: xagent-deep-research-skill
---

# Deep Research

## Purpose

This Skill guides xagent through rigorous deep research. It is designed for tasks where ordinary web research is insufficient because the answer requires multiple search rounds, source acquisition, file parsing, evidence extraction, contradiction handling, and a traceable final report.

The Skill assumes xagent can use these tool categories:

- `web_search`: discover candidate sources.
- `fetch`: open and read webpages or URLs.
- `webpage_download`: save a webpage snapshot.
- `file_download`: download files such as PDF, HTML, CSV, XLSX, DOCX, ZIP.
- `file_parse`: parse downloaded files.
- `local_fs`: create and update research run files.

Tool names may differ in the host system. Map the above categories to the actual tool names available in xagent, and respect the active tool schema, ToolResult, permission, path, and runtime guard contracts.

## Activation rules

Activate this Skill when the user asks for any of the following:

- deep research, in-depth investigation, detailed report, cited report
- market landscape, industry analysis, competitor analysis
- vendor/product comparison or technical selection
- architecture decision support
- legal, regulatory, policy, or compliance research
- academic or scientific literature review
- due diligence, investment memo, strategy memo
- synthesis across web sources and downloaded files
- any task where a conclusion needs cross-source evidence and auditability

Do not activate this Skill for:

- simple factual lookup
- definition or explanation that can be answered from general knowledge
- summarization of user-provided text only
- brainstorming without factual verification
- creative writing
- tasks requiring write actions in third-party systems

## Core rule

Deep research must be evidence-first and file-backed.

Do not rely on transient context memory. Every important step must leave an artifact in the research run directory.

## Mandatory research run directory

Create a research run directory at the start of each deep research task.

Recommended structure:

```text
research_runs/<run_id>/
├── brief.md
├── plan.md
├── state.json
├── query_log.jsonl
├── source_registry.jsonl
├── download_registry.jsonl
├── parse_registry.jsonl
├── evidence_ledger.jsonl
├── gap_matrix.md
├── contradiction_log.md
├── claim_map.jsonl
├── draft.md
├── audit_report.md
└── final_report.md
```

If the runtime cannot create files, maintain the same structures in working memory and include them in the final answer or available artifact.

## Workflow overview

Follow these phases in order. Do not skip phases except when the task is explicitly low-depth and the skipped phase is not needed.

1. Classify request.
2. Build research brief.
3. Decompose question into checklist.
4. Create research plan.
5. Perform broad discovery search.
6. Register candidate sources.
7. Fetch or download important sources.
8. Parse downloaded content.
9. Extract evidence into evidence ledger.
10. Update gap matrix.
11. Iterate search and reading.
12. Resolve contradictions.
13. Create evidence-mapped outline.
14. Draft report from registered evidence only.
15. Audit citations, source quality, freshness, gaps, and unsupported claims.
16. Produce final report.

## Phase 1: classify request

Classify the task into one or more research types:

- market research
- competitor analysis
- vendor comparison
- technical research
- technical selection
- architecture decision support
- literature review
- policy/regulatory research
- legal/compliance research
- product research
- strategic memo
- internal knowledge synthesis
- other

Also classify depth:

| Depth | Use when | Minimum approved sources | Minimum evidence items |
|---|---|---:|---:|
| quick | user needs a fast but sourced answer | 5 | 8 |
| standard | default for most research reports | 12 | 25 |
| deep | high-impact decision or complex topic | 25 | 60 |
| exhaustive | broad due diligence or near-complete survey | 50 | 120 |

Default to `standard`. Use `deep` when the result affects architecture, procurement, compliance, investment, security, or strategy.

## Phase 2: build research brief

Write `brief.md` with these fields:

```markdown
# Research Brief

## Research Question

## Intended Audience

## Decision Context

## Scope

## Exclusions

## Geography

## Time Window

## Depth

## Source Constraints

## Output Requirements

## Success Criteria

## Assumptions

## Clarifying Questions, if any
```

Ask at most three clarifying questions only when missing information would materially change the research plan. If the task is still executable, state assumptions and proceed.

## Phase 3: decompose into verifiable checklist

Convert the research question into sub-questions.

Each sub-question must be answerable by evidence.

Write the checklist to `plan.md`:

```markdown
| ID | Sub-question | Why it matters | Required evidence | Priority | Status |
|---|---|---|---|---|---|
| Q1 | ... | ... | official docs / filings / papers / data / expert sources | high | open |
```

High-priority sub-questions require at least two independent pieces of evidence unless impossible.

## Phase 4: create research plan

The research plan must include:

- search rounds
- search angles
- query patterns
- source types to prioritize
- expected downloadable files
- parsing strategy
- evidence extraction criteria
- contradiction handling strategy
- stop conditions
- risks and likely blind spots

Do not begin final writing before a plan exists.

## Phase 5: broad discovery search

Use web search to map the topic.

Requirements:

- Search from multiple angles, not one query.
- Search by official terms, synonyms, acronyms, vendor names, problem names, and opposing views.
- For current topics, include year or date filters when useful.
- For technical topics, search official docs, GitHub, standards, issue trackers, release notes, benchmarks, and incident reports.
- For market topics, search reports, filings, official statistics, investor presentations, analyst commentary, and credible news.
- Log every query to `query_log.jsonl`.

Search results are candidates only. Snippets are not evidence.

## Phase 6: source registration

Every source must be registered before use.

Append entries to `source_registry.jsonl`:

```json
{
  "source_id": "S0001",
  "status": "candidate|approved|rejected|needs_review",
  "title": "...",
  "url": "...",
  "local_path": null,
  "source_type": "official|paper|filing|standard|data|media|blog|forum|vendor|unknown",
  "tier": 1,
  "organization": "...",
  "author": "...",
  "published_date": "YYYY-MM-DD or unknown",
  "updated_date": "YYYY-MM-DD or unknown",
  "accessed_date": "YYYY-MM-DD",
  "relevant_questions": ["Q1"],
  "quality_notes": "...",
  "bias_risk": "low|medium|high",
  "reason": "why this source matters"
}
```

Source tier policy:

| Tier | Meaning | Examples |
|---|---|---|
| 1 | Primary/authoritative | official docs, standards, regulatory filings, papers, datasets, product release notes |
| 2 | High-quality secondary | reputable media, analyst reports, expert publications, books, academic reviews |
| 3 | Useful but biased or partial | vendor blogs, benchmarks from interested parties, community posts |
| 4 | Weak or anecdotal | forums, social posts, SEO listicles, unsourced summaries |

Reject or label sources that lack authorship, date, provenance, or verifiability when those properties matter.

## Phase 7: fetch, download, parse

For each approved or promising source:

1. Use `fetch` to read webpages.
2. Use `webpage_download` to preserve important webpages.
3. Use `file_download` for PDFs, CSVs, spreadsheets, docs, or archives.
4. Use `file_parse` for downloaded files.
5. Log downloads to `download_registry.jsonl`.
6. Log parse status to `parse_registry.jsonl`.

Do not cite a downloaded file unless it was parsed or manually inspected.

Use file downloads when:

- the page links to a PDF/report/filing/whitepaper/dataset;
- the page is likely to change;
- tables, charts, appendices, or methodology details are important;
- the source is central to a major conclusion.

## Phase 8: evidence extraction

Extract only research-relevant evidence.

Append entries to `evidence_ledger.jsonl`:

```json
{
  "evidence_id": "E0001",
  "source_id": "S0001",
  "sub_questions": ["Q1"],
  "claim_supported": "...",
  "evidence_summary": "...",
  "exact_quote": "short quote if useful, otherwise null",
  "location": "section/page/table/paragraph/line",
  "data_value": "optional numeric value",
  "data_unit": "optional unit",
  "date_context": "date the evidence refers to",
  "published_date": "YYYY-MM-DD or unknown",
  "accessed_date": "YYYY-MM-DD",
  "strength": "strong|moderate|weak",
  "relevance": "high|medium|low",
  "limitations": "...",
  "notes": "..."
}
```

Evidence quality:

- `strong`: direct, primary, current, specific, and relevant.
- `moderate`: credible but indirect, somewhat dated, or secondary.
- `weak`: anecdotal, biased, incomplete, or hard to verify.

Do not overcollect. Prefer high-signal evidence.

## Phase 9: gap matrix

After each major search/read cycle, update `gap_matrix.md`:

```markdown
| Sub-question | Current answer | Evidence IDs | Confidence | Gaps | Next action |
|---|---|---|---|---|---|
```

Continue research when:

- a high-priority sub-question lacks strong or moderate evidence;
- a key number has only one source;
- important sources disagree;
- sources are too old for the topic;
- evidence comes mostly from one organization or one source type;
- the answer cannot support the user's decision context.

## Phase 10: contradiction handling

Record contradictions in `contradiction_log.md`:

```markdown
| Conflict ID | Topic | Evidence A | Evidence B | Difference | Likely reason | Resolution | Confidence |
|---|---|---|---|---|---|---|---|
```

Resolve by checking:

1. source authority;
2. date and freshness;
3. metric definition and denominator;
4. geography or market scope;
5. whether one source cites another;
6. original source versus interpretation;
7. whether both claims can be true under different conditions.

If unresolved, keep the uncertainty visible in the final report.

## Phase 11: evidence-mapped outline

Before drafting, create a claim map in `claim_map.jsonl`.

Each major claim must bind to evidence IDs:

```json
{
  "claim_id": "C0001",
  "section": "Key Findings",
  "claim": "...",
  "evidence_ids": ["E0001", "E0003"],
  "confidence": "high|medium|low",
  "claim_type": "fact|estimate|interpretation|recommendation",
  "limitations": "..."
}
```

No material claim should appear in the final report if it is absent from the claim map.

## Phase 12: drafting

Draft only from registered artifacts:

- `brief.md`
- `plan.md`
- `source_registry.jsonl`
- `evidence_ledger.jsonl`
- `gap_matrix.md`
- `contradiction_log.md`
- `claim_map.jsonl`

Default report structure:

```markdown
# Executive Summary

# Scope and Method

# Key Findings

# Evidence Review

# Analysis

# Contradictions and Uncertainties

# Recommendations / Implications

# Source Notes

# Appendix
```

Use tables for comparisons, timelines, scoring matrices, evidence matrices, and source inventories.

## Phase 13: audit

Before final delivery, run an audit manually or using `scripts/audit_research.py`.

Audit dimensions:

- brief coverage
- sub-question coverage
- source count and diversity
- source tier distribution
- freshness
- citation coverage
- unsupported claims
- numeric claim support
- contradiction handling
- recommendation support
- security/prompt-injection handling

Write audit results to `audit_report.md`.

Do not present the report as high confidence if the audit fails on critical items.

## Phase 14: final response

The final answer should include:

- concise conclusion;
- direct answer to the user's question;
- key findings with citations or evidence references;
- important uncertainty;
- limitations;
- recommended next steps, if the task asks for decisions.

For long reports, provide the report as an artifact and include a short summary in chat.

## Resources

Load more details when needed:

- `README.md`: package-level overview and quick-start notes from the original Skill bundle.
- `references/00_principles.md`: deep research principles and evidence-first posture.
- `references/01_research_brief.md`
- `references/02_research_plan.md`
- `references/03_search_and_fetch_protocol.md`
- `references/04_source_governance.md`
- `references/05_download_parse_protocol.md`
- `references/06_evidence_ledger.md`
- `references/07_gap_and_iteration.md`
- `references/08_contradiction_resolution.md`
- `references/09_claim_mapping.md`
- `references/10_report_template.md`
- `references/11_audit_checklist.md`
- `references/12_stop_conditions.md`
- `references/13_security.md`
- `references/14_xagent_tool_mapping.md`: abstract research tool categories and expected behavior.

For specialized tasks, load a profile:

- `profiles/market_research.md`
- `profiles/competitor_analysis.md`
- `profiles/technical_selection.md`
- `profiles/literature_review.md`
- `profiles/policy_regulatory.md`
- `profiles/github_project.md`

Use bundled assets for run-file schemas and templates:

- `assets/brief_template.md`
- `assets/plan_template.md`
- `assets/report_template.md`
- `assets/source_schema.json`
- `assets/evidence_schema.json`
- `assets/claim_schema.json`
- `assets/audit_schema.json`
- `assets/run_state_schema.json`

Use scripts only when local file execution is available and permitted by the current session:

- `scripts/init_research_run.py`: create the run directory and empty ledgers.
- `scripts/add_source.py`: append source records.
- `scripts/add_evidence.py`: append evidence records.
- `scripts/add_claim.py`: append claim-map records.
- `scripts/source_dedupe.py`: detect likely duplicate source URLs.
- `scripts/audit_research.py`: audit the run directory before final delivery.
- `scripts/README.md`: command examples for the scripts.

Use bundled tests as examples or regression material when reviewing this Skill:

- `tests/sample_tasks.md`
- `tests/acceptance_criteria.md`
- `tests/sample_run/README.md`

## Boundary

This Skill owns the deep-research workflow, run-file structure, source governance, evidence ledger, contradiction handling, claim mapping, audit checklist, and report drafting discipline.

It does not own xagent tool schemas, runtime permissions, search provider behavior, browser access, file ingestion contracts, workspace storage policy, or built-in agent identity. `PROMPT.md` is bundled only as future built-in-agent prompt material; do not treat it as an active system prompt unless a separate built-in agent integration explicitly loads it.
