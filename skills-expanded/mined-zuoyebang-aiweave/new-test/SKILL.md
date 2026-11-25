---
name: new-test
description: 为指定接口生成 test/cases/ 下的接口级测试文件。基于 API 文档 + seed 数据生成 4 类用例骨架。
disable-model-invocation: true
argument-hint: <路由组/模块/接口> 例如 internal/{module}/{action} 或 operator/{module}/{action}
---

为 `$ARGUMENTS` 生成 `test/cases/` 下的接口级测试文件。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 特定内容如下。
>
> **职责**：补齐遗漏的测试。正常流程下，`/new-service` / `/new-controller` 在生成业务代码时就应同步测试。本 Skill 仅在发现某接口代码已有但测试缺失时使用。

## 第 0 步：拒绝规则与依赖前置

- ⛔ 拒绝（§A.1）：接口路径命中 `BUILD_STATUS.md` §0 中 🚫 模块时立即拒绝
- 状态检查（§A.2）：读 `BUILD_STATUS.md` §5 → handler 必须已实现（🟢）；未实现 → 停止，提示先 `/new-controller`
- 依赖（§A.3）：
  - 读 `docs/testing/testing_design.md` §4 确认框架 API 签名
  - 读 `test/fixtures/seed/README.md` 熟悉 seed 数据

## 第 1 步：读取设计文档（公共必读见 §B）

- 主文档：`docs/api/{audience}_interfaces.md`
- 提取：请求参数 / 响应结构 / 校验规则 / 错误码映射

## 第 2 步：生成测试文件

文件路径：`test/cases/{audience}/{module}_{action}_test.go`

按 §D 的 4 类用例模板生成（每类至少 1 个 sub test）：

```go
package {audience}_test

import (
    "testing"
    "{project}/test/framework"
)

func Test{Action}_Succ(t *testing.T) {
    body := map[string]interface{}{ /* 合法参数 */ }
    resp := framework.{Audience}Post(t, "{path}", {auth}, body)
    framework.AssertSucc(t, resp)
    framework.AssertJSONField(t, resp.{Audience}.Data, "xxx", "expected")
}

func Test{Action}_MissingXxx_Expected{Code}(t *testing.T) {
    body := map[string]interface{}{ /* 缺字段 */ }
    resp := framework.{Audience}Post(t, "{path}", {auth}, body)
    framework.AssertFail(t, resp, {errCode})
}

func Test{Action}_{Module}Disabled_Expected{Code}(t *testing.T) {
    // seed 中状态为禁用的 {核心实体}
    resp := framework.{Audience}Post(t, "{path}", {edge case auth}, body)
    framework.AssertFail(t, resp, {errCode})
}

func Test{Action}_WritesMysqlAndRedis(t *testing.T) {
    resp := framework.{Audience}Post(t, "{path}", {auth}, body)
    framework.AssertSucc(t, resp)
    framework.AssertMysqlExists(t, "{example_db}", "{example_table}", "field = ?", value)
    framework.AssertRedisHashField(t, "{ns}:info:"+entityId, "status", "1")
}
```

## 第 3 步：接入 TestMain

每个 `cases/{audience}/` 子包应有 `common_test.go` 提供 `TestMain`。新增测试文件不重复写。如是新路由组的第一个文件，先创建：

```go
package {audience}_test

import (
    "os"
    "testing"
    "{project}/test/framework"
)

func TestMain(m *testing.M) {
    code := framework.RunTests(m)
    os.Exit(code)
}
```

## 第 4 步：文档同步（公共项见 §C）

- 确认 BUILD_STATUS §9.5 对应行标 🟢
- seed 不足以支持某用例 → 在 `test/fixtures/seed/*.sql` 补 + 同步 `test/fixtures/seed/README.md`

## 第 5 步：验证（公共格式见 §E）

```bash
cd test
go build ./cases/{audience}/...
go vet ./cases/{audience}/...
go test -v ./cases/{audience}/... -run Test{Action}
```

测试红了：
- 检查 seed 数据是否匹配
- 检查业务代码是否有 bug（**报告给用户而非改测试迎合 bug**）
- 检查断言是否正确


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
