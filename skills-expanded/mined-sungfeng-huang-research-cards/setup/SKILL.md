---
name: setup
description: "Interactive config wizard for research-cards: create, inspect, or adjust ~/.config/research-cards/config.json by interviewing the user against config.example.json's inline docs. Use when the user asks to set up / configure / initialize research-cards, 建立 config、設定 research-cards、調整設定、初始化、幫我設定、check my config, enable a backend (backends list: local/heptabase/hackmd), change the output language, or turn features on/off."
---

# setup — config 精靈

把 `config.example.json` 的行內文件（`$comment` 們）變成一場**短訪談**：
建立、體檢、或調整 `~/.config/research-cards/config.json`。原則：

- **最小 config 優先**——純 .md 資料夾模式只需要 `obsidian.vault` 一個
  必填（`backends` 缺省即 `["local"]`）。不要把 example 整份抄給使用者。
- **絕不臆造 id**——heptabase 模式的 workspace_id／tag_id／property UUID
  一律由指令查出或使用者提供（`heptabase tag list`／`tag properties`）。
- **改前先讀**——調整模式永遠先讀現有 config，只動使用者要動的鍵；
  寫回後跑驗證器。

## Step 0 — 體檢（每次都先跑）

```bash
python3 <此 skill 目錄>/check_config.py          # 人讀報告
python3 <此 skill 目錄>/check_config.py --json    # 給 agent 解析
# heptabase 模式想順便測 app 連線：加 --probe
```

輸出告訴你：config 在哪（含 `RESEARCH_CARDS_CONFIG` env 覆蓋與 legacy
`heptabase-cards` 路徑）、載不載得起來（載入失敗會指名缺哪個 key）、
backend 的可及性（vault 目錄／heptabase CLI）、以及 **upgrade_hints**——
example 有記載、此 config 尚未設定的鍵（新功能的加購清單，如
`profile.language`、`obsidian.journal`）。

## 模式 A — 建立（config 不存在）

訪談順序（一次問一組，別轟炸）：

1. **用途**：讀論文管線（study）？研究專案卡（project）？都要？
   → `features.{study, project}`（預設皆開，都要就不用寫）。
2. **backends**：預設推薦**純 .md 資料夾**（不需要任何筆記 app；就是
   `backends: ["local"]`，可省略不寫；list 首位＝正本，舊單值
   `backend` 鍵仍相容）。使用者有 Heptabase 才問
   `heptabase`／`both`——並提醒 macOS＋desktop app＋CLI ≥ 0.4.0 的需求。
3. **資料夾**：`obsidian.vault` 路徑（iCloud 要提醒 Full Disk Access）＋
   `folders`（預設 `{"papers": "Papers", "overviews": "Overviews"}`）。
4. **profile**：`reader`（讀者身分，流進每張卡的「為什麼該讀」）、
   `field`（主領域）、`language`（產出語言；不設＝跟 Claude Code 的
   language 設定，再預設繁體中文）。
5. **agent**：跑無人值守腳本的 CLI（`claude`｜`codex`）；互動用途照預設。
6. 只寫使用者實際回答的鍵——寫入前把 draft 亮給使用者核可，寫入後跑
   Step 0 驗證。

Heptabase／both 額外流程（照 example 的 `heptabase` 段 `$comment`）：

```bash
heptabase tag list                       # 找 workspace 的 tag id
heptabase tag properties <tagId>        # 各 tag 的 property UUID
```

按使用者的 tag 命名收集 `workspace_id`、`collections`（papers／overviews／
projects 的 tag_id）、`props`（Tasks／Source Type／arxiv／Level）。查不到
的值**留空並明講**——heptabase 路徑的指令會在缺 key 時指名報錯，這是
設計（絕不猜 UUID）。

## 模式 B — 調整（config 已存在）

1. Step 0 體檢；把 `upgrade_hints` 攤給使用者（「example 新增了這些設定，
   要開嗎？」）。
2. 使用者點名要改的東西 → 讀 example 對應段的 `$comment` 給出選項與
   語義（例：`profile.language` 的 fallback 鏈、`overflow_spill` 預設
   已開、`email.hf_min_upvotes` 的選文語義）。
3. 只改點名的鍵；改完重跑驗證器並回報 diff。

常見調整的對照：

| 使用者說 | 動哪裡 |
|---|---|
| 「換輸出語言」 | `profile.language`（空＝跟 Claude Code 設定） |
| 「接上 Heptabase」 | `backends` → `["heptabase"]`／`["heptabase", "local"]`＋`heptabase` 段（模式 A 的 id 收集） |
| 「開信件剪報」 | `email.{account, mailbox}`（Mail.app 帳號＋專用資料夾；排程另見 README） |
| 「關掉 project 方向」 | `features.project: false` |
| 「裝了 hung-yi-lee」 | `integrations.hung_yi_lee.skill_path` |
| 「journal 換資料夾」 | `obsidian.journal.folder`（vault 相對；逃逸會被拒） |
| 「接上 HackMD／發佈到 HackMD」 | `hackmd.collections`（key → folder_id，`hackmd-cli folders` 查）＋permissions；token 走 `hackmd-cli login`／`HMD_API_ACCESS_TOKEN`，**絕不進 config**——詳見 hackmd-sync skill |

## 邊界

- **cluster（hb bridge）上不要建 heptabase config**：bridge 沒有
  `tag properties`，id 收集做不到；純 .md 模式可以（只要 vault 路徑），
  或提醒使用者回 Mac 設定。
- 這個 skill 只動 `config.json`——topics 目錄（`~/.config/research-cards/
  topics/`）的建立屬 overview 的 quickstart 流程，不在此處代辦。
- Agent（claude／codex）皆可執行；無 MCP 依賴。
