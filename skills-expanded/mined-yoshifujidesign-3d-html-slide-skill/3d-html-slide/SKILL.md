---
name: 3d-html-slide
description: >
  re-presentation.jpスタイルの3DワイヤーフレームHTMLスライドを生成するスキル。
  「3DワイヤーフレームHTMLスライド」というキーワードが含まれたときのみ、このスキルを使うこと。
---

# 3D HTML Slide Skill
**re-presentation.jp スタイル** — Three.js × 横スクロール × テーマカラー自動切替

## このスキルが生成するもの

単一HTMLファイル（外部ライブラリはCDN）で完結する、以下の特徴を持つプレゼンスライド：

- **Three.js 3D背景** — スライドごとに異なるワイヤーフレームジオメトリが浮かぶ
- **横スクロール** — scroll-snap による1枚ずつのページめくり
- **テーマカラー自動切替** — スライドが画面に入ると背景色・アクセントカラーが滑らかに変わる
- **視差効果（Parallax）** — data-parallax 属性で要素ごとに奥行き感を演出
- **GlassPanel / IsometricGrid** などの共通UIコンポーネント
- **完全レスポンシブ** — PC・スマホ両対応

---

## 必須ライブラリ（CDN）

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
```

---

## テーマカラー定義（4種）

スライドの `data-theme` 属性でテーマを指定する。スライド順に交互に使うと効果的。

| テーマ名 | 背景色 | アクセント | 用途イメージ |
|---|---|---|---|
| `theme-dark` | `#0F172A` (深紺) | `#00E8FE` (シアン) | タイトル・締め |
| `theme-amber` | `#FFAB00` (アンバー) | `#0F172A` (深紺) | 強調・章タイトル |
| `theme-light` | `#EFEFEF` (ライトグレー) | `#00E8FE` (シアン) | 説明・データ |
| `theme-cyan` | `#00E8FE` (シアン) | `#0F172A` (深紺) | アクセント・CTA |

---

## CSS変数システム

テーマ切替はこのCSS変数で一括制御する。必ずすべて定義すること。

```css
:root {
  --bg-color: #0F172A;
  --text-main: #FFFFFF;
  --text-sub: rgba(255, 255, 255, 0.7);
  --accent: #00E8FE;
  --glass-bg: rgba(255, 255, 255, 0.03);
  --glass-border: rgba(0, 232, 254, 0.3);
  --grid-color: rgba(0, 232, 254, 0.15);
  --shadow: rgba(0, 0, 0, 0.5);
}
body.theme-amber { /* 上書き定義 */ }
body.theme-light  { /* 上書き定義 */ }
body.theme-cyan   { /* 上書き定義 */ }
```

---

## 必須CSSクラス

以下を必ずstyleタグに含めること。

```css
/* テキスト・ボーダー */
.font-heading   { font-family: 'Share Tech Mono', monospace; }
.text-outline   { color: transparent; -webkit-text-stroke: 1.5px var(--accent); transition: all 0.8s ease; }
.text-dynamic   { color: var(--text-main); transition: color 0.8s ease; }
.text-sub-dynamic { color: var(--text-sub); transition: color 0.8s ease; }
.border-dynamic { border-color: var(--accent); transition: border-color 0.8s ease; }
.bg-dynamic     { background-color: var(--accent); transition: background-color 0.8s ease; }

/* スクロールコンテナ */
.scroll-container {
  display: flex; width: 100vw; height: 100dvh;
  overflow-x: auto; overflow-y: hidden;
  scroll-snap-type: x mandatory; scroll-behavior: smooth;
  -ms-overflow-style: none; scrollbar-width: none;
  perspective: 1500px;
}
.scroll-container::-webkit-scrollbar { display: none; }

/* スライド */
.slide {
  flex: 0 0 100vw; height: 100dvh;
  scroll-snap-align: center;
  position: relative; display: flex;
  align-items: center; justify-content: center;
  overflow: hidden; transform-style: preserve-3d;
}

/* GlassPanel */
.glass-panel {
  background: var(--glass-bg);
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--glass-border);
  box-shadow: 0 30px 60px var(--shadow), inset 0 0 0 1px rgba(255,255,255,0.1);
  transition: all 0.8s ease;
}

/* Isometric Grid背景 */
.iso-grid-bg {
  position: absolute; width: 300vw; height: 300vh;
  left: -100vw; top: -100vh;
  background-size: 80px 80px;
  background-image:
    linear-gradient(var(--grid-color) 1px, transparent 1px),
    linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
  transform: rotateX(60deg) rotateZ(45deg);
  mask-image: radial-gradient(circle at center, black 10%, transparent 65%);
  -webkit-mask-image: radial-gradient(circle at center, black 10%, transparent 65%);
  pointer-events: none; transition: background-image 0.8s ease;
}

/* Floating Label */
.floating-label { display: inline-flex; align-items: center; gap: 10px; }
.floating-label .line { width: 40px; height: 1px; background-color: var(--accent); transition: all 0.8s; }
.floating-label .box {
  border: 1px solid var(--accent); color: var(--accent);
  padding: 4px 12px; font-size: 0.7rem; letter-spacing: 0.1em;
  backdrop-filter: blur(4px); transition: all 0.8s ease;
}

/* UI Overlay corners (PC only) */
.viewport-corner { position: fixed; width: 40px; height: 40px; border-color: var(--accent); border-style: solid; z-index: 100; pointer-events: none; transition: border-color 0.8s; opacity: 0.5; }
.vp-tl { top: 30px; left: 30px; border-width: 2px 0 0 2px; }
.vp-tr { top: 30px; right: 30px; border-width: 2px 2px 0 0; }
.vp-bl { bottom: 30px; left: 30px; border-width: 0 0 2px 2px; }
.vp-br { bottom: 30px; right: 30px; border-width: 0 2px 2px 0; }
.ui-text { position: fixed; font-size: 10px; color: var(--accent); z-index: 100; pointer-events: none; letter-spacing: 0.1em; transition: color 0.8s; opacity: 0.8; }
.ui-tl { top: 40px; left: 80px; }
.ui-tr { top: 40px; right: 80px; text-align: right; }
.ui-bl { bottom: 40px; left: 80px; }
.ui-br { bottom: 40px; right: 80px; text-align: right; }

/* スマホスクロール非表示 */
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
.no-scrollbar::-webkit-scrollbar { display: none; }
```

---

## スライドHTMLテンプレート

### 基本構造（全スライド共通）

```html
<section class="slide" data-theme="theme-dark">
  <!-- Parallax背景グリッド -->
  <div class="absolute inset-0" data-parallax="0.8">
    <div class="iso-grid-bg"></div>
  </div>

  <!-- コンテンツ -->
  <div class="relative z-10 w-full max-w-6xl px-6 md:px-12
              max-h-full overflow-y-auto py-12 md:py-0 no-scrollbar
              flex flex-col justify-center min-h-[100dvh]"
       data-parallax="-0.3">
    <!-- ここにスライドの中身 -->
  </div>

  <!-- ナビゲーション矢印（全スライドに必須） -->
  <div class="absolute bottom-6 md:bottom-[40px] left-0 w-full flex justify-center z-50 pointer-events-none">
    <div data-parallax="-0.1" class="pointer-events-auto">
      <div onclick="scrollToNext()" class="animate-pulse hover:opacity-70 transition-opacity cursor-pointer scale-75 md:scale-100 flex items-center justify-center">
        <!-- ライトテーマ用矢印（画像がない場合はSVGで代替） -->
        <div class="light-arrow flex items-center gap-1">
          <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
            <path d="M18 8 L28 18 L18 28" stroke="currentColor" stroke-width="2" fill="none"/>
            <line x1="8" y1="18" x2="28" y2="18" stroke="currentColor" stroke-width="2"/>
          </svg>
        </div>
        <!-- ダークテーマ用矢印 -->
        <div class="dark-arrow flex items-center gap-1">
          <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
            <path d="M18 8 L28 18 L18 28" stroke="#00E8FE" stroke-width="2" fill="none"/>
            <line x1="8" y1="18" x2="28" y2="18" stroke="#00E8FE" stroke-width="2"/>
          </svg>
        </div>
      </div>
    </div>
  </div>
</section>
```

> **矢印について**: オリジナルは `arrow01.gif`（ダーク用）`arrow02.gif`（ライト用）を使用。
> 画像ファイルがない場合は上記SVGで代替する。

---

## スライドレイアウトパターン

### パターン1: タイトルスライド（大見出し + GlassPanel）
```html
<div class="floating-label mb-4 md:mb-8 font-heading">
  <div class="box">MODULE.01 : INTRODUCTION</div><div class="line"></div>
</div>
<h1 class="font-heading text-5xl sm:text-7xl md:text-[8rem] leading-[0.8] tracking-tighter mb-6 md:mb-8 text-outline">
  TITLE<br>HERE.
</h1>
<div class="glass-panel p-6 md:p-8 max-w-2xl border-l-4 border-dynamic">
  <h2 class="text-xl md:text-3xl font-bold mb-3 text-dynamic">サブタイトル</h2>
  <p class="text-sub-dynamic text-sm md:text-base font-light leading-relaxed">説明文をここに。</p>
</div>
```

### パターン2: 2カラム（左テキスト + 右GlassPanel）
```html
<div class="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-16 items-center ...">
  <div>
    <h2 class="font-heading text-4xl md:text-7xl text-outline mb-4">HEADING</h2>
    <p class="text-lg md:text-xl text-dynamic font-medium mb-4 leading-relaxed">メインテキスト</p>
    <p class="text-sub-dynamic text-sm md:text-base font-light leading-relaxed">サブテキスト</p>
  </div>
  <div class="glass-panel p-4 md:p-8 h-[250px] md:h-[400px] ..." data-parallax="-0.4">
    <!-- 右側コンテンツ（図・リスト等） -->
  </div>
</div>
```

### パターン3: センター大テキスト + GlassPanel
```html
<div class="w-full max-w-5xl mx-auto px-6 md:px-12 text-center ...">
  <h2 class="font-heading text-5xl md:text-8xl text-outline mb-6 md:mb-10">SECTION TITLE</h2>
  <div class="glass-panel p-6 md:p-12 mx-auto shadow-2xl">
    <p class="text-xl md:text-3xl text-dynamic font-bold mb-4">見出し</p>
    <p class="text-sub-dynamic text-sm md:text-lg font-medium leading-relaxed">説明文</p>
  </div>
</div>
```

### パターン4: 3カラムカード（比較・選択肢）
```html
<div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 text-left">
  <div class="glass-panel p-6 md:p-8 border-t-4 border-dynamic opacity-60">
    <h4 class="font-heading text-lg text-dynamic mb-2">OPTION 01</h4>
    <p class="text-lg font-bold text-dynamic mb-2">オプション名</p>
    <p class="text-sub-dynamic text-sm">説明文</p>
  </div>
  <!-- RECOMMENDEDカード（中央・強調） -->
  <div class="glass-panel p-6 md:p-8 border-t-4 border-dynamic transform scale-100 md:scale-110 shadow-2xl relative z-10">
    <div class="absolute -top-4 left-1/2 -translate-x-1/2 bg-dynamic text-white font-heading px-3 py-1 text-xs font-bold">RECOMMENDED</div>
    <h4 class="font-heading text-lg text-dynamic mb-2">OPTION 02</h4>
    <p class="text-xl font-bold text-dynamic mb-2">推奨オプション名</p>
    <p class="text-sub-dynamic text-sm">説明文</p>
  </div>
  <div class="glass-panel p-6 md:p-8 border-t-4 border-dynamic opacity-40">
    <!-- 3つ目 -->
  </div>
</div>
```

### パターン5: ステップ・プロセス（番号付き）
```html
<div class="space-y-4 md:space-y-6">
  <div class="glass-panel p-4 md:p-6 border-l-4 border-dynamic flex items-start gap-4">
    <span class="font-heading text-3xl text-dynamic opacity-40">01</span>
    <div>
      <span class="block font-heading text-dynamic text-xs mb-1">STEP 01</span>
      <p class="text-sub-dynamic text-sm font-light">説明文</p>
    </div>
  </div>
</div>
```

---

## data-parallax 速度ガイド

| 値 | 効果 | 推奨用途 |
|---|---|---|
| `0.8` | 背景がゆっくり流れる | iso-grid-bgの親要素 |
| `0.5〜0.6` | 中程度の奥行き | 背景装飾要素 |
| `-0.2〜-0.3` | コンテンツが少し逆方向に | メインコンテンツ |
| `-0.4` | 大きな逆視差 | GlassPanelなど右側要素 |
| `-0.1` | わずかな逆視差 | ナビゲーション矢印 |

---

## Three.js 設定

### ジオメトリとスライドの対応（10枚分）

スライドのインデックス順に以下を使う：

```javascript
const geometries = [
  new THREE.IcosahedronGeometry(4, 2),         // 0
  new THREE.TorusKnotGeometry(3, 0.8, 120, 20), // 1
  new THREE.OctahedronGeometry(4, 3),           // 2
  new THREE.DodecahedronGeometry(4, 2),         // 3
  new THREE.TorusGeometry(4, 1.5, 20, 100),     // 4
  new THREE.TetrahedronGeometry(4, 4),          // 5
  new THREE.SphereGeometry(4, 24, 24),          // 6
  new THREE.CylinderGeometry(3, 3, 8, 24, 4),  // 7
  new THREE.BoxGeometry(5, 5, 5, 4, 4, 4),     // 8
  new THREE.RingGeometry(1, 5, 32, 8)           // 9
];
```

> スライドが10枚未満でも問題なし（使われない分は画面外に配置される）。

### ワイヤーフレームマテリアル

```javascript
const wireMaterial = new THREE.LineBasicMaterial({
  color: 0x00E8FE, transparent: true, opacity: 0.3, linewidth: 0.5
});
```

### テーマカラーとThree.jsの同期

```javascript
const themeColors = {
  'theme-dark':  { bg: '#0F172A', wire: 0x00E8FE, fog: 0x0F172A },
  'theme-amber': { bg: '#FFAB00', wire: 0x0F172A, fog: 0xFFAB00 },
  'theme-light': { bg: '#EFEFEF', wire: 0x00E8FE, fog: 0xEFEFEF },
  'theme-cyan':  { bg: '#00E8FE', wire: 0x0F172A, fog: 0x00E8FE }
};
```

IntersectionObserver でスライドが60%表示されたとき `document.body.className = theme` を実行。

### カメラの動き（スクロール連動）

```javascript
camera.position.x = targetX + Math.sin(scrollProgress * Math.PI) * 12;
camera.position.y = Math.cos(scrollProgress * Math.PI) * 6;
camera.position.z = 12 + Math.sin(scrollProgress * Math.PI * 2) * 6;
camera.lookAt(targetX, 0, 0);
```

---

## スライド枚数の目安

| 枚数 | 構成例 |
|---|---|
| 5〜6枚 | ショートデモ・SNS投稿用 |
| 8〜10枚 | セミナー・ウェビナー登壇用 |
| 12〜15枚 | 本格プレゼン・ピッチデッキ |

---

## 生成手順

1. **スライド構成を確認** — 枚数、各スライドのテーマカラー、コンテンツ内容
2. **HTMLの骨格を作成** — `<!DOCTYPE html>` から `<body>` 開始まで（ライブラリ読込含む）
3. **CSSを丸ごと出力** — 上記「必須CSSクラス」を漏らさず記述
4. **スライドをセクションごとに出力** — 各 `<section class="slide">` を上記パターンで生成
5. **JavaScriptを出力** — Three.jsシーン構築 → テーマ切替 → パララックスループ → ナビゲーション

> **重要**: JavaScriptは `DOMContentLoaded` イベント内にすべてまとめること。

---

## よくあるミスと対策

| ミス | 対策 |
|---|---|
| テーマ切替でThree.jsの色が変わらない | `wireMaterial.color.lerp()` と `targetWireColor` の更新を確認 |
| スマホでスクロールが止まる | `scroll-snap-type: x mandatory` と `overflow-x: auto` の組み合わせを確認 |
| パララックスが効かない | `data-parallax` 属性とJS側の `querySelectorAll('[data-parallax]')` を確認 |
| ナビゲーション矢印が表示されない | `light-arrow` / `dark-arrow` の CSS切替ロジックを確認 |
| フォントが読み込まれない | Google Fonts の `<link rel="preconnect">` が2行あることを確認 |
