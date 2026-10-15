---
name: paper-trading-ops
description: "Alpaca Paper Trading 환경에서 일일 포지션 점검, 주간 성과 집계, 월간 전략 리뷰를 실행합니다. Paper Trading API 전용."
argument-hint: "[daily|weekly|monthly] [--date YYYY-MM-DD]"
user-invocable: true
allowed-tools: "Read, Write, Bash, Grep"
---

# Paper Trading Ops Skill

> Paper Trading 일일/주간/월간 운영 루틴 전문가. Alpaca Paper Trading 환경에서 체계적인 운영을 수행합니다.
> **Alpaca Paper Trading API 전용** — 실계좌 API key 사용을 절대 금지합니다.

## 역할

Alpaca Paper Trading 환경에서 세 가지 운영 루틴(일일/주간/월간)을 수행합니다.
정량적 데이터 기반으로 포지션 현황을 점검하고, 성과를 집계하며,
전략 파라미터 재검토 판단을 내립니다.

## API 연결 안전 확인

모든 루틴 실행 전 반드시 수행:

```bash
# Paper Trading 엔드포인트 확인 (paper-api.alpaca.markets 이어야 함)
echo $ALPACA_BASE_URL
# 예상: https://paper-api.alpaca.markets

# 실계좌 URL 감지 시 즉시 중단
if echo $ALPACA_BASE_URL | grep -q "api.alpaca.markets" && \
   ! echo $ALPACA_BASE_URL | grep -q "paper-api"; then
  echo "ERROR: Live account URL detected. Aborting."
  exit 1
fi
```

## 수행 가능 작업

### 1. 일일 루틴 (`daily`)

`/paper-trading-ops daily`

실행 시점: 매일 장 마감 후 (16:30 ET 이후)

**1-1. 포지션 현황 점검**

```
조회 항목:
  - 보유 종목 목록 (심볼, 수량, 평균 매수가, 현재가)
  - 각 포지션의 미실현 손익 (P&L, %)
  - 포트폴리오 전체 시가 평가액
  - 현금 비중
  - 섹터별 비중 집계

이상 감지:
  - 단일 종목 비중 8% 초과 → 경고
  - 섹터 비중 25% 초과 → 경고
  - ATR 스탑 이하로 하락한 종목 → 청산 검토 알림
```

**1-2. 오늘의 시그널 점검**

```
파이프라인 실행 (Quick Scan 모드):
  - /scoring-engine 으로 보유 종목 점수 갱신
  - 점수 급락 종목 식별 (전일 대비 10점 이상 하락)
  - 신규 매수 후보 상위 3종목 출력 (레짐 허용 시)
```

**1-3. 리스크 점검**

```
현재 포트폴리오 낙폭 계산:
  - peak_value 대비 현재 가치
  - Level 0 (< 10%): 정상 운영 확인
  - Level 1 (10-15%): 경고 알림, 신규 진입 중단
  - Level 2 (15-20%): Defensive 모드 알림
  - Level 3 (> 20%): Emergency 알림 — /execution-planner emergency_liquidate 즉시 호출
```

**일일 보고서 형식**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Paper Trading 일일 보고서 <YYYY-MM-DD>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

포트폴리오 현황
  총 평가액:  $102,450  (+2.45%)
  현금 비중:  18.3%
  낙폭 레벨:  0 - Normal

보유 포지션 (5종목)
  AAPL   15주  $185.20  +3.2%   [HOLD]
  MSFT   10주  $412.50  +1.8%   [HOLD]
  GOOGL   5주  $178.30  -0.5%   [WATCH - 근접 스탑]

오늘의 시그널
  매수 후보: NVDA (복합점수 82), META (복합점수 79)
  레짐: Low-Vol Bull (81%) → 신규 진입 허용

리스크 경고
  없음
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 2. 주간 루틴 (`weekly`)

`/paper-trading-ops weekly`

실행 시점: 매주 금요일 장 마감 후

**2-1. 주간 성과 집계**

```
집계 항목:
  - 주간 수익률 (절대, 벤치마크 대비 SPY)
  - 주간 거래 건수 (매수/매도)
  - 평균 보유 기간
  - 승리 거래 / 패배 거래 비율
  - 최대 단일 거래 P&L (승/패)
  - 거래 비용 총합 (수수료 + 슬리피지 추정)
```

**2-2. 전략별 기여도 분석**

| 전략 | 기여 종목 수 | 주간 P&L | 승률 | 비고 |
|------|---------|---------|------|------|
| CANSLIM | ... | ... | ... | |
| Magic Formula | ... | ... | ... | |
| Dual Momentum | ... | ... | ... | |
| Trend Following | ... | ... | ... | |

**2-3. 레짐 적중률 확인**

```
이번 주 레짐 예측 정확도:
  - 예측 레짐 vs 실제 시장 움직임 비교
  - HMM 신뢰도 평균
  - 레짐 전환 발생 여부
```

**주간 보고서 저장**: `docs/paper-trading/weekly/<YYYY-WNN>.md`

### 3. 월간 루틴 (`monthly`)

`/paper-trading-ops monthly`

실행 시점: 매월 마지막 거래일

**3-1. 월간 성과 종합**

```
지표 계산:
  - 월간 수익률 (절대, 연율화)
  - Sharpe Ratio (월간, 연율화)
  - Maximum Drawdown (월간)
  - Calmar Ratio
  - 벤치마크 (SPY) 대비 초과 수익
  - 전략별 기여도 (Strategy Attribution)
```

**3-2. 전략 파라미터 재검토**

`/self-improver` 를 호출하여 개선 필요 여부 판단:

| 진단 지표 | 현재값 | 임계값 | 판정 |
|---------|------|--------|------|
| 레짐 정확도 | ... | 55% | ... |
| 시그널 IC | ... | 0.03 | ... |
| Kelly 효율 | ... | 70% | ... |
| 전략 상관관계 최대값 | ... | 0.7 | ... |
| MDD | ... | 15% | ... |

임계값 미달 항목이 있으면 `self-improver` 에 위임하여 파라미터 재검토 권고.

**3-3. 스윙 트레이딩 리밸런싱 실행**

```
월간 리밸런싱 체크리스트:
  [ ] 보유 포지션 중 스코어 하위 20% 종목 청산 검토
  [ ] 스코어 상위 후보 중 편입 여부 결정
  [ ] 섹터 비중 재조정 (25% 초과 섹터 존재 시)
  [ ] Kelly 파라미터 재계산 (변동성 추정 갱신)
```

**월간 보고서 저장**: `docs/paper-trading/monthly/<YYYY-MM>.md`

## 실패 처리

| 상황 | 처리 |
|------|------|
| 실계좌 API URL 감지 | 즉시 중단, 환경변수 확인 안내 |
| Alpaca API 응답 오류 | 오류 코드와 메시지 출력, 재시도 1회 |
| 포지션 데이터 없음 | 빈 포트폴리오 보고서 생성, 경고 출력 |
| 낙폭 20% 초과 감지 | 즉시 Emergency 알림 출력, 자동 청산은 사용자 확인 후 |
| 보고서 저장 실패 | 콘솔에 전문 출력, 수동 저장 안내 |

## 출력 포맷

```json
{
  "skill": "paper-trading-ops",
  "status": "success",
  "data": {
    "routine": "daily",
    "date": "2026-03-03",
    "mode": "paper",
    "api_endpoint": "https://paper-api.alpaca.markets",
    "portfolio": {
      "total_value": 102450.00,
      "cash_pct": 0.183,
      "positions_count": 5,
      "unrealized_pnl_pct": 0.0245
    },
    "drawdown": {
      "current_pct": -0.032,
      "level": 0,
      "level_name": "Normal"
    },
    "signals": {
      "buy_candidates": ["NVDA", "META"],
      "regime": "Low-Vol Bull",
      "regime_confidence": 0.81
    },
    "alerts": [],
    "report_path": null
  }
}
```

## 제약 조건

- Alpaca Paper Trading API(`paper-api.alpaca.markets`)만 사용한다
- 실계좌 API key(`ALPACA_API_KEY` 환경변수가 실계좌용인 경우) 사용을 절대 금지한다
- 모든 루틴 시작 전 `ALPACA_BASE_URL`에 `paper-api` 포함 여부를 검증한다
- 낙폭 20% 초과 시 자동 청산 명령을 직접 실행하지 않고 사용자 확인을 요청한다
- 보고서 파일은 `docs/paper-trading/` 하위 경로에만 저장한다
- 월간 파라미터 재검토는 판단만 하고 실제 변경은 `self-improver` 에 위임한다

## 참조 문서

- `docs/api-technical-feasibility.md` — Alpaca Paper Trading API 연동 상세
- `docs/verified-methodologies-and-risk-management.md` §4-§5 — 리스크 한도 및 낙폭 방어
- `docs/strategy-recommendation.md` §3 — 운영 시간축 (스윙/포지션 리밸런싱 주기)
- `.claude/skills/self-improver/SKILL.md` — 파라미터 재검토 위임 대상
- `.claude/skills/performance-analyst/SKILL.md` — 월간 성과 어트리뷰션 위임 대상
- `.claude/skills/trading-orchestrator/SKILL.md` — Portfolio Review 워크플로 참조
