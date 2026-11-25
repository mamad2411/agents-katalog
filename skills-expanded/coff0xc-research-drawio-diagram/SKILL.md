---
name: coff0xc-research-drawio-diagram
description: "Use when / 当用户请求 draw.io、diagrams.net、.drawio、科研图、论文方法图、architecture/method/model diagram、algorithm pipeline、Transformer/CNN/GNN/diffusion/RAG/agent 架构图。绘制前需要 paper/arXiv/official GitHub/docs 或用户来源。手动触发：使用 coff0xc-research-drawio-diagram。"
---

# coff0xc-research-drawio-diagram

<!-- skill-id: cs-rdd-0f8d6e2b -->

## 快速规则（日常任务先读这里）
> **[证据先行]** 论文、官方仓库、README、代码或实验材料先定位；未知结构不能编造。
> **[图可编辑]** 默认交付 `.drawio`/diagrams.net 可编辑结构，不只给截图或口头描述。
> **[结构门禁]** 节点、边、层次、数据流、训练/推理/实验阶段必须能回到来源证据。
> **[硬边界]** 未公开论文、私有数据、专利/投稿敏感材料和外部发布先确认。

普通科研/算法图任务按本节先推进；只有论文级重构、复杂系统图或审稿级说明时再展开完整工作流。

## 能力定位
面向论文、算法、模型和研究流程的可编辑 draw.io 图生成能力。重点是交付可继续编辑的 `.drawio` 源文件，并把图中元素和公开证据对应起来。

## 能交付什么
- 可编辑 `.drawio` 文件
- 图结构 JSON/spec 或模块清单
- 证据表：论文段落、公式、图号、代码路径、官方文档
- 未确认推断边和不确定项说明

## 可以接收什么输入
- 论文 PDF/arXiv/OpenReview、官方 GitHub、项目文档
- 模型结构、算法 pipeline、实验流程、训练/推理说明
- 已有草图、截图、Mermaid 或图形要求

## 放心使用的边界
- 可直接基于用户材料和公开来源整理图
- 需要联网查论文/仓库时标注来源和证据等级
- 不把推断连接伪装成论文原文事实
- 默认只处理本地、可逆、可验证的低风险工作；涉及生产、凭据、付费、远程写入、删除、发布或权限变更时必须先确认。

## 为什么可以放心
- 优先生成 draw.io 可编辑源文件，不只给 PNG/Mermaid
- 图中关键模块要能追溯到证据
- 训练路径、推理路径和指标分层标注

## 典型使用方式
```text
使用 coff0xc-research-drawio-diagram 根据论文和官方 GitHub 画一个可编辑 draw.io 方法图。
使用 coff0xc-research-drawio-diagram 把 Transformer 论文方法整理成 .drawio 模型结构图。
Use coff0xc-research-drawio-diagram to create an editable diagrams.net method figure with evidence notes.
```

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## 按需展开
- 日常任务只执行上面的快速规则、能力边界和典型用法，不默认读取完整门禁。
- 深度架构、复杂多阶段、质量评测、发版、正式交付或当前任务证据不足时，再读取 `references/full-workflow.md`。
- 读取 reference 后仍保持最小必要上下文；不要因为 reference 存在就输出长篇流程或额外自证材料。
