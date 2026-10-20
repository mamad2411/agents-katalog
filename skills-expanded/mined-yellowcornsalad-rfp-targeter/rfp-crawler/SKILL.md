---
name: rfp_crawler
description: RFP-Targeter 크롤러가 정상 작동 중인지 검증. 주간 시간(평일 09~21 KST) 안에 마지막 크롤이 1시간 이내였는지 확인. 비주간 시간은 점검 skip. GitHub Actions monitor_crawler.yml 이 30분마다 같은 로직으로 자동 실행 + 이상 시 슬랙 알림.
---

# rfp_crawler — 크롤러 헬스 모니터링

## 목적

RFP-Targeter는 GitHub Actions cron 으로 매시 정각 크롤링되어야 한다. 그러나 IITP timeout / 어댑터 hang / 정부 사이트 응답 지연 등으로 cron 이 cancelled 되면 사용자는 알 수 없게 된다.

이 스킬은 다음을 검증한다:

1. **주간 시간 (평일 09~21 KST)** 에 한해 검증 (외 시간은 cron 안 돌아도 정상)
2. **마지막 크롤 시각** (`fetch_log` 의 가장 최근 `finished_at`) 이 1시간 이내인지
3. **GitHub Actions crawl.yml** 최근 5건 conclusion 에 `cancelled` / `failure` 가 있는지
4. **활성 보안 공고 score NULL** 발생 여부 (안전망 효과 확인)
5. **슬랙 누락 후보** (영업시간이라면 즉시 dispatch)
6. **활성 source 연속 0건** — 최근 3회 크롤 연속 `new+updated=0` 인 source (특정 source
   silent 장애. 크롤 전체는 성공해 2·3번으론 안 잡힘. 예: MSS data.go.kr 일 한도 429)

## 실행 방법

### 수동 호출 (Claude Code 안에서)

```
사용자: "크롤러 상태 점검해줘" / "rfp_crawler"
→ Claude 가 scripts/monitor_crawler.py 실행 + 결과 보고
```

### 자동 실행 (GitHub Actions)

`.github/workflows/monitor_crawler.yml` 이 평일 09~21 KST (UTC 0~12시) 매 30분 cron 으로 발화. 이상 발견 시 슬랙 webhook 으로 알림 발사. 사용자 PC OFF 와 무관, 365일 작동.

## 점검 절차 (6단계)

```python
# 0. 만료 공고 자동 dismiss (soft delete) — 슬랙·사이트 노출 자동 차단
UPDATE announcement SET is_dismissed = TRUE
  WHERE is_dismissed = FALSE
    AND deadline_at < CURRENT_DATE::text
# is_dismissed=FALSE 만 슬랙·UI 조회 → 자동 제외. DB row 는 보존 (회고용).

# 1. 현재 시각 평일 09~21 KST 인지
now = datetime.now(ZoneInfo("Asia/Seoul"))
is_business = now.weekday() < 5 and 9 <= now.hour <= 21
if not is_business:
    return "skip — 비주간 시간"

# 2. fetch_log 최근 finished_at (UTC) 가져와 KST 변환
last_run = SELECT MAX(finished_at) FROM fetch_log WHERE finished_at IS NOT NULL
gap_minutes = (now_utc - last_run).total_seconds() / 60

# 3. 임계 검증
if gap_minutes > 60:
    alert = "🚨 크롤러 정지 — 마지막 정상 크롤 {gap}분 전"

# 4. GitHub Actions 최근 5 run conclusion
recent = gh run list --workflow=crawl.yml --limit 5
if 2+ cancelled in last 5:
    alert += " · cron cancelled 패턴 감지"

# 5. score NULL / 슬랙 누락 후보
null_score = COUNT WHERE is_security AND score IS NULL AND active
pending = COUNT WHERE total_score >= 80 AND budget_mw >= 100 AND alerted_at IS NULL
if pending > 0 and is_business:
    dispatch_pending_alerts()
```

## 이상 신호 분류

> [2026-06-01 사용자 결정 — 슬랙 최소화] **슬랙은 '데이터 지연(staleness)'만** 발사.
> 취소 패턴·source 연속 0건·score NULL 은 **출력/홈페이지 배지**에서만 확인 (슬랙 X).
> 크롤이 데이터를 계속 갱신하는 한(홈페이지 정상) 슬랙은 조용 → 홈페이지와 상태 일치.

| 신호 | 임계 | 조치 |
|------|------|------|
| **만료 공고 (deadline < today)** | **1건+** | **`is_dismissed=TRUE` soft delete 자동 처리** |
| `last_finished` 가 70분 초과 | 데이터 지연 | **🔔 슬랙 알림** + `gh workflow run crawl.yml` 자동 dispatch |
| `crawl.yml` 최근 5건 중 2건+ cancelled | 패턴화된 timeout | 출력만 (슬랙 X — 자체복구 가능, 지연되면 위 항목이 잡음) |
| `score NULL` 활성 공고 발견 | 1건+ | 출력만 + `python scripts/backfill_scores.py` |
| 슬랙 누락 후보 (영업시간) | 1건+ | `dispatch_pending_alerts()` 즉시 호출 (액션) |
| 활성 source 연속 0건 수집 | 최근 3회 `new+updated=0` | **🖥 홈페이지 배지 '일부 수집 중단' 표시** (슬랙 X) — `recent_zero_yield_sources()` 공유 판정 |

### 만료 공고 자동 dismiss 동작

```
deadline_at < CURRENT_DATE 인 공고 → is_dismissed=TRUE
  ├─ 슬랙 알림: 자동 제외 (dispatch_pending_alerts SQL이 is_dismissed=FALSE 만 조회)
  ├─ 정적 사이트: 자동 제외 (build_static.py SQL 동일)
  ├─ DB row: 보존 (회고·통계·과거 매칭 키워드 데이터)
  └─ 복구: UPDATE announcement SET is_dismissed=FALSE WHERE id=...
```

비주간 시간에도 dismiss 단계는 실행됨 (즉 비영업시간에도 만료 정리는 한다). 점검·알림만 영업시간 제한.

## 슬랙 알림 메시지 형식

```
🚨 [RFP-Targeter 모니터] 2026-05-27 14:30 KST

크롤러 정지 감지 — 마지막 정상 완료 87분 전 (12:43)
원인 추정: IITP 어댑터 timeout (max_per_source 50)

GitHub Actions 최근 5 run:
  · 14:00 — cancelled (30분 timeout)
  · 13:00 — success
  · 12:00 — cancelled
  · 11:00 — success
  · 10:00 — success

조치 권장:
  1. gh workflow run crawl.yml --ref main  (수동 트리거)
  2. 또는 IITP max_per_source 추가 축소 (50 → 30)
```

## 알려진 회귀 패턴

`feedback_recurring_checks.md` 의 5번 항목과 연계 — 이 스킬이 자동 점검 부분을 담당.

- **IITP timeout 재발** — max_per_source 50 적용 후에도 가끔 30분 초과. 정부 사이트 응답 시간 변동.
- **NIPA 어댑터 hang** — 본문 `<header><nav>` 안에 있어 decompose 순서 중요. 안 풀리면 5/22~5/24처럼 며칠 동안 새 데이터 0건.
- **KOICA OpenAPI 죽음** — 2026-05 이후 unreachable. enabled=false 상태라 정상.
- **G2B 401 Unauthorized** — service_key 활용신청 미승인.

## 관련 파일

- `scripts/monitor_crawler.py` — 실제 점검 로직 (스킬과 워크플로우가 공유)
- `.github/workflows/monitor_crawler.yml` — 30분마다 자동 실행
- `src/rfp_targeter/pipeline.py` — `_verify_required_sources`, `_backfill_missing_scores`, `dispatch_pending_alerts`
