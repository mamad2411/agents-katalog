---
name: domain-invariant-check
description: 审计代码是否真正保护了领域不变量。扫描 service 方法，对照 docs/service/{module}_service.md §7 业务规则 / 隐式约束 / 业务状态机，校验伪码 [INVARIANT-CHECK: I-N] 标记与代码实现的一致性。命中标 🔴 严重（结构性问题）或 🟡 待复核。
disable-model-invocation: true
argument-hint: "[scope] 可选：当前 PR / {module} / {module}/{Method}；空则扫 git diff main..HEAD"
---

审计代码 ↔ 领域不变量一致性。范围：`$ARGUMENTS`。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 不生成代码。

## 第 0 步：🚫 模块 + 启用状态检查

1. 读 `BUILD_STATUS.md` §0 —— 命中 🚫 模块跳过
2. 读 `INDEX.md` §0 —— 如 `docs-spec/09 §7 领域不变量` 未启用 → 跳过本 Skill

## 第 1 步：读约束源

按顺序读：

1. `docs/service/{module}_service.md` §7 —— §7.1 业务规则 / §7.2 隐式约束 / §7.3 业务状态机
2. `docs/architecture/ai_dev_guide.md` §8.3 —— 领域不变量约束总清单
3. `docs/BUILD_STATUS.md` §11.3 —— 领域不变量启用状态（已设计 / 已启用条目数）

## 第 2 步：扫描代码范围

按 `$ARGUMENTS` 确定扫描范围：

- 空：`git diff main..HEAD --name-only` 取新增/修改的 service / controller / models 文件
- `{module}`：`service/{module}/**/*.go`
- `{module}/{Method}`：聚焦该方法实现及其测试

## 第 3 步：4 项审计

### 审计 1：[INVARIANT-CHECK: I-N] 标记 ↔ 代码实现匹配率

```
对每个含 [INVARIANT-CHECK: I-N] 标记的方法：
  1. 查 §7.1 业务规则表中 I-N 对应的"不变量"条目
  2. 在该方法的代码实现中搜索对应的校验语句（如 if {amount-field} < 0 / status 流转检查）
  3. 匹配 → 通过；不匹配 → 标 🔴 严重（标记与实现脱节，结构性问题）

匹配率统计：matched / total，<95% → 触发回头复审
```

### 审计 2：业务规则保护完整性

```
对 §7.1 中每条业务规则 I-N：
  1. 查所有引用 I-N 涉及的代码位置（§7.1 "代码位置"列）
  2. 校验这些位置的代码确实有校验该规则的逻辑
  3. 缺失 → 标 🔴 严重（漏校验是结构性缺陷）
  4. 校验逻辑被绕过（如新增 if 分支跳过校验）→ 标 🔴 严重
```

### 审计 3：隐式约束遵守情况

```
对 §7.2 中每条隐式约束：
  1. 查约束的应用范围（如"{核心校验接口} 不能写 MySQL"）
  2. 扫描对应代码路径是否真的避开了禁止的操作
  3. 违反 → 标 🟡 待复核（隐式约束往往无显式 grep 锚，需人工判断）
```

### 审计 4：业务状态机转换合法性

```
对 §7.3 业务状态机：
  1. 提取所有合法转换（PENDING→ACTIVE / ACTIVE→SUSPENDED 等）
  2. 在代码中搜索状态变更语句（UPDATE ... SET status=?）
  3. 校验每次变更是否：
     - 验证了当前状态（防止非法跳转）
     - 转换路径在 §7.3 表内
  4. 违反 → 标 🔴 严重（破坏状态机是数据一致性根因）
```

## 第 4 步：输出格式

按严重程度分组：

```
🔴 严重 — 标记 / 业务规则 / 状态机 结构性问题
  - [I-1] {Module}.{Method}：声明保护 {核心数值字段}≥0，但代码未发现校验
  - [State-Machine] {Module}.{Method}：UPDATE {状态字段}={state-A} WHERE {状态字段}={state-Z} （非法转换）

🟡 待复核 — 隐式约束疑似违反（需人工判断）
  - [§7.2] {file}:line：{核心校验接口} 调用了 MysqlClient.Save，与"不能写 MySQL"约束疑似冲突

🟢 通过 — 全部匹配

📊 统计
  - 不变量声明 / 实现匹配率：{N}/{M} = {P}%
  - 业务规则覆盖率：{N}/{M}
  - 状态机合法转换：{N}/{M}
  - 建议人工 reviewer 复核：M 处
```

## 第 5 步：测试同步

**不适用**——本 Skill 不生成业务代码。

但建议：如审计发现某条不变量虽有 `[INVARIANT-CHECK]` 标记但缺少对应测试用例（即缺"业务错误"类用例覆盖违反场景），提示在 PR 补充测试。

## 第 6 步：文档同步

本 Skill 不直接修改文档。审计结果应记录到 PR/工单，并对应到 BUILD_STATUS §11.3 领域不变量"已启用条目数"。

## 与其他 Skill 的关系

- 与 `doc-sync-check`：审计维度互补（前者代码 ↔ 文档；本 Skill 代码 ↔ 领域不变量约束）
- 与 `new-service`：建议在 `/new-service` 生成涉及业务规则的方法后自动触发 `/domain-invariant-check`
- 与 `failure-path-review`：并列的审计 Skill；不变量违反往往是失败路径未覆盖的根因


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
