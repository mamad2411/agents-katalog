---
name: one-slide
description: "直接把单页 Markdown 提示词、自然语言或附件实现为恰好一页原生可编辑 PowerPoint；不要求 JSON 页面规格。"
license: Apache-2.0
metadata:
  author: "周俊东 Marco"
  version: "2.5.4"
---

# OneSlide

Markdown 提示词是默认且完整的公开交接接口。接收用户当前提供或修改的 MD，直接理解设计并用原生 PowerPoint 对象施工；不得先调用 Deck Foundry 把完整提示词重新转换成 effective-page-spec，也不得要求伴随 JSON、来源哈希或对象注册表。文件标题和章节顺序不限，不要求用户套表。

只处理一页并交付一个原生可编辑 PPTX。多页 MD 中已指定页码时读取公共要求和该页；未指定且不能从对话推导时只询问页码。整册制作由外部编排逐页调用，不把整册塞进一页。

## 按需读取

- 默认入口：`references/input-contract.md`、`references/markdown-input.md`、`references/content-placement.md`、Bridge / Implementer / Verifier 各自的 `ENGINE.md`。
- 稀疏输入需要补充构图、处理未指定视觉细节或明确重设计时：`references/visual-reference.md`；完整设计直接实施，不重新选版。
- 即将生成或检查 PPTX：`references/presentation-runtime-contract.md`。
- 只有用户明确提供历史 effective-page-spec-2.2 JSON：读取 `references/legacy-json-runtime.md` 和 `references/effective-page-spec-input.md`；无需内容重分配时复用已有 consumer，需要迁移时按内容位置合同直接原生施工。旧 JSON 的存在不能覆盖本轮 MD；没有 JSON 不能成为阻断理由。

## 默认生产路径

用户 MD → Bridge 理解任务、页界与锁定内容 → Implementer 直接原生施工 → Verifier 对照同一 MD 检查。

Agent 负责理解自然语言和设计，脚本负责绘图、导出和机械检查。实现过程可以使用内存对象、图表数据或临时检查文件，不新增必须跨 Skill 传递的结构化规格。MD 必须在没有历史会话、内部 JSON 或本机路径的条件下可用。

读取完整提示词后，区分页面可见文案、讲者备注、设计指令和语义依据。保留全部明确事实、数据、单位、口径、标题、图形关系、颜色、图标与正文责任。不能为适配旧模块而改成卡片或文字列表；不能因去重而擅自删改用户锁定文案。设计指令不能当正文上屏。资料核验、模拟性质等附加边界说明按 `references/content-placement.md` 默认集中到讲者备注；完整保留是保留信息和对应对象，不要求这些说明原位上屏。计算条件、业务状态、必要口径和结论的不确定措辞仍属正文。

## 文字与旁置图标

默认标题、正文及强调文字均使用常规字重，以字号、间距和颜色区分层级，不自动加粗。文字旁的修饰图标按可见图形高度至少为对应文字可见字高的1.5倍，并让两者光学中心处在同一水平线上。具体量尺、执行及检查见 `references/markdown-input.md`；当前用户要求覆盖旧提示词或旧构建代码中的冲突样式。

## 原生施工

本 Skill 是本轮唯一演示创作规则，不加载通用 Presentations 的创作规则。通过运行时合同获取 `@oai/artifact-tool`，复用 `implementer/scripts/pptx_core.mjs`、现有图表模块、图标解析器、文本可编辑性修正及布局检查。

Agent 根据 MD 在内部运行目录编写本页构建代码；直接使用原生文字、形状、图表和连接，不生成完整 effective-page-spec。可调用 `implementer/scripts/render_markdown.mjs` 执行该代码，输入仍是原 MD。构建代码属于本地施工实现，不交给用户填写或作为下一次输入。

用户未指定的坐标、字号、间距和折行由 Implementer 求解；已明确的版式和视觉含义必须保持。三种既有画布 16:9、9:16、3:4 继续支持。完整提示词无需重新设计；稀疏意图可用上下文、默认值和可撤销假设补齐，只有事实冲突、任务不可识别、授权缺口或单页无法容纳才询问或报告具体问题。

图标继续使用 OneSlide 语义图标解析器及其授权资产；普通关系图形可用原生形状，不能冒充图标库图标。具体图标缺失时执行已声明 fallback，不得默默删去。图表保持原生可编辑，不以整页位图替代。

## 验证与交付

以当前 MD 为验收依据检查：内容、数据与口径；对象位置、方向、分组、焦点和颜色；正文与备注的分配及迁移覆盖，不把已迁移的附加说明补回画布；图标；原生对象；越界、重叠、可读性及单页数量。逐项对照实际页面确认视觉关系与内容忠实，发现差异后修复并复查受影响对象。

修改 MD 后重新按修改后的文件施工，旧缓存和 JSON 无权推翻它。预览、构建代码、布局数据和检查报告放内部目录；最终交付 PPTX。保存后主动在 PowerPoint 中查看画布与备注，并按任务检查原生编辑；发现重叠、遗漏或编辑障碍时修复、保存并重新打开复查。工具确实不可用且现有恢复路径无效时，交付已完成文件，说明具体受影响的使用项和恢复检查的下一步。交付先说明完成内容、可编辑对象和实际检查结果，保留会影响使用的必要条件。
