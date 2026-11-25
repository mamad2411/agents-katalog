---
name: offline-mode-test
description: 弱網 / 離線 / 斷線重連測試專屬流程，覆蓋 8 大網路韌性場景：完全離線讀快取、離線寫操作排隊、斷線自動重連、弱網高延遲、切換網路（wifi↔cellular）、樂觀更新與回滾、離線衝突解決、同步佇列冪等。整合 iOS（Network Link Conditioner + URLProtocol mock）/ Android（OkHttp MockWebServer + adb svc + WorkManager）/ Flutter（connectivity_plus + dio mock）/ Web（Playwright setOffline + Service Worker）。當使用者提到「離線測試 / offline mode / 弱網 / 斷網 / 斷線重連 / 飛航模式測試 / 網路韌性 / 樂觀更新 / optimistic update / 衝突解決 / 同步測試 / sync / retry / 重試 / 網路切換」時觸發。配套：test-master（規劃網路條件矩陣 TC）、test-automation（把離線場景掛進 UI test）、mobile-resource-test（離線重連的效能）、bug-report（追離線 bug）。
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
argument-hint: "[平台 / 場景] [--scenario=offline-read|offline-write|reconnect|conflict] [--platform=ios|android|flutter|web]"
---

# offline-mode-test

> ⚙️ **執行前先讀 [`modules/config-loader.md`](./modules/config-loader.md)**。

## 為什麼需要這個 skill

`test-master` 規劃功能 TC 時，網路條件常只測「有網路」這條 happy path。但**真實使用者在電梯、地鐵、停車場、出國漫遊**——網路是時有時無的。

最容易出包、也最難手動重現的就是這些：
- 離線時點按鈕 → 沒反應？崩潰？還是優雅排隊？
- 送出表單時斷線 → 資料掉了？重複送兩次？
- 回到線上 → 自動同步？還是要使用者手動重試？
- 離線改了資料，雲端也改了 → 誰蓋誰？

> mobile QA 最高頻痛點，但 26 個 skill 裡完全沒有網路狀態測試——本 skill 補這個缺口。

→ 本 skill 系統性產出**網路韌性測試**：注入網路條件 + 跑 8 大場景 + 驗證行為。

## 適用場景

- ✅ 任何會打 API / 有本地快取 / 有同步機制的 app
- ✅ 離線優先（offline-first）/ 樂觀更新架構的驗證
- ✅ 收到「網路不好就閃退 / 資料不見 / 重複送出」客訴
- ✅ Release 前網路韌性守門

## 不適用場景

- ❌ Server 端能扛多少流量 — 用 `performance-test-gen`
- ❌ 端側啟動/記憶體效能 — 用 `mobile-resource-test`
- ❌ 純功能（有網路下對不對）— 用 `test-master`

## 8 大網路韌性場景

| # | 場景 | 驗什麼 | 常見 bug |
|---|------|--------|---------|
| 1 | **完全離線讀** | 快取可讀 + 明確離線提示 | 白畫面 / 無限轉圈 / 崩潰 |
| 2 | **離線寫排隊** | 操作暫存本地，回線送出 | 操作直接丟失 / 報錯擋住 |
| 3 | **斷線重連** | 自動 retry，不重複送 | 不重連 / 重複送 2 次 |
| 4 | **弱網高延遲** | loading 狀態 + timeout 不卡死 | UI 凍結 / 永久 loading |
| 5 | **切換網路** | wifi↔cellular 連線優雅延續 | 連線中斷不恢復 |
| 6 | **樂觀更新 + 回滾** | UI 先更新，失敗回滾 | 假成功（UI 顯示成功實際失敗） |
| 7 | **離線衝突解決** | 離線改 vs 雲端改的 merge | 靜默覆蓋 / 資料遺失 |
| 8 | **同步佇列冪等** | 多筆離線操作順序 + 去重 | 順序錯亂 / 重複套用 |

## 工具對應

| 平台 | 注入網路條件 | Mock / 驗證 |
|------|-------------|------------|
| **iOS** | Network Link Conditioner（100% Loss / High Latency DNS） | `URLProtocol` stub · Proxyman/Charles |
| **Android** | `adb shell svc wifi/data disable` · emulator network type | OkHttp `MockWebServer`（`SocketPolicy.NO_RESPONSE` / 延遲） · WorkManager retry |
| **Flutter** | `connectivity_plus` 注入 · platform channel | `dio` interceptor mock · `http_mock_adapter` |
| **Web** | Playwright `context.setOffline(true)` · DevTools throttle | `route.abort()` · Service Worker offline |

## 執行流程

### Phase 1: 偵測平台 + 網路層

```bash
grep -rl "URLSession\|Alamofire" . 2>/dev/null      # iOS 網路層
grep -rl "OkHttp\|Retrofit\|WorkManager" . 2>/dev/null   # Android
grep -rl "dio\|http\|connectivity_plus" . 2>/dev/null    # Flutter
grep -rl "fetch\|axios\|serviceWorker" . 2>/dev/null     # Web
# 是否已有快取 / 同步機制
grep -rniE "cache|offline|sync|queue|retry|optimistic" . 2>/dev/null | head
```

### Phase 2: 注入網路條件（產對應碼）

#### iOS — URLProtocol stub（離線/逾時，可進 CI）

```swift
final class OfflineURLProtocol: URLProtocol {
    override class func canInit(with request: URLRequest) -> Bool { true }
    override func startLoading() {
        client?.urlProtocol(self, didFailWithError:
            NSError(domain: NSURLErrorDomain, code: NSURLErrorNotConnectedToInternet))
    }
    override func stopLoading() {}
}
// 測試時注入 → 驗證 UI 顯示離線提示而非崩潰
```

#### Android — OkHttp MockWebServer（弱網/逾時）

```kotlin
@Test fun offlineShowsCachedData() {
    server.enqueue(MockResponse().setSocketPolicy(SocketPolicy.NO_RESPONSE)) // 模擬斷線
    // 啟動畫面 → 驗證讀到快取 + 顯示「離線中」banner
    onView(withText("離線中")).check(matches(isDisplayed()))
}
```
真機切網用 `adb shell svc data disable` / `svc wifi disable`。

#### Flutter — dio mock adapter

```dart
final dioAdapter = DioAdapter(dio: dio);
dioAdapter.onGet('/feed', (s) => s.throws(
  408, DioException.connectionTimeout(timeout: Duration(seconds: 5), requestOptions: RequestOptions())));
// 驗證: 顯示 retry 按鈕，不是無限 loading
```

#### Web — Playwright offline

```typescript
test('offline shows cached + queues writes', async ({ page, context }) => {
  await page.goto('/feed');
  await context.setOffline(true);
  await page.getByRole('button', { name: '送出' }).click();
  await expect(page.getByText('已排隊，連線後送出')).toBeVisible();
  await context.setOffline(false);
  await expect(page.getByText('已送出')).toBeVisible(); // 回線自動同步
});
```

### Phase 3: 跑 8 大場景 + 驗證行為

每場景產一條可執行 test + 預期行為斷言。重點驗「**優雅降級**」而非崩潰：
- 離線 → 有明確提示（非白畫面 / 非崩潰）
- 寫操作 → 排隊或擋下，**絕不靜默丟失**
- 重連 → 自動同步且**冪等**（不重複套用）
- 樂觀更新失敗 → **回滾** UI（不留假成功）

### Phase 4: 統一報告

```markdown
# Offline Resilience Report · my-app · 2026-06-02

## 📊 8 場景結果
| # | 場景 | iOS | Android | 判定 |
|---|------|-----|---------|------|
| 1 | 離線讀快取 | ✅ | ✅ | pass |
| 2 | 離線寫排隊 | 🔴 操作丟失 | ✅ | fail |
| 3 | 斷線重連 | ⚠️ 重複送 2 次 | ✅ | fail |
| 6 | 樂觀更新回滾 | 🔴 假成功 | 🔴 假成功 | fail |

## 🔴 必修
### 離線送出表單 → 資料靜默丟失（場景 2, iOS）
- **重現**: 飛航模式 → 填表 → 送出 → 顯示成功，但回線後資料不存在
- **根因**: 無離線佇列，斷線時 request 直接 drop
- **修法**: 失敗的寫操作存本地佇列（Core Data / Room），回線由背景任務重送（冪等鍵去重）

### 斷線重連 → 重複送出（場景 3）
- **修法**: 每筆請求帶 idempotency-key，server 去重；client retry 用同一 key
```

### Phase 5: CI 整合

- iOS：URLProtocol stub 場景進 XCUITest，CI 每次跑
- Android：MockWebServer 場景進 Espresso/instrumented test
- Web：Playwright offline 場景進 E2E
- 標到 `smoke-test-analyzer`：場景 1-3（核心）進 T1 daily，4-8 進 T2 release

## ⚠️ 安全護欄

- ✅ 寫操作測試一律驗「**不靜默丟失**」——排隊或明確報錯，二選一
- ✅ 重連測試一律驗**冪等**——retry 不可造成重複扣款 / 重複貼文
- ✅ 樂觀更新一律驗**失敗回滾**——不可留假成功狀態
- ❌ 不用真實 production endpoint 做斷線注入（用 mock / staging）

## ♿ a11y 必檢（本 skill 專屬）

離線 / 錯誤 / 同步狀態是 a11y 高風險區（常只用 icon / 顏色）：
- [ ] 「離線中」狀態 VoiceOver / TalkBack 讀得出（不只灰色 icon）
- [ ] retry 按鈕有 accessibility label（不是只有箭頭圖示）
- [ ] 同步中 / 已排隊 / 已送出 三態有可讀的 accessibility value
- [ ] 離線錯誤提示非僅紅色，附文字；字級放大下不破版

## 設定依賴

| 設定 Key | 用途 | 預設 |
|---------|------|------|
| `offline_test.scenarios` | 啟用的場景編號 | 全部 1-8 |
| `offline_test.timeout_ms` | 請求逾時門檻 | 5000 |
| `offline_test.retry_policy` | 重試策略 | exponential-backoff |
| `offline_test.conflict_strategy` | 衝突解決策略 | last-write-wins / merge / ask |
| `offline_test.tools` | 注入工具 | 依平台自動 |

## 範例

詳見 [`examples.md`](./examples.md)
