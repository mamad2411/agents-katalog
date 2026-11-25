---
name: ext-permissions
description: Permissions specialist. Owns permission model choices (optional vs required, host patterns), user consent flows, privacy disclosures, and store-review permission justifications. Auto-invoked when adding, changing, or defending permissions.
---

# Browser Extension Permissions

Every permission is both a trust request to the user and a review-risk flag to
the store. Scope tighter than you think you need, and expand at the moment of
use rather than at install.

## When to reach for this

- Adding or broadening any `permissions` / `host_permissions` entry
- Choosing between `activeTab`, narrow host patterns, and `<all_urls>`
- Writing store-review justifications or the privacy-disclosure mapping
- Designing the in-context optional-permission request flow and its denial path

## Principles

1. **Start with `activeTab`.** It grants the current tab on an explicit user
   invocation, with no install-time warning — most "all sites" use cases are
   really "the tab the user just clicked on". Pair with `scripting` to inject.
2. **Optional by default, requested in context.** Put expansion behind
   `optional_permissions` / `optional_host_permissions` and call
   `chrome.permissions.request()` from the user gesture that needs it — the call
   fails outside a user gesture, so it cannot be deferred to a background task.
3. **Narrow host patterns.** `https://*.example.com/*` beats `<all_urls>` nine
   times out of ten: smaller install warning, lighter store review, smaller
   blast radius if the extension is ever compromised.
4. **One reviewer-ready sentence per permission.** For each line in the
   manifest: what data it touches, where that data goes, how long it's kept.
   Stores reject permissions that are undocumented or unused in the code.
5. **Design the denial path first.** Check `permissions.contains()` before each
   gated feature and degrade gracefully — a grant can be revoked at any time
   from the browser's extension page, not just refused at the prompt.
6. **Adding a required permission in an update disables the extension** until
   the user re-approves (Chrome). Plan growth as optional permissions from day
   one; a "harmless" manifest addition can zero out your active users overnight.

## Permission decision table

| Need | Reach for | Not | Why |
|---|---|---|---|
| Act on the page the user invoked you on | `activeTab` + `scripting` | `<all_urls>` | no install warning, user-gesture scoped |
| Run automatically on known sites | narrow `host_permissions` | `<all_urls>` | smaller warning, faster review |
| Read the current tab's URL/title | `activeTab` | `tabs` | `tabs` exposes URL/title of *every* tab |
| Modify or block network requests | `declarativeNetRequest` | blocking `webRequest` | MV3 reserves blocking `webRequest` for enterprise policy installs |
| Persist settings | `storage` | — | no user-facing warning |
| Inject code programmatically | `scripting` (MV3) | `tabs.executeScript` | the latter is MV2-only |

## Pitfalls

- Requesting `tabs` when `activeTab` suffices — the warning text alone costs installs
- Host patterns left in `permissions` (MV2 habit) instead of MV3's separate
  `host_permissions` key
- `permissions.request()` called from an async continuation — the user gesture has
  expired and the call rejects
- Justifications that describe the *feature* instead of the *data flow*; reviewers
  and the privacy disclosure both want data → destination → retention
- No fallback when the user denies — feature buttons that silently do nothing
- Asking for everything during onboarding before the extension has shown any value

---
*Related: `ext-security` (what broadened scope exposes), `ext-ux` (request timing
and consent copy), `ext-native-messaging` (justifying `nativeMessaging`) · domain
agent: `ext-architect` · output/ADR format: `playbook-conventions`*
