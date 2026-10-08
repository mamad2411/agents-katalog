---
name: html-effectiveness-report
description: 子 skill — 周期性报告。当用户要写每周状态报告（status.html，KPI/已发货/速率/carryover）或事故 postmortem（postmortem.html，timeline/根因/影响/行动项）时使用。当父 skill 路由命中"周报/状态/status report/postmortem/事故/RCA"类请求时加载。
---

# 08-report — 周期性报告

> "Recurring documents — status updates, post-mortems — benefit most from a bit of structure and color. A small chart and a colored timeline turn something people skim into something they actually read."

## 何时用

| 用户说 | 用哪个范式 | 模板 |
|-------|-----------|------|
| "写一份这周的 engineering status" | **状态周报** | `../../templates/status.html` |
| "周报模板填一下" | 同上 | 同上 |
| "昨天那个 incident 的 postmortem" | **事故报告** | `../../templates/postmortem.html` |
| "RCA / SEV-2 总结" | 同上 | 同上 |

---

## 范式 8.1 · 状态周报

**空间形状**：5 段，按"扫一眼 → 细看 → 跟进"顺序
1. **4 大数字 KPI** — 顶部一行卡片，3 秒能看完
2. **Highlights** — 3 个 bullet（高亮事件，不是流水账）
3. **Shipped** — 表格 (PR / Title / Author / Risk)
4. **Velocity** — 7 天柱状图（小图，不喧宾夺主）
5. **Carryover** — 三段 in-review / blocked / slipped，用 border-left 颜色区分

**关键 CSS**：

```css
.kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.kpi { padding: 20px; border-radius: 12px; background: var(--white);
       border: 1px solid var(--gray-300); }
.kpi .num { font-size: 36px; font-weight: 500; line-height: 1; }
.kpi .label { color: var(--gray-700); font-size: 13px; margin-top: 6px; }
.kpi .delta.up { color: var(--success); }
.kpi .delta.down { color: var(--danger); }

.carryover .item { border-left: 3px solid; padding: 12px 16px;
                   background: var(--white); border-radius: 8px; }
.carryover .in-review { border-left-color: var(--info); }
.carryover .blocked   { border-left-color: var(--warning); }
.carryover .slipped   { border-left-color: var(--gray-500); }
```

**Velocity 柱状图技巧**（不需要 Chart.js）：

```html
<div class="chart">
  <div class="bar"><div class="col" style="height:0%"  data-v="0"></div><small>Mon</small></div>
  <div class="bar"><div class="col" style="height:25%" data-v="1"></div><small>Tue</small></div>
  <!-- ... -->
</div>
```

```css
.chart { display: flex; align-items: flex-end; gap: 12px; height: 140px; }
.bar { flex: 1; display: flex; flex-direction: column; gap: 6px; }
.bar .col { width: 100%; max-width: 56px; background: var(--clay);
            border-radius: 4px 4px 0 0; position: relative; }
.bar .col::before { content: attr(data-v); position: absolute;
                    top: -22px; left: 50%; transform: translateX(-50%);
                    font-size: 12px; }
```

参见 `../shared/components.html` 第 3 节"KPI tiles"和第 4 节"Carryover items"。

**直接可用模板**：[`../../templates/status.html`](../../templates/status.html)

---

## 范式 8.2 · 事故报告（postmortem）

**空间形状**：5 段
1. **TL;DR** — 一段话：发生了什么、影响多大、怎么 mitigate 的
2. **Timeline** — 分钟级时间戳（用 `<ol class="timeline">` + `<time>`）
3. **Root cause** — 散文 + config diff 高亮（如有）
4. **Impact** — 表格 (失败请求数 / 错误率峰值 / 影响用户数 / 数据丢失 / SLA)
5. **Action items** — 表格 (Owner / Description / Due date)

**关键 CSS**（时间线）：

```css
.timeline { list-style: none; padding-left: 16px;
            border-left: 2px solid var(--gray-300); }
.timeline li { position: relative; padding: 8px 0 8px 24px; }
.timeline li::before { content: ''; position: absolute; left: -25px; top: 14px;
                       width: 12px; height: 12px; border-radius: 50%;
                       background: var(--clay); }
.timeline time { font-family: var(--font-mono); font-size: 13px;
                 color: var(--gray-700); display: inline-block; width: 60px; }
```

`shared/base.css` 已含 `.timeline`，直接使用。

**Action items 表格**：

```html
<table class="actions">
  <thead><tr><th>Owner</th><th>Action</th><th>Due</th></tr></thead>
  <tbody>
    <tr><td>DP</td><td>Revert cfg-9a12 and restore pool limit to 64</td><td>Apr 12</td></tr>
    <tr><td>MO</td><td>Add config-linter range check for max_connections</td><td>Apr 18</td></tr>
    <tr><td>SR</td><td>Surface "recent config rollouts" alongside deploys</td><td>Apr 25</td></tr>
  </tbody>
</table>
```

**直接可用模板**：[`../../templates/postmortem.html`](../../templates/postmortem.html)

---

## 共同原则

- **数字必须具体**——不要"latency improved"，要"p99 1.4s → 180ms"
- **timestamp 必须分钟级**——`14:02 / 14:06 / 14:31` 比 "around 2pm" 强 100 倍
- **行动项必须有 owner 和 due date**——没 owner 的 action 等于不存在
- **Carryover 三段必须用颜色区分**——in-review/blocked/slipped 是不同情绪
- **不要在 KPI 卡片里放图表**——KPI 是数字，图是图，分开
