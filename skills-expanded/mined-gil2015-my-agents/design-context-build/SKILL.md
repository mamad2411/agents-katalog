---
name: design-context-build
description: 当需要从项目代码、开发者补充、设计资源目录或用户口述中提炼 AI 可消费的项目设计规范/主题上下文文档，并供后续 UI 开发沿用时使用
---

# 设计上下文构建

## 概述

从项目代码、开发者手填信息、设计资源目录和当前轮文字描述中，提炼出 AI 可消费的 `design-context.md`，并按需补充 `component-catalog.md`。目标不是“总结设计稿”，而是沉淀一份全项目共用的设计基线，让后续 `ui-dev` 复用真实主题、token 和全局组件，而不是临场新写一套。

**核心原则：** 优先沉淀已验证的设计事实，不发明一套不存在的设计系统。

**违反规则的字面意思就是违反规则的精神。**

## 适用场景

**必须使用：**
- UI 开发经常重写一套新样式，没有沿用项目现有主题和组件
- 新项目刚开始，需要先把设计规范录入给 AI
- 已有设计规范文件、截图或资源目录，但缺少 AI 可消费的结构化文档
- 希望先沉淀一份全项目共用的设计基线，再让多个需求任务复用

**例外情况（需征询开发者）：**
- 一次性演示页或 PoC，不会沉淀为正式项目资产
- 项目已经存在可用且最新的 `design-context.md`，本轮也没有新增设计约束

觉得“设计风格看一眼代码就知道了”？停下来。AI 不会长期记住这些隐性约束，必须写成文档。

## 铁律

```text
PREFER VERIFIED DESIGN SOURCES - NEVER INVENT A DESIGN SYSTEM
```

没有证据支持的设计结论，只能标记为 `inferred` 或 `open_question`；绝不能伪装成项目既有规范。

## 产物

固定产物：

- 项目级基线：`{projectRoot}/.ai/docs/design-context.md`
- 可选组件清单：`{projectRoot}/.ai/docs/component-catalog.md`

规则：
- 所有需求任务共用同一份项目级设计基线
- 不在 mission 目录下重复维护设计规范或组件清单
- `ui-dev` 读取顺序固定为项目级基线
- 组件清单不是独立 skill；默认由本 skill 在同一次扫描中按需生成
- 组件清单只记录项目全局组件与 npm 安装组件，不记录业务模块级组件

## 正式支持的主题实现

当前优先识别以下主题实现方式：

- `css_vars`：通过 CSS Variables 定义颜色、字号、间距等设计 token
- `js_tokens`：通过 JS / TS theme 对象定义 token，并交给 `ConfigProvider` 或自定义 Provider 消费
- `mixed`：同时存在 CSS Variables 与 JS / TS token，且都在真实运行链路中生效
- `unknown`：无法确定主题接入方式，或当前项目未形成稳定主题体系

如果项目使用了其他方式，不要强行归类；记录真实接入路径，并标为 `unknown` 或 `mixed`。

针对 `css_vars`：
- 必须保留项目里的真实变量名和前缀，例如 `--m9-color-primary`
- 不要为了“统一语义”把前缀抹掉后重命名

针对 `js_tokens`：
- 重点记录真实 theme object 字段、Provider 入口和 token 消费方式
- 不额外要求人为补 CSS Variable 前缀映射

## 执行流程

1. `LOAD`：读取 `projectRoot`、历史设计文档、代码证据、资源目录和当前轮补充输入。
2. `DETECT`：识别主题接入方式、Provider 入口、token 文件和样式入口。
3. `EXTRACT`：提炼 token 映射、组件复用约束、布局模式、样式限制和禁用模式。
4. `MERGE`：按证据等级合并冲突信息，沉淀为项目级基线。
5. `PREVIEW`：若目标文档已存在，先生成拟更新草稿与变更摘要，等待用户确认。
6. `OUTPUT`：仅在用户明确同意后写入 `design-context.md` / `component-catalog.md`。

## 第 1 步：LOAD - 读取设计上下文来源

优先读取以下信息：
- `projectRoot`：当前项目根目录；这是主输入，不依赖 mission 才能运行
- 可选 `.ai/missions/{missionId}/config.json`：仅用于辅助获取 `projectRoot`、`componentRoot`、`uiLibPackage`
- 现有项目级 `design-context.md` 与 `component-catalog.md`
- 开发者补充的设计说明、品牌规范、组件使用说明
- 指定资源目录中的设计规范文件、图片、截图、标注文档
- 目标项目中的主题定义代码、Provider 入口、全局组件封装
- 当前轮用户口述的设计意图或限制

必须先确认：
- 本轮是否需要更新项目级设计基线、项目级组件清单，还是只更新其中之一
- 设计来源是否真实存在；缺失路径不能被静默忽略
- 项目是否已经有稳定主题入口，还是仍处于“开发者手填优先”的早期阶段
- 是否存在历史文档；如果存在，必须增量更新而不是整份重写
- 如果目标文档已存在，本轮是否只是补充、还是需要覆盖既有内容

**至少执行：**
- `test -d "{projectRoot}"`
- `test -d "{projectRoot}/.ai" || true`
- `test -f "{projectRoot}/.ai/docs/design-context.md" || true`
- `test -f "{projectRoot}/.ai/docs/component-catalog.md" || true`

**若上下文来自 mission 目录，可额外执行：**
- `test -f ".ai/missions/{missionId}/config.json"`
- `find ".ai/missions/{missionId}" -maxdepth 3 -type f | sort`

**若需要从项目代码提取设计规范，至少执行：**
- `rg -n "ConfigProvider|token\\s*:|theme\\s*:|createTheme|ThemeProvider|--[A-Za-z0-9-]+" "{projectRoot}"`
- `rg -n ":root|html|body|data-theme|var\\(--" "{projectRoot}"`
- `rg -n "export .* from|export \\{|components?/|widgets?/|Page|Table|Form|Modal" "{projectRoot}/src"`

## 第 2 步：DETECT - 识别主题接入方式

重点识别以下事实：
- 当前项目主主题模式是 `css_vars`、`js_tokens`、`mixed` 还是 `unknown`
- `ConfigProvider` 或自定义 Provider 的真实入口文件与组件路径
- token 定义文件、全局样式入口、运行时主题切换入口
- CSS Variables 是否存在统一前缀，例如 `--m9-`
- 是否存在“旧主题文件仍在仓库里，但已不再生效”的历史残留

规则：
- 只记录真实运行链路上的主题接入方式，不把弃用代码当现行规范
- 如果项目同时存在多个主题来源，优先记录当前业务页面实际走到的那条链路
- 无法确认生效顺序时，保留为 `open_question`，不要擅自合并

## 第 3 步：EXTRACT - 提炼 AI 可执行的设计约束

`design-context.md` 至少需要覆盖：
- 主题接入方式：Provider、token 文件、样式入口、当前生效链路
- token 映射：颜色、字号、间距、圆角、阴影、层级、动效
- 组件复用约定：优先复用哪些全局组件、哪些场景可以回退到 UI 库、哪些情况才允许新增本地组件
- 组件清单：高复用全局组件、npm 安装组件、导入路径、适用场景、禁止重复封装的模式
- 页面/布局约定：容器、区块、表单、表格、卡片、空态、错误态、操作区等常见模式
- 样式实现约束：什么时候必须使用 token / CSS Variables，什么时候允许局部样式
- 禁止事项：硬编码视觉 token、绕过 Provider、重复封装项目已有组件等

提炼规则：
- 找到真实 token 时，记录具体变量名、字段名或组件名
- 对 CSS Variables 记录真实前缀，例如 `--m9-`，不要只保留语义后半段
- 对组件只记录最小必要使用信息，不展开完整 props 说明
- 组件清单只记录两类组件：项目全局组件、npm 安装组件
- 找不到数值但能确认语义时，先记录语义约束和来源
- 截图、图片或口述只能用于补充视觉意图，不能覆盖代码中已验证的主题事实

## 第 4 步：MERGE - 合并多来源信息并标注证据

每条设计结论都要标注证据等级：

- `code_verified`：来自当前项目已生效代码
- `doc_verified`：来自明确的设计规范文档或开发者填写文档
- `user_provided`：来自当前轮用户/开发者口述
- `inferred`：基于有限证据推断得出

冲突处理规则：
- 项目级基线默认以 `code_verified` 优先，其次是 `doc_verified`、`user_provided`、`inferred`
- 如果多个来源冲突且无法判断谁是现行规范，不要强行给出单一结论；保留冲突说明与 `open_question`

## 第 5 步：PREVIEW - 先展示拟覆盖内容

若目标文档不存在，可直接进入 `OUTPUT`。

若目标文档已存在，不得直接覆盖。必须先展示：
- 即将写入的目标路径
- 主要新增 / 删除 / 替换点
- 至少一份拟覆盖文档的关键内容预览；如改动较大，应提供完整草稿

**硬约束：**
- 未获用户明确同意前，不写任何文件
- 未获用户明确同意前，只能在回复中展示草稿，不得落盘到 `.ai/docs/` 或其他临时文件

## 第 6 步：OUTPUT - 写入设计上下文文档

使用 `../../references/doc-templates/design-context-template.md` 与 `../../references/doc-templates/component-catalog-template.md` 作为模板，生成或更新：

1. 项目级基线：`{projectRoot}/.ai/docs/design-context.md`
2. 可选项目级组件清单：`{projectRoot}/.ai/docs/component-catalog.md`

写入要求：
- 顶部必须写清 `Theme Mode`、来源摘要和文档状态
- 每条关键规则都要能追溯到代码、文档、资源目录或用户输入
- 已有条目优先增量更新，不随意打乱现有结构
- 若设计信息仍不充分，输出“已确认事实 + 未确认问题”，不要补齐一套虚构规范
- 只有在用户明确同意后，才允许覆盖 `.ai/docs/` 下已存在的文档
- 若用户未同意覆盖，则保留旧文档，不做任何写入

## 速查表

| 阶段 | 关键动作 | 完成标准 |
|------|---------|---------|
| LOAD | 读取项目根目录、历史文档和多来源设计资料 | 明确本轮产物范围与可用来源 |
| DETECT | 识别主题模式与真实生效链路 | 能说明 token 从哪里定义、在哪里生效 |
| EXTRACT | 提炼 token、组件、布局和样式约束 | `ui-dev` 可直接复用，不必二次猜测 |
| MERGE | 按证据等级合并冲突信息 | 所有推断项都被显式标注 |
| PREVIEW | 展示拟覆盖内容 | 用户能在写入前审阅主要改动 |
| OUTPUT | 增量更新 `design-context.md` | 产物可被项目级 UI 开发直接消费 |

## 常见借口

| 借口 | 现实 |
|------|------|
| “主题文件太多了，先随便挑一个” | 先确认真实运行链路，不然会把废弃规范继续传播 |
| “这颜色肉眼看差不多” | 视觉接近不代表 token 相同，AI 需要明确 token 名或变量名 |
| “先写成一套完整规范，后面再修” | 一旦写成文档，后续 skill 会把它当真 |
| “用户说想要蓝一点，那就改项目主题” | 当前轮口述不一定代表项目长期基线，先确认是否真要更新项目规范 |
| “旧文档我先直接改了再说” | `.ai` 不在 git 里，覆盖前必须先给用户看拟修改内容并征得同意 |

## 危险信号 - 立即停下来

- 你在没有代码或文档证据时，写出了完整颜色/字号/spacing 体系
- 你把截图里的视觉印象当成已生效的主题实现
- 你发现仓库里有多个主题入口，却没有核实哪一个真的在运行
- 你把业务模块级组件写进了 `component-catalog.md`
- 你在未获同意前就准备覆写 `.ai/docs/` 下的现有文档

## 参考文档

| 主题 | 文件 |
|------|------|
| 通用规则 | `../../references/rules/common-rules.md` |
| 设计上下文模板 | `../../references/doc-templates/design-context-template.md` |
| 组件清单模板 | `../../references/doc-templates/component-catalog-template.md` |

## 集成关系

- **主消费方：** `step2-ui-dev`
- **可选触发者：** 开发者手动调用、orchestrator 在明确需要设计上下文时建议调用
- **非阻塞说明：** 缺少 `design-context.md` 不阻塞 `step2-ui-dev`，但 `step2-ui-dev` 必须显式说明设计上下文缺口
