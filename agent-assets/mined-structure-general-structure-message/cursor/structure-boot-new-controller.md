---
description: |
triggers:
  - 新建 Controller
  - 新增接口
  - 写 API
  - 新增 Controller
  - new controller
  - add api
  - 新增 REST 接口
role: developer
priority: high
category: coding
stack: structure-boot
alwaysApply: false
---


# structure-boot 新建 Controller

> 在 interfaces 模块创建 REST Controller。**MUST 统一响应 + 异常处理**。

## 执行步骤

### 第 1 步：确认 Controller 类型

| 类型 | 路径 | 说明 |
|---|---|---|
| 内部 Controller | `controller/api/{X}Controller.java` | 前端 / 内部服务调用 |
| 开放 Controller | `controller/open/Open{X}Controller.java` | 第三方服务调用 |

### 第 2 步：生成内部 Controller

```java
package cn.structured.{X}.interfaces.controller.api;

import cn.structure.common.entity.ResResultVO;
import cn.structure.common.utils.ResultUtilSimpleImpl;
import cn.structure.common.vo.ResPage;
import cn.structure.common.vo.ReqPage;
import cn.structured.{X}.application.I{X}Service;
import cn.structured.{X}.common.dto.{X}DTO;
import cn.structured.{X}.common.query.{X}Query;
import cn.structured.{X}.common.vo.{X}VO;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.annotation.Resource;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

/**
 * {X}管理 Controller
 *
 * @author <author>
 * @version <version>
 * @since JDK 17 <date>
 */
@Tag(name = "{X}管理")
@RestController
@RequestMapping("/api/v1/{x}")
public class {X}Controller {

    @Resource
    private I{X}Service {x}Service;

    @Operation(summary = "根据 ID 查询{X}")
    @GetMapping("/{id}")
    public ResResultVO<{X}VO> findById(@PathVariable Long id) {
        return ResultUtilSimpleImpl.success({x}Service.findById(id));
    }

    @Operation(summary = "分页查询{X}")
    @GetMapping("/page")
    public ResResultVO<ResPage<{X}VO>> page({X}Query query, ReqPage reqPage) {
        return ResultUtilSimpleImpl.success({x}Service.page(query, reqPage));
    }

    @Operation(summary = "创建{X}")
    @PostMapping
    public ResResultVO<Long> create(@RequestBody @Valid {X}DTO dto) {
        return ResultUtilSimpleImpl.success({x}Service.create(dto));
    }

    @Operation(summary = "更新{X}")
    @PutMapping("/{id}")
    public ResResultVO<Void> update(@PathVariable Long id, @RequestBody @Valid {X}DTO dto) {
        {x}Service.update(dto);
        return ResultUtilSimpleImpl.success(null);
    }

    @Operation(summary = "删除{X}")
    @DeleteMapping("/{id}")
    public ResResultVO<Void> delete(@PathVariable Long id) {
        {x}Service.delete(id);
        return ResultUtilSimpleImpl.success(null);
    }
}
```

### 第 3 步：关键约束

| 约束 | 说明 |
|---|---|
| **包名** | `cn.structured.{X}.interfaces.controller.api` 或 `...open` |
| **命名** | `{X}Controller` / `Open{X}Controller` |
| **路径** | 内部 `/api/v1/{resources}`，开放 `/api/open/v1/{resources}` |
| **响应** | MUST `ResResultVO<T>` + `ResultUtilSimpleImpl` |
| **参数** | MUST `@Valid` 校验 |
| **禁止** | Controller 抛异常；注入 Mapper/Repository；直接返回 Entity/PO |

### 第 4 步：（可选）生成开放 Controller

```java
@Tag(name = "开放-{X}管理")
@RestController
@RequestMapping("/api/open/v1/{x}")
public class Open{X}Controller {
    // 类似，但路径前缀 /api/open/
}
```

## 产出物

- {X}Controller.java
- Open{X}Controller.java（可选）
- {X}ControllerTest.java

## 下一步

完成本技能后 MUST 按以下顺序继续：

1. **如还需配套组件** → 调用对应栈级 `new-*` 技能
2. **本层组件完成** → 调用 `unit-testing` 写测试
3. **全部代码完成** → 调用 `expert-review` 评审
4. **评审通过** → 调用 `ci-gate` 提交
5. **多人协作** → 调用 `gh-pr-workflow` 提 PR

**推荐下一技能**：`unit-testing`

## 关联

- 前置：`structure-boot-new-service`
- 相关：`structure-boot-new-repository`
- Wiki：`wiki/structure-boot/swagger.md`
