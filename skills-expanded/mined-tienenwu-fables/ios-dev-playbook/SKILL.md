---
name: ios-dev-playbook
description: Use when writing, refactoring, or debugging iOS app code (Swift, SwiftUI, Swift Concurrency, Xcode) — before adding a feature, choosing state ownership (@State / @Observable / @Environment), touching MainActor/actor/Sendable, preparing a TestFlight/App Store build, or when facing App Store review rejection, provisioning profile errors, missing dSYM / unsymbolicated crashes, data races, or continuation misuse.
---

> 🌐 [English version](https://github.com/tienenwu/fables/blob/main/en/ios/SKILL.md) · 繁體中文（正本 / canonical）

# iOS 開發判準手冊

## 核心原則

1. **模擬器綠燈不算數**：簽章、provisioning、release optimization、`assert` 失效、背景模式、記憶體壓力都只在實機/release 才真實——上架路徑的改動要用實機 + release 級驗證。
2. **狀態只有一個擁有者，資料只往下流、事件只往上傳**：View 是狀態的函式，`body` 必須便宜且無副作用。
3. **UI 狀態一律在 MainActor**：不是靠自覺 `DispatchQueue.main`，而是用 `@MainActor` 讓型別系統替你保證。
4. **continuation 必須 resume 恰好一次**：橋接舊 API 時，零次＝永久卡死，兩次＝crash——這是紅線不是風格。
5. **取消是協作式的**：`Task` 不會自動停，長工作要主動 `Task.checkCancellation()`；`.task` modifier 才自動綁生命週期。

## 開工分流

| 情境 | 路徑 | 先讀 |
|------|------|------|
| 新增畫面/功能 | 先定狀態擁有者與資料流，再寫 View | references/architecture-state.md |
| 該不該建 ViewModel、狀態放哪 | 先判 MV vs MVVM，別反射性套 MVVM | references/architecture-state.md §2 |
| 導航、深連結、回退堆疊 | 用狀態驅動 NavigationStack path | references/architecture-state.md §5 |
| async/await、Task、actor、資料競爭 | 查 scope 與 MainActor 標註層級 | references/concurrency.md |
| 橋接舊 completion handler / delegate | continuation resume 恰一次 | references/concurrency.md §6 |
| Swift 6 strict concurrency 報 Sendable 錯 | 別亂加 @unchecked，先看資料歸屬 | references/concurrency.md §4 |
| 出 TestFlight / App Store / 改簽章 | 逐條跑必查清單 | references/release-checklist.md |
| 模擬器正常、實機/上架才爆 | 先假設簽章/optimization/背景模式 | references/release-checklist.md |

## 紅線（絕對禁止）

- **禁止只用模擬器驗證後宣告上架相關改動完成**——簽章、entitlement、background mode、release optimization 在模擬器全不真實。
- **禁止讓 continuation resume 兩次或零次**——兩次直接 crash，零次永久掛起；每條路徑都要恰好一次。
- **禁止在 App Store purpose string（`NSCameraUsageDescription` 等）寫敷衍或空字串**——Apple 直接以 Guideline 5.1.1 拒；缺對應權限說明會 crash 或被拒。
- **禁止把 UI 狀態更新丟到非 MainActor**——資料競爭 + 畫面更新在背景執行緒是未定義行為；用 `@MainActor` 標註而非手動切 queue。
- **禁止在 `body` 內做網路/IO/寫狀態**——`body` 每幀可能重算多次，副作用會爆量重跑；用 `.task`/`.onChange` 或下放 model。
- **禁止把 reference type 放進 `@State`、或每次重建 `@ObservedObject`**——前者 SwiftUI 不追蹤變更，後者每次刷新丟失狀態。
- **禁止改測試斷言讓 CI 變綠**——連紅兩次是方向錯誤訊號，退回上一決策點。

## 失敗訊號（該回頭，不是重試）

| 徵兆 | 多半是 | 退回 |
|------|--------|------|
| 畫面資料改了但 UI 不更新 | 值放錯 property wrapper（reference 進 @State / 忘了 @Observable） | 狀態擁有權設計 |
| 到處補 `DispatchQueue.main.async` 才不閃退/不警告 | MainActor 標註層級錯，該標型別卻標零散呼叫 | concurrency §2 |
| `.task` 換 `Task {}` 又冒出洩漏/重複請求 | 生命週期沒綁 View，手寫 Task 不取消 | concurrency §1 |
| Sendable 警告用 `@unchecked` 一個個壓 | 可變狀態沒有清楚歸屬 | concurrency §4 |
| 模擬器正常、實機 Archive 才失敗 | 簽章/provisioning/optimization 差異 | release-checklist 決策樹 |
| 上架被拒改一句 purpose string 又被拒 | 敷衍字串或漏了其他 guideline | release-checklist 審核清單 |
| 線上 crash 全是 `0x...` 無符號 | dSYM 沒上傳 | release-checklist §dSYM |

## references 索引

- `references/architecture-state.md` — SwiftUI 狀態擁有權決策表、MV vs MVVM、單向資料流、body 成本、NavigationStack 建模。動架構或新功能前讀。
- `references/concurrency.md` — Task 生命週期、@MainActor 標註層級、actor、Sendable/Swift 6、取消、continuation 橋接。碰非同步就讀。
- `references/release-checklist.md` — 簽章/provisioning 決策樹、App Store 審核被拒高頻原因、dSYM、release-only 差異、TestFlight、versioning。出版前必讀。
- `references/test-scenarios.md` — 判準測驗集，驗證接手模型是否照走。不給執行中的模型讀。
