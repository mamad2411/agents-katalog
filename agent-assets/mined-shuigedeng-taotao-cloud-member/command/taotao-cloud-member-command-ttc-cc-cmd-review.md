---
description: DDD 代码审查 — 检查领域模型、架构合规、代码质量
parameters:
  - name: scope
    type: string
    description: 审查范围（controller/service/domain/all）
    default: all
---

# DDD 代码审查

## 审查维度

### 1. 领域模型合规
- [ ] 聚合根是否维护了内部不变量（业务规则在聚合内，而非在 Service）
- [ ] 值对象是否不可变（final 字段、无 setter、构造时自验证）
- [ ] 跨聚合是否通过 ID 引用而非对象引用
- [ ] 领域事件是否在聚合内 `registerEvent()`，仓储 `save()` 时发布

### 2. 架构合规
- [ ] 依赖方向正确：`interfaces → application → domain ← infrastructure`
- [ ] 事务边界是否仅开在 `application/service/` 层
- [ ] Controller 是否不含业务逻辑（仅参数校验 + 响应封装）
- [ ] Application Service 是否不包含业务规则判断（仅编排）

### 3. 项目特定禁止项
- [ ] 聚合根中注入 Repository 或 Domain Service
- [ ] Controller 中直接调用 Repository
- [ ] Application Service 中包含业务规则判断
- [ ] domain 层出现 Spring 注解或持久化操作

### 4. 代码风格
- [ ] 包路径是否符合 `com.taotao.cloud.member.{module}`
- [ ] 命名是否符合项目约定（Agg 后缀、Val 后缀、Command/Query）

## 输出格式
```markdown
## 代码审查报告

### 严重问题（必须修复）
- [文件:行号] 问题描述 + 修复建议

### 警告（建议修复）
- [文件:行号] 问题描述 + 优化方案

### 优化建议
- 建议内容
```
