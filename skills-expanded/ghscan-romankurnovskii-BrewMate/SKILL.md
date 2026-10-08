---
name: app-store-deploy
description: Automates the build and deployment of the Electron app to the Mac App Store and TestFlight.
---

# Skill: App Store Deployment

This skill automates the versioning, building, and uploading of the BrewMate application to TestFlight / Mac App Store. It ensures that the app is properly signed and distributed using the correct Mac App Store (MAS) provisioning profiles and developer certificates.

## Prerequisites

- **macOS Environment**: The deployment must be run on a Mac with Xcode command-line tools installed.
- **Developer Certificates**: Ensure "3rd Party Mac Developer Application" and "3rd Party Mac Developer Installer" certificates are in your System Keychain.
- **Provisioning Profile**: A valid profile must be present at `.credentials/BrewMate_Distribution.provisionprofile`.
- **Environment Variables**: A `.env` file must contain:
  - `APPLE_ID`: Your Apple Developer email.
  - `APPLE_APP_SPECIFIC_PASSWORD`: An app-specific password generated from [appleid.apple.com](https://appleid.apple.com).
- **Tooling**: `jq` must be installed for version management.

## Automated Workflow

The easiest way to deploy is using the provided script:

```bash
# Deploys with automatic patch version increment (1.0.x -> 1.0.x+1)
./.agents/skills/app-store-deploy/scripts/deploy.sh

# Deploys with a specific version
./.agents/skills/app-store-deploy/scripts/deploy.sh 1.0.15
```

### What the script does:

1. **Loads credentials** from `.env`.
2. **Determines target version** (either auto-increments current patch version or uses specified parameter).
3. **Runs MAS Universal Build**: Executes the project's native build script `./scripts/build-mas-universal.sh` (or `npm run build:mas`) which compiles TypeScript, sets up code-signing with your 3rd Party Mac Developer certificates, and packages a signed `.pkg` file.
4. **Uploads to TestFlight**: Submits the generated bundle to App Store Connect using `xcrun altool --upload-app`.

## Manual Deployment Steps

If you need to perform steps manually:

### 1. Build for MAS

Run the following command to generate a signed `.pkg` file under `dist-app/`:

```bash
npm run build:mas
```

### 2. Upload to TestFlight

Use `altool` to upload the generated package:

```bash
xcrun altool --upload-app --type macos --file "dist-app/mas-universal/BrewMate-[version]-universal.pkg" --username "$APPLE_ID" --password "$APPLE_APP_SPECIFIC_PASSWORD"
```

Alternatively, you can open the generated package in the macOS Transporter application for a visual upload:

```bash
npm run submit:mas
```

## Troubleshooting

- **Signing Errors**: Ensure your Keychain is unlocked. Run `security unlock-keychain` if necessary.
- **Validation Errors (409)**: Usually due to a version conflict in App Store Connect. Ensure you have bumped the version or build number.
- **Architecture Mismatch**: Ensure you are using the `--universal` flag (automatically handled by the build-mas script).

## Success Checklist

- [ ] Version bumped in `package.json`.
- [ ] Universal binary built and signed successfully.
- [ ] `.pkg` file generated in `dist-app/mas-universal/`.
- [ ] Upload to TestFlight/App Store Connect completed successfully.
- [ ] Changes committed to the repository.
