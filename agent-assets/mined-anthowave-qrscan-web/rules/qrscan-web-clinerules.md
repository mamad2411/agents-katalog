# qrscan-web — Memory Bank

## Overview
Privacy-first QR code scanner PWA. Decode QR codes from clipboard, image files, or camera — with blurred results requiring explicit user action to reveal. Built with React + Vite + html5-qrcode + vite-plugin-pwa.

## Tech Stack
- **React 19** with Vite 8 (HMR dev server on `:5173`)
- **html5-qrcode** npm package (v2.x, `import { Html5Qrcode } from 'html5-qrcode'`)
- **vite-plugin-pwa** — PWA with `display: standalone`, auto-update SW, Workbox
- Plain CSS (no framework), CSS variables for theming
- Build output: `dist/` (includes SW + manifest + PWA icons)

## Architecture
```
src/
├── App.jsx              → Tab layout (From Clipboard / Upload / Camera) with global document paste listener
├── App.css              → Layout, tabs, container styling
├── index.css            → CSS variables, global reset, dark theme
├── main.jsx             → ReactDOM.createRoot + PWA SW registration
└── components/
    ├── PasteScanner.jsx/css    → Clipboard-first: global paste listener, visibilitychange auto-read, click-to-read with permission prompt
    ├── UploadScanner.jsx/css   → File input + drag-drop, uses Html5Qrcode on #file-scanner-helper
    ├── CameraScanner.jsx/css   → Live camera via Html5Qrcode instance on #reader div
     └── ResultBox.jsx/css       → Shared result display with privacy toggle, clipboard expiry, and smart content-type insight pill
```

## Theme: Minimalist Swiss/Linear
- Pure black #000 background, #0d0d0d surface, subtle #1f1f1f borders
- Fonts: Inter (sans-serif UI), JetBrains Mono (decoded content)
- White accent buttons on black, secondary in grayscale

## Privacy Features
1. **Result content blurred by default** — filter: blur(6px), eye-off icon centered
2. **Click to toggle reveal/blur** — eye-off ↔ eye icons, re-blur on click
3. **Copy button always visible** — works even while blurred
4. **Clipboard auto-expiry** — clears clipboard after 2 minutes
5. **Pasted thumbnails blurred** — filter: blur(3px) + 60% opacity
6. **Smart content-type insight pill** — before reveal, shows what's detected (URL, TOTP, Wi-Fi, vCard, email, phone, JSON, hex, Base64, number, English text)

## Key Design Decisions
- Html5Qrcode needs a real DOM element ID (hidden #file-scanner-helper div in index.html)
- scanFile() is an instance method, NOT static — must call new Html5Qrcode('id') first
- Clipboard getAsFile() returns nameless Blob → wrap in new File([blob], 'screenshot.png', {type}) for format detection
- ResultBox resets revealed=false on new content via useEffect dependency on content
- Eye icon toggle uses position: absolute; inset: 0 overlay with pointer-events: none
- detectContentType() in ResultBox.jsx analyzes decoded text via regex heuristics and returns a human-readable label
- extractOtpSecret() in ResultBox.jsx parses the `secret` query param from otpauth://totp/ URLs; when detected, Copy button copies only the secret value and an "otp-hint" badge appears ("Copies SECRET only")
- Insight pill rendered inside result-header flex row, pushed right via margin-left: auto, hidden when content is revealed
- PWA `display: standalone` — opens in dedicated window, Alt+Tab-able like native app
- Global document paste listener in App.jsx — paste anywhere, not just inside paste zone
- visibilitychange auto-reads clipboard when returning to PWA (if clipboard-read permission granted)
- Click on paste zone triggers navigator.clipboard.read() directly — browser handles permission prompt via user gesture
- tryReadClipboard() helper encapsulates clipboard read logic, used by mount, visibilitychange, and click handlers
- clipboardPerm state tracks permission status ('granted' | 'prompt' | 'denied' | 'unknown') with UX hint in paste zone
- Initial clipboard read attempted on mount (fails silently if permission not granted — user can click to prompt)
- HandleClick focuses paste zone then calls tryReadClipboard() + re-checks permission state after 500ms
- decodeImage + processClipboardItem + tryReadClipboard + checkPermission declared as useCallback before useEffect hooks to avoid TDZ
- Responsive layout: `min(100%, 480px)` container, `clamp()` padding, `100dvh` body, edge-to-edge at ≤480px

## Git Conventions
- Conventional Commits: feat(scope):, fix(scope):, style(scope):, docs:, chore:
- Branch: main
- **Always commit and push after completing a task** — this is part of the definition of done. After any meaningful change, stage, commit with a conventional commit message, and push to origin/main.

## Documentation
- README.md is **UI/UX-focused** — describes features from the user's perspective, not code/tech details. Includes `screenshot.png`.
- Technical/architecture details live in this memory bank (`.clinerules`), not in the README.
- CONTRIBUTING.md — contributor setup + conventions, plus a "Using Cline" section (how to read/update the memory bank).
- ROADMAP.md — honest idea list + `good first issue` candidates.

## Open Source & Repo Health
- Repo: `anthowave/qrscan-web` (public, MIT — `LICENSE` file added).
- CI: `.github/workflows/ci.yml` runs `npm run lint` + `npm run build` on push to main and PRs.
- Issue template (`.github/ISSUE_TEMPLATE/bug_report.md`) and PR template (`.github/pull_request_template.md`).
- No test suite yet (only lint) — adding one is on the roadmap.

## Common Commands
```bash
npm run dev      # Start dev server at :5173
npm run build    # Production build to dist/
npx vite build   # Vite build (same as npm run build)
```

## Active State
- Dev server runs at http://localhost:5173 (via npm run dev)
- Vite HMR handles live reload