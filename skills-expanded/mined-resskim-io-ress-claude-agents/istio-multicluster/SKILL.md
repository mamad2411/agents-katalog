---
name: istio-multicluster
category: service-mesh
description: "Istio 멀티클러스터 가이드 — Multi-Primary vs Primary-Remote, East-West Gateway, Shared Root CA, Cross-Cluster Discovery Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio 멀티클러스터 가이드

Multi-Primary vs Primary-Remote, East-West Gateway, Shared Root CA, Cross-Cluster Discovery

## Quick Reference (결정 트리)

```
멀티클러스터 토폴로지?
    │
    ├─ 같은 네트워크 ─────────────────────────────────────────┐
    │       │                                                  │
    │       ├─ 독립 운영 ──> Multi-Primary (Same Network)      │
    │       │                장애 격리 높음, 각 클러스터 독립    │
    │       │                                                  │
    │       └─ 단순 확장 ──> Primary-Remote (Same Network)     │
    │                        관리 단순, Primary SPOF 주의       │
    │                                                          │
    └─ 다른 네트워크 (멀티 리전/클라우드) ────────────────────┐
            │                                                  │
            ├─ 독립 운영 ──> Multi-Primary (Different Network) │
            │                East-West Gateway 필요             │
            │                                                  │
            └─ 에지 확장 ──> Primary-Remote (Different Network)│
                             East-West Gateway 필요             │
```

---

## CRITICAL: 아키텍처 비교

### 패턴별 비교

```
┌─────────────────────────────────────────────────────────────┐
│  Multi-Primary (Same Network)                                │
│                                                              │
│  Cluster 1             Cluster 2                             │
│  ┌──────────┐         ┌──────────┐                          │
│  │ istiod   │◄──xDS──▶│ istiod   │   각 클러스터 독립       │
│  │          │         │          │   API Server 상호 접근    │
│  ├──────────┤         ├──────────┤                          │
│  │ services │◄──직접──▶│ services │   Pod IP 직접 통신       │
│  └──────────┘         └──────────┘                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Multi-Primary (Different Network)                           │
│                                                              │
│  Cluster 1             Cluster 2                             │
│  ┌──────────┐         ┌──────────┐                          │
│  │ istiod   │         │ istiod   │                          │
│  ├──────────┤         ├──────────┤                          │
│  │ services │         │ services │                          │
│  ├──────────┤         ├──────────┤                          │
│  │ East-West│◄──TLS──▶│ East-West│   Gateway 경유           │
│  │ Gateway  │         │ Gateway  │                          │
│  └──────────┘         └──────────┘                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Primary-Remote                                              │
│                                                              │
│  Primary Cluster       Remote Cluster                        │
│  ┌──────────┐         ┌──────────┐                          │
│  │ istiod   │────xDS──▶│ (없음)   │   istiod는 Primary만    │
│  │          │◄──watch──│          │                          │
│  ├──────────┤         ├──────────┤                          │
│  │ services │◄───────▶│ services │                          │
│  └──────────┘         └──────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

| 패턴 | 제어 평면 | 장애 격리 | 복잡도 | 적합 시나리오 |
|------|-----------|-----------|--------|---------------|
| **Multi-Primary (Same Net)** | 각각 독립 | 높음 | 중간 | 같은 VPC/네트워크 |
| **Multi-Primary (Diff Net)** | 각각 독립 | 높음 | 높음 | 멀티 리전/클라우드 |
| **Primary-Remote (Same Net)** | Primary만 | 낮음 | 낮음 | 단순 확장 |
| **Primary-Remote (Diff Net)** | Primary만 | 낮음 | 중간 | 에지/리모트 |

---

## 사전 요구사항: Shared Root CA

### CRITICAL: 모든 패턴의 공통 선행 작업

```
멀티클러스터 mTLS를 위해 모든 클러스터가
동일한 Root CA를 공유해야 함.

각 클러스터에 Root CA로 서명된 Intermediate CA 설치:
  Root CA
    ├── Intermediate CA (Cluster 1)
    └── Intermediate CA (Cluster 2)
```

### 인증서 생성

```bash
# 1. Root CA 생성 (한 번만)
mkdir -p certs && cd certs

# Root CA 키 생성
openssl genrsa -out root-key.pem 4096

# Root CA 인증서 생성
openssl req -new -x509 -key root-key.pem -out root-cert.pem \
  -days 3650 -subj "/O=MyOrg/CN=Root CA"

# 2. Cluster 1 Intermediate CA
mkdir -p cluster1 && cd cluster1
openssl genrsa -out ca-key.pem 4096
openssl req -new -key ca-key.pem -out ca-csr.pem \
  -subj "/O=MyOrg/CN=Cluster1 Intermediate CA" \
  -config <(cat <<EOF
[req]
distinguished_name = req_distinguished_name
[req_distinguished_name]
EOF
)
openssl x509 -req -in ca-csr.pem -CA ../root-cert.pem \
  -CAkey ../root-key.pem -CAcreateserial \
  -out ca-cert.pem -days 1825 \
  -extfile <(echo "basicConstraints=CA:TRUE")
cat ca-cert.pem ../root-cert.pem > cert-chain.pem
cp ../root-cert.pem .

# 3. 각 클러스터에 Secret 생성
kubectl create secret generic cacerts -n istio-system \
  --from-file=ca-cert.pem \
  --from-file=ca-key.pem \
  --from-file=root-cert.pem \
  --from-file=cert-chain.pem \
  --context=cluster1
```

### cert-manager 연동 (자동화)

```yaml
# cert-manager로 Istio Root CA 관리
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: istio-root-ca
spec:
  selfSigned: {}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: istio-root-ca
  namespace: cert-manager
spec:
  isCA: true
  commonName: "Istio Root CA"
  secretName: istio-root-ca-secret
  duration: 87600h    # 10년
  issuerRef:
    name: istio-root-ca
    kind: ClusterIssuer
---
# Intermediate CA per cluster
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: istio-ca
  namespace: istio-system
spec:
  isCA: true
  commonName: "Istio Intermediate CA - Cluster1"
  secretName: cacerts
  duration: 43800h    # 5년
  renewBefore: 8760h  # 1년 전 갱신
  issuerRef:
    name: istio-root-ca-issuer
    kind: ClusterIssuer
  privateKey:
    algorithm: RSA
    size: 4096
```

---

## Multi-Primary (Same Network)

### IstioOperator 설정

```yaml
# Cluster 1
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster1
      network: network1       # 같은 네트워크
---
# Cluster 2
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1           # 같은 mesh ID
      multiCluster:
        clusterName: cluster2
      network: network1       # 같은 네트워크
```

### Remote Secret 교환

```bash
# Cluster 1에서 Cluster 2의 API Server 접근 설정
istioctl create-remote-secret \
  --name=cluster2 \
  --context=cluster2-context | \
  kubectl apply -f - --context=cluster1-context

# Cluster 2에서 Cluster 1의 API Server 접근 설정
istioctl create-remote-secret \
  --name=cluster1 \
  --context=cluster1-context | \
  kubectl apply -f - --context=cluster2-context
```

---

## Multi-Primary (Different Network)

### IstioOperator + East-West Gateway

```yaml
# Cluster 1
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster1
      network: network1       # 다른 네트워크
---
# Cluster 2
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster2
      network: network2       # 다른 네트워크
```

### East-West Gateway 설치

```bash
# Cluster 1에 East-West Gateway 설치
samples/multicluster/gen-eastwest-gateway.sh \
  --network network1 --cluster cluster1 | \
  istioctl install -f - --context=cluster1-context

# Cluster 2에 East-West Gateway 설치
samples/multicluster/gen-eastwest-gateway.sh \
  --network network2 --cluster cluster2 | \
  istioctl install -f - --context=cluster2-context

# 서비스 노출 (양쪽 클러스터 모두)
kubectl apply -n istio-system \
  -f samples/multicluster/expose-services.yaml \
  --context=cluster1-context

kubectl apply -n istio-system \
  -f samples/multicluster/expose-services.yaml \
  --context=cluster2-context
```

### expose-services.yaml 내용

```yaml
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: cross-network-gateway
  namespace: istio-system
spec:
  selector:
    istio: eastwestgateway
  servers:
  - port:
      number: 15443
      name: tls
      protocol: TLS
    tls:
      mode: AUTO_PASSTHROUGH
    hosts:
    - "*.local"
```

---

## Primary-Remote

### Primary 클러스터

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: primary
      network: network1
```

### Remote 클러스터

```bash
# Remote에는 istiod 없이 설치
istioctl install --context=remote-context \
  --set profile=remote \
  --set values.istiod.enabled=false \
  --set values.global.remotePilotAddress=<primary-istiod-ip>

# Primary에 Remote의 API Server Secret 추가
istioctl create-remote-secret \
  --name=remote \
  --context=remote-context | \
  kubectl apply -f - --context=primary-context
```

---

## Cross-Cluster 서비스 접근

### 자동 서비스 디스커버리

```
멀티클러스터 설정 후 서비스 자동 발견:

Cluster 1: payment-service.production.svc.cluster.local
Cluster 2: payment-service.production.svc.cluster.local

→ 같은 hostname으로 접근, Istio가 자동 로드밸런싱
→ Locality-aware 로드밸런싱 적용 (가까운 클러스터 우선)
```

### Locality-Aware 로드밸런싱

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: payment-locality
  namespace: production
spec:
  host: payment-service
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 10s
      baseEjectionTime: 30s
    loadBalancer:
      localityLbSetting:
        enabled: true
        failover:
        - from: us-east-1      # 로컬 리전 우선
          to: us-west-2         # 장애 시 다른 리전으로
        - from: us-west-2
          to: us-east-1
      simple: ROUND_ROBIN
```

### 클러스터별 트래픽 분배

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: payment-distribute
  namespace: production
spec:
  host: payment-service
  trafficPolicy:
    loadBalancer:
      localityLbSetting:
        enabled: true
        distribute:
        - from: "us-east-1/*"
          to:
            "us-east-1/*": 80   # 80% 로컬
            "us-west-2/*": 20   # 20% 원격
```

---

## 멀티클러스터 보안

### 클러스터 간 AuthorizationPolicy

```yaml
# Cluster 2의 서비스만 Cluster 1의 payment-service 접근 허용
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: cross-cluster-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: payment-service
  action: ALLOW
  rules:
  - from:
    - source:
        # SPIFFE ID에 클러스터 구분 없음 (같은 trust domain)
        principals:
        - "cluster.local/ns/production/sa/order-service"
    to:
    - operation:
        methods: ["POST"]
        paths: ["/api/v1/payments"]
```

---

## 디버깅

```bash
# 멀티클러스터 상태 확인
istioctl remote-clusters --context=cluster1-context

# Cross-cluster 엔드포인트 확인
istioctl proxy-config endpoints <pod> -n production | \
  grep payment-service

# East-West Gateway 상태
kubectl get svc -n istio-system -l istio=eastwestgateway

# mTLS 인증서 확인 (Root CA 일치 여부)
istioctl proxy-config secret <pod> -n production -o json | \
  jq '.dynamicActiveSecrets[0].secret.tlsCertificate'

# Remote Secret 확인
kubectl get secret -n istio-system -l istio/multiCluster=true
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Root CA 불일치 | 클러스터 간 mTLS 실패 | 같은 Root CA 공유 |
| meshID 불일치 | 서비스 디스커버리 안 됨 | 모든 클러스터 같은 meshID |
| East-West GW 미설치 | 다른 네트워크 통신 불가 | 양쪽 모두 East-West GW |
| Remote Secret 누락 | API Server 접근 불가 | 양방향 Secret 교환 |
| Locality 미설정 | 불필요한 크로스 리전 트래픽 | Locality-aware LB 활성화 |

---

## 체크리스트

### 사전 준비
- [ ] Shared Root CA 생성 및 배포
- [ ] 클러스터 간 네트워크 연결 확인
- [ ] meshID 통일
- [ ] Istio 버전 통일

### Multi-Primary
- [ ] 양쪽 IstioOperator 설치
- [ ] Remote Secret 양방향 교환
- [ ] East-West Gateway (다른 네트워크)
- [ ] expose-services 적용

### 검증
- [ ] Cross-cluster 서비스 디스커버리 확인
- [ ] mTLS 연결 확인
- [ ] Locality-aware 로드밸런싱 확인
- [ ] 장애 시 failover 테스트

**관련 skill**: `/istio-core`, `/istio-security`, `/istio-gateway`, `/k8s-traffic`
