---
name: dogfood
description: "Exploratory QA of web apps: find bugs, evidence, reports."
version: 1.0.0
author: Teknium (teknium1), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [qa, testing, browser, web, dogfood]
    related_skills: []
---

# Dogfood：系统化的Web应用程序质量检测

## 概述

本技能指南将指导您使用浏览器工具集对Web应用程序进行系统化的探索式质量检测。您将操作应用程序、与界面元素交互、收集问题证据，并生成结构化的缺陷报告。

## 先决条件

- 必须具备浏览器工具集（`browser_navigate`、`browser_snapshot`、`browser_click`、`browser_type`、`browser_vision`、`browser_console`、`browser_scroll`、`browser_back`、`browser_press`）
- 需要用户提供目标URL及测试范围

## 输入参数

用户需提供以下信息：
1. **目标URL** —— 测试的入口地址
2. **测试范围** —— 需要重点检测的区域/功能（如需全面测试则选择“整个网站”）
3. **输出目录**（可选）—— 截图和报告的保存路径（默认值为`./dogfood-output`）

## 工作流程

请按照以下5个阶段的系统化流程操作：

### 第1阶段：规划

1. 创建输出目录结构：
   ```
   {output_dir}/
   ├── screenshots/       # Evidence screenshots
   └── report.md          # Final report (generated in Phase 5)
   ```
2. 根据用户输入确定测试范围。  
3. 通过规划需要测试的页面和功能来构建初步的站点地图：  
   - 首页/主页  
   - 导航链接（页头、页脚、侧边栏）  
   - 关键用户流程（注册、登录、搜索、结账等）  
   - 表单与交互元素  
   - 边界情况（空状态、错误页面、404错误页）  

### 第二阶段：探索  

针对计划中的每个页面或功能：  

1. **导航**至该页面：
   ```
   browser_navigate(url="https://example.com/page")
   ```

2. **生成快照**以了解 DOM 结构：
   ```
   browser_snapshot()
   ```

3. 检查控制台是否存在 JavaScript 错误：
   ```
   browser_console(clear=true)
   ```
每次页面跳转以及发生任何重要交互后都应执行此操作。无声的 JavaScript 错误属于极具价值的发现线索。

4. **截取带注释的屏幕截图**，以便直观查看页面内容并识别各类交互元素：
   ```
   browser_vision(question="Describe the page layout, identify any visual issues, broken elements, or accessibility concerns", annotate=true)
   ```
`annotate=true` 参数会在交互元素上叠加带编号的 `[N]` 标签。每个 `[N]` 都会对应一个引用 `@eN`，以便后续在浏览器中执行相应命令。

5. **系统地测试交互元素**：
   - 点击按钮和链接：`browser_click(ref="@eN")`
   - 填写表单：`browser_type(ref="@eN", text="test input")`
   - 测试键盘导航功能：`browser_press(key="Tab")`、`browser_press(key="Enter")`
   - 滚动页面内容：`browser_scroll(direction="down")`
   - 使用无效输入测试表单验证功能
   - 测试空数据提交情况

6. **每次交互完成后**，需检查以下内容：
   - 控制台错误信息：`browser_console()`
   - 页面视觉变化：`browser_vision(question="交互后发生了哪些变化？")`
   - 实际行为与预期行为的差异

### 第三阶段：收集证据

对于发现的每一个问题：

1. **截取显示该问题的屏幕截图**：
   ```
   browser_vision(question="Capture and describe the issue visible on this page", annotate=false)
   ```
请从响应中保存 `screenshot_path`——您将在报告中引用该路径。

2. **记录详细信息**：
   - 问题出现的网址
   - 复现步骤
   - 预期行为
   - 实际行为
   - 控制台错误（如有）
   - 截图路径

3. 根据问题分类法对问题进行分类（详见 `references/issue-taxonomy.md`）：
   - 严重程度：严重 / 高 / 中 / 低
   - 类别：功能异常 / 视觉问题 / 无障碍性问题 / 控制台错误 / 用户体验问题 / 内容问题

### 第4阶段：分类处理

1. 审核所有收集到的问题。
2. 去重——合并那些在不同位置出现的相同缺陷。
3. 为每个问题确定最终的严重程度和类别。
4. 按严重程度排序（先严重，再高、中、低）。
5. 按严重程度和类别统计问题数量，以便生成执行摘要。

### 第5阶段：生成报告

使用 `templates/dogfood-report-template.md` 中的模板来生成最终报告。

报告必须包含以下内容：
1. **执行摘要**，说明问题总数、按严重程度划分的情况以及测试范围。
2. **每个问题的详情部分**，包括：
   - 问题编号和标题
   - 严重程度和类别标签
   - 问题出现的网址
   - 问题描述
   - 复现步骤
   - 预期行为与实际行为的对比
   - 截图引用（内嵌图片请使用 `MEDIA:<screenshot_path>` 格式）
   - 相关的控制台错误信息
3. **所有问题的汇总表**
4. **测试说明**——已进行的测试、未进行的测试以及任何阻碍因素。

将报告保存至 `{output_dir}/report.md` 文件中。

## 工具参考

| 工具 | 用途 |
|------|---------|
| `browser_navigate` | 访问指定网址 |
| `browser_snapshot` | 获取 DOM 文本快照（无障碍结构） |
| `browser_click` | 根据引用标识（`@eN`）或文本点击元素 |
| `browser_type` | 在输入框中输入内容 |
| `browser_scroll` | 向上/向下滚动页面 |
| `browser_back` | 返回浏览器历史记录中的上一页 |
| `browser_press` | 按下键盘按键 |
| `browser_vision` | 截图并配合 AI 进行分析；如需添加元素标签，请使用 `annotate=true` 参数 |
| `browser_console` | 获取 JavaScript 控制台输出及错误信息 |

## 使用提示

- **在访问页面或执行重要操作后，务必检查 `browser_console()` 的输出。** 潜在的 JavaScript 错误往往是极具价值的发现。
- 当需要确定交互元素的位置，或快照中的引用标识不明确时，**请在调用 `browser_vision` 时添加 `annotate=true` 参数**。
- **请同时使用有效和无效的输入数据进行测试**——表单验证错误较为常见。
- **对长页面进行滚动测试**——页面底部的内容可能存在渲染问题。
- **对导航流程进行端到端测试**——依次点击完成多步骤操作。
- **通过截图检查响应式表现**，留意其中出现的任何布局问题。
- **不要忽视边缘情况**：空状态、过长的文本、特殊字符以及快速连续点击等。
- 在向用户展示截图时，请附带 `MEDIA:<screenshot_path>` 参数，以便他们能够直接查看相关证据。
