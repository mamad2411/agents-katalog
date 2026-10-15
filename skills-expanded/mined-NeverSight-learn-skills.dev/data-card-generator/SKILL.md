---
name: data-card-generator
description: 将文字/数据转化为美观的 HTML 数据卡片网页，支持高清 PNG 下载。触发场景：帮我做一张卡片、生成数据海报、把这段文字做成图、制作信息卡片、数据可视化卡片、小红书配图、朋友圈数据图、PPT 配图文案。即使用户没有明确说"卡片"，只要请求涉及将文字/数据转化为美观图文形式，也应触发此 Skill。
---

# 数据卡片生成器 (Data Card Generator)

## Skill 简介

本 Skill 用于将用户提供的文字内容，生成一个**单文件 HTML**格式的数据卡片网页。这张卡片设计精美，用户可以在浏览器中打开，点击按钮后保存为高清 PNG 图片，用于小红书、朋友圈、PPT 配图等场景。

---

## 工作流程 (Workflow)

### 步骤 1 - 内容理解

- 判断用户输入是：一段待整理的原始文字，还是已经明确说了"标题是 X、内容是 Y"这类结构化需求
- 如果是原始文字：提炼出 3-6 个核心数据点，每个数据点包含一个小标题（不超过 8 字）和一段说明（不超过 50 字）
- 如果用户已经提供了结构化内容：直接使用，不要擅自改动
- 判断内容体量：如果内容较多、需要拆分为多张卡片，进入**多卡片模式**（详见规则 6）

### 步骤 2 - 方案选型

- 根据内容数量和用户要求，从**资产库**中选择最合适的尺寸、版式、皮肤、配色
- 如果用户没有指定，使用以下默认值：尺寸=Mobile 手机竖版，版式=经典竖排，皮肤=液态玻璃，配色=梦幻马卡龙
- 将选型结果简短告知用户（一行即可），例如："我将为你生成：Mobile 竖版 / 经典竖排 / 液态玻璃 / 梦幻马卡龙配色"

### 步骤 3 - 代码生成

- 根据步骤 2 选定的皮肤和布局，从下表找到对应模板，**在模板基础上修改内容，不得从零重建**：

| 皮肤 / 场景 | 起点模板 |
|-------------|----------|
| 液态玻璃（默认） | `template-mobile.html` |
| 赛博朋克 | `template-cyberpunk.html` |
| 黑金奢华 | `template-black-gold.html` |
| 粘土风 | `template-clay.html` |
| 多卡片横排（任意皮肤） | `template-multi-card.html`（在此基础上调整配色） |
| Desktop 宽卡 / 对比版式（Layout B） | `template-desktop.html` |
| 苹果极简 / 新拟态 / 极光渐变 / 复古像素 | 以 `template-mobile.html` 为结构起点，重写 `:root` 配色和皮肤相关 CSS |

- 对于表中未直接对应的皮肤，以结构最接近的模板为起点，只替换颜色变量和皮肤 CSS，保留所有 HTML 层级不变
- 严格按照**技术规范**章节的所有规则，生成完整的单文件 HTML 代码
- 代码必须完整可运行，不能有任何省略号或"此处省略"

### 步骤 4 - 代码交付

- 将完整 HTML 代码放在一个代码块中输出
- 在代码块下方，用简短的说明告诉用户：如何修改卡片标题、如何修改内容文字（指向 CSS :root 区域和 HTML 数据区）

### 步骤 5 - 等待反馈

- 询问用户是否需要调整版式、配色或内容

---

## 资产库 (Assets Library)

### 尺寸库 (3 种)

| 名称 | 规格 | 适用场景 |
|------|------|----------|
| Mobile 手机竖版 | max-width: 420px, min-height: 800px | 小红书、朋友圈 |
| Desktop 电脑横版 | max-width: 900px, min-height: 500px | PPT、网页配图 |
| Square 正方形 | width: 600px, height: 600px | Instagram、头像 |

### 版式库 (4 种)

| 名称 | 描述 | 适用场景 |
|------|------|----------|
| Layout A 经典竖排 | 数据块垂直分布 | 3-5 个数据点的深度内容 |
| Layout B 横向对比 | 左右分栏 | 两两对比类内容 |
| Layout C 九宫格 | Grid 自动适配列数 | 6 个以上的并列数据 |
| Layout D 金句引言 | 居中大字号，极简留白 | 单条金句或名言 |

### 皮肤库 (8 套)

| 编号 | 名称 | 视觉风格 | 适合内容 |
|------|------|----------|----------|
| 1 | 液态玻璃（默认） | 半透明毛玻璃质感，现代感强 | 通用内容 |
| 2 | 苹果极简 | 纯白背景，细线条 | 科技/产品类 |
| 3 | 赛博朋克 | 深色背景 + 霓虹色描边 | 科技/游戏类 |
| 4 | 极光渐变 | 绿蓝紫流动渐变 | 创意/艺术类 |
| 5 | 粘土风 | 圆角大、颜色柔和、带阴影 | 儿童/教育类 |
| 6 | 新拟态 | 灰底浮雕感 | 数据/金融类 |
| 7 | 复古像素 | 像素字体 + 方块纹理 | 游戏/怀旧类 |
| 8 | 黑金奢华 | 纯黑底 + 金色文字 | 高端/奢侈类 |

### 配色库 (6 套)

| 编号 | 名称 | 主色 | 适用场景 |
|------|------|------|----------|
| 1 | 梦幻马卡龙（默认） | 粉紫蓝柔和色 | 生活/情感类 |
| 2 | 商务深蓝 | 深蓝 + 白 | 商业/职场类 |
| 3 | 森林大地 | 绿棕米 | 自然/健康类 |
| 4 | 日落秋日 | 橙红黄 | 励志/人文类 |
| 5 | 赛博霓虹 | 紫粉青荧光色 | 科技/潮流类 |
| 6 | 高级灰底 | 灰 + 黑白 | 极简/设计类 |

---

## 技术规范 (Critical Rules - 必须完整遵守)

### ⚠️ 规则 1：下载按钮必须处于正常文档流，禁止使用 position: fixed

**错误做法（禁止）：** 把下载按钮设置为 `position: fixed` 固定在页面底部。

**正确做法：** 卡片区域和下载按钮都处于普通文档流中，`poster-wrapper`（或多卡片时的 `cards-grid`）在上，`action-wrapper` 在下，两者平级。

**单张卡片必须使用以下 HTML 结构：**

```html
<body>
  <div class="poster-wrapper">
    <div class="poster-container" id="poster">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
      <div class="content-layer">
        <!-- 标题区、数据卡片等 -->
      </div>
    </div>
  </div>

  <!-- ✅ action-wrapper 必须在 poster-wrapper 外面，两者平级 -->
  <div class="action-wrapper">
    <button class="download-btn" id="downloadBtn">保存为高清图片</button>
  </div>
</body>
```

---

### ⚠️ 规则 2：截图必须使用 html-to-image 库，禁止使用 html2canvas

**原因：** html2canvas 无法正确渲染 backdrop-filter（毛玻璃）和复杂 CSS 渐变，截图会失真。

**必须在 `<head>` 中引入：**

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/html-to-image/1.11.11/html-to-image.min.js"></script>
```

**下载按钮的 JS 逻辑必须完整照抄以下代码，不能修改结构：**

```javascript
const downloadBtn = document.getElementById('downloadBtn');
const poster = document.getElementById('poster');

downloadBtn.addEventListener('click', () => {
    const originalText = downloadBtn.innerText;
    downloadBtn.innerText = '正在生成超清原图...';
    downloadBtn.disabled = true;

    // 截图前暂停所有 CSS 动画，防止气泡飘到中途被冻结
    const blobs = poster.querySelectorAll('.blob');
    blobs.forEach(b => b.style.animation = 'none');

    htmlToImage.toPng(poster, {
        pixelRatio: 3,
        style: { transform: 'none' }
    })
    .then(function (dataUrl) {
        const link = document.createElement('a');
        link.download = 'DataCard_Export.png';
        link.href = dataUrl;
        link.click();
        downloadBtn.innerText = '保存成功 ✅';
        setTimeout(() => {
            downloadBtn.innerText = originalText;
            downloadBtn.disabled = false;
            blobs.forEach(b => b.style.animation = ''); // 恢复动画
        }, 2000);
    })
    .catch(function (error) {
        console.error('生成失败:', error);
        downloadBtn.innerText = '生成失败，请重试';
        blobs.forEach(b => b.style.animation = ''); // 恢复动画
        setTimeout(() => {
            downloadBtn.innerText = originalText;
            downloadBtn.disabled = false;
        }, 2000);
    });
});
```

**说明：**
- `pixelRatio: 3`：3 倍超清像素，确保截图文字清晰不模糊，不能删
- `style: { transform: 'none' }`：修复某些浏览器的渲染偏移 Bug，不能删
- 截图前暂停 `.blob` 动画：防止气泡浮动到一半被截图冻结，截完后必须恢复

---

### ⚠️ 规则 3：所有可修改的变量必须集中在 CSS :root 区域

在 `<style>` 标签最顶部，必须用 `:root` 声明所有颜色、圆角、尺寸变量，方便用户直接修改。

```css
:root {
    /* === 用户可修改区域 === */
    --card-width: 420px;             /* 卡片最大宽度 */
    --card-bg: linear-gradient(...); /* 背景色 */
    --accent-color-1: #a1c4fd;       /* 主题色 1 */
    --accent-color-2: #ffc3a0;       /* 主题色 2 */
    --text-primary: #333333;         /* 主要文字颜色 */
    --text-secondary: #666666;       /* 次要文字颜色 */
    --border-radius: 24px;           /* 卡片圆角 */
}
```

---

### ⚠️ 规则 4：HTML 数据内容必须集中放置，便于用户修改

所有用户可能需要修改的文字（标题、副标题、各数据点内容）都必须集中放在 HTML 的一个区域内，并在该区域上方用注释标注：

```html
<!-- ===== 用户数据区，修改这里的文字即可 ===== -->
<h1 class="main-title">卡片主标题</h1>
<p class="sub-title">副标题或描述</p>
<!-- 数据点内容 -->
<!-- ===== 数据区结束 ===== -->
```

---

### ⚠️ 规则 5：内容数量与质量标准

- 单张卡片的独立数据点：最少 2 个，最多 8 个
- **版式选择：** 超过 6 个数据点且用户未指定版式时，推荐使用 Layout C 九宫格，应在生成前告知用户并说明原因
- 每个数据点的小标题：不超过 10 个汉字
- 每个数据点的说明文字：移动端不超过 50 字，桌面端不超过 80 字
- 卡片必须有主标题（可以没有副标题）
- 卡片底部建议加一行署名或来源信息（如"— AI 探索笔记 —"）

---

### ⚠️ 规则 6：多张卡片使用横向网格布局，禁止垂直堆叠

当内容需要生成 **2 张或以上**卡片时，必须将所有卡片横向并排展示。

**卡片数量与列数的对应关系：**

| 卡片数量 | 列数 | 原因 |
|----------|------|------|
| 1 张 | 1 列 | 单卡片居中即可 |
| 2 张 | 2 列 | 左右并排 |
| 3 张 | 3 列 | 三列均分 |
| 4 张 | 2 列 | 4 列过于拥挤，改为 2×2 网格 |
| 5-6 张 | 3 列 | 每行 3 张 |
| 7 张以上 | 3 列 | 每行 3 张，自动换行 |

**必须使用以下 HTML/CSS 结构：**

```css
/* 网格容器：横向排列所有卡片 */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(2, 420px); /* 2 张卡片；3 张改为 repeat(3, 420px) */
    gap: 24px;
    justify-content: center;
    align-items: start; /* 卡片高度不一时顶部对齐，不拉伸 */
}

/* 多卡片时，poster-wrapper 宽度由 grid 控制，不再需要 max-width */
.poster-wrapper {
    width: 420px;
    border-radius: 24px;
    overflow: hidden;
}
```

```html
<body>
  <!-- 页面标题（可选） -->
  <div class="page-header"> ... </div>

  <!-- 横向网格：所有卡片放在这一个容器里 -->
  <div class="cards-grid">
    <div class="poster-wrapper">
      <div class="poster-container" id="poster1"> ... </div>
    </div>
    <div class="poster-wrapper">
      <div class="poster-container" id="poster2"> ... </div>
    </div>
  </div>

  <!-- ✅ 下载按钮区域在 cards-grid 外面，每张卡片对应一个按钮 -->
  <div class="action-wrapper">
    <button class="download-btn" id="downloadBtn1">保存第 1 张</button>
    <button class="download-btn" id="downloadBtn2">保存第 2 张</button>
  </div>
</body>
```

**多卡片 JS 规范：** 每张卡片单独绑定一个下载按钮；截图逻辑与规则 2 完全相同，poster 和 downloadBtn 的 id 分别用数字后缀区分（poster1/poster2、downloadBtn1/downloadBtn2）。

---

### ⚠️ 规则 7：CSS 类名必须与 HTML 严格一致，禁止混用

当新卡片的版式与 `template-mobile.html` 差异较大（如改为命令列表卡、对比卡等新结构），需要为新结构独立定义 CSS 类名。

**必须遵守以下原则：**
- CSS 里定义什么类名，HTML 里就用什么类名，完全一致
- 禁止 CSS 定义 `.foo`，HTML 却用 `.foo-bg` 或 `.foo-item`（类名不一致会导致样式完全失效）
- 在开始写 CSS 之前，先列出所有新 HTML 元素的类名，再逐一在 CSS 中对应定义，不得遗漏

---

## 参考样板说明

本 Skill 提供 6 份官方模板，覆盖主流皮肤和布局场景，AI 生成时直接读取对应文件，无需凭空创作：

| 文件名 | 皮肤风格 | 布局 | 适用内容 |
|--------|----------|------|----------|
| `template-mobile.html` | 液态玻璃 · 马卡龙 | 单卡竖版 | 通用，默认起点 |
| `template-cyberpunk.html` | 赛博朋克 · 霓虹 | 单卡竖版 | 科技、工具、命令速查 |
| `template-black-gold.html` | 黑金奢华 | 单卡竖版 | 励志、商业洞察、高端内容 |
| `template-clay.html` | 粘土风 · 马卡龙紫 | 单卡竖版 | 学习、生活、教育、亲子 |
| `template-multi-card.html` | 暖橙液态玻璃 | 双卡横排 | 内容较多需分页，演示 cards-grid 布局 |
| `template-desktop.html` | 商务深蓝 | 宽卡对比（左右分栏） | 两两对比、横版配图 |

### 所有模板共同遵守的核心结构规则

无论使用哪个模板，以下规则不变：

1. `poster-wrapper`（或多卡片时的 `cards-grid`）与 `action-wrapper` **平级**，按钮永远在卡片容器外面
2. 每张卡片的截图区域有且仅有一个带 `id="poster"` 或 `id="posterN"` 的元素
3. 截图 JS 在调用 `htmlToImage.toPng` 前先暂停该卡片内的 `.blob` 动画，截完后恢复
4. `:root` 集中声明所有颜色变量；HTML 数据区用 `<!-- ===== 用户数据区 ===== -->` 注释标注边界

---

## 边界与限制 (Limitations)

1. 本 Skill 仅输出单文件 HTML，不生成 React 组件或其他格式
2. 卡片截图依赖浏览器环境，需要用户在浏览器中打开 HTML 文件后点击下载按钮
3. 不支持在卡片中嵌入真实图片（用户未提供图片 URL 时，使用纯色/渐变色块代替）
4. 生成的 HTML 使用了 Google Fonts，在无网络环境下字体会降级为系统字体
5. 不保证 IE 浏览器兼容性，仅支持现代浏览器（Chrome、Safari、Edge）
6. 多卡片横向布局主要面向桌面端预览和下载，在手机浏览器上可能超出屏幕宽度
