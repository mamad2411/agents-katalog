---
name: appstorereject-resolve
description: Resolve App Store or Google Play rejections. Look up rejection by guideline code, get resolution steps, plan fixes in your codebase, or generate an appeal letter.
---

# Resolve App Store Rejection

Help the developer resolve a rejection they've received from Apple or Google.

## Step 1: Identify the Rejection

Determine the guideline code:

- **If the developer pasted a rejection email:** Extract the guideline code (pattern: "Guideline X.Y.Z" or "Section X.Y"). Also note the specific reasons cited.
- **If the developer gave a guideline code directly:** Use it (e.g., "2.1", "5.1.1", "3.1.1").
- **If the developer described the issue in words:** Search for it:
  ```
  {baseDir}/../appstorereject/scripts/asr-api.sh GET "/api/search?q=<keywords>&limit=5"
  ```
  Present the top matches and ask the developer to confirm which one.

## Step 2: Fetch Rejection Details

Once you have the slug (from search results or known mapping):

```
{baseDir}/../appstorereject/scripts/asr-api.sh GET "/api/rejections/detail?slug=<slug>"
```

**If authenticated:** You'll get full resolution steps, example rejection email, before/after examples, and community solutions.

**If unauthenticated:** You'll get a summary only. Tell the developer: "For full resolution steps and community solutions, set up an API key: `export ASR_API_KEY=asr_...` (get one at appstorereject.com/settings/api-keys)"

## Step 3: Present Resolution Guide

Show the developer:
1. **Title and description** of the rejection
2. **Difficulty level** and **estimated resolution time**
3. **Resolution steps** in order (if authenticated)
4. **Before/after examples** (if available and authenticated)
5. **Community solutions** ranked by effectiveness (if authenticated)

## Step 4: Plan Fix in Codebase Context

Read `{baseDir}/references/resolution-workflow.md` for the structured approach.

For each resolution step:
1. Search the developer's codebase for the relevant files
2. Propose specific changes tied to the resolution step
3. Explain **why** the change satisfies the guideline

Present the complete fix plan before making any changes. Wait for developer approval.

## Step 5 (Alternative): Appeal Letter

If the developer wants to appeal instead of fixing (they believe the rejection is wrong):

Generate an appeal letter using:
- The specific guideline cited in the rejection
- What the app actually does (from codebase context)
- Apple/Google's public review guidelines language

The appeal is generated locally by you (the AI agent) — no API call needed. Present the draft for the developer to review and edit before sending.

## Step 6: Report Analytics

After the developer resolves, appeals, or abandons:

```
{baseDir}/../appstorereject/scripts/asr-api.sh POST "/api/rejections/report" '{"bundleId":"<detected>","guidelineCode":"<code>","action":"resolved|appealed|abandoned","platform":"ios|android"}'
```

Auto-detect the bundleId from the project (Info.plist, build.gradle, app.json). If not detectable, ask the developer.
