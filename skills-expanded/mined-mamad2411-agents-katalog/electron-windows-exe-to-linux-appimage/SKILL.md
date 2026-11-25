---
name: electron-windows-exe-to-linux-appimage
description: Download a Windows Electron installer (.exe / Squirrel NUPKG), extract the app.asar and icons, repack into a Linux AppImage with launcher script, desktop entry, AppStream metadata, and optional update info for zsync delta updates.
category: appimage
version: 1.0.0
tags: [appimage, electron, packaging, linux, appdir, appimagetool, squirrel]
source_type: extracted-from-git
source_url: https://github.com/aaddrick/claude-desktop-debian.git
source_ref: main
source_commit: 2fd9faf9db4eaa409b88310bdce397f8bdb0e916
source_project: claude-desktop-debian
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

# Electron Windows EXE to Linux AppImage

## When to use

Use this pattern when:
- You have a Squirrel-packaged Windows `.exe` (which contains a `.nupkg`) and want to produce a Linux AppImage.
- No Linux binary is officially provided but the app is pure Electron (i.e., the `.asar` and `app.asar.unpacked` are platform-agnostic JS/assets).
- You want a self-contained portable binary that runs on any modern Linux distribution without installation.

## Pattern

### Stage 1: Extract the Windows installer

```
.exe → 7z extract → claude.nupkg → 7z extract → lib/net45/resources/
  ├── app.asar
  ├── app.asar.unpacked/
  └── *.png  (icons)
```

### Stage 2: Assemble AppDir

```
AppDir/
  ├── AppRun              (executable bash launcher)
  ├── app-id.desktop      (XDG desktop entry)
  ├── app-id.png          (256x256 icon)
  ├── .DirIcon            (copy of icon, for some tools)
  └── usr/
        ├── bin/
        ├── lib/
        │   ├── node_modules/electron/dist/  (bundled Electron)
        │   │   └── resources/
        │   │         ├── app.asar
        │   │         └── app.asar.unpacked/
        │   └── app-name/
        │         └── launcher-common.sh
        ├── share/
        │   ├── applications/app-id.desktop
        │   ├── icons/hicolor/256x256/apps/app-id.png
        │   └── metainfo/app-id.appdata.xml
```

### Stage 3: Invoke appimagetool

```bash
ARCH=x86_64 appimagetool [--updateinformation "..."] AppDir output.AppImage
```

## Minimal example

```bash
#!/usr/bin/env bash
version="$1"          # e.g. 1.0.1234
architecture="$2"     # amd64 or arm64
work_dir="$3"
app_staging_dir="$4"  # contains: node_modules/, app.asar, app.asar.unpacked/
package_name="$5"     # e.g. my-electron-app
component_id="io.github.myorg.${package_name}"

appdir="$work_dir/${component_id}.AppDir"
rm -rf "$appdir"
mkdir -p "$appdir/usr/bin" \
         "$appdir/usr/lib" \
         "$appdir/usr/share/icons/hicolor/256x256/apps" \
         "$appdir/usr/share/applications" \
         "$appdir/usr/lib/$package_name"

# Stage app into Electron's resources dir (matches process.resourcesPath)
resources_dir="$appdir/usr/lib/node_modules/electron/dist/resources"
mkdir -p "$resources_dir"
cp -a "$app_staging_dir/node_modules" "$appdir/usr/lib/"
cp -a "$app_staging_dir/app.asar" "$resources_dir/"
cp -a "$app_staging_dir/app.asar.unpacked" "$resources_dir/"

# Copy shared launcher library
cp scripts/launcher-common.sh "$appdir/usr/lib/$package_name/"

# AppRun launcher
cat > "$appdir/AppRun" << 'EOF'
#!/usr/bin/env bash
appdir=$(dirname "$(readlink -f "$0")")
source "$appdir/usr/lib/my-electron-app/launcher-common.sh"
setup_logging || exit 1
setup_electron_env
cleanup_stale_lock
detect_display_backend
electron_exec="$appdir/usr/lib/node_modules/electron/dist/electron"
app_path="$appdir/usr/lib/node_modules/electron/dist/resources/app.asar"
build_electron_args 'appimage'
electron_args+=("$app_path")
cd "$HOME" || exit 1
exec "$electron_exec" "${electron_args[@]}" "$@" >> "$log_file" 2>&1
EOF
chmod +x "$appdir/AppRun"

# Desktop entry
cat > "$appdir/${component_id}.desktop" << EOF
[Desktop Entry]
Name=My Electron App
Exec=AppRun %u
Icon=$component_id
Type=Application
Terminal=false
Categories=Network;Utility;
MimeType=x-scheme-handler/myapp;
StartupWMClass=MyElectronApp
X-AppImage-Version=$version
EOF
mkdir -p "$appdir/usr/share/applications"
cp "$appdir/${component_id}.desktop" "$appdir/usr/share/applications/"

# Icons
icon_src="$work_dir/icon-256x256.png"
cp "$icon_src" "$appdir/usr/share/icons/hicolor/256x256/apps/${component_id}.png"
cp "$icon_src" "$appdir/${component_id}.png"
cp "$icon_src" "$appdir/.DirIcon"

# AppStream metadata (required to suppress appimagetool warnings)
mkdir -p "$appdir/usr/share/metainfo"
cat > "$appdir/usr/share/metainfo/${component_id}.appdata.xml" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>$component_id</id>
  <metadata_license>CC0-1.0</metadata_license>
  <project_license>Proprietary</project_license>
  <name>My Electron App</name>
  <summary>My app for Linux</summary>
  <description><p>My app.</p></description>
  <launchable type="desktop-id">${component_id}.desktop</launchable>
  <releases><release version="$version" date="$(date +%Y-%m-%d)"/></releases>
  <content_rating type="oars-1.1"/>
</component>
EOF

# Get or download appimagetool
case "$architecture" in
    amd64) tool_arch='x86_64' ;;
    arm64) tool_arch='aarch64' ;;
esac
if ! command -v appimagetool &>/dev/null; then
    appimagetool_path="$work_dir/appimagetool-${tool_arch}.AppImage"
    wget -q -O "$appimagetool_path" \
        "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-${tool_arch}.AppImage"
    chmod +x "$appimagetool_path"
else
    appimagetool_path=$(command -v appimagetool)
fi

output="$work_dir/${package_name}-${version}-${architecture}.AppImage"
export ARCH="$tool_arch"
"$appimagetool_path" "$appdir" "$output"
```

## Why this works

### app.asar in Electron's resources dir

Electron resolves `process.resourcesPath` to the directory containing `app.asar`. In an AppImage, bundling Electron under `usr/lib/node_modules/electron/dist/` and placing `app.asar` in its `resources/` subdirectory mirrors the layout of an installed Electron app. The app code can then call `path.join(process.resourcesPath, 'my-resource')` and find files correctly.

### AppRun uses `readlink -f "$0"` to find APPDIR

When AppImageKit mounts the AppImage, `$0` inside `AppRun` is the path to the `AppRun` file itself. `dirname "$(readlink -f "$0")"` resolves symlinks and gives the absolute AppDir mount path. Storing it as `appdir` lets the rest of the launcher construct absolute paths. Do not rely on `$APPDIR` — it is set by some runtimes but not all.

### `--no-sandbox` for AppImage

AppImages mount via FUSE. FUSE mounts do not support the setuid bit required by Chromium's sandbox helper (`chrome-sandbox`). `--no-sandbox` must always be passed to Electron when running from an AppImage. This is not optional.

### AppStream metadata prevents appimagetool warnings

`appimagetool` looks for an `appdata.xml` in `usr/share/metainfo/` and will warn (not fail) if it's missing. Including a minimal but valid AppStream file silences the warning and enables software center discovery.

### zsync for delta updates (CI only)

The `--updateinformation` flag embeds a URL pattern that AppImage update tools use to find `.zsync` delta files. Only embed this in CI/release builds where you know the final download URL pattern. For local builds, omit it.

## Pitfalls

- **`ARCH` env var must match the electron binary's arch, not the system's** — appimagetool reads `$ARCH` to determine the ELF type to embed in the AppImage. Set it explicitly: `export ARCH=x86_64` or `aarch64`.
- **Top-level icon filename must match the `Icon=` field in the `.desktop`** — appimagetool reads the `.desktop` Icon field and looks for a matching file at the AppDir root. The name (without extension) must exactly match.
- **`app.asar.unpacked/` must travel alongside `app.asar`** — native addon `.node` files and other unpacked assets live in `app.asar.unpacked/`. If you copy only `app.asar`, native modules will fail to load at runtime.
- **Electron binary must be in the AppDir, not symlinked** — AppImages are self-contained. If Electron is symlinked to a system path, the AppImage will fail on a system without Electron installed. Bundle the full `electron/dist/` directory.
- **`cd "$HOME"` before exec** — Electron can behave unpredictably if the CWD does not exist or is inside the read-only AppImage mount. Always `cd "$HOME"` before exec-ing Electron.

## Source reference

`scripts/build-appimage.sh` — full AppDir construction, AppRun generation, metadata, icon copy, and appimagetool invocation
