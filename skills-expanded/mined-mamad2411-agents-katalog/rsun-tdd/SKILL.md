---
name: rsun-tdd
description: 強制 vertical slice tracer-bullet TDD — 禁 horizontal slicing。觸發詞：「寫 test」「TDD」「單元測試」「pytest」「vitest」「測試先寫」。沿襲 mattpocock/skills/engineering/tdd + 容晟 Anti-Pattern G 強制。**任何 production code 第一動作必跑此 skill**。
user-invocable: true
---

# /rsun-tdd — 容晟強制 TDD 紀律

## 為什麼這個 skill

**真實事件**：dashboard session 寫 Booking V2 後端時 — 1 個 mega-commit 含 5 個工作包，TDD 順序也是 horizontal（先寫 5 test 再寫 5 impl），結果：
- tests 變成 imagined behavior 不是 real behavior
- impl 寫 5 天後 test 已經跟現實脫節
- 再修 bug 多花 16 hr

CLAUDE.md Anti-Pattern G 已寫紀律但**沒 skill 強制**，Sonnet sub-agent 自由發揮繼續犯。

`/rsun-tdd` 強制 vertical slice tracer-bullet pattern，每次只做 1 個 RED→GREEN→commit slice。

## 何時必跑

- ✅ **任何 production code 第一動作**（強制）
- ✅ 客戶 deliverable code
- ✅ cron agent 改動
- ✅ MCP server 新增 tool
- ✅ user 說「寫 test」「TDD」「pytest」「vitest」
- ❌ 純文檔 / 註釋更新不需要
- ❌ config 改值不需要
- ❌ TRACKER HTML 內文 update 不需要

## 紀律：one test → one impl → repeat（vertical slice）

```
✅ RIGHT (vertical, tracer bullet):
  RED   write test 1 — run, see RED
  GREEN write impl 1 — run, see GREEN
  COMMIT (msg: "TDD RED → GREEN: <feature>")
  ──────────────────────────────────────────
  RED   write test 2 — based on what learned from slice 1
  GREEN write impl 2
  COMMIT
  ...
  → each slice ≤ 50 line diff，reviewer 看得懂
  → tests 反映 real behavior，每個 commit 都是 working software

❌ WRONG (horizontal, batched):
  RED   test 1, test 2, test 3, test 4, test 5（一口氣寫完）
  GREEN impl 1, impl 2, impl 3, impl 4, impl 5（再一口氣寫完）
  COMMIT "Sprint 0 done (5 work packages)"  ← MEGA-COMMIT
  → tests 是 imagined behavior，沒被 impl 約束
  → tests 跟 impl 互不檢驗 = crap tests
  → reviewer 看 5×50 = 250 行 diff 看不懂
```

## 執行步驟

### Step 0 — 先 grill 對齊（如果還沒）

確認用戶要的功能 + 範圍 + paradigm。沒對齊就直接寫 test = 浪費。

跳到 `/rsun-grill` 跑 Step 0+1 → 確認後回來。

### Step 1 — RED：寫 1 個失敗 test

挑「**最小可獨立 demo**」的 behavior：
- ❌ 不要從 helper / private function 開始
- ✅ 從 public API / user-facing behavior 開始
- ✅ 整合測試優先（exercise real code paths）
- ❌ 不要 mock internal collaborators

範例（Python pytest）：
```python
def test_booking_v2_create_returns_201_with_booking_id():
    """User 建 booking → 回 201 + uuid"""
    response = client.post("/api/booking", json={
        "service_id": "consult-30",
        "start_at": "2026-05-10T10:00:00Z",
        "customer_email": "test@example.com",
    })
    assert response.status_code == 201
    assert "id" in response.json()
    assert len(response.json()["id"]) == 36  # uuid format
```

範例（TypeScript vitest）：
```ts
test('booking POST returns 201 with id', async () => {
  const res = await fetch('/api/booking', {
    method: 'POST',
    body: JSON.stringify({ serviceId: 'consult-30', startAt: '...', email: 't@e.com' }),
  });
  expect(res.status).toBe(201);
  const data = await res.json();
  expect(data.id).toMatch(/^[0-9a-f-]{36}$/);
});
```

跑 test 確認 **真的 RED**：
```bash
pytest tests/test_booking.py::test_booking_v2_create_returns_201_with_booking_id -v
# 預期：FAILED — 因為 endpoint 還沒寫
```

→ 若不 RED（例：endpoint 已存在剛好回 201）→ test 沒測到新功能，重寫 test。

### Step 2 — GREEN：寫**最小** impl 讓 test 過

不要加額外 feature，不要 over-engineer。**只讓那一個 test 過**。

```python
@router.post("/api/booking", status_code=201)
async def create_booking(payload: BookingCreate):
    booking_id = str(uuid.uuid4())
    # 暫時不存 DB，下個 slice 再加
    return {"id": booking_id}
```

跑 test 確認 **真的 GREEN**：
```bash
pytest tests/test_booking.py -v
# 預期：PASSED ✅
```

### Step 3 — COMMIT（單 slice 1 commit）

commit message 必含「TDD RED → GREEN」字樣 + 1 句話描述：

```bash
git add tests/test_booking.py app/routers/booking.py
git commit -m "$(cat <<'EOF'
feat(booking): TDD RED → GREEN — POST /api/booking returns 201 + id

Slice 1/N:
- test_booking_v2_create_returns_201_with_booking_id
- impl: minimal handler returning uuid (no DB yet)

Next slice: persist booking to DB.

Co-Authored-By: <agent name>
EOF
)"
```

### Step 4 — Refactor（可選）

如果 GREEN 後看到明顯 dup / smell → refactor。**但 test 必須繼續 GREEN**。

不確定要不要 refactor → 跳過，下個 slice 再說。

### Step 5 — 下一個 slice

重複 Step 1-4。每個 slice 都是「上一個 slice 學到的東西」的 next step。

範例 slice 序列：
```
Slice 1: POST returns 201 + id (no DB)
Slice 2: POST persists to DB (drizzle)
Slice 3: POST validates start_at format (400 if bad)
Slice 4: POST sends confirmation email (Resend)
Slice 5: POST blocks double-booking same slot (409)
```

每個 slice 1 commit，每 commit ≤ 50 行 diff。

## Good test 的標準（借 mattpocock）

- ✅ Test **behavior through public interface** — 描述系統做什麼
- ✅ Integration-style 優先，real code paths
- ❌ 不要 mock internal collaborators
- ❌ 不要 test private methods
- 🚩 紅旗：refactor 沒改 behavior 但 test 壞了 → test 在測 implementation

## Mocking 規則（factory pattern）

外部依賴（API / DB / time / random）才 mock。用 factory：

```python
# tests/factories/booking.py
def get_mock_booking(**overrides) -> dict:
    return {
        "id": "bk_xxx",
        "service_id": "consult-30",
        "start_at": "2026-05-10T10:00:00Z",
        "customer_email": "test@example.com",
        **overrides,
    }
```

```ts
// tests/factories/booking.ts
export function getMockBooking(overrides?: Partial<Booking>): Booking {
  return { id: 'bk_xxx', serviceId: 'consult-30', ...DEFAULTS, ...overrides };
}
```

## 紅線

- ❌ **不准** horizontal slicing（先寫所有 test 再寫所有 impl）
- ❌ **不准** 1 commit 含多個 slice / 工作包
- ❌ **不准** mock internal collaborator（測 implementation detail）
- ❌ **不准** 跳過 RED 直接寫 GREEN（不知道 test 真的測到沒）
- ❌ **不准** commit message 沒「TDD RED → GREEN」字樣
- ✅ 可以 refactor（保持 GREEN）
- ✅ 可以多 test 細項在同一個 slice 內，前提是同一個 behavior

## 與其他 skill 的關係

- **`/rsun-grill`** — TDD 前先對齊，paradigm + 範圍確認
- **`/rsun-diagnose`** — debug 時跑此（先 reproduce 變 test，再 GREEN）
- **`/caveman`** — sub-agent dispatch 寫 test 也要 caveman 省 token
- **code-reviewer agent** — 每個 commit 後可以叫他二審

## 特別適用容晟情境

- 客戶 deliverable code（避免 Apex Gold 200 hr 浪費重演）
- cron agent 改動（13 production agents 的 _lib.py / sched-*.py）
- MCP server 新 tool（rsun-citation / rsun-architect / rsun-modules / rsun-files）
- Booking V2 backend / frontend
- Sentinel router 升級

對齊 CLAUDE.md Anti-Pattern G「Mega-commit + horizontal slicing」+ Wave 3 強制流程 #2。
