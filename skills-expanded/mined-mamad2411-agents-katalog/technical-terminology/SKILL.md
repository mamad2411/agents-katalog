---
name: technical-terminology
description: Use when 需要统一通用软件开发术语的中英文表达、翻译工程文档，或判断 API、命令、路径等标识是否应保留英文
---

# Technical Terminology：常见开发术语中英对照

## 核心原则

中文工程文档优先使用自然、稳定的中文术语，不在每次出现时重复括注英文。本表只保留容易混淆、存在多种合理译法或对本技能包规则有区分价值的词；显然的一对一常识翻译不占用上下文。

以下内容保留原始英文：

- 产品、项目、语言、框架和包的正式名称；
- API、SDK、CLI、HTTP、SQL、TDD、PR/MR、APM 等通行缩写；
- 命令、参数、环境变量、路径、文件名、配置键、符号、类型和错误信息；
- 技能名、Git 引用、协议标记和传输字段等必须精确匹配的值。

同一英文词有多种含义时按实际语义选择中文。例如 `path` 可以是文件路径、调用链或执行路径，`state` 可以是状态或外部数据。

## 开发工作流与歧义缩写

缩写在中文正文中保持原样。这里只收录开发工作流领域中不算约定俗成、展开后有助于查阅的缩写，以及存在多个合理展开的歧义缩写。

| 缩写 | English expansion | 中文释义与语境 |
|---|---|---|
| ADR | Architecture Decision Record | 架构决策记录 |
| RFC | Request for Comments | 征求意见文档；IETF 语境也指正式发布的技术文档 |
| RFD | Request for Discussion | 讨论请求；工程提案或设计讨论文档 |
| RFD | Reflected File Download | 反射型文件下载；Web 安全漏洞语境 |
| DoR | Definition of Ready | 就绪定义 |
| DoD | Definition of Done | 完成定义 |
| ATDD | Acceptance Test-Driven Development | 验收测试驱动开发 |
| RCA | Root Cause Analysis | 根因分析 |
| APM | Application Performance Monitoring / Application Performance Management | 应用性能监控 / 应用性能管理 |
| APM | Actions Per Minute | 每分钟操作数；交互或游戏语境 |
| CD | Continuous Delivery / Continuous Deployment | 持续交付 / 持续部署；同属持续产品化流程，区别通常在正式发布是否保留人工批准 |

## 需求、方法与证据

| English | 中文与使用边界 |
|---|---|
| development task | 开发任务 |
| investigation | 调查 |
| technical spike | 技术探索 |
| temporary artifact | 临时产物 |
| project artifact / deliverable | 项目产物 / 交付产物 |
| work unit | 工作单元 |
| invariant | 不变量 |
| trade-off | 权衡 |
| assumption / hypothesis | 假设；调试时可写“原因假设” |
| claim | 声明；强调判断结果时可写“结论” |
| verification | 验证 / 核验；检查是否满足明确规格或声明 |
| validation | 验证；确认满足用户需求或真实用途；输入与格式检查语境可写“校验” |
| regression | 回归 |
| baseline | 基线 |
| decision point | 决策点 |
| acceptance criteria | 验收标准 |
| non-goal | 非目标 |

## 实现、测试与运行

| English | 中文与使用边界 |
|---|---|
| production / production environment / production env / product environment / product env | 正式环境；这些项目内写法视为同一概念，固定搭配仍写“生产代码”“生产事故” |
| runtime | 运行时 |
| contract | 契约 |
| caller | 调用方 |
| consumer / provider | 使用方 / 提供方 |
| adapter / wrapper | 适配器 / 包装层 |
| fallback | 回退分支；恢复策略语境写“回退方案” |
| feature flag | 功能开关 |
| call path | 调用链 |
| data flow / control flow | 数据流 / 控制流 |
| mutable state | 可变状态 |
| breaking change | 破坏性变更 |
| generated output | 生成产物 |
| test seam | 测试接缝 |
| test double | 测试替身；`dummy`、`fake`、`stub`、`spy` 和 `mock` 等替代对象的总称 |
| fake | 伪实现；可工作但采用不适合正式环境的简化实现 |
| mock | 模拟对象；预置交互预期并在验证时检查 |
| test fixture | 测试夹具 |
| instrumentation | 观测代码；强调机制时写“插桩” |
| probe | 探测；契约验证语境可写“最小验证” |
| span | 跟踪片段；作为 APM 字段名时保留 `span` |

## Git、依赖与代理协作

| English | 中文与使用边界 |
|---|---|
| worktree | 工作树 |
| merge base | 合并基点 |
| finding | 审查意见；缺陷报告语境可写“问题” |
| handoff | 交接 |
| diff | 差异；指 Git 输出时可保留 `diff` |
| staged / unstaged | 已暂存 / 未暂存 |
| dirty working tree | 有未提交改动的工作树 |
| lockfile | 锁文件 |
| manifest | 清单文件 |
| peer / transitive dependency | 对等依赖 / 传递依赖 |
| override / resolution | 覆盖规则 / 解析规则 |
| lifecycle script | 生命周期脚本 |
| version pin | 版本锁定 |
| root agent / subagent | 根代理 / 子代理 |
| delegation | 委派 |
| bounded task | 边界明确的任务 |
| independent review | 独立评审 |
| fresh context | 独立上下文；强调时间时写“最新上下文” |
| fresh evidence | 最新证据 |
| owner | 负责人 |

## 使用规则

1. 先按语义选择中文，再检查是否属于必须保持字面精确的标识。
2. 同一文档对同一概念使用同一译法；项目术语表或用户明确用词优先。
3. 缩写保持原样；需要解释时使用其完整英文名称和中文语境。有多个合理展开时不得脱离上下文猜测。
4. 只有用户要求双语材料、存在真实歧义或正在解释术语时才同时展示中英文。
5. 不翻译代码、命令输出、错误信息、API 字段或符号。
6. 表中没有的词优先使用稳定、自然的行业中文；没有公认译法时保留英文，不生造中文。
