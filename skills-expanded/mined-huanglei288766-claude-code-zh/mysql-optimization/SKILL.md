# MySQL 查询优化与索引设计

## 概述

本 Skill 涵盖 MySQL 8.0 的查询优化、索引设计、表结构设计规范，帮助 Claude Code 给出高性能的数据库方案。

适用场景：
- 新建表时设计索引策略
- 慢查询分析与优化
- 大表分页查询优化
- 联合查询性能调优

---

## 索引设计原则

### 最左前缀原则

```sql
-- 联合索引 (a, b, c)，以下查询能否用到索引：
-- ✅ WHERE a = 1               → 用到 a
-- ✅ WHERE a = 1 AND b = 2     → 用到 (a, b)
-- ✅ WHERE a = 1 AND b > 2     → 用到 (a, b)，b 是范围条件后续列失效
-- ❌ WHERE b = 2               → 跳过 a，无法使用
-- ❌ WHERE b = 2 AND c = 3     → 跳过 a，无法使用

-- 正确建立联合索引：高选择性列在前，等值条件列在前，范围条件列在后
ALTER TABLE orders ADD INDEX idx_user_status_time (user_id, status, created_at);
-- 支持：WHERE user_id = ? AND status = ? AND created_at > ?
```

### 索引覆盖（避免回表）

```sql
-- ❌ 需要回表（idx_user_id 只有 user_id，还需要查主键取其他列）
SELECT id, order_no, amount FROM orders WHERE user_id = 123;

-- ✅ 覆盖索引（查询所需列都在索引里）
ALTER TABLE orders ADD INDEX idx_user_cover (user_id, id, order_no, amount);
-- EXPLAIN 中 Extra 显示 "Using index"
```

### 索引失效场景

```sql
-- ❌ 函数运算导致索引失效
SELECT * FROM orders WHERE DATE(created_at) = '2026-03-14';
-- ✅ 改写为范围查询
SELECT * FROM orders
WHERE created_at >= '2026-03-14 00:00:00'
  AND created_at <  '2026-03-15 00:00:00';

-- ❌ 隐式类型转换（user_id 是 varchar，传入数字）
SELECT * FROM orders WHERE user_id = 123456;
-- ✅ 类型匹配
SELECT * FROM orders WHERE user_id = '123456';

-- ❌ LIKE 以通配符开头
SELECT * FROM users WHERE name LIKE '%张%';
-- ✅ 改用全文索引或 ES
```

---

## 大表分页优化

```sql
-- ❌ 深分页性能极差（OFFSET 100万需要扫描100万行再丢弃）
SELECT * FROM orders ORDER BY id LIMIT 1000000, 20;

-- ✅ 方案一：游标分页（推荐，需要业务支持）
-- 第一页
SELECT * FROM orders WHERE id > 0 ORDER BY id LIMIT 20;
-- 下一页（传入上一页最后一条 id）
SELECT * FROM orders WHERE id > #{lastId} ORDER BY id LIMIT 20;

-- ✅ 方案二：子查询 + 覆盖索引
SELECT o.* FROM orders o
JOIN (
  SELECT id FROM orders ORDER BY id LIMIT 1000000, 20
) t ON o.id = t.id;

-- ✅ 方案三：业务限制（禁止跳页，只允许"下一页"）
```

---

## 常见慢查询模式与优化

### N+1 查询

```java
// ❌ N+1：查 100 个订单，再循环查 100 次用户
List<Order> orders = orderMapper.findAll();
for (Order order : orders) {
    User user = userMapper.findById(order.getUserId()); // N 次查询
    order.setUserName(user.getName());
}

// ✅ 批量查询 + Map 组装
List<Order> orders = orderMapper.findAll();
Set<Long> userIds = orders.stream().map(Order::getUserId).collect(toSet());
Map<Long, User> userMap = userMapper.findByIds(userIds).stream()
    .collect(toMap(User::getId, identity()));
orders.forEach(o -> o.setUserName(userMap.get(o.getUserId()).getName()));
```

### 联表查询 vs 多次单表

```sql
-- 数据量小（< 100万）：JOIN 性能好
SELECT o.*, u.name AS user_name
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 1;

-- 数据量大（> 百万）：分别查询再应用层组装，避免大表 JOIN
-- 1. SELECT * FROM orders WHERE status = 1 LIMIT 100
-- 2. 取出 user_ids
-- 3. SELECT * FROM users WHERE id IN (...)
```

---

## 表结构设计规范

```sql
CREATE TABLE orders (
    -- 主键：BIGINT UNSIGNED AUTO_INCREMENT（不用 UUID，索引性能差）
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

    -- 业务 ID：UUID v7 或雪花算法（对外暴露，不暴露自增 id）
    order_no    VARCHAR(32)     NOT NULL,

    -- 外键字段：不加外键约束（分布式/高并发场景）
    user_id     BIGINT UNSIGNED NOT NULL,

    -- 金额：DECIMAL，不用 FLOAT/DOUBLE（浮点精度问题）
    amount      DECIMAL(12, 2)  NOT NULL DEFAULT '0.00',

    -- 枚举状态：TINYINT（节省空间，代码里用常量映射）
    status      TINYINT         NOT NULL DEFAULT 0,

    -- 时间：DATETIME(3) 精确到毫秒，存 UTC
    created_at  DATETIME(3)     NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    updated_at  DATETIME(3)     NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
                                         ON UPDATE CURRENT_TIMESTAMP(3),
    -- 逻辑删除
    deleted     TINYINT(1)      NOT NULL DEFAULT 0,

    PRIMARY KEY (id),
    UNIQUE KEY uk_order_no (order_no),
    KEY idx_user_status (user_id, status),
    KEY idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## EXPLAIN 解读

```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 123 AND status = 1;
```

| 字段 | 好的值 | 警告值 | 含义 |
|------|--------|--------|------|
| type | const/ref/range | index/ALL | 扫描类型，ALL 是全表扫描 |
| key | 索引名 | NULL | 实际使用的索引 |
| rows | 越小越好 | 万级以上需优化 | 估计扫描行数 |
| Extra | Using index | Using filesort / Using temporary | 附加信息 |

**优化目标**: type 至少 range，避免 ALL；Extra 不出现 `Using filesort`（无索引排序）

---

## MyBatis-Plus 常见优化

```java
// ❌ 查询所有字段
orderMapper.selectList(new LambdaQueryWrapper<Order>()
    .eq(Order::getUserId, userId));

// ✅ 只查需要的字段
orderMapper.selectList(new LambdaQueryWrapper<Order>()
    .select(Order::getId, Order::getOrderNo, Order::getStatus)
    .eq(Order::getUserId, userId)
    .eq(Order::getDeleted, 0));

// ✅ 大批量操作用 saveBatch，不要循环 insert
orderMapper.insertBatchSomeColumn(orderList);  // MyBatis-Plus 批量插入
```
