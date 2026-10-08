---
name: rsun-find
description: 容晟「策研 Brain」搜尋短路徑。當用戶用顯式語法說「find 報價」「rsun-find client=apex 簡報」「找 .pdf 在 Drive」時使用。直接呼叫 rsun-files MCP 的 smart_search / find_file，不繞 LLM 推理。
user-invocable: true
allowed-tools: "mcp__rsun-files__smart_search mcp__rsun-files__find_file mcp__rsun-files__semantic_search mcp__rsun-files__files_for_unit mcp__rsun-files__list_in_folder mcp__rsun-files__recent_files mcp__rsun-files__file_stats mcp__rsun-files__get_file"
---

# /rsun-find — 顯式搜尋「策研 Brain」

用 DSL-style 短語法，直接打 MCP，不用自然語言。

## 參數

`$ARGUMENTS` — 必填。支援以下語法（key=value 任意組合）：

| 語法 | 範例 | 對應 MCP tool |
|------|------|--------------|
| `關鍵字` | `/rsun-find 報價` | smart_search（預設） |
| `關鍵字 ext=.pdf` | `/rsun-find 合約 ext=.docx` | smart_search + ext 過濾 |
| `關鍵字 root=Drive` | `/rsun-find 簡報 root=容晟科技` | smart_search + root 過濾 |
| `關鍵字 mode=keyword` | `/rsun-find 估價 mode=keyword` | find_file |
| `關鍵字 mode=semantic` | `/rsun-find 怎麼定價 mode=semantic` | semantic_search |
| `unit=CASE-X` | `/rsun-find unit=CASE-RSUN-CRM` | files_for_unit |
| `folder=X` | `/rsun-find folder=CRM定價專案` | list_in_folder |
| `recent days=N` | `/rsun-find recent days=3` | recent_files |
| `recent ext=.pdf` | `/rsun-find recent ext=.pdf days=7` | recent_files + ext |
| `stats` | `/rsun-find stats` | file_stats |
| `get FILE-xxx` | `/rsun-find get FILE-3229e5572a` | get_file |

## 解析 → 派發

1. 切 args by space
2. 提取 `key=value` pairs
3. 判斷模式：
   - 開頭是 `unit=` → files_for_unit
   - 開頭是 `folder=` → list_in_folder
   - 開頭是 `recent` → recent_files
   - 開頭是 `stats` → file_stats
   - 開頭是 `get` → get_file
   - 其他 → smart_search（除非 mode=keyword/semantic 顯式指定）
4. 剩餘的非 key=value tokens 拼成 query

## 輸出格式

精簡表格：

```
🔍 smart_search "報價 ext=.pdf" → 8 結果

#  分數    檔名                                     資料夾                     來源
1  0.018   RSun_定價方案_v3.pdf                     CRM定價專案/                kw+sem(0.71)
2  0.016   AIFA_估價單_v2.pdf                       客戶/AIFA/                  kw+sem(0.68)
3  0.011   PLX_報價v1.pdf                           客戶/PLX/                   kw
...

📎 連到 citation: CASE-RSUN-CRM (1) · CASE-AIFA (1)
```

如果命中 < 3 → 順便提示：
> 「結果偏少。試試：(a) `/rsun-find 報價 mode=semantic` (b) `/rsun-find 報價 include_archive=true`」

## 不做什麼

- ❌ 不下載檔案內容（用 get_file 看 preview 就好）
- ❌ 不自動寫筆記 / 連結（要寫的話用 `/rsun-cleanup` 或 `/rsun-link`）
- ❌ 沒命中時不假裝 — 直接回報「0 結果，建議改用 X」

## 範例

```
/rsun-find 報價
→ smart_search(query="報價")

/rsun-find 簡報 ext=.pptx root=Drive
→ smart_search(query="簡報", ext=".pptx", root="Drive")

/rsun-find unit=CASE-RSUN-CRM
→ files_for_unit(unit_id="CASE-RSUN-CRM")

/rsun-find recent days=3 ext=.pdf
→ recent_files(days=3, ext=".pdf")

/rsun-find folder=08_共通資源
→ list_in_folder(folder_substring="08_共通資源")

/rsun-find stats
→ file_stats()
```
