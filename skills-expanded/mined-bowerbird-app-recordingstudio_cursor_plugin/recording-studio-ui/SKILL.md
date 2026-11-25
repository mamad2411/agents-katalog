---
name: recording-studio-ui
description: Design Recording Studio screens as mountable UI slices with reusable helpers and view components. Use when adding or changing views, choosing page shape, mounting a gem's screens, replacing gem UI, or deciding layout. For which Flatpack component to render, use recording-studio-flatpack. For words on the screen, use recording-studio-text.
---

# Recording Studio UI

Gems ship **working UI slices** the host can mount, plus the **pieces** of that UI so a host can replace views and controllers without losing the capability. Screens stay small, one-job, and independent so they work on phones and so addons do not fight over layout.

Components: `recording-studio-flatpack`. Words: `recording-studio-text`. Taste: `recording-studio-taste`.

## Three layers

| Layer | Owner | Purpose |
|---|---|---|
| **Core methods** | Gem | Domain API that UI, API, and host overrides all call |
| **Controllers and views** | Gem | Default screens; upgrades reach every host that has not overridden them |
| **Routes and overrides** | Host | Mount paths; replace a view or controller only when the product must differ |

Hosts can mount as-is, override, or skip gem screens and call the same core methods. Do not copy gem templates into the app “just in case.”

Anything a host might put on *their* screen — a root switcher, a picker, a grant control — is a **helper or ViewComponent**, not only a gem template. **Root Switchable** is the pattern: screens optional, switcher reusable.

## Mount points, not whole gems

A gem may expose **several** mount points (user screens and a separate admin section). Each one navigates like a small app: enter, do the work, close or go back.

Per mount point: host mounts it → **section** (links to child jobs) → child screens → back/close to the hub that opened it. Mount points must not assume another gem’s chrome.

Use Recording Studio core’s **default layout** (back and close). Typical page: title, optional subtitle, optional buttons, then the form or content. One **primary action** per page.

Do not invent a competing shell, sidebar, or kitchen-sink dashboard. If several actions belong together, link them from the section and keep each on its own page.

## Do not

- Trap a reusable control inside a gem-only template.
- Treat the whole gem as one navigation stack when it has user and admin mounts.
- Fill a slice with unrelated actions so it “looks complete.”

## Related

`recording-studio-flatpack`, `recording-studio-text`, `recording-studio-api`, `recording-studio-admin`.
