---
name: diagnose
description: 有紀律的 Bug 診斷循環：建立回饋循環 → 重現 → 假設 → 檢測 → 修復 → 清理。說「幫我 debug」「這壞了」「報錯了」「性能退步」時觸發。
---

# Diagnose — 有紀律的診斷

先讀 CONTEXT.md 了解專案語言。

## Phase 1 — 建立回饋循環

**這就是整個 skill 的核心。** 為 bug 建立一個快速、確定性、Agent 可執行的 pass/fail 信號。有它就找得到原因；沒有，看再多程式碼也沒用。

投入不成比例的努力在這裡。**積極。創意。拒絕放棄。**

方法順序：
1. 失敗的測試 (unit/integration/e2e)
2. curl / HTTP script
3. CLI 調用 + diff snapshot
4. 無頭瀏覽器 (Playwright/Puppeteer)
5. 回放已捕獲的 trace
6. 一次性 harness (最小系統子集)
7. Fuzz loop (1000 次隨機輸入)
8. Bisection harness (git bisect run)
9. Differential loop (新舊版本對比輸出)
10. HITL bash script (最後手段)

有了 loop，問自己：能不能更快？訊號能不能更清晰？能不能更確定性？

**沒有 loop 就別繼續。**

## Phase 2 — 重現

跑 loop。確認：
- [ ] 失敗模式是**用戶描述的**那個，不是碰巧在附近的另一個 bug
- [ ] 多次運行可重現
- [ ] 已捕獲確切症狀

## Phase 3 — 假設

在測試前生成 **3-5 個排序假設**。每個必須可證偽：

> 「如果 <X> 是原因，那麼 <改變 Y> 會讓 bug 消失 / <改變 Z> 會讓它惡化。」

**先給用戶看排序清單再測試。**

## Phase 4 — 檢測

每次只改一個變數。優先：debugger/REPL > 針對性 log > 不要「log 所有東西再 grep」。

所有 debug log 用獨立前綴標記，如 `[DEBUG-a4f2]`。清理時一個 grep 搞定。

## Phase 5 — 修復 + 回歸測試

**先寫測試再修復** — 但前提是有正確的 seam。沒有正確 seam 本身就是發現 — 記下來，交給 `/improve-codebase-architecture`。

## Phase 6 — 清理 + 事後分析

- [ ] 原始 bug 不再重現
- [ ] 回歸測試通過
- [ ] 所有 debug 標記清除
- [ ] 一次性原型刪除
- [ ] 正確假設寫入 commit message

問：**什麼能防止這個 bug 再次發生？**
