---
name: web-flow
description: "将一句话产品意图落地为真实、带动效、可部署的前端站点，通过 research/prototype/design/build/deploy 子 Skill 渐进执行，并在每阶段交接调用 web-flow-benchmark 做有限评测；每个子 Skill 独立维护自己的错误 memory。用于仿做网站、建设官网或落地页、产出项目代码并部署到真实 URL；不处理纯后端、纯 CLI 或非可视产物，单文件 HTML 成品应使用 crafted-web。"
---

# web-flow · 总地图

> 把产品意图推进成可验证的真实网站。本文件只保留入口、硬约束与按需导航；不要一次性加载全部阶段 Skill。

## 何时使用

用于官网、落地页、产品站、参考站点重构，以及需要真实项目代码、浏览器验证或可选部署的前端任务。纯后端、纯 CLI、非可视产物不属于本 Skill；单文件 HTML 成品应使用 crafted-web。

## 开始前

1. 先读[工作流导航](references/workflow.md)，确认 create/update、attended/unattended、fast/full/adaptive，以及是否请求部署。
2. 再读[运行时状态](references/runtime-state.md)，通过 Node CLI 初始化 run；update 模式必须先记录源码变更计划，才可进入 build。
3. 只有当前阶段真的需要浏览器、设计或图像能力时，才读[外部能力](references/external-capabilities.md)并做一次最小探测。
4. 到达某阶段才读取对应 Skill，不预载后续阶段说明。

## 硬约束

1. `events.jsonl` 是运行事实源；`run.json` 只是可重建投影。所有机器状态由 JS 合约校验，禁止手写或直接改状态文件。
2. 所有持久化路径必须是项目相对 POSIX 路径；不得记录 token、认证头、用户绝对路径、localhost 或私网 URL。
3. 阶段产物先写文件，再登记不可变 artifact revision；更新只能追加 revision，复用必须记录来源 run、artifact ref 与 hash。
4. 每个生产阶段交给 `web-flow-benchmark` 独立评审。事实门失败立即阻断；主观评审最多两轮，每轮只修一个 `top_fix`。
5. attended 模式的 G1/G2/G3 由用户决定；unattended 只能由运行时依据已绑定的独立评审自动通过，不能替用户授权部署。
6. 部署是可选分支。只有用户在 G3 后明确授权，`web-flow-deploy` 才能发布；Node 运行时只记录 preflight 与发布证据，不执行网络发布。
7. 当前阶段 Skill 拥有自己的错误 memory 候选。只有真实错误、根因已验证、未来可复现三项同时成立才允许沉淀；主 Skill 不建中心 memory。
8. 终态必须通过 `finalize` 写入，随后以 `validate-run --require-terminal` 对账；不得直接把 run 标成完成。

## 阶段调用

- research：调用 [web-flow-research](../web-flow-research/SKILL.md)，产出内容规格、参考证据与素材需求。
- wireframe / prototype：调用 [web-flow-prototype](../web-flow-prototype/SKILL.md)，并处理 G1；full profile 还要处理 G2。
- design：调用 [web-flow-design](../web-flow-design/SKILL.md)，把已批准原型转成设计契约。
- build：调用 [web-flow-build](../web-flow-build/SKILL.md)，写入真实 sourceDir、启动预览并处理 G3。
- review：每个生产阶段调用 [web-flow-benchmark](../web-flow-benchmark/SKILL.md)，将评审和 rubric 原始字节绑定到事件。
- deploy：仅在请求且获授权时调用 [web-flow-deploy](../web-flow-deploy/SKILL.md)。

## 结束条件

交付至少包含真实预览或生产 URL、当前 G3 证据、验证结果、`skill-usage.md`、`retrospective.md` 与 residual。success、partial、failed、cancelled 都必须有可解释原因和可重放终态。
