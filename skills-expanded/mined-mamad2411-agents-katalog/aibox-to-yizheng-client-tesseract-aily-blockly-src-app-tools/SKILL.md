# x-dialog/
> L2 | 父级: /mnt/c/Users/sam/Documents/Sam/code/Tesseract/aily-blockly/src/app/tools/aily-chat/components/AGENTS.md

成员清单
aily-chat-code.component.ts: aily-* 代码块分发器，把 markdown block 折叠到对应 viewer。
x-dialog.component.ts: 聊天消息壳，承载消息流、thinking 状态和 markdown 渲染。
x-aily-dialogue-mode-viewer/: 对话模式主卡片 viewer，展示 skill / hardware / action / handoff。
x-aily-button-viewer/: 操作按钮 viewer，承接 aily-button JSON block，并在硬件端口确认时渲染 backend 下发的接口选择。
x-aily-state-viewer/: 统一状态条 viewer。
x-aily-config-guide-viewer/: 配置引导 viewer，负责说明当前节点与接口选择提示。
x-aily-workflow-blueprint-viewer/: 工作流蓝图 viewer。
x-aily-component-recommendation-viewer/: 组件推荐 viewer。
x-aily-mermaid-viewer/: 流程图 viewer。

法则
- `aily-chat-code.component.ts` 是唯一 block 注册入口，viewer 只做纯展示。
- 对话模式主卡片必须独立成 viewer，不能塞回 `x-dialog.component.ts` 的消息壳。
- 新 viewer 若需要动作，先通过 `aily-chat-action` 事件和现有容器约定对齐，不在组件里偷偷改状态机。
- hardware_port 接口表只从 backend `interaction.options` 下发，任何 viewer 都不允许私自复制一份端口常量或 mock 插入逻辑。

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
