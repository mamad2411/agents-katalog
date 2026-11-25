---
name: setup
description: Set up google-marketing-agent from zero, or fix a broken setup. Use when the user says "set up google-marketing-agent", "connect my Google Ads", "the doctor is red", "add another account", or when any tool fails with a sign-in, permission or access-level error.
---

# Setup

Walk the user from nothing to a green `setup_doctor`, one step at a time. Each step ends with a check; move on only
when that step is green.

## When to use

- First run: no profiles, or tools answer "No accounts configured" / "Not signed in".
- A tool failed with `invalid_grant`, `USER_PERMISSION_DENIED`, `PERMISSION_DENIED`, a disabled API, or test-level access.
- The user wants to add another Google Ads account or link GA4 / Search Console / Tag Manager.

## Inputs

None. Everything comes from `setup_doctor` and the user's answers.

## Steps

1. Call `setup_doctor`. If every line is ✓, say so and stop.
2. Read the first ✗ line and its fix. Handle the earliest broken stage first, in this order:
   1. **Signed out / no credentials** → step 3.
   2. **Google Ads access level** (only test accounts visible, or "Test level") → step 4.
   3. **Account not readable** (`USER_PERMISSION_DENIED`, wrong manager) → step 5.
   4. **GA4 / Search Console / Tag Manager** lines → step 6.
3. **Cloud project and OAuth client.** Explain the four one-time steps, wait for "done" after each:
   1. Create a Google Cloud project (console.cloud.google.com).
   2. Enable the Google Ads API, plus Google Analytics Data API, Google Analytics Admin API, Google Search Console API
      and Tag Manager API for the products they use.
   3. OAuth consent screen: **Internal** if they are in a Google Workspace organisation; otherwise **External** and set
      it to **In production**. Testing mode makes the sign-in expire after 7 days.
   4. Credentials → Create credentials → OAuth client ID → **Desktop app**.

   Then tell them to run `npx google-marketing-agent init` **in their own terminal** and pick their accounts.
   Call `guide("access")` if they ask about developer tokens or access levels.
4. **Access level.** The Cloud project that owns the OAuth client starts at Test level. Tell them: Cloud Console →
   APIs & Services → Google Ads API → Overview → apply for **Explorer** (usually approved within minutes). The OAuth
   client must be in that same project. Use `guide("access")` for the levels table.
5. **Account access.** Call `accounts_list`. If the account is listed "via manager", the profile needs that manager as
   `loginCustomerId`:
   `npx google-marketing-agent accounts set <alias> loginCustomerId <manager id>`.
   If it is not listed at all, the signed-in Google user needs access to it in Google Ads.
6. **Other products.** For each ✗ line, give the exact role from the fix text (GA4 Viewer, Editor for key events;
   Search Console Full or Restricted user; Tag Manager Read/Edit/Publish) and the profile field to set
   (`ga4PropertyId` numeric ID, `gscSiteUrl` exactly as Search Console lists it, `gtmContainerId` `GTM-XXXX`).
7. After each fix, call `setup_doctor` again and report only what changed.
8. When everything they need is green, call `account_profile` and summarise the profile. Mention that profiles are
   read-only; changes need `npx google-marketing-agent accounts set <alias> writes true` after reading the safety
   guide, then a restart of their MCP client.

## Output

A short checklist: each stage ✓ or ✗ with the one next action. End with either "Setup complete" or exactly what is
still missing and who has to grant it (the user, their Google Ads admin, their Workspace admin).

## Never

- Never ask the user to paste a client secret, refresh token or service-account key into the chat. Secrets go into
  `init` in their own terminal only.
- Never edit `~/.config/google-marketing-agent/*.json` by hand on their behalf; use the CLI commands above.
- Never turn on writes for them. Explain how, and let them decide.
