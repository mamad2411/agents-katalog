---
name: play-data-safety
description: Fill in Google Play's Data safety form for an Android app from its real code and libraries, and produce the CSV that Play Console imports. Use when the developer asks to fill, generate, update, check or fix their Play Data safety form / data safety section / privacy labels, before a Play release, or after adding or removing an SDK. Works on any Android (Gradle) project without changing its code.
---

# Play Data safety

You help an Android developer complete Google Play's **Data safety** form from evidence, not memory.
The output is `play-data-safety/play_data_safety.md` (human-readable answers) and
`play-data-safety/play_data_safety.csv` (what Play Console → Data safety → **Import from CSV** takes).

`SKILL_DIR` below means the folder this file is in. Every script needs only **JDK 17+**, which an
Android developer already has. Nothing is added to the developer's project except the
`play-data-safety/` output folder.

## Rules that matter more than speed

1. **Never declare what an SDK collects from your own knowledge.** Use only `SKILL_DIR/sdks/*.json`
   (each entry cites the vendor's page). If a library isn't in the table, tell the developer and
   look up the vendor's own Data safety page with them. Do not guess.
2. **A permission or API call is a question, not a declaration.** Play only counts data that
   **leaves the device**. Camera used for an on-device filter is not collected; a photo uploaded to
   a server is.
3. **"Shared" has a narrow meaning.** Sending data to a *service provider* that processes it on the
   developer's behalf (Firebase, Sentry, RevenueCat, Supabase…) is **not** sharing. Sending it to a
   party that uses it for its own purposes (ad and attribution networks) **is**. Follow each SDK
   entry's `shared` and `role`; when unsure, ask.
4. **Ask one topic at a time** and wait for the answer. Don't dump 15 questions at once.
5. **This is a draft for the developer to confirm, not legal advice.** Say so once, at the start.

## Step 1 — Scan

From the app's project root, run:

```bash
java SKILL_DIR/scripts/Scan.java . --skill-dir SKILL_DIR
```

- It runs the project's own Gradle (`:app:dependencies --configuration releaseRuntimeClasspath`) to
  get **every** library, including ones pulled in by other libraries. The first run can take a few
  minutes. It changes no project files.
- **Product flavors?** It picks the first `*ReleaseRuntimeClasspath` and says which. Ask the
  developer which flavor ships to Play and re-run with `--configuration <flavor>ReleaseRuntimeClasspath`.
- **Gradle fails?** Show the error. If it can't be fixed quickly, re-run with `--no-gradle`
  (reads build files only) and **tell the developer** transitive libraries were not checked.
- More than one app module? Use `--module :thatModule`.

It writes `play-data-safety/scan.json`, `scan.md`, and `play_data_safety.draft.md`.

## Step 2 — Show what was found

Read `play-data-safety/scan.json` and give the developer a short summary:
- SDKs recognised, and the data types they bring (`draftRows`), each with its source SDK.
- **On the classpath is not the same as active.** The scanner already leaves out Firebase SDKs
  when there is no `google-services.json` and no manual `FirebaseOptions` init (`inactiveSdks`,
  with the rows they would have added). For every other SDK, check it is really switched on: an
  init call in code, an API key set, or a feature flag (e.g. a template that ships an auth library
  with auth turned off). If one looks inactive, show the evidence and confirm with the developer.
  Then leave its rows out **and** record each one under `## Not collected` in Step 4, so the
  reason is written down and the CI check accepts it.
- Libraries **not** in the table (`unknownDependencies`). For each one that plausibly collects data
  (analytics, ads, crash, attribution, chat, payments, maps, auth), find the vendor's Data safety
  page and confirm with the developer. UI, image-loading, DI and similar libraries can be skipped.
  `supportingDependencies` are helpers of an SDK that was recognised; ignore them.
- Note `confidence: low` entries: say they need a manual check.

## Step 3 — Ask what code can't tell

Work through these, **one topic at a time**:

1. **Each `conditionalTypes` item**: data an SDK collects only in some setups (e.g. user IDs only if
   the app calls `setUserId`). Check the code first; ask only if the code doesn't settle it. Add a row
   for each one that applies.
2. **Each `ask` item** from the recognised SDKs (e.g. "Do you send the user's email to RevenueCat?").
3. **Each permission** in `permissions`: does that data leave the device? Where to?
4. **Each host** in `hosts` and each `network` code signal: what user data goes there? Your own
   backend counts. Audio, photos, free text or location sent to an AI or transcription API is
   collected (and the API provider is usually a service provider, so not shared).
5. **Other code signals** (location, contacts, audio, camera…): same question.
6. **Required or optional?** Per data type, can the user turn it off in the app (e.g. an analytics
   opt-out)? Only then is it "Users can choose whether this data is collected".
7. **Processed ephemerally?** Almost always **No**. Only Yes if the data is used in memory and never
   stored or logged, anywhere.
8. **Encrypted in transit?** Yes if every request uses HTTPS.
9. **Deletion:** can users ask for their data to be deleted, and at what **URL**? Play requires one.
10. **Accounts:** how do users create an account: Username and password, OAuth (e.g. Google
   sign-in), Other authentication, or None? If None: can they log in with an account made outside
   the app?

## Step 4 — Write `play-data-safety/play_data_safety.md`

Start from `play_data_safety.draft.md`. Fill every `TODO`, add rows from Step 3, remove rows the
developer ruled out (with their reason in your summary). The CSV generator parses this file, so
keep this exact shape:

```markdown
# Play Data Safety — <App name>

## Data collection and security

- **Does your app collect or share any of the required user data types?** Yes
- **Is all of the user data collected by your app encrypted in transit?** Yes
- **Do you provide a way for users to request that their data is deleted?** Yes
- **Data deletion URL:** https://example.com/delete-my-data
- **Account creation method:** OAuth
- **Accounts created outside the app:** No

## Data types collected

| Data type | Collected | Processed ephemerally | Required, or users choose | Shared | Purpose | Source |
|---|---|---|---|---|---|---|
| Personal info / Email address | Yes | No | Data collection is required | No | Account management | Firebase Auth |
| App activity / App interactions | Yes | No | Users can choose whether this data is collected | No | Analytics | Firebase Analytics |
```

- **Data type**: Google's canonical `Category / Type` label, verbatim (list in `SKILL_DIR/sdks/SCHEMA.md`).
- **Purpose**: `;`-separated, from: `App functionality`, `Analytics`, `Developer communications`,
  `Fraud prevention, security, and compliance`, `Advertising or marketing`, `Personalization`,
  `Account management`.
- One row per data type. If two SDKs collect the same type, merge: Shared = Yes if either shares,
  purposes combined, both named in Source.
- `Accounts created outside the app` only matters when the method is None.
- **Data types you ruled out** go under a final `## Not collected` heading, one bullet each:
  `- <Category / Type> — <why, with the evidence>`, e.g.
  `- Personal info / User IDs — Firebase Auth ships but sign-in is turned off (AUTH_ENABLED = false)`.
  Only list types a recognised SDK would otherwise bring. The CSV ignores this section; the CI
  check reads it, so a ruled-out type doesn't fail the build. Never use it for data that is
  actually sent.

## Step 5 — Generate the CSV

```bash
java SKILL_DIR/scripts/DataSafetyCsv.java \
  play-data-safety/play_data_safety.md \
  SKILL_DIR/reference/play-data-safety-template.csv \
  play-data-safety/play_data_safety.csv
```

- **PASS**: the CSV is written. Show the summary it prints.
- **FAIL**: nothing is written; it lists the exact problems (unknown label, bad purpose, missing
  URL, an unanswered TODO). Fix the `.md`, never the CSV, and run it again.

## Step 6 — Hand over

Print the final table from `play_data_safety.md` in the chat, then:

> **In Play Console:** Dashboard → *Set up your app* → **Data safety** → **Import from CSV** →
> upload `play-data-safety/play_data_safety.csv` → check the preview → **Save**.
> Your privacy policy must describe the same data. Re-run this whenever you add or remove an SDK.

Optionally offer the CI check, which fails a build when a recognised SDK collects a data type the
declaration doesn't list:

```bash
java SKILL_DIR/scripts/Scan.java . --skill-dir SKILL_DIR --check play-data-safety/play_data_safety.md
```

## When an SDK is missing from the table

After the developer confirms what a missing SDK collects from its vendor's page, offer to save it
as `SKILL_DIR/sdks/<id>.json` (format in `sdks/SCHEMA.md`, with the source URL and today's date) and
suggest contributing it upstream: https://github.com/wajahatkarim3/play-data-safety-skill
