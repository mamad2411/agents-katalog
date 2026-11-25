---
name: windows-settings-navigation
description: Open and navigate the Windows Settings app via ms-settings URIs and its accessibility tree.
version: 0.1.0
when:
  apps: [SystemSettings, ms-settings, Settings]
  keywords: [windows settings, control panel, wifi settings, display settings, default apps]
---
# Windows Settings navigation

Open a page directly with `desktop_launch` using an `ms-settings:` URI:
- `ms-settings:display`, `ms-settings:sound`, `ms-settings:network-wifi`, `ms-settings:bluetooth`
- `ms-settings:defaultapps`, `ms-settings:appsfeatures`, `ms-settings:startupapps`
- `ms-settings:privacy`, `ms-settings:windowsupdate`, `ms-settings:storagesense`
- `ms-settings:easeofaccess`, `ms-settings:dateandtime`

Inside the app:
1. `desktop_get_state` shows a left navigation list and a right content pane.
2. Use the search box ("Find a setting") with `desktop_set_value` when the URI is unknown.
3. Toggles appear as switch controls; clicking flips them. Read the state back afterwards.
4. Some pages open a second window (for example a UAC prompt); re-run `desktop_get_state`.

Safety: changing system settings, installing or uninstalling software, and anything behind a UAC prompt needs explicit user approval. Do not dismiss UAC prompts yourself.
