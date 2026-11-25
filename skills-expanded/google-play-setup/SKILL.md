---
name: google-play-setup
description: Set up Google Play Console, create an Android app listing, configure EAS credentials for Android builds, and set up the service account for CI/CD submissions. Use when publishing a new Android app, setting up Play Store automation, or troubleshooting AAB uploads.
---

# Google Play Setup

## Prerequisites

- Google Play Console account ($25 one-time fee) at [play.google.com/console](https://play.google.com/console)
- EAS CLI: `npm install -g eas-cli && eas login`

**Required reading — Expo official guides:**
- [Creating a Google Service Account](https://github.com/expo/fyi/blob/main/creating-google-service-account.md)
- [First Android Submission](https://github.com/expo/fyi/blob/main/first-android-submission.md)

---

## Step 1: Configure Android Package Name

Set the package name in `app.json` before the first build — it cannot be changed after the app is published:

```json
{
  "expo": {
    "android": {
      "package": "com.yourorg.appname"
    }
  }
}
```

Use reverse domain notation. Must be globally unique on Play Store.

---

## Step 2: Create Play Console App Listing

1. Go to [play.google.com/console](https://play.google.com/console) → **Create app**
2. Fill in:
   - **App name:** Display name
   - **Default language:** English
   - **App or game:** App
   - **Free or paid:** your choice
3. Accept policies → **Create app**

Note the **Application ID** from the URL: `play.google.com/console/u/0/developers/.../app/XXXXXXXXXXXXXXXXXX/`

---

## Step 3: Complete App Setup Requirements

Google requires these before you can upload any build:

**App content declarations** (Play Console → Policy → App content):
- [ ] Privacy Policy URL
- [ ] Ads declaration
- [ ] Content rating questionnaire (takes ~2 min)
- [ ] Target audience
- [ ] Data safety form (what data you collect — be honest)

**Store listing** (Play Console → Grow → Store presence → Main store listing):
- [ ] Short description (80 chars)
- [ ] Full description (4000 chars)
- [ ] Screenshots: Phone (minimum 2), Tablet optional
- [ ] Feature graphic: 1024×500 PNG
- [ ] App icon: 512×512 PNG

**None of this blocks the first upload** but it does block publishing to users.

**"Finish setting up your app" banner** — Play Console shows this dashboard banner after app creation. It lists required items before you can publish. Work through them in order — all must be green before the app goes live. This is separate from the store listing itself.

---

## Step 4: Configure EAS Credentials

```bash
cd mobile
eas credentials
```

Select **Android** → **production** → Let EAS manage the keystore (recommended).

EAS generates and stores the Android signing keystore. **Never lose this keystore** — you cannot update your app without it. EAS stores it encrypted.

To verify:
```bash
eas credentials --platform android
```

---

## Step 5: First Build and Manual Upload

Google requires the **very first AAB to be uploaded manually** via Play Console. Subsequent uploads work via `eas submit`.

```bash
# Build the AAB
cd mobile
eas build --platform android --profile production

# Download the AAB when done
eas build:list --platform android
# Click the download link from the output, or:
eas build:download --platform android --latest
```

Upload manually:
1. Play Console → **Release** → **Internal testing** → **Create new release**
2. Upload the downloaded `.aab` file
3. Add release notes → **Save** → **Review release** → **Start rollout**

After this first manual upload, `eas submit` will work for all future releases.

**Sharing the internal testing link** — Unlike TestFlight (email invites), Google Play internal testing uses a shareable opt-in link. After rollout:
1. Play Console → **Testing** → **Internal testing** → **Testers** tab
2. Copy the **opt-in URL** and send it to testers
3. Testers open the link on their Android device and click "Accept invitation"
They won't find the app by searching — they must use the link.

---

## Step 6: Service Account for CI/CD

Required for non-interactive submissions from GitHub Actions.

**Create service account:**
1. Play Console → **Setup** → **API access**
2. Click **Link to a Google Cloud Project** (or create new)
3. In Google Cloud Console: **IAM & Admin** → **Service Accounts** → **Create Service Account**
   - Name: `eas-submit`
   - Role: Skip (add via Play Console)
4. Click the service account → **Keys** → **Add Key** → **Create new key** → **JSON**
5. Download the JSON file

**Grant Play Console permissions:**
1. Back in Play Console → **Setup** → **API access**
2. Find the service account → **Manage Play Console permissions**
3. Grant: **Release manager** (minimum) or **Admin**
4. Apply and save

**Add to EAS:**
```bash
# Option A: Store in eas.json (committed, less secure)
# Point eas.json submit profile to the file path

# Option B: Upload to EAS secrets (recommended for CI)
eas secret:create --scope project --name GOOGLE_SERVICE_ACCOUNT_KEY --value "$(cat service-account.json)"
```

Or store locally and reference in `eas.json`:
```json
{
  "submit": {
    "production": {
      "android": {
        "serviceAccountKeyPath": "./google-services.json",
        "track": "internal",
        "releaseStatus": "draft"
      }
    }
  }
}
```

---

## Step 7: Submit via EAS

After the first manual upload and service account setup:

```bash
eas submit --platform android --profile production --latest
```

This uploads to the **internal testing track** with `draft` status by default. You manually promote to production in Play Console.

---

## Track Strategy

| Track | Who sees it | When to use |
|-------|-------------|-------------|
| **Internal** | Up to 100 testers (your team) | Every build for QA |
| **Closed testing (Alpha)** | Invited users | Beta before launch |
| **Open testing (Beta)** | Anyone who opts in | Public beta |
| **Production** | All users | Launch |

Start with Internal track. Promote builds through tracks in Play Console — no rebuild needed.

---

## Gotchas

**"Package name already taken"** — The package name is globally unique. Use a specific reverse domain.

**Upload rejected: "Version code already used"** — Always use `appVersionSource: "remote"` + `autoIncrement: true` in `eas.json`.

**"You need to upload an AAB first"** — You must manually upload the very first build. `eas submit` will fail until then.

**Service account upload fails with 403** — The service account needs **Release manager** or **Admin** permissions in Play Console (not just Google Cloud IAM). Check Play Console → API access → service account permissions.

**"App not found" during submit** — The `applicationId` in `eas.json` must exactly match the package name in `app.json` and Play Console.

**Data safety form blocks publishing** — Fill it in Play Console → Policy → App content → Data safety. Must declare all data collected (Supabase auth = email/user ID, PostHog = device info).

**First submission review takes 3–7 days** — Build your buffer into the timeline. Subsequent updates usually review in hours.

**Camera/microphone/location access requires a public Privacy Policy URL** — Google will reject or unpublish apps that request sensitive permissions without a publicly accessible privacy policy. The URL must be reachable without login.

**Data safety form blocks publishing** — Fill it in Play Console → Policy → App content → Data safety. Must declare all data collected (Supabase auth = email/user ID, PostHog = device info, camera = photos if saved).
