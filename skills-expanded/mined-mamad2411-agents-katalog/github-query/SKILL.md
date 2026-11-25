---
name: github-query
description: 回答關於 GitHub repo / issue / PR 的問題，vault-first 查詢。當用戶提到某個 GitHub repo、問某個 repo 做什麼、問 issue / PR、或說「這個 repo」、「那個倉庫」、「query repo」、「查 github」時使用。優先讀 vault 裡已沉澱的 research-repos note，未命中才 fallback 到本地 clone 與 `gh` CLI，並在發現值得追蹤時建議用 `/vault-assistant:watch-repo` 沉澱進 vault。
allowed-tools: Bash(gh:*), Bash(git:*), Bash(ls:*), Bash(cat:*), Read, Glob, Grep
metadata:
  version: 1.0.0
---

# GitHub Query — Vault-first GitHub 查詢

回答 GitHub 相關問題時的查詢層。核心原則：**vault 裡已有的知識優先於線上查詢**——因為 vault note 是人工提煉過、為長期追蹤而寫的，比 README 首段或 `gh repo view` 的原始輸出更有價值。

## 兩個資料來源

1. **Vault research-repos**（knowledge base，優先）
   - Index: `Areas/development/research-repos/index.md`
   - Notes: `Areas/development/research-repos/<REPO>.md`
   - 由 `/vault-assistant:watch-repo` 建立，由 `/vault-assistant:repo-patrol` 維護新鮮度
   - 包含「這個 repo 是什麼」「整體架構」「Tracking focus」「Update log」等提煉後內容

2. **本地 clone + `gh` CLI**（fallback）
   - Local root: `~/workspaces/github/`
   - Flat index: `~/workspaces/github/AGENTS.md`（由 `watch-repo` 同步維護）
   - `gh` CLI 用於查 issues / PRs / code / 搜尋不在本地的 repo

## 工作流程

### Step 1: 解析用戶問的是哪個 repo

從用戶訊息抽出：
- 完整 URL `https://github.com/<owner>/<repo>`
- `owner/repo` 縮寫
- 單純的 repo 名（如「openab 那個 repo」）

若只有 bare name 且歧義，先查下一步的索引再決定是否需要問用戶。

### Step 2: Vault research-repos 命中檢查

```bash
# 先看 index
grep -i "<repo>" Areas/development/research-repos/index.md
```

若命中 → 直接讀 `Areas/development/research-repos/<REPO>.md`，用這份 note 回答用戶問題。這份 note 有：
- **這個 repo 是什麼** — 定位與目標用戶
- **整體架構 / 子專案** — 模組或 monorepo 結構
- **Tech Stack** — 語言與關鍵依賴
- **Tracking focus** — 值得留意的方向
- **Update log** — 最近 snapshot 與變化

回答時引述 note 內容，並用 wikilink `[[<REPO>]]` 指向該 note，讓用戶可以自己跳轉。

**若 note 的最後一次 Update log 超過兩週**，在回答結尾附一行：「這份 note 上次更新是 `<date>`，可能落後——要不要 `/vault-assistant:repo-patrol <REPO>` 刷新？」

### Step 3: 本地 clone fallback

Vault 未命中時，檢查本地 clone：

```bash
ls ~/workspaces/github/ | grep -i "<repo>"
cat ~/workspaces/github/AGENTS.md 2>/dev/null | grep -i "<repo>"
```

若本地有 clone：
- 直接 `Read ~/workspaces/github/<REPO>/README.md` 等檔案回答
- 需要時用 `git -C ~/workspaces/github/<REPO> log`、`git show` 等查歷史
- **重要**：這個 repo 沒在 vault research-repos 裡——代表是 clone 過但沒沉澱。在回答結尾附建議：「這個 repo 還沒進 research-repos monitoring list，要我跑 `/vault-assistant:watch-repo <REPO>` 把它沉澱進 vault 嗎？」

### Step 4: `gh` CLI 線上查

本地也沒有時，用 `gh` CLI。常用指令：

```bash
# 搜尋 repo
gh search repos <關鍵字> --limit 10

# 查 repo 詳情
gh repo view <owner>/<repo>

# Issues
gh issue list --repo <owner>/<repo> --state open --limit 20
gh issue view <number> --repo <owner>/<repo>
gh search issues <關鍵字> --repo <owner>/<repo>

# PRs
gh pr list --repo <owner>/<repo> --state open --limit 20
gh pr view <number> --repo <owner>/<repo>

# Code search
gh search code <關鍵字> --repo <owner>/<repo>
```

優先用 `gh`（會自動處理 auth）而非 `curl`。若 `gh auth status` 失敗，提醒用戶跑 `gh auth login`。

回答後的建議規則：
- **若這個 repo 值得長期追蹤**（用戶表達持續興趣、或問題看起來會一再出現）→ 建議 `/vault-assistant:watch-repo <owner>/<repo>`
- **若只是一次性查詢**（用戶只是要確認某個 fact）→ 不必建議沉澱，直接回答

判斷準則：一次性 lookup（像「它最新 release 是什麼」）不用沉澱，概念性理解（像「這個 repo 架構是什麼」「它跟 X 有什麼差別」）值得沉澱。

### Step 5: Issue / PR 類查詢的特別處理

用戶問的是 **某個 repo 的 issues / PRs** 而不是 repo 本身：

- 查用戶自己的 issue/PR 未指定 owner → 預設 `ricky1698`
- 大量 issue 整理（不只是查詢一兩個）→ 改建議 `/vault-assistant:gh-issues-to-doc`，那個 skill 專門做結構化轉檔
- 單純 daily activity 查詢 → 改建議 `/vault-assistant:gh-daily-log`

這個 skill 只負責**對話式的查詢回答**，不負責把結果寫進 vault——寫入有對應的專門 command。

## 回答格式

- 命中 vault note：用繁中回答，引述 note 章節，附 `[[<REPO>]]` wikilink
- 本地 clone：直接摘要 README / 原始檔案回答，附 local path
- `gh` CLI：簡短 bullet 列出關鍵事實，附原始 URL

永遠讓用戶知道答案來源（vault note / 本地 clone / gh 線上），這樣他們能判斷可信度與新鮮度。

## 不要做的事

- **不要自動 clone**——`watch-repo` 才負責 clone。這個 skill 只查詢，需要沉澱時建議用戶跑命令
- **不要寫 vault 檔案**——這個 skill 是 read-only，任何寫入都走專門的 command（`watch-repo` / `repo-patrol` / `gh-issues-to-doc`）
- **不要重複 `gh-daily-log` / `gh-contribution-report` / `gh-issues-to-doc` 的工作**——那些是報表產生，這個是互動查詢
