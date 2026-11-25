---
name: electron-app-reverse-engineering
description: Bedah Electron apps into headless API maps.
tags: [reverse-engineering, electron, appimage, asar, api-extraction, farming]
version: 1.0
author: Me
license: MIT
---

# Electron App Reverse Engineering

## When to Use
Bedah an Electron desktop app to recover its backend API map, auth flow, and request headers — the goal is replicating the app's traffic headless (farming free-tier/promo resources that are "app-only"), NOT patching binaries. Typical triggers: a promo/plan is bound to the desktop app ("harus di aplikasi"), the web signup path is captcha-walled but the app talks to softer endpoints, or an OpenAI-compatible internal route is needed for a router/proxy.

## Procedure

### 1. Obtain the artifact
- Linux: `.AppImage` from the vendor CDN (`curl -sL -o app.AppImage <url>`). The in-app updater/telemetry URLs reveal the CDN pattern — grep the docs page or existing copy for `releases`.
- Windows: installed app dir `resources/app.asar` (usually `%LocalAppData%/Programs/<App>/`).
- macOS: `.dmg` → `hdiutil attach` → `<App>.app/Contents/Resources/app.asar`.

### 2. Extract the AppImage — self-extract only
```bash
chmod +x app.AppImage && ./app.AppImage --appimage-extract   # → squashfs-root/
```
- NEVER `unsquashfs` the carved payload and never trust `hsqs` magics found inside the file: modern AppImages pack non-standard squashfs, so manual `dd` carve yields a corrupted FS ("Can't find a valid SQUASHFS superblock", "read_id_table: failed"), and the ELF runtime stub contains decoy `hsqs` sequences. `--appimage-extract` is the only reliable route.
- If the stub refuses to run (FUSE/glibc mismatch), retry with `--appimage-extract-and-run` or inside a matching glibc container.

### 3. Unpack app.asar
```bash
npx @electron/asar extract squashfs-root/resources/app.asar app_extracted
```
- Big asars (300MB+) take minutes — run in background, verify `app_extracted/out/` exists before grepping.
- Layout: `out/main` (main proc), `out/renderer` (UI), `out/host` + `out/scheduler` (side services), `resources/config/` (provider configs / default.json). Grep `out/` first — `node_modules/` hits are vendor noise.

### 4. Map the backend (minified-chunk grep methodology)
```bash
cd app_extracted/out
grep -rhoE '"https?://[^"]+"' --include="*.js" . | sort -u          # all backend URLs
grep -rlE 'authorizeUrl|tokenUrl|redirectUri' --include='*.js' .   # auth provider defs
grep -rhoE '"X-[A-Za-z-]+"' --include="*.js" . | sort -u            # custom headers
grep -rhoE '[A-Z]{4,}_[A-Z_]+' --include="*.js" . | sort -u        # env-var config surface
```
- **Endpoint map**: builder functions return whole route tables — grep for `BaseUrl:` template keys (e.g. `zcodePlanOpenAiBaseUrl:`${o}/api/v1/zcode-plan``). One hit maps the entire backend.
- **Auth provider defs** are plain objects: `authorizeUrl`, `tokenUrl`, `userinfoUrl`, `appId`, `redirectUri` — client IDs are hardcoded in plain sight; grab them.
- **Custom-scheme redirect URIs** (`appname://oauth/callback`) are spoofable headless — intercept the final redirect instead of running the app.
- **Minified helper names** (`Vt`, `Wo`, `ba`) are import aliases: never chase `function Vt` definitions — they resolve to unrelated code. Trace them from call sites (`Vt(process.env,"/api/v1/...")`) and from const maps (`var Po="https://zcode.z.ai"`).
- **Zod schemas** embedded in chunks define request/response shapes — search by field names shown in the UI.

### 5. Replicate headless
- Verify each extracted endpoint with plain curl BEFORE wiring automation: an endpoint map is static fact from source, not a working flow.
- Claim/entitlement routes usually take the captcha token as a **HEADER** (`X-*-Captcha-Verify-Param`), not a body field; billing/preview routes often need only `Authorization` (JWT).
- Chat routes are usually OpenAI- or Anthropic-compatible with extra `X-*` headers — injectable straight into an OpenAI-compatible router once auth is minted.
- Keep request identity consistent with the app: copy its `User-Agent`, version header (`X-*-App-Version`), and `X-Platform`.

## Pitfalls
1. `unsquashfs`/manual `dd` carve on AppImage = dead end (non-standard packing + decoy magics in the stub) — `--appimage-extract` only.
2. Chasing minified function definitions = wasted hour — trace call sites and const maps instead.
3. Grepping the whole tree pulls vendor noise — scope to `out/` first.
4. An extracted API map is STATIC, unverified — curl-verify auth + claim E2E before calling a farm pipeline "proven".

## Supporting files
- `references/zcode-api-map.md` — full ZCode (Z.ai desktop) API/auth map: routes, client IDs, headers, env overrides, claim wiring.

## Related Skills
- app-account-farming — device spoofing for the signup side
- desktop-app-cracking — native PE license bypass (different toolstack, same class)
- frida-runtime-hooking — runtime hooking when static grep isn't enough

## Metadata (Hermes)
  hermes.tags: [reverse-engineering, electron, appimage, asar, api-extraction, farming]
  hermes.related_skills: [app-account-farming, desktop-app-cracking, frida-runtime-hooking]
