---
name: html-effectiveness-editor
description: 子 skill — 自定义编辑界面。当用户要在 HTML 里做"操作然后导出"的小工具时使用——拖拽分类板（triage）、配置编辑器（feature flag editor，输出 diff）、Prompt 调参器（live preview，输出 prompt）。每个编辑器**必须**有"复制结果"按钮让 UI 状态回到 agent。当父 skill 路由命中"triage/排序/配置/调 prompt/编辑器小工具"类请求时加载。
---

# 09-editor — 自定义编辑界面

> "Sometimes it's hard to describe what you want in a text box. Ask for a throwaway editor for the exact thing you're working on — and always end with an export button that turns whatever you did in the UI back into something you can paste into the agent or commit."

## 核心约束（不可妥协）

> **每个 09-editor 范式产出的页面必须有"复制结果"按钮**。
> 让用户在 UI 里的所有操作能 → 一段可粘贴的文本 → 回到 agent。
>
> 没有 export 出口的"编辑器" = 玩具，不是工具。

---

## 何时用

| 用户说 | 用哪个范式 | 模板 |
|-------|-----------|------|
| "20 个 ticket 帮我排优先级 / triage" | **拖拽分类板** | 自建 |
| "切一组 feature flag / 配置一些参数" | **配置编辑器** | 自建 |
| "调一个 prompt，要看几个样例" | **Prompt 调参器** | `../../templates/prompt.html` |
| "我要在 UI 里改完然后 copy 回来" | 任意 | — |

---

## 范式 9.1 · 拖拽分类板（triage board）

**空间形状**：N 列（典型 4 列：Now / Next / Later / Cut），每列一个 `<ul>`，卡片可在列间拖拽。顶部"Copy as markdown"导出。

**HTML5 drag-and-drop 关键 JS**：

```js
let dragged = null;
document.querySelectorAll('.card').forEach(c => {
  c.draggable = true;
  c.addEventListener('dragstart', () => { dragged = c; c.classList.add('dragging'); });
  c.addEventListener('dragend',   () => c.classList.remove('dragging'));
});

document.querySelectorAll('.column ul').forEach(col => {
  col.addEventListener('dragover', e => {
    e.preventDefault();
    const after = [...col.querySelectorAll('.card:not(.dragging)')]
      .find(c => e.clientY < c.getBoundingClientRect().top + c.offsetHeight / 2);
    if (after) col.insertBefore(dragged, after);
    else col.appendChild(dragged);
  });
});

// 导出
document.querySelector('#copy-md').onclick = async () => {
  const md = [...document.querySelectorAll('.column')].map(col => {
    const title = col.querySelector('h2').textContent;
    const items = [...col.querySelectorAll('.card')]
      .map(c => `- ${c.querySelector('.card-title').textContent.trim()}`)
      .join('\n');
    return `## ${title}\n${items}`;
  }).join('\n\n');
  await navigator.clipboard.writeText(md);
  document.querySelector('#copy-md').textContent = 'Copied ✓';
};
```

**关键 CSS**（列与拖拽态）：

```css
.board { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.column { background: var(--gray-100); border-radius: 12px; padding: 16px;
          min-height: 400px; }
.column h2 { font-size: 14px; text-transform: uppercase;
             letter-spacing: 0.06em; color: var(--gray-700); margin: 0 0 12px; }
.column ul { list-style: none; padding: 0; margin: 0;
             display: flex; flex-direction: column; gap: 8px; min-height: 100px; }
.card { background: var(--white); border: 1px solid var(--gray-300);
        border-radius: 8px; padding: 12px; cursor: grab; }
.card.dragging { opacity: 0.4; cursor: grabbing; }
.card:hover { border-color: var(--clay); }
```

无独立模板（数据因人而异，按需生成）。

---

## 范式 9.2 · 配置编辑器（feature flag editor）

**空间形状**：分组 fieldset，每个 flag 是 toggle。`change` 事件检查依赖（A 必须 B 也开）。"Copy diff" 输出**仅变化的 keys**。

**关键 JS**（diff 输出）：

```js
function readState() {
  const state = {};
  document.querySelectorAll('input[type="checkbox"][data-flag]').forEach(el => {
    state[el.dataset.flag] = el.checked;
  });
  return state;
}
const initial = readState();

// 依赖检查
document.addEventListener('change', () => {
  document.querySelectorAll('[data-requires]').forEach(el => {
    const reqs = el.dataset.requires.split(',');
    const unmet = reqs.find(r => !readState()[r]);
    el.parentElement.querySelector('.warning').hidden = !unmet || !el.checked;
    if (unmet && el.checked) {
      el.parentElement.querySelector('.warning').textContent =
        `Requires ${unmet} to be enabled`;
    }
  });
});

document.querySelector('#copy-diff').onclick = async () => {
  const now = readState();
  const diff = Object.fromEntries(
    Object.entries(now).filter(([k, v]) => initial[k] !== v)
  );
  if (Object.keys(diff).length === 0) {
    document.querySelector('#copy-diff').textContent = 'No changes';
    return;
  }
  await navigator.clipboard.writeText(JSON.stringify(diff, null, 2));
  document.querySelector('#copy-diff').textContent = 'Copied ✓';
};
```

无独立模板（flag 集合按项目而异）。

---

## 范式 9.3 · Prompt 调参器

**空间形状**：左 `<textarea>`（模板，含 `{{slot}}`）+ 右上 N 张样例输入卡 + 右下 N 张实时填充结果。键入立即重渲染。"Copy prompt" 输出当前模板。

**关键 JS**：

```js
const tpl = document.querySelector('#tpl');
const samples = JSON.parse(document.querySelector('#samples').textContent);

function fill(template, data) {
  return template.replace(/\{\{(\w+)\}\}/g, (_, k) =>
    data[k] != null ? data[k] : `{{${k}}}`
  );
}

function render() {
  document.querySelectorAll('.preview').forEach((p, i) => {
    p.textContent = fill(tpl.value, samples[i]);
  });
  document.querySelector('#tpl-meta').textContent =
    tpl.value.length + ' chars · ~' + Math.ceil(tpl.value.length / 4) + ' tokens';
}

tpl.addEventListener('input', render);
document.querySelector('#copy-tpl').onclick = async () => {
  await navigator.clipboard.writeText(tpl.value);
};
render();
```

样例数据嵌在页面里（不调外部 API）：

```html
<script type="application/json" id="samples">
[
  { "label": "Frustrated", "customer_name": "Mira", "tone": "calm", "issue": "..." },
  { "label": "Confused",   "customer_name": "Devon", "tone": "warm",  "issue": "..." }
]
</script>
```

**直接可用模板**：[`../../templates/prompt.html`](../../templates/prompt.html) — 含 3 个真实样例和 live preview。

---

## 通用导出按钮模板（标准实现）

```js
async function copyResult(text, btn) {
  try {
    await navigator.clipboard.writeText(text);
    const old = btn.textContent;
    btn.textContent = 'Copied ✓';
    setTimeout(() => { btn.textContent = old; }, 1500);
  } catch (e) {
    btn.textContent = 'Press Ctrl+C';
    // fallback: select hidden textarea + execCommand('copy')
  }
}
```

---

## 共同原则

- **永远有 export 按钮**——这是 09-editor 的标志，没有就不是这个范式
- **Export 格式服从 agent**——markdown / JSON diff / 纯文本，看用户后续要怎么用
- **真实数据 mock**——不要"Sample 1, Sample 2"，要 "Frustrated · long-time user / Confused · new user"
- **拖拽要有 hover 视觉反馈**——`.card.dragging { opacity: 0.4 }` 是底线
- **配置编辑器的依赖警告必须立即出现**——用 `change` event，不是 submit
- **Prompt 调参器的 token 计数估算用 chars/4**——不需要真 tokenizer
