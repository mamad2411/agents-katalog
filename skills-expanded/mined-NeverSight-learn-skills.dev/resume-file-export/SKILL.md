---
name: resume-file-export
description: >
  将简历内容导出为可投递的 PDF 或 Word 文件，提供 Markdown 规范化输出和多种转换方法。
  用户说"帮我导出简历"、"生成简历文件"、"怎么把简历转成 PDF"、
  "简历 Word 怎么做"、"帮我排好版"、"生成简历的 Markdown"时触发。
  也可作为 resume-editor 中 Mode C（生成文件）的执行 skill。
---

# 简历文件导出专项

## 你的任务

把用户已经优化好的简历内容，转化为**格式规范、可以直接投递的文件**。

两个核心路径：
- **路径 A（推荐）**：输出结构化 Markdown → 用户用工具转 PDF
- **路径 B（进阶）**：输出带样式的 HTML → 浏览器直接打印为 PDF

---

## 第一步：整理用户简历内容

如果用户还没有整理好内容：
→ 先完成内容优化（使用 resume-editor / resume-experience / 等专项 skill）
→ 内容定稿后，再回到本 skill 进行排版和导出

如果内容已经准备好：
→ 直接按以下格式规范输出

---

## 路径 A：Markdown 规范输出（推荐）

### Markdown 排版规范

以下是适合简历的 Markdown 写法规范：

```markdown
# 姓名

**求职意向**：XX 方向 | **手机**：XXX | **邮箱**：XXX@gmail.com | **GitHub**：github.com/xxx

---

## 教育背景

**XX 大学** · XX 专业（本科/硕士） · 2021.09 - 2024.06
- GPA：3.8/4.0，专业排名前 10%（可选，仅在排名靠前时写）

---

## 核心技能

**开发语言**：Python / TypeScript / SQL
**框架与库**：React 18 / FastAPI / LangChain
**工具与平台**：Docker / K8s（基础）/ GitHub Actions / AWS S3

---

## 工作 / 实习经历

**XX 公司 · XX 岗位** · 2023.07 - 2024.06 · 北京（全职/实习）

- 主导 XX 项目，通过 XX 方法，实现了 XX 结果（量化指标）。
- 负责 XX 模块开发，将接口响应时间从 Xms 降至 Yms。
- 参与 XX 工作，覆盖 XX 规模用户/客户。

---

## 项目经历

**项目名称** · 2023.03 - 2023.06 · [在线访问地址（如有）]

一句话背景（≤25 字）· 个人角色

- [行动]：[具体技术/方案] → [量化成果]
- [亮点]：[解决了什么难题 / 体现什么能力]

---

## 荣誉奖项（可选）

- XX 奖 · 级别（全国/省级/校级）· 年份

---

## 自我评价（可选）

[2-4 句，有事实支撑，参考 resume-summary 改写]
```

---

### 转 PDF 的三种方法（Markdown → PDF）

#### 方法 1：Typora（最简单，推荐新手）

1. 下载 Typora（https://typora.io，付费但有试用期）
2. 粘贴上方 Markdown 内容
3. 选择一个简洁主题（推荐：GitHub / Lark / Medium）
4. 菜单 → 文件 → 导出 → PDF

**优点**：操作极简，效果美观
**缺点**：付费软件，免费版可用 Obsidian 替代

#### 方法 2：Obsidian + 插件（免费）

1. 下载 Obsidian（免费）
2. 安装插件：`Obsidian to PDF` 或 `Pandoc Plugin`
3. 粘贴 Markdown，使用插件导出 PDF

**优点**：免费，功能丰富
**缺点**：需要一些插件配置

#### 方法 3：VS Code + Markdown PDF 插件（程序员友好）

1. 安装 VS Code 扩展：`Markdown PDF`（by yzane）
2. 打开 `.md` 文件，右键 → `Markdown PDF: Export (PDF)`

**优点**：程序员已有 VS Code，零额外成本
**缺点**：样式定制需要 CSS 知识

#### 方法 4：pandoc 命令行（最强自定义）

```bash
# 安装 pandoc（https://pandoc.org）
# 安装 LaTeX（MiKTeX / MacTeX）

pandoc resume.md \
  -o resume.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1.5cm \
  -V mainfont="思源黑体" \
  -V CJKmainfont="思源黑体"
```

**优点**：完全可控，适合批量生成
**缺点**：需要安装 LaTeX 环境，配置成本高

---

## 路径 B：HTML 模板输出（进阶·浏览器打印 PDF）

输出以下 HTML 模板（用户直接复制到 `.html` 文件，浏览器打开，Ctrl+P 打印为 PDF）：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: "Microsoft YaHei", "PingFang SC", "Source Han Sans", sans-serif;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #333;
    max-width: 800px;
    margin: 0 auto;
    padding: 24px 32px;
  }
  h1 {
    font-size: 22pt;
    color: #1a3c6e;
    margin-bottom: 4px;
  }
  .contact {
    font-size: 9.5pt;
    color: #666;
    margin-bottom: 16px;
    border-bottom: 1.5px solid #1a3c6e;
    padding-bottom: 8px;
  }
  h2 {
    font-size: 13pt;
    color: #1a3c6e;
    margin: 16px 0 6px 0;
    border-bottom: 0.5px solid #ccc;
    padding-bottom: 3px;
  }
  .exp-header {
    display: flex;
    justify-content: space-between;
    font-weight: bold;
    margin-bottom: 3px;
  }
  .exp-sub {
    color: #555;
    font-size: 9.5pt;
    margin-bottom: 4px;
  }
  ul {
    padding-left: 16px;
    margin-bottom: 10px;
  }
  li {
    margin-bottom: 2px;
  }
  @media print {
    body { padding: 0; }
    @page { margin: 1.5cm; }
  }
</style>
</head>
<body>

<h1>姓名</h1>
<div class="contact">
  求职意向：XX 方向 &nbsp;|&nbsp; 手机：XXX &nbsp;|&nbsp; 邮箱：xxx@gmail.com
</div>

<h2>教育背景</h2>
<div class="exp-header">
  <span>XX 大学 · XX 专业（本科）</span>
  <span>2021.09 - 2025.06</span>
</div>

<h2>核心技能</h2>
<ul>
  <li><strong>开发语言：</strong>Python / TypeScript / SQL</li>
  <li><strong>框架与库：</strong>React 18 / FastAPI / LangChain</li>
</ul>

<h2>工作 / 实习经历</h2>
<div class="exp-header">
  <span>XX 公司 · XX 岗位</span>
  <span>2023.07 - 2024.06</span>
</div>
<div class="exp-sub">全职 · 北京</div>
<ul>
  <li>主导 XX 项目，通过 XX 方法，实现了 XX 结果（量化指标）。</li>
  <li>负责 XX 模块，将接口响应时间从 Xms 降至 Yms。</li>
</ul>

<!-- 按相同结构继续添加 -->

</body>
</html>
```

**使用方式**：
1. 复制上方 HTML，将 `姓名 / XX 公司 / 技能` 等替换为实际内容
2. 保存为 `resume.html`
3. 用 Chrome 或 Edge 打开
4. 按 `Ctrl+P`（Windows）或 `Cmd+P`（Mac）
5. 目标打印机选"另存为 PDF"
6. 勾选"无页眉页脚"，去掉背景色

**优点**：完全可控排版；无需安装额外软件；跨平台一致
**缺点**：需要基础 HTML 编辑能力

---

## 投递规范提醒

导出后，投递前务必检查：

**文件命名规范**：
```
目标岗位-姓名-校招/社招.pdf

示例：
前端开发工程师-张明-校招.pdf
产品经理-李华-社招.pdf
```

**最终检查清单**：
- [ ] 用 PDF 阅读器打开，确认排版没有乱码/错位
- [ ] 手机号 / 邮箱 / 链接格式正确（邮箱别用 QQ 邮箱）
- [ ] 文件大小 < 5MB（HR 系统通常有限制）
- [ ] 英文 / 数字使用半角字符（不要全角）
- [ ] 是否需要根据目标公司 JD 再做最后一次关键词调整（配合 resume-jd-match）

---

## 需要 Word 格式（.docx）

部分公司要求提交 Word 简历（通常注明"请发送 Word 格式"才需要）。

**建议方案**：
1. **Pandoc 转换**：`pandoc resume.md -o resume.docx`（格式一般，需手动调整样式）
2. **WPS 粘贴调整**：将 Markdown 内容粘贴到 WPS 文字，手动应用样式模板
3. **直接在 WPS 里做**：用 WPS 的简历模板从头排版（选"简洁"系列模板）

> 国内最常用的简历是 PDF 格式。Word 仅在招聘方明确要求时才需要提供。

---

## 简历排版规范备忘

| 项目 | 规范 |
|------|------|
| 主色 | 深蓝（#1a3c6e）或深灰（#333333），不超过 2 色 |
| 正文字号 | 10.5pt |
| 标题字号 | 13pt，加粗 |
| 行间距 | 1.15–1.25 |
| 模块间距 | 6–8pt |
| 页边距 | 上下 1.5cm，左右 2cm |
| 长度 | 3 年内：1 页；3 年以上：不超过 2 页 |
| 条目符号 | 「—」或「•」统一，不混用 |
