---
name: redis-operations
category: infrastructure
description: "Redis 운영 — Standalone/Sentinel/Cluster 모드 선택, Cache-Aside·Write-Through 캐싱 전략과 Cache Stampede 방지, maxmemory·eviction 정책, Redlock 분산 락, K8s Operator/Helm 배포, 핵심 메트릭. Use when Redis 캐싱 전략·고가용성 구성·메모리 정책을 정하거나 K8s 위에서 Redis 를 운영할 때."
effort: xhigh
deprecated: false
---

# Redis 운영

모드 선택 · 캐싱 전략 · HA · 메모리 · K8s 운영.
Streams 를 메시지 브로커로 쓰는 경우는 [`redis-streams`](../redis-streams/SKILL.md), 분산 락 코드 패턴은 [`distributed-lock`](../distributed-lock/SKILL.md) 참조.

## Quick Reference

| 상황 | 접근 방식 | 참조 |
|------|----------|------|
| 캐시 설계 | TTL + Eviction 정책 | #caching-strategy |
| 고가용성 | Cluster 또는 Sentinel | #high-availability |
| 동시성 제어 | Lua 스크립트 / Redlock | #distributed-lock |
| K8s 운영 | Redis Operator | #kubernetes-redis |
| 메모리 부족 | maxmemory + eviction | #memory-management |

## Redis Mode 선택

| Mode | 용도 | 특징 |
|------|------|------|
| **Standalone** | 개발/소규모 | 단순, 단일 노드 |
| **Sentinel** | HA 필요, 읽기 중심 | 자동 failover, 복제 |
| **Cluster** | 대용량, 쓰기 분산 | 샤딩, 16384 슬롯 |

```
선택 기준
    │
    ├─ 데이터 < 10GB, 단일 쓰기 ──> Sentinel (3 nodes)
    │
    ├─ 데이터 > 10GB, 쓰기 분산 ──> Cluster (6+ nodes)
    │
    └─ 개발/테스트 ──────────────> Standalone
```

---

## Caching Strategy

### Cache-Aside (Lazy Loading)

```java
public User getUser(Long id) {
    String key = "user:" + id;
    User cached = redis.get(key);
    if (cached != null) return cached;

    User user = db.findById(id);
    redis.setex(key, 3600, user);  // TTL 1시간
    return user;
}
```

### Write-Through

```java
@Transactional
public User updateUser(Long id, UserDto dto) {
    User user = db.save(mapper.toEntity(dto));
    redis.setex("user:" + id, 3600, user);
    return user;
}
```

### TTL 가이드라인

| 데이터 유형 | TTL | 이유 |
|------------|-----|------|
| 세션 | 30분 | 보안 |
| 사용자 프로필 | 1시간 | 변경 적음 |
| 상품 목록 | 5분 | 자주 변경 |
| 실시간 순위 | 10초 | 최신성 중요 |

### Cache Stampede 방지

```java
// 분산 락 + 짧은 stale 허용
public User getUserWithLock(Long id) {
    String key = "user:" + id;
    User cached = redis.get(key);
    if (cached != null) return cached;

    String lockKey = "lock:" + key;
    if (redis.setnx(lockKey, "1", 5)) {  // 5초 락
        try {
            User user = db.findById(id);
            redis.setex(key, 3600, user);
            return user;
        } finally {
            redis.del(lockKey);
        }
    }
    // 락 획득 실패 시 짧은 대기 후 재시도
    Thread.sleep(100);
    return getUserWithLock(id);
}
```

---

## High Availability

### Redis Sentinel (3 노드 최소)

```yaml
# sentinel.conf
sentinel monitor mymaster 10.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1
```

```java
// Spring Boot 연결
@Bean
public LettuceConnectionFactory redisConnectionFactory() {
    RedisSentinelConfiguration config = new RedisSentinelConfiguration()
        .master("mymaster")
        .sentinel("10.0.0.1", 26379)
        .sentinel("10.0.0.2", 26379)
        .sentinel("10.0.0.3", 26379);
    return new LettuceConnectionFactory(config);
}
```

### Redis Cluster (6 노드 최소: 3 master + 3 replica)

```bash
# 클러스터 생성
redis-cli --cluster create \
  10.0.0.1:6379 10.0.0.2:6379 10.0.0.3:6379 \
  10.0.0.4:6379 10.0.0.5:6379 10.0.0.6:6379 \
  --cluster-replicas 1
```

```java
// Spring Boot Cluster 연결
@Bean
public LettuceConnectionFactory redisConnectionFactory() {
    RedisClusterConfiguration config = new RedisClusterConfiguration(
        List.of("10.0.0.1:6379", "10.0.0.2:6379", "10.0.0.3:6379")
    );
    config.setMaxRedirects(3);
    return new LettuceConnectionFactory(config);
}
```

**Cluster 키 설계**:

```
# Hash Tag로 같은 슬롯 강제
user:{1234}:profile
user:{1234}:orders
# {1234}가 동일하므로 같은 노드에 저장
```

---

## Memory Management

### maxmemory 설정

```conf
# redis.conf
maxmemory 4gb
maxmemory-policy allkeys-lru
```

| Policy | 설명 | 용도 |
|--------|------|------|
| `noeviction` | 메모리 초과 시 에러 | 데이터 유실 불가 |
| `allkeys-lru` | 모든 키 중 LRU 삭제 | **일반 캐시 (권장)** |
| `volatile-lru` | TTL 있는 키만 LRU | 일부 키 영구 보관 |
| `allkeys-lfu` | 사용 빈도 낮은 키 삭제 | 핫 데이터 유지 |

### 메모리 분석

```bash
# 메모리 사용량 분석
redis-cli info memory

# 큰 키 찾기
redis-cli --bigkeys

# 특정 패턴 키 메모리
redis-cli --memkeys "user:*"
```

---

## Distributed Lock (Redlock)

### Redisson 사용 (Java)

```java
@Service
public class InventoryService {
    private final RedissonClient redisson;

    public void decreaseStock(Long productId, int quantity) {
        RLock lock = redisson.getLock("stock:" + productId);
        try {
            // 10초 대기, 5초 후 자동 해제
            if (lock.tryLock(10, 5, TimeUnit.SECONDS)) {
                Stock stock = stockRepository.findById(productId);
                stock.decrease(quantity);
                stockRepository.save(stock);
            }
        } finally {
            if (lock.isHeldByCurrentThread()) {
                lock.unlock();
            }
        }
    }
}
```

### Lua 스크립트 (원자적 연산)

```lua
-- decrease_stock.lua
local stock = tonumber(redis.call('GET', KEYS[1]) or 0)
local quantity = tonumber(ARGV[1])

if stock >= quantity then
    redis.call('DECRBY', KEYS[1], quantity)
    return 1  -- 성공
else
    return 0  -- 재고 부족
end
```

```java
// Java에서 호출
String script = loadScript("decrease_stock.lua");
Long result = redis.eval(script, List.of("stock:1234"), List.of("5"));
```

---

## Kubernetes Redis

### Redis Operator (Spotahome)

```yaml
apiVersion: databases.spotahome.com/v1
kind: RedisFailover
metadata:
  name: redis-ha
spec:
  sentinel:
    replicas: 3
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
  redis:
    replicas: 3
    resources:
      requests:
        cpu: 500m
        memory: 1Gi
    storage:
      persistentVolumeClaim:
        spec:
          accessModes: [ReadWriteOnce]
          resources:
            requests:
              storage: 10Gi
```

### Bitnami Redis Cluster (Helm)

```bash
helm install redis-cluster bitnami/redis-cluster \
  --set cluster.nodes=6 \
  --set cluster.replicas=1 \
  --set persistence.size=10Gi \
  --set metrics.enabled=true
```

---

## Data Structures 활용

| 구조 | 용도 | 예시 |
|------|------|------|
| **String** | 단순 캐시, 카운터 | 세션, 조회수 |
| **Hash** | 객체 저장 | 사용자 프로필 |
| **List** | 큐, 최근 N개 | 메시지 큐, 최근 본 상품 |
| **Set** | 유니크 집합 | 좋아요 사용자 |
| **Sorted Set** | 랭킹, 스코어 | 리더보드 |
| **HyperLogLog** | 대용량 카운트 | UV 카운트 |
| **Stream** | 이벤트 로그 | 메시지 브로커 |

### Sorted Set 랭킹 예시

```bash
# 점수 추가
ZADD leaderboard 1500 "user:1" 1200 "user:2" 1800 "user:3"

# Top 10 조회 (높은 순)
ZREVRANGE leaderboard 0 9 WITHSCORES

# 특정 사용자 순위
ZREVRANK leaderboard "user:1"
```

---

## Monitoring

### 핵심 메트릭

```bash
redis-cli info stats | grep -E "keyspace_hits|keyspace_misses|expired_keys"
```

| 메트릭 | 정상 범위 | 액션 |
|--------|----------|------|
| `hit_rate` | > 90% | 낮으면 TTL/키 설계 검토 |
| `memory_used` | < maxmemory 80% | 초과 시 eviction 정책 |
| `connected_clients` | < 5000 | 높으면 connection pooling |
| `blocked_clients` | 0 | > 0이면 BLPOP 등 확인 |

### Prometheus + Grafana

```yaml
# redis_exporter
- job_name: 'redis'
  static_configs:
    - targets: ['redis-exporter:9121']
```

---

## Anti-Patterns

| 실수 | 올바른 방법 |
|------|------------|
| `KEYS *` 운영 환경 사용 | `SCAN` 커서 사용 |
| 큰 값(>100KB) 저장 | 압축 또는 분할 |
| 연결마다 새 클라이언트 | Connection Pool |
| TTL 없이 무한 저장 | 모든 캐시에 TTL 설정 |
| 단일 장애점 | Sentinel/Cluster |

---

## Checklist

### 캐시 설계
- [ ] 모든 캐시 키에 TTL 설정
- [ ] 키 네이밍 컨벤션 통일 (`entity:id:field`)
- [ ] Cache Stampede 방지 전략

### 고가용성
- [ ] Sentinel(3+) 또는 Cluster(6+) 구성
- [ ] 자동 failover 테스트 완료
- [ ] 백업 정책 (RDB/AOF)

### 운영
- [ ] maxmemory + eviction 정책 설정
- [ ] 모니터링 대시보드 구성
- [ ] 슬로우 로그 활성화 (`slowlog-log-slower-than 10000`)

## 참조 스킬

- [`redis-streams`](../redis-streams/SKILL.md) — Consumer Group / PEL / DLQ (메시징 용도)
- [`distributed-lock`](../distributed-lock/SKILL.md) — Redisson / Redsync / ShedLock / Fencing Token
- [`spring-cache`](../spring-cache/SKILL.md) — Spring `@Cacheable` 연동
- [`rate-limiting`](../rate-limiting/SKILL.md) — Redis Sliding Window 구현
- [`high-traffic-design`](../high-traffic-design/SKILL.md) — 캐시가 흡수해야 할 트래픽 규모 산정
- [`secrets-management`](../secrets-management/SKILL.md) — Redis 인증 정보 관리
