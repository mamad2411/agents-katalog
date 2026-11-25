---
name: godot-export-ci
description: Ship Godot 4.7 games - export presets and feature tags, .NET vs standard templates, headless CLI export with artifact checks, PCK/patches, Windows/macOS/Linux/Android/iOS/Web/server specifics, signing via env vars, shader baker, GitHub Actions CI. Use when exporting, packaging, signing or setting up CI builds.
license: MIT
compatibility: Godot 4.7+. Python 3.9+ for scripts/export.py.
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Export and CI (4.7)

**Run it:** `python scripts/export.py --list` shows presets plus whether templates are installed. `python scripts/export.py "Windows Desktop" [--debug|--pack|--patch] [--out path]` exports headless and verifies the file. C# projects get built by the export.

## Presets
- `export_presets.cfg` (commit it) holds the presets. **Secrets go to `.godot/export_credentials.cfg`** (never commit `.godot/`). Create presets in the editor (Project → Export). A preset written by hand needs `name`, `platform`, `runnable`, `export_filter`, `include_filter`, `exclude_filter`, `export_path` and a `[preset.N.options]` section.
- Options per platform are queryable: `api_lookup.py EditorExportPlatformWindows` lists every `codesign/*`, `application/*` and `binary_format/*` option with its default. The same works for `...Android`, `...Web`, `...MacOS`, `...LinuxBSD` and `...IOS`.
- Feature tags: platform (`windows`, `android`, `web`), `debug`/`release`, `dedicated_server`, plus custom tags per preset (`demo`, `steam`). Check them with `OS.has_feature("steam")`. Override project settings per tag (`setting.tag=value` in the editor's "Override for").
- Resources: export all, selected scenes or resources with filters, or "Dedicated Server" (strips textures and audio data). Exclude `test/`, `*.md` and dev tools with `exclude_filter`.
- **Shader baker** (4.5+): `shader_baker/enabled = true` per preset removes first-run shader hitches. It's slower to export.
- Version: `application/config/version` is used for file and store versions unless the preset overrides it.

## Templates
- They must match the editor exactly: `4.7.2.stable` for the standard editor, `4.7.2.stable.mono` for .NET. Location: Windows `%APPDATA%\Godot\export_templates\<ver>\`, Linux `~/.local/share/godot/export_templates/<ver>/`, macOS `~/Library/Application Support/Godot/export_templates/<ver>/`.
- The 4.7 editor can download templates per platform: Editor → Manage Export Templates. In CI, download `Godot_v4.7.2-stable[_mono]_export_templates.tpz` (a zip with `templates/`) from the GitHub release and unzip its contents into that folder.
- A .NET editor exports **only** with .NET templates, even for GDScript-only projects. `export.py` reports missing templates with the exact path.

## CLI
`godot --headless --path P --export-release "<preset>" build/game.exe` (also `--export-debug`, `--export-pack out.pck|.zip`, `--export-patch out.pck --patches base.pck`). Run `--import` first on fresh clones, which `export.py` does implicitly through the editor. The output folder must exist. Exit code 0 doesn't always mean success, so check that the artifact exists (`export.py` does).

## Platform notes
| Platform | Must know |
|---|---|
| Windows | `binary_format/embed_pck` gives a single exe. Editing icons and metadata needs no rcedit since 4.5. Code signing: `codesign/*` or env vars `GODOT_WINDOWS_CODESIGN_IDENTITY/_IDENTITY_TYPE/_PASSWORD`. Console wrapper exe for debug output. |
| macOS | Sign and notarize to avoid Gatekeeper blocks: env vars `GODOT_MACOS_CODESIGN_CERTIFICATE_FILE/_PASSWORD`, `GODOT_MACOS_NOTARIZATION_API_UUID/_API_KEY/_API_KEY_ID`. A universal binary is the default. |
| Linux | x86_64 and arm64 templates. Ship the `.pck` alongside, or embed it. Steam Runtime works fine. |
| Android | Set the Java SDK and Android SDK paths (Editor Settings). Keystores: `keystore/*`, or env vars `GODOT_ANDROID_KEYSTORE_RELEASE_PATH/_USER/_PASSWORD` (and `_DEBUG_*`). Gradle build (`gradle_build/use_gradle_build`) for plugins and AAB (`export_format`). C# requires net9.0 (the csproj condition). arm64-v8a only for modern stores. 4.7: GABE can build and publish from the Android editor. |
| iOS | Export produces an Xcode project; build and sign in Xcode. Needs macOS. C# is supported. |
| Web | **No C# in 4.x.** Use the Compatibility renderer. Threads need COOP/COEP headers (`variant/thread_support`, or a PWA with `progressive_web_app/ensure_cross_origin_isolation_headers`). Host over https, and expect audio to start after the first user input. |
| Server | Preset with "Dedicated Server" resources plus a `dedicated_server` feature tag. Run with `--headless`. |
Consoles need a licensed porting partner (W4 Games and others) or your own engine port. Steam: GodotSteam (GDExtension) and `steam_appid.txt` next to the exe during development only.

## Size and security
- Strip unused classes with a build profile (custom templates) only when you build engines. Usually it's enough to compress textures and exclude dev assets.
- PCK encryption needs custom-built templates with `GODOT_SCRIPT_ENCRYPTION_KEY`. It deters casual extraction and isn't DRM.

## CI
The workflow in [references/ci.md](references/ci.md) runs import, GDScript check, C# build, tests and exports on Linux runners, with templates cached. Keep the Godot version in one variable and pin it to the editor the team uses.
