---
name: finops-automation
category: sre
description: "FinOps: 자동화 가이드 — Infracost PR 통합, 유휴 리소스 자동 정리, 비용 최적화 자동화 Use when working with sre 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# FinOps: 자동화 가이드

Infracost PR 통합, 유휴 리소스 자동 정리, 비용 최적화 자동화

## Quick Reference

```
FinOps 자동화 영역?
    │
    ├─ IaC 비용 예측 ────> Infracost PR 통합
    │       │
    │       └─ PR 시점에 비용 영향 확인
    │
    ├─ 유휴 리소스 정리 ──> CronJob + Lambda
    │       │
    │       └─ 미사용 PVC, 완료된 Job 등
    │
    └─ 자동 Right-sizing ─> VPA + 권고사항
            │
            └─ 리소스 요청 최적화
```

---

## Infracost PR 통합

### GitHub Actions 워크플로우

```yaml
# .github/workflows/infracost.yaml
name: Infracost

on:
  pull_request:
    paths:
      - 'terraform/**'
      - '**/*.tf'

jobs:
  infracost:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - name: Setup Infracost
        uses: infracost/actions/setup@v3
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}

      # 기준선 (main 브랜치) 비용 계산
      - name: Checkout base branch
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.base.ref }}
          path: base

      - name: Generate base cost
        run: |
          infracost breakdown --path=base/terraform \
            --format=json \
            --out-file=/tmp/base.json

      # PR 브랜치 비용 계산
      - name: Checkout PR branch
        uses: actions/checkout@v4
        with:
          path: pr

      - name: Generate PR cost
        run: |
          infracost breakdown --path=pr/terraform \
            --format=json \
            --out-file=/tmp/pr.json

      # 비용 비교 및 PR 코멘트
      - name: Generate diff
        run: |
          infracost diff \
            --path=/tmp/pr.json \
            --compare-to=/tmp/base.json \
            --format=json \
            --out-file=/tmp/diff.json

      - name: Post PR comment
        run: |
          infracost comment github \
            --path=/tmp/diff.json \
            --repo=${{ github.repository }} \
            --pull-request=${{ github.event.pull_request.number }} \
            --github-token=${{ secrets.GITHUB_TOKEN }} \
            --behavior=update

      # 비용 증가 시 경고
      - name: Check cost threshold
        run: |
          DIFF=$(cat /tmp/diff.json | jq '.diffTotalMonthlyCost | tonumber')
          if (( $(echo "$DIFF > 100" | bc -l) )); then
            echo "::warning::Monthly cost increase exceeds $100"
          fi
```

### Infracost 정책 파일

```yaml
# infracost-policy.yml
version: 0.1
policies:
  # 월간 비용 증가 제한
  - name: cost-increase-limit
    resource_type: "*"
    description: "PR당 월간 비용 증가 $500 제한"
    conditions:
      - path: diffTotalMonthlyCost
        operator: gt
        value: 500
    action: deny
    message: "이 PR은 월간 비용을 $500 이상 증가시킵니다. FinOps 팀 승인이 필요합니다."

  # 고비용 인스턴스 제한
  - name: no-xlarge-instances
    resource_type: "aws_instance"
    description: "2xlarge 이상 인스턴스 승인 필요"
    conditions:
      - path: values.instance_type
        operator: regex
        value: ".*[2-9]xlarge.*"
    action: warn
    message: "대형 인스턴스 사용 시 비용 검토가 필요합니다."
```

---

## 유휴 리소스 자동 정리

### 유휴 리소스 탐지 (PromQL)

```promql
# 미사용 PVC (마운트되지 않음)
kube_persistentvolumeclaim_status_phase{phase="Bound"}
unless on(persistentvolumeclaim, namespace)
kube_pod_spec_volumes_persistentvolumeclaims_info

# 오래된 ReplicaSet (replicas=0, 7일 이상)
kube_replicaset_spec_replicas == 0
and
(time() - kube_replicaset_created) > 86400 * 7

# 미사용 Service (Endpoint 없음)
kube_service_info
unless on(service, namespace)
kube_endpoint_address_available

# 유휴 Pod (CPU 사용률 1% 미만, 24시간 이상)
avg_over_time(
  rate(container_cpu_usage_seconds_total[5m])[24h:]
) < 0.01
and on(pod, namespace)
kube_pod_status_phase{phase="Running"}
```

### 자동 정리 CronJob

```yaml
# cleanup-idle-resources.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cleanup-idle-resources
  namespace: finops
spec:
  schedule: "0 2 * * *"  # 매일 새벽 2시
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: finops-cleanup
          containers:
            - name: cleanup
              image: bitnami/kubectl:latest
              command:
                - /bin/bash
                - -c
                - |
                  set -e

                  # 1. 완료된 Job 정리 (7일 이상)
                  kubectl get jobs --all-namespaces -o json | \
                    jq -r '.items[] | select(.status.succeeded == 1) |
                      select((now - (.status.completionTime | fromdateiso8601)) > 604800) |
                      "\(.metadata.namespace)/\(.metadata.name)"' | \
                    xargs -I {} kubectl delete job -n {}

                  # 2. Evicted Pod 정리
                  kubectl get pods --all-namespaces -o json | \
                    jq -r '.items[] | select(.status.reason == "Evicted") |
                      "\(.metadata.namespace)/\(.metadata.name)"' | \
                    xargs -I {} kubectl delete pod -n {}

                  # 3. 미사용 ConfigMap 리포트 (삭제는 수동)
                  echo "=== Orphaned ConfigMaps ===" > /tmp/report.txt
                  # 분석 로직...

          restartPolicy: OnFailure
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: finops-cleanup
  namespace: finops
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: finops-cleanup
rules:
  - apiGroups: [""]
    resources: ["pods", "configmaps", "secrets", "persistentvolumeclaims"]
    verbs: ["get", "list", "delete"]
  - apiGroups: ["batch"]
    resources: ["jobs"]
    verbs: ["get", "list", "delete"]
  - apiGroups: ["apps"]
    resources: ["replicasets"]
    verbs: ["get", "list", "delete"]
```

### AWS 유휴 리소스 정리 (Lambda)

```python
# cleanup_aws_resources.py
import boto3
from datetime import datetime, timedelta
import json

def cleanup_idle_resources(event, context):
    ec2 = boto3.client('ec2')

    results = {
        'unattached_volumes': [],
        'old_snapshots': [],
        'unused_eips': []
    }

    # 1. 미연결 EBS 볼륨 (30일 이상)
    volumes = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )['Volumes']

    for vol in volumes:
        create_time = vol['CreateTime'].replace(tzinfo=None)
        if (datetime.now() - create_time).days > 30:
            results['unattached_volumes'].append({
                'id': vol['VolumeId'],
                'size': vol['Size'],
                'created': str(create_time)
            })
            # 삭제 (주의: 실제 환경에서는 승인 프로세스 필요)
            # ec2.delete_volume(VolumeId=vol['VolumeId'])

    # 2. 미사용 Elastic IP
    addresses = ec2.describe_addresses()['Addresses']
    for addr in addresses:
        if 'InstanceId' not in addr and 'NetworkInterfaceId' not in addr:
            results['unused_eips'].append({
                'ip': addr['PublicIp'],
                'allocation_id': addr['AllocationId']
            })

    # SNS로 리포트 발송
    sns = boto3.client('sns')
    sns.publish(
        TopicArn='arn:aws:sns:ap-northeast-2:123456789:finops-alerts',
        Subject='AWS Idle Resources Report',
        Message=json.dumps(results, indent=2)
    )

    return results
```

---

## 비정상 리소스 알림

### Prometheus 알림 규칙

```yaml
# idle-resource-alerts.yaml
groups:
  - name: idle-resources
    rules:
      - alert: UnusedPVC
        expr: |
          kube_persistentvolumeclaim_status_phase{phase="Bound"}
          unless on(persistentvolumeclaim, namespace)
          kube_pod_spec_volumes_persistentvolumeclaims_info
        for: 7d
        labels:
          severity: warning
          category: finops
        annotations:
          summary: "미사용 PVC 발견: {{ $labels.persistentvolumeclaim }}"
          description: "7일 이상 마운트되지 않은 PVC입니다."

      - alert: IdlePod
        expr: |
          avg_over_time(
            rate(container_cpu_usage_seconds_total[5m])[24h:]
          ) < 0.01
          and on(pod, namespace)
          kube_pod_status_phase{phase="Running"}
        for: 24h
        labels:
          severity: info
          category: finops
        annotations:
          summary: "유휴 Pod 감지: {{ $labels.pod }}"
          description: "24시간 동안 CPU 사용률 1% 미만"

      - alert: UnexpectedResourceGrowth
        expr: |
          (
            sum(kube_pod_info) - sum(kube_pod_info offset 1h)
          ) > 50
        for: 15m
        labels:
          severity: info
          category: finops
        annotations:
          summary: "1시간 내 Pod 50개 이상 증가"
```

---

## 체크리스트

### Infracost
- [ ] Infracost API 키 설정
- [ ] GitHub Actions 워크플로우
- [ ] 비용 증가 임계값 설정
- [ ] 정책 파일 작성

### 유휴 리소스 정리
- [ ] 정리 CronJob 배포
- [ ] RBAC 설정
- [ ] 리포트 알림 채널
- [ ] AWS Lambda 함수 (선택)

### 모니터링
- [ ] 유휴 리소스 알림 규칙
- [ ] 대시보드 구축

**관련 skill**: `/finops-advanced` (허브), `/finops-showback` (Showback/Chargeback)
