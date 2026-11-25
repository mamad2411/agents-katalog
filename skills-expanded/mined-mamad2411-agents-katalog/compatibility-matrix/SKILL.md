---
name: compatibility-matrix
category: infrastructure
description: "Compatibility Matrix 가이드 — K8s 에코시스템 버전 호환성 매트릭스 관리. EKS/GKE/kind 간 전환 시 버전 조합 검증. Use when working with infrastructure 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Compatibility Matrix 가이드

K8s 에코시스템 버전 호환성 매트릭스 관리. EKS/GKE/kind 간 전환 시 버전 조합 검증.

## Quick Reference (결정 트리)

```
버전 호환성 확인?
    │
    ├─ K8s 버전 매핑 ──────> kind ↔ EKS ↔ GKE 버전 대응표
    │
    ├─ Add-on 호환성 ──────> 공식 지원 매트릭스 확인
    │     │
    │     ├─ ArgoCD ────────> K8s 버전 지원 범위
    │     ├─ Istio ─────────> K8s + Envoy 버전
    │     ├─ OTel ──────────> Collector + SDK 버전
    │     └─ Prometheus ───> kube-prometheus-stack 버전
    │
    ├─ 검증 도구 ──────────> pluto, kubent, kubectl convert
    │
    └─ 업그레이드 경로 ────> N-2 지원 정책 확인
```

---

## K8s 버전 매핑 (kind ↔ EKS ↔ GKE)

### 버전 대응표 (2025-2026 기준)

```
┌──────────┬──────────────┬──────────────┬──────────────────────┐
│ K8s Ver  │ kind image   │ EKS          │ GKE                  │
├──────────┼──────────────┼──────────────┼──────────────────────┤
│ 1.32     │ v1.32.x      │ 예정         │ Rapid channel        │
│ 1.31     │ v1.31.x      │ 지원 중      │ Regular channel      │
│ 1.30     │ v1.30.x      │ 지원 중      │ Regular channel      │
│ 1.29     │ v1.29.x      │ 지원 중      │ Stable channel       │
│ 1.28     │ v1.28.x      │ Extended     │ Extended             │
│ 1.27     │ v1.27.x      │ EOL          │ EOL                  │
└──────────┴──────────────┴──────────────┴──────────────────────┘

권장: kind에서 사용하는 K8s 버전을 EKS/GKE 타겟 버전과 동일하게 맞춘다.
```

### kind 이미지 고정 방법

```yaml
# kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    image: kindest/node:v1.30.6@sha256:...  # 버전 고정
  - role: worker
    image: kindest/node:v1.30.6@sha256:...
```

```bash
# 특정 버전으로 클러스터 생성
kind create cluster --name dev --image kindest/node:v1.30.6
```

---

## Add-on 호환성 매트릭스

### 매트릭스 템플릿

```markdown
## Compatibility Matrix: [프로젝트명]

최종 업데이트: YYYY-MM-DD
타겟 K8s 버전: 1.30.x

| Component | Version | K8s 지원 범위 | Helm Chart | 비고 |
|-----------|---------|--------------|------------|------|
| ArgoCD | 2.13.x | 1.28-1.31 | argo/argo-cd 7.x | |
| Istio | 1.24.x | 1.28-1.31 | istio/istiod | Ambient GA |
| OTel Collector | 0.114.x | 1.27+ | open-telemetry/opentelemetry-collector | |
| kube-prometheus-stack | 65.x | 1.28+ | prometheus-community | Prom 2.55+ |
| Loki | 3.3.x | 1.28+ | grafana/loki | |
| Grafana | 11.x | - | grafana/grafana | |
| Fluent Bit | 3.2.x | 1.27+ | fluent/fluent-bit | |
| cert-manager | 1.16.x | 1.28-1.31 | jetstack/cert-manager | |
| External Secrets | 0.12.x | 1.27+ | external-secrets | |
| KEDA | 2.16.x | 1.28-1.31 | kedacore/keda | |
| Nginx Ingress | 4.12.x | 1.28+ | ingress-nginx | |
| AWS LB Controller | 2.10.x | 1.28+ | eks/aws-load-balancer-controller | EKS only |
```

### 주요 컴포넌트별 호환성 확인 방법

#### ArgoCD

```bash
# 공식 지원 매트릭스 확인
# https://argo-cd.readthedocs.io/en/stable/operator-manual/installation/#supported-versions

# 현재 설치된 버전 확인
argocd version --client
kubectl get deploy argocd-server -n argocd -o jsonpath='{.spec.template.spec.containers[0].image}'
```

| ArgoCD | K8s 1.28 | K8s 1.29 | K8s 1.30 | K8s 1.31 |
|--------|----------|----------|----------|----------|
| 2.13.x | O | O | O | O |
| 2.12.x | O | O | O | O |
| 2.11.x | O | O | O | - |
| 2.10.x | O | O | - | - |

#### Istio

```bash
# 공식 지원 매트릭스
# https://istio.io/latest/docs/releases/supported-releases/

istioctl version
istioctl verify-install
```

| Istio | K8s 1.28 | K8s 1.29 | K8s 1.30 | K8s 1.31 |
|-------|----------|----------|----------|----------|
| 1.24.x | O | O | O | O |
| 1.23.x | O | O | O | - |
| 1.22.x | O | O | - | - |

#### kube-prometheus-stack

```bash
# Helm chart 버전과 내부 컴포넌트 버전 매핑
helm show chart prometheus-community/kube-prometheus-stack --version 65.0.0
```

| Chart Ver | Prometheus | Grafana | AlertManager | K8s |
|-----------|-----------|---------|--------------|-----|
| 65.x | 2.55+ | 11.x | 0.27+ | 1.28+ |
| 60.x | 2.53+ | 10.x | 0.27+ | 1.27+ |
| 55.x | 2.49+ | 10.x | 0.26+ | 1.26+ |

---

## Deprecated API 검증

### pluto — deprecated/removed API 탐지

```bash
# 설치
brew install FairwindsOps/tap/pluto

# Helm release에서 deprecated API 탐지
pluto detect-helm -o wide

# 매니페스트 파일에서 탐지
pluto detect-files -d k8s/ -o wide

# 특정 K8s 버전 기준으로 검사
pluto detect-files -d k8s/ --target-versions k8s=v1.30.0

# 출력 예시
# NAME        KIND        VERSION              REPLACEMENT          DEPRECATED   REMOVED
# my-ingress  Ingress     extensions/v1beta1   networking.k8s.io/v1 true        true
```

### kubent — deprecated API 탐지 (클러스터 기반)

```bash
# 설치
brew install kubent

# 현재 클러스터에서 deprecated API 사용 현황 확인
kubent

# 특정 K8s 버전 기준
kubent --target-version 1.30
```

### kubectl convert (API 버전 변환)

```bash
# 플러그인 설치
kubectl krew install convert

# 구 API → 신 API 변환
kubectl convert -f old-ingress.yaml --output-version networking.k8s.io/v1
```

---

## 호환성 검증 프로세스

### Phase 전환 전 체크리스트

```markdown
## Pre-Migration Compatibility Check

### 1. K8s 버전 확인
- [ ] 타겟 K8s 버전 결정 (EKS/GKE 지원 버전 확인)
- [ ] kind 클러스터를 타겟 버전과 동일하게 설정
- [ ] `pluto detect-files` 실행 — deprecated API 없음 확인

### 2. Add-on 호환성
- [ ] 각 add-on의 공식 지원 매트릭스 확인
- [ ] Helm chart 버전 ↔ K8s 버전 교차 검증
- [ ] CRD 호환성 확인 (특히 Istio, cert-manager)

### 3. kind에서 사전 테스트
- [ ] kind를 타겟 K8s 버전으로 생성
- [ ] 모든 add-on을 타겟 버전으로 설치
- [ ] E2E 테스트 통과 확인
- [ ] 모니터링 정상 동작 확인

### 4. EKS/GKE 전용 검증
- [ ] AWS Load Balancer Controller / GKE Ingress 호환성
- [ ] CSI Driver 버전 (EBS CSI, PD CSI)
- [ ] CoreDNS 버전
- [ ] kube-proxy vs Cilium (eBPF)
- [ ] IRSA / Workload Identity 동작 확인
```

### 자동화 스크립트

```bash
#!/bin/bash
# check-compatibility.sh — 호환성 사전 검증 스크립트

TARGET_K8S="1.30"

echo "=== Deprecated API Check ==="
pluto detect-files -d k8s/ --target-versions k8s=v${TARGET_K8S}.0

echo ""
echo "=== Helm Chart Compatibility ==="
for chart in $(helm list -A -o json | jq -r '.[].chart'); do
  echo "Checking: $chart"
done

echo ""
echo "=== Current Versions ==="
echo "K8s: $(kubectl version --short 2>/dev/null | grep Server)"
echo "ArgoCD: $(kubectl get deploy argocd-server -n argocd -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null)"
echo "Istio: $(istioctl version --short 2>/dev/null)"

echo ""
echo "=== CRD API Versions ==="
kubectl get crd -o custom-columns='NAME:.metadata.name,VERSION:.spec.versions[*].name' 2>/dev/null
```

---

## EKS vs GKE 차이 매트릭스

kind에서 EKS/GKE로 넘어갈 때 달라지는 부분.

```
┌──────────────────┬──────────────────┬──────────────────┐
│ 항목             │ EKS              │ GKE              │
├──────────────────┼──────────────────┼──────────────────┤
│ Ingress          │ AWS ALB          │ GKE Ingress/     │
│                  │ Controller       │ Cloud LB         │
├──────────────────┼──────────────────┼──────────────────┤
│ Storage          │ EBS CSI (gp3)    │ PD CSI (pd-ssd)  │
│                  │ EFS CSI          │ Filestore CSI    │
├──────────────────┼──────────────────┼──────────────────┤
│ IAM              │ IRSA /           │ Workload         │
│                  │ Pod Identity     │ Identity         │
├──────────────────┼──────────────────┼──────────────────┤
│ DNS              │ Route53 +        │ Cloud DNS +      │
│                  │ ExternalDNS      │ ExternalDNS      │
├──────────────────┼──────────────────┼──────────────────┤
│ Autoscaler       │ Karpenter        │ GKE Autopilot /  │
│                  │ (권장)           │ NAP              │
├──────────────────┼──────────────────┼──────────────────┤
│ Networking       │ VPC CNI          │ GKE Dataplane V2 │
│                  │ (aws-node)       │ (Cilium 기반)    │
├──────────────────┼──────────────────┼──────────────────┤
│ Monitoring       │ CloudWatch /     │ Cloud Monitoring  │
│ (Managed)        │ AMP              │ / GMP            │
├──────────────────┼──────────────────┼──────────────────┤
│ Log              │ CloudWatch Logs  │ Cloud Logging    │
│ (Managed)        │                  │                  │
├──────────────────┼──────────────────┼──────────────────┤
│ Secret           │ AWS Secrets Mgr  │ GCP Secret Mgr   │
│                  │ + ESO            │ + ESO            │
├──────────────────┼──────────────────┼──────────────────┤
│ K8s 업그레이드   │ 수동 / Auto Mode │ 자동 (채널 기반) │
├──────────────────┼──────────────────┼──────────────────┤
│ 비용 모델        │ 시간당 $0.10     │ Autopilot: Pod당 │
│                  │ + 노드 비용      │ Standard: 무료   │
│                  │                  │ + 노드 비용      │
└──────────────────┴──────────────────┴──────────────────┘
```

### Helm values에서 클라우드별 차이 처리

```yaml
# values-eks.yaml
cloud:
  provider: aws
  region: ap-northeast-2

ingress:
  className: alb
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip

storage:
  className: gp3

serviceAccount:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789:role/myapp-role

secrets:
  backend: external-secrets
  provider: aws-secretsmanager
```

```yaml
# values-gke.yaml
cloud:
  provider: gcp
  region: asia-northeast3

ingress:
  className: gce
  annotations:
    kubernetes.io/ingress.class: gce

storage:
  className: pd-ssd

serviceAccount:
  annotations:
    iam.gke.io/gcp-service-account: myapp@project.iam.gserviceaccount.com

secrets:
  backend: external-secrets
  provider: gcp-secretsmanager
```

---

## 버전 고정 전략

### Helm Chart 버전 고정

```yaml
# argocd Application에서 chart 버전 고정
spec:
  source:
    chart: kube-prometheus-stack
    repoURL: https://prometheus-community.github.io/helm-charts
    targetRevision: "65.1.0"    # 버전 고정 (~ 범위 사용 금지)
```

### kind 이미지 SHA 고정

```yaml
# 재현 가능한 테스트를 위해 SHA 고정
nodes:
  - role: control-plane
    image: kindest/node:v1.30.6@sha256:b6d08db72079ba5ae1f4a88a09025c0a904af3b52387c5571f1571c5941373d0
```

### Renovate/Dependabot 설정

```json
// renovate.json — 자동 업데이트 + 호환성 체크
{
  "extends": ["config:base"],
  "kubernetes": {
    "fileMatch": ["k8s/.+\\.yaml$"]
  },
  "helm-values": {
    "fileMatch": ["charts/.+/values.*\\.yaml$"]
  },
  "packageRules": [
    {
      "matchPackagePatterns": ["kube-prometheus-stack", "argo-cd", "istio"],
      "groupName": "k8s-ecosystem",
      "schedule": ["every 2 weeks on Monday"]
    }
  ]
}
```
