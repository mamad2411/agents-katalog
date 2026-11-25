---
name: grovs-configure-platform
description: Configure iOS and Android platform settings — bundle IDs, Team IDs, package names, SHA-256 fingerprints, and redirect rules for Universal Links and App Links. Use when the user wants to set up Universal Links, App Links, change redirects, or update SDK configuration.
---

# Grovs: Configure Platform Settings

## Two tools, two different IDs

| Tool | ID type | Purpose |
|------|---------|---------|
| `configure_sdk` | **instance_id** (string) | Platform identity: bundle IDs, team IDs, package names, fingerprints |
| `configure_redirects` | **project_id** (string) | Where users land: App Store URL, Play Store URL, fallback website |

**These are different strings. Both come from `get_status`. Passing the wrong one is the #1 mistake.**

## Always show current state first

Call `get_status` and show the user what's currently configured before making changes. Prevents accidental overwrites.

## Redirect fields take full URLs

Pass `"https://apps.apple.com/app/id123456"` — not symbolic names like `"app_store"`. The schema validates with `z.url()`.

## Platform requirements

**iOS Universal Links** require both:
- `ios_bundle_id` (e.g., `com.company.app`)
- `ios_team_id` (Apple Developer Team ID)

Missing either → deep links won't open the app on iOS. `ios_app_store_id` is optional (only for App Store redirects).

**Android App Links** require both:
- `android_package_name` (e.g., `com.company.app`)
- `android_sha256_fingerprints` (array of strings from `keytool -list -v` or Play Console)

Missing either → deep links won't open the app on Android.

## Both tools are partial updates

Only send fields the user wants to change. Omitted fields stay unchanged.

## Example

User: "Add Android support, package is com.foodies.android, here's the fingerprint: AB:CD:EF:..."

```
configure_sdk(
  instance_id: "x7k2",
  android_package_name: "com.foodies.android",
  android_sha256_fingerprints: ["AB:CD:EF:..."]
)
```

Don't resend the iOS fields — they stay as-is.

## If something fails

- Error on `configure_sdk` → most likely you passed a project_id instead of instance_id
- Error on `configure_redirects` → check you passed a valid URL (not a bare domain like `"example.com"`, must be `"https://example.com"`)
- Per-link redirect overrides → that's `custom_redirects` on `create_link`/`update_link`, not these tools

## All tool responses are pre-formatted

Every Grovs tool returns human-readable formatted text. Don't reformat — just present and add context.
