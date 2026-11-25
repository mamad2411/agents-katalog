---
name: ito-commit
description: 掃描 git 工作區所有變更，智慧分組後依序 commit 並展示計畫待確認。適用於使用者說「commit」、「提交變更」、「幫忙 commit」。支援 fast mode（非 lock file 變更合為單一 commit）。不適用於需要手動控制 staging 或執行 push 的情境。
---

# ito-commit

## 概覽

掃描工作區所有未提交變更，透過目錄結構與語意分析自動分組，展示計畫後依序執行 commit。支援 `/ito-commit fast` 將所有變更合為單一 commit。

## 使用時機

- 使用者說「commit」、「幫我 commit」、「提交變更」
- 使用者輸入 `/ito-commit` 或 `/ito-commit fast`
- 需要將工作區變更整理成有意義的 commit 歷史

**不應使用的情況：** 需要手動控制 staging 的情境、需要執行 git push 的任務、需要 rebase 或 cherry-pick 的情境。

## 核心流程

### 步驟 1：判斷模式

讀取 args：
- 含 `fast` → fast mode，進入步驟 2，步驟 6 合為單一群組
- 無參數 → smart mode，完整流程

### 步驟 2：掃描工作區

執行以下指令取得變更清單：

```bash
git status --short
git diff -U1 --no-color
git diff --cached -U1 --no-color
```

去除 diff metadata header（`diff --git`、`index`、`---`、`+++` 開頭的行），保留變更行與相鄰 context。總行數超過 500 時截斷。

若工作區無任何變更，顯示「工作區無變更」後結束。

若 `git status --short` 輸出含 `UU`、`AA`、`DD`、`AU`、`UA` 等 merge conflict 標記，顯示「工作區有未解衝突，請先執行 git mergetool 或手動解決後再 commit」，列出衝突檔名後結束。

### 步驟 3：Lock file 前處理

偵測 lock file 模式：`package-lock.json`、`yarn.lock`、`pnpm-lock.yaml`、`*.lock`、`Cargo.lock`、`Gemfile.lock`。

命中時：跳過其 diff 內容，從主要變更清單移除，建立獨立群組，commit message 固定為 `chore: update lock file`。

### 步驟 4：敏感檔案偵測

掃描變更檔名，偵測高風險模式：`.env`、`.env.*`、`*.pem`、`*.key`、`*.p12`、`*secret*`、`*credential*`、`*password*`。

命中時顯示警告並列出檔名，等使用者確認後繼續。

### 步驟 5：語言偵測

```bash
git log --oneline -5
```

分析最近 5 筆 commit message 語言：
- 全為中文 → 沿用中文
- 全為英文 → 沿用英文
- 有混合 → 詢問：「最近的 commit 有中英文混用，這次要用哪種語言？」

### 步驟 6：分組

**smart mode：** 依目錄結構與語意分析分組。判斷原則：
- 同功能模組（相同目錄或緊密相關的跨目錄變更）歸為一組
- 測試檔與對應的業務邏輯視為同組
- 設定檔、文件、工具設定可獨立成組

分組數超過 5 時顯示：「分組較多（N 個 commit），是否改用 fast mode？」，等使用者選擇：若選 fast mode，合為單一群組後繼續步驟 7；若繼續，維持原分組進入步驟 7。

**fast mode：** 所有非 lock file 變更合為單一群組。

### 步驟 7：生成 Commit Message

對每個群組，依步驟 5 偵測的語言生成 Conventional Commits 格式 message：
- 從 `feat`、`fix`、`chore`、`refactor`、`test`、`docs`、`style`、`ci` 中選最適型別
- 有明確模組邊界時加入 scope（`feat(auth): ...`），否則省略
- subject 長度控制在 72 字元以內

### 步驟 8：展示計畫並確認

展示所有 commit 計畫：

```
將建立 N 個 commit：

[1] feat(auth): add token refresh logic
    - src/auth/token.ts
    - src/auth/refresh.ts

[2] test(auth): add token refresh tests
    - src/auth/token.test.ts

[3] chore: update lock file
    - package-lock.json

確認執行？(y/n)
```

收到 `y` 後進入步驟 9。收到 `n` 或修改指示時，等待使用者說明修改意見，依指示調整計畫後重新展示。

### 步驟 9：依序執行 Commit

對每個群組依序執行：

```bash
git add <group files>
git commit -m "<message>"
```

全部完成後顯示摘要（列出各 commit 的 hash 與 message），不執行 git push。

若某個 commit 因 pre-commit hook 失敗，顯示 hook 錯誤內容，停止後續 commit，提示使用者修復後重新執行。

## 常見合理化藉口

| 合理化藉口 | 實際情況 |
|---|---|
| 「使用者說 y 了，可以直接執行不用等」 | 計畫展示後才收 y，收到 y 前不能執行任何 git add 或 git commit |
| 「lock file 只有一個，放進主要分組不影響」 | lock file 固定獨立成 chore commit，不混入業務邏輯群組 |
| 「語言看起來是英文，直接用不用問」 | 有中英混合時必須詢問，不猜測使用者偏好 |
| 「fast mode 不用展示計畫，直接 commit 更快」 | Fast mode 仍需展示計畫等確認，只是群組只有一個 |

## 警訊

- 步驟 9 在收到 `y` 前執行
- 敏感檔案未顯示警告直接納入分組
- lock file 混入非 chore 的 commit 群組
- commit message 超過 72 字元
- fast mode 跳過計畫展示直接執行

## 驗證

- [ ] 所有計畫中的 commit 已建立（`git log --oneline -N` 可查看）
- [ ] Lock file 變更在獨立的 chore commit 中
- [ ] 無敏感檔案在未警告的情況下被 commit
- [ ] 無執行 git push

## 錯誤處理

- 若非 git 工作區（`git status` 失敗），顯示錯誤後結束。
- 若 pre-commit hook 失敗，顯示 hook 輸出，停止後續 commit，提示使用者修復後重新執行。
