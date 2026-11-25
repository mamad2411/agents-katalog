---
name: kappmaker-app-icons
description: Generate platform app-icon sets for a KAppMaker app — iOS AppIcon.appiconset and Android launcher icons. Use when the user asks for app icons, launcher icons or adaptive icons.
---

# KAppMaker — App Icons

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions.


### generate-ios-icons — iOS AppIcon.appiconset Generator

**Syntax**: `kappmaker generate-ios-icons [--source <logo>] [--output <dir>] [--background <hex>]`

**Options**:
- `--source <path>` — Path to source logo PNG. **Default**: auto-detect in `Assets/` (`logo.png`, `logo_no_bg.png`, `app_logo.png`, `app_logo_no_bg.png`, `icon.png`). If none found, prompts interactively.
- `--output <dir>` — Output AppIcon.appiconset directory. **Default**: auto-detect `MobileApp/iosApp/*/Assets.xcassets/AppIcon.appiconset`.
- `--background <hex>` — Flatten color for transparent logos (App Store rejects icons with alpha). **Default**: `#FFFFFF`.

**Prerequisites**: None — sharp-only, no AI, no API keys.

**What it does**:
1. Loads the source logo (warns if smaller than 1024×1024 or non-square).
2. Center-crops to a square + flattens alpha onto the background color.
3. Resizes to all 11 unique pixel sizes Apple needs: 29, 40, 57, 58, 60, 80, 87, 114, 120, 180, 1024.
4. Writes `Contents.json` mapping each PNG to its idiom (`iphone` / `ios-marketing`) + scale (`1x` / `2x` / `3x`) — same schema appicon.co produces.
5. Overwrites existing files silently (you're regenerating from a new logo).

**Tips**: Run after `create-logo` to mint the full iconset in one shot. If your logo has transparency, the default `#FFFFFF` flatten matches Apple's App Store requirement; pass `--background "#000000"` (or any hex) for a dark fill.

---

### generate-android-icons — Android Launcher Icon Generator

**Syntax**: `kappmaker generate-android-icons [--source <logo>] [--output <res-dir>] [--background <hex>] [--foreground-padding <ratio>]`

**Options**:
- `--source <path>` — Path to source logo PNG. **Default**: auto-detect in `Assets/` (`logo.png`, `logo_no_bg.png`, `app_logo.png`, `app_logo_no_bg.png`, `icon.png`). If none found, prompts interactively.
- `--output <dir>` — Output Android `res/` directory. **Default**: auto-detect `MobileApp/composeApp/src/androidMain/res` (KAppMaker KMM convention) → `MobileApp/androidApp/src/main/res` → `app/src/main/res`.
- `--background <hex>` — Adaptive icon background color (referenced by the generated XML). **Default**: `#FFFFFF`.
- `--foreground-padding <ratio>` — Padding each side of the adaptive foreground (0 = no padding, 0.25 = Android Asset Studio default). **Default**: `0.25`.

**Prerequisites**: None — sharp-only, no AI, no API keys.

**What it does**:
1. Loads the source logo (warns if smaller than 432×432, the xxxhdpi foreground size; warns if non-square — center-crops).
2. For each of 5 density buckets (`mdpi`, `hdpi`, `xhdpi`, `xxhdpi`, `xxxhdpi`):
   - Writes `ic_launcher.webp` and `ic_launcher_round.webp` at the legacy launcher size (48 / 72 / 96 / 144 / 192 px).
   - Writes `ic_launcher_foreground.webp` at the adaptive size (108 / 162 / 216 / 324 / 432 px), with the logo centered in the inner safe zone and transparent surround.
3. Writes `mipmap-anydpi-v26/ic_launcher.xml` and `ic_launcher_round.xml` — adaptive-icon definitions referencing `@color/ic_launcher_background` and `@mipmap/ic_launcher_foreground`.
4. Upserts the `ic_launcher_background` color in `values/colors.xml` (creates the file if missing, updates the value if present, adds the entry if other colors exist).
5. Overwrites existing files silently.

**Tips**: Run after `create-logo` to mint the full Android iconset in one shot. The default `--foreground-padding 0.25` matches Android Asset Studio's behavior — drop it to `0.1` for icons that fill more of the adaptive frame, or up to `0.4` for very small logo content. Pass `--background "#0F0A0D"` (or any brand hex) to set the adaptive icon backdrop.

---

## Where this sits in the flow

- **Before this:** **kappmaker-logo** — icons are generated from the logo.
- **After this:** **kappmaker-publish** (icons must exist before a release build).
