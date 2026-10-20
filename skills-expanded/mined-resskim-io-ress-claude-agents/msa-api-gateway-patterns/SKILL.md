---
name: msa-api-gateway-patterns
category: msa
description: "MSA API Gateway 패턴 가이드 — BFF, Gateway Aggregation, Protocol Translation, Layered Auth, API 버저닝 패턴의 설계 원칙과 실전 구현 Use when working with msa 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# MSA API Gateway 패턴 가이드

BFF, Gateway Aggregation, Protocol Translation, Layered Auth, API 버저닝 패턴의 설계 원칙과 실전 구현

## Quick Reference (결정 트리)

```
API Gateway 패턴 선택 가이드
    ├─ 클라이언트 종류가 다양한가?
    │   ├─ Yes ─> 클라이언트별 API 최적화 필요?
    │   │   ├─ Yes ──────────────> BFF (Backend for Frontend)
    │   │   └─ No ───────────────> 단일 Gateway + 응답 필터링
    │   └─ No ──> 단일 API Gateway
    ├─ 여러 서비스 응답을 조합해야 하는가?
    │   ├─ Yes ──────────────────> Gateway Aggregation
    │   └─ No ───────────────────> Gateway Routing (단순 프록시)
    ├─ gRPC 등 프로토콜 변환 필요?
    │   ├─ Yes ──────────────────> Protocol Translation (Envoy Transcoder)
    │   └─ No ───────────────────> HTTP 라우팅으로 충분
    └─ 인증/인가 처리 위치?
        ├─ JWT 검증만 ───────────> Gateway (Coarse-grained)
        ├─ 비즈니스 권한 ────────> Service (Fine-grained RBAC/ABAC)
        └─ 둘 다 ───────────────> Layered Authorization (권장)
Gateway 구현체: Spring Cloud Gateway(WebFlux) | Envoy Gateway(K8s) | Istio | Kong
```

---

## CRITICAL: Gateway 패턴 비교

| 패턴 | 목적 | 복잡도 | 핵심 이점 |
|------|------|-------|----------|
| Gateway Routing | 단순 요청 라우팅 | 낮음 | 단일 진입점, TLS 종료 |
| Gateway Aggregation | 다중 서비스 응답 조합 | 중 | 네트워크 왕복 감소 |
| Backend for Frontend | 클라이언트별 최적 API | 높음 | 클라이언트 맞춤 응답 |
| Gateway Offloading | 횡단 관심사 위임 | 중 | 서비스 로직 단순화 |
| Protocol Translation | gRPC <-> REST 변환 | 중 | 레거시/프론트 호환 |

---

## Backend for Frontend (BFF)

### 아키텍처

```
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ Web App  │  │Mobile App│  │3rd Party │
  └────┬─────┘  └────┬─────┘  └────┬─────┘
  ┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐
  │ Web BFF  │  │Mobile BFF│  │Partner   │
  │(풍부한    │  │(경량      │  │BFF       │
  │ 데이터)   │  │ 페이로드) │  │(제한 API)│
  └──┬──┬──┬─┘  └──┬──┬────┘  └──┬──┬────┘
  ┌──▼──▼──▼───────▼──▼──────────▼──▼──────┐
  │  [User Svc]  [Order Svc]  [Product Svc] │
  └─────────────────────────────────────────┘
```

- Web BFF: 대시보드용 풍부한 데이터 + 차트 집계
- Mobile BFF: 경량 payload, 이미지 최적화, 페이징 조정
- Partner BFF: 제한된 필드, API Key 인증, Rate Limit 강화

### Spring Cloud Gateway BFF 구현

```java
@Configuration
public class BffGatewayConfig {
    @Bean
    public RouteLocator bffRoutes(RouteLocatorBuilder builder) {
        return builder.routes()
            // 웹 BFF: 전체 필드 반환
            .route("web-user", r -> r.path("/web/api/users/**")
                .filters(f -> f.rewritePath("/web/api/(?<s>.*)", "/${s}")
                    .addResponseHeader("X-BFF-Type", "web"))
                .uri("lb://user-service"))
            // 모바일 BFF: compact 포맷
            .route("mobile-user", r -> r.path("/mobile/api/users/**")
                .filters(f -> f.rewritePath("/mobile/api/(?<s>.*)", "/${s}")
                    .addRequestHeader("X-Response-Format", "compact"))
                .uri("lb://user-service"))
            .build();
    }
}
```

K8s 배포: 각 BFF를 독립 Deployment로 분리하여 트래픽 패턴별 독립 스케일링

---

## Gateway Aggregation

### 여러 서비스를 병렬 호출 -> 단일 응답

```
  Client ── GET /dashboard ──> Gateway ──┬── User Svc
                                         ├── Order Svc
                                         └── Stats Svc
  Client <── 조합 JSON ─────── Gateway <─┘
```

### Spring Cloud Gateway + WebClient

```java
@RestController
@RequiredArgsConstructor
public class DashboardAggregationController {
    private final WebClient.Builder webClient;

    @GetMapping("/api/dashboard/{userId}")
    public Mono<DashboardResponse> getDashboard(@PathVariable String userId) {
        Mono<UserProfile> user = webClient.build()
            .get().uri("http://user-service/users/{id}", userId)
            .retrieve().bodyToMono(UserProfile.class)
            .timeout(Duration.ofSeconds(3))
            .onErrorResume(e -> Mono.just(UserProfile.fallback(userId)));
        Mono<List<Order>> orders = webClient.build()
            .get().uri("http://order-service/orders?userId={id}", userId)
            .retrieve().bodyToFlux(Order.class).collectList()
            .timeout(Duration.ofSeconds(3))
            .onErrorResume(e -> Mono.just(List.of()));
        Mono<DashboardStats> stats = webClient.build()
            .get().uri("http://stats-service/stats/{id}", userId)
            .retrieve().bodyToMono(DashboardStats.class)
            .timeout(Duration.ofSeconds(2))
            .onErrorResume(e -> Mono.just(DashboardStats.empty()));
        return Mono.zip(user, orders, stats)
            .map(t -> new DashboardResponse(t.getT1(), t.getT2(), t.getT3()));
    }
}
```

### Partial Failure 처리 원칙

- 핵심 서비스 실패 (User) -> 전체 에러 반환
- 보조 서비스 실패 (Stats) -> Fallback 값 + 부분 응답
- 응답에 `degradedServices` 필드로 실패 서비스 목록 포함
- 개별 서비스 timeout 2~5초 설정 필수

---

## Protocol Translation

### gRPC <-> REST 트랜스코딩

```
  REST Client ── HTTP/JSON ──> Envoy (Transcoder) ── gRPC ──> gRPC Service
```

### Envoy gRPC-JSON Transcoder 핵심 설정

```yaml
# envoy.yaml 핵심 부분
http_filters:
  - name: envoy.filters.http.grpc_json_transcoder
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.grpc_json_transcoder.v3.GrpcJsonTranscoder
      proto_descriptor: "/etc/envoy/proto.pb"   # protoc으로 생성한 descriptor
      services: ["mypackage.ProductService"]     # 트랜스코딩 대상 서비스
      print_options:
        always_print_primitive_fields: true
# 클러스터 설정: gRPC는 HTTP/2 필수
clusters:
  - name: grpc_backend
    typed_extension_protocol_options:
      envoy.extensions.upstreams.http.v3.HttpProtocolOptions:
        "@type": type.googleapis.com/envoy.extensions.upstreams.http.v3.HttpProtocolOptions
        explicit_http_config:
          http2_protocol_options: {}
    load_assignment:
      cluster_name: grpc_backend
      endpoints:
        - lb_endpoints:
            - endpoint:
                address:
                  socket_address: { address: grpc-service, port_value: 50051 }
```

### Proto HTTP 매핑 (google.api.http)

```protobuf
syntax = "proto3";
import "google/api/annotations.proto";
service ProductService {
  rpc GetProduct(GetProductRequest) returns (Product) {
    option (google.api.http) = { get: "/v1/products/{product_id}" };
  }
  rpc CreateProduct(CreateProductRequest) returns (Product) {
    option (google.api.http) = { post: "/v1/products" body: "*" };
  }
}
```

---

## Layered Authorization (CRITICAL)

### 인증/인가 계층 분리

```
  Client + JWT ──> [ Gateway: Coarse-grained ]     [ Service: Fine-grained ]
                    ├ JWT 서명 검증 (JWKS)      ->   ├ RBAC: 역할 기반 접근
                    ├ 토큰 만료 확인                  ├ ABAC: 속성 기반 (소유자)
                    └ Rate Limit / CORS              └ 비즈니스 규칙 검증
```

| 계층 | 담당 | 구현 위치 |
|------|------|----------|
| Gateway | JWT 검증, Rate Limit, CORS | Spring Cloud Gateway Filter |
| Service | RBAC, ABAC, 리소스 소유자 | Spring Security @PreAuthorize |
| IAM | OAuth2/OIDC 토큰 발급 | Keycloak, Auth0, Cognito |

### Spring Cloud Gateway JWT 필터

```java
@Component
public class JwtAuthGatewayFilterFactory
        extends AbstractGatewayFilterFactory<JwtAuthGatewayFilterFactory.Config> {
    private final ReactiveJwtDecoder jwtDecoder;

    public JwtAuthGatewayFilterFactory(ReactiveJwtDecoder jwtDecoder) {
        super(Config.class);
        this.jwtDecoder = jwtDecoder;
    }

    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            String auth = exchange.getRequest()
                .getHeaders().getFirst(HttpHeaders.AUTHORIZATION);
            if (auth == null || !auth.startsWith("Bearer ")) {
                exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
                return exchange.getResponse().setComplete();
            }
            return jwtDecoder.decode(auth.substring(7))
                .flatMap(jwt -> {
                    // 검증된 클레임을 하위 서비스 헤더로 전파
                    ServerHttpRequest req = exchange.getRequest().mutate()
                        .header("X-User-Id", jwt.getSubject())
                        .header("X-User-Roles",
                            String.join(",", jwt.getClaimAsStringList("roles")))
                        .build();
                    return chain.filter(exchange.mutate().request(req).build());
                })
                .onErrorResume(e -> {
                    exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
                    return exchange.getResponse().setComplete();
                });
        };
    }
    @Data
    public static class Config {
        private List<String> excludePaths = List.of("/auth/**", "/health");
    }
}
```

### WebFlux Security Config

```java
@Configuration
@EnableWebFluxSecurity
public class GatewaySecurityConfig {
    @Bean
    public SecurityWebFilterChain securityFilterChain(ServerHttpSecurity http) {
        return http.csrf(ServerHttpSecurity.CsrfSpec::disable)
            .authorizeExchange(auth -> auth
                .pathMatchers("/auth/**", "/health", "/actuator/**").permitAll()
                .pathMatchers("/admin/**").hasAuthority("SCOPE_admin")
                .anyExchange().authenticated())
            .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
            .build();
    }
    @Bean // JWKS URI에서 공개 키로 JWT 서명 검증
    public ReactiveJwtDecoder jwtDecoder() {
        return NimbusReactiveJwtDecoder
            .withJwkSetUri("https://auth.example.com/.well-known/jwks.json").build();
    }
}
```

---

## API Versioning & Deprecation

### 버저닝 전략

| 전략 | 형태 | 장점 | 단점 |
|------|------|------|------|
| URI Path | `/v1/users` | 직관적, 캐싱 용이 | URL 변경 필요 |
| Header | `Accept: vnd.api.v2+json` | URL 깨끗 | 테스트 불편 |
| Query | `/users?version=2` | 간단 | 비표준 |

**권장**: URI Path (가장 널리 사용, Gateway 라우팅 용이)

### Gateway 버전 라우팅 + Deprecation

```java
@Bean
public RouteLocator versionedRoutes(RouteLocatorBuilder builder) {
    return builder.routes()
        .route("users-v1", r -> r.path("/v1/users/**")
            .filters(f -> f.rewritePath("/v1/(?<s>.*)", "/${s}")
                .addResponseHeader("Deprecation", "true")          // RFC 9745
                .addResponseHeader("Sunset", "2026-01-01T00:00:00Z") // RFC 8594
                .addResponseHeader("Link",
                    "<https://api.example.com/docs/v2>; rel=\"deprecation\""))
            .uri("lb://user-service-v1"))
        .route("users-v2", r -> r.path("/v2/users/**")
            .filters(f -> f.rewritePath("/v2/(?<s>.*)", "/${s}"))
            .uri("lb://user-service-v2"))
        .build();
}
```

### 마이그레이션 타임라인

```
Phase 1 (D-12월): v2 출시 공지 + 마이그레이션 가이드 + 병행 운영
Phase 2 (D-6월):  v1에 Deprecation 헤더 추가, 사용량 모니터링 시작
Phase 3 (D-3월):  Sunset 헤더 추가, 잔여 사용자 연락, Rate Limit 축소
Phase 4 (D-Day):  v1 -> 410 Gone, 30일 유지 후 Route 완전 제거
```

---

## Gateway 성능 최적화

### 경량 유지 원칙 (CRITICAL)

Gateway에 비즈니스 로직을 넣지 않는다. 라우팅/인증/Rate Limit/CORS/TLS 전용.
DB 조회, 데이터 변환, 비즈니스 검증, 외부 API 체인, 세션 관리는 절대 금지.

### 핵심 설정 (Spring Cloud Gateway)

```yaml
spring.cloud.gateway:
  httpclient:
    pool: { type: ELASTIC, max-connections: 500, max-idle-time: 20s }
    connect-timeout: 3000
    response-timeout: 10s
  filter.local-response-cache: { enabled: true, time-to-live: 5m, size: 100MB }
  default-filters:
    - name: RequestRateLimiter
      args:
        redis-rate-limiter.replenishRate: 100
        redis-rate-limiter.burstCapacity: 200
        key-resolver: "#{@userKeyResolver}"
```

---

## Kubernetes 배포

### Envoy Gateway + HTTPRoute

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata: { name: envoy-gateway }
spec: { controllerName: gateway.envoyproxy.io/gatewayclass-controller }
---
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata: { name: api-gateway, namespace: infra }
spec:
  gatewayClassName: envoy-gateway
  listeners:
    - { name: https, protocol: HTTPS, port: 443,
        tls: { mode: Terminate, certificateRefs: [{ kind: Secret, name: api-tls }] } }
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata: { name: user-route, namespace: app }
spec:
  parentRefs: [{ name: api-gateway, namespace: infra }]
  hostnames: ["api.example.com"]
  rules:
    - matches: [{ path: { type: PathPrefix, value: /v2/users } }]
      backendRefs:                              # Canary 배포
        - { name: user-svc-v2, port: 8080, weight: 90 }
        - { name: user-svc-v3, port: 8080, weight: 10 }
    - matches: [{ path: { type: PathPrefix, value: /v1/users } }]
      filters:
        - type: ResponseHeaderModifier
          responseHeaderModifier:
            add: [{ name: Deprecation, value: "true" },
                  { name: Sunset, value: "2026-01-01T00:00:00Z" }]
      backendRefs: [{ name: user-svc-v1, port: 8080 }]
```

### 모니터링 핵심 지표

- `spring_cloud_gateway_requests_seconds` - 요청 레이턴시 (히스토그램)
- `spring_cloud_gateway_requests_total` - 전체 요청 수 (라우트별)
- `spring_cloud_gateway_requests_errors` - 에러 수 (4xx/5xx 분리)

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Gateway에 비즈니스 로직 | 미니 모놀리스화, 배포 병목 | 라우팅/인증/Rate Limit만 유지 |
| 단일 Gateway로 모든 클라이언트 | 모든 클라이언트에 비최적화 | BFF 패턴으로 분리 |
| Gateway에서 DB 직접 조회 | DB 커넥션 고갈 | 서비스를 통한 접근만 |
| JWT 검증 없이 서비스 노출 | 인증 우회 가능 | Gateway JWT + 내부 mTLS |
| Aggregation 타임아웃 미설정 | 느린 서비스가 전체 지연 | 개별 timeout + Partial Failure |
| 모든 API 버전 영구 유지 | 유지보수/보안 비용 | Sunset Header로 종료 공지 |
| Rate Limit 미적용 | DDoS에 백엔드 노출 | Edge Rate Limiting 필수 |
| 로그에 민감 정보 | PII/토큰 유출 | 마스킹 필터 적용 |
| 단일 인스턴스 운영 | SPOF | 2+ 레플리카 + HPA |
| gRPC 에러 매핑 누락 | 전부 HTTP 500 변환 | gRPC<->HTTP 상태코드 매핑 |

---

## 체크리스트

### 설계

- [ ] Gateway 패턴 선택 (Routing / Aggregation / BFF / Offloading)
- [ ] BFF 분리 여부 결정 (Web / Mobile / Partner)
- [ ] 인증/인가 계층 설계 (Gateway: coarse / Service: fine-grained)
- [ ] API 버저닝 전략 확정 (URI Path 권장)
- [ ] Protocol Translation 필요 여부 (gRPC <-> REST)

### 구현

- [ ] JWT 검증 필터 (JWKS 기반 서명 검증)
- [ ] Rate Limiting (Redis 분산 제한)
- [ ] Timeout (connect 3s, response 10s) + Connection Pool
- [ ] 요청/응답 로깅 (민감 정보 마스킹)
- [ ] CORS 정책 설정

### 운영

- [ ] 2+ 레플리카 + HPA
- [ ] Prometheus 메트릭 (레이턴시, 에러율, 요청수)
- [ ] Deprecation/Sunset 헤더 + 사용량 모니터링
- [ ] Circuit Breaker 연계 (Resilience4j / Envoy Outlier Detection)
- [ ] TLS 인증서 갱신 + JWT 키 로테이션
- [ ] 부하 테스트 (Gateway throughput 확인)

---

## 참조 스킬

- `/gateway-api` - Kubernetes Gateway API 리소스 설계
- `/gateway-api-migration` - Ingress에서 Gateway API 마이그레이션
- `/msa-resilience` - Circuit Breaker, Retry, Bulkhead 패턴
- `/spring-security` - Spring Security OAuth2/JWT 심화
- `/msa-event-driven` - 비동기 통신으로 Gateway 부하 분산
