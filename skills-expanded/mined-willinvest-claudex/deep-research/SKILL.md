---
name: deep-research
description: >-
  Deep, multi-source, fact-checked research reports — entirely on the Claude subscription,
  no API keys. Plans a TOC + acceptance criteria, fans out parallel Task subagents that search
  the live web (native WebSearch/WebFetch), gap-fills weak sections, then synthesizes a
  long-form report with inline [n] citations and a Sources list whose every URL is
  DETERMINISTICALLY verified against URLs that actually appeared in search results (fabricated
  citations are dropped). A subscription-only port of NVIDIA AI-Q's deep-research core. Use
  when the user wants a thorough researched report, a literature/landscape/market scan, a
  cited comparison, or "deep research" / "research X for me". BEFORE invoking, if the question
  is underspecified (e.g. "what car should I buy" with no budget/use/region), ask 2-3
  clarifying questions to narrow scope, then research the refined question.
license: Apache-2.0
---

# deep-research

A subscription-only port of NVIDIA AI-Q's deep-research core (Apache-2.0 — see `NOTICE`). The
**main agent is the orchestrator**: it plans, fans out parallel `Task` researchers that use
native `WebSearch`/`WebFetch`, gap-fills, synthesizes a long-form cited report, and then runs a
**deterministic** citation verifier so every `[n]` maps to a real, captured source URL.

`$SKILL_DIR` below is this skill's directory; prompts live in `prompts/`, the verifier in
`scripts/verify_citations.py`. Read each `prompts/*.md` when you reach its step.

## When to use
Researched reports, landscape/market/literature scans, cited comparisons, "deep research on
…", "research X and tell me the alternatives". Skip it for trivial chit-chat or pure factual
one-liners (the router will route those to a direct answer / shallow pass).

## Flow

**0. Route & disambiguate** — read `prompts/router.md`. Classify meta vs research, then
shallow vs deep. For a plainly trivial question, answer directly. If the query is genuinely
ambiguous and you can't pause for the user, state ONE interpretation line at the top of the
report and proceed.

**1. Set up a per-run working dir** — create a fresh run directory:
`<vault>/<topic>/runs/<run-id>/`. Inside it create:
- `<run-dir>/notes/`
- `<run-dir>/yt-report/`
- `<run-dir>/report_draft.md`
- `<run-dir>/report_final.md`
- `<run-dir>/audit.json`

Prior runs are never verifier input. The lane must not write to persistent shared `notes/`;
only the current run's `<run-dir>/notes/` is scanned by the verifier.

**2. Plan** — read `prompts/planner.md`. Run 2-4 scoping `WebSearch` calls, then produce the
plan object: task analysis, report title, TOC (≤8 sections), **constraints (acceptance
criteria)**, and **4-6** self-contained queries. Keep the plan in your context.

**3. Research (parallel fan-out)** — read `prompts/researcher.md`. Group the web queries into
2-3-per-bundle and launch **up to 6** `Task` (general-purpose) subagents **in a single
message** so they run concurrently. Give each subagent: the researcher prompt, its bundled
questions, the relevant constraints, and an instruction to **write its notes to
`<run-dir>/notes/researcher_<k>.md`** (a dedicated notes subdir — keep researcher notes separate from the draft; the verifier only scans `researcher_*.md` files, so this naming is REQUIRED) and also return them. Each researcher uses only
WebSearch/WebFetch, ≤8 calls, broad→narrow, and lists ONLY real captured URLs.

**3b. YouTube lane** — if any planned queries are marked `youtube_suited` and `gemini` is
available, run one `Bash -> gemini` task using `prompts/researcher_youtube.md`. Pass the
tagged queries, `<run-dir>`, fan-out cap <=4, search/fetch cap <=8 per subagent, and
links-per-video cap <=5. Gemini writes raw notes to `<run-dir>/yt-report/researcher_yt_<k>.md`
and opened logs to `<run-dir>/yt-report/opened_yt_<k>.json`. If `gemini` is absent, skip the
YouTube lane, log the skip, and continue web-only.

**3c. Codex trust check** — detect `codex` before checking YouTube outputs. If absent,
continue to the deterministic gate with opened-log enforcement and emit the integrity warning
`Codex trust-check skipped`. If present, run Codex read-only over `<run-dir>/yt-report/` using
`prompts/codex_check.md`; it may only write `<run-dir>/yt-report/codex_annotations.json`.
Codex must not edit Gemini files, add sources, write notes, or synthesize.

**3d. Filter YouTube notes** — before synthesis and verification, run the deterministic filter
for each raw YouTube note:

```bash
python3 "$SKILL_DIR/scripts/filter_yt_notes.py" \
    --run-dir <run-dir> \
    --index <k>
```

If Codex was detected as present for the run, add `--codex-present`. The filter writes
`<run-dir>/notes/researcher_yt_<k>.md` and `<run-dir>/yt-report/filter_integrity_yt_<k>.json`.
Opened-log exact-match enforcement always applies. Absent Codex emits
`Codex trust-check skipped`; present-but-failed Codex annotations exclude all YouTube notes.
`drop` URLs are removed mechanically at paragraph/list-item/sentence/marker scope. `flag` URLs
are kept and surfaced in integrity metadata. No semantic claim rewriting is promised beyond
those mechanics.

**4. Gap-fill (bounded, merit)** — read all `researcher_*.md`. Check each TOC
section/constraint for coverage. If a section came back empty or weak, dispatch **ONE** more
researcher to fill that specific gap, then proceed. Do not loop — "try once to fix, then
proceed".

**5. Synthesize** — read `prompts/synthesis.md`. Read EVERY note file, then write a
3000-5000+ word report that follows the TOC, with inline `[n]` citations and a `## Sources`
section. Cite ONLY URLs present in the notes; never from memory; no bare URLs in the body.
Write the draft to `<run-dir>/report_draft.md`.

**6. Verify (deterministic — the core merit)** — read `prompts/citations.md`. Run:

```bash
python3 "$SKILL_DIR/scripts/verify_citations.py" \
    --report <run-dir>/report_draft.md \
    --notes  <run-dir>/notes \
    --out    <run-dir>/report_final.md \
    --audit  <run-dir>/audit.json
```

The verifier rebuilds the source registry from the notes' real URLs and keeps a `[n]` only if
its URL resolves into that registry (repairing fuzzy-but-real URLs, dropping fabricated ones,
deduping, sanitizing, renumbering). URL matching is strict — exact / child-path / query-subset
only; a report URL that is merely a prefix of a captured one is rejected (truncated citations are
dropped, not guessed), and every URL in the final report must resolve into the registry. Then:
- **exit 3 / `captured_sources: 0`** → present under the `⚠️ UNVERIFIED — model knowledge
  only` banner (or re-run); never as a normal report.
- **exit 4** → sources were captured but the verified report has no surviving `[n]` (or no
  `## Sources`, or a bare/unresolved URL remained): the script emits an `⚠️ UNVERIFIED` banner
  and refuses to manufacture a citation. Do ONE targeted re-dispatch/rewrite citing only captured
  sources, then re-verify; never present exit-4 output as sourced.
- read `audit.json` and tell the user which citations (if any) were dropped and why
  (`citations_dropped`, `skipped_report_files`, `gate_failures`).
- verify the report against each planner **constraint**; note any unmet.
- apply the **done-gate** (length, ≥2 `##` headers, `## Sources` present, ≥1 verified
  citation, no giving-up phrasing). The script enforces the sources / ≥1-citation part (exit 4);
  the rest is on you. If it fails, ONE targeted re-dispatch, then re-verify.

**7. Present** `report_final.md` to the user, plus a one-line integrity note (sources captured,
citations verified, any dropped). Read every
`<run-dir>/yt-report/filter_integrity_yt_<k>.json` and aggregate its `warnings`,
`flagged_urls`, and `video_skips` into that note so flag/low-trust kept URLs and YouTube
degradation warnings are user-facing, including YouTube degradation warnings that would
otherwise be hidden in metadata.

## Dependency/degradation

| Dependency | If missing or degraded |
|---|---|
| `gemini` | Skip the YouTube lane, log the skip, and continue web-only. |
| `codex` absent | Continue with opened-log enforcement and deterministic verification; emit `Codex trust-check skipped`. |
| `codex` present-but-failed | Missing, empty, malformed, or unusable annotations fail closed: exclude all YouTube notes and log it. |
| `yt-dlp` | Comments and comment-links degrade to empty; transcript plus description still runs and the degradation is logged. |

## Hard rules (the AI-Q merits — do not weaken)
1. **Citation integrity is deterministic.** Cite only URLs the researchers recorded from
   WebSearch/WebFetch results; the script — not your judgment — is the gate (exit 3 = zero
   sources, exit 4 = zero surviving citations ⇒ the loud UNVERIFIED banner, never a normal
   report). The registry is built from the notes, so the script catches synthesis-time
   fabrication; for stronger provenance you can pass `--registry sources.json`.
2. **Gap-fill** once for weak sections before synthesizing.
3. **Constraint verification** against the planner's acceptance criteria at the end.
4. **Disambiguate** with a bias to proceed: state an interpretation rather than blocking.
5. **YouTube trust boundary is weaker.** The YouTube lane trust model is
   `Gemini-fetched -> opened-log filtered -> optional Codex-checked -> deterministically gated`.
   This is weaker than Claude WebSearch/WebFetch capture because Gemini's opened log is self-reported.
   Opened-log enforcement lives in `filter_yt_notes.py`; Codex is read-only and the verifier
   still receives only `<run-dir>/notes/`.

## Knobs
≤6 researchers · ≤8 searches each · 2 loops (round 1 + one gap-fill) · 4-6 plan queries · 2-3
queries per dispatch · ≤8 TOC sections · 3000-5000+ words (deep). See `references/aiq-mapping.md`.

## Always produce a report
Never stop to ask permission mid-run, and never emit "I can't produce a report". A partial
report with honestly-acknowledged gaps beats stopping — except the zero-sources case, which
must be labelled UNVERIFIED.
