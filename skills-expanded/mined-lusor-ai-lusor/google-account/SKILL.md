---
name: google-account
description: Add or sign in to a Google account on the Android phone (Settings → Accounts → Add account → Google, or any app's "Sign in with Google" / "Continue with Google"). Use when a task needs the user's own Google account signed in on the device or inside an app.
keywords: [google account, sign in, add account, gmail, sign in with google, continue with google, google login]
platform: android
app_package: com.google.android.gms
---

# Google account sign-in on Android

## Where it starts
- **Settings route:** Settings → *Passwords, passkeys & accounts* (or *Accounts*) → *Add account* → *Google*.
- **In-app route:** an app's *Sign in with Google* / *Continue with Google* button opens the same Google flow (or an account chooser if an account is already on the device).
- Both land in Google's own sign-in screens (`com.google.android.gms`, MinuteMaid). Wait 3 to 8 s for each screen to load before reading the UI.

## Step 1: "Sign in with ease" → always tap **SKIP**
- The first screen is often **"Sign in with ease"**: "We can search for accounts connected to this phone number by obtaining your number from your carrier…", with **SKIP** (bottom left) and **NEXT** (bottom right).
- **Tap SKIP.** Never tap NEXT here. NEXT asks the carrier for the phone number. A cloud phone's SIM has no real number, so the lookup sits on "Loading" indefinitely, and backing out may show "Something went wrong / Please go back and try again".
- If you already tapped NEXT and the screen is stuck on "Loading" or shows "Something went wrong", press Back (`key({ keyCode: 4 })`) until you return to *Add account*, start again, and tap SKIP.

## Credentials (vault only)
Use the credential vault. **NEVER** type a credential value with `type()`, and **NEVER** ask the human to paste one (see agent-guidelines → Credentials). The available secret ids are listed in the CREDENTIALS section of your system prompt (for example a Google email and password). If there is no CREDENTIALS section, or no Google entry, the session has no Google account to use: do not attempt sign-in. Call `request_human()` instead. **Never invent an account.**

## Step 2: email
- The screen shows **"Sign in"**, an **"Email or phone"** field, *Forgot email?*, *Create account* and **NEXT**.
- `type_secret({ secret_id: "<the Google email id>", index: <email-field-index>, clear: true })`, then tap NEXT.

## Step 3: password and verification
- The next screen is **"Welcome"**, showing the email, a password field, *Show password*, *Try another way* and NEXT.
- `type_secret({ secret_id: "<the Google password id>", index: <password-field-index>, clear: true })`, then tap NEXT.
- Google may then ask for 2-step verification (a code by SMS, an authenticator code, or a prompt on another device). If you cannot complete it, call `request_human()`. Do not guess and do not retry repeatedly: repeated failures can lock the account.
- Accept the terms screens (*I agree*) and skip optional offers (backup, Google One, payment) with *Skip* / *No thanks* / *Not now* unless the task asks for them.

## Confirming success
- Back in Settings → Accounts, a Google account is now listed (or the app that asked for sign-in shows you signed in).
- Report success by the **secret id** you used (for example "signed in with `<the Google email id>`"), never by the email value. The vault withholds credential values from you and redacts them from screen captures, so do not read, quote or reconstruct the email, password or any verification code.
