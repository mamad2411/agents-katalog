---
name: canon-favicons
description: Use when implementing favicons, touch icons, web app icons, or browser tab icons — the full set of sizes and formats needed for modern browsers, iOS home screen, Android, and PWA manifests. Trigger when the user mentions favicon, icon, apple-touch-icon, manifest icons, or browser tab icon.
---

# CANON · Favicons

Favicons are the smallest piece of branding and the most often botched. Modern browsers need multiple sizes, formats, and declarations.

## The minimal set

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
```

## Files to generate

| File | Size | Format | Purpose |
|---|---|---|---|
| `favicon.ico` | 32×32 (can embed 16×16) | ICO | Legacy browsers, bookmarks bar |
| `icon.svg` | Scalable | SVG | Modern browsers (Chrome, Firefox) |
| `apple-touch-icon.png` | 180×180 | PNG | iOS home screen |
| `icon-192.png` | 192×192 | PNG | Android home screen, PWA |
| `icon-512.png` | 512×512 | PNG | PWA splash screen |

## SVG favicon with dark mode

SVG favicons can adapt to dark mode:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <style>
    rect { fill: #0a0a0a; }
    @media (prefers-color-scheme: dark) {
      rect { fill: #f5f5f5; }
    }
  </style>
  <rect width="32" height="32" rx="4"/>
</svg>
```

## Web app manifest

```json
{
  "name": "My App",
  "short_name": "App",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#0a0a0a",
  "background_color": "#ffffff",
  "display": "standalone"
}
```

`theme_color` affects the browser toolbar color on Android.

## Design rules

- **Simple at 16px.** If your logo doesn't read at 16×16, simplify it to a lettermark or geometric shape.
- **No text at small sizes.** Text is illegible below 32px.
- **High contrast against both light and dark browser chrome.** Test on light and dark OS themes.
- **Square.** All favicon slots are square. Don't force a horizontal logo into a square; make a square variant.
- **No transparency for apple-touch-icon.** iOS fills transparent areas with black. Use a solid background.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Only a 16×16 favicon.ico | Blurry on retina, missing from home screens |
| Full logo crammed into 32px | Illegible |
| Transparent apple-touch-icon | Black background on iOS |
| No manifest for PWA | Missing home-screen icon on Android |
| favicon.png instead of .ico for legacy | Some browsers only check .ico |
| No SVG favicon | Missing dark-mode adaptation |

## Audit checklist

- [ ] `favicon.ico` at 32×32
- [ ] SVG favicon for modern browsers
- [ ] `apple-touch-icon.png` at 180×180 (no transparency)
- [ ] 192px and 512px PNG for PWA manifest
- [ ] `manifest.webmanifest` linked in `<head>`
- [ ] Icon reads clearly at 16×16
- [ ] Tested on light and dark browser chrome
- [ ] `theme_color` and `background_color` set in manifest

## Sources

- web.dev · "How to Favicon" (Andrey Sitnik)
- Apple · Configuring Web Applications (touch icons)
- W3C · Web App Manifest
- Real Favicon Generator · comprehensive tool
