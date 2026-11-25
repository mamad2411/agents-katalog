---
name: 教程类H5-小红书小工具
description: 用 AI 生图 + SPA 课程架构 + 离线 H5 zip = 在小红书"创作者中心 → 小工具"发布的多课程 H5 互动产品。讲清楚 4 层栈 / 5 步流程 / 7 节课程都适用。触发词：「做教程类 H5」「小红书小工具」「H5 课程」「离线 H5 课程」「多节课 H5」。
---

# 教程类 H5 · 小红书小工具

## 核心理念

**教程类 H5 = 离线 SPA 课程页 + AI 生图配图 + 杂志海报风视觉 + 强容器约束**。

| 维度 | 跟普通 H5 的差异 |
|---|---|
| **运行环境** | 小红书"小工具"容器（不是普通浏览器）—— 受限 CSP、纯离线、强容器约束 |
| **AI 能力** | ❌ **完全用不到** LLM / 联网 / 定位 —— H5 是"纯静态规则引擎" |
| **用户行为** | 读 5-10 分钟、收藏 / 转发 / 反复看，不是"用完即弃"的工具 |
| **复用价值** | 强（沉淀 1 次用 3 年）vs 互动小工具（弱，用 1 次就死） |
| **核心能力** | 文字 + 图 + 课程结构（SPA 多页） |

**核心主张**：教程类 H5 不是"评分小工具"——评分是用完即弃的伪需求；教程是**沉淀资产**。

> 案例：用户原始需求是"做评分小工具"，agent 推荐了 6 个候选 + 1 个推荐，被用户反馈"评分小工具很鸡肋"，最终改成"长篇讲解 + 多课程 SPA"——**结构升级后价值翻 10 倍**。

## 何时使用

- 用户要"做教程类 H5" / "小红书小工具" / "H5 课程"
- 主题是**讲清楚 1 个大知识点**（4 层栈 / 5 步流程 / 7 节课程 / 1 套范式）
- 想在**小红书创作者中心 → 小工具**发布
- 需要支持点击看详情 + 返回 + 上一节 / 下一节

## 不适用

- ❌ 需要 LLM / AI 推理的"智能工具"（H5 用不到 AI）
- ❌ 实时行情 / 联网 / 调 API 的"动态工具"
- ❌ 评分 / 测试 / 测评（用户反馈"很鸡肋"——沉淀价值低）
- ❌ 多 HTML 页面站点（容器只允许单页 + JS 视图切换）

---

## 5 步工作流

### Step 1 · 主题规划（10 分钟）

**目的**：把"想讲什么"变成可执行的内容大纲。

**关键决策**：

| 决策 | 推荐 | 理由 |
|---|---|---|
| 课程数 | **5-7 节** | < 5 节太单薄；> 7 节读者疲劳 |
| 每节长度 | **600-1200 字** | 5 分钟读完 |
| 每节结构 | **钩子 + 4 段正文 + 金句 + 行动** | 4 段 = 4 个子主题；金句 = 记忆点；行动 = 转化 |
| 课程目录 | 顶栏 logo + 课程列表 + 鸡汤句 | 0.5 秒 get 项目定位 |

**输出**：1 份 outline.md（每节 1 行标题 + 1 段简介）

### Step 2 · 内容准备（30-60 分钟）

**目的**：把大纲写成 5-7 节完整长文。

**每节模板**：

```markdown
# 课 X · {title}

## 钩子（1 句话）
{反常识 / 痛点 / 翻转，让读者想继续看}

## 段 1 · {heading}
{150-200 字，1 个具体概念 / 数据 / 案例}

## 段 2 · {heading}
{150-200 字，承接段 1，1 个新角度}

## 段 3 · {heading}
{150-200 字，对比 / 反例 / 易混概念}

## 段 4 · {heading}
{150-200 字，落地建议 / 操作步骤 / 怎么用}

## 金句（1 句）
{短句，能复述，能截图，能传播}

## 行动（1 段）
{今天就能做的 1 件事}
```

**关键决策**：

| 决策 | 推荐 | 反例 |
|---|---|---|
| 中文写作 | 0.5 秒 get 到的动词优先 | "实现价值创造" / "赋能业务" |
| 段落长度 | 150-200 字 / 段 | < 100 字太空，> 300 字读者跳读 |
| 金句 | "X 不是 Y，是 Z" 句式 | 抽象感叹（"加油" / "努力"） |
| 行动 | 具体到"今天做 1 件事" | "持续精进" / "深度思考" |

**输出**：5-7 节完整长文（共 4000-8000 字）

### Step 3 · 视觉准备（30 分钟）

**目的**：用 AI 生 4 张 16:9 配图 + 1 张 1:1 logo。

**资源清单**：

| 资产 | 比例 | 数量 | 用途 |
|---|---|---|---|
| 课程封面 | 16:9 | 1 张 | 首页 hero |
| 配图 | 16:9 | 3 张 | 课 1/2/3 配图（其他课程用 CSS 渐变占位） |
| logo | 1:1 | 1 张 | 小红书"图标"框 |

**共享 [4 STYLE] 段**（所有图共享风格锁）：

```
Chinese tech magazine cover style infographic.
Cool blue-white-gray palette: deep navy #0a1929 background,
mint green #64ffda accent, light cyan #ccd6f6 secondary.
Bold sans-serif English typography, key numbers in mint green.
Modular grid layout with generous whitespace, clean editorial typography.
Geometric patterns, subtle gradients, tech editorial aesthetic.
Wired magazine meets MIT Tech Review, sophisticated data poster quality.
NO realistic photos, NO emoji characters, NO decorative borders,
NO Chinese characters in the image.
```

**关键决策**：

| 决策 | 推荐 | 理由 |
|---|---|---|
| 图里要不要中文 | ❌ 0 中文 | AI 渲染中文长句易错；用 HTML 文字层覆盖更准 |
| 4 张图用同 1 套 [4 STYLE] | ✅ 强制 | 跨图风格锁 |
| 第 1 张喂给后续 | ✅ `input_urls` | matrix MCP 支持，锁视觉 |
| logo 主视觉 | **"AI" 大字 + FROM ZERO 副标** | 小白一眼 get，不强调内部框架数字（参考 4 层栈案例反馈） |

**输出**：4 张 16:9 配图（每张 < 800KB）+ 1 张 1:1 logo（< 500KB）

### Step 4 · 代码编写（30 分钟）

**目的**：写 4 个核心代码文件 + 1 个数据文件。

**文件清单**：

```
tool.zip
├── index.html       # 壳（顶栏 + 视图容器，< 1KB）
├── main.js          # SPA 路由 + 视图切换（< 8KB）
├── data.js          # 7 节课数据（钩子+段+金句+行动，< 25KB）
├── style.css        # 杂志海报风蓝白灰（< 10KB）
├── 00-cover.jpg     # 4 张配图 + 1 logo
├── 01-xxx.jpg
├── 02-xxx.jpg
├── 03-xxx.jpg
└── 00-logo.jpg      # 1:1 logo
```

**index.html 模板**（按 zip-artifact-spec §5）：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport"
        content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <title>{课程标题}</title>
  <link rel="stylesheet" href="./style.css" />
</head>
<body>
  <nav class="nav" id="top-nav">
    <a href="#home" class="nav-logo">{项目 logo}</a>
    <div class="nav-actions" id="nav-actions"></div>
  </nav>
  <main id="app"></main>
  <script src="./data.js"></script>
  <script src="./main.js"></script>
</body>
</html>
```

**data.js 模板**（用反引号避免引号陷阱，**关键**）：

```js
window.COURSE_DATA = {
  meta: { title, subtitle, motto, coverImage, author },
  courses: [
    {
      id: 1, title, subtitle, duration, image, built: true,
      hook, sections: [{heading, body}, ...], quote, action
    },
    // ... 5-7 节
  ]
};
```

**main.js 模板**（SPA 路由 + 3 视图）：

```js
(function () {
  var data = window.COURSE_DATA;
  var app = document.getElementById('app');
  var navActions = document.getElementById('nav-actions');

  function renderHome() { /* 课程目录页 */ }
  function renderCourse(id) { /* 课程详情页 + 顶栏/底部导航 */ }

  function handleRoute() {
    var hash = window.location.hash || '#home';
    // home / #course-{id}
  }

  window.addEventListener('hashchange', handleRoute);
  handleRoute();
})();
```

**style.css 模板**（杂志海报风蓝白灰）：

```css
:root {
  --bg-deep: #0a1929;
  --bg-card: #112240;
  --accent: #64ffda;
  --text-primary: #ccd6f6;
  --white: #e6f1ff;
  --border: rgba(100, 255, 218, 0.15);
}
body { font-family: system fonts; background: var(--bg-deep); color: var(--text-primary); }
/* 顶栏 / 课程列表 / 课程详情 / 底部导航 ... */
```

**输出**：4 个代码文件 + 1 个数据文件

### Step 5 · 打包上传（10 分钟）

**目的**：打 zip + 自检 + 上传小红书。

**打包命令**（**关键**：压缩目录内容，不是目录本身）：

```bash
cd {项目目录}
zip -r {输出 zip} . -x '*.DS_Store'
```

**自检清单**（zip-artifact-spec §6，6 项）：

| # | 项 | 通过条件 |
|---|---|---|
| 1 | **包结构** | index.html 在 zip 根目录（**不是** {项目名}/index.html） |
| 2 | **DOCTYPE / lang / charset / viewport** | 4 个全有 |
| 3 | **禁用项** | 无内联 `<script>` / 无 `onclick=` / 无 `javascript:` / 无 `eval(` / 无 `<iframe>` / 无 `<base href>` |
| 4 | **外链资源** | 0 个 `https://` 引用（图 / CSS / JS / 字体） |
| 5 | **路径** | 全部相对路径 `./xxx`，无 `/xxx` 绝对路径 |
| 6 | **体积** | 推荐总包 < 2MB（实测 2-3MB 也 OK）；单图 < 800KB |

**上传到小红书**（创作者中心 → 小工具）：

1. 打开 `creator.xiaohongshu.com` → Builder hub → 小工具
2. **第一步**：调整代码格式（自动校验 zip 结构）—— 这一步失败 = 你的 zip 结构错
3. **第二步**：上传并部署 —— 这一步失败通常是 vibe RPC server 临时 timeout，**5 分钟后重试**
4. **图标框**：上传 `00-logo.jpg`（1:1，< 5MB）
5. 填课程元数据（标题 / 简介 / 场景标签）
6. **发布**

**输出**：zip 上传成功 + 小红书后台能搜到这门课

---

## 4 大关键决策

### 决策 1 · 图必须**拍平到 zip 根**（不能用 `assets/` 子目录）

**问题**：小红书"小工具"容器对 `assets/` 子目录的图片引用有 bug，alt 文字会显示但图片加载失败。

**解决**：所有图直接放 zip 根，跟 `index.html` 同级：

```
# ❌ 错的（图片加载失败）
tool.zip
├── index.html
└── assets/
    └── 00-cover.jpg

# ✅ 对的（图片绝对能加载）
tool.zip
├── index.html
└── 00-cover.jpg
```

**数据同步**：data.js 里 `image: "./00-cover.jpg"`（不是 `./assets/00-cover.jpg`）

### 决策 2 · JS 字符串值**必须用反引号**（不能用双引号）

**问题**：中文字符串里嵌英文双引号 `"..."`（中文引号用法），跟 JS 外层双引号冲突 → 整个 data.js 解析失败 → `window.COURSE_DATA` 是 undefined → 整页空白。

**解决**：所有 string value 用 template literal（反引号 \`...`）包：

```js
// ❌ 错的（双引号嵌套）
{
  hook: "你以为你用的是 AI，其实是 LLM"思考者""
}
// ↑ "思考者"" 会终止外层字符串，JS 解析失败

// ✅ 对的（反引号包）
{
  hook: `你以为你用的是 AI，其实是 LLM"思考者"`
}
// ↑ " 不影响反引号字符串
```

**自动化检测**：

```bash
# 提取出 data.js 里的双引号嵌套行
grep -nE '"[^"]*"[^,]*"[^"]*"' data.js
# 输出空 = 没有嵌套问题
```

### 决策 3 · AI 图里**不放中文**（HTML 文字层覆盖）

**问题**：AI 生图对中文长句渲染不可靠，容易出现错字 / 漏字 / 鬼画符。

**解决**：

- **AI 图**：只画视觉骨架（4 层金字塔 / 流程图 / 4 层栈剖面），少量英文标签或符号
- **HTML 文字层**：覆盖所有中文标题 / 段落 / 标签

**好处**：
- 中文 100% 准确
- 视觉风格由 AI 保证
- 修改文字不用重生图

### 决策 4 · 体积控制：**单图 < 800KB，总包 < 3MB**

**实测**：

| 配置 | 大小 |
|---|---|
| 4 张 2K PNG | 9.3MB ❌ 超 |
| 4 张 2K JPG（quality 85） | 3.1MB ⚠️ 略超 |
| **4 张 2K JPG（quality 75）** | **2.6MB ✅** |
| 1 张 1:1 logo（quality 90） | 443KB ✅ |
| 代码（4 文件） | ~45KB ✅ |

**命令**：

```bash
# PNG → JPG quality 75
for f in *.png; do
  sips -s format jpeg -s formatOptions 75 "$f" --out "${f%.png}.jpg"
done
```

---

## 5 条反模式

### 反模式 1 · ❌ 评分小工具

> 用户原始反馈："这种评分小工具很鸡肋"

**问题**：
- 评分 = 假装权威（其实只是关键词命中数）
- 用完即弃（没有沉淀价值）
- 规则型打分对"伪装成好标题的烂标题"完全失效

**修正**：用长篇讲解（H5 课程页）替代——读 5-10 分钟 + 收藏 + 反复看，价值翻 10 倍。

### 反模式 2 · ❌ 多 HTML 页面

容器**强制**单页 + JS 视图切换：

```html
<!-- ❌ 错的（多 HTML） -->
<a href="course-1.html">课 1</a>
<a href="course-2.html">课 2</a>

<!-- ✅ 对的（SPA hash 路由） -->
<a href="#home">目录</a>
<a href="#course-1">课 1</a>
<a href="#course-2">课 2</a>
```

### 反模式 3 · ❌ 内嵌 script / 行内事件

容器 CSP **禁用** `unsafe-inline`：

```html
<!-- ❌ 全错 -->
<script>console.log('hi')</script>
<button onclick="go()">去</button>

<!-- ✅ 全对 -->
<script src="./main.js"></script>
<button id="go">去</button>
// main.js
document.getElementById('go').addEventListener('click', go);
```

### 反模式 4 · ❌ 绝对路径 / 外链

```html
<!-- ❌ -->
<img src="/00-cover.jpg">  <!-- 容器根目录不是 / -->
<img src="https://cdn.example.com/x.jpg">  <!-- 不联网 -->
<link rel="stylesheet" href="https://fonts.com/...">  <!-- 不联网 -->

<!-- ✅ -->
<img src="./00-cover.jpg">
```

### 反模式 5 · ❌ logo 强调内部框架数字

> 用户原始反馈："4 看不懂，4 从来不是重点，小白也能看懂的 AI 知识才对"

**问题**：内部技术框架（"4 层栈" / "5 步流程"）对小白用户没意义，logo 应该强调"是什么"而不是"怎么分"。

**修正**：

- ❌ 数字 + 内部框架（"4" / "STACK" / "5 STEPS"）
- ✅ 主题 + 友好副标（"AI" / "FROM ZERO" / "BRAIN 101" / "知识课程"）

---

## 6 项自检清单

打包前必走：

```bash
# 1. 包结构
unzip -l tool.zip | head -5
# 期望第一行直接是 index.html（不是 {项目名}/index.html）

# 2. DOCTYPE / lang / charset / viewport
grep -c "<!DOCTYPE html>" index.html     # = 1
grep -c 'lang="zh-CN"' index.html         # = 1
grep -c 'charset="UTF-8"' index.html      # = 1
grep -c "viewport-fit=cover" index.html   # = 1

# 3. 禁用项
grep -cE "<script>[^<]" index.html        # = 0
grep -c "onclick=" index.html             # = 0
grep -c "javascript:" index.html          # = 0
grep -cE "eval\(|new Function\(" main.js # = 0
grep -c "<iframe" index.html             # = 0

# 4. 外链
grep -E 'src="|href="' index.html | grep -E 'https?://'
# 期望：无输出

# 5. 路径
grep -E 'src="/|href="/' index.html
# 期望：无输出（全部用 ./xxx 相对路径）

# 6. 体积
du -sh tool.zip
# 期望：< 3MB
```

---

## 实战案例

**`examples/ai-knowledge-stack/`** —— 完整可参考案例。

| 维度 | 值 |
|---|---|
| 主题 | 零基础入门 AI 知识（4 层栈） |
| 课程数 | 7 节 |
| 总字数 | 6,722 字 |
| 配图 | 4 张 16:9 + 1 张 1:1 logo |
| zip 大小 | 3.0MB |
| 上传结果 | 成功 |

**5 节长文（已写在 data.js）可直接套用**——下次想出"X 知识 Y 层栈"系列（如"交易知识 5 层栈"），把 `data.js` 里的 7 节课内容替换即可，**模板代码 0 改动**。

---

## 可复用模板

**`templates/`** 4 个文件可作为下次新课程的起点：

| 文件 | 大小 | 用途 |
|---|---|---|
| `templates/index.html` | < 1KB | 壳（顶栏 + 视图容器 + 2 个 script src） |
| `templates/main.js` | < 8KB | SPA 路由 + renderHome + renderCourse + 顶栏/底部导航 |
| `templates/data.js` | < 3KB | 1 节占位 + 6 节占位 + 鸡汤句 |
| `templates/style.css` | < 10KB | 杂志海报风蓝白灰 + 课程列表 + 详情 + 导航 |

**复用流程**：

```bash
# 1. 复制模板到新项目
cp -r templates/ my-new-course/

# 2. 替换 data.js 里的 7 节课内容（保持 4 段 + 金句 + 行动结构）
# 3. 跑 Step 3-5（生图 + 改标题 + 打包上传）
```

**复用边角**：
- 同一 [4 STYLE] 段 → 任何"科技杂志风"图都能用
- 同一 SPA 架构 → 任何"多课程 / 多文章 / 多案例"场景都能用
- 同一杂志配色（蓝白灰）→ 任何"硬核技术 / 财经 / 教育"主题都能用

---

## 30 分钟起步（精简版）

```bash
# 1. 复制模板
cp -r templates/ my-course/
cd my-course

# 2. 写 7 节课内容到 data.js（30-60 分钟手写或 AI 辅助）
#    钩子 + 4 段 + 金句 + 行动 / 节

# 3. 生 4 张 16:9 + 1 张 1:1 logo（matrix MCP · 共享 [4 STYLE] 段）

# 4. 改 meta.title / coverImage / motto

# 5. 跑自检 + 打 zip
zip -r ../my-course.zip . -x '*.DS_Store'

# 6. 上传小红书创作者中心 → 小工具
```

---

## 延伸阅读

- **3F Content 范式**（pretty-skills 通用）→ `pretty-skills/content-triple-format/`
- **AI 生图 5 段式 prompt**（v3.23 认知锚点）→ pretty-skills 领悟 2
- **杂志海报风 5 大风格** → pretty-skills 视觉风格预设
- **pretty-skills 节奏**（3-6 个月实战 → knowhub）→ `pretty-skills/STRUCTURE.md`
- **真实案例** → `examples/ai-knowledge-stack/`

---

*最后更新：2026-07-14 · 基于"零基础入门 AI 知识"7 节课 H5 实战沉淀 · 跑 1 次可复用，后续跑 3-6 个月稳定后考虑升 knowhub methodology。*
