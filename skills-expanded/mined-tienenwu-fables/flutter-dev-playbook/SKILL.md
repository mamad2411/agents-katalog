---
name: flutter-dev-playbook
description: Use when writing, refactoring, or debugging Flutter/Dart app code (widgets, Riverpod, Bloc, setState, platform channel, pubspec) — before adding a screen, choosing state management, measuring performance, adding a plugin, or preparing a release build. Also when facing jank/dropped frames, rebuild storms, release mode crash (tree shaking / AOT-only), MissingPluginException, or "works in debug but crashes in release".
---

> 🌐 [English version](https://github.com/tienenwu/fables/blob/main/en/flutter/SKILL.md) · 繁體中文（正本 / canonical）

# Flutter 開發判準手冊

## 核心原則

1. **Debug(JIT) 的綠燈不算數**：release/profile 是 AOT 編譯，行為與 debug 不同——`assert` 被剝除、tree shaking 移掉只被反射/字串引用的符號、timing 更快會抖出 race。凡 release 相關的改動與**所有效能量測**都必須用 profile/release 驗，見 references/platform-build.md。
2. **`build()` 是純函式，每 frame 都可能被呼叫**：禁止在 build 內做 IO、網路、`setState`、建 controller、寫檔——副作用會每幀重跑。
3. **狀態先分 ephemeral 與 app state**：只有這個 widget 自己用、丟了無所謂 → `setState`；跨 widget 共享或要存活 → provider/Bloc。錯層＝rebuild 風暴或狀態遺失。
4. **rebuild 範圍要主動收窄**：讀 state 的位置越低越好；用 `select` / `Consumer` 下沉到真正用到值的葉節點，別讓整棵子樹跟著重建。
5. **兩平台是兩份工程**：權限宣告、簽章、build mode、plugin 原生實作在 Android 與 iOS 各一份，release 各跑一次才算驗過。

## 開工分流

| 情境 | 路徑 | 先讀 |
|------|------|------|
| 新增畫面/功能 | 先定狀態擁有者與分層，再寫 widget | references/state-architecture.md |
| 選 setState / Riverpod / Bloc | 走選型決策樹，別憑喜好 | references/state-architecture.md §1 |
| UI 卡頓 / 掉 frame / rebuild 太多 | 先 profile，不要先改 code | references/widgets-performance.md §jank |
| 抽 widget、const、ListView | 判準在此，別亂抽 helper method | references/widgets-performance.md |
| 要碰原生（相機/藍牙/系統 API） | 先問能否用現成 plugin | references/platform-build.md §channel |
| debug 正常、release 才爆 | 先假設 tree shaking / AOT / 環境差異 | references/platform-build.md §模式差異 |
| 出 release / 上架 | 逐條跑必查清單，兩平台各跑 | references/release-checklist.md |
| 加依賴套件 | 先查 pub.dev 分數與維護狀態 | references/release-checklist.md §套件 |

## 紅線（絕對禁止）

- **禁止在 debug/JIT 下量效能就下結論**——debug 有 JIT warmup 與額外檢查，數字比 release 慢數倍且失真；效能只在 profile mode 量。
- **禁止在 `build()` 裡做 IO / 網路 / 建立 controller / `setState`**——每次 rebuild 重跑，造成迴圈、洩漏、掉 frame。
- **禁止只用 debug build 就宣告 release 相關改動完成**——tree shaking、obfuscation、`assert` 剝除、簽章都只在 release 生效，debug 零證據力。
- **禁止用 `GlobalKey` 只為了「拿到某個 widget」**——重量級、破壞 rebuild、跨樹移動風險；先問是不是狀態設計錯了。
- **禁止 helper method 回傳 Widget 卻假設它有獨立效能邊界**——它不是 element、無法 const、父層重建就整段重跑，見 references/widgets-performance.md §抽 widget。
- **禁止 catch 後只 print 不改 state**——使用者看到永遠轉圈；錯誤要進 `AsyncValue.error` 或 error state。
- **禁止改測試斷言讓它變綠**——連紅兩次是方向錯誤訊號，退回上一決策點。

## 失敗訊號（該回頭，不是重試）

| 徵兆 | 多半是 | 退回 |
|------|--------|------|
| 加了一堆 `const`、rebuild 還是卡 | state 讀太高、整棵樹重建 | state 讀取位置設計（§收窄） |
| 到處補 `if (mounted)` 才不 crash | 在錯的地方持有 State/context | 生命週期與狀態擁有權 |
| release 才 crash，改一處又爆下一處 | tree shaking 掃掉反射/字串引用符號 | 序列化與 build mode 策略 |
| 效能「改了有感又沒感」反覆 | 在 debug mode 量，數字本身是噪音 | 改用 profile mode + DevTools timeline |
| MissingPluginException 換 plugin 還在 | 沒 `flutter clean` / 原生端沒註冊 | plugin 整合流程，不是換套件 |
| 一個 Bloc/Provider 越塞越多 event | 職責邊界沒切、當成垃圾桶 | 分層與擁有者設計 |

## references 索引

- `references/state-architecture.md` — 狀態選型決策樹、ephemeral vs app state、分層與依賴方向、AsyncValue 三態、rebuild 收窄。動架構或選型前讀。
- `references/widgets-performance.md` — build 純淨性、helper vs class、const、ListView、key、jank 排查、圖片記憶體。寫 UI 或查卡頓前讀。
- `references/platform-build.md` — 三種 build mode 證據力、platform channel、兩平台陷阱、obfuscation、web/desktop 現實。碰原生或 release-only bug 時讀。
- `references/release-checklist.md` — release 冒煙、versioning、雙平台簽章、套件審查、效能驗收。出版前逐條打勾。
- `references/test-scenarios.md` — 判準測驗集，驗證接手模型是否照走。不給執行中的模型讀。
