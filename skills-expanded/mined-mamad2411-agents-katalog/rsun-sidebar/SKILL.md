---
name: rsun-sidebar
description: 容晟科技 TRACKER 系列頁面的可收合側欄元件。當需要在 HTML 頁面新增或修改側欄時使用。包含 section 收合、整體收合、手機 Drawer、localStorage 記憶。
user-invocable: true
allowed-tools: "Read Edit Write Bash(ls *)"
---

# rsun-sidebar — 可收合側欄元件

適用於 `~/Projects/TRACKER/*.html` 及任何容晟禪意設計系統的靜態 HTML 頁面。

---

## 版型結構

```
body  (display:flex; flex-direction:column; height:100vh; overflow:hidden)
├── .topbar          ← 固定頂欄，放 logo + 功能按鈕
├── .sb-expand-pill  ← 側欄收合後浮出的 ▶ 藥丸（桌機用）
├── .sb-backdrop     ← 手機遮罩（點擊關閉 drawer）
└── .layout  (display:flex; flex:1; min-height:0; overflow:hidden)
    ├── .sidebar  (flex-shrink:0; width:200px; overflow-y:auto)
    │   ├── [.sb-group ×N]  ← 每個 section 一個 group
    │   │   ├── button.sb-group-toggle  data-id="唯一id"  ← 點擊收合
    │   │   └── .sb-group-body
    │   │       └── a.nav-link  ← 頁面連結
    │   └── button.sb-collapse-btn  ← ◀ 整體收合按鈕
    └── .main  (flex:1; overflow-y:auto; overflow-x:hidden)
        └── 頁面主要內容
```

---

## CSS（貼在 `</style>` 之前）

```css
/* === Sidebar collapse & groups === */
.sidebar{transition:width .22s ease,min-width .22s ease,padding .22s ease}
body.sidebar-collapsed .sidebar{width:0;min-width:0;overflow:hidden;padding:0}

.sb-group{border-bottom:1px solid rgba(216,206,188,.3)}
.sb-group-toggle{display:flex;align-items:center;justify-content:space-between;width:100%;padding:7px 18px 4px;font-size:11px;font-weight:700;color:var(--muted2);letter-spacing:1.2px;text-transform:uppercase;margin-top:10px;background:none;border:none;cursor:pointer;text-align:left;font-family:inherit;line-height:1.5}
.sb-group-toggle:hover{color:var(--text)}
.sb-arr{font-size:10px;transition:transform .2s;flex-shrink:0;margin-left:4px}
.sb-group.closed .sb-arr{transform:rotate(-90deg)}
.sb-group-body{overflow:hidden;transition:max-height .25s ease;max-height:600px}
.sb-group.closed .sb-group-body{max-height:0}

.sb-collapse-btn{display:flex;align-items:center;gap:6px;width:100%;padding:10px 18px;margin-top:12px;background:none;border:none;border-top:1px solid var(--border);cursor:pointer;font-size:12px;color:var(--muted2);font-family:inherit;text-align:left}
.sb-collapse-btn:hover{color:var(--text)}

.sb-expand-pill{display:none;position:fixed;left:0;top:50vh;transform:translateY(-50%);z-index:97;background:var(--card);border:1px solid var(--border);border-left:none;border-radius:0 8px 8px 0;padding:10px 8px;cursor:pointer;font-size:13px;color:var(--muted);box-shadow:2px 0 8px rgba(42,35,24,.08)}
.sb-expand-pill:hover{color:var(--text)}
body.sidebar-collapsed .sb-expand-pill{display:block}

.mobile-menu-btn{display:none;align-items:center;justify-content:center;width:32px;height:32px;background:none;border:1px solid var(--border);border-radius:6px;cursor:pointer;font-size:16px;color:var(--muted)}
.mobile-menu-btn:hover{color:var(--text)}

.sb-backdrop{display:none;position:fixed;inset:0;background:rgba(42,31,14,.45);z-index:98;backdrop-filter:blur(2px)}
.sb-backdrop.open{display:block}

@media(max-width:768px){
  .sidebar{position:fixed;left:0;top:0;height:100vh;z-index:99;transform:translateX(-100%);transition:transform .25s ease;width:220px!important;min-width:220px!important;padding:16px 0!important;overflow-y:auto}
  .sidebar.mobile-open{transform:translateX(0)}
  body.sidebar-collapsed .sidebar{width:220px!important;min-width:220px!important;overflow:auto!important;padding:16px 0!important;transform:translateX(-100%)}
  .sb-expand-pill{display:none!important}
  .sb-collapse-btn{display:none!important}
  .mobile-menu-btn{display:inline-flex}
}
```

---

## HTML — Sidebar 骨架

```html
<!-- 貼在 .layout 內，.main 之前 -->
<div class="sidebar" id="sidebar">

  <!-- GROUP 1：TRACKER 總覽 -->
  <div class="sb-group">
    <button class="sb-group-toggle" data-id="XX-tracker" onclick="toggleSbGroup(this)">
      TRACKER <span class="sb-arr">▾</span>
    </button>
    <div class="sb-group-body">
      <a href="/index.html" class="nav-link">📋 總覽</a>
      <a href="/clients/index.html" class="nav-link">👥 客戶 CRM</a>
      <a href="/livelink.html" class="nav-link">🔗 LiveLink</a>
      <a href="/ceyan.html" class="nav-link">🌿 澤晏</a>
      <a href="/infra.html" class="nav-link">⚙️ 基礎設施</a>
      <a href="/erp.html" class="nav-link">🏢 ERP</a>
      <a href="/brands.html" class="nav-link">🎨 品牌</a>
      <a href="/horizen.html" class="nav-link">🌅 先見明</a>
    </div>
  </div>

  <!-- GROUP 2：各專案（依頁面調整） -->
  <div class="sb-group">
    <button class="sb-group-toggle" data-id="XX-projects" onclick="toggleSbGroup(this)">
      各專案 <span class="sb-arr">▾</span>
    </button>
    <div class="sb-group-body">
      <a href="https://app.rsun.me" target="_blank" class="nav-link">⚡ rsun.me</a>
      <a href="https://ronsunai.tw" target="_blank" class="nav-link">🌐 ronsunai.tw</a>
      <a href="https://ceyan.ronsunai.tw" target="_blank" class="nav-link">🌿 ceyan</a>
      <a href="https://askai.vercel.app" target="_blank" class="nav-link">💬 askai</a>
      <a href="https://aiclass.vercel.app" target="_blank" class="nav-link">🎓 aiclass</a>
      <a href="https://wismath.work" target="_blank" class="nav-link">🔮 wismath</a>
    </div>
  </div>

  <!-- GROUP 3：頁面專屬區段（依需求新增） -->
  <!-- <div class="sb-group"> ... </div> -->

  <!-- 整體收合按鈕（固定在最底） -->
  <button class="sb-collapse-btn" onclick="toggleSidebar()">◀ 收合選單</button>
</div>
```

### 手機按鈕（加進 `.topbar-left`）

```html
<button class="mobile-menu-btn" onclick="openSidebar()" title="開啟選單">☰</button>
```

### 展開藥丸 + 遮罩（加在 `.topbar` 結尾的 `</div>` 之後，`.layout` 之前）

```html
<button class="sb-expand-pill" onclick="toggleSidebar()" title="展開選單">▶</button>
<div class="sb-backdrop" id="sb-backdrop" onclick="closeSidebar()"></div>
```

---

## JS（加在 `</script>` 之前，或新增 `<script>` 區塊）

```javascript
// --- Sidebar collapse & groups ---
function toggleSbGroup(btn){
  var g=btn.closest('.sb-group');
  g.classList.toggle('closed');
  var id=btn.dataset.id;
  if(id) localStorage.setItem('sbg-'+id, g.classList.contains('closed')?'1':'');
}
function toggleSidebar(){
  var c=document.body.classList.toggle('sidebar-collapsed');
  localStorage.setItem('sb-col', c?'1':'');
}
function openSidebar(){
  document.getElementById('sidebar').classList.add('mobile-open');
  document.getElementById('sb-backdrop').classList.add('open');
}
function closeSidebar(){
  document.getElementById('sidebar').classList.remove('mobile-open');
  document.getElementById('sb-backdrop').classList.remove('open');
}
// 初始化：還原 localStorage 狀態
(function(){
  if(localStorage.getItem('sb-col')) document.body.classList.add('sidebar-collapsed');
  document.querySelectorAll('.sb-group').forEach(function(g){
    var t=g.querySelector('.sb-group-toggle');
    var id=t&&t.dataset.id;
    if(id&&localStorage.getItem('sbg-'+id)) g.classList.add('closed');
  });
})();
```

---

## `data-id` 命名慣例

每個 `.sb-group-toggle` 的 `data-id` 需要唯一，建議格式：`{頁面縮寫}-{group用途}`

| 頁面 | 縮寫 | 範例 |
|------|------|------|
| index.html | idx | idx-tracker, idx-projects |
| livelink.html | ll | ll-tracker, ll-projects, ll-ronsunai |
| ceyan.html | cy | cy-tracker, cy-projects, cy-brand |
| infra.html | infra | infra-tracker, infra-projects |
| erp.html | erp | erp-tracker, erp-projects, erp-roadmap |
| brands.html | br | br-tracker, br-projects, br-brands |
| horizen.html | hz | hz-tracker, hz-projects, hz-views |
| clients/index.html | cl | cl-tracker, cl-projects, cl-crm |

---

## 當前頁面 active 標示

**不要用 class**，JS 的 `showSection()` 會清掉 `.active`。改用 inline style：

```html
<a href="/livelink.html" class="nav-link"
   style="color:var(--blue);background:rgba(30,64,175,.07);border-left-color:var(--blue);font-weight:600">
  🔗 LiveLink
</a>
```

---

## 注意事項

- 側欄 `width:0` 時 `overflow:hidden` 會蓋掉 `overflow-y:auto`，transition 結束後才顯現，**勿改動收合時的 overflow 設定**
- 手機版用 `position:fixed`，即使父層有 `overflow:hidden` 也能正確顯示
- `max-height` 動畫設定 `600px`（應大於所有 group 實際高度），若 group 內容超過需調大
- horizen.html 深色 topbar 的手機按鈕需加特殊 style：`style="border-color:rgba(255,255,255,.3);color:#F5F2EA"`
