# DonateMate Design System for Figma

You are generating HTML that will be imported into Figma using the HTML to Figma plugin. Use this design system to ensure consistency with the DonateMate mobile app.

## Setup

Always include these in your HTML `<head>`:

```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  /* Colors */
  --color-white: #FFFFFF;
  --color-black: #000000;
  --color-slate-50: #F8FAFC;
  --color-slate-100: #F2F5F9;
  --color-slate-200: #E2E8F0;
  --color-slate-300: #CBD5E1;
  --color-slate-400: #94A3B8;
  --color-slate-500: #64748B;
  --color-slate-600: #475569;
  --color-slate-900: #0F172A;
  --color-sky-300: #5DD3FF;
  --color-sky-400: #3DBAFE;
  --color-sky-500: #2AA8F0;
  --color-sky-600: #1E9AE8;
  --color-red-500: #EF4444;
  --color-red-600: #DC2626;
  --color-green-500: #22C55E;
  --color-green-600: #16A34A;

  /* Semantic Colors */
  --text-primary: #0F172A;
  --text-secondary: #64748B;
  --text-tertiary: #94A3B8;
  --text-label: #475569;
  --text-error: #DC2626;
  --text-success: #16A34A;
  --text-inverse: #FFFFFF;
  --bg-primary: #FFFFFF;
  --bg-secondary: #F8FAFC;
  --bg-tertiary: #F2F5F9;
  --bg-inverse: #0F172A;
  --border-primary: #E2E8F0;
  --border-secondary: #CBD5E1;
  --border-focus: #3DBAFE;
  --border-error: #EF4444;
  --border-success: #22C55E;
  --accent-primary: #3DBAFE;
  --accent-light: #5DD3FF;
  --accent-dark: #2AA8F0;
  --accent-darker: #1E9AE8;
  --icon-default: #64748B;
  --icon-muted: #94A3B8;
  --icon-active: #3DBAFE;
  --icon-error: #EF4444;
  --icon-success: #22C55E;
  --icon-inverse: #FFFFFF;

  /* Spacing */
  --space-2: 2px;
  --space-4: 4px;
  --space-8: 8px;
  --space-12: 12px;
  --space-16: 16px;
  --space-20: 20px;
  --space-24: 24px;
  --space-28: 28px;
  --space-32: 32px;
  --space-36: 36px;
  --space-40: 40px;
  --space-48: 48px;
  --space-56: 56px;
  --space-64: 64px;

  /* Border Radius */
  --radius-4: 4px;
  --radius-8: 8px;
  --radius-12: 12px;
  --radius-16: 16px;
  --radius-20: 20px;
  --radius-24: 24px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-xs: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 8px rgba(0,0,0,0.08);
  --shadow-lg: 0 8px 16px rgba(0,0,0,0.1);
  --shadow-xl: 0 12px 24px rgba(0,0,0,0.12);

  /* Typography */
  --font-family: 'DM Sans', sans-serif;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font-family); }
</style>
```

---

## Mobile Screen Dimensions

Always use iPhone 14 Pro dimensions for mobile screens:
- **Width:** 393px
- **Height:** 852px (or auto for scrollable content)
- **Safe area padding:** 24px horizontal, 59px top (status bar), 34px bottom (home indicator)

```html
<body style="
  width: 393px;
  min-height: 852px;
  background: var(--bg-primary);
  padding: 59px 24px 34px 24px;
">
```

---

## Typography

### Display (Hero Headlines)
```html
<!-- Display XL: 40px Bold -->
<h1 style="font-size: 40px; font-weight: 700; line-height: 130%; color: var(--text-primary);">
  Hero Title
</h1>

<!-- Display LG: 32px Bold -->
<h1 style="font-size: 32px; font-weight: 700; line-height: 131%; color: var(--text-primary);">
  Page Title
</h1>

<!-- Display MD: 28px Bold -->
<h2 style="font-size: 28px; font-weight: 700; line-height: 136%; color: var(--text-primary);">
  Section Title
</h2>
```

### Headings
```html
<!-- Heading XL: 24px SemiBold -->
<h2 style="font-size: 24px; font-weight: 600; line-height: 133%; color: var(--text-primary);">
  Heading XL
</h2>

<!-- Heading LG: 20px SemiBold -->
<h3 style="font-size: 20px; font-weight: 600; line-height: 150%; color: var(--text-primary);">
  Heading LG
</h3>

<!-- Heading MD: 18px SemiBold -->
<h4 style="font-size: 18px; font-weight: 600; line-height: 156%; color: var(--text-primary);">
  Heading MD
</h4>

<!-- Heading SM: 16px SemiBold -->
<h5 style="font-size: 16px; font-weight: 600; line-height: 150%; color: var(--text-primary);">
  Heading SM
</h5>
```

### Body Text
```html
<!-- Body LG: 18px Regular -->
<p style="font-size: 18px; font-weight: 400; line-height: 156%; color: var(--text-primary);">
  Large body text
</p>

<!-- Body MD: 16px Regular (Default) -->
<p style="font-size: 16px; font-weight: 400; line-height: 150%; color: var(--text-primary);">
  Default body text
</p>

<!-- Body SM: 14px Regular -->
<p style="font-size: 14px; font-weight: 400; line-height: 143%; color: var(--text-secondary);">
  Small body text, descriptions
</p>

<!-- Body XS: 12px Regular -->
<p style="font-size: 12px; font-weight: 400; line-height: 150%; color: var(--text-tertiary);">
  Caption, helper text
</p>
```

### Labels
```html
<!-- Label LG: 16px Medium -->
<span style="font-size: 16px; font-weight: 500; line-height: 150%; color: var(--text-primary);">
  Button Text
</span>

<!-- Label MD: 14px Medium -->
<span style="font-size: 14px; font-weight: 500; line-height: 143%; color: var(--text-label);">
  Form Label
</span>

<!-- Label SM: 12px Medium -->
<span style="font-size: 12px; font-weight: 500; line-height: 150%; color: var(--text-label);">
  Small Label
</span>
```

---

## Components

### Primary Button
```html
<button style="
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 56px;
  background: linear-gradient(180deg, #5DD3FF 0%, #3DBAFE 33%, #2AA8F0 66%, #1E9AE8 100%);
  color: var(--text-inverse);
  font-size: 16px;
  font-weight: 500;
  border: none;
  border-radius: var(--radius-16);
  cursor: pointer;
">
  Button Text
</button>
```

### Secondary Button
```html
<button style="
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 56px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 500;
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-16);
  cursor: pointer;
">
  Button Text
</button>
```

### Ghost Button / Text Link
```html
<button style="
  background: transparent;
  color: var(--accent-primary);
  font-size: 14px;
  font-weight: 500;
  border: none;
  cursor: pointer;
">
  Text Link
</button>
```

### Text Input
```html
<div style="display: flex; flex-direction: column; gap: 4px;">
  <label style="font-size: 14px; font-weight: 500; color: var(--text-label);">
    Label
  </label>
  <input style="
    width: 100%;
    height: 56px;
    padding: 0 16px;
    background: var(--bg-primary);
    border: 1px solid var(--border-primary);
    border-radius: var(--radius-12);
    font-family: var(--font-family);
    font-size: 16px;
    color: var(--text-primary);
    outline: none;
  " placeholder="Placeholder text">
  <span style="font-size: 12px; color: var(--text-secondary);">
    Helper text (optional)
  </span>
</div>
```

### Input - Focus State
```html
<input style="
  ...
  border: 2px solid var(--border-focus);
">
```

### Input - Error State
```html
<div style="display: flex; flex-direction: column; gap: 4px;">
  <label style="font-size: 14px; font-weight: 500; color: var(--text-label);">
    Label
  </label>
  <input style="
    width: 100%;
    height: 56px;
    padding: 0 16px;
    background: var(--bg-primary);
    border: 1px solid var(--border-error);
    border-radius: var(--radius-12);
    font-size: 16px;
    color: var(--text-primary);
  " value="Invalid input">
  <span style="font-size: 12px; color: var(--text-error);">
    Error message
  </span>
</div>
```

### Card
```html
<div style="
  background: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-16);
  padding: 16px;
  box-shadow: var(--shadow-sm);
">
  Card content
</div>
```

### Checkbox
```html
<!-- Unchecked -->
<div style="display: flex; align-items: center; gap: 12px;">
  <div style="
    width: 20px;
    height: 20px;
    border: 1px solid var(--border-primary);
    border-radius: var(--radius-4);
    background: var(--bg-primary);
  "></div>
  <span style="font-size: 14px; color: var(--text-primary);">Checkbox label</span>
</div>

<!-- Checked -->
<div style="display: flex; align-items: center; gap: 12px;">
  <div style="
    width: 20px;
    height: 20px;
    border-radius: var(--radius-4);
    background: var(--accent-primary);
    display: flex;
    align-items: center;
    justify-content: center;
  ">
    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
      <path d="M2 6L5 9L10 3" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>
  <span style="font-size: 14px; color: var(--text-primary);">Checkbox label</span>
</div>
```

### Modal / Bottom Sheet
```html
<!-- Overlay -->
<div style="
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  display: flex;
  align-items: flex-end;
  justify-content: center;
">
  <!-- Modal -->
  <div style="
    width: 100%;
    background: var(--bg-primary);
    border-radius: var(--radius-20) var(--radius-20) 0 0;
    padding: 24px;
    box-shadow: var(--shadow-xl);
  ">
    <div style="
      width: 36px;
      height: 4px;
      background: var(--border-secondary);
      border-radius: var(--radius-full);
      margin: 0 auto 16px;
    "></div>
    Modal content
  </div>
</div>
```

### Icon Button
```html
<button style="
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: var(--radius-full);
  cursor: pointer;
">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
    <path d="..." stroke="var(--icon-default)" stroke-width="2"/>
  </svg>
</button>
```

---

## Common Icons (SVG)

### Chevron Left (Back)
```html
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

### Chevron Right
```html
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

### Close (X)
```html
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

### Check
```html
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M5 12L10 17L20 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

### Eye (Show Password)
```html
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
</svg>
```

### Eye Off (Hide Password)
```html
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20C5 20 1 12 1 12A18.45 18.45 0 0 1 5.06 6.06M9.9 4.24A9.12 9.12 0 0 1 12 4C19 4 23 12 23 12A18.5 18.5 0 0 1 19.73 16.73" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M1 1L23 23" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

---

## Screen Templates

### Auth Screen (Sign In / Sign Up)
```html
<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>/* Include CSS variables from above */</style>
</head>
<body style="
  width: 393px;
  min-height: 852px;
  background: var(--bg-primary);
  padding: 59px 24px 34px 24px;
  display: flex;
  flex-direction: column;
">
  <!-- Header -->
  <div style="margin-bottom: 32px;">
    <h1 style="font-size: 28px; font-weight: 700; line-height: 136%; color: var(--text-primary); margin-bottom: 8px;">
      Welcome back
    </h1>
    <p style="font-size: 16px; color: var(--text-secondary);">
      Sign in to continue
    </p>
  </div>

  <!-- Form -->
  <div style="flex: 1; display: flex; flex-direction: column; gap: 16px;">
    <!-- Email Input -->
    <div style="display: flex; flex-direction: column; gap: 4px;">
      <label style="font-size: 14px; font-weight: 500; color: var(--text-label);">Email</label>
      <input style="
        width: 100%;
        height: 56px;
        padding: 0 16px;
        background: var(--bg-primary);
        border: 1px solid var(--border-primary);
        border-radius: 12px;
        font-family: inherit;
        font-size: 16px;
      " placeholder="you@example.com">
    </div>

    <!-- Password Input -->
    <div style="display: flex; flex-direction: column; gap: 4px;">
      <label style="font-size: 14px; font-weight: 500; color: var(--text-label);">Password</label>
      <div style="position: relative;">
        <input type="password" style="
          width: 100%;
          height: 56px;
          padding: 0 48px 0 16px;
          background: var(--bg-primary);
          border: 1px solid var(--border-primary);
          border-radius: 12px;
          font-family: inherit;
          font-size: 16px;
        " placeholder="••••••••">
        <button style="
          position: absolute;
          right: 12px;
          top: 50%;
          transform: translateY(-50%);
          background: none;
          border: none;
          cursor: pointer;
        ">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12Z" stroke="#94A3B8" stroke-width="2"/>
            <circle cx="12" cy="12" r="3" stroke="#94A3B8" stroke-width="2"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Forgot Password -->
    <div style="text-align: right;">
      <button style="background: none; border: none; color: var(--accent-primary); font-size: 14px; font-weight: 500; cursor: pointer;">
        Forgot password?
      </button>
    </div>
  </div>

  <!-- Bottom Actions -->
  <div style="display: flex; flex-direction: column; gap: 16px; margin-top: auto;">
    <button style="
      width: 100%;
      height: 56px;
      background: linear-gradient(180deg, #5DD3FF 0%, #3DBAFE 33%, #2AA8F0 66%, #1E9AE8 100%);
      color: white;
      font-size: 16px;
      font-weight: 500;
      border: none;
      border-radius: 16px;
      cursor: pointer;
    ">Sign In</button>

    <p style="text-align: center; font-size: 14px; color: var(--text-secondary);">
      Don't have an account?
      <button style="background: none; border: none; color: var(--accent-primary); font-weight: 500; cursor: pointer;">Sign Up</button>
    </p>
  </div>
</body>
</html>
```

---

## Best Practices

1. **Always use CSS variables** for colors, spacing, and radii - never hardcode values
2. **Use semantic color names** (`--text-primary`, `--bg-secondary`) not raw colors
3. **Maintain consistent spacing** - use the spacing scale (8, 12, 16, 20, 24, 32px)
4. **Use the gradient** for primary buttons: `linear-gradient(180deg, #5DD3FF 0%, #3DBAFE 33%, #2AA8F0 66%, #1E9AE8 100%)`
5. **Border radius:** 12px for inputs, 16px for buttons/cards, 20px for modals
6. **Input height:** 56px standard
7. **Button height:** 56px standard
8. **Mobile width:** 393px (iPhone 14 Pro)
9. **Content padding:** 24px horizontal
10. **Icon size:** 24px standard, stroke-width 2

---

## Color Quick Reference

| Use Case | Variable | Hex |
|----------|----------|-----|
| Primary text | `--text-primary` | #0F172A |
| Secondary text | `--text-secondary` | #64748B |
| Placeholder | `--text-tertiary` | #94A3B8 |
| Labels | `--text-label` | #475569 |
| Error text | `--text-error` | #DC2626 |
| Success text | `--text-success` | #16A34A |
| White text | `--text-inverse` | #FFFFFF |
| Main background | `--bg-primary` | #FFFFFF |
| Card background | `--bg-secondary` | #F8FAFC |
| Subtle background | `--bg-tertiary` | #F2F5F9 |
| Primary border | `--border-primary` | #E2E8F0 |
| Focus border | `--border-focus` | #3DBAFE |
| Error border | `--border-error` | #EF4444 |
| Accent/Primary | `--accent-primary` | #3DBAFE |
| Accent hover | `--accent-dark` | #2AA8F0 |
