---
name: design-md
description: Author/validate/export Google's DESIGN.md token spec files.
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, design-system, tokens, ui, accessibility, wcag, tailwind, dtcg, google]
    related_skills: [popular-web-designs, claude-design, excalidraw, architecture-diagram]
---

# DESIGN.md 技能

DESIGN.md 是 Google 推出的开放规范（采用 Apache-2.0 许可，文档地址为 `google-labs-code/design.md`），用于向编程智能体描述视觉设计规范。一个 DESIGN.md 文件包含以下两部分：

- **YAML 前置内容**——机器可读的设计令牌（标准化数值）
- **Markdown 正文**——供人类阅读的设计思路，按标准章节组织

设计令牌提供精确的数值，而正文则向智能体解释这些数值的设定依据及应用方法。通过命令行工具（`npx @google/design.md`），可对文件结构与 WCAG 对比度进行校验、对比不同版本以检测功能退化，并将内容导出为 Tailwind 或 W3C DTCG JSON 格式。

## 何时使用此技能

- 用户需要生成 DESIGN.md 文件、设计令牌或设计系统规范
- 用户希望在不同项目或工具中保持一致的 UI/品牌风格
- 用户粘贴现有的 DESIGN.md 文件，要求对其进行校验、对比、导出或扩展
- 用户希望将样式指南转换为智能体可识别的格式
- 用户需要对配色方案进行对比度检测或 WCAG 无障碍性验证

若仅需获取视觉灵感或布局示例，建议使用 `popular-web-designs` 技能。而对于从零开始设计单次使用的 HTML 文件（如原型、演示文稿、着陆页、组件库）时，涉及设计流程与风格选择的问题，则适合使用 `claude-design` 技能。本技能专用于处理正式的设计规范文件本身。

## 文件结构

```md
---
version: alpha
name: Heritage
description: Architectural minimalism meets journalistic gravitas.
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 3rem
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  body-md:
    fontFamily: Public Sans
    fontSize: 1rem
rounded:
  sm: 4px
  md: 8px
  lg: 16px
spacing:
  sm: 8px
  md: 16px
  lg: 24px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.sm}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary}"
---

## Overview

Architectural Minimalism meets Journalistic Gravitas...

## Colors

- **Primary (#1A1C1E):** Deep ink for headlines and core text.
- **Tertiary (#B8422E):** "Boston Clay" — the sole driver for interaction.

## Typography

Public Sans for everything except small all-caps labels...

## Components

`button-primary` is the only high-emphasis action on a page...
```

## Token类型

| 类型 | 格式 | 示例 |
|------|------|---------|
| 颜色 | 任意CSS颜色值（十六进制、`rgb()`、`oklch()`或命名颜色） | `"#1A1C1E"`, `"oklch(62% 0.18 250)"` |
| 尺寸 | 数字 + 单位（`px`、`em`、`rem`） | `48px`, `-0.02em` |
| Token引用 | `{path.to.token}` | `{colors.primary}` |
| 字体样式 | 包含`fontFamily`、`fontSize`、`fontWeight`、`lineHeight`、`letterSpacing`、`fontFeature`、`fontVariation`属性的对象 | 见上表 |

组件属性白名单：`backgroundColor`、`textColor`、`typography`、`rounded`、`padding`、`size`、`height`、`width`。不同状态（悬停、激活、按下）为**独立的组件条目**，其键名具有对应关系（如`button-primary-hover`），而非嵌套结构。

## 标准章节顺序

这些章节并非必须存在，但若存在则应按照此顺序排列。代码检查工具会标记顺序错误的章节（通过`section-order`选项发出警告），同时也会检测重复的标题——根据规范，解析器会自动忽略重复项，因此在返回文件之前需同时修正这两类问题。

1. 概述（别名：品牌与风格）
2. 颜色
3. 字体样式
4. 布局（别名：布局与间距）
5. 凸出度与深度（别名：凸出效果）
6. 形状
7. 组件
8. 正确做法与禁忌

对于未知的章节，系统会保留原样而不会报错。只要值类型有效，未知的Token名称也会被接受。而已知的组件属性若不存在，则会触发警告。

## 工作流程：编写新的DESIGN.md文件

1. **询问用户**（或自行推断）品牌风格、强调色以及字体方向。如果用户提供了网站链接、图片或整体氛围描述，需将其转化为上述的标记格式。
2. 使用 `write_file` 函数在项目根目录中创建 `DESIGN.md` 文件。该文件必须包含 `name:` 和 `colors:` 两项内容；其他部分虽非必需，但建议一并添加。
3. 在 `components:` 部分使用标记引用（如 `{colors.primary}`）来代替手动输入十六进制值，从而确保配色方案来自单一来源。
4. 对文件进行代码检查（详见下文）。在返回结果之前，需修复所有无效的引用或违反 WCAG 标准的问题。
5. **如果用户已有项目**，还需在该文件旁生成 Tailwind 或 DTCG 导出文件（如 `tailwind.theme.json`、`tokens.json`）。

## 工作流程：代码检查 / 对比差异 / 导出

该工具的 CLI 命名为 `@google/design.md`（基于 Node 环境）。可直接使用 `npx` 调用，无需全局安装。

```bash
# Validate structure + token references + WCAG contrast
npx -y @google/design.md lint DESIGN.md

# Compare two versions, fail on regression (exit 1 = regression)
npx -y @google/design.md diff DESIGN.md DESIGN-v2.md

# Export to Tailwind v3 theme JSON (`tailwind` is a back-compat alias)
npx -y @google/design.md export --format json-tailwind DESIGN.md > tailwind.theme.json

# Export to a Tailwind v4 CSS @theme block (--color-*, --text-*, --radius-*, ...)
npx -y @google/design.md export --format css-tailwind DESIGN.md > theme.css

# Export to W3C DTCG (Design Tokens Format Module) JSON
npx -y @google/design.md export --format dtcg DESIGN.md > tokens.json

# Print the spec itself — useful when injecting into an agent prompt
npx -y @google/design.md spec --rules-only --format json
```

所有命令均支持使用 `-` 指定标准输入。`lint` 命令在检测到错误时会返回退出码 1（仅警告则返回 0）。无论源代码中是否存在 `lint` 检测到的问题，`export` 命令在成功导出时都会返回 0 —— 若需针对这些问题进行过滤，请单独运行 `lint` 命令。输出结果默认为 JSON 格式；若需要以结构化方式呈现检测结果，则需对其进行解析。

在 Windows 系统上，`design.md` 这一命令名可能会与 `.md` 文件的默认关联冲突（此时要么无任何反应，要么文件会在编辑器中打开）。建议使用不含点号的别名：`npx -y -p @google/design.md designmd lint DESIGN.md`。

### `lint` 规则参考（截至 CLI 0.3.0 版本的 9 条规则）

- `broken-ref`（错误）—— `{colors.missing}` 指向了并不存在的色值标识
- `contrast-ratio`（警告）—— 组件的 `textColor` 与 `backgroundColor` 对比度未达到 WCAG AA 标准（要求为 4.5:1）
- `missing-primary`（警告）—— 已定义了颜色，但缺少 `primary` 色值标识
- `missing-typography`（警告）—— 已定义了颜色，但缺少与排版相关的色值标识
- `orphaned-tokens`（警告）—— 存在未被任何组件引用的色值标识
- `section-order`（警告）—— 各部分顺序不符合规范要求
- `unknown-key`（警告）—— 顶层 YAML 键似乎是架构键的拼写错误（如 `colours:` 应为 `colors:`）；自定义扩展键则不会触发该警告
- `token-summary`、`missing-sections`（信息）—— 显示各色值标识的数量以及缺失的可选部分

如果用户关注无障碍性，应在总结中明确提及相关检测结果 —— WCAG 标准检测结果是使用该 CLI 工具的最重要依据。

## 常见问题与注意事项

- **不得嵌套组件变体。** `button-primary.hover` 的写法是错误的；
  正确的做法是将 `button-primary-hover` 作为同级键使用。
- **十六进制颜色值必须用引号包裹。** 否则 YAML 解析器会因 `#` 符号而出错，
  或对类似 `#1A1C1E` 这样的颜色值进行异常截断。
- **负数值尺寸同样需要加引号。** `letterSpacing: -0.02em` 会被视为 YAML 的流式结构——
  应将其写为 `letterSpacing: "-0.02em"`。
- **尽管代码检查工具仅会发出警告，但各部分的顺序依然很重要。** 如果用户提供的文本内容顺序混乱，
  在保存之前请先按规范顺序重新排列——符合规范的工具会要求如此。
- **排版相关子属性的拼写错误会被直接忽略。** 自 CLI 0.3.0 版本起，
  如 `fontwight:` 这样的拼写错误不会被检测到，且对应的值也会从输出结果中消失——
  请务必根据规范核对子属性名称（`fontFamily`、`fontSize`、`fontWeight`、`lineHeight`、`letterSpacing`、`fontFeature`、`fontVariation`）。
- **当前规范的版本为 `version: alpha`**（截至 2026 年 7 月，CLI 0.3.0 版本）。该规范仍处于测试阶段，需注意可能出现的破坏性变更。
- **令牌引用通过点号路径来解析。** `{colors.primary}` 的写法有效；
  而 `{primary}` 则无效。

## 规范的权威来源

- 代码仓库：https://github.com/google-labs-code/design.md（Apache-2.0 许可证）
- CLI 工具：npm 上的 `@google/design.md`
- 生成的 DESIGN.md 文件的许可证：遵循用户项目所使用的许可证规范；
  而规范本身采用 Apache-2.0 许可证。
