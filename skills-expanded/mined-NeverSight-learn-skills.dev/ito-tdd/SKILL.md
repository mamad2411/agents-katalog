---
name: ito-tdd
description: 以測試驅動開發引導功能實作與 bug 修復。使用者明確提到 TDD、red-green-refactor 或 test-first 時使用。不適用於純設定變更、文件更新或無行為影響的靜態修改。
---

# ito-tdd

## 概覽

以 red-green-refactor 循環實作與 bug 修復。透過公開介面驗證行為，確保測試在重構後依然有效。

## 使用時機

- 使用者明確提到 TDD、red-green-refactor 或 test-first
- 要求以「先寫測試」方式實作功能
- 需要修復 bug 並確保有測試保護

**不應使用的情況：** 純設定變更、文件更新或無行為影響的靜態內容修改。

## 哲學

**核心原則**：測試應驗證行為，而非實作細節。程式碼可以全面改寫，測試不應因此失效。

**好測試**是整合式：透過公開 API 測真實執行路徑，描述*系統做什麼*而非*怎麼做*。這類測試能存活於重構，因為它不在乎內部結構。

**壞測試**耦合實作：mock 內部協作者、測試私有方法、或透過外部手段驗證。警訊：重構後測試失敗，但行為沒變。

詳細範例與 mocking 守則，讀取 `references/tests.md`。

## 反模式：水平切片

**不要先寫所有測試，再寫所有實作。** 這是「水平切片」。批量寫出的測試在測想像中的行為，不是真實的行為。

```
錯誤（水平）：
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

正確（垂直）：
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  ...
```

## 核心流程

以下為功能實作流程。收到 bug report 時，改見「Bug Fix 流程」。

### 步驟 1：規劃

寫任何程式碼之前：

- 確認需要哪些介面變更
- 確認要測哪些行為，排定優先級
- 識別 deep module 機會，讀取 `references/design.md`
- 列出要測試的行為，不是實作步驟
- 取得使用者核准

**無法測試所有事情。** 聚焦關鍵路徑和複雜邏輯，不是每一個邊界條件。

### 步驟 2：Tracer Bullet

寫一個測試確認系統的一件事：

```
RED:   為第一個行為寫測試 → 測試失敗
GREEN: 寫最少程式碼通過測試 → 測試通過
```

寫測試時，讀取 `references/tests.md` 了解實務守則。

這是 tracer bullet，確認路徑端到端可行。

### 步驟 3：漸進循環

針對每個剩餘行為重複：

```
RED:   寫下一個測試 → 失敗
GREEN: 最少程式碼通過 → 通過
```

守則：一次一個測試，只寫足以通過當前測試的程式碼，不預先猜測未來的測試，聚焦於可觀察的行為。

### 步驟 4：重構

所有測試通過後，尋找重構候選：

- **重複邏輯** → 提取函式或 class
- **過長方法** → 拆成私有 helper（測試保留在公開介面上）
- **Shallow module** → 合併或深化
- **Feature envy** → 把邏輯移到資料所在之處
- **Primitive obsession** → 引入 value object
- **既有程式碼** 被新程式碼揭示出的問題

**RED 時絕不重構。** 先到達 GREEN，每次重構後立即執行測試。

## Bug Fix 流程

### Prove-It Pattern

收到 bug report 時，不要直接修 bug，先寫重現測試：

```
收到 Bug report
       ↓
寫一個能展示 bug 的測試
       ↓
測試 FAILS（確認 bug 存在）
       ↓
實作 fix
       ↓
測試 PASSES（證明 fix 有效）
       ↓
跑完整測試套件（確認無 regression）
```

```typescript
// Bug：「完成任務時沒有更新 completedAt」

// 步驟 1：寫重現測試（應該 FAIL）
it('完成任務時設定 completedAt', async () => {
  const task = await taskService.create({ title: 'Test' });
  const completed = await taskService.complete(task.id);

  expect(completed.status).toBe('completed');
  expect(completed.completedAt).toBeInstanceOf(Date); // 此行失敗 → bug 確認
});

// 步驟 2：修 bug，步驟 3：測試通過 → regression 防護到位
```

## 每輪檢查清單

每完成一個 RED→GREEN 循環後確認：

- [ ] 測試描述行為，而非實作
- [ ] 測試只使用公開介面
- [ ] 測試能存活內部重構
- [ ] 程式碼是通過當前測試的最小實作
- [ ] 沒有加入推測性的功能

## 常見合理化藉口

| 合理化藉口 | 實際情況 |
|---|---|
| 「先把功能寫完再補測試」 | 事後補寫的測試測實作而非行為，而且通常根本不會補 |
| 「這太簡單了不需要測試」 | 簡單的程式碼會變複雜，測試記錄了預期行為 |
| 「一次把所有 test 寫完比較快」 | 批量寫出的測試測想像的行為，不是真實的行為 |
| 「修完 bug 再補重現測試就好」 | 先有重現測試才能證明 bug 存在，也才能防止 regression |
| 「重構不需要跑測試這麼頻繁」 | 重構時每一步都要跑，才能知道是哪一步壞掉的 |

## 警訊

- 寫程式碼前沒有對應的失敗測試
- 一次寫多個測試再一起實作（水平切片）
- 測試在第一次執行就通過
- 重構時測試失敗但行為沒有改變（測試耦合了實作）
- 修 bug 時沒有先寫重現測試

## 驗證

- [ ] 每個新行為都有對應測試
- [ ] 所有測試通過
- [ ] bug fix 包含一個在 fix 之前失敗的重現測試
- [ ] 測試名稱描述被驗證的行為
- [ ] 沒有跳過或停用的測試

## 延伸參考

- `references/tests.md`：好測試與壞測試的對比範例，mocking 守則，DAMP、AAA、One Assertion Per Concept 等寫測試實務
- `references/design.md`：為 testability 設計介面，deep module 模式
