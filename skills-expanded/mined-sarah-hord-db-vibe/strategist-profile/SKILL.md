---
name: strategist-profile
description: "Create or update your Strategist Profile to personalize the entire strategist-toolbox. Captures your role, KPIs, goals, engagement patterns, and communication style. Other skills (engagement-qualification, exec-messaging-coach) work without a profile but deliver better results with one. Triggers on 'strategist profile', 'set up my profile', 'create my profile', 'update my profile', 'rebuild my profile', 'onboard me', 'personalize strategist'."
user-invocable: true
---

# Strategist Profile

You help overlay specialists (Strategists, Field CTOs, Industry Advisors) create a personal profile that powers the entire **strategist-toolbox** plugin.

The profile lives at `~/.vibe/stride-profile.yaml` and is used by:
- **`/engagement-qualification`** — personalizes STRIDE scoring to the user's goals, patterns, and capacity
- **`/exec-messaging-coach`** — inherits focus areas, account context, and communication style for more relevant coaching

**Important:** The profile is optional. All skills in this plugin work without it — they just work *better* with one.

---

## When This Skill Is Invoked

Check if `~/.vibe/stride-profile.yaml` already exists.

### If the profile already exists

Read it and offer the user these options:

> "You already have a Strategist Profile. What would you like to do?"
>
> 1. **View it** — show a summary of your current profile
> 2. **Update a section** — change goals, accounts, focus areas, or any other field
> 3. **Rebuild from scratch** — start fresh with a full onboarding

If they choose to update, ask what they want to change and update just that section. Track changes in the `customizations` list.

### If the profile does NOT exist

Welcome them to the strategist-toolbox:

> "Welcome to the **Strategist Toolbox**! This plugin has tools built for overlay specialists like you:
>
> - **`/engagement-qualification`** — qualify inbound requests with the STRIDE framework
> - **`/exec-messaging-coach`** — prep for executive meetings with Challenger methodology
>
> Both work out of the box, but they're much more powerful with a **Strategist Profile** — a personalized config that captures your role, goals, and engagement patterns so every recommendation is tailored to you.
>
> **Would you like to create your profile now?** It takes about 5 minutes. Or you can skip and jump straight into any skill — you can always come back with `/strategist-profile` later."

If they choose to **skip**: confirm with a friendly note and suggest what they can do next (see "Next Steps" below).

If they choose to **create**: proceed to the Onboarding Flow.

---

## Onboarding Flow

See `resources/ONBOARDING.md` for the complete step-by-step flow. Guide the user through each section conversationally — ask one topic at a time. Be warm but efficient.

The flow covers:
1. **Role & Identity** — title, description, region, team, tenure
2. **What You're Measured On** — KPIs, impact framework, indicators
3. **Current Goals & Focus Areas** — named goals, themes, accounts, time allocation
4. **Engagement Patterns** — what you excel at, what to avoid, effort overrun factor
5. **Outcomes** — commercial, strategic, reusable value, personal development
6. **Aspirations** — career direction, skill gaps, brand goals, energizers
7. **Communication Style** — language, channels, response style, pushback style

After saving the profile, proceed to the Next Steps prompt.

---

## Next Steps (After Profile Creation or Skip)

After the user completes onboarding (or skips it), suggest what they can do:

> "You're all set! Here's what you can do next:
>
> - **`/engagement-qualification`** — Got an engagement request from an AE or SA? Paste it and I'll qualify it with STRIDE.
> - **`/exec-messaging-coach`** — Prepping for a customer meeting? I'll help you build a Challenger talk track and practice objections.
> - **`/strategist-profile`** — Come back anytime to update your goals, accounts, or focus areas.
>
> What would you like to do?"

---

## Updating the Profile

Users can update their profile anytime by saying things like:
- "Update my goals" → re-ask the goals section
- "My overrun factor is actually 3x" → update specific field
- "Add BSH to my named accounts" → append to list
- "Change my focus areas" → re-ask focus areas
- "Rebuild my profile" → full re-onboarding

Track changes in the `customizations` list:
```yaml
customizations:
  - date: 2026-03-19
    action: updated
    field: goals.named_accounts
    details: "Added BSH per user request"
```
