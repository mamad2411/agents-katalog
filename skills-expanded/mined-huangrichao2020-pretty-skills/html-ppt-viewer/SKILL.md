---
name: html-ppt-viewer
description: 把 N 张已经做好的图（AI 生图 / 截图 / 视觉稿）打包成一个**单页 PPT 风格 HTML 阅读器**：左侧 sidebar 翻页 + 中间大图全屏 + 键盘快捷键 + 浏览器打开即用。不是用 PPT，是用 HTML 模拟 PPT 体验。零依赖、秒加载、可分享链接、跨平台。
version: 2.0.0
author: Mavis · MiniMax Agent
triggers:
  - "做成 HTML PPT 阅读器"
  - "像 PPT 一样的 HTML"
  - "图打包成可翻页网页"
  - "PPT 风格 HTML 页面"
  - "我有一堆图想让人翻页看"
  - "可分享的网页 PPT"
  - "HTML 阅读器"
---

# HTML PPT 阅读器 Skill

## ⚠️ 出图前必走 · ppt 出图法 V2 7 步

**重要**：本 skill 只负责"把已有图打包成 HTML"。**生图前**必须走ppt 出图法 V2 7 步：

```
1. fetch 完整仓库内容（README + 子目录 + examples 并行）
2. reset todo（明确节奏）
3. 整理 "N 张图主题+核心一句话" 清单（每张 1 行）
4. 单张 prompt ≤ 60 行（不堆字体铁律）
5. 出 P1 hook → 渲染核对清单（10+ 项）→ 走批量
6. 接受 AI 主动加的细节和布局调整
7. 沉淀到 case 文档
```

ppt 出图法 V2 完整方法论见 `~/.mavis/knowledge/knowhub/domains/visual-creation/methodology/ppt-out-image-method.md`。

**反例**（2026-07-02 how-to-agent-ppt）：因为没走 V2 7 步 → PPT 图字体幼稚、布局不丰富、AI 调整被否定 → 用户反馈"前天的好多了"。

**正例**（2026-06-30 ai-training-ppt）：走了 V2 7 步 → 60 行 prompt + 接受 AI 加细节 + 渲染核对 → 8 张图一气呵成。

跳过 V2 7 步直接调本 skill = 极大概率翻车。

---

## 一句话定位

```
"我有一堆图，想让人像看 PPT 一样翻页看"
       ↓
   HTML 阅读器（PPT 风格 + 浏览器打开 + 键盘翻页）
       ↓
   chokepoint-ppt · ai-training-ppt · weekly-outlook-html · 任何"图片集"
```

## 5 区域架构

```
┌─────────────────────────────────────────────┐
│  [顶部]  品牌 logo + 标题 + badge           │
├──────┬──────────────────────────────────────┤
│      │  [tag + 标题 + 副标题]              │
│ side │  ┌──────────────────────────────┐    │
│ bar  │  │      [大图全屏展示区]        │    │
│      │  └──────────────────────────────┘    │
│      │  [← Prev / 1 of N / Next →]         │
└──────┴──────────────────────────────────────┘
        [角落] 键盘提示 ← → / 1-N
```

## 完整可复用模板（直接复制改 pages[]）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>YOUR TITLE</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Noto Serif CJK SC', 'Songti SC', Georgia, serif;
      background: #FFF5F5;       /* 奶油粉 */
      color: #1a1a1a; overflow: hidden; height: 100vh;
    }
    .header {
      height: 64px; padding: 0 32px;
      background: linear-gradient(135deg, #FFF5F5 0%, #FFE8E8 100%);
      border-bottom: 2px solid #B8860B;       /* 古铜金 */
      display: flex; align-items: center; justify-content: space-between;
    }
    .header h1 { font-size: 22px; color: #B8860B; }
    .badge {
      background: #B8860B; color: white;
      padding: 4px 12px; border-radius: 12px;
      font-size: 13px; font-weight: 600;
    }
    .layout { display: flex; height: calc(100vh - 64px); }
    .sidebar {
      width: 280px; padding: 16px;
      background: #FAF0EE; border-right: 1px solid #E0D0CC;
      overflow-y: auto;
    }
    .sidebar-title {
      font-size: 13px; color: #886; margin-bottom: 8px;
      text-transform: uppercase; letter-spacing: 1px;
    }
    .page-item {
      padding: 12px 14px; margin-bottom: 6px;
      border-radius: 8px; cursor: pointer;
      transition: all 0.2s;
      border-left: 3px solid transparent;
    }
    .page-item:hover { background: #FFEEEE; }
    .page-item.active { background: #B8860B; color: white; border-left-color: #8B6608; }
    .page-item.active .page-num { color: rgba(255,255,255,0.8); }
    .page-num { font-size: 11px; color: #B8860B; font-weight: 700; margin-bottom: 4px; }
    .page-title { font-size: 14px; font-weight: 600; line-height: 1.4; }
    .main { flex: 1; padding: 24px 32px; display: flex; flex-direction: column; }
    .slide-meta { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
    .slide-tag {
      background: #B8860B; color: white; padding: 4px 10px;
      border-radius: 4px; font-size: 11px;
    }
    .slide-title { font-size: 26px; color: #1a1a1a; font-weight: 700; }
    .slide-subtitle { color: #666; font-size: 14px; margin-bottom: 16px; }
    .slide-frame {
      flex: 1; background: white; border-radius: 12px;
      box-shadow: 0 8px 24px rgba(184, 134, 11, 0.15);
      overflow: hidden; display: flex; align-items: center; justify-content: center;
    }
    .slide-image {
      max-width: 100%; max-height: 100%; object-fit: contain;
      animation: fadeIn 0.5s ease-out;
    }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .footer {
      margin-top: 16px; display: flex; align-items: center; justify-content: space-between;
    }
    .nav-btn {
      padding: 8px 20px; background: #B8860B; color: white;
      border: none; border-radius: 6px; cursor: pointer; font-size: 14px;
    }
    .nav-btn:disabled { opacity: 0.3; cursor: not-allowed; }
    .keyboard-hint {
      position: fixed; bottom: 16px; right: 24px;
      background: rgba(0,0,0,0.7); color: white;
      padding: 8px 14px; border-radius: 6px; font-size: 12px; opacity: 0.8;
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>YOUR TITLE</h1>
    <div class="badge">YOUR BADGE</div>
  </div>

  <div class="layout">
    <aside class="sidebar">
      <div class="sidebar-title">章节导航</div>
      <div id="page-list"></div>
    </aside>

    <main class="main">
      <div class="slide-meta">
        <span class="slide-tag" id="tag">P01 · TAG</span>
        <h2 class="slide-title" id="title">TITLE</h2>
      </div>
      <div class="slide-subtitle" id="subtitle">SUBTITLE</div>
      <div class="slide-frame">
        <img id="slide-img" class="slide-image" src="images/01.png" alt="">
      </div>
      <div class="footer">
        <button class="nav-btn" id="prev">← 上一页</button>
        <span id="counter">1 / N</span>
        <button class="nav-btn" id="next">下一页 →</button>
      </div>
    </main>
  </div>

  <div class="keyboard-hint">← → 翻页 · 1-N 跳转</div>

  <script>
    // 配置：只改这个数组就能复用
    const pages = [
      // { file: "01.png", title: "...", subtitle: "...", tag: "..." },
    ];

    let current = 0;
    const $ = id => document.getElementById(id);
    const $img = () => $("slide-img");

    function render() {
      const page = pages[current];
      $("tag").textContent = `P0${current+1} · ${page.tag}`;
      $("title").textContent = page.title;
      $("subtitle").textContent = page.subtitle;
      $img().src = `images/${page.file}`;
      $img().style.animation = 'none';
      void $img().offsetWidth;             // 重启动画
      $img().style.animation = 'fadeIn 0.5s ease-out';
      $("counter").textContent = `${current+1} / ${pages.length}`;
      $("prev").disabled = current === 0;
      $("next").disabled = current === pages.length - 1;
      document.querySelectorAll(".page-item").forEach((el, i) => {
        el.classList.toggle("active", i === current);
      });
    }

    function renderSidebar() {
      const list = pages.map((p, i) => `
        <div class="page-item" data-idx="${i}">
          <div class="page-num">PAGE ${String(i+1).padStart(2,"0")}</div>
          <div class="page-title">${p.title}</div>
        </div>
      `).join("");
      $("page-list").innerHTML = list;
      document.querySelectorAll(".page-item").forEach(el => {
        el.onclick = () => { current = parseInt(el.dataset.idx); render(); };
      });
    }

    $("prev").onclick = () => { if (current > 0) { current--; render(); } };
    $("next").onclick = () => { if (current < pages.length-1) { current++; render(); } };

    document.addEventListener("keydown", e => {
      if (e.key === "ArrowLeft" && current > 0) { current--; render(); }
      if (e.key === "ArrowRight" && current < pages.length-1) { current++; render(); }
      if (/^[1-9]$/.test(e.key)) {
        const idx = parseInt(e.key) - 1;
        if (idx < pages.length) { current = idx; render(); }
      }
      if (e.key === " ") { e.preventDefault(); $("next").click(); }
    });

    renderSidebar();
    render();
  </script>
</body>
</html>
```

## 颜色速记

| 元素 | 颜色 | 色值 |
|---|---|---|
| 奶油粉底 | 主背景 | `#FFF5F5` |
| 古铜金 | 强调色（标题/badge/按钮） | `#B8860B` |
| 侧栏 | 浅粉 | `#FAF0EE` |
| hover | 浅粉 | `#FFEEEE` |

## 部署方案

| 方式 | 命令 | 适合 |
|---|---|---|
| 本地双击 | `open index.html` | 自己看 |
| 本地 HTTP server | `python3 -m http.server 8080` | 局域网分享 |
| 已有的 nginx 静态目录 | `cp -r ./ppt /var/www/html/` | 生产 |
| GitHub Pages | `gh repo create my-ppt --public` | 免费长期 |

## 实战案例

| 案例 | 路径 | 特点 |
|---|---|---|
| chokepoint-ppt | `frontend/public/chokepoint-ppt/` | 7 大卡脖子赛道 · 10 页 · 已部署 Aliyun |
| ai-training-ppt | `ai-training-ppt/` | 8 张手绘科教风图 · AI 培训方法论 |
| weekly-outlook-html | `frontend/public/weekly-outlook/` | 8 节长图 · 周报内容 |

**完整 case 文档（含完整 HTML/Prompt）**：
- `~/.mavis/knowledge/knowhub/domains/visual-creation/cases/2026-07-01-html-ppt-viewer-ai-training.md`
- `~/.mavis/knowledge/knowhub/domains/visual-creation/methodology/html-ppt-viewer.md`（源头，最全）

## 常见坑

| 坑 | 避免 |
|---|---|
| 图片溢出 | `.slide-image` 加 `overflow: hidden` |
| Sidebar 太宽挤压主区 | sidebar 固定 280px，主区 flex:1 |
| 中文渲染走样 | font-family 链含 'Noto Serif CJK SC' |
| 动画只触发一次 | 手动重置 `style.animation = 'none'` 再恢复 |
| Space 翻页滚动页面 | `e.preventDefault()` 阻止默认行为 |
| Sidebar 内容多挤压 | sidebar 加 `overflow-y: auto` |

## 30 秒起步

1. 复制上面完整模板到 `index.html`
2. 把图扔进 `images/`（命名 01.png, 02.png ...）
3. 改 `pages[]` 数组（file / title / subtitle / tag）
4. 改顶部标题和 badge
5. 双击 index.html 验证

## 进阶扩展

- sidebar 加"折叠按钮"（280px 偏大时）
- sidebar 顶部加"全文搜索"过滤 page-item
- 进度条（sidebar 顶部 N/N 可视化）
- 全屏模式（F11 / Fullscreen API）
- PDF 导出（`window.print()` + `@media print`，每页一张图 A4）
