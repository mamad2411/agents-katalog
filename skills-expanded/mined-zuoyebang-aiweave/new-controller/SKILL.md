---
name: new-controller
description: 根据 API 接口文档生成 Controller handler 文件。自动区分多种响应模式（Internal vs UserSelf/Admin）。
disable-model-invocation: true
argument-hint: <路由组/模块/接口> 例如 internal/{module}/{action} 或 operator/{module}/{action}
---

根据 `$ARGUMENTS` 生成 Controller handler 文件。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 特定内容如下。

## 第 0 步：拒绝规则与依赖前置

- ⛔ 拒绝（§A.1）：路径命中 `BUILD_STATUS.md` §0 中 🚫 模块路径（如 `admin/{disabled-module}/*`）时立即拒绝
- 状态检查（§A.2）：读 `BUILD_STATUS.md` §5 路由组状态
- 依赖（§A.3）：
  - 对应 service 未实现 → 先调 `/new-service` 生成
  - Internal 路由组首次生成时，先检查共享文件：`controllers/http/internal/render.go`（renderInternalResponse）+ `validator.go`，缺失则按 `docs/architecture/render_functions.md` 生成

## 第 1 步：读取设计文档（公共必读见 §B）

- 主文档：`docs/api/{audience}_interfaces.md`
- 额外必读：`docs/architecture/routing.md` §4、`docs/service/service_design.md`（确认 service 方法签名）

## 第 2 步：选择响应模板

### Internal 控制器模板（与外部协议对齐的响应格式）

```go
package {module}

import (
    "{project}/components"
    "{project}/pkg/gin"
    "{project}/service/{service_module}"
)

type {Action}Req struct {
    Field1 string `json:"field1" binding:"required,max=64"`
}

var {svcVar} = &{service_module}.{Service}Service{}

func {Action}(ctx *gin.Context) {
    var req {Action}Req
    if err := ctx.ShouldBindJSON(&req); err != nil {
        renderInternalResponse(ctx, components.NewServiceError({N}, "请求参数错误"), nil)
        return
    }
    resp, err := {svcVar}.{Method}(ctx, &req)
    renderInternalResponse(ctx, err, resp)
}
```

### UserSelf / Admin 控制器模板（标准 errNo/errStr 响应格式）

```go
package {module}

import (
    "{project}/components"
    "{project}/pkg/gin"
    "{project}/pkg/golib/v2/base"
    "{project}/service/{service_module}"
)

type {Action}Req struct {
    Field1 string `json:"field1" binding:"required,max=64"`
}

var {svcVar} = &{service_module}.{Service}Service{}

func {Action}(ctx *gin.Context) {
    var req {Action}Req
    if err := ctx.ShouldBindJSON(&req); err != nil {  // GET 用 ShouldBindQuery
        base.RenderJsonFail(ctx, components.ErrorParamInvalid)
        return
    }
    resp, err := {svcVar}.{Method}(ctx, &req)
    if err != nil {
        base.RenderJsonFail(ctx, err)
        return
    }
    base.RenderJsonSucc(ctx, resp)
}
```

## 第 3 步：生成 Controller 文件

文件路径：`controllers/http/{audience}/{module}/{action}.go`

**关键规范**：Controller 不写业务逻辑；POST 用 `ShouldBindJSON`，GET 用 `ShouldBindQuery`；请求 struct 在 controller 文件中（含 binding tag）；调用方身份字段（如 `{actor-id}`）从 ctx 提取：`ctx.GetString("{actor-id}")`。

## 第 4 步：文档同步（公共项见 §C）

- 确认 `api/{audience}_interfaces.md` 接口规格完整
- 确认 `routing.md` §5 路由表已含此接口（否则提示先 `/new-router`）
- 更新 BUILD_STATUS §5 状态

## 第 5 步：测试同步（4 类用例标准见 §D）

测试位置：`test/cases/{audience}/{module}_{action}_test.go`

```bash
cd test && go test -v ./cases/{audience}/... -run Test{Action}
```

## 第 6 步：验证（公共格式见 §E）

```bash
go build ./controllers/http/{audience}/{module}/...
go vet ./controllers/http/{audience}/{module}/...
```


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
