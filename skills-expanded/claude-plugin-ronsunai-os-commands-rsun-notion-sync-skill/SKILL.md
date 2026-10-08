---
name: rsun-notion-sync
description: 把 TRACKER 戰略 / 規格 / 報告 markdown 文件同步到 Notion「容晟科技」頁面下作子頁。當用戶說「同步到 Notion」「寫進 Notion」「鏡像到 Notion」「Notion 雙寫」「sync to Notion」「把這份 md 推上 Notion」時觸發。自動推導標題、轉換 blocks（含表格 / code / 引用 / inline 格式）、處理 100 block 上限。
user-invocable: true
allowed-tools: "Bash(python3 *) Bash(ls *) Bash(cat *) Read"
---

# 容晟戰略文件 → Notion 同步 SOP

## 用途

維持「TRACKER 為 source of truth + Notion 為人類查閱鏡像」雙寫架構。
TRACKER 主檔（git 控管、brain 索引）+ Notion 鏡像（行動裝置、視覺化）。

## 前置條件（已建好，無需重做）

- ✅ Notion Integration: **RONSUNAI** (Internal, workspace = Lai's Notion)
- ✅ Token 存於 `~/.claude/.env`（變數 `NOTION_TOKEN`）
- ✅ Notion MCP user-scope 已連線（fallback 用）
- ✅ 同步腳本: `~/Projects/TRACKER/scripts/sync-to-notion.py`
- ✅ 預設 parent page: 容晟科技 `752e23e4-dd33-4ccc-b4bc-b08c364036ad`

## 執行步驟

### Step 1：確認來源 markdown

詢問或從 context 確認：
- markdown 檔案路徑（通常在 `TRACKER/knowledge/nodes/rsun/strategy/` 下）
- 子頁標題（可從第一個 H1 自動推導，或讓用戶指定）
- 是否要放在「容晟科技」下（預設）或其他 page

如果用戶沒指定，**直接用預設**（容晟科技 page + H1 自動推導），不要反覆問。

### Step 2：執行同步

```bash
cd ~/Projects/TRACKER
python3 scripts/sync-to-notion.py <md_path>

# 或自訂標題
python3 scripts/sync-to-notion.py <md_path> --title "我的子頁"

# 或換 parent
python3 scripts/sync-to-notion.py <md_path> --parent <page_id_no_hyphen_or_with_hyphen>
```

預期輸出：
```
[1/3] Markdown → Notion blocks
      N top-level blocks
[2/3] Creating child page『...』 under 752e23e4-...
      child page id: ...
[3/3] Appending blocks (batched)
  appended N/N

✅ Done. URL: https://www.notion.so/...
```

### Step 3：更新 TRACKER index（讓 brain 知道有 Notion 鏡像）

在 `TRACKER/knowledge/nodes/rsun/index.md` 的「戰略文件 2026」或對應區塊，
為該文件加註「**Notion 鏡像：** ✅ {URL}」。

如果文件不在 `rsun/strategy/` 下，找對應的 `nodes/.../index.md`。

### Step 4：（選配）刷新 brain graph

如果這份文件是新建（不是覆寫舊內容）：

```bash
cd ~/Projects/TRACKER
./scripts/nightly.sh --no-deploy
```

這會：scan-assets → validate → build-knowledge → embed → 但不部署。
跑完 brain 就能在 retrieval 時找到這份新文件。

### Step 5：回報

給用戶以下資訊：
- ✅ Notion URL（複製即可開）
- ✅ TRACKER 主檔路徑
- ✅ index.md 是否已更新

## 例外處理

### 教育帳號 / 學校 workspace 限制

Notion 教育帳號（如 `@學校.edu.tw`）通常無法建 Internal Integration（學校 admin 鎖死）。
解法：用個人帳號 workspace（Lai's Notion 就是個人 workspace，已驗證可用）。

### Mermaid 圖渲染

Notion 原生支援 mermaid，但腳本上傳時會標成 `plain text`。
告知用戶：寫入後可手動到該 code block 把語言切成 `Mermaid`。

### 100 blocks 上限

腳本已用 `batch=90` 處理，自動分批 PATCH。如果有 nested children（如 list item 含 code block），
個別 block 內的 `children` 也會算入 100 上限 — 真遇到失敗會輸出 `/tmp/notion_failed_chunk_*.json` 供 debug。

### Token 失效

若 `~/.claude/.env` 的 `NOTION_TOKEN` 失效，到 https://www.notion.so/my-integrations 找 RONSUNAI → Show → Copy → 更新 `~/.claude/.env`。

## 進階：別的 parent page

若要寫到「容晟科技」以外的頁面：
1. 先讓用戶把目標 page 加 connections → RONSUNAI
2. 取得該 page 的 ID（從 URL 末段抓 32 字元）
3. 加 `--parent <id>` 參數

## 相關文件

- 腳本: `~/Projects/TRACKER/scripts/sync-to-notion.py`
- 知識節點: `~/Projects/TRACKER/knowledge/nodes/tools/notion-sync.md`
- 雙寫策略記憶: `~/.claude/projects/-Users-ezonelai-Projects-ronsunai-web/memory/project_rsun_tracker_notion_sync.md`
