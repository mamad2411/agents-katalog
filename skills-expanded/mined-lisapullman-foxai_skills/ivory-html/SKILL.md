---
name: ivory-html
description: >-
  文章转象牙文档风 HTML /ivoryhtml。当用户说「生成 ivory HTML」「象牙色排版」「象牙色文章页」
  「/ivoryhtml」「/ivory-html」，或要求象牙底·陶土强调·衬线标题的编辑风文档排版时触发。
  将文章链接或文本转换为高颜值简体中文单页 HTML，保留完整内容细节。
---

# Ivory HTML

将用户提供的文章链接或正文，转换为象牙文档风单页 HTML（象牙底 + 陶土强调 + 衬线标题）。只做结构化排版与视觉增强，不擅自删减、改写立场或补造事实。

## 风格定位

| 维度 | 规范 |
|------|------|
| 气质 | 编辑风 / 纸质文档，克制留白 |
| 背景 | `#FAF9F5` ivory |
| 内容底 | `#FFFFFF` paper |
| 主文字 | `#141413` slate |
| 强调色 | Clay `#D97757` / Clay-dark `#B85C3E` |
| 正向色 | Olive `#788C5D` |
| 标题字体 | 衬线 serif 500（Georgia / Songti SC），非粗黑无衬线 |
| 页眉 | 留白 + mono eyebrow + 细陶土短线，无实心色块大 banner |

## 工作流

1. **获取内容**
   - 用户给链接：抓取标题、作者、日期、正文、图片、图表、引用与出处；无法访问时请用户提供正文。
   - 用户给正文：提取标题、作者、日期、章节层级与关键数据；缺失元数据可省略，不编造。

2. **整理结构**
   - 按语义拆 `section`，用 `h2` / `h3` / `h4` 建层级。
   - 长段可拆短，但不丢细节。
   - 步骤/清单/排名 → `ol` / `ul`。
   - 独立信息点 → `.card-grid` + `.card`。
   - 核心结论 → `.key-point`（左侧陶土条）；可加 `.bite-tag` 小标签。
   - 金句 → `.quote` 或语义化 `blockquote.quote`。
   - 重要数字 → `.stat-number`、`.stat-strip` 或 `.stat-row` + `.stat`。
   - 术语 → `.highlight`；特别强调 → `.emphasis`。
   - 对比观点 → `.vs-grid` + `.vs-cell`（突出项加 `.actual`）。
   - 章节分隔 → `.divider`（两侧细线 + mono 大写标签）。
   - 长文目录 → `nav.toc` 胶囊链接。
   - 默认正文包在 `main.content` 白卡内；需要「成品窗口」感时用 `.artifact` + `.artifact-bar` + `.artifact-body`。

3. **生成 HTML**
   - 以本 skill 的 `assets/ivory-template.html` 为模板，复制后替换标题、元数据、正文与页脚。
   - 输出完整单文件：`<!DOCTYPE html>`、`lang="zh-CN"`、`meta viewport`、**内联 CSS**、可读 `<title>`。
   - 默认写一个 `.html`；未指定文件名时用标题 slug，无法判断时用 `article.html`。
   - 不留 `[占位符]`、`TODO`、模板注释或空图片区。

## 视觉规范

### 颜色

```css
--ivory:  #FAF9F5;   /* 页面背景 */
--paper:  #FFFFFF;   /* 卡片/内容底 */
--slate:  #141413;   /* 主文字 */
--clay:   #D97757;   /* 强调 / 链接 / eyebrow 线 */
--clay-d: #B85C3E;   /* 强调深色 / hover */
--oat:    #E3DACC;   /* 次要暖底 */
--olive:  #788C5D;   /* 成功 / 正向标签 */
--g100:   #F0EEE6;
--g200:   #E6E3DA;
--g300:   #D1CFC5;   /* 边框 */
--g500:   #87867F;   /* 次要标签 */
--g700:   #3D3D3A;   /* 次要正文 */
```

### 字体

- **标题**：`ui-serif, "Songti SC", "Noto Serif SC", Georgia, Times, serif`，`font-weight: 500`，字距约 `-0.015em`。
- **正文**：`system-ui, -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif`，行高约 `1.55`～`1.65`。
- **标签 / 元信息 / 代码**：`ui-monospace, "SF Mono", Menlo, Consolas, monospace`，小号、常大写、字距 `0.1em`～`0.14em`。

### 版式

- 内容区 `.wrap`：`max-width: 980px`，左右 `24px`。
- 页眉：`.eyebrow`（mono + 左侧 24×1.5px 陶土线）→ 衬线 `h1`（`clamp(32px, 5vw, 46px)`）→ `.lede` → `.meta`。
- 边框：`1.5px solid var(--g300)`；圆角 `10px`～`14px`；阴影克制。
- 链接：陶土色，下划线 oat，hover 加深。
- 卡片 hover：轻上移 + 边框变 slate。
- ≤640px：网格单列、收紧内边距、缩小引用字号。

### 组件

| 意图 | 类名 / 标签 | 说明 |
|------|-------------|------|
| 页眉标签 | `.eyebrow` | mono 大写 + 陶土短线 |
| 导语 | `.lede` | 16–16.5px，g700 |
| 作者/日期 | `.meta` | mono 小字 |
| 目录 | `nav.toc a` | 胶囊 pill 链接 |
| 关键结论 | `.key-point` / `.bite` | 左 3px 陶土条，象牙底 |
| 引用金句 | `.quote` / `blockquote` | 衬线斜体，左 oat 竖线 |
| 信息卡 | `.card-grid` + `.card` | 白底、细边、圆角 |
| 对比两栏 | `.vs-grid` / `.vs-cell.actual` | actual：陶土边 + 暖底 |
| 数字条 | `.stat-strip` / `.stat` | mono 或衬线大数字 |
| 章节线 | `.divider` | 两侧线 + 中部 mono 标签 |
| 小节眉题 | `.art-eyebrow` | 正文内 mono 分段标签 |
| 徽章 | `.badge` + 修饰类 | `.warn` / `.ok` / `.muted` / `.note` |
| 代码 | `code` / `pre` | mono，浅底细边 |
| 表格 | `.table-wrap` > `table` | thead g100 |
| 图片 | `figure` / `img` / `figcaption` | 圆角 + 细边 |
| 收束卡 | `.final-card` | 深边框 + 轻阴影，放结论 |
| 页脚 | `footer` | 顶部分割线，可选 `footer .k` 斜体 |

## 内容保真规则

- 保留原文完整细节；不为视觉压缩事实、合并观点或删限定条件。
- 不编造来源、日期、作者、参数、价格或实时信息。
- 表格用语义化 `table`；代码用 `pre > code`。
- 外链保留文本与 URL，必要时 `rel="noopener noreferrer"`。
- 基于最新网页时，先核对内容与日期再生成。

## 质量检查

- [ ] 单文件可本地打开，CSS 内联，无构建依赖
- [ ] 使用 ivory/clay/serif 系统（象牙底、陶土强调、衬线标题）
- [ ] 无占位符、空 section、空卡片
- [ ] 数字、术语、引用、列表、图片顺序与原文一致
- [ ] 移动端单列可读，文字不溢出
- [ ] 回复中给出生成文件路径；抓取失败须说明原因

## 文件约定

- 模板：本 skill 目录下 `assets/ivory-template.html`
- 输出：用户指定路径，或当前工作目录下的 slug `.html`
