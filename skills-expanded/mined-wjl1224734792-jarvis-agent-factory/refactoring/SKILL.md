---
name: refactoring
description: "重构安全网方法论——行为漂移检测、突变测试、覆盖率对比、重构边界管理。用于安全重构，确保不改坏现有功能。"
version: "4.3.8"
updated: "2026-05-14"
---

# 重构安全网方法论

## 概述

重构不是"改代码让它更好看"，而是**在不改变可观察行为的前提下，改善代码内部结构**。本技能提供一套完整的安全网机制，确保重构不出事故。

**核心原则：** 没有保护的改造是破坏。重构的三层安全网——测试套件 + 覆盖率监控 + 行为漂移检测——缺一不可。

## 何时使用

**适用场景：**
- 代码可读性差，需要提取函数/重命名
- 圈复杂度高，需要简化逻辑
- 模块耦合过紧，需要解耦
- 重复代码需要消除
- 为后续功能开发做准备的结构优化

**不适用场景：**
- 修复 Bug（Bug 修复和重构是两个独立操作）
- 添加新功能（功能开发和重构不可混在一个 PR）
- 不知道代码为什么这么写（切斯特顿之栏——先理解意图再改）

---

## 方法论

### 重构三层安全网

```
第一层: 测试套件 — 全部通过 = 功能无回归
第二层: 覆盖率监控 — 不下降 = 测试保护无减弱
第三层: 行为漂移检测 — 通过 = 对外行为不变
```

### 步骤 1：定义重构边界（R1）

明确划定重构范围和不变行为：

```
## 重构边界文档
### 重构目标
- 原因: UserService 40个方法，圈复杂度 avg 15
- 目标: 拆分为 3 个独立服务，圈复杂度 avg < 8

### 重构范围
- 涉及文件: src/services/user.ts, src/services/auth.ts, src/controllers/user.ts
- 边界外文件（绝不触碰）: src/db/*, src/middleware/*, src/config/*

### 不变行为清单
| 行为 | 当前表现 | 必须保持 |
|------|---------|---------|
| getUser(id) 返回格式 | { id, name, email } | JSON 结构不变 |
| 用户不存在返回 | 404 + { error: "Not Found" } | 状态码+格式不变 |
| createUser 失败 | 400 + 字段级错误 | 错误格式不变 |
```

### 步骤 2：建立基线（R2）

```bash
# 1. 运行测试套件，确认全部通过
npm test

# 2. 记录基线覆盖率
npm test -- --coverage
# 记录：行覆盖率 + 分支覆盖率 + 函数覆盖率

# 3. 保存基线报告
# .jarvis/YYYY-MM-DD/refactoring/baseline-coverage.json
```

### 步骤 3：执行重构（R3）

重构手法速查：

| 手法 | 适用场景 | 安全性 |
|------|---------|--------|
| **Extract Function** | 长函数中有明确职责的子逻辑 | 高（机械操作） |
| **Rename Variable** | 变量名不表意 | 高（IDE 重构） |
| **Replace Conditional with Polymorphism** | switch/if 链按类型分发 | 中（需理解逻辑） |
| **Extract Class** | 一个类承担多重职责 | 中（需理解职责边界） |
| **Simplify Conditional** | 嵌套条件可合并 | 高（逻辑等价变换） |
| **Remove Dead Code** | 确认不可达的代码 | 中（需确认不可达） |

重构执行原则：
- **每次改动 < 20 行**，改完就跑测试
- **测试红了立即回退**，不要猜原因
- **不改行为**，只改结构
- **不改边界外文件**

### 步骤 4：行为漂移检测（R4）

#### 4.1 重新运行测试
```bash
npm test -- --coverage
```

#### 4.2 覆盖率对比
| 指标 | R2 基线 | R4 当前 | 差异 | 判定 |
|------|--------|--------|------|------|
| 行覆盖率 | 85% | 86% | +1% | ✅ |
| 分支覆盖率 | 72% | 73% | +1% | ✅ |
| 函数覆盖率 | 90% | 90% | 0% | ✅ |
| 测试通过数 | 142 | 142 | 0 | ✅ |

#### 4.3 行为漂移检测

行为漂移检测方法：

**方法 1：API 契约快照对比**（适用于有 API 的项目）
```typescript
// 重构前拍快照
const snapshot = {
  getUser: { input: ['user-1'], output: getUser('user-1') },
  createUser: { input: [{ name: 'Test' }], output: createUser({ name: 'Test' }) },
};

// 重构后对比
for (const [fn, { input }] of Object.entries(snapshot)) {
  const before = snapshot[fn].output;
  const after = fn(input);
  assert(deepEqual(before, after), `${fn} 行为漂移`);
}
```

**方法 2：响应快照测试**（适用于 API 端点）
```bash
# 重构前
curl -s http://localhost:3000/api/users/user-1 > snapshot/user-1.json

# 重构后
curl -s http://localhost:3000/api/users/user-1 > current/user-1.json
diff snapshot/user-1.json current/user-1.json
# 无差异 = 行为一致
```

**方法 3：突变测试**（可选，适用于有 mutation-testing 工具的项目）
```bash
# Stryker Mutator (JS/TS)
npx stryker run

# 突变存活率 — 必须与 R2 基线相同或更好
```

### 步骤 5：生成重构报告（R5）

```markdown
# 重构报告
## 重构摘要
- 重构范围: src/services/user.ts → src/services/user/, auth/, profile/
- 变更文件数: 5
- 新增行: +340, 删除行: -280, 净增: +60
- 圈复杂度: 平均 15 → 6.2

## 覆盖率对比
- R2 基线: 行 85%, 分支 72%
- R4 最终: 行 86%, 分支 73%
- 结论: 覆盖率微增，无退化

## 行为漂移检测
- API 响应快照对比: 12/12 端点快照匹配
- 关键函数执行路径对比: 通过
- 结论: 未检测到行为漂移

## 架构改善
- 单一职责: UserService(40方法) → UserService(12) + AuthService(15) + ProfileService(10)
- 依赖关系: 循环依赖已消除
- 可测试性: 新模块均可隔离测试

## 后续建议
- 对 AuthService 添加更多边界测试
- ProfileService 仍可进一步提取数据访问逻辑
```

---

## 反模式

| 反模式 | 正确做法 |
|--------|---------|
| "这小重构不需要测试" | 无测试 = 无安全网 = 赌博 |
| 重构和加功能混在一个 PR | 分开！功能变更和结构调整绝不可混 |
| 重构时"顺便修个 Bug" | Bug 修复是独立任务，需要独立的测试和审查 |
| 不设基线就改代码 | 不知道重构前状态 = 无法判断是否退化 |
| 改动太大以至于测试全红 | 小步改，每步都保持测试绿 |
| 觉得代码难看就重构 | 切斯特顿之栏——不理解用途的代码不要碰 |

## 验证清单

- [ ] 重构边界文档已产出，含不变行为清单
- [ ] R2 基线测试全部通过
- [ ] R2 覆盖率已记录
- [ ] 重构后 R4 测试全部通过
- [ ] 覆盖率未下降（或下降有合理解释）
- [ ] 行为漂移检测通过
- [ ] 重构报告含变更摘要和架构改善说明
- [ ] 未修改边界外文件
- [ ] 重构 commit 不包含功能变更或 Bug 修复
