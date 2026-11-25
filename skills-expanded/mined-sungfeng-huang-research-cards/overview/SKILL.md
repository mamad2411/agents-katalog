---
name: overview
description: >-
  Maintain ALL Heptabase comparison-overview card families with one skill —
  tokenizer/codec, spoken-LM/speech-LLM (nesting the auditory 聽覺理解・推理
  sub-topic: audio understanding/reasoning/audio-LM 驗收), duplex S2S, 語音生成
  (TTS family), ASR (non-LLM), and speech frontend/security. Find newly Tasks-tagged papers an overview is missing,
  route each to the right topic and act card, author a hung-yi-lee-style
  section + dimension row + paradigm/synthesis updates, re-sort by arxiv ID,
  refresh the 導讀, and keep the knowledge graph bookkeeping green. Use when
  the user asks to update/sync/補/re-sort ANY comparison overview card
  (任何主題的 overview 卡).
allowed-tools: Bash(heptabase *) Bash(python3 *)
---

# Overview Maintenance — one skill, config-discovered topics

## Backend

`heptabase`/`both`：原路徑不變。`obsidian`：engine 的 read/save 與 corpus 掃描走 vault；
卡片連結＝`[[wikilink]]`（讀入時解析為 card mention，coverage 圖照常運作）。注意 topic
config 內的 card id 需為該 backend 的 id（obsidian 為 `Folder/Name`）。

Comparison-overview cards live under the study/overview knowledge graph
(topic hubs → act cards; see the `overview-graph` skill for STRUCTURAL changes).
This skill maintains card CONTENT: coverage, per-paper sections, tables, sort.

**Before authoring anything, read the topic doc `topics/<topic>.md`** — it has
the card list/ids, act-routing rules, paradigm taxonomies, DIM_COLS, size
budget, and topic quirks. This file only carries what is common.

## Topics

| topic key | scope (Tasks values) | cards |
|---|---|---|
| &nbsp;&nbsp;└ `auditory` | Audio Understanding · Reasoning · Audio LM | 3 cards (AU/R/(E)驗收) under 聽覺翼 sub-hub 77b0b1af — nested in spoken |

Topology (own cards / sub_topics / MATCH sort keys / task values) is
**graph-derived**: `topics/<topic>/topic_snapshot.json`, written by
`../_shared/topology.py refresh` after structural changes. Never hand-edit
snapshots. **Topics nest along the hub tree**: a sub-hub bullet in a hub's
子卡與閱讀順序 that is another topic's anchor makes that topic a `sub_topics`
child — the parent's `status`/`sort` runs the whole subtree (labelled per
sub-topic); the child key still works standalone.

## CLI

```bash
cd ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/research-cards}/skills/overview
python3 sync_overview.py <topic> status   # coverage diff → MISSING papers
python3 sync_overview.py <topic> sort     # re-sort own cards by arxiv ID
```

## Common workflow (per topic; details in topics/<topic>.md)

1. **Coverage diff** — `status`. A paper is covered if linked in the global
   comparison graph (any comparison card); nothing missing + no re-sort → stop.
   Papers marked `[elsewhere]` are covered ONLY outside this topic's own cards
   (subtree-wide for nesting topics) — informational, not missing: judge each
   by the topic doc's 分工約定 (deliberate delegation, e.g. LLM-ASR → spoken
   (D)) vs a genuine facet opportunity worth an own-angle section (then follow
   the duplication rule in step 2).
2. **Route & author** (Claude, by hand) — pick the destination act card by the
   topic doc's routing rules; read the paper card (lean: 快速摘要 + intro);
   write the house-style L3 section — heading 「Name（機構，年份）」 + card
   mention + **hung-yi-lee-style bold bullets**（貢獻/架構/核心差異; why-first,
   English terms kept, ~3 bullets — size budgets are tight）+ hr, inserted
   before 關鍵設計維度對比. Cross-card duplication rule: a paper may appear in
   multiple cards by facet; if a card's 導讀/歸納 mentions or compares it, that
   card needs a full facet section cross-ref'd to the main-facet card.
3. **Tables** — add the dimension-table row (per-topic DIM_COLS), append the
   short name to the matching paradigm cell, extend fitting synthesis bullets.
4. **MATCH** — sort keys auto-derive from section mentions' arxiv property at
   the next `topology.py refresh`; only non-arxiv papers or new short-name
   variants need an ALIAS entry in `../_shared/topology.py`.
5. **Sort** — `python3 sync_overview.py <topic> sort`, then re-run `status`.
6. **導讀 refresh** — re-run the card's 導讀 via the `overview-daodu` skill
   (idempotent replace) so the narrative covers the new papers.
7. **Graph bookkeeping** — `python3 ../overview-graph/scripts/audit_graph.py`;
   if the change was structural (new card / split / re-home), follow the
   `overview-graph` skill first (it ends with `topology.py refresh`).

## Programmatic authoring API

```python
import sync_overview as O
S = O.load("spoken")     # topic-bound namespace — same S.* API as before
md5, doc = S.read_card(S.OVERVIEW_CARD_B)
sec = S.section("NewModel（機構，年份）", "<paper-card-uuid>",
                [("貢獻", "…"), ("架構", "…"), ("核心差異", "…")])
# insert before 關鍵設計維度對比, add S.dim_row(...), then save via S.save_card
```

Each topic module re-exports its documented constants (`OVERVIEW_CARD*`,
`DIM_COLS`, …) and helpers (`section/bullet/dim_row/table/read_card/save_card/
node_text/arxiv_key/classify/enumerate_task_cards/sort_overview`). Topic
extras: `spoken` keeps `build`/`_gen_match` (lm_match.py); `duplex` keeps its
classify/sort_bench hooks (`topics/duplex/hooks.py`) — its benchmark card is
narrative, never run engine sort on it directly.

## Size budget

Heptabase caps card content at ~100K chars (+~20% for node ids on save). Keep
sections to 3 bullets; if a save fails on the limit, the topic needs a card
split — that is a STRUCTURAL change: switch to the `overview-graph` skill.

Related: `overview-daodu` (導讀), `overview-graph` (hierarchy/edges/re-splits,
`topology.py refresh`), `scholar-inbox-clip` (routes new papers here via
`OVERVIEW_TASKS` — values map to the topic keys above).
