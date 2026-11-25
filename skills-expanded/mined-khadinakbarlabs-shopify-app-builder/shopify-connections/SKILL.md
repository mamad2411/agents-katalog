---
name: shopify-connections
description: "Guide safe Shopify Dev Dashboard, Partner Dashboard and CLI account setup, plus optional Apify CLI research access, without requiring MCP or collecting credentials."
---

# Connect only what you need

A connection here means an official browser sign-in or CLI session owned by the user—not a bundled remote server or invented connector ID.

## Choose the minimum setup

| Purpose | Connection | Needed now? |
| --- | --- | --- |
| Plan, review code, use examples | None | Works offline with files |
| Scaffold/test an app | Shopify CLI + Dev Dashboard org/app/dev store | When testing live |
| Partner business, distribution and payouts | Partner Dashboard | Only for that workflow |
| Competitor/review research | Apify CLI or a Console export | Optional |

## Shopify setup, one step at a time

1. Inspect non-secret versions with shopify version and installed help. If absent, explain the official CLI installation prerequisites and proposed install before acting.
2. Open the official Dev Dashboard. The user chooses the correct organization and an authorized dev store; app developer access may require the organization owner.
3. For a new project use the current shopify app init flow; for an existing one inspect shopify app info. Let Shopify's supported command open browser sign-in when needed. Don't invent a separate auth command or extract a cached session.
4. Explain app config link can create/overwrite local configuration; confirm the selected app and preserve existing config before linking.
5. Run shopify app dev against the approved dev store, complete the install approval, then verify an embedded page and an authenticated read. Record only non-secret organization/app/store identifiers in the user's project notes.
6. Use the Partner Dashboard only when needed for partner/business or distribution steps. App creation/configuration has moved to Dev Dashboard. Verify the current dashboard path rather than following old screenshots.

## Optional Apify connection

Explain an Actor is a hosted program that can incur charges. Use the official Apify CLI or let the user export public results from Console.
The user completes apify login themselves through the official supported flow. Never use a token-display command, inspect the CLI credential file, or pass a token in an argument or URL.
Inspect apify --version and apify actors info khadinakbar/shopify-app-store-scraper --input, then use [app-market-research](../app-market-research/SKILL.md). No paid call is authorized by login or input inspection.

## Verify / recover

Connected is not the same as installed or tested. Confirm the intended org/app/dev store via supported non-secret status, and the working app in the dev store.
If access is denied, name the missing app developer role and provide the official permission guide. If no CLI/browser is available, give a checklist or manual Console path and continue offline work.
Do not request access to other organizations, production stores, or unrelated Actors.

## Sources

- [Shopify scaffold and CLI flow](https://shopify.dev/docs/apps/build/scaffold-app)
- [Dev Dashboard migration](https://shopify.dev/docs/apps/build/dev-dashboard/migrate-from-partners)
- [User permissions](https://shopify.dev/docs/apps/build/dev-dashboard/user-permissions)
- [Shopify CLI commands](https://shopify.dev/docs/api/shopify-cli/app)
- [Apify CLI reference](https://docs.apify.com/cli/docs/reference)
