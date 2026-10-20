---
name: canvas-2d-chart-implementation
description: Build animated, interactive Canvas 2D data visualization charts — coordinate mapping, smooth trajectories, hover interactions, tooltips, particle effects, and Firefox cross-browser compatibility. Covers the full pattern from data update to pixel rendering, not a specific chart library.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [canvas, charts, data-viz, animation, 2d-graphics]
    triggers:
      - "build a chart"
      - "canvas 2d visualization"
      - "data visualization chart"
      - "animated chart"
      - "player trajectory chart"
      - "crash chart"
      - "canvas data plot"
    related_skills: [p5js, sketch, architecture-diagram]
---
# Canvas 2D Chart Implementation

## Architecture Pattern

Use a single class with a consistent update/draw cycle:

```
Chart
  ├── constructor(containerId, options) — setup DOM, canvas, events, rAF
  ├── buildDOM() — create canvas at devicePixelRatio size
  ├── bindEvents() — mousemove/mouseleave for hover
  ├── handleResize() — ResizeObserver callback
  ├── update(data) — receive new data, reset animation state
  ├── draw(time) — render one frame
  ├── animate() — requestAnimationFrame loop
  └── destroy() — cleanup
```

## Canvas Setup Pattern

```javascript
buildDOM() {
  const canvas = document.createElement('canvas');
  canvas.width = this.width * devicePixelRatio;
  canvas.height = this.height * devicePixelRatio;
  canvas.style.width = this.width + 'px';
  canvas.style.height = this.height + 'px';
  this.container.appendChild(canvas);
  this.ctx = canvas.getContext('2d');
  this.ctx.scale(devicePixelRatio, devicePixelRatio);
}
```

## Coordinate System

Use getters for margins and plot dimensions:

```javascript
get margin() {
  return { left: 65, right: 20, top: 20, bottom: 40 };
}
get plotW() { return this.width - this.margin.left - this.margin.right; }
get plotH() { return this.height - this.margin.top - this.margin.bottom; }

toPlotX(week) {
  return this.margin.left + (week / maxWeek) * this.plotW;
}
toPlotY(value) {
  const norm = logScale(value);  // normalize to [0, 1]
  return this.margin.top + this.plotH * (1 - norm);
}
```

Use log scale for exponential data (bankroll growth):

```javascript
function logScale(value, minLog = 2, maxLog = 7) {
  if (value <= 0) return 0;
  const lv = Math.log10(value);
  return Math.max(0, Math.min(1, (lv - minLog) / (maxLog - minLog)));
}
```

## Smooth Trajectory Drawing

Use quadratic bezier interpolation for smooth curves between data points:

```javascript
ctx.beginPath();
ctx.moveTo(points[0].x, points[0].y);
for (let i = 1; i < points.length - 1; i++) {
  const xc = (points[i].x + points[i + 1].x) / 2;
  const yc = (points[i].y + points[i + 1].y) / 2;
  ctx.quadraticCurveTo(points[i].x, points[i].y, xc, yc);
}
if (points.length > 1) {
  ctx.lineTo(points[points.length - 1].x, points[points.length - 1].y);
}
```

## Animation Pattern

- `animPhase` counter [0..1] drives draw progress (incremented each frame by ~0.012)
- `performance.now()` for time-based effects (pulsing, particle movement)
- `requestAnimationFrame` loop — 60fps when visible, pauses when tab is hidden

## Hover Detection

Use point-in-circle hit testing against the latest position of each data point:

```javascript
checkHover() {
  let found = null, foundDist = Infinity;
  this.players.forEach(p => {
    const px = this.toPlotX(p.lastWeek);
    const py = this.toPlotY(p.lastValue);
    const dist = Math.hypot(this.mouseX - px, this.mouseY - py);
    if (dist < 18 && dist < foundDist) { found = p; foundDist = dist; }
  });
  // show/hide tooltip, update cursor
}
```

## Drawing Order

Draw layers back-to-front to get correct occlusion:

1. Grid (week lines, bankroll levels, axis labels)
2. Target markers (background dots at projected targets)
3. Goal line ($10M finish line)
4. Player trajectories (smooth curves with glow)
5. Flow particles (animated dots moving along paths)
6. Player end-position dots (pulsing glow spheres)
7. Labels (name + bankroll above each dot)
8. Legend (top-right corner list of active players)

## Particle System

For animated flow particles along paths:

```javascript
// On data update, spawn particles distributed along each trajectory
particles.push({
  playerName: p.name,
  t: i / count,         // position along path [0..1]
  speed: 0.008 + Math.random() * 0.006,  // per-frame advance
  color: p.color,
  dead: false,
});

// Each frame, advance t and interpolate position
this.particles.forEach(p => {
  p.t += p.speed;
  if (p.t >= 1) p.t = 0;  // loop
  const idx = p.t * (path.length - 1);
  const i0 = Math.floor(idx);
  const i1 = Math.min(i0 + 1, path.length - 1);
  const frac = idx - i0;
  px = path[i0].x + (path[i1].x - path[i0].x) * frac;
  py = path[i0].y + (path[i1].y - path[i0].y) * frac;
});
```

## Color Palette

Use a 20-color palette for unique per-player coloring:

```javascript
const PALETTE = [
  '#00ff88','#7c3aed','#f59e0b','#ef4444','#3b82f6',
  '#ff6b9d','#06b6d4','#f97316','#84cc16','#ec4899',
  // ...
];
function pickColor(name, idx) {
  if (idx != null) return PALETTE[idx % PALETTE.length];
  let h = 0;
  for (let i = 0; i < name.length; i++) h = ((h << 5) - h) + name.charCodeAt(i);
  return PALETTE[Math.abs(h) % PALETTE.length];
}
```

## User-Controlled Zoom

Add zoom controls for charts where users need to inspect detail at different levels:

```javascript
// Properties
this.zoomLevel = 1.0;  // 0.25 (max zoom in) to 3.0 (max zoom out)

// In yMaxLog or similar ceiling getter:
ceiling = ceiling / this.zoomLevel;
// Lower zoomLevel → lower ceiling → players fill more vertical space
// Higher zoomLevel → higher ceiling → more context

// Methods
zoomIn() {
  this.zoomLevel = Math.min(3.0, this.zoomLevel + 0.25);
  this.updateZoomLabel();
}
zoomOut() {
  this.zoomLevel = Math.max(0.25, this.zoomLevel - 0.25);
  this.updateZoomLabel();
}
zoomReset() {
  this.zoomLevel = 1.0;
  this.updateZoomLabel();
}
updateZoomLabel() {
  const label = this.container.querySelector('.chart-zoom-label');
  if (label) label.textContent = Math.round(this.zoomLevel * 100) + '%';
}
```

**Zoom controls DOM:** Render absolute-positioned buttons (—, +, ↺) with a % label in `buildDOM()`. Use event delegation on a `[data-zoom]` attribute for click handling. Position `top:10px; right:10px` with `z-index:10` so they overlay the chart canvas. Style with `backdrop-filter: blur(8px)` for glassmorphism over the dark chart background.

## Dynamic Y-Axis Scaling

For log-scale charts where data clusters near the bottom, dynamically compute a tight ceiling (~1.5x above max data) instead of the full range. When the $10M goal line is above the viewport, show a floating arrow badge instead. See the `dynamic-chart-y-axis-scaling` skill for full implementation.

- **Don't forget to reapply ctx.scale after resize.** Setting `canvas.width` or `canvas.height` resets the transform to the identity matrix. Always call `ctx.scale(dpr, dpr)` after any dimension change.
- **Don't use 8-digit hex (#RRGGBBAA) in canvas** — unsupported in Firefox <106. Use `rgba(r,g,b,a)` instead.
- **Don't use ctx.roundRect()** without a polyfill — unsupported in Firefox <112.
- **Don't declare unused `dpr` variables** in draw() — leftover from debugging, causes lint warnings.
- **Don't forget to handle empty data gracefully** — players array is initially empty, animPhase starts at 0. The first few frames draw just the grid until data arrives.
- **Don't forget the backend must supply ≥2 history points per player** — `drawPlayerTrajectories` has `if (path.length < 2) return;` which silently skips players with only 1 data point (e.g. just `week: 0, bankroll: 100`). This is invisible from the frontend: the player count label says "11 players" but only players with 2+ points draw lines. The backend's `generate_player_history` must always produce at least `week_reached + 1` points, even for flat-track players where `current_units == starting_units`. Otherwise the chart appears empty.
- **Don't rely on ResizeObserver firing after rAF** — browser order differs between Chrome (rAF first) and Firefox (ResizeObserver first). Apply scale in handleResize.
- **Font loading matters** — use Google Fonts loader or `document.fonts.ready` before measuring text with `ctx.measureText()`.
- **Audit ALL data update paths, not just the initial render.** When a chart has multiple code paths that call `update()` — initial load, tab/view switches, auto-refresh timers, post-action callbacks (profile save, bet log, sync) — each one is independently capable of rendering the wrong data. The auto-refresh timer is the most insidious: it silently overrides the correct initial render after its interval fires. If any single path applies a filter (e.g., "My Stats" filtering to current user), it will persist until the next update from a different path overwrites it.
  
  **Fix pattern:** Add auth-state guards at EVERY update site, not just the initial one. A common bug is the chart correctly rendering all players on init, then 30 seconds later the auto-refresh applies a filter that hides everything but one player — and the user sees an empty or single-player chart until they refresh the page:
  ```javascript
  // ❌ Wrong: only guards the initial render, auto-refresh ignores auth
  initChart() { chart.update(allData); }  // correct
  setInterval(() => { chart.update(filteredData); }, 30000);  // overrides to wrong state
  
  // ✅ Correct: guard every update path with the same auth check
  function updateChart(data) {
    const shouldFilter = AUTH.isLoggedIn && CHART_VIEW === 'mine';
    chart.update(shouldFilter ? filterToUser(data) : data);
  }
  // Then call updateChart() from init, auto-refresh, tab switch, AND post-action callbacks
  ```
  
  **When to look for this:** the chart renders correctly on page load but after a few seconds of idle time (or after clicking a tab then waiting), it shows different/wrong data. The auto-refresh timer is always the prime suspect.

## Related

- `references/firefox-canvas-compatibility.md` — full details on the three Firefox fixes
- `references/leaderboard-chart-cross-highlight.md` — syncing hover between DOM leaderboard and Canvas chart via CSS custom properties on ::before pseudo-elements
