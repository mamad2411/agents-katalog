---
name: virtual-waiting-room
category: business
description: "대규모 티켓팅 — Redis 대기열 기반 Virtual Waiting Room, SSE 입장 알림, 좌석 분산 잠금, 결제 Saga 연동, 100만 동접 Capacity Planning. Use when 티켓 오픈·수강신청·한정판 판매처럼 순간 트래픽이 몰려 대기열과 좌석 선점 제어가 필요할 때."
effort: xhigh
deprecated: false
---

# Virtual Waiting Room (대규모 티켓팅)

순간 폭주 트래픽을 대기열로 흡수하고 좌석을 안전하게 선점시키는 패턴.
일반 트래픽 설계는 [`high-traffic-design`](../high-traffic-design/SKILL.md), 봇/매크로 차단은 [`anti-bot`](../anti-bot/SKILL.md) 참조.

## Scale Targets

| 항목 | 목표 |
|------|------|
| Concurrent Users | 1,000,000+ |
| Seats | 15,000+ |
| TPS at Peak | 50,000+ |
| Response Time | P99 < 500ms |

## Virtual Waiting Room Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Virtual Waiting Room                          │
├─────────────────────────────────────────────────────────────────┤
│  [Users] ──► [CDN Edge] ──► [Queue Service] ──► [Origin]        │
│               │                   │                              │
│               ▼                   ▼                              │
│         Static Queue Page    Redis Sorted Set                   │
│         (waiting.html)       (position tracking)                │
│                                                                  │
│  Flow:                                                           │
│  1. User arrives → CDN serves waiting page                      │
│  2. JS polls queue position via API                             │
│  3. When turn comes → receive access token                      │
│  4. Token validates at origin → proceed to purchase             │
└─────────────────────────────────────────────────────────────────┘
```

### Redis Queue Implementation

```java
@Service
public class WaitingRoomService {
    private static final String QUEUE_KEY = "waiting:queue";
    private static final String TOKEN_KEY = "waiting:tokens:";

    // 대기열 진입
    public WaitingPosition enterQueue(String userId) {
        long timestamp = System.currentTimeMillis();
        redisTemplate.opsForZSet().add(QUEUE_KEY, userId + ":" + timestamp, timestamp);
        Long rank = redisTemplate.opsForZSet().rank(QUEUE_KEY, userId + ":" + timestamp);
        return WaitingPosition.builder()
            .position(rank + 1)
            .estimatedWaitSeconds(rank / 500)  // 초당 500명 입장 기준
            .build();
    }

    // 입장 토큰 발급 (스케줄러, 1초마다)
    @Scheduled(fixedRate = 1000)
    public void processQueue() {
        int batchSize = calculateAdmissionRate();  // 동적: (maxCapacity - activeUsers) * 0.1
        Set<String> nextUsers = redisTemplate.opsForZSet().range(QUEUE_KEY, 0, batchSize - 1);

        for (String member : nextUsers) {
            String userId = member.split(":")[0];
            String token = generateAccessToken(userId);
            redisTemplate.opsForValue().set(TOKEN_KEY + userId, token, Duration.ofMinutes(5));
            redisTemplate.opsForZSet().remove(QUEUE_KEY, member);
            notifyUserAdmission(userId, token);  // WebSocket/SSE
        }
    }
}
```

### SSE Endpoint (권장)

```java
@GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<WaitingStatus>> streamStatus(@RequestHeader("X-User-Id") String userId) {
    return Flux.interval(Duration.ofSeconds(2))
        .map(seq -> {
            String token = waitingRoomService.getAccessToken(userId);
            if (token != null) {
                return ServerSentEvent.<WaitingStatus>builder()
                    .event("admitted").data(WaitingStatus.admitted(token)).build();
            }
            return ServerSentEvent.<WaitingStatus>builder()
                .event("waiting").data(WaitingStatus.waiting(getPosition(userId))).build();
        })
        .takeUntil(sse -> "admitted".equals(sse.event()));
}
```

## Seat Reservation (Redis Distributed Lock)

```java
@Service
public class SeatReservationService {
    private static final String SEAT_LOCK_PREFIX = "lock:seat:";
    private static final Duration LOCK_TTL = Duration.ofMinutes(5);

    // 좌석 선택 (임시 잠금)
    public SeatLockResult selectSeat(String eventId, String seatId, String userId) {
        String lockKey = SEAT_LOCK_PREFIX + eventId + ":" + seatId;
        String lockValue = userId + ":" + System.currentTimeMillis();

        Boolean acquired = redisTemplate.opsForValue().setIfAbsent(lockKey, lockValue, LOCK_TTL);

        if (Boolean.FALSE.equals(acquired)) {
            String currentHolder = redisTemplate.opsForValue().get(lockKey);
            if (currentHolder.startsWith(userId + ":")) {
                redisTemplate.expire(lockKey, LOCK_TTL);  // 연장
                return SeatLockResult.extended(seatId, LOCK_TTL);
            }
            return SeatLockResult.alreadyLocked(seatId);
        }
        return SeatLockResult.success(seatId, LOCK_TTL);
    }

    // 다중 좌석 원자적 락 (Lua 스크립트)
    public MultiSeatLockResult selectMultipleSeats(String eventId, List<String> seatIds, String userId) {
        String script = """
            local locked, failed = {}, {}
            for i, seatId in ipairs(KEYS) do
                if redis.call('SET', ARGV[1]..seatId, ARGV[2], 'NX', 'EX', ARGV[3]) then
                    table.insert(locked, seatId)
                else
                    table.insert(failed, seatId)
                end
            end
            return {locked, failed}
            """;
        // Execute and return result
    }
}
```

## Saga Pattern (Payment Flow)

```java
@Service
public class ReservationSagaOrchestrator {

    public ReservationResult executeReservation(ReservationRequest request) {
        SagaContext context = new SagaContext(request);
        try {
            confirmSeats(context);      // Step 1
            processPayment(context);    // Step 2
            issueTickets(context);      // Step 3
            sendNotification(context);  // Step 4
            return ReservationResult.success(context);
        } catch (PaymentException e) {
            compensateSeats(context);   // 좌석 롤백
            return ReservationResult.failure("PAYMENT_FAILED", e.getMessage());
        } catch (TicketIssuanceException e) {
            compensatePayment(context); // 결제 취소
            compensateSeats(context);   // 좌석 롤백
            return ReservationResult.failure("TICKET_FAILED", e.getMessage());
        }
    }

    private void compensateSeats(SagaContext ctx) {
        ctx.getConfirmedSeats().forEach(seat ->
            seatService.releaseSeatWithCompensation(ctx.getEventId(), seat.getId(), ctx.getUserId()));
    }

    private void compensatePayment(SagaContext ctx) {
        if (ctx.getPaymentResult() != null) {
            paymentService.refund(ctx.getPaymentResult().getTransactionId());
        }
    }
}
```

## Performance Optimization

### Read Replica + Cache

```java
@Configuration
public class DataSourceConfig {
    @Bean
    public DataSource routingDataSource(DataSource primary, DataSource replica) {
        RoutingDataSource ds = new RoutingDataSource();
        ds.setTargetDataSources(Map.of("primary", primary, "replica", replica));
        return ds;
    }
}

// 읽기 전용은 Replica로
@Transactional(readOnly = true)
@TargetDataSource("replica")
public List<SeatDTO> getAvailableSeats(String eventId) { ... }

// 좌석 상태 캐시 (5초 TTL)
@Cacheable(value = "seatMap", key = "#eventId")
public SeatMapDTO getSeatMap(String eventId) { ... }
```

## Health Check Points

| 항목 | 정상 | 경고 | 위험 |
|------|------|------|------|
| 대기열 크기 | < 100K | 100K-500K | > 500K |
| 입장률 | > 300/s | 100-300/s | < 100/s |
| 좌석 락 TTL 근접 | < 50% | 50-80% | > 80% |
| DB Connection Pool | < 70% | 70-90% | > 90% |
| Redis Memory | < 60% | 60-80% | > 80% |

## Capacity Planning (100만 동접)

| 컴포넌트 | 스펙 | 수량 |
|----------|------|------|
| Application | 8 vCPU, 16GB | 20+ pods |
| Redis Cluster | 32GB Memory | 6 nodes |
| PostgreSQL | 16 vCPU, 64GB | 1 primary + 2 replica |

### HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 10
  maxReplicas: 100
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 60 }
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0  # 즉시 스케일업
```

## Anti-Patterns

```java
// 🚫 DB에서 좌석 잠금 (확장성 문제)
@Transactional
public void reserveSeat(String seatId) {
    seatRepository.findByIdWithLock(seatId);  // SELECT FOR UPDATE - 병목!
}

// 🚫 동기적 결제 처리
public void checkout() {
    paymentGateway.processSync();  // 느린 외부 API가 스레드 블로킹
}

// 🚫 모든 좌석 한번에 조회
public List<Seat> getAllSeats(String eventId) {
    return seatRepository.findAll();  // 15,000개 전체 로드!
}

// ✅ 섹션별 페이징 조회
public Page<SeatDTO> getSeatsBySection(String eventId, String section, Pageable pageable) {
    return seatRepository.findByEventIdAndSection(eventId, section, pageable);
}
```


## 참조 스킬

- [`high-traffic-design`](../high-traffic-design/SKILL.md) — Backpressure, CDN/Edge, Queue-based Load Leveling
- [`anti-bot`](../anti-bot/SKILL.md) — 매크로/봇 차단 (대기열 우회 방지)
- [`rate-limiting`](../rate-limiting/SKILL.md) — 대기열 진입/폴링 요청 제한
- [`distributed-lock`](../distributed-lock/SKILL.md) — 좌석 잠금 Redlock / Fencing Token
- [`msa-saga`](../msa-saga/SKILL.md) — 결제 실패 시 좌석 해제 보상 트랜잭션
- [`redis-operations`](../redis-operations/SKILL.md) — 대기열 Redis 운영 (Cluster / 메모리 / eviction)
- [`load-testing`](../load-testing/SKILL.md) — 대기열 시나리오 부하 검증
