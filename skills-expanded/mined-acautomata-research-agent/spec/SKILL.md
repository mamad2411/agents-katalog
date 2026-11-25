---
name: spec
description: spec — Translate validation designs (from design's output) into a claude-code task prompt. Triggers: 生成任务提示词, spec, claude-code task, claude-code 提示词, 实现规格.
---

# spec — claude-code 验证任务提示词生成

## Mission

将验证实验设计（`design` 产出）翻译成 claude-code 可直接执行的工程任务提示词，产出标题为 `# 发给 claude-code 的完整任务提示词` 的完整 Markdown 文档。

## When to use

- 已有 `design` 验证实验设计，需要转成 claude-code 可执行任务
- 用户请求"生成实现规格""写 claude-code 提示词"

不要用于：验证设计本身（`design`）、问题分析（`critic`）。

## 前置依赖

需要 `design` 的验证实验设计文档已存在（通常在 wiki 里）。若缺失，先运行 `design`（而 `design` 又需要 `critic`）。

## 输入

| 材料 | 必需 |
|------|------|
| `critic` 问题分析文档 | 是 |
| `design` 验证实验设计文档 | 是 |
| 论文基础 Wiki 文档 | 可选（背景） |
| 代码仓库路径或结构说明 | 可选 |

## 生成原则

1. 面向 claude-code，语言直接、工程化，不输出论文总结。
2. 把科研目标翻译成编码任务（配置开关、实验 runner、对照入口、消融逻辑、结果保存、批量脚本）。
3. 强调最小侵入：只做验证所需的最小改动，优先复用现有代码结构，配置化控制变量，结果可保存。
4. 论文描述、实验设计和代码实现不一致时，要求 claude-code 在最终汇报中指出。
5. 路径或文件名未提供时使用占位符，不臆造。

## 缺失信息占位符

- `此处应填写代码仓库路径`
- `此处应填写论文基础 Wiki 标识`
- `此处应填写训练入口文件路径`
- `请根据仓库结构自行定位`

若 `design` 中没有明确优先级，提示 claude-code 优先选择：最小改动、最容易控制变量、最直接对应核心问题、最容易保存和比较结果的实验。

## 输出结构

先输出为一份完整 md，写到 `raw/sources/<slug>.md`，然后调用 `ingest`（传入该 md 文件路径，`page_type: analysis`）统一写入 wiki；**不直接调用 `wiki_apply` 建页**。标题必须为 `# 发给 claude-code 的完整任务提示词`，标题下空一行写入 `` `category: spec` ``（作为可机读类别标识，供外部统计脚本提取），包含：

1. 任务背景
2. 可用输入材料
3. 当前论文方法与验证目标
4. 优先实现的验证实验（至少 3 个）
5. 总体实现要求（最小侵入、优先复用、配置化控制、结果可保存）
6. 建议优先查看的代码位置
7. 交付内容
8. 完成标准
9. claude-code 完成后的汇报格式

## 完成门禁

- 文件级别具体，无未填充的占位符（除非确实缺失）
- 聚焦实现任务，不含论文总结正文
- 产出 md 已经 `ingest` 写入 wiki（含 wiki 路径），且本 skill 未直接调 `wiki_apply` 建页
- 产出 md 在 `# Title` 下空一行包含 `` `category: spec` ``（作为可机读类别标识，供外部统计脚本提取）
