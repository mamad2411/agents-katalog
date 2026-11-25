# Redis 常见场景与最佳实践

## 概述

本 Skill 涵盖 Redis 在 Java Spring Boot 项目中的常见使用模式，包括缓存、分布式锁、限流、Session 等。

适用场景：
- 缓存设计与防穿透/击穿/雪崩
- 分布式锁实现
- 接口限流
- 延迟队列

---

## 缓存三大问题及解决方案

### 缓存穿透（查不存在的数据）

```java
// 问题：查询 DB 不存在的 key，每次都打到 DB
// 解决：缓存空值 + 布隆过滤器

@Service
public class UserCacheService {
    private final StringRedisTemplate redis;
    private final UserMapper userMapper;
    private static final String NULL_VALUE = "NULL";  // 空值占位符
    private static final long NULL_TTL = 60L;         // 空值缓存60秒

    public UserVO getUser(Long id) {
        String key = "user:" + id;
        String cached = redis.opsForValue().get(key);

        if (NULL_VALUE.equals(cached)) {
            return null;  // 缓存了空值，直接返回
        }
        if (cached != null) {
            return JSON.parseObject(cached, UserVO.class);
        }

        // 查 DB
        User user = userMapper.selectById(id);
        if (user == null) {
            // 缓存空值，防止穿透
            redis.opsForValue().set(key, NULL_VALUE, NULL_TTL, TimeUnit.SECONDS);
            return null;
        }

        UserVO vo = UserVO.from(user);
        redis.opsForValue().set(key, JSON.toJSONString(vo), 30, TimeUnit.MINUTES);
        return vo;
    }
}
```

### 缓存击穿（热点 key 过期瞬间大量请求）

```java
// 解决方案一：互斥锁（简单，但有等待）
public UserVO getUserWithMutex(Long id) {
    String key = "user:" + id;
    String lockKey = "lock:user:" + id;

    String cached = redis.opsForValue().get(key);
    if (cached != null) return JSON.parseObject(cached, UserVO.class);

    // 尝试获取互斥锁
    Boolean locked = redis.opsForValue().setIfAbsent(lockKey, "1", 10, TimeUnit.SECONDS);
    if (Boolean.TRUE.equals(locked)) {
        try {
            // 双重检查
            cached = redis.opsForValue().get(key);
            if (cached != null) return JSON.parseObject(cached, UserVO.class);

            User user = userMapper.selectById(id);
            UserVO vo = UserVO.from(user);
            redis.opsForValue().set(key, JSON.toJSONString(vo), 30, TimeUnit.MINUTES);
            return vo;
        } finally {
            redis.delete(lockKey);
        }
    } else {
        // 未获取到锁，短暂等待后重试（有限次数，防止无限递归）
        int maxRetry = 3;
        for (int i = 0; i < maxRetry; i++) {
            Thread.sleep(50);
            cached = redis.opsForValue().get(key);
            if (cached != null) return JSON.parseObject(cached, UserVO.class);
        }
        throw new ServiceException("获取数据超时，请重试");
    }
}

// 解决方案二：逻辑过期（不真正过期，性能更好）
// 缓存结构: { "data": {...}, "expireTime": 1710000000000 }
```

### 缓存雪崩（大量 key 同时过期）

```java
// 解决：TTL 加随机抖动
int baseTtl = 30;  // 基础 30 分钟
int jitter = new Random().nextInt(10);  // 随机 0-10 分钟
redis.opsForValue().set(key, value, baseTtl + jitter, TimeUnit.MINUTES);
```

---

## 分布式锁

```java
// 使用 Redisson（推荐，比手写可靠）
@Configuration
public class RedissonConfig {
    @Bean
    public RedissonClient redissonClient() {
        Config config = new Config();
        config.useSingleServer().setAddress("redis://localhost:6379");
        return Redisson.create(config);
    }
}

@Service
public class OrderService {
    private final RedissonClient redisson;

    public void createOrder(Long userId, CreateOrderDTO dto) {
        // 用户级别的分布式锁，防止重复下单
        RLock lock = redisson.getLock("lock:create-order:" + userId);
        try {
            // 最多等待3秒，持有锁最多10秒（自动续期watchdog机制）
            if (lock.tryLock(3, 10, TimeUnit.SECONDS)) {
                try {
                    // 幂等性检查
                    if (orderExists(dto.getOrderNo())) {
                        throw new BusinessException("订单已存在");
                    }
                    doCreateOrder(userId, dto);
                } finally {
                    lock.unlock();
                }
            } else {
                throw new BusinessException("操作频繁，请稍后重试");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new SystemException("获取锁被中断", e);
        }
    }
}
```

---

## 接口限流

```java
// 基于 Redis + Lua 脚本的滑动窗口限流（原子操作）
@Component
public class RateLimiter {
    private final StringRedisTemplate redis;

    // Lua 脚本保证原子性
    private static final String RATE_LIMIT_SCRIPT = """
        local key = KEYS[1]
        local limit = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])

        redis.call('ZREMRANGEBYSCORE', key, 0, now - window * 1000)
        local count = redis.call('ZCARD', key)

        if count < limit then
            redis.call('ZADD', key, now, now)
            redis.call('EXPIRE', key, window)
            return 1
        end
        return 0
        """;

    /**
     * @param key    限流 key（如 "rate:api:userId"）
     * @param limit  窗口内最大请求数
     * @param window 窗口大小（秒）
     */
    public boolean tryAcquire(String key, int limit, int window) {
        Long result = redis.execute(
            new DefaultRedisScript<>(RATE_LIMIT_SCRIPT, Long.class),
            Collections.singletonList(key),
            String.valueOf(limit),
            String.valueOf(window),
            String.valueOf(System.currentTimeMillis())
        );
        return Long.valueOf(1).equals(result);
    }
}

// 注解式使用（配合 AOP）
@RateLimit(key = "api:create-order", limit = 5, window = 1)  // 1秒内最多5次
@PostMapping("/orders")
public ApiResponse<?> createOrder(...) { ... }
```

---

## 延迟队列（延迟任务）

```java
// 使用 Redis ZSet 实现延迟队列
// score = 执行时间戳（毫秒）
@Service
public class DelayQueueService {
    private final StringRedisTemplate redis;
    private static final String DELAY_QUEUE_KEY = "delay:queue:orders";

    // 添加延迟任务（30分钟后执行）
    public void addDelayTask(String orderId, int delayMinutes) {
        long executeTime = System.currentTimeMillis() + delayMinutes * 60_000L;
        redis.opsForZSet().add(DELAY_QUEUE_KEY, orderId, executeTime);
    }

    // 轮询到期任务（定时任务每秒执行）
    @Scheduled(fixedDelay = 1000)
    public void processDelayTasks() {
        long now = System.currentTimeMillis();
        // 获取所有 score <= now 的任务
        Set<String> tasks = redis.opsForZSet().rangeByScore(
            DELAY_QUEUE_KEY, 0, now, 0, 10
        );
        if (tasks == null || tasks.isEmpty()) return;

        for (String orderId : tasks) {
            // 用 ZREM 保证只有一个实例处理（分布式场景）
            Long removed = redis.opsForZSet().remove(DELAY_QUEUE_KEY, orderId);
            if (removed != null && removed > 0) {
                handleExpiredOrder(orderId);  // 处理超时订单
            }
        }
    }
}
```

---

## Key 设计规范

```
# 格式：业务:模块:标识符
user:info:12345          # 用户信息
user:token:12345         # 用户 token
order:detail:ORDER_001   # 订单详情
order:list:user:12345    # 用户订单列表
lock:create-order:12345  # 分布式锁
rate:api:create-order    # 限流 key
delay:queue:orders       # 延迟队列

# 规则：
# 1. 全小写，冒号分隔层级
# 2. 避免包含特殊字符（空格/换行）
# 3. 大 Value 考虑压缩（gzip）
# 4. 设置合理 TTL，避免 key 堆积
```
