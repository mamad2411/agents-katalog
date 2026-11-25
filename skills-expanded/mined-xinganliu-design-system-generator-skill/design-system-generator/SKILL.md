---
name: design-system-generator
description: >
  Generate a complete, production-ready design system from a single brand color.
  Outputs OKLCH color palettes, W3C Design Tokens (JSON), CSS custom properties,
  component styles (Button, Card, Input, Badge, Alert, Modal, etc.), and a live
  preview HTML page with Light/Dark theme toggle. Trigger this skill when the user
  asks to create a design system, generate a color palette, build a theme, create
  UI tokens, or set up brand styles.
  从一个品牌色自动生成完整的设计系统：OKLCH 调色板、W3C Design Tokens、CSS 变量、
  组件样式和可视化预览页。
argument-hint: "<brand-color> [font-family] [style]"
---

# Design System Generator / 设计系统生成器

Generate a complete, production-ready design system from minimal brand inputs.
从最少的品牌输入自动生成完整的、可投产的设计系统。

## Core Principles / 核心原则

1. **One Color In → Full System Out**: The user only needs to provide a single brand color. Everything else is derived algorithmically.
2. **OKLCH-First**: All colors are generated in the OKLCH color space for perceptual uniformity and superior accessibility.
3. **W3C Standards**: Output follows the W3C Design Tokens specification (`$value` / `$type` format).
4. **Zero Dependencies**: Generated CSS uses only native custom properties — no preprocessors, no frameworks required.
5. **Accessibility by Default**: All color combinations meet WCAG 2.2 AA contrast ratios (4.5:1 for text, 3:1 for UI elements).
6. **Progressive Enhancement**: Dark mode uses `color-scheme` + `light-dark()` for native OS integration.

---

## Workflow / 工作流

You MUST follow these phases in order. Do NOT skip phases or generate all files at once without user confirmation at each stage.

你必须按顺序执行以下阶段。不要跳过阶段，也不要在未获得用户确认的情况下一次性生成所有文件。

---

### Phase 1: Brand Input Collection / 品牌输入收集

**Trigger / 触发**: User asks to create a design system, generate a theme, or build brand styles.

**Your Task / 你的任务**: Collect brand parameters through conversation. At minimum, you need ONE of these:

| Parameter | Required | Default | Example |
|-----------|----------|---------|---------|
| Brand color | ✅ Yes | — | `#6366f1`, `oklch(55% 0.25 270)`, `indigo` |
| Font family | Optional | `Inter, system-ui, sans-serif` | `"Outfit"`, `"Noto Sans SC"` |
| Border radius style | Optional | `rounded` (8px) | `sharp` (2px), `rounded` (8px), `pill` (9999px) |
| Density | Optional | `comfortable` | `compact`, `comfortable`, `spacious` |

**Steps**:
1. If user gives a color name (e.g., "blue", "coral"), convert it to a hex value first.
2. Convert any hex/rgb color to OKLCH using the algorithm in [color-system.md](references/color-system.md).
3. Present a summary of all parameters to the user and ask for confirmation.
4. If the user says "just use defaults" or gives only a color, proceed with defaults for all optional fields.

**Output**: Display the collected parameters in a table and wait for user confirmation.

---

### Phase 2: Color System Generation / 调色板生成

**Trigger / 触发**: User confirms Phase 1 parameters.

**Your Task / 你的任务**: Generate the complete color system. Read [color-system.md](references/color-system.md) for the OKLCH algorithm.

**Generate these palettes**:

#### 2.1 Primary Palette (10 steps)
From the brand color, generate a 10-step scale (50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950) by varying Lightness in OKLCH while keeping Chroma and Hue stable. The brand color should map to step 500 or 600.

#### 2.2 Neutral Palette (10 steps)
Take the brand color's Hue, reduce Chroma to near zero (0.01–0.03), and generate a neutral gray scale with a subtle brand tint.

#### 2.3 Semantic Colors
Generate these using complementary/analogous hue relationships from the brand color:
- **Success**: Hue ≈ 145° (green family)
- **Warning**: Hue ≈ 85° (amber/yellow family)
- **Error/Danger**: Hue ≈ 25° (red family)
- **Info**: Hue ≈ 230° (blue family)

Each semantic color gets a 5-step mini-scale: light, default, dark, contrast-text, subtle-bg.

#### 2.4 Theme Mapping
Create semantic token mappings for both Light and Dark themes:

```
Light Theme:
  --color-bg-primary:     neutral-50
  --color-bg-secondary:   neutral-100
  --color-text-primary:   neutral-900
  --color-text-secondary: neutral-600
  --color-border:         neutral-200

Dark Theme:
  --color-bg-primary:     neutral-950
  --color-bg-secondary:   neutral-900
  --color-text-primary:   neutral-50
  --color-text-secondary: neutral-400
  --color-border:         neutral-800
```

**Output**: Display the generated palettes as color swatches (use colored text or blocks if in terminal, or describe the colors). Wait for user confirmation before proceeding.

---

### Phase 3: Token Architecture / Token 架构

**Trigger / 触发**: User confirms Phase 2 color system.

**Your Task / 你的任务**: Generate the complete token files. Read the following references as needed:
- [typography-scale.md](references/typography-scale.md) for font sizes
- [spacing-system.md](references/spacing-system.md) for spacing values

**Generate these files**:

#### 3.1 `tokens.json` — W3C Design Tokens
Follow the template in [tokens.json.tmpl](templates/tokens.json.tmpl). Include:
- All color tokens (primitive + semantic)
- Typography tokens (font-family, font-size scale, font-weight, line-height, letter-spacing)
- Spacing tokens (4px base geometric progression)
- Border radius tokens
- Shadow tokens (3 levels: sm, md, lg)
- Z-index tokens
- Transition/animation duration tokens

#### 3.2 `tokens.css` — CSS Custom Properties
Follow the template in [tokens.css.tmpl](templates/tokens.css.tmpl). Structure:
```css
/* === Primitive Tokens === */
:root {
  --color-primary-50: oklch(...);
  /* ... all primitive values ... */
}

/* === Semantic Tokens (Light Theme — Default) === */
:root {
  color-scheme: light dark;
  --color-bg-primary: light-dark(var(--color-neutral-50), var(--color-neutral-950));
  /* ... semantic mappings using light-dark() ... */
}

/* === Dark Theme Override === */
[data-theme="dark"] {
  color-scheme: dark;
  --color-bg-primary: var(--color-neutral-950);
  /* ... explicit dark overrides for manual toggle ... */
}
```

**Output**: Write both files to `design-system/` directory. Show the user the file structure and a summary of generated tokens.

---

### Phase 4: Component Styles / 组件样式

**Trigger / 触发**: Phase 3 token files are generated.

**Your Task / 你的任务**: Generate production-ready component CSS. Read [component-patterns.md](references/component-patterns.md) and [dark-mode-guide.md](references/dark-mode-guide.md).

**Generate `components.css`** with these components:

| Component | Variants | States |
|-----------|----------|--------|
| `.btn` | `--primary`, `--secondary`, `--ghost`, `--danger` | hover, focus-visible, active, disabled |
| `.card` | `--elevated`, `--outlined`, `--filled` | hover (if interactive) |
| `.input` | `--default`, `--error` | focus, disabled, placeholder |
| `.badge` | `--primary`, `--success`, `--warning`, `--danger`, `--neutral` | — |
| `.alert` | `--info`, `--success`, `--warning`, `--danger` | dismissible |
| `.avatar` | size variants (sm, md, lg) | — |
| `.divider` | horizontal, vertical | — |
| `.skeleton` | — | loading animation |
| `.tooltip` | — | — |
| `.modal` | — | open/close animation |
| `.navbar` | — | sticky, transparent |

**Rules for component CSS**:
1. ONLY use `var(--token-name)` — never hardcode any color, size, or spacing value.
2. Use BEM-like naming: `.btn`, `.btn--primary`, `.btn:hover`.
3. Include `transition` on all interactive state changes (use `--transition-fast` / `--transition-normal`).
4. Include `focus-visible` outlines for keyboard accessibility.
5. Include subtle micro-animations (scale on button press, fade on card hover).
6. All components must look correct in both Light and Dark themes automatically.

**Output**: Write `components.css` to `design-system/`. Show the user a summary of generated components.

---

### Phase 5: Preview & Delivery / 预览与交付

**Trigger / 触发**: Phase 4 components are generated.

**Your Task / 你的任务**: Generate a visual preview page and deliver all files.

#### 5.1 Generate `preview.html`
Follow the template in [preview.html.tmpl](templates/preview.html.tmpl). The preview page must include:
- **Header** with project name and theme toggle button (Light/Dark switch)
- **Color Palette Section**: All color swatches with token names and values
- **Typography Section**: All font sizes rendered as sample text
- **Spacing Section**: Visual representation of spacing scale
- **Components Section**: All components rendered in all variants and states
- **Footer** with "Generated by Design System Generator"

The preview page must:
- Be a single self-contained HTML file (inline the CSS or use relative paths)
- Include a working Light/Dark toggle using JavaScript
- Be responsive (work on mobile and desktop)
- Use a clean, modern layout

#### 5.2 File Delivery Summary
Present the final file tree to the user:
```
design-system/
├── tokens.json          # W3C Design Tokens (machine-readable)
├── tokens.css           # CSS Custom Properties (import this in your project)
├── components.css       # Ready-to-use component styles
└── preview.html         # Open in browser to see your design system
```

#### 5.3 Usage Instructions
Tell the user how to use the generated files:
```html
<!-- Add to your HTML <head> -->
<link rel="stylesheet" href="design-system/tokens.css">
<link rel="stylesheet" href="design-system/components.css">
```

---

## Handling Edge Cases / 边界情况处理

### If user provides multiple colors
Use the first color as primary. Ask if other colors should be used for specific semantic roles (e.g., "Should I use the second color for success states?").

### If user wants to customize after generation
Offer to regenerate specific parts (e.g., "I can update just the color palette while keeping the components unchanged").

### If user asks for framework-specific output
Explain that this version generates vanilla CSS. Offer guidance on how to integrate:
- **Tailwind CSS**: Point them to use `tokens.json` values in `tailwind.config.js`
- **React/Vue**: Components can wrap the CSS classes
- **Sass/Less**: The CSS custom properties work directly

---

## Example Triggers / 示例触发

These user messages should activate this skill:
- "Generate a design system with brand color #6366f1"
- "Create a theme using indigo as the primary color"
- "Build a design token system for my project"
- "帮我生成一个以珊瑚色为主色的设计系统"
- "Create dark mode tokens for my app"
- "I need a color palette and component styles"
- "/design-system #e11d48 Outfit rounded"
