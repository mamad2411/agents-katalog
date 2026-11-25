---
name: new-service
description: 根据 service_design.md 的伪代码生成 Service 方法实现。自动选择错误类型、MySQL client 和双写模式。
disable-model-invocation: true
argument-hint: <service模块/方法名> 例如 {module-A}/{Method-1} 或 {module-B}/{Method-2}
---

根据 `$ARGUMENTS` 生成 Service 方法实现。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 特定内容如下。

## 第 0 步：拒绝规则与依赖前置

- ⛔ 拒绝（§A.1）：module 命中 `BUILD_STATUS.md` §0 中 🚫 模块时立即拒绝
- 状态检查（§A.2）：读 `BUILD_STATUS.md` §4 Service 层明细
- 依赖（§A.3）：
  - `components/constants.go` 不存在 → 先按 `constants.md` §10 生成
  - 如本 Skill 是核心校验类（auth 等）→ 检查 `service/{module}/cache_loaders.go` 是否就绪，否则先生成
  - 如本 Skill 是 Internal 业务上报类（需写 Kafka）→ 检查 `helpers/kafka_consumer.go` 是否就绪

## 第 1 步：读取设计文档（公共必读见 §B）

- 主文档：`docs/service/{module}_service.md` + `docs/service/service_design.md`
- 额外必读：`docs/schema/database_design.md`、`docs/cache/cache_design.md`

## 第 2 步：确定编码规则

### 错误类型选择

| 模块 | 错误类型 |
|------|---------|
| {特定方法集，详见 docs-spec/09 §5} | `*components.ServiceError`（业务状态码） |
| 其他 | `base.Error`（内部错误码） |

### MySQL Client 选择

按表所属库选择 `helpers.MysqlClient{Core/Trade/Log/CallLog}`。

### 双写模式

```go
// 1. 先写 MySQL
if err := helpers.MysqlClientCore.Model(&model).Updates(updates).Error; err != nil {
    return nil, components.ErrorDbUpdate.Wrap(err)
}
// 2. 写 Redis（失败不回滚，仅 WARN）
if err := helpers.{Project}CacheClient.HSet(ctx, key, ...); err != nil {
    tlog.WarnLogger(ctx, "redis write failed after mysql success",
        tlog.String("redisKey", key),
        tlog.String("error", err.Error()))
}
// 3. 清除本地缓存
helpers.{LocalCache1}.Delete(key)
```

## 第 3 步：生成 Service 文件

文件路径：`service/{module}/{module}.go`（核心校验类模块可拆分为 `{module}.go` + `checker.go`）

按 `{module}_service.md` 中的伪码精确实现。

## 第 4 步：文档同步（公共项见 §C）

- 确认 `{module}_service.md` 与实现一致；伪码需调整时同步更新 md
- 更新 BUILD_STATUS §4 状态

## 第 5 步：测试同步（4 类用例标准见 §D）

测试位置（按对外接口归属）：

| service 模块 | 测试位置 |
|-------------|---------|
| 核心校验类 | test/cases/internal/{module}_*_test.go |
| Internal 业务上报类（如 {module}.{Method-N}） | test/cases/internal/{module}_*_test.go 或 cases/operator/ |
| 其他业务模块 | test/cases/operator/ 或 cases/admin/ |
| 内部方法（无对外接口） | 同目录 `_test.go` 单元测试 |

```bash
cd test && go test -v ./cases/{scope}/... -run Test{Method}
```

## 第 6 步：验证（公共格式见 §E）

```bash
go build ./service/{module}/...
go vet ./service/{module}/...
```


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
