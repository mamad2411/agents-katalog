---
name: social-auth-setup
description: Configure Sign in with Apple and Sign in with Google for Supabase Auth. Use when adding social login, troubleshooting OAuth redirects, setting up Apple Services ID, Google OAuth credentials, or linking Google Play Console to Google Cloud.
---

# Social Auth Setup (Apple + Google)

## Overview

Both providers require setup in **three places**:
1. The provider's developer console (Apple Developer Portal / Google Cloud Console)
2. Supabase Auth settings
3. Mobile app (`app.json` + Expo config)

---

## Sign in with Apple

### Step 1: Enable Sign in with Apple on the App ID

1. [developer.apple.com/account/resources/identifiers](https://developer.apple.com/account/resources/identifiers)
2. Click your App ID (the one matching your `ios.bundleIdentifier`)
3. Scroll to **Sign in with Apple** → Enable → **Edit**
4. Leave as "Enable as a primary App ID" → **Save**

### Step 2: Create a Services ID (for web/Supabase callback)

This is separate from your App ID — it's used for the OAuth redirect flow.

1. Identifiers → **+** → **Services IDs** → Continue
2. Description: `Your App Name Sign In`
3. Identifier: `com.yourorg.appname.siwa` (convention: bundle ID + `.siwa`)
4. **Register**
5. Click the new Services ID → Enable **Sign in with Apple** → **Configure**
6. Add your Supabase callback URL:
   - Primary App ID: select your app
   - Domains: `YOUR_PROJECT.supabase.co`
   - Return URLs: `https://YOUR_PROJECT.supabase.co/auth/v1/callback`
7. **Save** → **Continue** → **Register**

### Step 3: Create a Private Key

1. [developer.apple.com/account/resources/authkeys](https://developer.apple.com/account/resources/authkeys) → **+**
2. Name: `Sign in with Apple - Your App`
3. Enable **Sign in with Apple** → Configure → select your App ID
4. **Continue** → **Register**
5. Download the `.p8` file — **one-time download, save it**
6. Note the **Key ID** (10 chars)

### Step 4: Configure Supabase

1. Supabase Dashboard → **Authentication** → **Providers** → **Apple**
2. Fill in:
   - **Service ID:** the Services ID from Step 2 (e.g. `com.yourorg.appname.siwa`)
   - **Team ID:** your 10-char Apple Team ID (top-right of developer.apple.com)
   - **Key ID:** from the key you downloaded
   - **Private Key:** paste the full contents of the `.p8` file
3. **Save**

### Step 5: Mobile app config

```bash
npx expo install expo-apple-authentication
```

`app.json`:
```json
{
  "expo": {
    "ios": {
      "usesAppleSignIn": true
    },
    "plugins": ["expo-apple-authentication"]
  }
}
```

Usage:
```typescript
import * as AppleAuthentication from "expo-apple-authentication";
import { supabase } from "@/lib/supabase";

const credential = await AppleAuthentication.signInAsync({
  requestedScopes: [
    AppleAuthentication.AppleAuthenticationScope.FULL_NAME,
    AppleAuthentication.AppleAuthenticationScope.EMAIL,
  ],
});

await supabase.auth.signInWithIdToken({
  provider: "apple",
  token: credential.identityToken!,
});
```

**Note:** Apple only returns the user's name and email on the **first sign-in**. Store them immediately in your DB — they won't come back on subsequent logins.

---

## Sign in with Google

### The Google Infrastructure Confusion

Google has two overlapping systems that share the same console:

| Thing | Where | Purpose |
|---|---|---|
| **OAuth Client ID** | Google Cloud Console → APIs & Services → Credentials | Sign in with Google |
| **Service Account** | Google Cloud Console → IAM & Admin | Play Console API (EAS Submit) |
| **Play Console API link** | Play Console → Setup → API access | Connects Play Console to a Cloud project |

**These must all be in the same Google Cloud Project.** If your Play Console is linked to Project A but your OAuth credentials are in Project B, social login and Play submissions won't share the project and you'll have permission confusion.

**Set up the Cloud project link first, before creating any credentials.**

### Step 1: Link Google Play Console to Google Cloud (do this first)

1. [play.google.com/console](https://play.google.com/console) → **Setup** → **API access**
2. Click **Link to a Google Cloud Project**
   - If you have an existing project: link to it
   - If not: create a new project here
3. This link is **permanent and one-way** — you cannot unlink or change it later
4. After linking, all service accounts for Play Console must be created in this project

### Step 2: Enable Google Sign-In API

In the linked Google Cloud project:

1. [console.cloud.google.com](https://console.cloud.google.com) → select your project
2. **APIs & Services** → **Library**
3. Search "Google Identity" → **Google Identity Toolkit API** → **Enable**

### Step 3: Configure OAuth Consent Screen

1. **APIs & Services** → **OAuth consent screen**
2. User type: **External** (unless you're a Google Workspace org)
3. Fill in:
   - App name, support email, developer email
   - **Authorized domains:** `supabase.co` and your production domain
4. Scopes: add `email` and `profile`
5. Save and continue through all steps

### Step 4: Create OAuth Client ID

1. **APIs & Services** → **Credentials** → **Create Credentials** → **OAuth client ID**
2. For **web** (Supabase callback):
   - Application type: **Web application**
   - Authorized redirect URIs: `https://YOUR_PROJECT.supabase.co/auth/v1/callback`
   - **Create** → copy **Client ID** and **Client Secret**
3. For **Android** (native sign-in):
   - Application type: **Android**
   - Package name: your `android.package` from `app.json`
   - SHA-1 certificate fingerprint (get from EAS): `eas credentials --platform android`
4. For **iOS** (native sign-in):
   - Application type: **iOS**
   - Bundle ID: your `ios.bundleIdentifier` from `app.json`

### Step 5: Configure Supabase

1. Supabase Dashboard → **Authentication** → **Providers** → **Google**
2. **Client ID:** the web OAuth client ID
3. **Client Secret:** the web OAuth client secret
4. **Save**

### Step 6: Mobile app config

```bash
npx expo install @react-native-google-signin/google-signin
```

`app.json` — add the iOS client ID from Step 4:
```json
{
  "expo": {
    "plugins": [
      ["@react-native-google-signin/google-signin", {
        "iosUrlScheme": "com.googleusercontent.apps.YOUR_IOS_CLIENT_ID"
      }]
    ]
  }
}
```

Usage:
```typescript
import { GoogleSignin } from "@react-native-google-signin/google-signin";
import { supabase } from "@/lib/supabase";

GoogleSignin.configure({
  webClientId: "YOUR_WEB_CLIENT_ID.apps.googleusercontent.com",
  iosClientId: "YOUR_IOS_CLIENT_ID.apps.googleusercontent.com",
});

const { idToken } = await GoogleSignin.signIn();

await supabase.auth.signInWithIdToken({
  provider: "google",
  token: idToken!,
});
```

---

## Supabase Redirect URLs

For both providers, add your app's deep link scheme to Supabase allowed redirect URLs:

1. Supabase Dashboard → **Authentication** → **URL Configuration**
2. Add to **Redirect URLs**:
   - `https://yourapp.com` (production web)
   - `yourapp://` (mobile deep link — must match `scheme` in `app.json`)
   - `http://localhost:3000` (local development)

`app.json`:
```json
{
  "expo": {
    "scheme": "yourapp"
  }
}
```

---

## Gotchas

**Apple login works on simulator but not on device** — Sign in with Apple requires a real device. It will always fail on simulator. Test on physical hardware before debugging further.

**Apple only sends name/email once** — On every subsequent sign-in, `credential.fullName` and `credential.email` are null. Save them to your DB on first sign-in:
```typescript
if (credential.fullName?.givenName) {
  await supabase.from("profiles").upsert({ id: userId, name: credential.fullName.givenName });
}
```

**Google sign-in fails: "Sign in is currently unavailable"** — OAuth consent screen is in "Testing" mode and your email isn't added as a test user. Either add the email in Cloud Console → OAuth consent screen → Test users, or publish the consent screen.

**Google Play Console API link: "SA not found"** — The service account must exist in the same Google Cloud project that Play Console is linked to. If you created it in a different project, it won't appear. Create a new service account in the correct linked project.

**`DEVELOPER_ERROR` on Android** — SHA-1 fingerprint mismatch. The Android OAuth client ID was created with a different SHA-1 than the one EAS uses. Run `eas credentials --platform android` to get the current SHA-1, then update the Android OAuth client in Google Cloud Console.

**Supabase callback URL rejected by Apple** — The return URL must exactly match what's in the Services ID configuration, including `https://` and no trailing slash. Re-check: `https://YOUR_PROJECT.supabase.co/auth/v1/callback`.

**Google OAuth works on web but not mobile** — Mobile uses the native client IDs (Android/iOS), not the web client ID. Make sure you created separate OAuth client entries for Android and iOS in Google Cloud Console and configured them in the app.

**Play Console linked to wrong Google Cloud project** — This cannot be undone. If you linked to the wrong project, you must use that project for all service accounts. Create the OAuth credentials there too to keep everything in one place.
