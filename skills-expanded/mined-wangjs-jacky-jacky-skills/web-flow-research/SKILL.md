---
name: web-flow-research
description: "web-flow 内部的调研阶段：观察参考站和已有资料，把页面内容逐条绑定来源，产出内容规格、参考证据和素材需求。仅在 web-flow 主 Skill 明确调用时使用；当前阶段为 research。不要因普通用户请求单独触发。"
---

# web-flow-research · 源接地调研

只处理 [WebFlow 工作流](../web-flow/references/workflow.md)中的 research，不负责原型设计。目标是让后续页面内容都有来源，而不是凭空补齐一份看似完整的营销文案。

## 独立 memory

若本 Skill 的 `memory/index.md` 存在，只读取与参考采集、来源可信度和外部观察相关的 1–3 条记忆；不存在时直接继续。通过三项验证的候选只写回本 Skill 的 `memory/`，不进入中心 memory。

## 输入边界

读取 run input 中的意图、用户提供的 references 和项目上下文。若需要打开参考站，按[外部能力规则](../web-flow/references/external-capabilities.md)首次使用 `reference_observation` 时再探测；没有可用工具就使用用户已有材料，不阻断内容梳理。

## 真实 SOP

1. **确认目标**：从用户意图提取受众、页面目标、主行动和不可编造的边界。
2. **采集五类来源**：按任务实际存在的材料检查用户原话、项目源码、已有文档、参考网页、截图或录屏。缺少某一类不代表失败，但必须明确写“未提供/未观察”。
3. **记录参考证据**：只保存公开 URL、项目相对路径、截图或录屏的 run 内相对路径，以及能复核结论的简短观察；不要保存认证信息和用户绝对路径。
4. **建立事实映射**：每条标题、功能、数字、卖点和行动按钮都绑定来源。无法证实的内容标为 gap 或 design hypothesis，不能伪装成事实。
5. **提炼内容规格**：按用户任务顺序定义页面 section、内容优先级、主行动、必要状态、事实声明和待确认项。
6. **提炼素材需求**：逐项说明用途、尺寸/比例、来源限制、是否阻断 prototype，以及可接受的 fallback。
7. **复核完整性**：检查关键事实是否可解析、五类来源状态是否明确，并区分事实内容与后续设计判断。

## 产物

在 run 内写入以下 Markdown：

- `research/content-spec.md`：受众、目标、section、事实声明、主行动、状态与 gap。
- `research/reference-evidence.md`：五类来源的状态，以及每项内容事实到证据的映射。
- `research/asset-requirements.md`：素材用途、规格、来源和 fallback。
- `research/stage-result.md`：观察、证据、决定、行动、验证、错误、根因、下次规则、residual 与 `next: wireframe`。

每个文件写完后通过 runtime `artifact add` 登记 revision 和 SHA-256。不能覆盖已登记证据；修改后追加新 revision。

## 交接评分

调用 `web-flow-benchmark` 的 research rubric，并把独立 review 写入该 stage 当前 attempt 的版本化 review 路径。must-pass 失败先修事实条件并 recheck；主观评审每轮只处理一个 `top_fix`，最多两轮。低分只生成当前阶段的 memory candidate，不直接写 memory。
