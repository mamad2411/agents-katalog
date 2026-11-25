---
name: font-optimization-reference
description: Web font optimization reference - font-display, WOFF2, variable fonts, Google Fonts, preloading, and performance
searchable: true
tags: [fonts, web-fonts, performance, woff2, google-fonts, font-display, preload, variable-fonts]
---

# Web Font Optimization Reference

Quick reference for web font optimization, loading strategies, and performance best practices.

## font-display Strategies

### Quick Decision Guide

| Strategy | FOIT | FOUT | Use Case |
|----------|------|------|----------|
| `swap` | ❌ | ✅ | Best for body text (recommended) |
| `block` | ✅ | ❌ | Icons, critical headings |
| `fallback` | Short | ✅ | Balanced approach |
| `optional` | Shortest | ✅ | Performance-first |
| `auto` | Browser | Browser | Not recommended |

### Implementation

```css
/* RECOMMENDED - Body text */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2');
  font-display: swap;
  font-weight: 400;
  font-style: normal;
}

/* Icons - Prevent layout shift */
@font-face {
  font-family: 'Material Icons';
  src: url('/fonts/material-icons.woff2') format('woff2');
  font-display: block;
}

/* Performance-first */
@font-face {
  font-family: 'Optional Font';
  src: url('/fonts/optional.woff2') format('woff2');
  font-display: optional;
}
```

## WOFF2 Format

### Complete Format Cascade

```css
@font-face {
  font-family: 'MyFont';
  src: url('font.woff2') format('woff2'),       /* Modern browsers */
       url('font.woff') format('woff'),         /* Fallback */
       url('font.ttf') format('truetype');      /* Legacy */
  font-display: swap;
}
```

### WOFF2 Only (Modern)

```css
@font-face {
  font-family: 'MyFont';
  src: url('font.woff2') format('woff2');
  font-display: swap;
}
```

## Font Preloading

### Critical Fonts

```html
<!-- Preload critical fonts -->
<link
  rel="preload"
  href="/fonts/inter-regular.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
```

### Multiple Weights

```html
<link rel="preload" href="/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-700.woff2" as="font" type="font/woff2" crossorigin>
```

⚠️ **Warning**: Only preload 1-2 critical fonts to avoid blocking rendering.

## Google Fonts Optimization

### Method 1: Preconnect (Fastest)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
```

### Method 2: Self-Hosting (Best Performance)

```css
/* Download fonts from google-webfonts-helper.herokuapp.com */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-v12-latin-regular.woff2') format('woff2');
  font-display: swap;
  font-weight: 400;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153;
}
```

### Method 3: Font API with Subsetting

```html
<!-- Only load Latin characters, weights 400 and 700 -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap&subset=latin" rel="stylesheet">
```

## Variable Fonts

### Basic Declaration

```css
@font-face {
  font-family: 'Inter Variable';
  src: url('inter-variable.woff2') format('woff2-variations');
  font-display: swap;
  font-weight: 100 900; /* Range */
}
```

### Usage with font-variation-settings

```css
.text {
  font-family: 'Inter Variable', sans-serif;
  font-weight: 600;
}

.custom {
  font-family: 'Inter Variable';
  font-variation-settings: 'wght' 650, 'slnt' -10;
}
```

### Benefits
- **1 file** replaces multiple weights (400, 500, 600, 700, etc.)
- **Smaller total size** for multi-weight usage
- **Smooth transitions** between weights

## Font Subsetting

### Unicode Range Subsetting

```css
/* Latin only */
@font-face {
  font-family: 'Inter';
  src: url('inter-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153;
}

/* Cyrillic only */
@font-face {
  font-family: 'Inter';
  src: url('inter-cyrillic.woff2') format('woff2');
  unicode-range: U+0400-045F, U+0490-0491, U+04B0-04B1;
}
```

### Tools
- **glyphhanger** - CLI tool for subsetting
- **pyftsubset** - FontTools subsetting
- **google-webfonts-helper** - Pre-subsetted Google Fonts

## System Font Stacks

### Modern System Stack

```css
body {
  font-family:
    -apple-system, BlinkMacSystemFont,
    'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans',
    'Helvetica Neue', sans-serif;
}
```

### GitHub Stack

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
```

### Monospace Stack

```css
font-family: ui-monospace, 'Cascadia Code', 'Source Code Pro', Menlo, Consolas, monospace;
```

## Performance Optimization

### Size-Adjust Descriptor

```css
@font-face {
  font-family: 'Inter';
  src: url('inter.woff2') format('woff2');
  size-adjust: 105%; /* Adjust to match fallback */
}
```

### Font Loading API

```javascript
// Check if font is loaded
document.fonts.ready.then(() => {
  console.log('All fonts loaded');
});

// Load specific font
const font = new FontFace('Inter', 'url(/fonts/inter.woff2)');
font.load().then(() => {
  document.fonts.add(font);
});
```

## Best Practices Checklist

✅ **DO:**
- Use WOFF2 format
- Add `font-display: swap` for body text
- Preload 1-2 critical fonts only
- Self-host Google Fonts when possible
- Subset fonts to required characters
- Use variable fonts for multiple weights
- Include fallback fonts
- Test on slow connections

❌ **DON'T:**
- Preload all fonts
- Use custom fonts for body text without fallback
- Load entire font families (all weights)
- Forget `crossorigin` on preload
- Skip WOFF2 compression
- Use EOT or SVG formats
- Load fonts from slow CDNs

## Core Web Vitals Impact

### LCP (Largest Contentful Paint)
- **Preload critical fonts** to avoid render blocking
- **Use system fonts** for fastest LCP
- **font-display: swap** to render text immediately

### CLS (Cumulative Layout Shift)
- **Use size-adjust** to match fallback metrics
- **Preload fonts** to reduce shift
- **font-display: optional** for zero shift (but may not load)

### FCP (First Contentful Paint)
- **System fonts** = instant FCP
- **Preconnect** to font providers
- **Limit font weights** to 2-3 maximum

## Quick Patterns

### Pattern 1: Performance-First

```html
<!-- System fonts with optional web font enhancement -->
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }
</style>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter&display=optional" rel="stylesheet">

<style>
  .enhanced {
    font-family: 'Inter', -apple-system, sans-serif;
  }
</style>
```

### Pattern 2: Self-Hosted Production

```html
<!-- Preload critical fonts -->
<link rel="preload" href="/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>

<style>
  @font-face {
    font-family: 'Inter';
    src: url('/fonts/inter-400.woff2') format('woff2');
    font-display: swap;
    font-weight: 400;
  }

  @font-face {
    font-family: 'Inter';
    src: url('/fonts/inter-700.woff2') format('woff2');
    font-display: swap;
    font-weight: 700;
  }

  body {
    font-family: 'Inter', -apple-system, sans-serif;
  }
</style>
```

### Pattern 3: Variable Font

```html
<link rel="preload" href="/fonts/inter-variable.woff2" as="font" type="font/woff2" crossorigin>

<style>
  @font-face {
    font-family: 'Inter Variable';
    src: url('/fonts/inter-variable.woff2') format('woff2-variations');
    font-display: swap;
    font-weight: 100 900;
  }

  body {
    font-family: 'Inter Variable', -apple-system, sans-serif;
    font-weight: 400;
  }

  h1 { font-weight: 700; }
  .thin { font-weight: 300; }
</style>
```

---

Use this reference for quick font optimization lookups and performance improvements.
