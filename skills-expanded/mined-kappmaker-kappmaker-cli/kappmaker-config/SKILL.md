---
name: kappmaker-config
description: Manage KAppMaker CLI configuration — API keys (fal.ai, OpenAI, imgbb, App Store Connect, Google service account), the template repo, bundle-ID prefix, and the App Store / Adapty defaults. Use when the user wants to set or check an API key, configure the CLI, fix a "missing credential" error, or change where new apps clone from.
---

# KAppMaker — Config

Configuration lives at `~/.config/kappmaker/config.json`. Almost every "command failed" that is
not a store-side error traces back here, so this is also the first stop when a credential error
appears.

### The commands

- `kappmaker config list` — show all values
- `kappmaker config get <key>` / `set <key> <value>` — read / write one value
- `kappmaker config path` — where the file lives
- `kappmaker config init` — interactive wizard; also offers App Store and Adapty defaults at the end

Prefer `config set` per key over `config init` when driving the CLI for a user — `init` is fully
interactive and hard to guide through. Keys are prompted inline on first use anyway, so
pre-configuring is optional; a missing key is never a fatal error.

**Valid keys**: `templateRepo`, `bundleIdPrefix`, `androidSdkPath`, `organization`, `falApiKey`,
`imgbbApiKey`, `openaiApiKey`, `ascAuthName`, `ascKeyId`, `ascIssuerId`, `ascPrivateKeyPath`,
`appleId`, `googleServiceAccountPath`, `revenuecatApiKey`, `revenuecatProjectId`,
`iosCertsRepo`, `iosCertsRepoToken`.

### Where each key comes from

| Key | Where to get it |
|-----|----------------|
| `falApiKey` | https://fal.ai/dashboard/keys |
| `imgbbApiKey` | https://api.imgbb.com (free) |
| `openaiApiKey` | https://platform.openai.com/api-keys |
| `ascKeyId` + `ascIssuerId` + `ascPrivateKeyPath` | App Store Connect → Users and Access → Integrations → App Store Connect API |
| `appleId` | The user's Apple ID email |
| `googleServiceAccountPath` | Google Cloud Console → IAM → Service Accounts → Keys → JSON, then grant access in Play Console → Users and permissions. Used by `kappmaker publish --platform android` and the entire `gpc` group. |
| `revenuecatApiKey` | RevenueCat dashboard → Project settings → API keys → V2 (secret `sk_…`; v1 keys don't work). **Per-project key** — this global value is a single-app shortcut. Multi-app accounts: `kappmaker revenuecat setup --api-key sk_...` saves each app's key into `~/.config/kappmaker/revenuecat-keys.json` by bundle ID. |
| `iosCertsRepo` | Private repo holding Apple signing certificates, shared by every app on ONE Apple Developer account (default `<owner>/apple-certificates`). Set once by `kappmaker ios-ci init`. Certificates are account-scoped and Apple allows only 3, so a per-app store locks you out on the fourth app. |
| `iosCertsRepoToken` | PAT with read access to that repo — the runner's built-in `GITHUB_TOKEN` cannot reach a second repository. Set once, reused by every app. |
| `revenuecatProjectId` | Rarely needed — a project-scoped key already identifies its project. Only for unusual account-wide keys that see several. |

### Store and provider defaults

Global default product sets, reused by every new app:

- `kappmaker config appstore-defaults --init` — interactive App Store defaults. Re-running
  backfills credit-pack IAPs missing from pre-1.4 defaults.
- `kappmaker config appstore-defaults --save <file>` — save a JSON file as the defaults
- `kappmaker config adapty-defaults --init` — Adapty defaults from the built-in template
  (subs + 3 credit packs + Credits Paywall + `credits_pack` placement). Re-running backfills
  whichever of `products` / `paywalls` / `placements` is empty.
- `kappmaker config adapty-defaults --save <file>` — save a JSON file as the defaults

---

## Where this sits in the flow

- **Before this:** — (this is the zeroth step; `create` triggers `config init` itself if no
  config exists yet).
- **After this:** any other kappmaker skill — they all read this config.
