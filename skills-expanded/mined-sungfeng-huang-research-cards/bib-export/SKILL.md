---
name: bib-export
description: "Export official BibTeX for all papers a Heptabase/Obsidian card links to — read the anchor card's card-links, resolve each linked paper card's arxiv ID property, and fetch entries from official sources only (Semantic Scholar / arxiv.org/bibtex / ACL Anthology .bib / OpenReview). Never fabricates an entry: unresolved papers become TODO comments. Use when the user asks to 匯出 BibTeX / 產生 .bib / export references / citations for an overview card, a project card, or a set of paper ids."
---

# bib-export

Turn a curated card into a `.bib` file. The overview cards and project cards
already ARE hand-vetted reference lists (every linked paper card carries an
`arxiv ID` property) — this skill closes the knowledge-base → paper-writing
gap by fetching the **official** BibTeX for each linked paper.

## Agent（claude / codex）

兩個 agent 皆可駕駛——純 CLI script，無 MCP 依賴。

## Backend

`heptabase`/`both`：`<card>` 傳卡片 UUID。`obsidian`：傳 vault 卡 id
（`Folder/Name`）；mentions 從 wikilinks 重建、`arxiv ID` 讀 frontmatter
`arxiv_id`。路由由 config `backend` 自動決定。注意：vault 是部分鏡像——
未同步的卡（如 blog 卡）在 vault 端是 Heptabase URL 而非 wikilink，obsidian
模式收不到；要完整清單（含 no-arxiv-ID 的 TODO 列表）用 heptabase 模式跑。

## Usage

```bash
cd "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/research-cards}/skills/bib-export"
python3 bib_export.py <card-id>                  # anchor 卡的直接 card-links
python3 bib_export.py <hub-card-id> --depth 2    # hub → 子 overview 卡 → 論文
python3 bib_export.py --ids 2606.12345,aclanthology:2026.eacl-short.18
python3 bib_export.py <card-id> -o refs.bib      # 指定輸出（'-' = stdout）
```

Default output: `<anchor-title>.bib` in the current directory.

## Fetch chain（絕不捏造）

| id form | chain |
|---|---|
| `2606.12345` (arxiv) | Semantic Scholar `citationStyles`（有正式 venue 就拿到出版版）→ `arxiv.org/bibtex/<id>`（官方） |
| `aclanthology:<id>` | 官方 `aclanthology.org/<id>.bib` → S2 `ACL:<id>` |
| `openreview:<id>` | OpenReview API v2→v1 `content._bibtex` → S2 title match |
| `alphaxiv:<slug>` | S2 title match，**僅在 normalized title 完全相等時採用** |

Every entry keeps its upstream citation key and is annotated
`% <card title> [source]`. Anything unresolvable is emitted as
`% TODO (unresolved): …` — **never invent fields by hand to fill one in**;
tell the user to resolve those manually instead.

## Workflow

1. Run the script on the card the user names (project card, overview card, or
   `--ids`). For a topic hub, use `--depth 2` so it descends through the
   sub-overview cards to the papers.
2. Report: resolved/total, the UNRESOLVED list with reasons, and where the
   `.bib` was written.
3. If the user wants entries for cards that have no `arxiv ID` property
   (blogs, hand-made notes), point them at the property gap — do NOT
   hand-write bib entries for them.

## Notes

- Anonymous Semantic Scholar traffic is rate-limited; the script sleeps 1s
  between papers and retries on 429. Big hubs (50+ papers) take ~1-2 min.
- `--depth 2` descends only **overview cards** (identified by their graph
  `Level` property / frontmatter `level`); any non-overview card without an
  `arxiv ID` is always reported as TODO, never silently expanded or dropped.
- Status lines (`resolved n/m`, `UNRESOLVED: …`) go to **stderr**, so
  `bib_export.py <card> -o - > refs.bib` yields a clean `.bib`.
- Dedup: same paper linked from multiple sub-cards is fetched once (mention
  walk de-duplicates); colliding citation keys for *different* papers get a
  numeric suffix.
- Pairs with `project-card-merge` (paper-grade project cards → 參考 section)
  and the `overview` family (comparison cards = curated bibliographies).
