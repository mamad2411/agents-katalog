---
name: web-flow-build
description: "web-flow 内部的实现阶段：按内容规格、已选原型、design tokens 和布局契约分 section 构建前端与动效，组装并验证真实预览。仅在 web-flow 主 Skill 明确调用时使用；当前阶段为 build。不要因普通用户请求单独触发。"
---

# web-flow-build · 实现与真实预览

按 [WebFlow 工作流](../web-flow/references/workflow.md)把已批准设计落实到真实项目。源码只写 `sourceDir`；run 目录只保存证据，不作为站点源码或构建输入。

## 独立 memory

若本 Skill 的 `memory/index.md` 存在，只读取并行 section、动效、响应式和集成相关的 1–3 条记忆；不存在时直接继续。通过三项验证的候选只写回本 Skill 的 `memory/`。

## 写入前安全门

1. 读取 run input、当前 G1/G2 绑定、`design/design-tokens.css` 和 `design/layout-contract.md`，确认 hash 未漂移。
2. create 模式确认 sourceDir 不存在或为空；不得把源码写进 `.web-flow/`。
3. update 模式先读取初始化生成的 `preexisting-state.md`，再执行 runtime `source plan` 登记精确 allowlist。
4. allowlist 与已有 dirty path 重叠属于 `dirty conflict`，没有用户逐路径确认就必须阻断。
5. typed transition 只有看到 source plan 才允许 update 进入 build；不能先改代码再补计划。

## 真实 SOP

1. **拆实现单元**：按 layout contract 的 slot 规划组件边界；每个单元只接收当前 section 所需内容和共享 tokens。
2. **保持单写者**：可以并行分析或生成补丁建议，但禁止并行写同一源码树。一个协调者按顺序把变更应用到 sourceDir，避免互相覆盖和 baseline 失真。
3. **按原型实现动效**：CSS 优先，动效必须支持信息理解或状态反馈；尊重减少动态效果设置。
4. **组装真实页面**：按布局契约拼装，保留内容来源和原型对应关系。
5. **执行源码验证**：运行项目自身的格式化、类型、测试和构建命令，记录命令与结果，不把依赖目录登记为 artifact。
6. **验证写入边界**：update 模式在 build 后执行 runtime `source verify`，对比初始化 baseline、allowlist、已确认 dirty 内容和当前 Git 状态；失败时不得进入评审。
7. **观察真实页面**：首次需要时按[外部能力规则](../web-flow/references/external-capabilities.md)探测 `browser_verification`。检查 HTTP 响应、桌面和移动视图、交互、关键资源及控制台；run 证据不持久化本机私有 URL。
8. **产 G3 预览**：登记 preview evidence，调用独立 benchmark 并 `review record`。attended 由用户通过 `gate decide` 决策；unattended 只依据绑定评审自动决策。

## 产物

真实源码和证据严格分开：

- sourceDir：唯一站点源码位置；不复制到 runDir。
- `preexisting-state.md`：update 初始化时生成的 Git baseline 与 dirty 摘要。
- `build/preview-evidence.md`：预览启动方式、构建 hash、HTTP/browser/console 事实、桌面与移动证据。
- `build/stage-result.md`：变更摘要、命令验证、source verify、residual 与 next。

对 `build/preview-evidence.md` 和 `build/stage-result.md` 执行 `artifact add`。G3 必须绑定当前 build preview revision 和实时 sourceDir hash；之后源码漂移会使批准失效。

## 交接评分

调用 `web-flow-benchmark` 的 build rubric。每轮只处理一个 `top_fix`，最多两轮；HTTP、关键资源、移动内容和控制台等事实性 `must_pass` 未通过时不能伪装成预览成功。
