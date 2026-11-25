---
name: rgaa-colors
description: "Audit a web page for RGAA v4.1.2 Theme 3 – Colors accessibility compliance. Checks that information is not conveyed by color alone, that text contrast ratios meet minimums (4.5:1 for normal text, 3:1 for large text), and that UI components and graphical elements have sufficient contrast (3:1). Use this skill when someone asks to check color contrast, verify RGAA Theme 3 compliance, audit contrast ratios, or check color accessibility on a website."
---

# RGAA Colors Accessibility Audit (Theme 3)

Audits a web page against the 3 criteria of RGAA v4.1.2 Theme 3: Colors.

## Audit procedure

### Step 1: Gather color data

Use `javascript_tool` to sample text contrast across key elements:

```javascript
(() => {
  const samples = [];
  const selectors = 'h1,h2,h3,h4,h5,h6,p,a,span,li,td,th,label,button,input,select,textarea';
  const seen = new Set();

  document.querySelectorAll(selectors).forEach(el => {
    const style = getComputedStyle(el);
    const color = style.color;
    const bg = style.backgroundColor;
    const fontSize = parseFloat(style.fontSize);
    const fontWeight = parseInt(style.fontWeight) || (style.fontWeight === 'bold' ? 700 : 400);
    const key = `${color}|${bg}|${fontSize}|${fontWeight}`;

    if (!seen.has(key) && el.textContent.trim()) {
      seen.add(key);
      samples.push({
        tag: el.tagName.toLowerCase(),
        text: el.textContent.trim().substring(0, 50),
        color: color,
        backgroundColor: bg,
        fontSize: fontSize,
        fontWeight: fontWeight,
        isLargeText: (fontSize >= 24) || (fontSize >= 18.5 && fontWeight >= 700)
      });
    }
  });

  // Check links distinguishability
  const links = [];
  document.querySelectorAll('a').forEach(el => {
    const style = getComputedStyle(el);
    links.push({
      href: el.href?.substring(0, 80),
      color: style.color,
      textDecoration: style.textDecorationLine,
      hasUnderline: style.textDecorationLine.includes('underline'),
      text: el.textContent.trim().substring(0, 50)
    });
  });

  return JSON.stringify({ samples: samples.slice(0, 50), links: links.slice(0, 20) }, null, 2);
})()
```

### Step 2: Evaluate criteria

**Criterion 3.1** – Information must not be conveyed by color alone.
Check for patterns where color is the sole differentiator: required fields marked only in red, links distinguished only by color (no underline), status messages using only color coding. This requires visual inspection — take a screenshot and analyze.

**Criterion 3.2** – Text contrast must meet minimums.
- Normal text (<24px, or <18.5px bold): minimum 4.5:1 contrast ratio
- Large text (≥24px, or ≥18.5px bold): minimum 3:1 contrast ratio
- Use the luminance formula to calculate contrast ratios from the computed color and background-color values.

Exceptions: logos, brand names, purely decorative text, disabled UI elements.

**Criterion 3.3** – UI components and graphical elements must have 3:1 contrast.
- Interactive component borders, icons, focus indicators: 3:1 minimum against adjacent background
- Informational graphical elements (chart bars, pie slices, icons conveying info): 3:1 minimum

Exceptions: inactive components, browser-native styles, elements where color is not needed for identification, logos, essential graphical representations.

### Step 3: Contrast calculation helper

To compute contrast ratio from RGB:
1. Convert sRGB to linear: `L = (v <= 0.03928) ? v/12.92 : ((v+0.055)/1.055)^2.4`
2. Relative luminance: `Y = 0.2126*R + 0.7152*G + 0.0722*B`
3. Contrast ratio: `(L1 + 0.05) / (L2 + 0.05)` where L1 is the lighter

### Step 4: Generate report

For each criterion, report status and list any failing elements with their current ratio and the required minimum. Provide specific CSS fixes (e.g., suggested color values that would pass).
