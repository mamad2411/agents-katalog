---
name: new-middleware
description: 根据 middleware.md 生成 Gin 认证中间件。
disable-model-invocation: true
argument-hint: <中间件名> 例如 {user_mw} 或 {sign_mw} 或 {admin_mw}
---

根据 `$ARGUMENTS` 生成认证中间件。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 特定内容如下。

## 第 0 步：拒绝规则与依赖前置

- ⛔ 拒绝（§A.1）：N/A（中间件通常不触发暂不实现模块）
- 状态检查（§A.2）：读 `BUILD_STATUS.md` §2 中 middleware 行
- 依赖（§A.3）：依赖的 helpers / Redis Key / 配置项必须就绪

## 第 1 步：读取设计文档（公共必读见 §B）

- 主文档：`docs/architecture/middleware.md` 对应中间件规格
- 额外必读：
  - `docs/architecture/routing.md` §1 中间件链
  - 签名类中间件 → `docs/architecture/{核心校验链}_flow.md` §1 签名算法
  - `docs/architecture/render_functions.md`（错误响应格式）

## 第 2 步：识别中间件类型

| 类型 | 关键逻辑 |
|------|---------|
| 内网 IP 白名单 | 检查 `ctx.ClientIP()` 是否属于内网段 |
| 签名校验 | MD5 / HMAC + 时间窗口校验 |
| 角色权限 | 提取 `X-{Actor}-Role` + 接口权限矩阵 |

## 第 3 步：生成中间件文件

文件路径：`middleware/{name}.go`

```go
package middleware

import (
    "{project}/components"
    "{project}/helpers"
    "{project}/pkg/gin"
    "{project}/pkg/golib/v2/tlog"
)

func {Name}() gin.HandlerFunc {
    return func(ctx *gin.Context) {
        // 1. {步骤 1}
        // 2. {步骤 2}
        // ...
        // N. ctx.Set("{key}", {value})
        ctx.Next()
    }
}
```

**错误响应处理（关键）**：

- 与外部协议对齐的路由组（Internal）→ `ctx.AbortWithStatusJSON(200, gin.H{"status":...,"message":...,"data":nil})`
- 标准内部路由组（UserSelf/Admin）→ `base.RenderJsonAbort(ctx, components.ErrorXxx)`
- 不要混用！

## 第 4 步：文档同步（公共项见 §C）

- 确认 `middleware.md` 规格与实现一致
- 确认 `routing.md` §1 中间件链描述一致
- 更新 BUILD_STATUS 状态

## 第 5 步：测试同步（4 类用例标准见 §D）

中间件本身不对应单接口测试，**必须**通过覆盖该路由组的下游接口测试间接覆盖：

| 中间件类型 | 测试覆盖 |
|----------|---------|
| 签名校验类 | `test/cases/internal/{module}_{action}_test.go`（含签名错误 / 时间过期 / 缺参数等） |
| 调用方身份注入类 | `test/cases/operator/common_test.go`（IP 白名单 / `{actor-id}` 注入） |
| 角色权限校验类 | `test/cases/admin/common_test.go`（多角色权限矩阵） |

## 第 6 步：验证（公共格式见 §E）

```bash
go build ./middleware/...
go vet ./middleware/...
cd test && go test -v ./cases/{scope}/...
```


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
