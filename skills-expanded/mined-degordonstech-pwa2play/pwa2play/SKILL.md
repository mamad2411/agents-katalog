---
name: pwa2play
description: Package a Progressive Web App into a Trusted Web Activity (TWA) Android app bundle for the Google Play Store with Bubblewrap. Covers target API level compliance, reusing the signing key, Digital Asset Links (assetlinks.json), version codes, and the testing-to-production path. Use whenever someone wants to publish or update a PWA or website on the Google Play Store, wrap a web app as an Android app, build a TWA or .aab/.apk, fix a "signed with the wrong key" or "target API level" rejection, or fix a TWA that opens with the browser address bar showing.
---

# Getting a PWA onto the Play Store without the usual pain

Wrapping a PWA as an Android app is a solved problem. The catch is that the default tools quietly set you up to fail, and Google's error messages do not tell you what actually went wrong. This skill is the checklist I wish I had the first time.

The technology is a Trusted Web Activity (TWA): a thin Android app that opens your website full screen, no browser chrome, as long as your site proves it owns the app. Google's Bubblewrap builds it. Everything below is about doing that build so it passes review and keeps updating for years.

## Before you start, you need

- **Node.js and a JDK** (Java 17 works well). Bubblewrap pulls the Android SDK itself.
- **A live PWA over HTTPS** with a valid `manifest.json` (name, icons including a 512x512, `start_url`, `display: standalone`).
- **A Play Console developer account.** Individual accounts have to run a closed test with 12 testers for 14 days before production. Organization accounts skip that, so if you have a business, verify as an organization first.

## The build, start to finish

1. Install Bubblewrap: `npm i -g @bubblewrap/cli`. Use the latest version. This matters, the current CLI is what targets the current Android API, and Google raises that requirement every year.

2. Initialize from your manifest:
   `bubblewrap init --manifest https://yoursite.com/manifest.json`
   This creates a project folder and a `twa-manifest.json`. It will ask you to create a signing key. Do that once and **guard that keystore file and its passwords with your life** (more on this below).

3. Pick your package id carefully when asked. Use reverse-domain, lowercase, e.g. `com.yoursite.twa`. **This is permanent.** Once an app with this id is uploaded, you can never change it for that listing.

4. Build: `bubblewrap build`. It produces `app-release-bundle.aab` (this is what you upload) and `app-release-signed.apk` (handy for local testing). It signs with the keystore from step 2.

5. Wire up Digital Asset Links so the app opens without a browser bar. See the assetlinks section, this is the step everyone gets wrong.

6. In Play Console, upload the `.aab` to **Internal testing first**, never straight to production. Confirm the bundle details show the right target API and version code, then promote.

## The rules that actually keep you from getting rejected

These are the ones that cost real time. Treat them as non-negotiable.

### 1. Generate the key once, then reuse that same key forever.

For a brand-new app you generate a fresh signing key, that is normal and expected. Bubblewrap offers to make one for you during `init`, and that is the right moment to do it. If you would rather make it yourself, `keytool -genkey -v -keystore my-app.keystore -alias my-app -keyalg RSA -keysize 2048 -validity 9125` gives you one.

The rule kicks in **after** that first upload. Every future update to the same app has to be signed with the **same** key. Build an update with a different key and Google rejects it with "signed with the wrong key," and there is no way to make the store accept it.

So: new app, new key is fine. Existing app, always the original key. Bubblewrap remembers your key in `twa-manifest.json` under `signingKey` (a path and an alias). Keep that keystore file and its two passwords somewhere safe and back them up. Losing them is the single most expensive mistake here.

Note on PWABuilder: the web packager is convenient, and for a first release letting it generate a key is fine (download the keystore it gives you and keep it). The catch is on updates, by default it generates a **fresh keystore every time you download a package**, so for any update you must supply your existing key in its Android options. If you already shipped once and lost the original key, you cannot rebuild, your only way out is **Play Console > Test and release > App integrity > request an upload key reset**.

### 2. assetlinks.json must carry the APP SIGNING key, not the upload key.

If your app opens showing the Chrome address bar, this is why. The TWA only goes full screen when your website hosts a file at `https://yoursite.com/.well-known/assetlinks.json` that lists the SHA-256 of the key that signs the installed app.

Here is the trap. New apps use **Play App Signing**: Google holds the real "app signing" key and re-signs your app, while you upload with your "upload" key. The fingerprint in assetlinks.json has to be the **app signing** SHA-256, which you get from **Play Console > Test and release > App integrity > App signing key certificate**, not the upload key that Bubblewrap prints. If Play also shows a second (post-quantum) fingerprint, add both.

The file looks like this:

```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.yoursite.twa",
    "sha256_cert_fingerprints": [
      "AA:BB:CC:...:the-app-signing-sha256"
    ]
  }
}]
```

Deploy it, make sure it returns HTTP 200 as JSON (not your app's HTML 404 page), and give it a few minutes to propagate before you retest.

### 3. Bump the version code on every single upload.

`appVersionCode` in `twa-manifest.json` must be a whole number higher than anything you have uploaded before, to any track. Reuse one and you get "Version code N has already been used." Increment it every release. `appVersionName` ("1.0.1") is the human label and does not have this rule.

### 4. Keep targeting the current API level.

Google requires your app to target an Android version within one year of the latest release, or you lose the ability to update it. As of the 2026 deadline that is **API 36 (Android 16)**. They raise it roughly every August.

To retarget an existing project: update the CLI (`npm i -g @bubblewrap/cli`), run `bubblewrap update` in the project, bump `appVersionCode`, rebuild, and upload to a test track. Confirm the new target API before promoting (see the check command).

### 5. Test track before production, and the 12-tester rule.

Upload to Internal testing, install it on a real device, and actually use it before anything goes public. If you are on a **personal** developer account, Google also makes you run a **closed test with at least 12 testers opted in for 14 continuous days** before you can apply for production. **Organization** accounts are exempt, one more reason to verify as an organization if you run a business.

## When something breaks

- **App opens with a browser address bar** -> assetlinks.json is missing, unreachable, or has the wrong fingerprint. Use the app signing SHA-256, confirm the file returns JSON with a 200, wait, retest.
- **"You uploaded an APK or Android App Bundle signed with the wrong key"** -> you built with a different keystore. Rebuild with the original, or reset the upload key in Play Console.
- **"Version code N has already been used"** -> raise `appVersionCode` and rebuild.
- **"Your app currently targets API level X and must target Y"** -> update Bubblewrap, `bubblewrap update`, bump version, rebuild.
- **PWABuilder gave you a package that will not update the app** -> almost always a new keystore. Rebuild with your original key.

## Checking a built app

Before uploading, or when a build looks wrong, read the actual target and version out of the built file rather than trusting the tool. `scripts/check-target-api.mjs` in this plugin reads the package id, version code, and target and min SDK straight from an `.apk`. Point it at the `.apk` Bubblewrap produced. If it reports a target below the current requirement, do not upload it, fix it first.
