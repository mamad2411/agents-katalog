---
name: cell-based-architecture
category: architecture
description: "Cell-Based Architecture 가이드 — 대규모 장애 격리를 위한 Cell 기반 아키텍처: Bulkhead 패턴, 블라스트 반경 제한, Horizontal Isolation. Use when cascade failure 격리 / 다중 리전 blast radius 분석이 필요할 때."
effort: max
deprecated: false
---

# Cell-Based Architecture 가이드

대규모 장애 격리를 위한 Cell 기반 아키텍처: Bulkhead 패턴, 블라스트 반경 제한, Horizontal Isolation

## Quick Reference (결정 트리)

```
아키텍처 선택?
    │
    ├─ 트래픽 < 10K/s, 단순 도메인 ──────> Modular Monolith
    │   └─ 장점: 개발 단순, 배포 간단 / 단점: 확장 제한
    │
    ├─ 기능별 독립 배포 필요 ─────────────> Microservices
    │   └─ 장점: 독립 배포, 기술 다양성 / 단점: 운영 복잡
    │
    └─ 트래픽 > 100K/s, 장애 격리 중요 ──> Cell-Based Architecture
        └─ 장점: Blast Radius 제한, 무제한 수평 확장 / 단점: 라우팅 복잡

Cell 파티셔닝 키?
    │
    ├─ B2B SaaS ─────────> Tenant ID (고객사별 격리)
    ├─ 글로벌 서비스 ──────> Geographic (리전별 격리)
    ├─ 대규모 트래픽 ──────> User ID Hash (균등 분산)
    └─ 복합 요구사항 ──────> Composite Key (tenant+region)
```

---

## CRITICAL: Cell-Based Architecture 개념

```
┌──────────────────────────────────────────────────────────┐
│                Cell-Based Architecture                     │
├──────────────────────────────────────────────────────────┤
│        ┌──────────────────────────────────────┐          │
│        │      Cell Router (Gateway)           │          │
│        │  Cell Key → Cell Mapping Logic       │          │
│        └───────┬──────────┬──────────┬────────┘          │
│                │          │          │                    │
│      ┌─────────▼──┐  ┌───▼──────┐  ┌▼──────────┐        │
│      │   Cell A   │  │  Cell B  │  │  Cell C   │        │
│      ├────────────┤  ├──────────┤  ├───────────┤        │
│      │ App Tier   │  │ App Tier │  │ App Tier  │        │
│      │ Cache(독립)│  │ Cache    │  │ Cache     │        │
│      │ DB (독립)  │  │ DB       │  │ DB        │        │
│      │ Queue(독립)│  │ Queue    │  │ Queue     │        │
│      └────────────┘  └──────────┘  └───────────┘        │
│                                                           │
│  핵심 원칙:                                               │
│  1. 각 Cell은 완전히 독립적 (상태 공유 X)                  │
│  2. Cell 장애 = 전체 트래픽의 1/N만 영향                   │
│  3. Blast Radius (폭발 반경) 제한                          │
│  4. 수평 확장: Cell 추가로 선형 확장                        │
└──────────────────────────────────────────────────────────┘
```

### AWS Well-Architected Cell 원칙

- **독립성**: 각 Cell은 자체 컴퓨팅, 스토리지, 네트워크 보유
- **격리**: Cell 간 상태 공유 금지, 장애 전파 차단
- **균등 분산**: Cell Router가 트래픽 균등 분배
- **고정 크기**: Cell 크기는 고정, 확장은 Cell 추가로만 수행

### 실전 사례

| 회사 | Cell 구성 | 파티셔닝 키 | 규모 |
|------|----------|-----------|------|
| **Slack** | Workspace별 Cell | Workspace ID | 10M+ 워크스페이스 |
| **Amazon Prime Video** | 리전별 Cell | Geographic | 글로벌 스트리밍 |
| **DoorDash** | 지역별 Cell | City Code | 미국 4000+ 도시 |
| **Uber** | Hex Geohash Cell | Geospatial | 글로벌 라이드 |

---

## Cell vs Microservices vs Monolith

| 구분 | Monolith | Microservices | Cell-Based |
|------|----------|---------------|------------|
| **배포 단위** | 전체 앱 | 서비스 | Cell (다수 서비스 묶음) |
| **상태 공유** | 공유 DB | 독립 DB (서비스별) | 독립 DB (Cell별) |
| **장애 격리** | 전체 영향 | 서비스 단위 | Cell 단위 (1/N) |
| **확장 방법** | Vertical | 서비스별 HPA | Cell 추가 (Horizontal) |
| **운영 복잡도** | 낮음 | 높음 | 매우 높음 |
| **Blast Radius** | 100% | 서비스 의존성 범위 | 1/N (고정) |
| **적합 규모** | < 10K/s | 10K~100K/s | > 100K/s |

---

## Cell 아키텍처 구성 요소

### 1. Cell Router

```
역할: 요청을 올바른 Cell로 라우팅
요구사항:
  ├─ Cell Key 추출 (Header, Path, Body)
  ├─ Cell Mapping (Hash/Lookup)
  ├─ Health Check (비정상 Cell 제외)
  └─ Fallback (장애 시 다른 Cell)
```

### 2. Cell Key 전략

| 전략 | 키 유형 | 적용 사례 | 장단점 |
|------|--------|----------|--------|
| **Tenant-based** | Customer ID | B2B SaaS, 멀티테넌트 | 고객별 완전 격리, 불균등 가능 |
| **Geographic** | Region/City | 글로벌 서비스, 지역 규제 | 지연 최소화, 리전별 관리 필요 |
| **Hash-based** | User ID % N | 대규모 C2C, SNS | 균등 분산, 리밸런싱 복잡 |
| **Composite** | Tenant+Region | 엔터프라이즈 글로벌 | 유연성 최대, 복잡도 증가 |

### 3. Cell 내부 구성

```yaml
# Cell 구성 요소 (예시: 주문 Cell)
Cell-Order-A:
  Services:
    - order-api (3 replicas)
    - order-processor (5 replicas)
    - inventory-service (2 replicas)
  Data:
    - PostgreSQL (Primary + Read Replica)
    - Redis Cluster (3 nodes)
  Messaging:
    - Kafka Topic: order-events-cell-a (3 partitions)
  Network:
    - 독립 VPC Subnet
    - Internal Load Balancer
```

---

## Cell Router 구현

### Spring Boot Cell Router (Consistent Hashing)

```java
@Component
public class CellRouter {
    private final Map<String, String> tenantCellMap;
    private final ConsistentHash<String> hashRing;

    public CellRouter(@Value("#{${cell.tenant-mapping}}") Map<String, String> mapping) {
        this.tenantCellMap = mapping;
        this.hashRing = new ConsistentHash<>(
            List.of("cell-a", "cell-b", "cell-c"), 100); // 가상 노드 수
    }

    public String routeCell(HttpServletRequest request) {
        // 1. Tenant 기반 라우팅 (우선순위)
        String tenantId = request.getHeader("X-Tenant-ID");
        if (tenantId != null && tenantCellMap.containsKey(tenantId))
            return tenantCellMap.get(tenantId);
        // 2. User Hash 기반 라우팅
        String userId = request.getHeader("X-User-ID");
        if (userId != null) return hashRing.get(userId);
        // 3. Fallback: 랜덤 Cell
        return hashRing.get(UUID.randomUUID().toString());
    }
}

// Consistent Hashing 구현
public class ConsistentHash<T> {
    private final TreeMap<Long, T> ring = new TreeMap<>();

    public ConsistentHash(List<T> nodes, int virtualNodes) {
        nodes.forEach(n -> {
            for (int i = 0; i < virtualNodes; i++)
                ring.put(hash(n.toString() + ":" + i), n);
        });
    }

    public T get(String key) {
        if (ring.isEmpty()) throw new IllegalStateException("No nodes available");
        Map.Entry<Long, T> entry = ring.ceilingEntry(hash(key));
        return entry != null ? entry.getValue() : ring.firstEntry().getValue();
    }

    private long hash(String key) {
        return MurmurHash3.hash64(key.getBytes(StandardCharsets.UTF_8));
    }
}
```

### Istio VirtualService 기반 라우팅

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: cell-router
  namespace: production
spec:
  hosts: [api.example.com]
  gateways: [istio-gateway]
  http:
    # Cell Key = Header에서 추출
    - match:
        - headers:
            x-tenant-id:
              regex: "^(tenant[0-4]).*"
      route:
        - destination:
            host: order-service.cell-a.svc.cluster.local
            port: { number: 80 }
      headers:
        request:
          set: { x-cell-id: "cell-a" }
    - match:
        - headers:
            x-tenant-id:
              regex: "^(tenant[5-9]).*"
      route:
        - destination:
            host: order-service.cell-b.svc.cluster.local
    # Fallback: 헤더 없으면 50/50 분배
    - route:
        - destination: { host: order-service.cell-a.svc.cluster.local }
          weight: 50
        - destination: { host: order-service.cell-b.svc.cluster.local }
          weight: 50
```

---

## Kubernetes Cell 구현

### Namespace per Cell + ArgoCD ApplicationSet

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: order-service-cells
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - cell: cell-a
            replicas: "5"
            db: order-db-cell-a.rds.amazonaws.com
          - cell: cell-b
            replicas: "5"
            db: order-db-cell-b.rds.amazonaws.com
          - cell: cell-c
            replicas: "3"
            db: order-db-cell-c.rds.amazonaws.com
  template:
    metadata:
      name: order-service-{{cell}}
    spec:
      project: default
      source:
        repoURL: https://github.com/example/order-service
        targetRevision: main
        path: k8s/overlays/cell
        helm:
          parameters:
            - { name: cellId, value: "{{cell}}" }
            - { name: replicaCount, value: "{{replicas}}" }
            - { name: database.host, value: "{{db}}" }
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{cell}}"
      syncPolicy:
        automated: { prune: true, selfHeal: true }
```

---

## Cell Sizing & Scaling

### Fixed-Size Cell 원칙

```
Cell 크기: 고정 (예: 10K RPS)

수평 확장 전략:
  현재: Cell A (10K) + Cell B (10K) = 20K RPS
  확장: + Cell C (10K) → 30K RPS

❌ 잘못된 방법: Cell A를 20K로 확장 (Vertical)
✅ 올바른 방법: Cell C 추가 (Horizontal)

장점:
  - 예측 가능한 성능
  - 균일한 Blast Radius (항상 1/N)
  - 단순한 용량 계획
```

### Cell 용량 모니터링

```promql
# Cell 포화도 (80% 이상 시 알림)
(sum(rate(http_requests_total{cell_id="cell-a"}[5m]))
 / scalar(max_rps{cell_id="cell-a"})) * 100 > 80

# Cell별 에러율
sum(rate(http_requests_total{cell_id="cell-a", status=~"5.."}[5m]))
/ sum(rate(http_requests_total{cell_id="cell-a"}[5m])) * 100

# Cell DB 커넥션 사용률
pg_stat_database_numbackends{cell_id="cell-a"}
/ pg_settings_max_connections{cell_id="cell-a"} * 100
```

---

## 장애 격리 & 복구

### Cell Health Check (Istio DestinationRule)

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: cell-a-outlier-detection
spec:
  host: order-service.cell-a.svc.cluster.local
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 100        # Cell 전체 제거 가능
    connectionPool:
      tcp: { maxConnections: 100 }
      http: { http1MaxPendingRequests: 50, http2MaxRequests: 100 }
```

### Chaos Engineering: Cell 장애 테스트

```yaml
# Chaos Mesh: Cell A의 Pod 50% 랜덤 Kill
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: cell-a-failure-test
  namespace: chaos-testing
spec:
  action: pod-kill
  mode: percentage
  value: "50"
  selector:
    namespaces: [cell-a]
    labelSelectors: { app: order-service }
  scheduler:
    cron: "@every 30m"

# 예상 결과:
# 1. Cell A: 50% Pod Kill → 나머지 50% Pod이 부하 처리
# 2. Cell A 과부하 시 Outlier Detection 작동 → Cell 전체 제거
# 3. Cell Router: Cell A 요청을 Cell B/C로 자동 우회
# 4. 영향 범위: Cell A 담당 Tenant만 영향 (전체 1/3)
```

---

## Cell 데이터 마이그레이션

### Tenant 재배치 (Zero-Downtime)

```java
@Service
public class CellMigrationService {
    private final JdbcTemplate jdbcTemplate;
    private final KafkaTemplate<String, TenantEvent> kafka;

    @Transactional
    public void migrateTenant(String tenantId, String fromCell, String toCell) {
        log.info("Migrating tenant {} from {} to {}", tenantId, fromCell, toCell);
        setTenantReadOnly(tenantId, true);           // 1. 신규 쓰기 차단
        copyTenantData(tenantId, fromCell, toCell);   // 2. 데이터 복제 (DMS/CDC)
        updateCellMapping(tenantId, toCell);           // 3. Cell Router 업데이트
        setTenantReadOnly(tenantId, false);            // 4. Read-only 해제
        kafka.send("tenant-events",
            TenantEvent.migrated(tenantId, fromCell, toCell)); // 5. 이벤트 발행
    }
}
```

```
마이그레이션 타임라인:
  Phase 1: 복제 시작 (백그라운드, 초기 복사 ~10분)
  Phase 2: Read-only 전환 (~2초)
  Phase 3: 라우팅 전환 (~1초)
  Phase 4: 검증 (~1분, Cell C 트래픽 확인, 에러율 모니터링)
  Phase 5: 정리 (백그라운드, Cell A에서 tenantX 데이터 삭제)
  총 다운타임: ~3초 (Read-only 전환 + 라우팅 업데이트)
```

---

## Gateway API 기반 Cell 라우팅

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: cell-route
  namespace: production
spec:
  parentRefs:
    - name: api-gateway
      namespace: gateway-system
  hostnames: [api.example.com]
  rules:
    # Tenant-based routing
    - matches:
        - headers:
            - name: x-tenant-id
              value: "tenant-[0-4].*"
              type: RegularExpression
      backendRefs:
        - name: order-service
          namespace: cell-a
          port: 80
    - matches:
        - headers:
            - name: x-tenant-id
              value: "tenant-[5-9].*"
              type: RegularExpression
      backendRefs:
        - name: order-service
          namespace: cell-b
          port: 80
    # Canary: 10% → Cell C (신규 Cell 검증)
    - matches:
        - headers:
            - name: x-canary
              value: "true"
      backendRefs:
        - name: order-service
          namespace: cell-c
          port: 80
          weight: 10
        - name: order-service
          namespace: cell-a
          port: 80
          weight: 90
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Cell 크기 불균등 | 예측 불가능한 장애 영향 | Fixed-size Cell 원칙 준수 |
| Cell 간 DB 공유 | 격리 실패, 장애 전파 | Cell별 독립 DB 필수 |
| Cell Key 미설계 | 부하 불균형 | Consistent Hashing + 모니터링 |
| 수직 확장 (Cell 확대) | Blast Radius 증가 | Cell 추가 (수평 확장) |
| Cell Router SPOF | 전체 장애 | HA 구성 + Health Check |
| 마이그레이션 미자동화 | 수동 작업 리스크 | IaC + Blue-Green 마이그레이션 |
| Cross-Cell 트랜잭션 | 분산 트랜잭션 복잡도 | Cell 경계 = 도메인 경계 설계 |
| Cell Health 미모니터링 | 장애 감지 지연 | Outlier Detection + Alert |

---

## 체크리스트

### 설계
- [ ] Cell 파티셔닝 키 선택 (Tenant/Geographic/Hash)
- [ ] Cell 크기 결정 (RPS, DB 커넥션, 리소스)
- [ ] Blast Radius 계산 (전체의 1/N)
- [ ] Cell 간 의존성 제거 (독립성 검증)

### 구현
- [ ] Cell Router 구현 (Istio/Gateway API/Code)
- [ ] Consistent Hashing 또는 Mapping Table
- [ ] Namespace per Cell + ArgoCD ApplicationSet
- [ ] Cell별 독립 DB + Cache + Queue

### 마이그레이션
- [ ] Tenant 마이그레이션 자동화
- [ ] Zero-Downtime 절차 정의
- [ ] Rollback 전략 수립

### 장애 대응
- [ ] Outlier Detection 설정 (Istio DestinationRule)
- [ ] Cell Drain 절차서 작성
- [ ] Chaos Engineering 테스트 (Cell 장애 시뮬레이션)

### 운영
- [ ] Cell 포화도 모니터링 (80% 알림)
- [ ] Cell별 SLI/SLO 정의
- [ ] 새 Cell 프로비저닝 자동화 (Crossplane/Terraform)

**관련 스킬**: `/msa-resilience`, `/high-traffic-design`, `/disaster-recovery`, `/k8s-autoscaling`, `/istio-core`, `/database-sharding`
