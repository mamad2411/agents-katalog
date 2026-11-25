---
name: ui-appshell
description: Enforce AppShell Layout v3.0 (Header 52px, Sidebar 52/280, MobileBottom 72px, RWD).
---

## Hard rules
- Header fixed 52px, z-index 100
- Sidebar desktop expanded 280px collapsed 52px
- Mobile (<901px): Sidebar hidden, MobileBottom fixed 72px
- Header right order: WidgetEditControls(owner-only) -> Notifications -> Account
- Do not break existing routes/pages

## Output requirements
- Provide Desktop + Mobile layout notes
- Provide component list + state flow
