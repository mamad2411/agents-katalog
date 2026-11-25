---
name: kafka-streams
category: messaging
description: "Kafka Streams 가이드 — KTable, GlobalKTable, Windowing, Interactive Queries, Stateful Processing, RocksDB 튜닝 Use when working with messaging 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Kafka Streams 가이드

KTable, GlobalKTable, Windowing, Interactive Queries, Stateful Processing, RocksDB 튜닝

## Quick Reference (결정 트리)

```
스트림 처리 요구사항?
    │
    ├─ Stateless 변환 ─────> KStream (filter, map, flatMap)
    │
    ├─ 최신 상태 유지 ─────> KTable (compact topic 기반)
    │       │
    │       ├─ 파티션 로컬 ──> KTable (Co-partitioning 필요)
    │       └─ 전체 데이터 ──> GlobalKTable (소규모 참조 데이터)
    │
    ├─ 시간 기반 집계 ─────> Windowed KTable
    │       │
    │       ├─ 고정 구간 ────> Tumbling Window
    │       ├─ 겹치는 구간 ──> Hopping Window
    │       └─ 활동 기반 ────> Session Window
    │
    └─ 외부 쿼리 ──────────> Interactive Queries (ReadOnly Store)
```

---

## CRITICAL: Kafka Streams 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│  Kafka Streams Application                                   │
│                                                              │
│  ┌─────────────────────────────────────────────┐            │
│  │  Stream Thread 1                             │            │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  │            │
│  │  │ Task 0   │  │ Task 1   │  │ Task 2   │  │            │
│  │  │ P0       │  │ P1       │  │ P2       │  │            │
│  │  │ RocksDB  │  │ RocksDB  │  │ RocksDB  │  │            │
│  │  └──────────┘  └──────────┘  └──────────┘  │            │
│  └─────────────────────────────────────────────┘            │
│                                                              │
│  Task = 1 Source Partition + 로컬 State Store (RocksDB)      │
│  Thread = N개 Task 처리                                      │
│  Instance = N개 Thread 실행                                  │
│                                                              │
│  State Store: RocksDB (로컬 디스크)                          │
│    ├─ Changelog Topic으로 자동 백업 (장애 복구)              │
│    └─ Standby Replica로 빠른 복구 가능                      │
└─────────────────────────────────────────────────────────────┘
```

### 핵심 개념

| 개념 | 설명 |
|------|------|
| **KStream** | 무한 이벤트 스트림 (INSERT 의미론) |
| **KTable** | 최신 상태 테이블 (UPSERT 의미론, compacted topic) |
| **GlobalKTable** | 전체 복제 테이블 (모든 인스턴스가 전체 데이터 보유) |
| **State Store** | RocksDB 기반 로컬 저장소 (KTable, 집계 결과 보관) |
| **Changelog Topic** | State Store 변경을 자동 백업하는 내부 토픽 |

---

## KTable vs GlobalKTable

### KTable (파티션 로컬)

```java
StreamsBuilder builder = new StreamsBuilder();

// KTable: 파티션별 데이터만 보유
KTable<String, String> userProfiles =
    builder.table("user-profiles",
        Materialized.<String, String, KeyValueStore<Bytes, byte[]>>
            as("user-profiles-store")
            .withKeySerde(Serdes.String())
            .withValueSerde(Serdes.String()));

// KStream-KTable Join (Co-partitioning 필수)
KStream<String, String> orders = builder.stream("orders");

KStream<String, String> enrichedOrders = orders.join(
    userProfiles,
    (order, profile) -> enrichOrder(order, profile),
    Joined.with(Serdes.String(), Serdes.String(), Serdes.String())
);
// ※ orders 토픽과 user-profiles 토픽의
//   파티션 수가 같고, 같은 키로 파티셔닝되어야 함
```

### GlobalKTable (전체 복제)

```java
// GlobalKTable: 모든 인스턴스가 전체 데이터 보유
GlobalKTable<String, String> countryCodes =
    builder.globalTable("country-codes",
        Materialized.<String, String, KeyValueStore<Bytes, byte[]>>
            as("country-codes-store"));

// KStream-GlobalKTable Join (Co-partitioning 불필요)
KStream<String, String> enrichedOrders = orders.join(
    countryCodes,
    (orderId, order) -> extractCountryCode(order),  // 조인 키 추출
    (order, country) -> enrichWithCountry(order, country)
);
```

### 선택 기준

| 기준 | KTable | GlobalKTable |
|------|--------|-------------|
| 데이터 크기 | 대규모 OK | 소규모만 (전체 복제) |
| Co-partitioning | 필수 | 불필요 |
| 메모리 사용 | 파티션/인스턴스 수로 분산 | 인스턴스마다 전체 데이터 |
| 적합 사용 | 사용자 프로필, 주문 상태 | 국가 코드, 설정, 환율 |
| Foreign Key Join | KTable-KTable FK Join 사용 | 자연스럽게 지원 |

---

## Windowing

### Tumbling Window (고정 구간, 겹침 없음)

```java
KStream<String, OrderEvent> orders = builder.stream("orders");

// 5분 단위 주문 수 집계
KTable<Windowed<String>, Long> orderCounts = orders
    .groupByKey()
    .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5)))
    .count(Materialized.as("order-counts-tumbling"));

// 결과 토픽으로 출력
orderCounts.toStream()
    .map((windowedKey, count) -> KeyValue.pair(
        windowedKey.key(),
        String.format("window=[%s-%s], count=%d",
            windowedKey.window().startTime(),
            windowedKey.window().endTime(),
            count)))
    .to("order-count-results");
```

### Hopping Window (고정 구간, 겹침 있음)

```java
// 5분 윈도우, 1분 간격으로 슬라이딩
KTable<Windowed<String>, Long> hoppingCounts = orders
    .groupByKey()
    .windowedBy(TimeWindows
        .ofSizeAndGrace(Duration.ofMinutes(5), Duration.ofMinutes(1))
        .advanceBy(Duration.ofMinutes(1)))  // 1분마다 새 윈도우
    .count(Materialized.as("order-counts-hopping"));
```

### Session Window (활동 기반, 유동적 크기)

```java
// 30분 비활동 시 세션 종료
KTable<Windowed<String>, Long> sessionCounts = orders
    .groupByKey()
    .windowedBy(SessionWindows
        .ofInactivityGapAndGrace(
            Duration.ofMinutes(30),   // 비활동 간격
            Duration.ofMinutes(5)))   // Grace period
    .count(Materialized.as("order-counts-session"));
```

### 윈도우 비교

| 윈도우 | 크기 | 겹침 | 적합 시나리오 |
|--------|------|------|-------------|
| **Tumbling** | 고정 | 없음 | 주기적 집계 (매 5분 매출) |
| **Hopping** | 고정 | 있음 | 이동 평균 (5분 윈도우, 1분 슬라이딩) |
| **Session** | 유동 | 없음 | 사용자 세션 분석 |
| **Sliding** | 고정 | 있음 | 연속 이벤트 감지 (5분 내 5회 실패) |

### Grace Period

```
Grace Period: 지연 도착 이벤트 허용 시간
  - 윈도우 종료 후 grace 기간 내 도착한 이벤트는 포함
  - grace 기간 이후 도착한 이벤트는 버림
  - Kafka Streams 3.0+: 기본 24시간 → 명시적 설정 권장

권장: ofSizeAndGrace() 사용, 비즈니스 요구에 맞는 grace 설정
```

---

## Interactive Queries

### 로컬 State Store 쿼리

```java
KafkaStreams streams = new KafkaStreams(builder.build(), props);
streams.start();

// Key-Value Store 쿼리
ReadOnlyKeyValueStore<String, Long> store =
    streams.store(StoreQueryParameters.fromNameAndType(
        "order-counts-tumbling",
        QueryableStoreTypes.keyValueStore()));

// 특정 키 조회
Long count = store.get("customer-123");

// 전체 조회
KeyValueIterator<String, Long> iter = store.all();
while (iter.hasNext()) {
    KeyValue<String, Long> entry = iter.next();
    System.out.printf("%s: %d%n", entry.key, entry.value);
}
iter.close();  // 반드시 close!
```

### Windowed Store 쿼리

```java
ReadOnlyWindowStore<String, Long> windowStore =
    streams.store(StoreQueryParameters.fromNameAndType(
        "order-counts-tumbling",
        QueryableStoreTypes.windowStore()));

// 시간 범위 쿼리
WindowStoreIterator<Long> iter = windowStore.fetch(
    "customer-123",
    Instant.now().minus(Duration.ofHours(1)),
    Instant.now());

while (iter.hasNext()) {
    KeyValue<Long, Long> entry = iter.next();
    Instant windowStart = Instant.ofEpochMilli(entry.key);
    System.out.printf("window=%s, count=%d%n", windowStart, entry.value);
}
iter.close();
```

### REST API 노출

```java
// Spring Boot REST API로 Interactive Queries 노출
@RestController
@RequiredArgsConstructor
public class OrderCountController {
    private final KafkaStreams streams;

    @GetMapping("/api/counts/{customerId}")
    public ResponseEntity<Long> getCount(@PathVariable String customerId) {
        ReadOnlyKeyValueStore<String, Long> store =
            streams.store(StoreQueryParameters.fromNameAndType(
                "order-counts", QueryableStoreTypes.keyValueStore()));

        Long count = store.get(customerId);
        if (count == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(count);
    }
}
```

### CRITICAL: 분산 환경에서 Interactive Queries

```
문제: 각 인스턴스는 자신에게 할당된 파티션의 데이터만 보유
해결: application.server 설정 + metadata API로 올바른 인스턴스로 라우팅

props.put(StreamsConfig.APPLICATION_SERVER_CONFIG, "host:port");

// 키가 어느 인스턴스에 있는지 조회
StreamsMetadata metadata = streams.queryMetadataForKey(
    "order-counts", customerId, Serdes.String().serializer());

if (metadata.equals(StreamsMetadata.NOT_AVAILABLE)) {
    // State Store가 아직 준비되지 않음
} else if (metadata.hostInfo().equals(thisInstance)) {
    // 로컬 조회
} else {
    // 원격 인스턴스로 HTTP 요청 라우팅
    forwardToRemote(metadata.hostInfo(), customerId);
}
```

---

## RocksDB 튜닝

### 기본 설정 커스터마이징

```java
public class CustomRocksDBConfig implements RocksDBConfigSetter {
    @Override
    public void setConfig(String storeName, Options options,
                          Map<String, Object> configs) {
        BlockBasedTableConfig tableConfig = new BlockBasedTableConfig();
        tableConfig.setBlockCacheSize(50 * 1024 * 1024L);  // 50MB
        tableConfig.setBlockSize(4096);
        tableConfig.setCacheIndexAndFilterBlocks(true);
        options.setTableFormatConfig(tableConfig);
        options.setMaxWriteBufferNumber(3);
        options.setWriteBufferSize(16 * 1024 * 1024);  // 16MB
        options.setCompactionStyle(CompactionStyle.LEVEL);
    }
}

// 설정 적용
props.put(StreamsConfig.ROCKSDB_CONFIG_SETTER_CLASS_CONFIG,
    CustomRocksDBConfig.class.getName());
```

### 핵심 튜닝 포인트

| 설정 | 기본값 | 설명 | 튜닝 방향 |
|------|--------|------|-----------|
| `block.cache.size` | 50MB | 읽기 캐시 | 읽기 많으면 증가 |
| `write.buffer.size` | 16MB | 쓰기 버퍼 | 쓰기 많으면 증가 |
| `max.write.buffer.number` | 3 | 쓰기 버퍼 수 | 쓰기 burst 대응 |
| `compaction.style` | LEVEL | 압축 방식 | 공간 효율 vs 쓰기 성능 |

### Standby Replicas (빠른 복구)

```java
// State Store 복구 시간 단축
props.put(StreamsConfig.NUM_STANDBY_REPLICAS_CONFIG, 1);
// → 다른 인스턴스에 State Store 복제본 유지
// → 장애 시 복제본에서 즉시 복구 (changelog 리플레이 불필요)
// → 메모리/디스크 2배 사용
```

---

## 실전 패턴: 실시간 주문 집계

```java
StreamsBuilder builder = new StreamsBuilder();

// 1. 주문 이벤트 스트림
KStream<String, OrderEvent> orders = builder.stream("orders",
    Consumed.with(Serdes.String(), orderEventSerde));

// 2. 카테고리별 실시간 매출 (Tumbling 1분)
KTable<Windowed<String>, Double> categorySales = orders
    .groupBy((key, order) -> order.getCategory(),
        Grouped.with(Serdes.String(), orderEventSerde))
    .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(1)))
    .aggregate(
        () -> 0.0,
        (category, order, total) -> total + order.getAmount(),
        Materialized.<String, Double, WindowStore<Bytes, byte[]>>
            as("category-sales")
            .withValueSerde(Serdes.Double()));

// 3. 고객별 최근 주문 수 (Session 30분)
KTable<Windowed<String>, Long> customerSessions = orders
    .groupByKey()
    .windowedBy(SessionWindows.ofInactivityGapWithNoGrace(
        Duration.ofMinutes(30)))
    .count(Materialized.as("customer-sessions"));

// 4. 결과 출력
categorySales.toStream()
    .to("category-sales-output",
        Produced.with(WindowedSerdes.timeWindowedSerdeFrom(String.class),
            Serdes.Double()));
```

---

## 체크리스트

### 설계
- [ ] KStream vs KTable 선택
- [ ] Co-partitioning 요구사항 확인
- [ ] 윈도우 타입/크기 결정
- [ ] Grace period 설정

### 성능
- [ ] num.stream.threads 워크로드에 맞게 설정
- [ ] RocksDB 캐시/버퍼 튜닝
- [ ] num.standby.replicas 설정 (복구 시간)
- [ ] State Store changelog 압축 설정

### 운영
- [ ] Interactive Queries REST API 구현
- [ ] 분산 쿼리 라우팅 (application.server)
- [ ] State Store 크기 모니터링
- [ ] Consumer Lag / 처리 지연 알림

**관련 skill**: `/kafka`, `/kafka-patterns`, `/kafka-advanced`, `/msa-cqrs-eventsourcing`
