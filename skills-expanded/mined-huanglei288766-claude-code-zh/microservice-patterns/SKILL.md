---
name: microservice-patterns
description: 微服务设计模式与 Spring Cloud Alibaba 实践，涵盖服务拆分、通信、网关、注册发现、配置中心、分布式事务、熔断降级、链路追踪
version: "1.0"
---

# 微服务设计模式

## 概述

本 Skill 提供微服务架构的核心设计模式和 Spring Cloud Alibaba 的完整实践方案，适用于中大型分布式系统的设计与落地。

适用场景：
- 单体应用拆分为微服务
- 微服务间通信方案选型
- API 网关设计与实现
- 分布式事务、熔断降级、链路追踪落地

---

## 服务拆分原则

### 按限界上下文拆分

```
# 电商系统拆分示例

┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  用户服务    │  │  商品服务    │  │  订单服务    │
│  user-svc   │  │  product-svc │  │  order-svc   │
│             │  │             │  │             │
│ - 注册/登录 │  │ - 商品管理   │  │ - 下单      │
│ - 用户信息  │  │ - SKU 管理   │  │ - 支付      │
│ - 权限管理  │  │ - 库存管理   │  │ - 退款      │
└─────────────┘  └─────────────┘  └─────────────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
              ┌─────────────────┐
              │   支付服务       │
              │   payment-svc   │
              │                 │
              │ - 支付渠道对接  │
              │ - 对账          │
              └─────────────────┘
```

### 拆分判断清单

```
拆分信号（应该拆）：
  [x] 不同团队负责不同模块
  [x] 模块之间变更频率差异大
  [x] 模块需要独立扩缩容
  [x] 模块的技术栈需求不同
  [x] 模块存在清晰的领域边界

不拆信号（保持单体或模块化单体）：
  [x] 团队人数少于 5 人
  [x] 模块间强耦合，频繁互相调用
  [x] 没有独立部署的需求
  [x] 数据一致性要求极高
```

---

## 服务间通信

### 同步通信：OpenFeign（REST）

```java
// 声明式 HTTP 客户端 — 订单服务调用商品服务
@FeignClient(
    name = "product-svc",                          // 服务名（Nacos 注册名）
    fallbackFactory = ProductClientFallbackFactory.class  // 降级工厂
)
public interface ProductClient {

    // 查询商品信息
    @GetMapping("/api/v1/products/{productId}")
    Result<ProductDTO> getProduct(@PathVariable("productId") Long productId);

    // 批量扣减库存
    @PostMapping("/api/v1/products/stock/deduct")
    Result<Void> deductStock(@RequestBody List<StockDeductRequest> requests);
}

// 降级工厂 — 调用失败时的兜底逻辑
@Component
public class ProductClientFallbackFactory implements FallbackFactory<ProductClient> {

    private static final Logger log = LoggerFactory.getLogger(ProductClientFallbackFactory.class);

    @Override
    public ProductClient create(Throwable cause) {
        log.error("商品服务调用失败，触发降级", cause);
        return new ProductClient() {
            @Override
            public Result<ProductDTO> getProduct(Long productId) {
                // 返回缓存数据或默认值
                return Result.fail("商品服务暂时不可用，请稍后重试");
            }

            @Override
            public Result<Void> deductStock(List<StockDeductRequest> requests) {
                // 库存扣减不能降级，抛出异常触发事务回滚
                throw new ServiceUnavailableException("库存服务不可用");
            }
        };
    }
}
```

### 同步通信：gRPC（高性能场景）

```protobuf
// product.proto — 商品服务接口定义
syntax = "proto3";

package com.example.product;

option java_package = "com.example.product.grpc";
option java_outer_classname = "ProductProto";

// 商品服务
service ProductService {
  // 查询商品
  rpc GetProduct (GetProductRequest) returns (ProductResponse);
  // 批量查询（服务端流）
  rpc ListProducts (ListProductsRequest) returns (stream ProductResponse);
}

message GetProductRequest {
  int64 product_id = 1;
}

message ProductResponse {
  int64 id = 1;
  string name = 2;
  int64 price_cents = 3;  // 价格（分）
  int32 stock = 4;
}
```

```java
// gRPC 客户端调用
@GrpcClient("product-svc")
private ProductServiceGrpc.ProductServiceBlockingStub productStub;

public ProductDTO getProduct(Long productId) {
    GetProductRequest request = GetProductRequest.newBuilder()
            .setProductId(productId)
            .build();
    ProductResponse response = productStub.getProduct(request);
    return ProductDTO.fromGrpc(response);
}
```

### 异步通信：RocketMQ

```java
// 生产者 — 订单创建后发送消息
@Component
public class OrderEventProducer {

    private final RocketMQTemplate rocketMQTemplate;

    public OrderEventProducer(RocketMQTemplate rocketMQTemplate) {
        this.rocketMQTemplate = rocketMQTemplate;
    }

    // 发送订单创建事件
    public void sendOrderCreatedEvent(OrderCreatedEvent event) {
        String topic = "order-topic";
        String tag = "order-created";
        // 使用订单 ID 作为 key，保证同一订单的消息有序
        Message<OrderCreatedEvent> message = MessageBuilder
                .withPayload(event)
                .setHeader(RocketMQHeaders.KEYS, String.valueOf(event.getOrderId()))
                .build();
        rocketMQTemplate.syncSend(topic + ":" + tag, message);
    }

    // 发送延迟消息（订单超时自动取消）
    public void sendOrderTimeoutMessage(Long orderId) {
        Message<Long> message = MessageBuilder.withPayload(orderId).build();
        // 延迟级别 16 = 30 分钟
        rocketMQTemplate.syncSend("order-topic:order-timeout", message, 3000, 16);
    }
}

// 消费者 — 商品服务监听订单事件
@Component
@RocketMQMessageListener(
    topic = "order-topic",
    selectorExpression = "order-created",
    consumerGroup = "product-consumer-group"
)
public class OrderCreatedConsumer implements RocketMQListener<OrderCreatedEvent> {

    private final StockService stockService;

    public OrderCreatedConsumer(StockService stockService) {
        this.stockService = stockService;
    }

    @Override
    public void onMessage(OrderCreatedEvent event) {
        // 扣减库存
        stockService.deductStock(event.getItems());
    }
}
```

### 通信方式选型

```
场景                    推荐方式        原因
──────────────────────────────────────────────────────────
查询类操作              REST/Feign     简单直观，易调试
高频内部调用            gRPC           高性能，强类型
事件通知                消息队列       解耦，削峰
最终一致性              消息队列       可靠投递，重试
实时性要求高            REST/gRPC      同步等待结果
跨语言服务              gRPC           IDL + 多语言代码生成
```

---

## API 网关模式

### Spring Cloud Gateway 配置

```yaml
# gateway 服务 application.yml
spring:
  cloud:
    gateway:
      # 全局默认过滤器
      default-filters:
        - StripPrefix=1                    # 去掉第一层路径前缀
        - name: RequestRateLimiter         # 全局限流
          args:
            redis-rate-limiter.replenishRate: 100
            redis-rate-limiter.burstCapacity: 200
            key-resolver: "#{@ipKeyResolver}"

      # 路由规则
      routes:
        # 用户服务
        - id: user-svc
          uri: lb://user-svc               # lb:// 表示负载均衡
          predicates:
            - Path=/api/user/**
          filters:
            - name: CircuitBreaker         # 熔断
              args:
                name: userCircuitBreaker
                fallbackUri: forward:/fallback/user

        # 商品服务
        - id: product-svc
          uri: lb://product-svc
          predicates:
            - Path=/api/product/**

        # 订单服务
        - id: order-svc
          uri: lb://order-svc
          predicates:
            - Path=/api/order/**
          filters:
            - name: Retry                  # 重试
              args:
                retries: 2
                statuses: SERVICE_UNAVAILABLE
                backoff:
                  firstBackoff: 200ms
                  maxBackoff: 2000ms
```

### 全局认证过滤器

```java
// 统一鉴权过滤器
@Component
public class AuthGlobalFilter implements GlobalFilter, Ordered {

    private static final List<String> WHITE_LIST = List.of(
            "/api/user/login",
            "/api/user/register",
            "/api/product/list"
    );

    private final JwtTokenProvider tokenProvider;

    public AuthGlobalFilter(JwtTokenProvider tokenProvider) {
        this.tokenProvider = tokenProvider;
    }

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String path = exchange.getRequest().getURI().getPath();

        // 白名单跳过认证
        if (WHITE_LIST.stream().anyMatch(path::startsWith)) {
            return chain.filter(exchange);
        }

        // 提取并验证 Token
        String token = exchange.getRequest().getHeaders().getFirst("Authorization");
        if (token == null || !token.startsWith("Bearer ")) {
            return unauthorized(exchange, "缺少认证令牌");
        }

        try {
            String jwt = token.substring(7);
            Claims claims = tokenProvider.parseToken(jwt);
            // 将用户信息传递给下游服务
            ServerHttpRequest mutatedRequest = exchange.getRequest().mutate()
                    .header("X-User-Id", claims.getSubject())
                    .header("X-User-Name", claims.get("username", String.class))
                    .header("X-User-Roles", claims.get("roles", String.class))
                    .build();
            return chain.filter(exchange.mutate().request(mutatedRequest).build());
        } catch (Exception e) {
            return unauthorized(exchange, "令牌无效或已过期");
        }
    }

    @Override
    public int getOrder() {
        return -100;    // 优先级最高
    }

    private Mono<Void> unauthorized(ServerWebExchange exchange, String message) {
        exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
        exchange.getResponse().getHeaders().setContentType(MediaType.APPLICATION_JSON);
        String body = "{\"code\":401,\"message\":\"" + message + "\"}";
        DataBuffer buffer = exchange.getResponse().bufferFactory().wrap(body.getBytes());
        return exchange.getResponse().writeWith(Mono.just(buffer));
    }
}
```

---

## 服务注册与发现（Nacos）

### 服务端配置

```yaml
# application.yml — 微服务注册到 Nacos
spring:
  application:
    name: order-svc
  cloud:
    nacos:
      discovery:
        server-addr: ${NACOS_ADDR:127.0.0.1:8848}
        namespace: ${NACOS_NAMESPACE:dev}        # 环境隔离
        group: DEFAULT_GROUP
        # 元数据，用于灰度发布等
        metadata:
          version: v1.2.0
          env: ${SPRING_PROFILES_ACTIVE:dev}
```

### 配置中心（Nacos Config）

```yaml
# bootstrap.yml — 从 Nacos 拉取配置
spring:
  application:
    name: order-svc
  cloud:
    nacos:
      config:
        server-addr: ${NACOS_ADDR:127.0.0.1:8848}
        namespace: ${NACOS_NAMESPACE:dev}
        file-extension: yaml
        # 共享配置（多服务复用）
        shared-configs:
          - data-id: common-db.yaml       # 数据库公共配置
            group: SHARED_GROUP
            refresh: true
          - data-id: common-redis.yaml    # Redis 公共配置
            group: SHARED_GROUP
            refresh: true
        # 扩展配置（本服务私有）
        extension-configs:
          - data-id: order-rocketmq.yaml
            group: ORDER_GROUP
            refresh: true
```

```java
// 配置热更新 — 使用 @RefreshScope 或 @ConfigurationProperties
@ConfigurationProperties(prefix = "order.config")
public class OrderConfig {
    // Nacos 修改后自动生效，无需重启
    private Integer maxRetryTimes = 3;      // 最大重试次数
    private Integer timeoutMinutes = 30;    // 订单超时时间（分钟）
    private Boolean enablePromotion = true; // 是否启用促销

    // getter/setter 省略
}
```

---

## 分布式事务

### Seata Saga 模式（推荐长事务场景）

```java
// 下单流程编排 — Saga 状态机 JSON 定义
// resources/statemachine/order-create.json
/*
{
  "Name": "orderCreateSaga",
  "States": {
    "CreateOrder":    { "Type": "ServiceTask", "Next": "DeductStock",    "CompensateState": "CancelOrder" },
    "DeductStock":    { "Type": "ServiceTask", "Next": "DeductBalance",  "CompensateState": "RestoreStock" },
    "DeductBalance":  { "Type": "ServiceTask", "Next": "Succeed",        "CompensateState": "RefundBalance" },
    "CancelOrder":    { "Type": "ServiceTask" },
    "RestoreStock":   { "Type": "ServiceTask" },
    "RefundBalance":  { "Type": "ServiceTask" },
    "Succeed":        { "Type": "Succeed" }
  }
}
*/

// Saga 服务实现
@Service
public class OrderSagaService {

    // 正向操作：创建订单
    public OrderDTO createOrder(CreateOrderCommand cmd) {
        Order order = Order.create(cmd.getUserId(), cmd.getItems());
        orderRepository.save(order);
        return OrderDTO.from(order);
    }

    // 补偿操作：取消订单
    public void cancelOrder(OrderDTO orderDTO) {
        Order order = orderRepository.findById(orderDTO.getId())
                .orElseThrow(() -> new OrderNotFoundException(orderDTO.getId()));
        order.cancel("Saga 补偿回滚");
        orderRepository.save(order);
    }
}

@Service
public class StockSagaService {

    // 正向操作：扣减库存
    public void deductStock(List<StockDeductRequest> items) {
        items.forEach(item -> {
            int affected = stockMapper.deductStock(item.getSkuId(), item.getQuantity());
            if (affected == 0) {
                throw new InsufficientStockException(item.getSkuId());
            }
        });
    }

    // 补偿操作：恢复库存
    public void restoreStock(List<StockDeductRequest> items) {
        items.forEach(item ->
            stockMapper.restoreStock(item.getSkuId(), item.getQuantity())
        );
    }
}
```

### 本地消息表（轻量方案）

```java
// 可靠消息最终一致性 — 不依赖 Seata
@Service
public class OrderService {

    private final OrderRepository orderRepository;
    private final OutboxRepository outboxRepository;

    // 下单 + 写消息表在同一个本地事务中
    @Transactional
    public Order createOrder(CreateOrderCommand cmd) {
        // 1. 创建订单
        Order order = Order.create(cmd);
        orderRepository.save(order);

        // 2. 写消息到本地 outbox 表
        OutboxMessage message = OutboxMessage.builder()
                .topic("order-topic")
                .tag("order-created")
                .messageKey(String.valueOf(order.getId()))
                .payload(JSON.toJSONString(OrderCreatedEvent.from(order)))
                .status(OutboxStatus.PENDING)
                .build();
        outboxRepository.save(message);

        return order;
    }
}

// 定时任务扫描 outbox 表发送消息
@Component
public class OutboxPublisher {

    private final OutboxRepository outboxRepository;
    private final RocketMQTemplate rocketMQTemplate;

    @Scheduled(fixedDelay = 1000)    // 每秒扫描一次
    public void publishPendingMessages() {
        List<OutboxMessage> messages = outboxRepository
                .findByStatusOrderByCreatedAtAsc(OutboxStatus.PENDING, PageRequest.of(0, 100));

        for (OutboxMessage msg : messages) {
            try {
                rocketMQTemplate.syncSend(msg.getTopic() + ":" + msg.getTag(),
                        MessageBuilder.withPayload(msg.getPayload()).build());
                msg.markAsSent();
                outboxRepository.save(msg);
            } catch (Exception e) {
                msg.incrementRetryCount();
                outboxRepository.save(msg);
            }
        }
    }
}
```

---

## 熔断降级（Sentinel）

### 流控与熔断规则

```java
// 注解方式定义资源和降级逻辑
@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {

    private final OrderAppService orderAppService;

    public OrderController(OrderAppService orderAppService) {
        this.orderAppService = orderAppService;
    }

    @GetMapping("/{orderId}")
    @SentinelResource(
        value = "getOrder",
        blockHandler = "getOrderBlock",           // 限流/熔断时的处理
        fallback = "getOrderFallback"             // 业务异常时的降级
    )
    public Result<OrderVO> getOrder(@PathVariable Long orderId) {
        return Result.success(orderAppService.getOrder(orderId));
    }

    // 限流/熔断处理方法（参数需与原方法一致 + BlockException）
    public Result<OrderVO> getOrderBlock(Long orderId, BlockException ex) {
        return Result.fail(429, "请求过于频繁，请稍后重试");
    }

    // 业务异常降级方法
    public Result<OrderVO> getOrderFallback(Long orderId, Throwable ex) {
        return Result.fail(503, "订单服务暂时不可用");
    }
}
```

```yaml
# application.yml — Sentinel 配置
spring:
  cloud:
    sentinel:
      transport:
        dashboard: ${SENTINEL_DASHBOARD:localhost:8080}
        port: 8719
      # 从 Nacos 加载规则（持久化）
      datasource:
        flow:
          nacos:
            server-addr: ${NACOS_ADDR:localhost:8848}
            data-id: ${spring.application.name}-flow-rules
            group-id: SENTINEL_GROUP
            data-type: json
            rule-type: flow
        degrade:
          nacos:
            server-addr: ${NACOS_ADDR:localhost:8848}
            data-id: ${spring.application.name}-degrade-rules
            group-id: SENTINEL_GROUP
            data-type: json
            rule-type: degrade
```

### 规则定义示例

```json
// Nacos 中的流控规则：order-svc-flow-rules
[
  {
    "resource": "getOrder",
    "limitApp": "default",
    "grade": 1,
    "count": 100,
    "strategy": 0,
    "controlBehavior": 0,
    "clusterMode": false
  }
]

// Nacos 中的熔断规则：order-svc-degrade-rules
// 10 秒内请求数 >= 5 且慢调用比例 > 50% 时熔断 30 秒
[
  {
    "resource": "getOrder",
    "grade": 0,
    "count": 1000,
    "slowRatioThreshold": 0.5,
    "timeWindow": 30,
    "minRequestAmount": 5,
    "statIntervalMs": 10000
  }
]
```

---

## 链路追踪（SkyWalking）

### 接入配置

```yaml
# application.yml — SkyWalking Agent 配置（通常通过 JVM 参数注入）
# java -javaagent:/path/to/skywalking-agent.jar \
#      -Dskywalking.agent.service_name=order-svc \
#      -Dskywalking.collector.backend_service=localhost:11800 \
#      -jar app.jar

# Dockerfile 中集成 SkyWalking Agent
# COPY --from=skywalking/agent:9.0.0 /skywalking/agent /opt/skywalking-agent
# ENV SW_AGENT_NAME=order-svc
# ENV SW_AGENT_COLLECTOR_BACKEND_SERVICES=skywalking-oap:11800
# ENTRYPOINT ["java", "-javaagent:/opt/skywalking-agent/skywalking-agent.jar", ...]
```

### 自定义 Span（手动埋点）

```java
// 对关键业务逻辑添加自定义追踪
@Service
public class PaymentService {

    @Trace                                    // 自动创建 Span
    @Tags({
        @Tag(key = "orderId", value = "arg[0]"),
        @Tag(key = "amount", value = "arg[1]")
    })
    public PaymentResult pay(Long orderId, BigDecimal amount) {
        // SkyWalking 自动记录方法的耗时、参数、返回值
        ActiveSpan.tag("payChannel", "alipay");   // 自定义标签
        ActiveSpan.info("开始调用支付渠道");        // 日志事件

        try {
            PaymentResult result = payChannel.execute(orderId, amount);
            ActiveSpan.tag("payStatus", result.getStatus().name());
            return result;
        } catch (Exception e) {
            ActiveSpan.error(e);                  // 标记异常
            throw e;
        }
    }
}
```

### 日志关联 TraceId

```xml
<!-- logback-spring.xml — 日志中自动注入 TraceId -->
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <!-- [TID] 占位符由 SkyWalking logback 插件自动替换为 TraceId -->
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] [TID:%X{tid}] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <!-- SkyWalking 日志上报 -->
    <appender name="SW_GRPC_LOG" class="org.apache.skywalking.apm.toolkit.log.logback.v1.x.log.GRPCLogClientAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <root level="INFO">
        <appender-ref ref="CONSOLE" />
        <appender-ref ref="SW_GRPC_LOG" />
    </root>
</configuration>
```

---

## 微服务技术栈总览

```
层次            技术选型                       说明
─────────────────────────────────────────────────────────────
API 网关       Spring Cloud Gateway            路由、限流、鉴权
服务通信       OpenFeign / gRPC / RocketMQ     同步 + 异步
注册发现       Nacos Discovery                 服务注册与健康检查
配置中心       Nacos Config                    动态配置热更新
熔断降级       Sentinel                        流控、熔断、系统保护
分布式事务     Seata (Saga/TCC) / 本地消息表   根据场景选择
链路追踪       SkyWalking                      全链路追踪 + 日志关联
日志收集       ELK (Filebeat + Logstash)       集中式日志管理
监控告警       Prometheus + Grafana            指标采集与可视化
容器编排       Docker + Kubernetes             部署与扩缩容
```

---

## 常见问题速查

| 问题 | 解决方案 |
|------|---------|
| 服务间循环依赖 | 引入事件驱动解耦，或抽取公共服务 |
| Feign 调用超时 | 调整 `connectTimeout` 和 `readTimeout`，配合熔断 |
| 分布式 ID 冲突 | 使用雪花算法（Snowflake）或 Leaf |
| 配置变更不生效 | 检查 `@RefreshScope` 或 `@ConfigurationProperties` 是否生效 |
| 消息重复消费 | 消费端做幂等处理（唯一键 / 状态机） |
| 链路追踪丢失 | 检查线程池是否传递了 TraceContext |
| 服务雪崩 | 配置 Sentinel 熔断规则 + 降级兜底 |
| 灰度发布 | Nacos metadata + Gateway 路由权重 |
