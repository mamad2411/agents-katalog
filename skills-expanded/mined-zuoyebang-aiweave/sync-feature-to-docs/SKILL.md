---
name: sync-feature-to-docs
description: 增量需求同步 — 开发完需求后，把代码改动反向同步到全链路 docs/（INDEX/BUILD_STATUS/各架构 md/API/Service/缓存/错误码/常量/测试覆盖）。
disable-model-invocation: true
argument-hint: <需求标识或简述> 例如 "feat-batch-export" 或 "新增批量导出接口"
---

把单次需求的代码改动 + 需求设计文档反向同步到全链路 docs/。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。
>
> **B1 增量同步场景的核心 Skill**。规范见 `aiweave/docs-spec/19_incremental_sync_spec.md`。

## 第 0 步：拒绝规则与输入完整性检查

- ⛔ 拒绝（§A.1）：改动触碰 `BUILD_STATUS.md` §0 中 🚫 模块时立即停止
- 输入完整性检查：
  - 缺需求技术文档 → 提示用户补充："本次同步可能遗漏 X 处"
  - 缺 git diff / 改动清单 → 提示提供
  - PR 跨多个独立特性 → 提示拆分

## 第 1 步：读输入（公共必读见 §B）

```
1.1 读取本规范：
    - aiweave/PRINCIPLES.md
    - aiweave/docs-spec/00..19（全部）
1.2 读取本工程：
    - docs/INDEX.md
    - docs/BUILD_STATUS.md
    - CLAUDE.md（拿到范围判定表）
1.3 读取用户提供：
    - 需求技术文档
    - git diff / 改动清单 / 关键代码片段
```

## 第 2 步：差异分类（按 CLAUDE.md 范围判定表）

| 改动文件 | 影响的 docs/ |
|---------|------------|
| `models/{db}/{table}.go` | `docs/schema/database_design.md` §3.X |
| `service/{module}/*.go` | `docs/service/{module}_service.md` + `service_design.md` |
| `service/{audit-module}/*` | `docs/architecture/audit_log.md` |
| `controllers/http/{audience}/{module}/*.go` | `docs/api/{audience}_interfaces.md` |
| `controllers/command/*.go` + `router/command.go` | `docs/service/scheduled_tasks_design.md` |
| `controllers/mq/*.go` + `router/mq.go` | `docs/service/scheduled_tasks_design.md` §3 |
| `middleware/*.go` | `docs/architecture/middleware.md` |
| `router/http*.go` | `docs/architecture/routing.md` |
| `helpers/*.go`（导出 / 全局） | `docs/architecture/helpers_api.md` |
| `helpers/{cache_loaders}.go` | `docs/cache/cache_helpers.md` |
| `helpers/kafka.go` / `kafka_consumer.go` | `docs/architecture/helpers_api.md` + `scheduled_tasks_design.md` §3 |
| `helpers/circuit_breaker.go` | `docs/circuit_breaker/circuit_breaker_design.md` |
| 涉及 Redis 操作（新 Key / Hash 字段） | `docs/cache/cache_design.md` §2.X + `database_design.md` §4 |
| `components/error.go` / `service_error.go` | `docs/architecture/status_codes.md` |
| `components/constants.go` | `docs/architecture/constants.md` |
| `conf/` | `docs/architecture/config.md` |
| `pkg/**` | `docs/architecture/pkg_api.md` |
| `test/framework/` | `docs/testing/testing_design.md` |
| `test/cases/` | 对应 `docs/api/*.md` |

## 第 3 步：每篇 md 的更新动作

| 改动类型 | 必更新字段 |
|---------|-----------|
| 新增 API | docs-spec/07 §5 单接口完整规格 |
| 修改 API 字段 | 校验规则表 + Go struct + Controller 伪码 |
| 新增 service 方法 | docs-spec/09 §10 + §3 + §6 接口映射 |
| 新增表 | docs-spec/05 §3 完整 DDL + §4 Redis Key + §6 GORM 规范 |
| 修改字段 | DDL + 字段说明 + 索引 + 关联 |
| 新增 Hash 字段 | docs-spec/06 §4.2 + database_design §4.6 |
| 新增 Redis Key | docs-spec/06 §2.X + database_design §4 |
| 新增错误码 | docs-spec/14 §2.3 / §3.3 + 业务状态枚举 |
| 新增常量 | docs-spec/16 §X + §10 components/constants.go |
| 新增中间件 | docs-spec/04 §5 + routing §1 |
| 新增定时任务 | docs-spec/10 §1.2 + §2/§3/§4 + §6 |
| 新增 MQ topic | docs-spec/11 §3.1 + §3.2 + §3.5 |
| 新增 helper 全局变量 | docs-spec/15 §3.2 |
| 新增 helper 函数 | docs-spec/15 §3.1 |

## 第 4 步：交叉一致性检查（公共项见 §C，额外项如下）

```
4.1 INDEX.md 是否登记新增 md？
4.2 BUILD_STATUS 状态是否更新（⬜ → 🟢 / 🟡）？
4.3 新 Redis Key 在 cache_design §4 与 database_design §4 双向出现？
4.4 新常量在 constants §X 表 与 §10 Go 双向？
4.5 新接口在 api/*.md 与 routing §5 双向？
4.6 新 service 方法在 service_design §6 接口映射？
4.7 新 helper 函数在 helpers_api §1 / §2？
4.8 新 / 改代码已同步测试用例？
```

## 第 5 步：检测签名冲突

按 `aiweave/PRINCIPLES.md` §5 签名冲突裁决：

- 既有契约（已被业务代码引用） → 以代码为准，修正 md
- 未来设计（业务代码尚未引用） → 以 md 为准，修代码

显式报告每条冲突，由用户裁决。

## 第 6 步：输出与确认

按 docs-spec/19 §4 五类输出契约组织最终回复：

```markdown
## 文档变更清单

### 新增的 md
- ...

### 修改的 md
- ...

### 无变更（已审查）
- ...

## 每条变更的 diff 摘要
（diff 块）

## 自检清单（含公共 §C 全部 + 本 Skill §4）
- [x] 新增代码 → 都已找到对应 md
- [x] 修改代码 → 都已更新关联 md
- [x] 新增 md → 已登记 INDEX
- [x] 删除代码 → 同步清理 md
- [x] 测试用例已同步
- [x] 未触碰 🚫 模块
- [x] BUILD_STATUS 已更新

## 签名冲突报告（如有）
（按 PRINCIPLES.md §5 处理）

## 文档同步声明
文档同步：更新了 docs/api/xxx.md、docs/service/yyy.md、...
```

**不要静默修改 md** — 必须列出所有变更让用户审阅。

## 测试同步（特殊，标准见 §D）

本 Skill **不直接生成测试代码**。但必须：

- 检查每个新接口 / 新 service 方法是否有 `test/cases/` 下对应文件
- 检查测试用例数量是否达 4 类底线
- 缺失 → 列出并提示用户调 `/new-test {scope}` 补齐

## 第 7 步：验证

无独立验证命令；输出即为产出。建议用户在 PR 合并前再跑一次 `/doc-sync-check all` 兜底。


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
