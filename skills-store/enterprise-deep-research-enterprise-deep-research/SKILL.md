---
name: enterprise-deep-research
description: >-
  Produce a full multi-layer research dossier (~42,500 words, 6 executive layers
  + 10-metric quality audit + Word export) on a stated use case. Use only when
  the user explicitly asks for a deep-research dossier, an enterprise research
  report, or a comparable multi-day research deliverable — not for ordinary
  literature lookups, single questions, or summaries, which the individual
  database and web-search tools already answer directly.
---

# Enterprise Deep Research

Six executive layers written by subagents, audited against ten quality metrics,
compiled into one Markdown dossier and exported to Word.

**Cost warning — state this to the user before starting.** A full run dispatches
6+ subagents, issues 40–100 searches, and produces ~42,500 words. It takes
multiple turns and a large token budget. If the user wants a quick answer, use
`WebSearch` or a database skill instead and say so.

## Preconditions

1. `uv` on PATH (`uv --version`). The exporter declares its own dependencies
   inline; no venv setup is needed.
2. A working directory the user has chosen. Everything is written there —
   never into this skill's own directory.
3. Confirm with the user: use case, domain (biomedical / computer science /
   financial / engineering / qualitative), classification label, and whether
   Word export is wanted.

## Tools this skill actually uses

| Purpose | Tool |
| :--- | :--- |
| Dispatch layer writers | `Agent` (subagent_type `general-purpose`) |
| Broad literature and market search | `WebSearch`, `WebFetch` |
| Biomedical citations and verification | `mcp__plugin_bio-research_*` (PubMed, bioRxiv, ClinicalTrials, ChEMBL, Consensus, OpenTargets) |
| Read/write layer files and the dossier | `Read`, `Write`, `Edit`, `Glob` |
| Word export, file manifest | `PowerShell` |

If a bio-research MCP server is not connected, fall back to `WebSearch` +
`WebFetch` against the publisher or DOI resolver and record which index was
used in the scorecard's `sample.index_used` field. Do not claim a citation was
verified against an index you did not query.

---

## Phase 1 — Scope

1. Decompose the use case into a MECE problem tree; name the sub-problems.
2. Write 3–5 search query strings per sub-problem, tuned for the indices above.
3. `New-Item -ItemType Directory -Force dossier_temp` in the working directory.
4. Write `dossier_temp/00_scope.md`: use case, domain, sub-problems, queries,
   inclusion/exclusion criteria, date range. Every layer subagent reads this.

## Phase 2 — Layers 1 and 2 (dependency-ordered)

Layer 2 formalizes the architectures Layer 1 proposes, so **Layer 1 finishes
before Layer 2 starts**. Dispatch them sequentially, one `Agent` call each.

Each dispatch prompt contains: the use case, the absolute path of
`dossier_temp/00_scope.md`, the absolute path of
`references/executive_layers.md`, the target file path, the word target, and
this instruction — *"Search first, then write. Every factual claim carries an
inline citation with a resolvable URL or DOI. Write the complete file with the
`Write` tool before returning. Return only the file path and its word count."*

After each subagent returns, verify its work rather than trusting the report:

```powershell
Get-ChildItem dossier_temp -File | Select-Object Name, Length, LastWriteTime
(Get-Content dossier_temp/layer1_analyst.md -Raw).Split().Count
```

If the file is missing, or under 60% of target, re-dispatch **that one subagent**
with the specific thin sections named. Cap at 2 retries, then continue with what
exists and record the shortfall in section 4.4 (Limitations).

> [!IMPORTANT]
> **HITL Gate 1.** Stop here. Show the user the candidate architectures from
> Layer 1 and the model selection from Layer 2, and get explicit approval or
> corrections before dispatching Layers 3–5. Approving after those layers have
> already run would be theatre — their token cost is already spent.

## Phase 3 — Layers 3, 4, 5 and 6

Layers 3 and 4 are independent of each other; dispatch both in a single message
(two `Agent` calls in parallel). Layer 5 reads layers 2 and 4, so it goes after
Layer 4 returns. Layer 6 reads all five and is written by **you**, the
coordinator — not a subagent — because synthesis needs the full picture.

```
[L1] -> [L2] -> GATE 1 -> [L3 ‖ L4] -> [L5] -> [L6 by coordinator]
```

Verify each returned file the same way as Phase 2.

## Phase 4 — Quality Audit

Score the drafts against [subordinate_metrics.md](references/subordinate_metrics.md).
That file is the sole definition of the metrics, the weights, the gate and the
JSON schema.

1. **Verify citations.** Sample `max(5, ceil(0.2 × bibliography_size))` citations,
   capped at 15. Resolve each one against a real index — `search_articles` for
   biomedical, `WebFetch` on `https://doi.org/{doi}` otherwise. Query them one
   at a time. Any citation that will not resolve is removed from the dossier and
   replaced with a verified reference; note the swap in section 5.3.
2. **Apply the domain rubric** for the declared domain. All four items need
   evidence, not assertions.
3. **Score all ten metrics** and compute the weighted composite. Show the
   contribution column and check that it sums to your reported composite.
4. **Gate:** composite ≥ 70 and no metric < 50. On failure, identify the weakest
   metric, run targeted searches to patch that specific gap, update the affected
   layer file, and re-score. Cap at 2 audit loops — if it still fails, report the
   failing metrics to the user honestly instead of looping further.
5. Emit the JSON scorecard exactly as schematized.

> [!IMPORTANT]
> **HITL Gate 2.** Show the user the scorecard, the composite, the verification
> sample results, and any citations that were replaced. Get sign-off before
> compiling.

## Phase 5 — Compile and Export

1. Write the file manifest **first**, while the intermediate files still exist:

```powershell
Get-ChildItem dossier_temp -File | ForEach-Object {
  [pscustomobject]@{ File=$_.Name; Bytes=$_.Length; SHA256=(Get-FileHash $_.FullName).Hash }
} | Format-Table -AutoSize
```

2. Compile `Enterprise_Research_Report.md` in the working directory, following
   the 11-section contract in [report_template.md](references/report_template.md).
   Read each layer file and inline it under section 6. Paste the manifest into
   section 11.

3. Export to Word (absolute path — the script does not live in the working
   directory):

```powershell
uv run "$HOME\.claude\skills\enterprise-deep-research\scripts\docx_generator.py" --input Enterprise_Research_Report.md --output output\Enterprise_Research_Report.docx
```

The exporter renders the dossier top to bottom, so every one of the 11 sections
reaches the .docx. It creates the output directory itself. Check the exit code
and the reported output path before reporting success.

4. **Ask before deleting.** `dossier_temp/` holds the per-layer sources. Offer to
   remove it; delete only on an explicit yes.

```powershell
Remove-Item -Recurse -Force dossier_temp
```

5. Deliver both files, and state plainly: the composite score, any metric that
   failed its threshold, the citation sample size and pass rate, and any layer
   that came in short.

---

## Reference

- Layer personas, structures, word targets, dependency order: [executive_layers.md](references/executive_layers.md)
- Metric definitions, weights, gate, JSON schema, domain rubrics: [subordinate_metrics.md](references/subordinate_metrics.md)
- Dossier section contract and formatting: [report_template.md](references/report_template.md)
- Word branding (fonts, colors, page size): `resources/report_styles.json`
- Exporter self-test: `uv run scripts/docx_generator.py --self-check`
