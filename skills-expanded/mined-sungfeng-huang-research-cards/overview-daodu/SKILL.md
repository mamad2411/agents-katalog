---
name: overview-daodu
description: "Add or refresh a Hung-Yi-Lee-style teaching 導讀 (narrative intro) at the top of a Heptabase comparison/overview card — weaving the papers the card lists into ONE evolution thread with a punchline, grounded ONLY in the card's own content. Idempotent: re-running updates the existing 導讀 in place instead of duplicating. Use when the user asks to add/update/refresh a 導讀 / 教學導讀 / 導言 / teaching intro on an overview card (Tokenizer/Codec, Spoken LM, Reasoning, Duplex S2S, Audio Understanding, …)."
---

# overview-daodu

## Agent（claude / codex）

兩個 agent 皆可駕駛（Codex 端：`research-cards@private-plugins` plugin 的 overview-daodu skill）。讀卡一律優先用
`heptabase note read <id>`（或 obsidian 模式直接讀 vault 檔案）——不要依賴
mcp get_object（僅 Claude 有）。

## Backend

`heptabase`/`both`：原路徑不變。`obsidian`：`--card` 傳 vault 卡 id（`Folder/Name`），
讀寫走 vault，導讀插入邏輯不變。

The unified `overview` skill's topics produce **structured but list-like** cards (paradigm tables, per-paper bullets, dimension tables). This skill adds the one thing those cards lack: a **teaching 導讀** at the very top that turns the pile of papers into a *story* — how the idea evolved, what problem each wave was answering — in the Hung-Yi Lee teaching voice.

Division of labour: **you (the model) write the 導讀 prose**; the bundled `insert_daodu.py` does the mechanical insert/replace into the card. This is a **Mac-only** flow (local Heptabase + `heptabase` CLI).

## When To Use

- User asks to add / 補 / 更新 / refresh a 導讀 / 導言 / 教學導讀 / teaching intro on an overview or comparison card.
- After the `overview` skill adds new papers to a topic (missing 補洞 or an [elsewhere] facet fill) and the 導讀 should be re-synced to reflect them.

## Procedure

1. **Get the card id.** If the user named a topic (e.g. "Tokenizer/Codec (I)"), resolve it to the card id (the unified `overview` skill's `topics/<key>/config.py` exports the `OVERVIEW_CARD*` ids; the Key IDs table in `overview/topics/<key>.md` lists them too). Confirm with the user if ambiguous.
2. **Read the card content** with the `mcp__heptabase-mcp__get_object` tool (objectType `card`). This is your ONLY source of facts.
3. **Write the 導讀** following the Teaching Contract below. Start it with a `## 導讀：…` heading and end it with a `---`.
4. **Insert it** by piping the markdown to the script:
   ```bash
   printf '%s' "$DAODU_MD" | python3 <skill>/insert_daodu.py --card <CARD_ID>
   # or: python3 <skill>/insert_daodu.py --card <CARD_ID> --md-file /path/to/daodu.md
   # preview first with --dry-run
   ```
   It backs up the original doc to `~/.cache/overview-daodu/<card_id>.<ts>.json`, then inserts the 導讀 before the card's first `##` section — or, if a `## 導讀…` section already exists, **replaces it in place**.
5. **Verify** by re-reading the card (`get_object`) and confirm the 導讀 is at the top and the rest of the card is untouched. Report the backup path.

## Teaching Contract

Apply the **[[hung-yi-lee]]** skill's teaching rules (read that skill for the full voice). The load-bearing ones here:

- **脈絡, not 流水帳 (Rule 1):** weave the papers into ONE thread where each wave answers the previous wave's limitation and the idea visibly *evolves*. Never walk the papers one-by-one — that's what the table below the 導讀 already does.
- **Problem → method genealogy (Rule 3):** each section starts from a problem ("怎麼辦呢？") and lets the method arrive as the rescue. Don't state finished methods.
- **One punchline (Rule 2):** find the single tension/axis the whole card turns on (e.g. a three-way trade-off the papers keep fighting) and open + close with it.
- **Deflation & oral voice:** 「其實就是 X 而已」, short sentences, 比如說 / 你會發現 / 怎麼辦呢, keep English terms (token, RVQ, codec, streaming…) but demystify them.
- **No negative verdict on any specific entity** (person/company/product) — critique ideas/methods/trade-offs only.

**Grounding (hard rule):** every paper name, mechanism, number, and the punchline must come from the card you read. Do NOT add papers, claims, or facts the card doesn't contain. If the punchline (e.g. a named trade-off) is stated by one of the cards, you may lean on it — that's grounded.

**Length:** a 導讀, not a lecture — roughly 5–8 short paragraphs. It orients the reader, then explicitly hands off to the tables ("底下的表格其實就是把這條線上每個取捨攤開…"). Bold only the skeleton sentences (the thread markers and the punchline), not everything.

## Idempotency & Safety

- Re-running **updates** the 導讀 (the script replaces the existing `## 導讀…` section up to the next `##`), so you can refresh it after papers are added without duplicating.
- Every run backs up the original card doc to `~/.cache/overview-daodu/<card_id>.<ts>.json`. To revert, use the script's restore mode (it reads the backup's doc and re-saves it with the card's *current* md5): `python3 <skill>/insert_daodu.py --card <CARD_ID> --restore <backup>`.
- Mac-only: needs the local `heptabase` CLI. This edits the live Heptabase card directly; it is **not** a private-config change, so nothing to commit/sync.

## Gold Reference

The 導讀 on the card configured at config `gold_cards.overview_daodu` is the reference for tone, length, and the "three-era + trade-off punchline" thread shape. (The overview cards form a hierarchy — root index → topic hubs → comparison cards, tag `study/overview`, `Level` property = tree depth; 導讀s live on the comparison cards.)
