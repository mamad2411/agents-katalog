# Spring Boot DDD 领域驱动设计

## 概述

本 Skill 指导你在 Spring Boot 项目中实现领域驱动设计（DDD）四层架构，包含完整的代码模板和最佳实践。

适用场景：
- 新建 Spring Boot 服务时确定分层结构
- 重构现有项目至 DDD 架构
- 设计领域模型、聚合根、值对象
- 编写 Repository 接口和 Infrastructure 实现

## 四层架构

```
Interfaces → Application → Domain ← Infrastructure
```

### 目录结构

```
src/main/java/com/example/{bizModule}/
├── interfaces/
│   ├── controller/     # REST 控制器
│   ├── facade/         # 门面层（可选）
│   ├── vo/             # 视图对象
│   ├── assembler/      # VO ↔ DTO 转换
│   ├── mq/             # MQ 消费者
│   └── job/            # 定时任务
├── application/
│   ├── service/        # 应用服务（I{Biz}AppService）
│   ├── dto/            # 数据传输对象
│   └── executor/       # 命令执行器
├── domain/
│   ├── model/          # 领域模型（充血模型）
│   ├── valueobject/    # 值对象（不可变）
│   ├── repository/     # Repository 接口
│   └── service/        # 领域服务（I{Biz}DomainService）
└── infra/
    ├── repository/
    │   ├── mysql/      # MySQL 实现
    │   ├── es/         # ES 实现
    │   ├── po/         # 持久化对象
    │   └── assembler/  # PO ↔ Model 转换
    ├── proxy/          # 外部服务代理
    └── mq/             # MQ 生产者
```

## 各层代码规范

### Domain 层 — 聚合根示例

```java
// domain/model/Order.java
public class Order {
    private OrderId id;
    private UserId userId;
    private List<OrderItem> items;  // 聚合内实体
    private OrderStatus status;
    private Money totalAmount;      // 值对象
    private LocalDateTime createdAt;

    // 工厂方法（代替 new）
    public static Order create(UserId userId, List<OrderItem> items) {
        Order order = new Order();
        order.id = OrderId.generate();
        order.userId = userId;
        order.items = new ArrayList<>(items);
        order.status = OrderStatus.PENDING;
        order.totalAmount = calculateTotal(items);
        order.createdAt = LocalDateTime.now();
        return order;
    }

    // 领域行为（充血模型）
    public void confirm() {
        if (this.status != OrderStatus.PENDING) {
            throw new DomainException("只有待确认的订单可以确认");
        }
        this.status = OrderStatus.CONFIRMED;
    }

    public void cancel(String reason) {
        if (this.status == OrderStatus.COMPLETED) {
            throw new DomainException("已完成的订单不可取消");
        }
        this.status = OrderStatus.CANCELLED;
        this.cancelReason = reason;
    }

    private static Money calculateTotal(List<OrderItem> items) {
        return items.stream()
            .map(OrderItem::getSubtotal)
            .reduce(Money.ZERO, Money::add);
    }
}
```

### Domain 层 — 值对象示例

```java
// domain/valueobject/Money.java
public record Money(BigDecimal amount, Currency currency) {
    public static final Money ZERO = new Money(BigDecimal.ZERO, Currency.CNY);

    public Money {
        Objects.requireNonNull(amount, "金额不能为空");
        Objects.requireNonNull(currency, "货币类型不能为空");
        if (amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new DomainException("金额不能为负数");
        }
    }

    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new DomainException("不同货币无法相加");
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }

    public Money multiply(int quantity) {
        return new Money(this.amount.multiply(BigDecimal.valueOf(quantity)), this.currency);
    }
}
```

### Domain 层 — Repository 接口

```java
// domain/repository/IOrderRepository.java
public interface IOrderRepository {
    Optional<Order> findById(OrderId id);
    List<Order> findByUserId(UserId userId);
    void save(Order order);
    void delete(OrderId id);
}
```

### Application 层 — AppService

```java
// application/service/IOrderAppService.java
public interface IOrderAppService {
    OrderDTO createOrder(CreateOrderCommand command);
    void confirmOrder(OrderId orderId);
    void cancelOrder(OrderId orderId, String reason);
    PageResult<OrderDTO> listOrders(OrderQueryDTO query);
}

// application/service/OrderAppServiceImpl.java
@Service
@Transactional  // 事务只在 AppService 层
public class OrderAppServiceImpl implements IOrderAppService {
    private final IOrderRepository orderRepository;
    private final IOrderDomainService orderDomainService;

    @Override
    public OrderDTO createOrder(CreateOrderCommand command) {
        // 1. 参数校验
        command.validate();
        // 2. 构建领域对象
        List<OrderItem> items = command.getItems().stream()
            .map(this::toOrderItem)
            .toList();
        // 3. 调用领域服务（复杂业务）或直接构建聚合根（简单业务）
        Order order = Order.create(command.getUserId(), items);
        // 4. 持久化
        orderRepository.save(order);
        // 5. 返回 DTO
        return OrderDTO.from(order);
    }
}
```

### Infrastructure 层 — Repository 实现

```java
// infra/repository/mysql/OrderRepositoryImpl.java
@Repository
public class OrderRepositoryImpl implements IOrderRepository {
    private final OrderMapper orderMapper;
    private final OrderItemMapper orderItemMapper;
    private final OrderPoAssembler assembler;

    @Override
    public Optional<Order> findById(OrderId id) {
        OrderPO po = orderMapper.selectById(id.getValue());
        if (po == null) return Optional.empty();
        List<OrderItemPO> itemPos = orderItemMapper.selectByOrderId(id.getValue());
        return Optional.of(assembler.toDomain(po, itemPos));
    }

    @Override
    @Transactional(propagation = Propagation.MANDATORY)  // 强制要求外部事务
    public void save(Order order) {
        OrderPO po = assembler.toPo(order);
        orderMapper.insertOrUpdate(po);
        // 批量保存订单项
        List<OrderItemPO> itemPos = assembler.toItemPos(order.getItems());
        orderItemMapper.batchInsertOrUpdate(itemPos);
    }
}
```

### Interfaces 层 — Controller

```java
// interfaces/controller/OrderController.java
@RestController
@RequestMapping("/api/v1/orders")
@Validated
public class OrderController {
    private final IOrderAppService orderAppService;

    @PostMapping
    public ApiResponse<OrderVO> createOrder(@Valid @RequestBody CreateOrderRequest request) {
        CreateOrderCommand command = OrderVoAssembler.toCommand(request);
        OrderDTO dto = orderAppService.createOrder(command);
        OrderVO vo = OrderVoAssembler.toVO(dto);
        return ApiResponse.success(vo);
    }

    @PutMapping("/{orderId}/confirm")
    public ApiResponse<Void> confirmOrder(@PathVariable String orderId) {
        orderAppService.confirmOrder(OrderId.of(orderId));
        return ApiResponse.success();
    }
}
```

## 常见错误与正确做法

### ❌ 错误：Controller 直接调用 Repository

```java
// 错误！跨层调用
@PostMapping
public ApiResponse<?> create(...) {
    orderRepository.save(order);  // 不应在 Controller 出现
}
```

### ✅ 正确：通过 AppService 调用

```java
@PostMapping
public ApiResponse<?> create(...) {
    orderAppService.createOrder(command);  // 只调用 AppService
}
```

### ❌ 错误：Domain 层依赖 Spring 注解

```java
// 错误！Domain 不依赖 Spring
@Component
public class Order {
    @Autowired
    private SomeService service;
}
```

### ✅ 正确：Domain 纯 POJO

```java
public class Order {
    // 无任何 Spring 注解
    // 通过构造器或工厂方法创建
}
```

## 相关规则

- [java-coding-style](../../rules/java-coding-style.md)
