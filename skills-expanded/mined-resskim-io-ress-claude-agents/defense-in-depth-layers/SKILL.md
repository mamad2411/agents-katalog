---
name: defense-in-depth-layers
category: kubernetes
description: Kubernetes 보안을 L3/L4 NetworkPolicy + L7 AuthorizationPolicy + Pod Security + Image policy 4중 레이어로 강제하는 체크리스트. OWASP K8s Top 10 2025 기반. 단일 레이어 의존 안티패턴 차단.
---

# Defense in Depth Layers (M5: 보안 모델 단순화)

K8s 보안을 단일 레이어 (AuthorizationPolicy 만, 또는 NetworkPolicy 만) 로 막으면 **부분 우회**가 쉽다. 4중 방어 레이어를 모두 적용해야 한다.

> Claude mental model 오류: "Istio AuthorizationPolicy 가 막으면 끝" → mTLS 가 우회되거나, sidecar bypass / hostNetwork Pod / NodePort 노출 등으로 **L7 보안만으로는 불충분**.

---

## 4 레이어 방어 모델

```
┌─────────────────────────────────────────────────────────┐
│ L1: Image / Supply chain                                │
│   - signed image / SBOM / vulnerability scan            │
│   - admission controller (Kyverno / Gatekeeper)         │
├─────────────────────────────────────────────────────────┤
│ L2: Pod runtime (workload identity)                     │
│   - PodSecurity admission (restricted)                  │
│   - readOnlyRootFilesystem / runAsNonRoot               │
│   - ServiceAccount 최소 권한                            │
├─────────────────────────────────────────────────────────┤
│ L3-L4: Network (NetworkPolicy)                          │
│   - ingress: 허용 namespace/pod label만                 │
│   - egress: 외부 도메인 / DNS / API server 명시         │
├─────────────────────────────────────────────────────────┤
│ L7: Service mesh (Istio AuthorizationPolicy)            │
│   - PeerAuthentication: STRICT mTLS                     │
│   - AuthZ: HTTP method + path + JWT claim 검증          │
└─────────────────────────────────────────────────────────┘
```

**핵심 원칙**: 한 레이어가 뚫려도 다음 레이어가 막는다. **단일 레이어 의존 = 안티패턴**.

---

## ❌ 안티패턴 5종 (OWASP K8s Top 10 2025)

### K01: Insecure workload configurations

```yaml
# ❌ root 권한 + 쓰기 가능 rootfs
spec:
  containers:
  - name: app
    image: app:latest
    # securityContext 없음
```

```yaml
# ✅ Pod Security restricted
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    fsGroup: 10001
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: app:1.2.3   # tag 고정
    securityContext:
      readOnlyRootFilesystem: true
      allowPrivilegeEscalation: false
      capabilities:
        drop: [ALL]
```

### K04: Lack Of Cluster Level Policy Enforcement (Supply chain)

```yaml
# ❌ unsigned image
image: docker.io/randomuser/app:latest

# ✅ 사내 registry + digest 고정 + Kyverno verify
image: ecr.amazonaws.com/app@sha256:abc123...
```

Admission policy:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image
spec:
  rules:
  - name: check-signature
    verifyImages:
    - imageReferences:
      - "ecr.amazonaws.com/*"
      attestors:
      - entries:
        - keys: {publicKeys: "..."}
```

### K02: Overly Permissive Authorization Configurations

```yaml
# ❌ cluster-admin 부여
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]

# ✅ 최소 권한
- apiGroups: [""]
  resources: ["configmaps"]
  resourceNames: ["my-app-config"]   # 특정 리소스만
  verbs: ["get", "list", "watch"]
```

### K09: Broken Authentication Mechanisms

`ServiceAccount` token 자동 mount 비활성화:

```yaml
spec:
  automountServiceAccountToken: false   # 명시적으로 필요한 Pod 만 mount
```

### K05: Missing Network Segmentation Controls

NetworkPolicy 3중 체크 (운영 환경에서 빈도 높음):

```yaml
# ✅ 1. default deny ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
---
# 2. 명시적 ingress 허용
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-istio
spec:
  podSelector:
    matchLabels: {app: my-app}
  ingress:
  - from:
    - namespaceSelector:
        matchLabels: {istio-injection: enabled}
---
# 3. egress 명시 (DNS + API server + 외부 의존)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-egress
spec:
  podSelector:
    matchLabels: {app: my-app}
  egress:
  - to:
    - namespaceSelector:
        matchLabels: {kubernetes.io/metadata.name: kube-system}
      podSelector:
        matchLabels: {k8s-app: kube-dns}
    ports: [{port: 53, protocol: UDP}]
  - to:
    - ipBlock: {cidr: 10.0.0.0/16}   # API server
    ports: [{port: 443}]
  - to:
    - namespaceSelector:
        matchLabels: {kubernetes.io/metadata.name: default}
      podSelector:
        matchLabels: {app: postgresql}
    ports: [{port: 5432}]
```

---

## Istio AuthorizationPolicy + PeerAuthentication 조합

```yaml
# 1. STRICT mTLS — 평문 트래픽 차단
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: my-app
spec:
  mtls:
    mode: STRICT
---
# 2. AuthZ — HTTP method/path + identity
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: my-app-allow
  namespace: my-app
spec:
  selector:
    matchLabels: {app: my-app}
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/gateway/sa/istio-ingressgateway"]
    to:
    - operation:
        methods: [GET, POST]
        paths: [/api/v1/*]
```

**중요**: AuthZ 만 있고 NetworkPolicy 없으면 → sidecar bypass (hostNetwork=true 또는 cross-NS 직접 Pod IP 호출) 시 막히지 않음.

---

## ✅ 4중 체크리스트 (PR 단위 의무)

L1 (Image):
- [ ] image tag 고정 + digest 명시
- [ ] vulnerability scan 통과 (trivy / grype)
- [ ] signed image 검증 (cosign + Kyverno verify)

L2 (Pod runtime):
- [ ] `runAsNonRoot: true` + `runAsUser` 명시
- [ ] `readOnlyRootFilesystem: true` (필요 시 emptyDir 마운트)
- [ ] `capabilities.drop: [ALL]`
- [ ] `automountServiceAccountToken: false` (필요 시만 true)
- [ ] `seccompProfile: RuntimeDefault`

L3-L4 (Network):
- [ ] **default deny** NetworkPolicy 존재 (ingress + egress)
- [ ] ingress 허용 source 명시 (namespace + pod label)
- [ ] egress 명시 (DNS / API server / 외부 의존 도메인)
- [ ] hostNetwork=true / hostPort 사용 금지 (필요 시 ADR)

L7 (Service mesh):
- [ ] `PeerAuthentication mode: STRICT`
- [ ] AuthorizationPolicy 의 `action: ALLOW` (default deny 모델)
- [ ] HTTP method + path 별 권한 분리
- [ ] JWT 검증 시 `RequestAuthentication` + claim-based AuthZ

---

## 외부 근거

- [OWASP Kubernetes Top Ten 2025](https://owasp.org/www-project-kubernetes-top-ten/)
- [Kubernetes Security Cheat Sheet — OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html)
- [OWASP K8s Top 10 — Sysdig overview](https://www.sysdig.com/blog/top-owasp-kubernetes)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [Pod Security Standards — Kubernetes Docs](https://kubernetes.io/docs/concepts/security/pod-security-standards/)

---

## 연계 skill

- [`kubernetes/netpol-defense-depth.md`](../netpol-defense-depth/SKILL.md) — NetworkPolicy 3중 체크리스트 상세
- [`kubernetes/k8s-security.md`](../k8s-security/SKILL.md) — Pod Security 상세
- [`architecture/service-ownership-matrix.md`](../service-ownership-matrix/SKILL.md) — 각 레이어 owner
