---
name: sprint-close
description: Merge sprint branch to base branch, tag release, and clean up branches
allowed-tools: Read, Glob, Bash
---

# Sprint 結案

老闆 + PM 確認所有 Gate 通過後執行，將 sprint branch merge 回 base branch。

## 使用方式
```
/sprint-close <sprint-number>
```

## 參數
- `$0`: Sprint 編號（如 `1`）

## 執行步驟

1. **確認所有任務已完成**：
   使用 Glob tool 搜尋 `.tasks/sprint-$0/*.md`，用 Read tool 逐一讀取，確認所有任務 `| 狀態 |` 欄位均為 `done`。
   若有任一非 `done` → 列出未完成任務，停止執行。

2. **讀取 base branch**：
   使用 Glob tool 搜尋 `proposal/sprint$0-dev-plan.md`，用 Read tool 讀取，找到 `| Base Branch |` 欄位取得 base branch 名稱（如 `main` 或 `master`）。

3. **切換並 merge**：
   ```bash
   git checkout {base-branch}
   git merge --no-ff sprint-$0 -m "release: sprint-$0 結案"
   ```

4. **建立 Tag**：
   ```bash
   git tag sprint-$0-release
   ```

5. **清理已 merge 的 task branches**：
   ```bash
   git branch --merged {base-branch} | grep "task/s$0-" | xargs git branch -d
   ```
   > 只刪除已完整 merge 進 base branch 的 task branches，未 merge 的保留並輸出警告。

6. **刪除 sprint branch**：
   ```bash
   git branch -d sprint-$0
   ```

7. **輸出結案摘要**：
```
✅ Sprint $0 結案完成

Base Branch：{base-branch}
Tag：sprint-$0-release
清理 branches：{已刪除的 branch 列表，或「無」}

git log --oneline -5 顯示最近 commit：
{輸出}
```
