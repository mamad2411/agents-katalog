---
name: new-saga-step
description: 生成 Saga 步骤的正向操作 + 补偿操作 + 幂等保证。读 docs/service/transaction_design.md §2 事务边界清单中标 Saga 的方法，按 §3 补偿逻辑设计 + §4 幂等性设计生成代码。
disable-model-invocation: true
argument-hint: "{module}/{Method}/step-{N}（占位符；落地按业务替换，具体示例见 SKILL §10 参考示例）"
---

生成 Saga 步骤代码。参数：`$ARGUMENTS`，格式 `{module}/{Method}/step-{N}`。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。

## 第 0 步：🚫 模块 + 启用状态检查

1. 读 `BUILD_STATUS.md` §0 —— 命中 🚫 模块立即拒绝
2. 读 `INDEX.md` §0 AIWeave 采纳进度 —— 如 `docs-spec/21_distributed_transaction` 未启用 → 拒绝，提示"本工程未启用 21，请先启用"

## 第 1 步：读设计文档

按顺序读：

1. `docs/service/transaction_design.md` —— §2 事务边界清单 + §3 补偿逻辑设计 + §4 幂等性设计 + §6 失败路径全景图
2. `docs/service/{module}_service.md` —— §4.N 单个方法的完整规格 + §4.N.3 处理步骤伪码 + §4.N.8 事务与一致性
3. `docs/architecture/concurrency_safety.md` §2 —— 涉及的共享状态（如 Redis Key 锁）
4. `docs/architecture/ai_dev_guide.md` §8.2 —— 事务与一致性约束总清单

## 第 2 步：校验前置

- 目标方法必须在 `transaction_design.md §2` 标 "Saga N 步"；如未登记 → 拒绝，要求先补 §2
- 目标 step-N 必须在 §3 补偿逻辑设计表中有"正向 + 补偿"对照行；如缺 → 拒绝，要求先补 §3
- 幂等 Key 必须在 §4 已定义；如缺 → 拒绝，要求先补 §4

## 第 3 步：生成代码

按 service 方法伪码生成 step-N 代码。**必须包含**以下结构：

```go
// {Module}{Method}Step{N} 是 Saga 第 N 步的正向操作
func (s *{Module}Service) {Method}Step{N}(ctx context.Context, req *{Method}Step{N}Req) error {
    // [IDEMPOTENT-CHECK: key={ns}:idemp:{action}:{key-field}]
    if exists, err := s.checkIdempotent(ctx, req); err != nil {
        return err
    } else if exists {
        return nil // 幂等，跳过
    }

    // [INVARIANT-CHECK: I-N]  // 如本步关联领域不变量
    if violates := s.checkInvariant(req); violates != nil {
        return violates
    }

    // [SAGA-STEP-N] 正向操作
    if err := s.do{Step-N-Action}(ctx, req); err != nil {
        return err
    }

    // [METRIC-EMIT: {action}_step_{N}_total{result="ok"}]
    return nil
}

// {Module}{Method}Compensate{N} 是 Saga 第 N 步的补偿操作
// 必须可重复执行而不产生副作用（详见 transaction_design.md §3.2）
func (s *{Module}Service) {Method}Compensate{N}(ctx context.Context, req *{Method}Step{N}Req) error {
    // 补偿幂等去重
    lockKey := "{ns}:compensation_lock:{key-field}"
    if locked, err := s.acquireLock(ctx, lockKey); err != nil || !locked {
        return err
    }
    defer s.releaseLock(ctx, lockKey)

    // [COMPENSATE-N] 补偿操作
    return s.undo{Step-N-Action}(ctx, req)
}
```

## 第 4 步：文档同步

- `transaction_design.md §2`：如步骤数变化，同步事务范围列（如从 "Saga 3 步" → "Saga 4 步"）
- `transaction_design.md §6 失败路径全景图`：如本步引入新的失败分支，扩展 ASCII 图
- `{module}_service.md §4.N.3`：处理步骤伪码确保有 `[SAGA-STEP-N]` / `[COMPENSATE-N]` / `[IDEMPOTENT-CHECK]` 标记
- `BUILD_STATUS.md §11 约束清单状态轨道`：事务约束 / 幂等接口数 +1

## 第 5 步：测试同步

生成的 step-N 必须配套：

1. **正向用例**：成功路径
2. **补偿用例**：模拟下游失败，验证补偿被触发
3. **幂等用例**：连续两次调用，结果一致
4. **超时用例**：模拟 Saga 卡在本步超过 §3.3 补偿超时阈值，验证自动补偿
5. **故障注入用例**：使用 `framework.InjectMysqlFailure` / `InjectRedisFailure`（详见 [`docs-spec/17 §4.7`](../../../docs-spec/17_testing_design_spec.md)）

## 第 6 步：验证

```bash
go build ./service/{module}/...
go test -race ./service/{module}/...
go test ./test/cases/{audience}/{module}_*_test.go
```

## 与其他 Skill 的关系

- 与 `new-service`：本 Skill 是 `new-service` 在涉及 Saga 场景下的特化版本；普通方法仍用 `new-service`
- 与 `failure-path-review`：生成 step-N 后建议调用 `/failure-path-review` 审计失败分支覆盖
- 与 `domain-invariant-check`：如本步带 `[INVARIANT-CHECK]` 标记，建议调用 `/domain-invariant-check` 确认实现真正保护了不变量

---

## 第 10 步：参考示例（仅示意，落地按业务替换）

> ⚠️ 以下为示意，本 SKILL 主体（frontmatter / 第 0-第 6 步 / 与其他 Skill 的关系）已用占位符表达；落地工程时按业务语义替换占位符，不得直接照搬本节具体业务名作为规范。
>
> 示例服从 [`PRINCIPLES.md §12 占位符规则`](../../../PRINCIPLES.md#12-占位符规则强制--双轨结构) 的"参考示例段豁免"。

### 10.1 argument-hint 调用示例

落地工程实际调用本 Skill 的格式（举一个具体业务的例子）：

```
/new-saga-step billing/Deduct/step-2
```

含义：为 `billing` 模块的 `Deduct`（扣减余额）方法的 Saga 第 2 步生成代码。

### 10.2 占位符 → 业务名 对照（示例）

| 占位符 | 本节示例值 |
| --- | --- |
| `{module}` | billing |
| `{Method}` | Deduct |
| `{N}` | 2 |
| `{action}` | deduct |
| `{ns}` | acc |
| `{key-field}` | orderId |
| `{Step-N-Action}` | DecrBalance |
| `{Module}Service` | BillingService |


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
