---
name: observability-instrument
description: Adds production observability to a service — structured logging, RED/USE metrics, OpenTelemetry distributed tracing, plus Prometheus/Grafana dashboards and actionable SLO-based alerts. Triggers when instrumenting code, designing metrics/dashboards, defining SLI/SLO, or fixing noisy/missing alerts.
when_to_use: เพิ่ม logging/metrics/tracing ลง service, ออกแบบ dashboard, ตั้ง SLI/SLO/alert, alert noisy หรือ blind spot
---

## When to Use

ใช้ skill นี้เมื่อทำงานข้อใดข้อหนึ่ง:

- เพิ่ม observability (logging/metrics/tracing) ลง service ที่ยัง blind
- ออกแบบ metric/dashboard ใหม่ หรือต้องเลือกว่าจะวัด signal อะไร
- กำหนด SLI/SLO + error budget
- แก้ alert ที่ noisy (เด้งบ่อยจนคนเมิน) หรือ blind spot (incident เกิดแต่ไม่มี alert)
- debug latency/error ที่กระจายข้ามหลาย service (ต้อง distributed tracing)

**ไม่ใช้เมื่อ:** แค่ debug ครั้งเดียวด้วย print/log ชั่วคราว, service เป็น prototype throwaway, หรือมี platform team จัดการ instrumentation มาตรฐานให้แล้ว (ใช้ของเขา)

## Steps

ทำตามลำดับ — แต่ละ step verify ได้จริง ห้ามข้ามไป dashboard ก่อนมี metric

### 1. เลือก signal: RED สำหรับ request-driven, USE สำหรับ resource

- **RED** (service ที่รับ request: API, RPC, consumer) → วัด 3 ตัวต่อ endpoint/route:
  - **Rate** — requests/sec
  - **Errors** — failed requests/sec (แยกจาก rate, ไม่ใช่ ratio ตอน emit — คำนวณ ratio ตอน query)
  - **Duration** — latency distribution (histogram เสมอ ไม่ใช่ avg)
- **USE** (resource: CPU, memory, disk, queue, connection pool) → วัด **Utilization, Saturation, Errors**
- เริ่มจาก golden path: instrument entry point (HTTP handler / message consumer) ก่อน แล้วค่อยลงลึก dependency call (DB, cache, downstream HTTP)

### 2. Structured logging — JSON + correlation/trace id ทุก log line

- ออก log เป็น **JSON (one object per line)** ไม่ใช่ printf string — เพื่อ query/filter ได้
- ทุก log entry ต้องมี field: `timestamp` (RFC3339/ISO8601 UTC), `level`, `message`, `service`, `trace_id`, `span_id`
- **inject `trace_id` จาก context** ทุก log ที่อยู่ใน request scope — เพื่อ jump จาก log → trace ได้ (logs↔traces correlation)
- log levels จริง: `ERROR` = ต้องมีคนดู / `WARN` = degraded แต่ทำงานได้ / `INFO` = state change สำคัญ (start/stop/deploy) / `DEBUG` = ปิดใน prod ปกติ
- **ห้าม log PII/secret** (password, token, full card, email เต็ม) — redact ก่อน ออก field ที่ filter ได้แทน (เช่น `user_id` ไม่ใช่ email)
- ใส่ context เป็น field ไม่ใช่ string interpolation: `{"event":"order_failed","order_id":"123","reason":"timeout"}` ไม่ใช่ `"order 123 failed: timeout"`

### 3. OTel tracing — span ครอบ unit of work + propagate context

- ใช้ **OpenTelemetry SDK** (vendor-neutral) — auto-instrumentation สำหรับ HTTP/gRPC/DB client ก่อน, manual span เฉพาะ business logic สำคัญ
- 1 span = 1 unit of work ที่มีความหมาย (handle request, query DB, call downstream, ประมวลผล batch)
- **propagate context ข้าม boundary** — ใส่ `traceparent` header (W3C Trace Context) ทุก outbound HTTP/RPC/message; ฝั่งรับ extract → ต่อ trace เดียวกัน
- ใส่ span attributes ที่ filter ได้: `http.route`, `http.status_code`, `db.system`, `messaging.destination` — **ห้ามใส่ high-cardinality** (user_id, request_id) เป็น attribute ถ้าจะ aggregate (ใส่เป็น event/log แทน)
- mark span error ให้ถูก: set status `ERROR` + record exception → ไม่งั้น trace ดู green ทั้งที่ fail
- **sampling**: head-based (เช่น 10%) สำหรับ traffic สูง แต่ **always-sample error/slow span** (tail-based ถ้า backend รองรับ) — ไม่งั้น trace ของ incident หาย

### 4. Prometheus metrics — naming + label กัน cardinality ระเบิด

- metric type ให้ถูก: **Counter** (monotonic: requests, errors) / **Histogram** (latency, size — ได้ percentile) / **Gauge** (queue depth, pool in-use)
- naming convention: `<namespace>_<subsystem>_<name>_<unit>` + suffix มาตรฐาน — `_total` (counter), `_seconds` (duration), `_bytes` (size)
  - ดี: `http_requests_total`, `http_request_duration_seconds`, `db_pool_connections_in_use`
- **base unit เสมอ**: seconds ไม่ใช่ ms, bytes ไม่ใช่ MB
- **🔴 cardinality discipline (gotcha ที่ทำ Prometheus ล่มบ่อยสุด):**
  - label = bounded set เท่านั้น: `method`, `route` (template `/users/:id` ไม่ใช่ `/users/42`), `status_code`, `status_class` (2xx/4xx/5xx)
  - **ห้ามใส่ unbounded เป็น label**: user_id, request_id, email, full URL with query, raw error message, timestamp
  - cardinality = ผลคูณของจำนวนค่าทุก label → 3 labels × (10 routes × 5 methods × 6 status) = 300 series/metric; ถ้าใส่ user_id (1M users) = 1M series → OOM
- histogram bucket: ตั้ง bucket ให้ครอบ SLO threshold (เช่น SLO p99 < 300ms → ต้องมี bucket ที่ 0.3) ไม่งั้นวัด SLO ไม่ได้

### 5. Grafana dashboard — RED panels + SLI ต่อ service

- 1 dashboard ต่อ service, layout top→down: **SLI summary → RED → dependencies → saturation**
- RED panels (PromQL):
  - Rate: `sum(rate(http_requests_total[5m])) by (route)`
  - Errors: `sum(rate(http_requests_total{status_class="5xx"}[5m])) by (route)` และ error ratio = errors/rate
  - Duration: `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, route))` — **p50/p95/p99 แยกเส้น ห้ามใช้ avg**
- ใช้ template variable (`$service`, `$route`) ให้ reuse dashboard ได้หลาย service
- ทุก panel ต้อง answer คำถาม operational จริง — panel ที่ไม่เคยถูกดูตอน incident = ลบทิ้ง

### 6. SLO + error budget → alert ที่ actionable (multi-window burn rate)

- กำหนด **SLI** (วัดได้จาก metric ที่มีจริง): availability = `good_requests / total_requests`, latency = `% requests < threshold`
- ตั้ง **SLO** เป็นเป้า (เช่น 99.9% / 30 วัน) → **error budget** = 0.1% = ~43 นาที downtime/เดือน
- **alert บน burn rate ของ error budget ไม่ใช่ raw threshold** — นี่คือกุญแจกัน noise:
  - **multi-window, multi-burn-rate**: fast burn (เช่น 14.4× budget ใน 1h window + 5m window ยืนยัน) → page; slow burn (เช่น 3× ใน 6h) → ticket
  - 2 window (long + short) กัน flapping: long window จับว่า "เผาจริง", short window กัน alert ค้างหลังหายแล้ว
- **ทุก alert ต้อง actionable**: มี runbook link, บอกว่าใคร impact, มี action ชัด — alert ที่ทำอะไรไม่ได้ = ลบ
- แยก **symptom-based** (user เจ็บจริง: error rate, latency สูง → page) ออกจาก **cause-based** (CPU สูง, disk เต็ม → ticket/warn) — page เฉพาะ symptom

### 7. Verify — sample query + trace จริง

- ดู Common Errors + Verify ด้านล่าง รัน end-to-end ก่อน declare done

## Common Errors

Gotcha จริงที่เจอซ้ำ — เช็คก่อน ship:

- **Cardinality bomb** — ใส่ user_id/request_id/raw error เป็น Prometheus label → series ระเบิด → Prometheus OOM/ช้า. แก้: label เป็น bounded set, route ใช้ template (`/users/:id`), error เก็บใน trace/log แทน
- **avg latency โกหก** — `avg(duration)` ซ่อน tail; p99 800ms แต่ avg 50ms = ผู้ใช้ 1% เจ็บแต่ dashboard เขียว. ใช้ `histogram_quantile` percentile เสมอ
- **histogram bucket ไม่ครอบ SLO** — SLO p99<300ms แต่ bucket กระโดด 0.1→0.5 → คำนวณ p99 ผิดเพราะ interpolate. ตั้ง bucket ให้มีขอบที่ threshold พอดี
- **trace ขาดตอน** — ลืม propagate `traceparent` ที่ boundary (async job, message queue, new HTTP client) → trace แตกเป็นหลายอัน หา root cause ไม่ได้. เช็คทุก outbound call ใส่ context
- **error span ดู green** — catch exception แล้วไม่ set span status ERROR → trace ดูปกติทั้งที่ fail. ต้อง `span.recordException` + set status
- **rate() บน gauge / sum บน histogram_bucket ผิด le** — `rate()` ใช้กับ counter เท่านั้น; `histogram_quantile` ต้อง `by (le, ...)` มี `le` เสมอ ไม่งั้นได้ NaN
- **alert บน raw threshold** (เช่น CPU>80%) → noisy, page ตอนตี 3 โดยไม่มี user เจ็บ. ย้ายไป burn-rate/symptom-based
- **counter ไม่มี `_total`, duration เป็น ms** → ผิด convention, query/recording rule พัง. base unit + suffix มาตรฐานเสมอ
- **log PII รั่ว** — ออก email/token/PII ลง log JSON → compliance/security incident. redact ก่อน emit
- **sampling กิน error traces** — head sampling 10% ทำให้ trace ของ incident หาย 90%. always-keep error/slow span
- **double-counting จาก label ที่หาย** — เปลี่ยน label set ของ metric เดิม → recording rule/alert คำนวณผิดช่วง transition. version metric หรือ migrate พร้อม recording rule

## Verify

ก่อน declare done ต้องผ่านทุกข้อ (มีหลักฐานจริง ไม่ใช่ "น่าจะได้"):

1. **Metrics scrape ได้** — `curl localhost:<port>/metrics` เห็น metric ที่ instrument + format ถูก (มี `_total`/`_seconds`, HELP/TYPE line). ตรวจ Prometheus target = `UP`
2. **PromQL ของ RED ทั้ง 3 คืนค่า** — รัน query rate/errors/duration จริง ได้ตัวเลข ไม่ใช่ empty/NaN; `histogram_quantile` มี `le` ครบ
3. **Cardinality check** — `count({__name__="<metric>"})` ดู series count สมเหตุผล (สิบ–พัน ไม่ใช่ แสน+); ยิง test request ด้วย id ต่างกันหลายตัว → series ต้องไม่เพิ่มตาม id
4. **Trace ครบ end-to-end** — ยิง request ผ่าน ≥2 service เห็น 1 trace เดียวเชื่อม span ครบ ใน tracing backend; error case → span status = ERROR + exception ติด
5. **Log↔trace correlation** — เปิด log ของ request นั้น เห็น `trace_id` ตรงกับ trace; click จาก log ไป trace ได้
6. **Alert ยิงจริงตอนควรยิง** — trigger error/latency เกิน SLO (load test / fault inject) → burn-rate alert fire ภายใน window ที่ตั้ง; พอหาย → alert resolve (ไม่ค้าง)
7. **Alert เงียบตอนควรเงียบ** — spike สั้นๆ ใต้ burn-rate threshold → ไม่ page (กัน noise); confirm short+long window ทำงาน
8. **Dashboard อ่านออกตอน incident** — เปิด dashboard ระหว่าง fault inject เห็น RED panel เปลี่ยนชัด ชี้ไป root cause ได้
