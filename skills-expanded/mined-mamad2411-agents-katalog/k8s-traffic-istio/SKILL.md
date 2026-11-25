---
name: k8s-traffic-istio
category: service-mesh
description: "Istio Rate Limiting & Circuit Breaker — Istio 기반 Global/Local Rate Limiting, Circuit Breaker 패턴 Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio Rate Limiting & Circuit Breaker

Istio 기반 Global/Local Rate Limiting, Circuit Breaker 패턴

## Quick Reference

```
Istio Rate Limiting
    │
    ├─ Global Rate Limit ───> 중앙 집중식 (Redis 기반)
    │   └─ 모든 Pod에서 공유 카운터
    │
    └─ Local Rate Limit ────> 사이드카 레벨
        └─ Pod별 독립적 카운터
```

---

## 아키텍처

```
┌──────────┐     ┌──────────┐     ┌─────────────┐
│  Client  │────▶│  Envoy   │────▶│  Ratelimit  │
└──────────┘     │ (Sidecar)│     │  Service    │
                 └────┬─────┘     └──────┬──────┘
                      │                  │
                      ▼                  ▼
                 ┌──────────┐      ┌──────────┐
                 │   App    │      │  Redis   │
                 └──────────┘      └──────────┘
```

---

## Global Rate Limiting

### Ratelimit 서비스 배포

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ratelimit-config
  namespace: istio-system
data:
  config.yaml: |
    domain: ticket-api
    descriptors:
      # 전체 API 제한: 10,000 req/s
      - key: generic_key
        value: global
        rate_limit:
          unit: second
          requests_per_unit: 10000

      # 엔드포인트별 제한
      - key: header_match
        value: ticket-reserve
        rate_limit:
          unit: second
          requests_per_unit: 1000

      # 사용자별 제한: 10 req/s per user
      - key: user_id
        rate_limit:
          unit: second
          requests_per_unit: 10
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ratelimit
  namespace: istio-system
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: ratelimit
        image: envoyproxy/ratelimit:v1.4.0
        env:
        - name: REDIS_SOCKET_TYPE
          value: tcp
        - name: REDIS_URL
          value: redis:6379
        - name: RUNTIME_ROOT
          value: /data
        - name: RUNTIME_SUBDIRECTORY
          value: ratelimit
        volumeMounts:
        - name: config
          mountPath: /data/ratelimit/config
```

### EnvoyFilter 설정

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: ratelimit-filter
  namespace: istio-system
spec:
  configPatches:
  - applyTo: HTTP_FILTER
    match:
      context: SIDECAR_INBOUND
      listener:
        filterChain:
          filter:
            name: envoy.filters.network.http_connection_manager
    patch:
      operation: INSERT_BEFORE
      value:
        name: envoy.filters.http.ratelimit
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.http.ratelimit.v3.RateLimit
          domain: ticket-api
          failure_mode_deny: false
          rate_limit_service:
            grpc_service:
              envoy_grpc:
                cluster_name: rate_limit_cluster
            transport_api_version: V3

  - applyTo: CLUSTER
    patch:
      operation: ADD
      value:
        name: rate_limit_cluster
        type: STRICT_DNS
        connect_timeout: 1s
        lb_policy: ROUND_ROBIN
        http2_protocol_options: {}
        load_assignment:
          cluster_name: rate_limit_cluster
          endpoints:
          - lb_endpoints:
            - endpoint:
                address:
                  socket_address:
                    address: ratelimit.istio-system.svc.cluster.local
                    port_value: 8081
```

---

## Local Rate Limiting

중앙 서비스 없이 각 Pod에서 직접 제한:

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: local-ratelimit
  namespace: ticket
spec:
  workloadSelector:
    labels:
      app: ticket-api
  configPatches:
  - applyTo: HTTP_FILTER
    match:
      context: SIDECAR_INBOUND
    patch:
      operation: INSERT_BEFORE
      value:
        name: envoy.filters.http.local_ratelimit
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
          stat_prefix: http_local_rate_limiter
          token_bucket:
            max_tokens: 100
            tokens_per_fill: 100
            fill_interval: 1s
          filter_enabled:
            runtime_key: local_rate_limit_enabled
            default_value:
              numerator: 100
              denominator: HUNDRED
          response_headers_to_add:
          - append: false
            header:
              key: x-rate-limit-remaining
              value: "%DYNAMIC_METADATA(envoy.http.local_rate_limit:tokens_remaining)%"
```

---

## Circuit Breaker

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: ticket-api-circuit-breaker
spec:
  host: ticket-api
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: UPGRADE
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
        maxRequestsPerConnection: 10
        maxRetries: 3
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 30
```

---

## 체크리스트

- [ ] Global Rate Limit 설정
- [ ] Redis HA 구성
- [ ] EnvoyFilter 적용 확인
- [ ] Circuit Breaker 설정
- [ ] Outlier Detection 튜닝

**관련 skill**: `/k8s-traffic`, `/istio-core`, `/istio-gateway`
