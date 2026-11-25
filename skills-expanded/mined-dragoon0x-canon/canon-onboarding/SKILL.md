---
name: canon-onboarding
description: Use when designing first-run experiences, product tours, coachmarks, progressive onboarding, or empty-state-as-onboarding. Covers the principles of gradual engagement, contextual hints over upfront tutorials, and when to use tours vs inline guidance vs empty states. Trigger when the user mentions onboarding, first-run, product tour, coachmark, walkthrough, or getting started.
---

# CANON · Onboarding

The best onboarding is the interface being obvious enough to not need onboarding. When that's not possible, teach in context, not upfront.

## Onboarding hierarchy (best to worst)

1. **Self-evident UI** — labels, layout, and flow are clear. No onboarding needed.
2. **Smart defaults** — pre-fill the first project, pre-select common settings.
3. **Empty states with guidance** — "No projects yet. Create one to get started."
4. **Contextual tooltips/coachmarks** — appear when the user first reaches a feature.
5. **Checklist** — "Complete your setup: ✓ Profile, ○ Team, ○ First project."
6. **Interactive walkthrough** — step-by-step guide within the product.
7. **Video/tutorial modal** — the fallback. Most users skip it.

## Principles

- **Earn before asking.** Don't ask for preferences before the user has experienced value.
- **Just-in-time over just-in-case.** Explain the feature when the user encounters it, not 12 screens earlier.
- **Progressive disclosure.** Reveal complexity as users demonstrate readiness.
- **Let users skip everything.** Every tour, modal, and tooltip must have a clear dismiss.
- **Never block the interface.** Overlays and modals that prevent exploration are anti-onboarding.

## Coachmarks

Small tooltips pointing to a UI element on first encounter.

- One at a time. Never 5 coachmarks on screen.
- Dismiss on click, after action, or after a few seconds.
- Don't re-show after dismissal (persist state).
- Position per `canon-tooltips` rules.

## Checklists

Work well for multi-step setup (profile, invite team, connect integration).

- Show progress (2 of 5 complete).
- Mark completed items visually (checkmark, strikethrough).
- Lead with the easiest step (quick win builds momentum).
- Allow out-of-order completion.
- Collapse or dismiss after completion.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| 5-screen carousel before the product | Users skip or forget by screen 3 |
| Mandatory video on first visit | Most users close immediately |
| Covering the entire UI with overlay instructions | Users can't explore |
| Asking for 10 preferences before showing value | Premature commitment |
| Coachmarks that can't be dismissed | Trapped |
| Re-showing dismissed tours | Annoying, shows disrespect |
| No skip option anywhere | Hostile to returning users |

## Audit checklist

- [ ] Interface is understandable without any onboarding
- [ ] Smart defaults reduce setup friction
- [ ] Empty states guide toward first action
- [ ] Coachmarks show one at a time and are dismissable
- [ ] Checklists show progress and allow out-of-order
- [ ] Every step is skippable
- [ ] Dismissed state persisted (don't re-show)
- [ ] No blocking modals before the user has seen the product

## Sources

- Samuel Hulick · UserOnboard teardowns
- Nielsen Norman · "Onboarding and First-Time Use"
- Intercom · "The Elements of User Onboarding"
