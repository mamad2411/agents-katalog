---
name: web-flow-design
description: "web-flow 内部的设计系统阶段：消费已确认原型，提炼 design tokens 和布局契约，保证后续并行实现共享同一视觉与结构事实源。仅在 web-flow 主 Skill 明确调用时使用；当前阶段为 design。不要因普通用户请求单独触发。"
---

# web-flow-design · 设计系统

按 [WebFlow 工作流](../web-flow/references/workflow.md)消费视觉门已批准的 artifact，不在本阶段重新发明信息架构或视觉方向。

## 输入选择

- fast：只消费 G1 决策绑定的 `approved wireframe`。
- full：只消费 G2 决策绑定的 `approved prototype`。

不能读取“最新文件”来猜输入；必须使用 gate event 绑定的 artifact revision 和实时 hash。

## 独立 memory

若本 Skill 的 `memory/index.md` 存在，只读取设计一致性、布局契约和当前外部设计工具相关的 1–3 条记忆；不存在时直接继续。通过三项验证的候选只写回本 Skill 的 `memory/`。

## 真实 SOP

1. **观察原型**：识别层级、节奏、关键状态和桌面/移动差异，记录证据。
2. **提炼 tokens**：定义颜色、字体、间距、圆角、边框、阴影和动效节奏；每个值都能追溯到已批准 artifact 或明确决策。
3. **建立布局契约**：定义 sections 顺序、slot、容器、断点和关键组件状态，作为并行实现的共同输入。
4. **写可执行 CSS**：把自定义属性、字体声明、断点和 motion tokens 写成普通 CSS，避免后续再翻译一层配置格式。
5. **检查一致性**：用代表性 section 验证 tokens 与布局能复现已批准输入，不把工具默认样式当设计决策。

## 产物

写入 run：

- `design/design-tokens.css`：可读取、可复制的 tokens 契约证据。
- `design/layout-contract.md`：sections、slots、断点、状态、动效意图和响应式变化。
- `design/stage-result.md`：观察、证据、决定、行动、验证、residual 和 `next: build`。

run 内 CSS 只是不可变的契约证据。真实站点样式由 build 阶段写入 `sourceDir`，不得让运行时 artifact 路径成为网站源码依赖。

每个文件完成后执行 runtime `artifact add`；任何修订都追加 revision，不覆盖旧设计证据。

## 交接评分

调用 `web-flow-benchmark` 的 design rubric，并通过 `review record` 绑定当前 artifact、review 文档和 rubric hash。每轮只处理一个 `top_fix`，最多两轮；`must_pass` 未通过时保持阻断并单独 recheck。
