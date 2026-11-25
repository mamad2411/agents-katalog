---
name: prefer-html-output
description: 当 agent 准备输出长 markdown（周报、PR 评审、方案对比、概念讲解、流程图、设计系统等给人阅读的交付物）时，主动评估是否改用 HTML 渲染。基于 ThariqS/html-effectiveness 的 20 个示例。识别明确高价值场景时询问用户，同意后生成 HTML 文件并自动打开浏览器。
---

# prefer-html-output

让 agent 在合适的场景把"给人看的 markdown 长输出"改用 HTML 渲染，使内容更易消化。基于 Anthropic Claude Code 工程负责人 Thariq Shihipar 的 [html-effectiveness](https://github.com/ThariqS/html-effectiveness) 项目里 20 个真实示例。

## 何时触发本 skill（混合模式）

Agent 在每次准备输出回复时按下面三层依次判断；只在 Layer 2 命中时才打扰用户：

### Layer 1 · 硬性排除（命中任一 → 静默走 markdown）
- 输出会被自动管道消费（写 `.md` 文件、回填 PR/Issue 描述、生成 commit message、写日志等）
- 用户明确要求 markdown / 纯文本
- 短回复（< ~20 行）或对话式问答
- 输出主体是源代码编辑、命令执行、调试输出

### Layer 2 · 高价值场景识别（命中才进入提议环节）

查 `references/scenario-map.md`，看输出意图是否匹配以下任一类。每类后括号是对应示例编号（与 `references/examples/` 中文件名一致）：

| 类别 | 何时命中 | 示例编号 |
|---|---|---|
| 方案/设计对比 | "对比 3 种方案"、"几个设计方向"、"A/B/C 路径" | 01, 02 |
| 实施计划 | "实施路线"、"里程碑 + 时间轴"、"风险表" | 16 |
| 代码审查输出 | "PR 评审报告"、"diff 注释"、"逐文件评论" | 03, 17 |
| 代码理解 / 架构图 | "模块依赖"、"陌生代码包讲解" | 04 |
| 设计系统 / 组件展示 | "色板"、"组件状态总览" | 05, 06 |
| 原型 / 动画 / 交互 | "动画效果"、"点击流程"、"交互草稿" | 07, 08 |
| 图示 / 流程图 | "SVG 图"、"部署流程"、"决策树" | 10, 13 |
| 演示 / 报告 / 讲解 | "幻灯片"、"周报"、"事件复盘"、"概念讲解器"、"功能讲解" | 09, 11, 12, 14, 15 |
| 临时编辑器（少见） | "看板分类"、"feature flag 编辑"、"prompt 调优" | 18, 19, 20 |

### Layer 3 · 提议话术

命中 Layer 2 后用以下格式提议：

> 这块内容比较适合用 HTML 渲染（场景：**{类别名}**，参考示例 **#{编号} {slug}**）。需要我生成 HTML 并在浏览器打开吗？（回复"继续 md"则保持原计划）

- 用户同意 → 进入"生成流程"
- 用户拒绝（"继续 md"/"不用"/否定） → 走原 markdown 计划，本次会话同类场景下次也降低提议频率

## 生成流程

1. **学习风格**：先用 Read 工具读取对应示例文件 `references/examples/NN-*.html`，理解其布局、样式、可视化逻辑。
2. **生成 HTML**：用 Write 工具把完整 HTML（含 `<!DOCTYPE html>`、内联 CSS、必要时内联 JS）写到 `/tmp/<slug>.html`。
   - 不引用外部 CSS/JS 库（除非该示例本身用了 CDN）
   - 优先使用语义化标签（section/article/figure）
   - 中文内容用合适字体栈（`-apple-system, "PingFang SC", ...`）
3. **调用 render.sh**：
   ```bash
   bash ~/.claude/skills/prefer-html-output/scripts/render.sh /tmp/<slug>.html --scenario <key>
   ```
   `<key>` 对照 `references/scenario-map.md` 末尾的"场景关键词 → 编号 快查"表的 scenario key 列。
4. **回复用户**：用一句话告知最终路径（取脚本 stdout）+ 浏览器已打开。

## scenario key 速查

详见 `references/scenario-map.md` 末尾表。常用：

- 周报 → `weekly-report`（落 `文章/YYYY-MM-DD/`）
- 事件复盘 → `incident-report`（落 `文章/`）
- 概念讲解 → `concept-explainer`（落 `文章/`）
- 功能讲解 → `feature-explainer`（落 `文章/`）
- 幻灯片 → `slide-deck`（落 `文章/`）
- 方案对比 → `comparison`（落 `临时/html-output/`）
- 实施计划 → `implementation-plan`（落 `临时/`）
- PR 评审 → `pr-review`（落 `临时/`）
- 设计系统 → `design-system`（落 `临时/`）
- 流程图 → `flowchart`（落 `临时/`）

如不确定，省略 `--scenario` 参数（默认落 `临时/html-output/`）。

## render.sh 参数

```
bash scripts/render.sh <html_file> [--scenario <key>] [--no-open] [--long-term]
```

- `<html_file>`：必填，agent 先写到 `/tmp/` 的 HTML
- `--scenario <key>`：可选，决定归档目录
- `--no-open`：可选，调试用，不调起浏览器
- `--long-term`：可选，强制落到 `常驻文件/html/`（长期保存）

输出：最终绝对路径（stdout 单行）。

## 注意事项

- **绝不在用户没明确同意时直接生成 HTML**：本 skill 默认提议→等回复→执行。
- **生成后必须先读示例**：避免风格漂移、避免空喊"HTML 渲染"实际效果差。
- **用户拒绝就不再坚持**：本次会话同类场景下次降低提议频率。
- **路径决策只走 render.sh**：不要自己拼 `open` 或 `mv`，否则会绕过 CLAUDE.md 目录规则。
