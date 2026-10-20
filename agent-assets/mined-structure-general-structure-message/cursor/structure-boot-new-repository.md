---
description: |
triggers:
  - 新建 Repository
  - 新增仓储
  - 写数据访问层
  - 新增 Repository
  - new repository
  - add repository
  - 新建 Mapper
role: developer
priority: high
category: coding
stack: structure-boot
alwaysApply: false
---


# structure-boot 新建 Repository

> 按 **RepositoryFacade + Delegate** 模式创建仓储层。**MUST 区分 Entity / PO**。

## 执行步骤

### 第 1 步：生成领域接口（domain 模块）

```java
package cn.structured.{X}.domain.repository;

import cn.structured.{X}.domain.entity.{X}Entity;
import java.util.Optional;

/**
 * {X}仓储接口
 */
public interface {X}Repository {

    Optional<{X}Entity> findById(Long id);

    {X}Entity save({X}Entity entity);

    void deleteById(Long id);

    // ... 其他业务方法
}
```

### 第 2 步：生成 RepositoryImpl（infra 模块）

```java
package cn.structured.{X}.infra.repository;

import cn.structure.infra.repository.RepositoryFacade;
import cn.structured.{X}.domain.entity.{X}Entity;
import cn.structured.{X}.domain.repository.{X}Repository;
import cn.structured.{X}.infra.repository.delegate.{X}RepositoryDelegate;
import org.springframework.stereotype.Component;

/**
 * {X}仓储实现
 */
@Component("{x}Repository")
public class {X}RepositoryImpl
        extends RepositoryFacade<{X}Entity, Long, {X}RepositoryDelegate>
        implements {X}Repository {

    // 继承 baseMapper / 通用方法通过 getDelegate() 调用
}
```

### 第 3 步：生成 RepositoryDelegate 接口（infra 模块）

```java
package cn.structured.{X}.infra.repository.delegate;

/**
 * {X}仓储 Delegate 接口（业务侧）
 */
public interface {X}RepositoryDelegate {
    // 业务方法
}
```

### 第 4 步：生成 MybatisPlusDelegate（repository-mybatis 模块）

```java
package cn.structured.{X}.repository.repository;

import cn.structure.infra.repository.mybatis.MybatisPlusRepositoryDelegate;
import cn.structured.{X}.domain.entity.{X}Entity;
import cn.structured.{X}.infra.repository.delegate.{X}RepositoryDelegate;
import cn.structured.{X}.repository.po.{X}PO;
import cn.structured.{X}.repository.mapper.{X}Mapper;
import org.springframework.stereotype.Component;

/**
 * {X} MyBatis-Plus Delegate
 */
@Component
public class {X}MybatisPlusDelegate
        extends MybatisPlusRepositoryDelegate<{X}Entity, {X}PO, Long>
        implements {X}RepositoryDelegate {

    @Override
    protected {X}Entity toEntity({X}PO po) {
        // MUST 显式实现
        if (po == null) return null;
        {X}Entity entity = new {X}Entity();
        // ... 字段映射
        return entity;
    }

    @Override
    protected {X}PO toPo({X}Entity entity) {
        // MUST 显式实现
        if (entity == null) return null;
        {X}PO po = new {X}PO();
        // ... 字段映射
        return po;
    }
}
```

### 第 5 步：关键约束

| 约束 | 说明 |
|---|---|
| **包路径异常** | `repository-mybatis` 模块实际包是 `cn.structured.{X}.repository.repository.*`（**双 repository**，历史遗留） |
| **toEntity / toPo** | MUST 显式重写，**不依赖框架自动转换** |
| **Entity vs PO** | Entity 在 domain（无持久化注解），PO 在 repository-mybatis（含 MyBatis-Plus 注解） |
| **禁止** | Service / Controller 注入 Mapper 或 PO |

## 产出物

- {X}Repository.java
- {X}RepositoryImpl.java
- {X}RepositoryDelegate.java
- {X}MybatisPlusDelegate.java
- {X}PO.java
- {X}Mapper.java

## 下一步

完成本技能后 MUST 按以下顺序继续：

1. **如还需配套组件** → 调用对应栈级 `new-*` 技能
2. **本层组件完成** → 调用 `unit-testing` 写测试
3. **全部代码完成** → 调用 `expert-review` 评审
4. **评审通过** → 调用 `ci-gate` 提交
5. **多人协作** → 调用 `gh-pr-workflow` 提 PR

**推荐下一技能**：`structure-boot-new-service`

## 关联

- 前置：`model-design`
- 相关：`structure-boot-new-service` / `structure-boot-new-entity`
- Wiki：`wiki/structure-boot/components.md`
