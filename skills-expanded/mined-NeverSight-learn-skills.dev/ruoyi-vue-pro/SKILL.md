---
name: ruoyi-vue-pro
description: 芋道源码 ruoyi-vue-pro 后端框架专家。适用于 Spring Boot 单体项目中的模块开发、Controller/Service/Mapper/DO/VO 编写、MyBatis Plus 数据访问、权限控制、多租户、数据权限、Excel 导出、定时任务等后端开发任务。
metadata:
  version: "1.0.0"
---

# 芋道 ruoyi-vue-pro

基于 **Spring Boot 2.7 + MyBatis Plus + Maven** 的 Java 单体后端脚手架（JDK 8+），提供完整的企业级管理后台功能模块。

## 项目结构

→ 详见 [ruoyi-dir](references/ruoyi-dir.md)

## 开发指南

| 主题 | 说明 | 参考 |
|------|------|------|
| 新增模块 CRUD | 创建 Controller、Service、Mapper、DO、VO 全套 | [ruoyi-crud](references/ruoyi-crud.md) |
| 新增 API 接口 | 编写 RESTful Controller 接口与 Swagger 文档 | [ruoyi-add-api](references/ruoyi-add-api.md) |
| 数据访问层 | MyBatis Plus BaseMapperX、LambdaQueryWrapperX 用法 | [ruoyi-mapper](references/ruoyi-mapper.md) |
| 权限与安全 | Spring Security + OAuth2 + 多租户 + 数据权限 | [ruoyi-security](references/ruoyi-security.md) |

## 关键约定

### 分层架构

每个业务模块（`yudao-module-xxx`）遵循严格分层：

```
controller/admin/       — 管理后台 RESTful 接口
controller/admin/vo/    — 请求/响应 VO（不暴露 DO）
controller/app/         — 用户端接口（可选）
service/                — Service 接口 + Impl 实现
dal/dataobject/         — MyBatis Plus DO（对应数据库表）
dal/mysql/              — Mapper 接口（继承 BaseMapperX）
convert/                — MapStruct 转换器（旧模块使用，新模块用 BeanUtils）
enums/                  — 模块内枚举与错误码
```

### 通用返回结构

所有接口返回 `CommonResult<T>`：

```java
@Data
public class CommonResult<T> {
    private Integer code;   // 0 表示成功
    private String msg;     // 错误提示
    private T data;         // 返回数据
}
```

- 成功：`return success(data)` — 静态导入 `CommonResult.success`
- 分页：`return success(new PageResult<>(list, total))`

### 实体基类

所有 DO 继承 `BaseDO`（自动填充 `createTime`、`updateTime`、`creator`、`updater`、`deleted`）。

多租户 DO 继承 `TenantBaseDO`（额外自动填充 `tenantId`）。

```java
@TableName("system_xxx")
@KeySequence("system_xxx_seq")
@Data
@EqualsAndHashCode(callSuper = true)
public class XxxDO extends TenantBaseDO {
    @TableId
    private Long id;
    // 业务字段...
}
```

### VO 规范

- **SaveReqVO** — 创建和更新共用（`id` 可选，创建时为 null）
- **RespVO** — 查询响应
- **PageReqVO** 继承 `PageParam` — 分页查询参数
- **SimpleRespVO** — 精简响应（下拉选项等）
- 使用 `@Schema` 注解生成 Swagger 文档
- 使用 `@NotBlank`、`@NotNull`、`@Size`、`@Email` 等 JSR 380 校验

### Controller 约定

```java
@Tag(name = "管理后台 - 部门")
@RestController
@RequestMapping("/system/dept")
@Validated
public class DeptController {

    @Resource
    private DeptService deptService;

    @PostMapping("create")
    @Operation(summary = "创建部门")
    @PreAuthorize("@ss.hasPermission('system:dept:create')")
    public CommonResult<Long> createDept(@Valid @RequestBody DeptSaveReqVO createReqVO) {
        return success(deptService.createDept(createReqVO));
    }

    @PutMapping("update")
    @Operation(summary = "更新部门")
    @PreAuthorize("@ss.hasPermission('system:dept:update')")
    public CommonResult<Boolean> updateDept(@Valid @RequestBody DeptSaveReqVO updateReqVO) {
        deptService.updateDept(updateReqVO);
        return success(true);
    }

    @DeleteMapping("delete")
    @Operation(summary = "删除部门")
    @PreAuthorize("@ss.hasPermission('system:dept:delete')")
    public CommonResult<Boolean> deleteDept(@RequestParam("id") Long id) {
        deptService.deleteDept(id);
        return success(true);
    }

    @GetMapping("/page")
    @Operation(summary = "获取部门分页")
    @PreAuthorize("@ss.hasPermission('system:dept:query')")
    public CommonResult<PageResult<DeptRespVO>> getDeptPage(@Valid DeptPageReqVO pageVO) {
        PageResult<DeptDO> pageResult = deptService.getDeptPage(pageVO);
        return success(BeanUtils.toBean(pageResult, DeptRespVO.class));
    }
}
```

### Mapper 约定

所有 Mapper 继承 `BaseMapperX<T>`（扩展自 MyBatis Plus `BaseMapper` + `MPJBaseMapper`）：

```java
@Mapper
public interface DeptMapper extends BaseMapperX<DeptDO> {

    default List<DeptDO> selectList(DeptListReqVO reqVO) {
        return selectList(new LambdaQueryWrapperX<DeptDO>()
                .likeIfPresent(DeptDO::getName, reqVO.getName())
                .eqIfPresent(DeptDO::getStatus, reqVO.getStatus()));
    }

    default PageResult<DeptDO> selectPage(DeptPageReqVO reqVO) {
        return selectPage(reqVO, new LambdaQueryWrapperX<DeptDO>()
                .likeIfPresent(DeptDO::getName, reqVO.getName())
                .eqIfPresent(DeptDO::getStatus, reqVO.getStatus())
                .orderByDesc(DeptDO::getId));
    }
}
```

`BaseMapperX` 提供的便捷方法：
- `selectPage(PageParam, Wrapper)` — 分页查询，返回 `PageResult<T>`
- `selectOne(SFunction, Object)` — 按字段查单条
- `selectList(SFunction, Object)` — 按字段查列表
- `selectCount(SFunction, Object)` — 按字段计数
- `insertBatch(Collection)` — 批量插入
- `updateBatch(Collection)` — 批量更新
- `delete(SFunction, Object)` — 按字段删除

`LambdaQueryWrapperX` 提供 `xxxIfPresent` 方法（值为空时自动跳过条件）。

### Service 约定

```java
public interface DeptService {
    Long createDept(DeptSaveReqVO createReqVO);
    void updateDept(DeptSaveReqVO updateReqVO);
    void deleteDept(Long id);
    DeptDO getDept(Long id);
    PageResult<DeptDO> getDeptPage(DeptPageReqVO reqVO);
}
```

实现类使用 `@Service` + `@Validated`，依赖通过 `@Resource` 注入。

VO → DO 转换使用 `BeanUtils.toBean(source, targetClass)` 工具方法。

抛出业务异常使用 `ServiceExceptionUtil.exception(ErrorCode)`。

### 权限控制

- `@PreAuthorize("@ss.hasPermission('module:resource:action')")` — 细粒度权限
- 权限编码格式：`模块:资源:操作`（如 `system:dept:create`）
- 错误码定义在各模块 `enums/ErrorCodeConstants` 中

### 依赖管理

- 所有版本统一在 `yudao-dependencies/pom.xml` 中通过 BOM 管理
- 模块引用框架组件：`yudao-spring-boot-starter-xxx`（不指定 version）

### 错误码范围

```
模块          错误码范围
system       1-002-000-000 ~ 1-002-999-999
infra        1-001-000-000 ~ 1-001-999-999
member       1-004-000-000 ~ 1-004-999-999
pay          1-007-000-000 ~ 1-007-999-999
...更多见 ServiceErrorCodeRange
```

## 框架组件参考

| 组件 | 路径 | 用途 |
|------|------|------|
| `yudao-common` | `yudao-framework/yudao-common` | CommonResult、PageParam、PageResult、BaseDO、异常体系 |
| `yudao-spring-boot-starter-mybatis` | `yudao-framework/...` | BaseMapperX、LambdaQueryWrapperX、BaseDO |
| `yudao-spring-boot-starter-security` | `yudao-framework/...` | Spring Security + OAuth2 + 操作日志 |
| `yudao-spring-boot-starter-web` | `yudao-framework/...` | API 访问日志、脱敏、数据验证 |
| `yudao-spring-boot-starter-biz-tenant` | `yudao-framework/...` | SaaS 多租户支持 |
| `yudao-spring-boot-starter-biz-data-permission` | `yudao-framework/...` | 行级数据权限 |
| `yudao-spring-boot-starter-excel` | `yudao-framework/...` | EasyExcel 导入导出 |
| `yudao-spring-boot-starter-job` | `yudao-framework/...` | 定时任务 |
| `yudao-spring-boot-starter-mq` | `yudao-framework/...` | 消息队列 |
| `yudao-spring-boot-starter-redis` | `yudao-framework/...` | Redis 缓存 |

## 业务模块

| 模块 | 路径 | 功能 |
|------|------|------|
| `yudao-module-system` | 核心 | 用户、角色、菜单、部门、字典、租户、OAuth2 |
| `yudao-module-infra` | 核心 | 代码生成、文件管理、配置中心、API 日志 |
| `yudao-module-bpm` | 扩展 | 工作流（Flowable） |
| `yudao-module-pay` | 扩展 | 支付（微信/支付宝） |
| `yudao-module-mall` | 扩展 | 电商（商品/订单/营销） |
| `yudao-module-crm` | 扩展 | 客户关系管理 |
| `yudao-module-erp` | 扩展 | 进销存 |
| `yudao-module-mp` | 扩展 | 微信公众号 |
| `yudao-module-ai` | 扩展 | AI 大模型集成 |
| `yudao-module-iot` | 扩展 | 物联网 |

## 常用命令

```bash
# 编译全部
mvn clean install -DskipTests

# 启动服务
cd yudao-server && mvn spring-boot:run

# 仅编译某模块
mvn clean install -pl yudao-module-system -am -DskipTests
```
