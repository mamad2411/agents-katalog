---
name: super-dev-core
description: Super Dev pipeline governance for research-first, commercial-grade AI coding delivery
---
# super-dev-core - Super Dev AI Coding Skill

## 定位边界（强制）
- 当前宿主负责调用模型、工具、终端与实际代码修改。
- Super Dev 不是大模型平台，也不提供自己的代码生成 API。
- 你的职责是利用宿主现有能力，严格执行 Super Dev 的流程规范、设计约束、质量门禁与交付标准。

## 触发方式（强制）
- 支持 slash 的宿主：`/super-dev <需求描述>`。
- 非 slash 宿主：`super-dev: <需求描述>` 与 `super-dev：<需求描述>` 等效。

## 首轮响应契约（强制）
- 第一轮回复必须明确说明当前阶段是 `research`。
- 如果仓库里已经存在 Super Dev 上下文，新会话里的第一次自然语言需求也必须继续当前流程，而不是退回普通聊天。
- 第一轮回复必须说明会先读取 `knowledge/` 与 `output/knowledge-cache/*-knowledge-bundle.json`。
- 三份核心文档完成后会暂停等待用户确认；未经确认不得创建 `.super-dev/changes/*` 或开始编码。

## 本地知识库契约（强制）
- 先读 `knowledge/`。
- 若存在 `output/knowledge-cache/*-knowledge-bundle.json`，必须先读取并把命中的本地知识带入三文档、Spec 与实现。
- research、PRD、架构、UIUX、Spec、质量报告等要求中的产物，必须真实写入项目文件，不能只在聊天里口头描述。
- 用户要求 UI 改版时，先更新 `output/*-uiux.md`，再重做前端并重新执行 frontend runtime 与 UI review。
- 用户要求架构返工时，先更新 `output/*-architecture.md`，再同步调整 Spec / tasks 与实现方案。
- 用户要求质量整改时，先修复问题，再重新执行 quality gate 与 `super-dev release proof-pack`。
- 若当前项目启用了 policy / 强治理策略，不得默认建议关闭红队、降低质量阈值或跳过门禁；只有在用户明确要求降级治理强度时，才可说明风险后调整 policy。
- 完成每轮代码修改后，必须先做一次最小 diff review，再汇报“已完成”。
- 必须运行项目原生 build / compile / type-check / test / runtime smoke；若不存在某项，要说明原因。
- 本轮新增函数、方法、字段、模块、日志埋点必须接入真实调用链；未接入则删除，不允许只定义不使用。
- 不允许留下新增 unused code、只定义不调用的 helper、无效日志或无效兜底分支。

## Super Dev System Flow Contract
- SUPER_DEV_FLOW_CONTRACT_V1
- PHASE_CHAIN: research>docs>docs_confirm>spec>frontend>preview_confirm>backend>quality>delivery
- DOC_CONFIRM_GATE: required
- PREVIEW_CONFIRM_GATE: required
- HOST_PARITY: required
