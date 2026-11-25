---
name: rsun-cleanup
description: 容晟「策研 Brain」清理介面。當用戶說「清理」「cleanup」「整理檔案」「重複檔案」「孤兒節點」「inbox」時使用。逐筆 review knowledge/cleanup-inbox.md 內的偵測結果，互動式套用或忽略。
user-invocable: true
allowed-tools: "Read Edit Bash(python3 scripts/cleanup/*) Bash(git *) Bash(mv *) Bash(cp *) Bash(rm *) AskUserQuestion"
---

# 容晟科技「策研 Brain」清理流程

每天 nightly 會跑 `scripts/cleanup/detect-*.py`，產出
`knowledge/cleanup-inbox.md` ＋ `knowledge/cleanup-inbox.json`。
這個 skill 負責「人機 review 迴圈」。

## 參數

`$ARGUMENTS` — 選填。
- 沒給 → 列出 inbox 全部 section，問用戶要先看哪個
- `dup-embeddings` / `dup-files` / `link-suggestions` → 直接跳到該 section
- `--auto-green` → 一次套用所有 🟢 安全自動項，跳過 🟡

## 執行步驟

### Step 1：載入 inbox 狀態

```bash
cd ~/Projects/TRACKER
[ -f knowledge/cleanup-inbox.json ] && cat knowledge/cleanup-inbox.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('## sections:')
for k, sec in d.get('sections', {}).items():
    print(f'  • {sec[\"color\"]} {k} — {sec[\"title\"]} ({len(sec[\"items\"])} items)')
print('## recent applied:', len(d.get('applied', [])))
"
```

如果 inbox 空白 → 跑一次 detector 重生：
```bash
python3 scripts/cleanup/detect-dup-embeddings.py
python3 scripts/cleanup/detect-duplicate-files.py
```

### Step 2：依顏色處理

#### 🟢 GREEN — 安全自動套用

對每個 🟢 section，問用戶 1 次「要套用嗎？」，是 → 跑對應 applier。

| Section key | Applier |
|-------------|---------|
| `dup-embeddings` | `python3 scripts/cleanup/apply-dedupe-embeddings.py` |
| `link-suggestions` | `python3 scripts/cleanup/apply-link-suggestions.py` |

#### 🟡 YELLOW — 逐筆人工確認

例如 `dup-files`（疑似重複檔案）：
逐組 list 出 paths，用 `AskUserQuestion` 問：

> 「Apex_Gold_估價單 — 找到 3 份疑似同一檔，要怎麼處理？」
> A. 保留最新 PDF，其餘 mv 到 _舊版/
> B. 保留所有不動
> C. 全刪只留 PDF
> D. 跳過下一組

按答案執行 mv / rm，每筆獨立 `git commit`。

#### 🔴 RED — 只報告，不處理

純列出，不問動作。讓用戶自己評估。

### Step 3：收尾

```bash
# 重跑 detector 確認 inbox 已清乾淨
python3 scripts/cleanup/detect-dup-embeddings.py
python3 scripts/cleanup/detect-duplicate-files.py

# 如果套了任何東西，重建知識庫
python3 scripts/build-knowledge.py
```

回報：「本次處理 N 筆 · X 個 commit · inbox 剩 M 筆未決」

## Risk gradient（不要違反）

- **絕對不可**：刪 source 檔（Documents / Drive 內的 PDF / docx）— 只能 `mv` 到 `_舊版/`
- **絕對不可**：刪 citation node（knowledge/nodes/**/*.md）— 只能標 deprecated
- **絕對不可**：未經 commit 就改超過 3 個檔案
- 套用前一定要先 git status 確認 clean tree

## 範例對話

```
用戶：清理一下
Claude:
  📋 Cleanup Inbox（2026-04-23 09:00）
  🟢 dup-embeddings — 67 個重複 keys（建議：自動 dedupe）
  🟢 link-suggestions — 5 條高信心連結（建議：自動套）
  🟡 dup-files — 12 組疑似重複檔（需逐筆 review）

  先處理 🟢 兩件嗎？
用戶：好
Claude: [跑 apply-dedupe + apply-link-suggestions]
  ✅ commit a1b2c3d / d4e5f67
  接著 🟡 dup-files 第 1/12 組...
```
