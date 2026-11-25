---
name: payment-test
description: 金流 / 付款測試專屬流程。覆蓋 App 內購（StoreKit 2 / Play Billing）、Stripe、Apple Pay / Google Pay、訂閱（續訂 / 過期 / 寬限期 / 退款 / 升降級 proration）。驗證購買成功/取消、restore purchases、server 端收據驗證、idempotency（不重複扣款）、價格/幣別/稅、促銷碼、付款中斷網（接 offline）、entitlement 同步。當使用者提到「金流測試 / 付款測試 / payment test / 內購 / IAP / StoreKit / Play Billing / Stripe / Apple Pay / Google Pay / 訂閱測試 / subscription / 退款 / 收據驗證 / 重複扣款」時觸發。配套：compliance-test（PCI-DSS）、offline-mode-test（付款中斷線）、security-scan（金流漏洞）、test-master（規劃金流 TC）、bug-report。
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
argument-hint: "[--provider=storekit|play-billing|stripe] [--scenario=purchase|subscription|refund|restore] [--platform=ios|android]"
---

# payment-test

> ⚙️ **執行前先讀 [`modules/config-loader.md`](./modules/config-loader.md)**。

## 為什麼需要這個 skill

金流是**錯一塊就是真金白銀 + 信任崩塌**的地方：重複扣款、訂閱該停沒停、退款沒同步、收據被偽造繞過付費牆。這些場景手動測極痛（要等訂閱週期、要造各種沙盒帳號），且 `test-master` 很難涵蓋金流狀態機與沙盒細節。

> 金流是最高風險域之一，但 29 個 skill 沒有專門處理付款/訂閱狀態機與沙盒驗證的——本 skill 補這個缺口。

→ 本 skill 系統性產出**付款流程 + 訂閱生命週期 + 防重複扣款 + 收據驗證**測試。

## 適用場景

- ✅ 有 App 內購 / 訂閱 / Stripe / Apple Pay / Google Pay
- ✅ 出過重複扣款 / 訂閱狀態不同步 / 收據繞過
- ✅ Release 前金流守門、上架審查前驗沙盒

## 不適用場景

- ❌ PCI-DSS 合規（卡號不落地等）— 用 `compliance-test`
- ❌ 金流程式漏洞掃描 — 用 `security-scan`
- ❌ 付款 API 的純壓測 — 用 `performance-test-gen`

## 核心測試場景

| # | 場景 | 驗什麼 | 常見 bug |
|---|------|--------|---------|
| 1 | **購買成功** | 付款完成 → entitlement 開通 | 付了沒開通 |
| 2 | **取消 / 失敗** | 中途取消不扣款、UI 正確 | 假成功 |
| 3 | **Restore purchases** | 換機/重裝可還原已購 | 還原不了（蘋果審查必退件） |
| 4 | **訂閱續訂** | 週期到自動續、entitlement 延續 | 續了沒延長 |
| 5 | **訂閱過期 / 寬限** | 過期收回權益、寬限期處理 | 過期還能用 / 寬限期直接斷 |
| 6 | **退款** | 退款 → 權益收回 + 同步 | 退了還有權益 |
| 7 | **升降級 proration** | 方案變更按比例計費 | 重複收 / 算錯 |
| 8 | **收據驗證** | **server 端**驗，不信 client | client 偽造收據繞付費牆 |
| 9 | **idempotency** | 重送/重連不重複扣款 | 重複扣款 |
| 10 | **促銷碼 / 價格 / 幣別 / 稅** | 各區價格、稅、折扣正確 | 幣別/稅錯 |

## 工具對應

| Provider | 沙盒 / 測試 |
|----------|------------|
| **iOS IAP** | StoreKit 2 + `.storekit` config 本地測試 + Sandbox 帳號 |
| **Android IAP** | Play Billing Library + 測試帳號 + license testing |
| **Stripe** | Test mode（`4242...` 測試卡）+ webhook 測試（`stripe listen`） |
| **Apple/Google Pay** | 測試卡 / 測試環境 |

## 執行流程

### Phase 1: 盤點 provider
```bash
grep -rniE "StoreKit|SKProduct|Product\.|Play.?Billing|BillingClient|stripe|PaymentSheet|ApplePay|PKPayment" . 2>/dev/null | head
```

### Phase 2: 產測試（一律沙盒 / test mode）

iOS StoreKit 2（`.storekit` 本地，可進 CI）:
```swift
func testPurchaseGrantsEntitlement() async throws {
    let product = try await Product.products(for: ["pro_monthly"]).first!
    let result = try await product.purchase()
    // 驗 verification + entitlement 開通
    if case .success(let verification) = result {
        let txn = try checkVerified(verification)   // server-side 風格驗證
        XCTAssertTrue(entitlements.contains("pro"))
        await txn.finish()
    }
}
```

Stripe webhook idempotency:
```python
def test_charge_idempotent(stripe_client):
    key = "idem-abc-123"
    r1 = stripe_client.charge(amount=999, idempotency_key=key)
    r2 = stripe_client.charge(amount=999, idempotency_key=key)  # 重送
    assert r1.charge_id == r2.charge_id   # 同一筆，不重複扣
```

### Phase 3: 關鍵斷言
- **收據一律 server 端驗**（client 收據視為不可信）
- **idempotency key** 防重送重複扣款
- 訂閱狀態（active/expired/grace/refunded）↔ entitlement **一致**
- restore purchases 可還原（蘋果硬性要求）

### Phase 4: 報告
`payment-test-report.md`：10 場景 × provider matrix + 金流安全斷言 + 必修。

### Phase 5: CI
購買 happy path + 收據驗證進 smoke；訂閱生命週期（續/過期/退款）進 release。

## ⚠️ 安全護欄

- ❌ **絕不用真實信用卡 / 真實金錢**——一律沙盒 / test mode / 測試卡
- ❌ **絕不信任 client 端收據**——收據驗證必須 server 端
- ❌ 不 log 完整卡號 / 付款 token（PCI → 交 `compliance-test`）
- ✅ idempotency key 防重複扣款，有斷言
- ✅ 訂閱狀態與 entitlement 一致性必驗
- ✅ restore purchases 必測（上架審查硬性要求）

## ♿ a11y 必檢（本 skill 專屬）

- [ ] 價格 / 方案 / 「購買」按鈕有 accessibility label（金額讀得出，不只視覺）
- [ ] 訂閱條款 / 試用到期說明可被讀屏讀取（法規 + 商店審查要求揭露）
- [ ] 付款錯誤 / 失敗訊息非僅紅色、附文字
- [ ] 價格在最大字級下不破版、不被截斷

## 設定依賴

| 設定 Key | 用途 | 預設 |
|---------|------|------|
| `payment_test.providers` | 啟用的金流 | [] |
| `payment_test.sandbox` | **強制沙盒**（禁 production 扣款） | true |
| `payment_test.currencies` | 測試幣別 | ["USD"] |
| `payment_test.subscription_tiers` | 訂閱方案 | [] |
| `payment_test.webhook_url` | Stripe 等 webhook（測試） | "" |

## 範例

詳見 [`examples.md`](./examples.md)
