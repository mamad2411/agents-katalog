---
name: rsun-session-end
description: Session 結束標準收尾流程。當用戶說「session 結束」「收尾」「今天做完了」「更新 NEXT_SESSION」時使用。依序完成：更新 NEXT_SESSION.md → commit docs → 更新 TRACKER → 同步 GitHub Issues → RS-TRACKER。
user-invocable: true
allowed-tools: "Bash(git *) Bash(zsh *) Bash(npx *) Read Write Edit Glob Grep"
---

# Session 收尾標準流程（Phase D）

依照容晟科技 AI_START.md 的 Phase D 流程執行。

## 參數

`$ARGUMENTS` — 選填。指定本次 session 完成了什麼（如「auth cookie fix + 7 tests」）。若未提供，從 git log 自動推導。

## 執行步驟

### D1：更新當前專案 NEXT_SESSION.md

1. 讀取 `docs/NEXT_SESSION.md`
2. 把本 session 完成的項目：
   - `[ ]` → `[x]`（已完成）
   - 在「✅ 本 Session 完成」區塊新增條目
3. 把下次待辦整理到「🔴 下次優先」
4. 更新文件頭的「最後更新」日期為今天

### D2：Commit docs

```bash
git add docs/NEXT_SESSION.md
git commit -m "docs: session 收尾 — <一行摘要>\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

只 add `docs/NEXT_SESSION.md`，不要 `git add -A`。

### D3：更新 TRACKER

1. 讀取 `/Users/ezonelai/Projects/TRACKER/index.html`
2. 找到對應專案的 `AI_UPDATE` 標記區塊
3. 更新完成項目和待辦狀態
4. 在 TRACKER 目錄執行：
   ```bash
   cd ~/Projects/TRACKER
   git add index.html
   git commit -m "tracker: <專案> session 收尾" --trailer "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
   npx wrangler pages deploy . --project-name rsun-tracker --commit-dirty=true --commit-message="tracker: session sync"
   ```

### D4：同步 GitHub Issues → RS-TRACKER

把 NEXT_SESSION.md 更新後剩餘的 `[ ]` 待辦自動建為 GitHub Issues 並加入 RS-TRACKER Project #2：

```bash
zsh ~/Projects/scripts/pm-issue.sh
```

- 已存在的 Issue 自動略過（不重複建立）
- 新 Issue 自動加入 [RS-TRACKER](https://github.com/users/EZoneLai/projects/2)
- 若 pm-issue.sh 找不到當前 repo，輸出提示但不中斷

### D5：最終確認

輸出摘要：
```
✅ NEXT_SESSION.md 已更新（X 項完成，Y 項待辦）
✅ docs commit：<hash>
✅ TRACKER 已更新並部署 → rsun-tracker.pages.dev
✅ GitHub Issues 同步：新建 N 個，略過 M 個（已存在）
⏳ 待 push（確認後執行）：git push origin main
```

## 注意事項

- **不要自動 push 到 GitHub**，commit 完說「要 push 嗎？」等用戶確認
- 不要 `git add -A` 或 `git add .`，只 add 指定檔案
- 如果不確定本 session 完成了什麼，先 `git log --oneline -10` 看 commit 記錄再寫
- D4 只對有 NEXT_SESSION.md 且在 pm-issue.sh 清單內的 repo 生效
