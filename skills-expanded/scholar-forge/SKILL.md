---
name: scholar-forge
description: >-
  End-to-end academic research and writing skill with citation integrity,
  venue-aware formatting, bilingual CN/EN support (GB/T 7714), and full
  lifecycle workflows (literature review, IMRaD, thesis, grant, peer review,
  rebuttal). Fetches live journal guidelines before writing. Use when writing
  papers, theses, proposals, LaTeX manuscripts, citations, literature reviews,
  reviewer responses, or any scholarly document. Triggers on 论文, 文献综述,
  学位论文, arXiv, BibTeX, IMRaD, PRISMA, rebuttal, grant proposal.
---

# Scholar Forge

One skill, full academic lifecycle — integrity-first, venue-aware, bilingual.

## Non-Negotiables

1. **No fabricated citations** — every reference must be located and verified (title, authors, venue, year, DOI/URL). Mark unverified as `[UNVERIFIED]`.
2. **Evidence-first** — non-trivial claims need a citation or an explicit result in the document.
3. **Label source status** — peer-reviewed / preprint / grey literature / web.
4. **Venue before prose** — fetch target journal or school guidelines before drafting (see [venue-intelligence.md](references/venue-intelligence.md)).
5. **Two-stage writing** — outline with claim-evidence map → prose. Never skip outline for full manuscripts.
6. **Compile or validate** — after LaTeX edits, run `latexmk` or report the specific error.

## Mode Router

Identify the user's task and load the matching task file **before** writing.

| Mode | Triggers | Task file |
|------|----------|-----------|
| Literature review | 综述, survey, PRISMA, systematic review | [tasks/literature-review.md](tasks/literature-review.md) |
| Research paper | IMRaD, conference, journal article | [tasks/imrad-paper.md](tasks/imrad-paper.md) |
| Thesis / dissertation | 学位论文, PhD, master's thesis | [tasks/thesis.md](tasks/thesis.md) |
| Grant / proposal | 基金, NSF, NSFC, 国自然, R01 | [tasks/grant-proposal.md](tasks/grant-proposal.md) |
| Peer review | review this paper, 审稿意见 | [tasks/peer-review.md](tasks/peer-review.md) |
| Revision / rebuttal | rebuttal, response to reviewers, 修回 | [tasks/revision-rebuttal.md](tasks/revision-rebuttal.md) |
| Material integration | chat log, notes → paper, vibe writing | [tasks/material-integration.md](tasks/material-integration.md) |

If multiple modes apply, confirm priority with the user. Default order: clarify requirements → venue intelligence → discovery → outline → prose → QA.

## Execution Plan (show first)

```
SCHOLAR FORGE — EXECUTION PLAN
==============================
Mode:           [from router]
Target venue:   [journal / school / funder]
Language:       [EN / 中文 / bilingual abstract]
Citation style: [IEEE / APA / ACM / GB/T 7714 / venue-specific]
Reporting:      [IMRaD / PRISMA / CONSORT / STROBE / none]
Output:         [LaTeX + .bib / Markdown / DOCX via pandoc]
Venue profile:  [PENDING → fetch before writing]
```

## Phase 1 — Requirements (ask if missing)

Essential: document type, topic/contribution, target venue, length limit, citation style, deadline, language.

Use this intake template when helpful:

```markdown
## Scholar Forge Request
**Mode:** [paper / review / thesis / grant / rebuttal / integrate]
**Topic:** [...]
**Venue:** [Nature Methods / IEEE TNNLS / 清华大学学位论文 / NSFC 青年基金]
**Length:** [words or pages]
**Citation:** [auto from venue or specify]
**Data/files:** [@mentions]
**Language:** [EN / 中文]
```

## Phase 2 — Venue Intelligence

**Always run for papers, theses, and grants.** Do not rely on stale knowledge.

1. WebSearch official author guidelines + AI authorship policy for the target venue.
2. WebFetch the guidelines page; extract limits, citation style, abstract structure, figure limits, template URL.
3. Save `writing_outputs/<project>/venue_profile.yaml` using the schema in [venue-intelligence.md](references/venue-intelligence.md).
4. For Chinese theses, also load [chinese-academic.md](references/chinese-academic.md).

## Phase 3 — Discovery & Verification

### Search strategy

| Domain | Primary sources |
|--------|-----------------|
| CS / Engineering | Semantic Scholar, arXiv, ACM DL, IEEE Xplore |
| Biomedical | PubMed, PMC, bioRxiv |
| General | OpenAlex, Crossref, Google Scholar |
| Chinese | CNKI 知网, 万方, 维普 (user may need institutional access) |

Query patterns: broad survey → recency filter → exact phrase → snowball from 2–3 anchor papers.

### Per-source record

```markdown
## [citation_key]
- Title / Authors / Year / Venue
- Status: peer-reviewed | preprint | grey
- DOI / URL
- Takeaway (1–2 lines) | Use in: [section]
```

Maintain `references.bib` as single source of truth. Run validation when scripts are available:

```bash
python scripts/validate_bib.py references.bib
python scripts/check_citations.py paper.tex references.bib
```

Details: [integrity-protocol.md](references/integrity-protocol.md), [citation-formats.md](references/citation-formats.md).

## Phase 4 — Outline & Claim-Evidence Map

Before prose, produce:

1. Section outline with word budgets per venue profile.
2. Claim-evidence map (template: [templates/claim-evidence-map.md](templates/claim-evidence-map.md)).
3. Figure/table plan with one-sentence takeaway each.

## Phase 5 — Writing

### Universal prose rules

- Flowing paragraphs in Abstract, Introduction, Discussion, Conclusion — no bullets unless venue allows structured abstract.
- Active voice preferred ("We measured…").
- Hedge appropriately; avoid AI tells: "remarkably", "delve", "landscape", "it's important to note", "in conclusion" opener.
- Match the paper's established voice; add transition sentences between inserted blocks.

### Citation styles

| Style | Typical use | Guide |
|-------|-------------|-------|
| IEEE | CS, engineering | [citation-formats.md](citation-formats.md) |
| APA 7 | social sciences | same |
| ACM | computing venues | same |
| GB/T 7714 | 中文学位论文、期刊 | [chinese-academic.md](chinese-academic.md) |

### LaTeX

- Prefer official publisher templates from venue profile.
- Scaffolds: [templates/ieee-conference.tex](templates/ieee-conference.tex), [templates/gb7714-thesis.tex](templates/gb7714-thesis.tex).
- Compile: `latexmk -pdf -bibtex paper.tex` (or `-usebiber` for biblatex).

## Phase 6 — Quality Assurance

Run before delivery:

### Integrity audit
- [ ] Every `\cite{}` key exists in `.bib`
- [ ] No `[UNVERIFIED]` entries in final bibliography
- [ ] Claim-evidence map satisfied for major claims
- [ ] Retraction check for critical citations (Crossref / Retraction Watch if available)

### Venue compliance
- [ ] Word limits (abstract, main text, references)
- [ ] Required sections and abstract structure
- [ ] AI disclosure statement if required by venue

### Writing audit
- [ ] AI-voice patterns removed (see [writing-quality.md](references/writing-quality.md))
- [ ] Abstract matches paper content
- [ ] Limitations and threats to validity stated

### Reproducibility (if empirical)
- [ ] Data/code availability statement
- [ ] Seeds, splits, baselines, compute budget documented

## Output Deliverables

1. Source files (`.tex`, `references.bib`, `venue_profile.yaml`)
2. Brief change log: what was written, integrated, or verified
3. Compilation status or validation script output
4. Open items flagged for user (paywalled papers, unverified claims)

## Additional Resources

- [integrity-protocol.md](references/integrity-protocol.md) — verification, retraction, predatory journals
- [venue-intelligence.md](references/venue-intelligence.md) — live guideline extraction schema
- [chinese-academic.md](references/chinese-academic.md) — GB/T 7714, thesis norms, CNKI workflow
- [writing-quality.md](references/writing-quality.md) — AI-voice audit, hedging, transitions
- [reporting-guidelines.md](references/reporting-guidelines.md) — PRISMA, CONSORT, STROBE, ARRIVE
