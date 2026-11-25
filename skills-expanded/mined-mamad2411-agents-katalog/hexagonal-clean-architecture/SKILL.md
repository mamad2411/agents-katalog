---
name: hexagonal-clean-architecture
category: architecture
description: "Hexagonal Architecture (Clean Architecture) — Ports & Adapters 패턴, 의존성 역전, 도메인 중심 설계로 테스트 가능하고 유연한 시스템 구축 Use when working with architecture 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Hexagonal Architecture (Clean Architecture)
Ports & Adapters 패턴, 의존성 역전, 도메인 중심 설계로 테스트 가능하고 유연한 시스템 구축

---

## Quick Reference

```
아키텍처 스타일 선택 결정 트리
│
├─ CRUD 중심, 단순 비즈니스 로직?
│  └─ YES → Layered Architecture (Spring MVC 전통 방식)
├─ 복잡한 비즈니스 규칙, 여러 외부 시스템 연동?
│  ├─ 도메인 로직이 핵심 자산? → Hexagonal Architecture
│  └─ 엔터프라이즈급, 명확한 계층 분리 → Clean Architecture (4-Layer)
└─ DDD Aggregate + 인프라 교체 필요? → Hexagonal + DDD

패턴 매핑: Hexagonal ≈ Clean ≈ Onion (같은 철학, 다른 용어)
  - Hexagonal: Port/Adapter 강조
  - Clean: Dependency Rule + 4계층 명시
  - Onion: Domain Core 중심, 동심원 구조
```

---

## CRITICAL: Hexagonal Architecture (Ports & Adapters)

### 핵심 원칙 (Alistair Cockburn, 2005)

1. **도메인이 중심** (비즈니스 로직이 프레임워크/DB/UI에 의존하지 않음)
2. **Port = 인터페이스** (도메인이 외부와 통신하는 경계)
3. **Adapter = 구현체** (Port를 실제 기술로 구현)
4. **의존성 역전** (외부 → 도메인 방향, 도메인은 외부를 모름)

### 아키텍처 다이어그램

```
  Driving Adapters (Primary)        Driven Adapters (Secondary)
  REST, GraphQL, gRPC, CLI         JPA, Kafka, Redis, S3
        │ implements                      ▲ implements
  ┌─────▼──────────────┐    ┌─────────────┴──────────────┐
  │ Driving Ports (In)  │    │ Driven Ports (Out)         │
  │ OrderService        │    │ OrderRepository            │
  │ PaymentUseCase      │    │ PaymentGateway             │
  └─────────┬───────────┘    └────────────▲──────────────┘
            │     Domain Core (Hexagon)    │
            └──► Order, Payment, Rules ────┘
```

### Port & Adapter 종류

| Port 타입 | 방향 | 역할 | 예시 |
|----------|-----|-----|------|
| **Driving Port** (Inbound) | 외부 → 도메인 | 도메인 기능 노출 | OrderService, PaymentUseCase |
| **Driven Port** (Outbound) | 도메인 → 외부 | 외부 기능 정의 | OrderRepository, PaymentGateway |

| Adapter 타입 | 구현 대상 | 예시 |
|-------------|---------|------|
| **Driving** (Primary) | Driving Port | RestController, gRPC Server |
| **Driven** (Secondary) | Driven Port | JpaRepository, KafkaProducer |

---

## CRITICAL: Clean Architecture와의 관계

```
┌─────────────────────────────────────┐
│ Frameworks & Drivers (최외곽)       │ ← Web, DB, External
│  ┌───────────────────────────────┐  │
│  │ Interface Adapters            │  │ ← Controllers, Gateways
│  │  ┌─────────────────────────┐  │  │
│  │  │ Application (Use Cases) │  │  │ ← 도메인 로직 조율
│  │  │  ┌───────────────────┐  │  │  │
│  │  │  │ Entities (Core)   │  │  │  │ ← 핵심 비즈니스 규칙
│  │  │  └───────────────────┘  │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
Dependency Rule: 안쪽으로만 의존
```

| Hexagonal | Clean Architecture | 역할 |
|-----------|-------------------|------|
| Domain Core | Entities | 핵심 비즈니스 규칙 |
| Driving Port 구현 | Use Cases | 애플리케이션 로직 |
| Adapter | Interface Adapters | Controller, Gateway |
| Infrastructure | Frameworks & Drivers | Spring, JPA, Kafka |

---

## CRITICAL: Spring Boot 구현

### 패키지 구조

```
com.example.order/
├── domain/                    # 순수 비즈니스 로직 (외부 의존성 없음)
│   ├── model/Order.java, OrderItem.java, OrderStatus.java
│   ├── service/OrderPricingService.java
│   └── exception/OrderNotFoundException.java
├── application/               # Use Case
│   ├── port/
│   │   ├── in/OrderUseCase.java, PaymentUseCase.java
│   │   └── out/OrderRepository.java, PaymentGateway.java, EventPublisher.java
│   └── service/OrderService.java
├── adapter/
│   ├── in/web/OrderController.java, dto/
│   └── out/persistence/OrderJpaAdapter.java, OrderEntity.java
└── config/ApplicationConfig.java
```

### 1. Domain Core

```java
// domain/model/Order.java — 순수 도메인, 외부 의존 없음
public class Order {
    private String id;
    private String customerId;
    private List<OrderItem> items = new ArrayList<>();
    private OrderStatus status;
    private BigDecimal totalAmount;

    public static Order create(String customerId, List<OrderItem> items) {
        if (items.isEmpty()) throw new IllegalArgumentException("Order must have at least one item");
        Order order = new Order();
        order.customerId = customerId;
        order.items = new ArrayList<>(items);
        order.status = OrderStatus.PENDING;
        order.totalAmount = items.stream().map(OrderItem::getPrice).reduce(BigDecimal.ZERO, BigDecimal::add);
        return order;
    }
    public void complete() {
        if (status != OrderStatus.PENDING) throw new IllegalStateException("Only pending orders can be completed");
        this.status = OrderStatus.COMPLETED;
    }
    public void cancel() {
        if (status == OrderStatus.COMPLETED) throw new IllegalStateException("Completed orders cannot be cancelled");
        this.status = OrderStatus.CANCELLED;
    }
}
```

### 2. Application Ports

```java
// Driving Port (Inbound)
public interface OrderUseCase {
    OrderResult createOrder(CreateOrderCommand command);
    OrderResult getOrder(String orderId);
    void cancelOrder(String orderId);
}
public record CreateOrderCommand(String customerId, List<OrderItemDto> items) {}

// Driven Port (Outbound)
public interface OrderRepository {
    Order save(Order order);
    Optional<Order> findById(String id);
}
public interface PaymentGateway {
    PaymentResult processPayment(String orderId, BigDecimal amount);
}
public interface EventPublisher {
    void publishOrderCreated(Order order);
    void publishOrderCompleted(Order order);
}
```

### 3. Use Case (Application Service)

```java
@Service @Transactional
public class OrderService implements OrderUseCase {
    private final OrderRepository orderRepository;
    private final PaymentGateway paymentGateway;
    private final EventPublisher eventPublisher;

    public OrderService(OrderRepository orderRepo, PaymentGateway paymentGw, EventPublisher eventPub) {
        this.orderRepository = orderRepo;
        this.paymentGateway = paymentGw;
        this.eventPublisher = eventPub;
    }

    @Override
    public OrderResult createOrder(CreateOrderCommand command) {
        List<OrderItem> items = command.items().stream()
            .map(dto -> new OrderItem(dto.productId(), dto.quantity(), dto.price())).toList();
        Order order = Order.create(command.customerId(), items);
        Order saved = orderRepository.save(order);
        PaymentResult payment = paymentGateway.processPayment(saved.getId(), saved.getTotalAmount());
        if (payment.isSuccess()) {
            saved.complete();
            orderRepository.save(saved);
            eventPublisher.publishOrderCompleted(saved);
        }
        return OrderResult.from(saved);
    }
}
```

### 4. Driving Adapter (REST Controller)

```java
@RestController @RequestMapping("/api/orders")
public class OrderController {
    private final OrderUseCase orderUseCase;
    public OrderController(OrderUseCase orderUseCase) { this.orderUseCase = orderUseCase; }

    @PostMapping @ResponseStatus(HttpStatus.CREATED)
    public OrderResponse createOrder(@RequestBody CreateOrderRequest request) {
        CreateOrderCommand cmd = new CreateOrderCommand(request.customerId(), request.items());
        return OrderResponse.from(orderUseCase.createOrder(cmd));
    }
    @GetMapping("/{id}")
    public OrderResponse getOrder(@PathVariable String id) {
        return OrderResponse.from(orderUseCase.getOrder(id));
    }
}
```

### 5. Driven Adapter (JPA)

```java
@Repository
public class OrderJpaAdapter implements OrderRepository {
    private final OrderJpaRepository jpaRepository;
    private final OrderMapper mapper;

    public OrderJpaAdapter(OrderJpaRepository jpaRepo, OrderMapper mapper) {
        this.jpaRepository = jpaRepo; this.mapper = mapper;
    }
    @Override public Order save(Order order) {
        return mapper.toDomain(jpaRepository.save(mapper.toEntity(order)));
    }
    @Override public Optional<Order> findById(String id) {
        return jpaRepository.findById(id).map(mapper::toDomain);
    }
}
```

### 6. ArchUnit 의존성 검증

```java
class ArchitectureTest {
    JavaClasses classes = new ClassFileImporter().importPackages("com.example.order");

    @Test void domainShouldNotDependOnOutside() {
        noClasses().that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAnyPackage("..adapter..", "..application..", "org.springframework..")
            .check(classes);
    }
    @Test void hexagonalArchitecture() {
        onionArchitecture()
            .domainModels("..domain.model..")
            .applicationServices("..application..")
            .adapter("web", "..adapter.in.web..")
            .adapter("persistence", "..adapter.out.persistence..")
            .check(classes);
    }
}
```

---

## Go 구현

### 패키지 구조

```
cmd/order-service/main.go
internal/
├── domain/order.go
├── port/
│   ├── inbound/order_usecase.go
│   └── outbound/order_repository.go, payment_gateway.go
├── application/order_service.go
└── adapter/
    ├── inbound/http/order_handler.go
    └── outbound/postgres/order_repository.go
```

### 1. Domain Core

```go
// internal/domain/order.go
type OrderStatus string
const (
    StatusPending   OrderStatus = "PENDING"
    StatusCompleted OrderStatus = "COMPLETED"
    StatusCancelled OrderStatus = "CANCELLED"
)
type Order struct {
    ID, CustomerID string
    Items          []OrderItem
    Status         OrderStatus
    TotalAmount    float64
    CreatedAt      time.Time
}

func NewOrder(customerID string, items []OrderItem) (*Order, error) {
    if len(items) == 0 { return nil, errors.New("order must have at least one item") }
    return &Order{CustomerID: customerID, Items: items, Status: StatusPending,
        TotalAmount: calculateTotal(items), CreatedAt: time.Now()}, nil
}
func (o *Order) Complete() error {
    if o.Status != StatusPending { return errors.New("only pending orders can be completed") }
    o.Status = StatusCompleted; return nil
}
func (o *Order) Cancel() error {
    if o.Status == StatusCompleted { return errors.New("completed orders cannot be cancelled") }
    o.Status = StatusCancelled; return nil
}
```

### 2. Ports

```go
// internal/port/inbound/order_usecase.go
type OrderUseCase interface {
    CreateOrder(ctx context.Context, cmd CreateOrderCommand) (*OrderResult, error)
    GetOrder(ctx context.Context, id string) (*OrderResult, error)
    CancelOrder(ctx context.Context, id string) error
}
type CreateOrderCommand struct { CustomerID string; Items []OrderItemDTO }

// internal/port/outbound/order_repository.go
type OrderRepository interface {
    Save(ctx context.Context, order *domain.Order) error
    FindByID(ctx context.Context, id string) (*domain.Order, error)
}
type PaymentGateway interface {
    ProcessPayment(ctx context.Context, orderID string, amount float64) (*PaymentResult, error)
}
```

### 3. Application Service

```go
// internal/application/order_service.go
type OrderService struct {
    repo    outbound.OrderRepository
    payment outbound.PaymentGateway
}
func NewOrderService(repo outbound.OrderRepository, payment outbound.PaymentGateway) *OrderService {
    return &OrderService{repo: repo, payment: payment}
}
func (s *OrderService) CreateOrder(ctx context.Context, cmd inbound.CreateOrderCommand) (*inbound.OrderResult, error) {
    items := make([]domain.OrderItem, len(cmd.Items))
    for i, dto := range cmd.Items {
        items[i] = domain.OrderItem{ProductID: dto.ProductID, Quantity: dto.Quantity, Price: dto.Price}
    }
    order, err := domain.NewOrder(cmd.CustomerID, items)
    if err != nil { return nil, err }
    if err := s.repo.Save(ctx, order); err != nil { return nil, err }
    result, err := s.payment.ProcessPayment(ctx, order.ID, order.TotalAmount)
    if err != nil { return nil, err }
    if result.Success { order.Complete(); s.repo.Save(ctx, order) }
    return &inbound.OrderResult{ID: order.ID, Status: string(order.Status)}, nil
}
```

### 4. HTTP Handler (Driving Adapter)

```go
// internal/adapter/inbound/http/order_handler.go
type OrderHandler struct { useCase inbound.OrderUseCase }

func NewOrderHandler(uc inbound.OrderUseCase) *OrderHandler { return &OrderHandler{useCase: uc} }

func (h *OrderHandler) CreateOrder(w http.ResponseWriter, r *http.Request) {
    var req CreateOrderRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest); return
    }
    cmd := inbound.CreateOrderCommand{CustomerID: req.CustomerID, Items: req.Items}
    result, err := h.useCase.CreateOrder(r.Context(), cmd)
    if err != nil { http.Error(w, err.Error(), http.StatusInternalServerError); return }
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(result)
}
```

---

## 실전 적용 가이드

| 시나리오 | Hexagonal 적합도 | 추천 아키텍처 |
|---------|----------------|-------------|
| CRUD 중심 (간단한 비즈니스 로직) | 오버엔지니어링 | Layered (전통 MVC) |
| 복잡한 비즈니스 규칙, 외부 시스템 연동 | 적합 | Hexagonal |
| 도메인 핵심 자산 (금융, 헬스케어) | 강력 추천 | Hexagonal + DDD |
| 인프라 교체 가능성 높음 (멀티 클라우드) | 강력 추천 | Hexagonal |

### 점진적 도입 전략

```
1단계: 기존 Service → Domain + Application 분리
2단계: Repository 인터페이스를 port/out으로 이동, Adapter 생성
3단계: Controller → adapter/in/web, JpaRepo → adapter/out/persistence
4단계: ArchUnit 의존성 규칙 자동 검증
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Adapter에서 비즈니스 로직 | 도메인 규칙 분산 | Controller는 Use Case 위임만 |
| Port 없이 구체 클래스 의존 | 인프라 교체 불가, 테스트 어려움 | Port 인터페이스 통해 의존 |
| 과도한 Mapping (8단계 DTO 변환) | 유지보수 지옥 | 경계에서만 변환 (4단계) |
| 모든 프로젝트에 무조건 적용 | 단순 CRUD에 오버엔지니어링 | CRUD는 Layered, 복잡한 도메인만 Hexagonal |
| Domain이 Spring/JPA에 의존 | 프레임워크 종속, 테스트 어려움 | Domain은 순수 Java/Go만 |

---

## 체크리스트

### 설계
- [ ] 도메인 복잡도가 Hexagonal을 정당화하는가?
- [ ] Port가 도메인 관점에서 정의되었는가? (기술 중립적)
- [ ] Driving Port와 Driven Port 명확히 구분
- [ ] Domain Core가 외부 라이브러리에 의존하지 않는가?

### 구현
- [ ] 패키지 구조가 레이어 경계를 명확히 표현
- [ ] Application Service가 Use Case를 표현
- [ ] Adapter가 단순 변환만 수행, 비즈니스 로직 없음
- [ ] Entity-Domain 매핑 시 불필요한 변환 중복 제거

### 검증
- [ ] ArchUnit으로 의존성 규칙 자동 검증
- [ ] 도메인 로직을 인프라 없이 단위 테스트 가능
- [ ] 새로운 Adapter 추가 시 도메인 수정 불필요

### 유지보수
- [ ] 새 팀원이 레이어 경계를 이해하고 있는가?
- [ ] 비즈니스 규칙 변경 시 Domain Core만 수정하는가?
- [ ] 기술 스택 변경 시 도메인 불변성 유지되는가?

**관련 스킬**: `/msa-ddd`, `/go-microservice`, `/spring-testing`, `/msa-event-driven`, `/msa-resilience`
