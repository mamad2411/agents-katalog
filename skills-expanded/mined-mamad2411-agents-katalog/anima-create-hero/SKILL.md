# /anima-create-hero — Generate Repo Hero Pages

Create a single-file `hero.html` marketing banner for any RobotFlow Labs repository. Industrial Cyberpunk design. Output: `{repo}/assets/hero.html`. Works for MLX ports, ANIMA modules, research projects — anything in the org.

## IMPORTANT: This is a MARKETING tool

The hero is the first thing investors, developers, and visitors see. It must SELL the project.

**NEVER include in the hero:**
- PRD counts, test counts, or build status
- Internal engineering metrics
- "In Progress" / "Scoped" / "Placeholder" language
- Anything that makes the project look unfinished

**ALWAYS include in the hero:**
- Bold, confident claims about what the project does
- The paper/research it's based on (adds credibility)
- Impressive numbers that sell (CUDA kernels ported, speed gains, zero dependencies)
- Technology keywords that attract the right audience
- "OPERATIONAL" / "NATIVE" / "ZERO COMPROMISE" language

The hero should make someone think: "This is serious. These people ship."

---

## Workflow

### Step 1: Gather Project Info (ASK the user)

Collect the following. If the user provides a repo name, research it first (GitHub stars, description, original authors, kernel count, paper reference).

| Field | Example | Notes |
|-------|---------|-------|
| `PROJECT_NAME` | diff-gaussian-rasterization-mlx | Repo name |
| `MODULE_CODE` | MLX-017 | Module ID in the org |
| `PILLAR` | PILLAR 01 — MLX INFRASTRUCTURE | Which pillar |
| `ORIGINAL_REPO` | graphdeco-inria/diff-gaussian-rasterization | Upstream |
| `ONE_LINER` | The SIGGRAPH 2023 rasterizer, native on Apple Silicon | Sells, not describes |
| `PAPER_REF` | Kerbl et al., SIGGRAPH 2023 | Credibility |
| `SELL_STATS` | 5 CUDA Kernels Ported / 0 NVIDIA Dependencies / Native Metal | 3 impressive numbers |
| `TAGS` | MLX, 3DGS, APPLE SILICON, etc. | 6 max, marketing keywords |
| `STATUS_BAR` | FORWARD PASS: OPERATIONAL, etc. | System status feel |

### Step 2: Generate hero.html

Write `{repo_path}/assets/hero.html` using the CANONICAL TEMPLATE below. Replace ALL placeholders. Make it look incredible.

### Step 3: Tell the user to screenshot

**CRITICAL — the .png workflow:**

> The `hero.html` is ready at `assets/hero.html`.
>
> **To create the hero.png:**
> 1. Open `assets/hero.html` in Chrome/Safari
> 2. The page is exactly 1280x640px — take a full screenshot of the `.hero-wrap` element
> 3. Save as `assets/hero.png`
> 4. The README already references `assets/hero.png` — it will show up automatically
>
> **Tip:** In Chrome DevTools, right-click the `.hero-wrap` div → "Capture node screenshot"
>
> Let me know when you've saved the .png and I'll verify the README links it correctly.

**The agent NEVER generates the .png.** The agent generates the .html, the user screenshots it to create the .png. This is the workflow.

---

## Design System (STRICT — from robotflow-labs.github.io)

### CSS Variables (NEVER deviate)
```css
--rf-accent: #FF3B00;           /* Industrial Orange */
--rf-accent-glow: rgba(255, 59, 0, 0.3);
--rf-accent-dim: rgba(255, 59, 0, 0.15);
--rf-bg: #050505;               /* Void Black */
--rf-bg-panel: #1A1A1A;         /* Dark Gray */
--rf-border: #333333;
--rf-text: #ffffff;
--rf-text-dim: #999999;
--rf-text-muted: #666666;
--rf-success: #00FF88;           /* Green status */
--rf-warning: #FFB800;           /* Orange/yellow warning */
--rf-restricted: #9B5EFF;        /* Purple for ANIMA restricted */
--rf-font-display: 'Oswald', sans-serif;
--rf-font-mono: 'JetBrains Mono', monospace;
--rf-font-tech: 'Chakra Petch', sans-serif;
```

### Style Rules (NEVER BREAK)
1. NO rounded corners — everything is sharp/square
2. NO gradients on elements (only subtle grid background)
3. NO soft shadows
4. NO colors outside the palette
5. NO fonts outside Oswald / JetBrains Mono / Chakra Petch
6. Scanline overlay on body (`repeating-linear-gradient`)
7. Grid background pattern (40px grid, `rgba(255, 59, 0, 0.04)`)
8. Corner brackets on hero-wrap (accent-colored L-shaped borders)
9. All display text uppercase
10. Letter-spacing on mono text: `1-4px`
11. Glow line animation at top (`scan` keyframe)
12. Status bar at bottom with colored dots (green = operational, orange = pending)

---

## CANONICAL TEMPLATE (the SHIPPED example from diff-gaussian-rasterization-mlx)

This is the EXACT code that ships. Copy this structure, replace the content placeholders.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{PROJECT_NAME_UPPER}} // HERO</title>
  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;700;900&family=JetBrains+Mono:wght@400;500;700&family=Chakra+Petch:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --rf-accent: #FF3B00;
      --rf-accent-glow: rgba(255, 59, 0, 0.3);
      --rf-accent-dim: rgba(255, 59, 0, 0.15);
      --rf-bg: #050505;
      --rf-bg-panel: #1A1A1A;
      --rf-border: #333333;
      --rf-text: #ffffff;
      --rf-text-dim: #999999;
      --rf-success: #00FF88;
      --rf-restricted: #9B5EFF;
      --rf-font-display: 'Oswald', sans-serif;
      --rf-font-mono: 'JetBrains Mono', monospace;
      --rf-font-tech: 'Chakra Petch', sans-serif;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: var(--rf-font-mono);
      background: var(--rf-bg);
      color: var(--rf-text);
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      overflow: hidden;
    }

    /* SCANLINE */
    body::after {
      content: '';
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 9999;
      background: repeating-linear-gradient(
        to bottom, transparent, transparent 2px,
        rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px
      );
    }

    /* GRID BG */
    .hero-wrap {
      position: relative;
      width: 1280px;
      height: 640px;
      background:
        linear-gradient(rgba(255,59,0,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,59,0,0.04) 1px, transparent 1px);
      background-size: 40px 40px;
      border: 1px solid var(--rf-border);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      overflow: hidden;
    }

    /* CORNER BRACKETS */
    .hero-wrap::before,
    .hero-wrap::after {
      content: '';
      position: absolute;
      width: 40px;
      height: 40px;
      border-color: var(--rf-accent);
      border-style: solid;
    }
    .hero-wrap::before {
      top: 12px; left: 12px;
      border-width: 2px 0 0 2px;
    }
    .hero-wrap::after {
      bottom: 12px; right: 12px;
      border-width: 0 2px 2px 0;
    }

    .corner-tr, .corner-bl {
      position: absolute;
      width: 40px;
      height: 40px;
      border-color: var(--rf-accent);
      border-style: solid;
    }
    .corner-tr { top: 12px; right: 12px; border-width: 2px 2px 0 0; }
    .corner-bl { bottom: 12px; left: 12px; border-width: 0 0 2px 2px; }

    /* GLOW LINE */
    .glow-line {
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 2px;
      background: linear-gradient(90deg, transparent, var(--rf-accent), transparent);
      animation: scan 3s ease-in-out infinite;
    }
    @keyframes scan {
      0%, 100% { opacity: 0.3; }
      50% { opacity: 1; }
    }

    /* TAG */
    .hero-tag {
      font-family: var(--rf-font-mono);
      font-size: 11px;
      letter-spacing: 3px;
      color: var(--rf-accent);
      text-transform: uppercase;
      margin-bottom: 12px;
      padding: 4px 16px;
      border: 1px solid var(--rf-accent);
      background: rgba(255,59,0,0.08);
    }

    /* MODULE CODE */
    .module-code {
      font-family: var(--rf-font-mono);
      font-size: 13px;
      color: var(--rf-text-dim);
      letter-spacing: 4px;
      margin-bottom: 8px;
    }

    /* TITLE */
    .hero-title {
      font-family: var(--rf-font-display);
      font-size: 64px;
      font-weight: 900;
      letter-spacing: -1px;
      line-height: 1.0;
      text-transform: uppercase;
      margin-bottom: 4px;
    }
    .hero-title .accent { color: var(--rf-accent); }

    /* SUBTITLE */
    .hero-subtitle {
      font-family: var(--rf-font-tech);
      font-size: 18px;
      font-weight: 500;
      color: var(--rf-text-dim);
      letter-spacing: 2px;
      margin-bottom: 24px;
    }

    /* DESC */
    .hero-desc {
      font-size: 14px;
      color: var(--rf-text-dim);
      max-width: 700px;
      text-align: center;
      line-height: 1.7;
      margin-bottom: 28px;
    }

    /* STATS ROW */
    .stats-row {
      display: flex;
      gap: 32px;
      margin-bottom: 28px;
    }
    .stat {
      text-align: center;
      padding: 12px 24px;
      border: 1px solid var(--rf-border);
      background: var(--rf-bg-panel);
    }
    .stat-value {
      font-family: var(--rf-font-display);
      font-size: 32px;
      font-weight: 700;
      color: var(--rf-accent);
    }
    .stat-label {
      font-size: 10px;
      letter-spacing: 2px;
      color: var(--rf-text-dim);
      text-transform: uppercase;
      margin-top: 4px;
    }

    /* TAGS */
    .tag-row {
      display: flex;
      gap: 8px;
      margin-bottom: 20px;
    }
    .tag {
      font-size: 10px;
      letter-spacing: 1px;
      padding: 4px 12px;
      border: 1px solid var(--rf-border);
      color: var(--rf-text-dim);
      text-transform: uppercase;
    }
    .tag.active { border-color: var(--rf-success); color: var(--rf-success); }

    /* BOTTOM STATUS BAR */
    .status-bar {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 36px;
      background: var(--rf-bg-panel);
      border-top: 1px solid var(--rf-border);
      display: flex;
      align-items: center;
      padding: 0 20px;
      gap: 24px;
      font-size: 11px;
      color: var(--rf-text-dim);
      letter-spacing: 1px;
    }
    .status-bar .dot {
      display: inline-block;
      width: 6px;
      height: 6px;
      border-radius: 50%;
      margin-right: 6px;
    }
    .dot.green { background: var(--rf-success); box-shadow: 0 0 8px var(--rf-success); }
    .dot.orange { background: #FFB800; box-shadow: 0 0 8px #FFB800; }

    /* CREDITS */
    .credits {
      position: absolute;
      top: 16px;
      right: 60px;
      font-size: 10px;
      color: var(--rf-text-dim);
      letter-spacing: 1px;
      text-align: right;
      line-height: 1.8;
    }
    .credits a { color: var(--rf-accent); text-decoration: none; }

    /* PILLAR TAG */
    .pillar-tag {
      position: absolute;
      top: 16px;
      left: 60px;
      font-size: 10px;
      color: var(--rf-accent);
      letter-spacing: 3px;
      text-transform: uppercase;
    }
  </style>
</head>
<body>
  <div class="hero-wrap">
    <div class="glow-line"></div>
    <div class="corner-tr"></div>
    <div class="corner-bl"></div>

    <div class="pillar-tag">{{PILLAR}}</div>

    <div class="credits">
      UPSTREAM: <a href="https://github.com/{{ORIGINAL_REPO}}">{{ORIGINAL_ORG_UPPER}}</a><br>
      PORT: <a href="https://robotflow-labs.github.io">ROBOTFLOW LABS</a>
    </div>

    <div class="hero-tag">MODULE {{MODULE_CODE}}</div>
    <div class="module-code">{{PROJECT_NAME_UPPER}}</div>
    <div class="hero-title">
      <span class="accent">{{TITLE_ACCENT}}</span> {{TITLE_REST}}
    </div>
    <div class="hero-subtitle">{{SUBTITLE}} &mdash; NATIVE TO APPLE SILICON</div>

    <p class="hero-desc">
      {{DESCRIPTION_LINE_1}}<br>
      {{DESCRIPTION_LINE_2}}
    </p>

    <div class="stats-row">
      <div class="stat">
        <div class="stat-value">{{STAT_1_VALUE}}</div>
        <div class="stat-label">{{STAT_1_LABEL}}</div>
      </div>
      <div class="stat">
        <div class="stat-value">{{STAT_2_VALUE}}</div>
        <div class="stat-label">{{STAT_2_LABEL}}</div>
      </div>
      <div class="stat">
        <div class="stat-value">{{STAT_3_VALUE}}</div>
        <div class="stat-label">{{STAT_3_LABEL}}</div>
      </div>
    </div>

    <div class="tag-row">
      <!-- .active tags get green border, plain tags get gray -->
      <span class="tag active">{{TAG_1}}</span>
      <span class="tag active">{{TAG_2}}</span>
      <span class="tag">{{TAG_3}}</span>
      <span class="tag">{{TAG_4}}</span>
      <span class="tag">{{TAG_5}}</span>
      <span class="tag active">{{TAG_6}}</span>
    </div>

    <div class="status-bar">
      <!-- green dot = operational, orange dot = pending/wip -->
      <span><span class="dot green"></span>{{STATUS_1}}</span>
      <span><span class="dot green"></span>{{STATUS_2}}</span>
      <span><span class="dot green"></span>{{STATUS_3}}</span>
      <span><span class="dot orange"></span>{{STATUS_4}}</span>
      <span style="margin-left:auto; color:#666;">{{PAPER_REF_SHORT}}</span>
    </div>
  </div>
</body>
</html>
```

---

## SHIPPED EXAMPLE: diff-gaussian-rasterization-mlx

This is the REAL output that lives at `RobotFlow-Labs/diff-gaussian-rasterization-mlx/assets/hero.html`:

- **PILLAR**: `PILLAR 01 — MLX INFRASTRUCTURE`
- **MODULE_CODE**: `MLX-017`
- **PROJECT_NAME_UPPER**: `DIFF-GAUSSIAN-RASTERIZATION`
- **TITLE**: `<span class="accent">3D GAUSSIAN</span> SPLATTING`
- **SUBTITLE**: `DIFFERENTIABLE RASTERIZER`
- **DESC**: "The official SIGGRAPH 2023 rasterizer ported entirely to MLX. / 5 CUDA kernels replaced with pure MLX ops. No NVIDIA. No PyTorch. Just your Mac."
- **STATS**: 5 CUDA Kernels Ported | 0 NVIDIA Dependencies | Native Metal — **NOTE: stats that SELL, never test counts or PRD counts**
- **TAGS**: MLX (active), 3DGS (active), SIGGRAPH 2023, EWA SPLATTING, SH DEGREE 3, APPLE SILICON (active)
- **STATUS BAR**: FORWARD PASS: OPERATIONAL (green) | BACKWARD PASS: OPERATIONAL (green) | VJP: WIRED (green) | METAL KERNELS: PENDING (orange)
- **CREDITS**: UPSTREAM: INRIA GRAPHDECO | PORT: ROBOTFLOW LABS

### What makes good SELL_STATS (3 numbers that impress):

**DO use:**
- `5` CUDA Kernels Ported (shows engineering depth)
- `0` NVIDIA Dependencies (shows independence)
- `330x` Faster (shows performance gain)
- `Native` Metal (shows platform commitment)
- `10` Policies Supported (shows breadth)
- `22K` Stars Upstream (shows importance of original)

**DO NOT use:**
- `14` Tests Passing (internal metric, nobody cares)
- `7/8` PRDs Complete (internal metric)
- `75%` MVP Readiness (makes it look unfinished)
- `Beta` / `Scaffold` (internal status language)

---

## REFERENCE: Mission Control Page Design (robotflow-labs.github.io)

The hero pages must feel like they belong to the same design system as the main Mission Control page. Key patterns from the main page to maintain consistency:

### Header brand pattern
```html
<a class="header-brand">ROBOTFLOW <span>LABS</span></a>  <!-- span = accent color -->
```

### Hero section pattern
```html
<div class="hero-tag">MISSION CONTROL</div>              <!-- bordered tag, accent color -->
<h1>ROBOTFLOW LABS<span>REINDUSTRIALIZING INTELLIGENCE</span></h1>
<div class="hero-status"><span class="status-dot"></span>SYSTEM: ONLINE</div>
```

### Module card pattern (for reference — NOT used in hero pages)
```html
<a class="module-card">
  <div class="module-code">MLX-001</div>                  <!-- e.g. MLX-001, ANM-001 -->
  <div class="module-name">LEROBOT-MLX</div>              <!-- Oswald 22px bold upper -->
  <div class="module-status deployed">                     <!-- deployed/active/restricted -->
    <span class="module-status-dot"></span>PUBLIC
  </div>
  <div class="module-desc">Description text...</div>
  <div class="module-test-count">&#9632; 739+ TESTS</div>
  <div class="module-tags"><span class="module-tag">MLX</span></div>
</a>
```

### Telemetry rail pattern
```html
<div class="telemetry-rail">
  <div class="telemetry-item">
    <div class="telemetry-value">39</div>                  <!-- Oswald 36px bold accent -->
    <div class="telemetry-label">TOTAL MODULES</div>       <!-- Mono 10px dim -->
  </div>
</div>
```

### Ticker pattern
```html
<div class="ticker-wrap">
  <div class="ticker">
    <span class="ticker-item"><span class="accent">&#9632;</span> TEXT: <span class="accent">VALUE</span></span>
  </div>
</div>
```

### Status colors
- `deployed` / `online` → green (`#00FF88`) with green dot glow
- `active` → accent (`#FF3B00`) with accent dot
- `restricted` → purple (`#9B5EFF`) with lock icon
- pending/wip → warning orange (`#FFB800`)

---

## Customization Guide

### For ANIMA modules (not MLX ports)
- Change pillar to `PILLAR 02 — ANIMA SUITE // RESTRICTED`
- Use `--rf-restricted` (#9B5EFF) instead of `--rf-accent` for borders
- Add lock icon: `&#128274;`
- Credits: `SYSTEM: ANIMA` instead of `UPSTREAM:`

### For research projects (Pillar 3)
- Change pillar to `PILLAR 03 — FRONTIER RESEARCH`
- Keep accent color
- Stats might be: Papers Referenced | Datasets | Experiments

### Stat value rules
- If 0, show `0` (not a dash) — "0 NVIDIA Dependencies" is a selling point
- For large numbers use `3K+` format
- Always 3 stats in the row

### Tag rules
- Max 6 tags
- `.active` class = green border (use for: MLX, APPLE SILICON, key differentiator)
- Plain tags = gray border (use for: paper refs, techniques, standards)

### Status bar rules
- Max 4-5 status items + paper ref right-aligned
- Green dot = working/operational
- Orange dot = pending/WIP/TODO
- Always end with paper reference or org credit

## File Output

Always write to: `{repo_root}/assets/hero.html`

Create the `assets/` directory if it doesn't exist.
