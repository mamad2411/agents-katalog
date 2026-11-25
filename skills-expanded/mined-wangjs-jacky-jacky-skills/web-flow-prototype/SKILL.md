---
name: web-flow-prototype
description: "web-flow 内部的原型设计阶段：以 wireframe 和 prototype 两种模式，把源接地内容转成低保真草图与可观察的视觉或交互原型；运行时按需复用外部能力，缺失时降级为 HTML/CSS。仅在 web-flow 主 Skill 明确调用时使用。不要因普通用户请求单独触发。"
---

# web-flow-prototype · 草图与视觉原型

> 原型不是“让图片模型出一张图”。它复现人真实的设计过程：先排结构并评审 G1，再做视觉原型并评审 G2。

从 [WebFlow 工作流](../web-flow/references/workflow.md)读取当前 profile、mode 和已登记的 research artifact。只处理 wireframe 和 full profile 的 prototype，不在本阶段写真实项目源码。

## 独立 memory

若本 Skill 的 `memory/index.md` 存在，只沿当前 mode 和外部原型工具相关入口读取 1–3 条记忆；不存在时直接继续。通过三项验证的候选只写回本 Skill 的 `memory/`。

## `wireframe` 模式（G1）

1. 从 `research/content-spec.md` 和 `research/reference-evidence.md` 确认受众、主任务、主行动与必须出现的信息。
2. 按用户完成任务的顺序建立信息架构，明确首屏重点与页面节奏。
3. 写可真实打开的 `wireframe/wireframe.html`，不依赖构建工具也能检查信息层级、阅读路径和桌面/移动布局。
4. 写 `wireframe/stage-result.md`，用 runtime `artifact add` 登记两个文件；调用 `web-flow-benchmark` 的 wireframe rubric 并用 `review record` 登记版本化评审。
5. 评审路径必须是 `reviews/<stage>/attempt-<n>/round-<n>--<artifact-id>-r<revision>.md`；must-pass recheck 使用运行时规定的独立槽位，不占主观两轮。
6. 通过 `gate decide` 记录 G1。attended 展示 artifact 后由用户 approve/revise/defer/reject；unattended 只能依据当前独立评审决定。
7. revise 会进入新的 attempt，并要求新 artifact revision、review 和 gate decision，不能覆盖 attempt-1 的文件。
8. G1 时锁定 profile：fast 直接进入 design，full 进入 prototype，adaptive 必须在这里选择其一。

## `prototype` 模式（G2）

1. 只接受 full profile，并读取已批准 G1 所绑定的 wireframe 与 `research/asset-requirements.md`。
2. 按[外部能力规则](../web-flow/references/external-capabilities.md)，对 `prototype_design` 及必要的 `visual_asset_generation` 执行“本轮首次使用才探测”。
3. 使用第一个满足输入输出的候选；全部不可用时降级为本地 HTML/CSS，不静默跳过原型。
4. 写可打开的 `prototype/prototype.html`，保留与内容证据、草图和关键素材需求的对应关系。
5. 真实观察桌面与移动视图，检查主行动、层级、可读性和关键状态。
6. 写 `prototype/stage-result.md`，依次执行 `artifact add`、独立 benchmark、`review record`。
7. 通过 `gate decide` 记录 G2；revise 同样产生新的 attempt 和全部新版本证据。
8. attended 模式给用户看 G2；unattended 模式只依据当前通过的独立评审进入 design。

本 Skill 只选择与编排，不复制外部 Skill 的完整说明，也不把供应者写死为永久依赖。

## fast 的 G2

fast profile 不运行 prototype，必须通过 typed transition 把 G2 记为 `not_applicable`；不得创建假的 prototype、review 或批准记录。

## stage-result 内容

两个 mode 的 `stage-result.md` 都记录观察、证据、决定、行动、验证、错误、根因、下次规则、residual 和 next。只写可审计事实，不写冗长原始推理。
