---
name: apple-appstore-setup
description: Set up Apple Developer account, App Store Connect app listing, and EAS credentials for iOS builds and TestFlight distribution. Use when creating a new iOS app, configuring Apple certificates/provisioning, or troubleshooting App Store Connect submission issues.
---

# Apple App Store Setup

## Prerequisites

- Apple Developer Program membership ($99/year) at [developer.apple.com](https://developer.apple.com)
- Xcode installed (for Simulator; not required for EAS cloud builds)
- EAS CLI: `npm install -g eas-cli && eas login`

---

## Step 1: Configure App Identifier

1. Go to [developer.apple.com/account/resources/identifiers](https://developer.apple.com/account/resources/identifiers)
2. Click **+** → **App IDs** → **App**
3. Fill in:
   - **Description:** Your app name
   - **Bundle ID:** Explicit — `com.yourorg.appname` (must match `ios.bundleIdentifier` in `app.json`)
4. Enable capabilities you need: **Push Notifications**, **Sign in with Apple**, **Associated Domains** (deep links)
5. **Register**

Bundle ID in `app.json`:
```json
{
  "expo": {
    "ios": {
      "bundleIdentifier": "com.yourorg.appname"
    }
  }
}
```

---

## Step 2: Create App Store Connect Listing

1. Go to [appstoreconnect.apple.com](https://appstoreconnect.apple.com)
2. **My Apps** → **+** → **New App**
3. Fill in:
   - **Platform:** iOS
   - **Name:** Your app display name
   - **Primary Language:** English (or your language)
   - **Bundle ID:** Select the one you just registered
   - **SKU:** Unique internal identifier (e.g. `com-yourorg-appname`)
4. **Create**

Note the **App ID** (10-digit number) from the URL: `appstoreconnect.apple.com/apps/XXXXXXXXXX` — you need this for `eas.json`.

---

## Step 3: Configure EAS Credentials

EAS manages certificates and provisioning profiles in the cloud. Run once per app:

```bash
cd mobile
eas credentials --platform ios
```

Select: **production** → **Manage credentials** → let EAS generate certificates automatically.

**Then set up the App Store Connect API Key for submissions** (required for `eas submit` to work):

```bash
eas credentials --platform ios
```

Select: **production** → **App Store Connect: Manage your API Key** → **Set up your project to use an API Key for EAS Submit**

Follow the prompts — EAS will ask for your Key ID, Issuer ID, and `.p8` file. This is separate from build credentials and must be done before the first `eas submit`.

EAS stores everything encrypted on its servers — no local `.p12` files needed.

---

## Step 4: Configure eas.json

```json
{
  "cli": {
    "version": ">= 12.0.0",
    "appVersionSource": "remote"
  },
  "build": {
    "production": {
      "distribution": "store",
      "autoIncrement": true,
      "env": {
        "EXPO_PUBLIC_SUPABASE_URL": "https://xxx.supabase.co",
        "EXPO_PUBLIC_SUPABASE_PUBLISHABLE_KEY": "eyJ..."
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "ascAppId": "XXXXXXXXXX"
      }
    }
  }
}
```

`ascAppId` is the 10-digit App ID from App Store Connect.

---

## Step 5: App Store Connect API Key (for CI/CD)

Required for non-interactive submissions from GitHub Actions.

1. [appstoreconnect.apple.com/access/api](https://appstoreconnect.apple.com/access/api)
2. **Keys** → **+**
3. Name: `CI/CD`, Access: **App Manager**
4. Download the `.p8` file — **download once only**
5. Note the **Key ID** (10 chars) and **Issuer ID** (UUID at top of page)

Upload to EAS (run once):
```bash
eas secret:create --scope project --name APPLE_API_KEY_P8 --value "$(cat AuthKey_XXXXXXXXXX.p8 | base64)"
eas secret:create --scope project --name APPLE_API_KEY_ID --value "XXXXXXXXXX"
eas secret:create --scope project --name APPLE_API_KEY_ISSUER --value "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

Or add to GitHub Actions secrets (see `dev-to-prod.sh` output).

---

## Step 6: First Build and TestFlight

```bash
# Build (takes 10–20 min on EAS cloud)
cd mobile
eas build --platform ios --profile production

# Monitor build
eas build:list --platform ios

# Submit to TestFlight after build completes
eas submit --platform ios --profile production --latest
```

After submission, Apple processes the build for **10–15 minutes**, then it appears in TestFlight.

Add internal testers: App Store Connect → TestFlight → Internal Testing → Add testers.

---

## App Store Submission Checklist

Before submitting for App Review:

- [ ] App icon: 1024×1024 PNG, no transparency, no rounded corners (Apple rounds them)
- [ ] Screenshots: Required sizes — iPhone 6.7" (1290×2796), iPad 12.9" (2048×2732)
- [ ] Privacy Policy URL: **must be a publicly accessible URL** — Apple rejects apps where the URL requires login or returns 404
- [ ] App description, keywords, category filled in App Store Connect
- [ ] Age rating configured
- [ ] Camera/microphone/location usage: if your app requests any of these, **Privacy Policy URL is mandatory** — no exceptions
- [ ] `expo-tracking-transparency` installed if using PostHog/analytics (iOS 14.5+)
- [ ] Test on physical device, not just simulator

Generate screenshots with Maestro or manually in Simulator: `Device → Take Screenshot`.

---

## iOS vs Android: Key Difference

**iOS creates everything automatically** — EAS handles provisioning profiles, certificates, and push notification entitlements. You create the App Store Connect listing once and EAS does the rest. No manual cert management needed.

Android is the opposite: the first AAB upload must be done manually, service accounts must be created manually, and the Play Console listing has many required forms to fill before publishing.

---

## Gotchas

**"Missing compliance"** — Set `ITSAppUsesNonExemptEncryption = false` in `app.json` if your app doesn't use custom encryption (most apps):
```json
{ "expo": { "ios": { "infoPlist": { "ITSAppUsesNonExemptEncryption": false } } } }
```

**"Bundle ID already registered"** — Someone else (or a previous project) used that bundle ID. Choose a unique one.

**Build number conflict** — Always use `appVersionSource: "remote"` + `autoIncrement: true` to avoid this.

**TestFlight build missing after 15 min** — Check App Store Connect → Activity for processing errors. Usually a missing compliance declaration.

**"Invalid API key"** — The `.p8` file must be base64-encoded before storing as a secret. Verify with `echo $APPLE_API_KEY_P8 | base64 -d | head -1` — should show `-----BEGIN PRIVATE KEY-----`.

**Signing certificate expired** — Run `eas credentials --platform ios` and select "Remove" then re-generate. EAS handles this automatically.

**`eas submit` fails with "Set ascAppId in the submit profile"** — Add the 10-digit App ID to `eas.json`:
```json
{ "submit": { "production": { "ios": { "ascAppId": "6758882748" } } } }
```
Get it from the App Store Connect URL: `appstoreconnect.apple.com/apps/XXXXXXXXXX`.

**`eas submit` fails with "no API key configured"** — Run `eas credentials --platform ios` → production → **App Store Connect: Manage your API Key** and complete the setup. Build credentials and submit credentials are configured separately.
