---
name: stitch-design
description: Automate high-fidelity UI prototyping with Google Stitch MCP. Use when the user needs to generate, iterate, or refine UI screens via Stitch prompts.
---

# Stitch Design Skill

Automate high-fidelity UI prototype generation using Google Stitch via MCP tools.
This skill covers prompt engineering, generation, evaluation, iteration, multi-page consistency, and asset delivery.

---

## When to Use

- User asks to generate a UI screen / mockup / prototype
- User asks to refine or iterate an existing Stitch design
- User needs multi-page design with consistent visual language
- User wants design variants for A/B exploration

---

## Prerequisites

Stitch MCP Server must be available. Verify with:

```bash
# Claude Code: check MCP tool availability
# Confirm tools: generate_screen_from_text, get_screen, edit_screens, generate_variants, list_screens
```

If unavailable, guide user to configure MCP in their Claude Code settings or `~/.claude/settings.json`.

---

## Step 1: Analyze Requirements & Build Prompt

### 1.1 Extract from User Request

Identify: target platform, page type, visual style, core components, color palette, typography, constraints.

### 1.2 Prompt Engineering Rules

Follow these principles strictly -- they are derived from official Stitch team guidance and battle-tested community patterns:

| Rule | Detail |
|------|--------|
| Broad first, detail later | Start with a high-level concept to explore direction, then drill into per-screen details |
| Global style first | Define colors / fonts / vibe BEFORE specific elements |
| Single change per prompt | Each prompt modifies ONE dimension only |
| Visual precision | Use Hex codes (`#FFF8F0`), material adjectives (`soft glow shadow`, `warm off-white`) |
| Reserved zones | Explicitly mention system UI areas (WeChat capsule, iOS status bar, Android nav bar) |
| Plain text preferred | Official recommendation: use natural language, NOT XML/JSON structures |
| Adjectives set the vibe | Words like `vibrant`, `minimalist`, `brutalist` directly influence color/font/image choices |
| Reference by name | Always specify page name + component name + position (e.g. "primary button on sign-up form") |

### 1.3 Structured Prompt Template

Assemble requirements into this format:

```
Platform: [iOS / Android / Web / WeChat Mini Program]
Screen: [page name]
Style: [visual style keywords + adjectives]
Layout: [layout description]
Components: [component list with positions]
Colors: [primary #HEX, secondary #HEX, background #HEX]
Typography: [font suggestions]
Constraints: [reserved areas / special limits]
```

**Example -- recipe sharing app detail page:**

```
Platform: iOS (iPhone 15 Pro, 393x852)
Screen: Recipe Detail
Style: Warm editorial, clean white background, food photography focus
Layout: Full-screen hero image at top, scrollable content below
Components:
  - Top: full-width hero image of the dish (16:9 ratio)
  - Below image: recipe title (large serif), author avatar + name, rating stars
  - Info row: prep time / cook time / servings as icon + label pairs
  - Bottom: floating "Start Cooking" button, full-width
Colors: primary #E85D3A, secondary #F4A261, background #FEFCFB
Typography: Playfair Display for titles, Inter for body
Constraints: iOS status bar reserved, bottom safe area for home indicator
```

---

## Step 2: Generate Screen

```python
# Use MCP tool
result = generate_screen_from_text(
    projectId="<project_id>",
    prompt="<assembled prompt>",
    deviceType="MOBILE"  # or DESKTOP / TABLET
)
# Record: projectId, screenId from result
```

If `output_components` contains suggestions, present them to user for selection before proceeding.

---

## Step 3: Evaluate Result

Retrieve the screen and assess on these dimensions:

```python
screen = get_screen(
    name="projects/<pid>/screens/<sid>",
    projectId="<pid>",
    screenId="<sid>"
)
```

### Evaluation Checklist

| Dimension | Check |
|-----------|-------|
| Layout | Spacing, alignment, visual hierarchy clear? |
| Color consistency | Matches specified palette? |
| Component completeness | All requested UI components present? |
| Platform fit | System UI areas unobstructed? |
| Overall quality | Feels high-fidelity, not wireframe-level? |

---

## Step 4: Iterate (Max 3 Rounds)

If evaluation fails on any dimension:

1. Identify the SINGLE most impactful issue
2. Craft a targeted edit prompt addressing ONLY that issue
3. Call `edit_screens`:

```python
edit_screens(
    projectId="<pid>",
    selectedScreenIds=["<sid>"],
    prompt="<targeted fix prompt>"
)
```

4. Re-evaluate (back to Step 3)
5. **Hard limit: 3 iteration rounds.** After 3 rounds, deliver best result with notes on remaining issues.

### Iteration Anti-Patterns (Avoid These)

- Do NOT mix layout changes with component styling in one prompt
- Do NOT assume Stitch remembers prior designs -- be explicit every time
- Do NOT use overly long prompts (5000+ chars) for edits -- keep edits surgical
- Do NOT retry the same failing prompt -- rephrase or decompose

---

## Step 5: Deliver Assets

Once satisfied:

1. Save screen data to project `design/` directory
2. Present final screenshot to user
3. Provide screen IDs for future reference

```python
# List all screens in project for reference
screens = list_screens(projectId="<pid>")
```

---

## Multi-Page Workflow

When generating multiple pages for the same app:

1. **Home page first** -- establishes the global visual tone
2. **Subsequent pages** reference the home page explicitly:
   ```
   Using the design context from the Home Screen, generate a [PageName] screen
   with the same color palette (#FF8C42 primary, #FFF8F0 background),
   typography, and component styling...
   ```
3. Each page goes through Steps 2-5 independently
4. After all pages, run a **Consistency Patch Pass** (see below)

---

## Design Variants

When user is exploring direction:

1. Generate baseline with `generate_screen_from_text`
2. Generate variants:

```python
generate_variants(
    projectId="<pid>",
    selectedScreenIds=["<sid>"],
    prompt="Generate 3 style variants",
    variantOptions={
        "numVariants": 3,
        "creativeRange": "HIGH",
        "focusAspects": ["color_palette", "layout"]
    }
)
```

3. Present all variants to user for direction selection
4. Continue iterating on the chosen variant

---

## Consistency Patch

When cross-page component styles diverge:

1. Identify the "golden" version (page + component)
2. Send targeted patch to divergent pages:

```
Redesign the [component] on this page to exactly match [Page X]:
[describe the exact style -- colors, shapes, borders, shadows]
```

**Example:**
```
Redesign the slider on this page to exactly match Screen 2:
solid amber fill blob, white circular thumb with warm amber border,
no center track line.
```

---

## Multi-Language UI Patching

1. Generate the refined UI in English first (baseline)
2. Batch-translate in one prompt per page:

```
Change all UI text to Simplified Chinese:
- "Searching..." -> "正在搜索..."
- "Connect" -> "连接"
- "Settings" -> "设置"
- "Intensity" -> "强度"
```

3. This counts as ONE change (respects single-change-per-prompt rule)

---

## Image Control Techniques

Stitch can modify images within generated screens. Key techniques:

### Batch Modify Images

Target all images of a type at once:

```
Change background of all product images on the landing page to light taupe.
```

### Target a Specific Image

Reference by person, position, or label:

```
On the Team page, the image of "Dr. Carter (Lead Dentist)": update her lab coat to black.
```

### Coordinate Images with Theme Changes

When changing theme, explicitly ask images to follow:

```
Update theme to light orange. Ensure all images and illustrative icons
match this new color scheme.
```

### Describe Desired Image Style

For hero/background images, give photographic direction:

```
Music player page for "Suburban Legends." Album art is a macro, zoomed-in
photo of ocean water. Page background and imagery should reflect this.
```

---

## Font & Border Control

Precise typography and border control techniques:

### Font Style

```
Use a playful sans-serif font for all body text.
Change all headings to a bold serif font.
```

### Button & Border Shapes

```
Make all buttons have fully rounded corners (pill shape).
Give all input fields a 2px solid black border with 8px border-radius.
```

### Combined Theme Application

Apply font + color + border in a single themed prompt:

```
Book discovery app: use a serif font for all text, light green (#A8D5BA)
as brand accent color, rounded pill buttons, and subtle card shadows.
```

---

## Prompt Enhancer Pattern

For complex screens, use an AI (Gemini / ChatGPT / Claude) to transform a simple user idea into a structured Stitch prompt before sending it.

### How It Works

1. User provides a brief idea: `"A dashboard for marathon runners"`
2. AI Enhancer expands it into the structured template (Platform / Screen / Style / Layout / Components / Colors / Typography / Constraints)
3. Send the enhanced prompt to Stitch

### Enhancer Prompt Template

Use this meta-prompt to generate Stitch prompts:

```
You are a Stitch Prompt Engineer. Given a brief app idea,
generate a detailed Stitch prompt using this structure:

Platform: [detect from context or default to iOS]
Screen: [infer the most important page]
Style: [pick 3-4 visual adjectives that match the domain]
Layout: [describe spatial organization]
Components: [list 5-8 specific UI elements with positions]
Colors: [generate a harmonious 3-color palette with hex codes]
Typography: [suggest appropriate font pairing]
Constraints: [platform-specific reserved areas]

User idea: "{{user_input}}"
```

### When to Use

- User gives a vague or one-line description
- Complex multi-component pages where manual prompt writing is tedious
- Exploring visual directions rapidly (generate 3 different enhanced prompts for the same idea)

---

## Community-Proven Tips

| Tip | Source |
|-----|--------|
| Decompose complex pages into sequential prompts (structure -> filters -> alignment) | tempo (factory dashboard case) |
| Screenshot after every successful step -- Stitch may reset designs | tempo |
| Use ChatGPT/Gemini to pre-generate structured component-block prompts for reuse | John Kenny |
| For mobile: ultra-detailed first prompt (~5000 chars) gets ~60% match, then micro-tune | Hoang Anh Huynh |
| Stitch experimental mode is more accurate than standard mode | Yusouph Sadick |
| Use Annotate feature for same-screen iteration (official recommendation) | Stitch team (Vincent, Rishabh) |

---

## Failure Modes & Workarounds

| Failure | Workaround |
|---------|------------|
| Edit completely rebuilds layout | Decompose: do structure first, then style, then details |
| Cross-page styles inconsistent | Use Consistency Patch with explicit style description |
| Small detail edits (checkbox, alignment) don't work | Known Stitch limitation; note for user and suggest manual CSS fix |
| Prompt too vague, result off-target | Add visual precision: hex colors, material adjectives, exact positions |
