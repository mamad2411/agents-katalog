---
name: rsun-diagnose
description: 強制 reproduce → minimise → instrument → fix → verify 的 debug 紀律。觸發詞：「bug」「debug」「壞了」「不會動」「修一下」「為什麼」「fix」。沿襲 mattpocock/skills/engineering/diagnose + 容晟 13 cron agent debug 經驗。**任何 bug fix 第一動作必跑此 skill**。
user-invocable: true
---

# /rsun-diagnose — 容晟強制 debug 紀律

## 為什麼這個 skill

**真實事件**：
- 2026-04-27 Llama 3.1 deprecated 全 fleet 炸 — 沒先 minimize 直接亂改 5 個 agent，第 6 hr 才發現是同一個 root cause
- Card 1 HTTP 404 + valid JSON — 沒 reproduce 直接猜「應該是 cors」，改了 30 分鐘無效
- Pawx 12.5 hr 空轉 — 沒 instrument 看不到中間狀態

舊 `/engineering:debug` 太鬆，Sonnet 跳步驟自由發揮。

`/rsun-diagnose` 強制 5 步驟，每步必交付物，跳步直接停。

## 何時必跑

- ✅ **任何 bug fix 第一動作**（強制）
- ✅ 「為什麼這個壞了」型問題
- ✅ cron agent / workflow 失敗
- ✅ test 突然 RED
- ✅ user 說「壞了」「不會動」「修一下」「fix」
- ❌ 純功能新增不需要（走 `/rsun-tdd`）
- ❌ refactor 不需要

## 執行 5 步驟（不可跳）

### Step 1 — REPRODUCE：寫最小可重現

**規則**：在能寫 fix 之前，**必須**有一個能 100% reproduce bug 的步驟。

交付物：一段「跑了就壞」的命令 / curl / test。

```bash
# 範例（cron agent）：
cd ~/Projects/TRACKER && set -a && . .env && set +a
python3 scripts/sched/sched-09-vista.py 2>&1 | tail -20
# Output: HTTP 429 rate limit ← 重現了

# 範例（API）：
curl -i https://rsun.me/api/clients/123 -H "X-Admin-Pin: 666"
# Output: 500 Internal Server Error ← 重現了

# 範例（test）：
pytest tests/test_booking.py::test_create -v
# Output: FAILED — assert 201 == 500 ← 重現了
```

**reproduce 不出來 → 停**。先問 user：
- 你怎麼觸發的？
- 哪個環境？（local / preview / production）
- 哪個時間？（先看 logs）

不要在 reproduce 不到的狀態下改 code。

### Step 2 — MINIMISE：砍到最小

把 reproduce 的 input / scenario 砍到**最小可重現的 example**。

範例：
```
原本：用戶 A 訪問頁面 X，點按鈕 Y，填表單 Z，submit 後 500
↓ 砍
最小：直接 curl POST /api/booking 帶 minimal payload → 500
↓ 再砍
最終：payload 只留 1 個 required field → 還是 500，跟其他 field 無關
```

```python
# 原本一個 200 行 test
def test_full_flow():
    setup_user(); setup_service(); ...
    response = client.post(...)
    assert response.status == 201

# 砍到
def test_minimal_repro():
    response = client.post("/api/booking", json={"service_id": "x"})
    # 只留必要 field，移除其他 noise
```

交付物：**< 20 行**的 reproduction script / test。

→ minimise 過程**常常順便發現 root cause**（「啊原來只是 X 欄位的問題」）。

### Step 3 — INSTRUMENT：插探針看 internal state

不要憑感覺猜，**看實際數據**。

| 場景 | Instrument 工具 |
|---|---|
| Python script | `print(f"DEBUG: x={x!r} type={type(x)}")` 或 `logging.warning()` |
| API request | `curl -v` 看 headers + status，`tcpdump` 看 wire |
| frontend | `console.log` + Chrome DevTools Network tab |
| cron agent | tail logs：`gh run view <id> --log` |
| DB | `EXPLAIN ANALYZE` + `pg_stat_statements` |

範例（Vista 429）：
```python
# 加 instrument
import time
print(f"[{time.time()}] calling groq...")
response = groq_complete(prompt)
print(f"[{time.time()}] response status={response.status} headers={dict(response.headers)}")
print(f"[{time.time()}] x-ratelimit-remaining={response.headers.get('x-ratelimit-remaining')}")
```

→ 看到 `x-ratelimit-remaining: 0` → 確認是 rate limit 不是 key 失效。

**不准猜**。看到實際 state 才下一步。

### Step 4 — HYPOTHESIS → FIX：基於 instrument 數據提假設

格式必填：

```markdown
## Hypothesis
看到 X = <實際數據>，所以 root cause 可能是 Y。
如果是 Y，那 fix Z 應該能解決。
驗證方式：跑 Step 1 reproduce 命令，預期 status=201 不是 500。
```

範例：
```markdown
## Hypothesis
看到 x-ratelimit-remaining: 0，所以 root cause 是 cron 太密集連打 Groq RPD。
如果是 RPD 限制，那 fix 是把 Vista cron 從 daily 改成 monthly（1/15 觸發）。
驗證方式：手動跑 Vista 一次（不用等 30 天）→ 預期 200 + 真實 markdown 出貨。
```

寫 fix code（**最小 diff**，不順手 refactor）：
```python
# scripts/sched/sched-09-vista.py
# 加 retry + jitter
import random
for attempt in range(3):
    try:
        response = groq_complete(prompt)
        break
    except RateLimitError:
        sleep(2 ** attempt + random.random())
else:
    alert("vista", "rate limit exhausted")
    return  # graceful degrade
```

### Step 5 — VERIFY：跑 reproduce 確認 fix

**回到 Step 1 命令**，再跑一次。預期：
- 之前壞的現在 work
- 加一個 regression test 防止再壞

```bash
pytest tests/test_vista.py::test_handles_rate_limit -v  # 新加的 regression
pytest tests/test_vista.py -v  # 全部還 GREEN
```

最後 commit（含「fixes #issue」+ 描述 root cause + verify steps）：

```bash
git commit -m "$(cat <<'EOF'
fix(vista): retry with jitter on Groq RPD exhaustion

Root cause: Vista cron 1/15 觸發但測試時連打導致 RPD: 0
Fix: 3-retry exponential backoff + alert on exhaustion
Verify: pytest tests/test_vista.py::test_handles_rate_limit GREEN

EOF
)"
```

## 紅線

- ❌ **不准** Step 1 reproduce 不到就寫 fix
- ❌ **不准** 跳 Step 2 minimise（會 fix 錯地方）
- ❌ **不准** Step 3 instrument 沒看實際數據就猜 hypothesis
- ❌ **不准** Step 4 fix 順手 refactor 別的東西（minimal-change-engineer 紀律）
- ❌ **不准** Step 5 沒 verify 就 commit
- ✅ minimise 時發現 root cause → 直接跳到 Step 4（不用再 instrument）
- ✅ 發現 hypothesis 錯 → 回 Step 3 重新 instrument 不同地方

## 對接 sub-agent

debug 鏈建議：

```
1. minimal-change-engineer  ← Step 4 寫 fix code
2. evidence-collector       ← Step 5 截圖 / 錄影 verify
3. code-reviewer            ← commit 前終審
```

每站有交付物 → 下一站才能跑。

## 特別適用容晟情境

- 13 cron agent 失敗（task_runs jsonl + agent-alerts.json 是 instrument 來源）
- Booking V2 / Sentinel router 異常
- CF Workers / Pages 部署炸
- 客戶頁面 user 回報 bug
- test 突然紅（先 reproduce 在 local，再看 CI）

對齊 CLAUDE.md Wave 3 強制流程 #3 + Anti-Pattern E（HTTP error 不分 valid JSON）。
