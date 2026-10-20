---
name: aiops-remediation
category: observability
description: "AIOps: RCA & 자동 복구 — 근본 원인 분석 (RCA), 자동 복구 (Auto-Remediation) Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# AIOps: RCA & 자동 복구

근본 원인 분석 (RCA), 자동 복구 (Auto-Remediation)

## Quick Reference

```
RCA 방식?
    │
    ├─ LLM 기반 ──────────> 컨텍스트 수집 + GPT 분석
    │       │
    │       └─ 빠른 요약, 자연어 설명
    │
    └─ 인과 모델 ─────────> 의존성 그래프 + 전파 규칙
            │
            └─ 정확한 원인 추적, 반복 패턴

자동 복구?
    │
    ├─ Runbook 자동화 ────> 조건부 스크립트 실행
    └─ KEDA 스케일링 ─────> 메트릭 기반 자동 스케일
```

---

## 근본 원인 분석 (RCA)

### LLM 기반 RCA 자동화

```python
# rca_analyzer.py
from openai import OpenAI
from kubernetes import client, config
import json

class RCAAnalyzer:
    def __init__(self):
        self.llm = OpenAI()
        config.load_incluster_config()
        self.k8s = client.CoreV1Api()

    def analyze_incident(self, alert: dict) -> dict:
        # 1. 관련 데이터 수집
        context = self._gather_context(alert)

        # 2. LLM 분석
        analysis = self._llm_analyze(alert, context)

        # 3. 결과 구조화
        return {
            "incident": alert,
            "root_cause": analysis["root_cause"],
            "impact": analysis["impact"],
            "remediation": analysis["remediation"],
            "confidence": analysis["confidence"]
        }

    def _gather_context(self, alert: dict) -> dict:
        namespace = alert.get("namespace", "default")
        pod = alert.get("pod")

        context = {
            "events": [],
            "logs": [],
            "metrics": {}
        }

        # Kubernetes 이벤트 수집
        events = self.k8s.list_namespaced_event(
            namespace=namespace,
            field_selector=f"involvedObject.name={pod}"
        )
        context["events"] = [
            {"reason": e.reason, "message": e.message, "time": str(e.last_timestamp)}
            for e in events.items[-10:]
        ]

        # Pod 상태 수집
        pod_obj = self.k8s.read_namespaced_pod(name=pod, namespace=namespace)
        context["pod_status"] = {
            "phase": pod_obj.status.phase,
            "conditions": [
                {"type": c.type, "status": c.status, "reason": c.reason}
                for c in (pod_obj.status.conditions or [])
            ]
        }

        return context

    def _llm_analyze(self, alert: dict, context: dict) -> dict:
        prompt = f"""
        당신은 SRE 전문가입니다. 다음 Kubernetes 인시던트를 분석하세요.

        ## Alert
        {json.dumps(alert, indent=2)}

        ## Context
        {json.dumps(context, indent=2)}

        다음 형식으로 응답하세요:
        1. Root Cause: 근본 원인 (1-2문장)
        2. Impact: 영향 범위 (서비스/사용자)
        3. Remediation: 복구 단계 (번호 목록)
        4. Confidence: 분석 신뢰도 (0-100%)
        """

        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return self._parse_response(response.choices[0].message.content)
```

### 인과 관계 그래프 (Causal Graph)

```yaml
# 서비스 의존성 정의
apiVersion: v1
kind: ConfigMap
metadata:
  name: service-topology
data:
  topology.yaml: |
    services:
      - name: frontend
        depends_on: [api-gateway]
        metrics:
          - http_requests_total
          - http_request_duration_seconds

      - name: api-gateway
        depends_on: [order-service, user-service]
        metrics:
          - gateway_requests_total
          - gateway_latency_seconds

      - name: order-service
        depends_on: [postgres, redis]
        metrics:
          - order_processing_total
          - order_latency_seconds

      - name: postgres
        type: database
        metrics:
          - pg_connections
          - pg_query_duration_seconds

    # 장애 전파 규칙
    propagation_rules:
      - if: postgres.pg_connections > 90%
        then: order-service.latency_increase
        confidence: 0.85

      - if: order-service.error_rate > 5%
        then: api-gateway.error_rate_increase
        confidence: 0.90
```

---

## 자동 복구 (Auto-Remediation)

### Runbook 자동화

```yaml
# runbook-operator CRD
apiVersion: aiops.io/v1
kind: Runbook
metadata:
  name: pod-crash-loop-remediation
spec:
  trigger:
    alertname: PodCrashLoopBackOff
    severity: critical

  conditions:
    - type: pod_restart_count
      operator: ">"
      value: 5

  actions:
    - name: collect-diagnostics
      type: kubectl
      command: |
        kubectl logs {{ .pod }} -n {{ .namespace }} --previous > /tmp/crash-logs.txt
        kubectl describe pod {{ .pod }} -n {{ .namespace }} > /tmp/pod-describe.txt

    - name: check-resources
      type: prometheus
      query: |
        container_memory_working_set_bytes{
          pod="{{ .pod }}",
          namespace="{{ .namespace }}"
        } / container_spec_memory_limit_bytes > 0.95

    - name: remediate-oom
      type: kubectl
      condition: "{{ .check-resources.result == true }}"
      command: |
        kubectl patch deployment {{ .deployment }} -n {{ .namespace }} \
          -p '{"spec":{"template":{"spec":{"containers":[{
            "name":"{{ .container }}",
            "resources":{"limits":{"memory":"{{ .current_memory * 1.5 }}"}}
          }]}}}}'

    - name: restart-pod
      type: kubectl
      condition: "{{ .check-resources.result == false }}"
      command: |
        kubectl delete pod {{ .pod }} -n {{ .namespace }}

  notification:
    slack:
      channel: "#incidents"
      message: |
        Auto-remediation executed for {{ .pod }}
        Action: {{ .executed_action }}
        Result: {{ .result }}
```

### KEDA 기반 자동 스케일링

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: aiops-autoscaler
spec:
  scaleTargetRef:
    name: order-service
  minReplicaCount: 2
  maxReplicaCount: 20
  triggers:
    # 에러율 기반 스케일링
    - type: prometheus
      metadata:
        serverAddress: http://prometheus:9090
        metricName: error_rate
        threshold: "5"
        query: |
          sum(rate(http_requests_total{
            status=~"5..",
            service="order-service"
          }[5m])) /
          sum(rate(http_requests_total{
            service="order-service"
          }[5m])) * 100

    # 지연 시간 기반 스케일링
    - type: prometheus
      metadata:
        metricName: p99_latency
        threshold: "1000"  # 1초
        query: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket{
              service="order-service"
            }[5m])) by (le)
          ) * 1000
```

---

## 모니터링 대시보드

### Grafana AIOps 대시보드

```json
{
  "title": "AIOps Overview",
  "panels": [
    {
      "title": "Anomaly Score",
      "type": "timeseries",
      "targets": [{
        "expr": "anomaly_score{job=\"aiops-detector\"}",
        "legendFormat": "{{ service }}"
      }],
      "thresholds": {
        "steps": [
          {"color": "green", "value": 0},
          {"color": "yellow", "value": 0.7},
          {"color": "red", "value": 0.9}
        ]
      }
    },
    {
      "title": "Auto-Remediation Actions",
      "type": "stat",
      "targets": [{
        "expr": "sum(increase(remediation_actions_total[24h]))"
      }]
    },
    {
      "title": "MTTR Trend",
      "type": "timeseries",
      "targets": [{
        "expr": "avg(incident_resolution_time_seconds) / 60"
      }],
      "unit": "minutes"
    }
  ]
}
```

---

## 체크리스트

### AIOps Level 3 (예측적)
- [ ] LLM 기반 RCA
- [ ] 인과 관계 그래프
- [ ] Runbook 자동화

### AIOps Level 4 (자율 운영)
- [ ] 자동 복구 파이프라인
- [ ] 예측적 스케일링
- [ ] Self-Healing 시스템
- [ ] 승인 게이트 설정

**관련 agent**: `incident-responder`, `k8s-troubleshooter`
**관련 skill**: `/aiops` (기본, 이상 탐지), `/observability`, `/alerting`

---

## Sources

- [Kubernetes Observability Trends 2026](https://www.usdsi.org/data-science-insights/kubernetes-observability-and-monitoring-trends-in-2026)
- [AI-Based Observability 2026](https://middleware.io/blog/how-ai-based-insights-can-change-the-observability/)
- [LLMs for Root Cause Analysis](https://dzone.com/articles/llms-automated-root-cause-analysis-incident-response)
- [Causal Reasoning in Observability](https://www.infoq.com/articles/causal-reasoning-observability/)
