---
name: doc-sync-check
description: 检查 docs/ 文档与代码的一致性，发现缺失文档、过期文档和未登记的文档。同时审计 aiweave 规范本体是否含业务名泄漏（PRINCIPLES §12），并机械扫描配置安全（R-CONF-*）与部署/运行时生命周期（R-SHUTDOWN-* / R-PROBE-* / R-DEPLOY-*）、数据对外暴露（R-SEC-*）危险锚。用于定期审计文档质量。
disable-model-invocation: true
argument-hint: "[scope] 可选：api / service / schema / architecture / cache / aiweave / all"
---

检查文档与代码的一致性。范围：`$ARGUMENTS`（空或 all 则全量）。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 不生成代码，故第 5 步测试同步不适用，但仍需读 §A-§C。

## 第 0 步：🚫 模块特殊规则（§A 之扩展）

当前阶段的 🚫 模块（`BUILD_STATUS.md` §0）：

- **代码侧**：相关代码文件不存在是**预期**，**不**报"代码缺失"
- **文档侧**：相关 md 完整保留是**预期**，**不**报"文档多余"
- 输出时把 🚫 项独立成"已知跳过项"小节

## 第 1 步：读取范围判定表（公共必读见 §B）

读 `CLAUDE.md`「范围判定表」——它是"代码路径 ↔ 文档路径"的完整双向映射。

## 第 2 步：9 维度检查

**维度 1：代码存在但文档缺失（最严重）**

- 扫描 `controllers/http/{audience}/` 下所有 .go → 检查 `docs/api/` 对应文档
- 扫描 `service/` 下所有 public 方法 → 检查 `docs/service/service_design.md`
- 扫描 `models/` 下所有 struct → 检查 `docs/schema/database_design.md`，逐字段对比
- 扫描 `middleware/` → 检查 `docs/architecture/middleware.md`
- 扫描 `router/command.go` 注册的命令 → 检查 `docs/service/scheduled_tasks_design.md`
- 扫描 `helpers/` 导出函数 → 检查 `docs/architecture/helpers_api.md`

**维度 2：文档存在但代码缺失**

- 扫描 `docs/api/` 中接口 → 检查对应 controller
- 扫描 `docs/service/service_design.md` 方法 → 检查对应 service
- 扫描 `docs/schema/database_design.md` 表 → 检查对应 model

**维度 3：INDEX.md 完整性**

扫描 `docs/` 下所有 .md（递归）→ 检查 `docs/INDEX.md` 是否登记

**维度 4：路由一致性**

- 读 `docs/architecture/routing.md` §5 完整路由表
- 读 `router/` 下 .go 文件，提取实际注册路由
- 双向对比

**维度 5：Redis Key 一致性**

- 从 `docs/cache/cache_design.md` 和 `docs/schema/database_design.md` §4 提取所有 Key 模式
- 在 `service/` 和 `controllers/` 中搜索 Redis 操作
- 检查 Key 名称一致性

**维度 6：错误码一致性**

- 从 `components/error.go` / `service_error.go` 提取所有定义
- 与 `docs/architecture/status_codes.md` 对比

**维度 7：测试覆盖**

- 扫描 `controllers/http/` 下已实现的 handler
- 检查 `test/cases/{audience}/` 是否有对应测试文件
- 输出"代码已实现但测试缺失"列表 → 🔴

**维度 8：规范主体业务名泄漏（仅当 scope 含 `aiweave` 或 `all` 时启用）**

> 此维度审计 `aiweave/docs-spec/*` 与 `aiweave/skills-spec/*` 的"规范主体 vs 参考示例"双轨结构是否被违反。详细规则见 [`PRINCIPLES.md §12 占位符规则`](../../../PRINCIPLES.md#12-占位符规则强制--双轨结构)。

> ⚠️ **本维度自身豁免声明（§12.6 #6 meta 内容）**：本节下方第 2 步的"业务名关键词清单"、第 5 步的"误报抑制规则"是 audit 规则的 meta 内容——这些清单行**不参与**自身的维度 8 审计。AI 在扫描 `templates/skills/doc-sync-check/SKILL.md` 时应主动跳过本节内的关键词清单与对照表（按行匹配"`Register / Login`"类清单格式即可识别）。

执行步骤：

1. 锁定主体范围：每个 `docs-spec/*.md` / `skills-spec/*.md`，从首行到最后一节，**排除**任何标题为"参考示例"/"参考实现"或带 `示例` / `仅示意` 字样的小节。
2. 在主体范围内 grep 业务名关键词清单（不区分大小写）：
   - **英文动作 / 方法**：`Register` / `Login` / `Logout` / `Verify` / `Report` / `Recharge` / `Deduct` / `Activate` / `Refund` / `Withdraw`
   - **英文实体 ID**：`userId` / `orderId` / `accountId` / `rechargeId` / `logId`
   - **英文 struct / Service**：`RegisterReq` / `LoginReq` / `VerifyReq` / `VerifyResp` / `ReportReq` / `AccountService` / `BillingService` / `UserService` / `OrderService`
   - **英文字段 / 概念**：`verify_code` / `balance` / `password_hash` / `access_token` / `refresh_token` / `app_secret`
   - **英文业务模块名**（与 PRINCIPLES §12.3 反例对照表对齐）：
     - 典型业务模块：`account` / `order` / `billing` / `product` / `merchant` / `payment` / `recharge` / `customer` / `cart` / `checkout`
     - 作 `package` 声明 / 路径 `service/` / `notice.module` 标签值 / Redis 命名空间前缀等出现皆视为泄漏
   - **英文业务字段 / 业务量化**（含计数 / 计费 / 额度类业务专属字段）：
     - 业务标识字段：`app_key` / `api_code` / `account_id` / `order_id` / `product_id` / `merchant_id`
     - 业务量化字段：`total_amount` / `used_amount` / `remaining` / `quota`
     - 业务计数字段：`total_count` / `success_count` / `fail_count` / `counted_count`
     - 业务消息字段：`msg.cost` / `msg.billed` / `msg.statusCode`（业务语境而非 HTTP）
     - 业务过期时间：`expire_at`（业务过期，vs 通用 TTL）
   - **英文文件 / 函数 / 变量**：`account_flow` / `auth_flow` / `billing_flow` / `pickMode` / `generateUserId` / `userSeq` / `monthly-report` / `daily-report` / `call_log_consumer` / `CleanExpiredQuota` / `FlushDailyStats`（任务名 / 方法名含业务词）
   - **中文业务概念**：`用户` / `订单` / `余额` / `注册` / `登录` / `扣减` / `充值` / `开户` / `套餐` / `状态扣减` / `状态上报` / `余额检查` / `负余额` / `余额已扣` / `余额不足` / `用户禁用` / `用户态` / `额度` / `已使用量` / `总额度` / `剩余额度` / `计费` / `结算`
3. 命中 → 标 🔴 严重；标注文件路径 + 行号 + 命中关键词；建议动作"迁移到末尾参考示例段或改占位符"。
4. 末尾参考示例段必须有 `> ⚠️` 警告行；缺失 → 标 🟡 中度。
5. 误报抑制（按优先级）：
   - a. 占位符内部 hint 词不算泄漏：grep 前先剔除主体范围内所有 `{...}` 包裹的内容（占位符语法是清晰标识）
   - b. 中文"用户"指代开发者/操作者/调用方时不算泄漏（如"提示用户"、"用户裁决"、"用户提供需求文档"等开发协作语境）；判定见 PRINCIPLES §12.6 第 5 条
   - c. §12.4 自身的关键词清单 / §12.3 自身的反例对照表 / 本 Skill 第 2 步 b 项的关键词清单—— meta 内容，不参与审计
   - d. AIWeave 规范本体引用 template 文件实名（如 `templates/docs/architecture/auth_flow.md`）不算泄漏，但应注明"template 文件实际名为 X，落地按业务重命名"
   - e. 行末含 `<!-- aiweave:allow=domain-leak reason=... -->` 注解时跳过。每文件豁免不超过 3 处，超出 → 标 🟡 中度（建议结构调整）。

**维度 9：配置安全 + 部署/运行时 + 数据对外暴露危险锚（仅当对应规范启用时）**

> 折叠审计：参照 26 把 `R-CONF-*` 折叠进本 Skill 的模式，27 的部署/运行时锚同样在此机械扫描，不另设审计 Skill。锚定义见 [`ai_dev_guide.md §10.8`](../../../templates/docs/architecture/ai_dev_guide.md)（R-CONF-*）/ §10.9（R-SHUTDOWN-* / R-PROBE-* / R-DEPLOY-*）/ §10.11（R-SEC-*）。grep 锚为信号级，命中标 🟡 待复核。

- **配置安全（如启用 26）**：扫描配置文件 / 代码中的明文凭据、硬编码密钥、拉取未 fail-fast（`R-CONF-PLAINTEXT-CRED` / `R-CONF-HARDCODE-SECRET` / `R-CONF-SECRET-COMMIT` / `R-CONF-NO-FAILFAST`）
- **部署/运行时（如启用 27）**：
  - 进程入口（`func main` / 子命令）未注册 `signal.Notify` 终止信号 / 收到信号即硬退出 → `R-SHUTDOWN-NO-SIGNAL` / `R-SHUTDOWN-NO-DRAIN`
  - 与 `concurrency_safety.md §1.1` 常驻 goroutine 清单对账，未接入关闭排空 → `R-SHUTDOWN-LEAK-GOROUTINE`（与 `/concurrency-review` 交叉复核）
  - liveness 探针 handler 内含依赖检查（`.Ping(` / 下游调用）→ `R-PROBE-LIVENESS-DEEP`；对外服务缺探针端点 → `R-PROBE-MISSING`
  - 镜像定义缺非 root 声明 → `R-DEPLOY-ROOT`；编排清单缺 requests/limits → `R-DEPLOY-NO-LIMITS`
- **数据对外暴露 / 加密（如启用对外 ID 加密）**：assembler / 出口渲染直接返回未加密真实主键 / 内部 ID → `R-SEC-ID-PLAINTEXT`；对外 ID 解密失败返差异化错误 / 4xx / 携带失败细节（而非统一"查无结果"）→ `R-SEC-DECRYPT-ORACLE`（核对 `status_codes.md §6.5` / docs-spec/14 §9.5）
- 命中且未豁免（行末 `// aiweave:allow=<rule-id>`）→ 列入 🟡 待复核，核对 `deployment.md` §3/§5 与代码一致

## 第 3 步：输出格式

按严重程度分组：

```
🔴 严重 — 代码存在但文档完全缺失 / 规范主体业务名泄漏
  - {列表}

🟡 警告 — 文档与代码不一致 / 参考示例段缺警告行 / 豁免过多

🟢 提示 — INDEX.md 未登记
  - {列表}

⬜ 文档已设计但代码未实现（正常，待编码）
  - {列表}

🚫 已知跳过项（暂不实现模块）
  - {列表}

📊 进度统计
  - Controller / Service / Model / Middleware / 定时任务：已实现 X / 文档定义 N
```

## 第 4 步：文档同步（公共项见 §C）

本 Skill 不生成代码，无需更新 BUILD_STATUS。但**审计结果应记录到 PR/工单**，让用户追踪修复进度。

## 第 5 步：测试同步

**不适用**——本 Skill 不生成业务代码。但建议运行 `cd test && go test ./...` 确认现有测试在审计后仍全绿。

## 第 6 步：验证

无额外验证命令；审计输出即为产出。


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
