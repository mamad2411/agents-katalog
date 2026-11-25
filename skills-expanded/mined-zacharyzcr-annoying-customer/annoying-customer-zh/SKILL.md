---
name: annoying-customer-zh
description: 让具备视觉能力的 AI 扮演挑剔的真实客户，包括懂技术的用户、非技术客户、领导、商务人员和系统运维人员；仅通过浏览器截图、可见文字、点击、输入、滚动和等待来体验已部署产品。适用于上线前合成用户研究、探索式 UX 测试、客户旅程评估、首次使用测试、分角色可用性审查，以及缺少真实用户时基于证据的产品反馈。只产出候选问题和改进建议，绝不把模拟偏好当作市场验证。
---

# 烦人的客户——中文版

让边界明确的合成用户操作产品。通过可见 UI 行为发现使用阻力，并严格区分观察、已复现缺陷、假设和建议。

## 前置条件

1. 明确目标 URL、允许使用的环境、凭据来源和变更边界。
2. 优先使用 staging 或带测试数据的环境。未经明确授权，不在生产环境执行破坏性旅程。
3. 确认存在具备浏览器操作能力的工具。Actor 必须使用产品真实浏览器界面，不能靠阅读源码体验产品。
4. 选择角色时阅读 [references/role-catalog.md](references/role-catalog.md)。
5. 执行旅程前阅读 [references/actor-policy.md](references/actor-policy.md)。
6. 评判结果前阅读 [references/evaluator-policy.md](references/evaluator-policy.md)。

如果没有浏览器工具，在声称完成模拟用户测试前停止。只能提供场景和 persona 设计。

## 工作流

### 1. 建立研究范围

记录：

- 产品和环境；
- 研究问题；
- 允许和禁止的操作；
- 初始状态和重置方法；
- 核心任务；
- 角色和运行次数；
- 确定性的成功证据；
- 隐私和凭据限制。

每个与产品相关的用户群至少选一个角色。不得编造与产品没有合理关系的角色。

### 2. 准备 persona 和场景

从 `assets/personas/` 的五个预设开始，或复制 [assets/persona.example.yaml](assets/persona.example.yaml) 和 [assets/scenario.example.yaml](assets/scenario.example.yaml)。使用以下命令校验：

```bash
python scripts/validate_config.py persona path/to/persona.yaml
python scripts/validate_config.py scenario path/to/scenario.yaml
```

明确写出角色、知识水平、目标、耐心、风险承受度、阅读深度、探索倾向、设备和操作预算。Actor 只能知道该角色在现实中合理掌握的信息。

### 3. 运行 Actor

每次运行使用全新的浏览器上下文，除非场景明确测试回访用户状态。

每一步都要：

1. 截图并记录可见或无障碍页面状态。
2. 更新 Actor 状态：当前认知、信心、挫败感、信任、目标进度和剩余预算。
3. 只选择一个可见用户动作：点击、输入、选择、滚动、后退、等待、刷新或放弃。
4. 通过浏览器执行该动作。
5. 记录动作、理由、可见反馈、耗时和错误。

不得使用仓库搜索、实现知识、数据库直查、隐藏 API、DOM 修改、JavaScript 注入或开发者工具帮助 Actor 导航。诊断证据只能在 Actor 运行结束后单独收集。

允许真实失败。persona 的耐心、时间或操作预算耗尽时应当放弃。不得为了让报告好看而强迫任务成功。

### 4. 应用真实行为

把 persona 特征转化为行为：

- 耐心低：等待一次、重试一次，然后放弃或寻找另一条可见路径。
- 阅读深度低：只扫标题、标签、主按钮和首段可见文字。
- 产品知识低：按字面理解术语，允许出现合理误解。
- 风险承受度低：影响、范围或回滚不清楚时犹豫或拒绝操作。
- 时间压力高：优先使用显眼的快捷入口和摘要，不做穷举探索。
- 技术能力高：检查可见细节和术语，但仍禁止源码和隐藏 API。
- 技术能力低：偏好白话标签、引导和熟悉的导航模式。

不要为了表演而随机犯错。每个错误都必须来自 persona、可见 UI 或先前认知。

### 5. 独立评估

Actor 的自我评价和 Judge 必须分离。

按以下顺序判断：

1. 获得授权时使用确定性的 API、数据库或业务状态证据；
2. 可见确认和操作后的 UI 状态；
3. 操作轨迹一致性；
4. 仅对歧义、清晰度、信任和感知成本使用模型判断。

每个发现必须归为以下一种：

- `confirmed_bug`：通过客观证据复现的功能或状态缺陷；
- `high_confidence_friction`：跨运行或角色重复出现的阻塞；
- `ux_hypothesis`：合理但尚未重复或客观验证的假设；
- `preference`：主观反应，不能单独当作缺陷；
- `test_artifact`：浏览器、模型、测试数据或测试工具故障。

### 6. 重复并汇总

成本允许时，每个 persona 和场景组合至少运行三次。不得把一次偶发的模型行为升级为高置信问题。

按 [references/result-schema.md](references/result-schema.md) 为每次运行保存一份 JSON，然后汇总：

```bash
python scripts/aggregate_runs.py runs/*.json --output synthetic-user-report.md
```

按可复现性、受影响角色、任务影响、严重程度、恢复难度和证据质量排序。不要按 Actor 抱怨得有多凶来排序。

### 7. 报告与交接

使用 [assets/report-template.md](assets/report-template.md)，包括：

- 环境和研究限制；
- 角色、任务、运行矩阵；
- 完成率、放弃率、中位步骤和中位耗时；
- 重复出现的困惑和失败点；
- 证据链接或产物路径；
- 已确认缺陷和 UX 假设分开列出；
- 每个高置信问题对应的最小有效改进；
- 风险和仍需真实用户验证的内容。

只有得到明确授权后才能创建 Issue 或修改产品。调查、排序和实施必须分阶段进行。

## 完整性规则

- 不得声称合成用户证明了产品市场匹配、吸引力、付费意愿或真实用户偏好。
- 不得在报告中暴露凭据、Token、个人数据或敏感截图。
- 不得让 Actor 看到预期点击路径或成功判定条件。
- 不得只依赖同一个模型的 Actor 叙述和 Judge 判断作为证据。
- 不得把 HTTP 200、服务状态或模型自述当成已完成的用户旅程。
- 浏览器工具不可用、认证过期、测试数据错误和环境故障必须标记为测试产物，除非已证明是产品问题。

## 资源

- [references/role-catalog.md](references/role-catalog.md)：默认角色和行为差异。
- [references/actor-policy.md](references/actor-policy.md)：仅浏览器模拟和状态转换规则。
- [references/evaluator-policy.md](references/evaluator-policy.md)：证据层级和问题分类。
- [references/result-schema.md](references/result-schema.md)：运行产物格式。
- [assets/persona.example.yaml](assets/persona.example.yaml)：persona 模板。
- `assets/personas/`：技术、非技术、领导、商务和系统运维预设。
- [assets/scenario.example.yaml](assets/scenario.example.yaml)：场景模板。
- [assets/report-template.md](assets/report-template.md)：最终报告模板。
- `scripts/validate_config.py`：确定性校验 persona 和场景。
- `scripts/aggregate_runs.py`：把多份运行 JSON 汇总为 Markdown 报告。
