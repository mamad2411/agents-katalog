---
name: unity-uss
description: >
  Unity 6000.3 LTS UI Toolkit USS (Unity Style Sheets) patterns. Covers selectors,
  flexbox layout, visual properties, transitions, USS variables, filters, and responsive patterns.
  Trigger: When creating or editing .uss files, styling Unity UI Toolkit elements,
  working with USS selectors, transitions, filters, or responsive UI layouts.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Creating or modifying `.uss` files for Unity UI Toolkit
- Styling UI elements with selectors (class, id, type, pseudo-class)
- Implementing flexbox layouts
- Adding transitions and animations
- Using USS variables for theming
- Applying filters (blur, brightness, etc.) to UI elements

## Critical Rules

### USS Syntax is CSS-Inspired but NOT CSS

```css
/* ✅ CORRECT USS syntax */
.my-class {
    flex-direction: column;
    background-color: rgb(50, 50, 50);
}

/* ❌ WRONG — CSS shorthand not always supported */
.my-class {
    background: rgb(50, 50, 50);  /* Use background-color instead */
}
```

### Selector Rules

- Must begin with letter (A-Z, a-z) or underscore (_)
- Can contain letters, digits, hyphens, underscores
- **Case-sensitive**
- Cannot start with digit or hyphen+digit

### Text Properties Propagate to Children

Unlike most USS properties, text properties cascade:

```css
/* This affects ALL text descendants */
.container {
    font-size: 16px;
    color: white;
    -unity-font-style: bold;
}
```

### Transitions Require EXACT Matching Filter Functions

```css
/* ✅ INTERPOLATES — Same functions, same order */
.element {
    filter: blur(5px) brightness(1.2);
    transition: filter 0.3s ease;
}
.element:hover {
    filter: blur(10px) brightness(1.2);
}

/* ❌ SNAPS — Different order, NO interpolation */
.element:hover {
    filter: brightness(1.2) blur(10px);  /* Order changed! */
}
```

## Selectors

### Simple Selectors

| Type | Syntax | Matches |
|------|--------|---------|
| Type | `Label { }` | All elements of C# type `Label` |
| Class | `.my-class { }` | Elements with `class="my-class"` |
| Name (ID) | `#myElement { }` | Element with `name="myElement"` |
| Universal | `* { }` | All elements |

### Complex Selectors

| Type | Syntax | Matches |
|------|--------|---------|
| Descendant | `.parent .child { }` | `.child` anywhere inside `.parent` |
| Child | `.parent > .child { }` | `.child` as direct child of `.parent` |
| Multiple | `Label.my-class { }` | `Label` elements that also have `.my-class` |
| Selector list | `Label, Button { }` | Both `Label` AND `Button` elements |

### Pseudo-Classes

```css
/* Interaction states */
.button:hover { }
.button:active { }
.input:focus { }
.toggle:checked { }
.button:disabled { }

/* Structural pseudo-classes */
.item:first-child { }
.item:last-child { }
.item:nth-child(2n) { }

/* Combined pseudo-classes */
.button:hover:focus { }  /* Both hover AND focus */
```

### Common Unity Pseudo-Classes

| Pseudo-Class | When Active |
|--------------|-------------|
| `:hover` | Pointer is over element |
| `:active` | Element is being pressed/clicked |
| `:focus` | Element has keyboard focus |
| `:checked` | Toggle/RadioButton is checked |
| `:disabled` | Element is disabled |
| `:enabled` | Element is enabled |
| `:selected` | ListView item is selected |

## Flexbox Layout

### Container Properties

```css
.flex-container {
    flex-direction: row;           /* row | column | row-reverse | column-reverse */
    justify-content: flex-start;   /* flex-start | flex-end | center | space-between | space-around */
    align-items: stretch;          /* flex-start | flex-end | center | stretch | baseline */
    align-content: flex-start;     /* flex-start | flex-end | center | space-between | space-around | stretch */
    flex-wrap: nowrap;             /* nowrap | wrap | wrap-reverse */
    gap: 10px;                     /* spacing between items */
}
```

### Item Properties

```css
.flex-item {
    flex-grow: 0;                  /* 0 = don't grow, 1 = fill available space */
    flex-shrink: 1;                /* 1 = can shrink, 0 = fixed size */
    flex-basis: auto;              /* auto | length | percentage */
    align-self: auto;              /* auto | flex-start | flex-end | center | stretch */
}

/* Shorthand: flex-grow flex-shrink flex-basis */
.flex-item-shorthand {
    flex: 1 0 auto;
}
```

### Common Layout Patterns

#### Centered Content

```css
.center-container {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
}
```

#### Full-Width Header/Content/Footer

```css
.header {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
}

.content {
    margin-top: 60px;
    margin-bottom: 60px;
    flex-grow: 1;
}

.footer {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 60px;
}
```

#### Card Layout

```css
.card {
    background-color: rgb(50, 50, 50);
    border-radius: 10px;
    padding: 20px;
    margin: 10px;
    flex-direction: column;
}

.card-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
}

.card-content {
    font-size: 14px;
    color: rgb(200, 200, 200);
}
```

#### Grid-like Layout (flex-wrap)

```css
.grid {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 10px;
}

.grid-item {
    flex-basis: calc(33% - 10px);
    flex-grow: 0;
    flex-shrink: 0;
}
```

## Positioning

```css
.positioned {
    position: relative;            /* relative | absolute */
    left: 10px;
    top: 20px;
    right: auto;
    bottom: auto;
}
```

## Sizing

```css
.sized {
    width: 200px;
    height: 100px;
    min-width: 100px;
    min-height: 50px;
    max-width: 400px;
    max-height: 200px;
}

/* Responsive sizing */
.responsive {
    width: 100%;
    height: 100%;
}

/* Viewport units */
.viewport-sized {
    width: 50vw;
    height: 30vh;
}
```

## Spacing

```css
.spaced {
    /* Margin — all sides */
    margin: 10px;

    /* Margin — individual */
    margin-top: 5px;
    margin-right: 10px;
    margin-bottom: 15px;
    margin-left: 20px;

    /* Margin — shorthand */
    margin: 10px 20px;           /* top/bottom  left/right */
    margin: 5px 10px 15px 20px;  /* top right bottom left */

    /* Padding — same patterns */
    padding: 10px;
    padding: 5px 10px 15px 20px;
}
```

## Visual Properties

### Background

```css
.background {
    background-color: rgb(255, 0, 0);
    background-image: url("path/to/image.png");
}

/* Background scale modes */
.stretch {
    -unity-background-scale-mode: stretch-to-fill;
}

.scale-and-crop {
    -unity-background-scale-mode: scale-and-crop;
}

.scale-to-fit {
    -unity-background-scale-mode: scale-to-fit;
}
```

### 9-Slice

```css
.nine-sliced {
    -unity-slice-left: 10px;
    -unity-slice-right: 10px;
    -unity-slice-top: 10px;
    -unity-slice-bottom: 10px;
    -unity-slice-scale: 2px;
    -unity-slice-type: tiled;    /* tiled | stretched */
}
```

### Borders

```css
.bordered {
    border-width: 2px;
    border-color: rgb(0, 0, 0);
    border-radius: 10px;

    /* Individual corners */
    border-top-left-radius: 5px;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 15px;
    border-bottom-left-radius: 20px;
}
```

### Text

```css
.text {
    color: rgb(255, 255, 255);
    font-size: 16px;
    font-style: normal;          /* normal | italic */
    font-weight: normal;         /* normal | bold | 100-900 */
    -unity-font-style: bold-and-italic;  /* Unity-specific: bold, italic, bold-and-italic */
    -unity-text-align: middle-center;    /* middle-left | middle-center | middle-right | upper-left | etc. */
    white-space: normal;         /* normal | nowrap */
    overflow: hidden;            /* visible | hidden */
    text-overflow: ellipsis;     /* clip | ellipsis */
}
```

### Font Definition

```css
Label {
    -unity-font-definition: url("/Assets/UI Toolkit/Resources/Fonts & Materials/LiberationSans SDF.asset");
}
```

### Text Auto-Sizing (ATG required)

```css
.auto-size {
    -unity-text-auto-size: best-fit 12px 48px;
}
```

### Text Shadow (SDF fonts only)

```css
Label {
    text-shadow: 6.1px -2.4px 0px rgb(144, 31, 32);
}

/* Individual properties */
Label {
    text-shadow-offset-x: 6.1px;
    text-shadow-offset-y: -2.4px;
    text-shadow-blur-radius: 0px;
    text-shadow-color: rgb(144, 31, 32);
}
```

### Text Outline (SDF fonts only)

```css
Label {
    text-outline: 6px rgb(144, 31, 32);
}

/* Individual properties */
Label {
    -unity-text-outline-width: 6px;
    -unity-text-outline-color: rgb(144, 31, 32);
}
```

### Text Direction

```css
.rtl {
    unity-text-direction: rtl;
}

.ltr {
    unity-text-direction: ltr;
}
```

### Opacity

```css
.semi-transparent {
    opacity: 0.5;
}
```

### Transform

```css
.transformed {
    translate: 10px 20px;
    rotate: 45deg;
    scale: 1.5 1.5;
}
```

## Transitions

### Simple Transition

```css
.animated {
    background-color: rgb(0, 31, 138);
    transition: background-color 3s ease-in-out 1s;
}

.animated:hover {
    background-color: rgb(177, 221, 111);
}
```

### Transition Shorthand

```css
/* transition: property duration timing-function delay */
.multi-transition {
    transition: background-color 0.3s ease, opacity 0.5s ease-in-out;
}
```

### Transition with Individual Properties

```css
.transition-details {
    transition-property: background-color, opacity;
    transition-duration: 0.3s, 0.5s;
    transition-timing-function: ease, ease-in-out;
    transition-delay: 0s, 0.1s;
}
```

### Transition Events (C# side)

```css
/* USS defines the transition */
.color-changer {
    background-color: rgb(0, 31, 138);
    transition-duration: 3s;
}

.color-transition {
    background-color: rgb(177, 221, 111);
}
```

```csharp
// C# toggles class to trigger transition
colorChanger.ToggleInClassList("color-transition");
```

### Looping Transitions — Yo-Yo (A→B→A)

```css
#yoyo-label {
    transition-duration: 3s;
}

.enlarge-scale-yoyo {
    scale: 1.5 1.5;
}
```

### Looping Transitions — A-to-B (A→B with transition, B→A instant)

```css
.enlarge-scale-a2b {
    scale: 1.5 1.5;
    transition-duration: 3s;
}
```

## USS Variables (Custom Properties)

### Defining Variables

```css
/* Global variables on :root */
:root {
    --primary-color: rgb(68, 138, 255);
    --font-size: 20px;
    --spacing: 10px;
}

/* Scoped variables on a selector */
.my-selector {
    --local-color: rgb(255, 0, 0);
}
```

### Using Variables

```css
.my-element {
    color: var(--primary-color);
    font-size: var(--font-size);
    padding: var(--spacing);
}
```

### Variable Types

| Type | Example |
|------|---------|
| Color | `--my-color: rgb(68, 138, 255);` |
| Number | `--my-number: 1.5;` |
| Dimension | `--my-size: 20px;` |
| String | `--my-string: "hello";` |
| Enum | `--my-direction: row;` |
| Resource | `--my-image: url("path/to/image.png");` |

### Variable Precedence

- Variables defined last take precedence if same name
- Inline styles override USS variables
- Scoped variables override global variables

## Filters

### Built-in Filters

| Filter | Syntax | Description |
|--------|--------|-------------|
| Blur | `filter: blur(5px)` | Gaussian blur |
| Brightness | `filter: brightness(1.5)` | 1.0 = normal |
| Contrast | `filter: contrast(1.2)` | 1.0 = normal |
| Grayscale | `filter: grayscale(100%)` | 0-100% |
| Hue Rotate | `filter: hue-rotate(90deg)` | Degrees |
| Invert | `filter: invert(100%)` | 0-100% |
| Opacity | `filter: opacity(50%)` | 0-100% |
| Saturate | `filter: saturate(200%)` | 100% = normal |
| Sepia | `filter: sepia(100%)` | 0-100% |

### Combining Filters

```css
.combined {
    filter: blur(2px) brightness(1.2) contrast(1.1);
    transition: filter 0.3s ease;
}
```

## Rich Text Style Sheets

```html
<style="assetName" name="styleName">Heading</style>

<!-- If default style sheet set in UITK Text Settings: -->
<style="H1">This is heading 1</style>
```

## Responsive Patterns

### Using Percentages

```css
.responsive-container {
    width: 100%;
    height: 100%;
}

.responsive-item {
    width: 50%;
    flex-grow: 1;
}
```

### Using calc()

```css
.calculated {
    width: calc(100% - 20px);
    height: calc(50vh - 10px);
}
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Styles not applying | Wrong selector name | Verify class/id names match UXML |
| Elements not sizing | Missing flex properties | Set `flex-grow` or explicit size |
| Text overflowing | No overflow handling | Use `text-overflow: ellipsis` |
| Layout breaking | Wrong flex-direction | Check `row` vs `column` |
| Transitions not working | Different property types between states | Ensure same properties in both states |
| Filter transition snaps | Different function order | Keep same functions in same order |
| Text effects not showing | Using bitmap font | Switch to SDF font asset |
| Variable not working | Typo in var() name | Check variable name matches definition |

## Best Practices

1. **Use classes over IDs** — More reusable, easier to maintain
2. **Group related styles** — Keep layout, visual, and text properties organized
3. **Use transitions for feedback** — Hover/focus states feel more responsive
4. **Avoid inline styles in UXML** — Keep styling in USS files
5. **Use variables for theming** — Define colors/sizes in one place
6. **Test at multiple sizes** — Ensure layouts work responsively
7. **Use flexbox over absolute** — More maintainable layouts
8. **Text effects need SDF fonts** — Shadows/outlines only work with SDF font assets
