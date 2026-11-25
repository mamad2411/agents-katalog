---
name: release-packaging
description: Package, release, and update desktop and web applications: Electron/Tauri builds, installers, auto-update, code signing, web builds, environment config, versioning, release notes, rollback, and distribution checks. Use with ship-pro for release readiness.
---

# Release Packaging

## Workflow

1. Identify target platforms, build commands, signing requirements, updater, and distribution channel.
2. Separate build-time config, runtime config, and secrets.
3. Verify versioning, artifact naming, installer behavior, and update metadata.
4. For desktop apps, check code signing, notarization where relevant, auto-update, native permissions, and startup after install.
5. For web apps, check build output, cache headers, environment variables, CDN/deploy behavior, and rollback path.
6. Update release docs, changelog, and packaging notes when behavior changes.

## Required Checks

- Do not embed production secrets in client artifacts.
- Keep release artifacts reproducible enough to debug.
- Verify startup after install/update.
- Document rollback or previous-version recovery.
- Keep changelog or release notes tied to actual changes.
- Confirm migrations or config changes are compatible with rollback.

## Desktop Checklist

- App name, bundle identifier, icons, and version are correct.
- Installer/package opens and launches.
- Auto-update config is correct when used.
- Signing/notarization requirements are known.
- Platform-specific permissions are documented.

## Web/API Checklist

- Environment variables are documented.
- Static assets and cache behavior are understood.
- API compatibility risks are documented.
- Monitoring or error visibility exists for release validation.

## Output

State artifacts produced, config assumptions, verification commands, release risk, and rollback note.
