---
name: istio-gitops
category: service-mesh
description: "Istio GitOps 통합 가이드 — ArgoCD로 Istio 설치/관리, CRD sync wave, kind 주의점, cert-manager 통합 Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio GitOps 통합 가이드

ArgoCD로 Istio 설치/관리, CRD sync wave, kind 주의점, cert-manager 통합

## Quick Reference (결정 트리)

```
Istio + ArgoCD 설치?
    │
    ├─ 설치 순서 ──────────> 3단계 분리 (Sync Wave)
    │     │
    │     ├─ Wave -3: istio-base (CRD)
    │     ├─ Wave -2: istiod (control plane)
    │     └─ Wave -1: istio-gateway (data plane)
    │
    ├─ kind에서 설치? ─────> NodePort + 포트 매핑
    │     │
    │     └─ MetalLB 또는 kind extraPortMappings
    │
    ├─ TLS 관리 ───────────> cert-manager + Istio Gateway
    │
    └─ 업그레이드 ─────────> Canary upgrade (revision 기반)
```

---

## ArgoCD로 Istio 설치

### 3개 Application 분리 (필수)

Istio는 CRD → Control Plane → Data Plane 순서로 설치해야 한다.
하나의 Application으로 하면 CRD가 아직 없는데 리소스를 만들려고 해서 실패.

```yaml
# 1. istio-base (CRD 설치) — Wave -3
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: istio-base
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-3"
spec:
  project: platform
  source:
    repoURL: https://istio-release.storage.googleapis.com/charts
    chart: base
    targetRevision: "1.24.2"
  destination:
    server: https://kubernetes.default.svc
    namespace: istio-system
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true           # CRD는 SSA 필수

---
# 2. istiod (Control Plane) — Wave -2
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: istiod
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-2"
spec:
  project: platform
  source:
    repoURL: https://istio-release.storage.googleapis.com/charts
    chart: istiod
    targetRevision: "1.24.2"
    helm:
      valueFiles:
        - $values/istio/istiod-values.yaml
  sources:
    - repoURL: https://istio-release.storage.googleapis.com/charts
      chart: istiod
      targetRevision: "1.24.2"
      helm:
        valueFiles:
          - $values/istio/istiod-values.yaml
    - repoURL: https://github.com/my-org/k8s-config.git
      targetRevision: main
      ref: values
  destination:
    server: https://kubernetes.default.svc
    namespace: istio-system
  syncPolicy:
    automated:
      prune: true
      selfHeal: true

---
# 3. istio-gateway (Data Plane) — Wave -1
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: istio-ingressgateway
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
spec:
  project: platform
  source:
    repoURL: https://istio-release.storage.googleapis.com/charts
    chart: gateway
    targetRevision: "1.24.2"
    helm:
      values: |
        service:
          type: LoadBalancer            # 환경별 override
  destination:
    server: https://kubernetes.default.svc
    namespace: istio-ingress
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
```

### istiod values (환경별)

```yaml
# istio/istiod-values.yaml (공통)
pilot:
  resources:
    requests:
      cpu: 100m
      memory: 256Mi

meshConfig:
  accessLogFile: /dev/stdout
  accessLogEncoding: JSON
  enableTracing: true
  defaultConfig:
    tracing:
      sampling: 100                    # dev: 100%, prod: 1%

  # OTel 연동 (ExtensionProvider)
  extensionProviders:
    - name: otel-collector
      opentelemetry:
        service: otel-collector.observability.svc.cluster.local
        port: 4317

global:
  proxy:
    resources:
      requests:
        cpu: 50m
        memory: 64Mi
      limits:
        cpu: 200m
        memory: 128Mi
```

```yaml
# istio/istiod-values-prod.yaml
pilot:
  replicaCount: 2                     # HA
  resources:
    requests:
      cpu: 500m
      memory: 1Gi

meshConfig:
  defaultConfig:
    tracing:
      sampling: 1                      # prod: 1%만 샘플링

global:
  proxy:
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 500m
        memory: 256Mi
```

---

## kind에서 Istio 설치 주의점

### 문제: LoadBalancer가 kind에서 동작하지 않음

kind는 bare-metal 환경이므로 `type: LoadBalancer`가 Pending 상태로 멈춤.

### 해결 1: NodePort + kind extraPortMappings (간단)

```yaml
# kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    extraPortMappings:
      - containerPort: 30080           # HTTP
        hostPort: 80
        protocol: TCP
      - containerPort: 30443           # HTTPS
        hostPort: 443
        protocol: TCP
```

```yaml
# istio-gateway values override (kind)
service:
  type: NodePort
  ports:
    - name: http2
      port: 80
      targetPort: 80
      nodePort: 30080
    - name: https
      port: 443
      targetPort: 443
      nodePort: 30443
```

### 해결 2: MetalLB (LoadBalancer IP 할당)

```yaml
# MetalLB 설치 (ArgoCD Application)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: metallb
  annotations:
    argocd.argoproj.io/sync-wave: "-4"   # Istio보다 먼저
spec:
  source:
    repoURL: https://metallb.github.io/metallb
    chart: metallb
    targetRevision: "0.14.8"
  destination:
    server: https://kubernetes.default.svc
    namespace: metallb-system

---
# MetalLB IP Pool (kind Docker 네트워크 대역)
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: kind-pool
  namespace: metallb-system
spec:
  addresses:
    - 172.18.255.200-172.18.255.250    # kind 네트워크 대역
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: kind-l2
  namespace: metallb-system
```

```bash
# kind 네트워크 대역 확인
docker network inspect kind | jq '.[0].IPAM.Config[0].Subnet'
# → "172.18.0.0/16" → IP Pool: 172.18.255.200-250
```

---

## cert-manager + Istio + ArgoCD 통합

### Sync Wave 순서

```
Wave -4: MetalLB (kind only)
Wave -3: istio-base (CRD)
Wave -3: cert-manager (CRD + controller)
Wave -2: istiod
Wave -2: ClusterIssuer (cert-manager)
Wave -1: istio-gateway
Wave -1: Certificate (TLS 인증서)
Wave  0: Gateway + HTTPRoute (앱 라우팅)
```

### cert-manager ArgoCD Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: cert-manager
  annotations:
    argocd.argoproj.io/sync-wave: "-3"
spec:
  source:
    repoURL: https://charts.jetstack.io
    chart: cert-manager
    targetRevision: "v1.16.2"
    helm:
      values: |
        crds:
          enabled: true
        resources:
          requests:
            cpu: 50m
            memory: 64Mi
  destination:
    server: https://kubernetes.default.svc
    namespace: cert-manager
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
```

### ClusterIssuer + Certificate

```yaml
# Let's Encrypt (prod)
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
  annotations:
    argocd.argoproj.io/sync-wave: "-2"
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod-key
    solvers:
      # EKS: Route53 DNS solver
      - dns01:
          route53:
            region: ap-northeast-2
      # GKE: Cloud DNS solver
      # - dns01:
      #     cloudDNS:
      #       project: my-project-id

---
# Istio Gateway용 TLS 인증서
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: gateway-tls
  namespace: istio-ingress
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
spec:
  secretName: gateway-tls-cert
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
    - "*.example.com"
    - "example.com"
```

### Istio Gateway에서 cert-manager 인증서 사용

```yaml
# Gateway API 방식 (K8s native)
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: main-gateway
  namespace: istio-ingress
spec:
  gatewayClassName: istio
  listeners:
    - name: https
      protocol: HTTPS
      port: 443
      tls:
        mode: Terminate
        certificateRefs:
          - name: gateway-tls-cert      # cert-manager가 생성한 Secret
      allowedRoutes:
        namespaces:
          from: All
    - name: http
      protocol: HTTP
      port: 80
      allowedRoutes:
        namespaces:
          from: All
```

---

## Istio 업그레이드 (ArgoCD)

### Canary Upgrade (Revision 기반)

```
1. 새 istiod revision 배포 (기존과 공존)
2. namespace별로 새 revision으로 전환
3. 검증 후 구 revision 삭제

→ ArgoCD에서는 targetRevision만 변경하고
  istio.io/rev label로 namespace별 전환
```

```yaml
# 새 revision istiod (1.24 → 1.25)
spec:
  source:
    chart: istiod
    targetRevision: "1.25.0"
    helm:
      values: |
        revision: 1-25                  # revision 이름
        pilot:
          replicaCount: 2
```

```bash
# namespace를 새 revision으로 전환
kubectl label namespace myapp istio.io/rev=1-25 --overwrite

# Pod 재시작 (새 sidecar 주입)
kubectl rollout restart deployment -n myapp

# 검증 후 구 revision ArgoCD Application 삭제
```

---

## ArgoCD ignoreDifferences (Istio 전용)

Istio가 동적으로 변경하는 필드를 ArgoCD가 OutOfSync로 표시하지 않도록.

```yaml
spec:
  ignoreDifferences:
    # Istio webhook caBundle
    - group: admissionregistration.k8s.io
      kind: MutatingWebhookConfiguration
      name: istio-sidecar-injector
      jsonPointers:
        - /webhooks/0/clientConfig/caBundle
    - group: admissionregistration.k8s.io
      kind: ValidatingWebhookConfiguration
      name: istio-validator-istio-system
      jsonPointers:
        - /webhooks/0/clientConfig/caBundle
    # Istio가 자동 생성하는 필드
    - group: networking.istio.io
      kind: EnvoyFilter
      jsonPointers:
        - /spec/configPatches
```
