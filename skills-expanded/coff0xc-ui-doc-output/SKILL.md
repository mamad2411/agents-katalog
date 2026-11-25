---
name: coff0xc-ui-doc-output
description: "Use when / 当用户请求 UI/frontend/product surface/report/translation polish：dashboard/admin/SaaS、component/design system、responsive/mobile、accessibility/ARIA/contrast、loading/empty/error/hover/focus/keyboard states、browser smoke/screenshot/console cleanliness、anti-AI visual polish。正式 Office 文件用 office-doc-tools。手动触发：使用 coff0xc-ui-doc-output。"
---

# coff0xc-ui-doc-output

<!-- skill-id: cs-udo-c8e51b29 -->

## 快速规则（日常任务先读这里）
> **[先扫系统]** 先看现有 route/component/token/theme/icon/copy/test/browser path，复用项目设计语言。
> **[状态门禁]** UI 必须覆盖 loading、empty、error、success、disabled、focus、hover、mobile 和长文本/空数据。
> **[视觉证据]** 重要 UI 改动要做浏览器 smoke、截图或等价渲染检查，并记录 console/重叠/响应式问题。
> **[硬边界]** 发布网站、下载外部资产、上传文档、客户/隐私数据处理和付费服务先确认。

普通 UI/报告/翻译任务按本节快路径执行；只有深度审美、外部 UI skill 合并、quality eval 或发版门禁才读取 references。

## 能力定位
面向 UI、前端体验、报告表达和技术翻译交付的产物质量能力。它不只润色文字，还要求界面、交互状态和报告叙事真实可用、可读、可验证。

正式 Office/PDF 文件产物，例如 PPTX、DOCX、PDF、Excel/XLSX/CSV 的创建、编辑、批注、公式和渲染验证，优先使用 `coff0xc-office-doc-tools`。

## 能交付什么
- 可用 UI/组件/页面改动或设计建议
- 桌面/移动端截图或浏览器 smoke 结果
- 报告结构、交付文案和版式建议
- 翻译润色稿、术语一致性和交付说明

## 可以接收什么输入
- 前端仓库、页面截图、设计稿、组件代码
- Markdown、报告草稿、翻译文本、截图、页面文案
- 用户反馈、移动端问题、可访问性或版式问题

## 放心使用的边界
- 可直接处理本地 UI 和文档产物
- 正式 PPTX/DOCX/PDF/XLSX/CSV 文件交付转入 `coff0xc-office-doc-tools`
- 下载外部资产、上传文档、发布网站、付费服务必须先确认
- 含个人信息或客户数据的内容要先确认脱敏要求
- 默认只处理本地、可逆、可验证的低风险工作；涉及生产、凭据、付费、远程写入、删除、发布或权限变更时必须先确认。

## 为什么可以放心
- 版式相关任务必须渲染或截图验证
- UI 覆盖 loading/empty/error/success 等状态
- 翻译不改变事实、数字、命令和路径

## 典型使用方式
```text
使用 coff0xc-ui-doc-output 优化这个 dashboard，并用截图检查移动端。
使用 coff0xc-ui-doc-output 把这份中文报告翻译润色成英文交付版。
Use coff0xc-ui-doc-output to polish the report narrative and UI copy for these findings.
```


## Core Gates
- 明确 UI/报告/翻译任务直接执行本 skill；只有跨领域或不确定任务才先用 `coff0xc-skill-router`。
- UI 前先查现有组件、tokens、theme、icons、样式系统、截图和可用验证命令。
- 外部/朋友/项目专用 UI skill 只能抽象成通用规则；不要保留个人称呼、机器路径、绝对口味禁令或默认授权语句。
- UI 不做 happy path 静态壳：至少考虑 populated、empty、loading、error、disabled、hover/focus、long-content 和 small-screen。
- 避免 AI 味：模板 hero、三列卡片堆、紫蓝霓虹、卡片套卡片、无意义 bento、只靠图标/说明文字解释功能。
- 数据展示不编数字：关键总数、金额、百分比、时间范围、单位和图表轴必须来自可信数据/API/公式或注明假设。
- 报告/翻译保留事实、数字、代码、命令、路径、引用和不确定性；正式 PPTX/DOCX/PDF/XLSX/CSV 交付转 `coff0xc-office-doc-tools`。

## Verification
- UI 代码改动后，能启动本地服务就启动；能静态打开就给本地 HTML 路径。
- 至少检查一个桌面和一个移动视口；复杂工具再加窄屏/平板宽度。
- 看 console、资源加载、空白渲染、重叠、裁切、文本溢出、按钮可点性、表单基本路径和焦点状态。
- Canvas/WebGL/Three.js 必须检查非空像素、场景 framing、移动/交互是否可见。
- 如果浏览器或截图不可用，最终写“代码已改但未做视觉验收”，不能说 UI 已验证。

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## References
普通任务不要默认读取这些文件。

| Reference | 何时读取 |
| --- | --- |
| `references/ui-generalized-rules.md` | 合并外部 UI skill、深度审美/前端工程 review、Figma/Playwright/截图质量门禁、UI quality eval。 |

## Output Contract
```markdown
完成：
- ...

验证：
- ...

还剩：
- ...

下一步：
- ...
```
