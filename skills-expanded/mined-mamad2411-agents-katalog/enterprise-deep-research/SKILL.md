---
name: enterprise-deep-research
description: >-
  Produce a full multi-layer research dossier (~42,500 words, 6 executive layers
  + 10-metric quality audit + Word export) on a stated use case. Use only when
  the user explicitly asks for a deep-research dossier, an enterprise research
  report, or a comparable multi-day research deliverable — not for ordinary
  literature lookups, single questions, or summaries, which the individual
  Science Skills already answer directly.
---

# Enterprise Deep Research

Six executive layers, audited against ten quality metrics, compiled into one
Markdown dossier and exported to Word.

**Cost warning — state this to the user before starting.** A full run issues
40–100 searches and produces ~42,500 words across many turns. If the user wants
a quick answer, use `literature-search-openalex`, `pubmed-database` or
`search_web` directly and say so.

## Prerequisites

1. **`uv`** — read the `uv` skill and follow its Setup instructions.
2. **Source skills** — this workflow calls `literature-search-openalex`,
   `pubmed-database` and `search_web`. Their own license-notification and
   credential rules apply; follow them, including the `credentials` skill
   protocol when a key is needed.
3. **Working directory** — everything is written to the user's workspace, never
   into this skill's directory.
4. Confirm with the user: use case, domain (biomedical / computer science /
   financial / engineering / qualitative), classification label, and whether
   Word export is wanted.

## Execution model

The coordinator writes each layer file itself, one layer per turn, in dependency
order. This works in any Antigravity session and needs no delegation tool.

If — and only if — the running environment exposes a verified subagent
delegation tool, Layers 3 and 4 may be dispatched in parallel, since they are the
only two layers with no dependency on each other. Check the tool exists before
relying on it. Do not invent a delegation call: a hallucinated tool name fails
the whole run silently.

```
[L1] -> [L2] -> GATE 1 -> [L3, L4] -> [L5] -> [L6]
```

---

## Phase 1 — Scope

1. Decompose the use case into a MECE problem tree; name the sub-problems.
2. Write 3–5 query strings per sub-problem for the databases above.
3. Create `dossier_temp/` in the user's workspace.
4. Write `dossier_temp/00_scope.md`: use case, domain, sub-problems, queries,
   inclusion/exclusion criteria, date range. Re-read it at the start of every
   later layer.

## Phase 2 — Layers 1 and 2

Write `dossier_temp/layer1_analyst.md`, then `dossier_temp/layer2_scientist.md`,
following [executive_layers.md](references/executive_layers.md). Layer 2 must
formalize the exact architectures Layer 1 proposed, so read Layer 1's file first.

Search before writing. Every factual claim carries an inline citation with a
resolvable DOI or URL.

After each file, verify it on disk rather than from memory:

```powershell
Get-ChildItem dossier_temp -File | Select-Object Name, Length, LastWriteTime
(Get-Content dossier_temp/layer1_analyst.md -Raw).Split().Count
```

A layer under 60% of its word target gets one targeted expansion pass on the
thin sections. If it is still short, continue and record the shortfall in
section 4.4 (Limitations).

> [!IMPORTANT]
> **HITL Gate 1.** Stop. Present the candidate architectures and model selection
> to the user and get explicit approval or corrections before writing Layers 3–5.

## Phase 3 — Layers 3, 4, 5 and 6

Write `layer3_novel.md` and `layer4_sota.md` (independent of each other), then
`layer5_methodology.md` (reads layers 2 and 4), then `layer6_cro_synthesis.md`
(reads all five). Layer 4 must catalog at least 15 peer-reviewed studies, each
one confirmed to exist before it is listed.

## Phase 4 — Quality Audit

Score the drafts against [subordinate_metrics.md](references/subordinate_metrics.md).
That file is the sole definition of the metrics, weights, gate and JSON schema.

1. **Verify citations.** Sample `max(5, ceil(0.2 × bibliography_size))`, capped
   at 15. Resolve each against `literature-search-openalex` or
   `pubmed-database`, one query at a time — those skills' own CLIs handle
   retries and rate limits, so do not build a retry loop around them. If a
   lookup fails, fall back to `search_web` on the DOI and record which index was
   actually used. Never mark a citation verified against an index you did not
   query. Unresolvable citations are removed and replaced; note the swap in 5.3.
2. **Apply the domain rubric** for the declared domain — all four items need
   evidence, not assertions.
3. **Score all ten metrics**, compute the weighted composite, and show the
   contribution column. Check that it sums to the composite you report.
4. **Gate:** composite ≥ 70 and no metric < 50. On failure, patch the weakest
   metric with targeted searches, update that layer file, re-score. Cap at 2
   loops, then report the failing metrics honestly rather than looping further.
5. Emit the JSON scorecard exactly as schematized.

> [!IMPORTANT]
> **HITL Gate 2.** Present the scorecard, composite, verification sample results
> and any replaced citations. Get sign-off before compiling.

## Phase 5 — Compile and Export

1. Write the file manifest **first**, while the intermediate files still exist:

```powershell
Get-ChildItem dossier_temp -File | ForEach-Object {
  [pscustomobject]@{ File=$_.Name; Bytes=$_.Length; SHA256=(Get-FileHash $_.FullName).Hash }
} | Format-Table -AutoSize
```

2. Compile `Enterprise_Research_Report.md` in the workspace, following the
   11-section contract in [report_template.md](references/report_template.md).
   Inline each layer file under section 6; paste the manifest into section 11.

3. Export to Word using the skill's absolute path — the script does not live in
   the user's workspace:

```powershell
uv run "$HOME\.gemini\config\skills\enterprise_deep_research\scripts\docx_generator.py" --input Enterprise_Research_Report.md --output output\Enterprise_Research_Report.docx
```

The exporter renders the dossier top to bottom, so all 11 sections reach the
.docx. It creates the output directory itself. Check the exit code and the
reported path before claiming success.

4. **Ask before deleting.** Offer to remove `dossier_temp/`; delete only on an
   explicit yes.

```powershell
Remove-Item -Recurse -Force dossier_temp
```

5. Deliver both files and state plainly: composite score, any metric below its
   threshold, citation sample size and pass rate, and any layer that came up
   short.

---

## Reference

- Layer personas, structures, word targets, dependency order: [executive_layers.md](references/executive_layers.md)
- Metric definitions, weights, gate, JSON schema, domain rubrics: [subordinate_metrics.md](references/subordinate_metrics.md)
- Dossier section contract and formatting: [report_template.md](references/report_template.md)
- Word branding (fonts, colors, page size): `resources/report_styles.json`
- Exporter self-test: `uv run scripts/docx_generator.py --self-check`
