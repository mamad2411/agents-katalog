---
name: deb-package-from-electron-with-icons
description: Build a .deb package for a Linux Electron app with a full hicolor icon tree (16/24/32/48/64/256), a sourced launcher script, .desktop entry with MIME handler, and a postinst that sets chrome-sandbox setuid permissions.
category: deb
version: 1.0.0
tags: [deb, debian, packaging, electron, icons, hicolor, desktop-entry, postinst]
source_type: extracted-from-git
source_url: https://github.com/aaddrick/claude-desktop-debian.git
source_ref: main
source_commit: 2fd9faf9db4eaa409b88310bdce397f8bdb0e916
source_project: claude-desktop-debian
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

# Debian Package from Electron App with Icons

## When to use

Use this pattern when:
- You are creating a `.deb` package for an Electron application on Debian/Ubuntu.
- You have PNG icons extracted from the application at multiple sizes.
- You want proper system integration: hicolor icon theme, `.desktop` entry, MIME handler registration, and chrome-sandbox permissions.
- You are building the package from a script (no `dh`/`debhelper`) using `dpkg-deb --build`.

## Pattern

### Directory layout

```
package/
  DEBIAN/
    control        (package metadata: name, version, arch, maintainer)
    postinst       (sets chrome-sandbox perms; updates desktop DB)
  usr/
    bin/
      app-name     (launcher script)
    lib/
      app-name/
        node_modules/electron/dist/  (bundled electron + chrome-sandbox)
          resources/
            app.asar
            app.asar.unpacked/
        launcher-common.sh           (shared launcher library)
    share/
      applications/
        app-name.desktop
      icons/hicolor/
        16x16/apps/app-name.png
        24x24/apps/app-name.png
        32x32/apps/app-name.png
        48x48/apps/app-name.png
        64x64/apps/app-name.png
        256x256/apps/app-name.png
```

### Key constraints

- `DEBIAN/` directory permissions must be exactly `755` or `dpkg-deb` will reject the package.
- Scripts in `DEBIAN/` must have execute permission (`755`).
- `chrome-sandbox` must be owned by root and have setuid bit (`4755`) — this is done in `postinst`, not at package build time.
- The `control` file must not declare runtime deps on `nodejs`, `npm`, or `p7zip` — those are build-time only. Electron bundles its own Node runtime.

## Minimal example

```bash
#!/usr/bin/env bash
version="$1"; architecture="$2"; work_dir="$3"
app_staging_dir="$4"; package_name="$5"
maintainer="$6"; description="$7"

package_root="$work_dir/package"
install_dir="$package_root/usr"
rm -rf "$package_root"

# Create structure
mkdir -p "$package_root/DEBIAN" \
         "$install_dir/lib/$package_name" \
         "$install_dir/share/applications" \
         "$install_dir/bin"

# --- Icons (hicolor tree) ---
declare -A icon_files=([16]=file_index_for_16 [24]=file_index_for_24 \
    [32]=file_index_for_32 [48]=file_index_for_48 \
    [64]=file_index_for_64 [256]=file_index_for_256)

for size in "${!icon_files[@]}"; do
    icon_dir="$install_dir/share/icons/hicolor/${size}x${size}/apps"
    mkdir -p "$icon_dir"
    # icon files named like: app_INDEX_SIZExSIZEx32.png
    icon_src="$work_dir/app_${icon_files[$size]}_${size}x${size}x32.png"
    [[ -f $icon_src ]] && install -Dm 644 "$icon_src" "$icon_dir/$package_name.png"
done

# --- App files ---
cp -r "$app_staging_dir/node_modules" "$install_dir/lib/$package_name/"
resources_dir="$install_dir/lib/$package_name/node_modules/electron/dist/resources"
mkdir -p "$resources_dir"
cp "$app_staging_dir/app.asar" "$resources_dir/"
cp -r "$app_staging_dir/app.asar.unpacked" "$resources_dir/"
cp scripts/launcher-common.sh "$install_dir/lib/$package_name/"

# --- Desktop entry ---
cat > "$install_dir/share/applications/$package_name.desktop" << EOF
[Desktop Entry]
Name=My App
Exec=/usr/bin/$package_name %u
Icon=$package_name
Type=Application
Terminal=false
Categories=Office;Utility;
MimeType=x-scheme-handler/myapp;
StartupWMClass=MyApp
EOF

# --- Launcher script ---
cat > "$install_dir/bin/$package_name" << LAUNCHER
#!/usr/bin/env bash
source "/usr/lib/$package_name/launcher-common.sh"
setup_logging || exit 1
setup_electron_env
cleanup_stale_lock
detect_display_backend
electron_exec="/usr/lib/$package_name/node_modules/electron/dist/electron"
app_path="/usr/lib/$package_name/node_modules/electron/dist/resources/app.asar"
build_electron_args 'deb'
electron_args+=("\$app_path")
cd "/usr/lib/$package_name" || exit 1
"\$electron_exec" "\${electron_args[@]}" "\$@"
LAUNCHER
chmod +x "$install_dir/bin/$package_name"

# --- Control file ---
# No runtime deps: Electron bundles its own Node.js
cat > "$package_root/DEBIAN/control" << EOF
Package: $package_name
Version: $version
Section: utils
Priority: optional
Architecture: $architecture
Maintainer: $maintainer
Description: $description
 My electron application.
EOF

# --- postinst: set chrome-sandbox setuid ---
cat > "$package_root/DEBIAN/postinst" << 'EOF'
#!/bin/sh
set -e
update-desktop-database /usr/share/applications >/dev/null 2>&1 || true
SANDBOX="/usr/lib/PKGNAME/node_modules/electron/dist/chrome-sandbox"
if [ -f "$SANDBOX" ]; then
    chown root:root "$SANDBOX" || true
    chmod 4755 "$SANDBOX" || true
fi
EOF
# Substitute PKGNAME
sed -i "s|PKGNAME|$package_name|g" "$package_root/DEBIAN/postinst"
chmod 755 "$package_root/DEBIAN/postinst"

# --- Build .deb ---
chmod 755 "$package_root/DEBIAN"
deb_file="$work_dir/${package_name}_${version}_${architecture}.deb"
dpkg-deb --build "$package_root" "$deb_file"
echo "Built: $deb_file"
```

## Why this works

### Hicolor icon tree at multiple sizes

The XDG icon specification requires applications to provide icons in the standard hicolor theme at multiple sizes. Desktop environments choose the best size for each context (application launcher, taskbar, file manager). Providing only a 256x256 icon causes blurry rendering at small sizes because the DE scales down without a native small icon. The standard sizes are 16, 24, 32, 48, 64, and 256.

### `install -Dm 644` vs `cp`

`install -Dm 644 src dst` creates all parent directories and sets the exact file permissions in one command. Using `cp` requires a separate `chmod`. The `-m 644` flag ensures icons are world-readable but not executable, which is required for correct dpkg permission audits.

### `DEBIAN/` permissions must be `755`

`dpkg-deb` validates directory permissions. If `DEBIAN/` is `700` or `777`, the build fails with "control directory has bad permissions". Always set `chmod 755 "$package_root/DEBIAN"` before calling `dpkg-deb`.

### `postinst` for chrome-sandbox setuid

`dpkg-deb --build` cannot set setuid bits (they would require root to set and the build runs as a non-root user). The `postinst` script runs as root during package installation and can set `chown root:root` and `chmod 4755` on the sandbox binary. Without the setuid bit, Chromium processes crash at startup.

### No nodejs/npm runtime dependency

Electron bundles its own Node.js runtime inside the `dist/` directory. Declaring `Depends: nodejs` would install a system Node.js that is never used by the app and could cause confusion. The control file should have no runtime dependencies beyond standard libraries already guaranteed by the base system.

### `update-desktop-database` in postinst

MIME type associations from the `.desktop` file's `MimeType=` field are only activated after `update-desktop-database` runs. Without it, the `x-scheme-handler/myapp` deep link registration does not work immediately after installation.

## Pitfalls

- **`app.asar.unpacked/` must be in the same directory as `app.asar`** — Electron looks for unpacked files relative to `app.asar`. If the directory is missing, native modules fail silently or with cryptic errors.
- **Launcher must `cd` to the app directory before exec** — some Electron apps resolve resources relative to `process.cwd()`. Running from `/` or `/tmp` causes ENOENT on relative paths. `cd "/usr/lib/$package_name"` before exec is the safe default.
- **Embedded launchers from heredoc need `\$` for literal `$`** — inside a heredoc with unquoted delimiter (`<< EOF`), variable expansions happen. If the launcher script needs literal `$@` or `$?`, escape them as `\$@` or use a quoted delimiter (`<< 'LAUNCHER'`).
- **`chmod 4755` on chrome-sandbox requires root** — do not attempt this in the build script; only in postinst. Running as a non-root build user will silently fail or produce a package that requires root to fix after installation.
- **Version string format** — Debian version strings follow the `[epoch:]upstream-revision` format. Hyphens are allowed (they separate the upstream version from the Debian revision). `dpkg` parses versions semantically; do not embed build metadata in the version string.

## Source reference

`scripts/build-deb-package.sh` — full implementation
