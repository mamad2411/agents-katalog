---
name: shopping-monitor
description: "상품/사이트 모니터링 등록, 조회, 취소, 즉시 확인. 뉴스 알림(출시·발표), 가격 알림(목표가 이하), 이벤트 알림(할인 쿠폰·특가). 예: '맥미니 M5 출시 소식 알려줘', '에어팟 15만원 이하면 알려줘', '쿠팡에서 특가 이벤트 생기면 알려줘'"
metadata:
  {
    "openclaw":
      {
        "emoji": "🛒",
        "requires": { "bins": ["curl"] }
      }
  }
---

# Shopping Monitor Skill

> **IMPORTANT**: For EVERY user request, you MUST call the `exec` tool to run the curl command first.
> Do NOT respond before exec is called — you have no knowledge of registration state without the webhook call.

사용자 요청을 받아 3가지 유형의 모니터링을 등록하고 관리한다.

| type | 설명 | 예시 요청 |
|------|------|----------|
| `news` | 제품/토픽 뉴스·출시 감지 | "맥미니 M5 출시 소식 알려줘" |
| `price` | 목표가 이하 도달 시 알림 | "에어팟 프로 15만원 이하면 알려줘" |
| `event` | 사이트 할인 쿠폰·특가 감지 | "쿠팡에서 특가 이벤트 생기면 알려줘" |

지원 액션: `register` · `list` · `cancel` · `check-now`

All requests use: `POST "${N8N_WEBHOOK_BASE_URL}?type=shopping&mode=monitor&action={action}"`

---

## Action Mapping

| 사용자 의도 | action |
|------------|--------|
| ~알려줘, ~되면 알려줘, 추적해줘, 모니터링해줘 | `register` |
| 목록 보여줘, 내가 등록한 것, 뭐 추적 중이야 | `list` |
| 취소, 삭제, 그만 봐, 추적 해제 | `cancel` |
| 지금 확인해줘, 현재 상태 어때, 지금 얼마야 | `check-now` |

---

## Required Fields per type

### type=news (뉴스·출시 감지)

| Field | Key | Format | 필수 |
|-------|-----|--------|------|
| 타입 | type | `"news"` | ✅ |
| 검색 키워드 | name | string | ✅ |

예: `{"type":"news","name":"맥미니 M5"}`

### type=price (가격 추적)

| Field | Key | Format | 필수 |
|-------|-----|--------|------|
| 타입 | type | `"price"` | ✅ |
| 제품명 | name | string | ✅ |
| 목표가 | target_price | number (원 단위) | ✅ |
| 제품 URL | url | string | ❌ (있으면 정확도 향상) |

예: `{"type":"price","name":"에어팟 프로 4세대","target_price":150000}`

### type=event (사이트 이벤트 감지)

| Field | Key | Format | 필수 |
|-------|-----|--------|------|
| 타입 | type | `"event"` | ✅ |
| 사이트명 또는 URL | name | string (사이트명) | ✅ |
| 사이트 URL | url | string | ❌ (있으면 더 정밀) |

- 사이트명만 있으면: `{"type":"event","name":"쿠팡"}`
- URL도 있으면: `{"type":"event","name":"쿠팡","url":"https://www.coupang.com"}`

---

## Field Collection Rules

- `target_price` 누락 시 (price 타입): "얼마 이하면 알림을 드릴까요?" 질문
- `name` 누락 시: 타입에 맞게 질문
  - news: "어떤 제품이나 키워드를 모니터링할까요?"
  - price: "어떤 제품을 추적할까요?"
  - event: "어느 사이트를 모니터링할까요? (사이트명 또는 URL)"
- `cancel` 시 후보가 여러 개이면 목록을 먼저 보여주고 확인 요청

---

## action=register

```bash
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=shopping&mode=monitor&action=register" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"type":"news","name":"맥미니 M5"}'
```

**Success**: `status === "ok"` AND `message` field present.

등록 완료 메시지를 전달하고, 등록된 항목 요약 (타입, 이름, 목표가 있을 경우)을 함께 안내.

**Failure**: `status` ≠ `"ok"` → 등록 실패 안내. `message` 필드 포함.

---

## action=list

```bash
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=shopping&mode=monitor&action=list" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{}'
```

**Success**: `status === "ok"` AND `items` array present.

`items` 배열을 타입별로 구분하여 표시:
- news: `📰 [키워드] 뉴스 감지 모드 | 등록일: {added_at}`
- price: `💰 [제품명] 목표가: {target_price}원 | 최근가: {current_price}원 | 등록일: {added_at}`
- event: `🎉 [사이트명] 이벤트 감지 모드 | 등록일: {added_at}`

추적 항목이 없으면 "현재 모니터링 중인 항목이 없습니다." 안내.

**Failure**: `status` ≠ `"ok"` → 조회 실패 안내.

---

## action=cancel

```bash
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=shopping&mode=monitor&action=cancel" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"name":"맥미니 M5"}'
```

**Success**: `status === "ok"` → "{name} 모니터링을 취소했습니다." 안내.

**Failure**: `status` ≠ `"ok"` → 취소 실패 안내. `message` 필드 포함 (항목 없음 등).

---

## action=check-now

```bash
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=shopping&mode=monitor&action=check-now" \
  -H "Content-Type: application/json" \
  --max-time 60 \
  -d '{"name":"맥미니 M5"}'
```

**Success**: `status === "ok"` AND `result` field present.

결과 표시:
- news: `result.summary` (최신 소식 요약)
- price: `result.price` (현재가), `result.source` (출처), `result.confidence`가 `"low"`이면 "불확실 — 직접 확인 권장" 추가
- event: `result.summary` (현재 진행 중인 이벤트 요약)

**Failure**: `status` ≠ `"ok"` → 확인 실패 안내.

---

## Language

항상 한국어로 응답.
