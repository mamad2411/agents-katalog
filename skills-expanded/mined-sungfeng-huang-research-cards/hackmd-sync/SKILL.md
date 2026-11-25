---
name: hackmd-sync
description: "Mirror research-cards collections to HackMD (the plugin's third note surface, aimed at sharing/publishing): incremental forward sync from the active backend (heptabase/obsidian/both) into HackMD folders with real note-to-note links, plus OPTIONAL level-2 write-back (config hackmd.write_back) — HackMD-side edits on owner-writable notes merge back into the vault paragraph-by-paragraph; shared-writable notes and two-sided edits stay conflicts. Use when the user asks to sync/publish cards to HackMD, 同步到 HackMD、把總覽卡發到 HackMD、鏡像到 hackmd、雙向同步 hackmd、check HackMD drift, or set up the hackmd section of the config."
---

# hackmd-sync — 把卡片庫鏡像到 HackMD

> **已併入 [note-sync]**：日常請用 `skills/note-sync/sync.py`（單一入口、全鏈編排＋衝突彙總；`--mode hackmd` 等價單跑本段）。本檔保留引擎語義的完整說明；引擎 `sync.py` 檔案原位不動。

第三個筆記介面，定位是**分享**：把選定的 collection（典型是 overviews）
發佈成 HackMD notes，互連卡變成真的 note-to-note 連結。語義
（與 heptabase-sync 引擎的演進史同款）：

- **前向增量**：本地 backend 為準；來源 markdown md5 沒變就跳過。
  `both` 時來源刻意取 **obsidian 側**（vault）而非 Heptabase——寫回落在
  純 .md，再由 heptabase 段的區塊級二級送回 Heptabase（星狀中樞
  的鏈，不重複造引擎）。
- **變更偵測**：HackMD 端的 `lastChangedAt` 在上次同步後動了 → 進入
  level 2 判定（下條）或報 conflict、**不覆蓋**。
- **Level 2 寫回（選配，config `hackmd.write_back: true`）**：HackMD 端
  的編輯寫回 vault。**信任邊界＝只寫回有效 `write_permission` 為 owner
  的 note**（HackMD 上只有你能編輯的）；開放編輯的 note 永遠只報衝突。
  兩邊都改＝真三方衝突不動。合併是**段落級**：沒動的段落保留 vault
  原文（降級成純文字的 mention 不會被固化），動過的段落連結逆向
  （HackMD 連結→wikilink）＋round-trip 驗證，會變形就**整卡凍結**報
  conflict。寫回需要 base 快照（前向時自動維護；升級後先跑一輪前向）。
- **連結改寫**：`[[wikilink]]`／card mention／Heptabase URL 的目標若也
  在鏡像集合裡 → 改成 `[標題](https://hackmd.io/<noteId>)`；不在 →
  退化成純文字標題。

## 前置

1. `npm install -g @hackmd/hackmd-cli`
2. Token（hackmd.io → Settings → API → Create API token）：
   `hackmd-cli login` 一次（存 `~/.hackmd/config.json`）或設
   `HMD_API_ACCESS_TOKEN` env——**token 絕不放 research-cards config**。
3. Config `hackmd` 段（`setup` skill 可帶你設；`hackmd-cli folders` 查
   folder id）：

   ```json
   "hackmd": {
     "collections": {
       "overviews": { "folder_id": "<folder-id>" },
       "projects":  { "folder_id": "<folder-id>",
                      "read_permission": "owner", "write_permission": "owner" },
       "progress":  { "folder_id": "<unassigned-logs-folder-id>",
                      "read_permission": "owner", "write_permission": "owner" }
     },
     "project_bundles": {
       "<canonical-entry-card-uuid>": {
         "folder_id": "<Projects/Project A folder-id>",
         "logs_folder_id": "<Projects/Project A/Logs folder-id>",
         "read_permission": "owner",
         "write_permission": "owner"
       }
     },
     "read_permission": "owner",
     "write_permission": "owner",
     "write_back": false
   }
   ```

   collection 條目內的 `read_permission`／`write_permission` 覆蓋全域——
   典型用法：全域開分享（signed_in／guest）但 projects 釘死私密。
   `project_bundles` 再以 entry UUID 覆蓋 projects/progress：entry 與續卡
   移入 `folder_id`、relation-linked log 移入 `logs_folder_id`，仍是原本
   同一張 HackMD note，**不建立副本**。要分享單一專案只把該 bundle 的
   `read_permission` 改成 `signed_in`（或明確要公開才用 `guest`）；
   `write_permission` 建議維持 `owner`。
   `write_back` 開 level 2（需 backend obsidian／both）。
   `book_index`＝書本目錄卡 id：該卡 render 自動轉 Book mode 形態
   （setext 標題、`/noteId` 相對連結、自動補書名 H1——與官方
   tutorials 書同款）；開書要在 HackMD 網頁 Share → Book mode 點一次。

## 日常

| 你說 | 指令 |
|---|---|
| 「同步到 HackMD」 | `python3 <此 skill 目錄>/sync.py` |
| 「先看會動哪些」 | `python3 <…>/sync.py --dry-run` |
| 「只同步這張卡」 | `python3 <…>/sync.py --card <id>` |
| 「HackMD 那邊有沒有被改過」 | `python3 <…>/sync.py verify` |

輸出 JSON：`created`／`updated`／`skipped`／`conflicts`（HackMD 端
編輯過的卡）／`errors`。Agent 跑完把 conflicts 攤給使用者。

## 邊界與注意

- **State**：`~/.config/research-cards/hackmd-state.json`（cardId ↔
  noteId／md5／lastChangedAt）。刪掉某卡的條目＝下次強制重建/覆蓋。
- **方言**：顏色 `<span style>`／`<u>` HackMD 原生渲染；toggle 的
  `- ⏵ ` 字首是純文字 bullet（可讀、不可折疊）；圖片 data-URL 過大時
  HackMD 可能拒收——大圖卡先觀察 `errors`。
- **權限**：出廠預設 `owner/owner`＝私密（只有你）；要分享才改 `signed_in`／`guest`——`guest` 等於公開發佈，想清楚再開；
  對外連結是 `https://hackmd.io/<noteId>`。讀權限是**宣告式**的：每輪
  sync 把遠端漂移校正回 config 值（連 conflict 卡也校——內容凍結、
  權限照管）。
- **刪除**：本地刪卡不會刪 HackMD note（刪除不傳播，兩個方向都是）；
  `verify` 的 `missing_remote` 反向列出 HackMD 端被刪的 note。
- **限流**：HackMD 基礎設施有短視窗 429（付費方案也有）——內建指數退避
  （60/120/240s）；連續多卡重試仍失敗＝長視窗，本輪提前收尾（報告
  `aborted` 欄），重跑即續傳。大量首發分幾輪磨完是正常的。
- Agent（claude／codex）皆可；無 MCP 依賴。cluster 亦可跑（hackmd-cli
  走網路、不依賴 Mac）——但來源 backend 是 heptabase 時要 Mac（CLI 讀卡）。
