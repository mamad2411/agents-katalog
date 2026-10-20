---
name: ux-law-jakob-consistency
description: Use when designing a new pattern (navigation, icon meaning, gesture, form layout) and deciding whether to invent something new or follow convention — Jakob's Law (users spend most of their time on other sites/apps and expect yours to work the same way). Triggers on "should we invent our own pattern", "non-standard navigation", "custom icon for a common action", "onboarding new UI pattern".
allowed-tools: Read, Edit, Grep, Glob
---

# Jakob's Law

Users transfer expectations from every other product they've used. Default to established conventions (hamburger menu, cart icon, trash icon = delete, pull-to-refresh, breadcrumbs) unless deviating produces a measurable, justified improvement.

## Rules of thumb
- Reuse the platform's native patterns first (iOS/Android/web conventions) before inventing.
- Novel interaction patterns cost onboarding/learning time — only justified when they solve a real friction the standard pattern doesn't.
- When you must deviate, add a lightweight affordance/hint the first time a user hits it (tooltip, coachmark), not a full tutorial.
- Check competitor/reference apps in the same domain for the pattern users likely already know from that specific task (e.g., checkout flow, file upload).

## Review checklist
1. Is this pattern one the user has likely seen elsewhere doing the same job?
2. If not, is the deviation earning its learning cost?
3. Is there a hint for first-time encounters with the novel pattern?
