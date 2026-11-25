---
name: salin-dashboard-builder
description: 设计、专项审查、重构或实现 Dashboard 和数据产品界面，统一处理页面信息架构、侧边栏导航、指标摘要、筛选、交互图表、数据口径、状态联动、响应式与工程验收。用于 SaaS 后台、CRM、运营看板、数据监控型 AI 工作台、Web/App/小程序数据页面，也可处理独立的 Dashboard 导航侧栏或交互图表任务。与数据无关的普通页面局部侧区、纯数据计算、静态 CSV、营销官网或通用 UI 质量审查不使用本 skill。
---

# Salin Dashboard Builder

把 Dashboard 当成帮助用户“发现变化、理解原因、采取行动”的产品界面，而不是卡片和图表的拼盘。根据任务只加载需要的模块；不要让侧栏任务承担图表流程，也不要让单图表任务扩张成整页重构。

## 任务路由

| 用户目标 | 必读参考 |
|---|---|
| 从零设计或重构完整 Dashboard | [references/dashboard-architecture.md](references/dashboard-architecture.md)，再按需读侧栏与图表参考 |
| 只设计、审查或实现侧边栏 | [references/sidebar-patterns.md](references/sidebar-patterns.md)；实现时再读 [references/implementation-playbook.md](references/implementation-playbook.md) |
| 不知道数据该用什么图表 | [references/chart-selection-guide.md](references/chart-selection-guide.md) |
| 指定图表并要求交互 | [references/chart-interaction-patterns.md](references/chart-interaction-patterns.md) + [references/interaction-spec-template.md](references/interaction-spec-template.md) |
| 在已有项目中编码 | 先检查项目，再读 [references/implementation-playbook.md](references/implementation-playbook.md) 与任务对应模块 |
| 审查页面、侧栏或图表 | [references/qa-checklist.md](references/qa-checklist.md)，只报告已经确认的问题 |

除非用户要求完整 Dashboard，不要一次加载所有参考文件。

审查按对象分流：图表选型、数据口径、坐标轴、视觉编码、Dashboard 导航与筛选联动由当前 skill 主责；整体产品体验、通用无障碍、反模板化、上线质量或跨页面一致性由 `salin-ui-quality-audit` 主责，当前 skill 只提供 Dashboard 专项证据。

## 核心工作流

1. **定义任务**：明确用户、设备、要监控/比较/诊断/执行的事情，以及成功标准。缺少非关键细节时注明假设继续。
2. **检查现状**：已有项目先读 README、AGENTS/CLAUDE、依赖、路由、布局、数据获取、权限、组件、design tokens 和 Git 状态；保留未提交修改。
3. **建立页面层级**：完整 Dashboard 先确定上下文、全局筛选、指标摘要、主洞察、证据和行动区；不要先画等宽卡片网格。
4. **设计导航**：根据导航深度、入口数量和切换频率选择侧栏结构与视觉模式；信息架构优先于材质。
5. **设计数据表达**：先写用户问题与数据口径，再选择最简单足够的图表；定义视觉编码、交互与异常值。
6. **统一状态**：明确筛选、日期范围、路由、图表选择、表格详情之间的联动和状态所有权，防止组件各自为政。
7. **项目内实现**：复用现有技术栈、路由、权限、图表库和组件；只有关键能力缺失时才新增依赖。
8. **真实验收**：按 [references/qa-checklist.md](references/qa-checklist.md) 检查业务流程、权限、极端数据、长菜单、响应式、触摸、键盘、减少动画和性能，并运行项目已有检查。

## 全局约束

- 一屏先回答一个主要业务问题；其余信息形成清晰的次级层级。
- 侧栏负责稳定定位，不与图表争抢注意力；品牌色只用于少量关键状态。
- 一张图优先回答一个问题；精确比较优先位置和长度，不滥用面积、角度或装饰动画。
- 当前项、数据状态和告警不能只靠颜色表达。
- hover 不能是唯一入口；触摸与键盘必须有等价操作。
- loading、empty、error、disabled、无权限、零值、负值、缺失值和超目标值按业务语义处理。
- 移动端不是桌面版缩小：侧栏通常变抽屉，图表减少同时可见信息，关键操作保持可达。
- 不从参考视频复制品牌、文案和视觉资产；视频数值只作为可调基线。
- 输出深度服从用户请求：页面设计不自动扩张为接口、数据库、异常规则或后端任务；只有实现需要时才补充这些内容。
- 不把推测当项目事实。未知路由、字段、权限、阈值和组件只能标为“建议/假设/待确认”，已有项目必须以真实代码和文档为准。
- 用户要求实现时必须进入真实项目并验证，不能以规格、伪代码或静态截图代替完成。

## 输出契约

完整 Dashboard 设计优先输出：

```markdown
## Dashboard 方案
- 设计读法：产品 / 用户 / 主要决策 / 设备
- 页面结构：上下文 / 筛选 / 指标 / 主洞察 / 证据 / 行动
- 侧边栏：信息架构 / 推荐模式 / 状态 / 响应式
- 图表：业务问题 / 选型 / 数据映射 / 交互 / 数据边界
- 联动：筛选、图表、表格、详情和 URL 状态
- 完整状态：加载 / 空 / 错误 / 无权限 / 极端数据
- 验收标准：可观察、可复现的结果
```

只做侧栏或图表时，删除无关章节，不为凑模板扩张范围。实现任务还需汇报关键文件、依赖变化、已运行检查、未验证项与残余风险。

默认只给一个推荐方案和必要备选。除非用户明确要求完整技术规格，不自动输出接口 schema、后台拆分、全量字段表或长篇教程。

## 完成前检查

- 用户能否在首屏判断“发生了什么、为什么、下一步做什么”。
- 导航层级、页面层级和数据层级是否一致。
- 图表口径、单位、轴、阈值和交互是否真实且不误导。
- 侧栏、筛选、图表、表格和详情状态是否同步。
- 桌面、触摸、键盘、移动端和减少动画是否都有可用路径。
- 是否基于真实页面验证，而不只依赖编译或静态代码检查。
