---
name: native-installers
description: >
  Extends agent's knowledge of customizing platform-specific native
  installers (deb/msi/dmg) for Java POS applications. Use when branding,
  signing, or post-install configuring packaged JavaFX installers.
compatibility: Java 21+
metadata:
  domain: packaging
  level: advanced
  stack: [java-21, jpackage, wix, dpkg, maven-3.9]
  version: "1.0.0"
---

# Native Installers

Beyond basic `jpackage`, each platform has specific customizations:
license files, desktop shortcuts, file associations, signing, and
post-install hooks. POS apps need branded installers that configure
the POS terminal on first launch.

## Concepts

- **`.wix` / WiX** — Windows MSI custom actions (service install, file
  associations).
- **`dpkg-deb` / `debhelper`** — Linux `.deb` maintainer scripts
  (`postinst`, `prerm`).
- **`pkgbuild` / `productbuild`** — macOS `.pkg` and `.dmg` creation.
- **Code signing** — Authenticode (Windows), Apple `codesign` + notarization (macOS),
   GPG (Linux) to avoid OS warning dialogs.

## Rules

1. Bundle a JRE via `jlink` runtime image — never depend on system JRE
   in native installers.
2. Include `postinst` on Linux to create symlink in `/usr/local/bin` and
   register `.desktop` file.
3. Sign Windows MSIs with Authenticode or users see "Unknown publisher".
4. Store installer version in the filename: `pos-installer-1.0.0.msi`.
5. Test install, upgrade, and uninstall on each target OS in CI.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- jpackage-basics — base jpackage configuration
- shading-and-packaging — uber-jar fallback for non-modular apps
