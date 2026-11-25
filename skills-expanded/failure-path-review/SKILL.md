---
name: failure-path-review
description: 审计 service 方法的所有失败分支是否在 transaction_design.md §6 失败路径全景图中覆盖，且每条分支都有对应测试用例。命中标 🔴 严重（缺失关键分支）或 🟡 待复核。
disable-model-invocation: true
argument-hint: "[scope] 可选：当前 PR / {module} / {module}/{Method}；空则扫 git diff main..HEAD"
---

审计 service 方法失败路径覆盖完整性。范围：`$ARGUMENTS`。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 不生成代码。

## 第 0 步：🚫 模块 + 启用状态检查

1. 读 `BUILD_STATUS.md` §0 —— 命中 🚫 模块跳过
2. 读 `INDEX.md` §0 —— 如 `docs-spec/21` 未启用 → 跳过本 Skill

## 第 1 步：读约束源

按顺序读：

1. `docs/service/transaction_design.md` §6 —— 失败路径全景图（ASCII 图 + 分支清单）
2. `docs/architecture/cross_service_contract.md` §4 —— 故障传播矩阵
3. `docs/service/{module}_service.md` §4.N.7 —— 单方法的边界情况
4. `docs/testing/testing_design.md` §4.7 / §5.5 —— 故障注入 framework API + 高级用例 3 类
5. `docs/architecture/ai_dev_guide.md` §8.2 / §8.9 —— 事务一致性 / 跨服务合约约束总清单

## 第 2 步：扫描代码范围

按 `$ARGUMENTS` 确定扫描范围：

- 空：`git diff main..HEAD --name-only` 取新增/修改的 service / controller 文件
- `{module}`：`service/{module}/**/*.go`
- `{module}/{Method}`：聚焦该方法

## 第 3 步：5 项审计

### 审计 1：失败分支提取

```
对每个被扫描方法，静态分析提取所有"失败返回点"：
  - 所有 `return ..., err` 或 `return ..., Error{...}` 语句
  - 所有 panic / log.Fatal（应该 = 0）
  - 所有调用下游 / DB / Redis / MQ 的错误处理路径

每个失败分支命名为 F-N（按代码出现顺序）
```

### 审计 2：失败路径文档覆盖

```
对每个 F-N：
  1. 查 transaction_design.md §6 失败路径全景图 是否包含该分支
  2. 如涉及下游故障 → 查 cross_service_contract.md §4 故障传播矩阵
  3. 文档未覆盖 → 标 🔴 严重（结构性问题：失败路径无据可查）
```

### 审计 3：失败分支测试覆盖

```
对每个 F-N：
  1. 在 test/cases/{audience}/{module}_*_test.go 中搜索是否有触发该分支的测试用例
  2. 缺失 → 标 🔴 严重（按 PRINCIPLES §8 测试是验收唯一标准）
  3. 有 stub 但断言不完整（如只断言 err != nil 而无 errNo / 副作用）→ 标 🟡 待复核
```

### 审计 4：故障注入测试覆盖

```
对涉及下游调用的 F-N：
  1. 测试用例是否使用 framework.InjectRedisFailure / InjectMysqlFailure / 
     InjectKafkaFailure / ForceCircuitOpen 等 §4.7 故障注入 API
  2. 仅靠"巧合性测试"（如下游真的失败时）覆盖 → 标 🟡 待复核（不稳定）
```

### 审计 5：HOT-PATH 失败路径优先级

```
对带 [HOT-PATH] 标记的方法的 F-N：
  1. 失败路径必须无锁内 IO、无大对象分配（错误对象 < 1kB）
  2. 错误日志必须有限频 / 采样
  3. 违反 → 标 🟡 待复核（与 performance-review R-PERF-* 协作判断）
```

## 第 4 步：输出格式

按严重程度分组：

```
🔴 严重 — 失败分支未覆盖
  - [F-3 doc] {Module}.{Method}: line {N}  → return ErrorXyz
            transaction_design.md §6 未列出该分支，建议补 §6
  - [F-5 test] {Module}.{Method}: line {N}  → MySQL INSERT failed
            test/cases/{audience}/{module}_*_test.go 无对应用例

🟡 待复核 — 测试断言不完整 / 故障注入缺失
  - [F-2 weak] {Method}: 测试仅断言 err != nil，未断言 errNo
  - [F-7 unstable] {Method}: 测试依赖下游真的失败，未用 framework.InjectXxxFailure

🟢 通过 — 全部分支文档 + 测试覆盖完整

📊 统计
  - 扫描方法数：N
  - 失败分支数：M（按方法分布）
  - 文档覆盖率：{N}/{M} = {P}%
  - 测试覆盖率：{N}/{M} = {P}%
  - 故障注入使用率：{N}/{M} = {P}%
```

## 第 5 步：测试同步

**不适用**——本 Skill 不生成业务代码。但**如审计发现缺失测试，主动提示在 PR 中补齐**，引用 [`docs-spec/17 §5.5`](../../../docs-spec/17_testing_design_spec.md) 高级用例 3 类的"故障注入"类别。

## 第 6 步：文档同步

本 Skill 不直接修改文档；但**审计结果应记录到 PR/工单**，对应到 BUILD_STATUS §11 跨服务合约 / 事务约束的"已启用条目数"。

## 与其他 Skill 的关系

- 与 `doc-sync-check`：审计维度互补
- 与 `domain-invariant-check`：并列；不变量违反与失败路径缺失常同根
- 与 `new-saga-step`：新生成 Saga 步骤后建议自动触发 `/failure-path-review`
- 与 `performance-review`：HOT-PATH 失败路径需协作审计


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
