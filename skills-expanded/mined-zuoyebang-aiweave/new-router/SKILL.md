---
name: new-router
description: 根据 routing.md 生成路由注册文件（http.go 主入口 + http_{audience}.go 子文件）。
disable-model-invocation: true
argument-hint: <路由组> 例如 operator 或 internal 或 admin 或 all
---

根据 `$ARGUMENTS` 生成路由注册文件。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 特定内容如下。

## 第 0 步：拒绝规则与依赖前置

- ⛔ 拒绝（§A.1）：生成 admin 路由组时**必须跳过** `BUILD_STATUS.md` §0 中 🚫 模块对应路由（即使 `routing.md` §5 表中列出也不能注册，可以注释占位 + 标注 "🚫 ..."）
- 状态检查（§A.2）：读 `BUILD_STATUS.md` §2 router 行
- 依赖（§A.3）：扫描 `controllers/http/{audience}/` 下文件，缺失的 controller 先列清单提醒用户

## 第 1 步：读取设计文档（公共必读见 §B）

- 主文档：`docs/architecture/routing.md` §3（注册代码）+ §5（完整路由表）
- 确认每条路由的：HTTP 方法 / 路径 / 控制器函数 / 校验中间件
- 确认包导入别名约定（§4）

## 第 2 步：生成路由文件

### http.go 主入口

```go
package router

import (
    "{project}/controllers/http/probe"
    "{project}/middleware"
    "{project}/pkg/gin"
)

func Http(engine *gin.Engine) {
    engine.Use(middleware.Cors)
    engine.Use(middleware.Metrics)

    engine.GET("/{prefix}/ready", probe.Ready)

    registerInternalRoutes(engine)
    registerOperatorRoutes(engine)
    registerAdminRoutes(engine)
}
```

### http_{audience}.go 子文件

按 routing.md §3.2 代码结构生成，例：

```go
func registerOperatorRoutes(engine *gin.Engine) {
    op := engine.Group("/{prefix}/operator")

    // 免校验
    op.POST("/{module}/{action}", {audience}_{module}.{Action})

    // 需校验
    protected := op.Group("")
    protected.Use(middleware.{UserMw}())
    {
        registerOperator{Module}Routes(protected)
    }
}
```

## 第 3 步：文档同步（公共项见 §C）

- 确认 `routing.md` §5 路由表与代码完全一致（含 🚫 跳过项注释）
- 更新 BUILD_STATUS §2 router 行

## 第 4 步：测试同步（4 类用例标准见 §D）

路由是连接层，测试通过下游接口用例间接覆盖：

```bash
cd test && go test -v ./cases/{audience}/...
```

如生成 admin 组：必须验证 `cases/admin/{disabled-module}_blocked_test.go` smoke 用例（验证 `/admin/{disabled-module}/*` 返回 404）。

## 第 5 步：验证（公共格式见 §E）

```bash
go build ./router/...
go vet ./router/...
```


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
