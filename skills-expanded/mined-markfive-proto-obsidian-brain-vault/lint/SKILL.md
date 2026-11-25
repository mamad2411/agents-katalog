---
name: lint
description: "Health-check a markdown knowledge base. Find broken links, orphan notes, missing frontmatter, inconsistent facts, duplicate concepts, and suggest new articles to fill gaps. Use when the user says 'lint my wiki', 'check my KB health', 'find inconsistencies', 'what should I write next'. Part of the knowledge-base pack."
license: MIT
metadata:
  author: markfive-proto
  version: "0.1.0"
  pack: knowledge-base
---

# Lint Pack — "Keep my KB clean and complete"

`lint` is the **maintenance layer**. A growing wiki rots silently. This skill surfaces rot, impute-able gaps, and high-value next writes.

## Output convention

Lint always writes a report to `outputs/lint/<YYYY-MM-DD>-<run-type>.md`. Never replies in chat only.

## Commands

### /lint — Full health check

When the user invokes `/lint`:

1. Run all the sub-checks below in parallel, merge findings.
2. Write a single report at `outputs/lint/<date>-full.md`.
3. Summarize chat-side: totals per severity (error / warn / info) and link to the report.

### Sub-checks (each is also runnable individually)

#### /lint-links — Broken links

- For every `[[wikilink]]` in the vault, check the target file exists.
- For every markdown `[text](relative-path)` link, check the path resolves.
- For every external URL, optionally HEAD-request and flag 404s (off by default; opt-in via `--check-urls`).
- Report: file, line number, bad target, suggested fix (closest existing filename via fuzzy match).

#### /lint-orphans — Disconnected notes

- A note is an **orphan** if: 0 incoming wikilinks AND 0 outgoing wikilinks AND not in a designated "inbox" folder.
- Report each orphan with its first 200 chars of content.
- Suggest: delete / link to existing concept / promote to concept page.

#### /lint-frontmatter — Missing or invalid metadata

- Every file under `compiled/` should have frontmatter with at least: `title`, `type`, `tags`, `last_updated`.
- Every file under `raw/` should have: `source_type`, `source_url` (if applicable), `tags`.
- Report missing fields with suggested values (infer from content/filename).

#### /lint-duplicates — Concept dedupe

- Group `compiled/concepts/*.md` by stemmed title.
- Flag pairs/triples that are likely duplicates (e.g., `transformer.md` and `transformers.md`, `self-attention.md` and `scaled-dot-product-attention.md`).
- Suggest canonical name and merge plan (do NOT merge automatically).

#### /lint-inconsistencies — Conflicting facts

- Build a fact map: for each concept, extract atomic factual claims (dates, numbers, named-entity relationships).
- Cross-check claims across sources.
- Flag contradictions. Example: "Raw A says founded 2017; raw B says founded 2018."
- Suggest resolution: which source is more authoritative, or mark as disputed.

#### /lint-gaps — New-article candidates

Use two signals:
1. **High-degree stubs:** any concept page with `sources_count >= 3` but TL;DR < 100 words → under-written, needs deeper synthesis.
2. **Dangling wikilinks:** `[[concept-that-doesnt-exist-yet]]` referenced from 2+ notes → candidate for a new concept page.
3. **Question accumulation:** count entries in every `## Open questions` section across the vault; top 10 by count are prime research targets.

Output a prioritized "Next to write" list.

#### /lint-impute — Fill missing data with web search

For any concept page with frontmatter `last_updated` older than 90 days AND TL;DR shorter than 150 words:
1. Extract 1-2 specific sub-questions that would strengthen the page.
2. Web-search for authoritative sources.
3. Propose ingests to the user (do not auto-ingest).
4. Report as: "Concept X is stale — consider `/ingest <url-suggestion>` to refresh."

#### /lint-tag-drift — Tag hygiene

- Find tags used only once or twice (probably typos or singletons).
- Find near-duplicate tags (`#ml-ops` vs `#mlops`).
- Suggest canonicalization.

#### /lint-connections — Suggest new links

- For each pair of concept pages sharing 2+ tags AND 3+ raw sources in common, check whether they already link to each other.
- If not, propose mutual wikilinks with a 1-line reason.

## Severity model

| Level | Meaning | Example |
|---|---|---|
| error | Broken state; user action required | Broken wikilink target |
| warn | Degraded quality | Missing frontmatter field |
| info | Suggestion / improvement | Tag drift, link opportunity |

Report counts per severity at the top of the lint output.

## Report template

```markdown
---
title: Lint Report — <YYYY-MM-DD>
type: lint-report
run: full
tags: [output, lint]
---

# Lint Report — <date>

## Summary
- Errors: <N>
- Warnings: <N>
- Info: <N>
- Notes scanned: <N>

## Errors

### Broken links (<N>)
- `[[missing-concept]]` in [[file]] line <N> → suggest [[closest-existing]]

### Other errors
...

## Warnings
...

## Info / suggestions
...

## Next-to-write (prioritized)
1. <concept-name> — reason: 5 dangling links, 3 open questions
2. ...
```

## Auto-fix mode (opt-in)

When the user passes `/lint --fix` or says "fix the safe stuff":

- Safe auto-fixes only:
  - Add missing `last_updated` from file mtime.
  - Canonicalize near-duplicate tags with the canonical form.
  - Remove trailing whitespace.
- Unsafe (NEVER auto-fix):
  - Merging concept pages.
  - Rewriting content.
  - Deleting orphans.

Report every auto-fix applied with file + diff.

## Scheduling

Recommend to the user: run `/lint` after every 10+ ingests, or weekly. Can be automated via `cron` or `schedule` skill.

## Related skills (same pack)

- `[[ingest]]` — upstream; lint suggests new ingests
- `[[compile]]` — lint flags things compile missed
- `[[qa]]` — outputs of qa are NOT linted as content (only format)
- `[[render]]` — lint reports can be rendered as dashboards

## Attribution

Pack inspired by Karpathy's "LLM health checks over the wiki" practice — surfacing inconsistencies, imputing gaps, suggesting next writes.
