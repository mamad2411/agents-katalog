---
name: leaddocket-settings
description: >
  Retrieve system settings and account configuration options from LeadDocket.
  Use to discover instance configuration at startup, validate feature flags,
  or build conditional logic in integrations based on the account's active
  features.
---

# LeadDocket — Settings

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

---

## Get system settings and options

```http
GET /api/settings/get-options
```

Returns `SettingsOptionsApi` — a configuration object representing the account's current system settings.

Key fields typically include:
- Feature flags (SMS enabled, DocuSign enabled, Filevine connected, etc.)
- Timezone configuration
- Default lead role assignments
- Account plan information

---

## Best Practices

- **Call at startup**: Fetch settings once at application startup and cache. Use to conditionally enable features in your integration (e.g., only enable SMS sending if the SMS feature is active).
- **Re-fetch on config changes**: If your integration allows admins to modify settings, invalidate the cache and re-fetch after saves.
- **Use for feature detection**: Rather than hardcoding "this instance has DocuSign", check the settings response to enable/disable integration branches dynamically.
