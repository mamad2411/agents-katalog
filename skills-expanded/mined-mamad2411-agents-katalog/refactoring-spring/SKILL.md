---
name: refactoring-spring
category: spring
description: "Spring Refactoring Patterns — Spring Boot 코드 리팩토링 패턴 및 best practices. Use when working with spring 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Spring Refactoring Patterns

Spring Boot 코드 리팩토링 패턴 및 best practices.

## Quick Reference

```
Spring 리팩토링 패턴
    │
    ├─ God Class (500줄+) ───> 책임별 클래스 분리
    │
    ├─ N+1 쿼리 ────────────> @EntityGraph / Fetch Join
    │
    ├─ 필드 주입 ──────────> 생성자 주입
    │
    ├─ 계층 혼재 ──────────> Controller → Service → Repository
    │
    └─ 시간 의존성 ────────> Clock 주입
```

---

## CRITICAL: 리팩토링 안전망

| 단계 | 체크 |
|------|------|
| 테스트 존재 | 단위 + 통합 테스트 커버리지 |
| DB 마이그레이션 분리 | 스키마 변경은 별도 커밋 |
| 작은 커밋 | 하나의 리팩토링 = 하나의 커밋 |
| 롤백 가능 | 배포 후에도 복구 가능해야 함 |

---

## 메서드 추출 (Extract Method)

### 긴 메서드 분리

```java
// Before: 긴 메서드 (60줄+)
@Transactional
public Order createOrder(CreateOrderRequest request) {
    // 1. 유효성 검증 (15줄)
    if (request.getUserId() == null) {
        throw new IllegalArgumentException("User ID required");
    }
    if (request.getItems() == null || request.getItems().isEmpty()) {
        throw new IllegalArgumentException("Items required");
    }
    User user = userRepository.findById(request.getUserId())
        .orElseThrow(() -> new NotFoundException("User not found"));
    // ... 더 많은 검증

    // 2. 재고 확인 (15줄)
    for (OrderItemRequest item : request.getItems()) {
        Product product = productRepository.findById(item.getProductId())
            .orElseThrow(() -> new NotFoundException("Product not found"));
        if (product.getStock() < item.getQuantity()) {
            throw new BusinessException("Insufficient stock");
        }
    }

    // 3. 주문 생성 (15줄)
    Order order = Order.builder()
        .user(user)
        .status(OrderStatus.PENDING)
        .build();
    // ...

    // 4. 알림 발송 (15줄)
    notificationService.sendOrderCreated(order);

    return orderRepository.save(order);
}

// After: 책임별 메서드 추출
@Transactional
public Order createOrder(CreateOrderRequest request) {
    User user = validateAndGetUser(request);
    List<OrderItem> items = validateAndReserveStock(request.getItems());

    Order order = buildOrder(user, items);
    Order savedOrder = orderRepository.save(order);

    sendOrderNotification(savedOrder);

    return savedOrder;
}

private User validateAndGetUser(CreateOrderRequest request) {
    if (request.getUserId() == null) {
        throw new IllegalArgumentException("User ID required");
    }
    return userRepository.findById(request.getUserId())
        .orElseThrow(() -> new NotFoundException("User not found"));
}

private List<OrderItem> validateAndReserveStock(List<OrderItemRequest> items) {
    if (items == null || items.isEmpty()) {
        throw new IllegalArgumentException("Items required");
    }
    // ...
}
```

---

## God Class 분해

### 500줄+ 클래스 분리 전략

```java
// Before: OrderService 800줄 (재고, 가격, 결제, 배송, 알림 모두 처리)
@Service
public class OrderService {

    public Order createOrder(CreateOrderRequest req) {
        // 재고 확인 (100줄)
        // 가격 계산 (100줄)
        // 결제 처리 (150줄)
        // 배송 예약 (100줄)
        // 알림 발송 (50줄)
    }

    // 30개+ 메서드...
}

// After: 책임별 서비스 분리
@Service
@RequiredArgsConstructor
public class OrderService {
    private final InventoryService inventoryService;
    private final PricingService pricingService;
    private final PaymentService paymentService;
    private final ShippingService shippingService;
    private final NotificationService notificationService;

    @Transactional
    public Order createOrder(CreateOrderRequest req) {
        // 1. 재고 확인 및 예약
        inventoryService.reserve(req.getItems());

        // 2. 가격 계산
        OrderPrice price = pricingService.calculate(req);

        // 3. 결제 처리
        Payment payment = paymentService.process(req.getPaymentInfo(), price);

        // 4. 주문 생성
        Order order = Order.builder()
            .items(req.getItems())
            .price(price)
            .payment(payment)
            .build();
        Order savedOrder = orderRepository.save(order);

        // 5. 배송 예약 (비동기)
        shippingService.scheduleAsync(savedOrder);

        // 6. 알림 (비동기)
        notificationService.sendOrderCreatedAsync(savedOrder);

        return savedOrder;
    }
}
```

### 분리 기준

| 기준 | 설명 |
|------|------|
| 변경 이유 | 같이 변경되는 것들을 모음 |
| 도메인 개념 | 재고, 결제, 배송은 별개 도메인 |
| 팀 경계 | 다른 팀이 담당하면 분리 |

---

## 계층 분리 리팩토링

### Controller → Service → Repository

```java
// Before: Controller에 비즈니스 로직 (Anti-pattern)
@RestController
public class UserController {

    @Autowired
    private UserRepository userRepository;

    @PostMapping("/users")
    public ResponseEntity<User> createUser(@RequestBody CreateUserRequest req) {
        // 비즈니스 로직이 Controller에!
        if (userRepository.existsByEmail(req.getEmail())) {
            throw new DuplicateException("Email already exists");
        }

        User user = new User();
        user.setEmail(req.getEmail());
        user.setPassword(passwordEncoder.encode(req.getPassword()));
        user.setCreatedAt(LocalDateTime.now());

        return ResponseEntity.ok(userRepository.save(user));
    }
}

// After: 계층 분리
@RestController
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @PostMapping("/users")
    public ResponseEntity<UserResponse> createUser(@Valid @RequestBody CreateUserRequest req) {
        User user = userService.createUser(req);
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(UserResponse.from(user));
    }
}

@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional
    public User createUser(CreateUserRequest req) {
        if (userRepository.existsByEmail(req.getEmail())) {
            throw new DuplicateException("Email already exists");
        }

        User user = User.builder()
            .email(req.getEmail())
            .password(passwordEncoder.encode(req.getPassword()))
            .build();

        return userRepository.save(user);
    }
}
```

---

## N+1 쿼리 리팩토링

### 문제 발견

```java
// N+1 발생 코드
List<Order> orders = orderRepository.findByUserId(userId);  // 1번 쿼리
for (Order order : orders) {
    List<OrderItem> items = order.getItems();  // N번 쿼리!
}
```

### 해결 방법 요약

| 방법 | 적용 시점 | 특징 |
|------|----------|------|
| `@EntityGraph` | Repository 메서드 | 명시적 연관관계 로딩 |
| Fetch Join | JPQL 쿼리 | 유연한 조인 제어 |
| Batch Size | application.yml | 전역 IN 쿼리 최적화 |
| Projection | DTO 조회 | 필요한 필드만 조회 |

자세한 JPA 패턴은 `/spring-data` 참조.

---

## 의존성 주입 개선

### @Autowired 필드 → 생성자 주입

```java
// Before: 필드 주입 (테스트 어려움)
@Service
public class OrderService {

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private PaymentService paymentService;

    @Autowired
    private NotificationService notificationService;
}

// After: 생성자 주입 + final
@Service
@RequiredArgsConstructor  // Lombok
public class OrderService {

    private final OrderRepository orderRepository;
    private final PaymentService paymentService;
    private final NotificationService notificationService;
}
```

### 생성자 주입 장점

| 장점 | 설명 |
|------|------|
| 불변성 | `final` 필드로 선언 가능 |
| 테스트 용이 | new로 직접 주입 가능 |
| 순환 참조 방지 | 컴파일 타임에 발견 |
| 필수 의존성 명확 | 생성자에 모두 노출 |

---

## 테스트 가능성 향상

### Clock 주입 (시간 의존성 분리)

```java
// Before: 테스트 불가능 (시간 고정 불가)
@Service
public class OrderService {

    public boolean isExpired(Order order) {
        return order.getCreatedAt()
            .plusDays(7)
            .isBefore(LocalDateTime.now());  // 테스트 시 시간 제어 불가
    }
}

// After: Clock 주입
@Service
@RequiredArgsConstructor
public class OrderService {

    private final Clock clock;  // 테스트 시 고정 시간 주입 가능

    public boolean isExpired(Order order) {
        return order.getCreatedAt()
            .plusDays(7)
            .isBefore(LocalDateTime.now(clock));
    }
}

// 프로덕션 설정
@Configuration
public class ClockConfig {
    @Bean
    public Clock clock() {
        return Clock.systemDefaultZone();
    }
}

// 테스트
@Test
void testIsExpired() {
    Clock fixedClock = Clock.fixed(
        Instant.parse("2024-01-15T10:00:00Z"),
        ZoneId.systemDefault()
    );
    OrderService service = new OrderService(fixedClock);

    Order order = Order.builder()
        .createdAt(LocalDateTime.of(2024, 1, 1, 10, 0))
        .build();

    assertTrue(service.isExpired(order));
}
```

### 외부 API Mock

```java
// Before: 외부 API 직접 호출
@Service
public class PaymentService {
    private final RestTemplate restTemplate;

    public PaymentResult process(PaymentRequest req) {
        return restTemplate.postForObject(
            "https://payment.api.com/charge",
            req,
            PaymentResult.class
        );
    }
}

// After: 인터페이스 추출
public interface PaymentGateway {
    PaymentResult charge(PaymentRequest req);
}

@Component
@Profile("!test")
public class ExternalPaymentGateway implements PaymentGateway {
    private final RestTemplate restTemplate;
    // 실제 API 호출
}

@Component
@Profile("test")
public class MockPaymentGateway implements PaymentGateway {
    @Override
    public PaymentResult charge(PaymentRequest req) {
        return PaymentResult.success("mock-tx-id");
    }
}
```

---

## 예외 처리 리팩토링

### 일반 예외 → 도메인 예외

```java
// Before: 일반적인 예외
if (product.getStock() < quantity) {
    throw new RuntimeException("Insufficient stock");
}

// After: 도메인 예외 + @ExceptionHandler
public class InsufficientStockException extends BusinessException {
    private final Long productId;
    private final int available;
    private final int requested;

    public InsufficientStockException(Long productId, int available, int requested) {
        super(String.format("Insufficient stock for product %d: available=%d, requested=%d",
            productId, available, requested));
        this.productId = productId;
        this.available = available;
        this.requested = requested;
    }
}

// 전역 예외 핸들러
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(InsufficientStockException.class)
    public ResponseEntity<ErrorResponse> handleInsufficientStock(InsufficientStockException e) {
        return ResponseEntity.status(HttpStatus.CONFLICT)
            .body(ErrorResponse.of("INSUFFICIENT_STOCK", e.getMessage()));
    }
}
```

---

## Anti-Patterns

| Anti-Pattern | 문제 | 해결 |
|--------------|------|------|
| Setter 주입 | 불변성 보장 안됨 | 생성자 주입 |
| @Autowired on field | 테스트 어려움 | 생성자 주입 |
| Service에서 HttpServletRequest | 계층 혼재 | DTO로 전달 |
| @Transactional on private | 작동 안함 | public 메서드에 |
| Lazy Loading in Controller | N+1, 세션 문제 | Fetch Join/DTO |
| 거대한 @Configuration | 관리 어려움 | 도메인별 분리 |

---

## 체크리스트

### 리팩토링 전

- [ ] 테스트 커버리지 충분?
- [ ] N+1 쿼리 확인? (`spring.jpa.show-sql=true`)
- [ ] 순환 참조 없음?

### 리팩토링 중

- [ ] 계층 분리 준수? (Controller/Service/Repository)
- [ ] 생성자 주입 사용?
- [ ] 메서드 20줄 이하?
- [ ] God Class 없음? (500줄 미만)

### 리팩토링 후

- [ ] 단위 테스트 통과?
- [ ] 통합 테스트 통과?
- [ ] 성능 저하 없음?

---

**관련 skill**: `/refactoring-principles`, `/spring-data`, `/spring-testing`
