---
description: |
triggers:
  - 新建 Service
  - 新增 Service
  - 写 Service
  - 新增业务服务
  - 写业务逻辑
  - new service
  - add service
role: developer
priority: high
category: coding
stack: structure-boot
alwaysApply: false
---


# structure-boot 新建 Service

> 在 application 模块创建 Service 接口 + 实现类。**MUST 遵守 structure-boot 生态约束**。

## 前置条件

- 变更提案存在
- 已识别为 structure-boot 项目

## 执行步骤

### 第 1 步：确认 Service 位置

- 接口：`structure-{X}-application/src/main/java/cn/structured/{X}/application/I{X}Service.java`
- 实现：`structure-{X}-application/src/main/java/cn/structured/{X}/application/{X}ServiceImpl.java`

### 第 2 步：生成 Service 接口

```java
package cn.structured.{X}.application;

import cn.structure.common.vo.ResPage;
import cn.structure.common.vo.ReqPage;
import cn.structured.{X}.common.dto.{X}DTO;
import cn.structured.{X}.common.query.{X}Query;
import cn.structured.{X}.common.vo.{X}VO;

/**
 * {X}服务接口
 *
 * @author <author>
 * @version <version>
 * @since JDK 17 <date>
 */
public interface I{X}Service {

    /**
     * 根据 ID 查询
     */
    {X}VO findById(Long id);

    /**
     * 分页查询
     */
    ResPage<{X}VO> page({X}Query query, ReqPage reqPage);

    /**
     * 创建
     */
    Long create({X}DTO dto);

    /**
     * 更新
     */
    void update({X}DTO dto);

    /**
     * 删除
     */
    void delete(Long id);
}
```

### 第 3 步：生成 ServiceImpl

```java
package cn.structured.{X}.application;

import cn.structure.common.utils.ResultUtilSimpleImpl;
import cn.structured.{X}.domain.repository.{X}Repository;
import cn.structured.{X}.common.exception.{X}ExceptionEnum;
import cn.structure.common.exception.CommonException;
import jakarta.annotation.Resource;
import org.springframework.stereotype.Service;

/**
 * {X}服务实现
 *
 * @author <author>
 * @version <version>
 * @since JDK 17 <date>
 */
@Service
public class {X}ServiceImpl implements I{X}Service {

    @Resource
    private {X}Repository {x}Repository;

    @Override
    public {X}VO findById(Long id) {
        // 调用 Repository 层
        return {x}Repository.findById(id)
            .map({X}Assembler::toVO)
            .orElseThrow(() -> new CommonException({X}ExceptionEnum.{X}_NOT_FOUND));
    }

    // ... 其他方法实现
}
```

### 第 4 步：关键约束（MUST 遵守）

| 约束 | 说明 |
|---|---|
| **包名** | `cn.structured.{X}.application`（**有 d**） |
| **命名** | 接口 `I{X}Service`，实现 `{X}ServiceImpl` |
| **DI** | MUST `@Resource`（**不用 @Autowired**） |
| **异常** | MUST `CommonException` + `{X}ExceptionEnum` |
| **禁止** | 注入 `Mapper` / `PO`；写 SQL |
| **依赖方向** | Service → Repository（接口）→ RepositoryImpl |

### 第 5 步：生成单元测试

```java
@ExtendWith(MockitoExtension.class)
class {X}ServiceImplTest {
    // ...
}
```

## 产出物

- I{X}Service.java
- {X}ServiceImpl.java
- {X}ServiceImplTest.java

## 下一步

完成本技能后 MUST 按以下顺序继续：

1. **如还需配套组件** → 调用对应栈级 `new-*` 技能
2. **本层组件完成** → 调用 `unit-testing` 写测试
3. **全部代码完成** → 调用 `expert-review` 评审
4. **评审通过** → 调用 `ci-gate` 提交
5. **多人协作** → 调用 `gh-pr-workflow` 提 PR

**推荐下一技能**：`structure-boot-new-controller`

## 关联

- 前置：`coding`（含 requirement-analysis）
- 相关：`structure-boot-new-controller` / `structure-boot-new-repository`
- Wiki：`wiki/structure-boot/developer.md`
