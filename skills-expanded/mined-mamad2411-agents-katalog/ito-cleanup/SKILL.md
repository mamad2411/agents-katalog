---
name: ito-cleanup
description: 清理 git 變更或單一檔案中的程式碼，移除 debug log、未使用 import、commented-out code、冗餘邏輯、命名問題與結構複雜度，行為完全保留。不適用於修改邏輯、新增功能、大幅重構或半成品 code。僅限手動呼叫。
---

# ito-cleanup

## 概覽

掃描 git 變更或指定檔案，自動清理常見問題：debug log、未使用 import、commented-out code、冗餘邏輯、命名問題與結構複雜度。完成後展示 diff，測試通過才算結束。

## 使用時機

**僅限使用者手動呼叫 `/ito-cleanup`，agent 不自行判斷是否執行。**

- 完成功能實作後，整理該檔案 code 品質
- 發現 code 有巢狀過深、泛用命名、殘留 debug log 等問題需修正

**不應使用的情況：** 需要修改邏輯或新增功能的任務、大幅重構架構、尚未完成實作的半成品 code。

## 核心流程

### 步驟 1：判斷模式與範圍

1. 若帶有路徑參數（`/ito-cleanup <檔案路徑>`），進入**單檔模式**。
2. 若無參數，進入 **git diff 模式**，判斷目前有變更的檔案範圍。
3. 估算總改動量。若超過 500 行，停止並提示：「變更範圍超過 500 行，建議用 `/ito-cleanup <檔案路徑>` 指定特定檔案。」並列出有變更的檔案清單供使用者選擇。
4. 先讀取 `CLAUDE.md` 與鄰近 code，確認專案慣例後再繼續。

### 步驟 2：逐檔清理

依清理項目依序處理每個目標檔案：

**結構複雜度**
- 深層巢狀（3 層以上）→ 提取為 guard clause 或輔助函式
- 過長函式（50 行以上）→ 拆分為職責單一的函式
- 巢狀三元運算 → 改為 if/else 或查找表
- boolean 參數 flag → 改為 options 物件或獨立函式
- 重複的條件判斷 → 提取為命名 predicate 函式

**命名與可讀性**
- 泛用命名（`data`、`result`、`temp`、`val`）→ 改為描述內容的具體名稱
- 縮寫（`usr`、`cfg`、`btn`）→ 展開為完整單字（`id`、`url`、`api` 等慣例縮寫保留）
- 誤導性命名（函式名稱與行為不符）→ 修正命名
- what 註解（解釋「做什麼」）→ 刪除
- why 註解（解釋「為什麼」）→ 保留

**冗餘**
- 重複邏輯（同一段 5 行以上邏輯出現多處）→ 提取為共用函式
- 死碼（不可達分支、未使用變數）→ 理解用途後移除（遵循 Chesterton's Fence 原則）
- 無意義的 wrapper 函式 → 內聯呼叫

**擴充清理項目**
- 移除未使用 import（不排序，排序交給 linter）
- 清除 debug log：
  - JS/TS：`console.log`、`console.error`、`console.warn`、`console.debug`、`console.info`、`debugger`
  - Ruby/Rails：`puts`、`p`、`pp`、`binding.pry`、`byebug`
  - `Rails.logger.*`：判斷是否為 debug 殘留（有明確業務意義的 logging 保留）
- 清除 commented-out code：有上下文說明的保留（例如 `# disabled until #123 fixed`），孤立的 commented-out block 移除
- 多餘 type assertion → 移除

**Test 檔案例外：** 只清除 debug log 和未使用 import，不動結構與命名。

**TODO/FIXME：** 掃描過程中記錄全部項目，不刪除，步驟 4 統一列出。

### 步驟 3：執行測試

1. 偵測專案測試指令（`package.json` scripts、`Rakefile`、`Makefile` 等）。
2. 若有測試，執行測試套件：
   - 通過 → 繼續步驟 4
   - 失敗 → revert 所有變更，回報失敗的測試名稱與對應清理項目，結束
3. 若無測試套件，詢問使用者：「偵測不到測試環境，是否繼續？（繼續代表風險由你承擔）」
   - 使用者確認 → 繼續步驟 4
   - 使用者拒絕 → revert 所有變更，結束

### 步驟 4：展示結果

1. 展示所有變更的 diff。
2. 若有 TODO/FIXME，在 diff 之後獨立展示：
   ```
   === TODO/FIXME 清單 ===
   src/components/Auth.tsx:42: TODO: 處理 token 過期的 edge case
   app/models/user.rb:18: FIXME: 此處的 N+1 查詢需要優化
   ```
3. 展示完畢後，清理流程結束。

## 五大原則

### 1. 行為完全保留

不改變 code 的輸入、輸出、副作用與 error 行為。每次修改前自問：

```
→ 所有輸入的輸出結果相同嗎？
→ error 行為保留了嗎？
→ 副作用與執行順序不變嗎？
→ 所有現有測試不需修改就能通過嗎？
```

若無法確定某項簡化是否保留行為，不要做。

### 2. 遵循專案慣例

清理是讓 code 更符合 codebase 的一致性，不是套用個人偏好。清理前：

1. 讀取 `CLAUDE.md` 與專案慣例文件
2. 觀察鄰近 code 如何處理相同的模式
3. 對齊專案的 import 順序、函式宣告風格、命名慣例、error handling 模式

破壞一致性的清理不是清理，是製造雜訊。

### 3. 清晰優於聰明

明確的 code 勝過精簡但需要停頓解讀的 code。

```typescript
// 不清楚：巢狀三元徒增理解負擔
const label = isNew ? '新增' : isUpdated ? '更新' : isArchived ? '封存' : '啟用';

// 清楚：一眼就能對應狀態
function getStatusLabel(item: Item): string {
  if (item.isNew) return '新增';
  if (item.isUpdated) return '更新';
  if (item.isArchived) return '封存';
  return '啟用';
}
```

### 4. 維持平衡

清理有過度簡化的失敗模式，避免以下情況：

- 過度內聯：移除了一個有意義名稱的輔助函式，讓呼叫端更難讀
- 合併不相關邏輯：兩個簡單函式合成一個複雜函式，不是更簡單
- 移除「不必要」的抽象：有些抽象為了可測試性或延伸性而存在
- 以行數為目標：行數少不代表更清晰

### 5. 範圍限於有變更的 code

預設只清理有變更的部分，不做不相關的順手整理。不相關的清理讓 diff 產生噪音，也增加意外引入 regression 的風險。

## 常見合理化藉口

| 合理化藉口 | 實際情況 |
|---|---|
| 「這段 commented-out code 可能之後用得到」 | git history 保存紀錄，孤立的 commented-out code 是噪音 |
| 「`console.log` 只有一行，留著沒差」 | debug log 是常見雜訊，統一清除是核心價值 |
| 「test 檔也應該完整清理」 | test code 命名常故意冗長，只做安全清理 |
| 「diff 超過 500 行但我判斷可以處理」 | 閾值存在是為了保護使用者，超過就請指定範圍 |
| 「測試沒有覆蓋這個部分，不用跑」 | 測試套件能抓到意外的 side effect，沒有完整覆蓋也要跑 |

## 警訊

- 清理後需要修改 test 才能通過（代表行為被改變）
- 清理後 code 比原本更難理解
- 依個人偏好重新命名，而非遵循專案慣例
- 移除了 error handling
- 一次批次大量修改而未逐步測試
- 清理了不在任務範圍內的 code

## 錯誤處理

- 若測試失敗，revert 所有變更，回報具體的失敗測試名稱與對應清理項目。
- 若 diff 超過 500 行，停止執行並列出有變更的檔案清單，建議使用者選擇特定檔案重新執行。
- 若無法判斷某段 commented-out code 是否為刻意保留，保留它並在結尾標記為待確認項目。

## 驗證

- [ ] 所有測試通過（無需修改任何 test）
- [ ] 建置成功，無新的警告
- [ ] Linter 通過
- [ ] diff 乾淨，無不相關的變更
- [ ] 遵循專案慣例（已讀 CLAUDE.md）
- [ ] 未移除或削弱 error handling
- [ ] TODO/FIXME 清單已列出（若有）

