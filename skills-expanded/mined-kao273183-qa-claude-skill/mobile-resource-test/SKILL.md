---
name: mobile-resource-test
description: 端側（裝置上）效能測試專屬流程，覆蓋冷/熱啟動時間、記憶體洩漏、電量消耗、ANR、掉幀/卡頓（jank）、CPU/GPU。整合 iOS（XCTest Metrics + Instruments + MetricKit）/ Android（Macrobenchmark + Perfetto + LeakCanary + JankStats）/ Flutter（DevTools + profile mode）。產出含 SLA 門檻、迴歸偵測、CI 整合的端側效能報告。當使用者提到「端側效能 / 冷啟動 / app 啟動時間 / 記憶體洩漏 / memory leak / 電量測試 / ANR / 掉幀 / jank / 卡頓 / 掉幀率 / Instruments / Macrobenchmark / LeakCanary / 幀率 / fps 測試」時觸發。配套：performance-test-gen（server 端 API 壓測，本 skill 是端側補強）、test-automation（把效能測試掛進 UI test）、smoke-test-analyzer（效能迴歸屬 T2 release）、bug-report（追效能 bug）。
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
argument-hint: "[平台 / 場景] [--metric=startup|memory|jank|battery] [--platform=ios|android|flutter]"
---

# mobile-resource-test

> ⚙️ **執行前先讀 [`modules/config-loader.md`](./modules/config-loader.md)**。

## 為什麼需要這個 skill

`performance-test-gen` 做的是 **server 端壓測**（k6 / JMeter / Locust 打 API，量 p95 / error rate）——那是「後端扛不扛得住」。

但使用者實際**握在手上的體感**是端側的：
- App 點開要等幾秒（冷啟動）
- 滑動會不會卡（掉幀 / jank）
- 用久了會不會越來越燙、耗電、記憶體爆掉被系統殺掉
- 按下去沒反應（ANR / 主執行緒卡死）

> 你以 iOS / Android 為主，但 24 個 skill 裡**端側效能完全空白**——本 skill 補這個缺口。

→ 本 skill 專做 **on-device 效能量測 + 洩漏偵測 + 迴歸守門**。

## 適用場景

- ✅ Release 前端側效能守門（啟動 / 卡頓 / 記憶體不退步）
- ✅ 重構 / 加大功能後驗證沒拖慢 app
- ✅ 收到「app 好慢 / 好耗電 / 會閃退」客訴要量化重現
- ✅ 把效能 metric 掛進 CI，PR 時就擋住退步

## 不適用場景

- ❌ Server / API 壓測 — 用 `performance-test-gen`
- ❌ 功能對不對 — 用 `test-master` / `test-automation`
- ❌ 視覺有沒有跑掉 — 用 `visual-regression-gen`

## 5 大端側 metric + 工具對應

| Metric | 它代表 | iOS | Android | Flutter |
|--------|-------|-----|---------|---------|
| **啟動時間** | 點開到可互動 | XCTApplicationLaunchMetric / Organizer | Macrobenchmark `StartupTimingMetric` | `flutter run --profile` timeline |
| **記憶體** | 洩漏 / 峰值 | Instruments Leaks/Allocations · XCTMemoryMetric | LeakCanary · Android Profiler · StrictMode | DevTools Memory |
| **掉幀 / jank** | 滑動順不順 | XCTOSSignpostMetric · Hitches (Instruments) | Macrobenchmark `FrameTimingMetric` · JankStats | DevTools Timeline · frame stats |
| **電量** | 耗不耗電 | Energy Log · MetricKit | Battery Historian · Profiler Energy | （走原生工具） |
| **ANR / 卡死** | 按了沒反應 | Main Thread Checker · watchdog | ANR trace · StrictMode | （平台層） |

## SLA 門檻（預設，可由 config 覆蓋）

| Metric | 目標 | 來源 |
|--------|------|------|
| 冷啟動 (cold) | < 2000 ms | Google Play vitals 建議 < 5s，優秀 < 2s |
| 熱啟動 (warm) | < 1000 ms | |
| Jank rate | < 1%（frozen frames < 0.1%） | Android vitals |
| 幀率 | 穩定 60fps（高刷 120fps 不掉） | |
| 記憶體洩漏 | 0 leak（重複進出畫面記憶體回穩） | |
| 記憶體峰值 | < config 上限（依裝置） | |
| ANR | 0 | |

## 執行流程

### Phase 1: 偵測平台 + 工具

```bash
ls *.xcodeproj *.xcworkspace 2>/dev/null   # iOS
ls build.gradle* settings.gradle* 2>/dev/null   # Android
ls pubspec.yaml 2>/dev/null   # Flutter
# 檢查是否已有 benchmark module
grep -rl "androidx.benchmark.macro" . 2>/dev/null   # Android Macrobenchmark
grep -rl "XCTApplicationLaunchMetric\|measure(metrics" . 2>/dev/null   # iOS
```

### Phase 2: 量測（依 metric 生對應碼）

#### iOS — XCTest Metrics（可進 CI）

```swift
import XCTest

final class LaunchPerformanceTests: XCTestCase {
    func testColdLaunchTime() throws {
        measure(metrics: [XCTApplicationLaunchMetric()]) {
            XCUIApplication().launch()
        }
    }

    func testScrollHitches() throws {
        let app = XCUIApplication(); app.launch()
        measure(metrics: [XCTOSSignpostMetric.scrollDecelerationMetric]) {
            app.tables.firstMatch.swipeUp(velocity: .fast)
        }
    }

    func testMemoryFootprint() throws {
        measure(metrics: [XCTMemoryMetric()]) {
            // 重複進出詳情頁 10 次，看記憶體是否回穩
        }
    }
}
```

> 配 MetricKit（`MXMetricManager`）收集**真實使用者**的啟動 / hang / 電量資料。

#### Android — Macrobenchmark（可進 CI）

```kotlin
@RunWith(AndroidJUnit4::class)
class StartupBenchmark {
    @get:Rule val rule = MacrobenchmarkRule()

    @Test fun coldStartup() = rule.measureRepeated(
        packageName = "com.example.app",
        metrics = listOf(StartupTimingMetric()),
        iterations = 10,
        startupMode = StartupMode.COLD
    ) { pressHome(); startActivityAndWait() }

    @Test fun scrollJank() = rule.measureRepeated(
        packageName = "com.example.app",
        metrics = listOf(FrameTimingMetric()),
        iterations = 10
    ) { /* 滑動 RecyclerView */ }
}
```

> 記憶體洩漏用 **LeakCanary**（debug build 自動偵測 retained instance）；主執行緒 IO 用 **StrictMode** 抓。

#### Flutter — profile mode + DevTools

```bash
flutter run --profile          # 絕不用 debug 量效能（debug 有額外開銷）
flutter drive --profile --target=integration_test/perf_test.dart
```
```dart
// 收集 frame timing
await binding.traceAction(() async {
  await tester.fling(find.byType(ListView), const Offset(0, -500), 3000);
  await tester.pumpAndSettle();
}, reportKey: 'scrolling_timeline');
// 解析 → 看 build/raster 是否超過 16ms (60fps)
```

### Phase 3: 洩漏 / ANR 深度偵測

| 問題 | iOS | Android |
|------|-----|---------|
| 記憶體洩漏 | Instruments Leaks + Allocations（Generation 標記，重複操作看是否成長） | LeakCanary heap dump |
| Retain cycle | Memory Graph Debugger（看強引用環） | LeakCanary 指出 leak trace |
| 主執行緒卡死 | Main Thread Checker / Time Profiler | ANR trace + StrictMode |

### Phase 4: 統一報告 + 迴歸偵測

合併輸出 → `mobile-resource-report.md`：

```markdown
# Mobile Resource Report · my-app · 2026-06-02

## 📊 端側效能總覽
| Metric | 本次 | 門檻 | 上次 | 判定 |
|--------|------|------|------|------|
| 冷啟動 (iOS) | 1840ms | <2000 | 1620ms | ⚠️ 退步 +220ms |
| 冷啟動 (Android) | 1210ms | <2000 | 1190ms | ✅ |
| Jank rate | 0.6% | <1% | 0.4% | ✅ |
| 記憶體峰值 | 412MB | <450 | 398MB | ✅ |
| Leak | 1 | 0 | 0 | 🔴 新增洩漏 |
| ANR | 0 | 0 | 0 | ✅ |

## 🔴 必修
### 記憶體洩漏 — ProfileViewController
- **工具**: Instruments Leaks
- **trace**: `ImageCache` 強引用 `self`，detail 頁退出未釋放
- **重現**: 進出 profile 頁 10 次 → 記憶體 +38MB 不回收
- **修法**: closure 用 `[weak self]`，或 cache 改 NSCache 自動回收

### 冷啟動退步 +220ms
- **疑因**: 新增的 SDK 在 `application(_:didFinishLaunching:)` 同步初始化
- **修法**: 延後 / 背景初始化，或用 baseline profile (Android)

## 📋 修復清單 + 估時
## 📈 趨勢（近 3 次）
```

### Phase 5: CI 整合 + 守門

- iOS：XCTest Metrics 設 baseline，超過容忍度 CI fail
- Android：Macrobenchmark + `baselineprofile` gradle，迴歸擋 PR
- Flutter：解析 timeline summary，build/raster p90 超標 fail
- 把效能迴歸標到 `smoke-test-analyzer` 的 T2（release 才全跑，PR 只跑啟動）

## ⚠️ 安全護欄

- ❌ **絕不用 debug build 量效能**（debug 有 assertion / 無最佳化，數字失真）→ iOS Release、Android `benchmark` buildType、Flutter `--profile`
- ✅ 每個數字標**裝置 + OS 版本**（不同機差很大，跨機比較無意義）
- ✅ 多次取樣取中位數 / p90，不用單次（端側噪音大）
- ✅ 區分「真退步」與「量測噪音」——退步需超過容忍度才報

## ♿ a11y 必檢（本 skill 專屬）

無障礙設定會放大效能負擔，要一起量：
- [ ] **最大字級**（iOS AX5 / Android 200%）下，滑動 jank 是否仍 < 1%（字級放大 → layout 重算成本暴增）
- [ ] **Reduce Motion / 關閉動畫** 時不應有殘留耗電的隱形動畫迴圈
- [ ] VoiceOver / TalkBack 開啟時 a11y tree 計算不造成主執行緒卡頓
- [ ] 高對比 / 深色模式切換不觸發整頁重繪掉幀

## 🪟 Android split-screen 效能檢查（本 skill 專屬）

分割畫面（split-screen）多工模式會觸發 `onMultiWindowModeChanged`/resize/reconfiguration，且系統因兩個 App 共享記憶體與 CPU，容易放大效能問題（範例：`test-master` 的 UOP-7890，健康首頁在分割畫面下持續載入失敗）。這類問題在全螢幕測試下不會出現，要獨立量測：

- [ ] **進入/退出分割畫面的 resize 耗時 + 掉幀**：觸發 `onMultiWindowModeChanged` 後的 relayout 是否造成明顯 jank（比對全螢幕下同一畫面的 jank rate 基準）
- [ ] **分割畫面下記憶體行為**：系統在多工模式下可能更早觸發 `onTrimMemory`/low-memory callback，確認畫面在記憶體降級時是否正常降級而非白屏/crash
- [ ] **分割畫面下 ANR 風險**：resize 期間主執行緒是否有重工作（如重新請求/重新渲染整頁）造成卡死
- [ ] **分割畫面尺寸變化時的重複請求**：resize 是否誤觸發重複 API call 或無限重試（loading 迴圈），這是 UOP-7890 的實際症狀
- **工具**：Macrobenchmark 對 multi-window 情境的官方支援有限，建議先用 `adb shell wm size` / 手動觸發分割畫面 + 目視觀察 jank，或用 Layout Inspector 搭配手動操作；沒有現成的自動化 benchmark API 時不要硬套，先用手動量測記錄現況
- iOS 無對應系統級分割畫面模式，此section僅適用 Android

## 設定依賴

| 設定 Key | 用途 | 預設 |
|---------|------|------|
| `mobile_resource.cold_start_ms` | 冷啟動門檻 | 2000 |
| `mobile_resource.warm_start_ms` | 熱啟動門檻 | 1000 |
| `mobile_resource.jank_threshold` | 掉幀率上限 | 0.01 |
| `mobile_resource.memory_peak_mb` | 記憶體峰值上限 | 450 |
| `mobile_resource.frame_rate_target` | 目標幀率 | 60 |
| `mobile_resource.tools` | 啟用工具 | 依平台自動 |
| `platforms.ios.repo` / `platforms.android.repo` | 量測迴歸的版本對應 | — |

## 範例

詳見 [`examples.md`](./examples.md)
