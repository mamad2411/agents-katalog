---
name: reading-pipeline
version: 1.0.0
description: "Universal 5-layer book distillation skill — turn books, long PDFs, EPUBs, AZW3/MOBI, or research papers into compounding knowledge instead of one-off summaries. Use when user asks to: distill / read / digest / analyze / unpack / break down a book; build a reading note; turn a book into a skill (book2skill); create cross-book synthesis with explicit Convergence + Divergence; do RQ-driven deep reading; add a new book to an existing topic cluster; produce an Obsidian-compatible reading-note with citations; or asks in Chinese 拆解 / 蒸馏 / 深读 / 拆书 / 求同存异 / 知识编排 / 跨书综合 / 书做成skill / 多本书合并 / book2skill / 概念聚合 / 读书拆解 / 长文蒸馏. Compatible with Codex, Hermes, Claude Code, and any agent reading SKILL.md frontmatter. Not for casual summaries — every output must promote to L3/L4 or be explicitly archive_only."
metadata:
  requires:
    config: "config.yaml"
    optional_bins: ["docling", "pandoc", "pdftotext"]
    optional_skills: ["docling", "book-collector", "ebook-finder", "pdf"]
  supersedes:
    - reading-knowledge-compiler
    - deep-reading-domain-memory
  produces:
    - "L2 reading-note (Markdown with frontmatter)"
    - "L3 wiki-concept page (Markdown with frontmatter, multi-source aware)"
    - "L3.5 cross-book-synthesis (topic-map Markdown)"
    - "L4 skill body (SKILL.md + references/) plus Obsidian pointer card"
  artifacts_outside_vault:
    - "${SCRATCH_PATH}/<project>/*.txt + *-headings.md + index.json (L0)"
    - "${SCRATCH_PATH}/<project>/<book>-relevance.json (L1)"
---

# reading-pipeline — 5-Layer Book Distillation Skill

This skill turns reading into a **compounding asset**. Books, long PDFs, and research papers go in; structured Markdown knowledge in a configurable vault comes out, in 5 layers (L0 → L4).

For full project context, see the README in the skill's repo. For execution, follow this Operating Contract and the `references/` manuals.

## What this skill does

| Layer | Output | Location |
| --- | --- | --- |
| L0 — Raw Extract | txt + headings + index.json | `${SCRATCH_PATH}/<project>/` |
| L1 — Question Match | `relevance.json` (RQ-driven gate) | `${SCRATCH_PATH}/<project>/` |
| L2 — Single-Book Distillation | 9-section reading-note | `${VAULT_PATH}/${PATHS.L2_READING_NOTES}/<date>-<slug>-L2.md` |
| L3 — Concept Aggregation | wiki-concept with mandatory Convergence/Divergence/Synthesis | `${VAULT_PATH}/${PATHS.L3_CONCEPTS}/<concept>.md` |
| L3.5 — Cross-Book Synthesis | topic-map with Authority Matrix + Divergences | `${VAULT_PATH}/${PATHS.L3_5_CROSS_BOOK}/<topic>-cross-book-synthesis.md` |
| L4 — Method / Skill | Codex skill body + Obsidian pointer card | `${CODEX_SKILLS_PATH}/<slug>/` + `${VAULT_PATH}/${PATHS.L4_SKILL_POINTERS}/<slug>.md` |

## What this skill does NOT do

- Not a casual summarizer (use ChatGPT for that)
- Not a book downloader (delegate to `ebook-finder` or user-provided files)
- Not a PDF extractor by itself (delegate to `docling` or `pandoc` — see `references/skill-bridges.md`)
- Not an auto-publisher (vault is internal; publication is downstream)
- Not for casual "read this and summarize" — every output must promote to L3/L4 or `archive_only` with reason

## Configuration

Read `${SKILL_DIR}/config.yaml` (or `config.example.yaml` for the template) for personalized paths and research questions. All `${VAULT_PATH}` / `${SCRATCH_PATH}` / `${PATHS.*}` references in this skill resolve from `config.yaml`.

If `config.yaml` is missing, refuse to proceed and ask the user to create one from `config.example.yaml`.

## Operating Contract (10 hard rules)

1. **Read the schema first.** Open `schema/reading-pipeline-schema.md` (in skill directory) before any non-trivial decision. The schema defines field names, section requirements, lint gates, and promotion rules. Do not improvise these.

2. **Classify the request.** Use `references/00-pipeline-overview.md` §2 Request Triage. Different entry points: new-book ingest / cluster-merge / quarterly re-distillation / single-concept revision.

3. **Always run the L1 RQ-match gate.** Even if user says "just read it," confirm at least one research question (from `config.yaml` + `${VAULT_PATH}/${PATHS.RESEARCH_QUESTIONS}/`) is matched, or get explicit `--force-full` override. Unfocused reading is the most common failure mode.

4. **Resolve citations.** No L2 reading-note ships with `citations_resolved: true` unless every Reusable Framework in §4 has a row in §5 with a `(source: §section / heading-anchor)` reference. Otherwise set `citations_pending_l0: true`.

5. **Fill Differential Value.** Before saving L2, list already-read books in the same cluster and write the head-to-head comparison. If first in cluster: write "baseline" + frameworks setting the bar. Abstract praise ("classic", "comprehensive", "insightful") is forbidden.

6. **Grep before creating L3.** Search `concept:` and `aliases:` fields across `${VAULT_PATH}/${PATHS.L3_CONCEPTS}/` before creating any new wiki-concept. If a synonym matches, `merge_into_concept` — never fork. Be aggressive with aliases (include Chinese + English variants).

7. **Forbid empty Synthesis at status:active.** L3 pages without user judgment are noise. Either get the user's synthesis (or your best draft pending review with `status: draft`), or `merge_into_concept` an existing page, or do not create.

8. **Pointer card is part of L4.** Creating a Codex skill body without `${VAULT_PATH}/${PATHS.L4_SKILL_POINTERS}/<slug>.md` is incomplete. Both must exist in the same turn. The pointer card body is ≤ 150 lines and does NOT copy SKILL.md content.

9. **Use the 5-tag merge taxonomy** when merging new books into existing concepts: SUPPORTS / REFINES / CONTRADICTS / NEW (sub-aspect) / NEW (concept). Tag every contribution explicitly. CONTRADICTS triggers user-review flag, never silent Synthesis overwrite.

10. **Quarterly re-distillation is not optional.** When triggered (90 days default), regenerate Synthesis for any L3 with `sources ≥ 3`, and update L3.5 Authority Matrix. Skipping = compounding drift. Append entry to `${VAULT_PATH}/${PATHS.CHANGE_LOG}`.

## Default Output

Unless the user specifies otherwise, when asked to ingest a new book the skill produces, in order:

1. L0 extraction artifacts (txt + headings.md + index.json) in `${SCRATCH_PATH}/<project>/`
2. L1 relevance.json with RQ matches and `recommended_depth`
3. L2 reading-note in `${VAULT_PATH}/${PATHS.L2_READING_NOTES}/<date>-<slug>-L2.md`, using `templates/L2-single-book-reading-note.md`
4. L3 wiki-concept pages (created or updated) per the Distillation Recommendation
5. L3.5 topic synthesis if the book belongs to an existing or newly-formed cluster
6. L4 skill update or new skill if frameworks cross the threshold defined in §References below
7. Updates to `${VAULT_PATH}/${PATHS.READING_INDEX}` and `${VAULT_PATH}/${PATHS.ROUTING_INDEX}`
8. End-of-run summary listing every file created or modified, with quality-gate status

## Pipeline Entry Points

| Trigger | Entry | Primary reference |
| --- | --- | --- |
| New book to ingest | `references/00-pipeline-overview.md` §1 | `references/10-l0-extraction.md` |
| Additional book in existing cluster | `references/70-new-book-merger.md` | merger protocol |
| Quarterly re-distillation | `references/80-quality-gates.md` §quarterly | re-distillation routine |
| Audit existing L2/L3 quality | `references/80-quality-gates.md` §lint | lint checklists |
| Create or upgrade an L4 skill from concepts | `references/60-l4-skill-distillation.md` | skill creation flow |
| Look up exact prompts to use | `references/90-prompt-templates.md` | concrete LLM prompts per layer |
| See what good output looks like | `references/95-case-studies.md` | 3 worked clusters as gold standard |
| Verify skill behavior | `references/self-test.md` | smoke + behavior + failure mode tests |
| Diagnose an issue | `references/known-issues.md` | common pitfalls + fixes |
| Coordinate with other skills | `references/skill-bridges.md` | docling, book-collector, lark-doc, etc. |
| Find templates / schemas | `references/source-templates-index.md` | canonical paths |

## References

Open the relevant reference in full when executing that stage. **Do not paraphrase** — these references are precise enough that paraphrasing introduces drift.

### Layer specs
- `references/00-pipeline-overview.md` — 5-layer flow, request triage, end-of-run summary template
- `references/10-l0-extraction.md` — epub/pdf extraction, headings parsing, index.json contract
- `references/20-l1-question-match.md` — RQ match algorithm, depth-decision rules, skip criteria
- `references/30-l2-single-book.md` — L2 9-section structure, citation resolution, differential value rules
- `references/40-l3-concept-aggregation.md` — wiki-concept creation, uniqueness grep, 5-tag merge taxonomy
- `references/50-l3-5-cross-book-synthesis.md` — Authority Matrix, Divergences discipline, 12 mandatory sections
- `references/60-l4-skill-distillation.md` — Codex skill body + pointer card contract
- `references/70-new-book-merger.md` — incremental updates, tag propagation
- `references/80-quality-gates.md` — per-layer lint, quarterly re-distillation

### Operational manuals
- `references/90-prompt-templates.md` — concrete LLM prompts per layer (drop-in)
- `references/95-case-studies.md` — 3 fully worked clusters (strategy / thinking method / quant) as gold standard
- `references/self-test.md` — verify skill behavior; smoke + behavior + failure tests
- `references/known-issues.md` — common pitfalls (entity pollution, empty Synthesis, etc.) + fixes
- `references/skill-bridges.md` — cooperation with docling / book-collector / ebook-finder / lark-doc / pdf

### Reference data
- `references/source-templates-index.md` — canonical paths to all templates and schemas
- `schema/reading-pipeline-schema.md` — authoritative 5-layer specification (the constitution)
- `schema/knowledge-classification-schema.md` — folder taxonomy, canonical types, canonical domains

## Quality Rules (hard constraints — see references/80-quality-gates.md for full lint)

- Do not write durable concept content to `${PATHS.L2_READING_NOTES}` (raw is for source captures, not concepts)
- Do not write skill bodies into `${PATHS.L4_SKILL_POINTERS}` (only pointer cards live in vault; bodies live in `${CODEX_SKILLS_PATH}`)
- Do not create wiki-concept pages whose `Synthesis` section is empty AND `status: active`
- Do not create L2 reading-notes with `citations_resolved: true` if §5 Citations is empty or placeholder
- Do not allow `concepts_to_promote` to contain person names, tool names, product names, or any non-abstract terms
- Do not silently flatten conflicts in cross-book synthesis — every divergence between sources gets its own row
- Do not skip writing the pointer card when creating a new Codex skill — both files must land in the same turn
- Do not run a quarterly re-distillation without appending to `${VAULT_PATH}/${PATHS.CHANGE_LOG}`
- Do not invent values for the `domain:` frontmatter field — must be one of `canonical_domains` in `config.yaml`
- Do not write outside the paths declared in `config.yaml.paths` and `${SCRATCH_PATH}`

## Self-Check Before Final

Before declaring the pipeline complete for a given book or topic, verify:

- L2 reading-note exists, all 9 sections filled, lint passes (`references/80-quality-gates.md` §L2)
- Every `concepts_to_promote` entry has been resolved (created or merged)
- If a new L4 skill was created: both Codex body and Obsidian pointer card exist
- If the book belongs to an L3.5 cluster: cluster's Authority Matrix and Integration History updated
- `${VAULT_PATH}/${PATHS.READING_INDEX}` lists the new L2 entry
- End-of-run summary lists every file touched and any open question requiring user judgment

See `references/self-test.md` for the full verification suite.

## Locale awareness

Per `config.yaml.locale`:
- Concept naming: prefer the source's originating language when distinct (e.g. `Evidence Matrix`, not `证据矩阵`, since the framework originated in English-language management literature)
- Aliases: always populate both Chinese and English variants when applicable — every alias miss is a future fork
- Operating Contract, this SKILL.md, and references are written in English by default for broader collaboration; the user's vault content can be in any language
