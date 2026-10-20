---
name: data-mesh
category: architecture
description: "Data Mesh Architecture 가이드 — Zhamak Dehghani의 분산 데이터 아키텍처. 도메인 소유권, Data as a Product, 셀프서비스 플랫폼, 연합 거버넌스 Use when working with architecture 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Data Mesh Architecture 가이드

Zhamak Dehghani의 분산 데이터 아키텍처. 도메인 소유권, Data as a Product, 셀프서비스 플랫폼, 연합 거버넌스

## Quick Reference (결정 트리)

```
데이터 아키텍처 선택?
    |
    +-- 소규모, 단일 팀 ----------------> Centralized Data Warehouse
    +-- 중규모, 도메인 분리 시작 -------> Data Lakehouse
    +-- 대규모, 도메인 자율성 필요 -----> Data Mesh
    +-- 하이브리드 (실용적) ------------> Federated Governance + Domain Ownership

Data Mesh 도입 준비도?
    |
    +-- 도메인팀 3개+ / 데이터 생산·소비 분리 --> 즉시 도입
    +-- 중앙 데이터팀 과부하 ------------------> 점진적 전환
    +-- 조직 변경 불가 ------------------------> Data Lakehouse 유지
```

---

## CRITICAL: 4가지 핵심 원칙 (Four Pillars)

### 아키텍처 비교

| 항목 | Centralized DW | Data Lakehouse | Data Mesh |
|------|---------------|----------------|-----------|
| **소유권** | 중앙 데이터팀 | 중앙 데이터팀 | 도메인팀 |
| **거버넌스** | 중앙 집중 | 중앙 집중 | 연합(Federated) |
| **확장 병목** | 데이터팀 인력 | 플랫폼 복잡도 | 조직 성숙도 |
| **스키마 관리** | 글로벌 스키마 | Schema-on-Read | Data Contract |
| **적합 규모** | 팀 1~3개 | 팀 3~10개 | 팀 10개+ |
| **기술 스택** | Snowflake/BQ | Spark+Iceberg | 도메인별 자율 |

### 핵심 다이어그램

```
┌─────────────────────────────────────────────────┐
│                Organization                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Order    │  │ Payment  │  │ Customer │       │
│  │ Domain   │  │ Domain   │  │ Domain   │       │
│  │ ┌──────┐ │  │ ┌──────┐ │  │ ┌──────┐ │       │
│  │ │ Data │ │  │ │ Data │ │  │ │ Data │ │       │
│  │ │ Prod │ │  │ │ Prod │ │  │ │ Prod │ │       │
│  │ └──┬───┘ │  │ └──┬───┘ │  │ └──┬───┘ │       │
│  └────┼─────┘  └────┼─────┘  └────┼─────┘       │
│       └──────── Mesh Gateway ─────┘              │
│                     │                            │
│          Federated Governance                    │
└─────────────────────────────────────────────────┘
```

### Pillar 1: Domain-oriented Data Ownership

- 각 도메인팀이 자신의 데이터 파이프라인, 스키마, 품질 책임
- 중앙 데이터팀은 플랫폼 제공자로 역할 전환
- Conway's Law: 데이터 아키텍처 = 조직 구조

### Pillar 2: Data as a Product

- 데이터를 1급 제품으로 취급, SLO 정의 (freshness, completeness, accuracy)
- 소비자 관점 사용성 최적화, 버전 관리/문서화/디스커버리 필수

### Pillar 3: Self-serve Data Platform

- 도메인팀이 인프라 걱정 없이 Data Product 생성/배포
- Terraform 모듈 + Backstage 템플릿으로 자동 프로비저닝

### Pillar 4: Federated Computational Governance

- 글로벌 정책: 자동 적용 (PII 마스킹, 보존 기간, 접근 제어)
- 도메인 로컬 정책: 도메인팀 자율 (스키마 진화, 접근 범위)
- 정책을 코드로 관리 (OPA, Policy-as-Code)

---

## CRITICAL: Data Product 설계

### Data Contract 정의

```yaml
apiVersion: datamesh/v1
kind: DataContract
metadata:
  name: orders-daily
  domain: order
  owner: order-team@company.com
  version: "2.1.0"
spec:
  schema:
    type: avro
    ref: "schemas/orders-daily-v2.avsc"
  slo:
    freshness: "< 1 hour"
    completeness: "> 99.5%"
    accuracy: "> 99.9%"
    availability: "99.95%"
  classification:
    pii: [customer_email, phone]
    retention: "7 years"
  ports:
    input:
      - type: kafka-topic
        name: orders.events
    output:
      - type: rest-api
        path: /data-products/orders
      - type: iceberg-table
        catalog: orders.daily_summary
```

### Data Product Port 유형

| Port 유형 | 설명 | 사용 사례 |
|-----------|------|-----------|
| **Source-aligned** | 원본 도메인 이벤트 그대로 | CDC, 이벤트 스트림 |
| **Consumer-aligned** | 소비자 요구에 맞춘 뷰 | API, 정제된 테이블 |
| **Aggregate** | 여러 소스 조합 | 대시보드, 리포트 |

### 메타데이터 카탈로그

```
개발자 → Backstage/DataHub → Data Product 검색
                                  │
                  ┌───────────────┼───────────────┐
                  ▼               ▼               ▼
            스키마 확인      SLO 확인        Lineage 추적
```

| 도구 | 강점 | 약점 |
|------|------|------|
| **DataHub** | LinkedIn 오픈소스, Lineage 강력 | 운영 복잡 |
| **OpenMetadata** | UI 직관적, 오픈소스 | 커뮤니티 작음 |
| **Atlan** | 엔터프라이즈, AI 기반 | 비용 높음 |
| **Backstage** | 개발자 포탈 통합 | 데이터 전용 아님 |

---

## Spring Boot Data Product 구현

```java
// === Data Product REST API ===
@RestController
@RequestMapping("/data-products/orders")
public class OrderDataProductController {
    private final OrderDataProductService service;
    private final DataContractRegistry contractRegistry;

    @GetMapping
    public DataProductResponse<OrderSummary> getOrders(
            @RequestParam Instant since,
            @RequestParam(defaultValue = "100") int limit,
            @RequestParam(required = false) String cursor) {
        return service.queryOrders(since, limit, cursor);
    }

    @GetMapping("/schema")
    public DataContract getSchema() {
        return contractRegistry.getContract("orders-daily");
    }

    @GetMapping("/slo")
    public DataProductSLO getSLOStatus() {
        return service.currentSLOStatus();
    }
}

// === Data Contract + SLO 모델 ===
public record DataContract(
    String name, String version, String owner, String domain,
    JsonSchema schema, SLO slo, Classification classification
) {}

public record SLO(
    Duration freshness, double completeness,
    double accuracy, double availability
) {}

public record Classification(List<String> piiFields, Duration retention) {}

// === SLO 모니터링 ===
@Component
public class DataProductSLOMonitor {
    private final MeterRegistry meterRegistry;

    @Scheduled(fixedRate = 60_000)
    public void checkFreshness() {
        Instant lastUpdate = getLastUpdateTime();
        Duration lag = Duration.between(lastUpdate, Instant.now());
        meterRegistry.gauge("data_product.freshness_lag_seconds",
            lag.toSeconds());
        if (lag.compareTo(Duration.ofHours(1)) > 0) {
            alertSLOViolation("freshness", lag.toString());
        }
    }

    @Scheduled(fixedRate = 300_000)
    public void checkCompleteness() {
        meterRegistry.gauge("data_product.completeness_ratio",
            calculateCompleteness());
    }
}

// === Response ===
public record DataProductResponse<T>(
    List<T> data, String nextCursor, DataProductMetadata metadata
) {}

public record DataProductMetadata(
    Instant generatedAt, String version,
    long totalRecords, SLOStatus sloStatus
) {}
```

---

## Go Data Product 구현

```go
package datamesh

import "time"

type DataProduct struct {
    Name     string       `json:"name"`
    Domain   string       `json:"domain"`
    Version  string       `json:"version"`
    Owner    string       `json:"owner"`
    Contract DataContract `json:"contract"`
    Ports    []DataPort   `json:"ports"`
}

type DataContract struct {
    SchemaRef      string `json:"schema_ref"`
    SLO            SLO    `json:"slo"`
    Classification Classification `json:"classification"`
}

type SLO struct {
    Freshness    time.Duration `json:"freshness"`
    Completeness float64       `json:"completeness"`
    Accuracy     float64       `json:"accuracy"`
}

type DataPort struct {
    Type     PortType `json:"type"`
    Protocol string   `json:"protocol"`
    Endpoint string   `json:"endpoint"`
}

type PortType string
const (
    SourceAligned   PortType = "source-aligned"
    ConsumerAligned PortType = "consumer-aligned"
    Aggregate       PortType = "aggregate"
)

// === HTTP Handler ===
func NewDataProductHandler(dp *DataProduct) http.Handler {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /data-products/{name}", dp.handleQuery)
    mux.HandleFunc("GET /data-products/{name}/schema", dp.handleSchema)
    mux.HandleFunc("GET /data-products/{name}/slo", dp.handleSLO)
    return mux
}

func (dp *DataProduct) handleQuery(w http.ResponseWriter, r *http.Request) {
    since := r.URL.Query().Get("since")
    t, _ := time.Parse(time.RFC3339, since)
    data, cursor, err := dp.queryData(r.Context(), t)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    json.NewEncoder(w).Encode(DataProductResponse{
        Data: data, NextCursor: cursor,
        Metadata: Metadata{GeneratedAt: time.Now(), Version: dp.Version},
    })
}

// === SLO 모니터링 ===
func (m *SLOMonitor) CheckFreshness(ctx context.Context) error {
    lastUpdate, _ := m.product.getLastUpdate(ctx)
    lag := time.Since(lastUpdate)
    m.metrics.Gauge("data_product_freshness_lag_seconds").Set(lag.Seconds())
    if lag > m.product.Contract.SLO.Freshness {
        return m.alerter.Fire("freshness_violation", lag.String())
    }
    return nil
}
```

---

## Self-serve Data Platform

### Terraform 기반 Data Product 인프라

```hcl
module "data_product" {
  source = "modules/data-product"
  name   = "orders-daily"
  domain = "order"
  owner  = "order-team"
  storage    = { type = "iceberg", bucket = "data-products-${var.domain}", format = "parquet" }
  ingestion  = { source_topic = "orders.events", transform = "sql/orders_daily.sql", schedule = "0 * * * *" }
  governance = { pii_columns = ["customer_email", "phone"], retention_days = 2555, access_policy = "domain-readers" }
}
```

### Backstage Data Product 카탈로그

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: orders-data-product
  annotations:
    datamesh/domain: order
    datamesh/slo-dashboard: "https://grafana/d/orders-dp"
spec:
  type: data-product
  lifecycle: production
  owner: order-team
  providesApis: [orders-data-api]
  dependsOn: [component:order-service]
```

### Apache Iceberg 통합

```
Kafka Topic → Flink/Spark → Iceberg Table → Query Engine (Trino/Presto)
(원본 이벤트)   (변환/집계)    (ACID 보장)
장점: Schema Evolution / Time Travel / Partition Evolution 자동
```

---

## Federated Governance 구현

### 거버넌스 레이어

```
┌─────────────────────────────────────────────┐
│           Global Policies (자동 적용)         │
│  PII 마스킹 │ 보존 정책 │ 감사 로깅 │ ACL    │
├─────────────────────────────────────────────┤
│      Computational Policies (OPA)           │
│  schema_valid() │ slo_met() │ pii_masked()  │
├──────────┬──────────┬───────────────────────┤
│ Order    │ Payment  │ Customer              │
│ - 스키마  │ - PCI    │ - GDPR               │
│   진화   │   준수   │   동의 관리            │
│ - 접근   │ - 암호화  │ - 삭제 요청            │
│   제어   │   필수   │   처리                │
└──────────┴──────────┴───────────────────────┘
```

### Data Lineage 추적

```
주문 이벤트 → 주문 Data Product → 매출 리포트
    │                                  ▲
    └── 결제 이벤트 → 결제 Data Product ─┘

도구: OpenLineage + Marquez
- 자동 수집: Spark/Flink 메타데이터 자동 전송
- 영향 분석: 상류 스키마 변경 시 하류 영향 범위 파악
```

### OPA 정책 예시

```rego
package datamesh.governance

default allow = false

allow {
    input.action == "publish"
    has_valid_contract
    slo_defined
}

has_valid_contract { input.contract.version != ""; input.contract.schema_ref != "" }
slo_defined { input.contract.slo.freshness != ""; input.contract.slo.completeness > 0 }
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 중앙 데이터팀이 모든 데이터 소유 | 병목, 도메인 지식 부족 | 도메인팀에 소유권 이관 |
| Data Contract 없이 API 공개 | 스키마 깨짐, 소비자 장애 | Contract + SLO 필수 정의 |
| 너무 세분화된 Data Product | 관리 복잡, 조합 비용 | Bounded Context 단위 설계 |
| 조직 변경 없이 기술만 도입 | 중앙 팀이 여전히 병목 | 조직 구조 먼저 변경 |
| 모든 데이터를 Product화 | 과도한 오버헤드 | 소비자 있는 것만 Product화 |
| 거버넌스 무시 | 데이터 사일로, 불일치 | Federated Governance 초기 구축 |
| 기술 스택 강제 | 도메인 특성 무시 | 가이드라인만, 자율 선택 |

---

## 실제 도입 사례

### 성공 사례

| 기업 | 규모 | 접근 방식 | 성과 |
|------|------|-----------|------|
| **Netflix** | 수백 도메인 | 점진적 도메인 분리 | 데이터팀 병목 해소 |
| **Zalando** | 3,000+ Data Products | Data Contract 표준화 | 셀프서비스 접근 |
| **JPMorgan** | 글로벌 금융 | 연합 거버넌스 중심 | 규제 준수 + 민첩성 |

### 실패 패턴

```
실패 원인 Top 3:
1. 조직 변경 없이 기술만 도입 → 기존과 동일한 병목
2. Self-serve Platform 없이 도메인 책임 부여 → 반발, 품질 저하
3. Governance 부재 → 데이터 사일로 심화, 상호운용 불가
```

### 점진적 도입 로드맵

```
Phase 1 (3개월): 파일럿 — 2~3개 도메인, Data Contract 표준 수립
Phase 2 (6개월): 플랫폼 — Self-serve MVP, 메타데이터 카탈로그
Phase 3 (12개월): 확장 — 전사 도메인, Federated Governance 자동화
Phase 4 (18개월+): 최적화 — SLO 자동 알림, Data Marketplace
```

---

## 도입 체크리스트

### 조직 준비도

- [ ] 도메인별 크로스펑셔널 팀 구성 가능
- [ ] 중앙 데이터팀 → 플랫폼팀 전환 합의
- [ ] 경영진 스폰서십 확보
- [ ] 데이터 리터러시 교육 계획

### Data Product 정의

- [ ] 소비자 있는 핵심 데이터 식별
- [ ] Data Contract 표준 템플릿 작성
- [ ] SLO 기준 정의 (freshness, completeness, accuracy)
- [ ] Input/Output Port 설계

### 플랫폼

- [ ] 셀프서비스 인프라 프로비저닝 (Terraform)
- [ ] 메타데이터 카탈로그 (DataHub/OpenMetadata)
- [ ] 모니터링 대시보드 (Grafana)
- [ ] Data Lineage 추적 (OpenLineage)

### 거버넌스

- [ ] 글로벌 정책 정의 (PII, 보존, 접근 제어)
- [ ] Policy-as-Code 구현 (OPA)
- [ ] 스키마 진화 전략 (backward/forward compatible)
- [ ] 감사 로깅 활성화

---

## 관련 스킬

- `/msa-ddd` — Bounded Context 설계 (도메인 경계 = Data Product 경계)
- `/msa-event-driven` — 이벤트 드리븐 아키텍처 (Data Product 소스)
- `/kafka-connect-cdc` — CDC 기반 데이터 캡처 (Source-aligned Port)
- `/developer-self-service` — 셀프서비스 플랫폼 패턴
- `/backstage` — 개발자 포탈 (Data Product 카탈로그)
