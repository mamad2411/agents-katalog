---
name: webos-tv
description: Develop and deploy hosted web apps for LG webOS TV. Use when building TV apps, configuring appinfo.json, handling Magic Remote input, managing app lifecycle events, or deploying Next.js/web apps to webOS TV.
---

# webOS TV Development

Build and deploy hosted web apps for LG Smart TVs running webOS.

## Quick Reference

### CLI Commands

```bash
# Install CLI
npm install -g @webos-tools/cli

# Create app
ares-generate -t basic ./myApp

# Package
ares-package ./myApp

# Install to device
ares-install -d myTV com.domain.app_1.0.0_all.ipk

# Launch
ares-launch -d myTV com.domain.app

# Launch on simulator
ares-launch -s 24 ./myApp

# Debug (opens Chrome DevTools)
ares-inspect -d myTV com.domain.app

# Device setup
ares-setup-device
ares-novacom --device myTV --getkey
```

### Device Connection

1. Install "Developer Mode" app from LG Content Store
2. Sign in with LG Developer account
3. Enable Dev Mode Status (TV reboots)
4. Enable Key Server
5. Run: `ares-setup-device` → add device (port: 9922, user: prisoner)
6. Run: `ares-novacom --device myTV --getkey` → enter passphrase from TV

## Hosted Web App Setup

For Next.js or any web app served from a remote URL:

### appinfo.json (minimal)

```json
{
  "id": "com.company.app.name",
  "title": "App Name",
  "main": "index.html",
  "icon": "icon_80x80.png",
  "largeIcon": "icon_130x130.png",
  "type": "web",
  "version": "1.0.0"
}
```

### index.html (redirect to hosted URL)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>App Name</title>
  <script>
    window.location.href = 'https://your-app.vercel.app';
  </script>
</head>
<body></body>
</html>
```

### Required Assets

- `icon_80x80.png` - small icon (PNG)
- `icon_130x130.png` - large icon (PNG)
- `splash_1920x1080.png` - splash screen (optional)

## appinfo.json Key Properties

| Property | Required | Description |
|----------|----------|-------------|
| `id` | Yes | Reverse DNS format. No `-` if using JS services |
| `title` | Yes | Display name on launcher |
| `main` | Yes | Entry point HTML file |
| `icon` | Yes | 80x80 PNG |
| `type` | Yes | Always `"web"` |
| `version` | Yes | `X.Y.Z` format (no leading zeros) |
| `resolution` | No | `"1920x1080"` (default) or `"1280x720"` |
| `disableBackHistoryAPI` | No | `true` to handle back button manually |
| `handlesRelaunch` | No | `true` to handle relaunch in background |
| `splashBackground` | No | 1920x1080 PNG splash image |

## Magic Remote Input

### Keycodes

| Key | Code | | Key | Code |
|-----|------|---|-----|------|
| Left | 37 | | OK/Enter | 13 |
| Up | 38 | | Back | 461 |
| Right | 39 | | Red | 403 |
| Down | 40 | | Green | 404 |

### Input Modes

- **Pointer mode**: Mouse-like, use `onclick`, `onmouseover`
- **5-way mode**: Arrow keys + Enter, activated by pressing arrows

```javascript
document.addEventListener('keydown', (e) => {
  switch (e.keyCode) {
    case 461: // Back
      e.preventDefault();
      handleBack();
      break;
    case 13: // OK
      handleSelect();
      break;
  }
});
```

**Critical**: All apps MUST support both pointer and 5-way navigation.

## App Lifecycle Events

```javascript
// Initial launch
document.addEventListener('webOSLaunch', (e) => {
  console.log('Launch params:', e.detail);
}, true);

// Re-launch (if handlesRelaunch: true)
document.addEventListener('webOSRelaunch', (e) => {
  console.log('Relaunch params:', e.detail);
  // Do background work, then:
  webOSSystem.activate(); // or PalmSystem.activate()
}, true);

// Visibility change (app hidden/shown)
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    // Pause media, stop animations
  } else {
    // Resume
  }
}, true);
```

## Back Button Handling

Two modes controlled by `disableBackHistoryAPI`:

**`false` (default)**: webOS manages history via `history.pushState()`, `history.back()`, `popState`

**`true`**: App receives keycode 461, must handle manually:

```javascript
document.addEventListener('keydown', (e) => {
  if (e.keyCode === 461) {
    e.preventDefault();
    if (canGoBack()) {
      navigateBack();
    } else {
      // Let system handle (shows exit popup on webOS 6+)
    }
  }
});
```

## TV Resolution & Scaling

- Default: 1920x1080 (FHD)
- Use `window.innerWidth`, `window.innerHeight` for actual dimensions
- UHD (4K) NOT supported for web apps
- Design for 10-foot viewing distance (larger fonts, touch targets)

## Debugging

```bash
# Open Chrome DevTools for running app
ares-inspect -d myTV com.domain.app --open
```

Or use Chrome DevTools manually at `http://TV_IP:9998`

## AV Format Support

| Codec | Max Resolution |
|-------|---------------|
| H.264 | 4K@30fps (3840x2160) |
| HEVC | 4K@60fps |
| VP9 | 4K@60fps |
| AV1 | 4K@60fps |

Audio: AAC, Dolby Digital, Dolby Digital Plus, MP3, FLAC, OGG

## Common Issues

### Session timeout
Dev Mode expires. Click **EXTEND** in Developer Mode app while connected to network.

### App not launching
Verify: `ares-device --system-info --device myTV`

### Back button closes app unexpectedly
Set `disableBackHistoryAPI: true` and handle keycode 461.

### Focus issues
Ensure focusable elements have `tabindex="0"` for 5-way navigation.

## Resources

- [Developer Portal](https://webostv.developer.lge.com)
- [appinfo.json Reference](https://webostv.developer.lge.com/develop/references/appinfo-json)
- [Sample Apps](https://github.com/webOS-TV-app-samples)
