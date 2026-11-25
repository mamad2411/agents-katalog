---
name: deep-research
description: Execute deep research through the local SOUL.md contract with structured artifacts, hybrid search, the local Tavily adapter, claim verification, and a quality gate.
---

# Deep Research Skill (Subagent Workspace)

This copy exists inside the research workspace so the subagent sees the same contract from its own sandbox.

## Execution Summary

1. Initialize `tmp/` artifacts with `python scripts/init_research_run.py --topic "<goal-summary>" --language "<language>" --task-date "<YYYY-MM-DD>" --workspace "."` at the start of every new task, even if old files already exist in `tmp/`. This step must succeed before any search begins. Then read `tmp/research_plan.json` and treat `report_target` as the only valid destination for the report.
2. Follow the 5-stage pipeline from `SOUL.md`: `plan -> scout -> harvest -> verify -> synthesize`.
3. In scout, use the local Tavily adapter as the default path:
   `python scripts/tavily.py "<query>" --query-family baseline --append-query-log tmp/query_log.json --append-source-registry tmp/source_registry.json --output tmp/tavily_last.json`
4. Keep raw `web_search` bounded: normally no more than 2 broad or recency `web_search` calls before the first harvest pass. After that, prefer Tavily plus targeted `web_fetch`.
5. After each broad `web_search`, materialize the top 1-2 novel external URLs into artifacts with `python scripts/materialize_query_results.py --provider web_search --query "<query>" --query-family <family> --urls <url1> <url2> --append-query-log tmp/query_log.json --append-source-registry tmp/source_registry.json`.
5. Run a mini-harvest pass for shortlist models and shortlist claims before synthesis; snippets alone are not enough for final findings.
6. Run `python scripts/expand_research_coverage.py --workspace "<workspace-root>"` after the first verify pass. If it reports `needed=true`, execute only the suggested follow-up queries, harvest up to 2 new sources per unresolved core question, and run it once more.
7. Build evidence in JSON artifacts first, then run `python scripts/normalize_research_artifacts.py --workspace "<workspace-root>"`.
7. Keep machine-readable JSON artifacts ASCII-safe where practical; prefer English strings in artifacts even when the final report is in Russian.
8. Lint the report with `python scripts/report_lint.py --report "<absolute-report-path>" --workspace "<workspace-root>"`.
9. Validate the report with `python scripts/validate_research_report.py --report "<absolute-report-path>"`.
10. Finalize the M2M JSON with `python scripts/finalize_research_run.py --report "<absolute-report-path>"` and return that JSON verbatim.

## Non-Negotiables

- Search tools are discovery tools, not evidence by themselves.
- Do not manually inspect environment secrets during research; rely on the local Tavily adapter to resolve `TAVILY_API_KEY`.
- Do not reuse stale `tmp/` state across tasks; the current run must be anchored by a freshly initialized `tmp/research_plan.json` whose topic and task date match the current request.
- On a fresh run, do not open old files in `reports/` to continue from them. Only use `tmp/research_plan.json.report_target` unless the task explicitly says to resume a previous run.
- `web_fetch` or equivalent full-page retrieval is required for high-value sources.
- If `web_fetch` on Reddit, YouTube, LinkedIn, forums, or other low-value community pages returns a wall of CSS, a login wall, or unusable boilerplate, stop retrying that page and keep it only as discovery context.
- Every high-impact claim must have fetched supporting evidence before it can stay `verified`.
- Use inline Markdown links in findings and a numbered bibliography at the end.
- Each finding bullet, paragraph, or table row must contain at least one inline Markdown link to a supporting external source.
- Only real external `http/https` URLs from `source_registry.json` may be cited; never use local files like `tmp/tavily_last.json` or other workspace artifacts as evidence.
- Treat `source_count` as a soft breadth signal, not the success criterion.
- Preserve breadth honestly: keep discovery-only external URLs in `source_registry.json` when they are novel, canonical, and useful for breadth accounting, even if they remain `fetched=false`.
- Materialize `web_search` breadth the same way as Tavily breadth; otherwise `source_count` and coverage breadth will stay artificially low.
- Anchor the report to the task date and mention it explicitly in the report body.
- Do not return `SUCCESS` if required artifacts are missing, stale, not materialized on disk, or either `report_lint.py` or the validator fails.
- Do not handcraft the final M2M JSON; return the finalizer output verbatim.
- Do not create ad hoc mutation scripts inside `tmp/`; use the checked-in scripts under `scripts/` and update artifact JSON directly.
- High-impact claims require two independent supporting sources whenever possible.
- Machine-readable JSON artifacts should stay English and ASCII-safe; keep Russian for the user-facing report only.



