---
name: concurrency-spring
category: spring
description: "Spring Concurrency Patterns — MSA/대규모 트래픽 환경에서의 동시성 문제 해결 패턴 Use when working with spring 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Spring Concurrency Patterns

MSA/대규모 트래픽 환경에서의 동시성 문제 해결 패턴

## 문제 유형

| 문제 | 설명 | 증상 |
|------|------|------|
| Race Condition | 동시 수정으로 데이터 불일치 | 재고가 음수, 중복 결제 |
| Lost Update | 한쪽 변경이 유실 | 마지막 저장만 반영 |
| Deadlock | 순환 대기로 교착 | 트랜잭션 타임아웃 |

---

## Optimistic Locking (낙관적 락)

충돌이 드문 경우 사용. DB 락 없이 버전으로 충돌 감지.

### 구현
```java
@Entity
public class Product {
    @Id
    private Long id;

    @Version  // 핵심: 자동 버전 관리
    private Long version;

    private Integer stock;

    public void decreaseStock(int quantity) {
        if (this.stock < quantity) {
            throw new InsufficientStockException();
        }
        this.stock -= quantity;
    }
}
```

### 충돌 처리
```java
@Service
@RequiredArgsConstructor
public class OrderService {
    private final ProductRepository productRepository;

    @Transactional
    @Retryable(
        retryFor = ObjectOptimisticLockingFailureException.class,
        maxAttempts = 3,
        backoff = @Backoff(delay = 100, multiplier = 2)
    )
    public void placeOrder(Long productId, int quantity) {
        Product product = productRepository.findById(productId)
            .orElseThrow(() -> new NotFoundException("Product not found"));

        product.decreaseStock(quantity);
        // save 시 version 불일치하면 OptimisticLockException 발생
    }

    @Recover
    public void recoverPlaceOrder(ObjectOptimisticLockingFailureException e,
                                   Long productId, int quantity) {
        log.error("주문 실패 - 재고 동시 수정 충돌: productId={}", productId);
        throw new OrderFailedException("일시적 오류, 다시 시도해주세요");
    }
}
```

### 의존성
```groovy
implementation 'org.springframework.retry:spring-retry'
implementation 'org.springframework:spring-aspects'
```

```java
@Configuration
@EnableRetry
public class RetryConfig {}
```

---

## Pessimistic Locking (비관적 락)

충돌이 잦은 경우 사용. DB 레벨에서 락 획득.

### Repository
```java
public interface ProductRepository extends JpaRepository<Product, Long> {

    // 배타적 락 (읽기/쓰기 차단)
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    Optional<Product> findByIdWithLock(@Param("id") Long id);

    // 공유 락 (쓰기만 차단)
    @Lock(LockModeType.PESSIMISTIC_READ)
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    Optional<Product> findByIdWithReadLock(@Param("id") Long id);
}
```

### 사용
```java
@Service
@RequiredArgsConstructor
public class StockService {
    private final ProductRepository productRepository;

    @Transactional
    public void decreaseStock(Long productId, int quantity) {
        // SELECT ... FOR UPDATE 실행
        Product product = productRepository.findByIdWithLock(productId)
            .orElseThrow(() -> new NotFoundException("Product not found"));

        product.decreaseStock(quantity);
    }
}
```

### 타임아웃 설정 (데드락 방지)
```java
@Lock(LockModeType.PESSIMISTIC_WRITE)
@QueryHints({
    @QueryHint(name = "jakarta.persistence.lock.timeout", value = "3000")  // 3초
})
@Query("SELECT p FROM Product p WHERE p.id = :id")
Optional<Product> findByIdWithLockTimeout(@Param("id") Long id);
```

---

## Deadlock 방지

### 1. 일관된 락 순서
```java
// BAD: 순서가 다르면 데드락 발생 가능
// Thread A: lock(product) -> lock(order)
// Thread B: lock(order) -> lock(product)

// GOOD: 항상 같은 순서로 락 획득
@Transactional
public void processOrder(Long productId, Long orderId) {
    // ID 오름차순으로 락 획득
    if (productId < orderId) {
        lockProduct(productId);
        lockOrder(orderId);
    } else {
        lockOrder(orderId);
        lockProduct(productId);
    }
}
```

### 2. 트랜잭션 범위 최소화
```java
// BAD: 트랜잭션 내에서 외부 API 호출
@Transactional
public void badExample(Long orderId) {
    Order order = orderRepository.findByIdWithLock(orderId);
    paymentService.callExternalApi();  // 느린 외부 호출 (락 오래 유지)
    order.complete();
}

// GOOD: 락 범위 최소화
public void goodExample(Long orderId) {
    PaymentResult result = paymentService.callExternalApi();  // 락 밖에서 호출

    completeOrder(orderId, result);  // 짧은 트랜잭션
}

@Transactional
public void completeOrder(Long orderId, PaymentResult result) {
    Order order = orderRepository.findByIdWithLock(orderId);
    order.complete(result);
}
```

### 3. 데드락 재시도
```java
@Retryable(
    retryFor = {
        DeadlockLoserDataAccessException.class,
        PessimisticLockingFailureException.class,
        CannotAcquireLockException.class
    },
    maxAttempts = 3,
    backoff = @Backoff(delay = 100, multiplier = 2, random = true)  // 랜덤 백오프
)
@Transactional
public void processWithRetry(Long id) {
    // 데드락 발생 시 자동 재시도
}
```

---

## 선택 가이드

```
충돌 빈도?
    │
    ├─ 낮음 (읽기 많음) ──────> Optimistic (@Version + @Retryable)
    │
    └─ 높음 (쓰기 많음)
           │
           ├─ 단일 서버 ──────> Pessimistic (@Lock)
           │
           └─ MSA/다중 서버 ───> Distributed Lock (/distributed-lock)
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 트랜잭션 내 외부 API 호출 | 락 장시간 유지 | 트랜잭션 밖으로 분리 |
| 락 타임아웃 미설정 | 무한 대기 | `lock.timeout` 설정 |
| @Retryable 순서 잘못 | 같은 트랜잭션에서 재시도 | @Retryable이 @Transactional 감싸야 함 |
| 버전 없이 동시 업데이트 | Lost Update | @Version 추가 |
| findAll() 후 수정 | 레이스 컨디션 | 개별 조회 + 락 |

---

## 체크리스트

- [ ] 동시 수정 가능한 엔티티에 `@Version` 추가
- [ ] Optimistic 락 사용 시 `@Retryable` 설정
- [ ] Pessimistic 락 사용 시 타임아웃 설정
- [ ] 트랜잭션 범위 최소화
- [ ] 다중 락 획득 시 순서 일관성 확인
- [ ] MSA 환경이면 분산 락 검토 (/distributed-lock)
