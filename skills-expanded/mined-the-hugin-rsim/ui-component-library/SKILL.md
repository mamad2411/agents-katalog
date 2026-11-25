# Skill: UI Component Library

**Purpose:** Catalog of ready-to-use HTML/CSS/JS components for dashboard projects.
Insert components directly — no reinventing each time.
**When:** Building a dashboard, admin panel, or monitoring UI in plain HTML/CSS/Jinja2.
**Output:** Ready CSS + HTML markup + formulas for each component.

---

## Дизайн-система (тёмная тема)

```css
:root {
  --bg:      #07090f;   /* page background */
  --surface: #0d1117;   /* cards, panels */
  --s2:      #131c27;   /* hover, inputs */
  --s3:      #18253a;   /* progress tracks */
  --border:  #1e2d3d;
  --border2: #2a3f57;
  --text:    #dce8f6;
  --muted:   #4e6278;
  --muted2:  #637b95;
  --accent:  #38bdf8;   /* sky blue — links, primary */
  --green:   #34d399;
  --crit:    #f43f5e;   /* CRITICAL */
  --high:    #fb923c;   /* HIGH */
  --med:     #fbbf24;   /* MEDIUM */
  --low:     #60a5fa;   /* LOW */
  --r:  5px;
  --r2: 8px;
}
```

---

## Components

### 1. KPI Card Strip

```css
.kpi-row { display:grid; grid-template-columns:repeat(auto-fill,minmax(110px,1fr)); gap:10px; margin-bottom:18px }
.kpi { background:var(--surface); border:1px solid var(--border); border-radius:var(--r2); padding:14px 16px; position:relative; overflow:hidden }
.kpi::after { content:''; position:absolute; top:0; left:0; right:0; height:2px }
.kpi.k-crit::after  { background:var(--crit) }
.kpi.k-high::after  { background:var(--high) }
.kpi.k-med::after   { background:var(--med) }
.kpi.k-green::after { background:var(--green) }
.kpi.k-accent::after{ background:var(--accent) }
.kpi.k-blue::after  { background:var(--low) }
.kpi-v { font-size:24px; font-weight:700; line-height:1; margin-bottom:5px }
.kpi-l { font-size:9.5px; font-weight:700; color:var(--muted); letter-spacing:.8px; text-transform:uppercase }
```

```html
<div class="kpi-row">
  <div class="kpi k-accent">
    <div class="kpi-v accent">{{ value }}</div>
    <div class="kpi-l">Label</div>
  </div>
  <div class="kpi k-crit">
    <div class="kpi-v crit">{{ value }}</div>
    <div class="kpi-l">Critical</div>
  </div>
</div>
```

---

### 2. SVG Score Ring

**Formula:** `dash = floor(score / 100 × C)`, where `C = floor(2π × r)`

| Размер | r  | C   | viewBox     |
|--------|----|-----|-------------|
| Small  | 13 | 82  | 0 0 38 38   |
| Large  | 20 | 126 | 0 0 52 52   |

```css
.s-ring { position:relative; width:38px; height:38px; flex-shrink:0 }
.s-ring svg { position:absolute; top:0; left:0 }
.s-ring .s-num { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700 }
/* stroke color helpers */
.rc      { stroke:var(--accent) }
.rc-crit { stroke:var(--crit) }
.rc-high { stroke:var(--high) }
.rc-med  { stroke:var(--med) }
```

```html
<!-- Small ring (r=13, C=82) -->
{% set dash = (score / 100 * 82)|int %}
{% set rclass = "rc-crit" if severity == "CRITICAL" else "rc-high" if severity == "HIGH" else "rc-med" if severity == "MEDIUM" else "rc" %}
<div class="s-ring">
  <svg width="38" height="38" viewBox="0 0 38 38" style="transform:rotate(-90deg)">
    <circle cx="19" cy="19" r="13" fill="none" stroke="var(--s3)" stroke-width="3"/>
    <circle cx="19" cy="19" r="13" fill="none" stroke-width="3" stroke-linecap="round"
            stroke-dasharray="{{ dash }} 82" class="{{ rclass }}"/>
  </svg>
  <span class="s-num sev-{{ severity }}">{{ score|int }}</span>
</div>
```

---

### 3. Severity Badge

```css
.badge { display:inline-flex; align-items:center; gap:4px; padding:2px 8px; border-radius:20px; font-size:10px; font-weight:700; letter-spacing:.4px; white-space:nowrap }
.badge-CRITICAL { background:rgba(244,63,94,.12);  color:var(--crit); border:1px solid rgba(244,63,94,.2) }
.badge-HIGH     { background:rgba(251,146,60,.12); color:var(--high); border:1px solid rgba(251,146,60,.2) }
.badge-MEDIUM   { background:rgba(251,191,36,.12); color:var(--med);  border:1px solid rgba(251,191,36,.2) }
.badge-LOW      { background:rgba(96,165,250,.12); color:var(--low);  border:1px solid rgba(96,165,250,.2) }
/* row left-border by severity */
tr.sev-CRITICAL { border-left:3px solid var(--crit) }
tr.sev-HIGH     { border-left:3px solid var(--high) }
tr.sev-MEDIUM   { border-left:3px solid var(--med) }
tr.sev-LOW      { border-left:3px solid var(--low) }
```

```html
<span class="badge badge-{{ severity }}">{{ emoji }} {{ severity }}</span>
```

---

### 4. Signal Bars (детекторы / scores)

```css
.sig-col { display:flex; flex-direction:column; gap:3px }
.sig-row { display:flex; align-items:center; gap:5px }
.sig-b   { height:4px; border-radius:2px; background:var(--accent); opacity:.65; min-width:2px }
.sig-n   { font-size:10px; color:var(--muted2); white-space:nowrap }
.sig-v   { font-size:10px; font-weight:600; min-width:22px; color:var(--text) }
```

```html
<div class="sig-col">
  {% for name, score in detector_scores %}
  <div class="sig-row">
    <div class="sig-b" style="width:{{ (score/100*44)|int }}px"></div>
    <span class="sig-v">{{ score }}</span>
    <span class="sig-n">{{ name.replace('_',' ') }}</span>
  </div>
  {% endfor %}
</div>
```

---

### 5. Bar Chart (bchart)

```css
.bchart { display:flex; flex-direction:column; gap:6px }
.brow   { display:flex; align-items:center; gap:10px }
.b-lbl  { width:100px; text-align:right; font-size:11px; color:var(--muted); flex-shrink:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap }
.b-track{ flex:1; height:10px; background:var(--s2); border-radius:5px; overflow:hidden }
.b-fill { height:100%; border-radius:5px; background:var(--accent); transition:width .3s }
.b-stat { font-size:11px; color:var(--text); min-width:70px; white-space:nowrap }
```

```html
<div class="bchart">
  {% for row in data %}
  <div class="brow">
    <span class="b-lbl">{{ row.label }}</span>
    <div class="b-track">
      <div class="b-fill" style="width:{{ (row.value / max_value * 100)|int }}%"></div>
    </div>
    <span class="b-stat">{{ row.value }}</span>
  </div>
  {% endfor %}
</div>
```

---

### 6. Panel

```css
.panel     { background:var(--surface); border:1px solid var(--border); border-radius:var(--r2); margin-bottom:14px }
.panel-hdr { padding:10px 16px; border-bottom:1px solid var(--border); font-size:10px; font-weight:700; color:var(--muted); letter-spacing:.8px; text-transform:uppercase; display:flex; align-items:center; gap:8px }
.panel-body{ padding:16px }
```

```html
<div class="panel">
  <div class="panel-hdr">Section title</div>
  <div class="panel-body">
    <!-- content -->
  </div>
</div>
```

---

### 7. Section Header

```css
.sec-hdr { font-size:10px; font-weight:700; color:var(--muted); letter-spacing:.9px; text-transform:uppercase; display:flex; align-items:center; gap:10px; margin:20px 0 10px }
.sec-hdr::after { content:''; flex:1; height:1px; background:var(--border) }
```

```html
<div class="sec-hdr">Section Name</div>
```

---

### 8. Profile Card

```css
.prof-card  { background:var(--surface); border:1px solid var(--border); border-radius:var(--r2); padding:20px 24px; margin-bottom:16px }
.prof-title { display:flex; align-items:center; gap:10px; margin-bottom:16px; flex-wrap:wrap }
.prof-name  { font-size:16px; font-weight:700 }
.metric-row { display:flex; gap:18px; flex-wrap:wrap; margin-bottom:14px }
.metric .m-l{ font-size:9.5px; font-weight:700; color:var(--muted); letter-spacing:.6px; text-transform:uppercase; margin-bottom:2px }
.metric .m-v{ font-size:17px; font-weight:700 }
```

```html
<div class="prof-card">
  <div class="prof-title">
    <!-- score ring + name + badge here -->
  </div>
  <div class="metric-row">
    <div class="metric">
      <div class="m-l">Label</div>
      <div class="m-v accent">{{ value }}</div>
    </div>
  </div>
</div>
```

---

### 9. Trade Direction Indicators

```css
.t-buy  { color:var(--green); font-weight:600 }
.t-sell { color:var(--crit);  font-weight:600 }
.t-sub  { font-size:11px; color:var(--muted2); margin-top:2px }
```

```html
{% if side == 'BUY' %}<span class="t-buy">▲ BUY</span>
{% else %}<span class="t-sell">▼ SELL</span>{% endif %}
```

---

### 10. Result Indicators

```css
.res-won  { color:var(--green) }
.res-lost { color:var(--crit) }
.res-na   { color:var(--muted) }
```

```html
{% if outcome == 'won' %}<span class="res-won" title="+{{ roi }}%">✓</span>
{% elif outcome == 'lost' %}<span class="res-lost" title="-100%">✗</span>
{% else %}<span class="res-na">·</span>{% endif %}
```

---

### 11. Relative Time (JS)

```js
function timeAgo(iso) {
  if (!iso) return '—';
  const s = iso.replace(' ', 'T');
  const n = /[Zz]$|[+-]\d\d:\d\d$/.test(s) ? s : s + 'Z';
  const d = Math.floor((Date.now() - new Date(n)) / 1000);
  if (isNaN(d) || d < 0) return iso.slice(0, 16);
  if (d < 60)    return d + 's';
  if (d < 3600)  return Math.floor(d / 60) + 'm';
  if (d < 86400) return Math.floor(d / 3600) + 'h';
  return Math.floor(d / 86400) + 'd';
}
// Apply to all .time-ago[data-ts] elements:
document.querySelectorAll('.time-ago[data-ts]').forEach(el => {
  if (el.dataset.ts) el.textContent = timeAgo(el.dataset.ts);
});
```

---

### 12. Lazy Wallet Name Loading (JS)

```js
// Requires /api/wallet-name/{addr} endpoint returning {name: string|null}
async function loadNames() {
  const links = document.querySelectorAll('.wallet-link[data-addr]');
  for (const el of links) {
    if (el.querySelector('.wallet-name')) continue;
    try {
      const r = await fetch(`/api/wallet-name/${el.dataset.addr}`);
      if (!r.ok) continue;
      const d = await r.json();
      if (d.name) el.innerHTML = `<span class="wallet-name" style="font-weight:600">${d.name}</span>`;
    } catch {}
    await new Promise(r => setTimeout(r, 400)); // rate limit: 400ms between requests
  }
}
loadNames();
```

> **Note:** if `.wallet-link` has other child elements (flags ⚑, address),
> preserve them before overwrite: check `el.innerHTML.includes('⚑')` before replacement.
