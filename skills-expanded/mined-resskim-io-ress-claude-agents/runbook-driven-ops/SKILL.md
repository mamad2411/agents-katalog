---
name: runbook-driven-ops
category: operations
description: SRE Runbook 표준 + 실행 자동화 — preventive/reactive/recovery/change 분류, 작성 템플릿(trigger/prereq/steps/verify/rollback/escalation), 자동화 단계(수동→semi→auto-remediation), MTTR/false-trigger 메트릭, on-call 핸드오프, alert↔runbook drift 방지(CI). Phase 안정화·on-call 표준화 hub.
license: MIT
---

# Runbook-Driven Ops — 운영 표준화 hub

운영 사고와 변경 작업의 재현 가능성을 보장하는 Runbook 표준. 알림(Alert)이 runbook을 가리키고, runbook이 단계별 검증 가능한 명령으로 구성되며, 실행 결과가 audit + 메트릭으로 누적되는 closed loop을 만든다.

> 이 skill은 운영 표준화 hub. **인시던트 대응 흐름**(Detect → Triage → Investigate → Mitigate)은 `observability/observability-incident-playbook.md`. **사고 회고**는 `operations/incident-postmortem.md`. **장애 주입**으로 runbook을 검증하려면 `sre/chaos-engineering.md`.

## When to Use

- 알림에 대응 가능한 SOP가 없는 상태에서 on-call 시작
- 같은 장애를 매번 다른 사람이 다른 방식으로 해결 → 표준화 필요
- "이 runbook 정말 동작해?" 검증되지 않은 wiki 문서를 운영 표준으로 끌어올리기
- 알림에 link 걸린 runbook이 사라지거나 outdated (drift 방지)
- 수동 운영 → semi-auto → full-auto 점진 자동화 로드맵
- on-call 핸드오프에서 컨텍스트 손실
- Phase 1 안정화 — 운영 표준화 본격화
- chaos engineering 결과를 runbook으로 환류

**관련 skill (cross-link)**:
- `observability/observability-incident-playbook.md` — 인시던트 5단계 대응 흐름
- `operations/incident-postmortem.md` — 사고 회고 + action item으로 runbook 추가/개선
- `sre/chaos-engineering.md` — runbook 동작 검증 game-day
- `sre/sre-sli-slo.md` — SLO 위반 시 트리거되는 reactive runbook
- `observability/aiops-remediation.md` — 자동화 단계 3~4 (auto-suggested / auto-remediation)
- `observability/alerting-discord.md` — alert→runbook link 강제
- `cicd/deployment-strategies.md` — change runbook (canary/blue-green 절차)
- `platform/golden-paths.md` — 신규 서비스 runbook 템플릿 자동 생성

**관련 agent**: `incident-responder`, `k8s-troubleshooter`, `debugging-expert`, `tech-lead`
**관련 skill**: [`observability-otel`](../observability-otel/SKILL.md), [`broker-troubleshooting`](../broker-troubleshooting/SKILL.md)

---

## 1. Runbook 분류 매트릭스

| 분류 | 트리거 | 예시 | 자동화 가능성 | 검증 주기 |
|---|---|---|---|---|
| **Preventive** | 정기 / 임계값 임박 | 디스크 80% 도달 시 정리 | 매우 높음 (cron) | 분기 |
| **Reactive** | 알림 발생 | SSE 단절률 5% 초과 | 중 (semi-auto) | 분기 (chaos game-day) |
| **Recovery** | 장애 후 복구 | DB primary 장애 → replica promotion | 낮음 (수동 + 검증 강함) | 반기 (DR 훈련) |
| **Change** | 계획된 변경 | DB 마이그레이션, K8s upgrade | 중 (Argo Workflow) | 변경 직전 dry-run |

> 분류가 다르면 **자동화 전략**과 **검증 주기**가 달라진다. 같은 템플릿으로 통일 X.

---

## 2. 작성 표준 템플릿

```markdown
---
runbook_id: rb-tracking-sse-001
title: Tracking SSE 단절률 급증 대응
severity: SEV2
category: reactive
trigger_alert: SSEDisconnectRateHigh
estimated_duration: 15m
last_verified: 2026-04-15
verified_by: tracking-team
owner: tracking-team
---

## Trigger
- 알림: `SSEDisconnectRateHigh` (Discord/PagerDuty)
- 메트릭: `rate(sse_disconnects_total[5m]) > 0.05`
- 영향: 학부모 앱 위치 표시 멈춤 → SEV2

## Prerequisites
- [ ] kubectl 접근 권한 (eodini-system namespace)
- [ ] Grafana 대시보드 접근 (Tracking)
- [ ] Discord #eodini-incident 채널
- [ ] (자동화 시) StackStorm role: incident-responder

## Steps
1. **영향 범위 확인** (5분)
   - Grafana → Tracking dashboard → SSE Active Connections
   - 정상: ~500 / 현재: ?
   - p95 latency 추세

2. **최근 배포 확인**
   ```
   kubectl rollout history -n eodini-system deploy/tracking-service
   ```

3. **Pod 상태 점검**
   ```
   kubectl get pods -n eodini-system -l app=tracking-service
   kubectl logs -n eodini-system -l app=tracking-service --tail=200
   ```
   - CrashLoopBackOff / OOMKilled 여부

4. **Redis 연결 점검** (SSE state)
   ```
   redis-cli -h $REDIS_HOST PING
   redis-cli -h $REDIS_HOST INFO clients
   ```

5. **Mitigation 결정 분기**
   - Pod OOM → resource 증액 + 재배포
   - Redis 끊김 → Redis 점검 (별도 runbook `rb-redis-001`)
   - 트래픽 급증 → HPA 수동 스케일

## Verification
- [ ] SSE Active Connections 정상치(±10%) 5분 유지
- [ ] p95 latency < 200ms
- [ ] 학부모 앱 sample test (10명 위치 표시 정상)
- [ ] 알림 자동 해제 (5분 hysteresis)

## Rollback
- 배포 원인이면: `kubectl rollout undo -n eodini-system deploy/tracking-service`
- 트래픽 원인이면: HPA 임계 원복

## Escalation
- 30분 내 미해결 → Tracking 팀 리드 호출
- 1시간 → CTO + 학부모 공지 (status page)
- 사용자 1만+ 영향 → SEV1 승격 + war room

## Related
- `rb-redis-001` — Redis 장애 대응
- `rb-tracking-mqtt-001` — MQTT broker 장애
- Postmortem template: `operations/incident-postmortem.md`
```

> **Steps는 검증 가능한 명령**으로. "확인한다", "점검한다" 같은 모호한 동사 금지.

---

## 3. 명명 규칙 + 디스커버리

### 3.1 Runbook ID 규칙

```
rb-{service}-{symptom-or-action}-{seq}

rb-tracking-sse-001         # Tracking SSE 단절
rb-mqtt-restart-001         # MQTT broker 재시작
rb-kafka-lag-001            # Kafka consumer lag
rb-fcm-push-fail-001        # FCM 발송 실패
rb-change-db-migration      # 변경 (DB 마이그레이션)
rb-recovery-pg-failover     # 복구 (Postgres failover)
```

### 3.2 위치

GitOps repo `runbooks/{service}/{id}.md`. wiki에 두면 drift 발생.

### 3.3 알림 → Runbook Link

Prometheus AlertManager annotation:

```yaml
- alert: SSEDisconnectRateHigh
  expr: rate(sse_disconnects_total[5m]) > 0.05
  for: 2m
  annotations:
    summary: "SSE 단절률 5% 초과"
    runbook_url: https://runbooks.eodini.io/tracking/rb-tracking-sse-001
```

---

## 4. 실행 자동화 단계

| 단계 | 동작 | 도구 | 위험 |
|---|---|---|---|
| **0. Manual** | 사람이 명령 복붙 | wiki + grafana | 오타·누락 |
| **1. Doc-Driven** | runbook md 보면서 실행 | doc + cli | 표준화 부족 |
| **2. Semi-Auto** | 사람이 트리거, 명령은 자동 | bash script, ansible playbook, Argo Workflow | 검증 부족하면 사고 확대 |
| **3. Auto-Suggested** | 알림에 자동 가설+수정안 제시 | aiops-remediation | LLM 환각 |
| **4. Auto-Remediation** | 알림 → 자동 실행 (사람 사후 검증) | StackStorm, Rundeck, Argo Events | false-trigger 폭주 |

> **단계 상승 조건**: 직전 단계 30회 무사고 + chaos game-day 검증 + 롤백 자동화. 검증 없이 4단계로 점프 금지.

### 4.1 자동화 후보 식별

| 기준 | 점수 |
|---|---|
| 발생 빈도 (월 N회) | 높을수록 자동화 가치 ↑ |
| 평균 처리 시간 | 길수록 자동화 가치 ↑ |
| 위험도 (사고 확대 가능성) | 높을수록 자동화 위험 ↑ |
| 컨텍스트 의존성 | 의존성 높을수록 자동화 어려움 |
| 가역성 | 비가역 작업은 자동화 금지 (DB drop 등) |

---

## 5. 도구 비교

| 도구 | 강점 | 약점 | 추천 단계 |
|---|---|---|---|
| **Ansible Playbook** | 보편적, idempotent 추구 | 멱등성 직접 챙김, K8s 통합 약함 | 2~3 |
| **StackStorm** | 이벤트 기반 자동화, 풍부한 integration | 학습곡선 가파름 | 3~4 |
| **Argo Workflows** | K8s 네이티브, GitOps 친화 | 운영자 친숙성 낮음 | 2~3 (change runbook) |
| **Rundeck** | UI/RBAC 잘 갖춤 | OSS 활성도 둔화 | 2~3 |
| **GitHub Actions** | 익숙함, 무료 | 운영 자동화 도구 아님 | 1~2 (change) |
| **Custom shell** | 빠른 시작 | 표준화·관측·롤백 모두 직접 | 0~1 |

> eodini는 ArgoCD 운영 중 → **Argo Workflows + StackStorm** 조합 권장.

---

## 6. 실행 메트릭

```promql
# MTTR (Mean Time To Recover) - reactive runbook
histogram_quantile(0.95,
  sum by (le, runbook_id) (
    rate(runbook_execution_duration_seconds_bucket{category="reactive"}[7d])
  )
)

# Success rate
sum(rate(runbook_execution_total{result="success"}[7d])) by (runbook_id)
  / sum(rate(runbook_execution_total[7d])) by (runbook_id)

# False-trigger rate (auto run이 실제 변경 0건)
sum(rate(runbook_execution_total{trigger="auto", outcome="no_change_needed"}[7d]))
  / sum(rate(runbook_execution_total{trigger="auto"}[7d]))

# Stale runbooks (last_verified > 90일)
runbook_last_verified_days_ago > 90
```

### 6.1 메트릭 소스

- `runbook_execution_total{runbook_id, trigger, result, outcome}` (counter)
- `runbook_execution_duration_seconds` (histogram)
- `runbook_last_verified_days_ago{runbook_id}` (gauge, CI에서 매일 갱신)

---

## 7. On-Call 핸드오프 통합

### 7.1 핸드오프 회의 의제

```
[월요일 10:00 — 30분]
1. 지난 주 인시던트 요약 (5분)
2. 오픈 인시던트 + 진행 중 runbook 실행 (10분)
3. 새/수정된 runbook 공유 (5분)
4. last_verified 만료 임박 runbook (3분)
5. 다음 주 예정 change (5분)
```

### 7.2 Runbook 실행 audit

```
audit log:
  who: who triggered (human user_id 또는 system)
  what: runbook_id, version (commit hash)
  when: started_at, ended_at
  why: alert_id 또는 manual reason
  result: success / partial / failed
  changes: kubectl 명령 결과, DB 변경 등 diff
```

> audit log는 회고(`operations/incident-postmortem.md`)에 그대로 인용.

---

## 8. Drift 방지 — Alert ↔ Runbook 검증

### 8.1 CI 룰

- **모든 alert에 `runbook_url` 강제** — 없는 alert는 빌드 fail
- **runbook_url이 가리키는 파일 존재** 확인 (HEAD 요청 또는 GitOps repo 검증)
- **frontmatter `last_verified` 날짜 파싱** + 90일 초과 시 경고
- **runbook_id 중복 검사**

### 8.2 GitHub Actions 예시

```yaml
- name: Validate alert runbooks
  run: |
    set -e
    # 모든 alert가 runbook_url 보유
    yq '.. | select(.alert?) | select(.annotations.runbook_url == null)' \
      monitoring/alerts/*.yaml | grep -q . && {
      echo "Alert without runbook_url found"; exit 1;
    }

    # runbook_url 가리키는 파일 존재
    yq '.. | select(.annotations.runbook_url) | .annotations.runbook_url' \
      monitoring/alerts/*.yaml | while read url; do
      slug=$(basename "$url" .md)
      [ -f "runbooks/**/$slug.md" ] || { echo "Missing runbook: $url"; exit 1; }
    done

    # last_verified 90일 초과 검증
    python scripts/validate-runbook-freshness.py runbooks/
```

---

## 9. eodini 도메인 매핑

| 알림 / 변경 | Runbook ID | 분류 | 자동화 단계 |
|---|---|---|---|
| SSE 단절률 5% 초과 | `rb-tracking-sse-001` | reactive | 1 (doc-driven) |
| MQTT broker 재시작 | `rb-mqtt-restart-001` | recovery | 2 (semi-auto) |
| Kafka consumer lag 임계 | `rb-kafka-lag-001` | reactive | 3 (auto-suggested) |
| FCM 발송 실패율 1% 초과 | `rb-fcm-push-fail-001` | reactive | 1 |
| TimescaleDB 디스크 80% | `rb-timescale-disk-001` | preventive | 2 (auto cleanup cron) |
| Pod OOMKill 반복 (5회/h) | `rb-pod-oom-001` | reactive | 1 |
| ArgoCD sync 실패 | `rb-argocd-sync-001` | reactive | 1 |
| DB 마이그레이션 (스키마 변경) | `rb-change-db-migration` | change | 2 (Argo Workflow) |
| Postgres primary failover | `rb-recovery-pg-failover` | recovery | 1 (수동 + 검증) |
| Istio sidecar 수동 inject | `rb-istio-inject-fix` | reactive | 1 |
| 위치정보 즉시 파기 cron 실패 | `rb-purge-location-fail` | reactive | 1 (법적 의무 우선) |

---

## 10. 함정 (자주 빠뜨리는 것)

| 함정 | 결과 | 대응 |
|---|---|---|
| runbook 없이 알림 → on-call 첫 5분 손실 | MTTR 폭주 | alert에 runbook_url 강제 |
| "확인했음"만 적힌 runbook (절차 없음) | 실효 없음 | 검증 가능한 명령 강제 |
| copy-paste 위험 명령 (`rm -rf`, `DROP TABLE`) | 사고 확대 | dry-run 옵션 / 강제 확인 |
| `last_verified` 안 갱신 | outdated 명령 실행 | 90일 SLO + chaos game-day |
| 자동화에 사람 검증 단계 없음 | false-trigger 사고 | dry-run → manual approve → execute 단계 |
| runbook 권한 폭주 (모든 운영자가 prod 변경) | 무단 변경 | RBAC + 변경 audit |
| 알림 없는데 runbook만 존재 | 죽은 문서 | 분기마다 alert↔runbook 매핑 검증 |
| chaos engineering 결과 환류 안 함 | runbook 진화 정체 | game-day 후 PR 강제 |
| Recovery runbook을 자동화 (DB primary 등) | 비가역 실수 | 가역성 매트릭스 적용 |
| runbook을 wiki에 둠 | drift 폭주 | GitOps repo로 이전 |
| 한 runbook이 여러 alert을 cover | 진단 모호 | 1:1 매핑 권장 (또는 명시 분기) |
| alert 메시지에 명령어 직접 적음 (run 'X') | runbook 우회 | 모든 명령은 runbook 안에 |

---

## 11. 운영 체크리스트

### 표준화
- [ ] 모든 alert에 `runbook_url` annotation + CI 검증
- [ ] runbook 표준 template (trigger/prereq/steps/verification/rollback/escalation)
- [ ] runbook ID 규칙 (`rb-{service}-{symptom}-{seq}`)
- [ ] GitOps repo `runbooks/` 위치 + wiki에서 마이그레이션

### 자동화 로드맵
- [ ] 0→1 전환 (모든 운영 작업 doc-driven, wiki 미사용)
- [ ] 1→2 자동화 후보 식별 (빈도×시간×위험도×가역성)
- [ ] 자동화 권한 RBAC (semi-auto trigger 권한, full-auto 정책)
- [ ] 비가역 작업 자동화 금지 룰

### 메트릭·검증
- [ ] MTTR / success rate / false-trigger 대시보드
- [ ] last_verified 90일 SLO + 만료 임박 알림
- [ ] 핸드오프 회의 의제에 runbook audit 포함
- [ ] 분기마다 chaos game-day로 reactive/recovery runbook 검증

### 환류
- [ ] 회고(`operations/incident-postmortem.md`)에서 도출된 action items → runbook PR 강제
- [ ] chaos engineering 발견 → runbook 업데이트
- [ ] 새 alert 도입 시 runbook 동시 PR 강제 (CI block)

---

## 부록 A: 자주 묻는 질문

**Q. 새 alert를 만들면 runbook이 먼저인가, alert가 먼저인가?**
A. **runbook 먼저**. runbook이 검증 가능한 단계로 동작하면 그 시점부터 alert 활성화. 그 전엔 silent (or warning만).

**Q. 자동화(단계 4) 실행이 실패하면 어떻게?**
A. (1) 자동 롤백 트리거 (2) on-call 호출 + 수동 fallback runbook (단계 1) (3) auto-runbook 비활성화 검토. **자동화는 항상 fallback runbook을 가진다**.

**Q. 기존 wiki를 runbook으로 마이그레이션하려면?**
A. (1) 빈도 높은 wiki page 우선. (2) 표준 template로 변환 + 검증 가능 명령으로. (3) chaos game-day로 검증 후 alert과 link. (4) 나머지 wiki는 그대로 두되 신규 작성 금지.

**Q. chaos engineering 결과를 어떻게 runbook에 환류하나?**
A. game-day 직후 발견된 모든 실패는 (1) 새 runbook 생성, (2) 기존 runbook 단계 추가, (3) alert 임계치 조정 중 하나로 PR 발행. 미환류 발견은 다음 game-day에서 재검출됨.

**Q. 외주 운영팀에게 runbook을 어떻게 공유?**
A. GitOps repo read 권한 + RBAC으로 실행 권한은 단계별로. 외주는 단계 1~2 위주. 권한 범위는 분기마다 재검토.

**Q. runbook이 너무 많아지면 검색이 어려워지지 않나?**
A. ID 규칙(rb-{service}-{symptom}) + 알림에 직접 link → 검색 거의 불필요. 분기 정리로 outdated runbook 제거.

**Q. recovery runbook(예: DB failover)은 평소 검증 어려운데?**
A. (1) staging DR 훈련 (분기/반기). (2) prod 검증은 chaos engineering 의도적 fail-over. (3) 검증 없이 prod 시 실패 가능성 명시.

---

## 참고 자료

- Google SRE Book Chapter 11 (On-Call), Chapter 14 (Managing Incidents)
- Beyer et al. "The Site Reliability Workbook" — Runbook Adoption
- StackStorm / Rundeck / Argo Workflows 공식 문서
- PagerDuty Incident Response Documentation (오픈소스)
