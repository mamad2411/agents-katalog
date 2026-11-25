---
namespace: aiwg
name: research-expand
platforms: [all]
description: Find papers similar to the corpus using seed-based Semantic Scholar recommendations and a ranked candidate queue
triggers:
  - "find papers similar to the corpus"
  - "expand the research corpus"
  - "recommend papers from corpus seeds"
  - "review corpus expansion candidates"
commandHint:
  argumentHint: "[--seeds REF-0001,REF-0002 | --since YYYY-MM-DD | --all] [--max-seeds N] [--write]"
  category: research-discovery
---

# Research Expand

Find papers similar to the corpus without automatically inducting them or filing issues.

> Expand from REF-0001 and REF-0002, then list the ranked candidates with their scores. Preview accepting one candidate with an induction brief, rejecting another with a reason, and deferring a third. Save decisions only when I request it. Show the changed candidates and preserve all other entries.

To refine the result: “Use the recorded DOI alias for that candidate and show the seed REFs in its induction brief.”

## Triggers

- "find papers similar to the corpus"
- "expand the research corpus"
- "recommend papers from corpus seeds"
- "review corpus expansion candidates"

## Instructions

1. Preview with `aiwg corpus expand --all --max-seeds 20 --json`. A scope is required: choose one of `--seeds REF-0001,REF-0002`, `--since YYYY-MM-DD` or `--all`. Without one, the command exits 1 and makes no requests. `--since` uses induction/discovery dates from reference or citation-sidecar frontmatter, then the reference document’s first-add date in the corpus repository’s Git history (following renames). Untracked files, corpora outside Git, or unavailable Git history fall back to document modification time; one summary warning reports how many REFs used that fallback. Fresh-clone mtimes do not override available Git dates. Shallow clones cannot establish first-add dates beyond their history boundary: those REFs use mtime with a warning naming shallow history; use a full clone for stable `--since` scoping. Documents deleted after corpus load are skipped with a warning.
2. Seeds come from arXiv or DOI frontmatter in references and citation sidecars; both `arxiv:` and `arxiv_id:` work. An arXiv body URL is a fallback. Version suffixes and old-style IDs use the shared research identity normalization. If primary and sidecar preferred seed IDs disagree, one warning per conflicting REF reports both; the primary wins.
3. Review the preview, then run with `--write` when the user requests persistence. Only `--write` writes files. Use `--max-seeds N` to resume a large first pass. Successful seeds stay explored for `--reexplore-after 180d`; throttled or failed seeds are retried next run. An immediate repeat of a completed run makes no API calls. Writes compact the frontier ledger to the latest row per REF, preserving every seed’s status, including seeds outside the current scope.
4. Recommendations use Semantic Scholar's paced, retrying client and `S2_API_KEY` when set. Defaults: `--per-seed 20`, `--from recent` (alternative: `all-cs`), `--min-year 2018`. `--overlap` optionally adds one graph lookup per top-20 candidate, with normal transport retries; it is off by default and cached in the queue.
5. Resolve the payload destination with `aiwg artifacts path --json --check-write`. Under its `artifact_root`, read `research/discovery/expansion-state.jsonl`, `candidates.jsonl`, `expansion-report.md`, and `rejected-candidates.jsonl`. An unavailable external root is an error; never substitute a local payload directory.
6. Rank candidates by distinct seed convergence, publication year, then optional in-corpus reference overlap. Queue rows include `paper`, `identity_keys`, `seed_refs`, `score_parts` and `discovery`. Dedup uses arXiv, DOI, S2 ID and normalized title against corpus, queue and rejected list. List saved candidates with `aiwg corpus review list --json` (or omit `list`); text output includes score components too. This makes no HTTP requests.
7. Preview `aiwg corpus review accept <id>`, `reject <id> --reason "Outside scope"`, or `defer <id>`. IDs are `paper.id`, full recorded identity keys (for example `doi:10.1234/example`), bare S2 identifiers, or complete recognized DOI/arXiv/OpenReview/ACL/S2 alias forms and URLs. Arbitrary bare key suffixes and text containing an alias are not IDs. Unknown or ambiguous IDs exit 1 without writes. Add `--write` to persist: accept/defer retain only the selected entry with `review.status` (`accepted`/`deferred`) and `review.reviewed_on`; reject records it with its aliases and optional reason in the existing rejected list, then removes it from the queue. Other entries are unchanged. Reviews survive re-expansion; rejected identities remain suppressed on fresh expansion. Older flat rejected-list objects remain supported. Write ordering is crash-consistent: rejection suppression is saved before the queue, report, and ledger compaction. If a later write fails, a subsequent `expand --all --write` reconciles the queue and compacts the ledger without restoring rejected identities.
8. Request `aiwg corpus review accept <id> --brief` to emit an induction brief on stdout (JSON field `brief` with `--json`), including title, IDs, seed REFs, score components and discovery provenance. This is a dry run unless `--write` is supplied; `--brief` does not write a brief file. Without `--brief`, accept produces no induction brief.
9. Present the report and let the user select papers for `induct-research`. Never auto-induct and never auto-file intake issues. On an explicitly requested induction, preserve the queued provenance in the new citation sidecar with `aiwg corpus discovery-log --ref REF-XXXX --surface s2-recommendation --via "S2 recommendations for REF-0001, REF-0002" --write`.

## Examples

```bash
aiwg corpus expand --all --max-seeds 100 --write --json
aiwg corpus expand --seeds REF-0001,REF-0002 --from all-cs --per-seed 30
aiwg corpus expand --since 2026-10-01 --reexplore-after 180d --overlap
aiwg corpus review list --json
aiwg corpus review accept doi:10.1234/example --brief
aiwg corpus review reject <paper-id> --reason "Outside scope" --write
aiwg corpus review defer <paper-id> --write
```

Exit codes: 0 complete, 3 incomplete with retryable failures, 1 usage/storage error. JSON results remain available on exit 3. A capped pass reports remaining seeds; run again with the same cap to continue.

Review exit codes: 0 complete, 1 usage/storage error. `--json` errors follow the corpus resolve/expand envelope (`error.code`, `error.message`, optional `error.hint`, `exitCode`). All review mutations default to dry run; only `--write` persists. Review never inducts sources or files issues.
