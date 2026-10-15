---
name: webpage-designer
description: 将用户给出的内容转成网页文件。先理解内容，再根据内容选择风格（或用户指定风格），加载对应提示词，最后生成网页代码。使用时机：用户需要生成网页、落地页、作品集，或任何需要网页界面的场景。
---

# 网页设计技能 (Webpage Designer)

用于把用户给出的内容转成网页文件：先理解内容，再选风格，再加载对应提示词，最后生成网页代码。

## 目标能力

输入：
- 用户内容（文案、品牌信息、目标用户、业务场景）
- 可选约束（风格偏好、技术栈、是否单页）
- 可选产出模式（见"产出物模式"）

输出：
- 可直接运行的网页文件（默认独立 HTML）
- 页面内容与用户输入语义一致
- 视觉风格与所选 `prompts/{style}.md` 一致

---

## 产出物模式（用户可选）

1. 独立 HTML（默认）
- 单文件 `index.html`
- 内嵌 `<style>` 和 `<script>`
- 允许使用在线脚本与在线字体（CDN）

2. 单页分离文件
- `index.html` + `styles.css` + `script.js`
- 字体与资源配置独立（如 `fonts.css` 或单独字体导入文件）

3. 指定技术栈文件
- 按用户指定技术栈输出（如 React / Next.js / Vue / Svelte 等）
- 文件结构遵循目标技术栈惯例

---

## 标准工作流（必须）

1. 确认产出模式
- 若用户明确指定，严格按指定模式输出
- 若未指定，默认使用"独立 HTML（单文件）"

2. 分析用户内容
- 提取主题、行业、语气、目标受众、核心诉求
- 识别页面类型：品牌官网 / 落地页 / 作品集 / 文档站 / 活动页

3. 选择风格（1 个主风格 + 可选 1 个辅助风格）
- 用户指定风格时，直接使用用户指定的风格
- 用户未指定时，根据内容语义自动匹配最合适的设计风格
- 主风格用于整体视觉语言
- 辅助风格只允许用于局部细节（动效、排版或组件细节），不能破坏主风格一致性

4. 加载提示词
- 读取 `prompts/{style}.md`
- 使用其中的 `<role>` 与 `<design-system>` 约束生成代码

5. 结合用户内容生成网页
- 把用户内容映射为页面信息架构（Hero/功能区/证据区/CTA）
- 按选定产出模式生成完整页面文件
- 保证响应式和基础可访问性

6. 自检
- 视觉一致性：是否符合所选风格
- 内容一致性：是否忠实于用户原文
- 工程完整性：文件可打开、无明显结构错误

---

## 风格选择映射（快速规则）

- 极简/留白/编辑感：`monochrome`, `swiss-minimalist`, `minimal-dark`
- 科技/SaaS/企业：`saas`, `professional`, `enterprise`, `modern-dark`
- 复古/怀旧：`retro`, `vaporwave`, `art-deco`, `newsprint`
- 学术/出版：`academia`, `newsprint`
- 自然/有机：`botanical`, `organic`
- 实验/艺术/冲击力：`bauhaus`, `neo-brutalism`, `maximalism`, `kinetic`
- 开发者/命令行：`terminal`, `modern-dark`
- 未来感/赛博：`cyberpunk`, `web3`

当用户未指定风格时：
- 优先选择和行业语义最匹配的风格
- 若用户内容偏正式（B2B/企业），默认优先 `professional` 或 `enterprise`

当用户指定风格时：直接使用用户指定的风格

---

## 仓库结构

```text
webpage-designer/
├── SKILL.md
├── fetch_prompts.sh
├── prompts/
│   └── *.md (30 个风格提示词)
└── sites/
    └── designprompts.dev.md
```

---

## 提示词文件契约

每个 `prompts/*.md` 必须满足：
- 包含头部字段：`Description`、`Mode`、`Typography`
- 正文只包含一个 `<role>` 块和一个 `<design-system>` 块
- 不包含站点导航噪音（如 `Copy Prompt`）

---

## 站点来源文档

所有"按站点区分"的抓取说明与问题记录放在：
- `sites/*.md`

当前已接入：
- `sites/designprompts.dev.md`

后续新增站点时，按同样方式新增：
- `sites/{domain}.md`
