---
name: myconfig
description: 列出或安裝本倉庫（agent-prompt-rules-system）的 Claude Code 場景配置包：prd-design、frontend-dev、backend-dev、dev-ops 整包或其中單一維度。會話中只做預演；寫入改給一條命令由使用者執行。全域工具、個人使用者層級與 Codex 配置也只給命令。
when_to_use: 使用者問「這個倉庫能配什麼」「有哪些場景配置」，或說「把 backend-dev 裝到 <目錄>」「給這個專案裝前端場景配置」「更新場景配置」時；「裝 gstack」「同步個人 skills」「裝 Codex 規則」也適用。修改本機 settings.json 個別欄位用 update-config；推薦專案該用哪些 Claude Code 功能用 claude-automation-recommender。
argument-hint: "[場景或配置] [目標專案目錄]"
allowed-tools: Bash(sh "${CLAUDE_SKILL_DIR}/scripts/catalog" || printf 'REPO=UNREADABLE\n')
---

# 場景配置清單與安裝

## 硬性規則

- 技能自己只執行只讀命令與預演（`-d`／`--dry-run`）；所有寫入都給出完整命令，由使用者執行。原因（2026-10-29 實測）：沙箱即使在目前目錄也禁止寫入 `.claude/settings.json`、`.claude/skills/`、`.claude/hooks/`，整包無法在會話中裝完；全域與使用者層級路徑更不可寫。
- `-F` 只在使用者選擇時加入命令。
- 只呼叫倉庫 `scripts/` 下的腳本；不自行複製檔案、不改倉庫範本；不對倉庫自身做專案級安裝。唯一例外：`commands.md`「跨場景陷阱」指明要從倉庫補的檔案（如單裝 backend-dev settings 時的 `go-fmt.sh`），可把 `cp` 併入交付給使用者的命令，並說明原因；技能自己仍不執行。
- 不用 `-m ask`。使用者貼回失敗輸出時，原樣引用錯誤行與退出碼；只建議重跑失敗的單元，不建議整段重跑。

## 目前倉庫的配置

!`sh "${CLAUDE_SKILL_DIR}/scripts/catalog" || printf 'REPO=UNREADABLE\n'`

若上方沒有展開清單（例如在不支援注入的客戶端），先執行本技能目錄下的 `scripts/catalog`。第一行 `REPO=` 即倉庫路徑，以下稱 `<R>`。`REPO=NOT_FOUND` 時停止，轉述清單中的設定方法。`REPO=UNREADABLE`（前面通常有 `Operation not permitted`）表示沙箱擋住讀取本技能目錄或倉庫：請使用者在 `~/.claude/settings.json` 的 `sandbox.filesystem.allowRead` 加入倉庫路徑與 `~/.claude/skills/myconfig`，不自行修改。

四個場景：

| 場景 | 適用 | 整包內容重點 |
|---|---|---|
| `prd-design` | 需求說明書、PRD、線框圖、基礎原型 | PM 類 agents、pm-skills 支援包、playground、document-skills |
| `frontend-dev` | UI 實作、前端互動、對接後端 API | 前端 agents、瀏覽器驗證外掛 |
| `backend-dev` | 系統與資料庫設計、Go 後端開發 | Go 分層 rules、7 個設計類 skill、資料庫 MCP、codegraph、OpenSpec |
| `dev-ops` | CI/CD、上線、可觀測性 | 部署 permissions、middleware-ops skill、GlitchTip MCP |

`fullstack-dev` 只有 settings 範本，沒有整包。命令、參數與輸出判讀見 `references/commands.md`，安裝前讀一次。

## 判斷使用者要什麼

| 使用者說 | 做法 |
|---|---|
| 只叫 `/myconfig`、「能配什麼」 | 列表：轉述上方清單與四場景表，附 3 條可直接說的示例（例如「把 backend-dev 裝到這裡」「只裝 frontend-dev 的 settings」「更新這個專案的 dev-ops 配置」）。不執行任何命令 |
| 指明場景與目標 | 走「安裝流程」 |
| 只有目標，沒說場景 | 依「場景推斷」給推薦，用 AskUserQuestion 讓使用者選；線索不明確時直接列四個場景 |
| 只有場景，沒說目標 | 目標預設為目前目錄；目前目錄就是 `<R>` 時，請使用者給路徑 |
| 一次多個單元（「settings 加 agents」） | 合併為一份預演、一次確認；交付時依 `commands.md` 的順序用 `&&` 串成一條命令（任一步失敗即停） |
| 「更新」 | 整包加 `-F`；結果有 `[STALE]` 時再提示單獨更新支援包 |
| 全域工具、個人使用者層級、Codex | 不預演，從 `commands.md` 的「全域與使用者層級」表取命令與影響說明 |

## 安裝流程

1. **前置**：`REPO=` 不是路徑，或預演出現 `Operation not permitted` 時，照「目前倉庫的配置」下方的說明請使用者調整 allowRead 後停止。
2. **解析**：目標轉為絕對路徑 `<P>`，確認存在；依 `commands.md` 組出命令。保持目前目錄不變，以 `sh "<R>/scripts/…"` 呼叫。
3. **只讀預檢**：
   - `<P>` 是否 git 倉庫、有無未提交改動；
   - `.gitignore` 是否含 `*.bak.*`、`*.backup-*`、`.claude-project-backup-*`、`settings.local*.json`；
   - 哪些目標檔已存在。
4. **預演**：整包與支援包跑 `-d`／`--dry-run`；其他單元自行列出「源 → 目標」。輸出壓縮成：將新增 N 個檔案；已存在 M 個（列出，預設跳過）；將安裝的支援包及其專案外副作用。
5. **一次確認**（AskUserQuestion，確認的是要給出哪一條命令）：
   - 選項：「安裝（推薦）」「加 -F 覆蓋已存在的檔案（先備份）」「取消」。沒有已存在檔案時省略 `-F` 選項。
   - 單裝 settings 且目標已有同名檔時，選項改為「overwrite：先備份，範本 permissions 生效」與「merge：只合併外掛與 skillOverrides，permissions 不寫入」。整包遇到已存在的 `settings.json` 只有跳過或 `-F`（先備份再整檔覆蓋，使用者自己加的 permissions 或外掛要從備份手動合回）。
   - 問題文字寫明不會復原的副作用（全域 npm、外掛下載）。
   - 參數中已含「確認」或 `-y` 時視為選了推薦項，直接交付命令。AskUserQuestion 不可用時，改用文字提問後停止。
6. **交付命令**：沿用預演的同一組參數，去掉 `-d`／`--dry-run`，給出一條可直接複製的命令（多單元用 `&&` 串接，依固定順序）。
   - 只含配置複製的命令，建議在提示列輸入 `! <命令>`，輸出會回到會話；出現 `Operation not permitted` 就改到一般終端機執行，再貼回輸出。含支援包的命令直接建議到終端機執行（會跑 `npm`、`git clone`，可能要幾分鐘）。
   - 從 `!` 改到終端機重跑時，先前已複製的檔案會顯示 `[MANUAL]`，內容與倉庫相同；回報時說明這是上一次部分寫入的結果。
7. **回報**（拿到執行輸出後）：
   - 依 `commands.md`「輸出判讀」計數標籤，分「配置複製」「支援包」兩段寫。數字只引用腳本摘要（如 `copied=`、`manual=`）與標籤行數，不自行按類別（rules、skills 等）計數；要說明內容時只列類別名稱。
   - exit 0 但有 `[MANUAL]` 時，明說未更動的檔案。
   - 列出全部備份路徑。
   - 讀 `<R>/dot_claude_projects/.claude-<FLAG>/README.md` 的 `## 手动安装与恢复`、`## MCP 服务器`（標題為原文；後者只有 backend-dev、dev-ops 有）兩節，列出使用者還要手動做的事：外掛安裝命令、環境變數、`codegraph init` 等。
   - 再加上 `commands.md`「跨場景陷阱」中適用的條目。

## 場景推斷

只讀目標根目錄，給出推薦，不自動決定：

| 線索 | 推薦 |
|---|---|
| `go.mod`、`migrations/`、`*.sql`；`package.json` 含 express、fastify、@nestjs、prisma、mongoose | backend-dev |
| `package.json` 含 react、vue、svelte、vite | frontend-dev |
| 前後端都有，或用 next、nuxt | 說明沒有 fullstack 整包；推薦 backend-dev 或 frontend-dev 整包，再加 `fullstack-dev` settings |
| 只有 Dockerfile、compose、`.github/workflows/` | dev-ops |
| 以文件為主、沒有程式碼 | prd-design |

## 回報範例

```
backend-dev → /path/to/api
配置複製：新增 48 個檔案；CLAUDE.md 已存在，未更動（可用 -F 覆蓋）
支援包：codegraph、OpenSpec 安裝成功
備份：無
接下來要手動做：
1. claude plugin install mongodb@claude-plugins-official --scope project（另 3 個見下）
2. 啟動前設定 MYSQL_HOST 等環境變數；只用唯讀帳號
3. 在專案中執行 codegraph init
```
