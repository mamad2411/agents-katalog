---
name: chaos-engineering-gameday
category: sre
description: "Chaos Engineering GameDay 가이드 — GameDay 운영, 모니터링, 알림 Use when working with sre 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Chaos Engineering GameDay 가이드

GameDay 운영, 모니터링, 알림

## GameDay 운영

### GameDay 체크리스트

```markdown
## Pre-GameDay
- [ ] 시나리오 정의 및 문서화
- [ ] Steady State 지표 정의 (SLI 기반)
- [ ] 롤백 절차 준비
- [ ] 참가자 알림 및 역할 배정
- [ ] 모니터링 대시보드 준비
- [ ] 알림 채널 음소거 (필요시)

## During GameDay
- [ ] 시작 전 Steady State 확인
- [ ] 단계별 실험 실행
- [ ] 실시간 모니터링
- [ ] 이슈 발생 시 즉시 롤백
- [ ] 관찰 내용 기록

## Post-GameDay
- [ ] 결과 분석 및 문서화
- [ ] 발견된 이슈 티켓 생성
- [ ] 개선 사항 우선순위 지정
- [ ] 회고 미팅
- [ ] 다음 GameDay 계획
```

### GameDay 시나리오 예시

```yaml
# gameday-scenario.yaml
name: "Order Service Resilience"
date: "2024-01-20"
duration: "2 hours"
participants:
  - role: "Facilitator"
    name: "SRE Team Lead"
  - role: "Observer"
    name: "Backend Engineers"

steady_state:
  - metric: "Order Success Rate"
    threshold: "> 99.9%"
    query: "sum(rate(orders_total{status='success'}[5m])) / sum(rate(orders_total[5m]))"
  - metric: "P99 Latency"
    threshold: "< 500ms"
    query: "histogram_quantile(0.99, rate(order_duration_seconds_bucket[5m]))"

experiments:
  - name: "Single Pod Failure"
    hypothesis: "Order service는 1개 Pod 실패 시에도 99.9% 성공률 유지"
    chaos:
      type: pod-delete
      target: order-service
      params:
        pods_affected: 1
    expected_result: "자동 복구, SLO 유지"
    blast_radius: "1 pod (of 3)"

  - name: "Database Latency"
    hypothesis: "DB 100ms 추가 지연 시에도 P99 1초 미만"
    chaos:
      type: network-latency
      target: postgresql
      params:
        latency_ms: 100
    expected_result: "지연 증가하나 SLO 내"
    blast_radius: "DB connections"

  - name: "Full AZ Failure"
    hypothesis: "1개 AZ 장애 시에도 서비스 지속"
    chaos:
      type: az-failure-simulation
      target: ap-northeast-2a
    expected_result: "다른 AZ로 트래픽 전환"
    blast_radius: "33% of capacity"

rollback_procedure: |
  1. ChaosEngine 삭제: kubectl delete chaosengine -n production --all
  2. Pod 재시작: kubectl rollout restart deployment/order-service
  3. 상태 확인: kubectl get pods -n production
```

### 실험 스케줄링 (CI/CD 통합)

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosSchedule
metadata:
  name: weekly-chaos
  namespace: litmus
spec:
  schedule:
    now: false
    repeat:
      # 매주 화요일 오전 10시
      minChaosInterval: "168h"
      timeRange:
        startTime: "10:00"
        endTime: "12:00"
      workDays:
        includedDays: "Tue"
  engineTemplateSpec:
    appinfo:
      appns: staging
      applabel: "app=order-service"
      appkind: deployment
    engineState: active
    chaosServiceAccount: litmus-admin
    experiments:
      - name: pod-delete
        spec:
          components:
            env:
              - name: TOTAL_CHAOS_DURATION
                value: "30"
```

---

## 모니터링 & 알림

### Prometheus 메트릭

```promql
# Chaos 실험 상태
litmuschaos_experiment_result{result="Pass"}
litmuschaos_experiment_result{result="Fail"}

# 실험 지속 시간
litmuschaos_experiment_duration_seconds

# 영향받은 Pod 수
litmuschaos_affected_pods_count
```

### Grafana 대시보드

```json
{
  "panels": [
    {
      "title": "Chaos Experiment Status",
      "targets": [{
        "expr": "litmuschaos_experiment_result",
        "legendFormat": "{{experiment_name}} - {{result}}"
      }]
    },
    {
      "title": "Service Health During Chaos",
      "targets": [{
        "expr": "rate(http_requests_total{status!~\"5..\"}[1m]) / rate(http_requests_total[1m])",
        "legendFormat": "Success Rate"
      }]
    }
  ]
}
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 프로덕션 첫 실험 | 서비스 장애 | 스테이징부터 시작 |
| Steady State 없음 | 성공/실패 판단 불가 | SLI 기반 지표 정의 |
| 롤백 계획 없음 | 장애 확대 | 롤백 절차 사전 준비 |
| 모니터링 없이 실험 | 영향 파악 불가 | 대시보드 준비 |
| 너무 큰 폭발 반경 | 심각한 장애 | 작은 범위부터 시작 |
| GameDay 기록 안함 | 지식 손실 | 실시간 기록 및 문서화 |
| 회고 미실시 | 개선 없음 | Post-GameDay 회고 필수 |

---

## 체크리스트

### GameDay 준비
- [ ] 시나리오 문서화
- [ ] 참가자 역할 배정 (Facilitator, Observer)
- [ ] Steady State 지표 정의
- [ ] 롤백 절차 문서화
- [ ] 모니터링 대시보드 준비

### 실험 실행
- [ ] 스테이징 환경 먼저 검증
- [ ] 단계적 실험 (작은 범위 -> 넓은 범위)
- [ ] Probe 설정 (성공/실패 자동 판정)
- [ ] 실시간 모니터링 및 기록

### 사후 분석
- [ ] 결과 분석 및 문서화
- [ ] 발견된 이슈 티켓 생성
- [ ] 개선 사항 우선순위 지정
- [ ] 회고 미팅 실시
- [ ] 다음 GameDay 일정 수립

---

## Sources

- [LitmusChaos Documentation](https://docs.litmuschaos.io/)
- [Principles of Chaos Engineering](https://principlesofchaos.org/)
- [GameDay Best Practices](https://aws.amazon.com/blogs/devops/automating-safe-hands-off-deployments/)

---

## 참조 스킬

- `/chaos-engineering` - Chaos Engineering 기본 가이드 (LitmusChaos, 실험, Probe)
- `/sre-sli-slo` - SLI/SLO 기반 Steady State 정의
- `/load-testing` - 부하 테스트
- `/monitoring-troubleshoot` - 모니터링 트러블슈팅
