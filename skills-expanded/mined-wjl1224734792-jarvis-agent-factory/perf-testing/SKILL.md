---
name: perf-testing
description: "性能测试方法论——k6/Artillery 脚本编写、基线对比、瓶颈定位、性能回归检测。用于性能测试、负载测试和容量规划。"
version: "4.3.8"
updated: "2026-05-14"
---

# 性能测试方法论

## 概述

性能测试不是"跑个压测看能不能扛住"，而是**系统化的容量验证和退化检测过程**。本技能指导你从定义指标到定位瓶颈的完整方法论。

**核心原则：** 性能是特性，不是事后优化。每个关键路径都应有性能预算，每次发布都应验证性能无退化。

## 何时使用

**适用场景：**
- 新 API 端点上线前的性能验证
- 系统容量规划（能支撑多少并发用户）
- 性能回归检测（发布前对比基线）
- 慢查询 / 慢接口根因定位
- 基础设施选型验证

**不适用场景：**
- 简单页面的首屏加载（用 Lighthouse 即可）
- 已知无性能要求的内部工具
- 开发环境中的临时调试

---

## 方法论

### 步骤 1：定义性能预算

为每个关键路径定义性能预算（SLO）：

| 路径 | 指标 | 预算 | 严重度 |
|------|------|------|--------|
| GET /api/users | P95 延迟 | < 200ms | High |
| POST /api/orders | P99 延迟 | < 1000ms | Medium |
| GET /api/search | 吞吐量 | > 100 rps | High |
| WebSocket 推送 | 延迟 | < 50ms | Critical |

### 步骤 2：选择测试类型

| 测试类型 | 目的 | 工具 |
|---------|------|------|
| **负载测试** | 验证预期负载下的性能 | k6 / Artillery |
| **压力测试** | 找到系统崩溃的极限 | k6 / wrk |
| **浸泡测试** | 检测内存泄漏和资源耗尽 | k6 (长时间) |
| **尖峰测试** | 验证突发流量下的行为 | k6 (ramping-arrival-rate) |
| **基准测试** | 建立性能基线 | autocannon / k6 |

### 步骤 3：编写测试脚本

#### k6 脚本模板
```javascript
import http from 'k6/http';
import { check, sleep, group } from 'k6';

export const options = {
  // 负载配置
  scenarios: {
    // 场景1: 渐进式负载
    ramp_up: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30s', target: 20 },  // 爬升
        { duration: '1m', target: 20 },   // 保持
        { duration: '30s', target: 0 },   // 下降
      ],
    },
    // 场景2: 恒定吞吐量
    constant_rate: {
      executor: 'constant-arrival-rate',
      rate: 100,
      timeUnit: '1s',
      duration: '1m',
      preAllocatedVUs: 20,
    },
  },
  
  // 性能门禁
  thresholds: {
    http_req_duration: [
      'p(95)<500',     // 95% 请求 < 500ms
      'p(99)<1000',    // 99% 请求 < 1s
    ],
    http_req_failed: ['rate<0.01'],  // 错误率 < 1%
    http_reqs: ['rate>50'],          // QPS > 50
  },
  
  // 摘要输出
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
};

export default function () {
  // 用户注册
  group('注册', () => {
    const payload = JSON.stringify({
      username: `user_${__VU}_${__ITER}`,
      email: `user_${__VU}_${__ITER}@test.com`,
    });
    const params = { headers: { 'Content-Type': 'application/json' } };
    const res = http.post('http://localhost:3000/api/register', payload, params);
    check(res, { '注册成功': (r) => r.status === 201 });
  });
  
  sleep(1);
}
```

#### Artillery 脚本模板
```yaml
config:
  target: "http://localhost:3000"
  phases:
    # 阶段1: 预热
    - duration: 30
      arrivalRate: 5
    # 阶段2: 稳定负载  
    - duration: 60
      arrivalRate: 20
    # 阶段3: 尖峰
    - duration: 30
      arrivalRate: 50
  plugins:
    expect: {}
    metrics-by-endpoint: {}
  ensure:
    p95: 500
    errorRate: 0.01

scenarios:
  - name: "用户注册流程"
    weight: 3
    flow:
      - post:
          url: "/api/register"
          json:
            username: "{{ $randomString() }}"
            email: "{{ $randomString() }}@test.com"
          expect:
            statusCode: 201
            contentType: json

  - name: "获取用户列表"
    weight: 7
    flow:
      - get:
          url: "/api/users"
          expect:
            statusCode: 200
```

### 步骤 4：建立性能基线

首次运行记录基线：
```bash
# k6
k6 run --out json=baseline.json script.js

# 基线数据保存位置
# .jarvis/YYYY-MM-DD/testing/perf-baselines/<场景名>-baseline.json
```

基线数据应包含：
- 每个端点的 P50/P95/P99 延迟
- 吞吐量 (RPS)
- 错误率
- 并发 VU 数
- 运行时间和环境信息

### 步骤 5：对比与判定

每次发布前重新运行，对比基线：

```bash
# 运行当前测试
k6 run --out json=current.json script.js

# 对比脚本
node scripts/compare-perf.js baseline.json current.json
```

退化判定规则：
| 指标 | 警告阈值 | 阻塞阈值 |
|------|---------|---------|
| P50 | +20% | +50% |
| P95 | +15% | +30% |
| P99 | +10% | +25% |
| 吞吐量 | -10% | -25% |
| 错误率 | +0.5% | +2% |

### 步骤 6：定位瓶颈

性能退化时的排查路径：
1. **数据库**：慢查询日志 → 缺失索引 → N+1 查询
2. **API**：序列化开销 → 无缓存 → 同步阻塞
3. **网络**：连接池耗尽 → DNS 解析 → 超时配置
4. **内存**：GC 压力 → 内存泄漏 → 大对象分配
5. **CPU**：正则回溯 → 加密运算 → 无限循环

---

## 反模式

| 反模式 | 正确做法 |
|--------|---------|
| 所有测试用一个并发数 | 至少 3 级并发（低/中/高）找性能拐点 |
| 只测 P50 延迟 | 必须覆盖 P95/P99，长尾延迟伤害最大 |
| 不设性能门禁就宣称通过 | 门禁是客观标准，没有就是主观判断 |
| 负载测试数据和生产差异巨大 | 测试数据分布应模拟生产 |
| 在已运行的服务器上加压 | 每次测试冷启动，基线可对比 |
| 忽视预热效应 | JIT/缓存需要预热，测试应包含预热阶段 |

## 验证清单

- [ ] 关键路径定义了性能预算（SLO）
- [ ] 测试脚本覆盖了主要 API 端点
- [ ] 使用多级负载找到性能拐点
- [ ] 已建立性能基线并保存到文档目录
- [ ] 当前测试与基线对比在门禁内
- [ ] 测试数据分布模拟生产环境
- [ ] 测试环境隔离（不污染生产和开发环境）
