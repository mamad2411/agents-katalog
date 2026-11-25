---
name: loom-write
description: Write drafts and articles from research, create Topic Notes, and finalize publication output. Use when the user asks to write an article, draft from a synthesis pack or notes, create or update a topic note, or turn research into publishable prose.
---

# Loom Write

Write from research, then settle knowledge. Pipeline: draft → topic → index.

## Read First

- `../shared/references/schemas.md`
- `<vault-root>/.loom/config.yaml` if it exists (vault configuration)

## Stage 1 — Draft

Write article prose from a Synthesis Pack (or reviewed Daily Notes if user explicitly wants a lighter workflow).

### Focus narrowing

Before drafting, review the Article Spine from the Synthesis Pack. Select 3-4 focus angles to go deep on. State which points get full treatment and which get brief mention or are omitted. Prefer narrow and deep over broad and thin.

### Source grounding

Before drafting, re-read all Source Briefs from the vault. The Synthesis Pack provides structure; the Source Briefs provide substance.

When drafting each section:
- Every specific claim, data point, or code pattern must trace to at least one Source Brief. Cite sources inline with source ID (e.g. "S1 发现...", "根据 S2 的实现...").
- For direct quotes, read the Raw Capture to verify exact wording.
- If the Article Spine calls for content not covered by any Source Brief, mark it [需要额外来源] rather than fabricating from model knowledge.

### Writing flow — 5-step critical writing

1. 摆观点: put the core viewpoint on the table explicitly.
2. 第一刀 — 反问/追问/翻转: first cut — challenge with counter-question, deeper inquiry, or perspective flip.
3. 第二刀: second cut pushes further into the tension.
4. 切到底: cut to the bottom — reach the irreducible position.
5. 综合: synthesize with the user's voice. Match depth to topic scope — focused single-angle ~800 words, comprehensive multi-angle 2500-3500 words.

### Output formatting

- Detect article type and apply appropriate structure.
- Consistent heading hierarchy (H1 title, H2 sections, H3 subsections).
- Proper markdown: links, emphasis, blockquotes for cited material.
- YAML frontmatter with metadata.

### Draft rules

- Draft may polish, reorganize, and strengthen the user's voice.
- Draft must NOT overwrite Raw Capture, Daily Note, Source Brief, Synthesis Pack, or Topic Note.
- Draft content must be derivable from the Synthesis Pack.
- Draft claims must be traceable to Source Briefs. No unsourced factual assertions.
- Default destination: `01_Daily_Notes/YYYY/working/`.
- Do not move to `published/` unless user explicitly confirms.
- Preserve high-risk claim markers until verified or consciously accepted.

### Quality check — 9 red lines

Apply as final pass on the draft:
1. 口语测试: if you can't say it aloud naturally, rewrite.
2. 零术语: no unexplained jargon.
3. 短词优先: prefer short words.
4. 一句一事: one idea per sentence.
5. 具象优先: concrete over abstract.
6. 理由先行: give reason before conclusion.
7. 不说废话: no filler phrases.
8. 信任读者: trust the reader's intelligence.
9. 诚实: be honest about uncertainty.

## Stage 2 — Topic Note

Convert trusted research into durable knowledge.

### Input priority

1. Synthesis Pack.
2. `reviewed` Daily Notes.
3. Final or Published Article.

### Topic creation flow

**Structural decomposition:**
- Identify the irreducible generators of the topic.
- Map how they combine to produce observed phenomena.
- Draw ASCII structural diagram.

**Depth layers:**
- Layer: surface facts → mechanisms → principles → axioms.
- Mark where knowledge is solid vs. uncertain.

### Output

- Synthesis Topic Note in `02_Topic_Notes/<Category>/`.
- Category directories use Pascal_Case.
- Filename: `YYYY-MM-DD_Title-With-Words.md`.
- When updating, increment minor version (1.0.0 → 1.1.0).

### Topic rules

- Use calm knowledge-base voice. Not article rhetoric or platform tone.
- Focus on structure, mechanisms, applicability, boundaries, related work, reusable insights.
- Do not default to unreviewed Draft input. If user insists, mark source confidence explicitly.
- Preserve link-only Topic Notes unless user requests synthesis.

## Stage 3 — Index

Update vault indexes after Topic Note creation or changes.

### Index files

- `00_Index/TOPIC_INDEX.md` — match rows by exact title, update in place, append new.
- `00_Index/TIMELINE_INDEX.md` — months newest first, all three sections per month (New Topics, Updated Topics, Archived), newest first within sections.

### Index scripts

```bash
# Dry run (default)
python3 ../shared/scripts/build_indexes.py <vault-root>

# Write when explicitly requested
python3 ../shared/scripts/build_indexes.py <vault-root> --write
```

### Index rules

- Prefer dry-run before writing.
- Do not generate new knowledge insights during indexing.
- Do not run connection analysis here — that belongs to `loom-maintain`.

## Full Pipeline Rules

- Draft/Final must not overwrite any upstream artifact.
- Topic Notes remove article rhetoric and return to knowledge-base voice.
- Index updates happen after Topic Note creation, not before.
