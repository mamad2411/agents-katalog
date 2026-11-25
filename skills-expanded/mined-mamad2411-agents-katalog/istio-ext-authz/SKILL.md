---
name: istio-ext-authz
category: service-mesh
description: "Istio External Authorization (ext-authz) — CUSTOM AuthorizationPolicy, OPA/외부 인증 서버 연동, 다계층 정책 조합 Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio External Authorization (ext-authz)

CUSTOM AuthorizationPolicy, OPA/외부 인증 서버 연동, 다계층 정책 조합

## Quick Reference (결정 트리)

```
외부 인가 필요?
    │
    ├─ OPA (Rego 정책) ──────> envoyExtAuthzGrpc + OPA sidecar/서비스
    │
    ├─ 자체 인증 서버 ────────> envoyExtAuthzHttp + Custom AuthZ 서비스
    │
    └─ OAuth2 Proxy ──────────> envoyExtAuthzHttp + oauth2-proxy
```

---

## CRITICAL: ext-authz 아키텍처

```
┌──────────────────────────────────────────────────────────┐
│  정책 평가 순서 (CRITICAL)                                │
│                                                           │
│  1. CUSTOM (ext-authz)  ←── 가장 먼저 평가                │
│     │  ALLOW → 다음 단계                                  │
│     │  DENY  → 즉시 거부 (2,3 평가 안 함)                 │
│     │                                                     │
│  2. DENY 정책                                             │
│     │  매칭 → 즉시 거부                                   │
│     │  미매칭 → 다음 단계                                 │
│     │                                                     │
│  3. ALLOW 정책                                            │
│     │  매칭 → 허용                                        │
│     │  미매칭 → 거부 (ALLOW 정책이 있으면)                │
│     │        → 허용 (ALLOW 정책이 없으면)                 │
│                                                           │
│  ※ 정책 없음 = 기본 허용                                  │
│  ※ 빈 spec {} = 모든 트래픽 거부                           │
└──────────────────────────────────────────────────────────┘
```

### 트래픽 흐름

```
Client → Envoy Sidecar → ext-authz 서버 → 인가 결정
                │                              │
                │  ALLOW + 헤더 추가 ←─────────┘
                │  DENY  + 에러 응답 ←─────────┘
                ▼
           Upstream Service
```

---

## ExtensionProvider 등록

### MeshConfig 설정

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    extensionProviders:
    # gRPC 방식 (OPA, 자체 gRPC 서버)
    - name: "opa-authz"
      envoyExtAuthzGrpc:
        service: opa.opa-system.svc.cluster.local
        port: 9191
        timeout: 500ms
        failOpen: false           # ext-authz 장애 시 거부 (보안 우선)

    # HTTP 방식 (자체 HTTP 서버, oauth2-proxy)
    - name: "custom-authz-http"
      envoyExtAuthzHttp:
        service: authz-service.auth.svc.cluster.local
        port: 8080
        timeout: 500ms
        includeRequestHeadersInCheck:
        - authorization
        - x-custom-header
        - cookie
        headersToUpstreamOnAllow:
        - x-user-id
        - x-user-role
        - x-tenant-id
        headersToDownstreamOnDeny:
        - x-error-message
        - www-authenticate
        includeAdditionalHeadersInCheck:
          x-auth-source: "istio-ext-authz"
```

### 주요 옵션

| 옵션 | gRPC | HTTP | 설명 |
|------|------|------|------|
| `timeout` | O | O | 인가 요청 타임아웃 |
| `failOpen` | O | O | ext-authz 장애 시 허용 여부 (기본: false) |
| `includeRequestHeadersInCheck` | - | O | ext-authz로 전달할 요청 헤더 |
| `headersToUpstreamOnAllow` | - | O | 허용 시 업스트림에 추가할 헤더 |
| `headersToDownstreamOnDeny` | - | O | 거부 시 클라이언트에 반환할 헤더 |
| `statusOnError` | O | O | ext-authz 에러 시 HTTP 상태 코드 |

---

## CUSTOM AuthorizationPolicy

### 기본 설정

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: ext-authz-check
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-gateway
  action: CUSTOM
  provider:
    name: "opa-authz"             # MeshConfig에 등록된 이름
  rules:
  - to:
    - operation:
        paths: ["/api/*"]
        notPaths: ["/api/health", "/api/public/*"]
```

### 경로별 다른 ext-authz Provider

```yaml
# API 경로 → OPA
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: api-ext-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-gateway
  action: CUSTOM
  provider:
    name: "opa-authz"
  rules:
  - to:
    - operation:
        paths: ["/api/v1/*"]
---
# Admin 경로 → Custom HTTP AuthZ
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: admin-ext-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-gateway
  action: CUSTOM
  provider:
    name: "custom-authz-http"
  rules:
  - to:
    - operation:
        paths: ["/admin/*"]
```

---

## OPA 연동

### OPA 서비스 배포

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: opa
  namespace: opa-system
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: opa
        image: openpolicyagent/opa:latest-envoy
        args:
        - "run"
        - "--server"
        - "--addr=0.0.0.0:8181"
        - "--diagnostic-addr=0.0.0.0:8282"
        - "--set=plugins.envoy_ext_authz_grpc.addr=:9191"
        - "--set=plugins.envoy_ext_authz_grpc.path=envoy/authz/allow"
        - "--set=decision_logs.console=true"
        - "/policies"
        ports:
        - containerPort: 9191
          name: grpc
        - containerPort: 8181
          name: http
        volumeMounts:
        - name: policies
          mountPath: /policies
      volumes:
      - name: policies
        configMap:
          name: opa-policies
```

### OPA Rego 정책 예시

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: opa-policies
  namespace: opa-system
data:
  policy.rego: |
    package envoy.authz

    import input.attributes.request.http as http_request

    default allow := false

    # JWT 토큰에서 role 추출
    token := payload {
      auth_header := http_request.headers.authorization
      startswith(auth_header, "Bearer ")
      t := substring(auth_header, 7, -1)
      [_, payload, _] := io.jwt.decode(t)
    }

    # admin role은 모든 경로 허용
    allow {
      token.role == "admin"
    }

    # user role은 GET만 허용
    allow {
      token.role == "user"
      http_request.method == "GET"
    }

    # 서비스 간 통신 허용 (SPIFFE ID 기반)
    allow {
      startswith(http_request.headers["x-forwarded-client-cert"],
        "By=spiffe://cluster.local/ns/production/sa/")
    }
```

---

## 다계층 정책 조합 (실전 패턴)

### 시나리오: API Gateway 보안

```yaml
# 1. CUSTOM: 외부 인가 (OPA) - admin 경로
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: custom-admin-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-gateway
  action: CUSTOM
  provider:
    name: "opa-authz"
  rules:
  - to:
    - operation:
        paths: ["/admin/*", "/api/v1/admin/*"]
---
# 2. DENY: dev 네임스페이스 → production 접근 차단
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: deny-dev-access
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-gateway
  action: DENY
  rules:
  - from:
    - source:
        namespaces: ["development", "staging"]
    to:
    - operation:
        paths: ["/api/v1/*"]
        notPaths: ["/api/v1/health"]
---
# 3. ALLOW: 허용된 서비스만 접근
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: allow-authorized
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-gateway
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - "cluster.local/ns/production/sa/frontend"
        - "cluster.local/ns/production/sa/mobile-bff"
    to:
    - operation:
        methods: ["GET", "POST", "PUT", "DELETE"]
        paths: ["/api/v1/*"]
  # 헬스체크는 모두 허용
  - to:
    - operation:
        methods: ["GET"]
        paths: ["/health", "/ready"]
```

---

## OAuth2 Proxy 연동

```yaml
# MeshConfig
extensionProviders:
- name: "oauth2-proxy"
  envoyExtAuthzHttp:
    service: oauth2-proxy.auth.svc.cluster.local
    port: 4180
    includeRequestHeadersInCheck:
    - cookie
    - authorization
    headersToUpstreamOnAllow:
    - x-user
    - x-email
    - authorization
    headersToDownstreamOnDeny:
    - set-cookie
    - location
---
# AuthorizationPolicy
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: oauth2-check
  namespace: production
spec:
  selector:
    matchLabels:
      app: web-frontend
  action: CUSTOM
  provider:
    name: "oauth2-proxy"
  rules:
  - to:
    - operation:
        notPaths: ["/static/*", "/favicon.ico"]
```

---

## 디버깅

```bash
# ext-authz provider 등록 확인
istioctl mesh-config | grep -A 10 extensionProviders

# Envoy ext_authz 필터 확인
istioctl proxy-config listener <pod> -n production -o json | \
  grep -A 20 "ext_authz"

# ext-authz 서버 로그 확인
kubectl logs -n opa-system -l app=opa -f

# AuthorizationPolicy 적용 상태 확인
istioctl x authz check <pod> -n production

# ext-authz 응답 확인 (Envoy 디버그 로그)
istioctl proxy-config log <pod> --level rbac:debug,ext_authz:debug
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| failOpen: true | ext-authz 장애 시 인가 우회 | false 권장 (보안 우선) |
| timeout 미설정 | ext-authz 지연 시 요청 지연 | 500ms 이내 설정 |
| CUSTOM만 사용 | DENY/ALLOW 정책 무시 | 계층별 조합 |
| 모든 경로에 ext-authz | 헬스체크/공개경로까지 인가 | notPaths로 제외 |
| OPA 정책 미테스트 | 프로덕션 인가 장애 | conftest/opa test 사전 검증 |

---

## 체크리스트

- [ ] ExtensionProvider MeshConfig 등록
- [ ] ext-authz 서비스 HA 구성 (replicas >= 2)
- [ ] failOpen 정책 결정 (보안 vs 가용성)
- [ ] timeout 설정 (500ms 이내)
- [ ] CUSTOM + DENY + ALLOW 조합 검증
- [ ] 헬스체크/공개경로 notPaths 제외
- [ ] ext-authz 서버 모니터링/알림 설정
- [ ] OPA 정책 단위 테스트

**관련 skill**: `/istio-security`, `/istio-core`, `/k8s-security`
