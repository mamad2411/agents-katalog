---
name: research-synthesis
description: Use when the task requires synthesizing multiple sources, search results, documents, notes, papers, reports, competitor material, internal artifacts, or conflicting evidence into a cited answer, evidence table, research brief, literature-style summary, market landscape, or recommendation. Prefer this Skill when source authority, freshness, deduplication, confidence, gaps, or iterative research checkpoints matter. Do not use for simple single-source summary or casual writing.
meta:
  version: 6
  display_name: 研究综合
  source: w95/awesome-claude-corporate-skills knowledge-synthesis; Anjos2/recursive-research; jezweb/claude-skills deep-research
  license: MIT
---

# Research Synthesis

## Purpose

Synthesize evidence from multiple sources into a clear, traceable answer. The result should show what is known, what conflicts, how strong the evidence is, and what still needs verification.

This Skill is for research judgment, not just summarization. It is useful when the user needs to compare sources, reconcile conflicting claims, produce a report, or decide what evidence supports a conclusion.

## Use When

Use for:

- Multi-source research answers.
- Claim verification, source validation, and evidence-backed comparisons.
- Current-state checks where freshness, exact dates, or primary sources matter.
- Market, competitor, industry, or policy landscape synthesis.
- Literature-style summaries and source comparison.
- Evidence-backed recommendations.
- Internal document, note, ticket, or artifact synthesis.
- Conflicting source reconciliation.
- Research briefs with citations, evidence tables, confidence, and gaps.
- Iterative research where each cycle should produce a checkpoint before expanding scope.

## Do Not Use When

Do not use for:

- Simple fact lookup.
- Single-document summary with no cross-source judgment.
- Writing that does not require evidence handling.
- Provided-document understanding where external/source comparison is not central; use `document-understanding`.
- Data analysis that requires computation over structured data; use `data-visual-report-builder`.
- Formal Chinese official documents; use `official-document-drafting`.
- Solution option framing where the answer is mainly a proposed approach; use `solution-brief`.
- Inventing citations, sources, metrics, or conclusions from missing evidence.

## Material Gate

Before synthesizing, identify:

- Research question, decision, audience, and expected output.
- Source scope: web, provided files, workspace artifacts, internal notes, links, or mixed.
- Required freshness: current status, historical background, evergreen method, or time-bounded comparison.
- Required depth: quick answer, evidence brief, full report, literature review, or recursive investigation.
- Preferred and excluded source types.
- Required citation style, if any.
- Whether the user expects recommendations or only neutral synthesis.

If the question, source scope, or freshness requirement is ambiguous and the answer would be materially different, ask one focused question. Otherwise state assumptions and proceed.

If the task requires unknown-source discovery, current facts, market/industry landscape, concrete cases, competitor examples, or source-backed recommendations, verify that a search/source-discovery capability is available before planning. `http_request` and `web_fetch` only retrieve known URLs; they do not discover sources from a query. If no search/source-discovery tool is visible, use `tools_find` when available, ask the user for source material, or report an evidence blocker. Do not synthesize a source-backed answer from model memory alone.
If the task also needs domain judgment, such as market landscape, business model, investment, legal, technical, or workflow analysis, use `skills_find` / `skills_load` for the relevant domain Skill when available. This Skill owns evidence synthesis; domain Skills own domain-specific interpretation.
If the task needs a final user-facing report, use `skills_find` / `skills_load` for `html-report-builder` or an equivalent visual report Skill when available. This Skill should provide the evidence ledger, confidence model, caveats, and synthesized findings for that final report.

## Workflow

1. Restate the research question and scope in one line.
2. Before planning, split required Skills by capability dimension:
   - source discovery or retrieval tools;
   - domain interpretation Skill;
   - evidence synthesis Skill;
   - final report or visual packaging Skill.
3. Use focused `skills_find` passes for missing domain or deliverable Skills instead of one broad find.
4. Build a source plan using `references/synthesis-rules.md`: source tiers, freshness need, exclusion rules, and minimum corroboration.
5. Gather or inspect only sources available through the current XAgent session, provided materials, or user-approved tools. For unknown-source discovery, first use a real search/discovery tool; for known links, use retrieval tools such as explicit URL fetchers.
6. Keep a source log: source title, origin, date, author or owner when known, type, tier, inspected portion, and relevance.
7. Deduplicate near-identical material before counting evidence strength. Prefer the most complete, authoritative, and recent version.
8. Extract claims as evidence units, not as whole-source summaries.
9. Group evidence by theme, question, option, actor, timeline, or decision criterion.
10. Mark confidence for each major conclusion based on source authority, freshness, independence, agreement, and directness.
11. Surface conflicts instead of averaging them away. Explain which source is stronger and why, or mark unresolved.
12. For broad research, run progressive passes: focused answer, wider landscape, then deeper validation only when the task needs it.
13. Stop expanding when new sources repeat existing evidence or no longer change the answer.
14. If the expected output is a report-like deliverable, separate research work from final presentation:
   - this Skill owns source planning, evidence extraction, synthesis, conflicts, confidence, gaps, and recommendations;
   - use a visual report Skill such as `html-report-builder` for the final user-facing report when available;
   - keep Markdown only for source logs, evidence ledgers, intermediate notes, or drafts unless the user explicitly requests Markdown as the final format.
15. Validate with the checks below.

For report-like deliverables, create a visible evidence ledger before final packaging. Use a compact structure such as:

```yaml
source_log:
  - ref:
    title:
    origin:
    date:
    type:
    tier:
    inspected_portion:
    relevance:
claim_evidence:
  - claim:
    status: verified | inferred | disputed | unverified
    source_refs:
    confidence:
    caveat:
unverified_items:
  - item:
    needed_to_verify:
```

This ledger is task content, not hidden reasoning. Pass it to the final report Skill or expose it in the answer.

## Checks

- Every important claim has a traceable source or is labeled as inference.
- Source authority and freshness match the question.
- Duplicates are not counted as independent confirmation.
- Conflicts, minority views, and missing evidence are visible.
- Recommendations are separated from evidence.
- Confidence is not stronger than the evidence supports.
- Time-sensitive claims include dates or freshness limits.
- The output distinguishes facts, interpretations, assumptions, and open questions.
- No citation, quote, metric, title, or author is invented.
- Final reports expose source refs, confidence, caveats, and unverified items in a user-visible way instead of hiding them in internal notes.
- Search snippets, titles, and result summaries are discovery leads, not inspected sources. Do not cite them as evidence until the source itself is inspected.
- Run a contradiction pass before finalizing source-backed reports: check dates, names, metrics, rankings, recommendations, and cited case facts across inspected sources.
- HTML or visual reports must include visible source/evidence blocks, caveats, and unverified-item markers in the artifact, not only in chat.
- Source-backed completion requires at least one inspected source URL, provided source ref, or concrete tool/raw ref that is not merely a self-authored final artifact. If none exists, label the output as assumption-only or blocked for evidence, and do not set `no_external_evidence=false`.
- Concrete case analysis requires named cases with inspected sources, or explicit `未验证案例` / `unverified case` labels.

## Outputs

Produce one or more of:

- cited research answer
- evidence table
- source log
- conflict matrix
- confidence summary
- gap analysis
- literature-style synthesis
- market or competitor landscape synthesis
- recommendation with evidence basis
- recursive research checkpoint
- final research report

Use the user's requested format. Do not force a report template when a concise source-backed answer is enough. When a report is required and no other final format is specified, prefer a visual single-file HTML report by composing with `html-report-builder` when available.

When handing off to `html-report-builder`, provide a `report-spec` with at least:

- title, audience, language, purpose, and date/source scope;
- summary, key findings, section outline, recommended visual modules, and tables/charts only when data is available;
- `source_log`, `claim_evidence`, `caveats`, `unverified_items`, and `data_needed`;
- exact refs for inspected URLs, provided files, workspace refs, tool refs, or raw refs.

## Recovery

If evidence is weak, produce a low-confidence synthesis with explicit gaps and next verification steps. If sources conflict, preserve the conflict and explain possible reasons. If source access is unavailable, state exactly which sources were not inspected and avoid pretending completeness.

## Boundary

Skill owns research framing, source tiering, evidence extraction, deduplication, conflict handling, confidence language, checkpoints, and research-content structure.

It does not own final HTML visual packaging when `html-report-builder` is available, XAgent tool schemas, search provider behavior, browser access, MCP access, Notion integration, database storage, file ingestion, citation-manager APIs, academic database subscriptions, or final legal/medical/financial conclusions. It must not run shell, Python, Node, MCP, Gemini, Notion, browser automation, package install, database, or document-export commands by itself; those actions belong to XAgent tools visible in the current session.

## Resources

- `references/synthesis-rules.md`: source tiers, research depth, deduplication, confidence, conflict, and checkpoint rules.
- `templates/research-synthesis.md`: reusable research synthesis artifact template.
- `LICENSE`: source and license notice.
