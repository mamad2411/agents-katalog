---
name: rebuild-from-docs
description: 从 docs/ 文档重建指定模块的代码。这是 AI 原生工程的终极能力：仅凭文档即可重建整个系统。
disable-model-invocation: true
argument-hint: <模块> 例如 middleware 或 service/{module} 或 controllers/http/internal 或 router 或 all
---

从 `docs/` 文档重建 `$ARGUMENTS` 指定模块的代码。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 是其他 `/new-*` Skill 的批量编排版本。

## ⛔ 模块黑名单（§A.1 之扩展）

按 `BUILD_STATUS.md` §0：

| 参数 | 行为 |
|------|------|
| `service/{🚫_module}` | 直接拒绝 |
| `service/all` | 跳过 🚫，继续其余 |
| `controllers/http/admin/{🚫_module}` | 跳过 |
| `scheduled-tasks` | 跳过 🚫 任务 |
| `router` | admin 生成时跳过 🚫 路由 |
| `all` | 整体跳过 🚫，且空壳保持空壳 |

## ⚠️ 强烈建议

对于 `all` 或整层级重建（`service/all` / `controllers/http/{audience}`），**优先使用 `docs/architecture/mvp_rebuild_path.md` 的分阶段法**，而不是本 Skill 一次性生成。

仍坚持 `all` 时：先读 mvp_rebuild_path.md，按 Stage 顺序触发，每 Stage 间用户确认。

## 原则

1. 文档是唯一真相
2. 先读后写
3. 逐层构建
4. 持续验证
5. BUILD_STATUS 先查后写

## 流程

### 第 1 步：确定重建范围

| 参数模式 | 读取文档 | 重建代码 |
|---------|---------|---------|
| `components-constants` | `architecture/constants.md` | `components/constants.go` |
| `helpers-utils` | `architecture/helpers_api.md` §1 | `helpers/{ip,crypto,math}.go` |
| `models` | `schema/database_design.md` | `models/` 各包 |
| `cache-helpers` | `cache/cache_helpers.md` | `service/{module}/cache_loaders.go` |
| `middleware` | `architecture/middleware.md` + `{核心校验链}_flow.md` | `middleware/*.go` |
| `internal-render` | `architecture/render_functions.md` | `controllers/http/internal/render.go` + `validator.go` |
| `router` | `architecture/routing.md` | `router/http*.go` |
| `service/{module}` | `service/{module}_service.md` | `service/{module}/` |
| `service/all` | `service/*_service.md` | `service/` 所有模块（跳过 🚫） |
| `controllers/http/{audience}` | `api/{audience}_interfaces.md` | `controllers/http/{audience}/` |
| `scheduled-tasks` | `service/scheduled_tasks_design.md` | `controllers/command/` + 注册 |
| `mq-consumer` | `service/scheduled_tasks_design.md` §3 | `helpers/kafka_consumer.go` + `controllers/mq/` + 注册 |
| `all` | 全部 docs | 整工程（**改用 mvp_rebuild_path 分阶段**） |

### 第 2 步：读取所有相关文档（公共必读见 §B）

1. 从 `docs/INDEX.md` 定位所有相关 md
2. 读 `docs/BUILD_STATUS.md`
3. 完整读取每个 md
4. 必读：见公共 §B
5. 额外必读：
   - `docs/cache/cache_design.md` §2.x（Hash 字段映射）
   - `docs/cache/cache_design.md` §2.5（分布式锁）

### 第 3 步：按依赖顺序重建（all 模式）

严格按 `docs/architecture/mvp_rebuild_path.md` 的 Stage 顺序。

### 第 4 步：逐层验证

每完成一层后立即：

```bash
go build ./{layer}/...
go vet ./{layer}/...
```

### 第 5 步：更新 BUILD_STATUS + 交叉验证（公共项见 §C）

1. 每完成一层，状态 ⬜ / 🟡 → 🟢
2. 重建完成 → `/doc-sync-check` 全量校验
3. 文档漏洞按 `PRINCIPLES.md` §5 签名冲突裁决

### 第 6 步：测试同步（4 类用例标准见 §D）

每生成完一层业务代码：

- `service/{module}` → `cases/{audience}/` 对应接口用例全绿
- `controllers/http/{audience}/` → `cases/{audience}/` 全部用例全绿
- `controllers/mq/` → `cases/internal/{producer}_test.go` 的 Kafka 断言绿
- `router/` → 全量 `go test ./test/cases/...` 通过

测试红了 = 本 Stage 未完成。

## 安全提醒

- **不覆盖现有代码**，除非用户明确要求
- 文档与现有代码不一致 → 先报告差异，让用户决定
- `all` 模式需用户二次确认，且**默认拒绝**，建议导向 mvp_rebuild_path


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
