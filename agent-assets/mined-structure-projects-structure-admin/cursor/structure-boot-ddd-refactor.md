---
description: |
triggers:
  - DDD 重构
  - 模块拆分
  - 迁移到 DDD
  - 重构
  - refactor
  - ddd refactor
role: architect
priority: high
category: architecture
stack: structure-boot
alwaysApply: false
---


# structure-boot DDD 重构

> 将老项目 4 模块 + Manager 模式迁移到 DDD 7+1 + RepositoryFacade + Delegate 模式。
> **MUST 渐进式迁移，禁止一次性大爆炸重构**。

## 前置条件

- 老项目已通过 `legacy-onboarding` 接入（`audit-report.md` 存在）
- 变更提案已创建（`changes/proposals/<current>/proposal.md`）

## 执行步骤

### 第 1 步：分析现有模块结构

扫描老项目 4 模块结构（api / service / dao / common）：

```bash
# 扫描模块
find . -name "pom.xml" -maxdepth 2 | sort

# 扫描 Manager 模式
grep -rn "class.*Manager" --include="*.java" | head -20

# 扫描 Service 直接注入 Mapper
grep -rn "@Autowired.*Mapper\|@Resource.*Mapper" --include="*.java" | head -20

# 扫描 PO 跨层传递
grep -rn "class.*Controller" --include="*.java" -A 5 | grep "PO"
```

**产出**：现有架构清单（模块 / Manager / Service / DAO / PO 清单）

### 第 2 步：建立模块映射表

| 老模块 | 新模块（DDD 7+1） | 说明 |
|---|---|---|
| `common` | `common` | DTO / VO / Query / enums / exception（保留） |
| `service` | `application` | I{X}Service / {X}ServiceImpl / {X}Assembler |
| `dao` | `infrastructure` + `repository-mybatis` | RepositoryImpl / Delegate / PO / Mapper |
| `api` | `interfaces` | Controller（api/ + open/） |
| —（新增） | `domain` | Entity / Repository 接口 / DomainService |
| —（新增） | `boot` / `start` | 启动类 + application.yaml |

**产出**：模块迁移映射表（写入 `changes/proposals/<current>/design.md`）

### 第 3 步：迁移 Service → application

```java
// 老：service 模块
public class {X}ServiceImpl {
    @Autowired private {X}Manager manager;  // 禁止
    @Autowired private {X}Mapper mapper;     // 禁止
}

// 新：application 模块
public class {X}ServiceImpl implements I{X}Service {
    private final {X}Repository repository;  // MUST 注入 Repository
    // ...
}
```

**约束**：
- MUST 拆分为 `I{X}Service`（接口）+ `{X}ServiceImpl`（实现）
- MUST 注入 `Repository`，禁止注入 `Manager` / `Mapper`
- MUST 用 `{X}Assembler` 做 Entity ↔ DTO 转换

### 第 4 步：迁移 Manager/DAO → RepositoryFacade + RepositoryImpl

```java
// 老：Manager 模式（禁止）
public class {X}Manager {
    @Autowired private {X}Mapper mapper;
    public {X}PO findById(Long id) { return mapper.selectById(id); }
}

// 新：RepositoryFacade + Delegate 模式
// domain 模块：Repository 接口
public interface {X}Repository {
    Optional<{X}Entity> findById(Long id);
}

// infra 模块：RepositoryImpl
public class {X}RepositoryImpl
        extends RepositoryFacade<{X}Entity, Long, {X}RepositoryDelegate>
        implements {X}Repository {
}

// repository-mybatis 模块：MybatisPlusDelegate
public class {X}MybatisPlusDelegate
        extends MybatisPlusRepositoryDelegate<{X}Entity, {X}PO, Long>
        implements {X}RepositoryDelegate {
    @Override
    protected {X}Entity toEntity({X}PO po) { /* MUST 显式实现 */ }
    @Override
    protected {X}PO toPo({X}Entity entity) { /* MUST 显式实现 */ }
}
```

**约束**：
- MUST 用 `RepositoryFacade + Delegate` 模式
- MUST 手写 `toEntity` / `toPo`，不依赖框架自动转换
- 禁止 `Manager` 模式 / Service 直接注入 Mapper

### 第 5 步：迁移 PO/Entity 分离

```java
// 老：PO 跨层传递（禁止）
// Controller 直接返回 PO，Service 直接操作 PO

// 新：PO 留 infrastructure，Entity 入 domain
// domain/entity/{X}Entity.java —— 无持久化注解
// repository-mybatis/po/{X}PO.java —— 含 @TableName/@TableId/@TableLogic
```

**约束**：
- Entity 在 `domain`（无 `@TableId` / `@TableLogic` 等持久化注解）
- PO 在 `repository-mybatis`（含 MyBatis-Plus 注解）
- 禁止 PO 跨层传递（Service / Controller MUST 用 Entity / DTO / VO）

### 第 6 步：迁移事件（EventManager.publish + StreamEvent）

```java
// 老：直接调用 / 无事件
{x}Service.create(dto);
otherService.notify();  // 强耦合

// 新：领域事件解耦
EventManager.publish(new {X}CreatedEvent(entity));
// 其他模块订阅 StreamEvent
```

**约束**：
- MUST 用 `EventManager.publish` + `StreamEvent` 解耦
- 跨模块通信优先用领域事件，禁止直接调用其他模块 Service

### 第 7 步：验证

```bash
# 编译
mvn clean package -DskipTests

# 单测
mvn test

# 冒烟测试
mvn spring-boot:run  # 启动验证
# 调用核心接口验证
```

**验证标准**：
- 编译通过
- 单测全部通过
- 冒烟测试核心接口正常
- 无 Manager / 直接注入 Mapper / PO 跨层传递

## 产出物

- 重构计划（`changes/proposals/<current>/design.md`）
- 模块迁移映射表
- 代码变更（按模块提交，渐进式）

## 下一步

完成本技能后 MUST 按以下顺序继续：

1. **逐模块迁移完成** → 调用 `unit-testing` 补测试
2. **全部迁移完成** → 调用 `expert-review` 评审
3. **评审通过** → 调用 `ci-gate` 提交
4. **多人协作** → 调用 `gh-pr-workflow` 提 PR

**推荐下一技能**：`unit-testing`

## 关联

- 前置：`legacy-onboarding`
- 相关：`structure-boot-new-entity` / `structure-boot-new-repository` / `structure-boot-new-service`
- Wiki：`wiki/structure-boot/architect.md` `wiki/structure-boot/ddd-patterns.md` `wiki/structure-boot/legacy-migration.md`
