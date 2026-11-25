---
name: expo-setup
description: Sets up EAS Build, OTA updates, and app.json configuration for Expo projects
argument-hint: [platform: ios|android|all]
user-invocable: true
allowed-tools: Read Edit Bash
effort: medium
---

## Expo / EAS Setup

Platform: **$1** (ios | android | all - default: all)

1. Check current state:
```bash
cat app.json 2>/dev/null
cat eas.json 2>/dev/null
npx expo-env-info 2>/dev/null | head -10
```

2. Configure `app.json`:
   - `expo.name`, `expo.slug` set correctly?
   - iOS: `bundleIdentifier` set?
   - Android: `package` set?
   - `scheme` for deep links?
   - `icon` and `splash` configured?

3. Generate `eas.json` with 3 profiles:
```json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "channel": "preview"
    },
    "production": {
      "autoIncrement": true
    }
  }
}
```

4. Set up OTA updates config (expo-updates).

5. Generate GitHub Actions workflow for:
   - PR → build preview
   - Main push → production build

6. Document secrets needed in GitHub/EAS secrets.
