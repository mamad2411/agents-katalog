---
name: html-effectiveness-review
description: 子 skill — 代码评审与理解。当用户要 PR 评审、PR 写作（作者侧）、或要理解陌生代码模块的请求路径/调用栈时使用。包含 PR 评审（diff.html）、PR 写作（pr.html）、模块图三种范式。当父 skill 路由命中"评审/PR/审阅/这段代码怎么工作"类请求时加载。
---

# 02-review — 代码评审与理解

> "Diffs and call-graphs are spatial information; markdown flattens them. Let the agent render the change as an annotated diff, draw the module as boxes and arrows, or write the PR description your reviewers actually want."

## 何时用

| 用户说 | 用哪个范式 | 模板 |
|-------|-----------|------|
| "review this PR / 评审一下 #312" | **PR 评审** (reviewer 视角) | `../../templates/diff.html` |
| "帮我写 PR 描述 / write a PR writeup" | **PR 写作** (author 视角) | `../../templates/pr.html` |
| "X 在这个 repo 怎么工作 / 调用栈是什么" | **模块图** | 自建（见下） |
| "解释一下 auth flow / sync 是怎么转的" | **模块图** | 同上 |

---

## 范式 2.1 · PR 评审（reviewer 视角）

**空间形状**：
- 顶部：一句话总结 + **文件风险地图**（每文件一个圆点，颜色=风险，大小=改动量）
- 文件列表：每文件折叠区块；标题含 risk badge + diff 行数；展开看带行号 diff
- 行号 diff 必须**等宽对齐**

**风险标签 3 档**（不要再细分，用户记不住）：
- `safe` — 纯加法 / 类型扩展 / 测试 → 绿色
- `worth a look` — 行为微变 / 重构 → 黄色
- `needs attention` — 关键路径 / 新抽象 / 易错点 → 红色

**HTML 骨架**：

```html
<header class="pr-summary">
  <h1>PR #247 — Review Summary</h1>
  <p>[一句话: what this PR does]</p>
</header>

<section class="risk-map">
  <h2>Risk map</h2>
  <svg viewBox="0 0 600 120">
    <g><circle cx="60"  cy="60" r="14" class="needs-attn" />
       <text x="60" y="95" text-anchor="middle">useOptimisticTasks.ts</text></g>
    <g><circle cx="160" cy="60" r="20" class="worth" />
       <text x="160" y="95" text-anchor="middle">TaskList.tsx</text></g>
    <!-- ... 圆点大小 = LOC log；位置随便排但保持视觉密度 -->
  </svg>
</section>

<section class="files">
  <details open>
    <summary>
      <code>src/hooks/useOptimisticTasks.ts</code>
      <span class="badge danger">needs attention</span>
      <span class="muted">+58 −0</span>
    </summary>
    <pre class="diff"><div class="line added"><span class="ln">12</span><span>+ ...</span></div></pre>
  </details>
</section>
```

**关键 CSS**（diff 行号）：

```css
.diff { font-family: var(--font-mono); font-size: 12.5px; line-height: 1.55; }
.diff .line { display: grid; grid-template-columns: 56px 1fr; gap: 0; }
.diff .ln { color: var(--gray-500); padding: 0 12px; text-align: right;
            background: var(--gray-100); user-select: none; }
.diff .added   { background: rgba(120, 140, 93, 0.12); }
.diff .removed { background: rgba(176, 74, 74, 0.10); }
```

`shared/base.css` 已含上述类，直接使用。

**直接可用模板**：[`../../templates/diff.html`](../../templates/diff.html)

---

## 范式 2.2 · PR 写作（author 视角）

**空间形状**：6 段，按 reviewer 阅读顺序排：
1. **TL;DR 框** — 一段话讲完动机和结果
2. **Why** — 为什么之前的做法不行
3. **Before / After** — 双列对比，4 条 vs 4 条
4. **File-by-file** — 按建议阅读顺序，每文件折叠
5. **Where to focus** — 编号 1/2/3，每条说"看这里因为什么"，含 "what I deliberately did NOT do"
6. **Test plan** — unit / integration / staging / manual 四组
7. **Rollout** — Day 0 / Day 2 / Day 4 阶梯

**关键 CSS**（rollout 阶梯）：

```css
ol.ramp { list-style: none; padding: 0; display: grid;
          grid-template-columns: repeat(3, 1fr); gap: 12px; }
ol.ramp li { padding: 16px 18px; background: var(--white);
             border: 1px solid var(--gray-300); border-radius: 10px;
             display: flex; flex-direction: column; gap: 4px; }
ol.ramp .pct { font-size: 22px; font-weight: 500; color: var(--clay); }
```

**直接可用模板**：[`../../templates/pr.html`](../../templates/pr.html)

---

## 范式 2.3 · 模块图 / Code Understanding

**空间形状**：
- 顶部：请求路径 SVG（盒子 + 箭头），高亮 hot path
- 下方：编号 1/2/3/4/5 的 callstack
  - 每步：文件名 + 行号 + 一段中英说明 + `<details>` 折叠源码

**关键 CSS**：

```css
.callstack li { display: grid; grid-template-columns: 32px 1fr; gap: 16px;
                margin-bottom: 24px; list-style: none; }
.callstack .num { width: 32px; height: 32px; border-radius: 50%;
                  background: var(--clay); color: white; display: grid;
                  place-items: center; font-weight: 600;
                  font-family: var(--font-mono); }
.callstack .file { font-family: var(--font-mono); font-size: 13px;
                   color: var(--gray-700); }
.callstack details summary { cursor: pointer; padding: 6px 0;
                              color: var(--info); font-size: 13px; }
```

无独立模板（按需生成，结构清晰，可由 plan.html 的 step 部分启发）。

---

## 共同原则

- **风险标签必须是 agent 真给出的判断**，不要"All files look fine"
- **行号 diff 必须等宽**——浏览器渲染才有"diff"的感觉
- **Where to focus 永远要有 "what I did NOT do"**——避免 reviewer 浪费时间提"为什么没加 X"
- **PR 写作的 file-by-file 要按阅读顺序**，不是字母序——告诉 reviewer 从哪开始
