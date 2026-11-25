---
name: canon-brand-voice
description: Use when defining or auditing a product's written voice — the consistent personality across all UI copy. Covers voice vs tone, voice attribute definition, do/don't tables, and how to keep AI-generated copy on-brand. Trigger when the user mentions brand voice, tone of voice, writing style guide, copy guidelines, or product personality.
---

# CANON · Brand Voice

Voice is who you are. Tone is how you adapt to the moment. Voice stays the same across every screen; tone shifts based on context.

## Voice vs tone

| | Voice | Tone |
|---|---|---|
| Changes? | No — consistent everywhere | Yes — contextual |
| Example | "We speak plainly and directly" | Error: softer. Success: quieter. Onboarding: warmer. |
| Defined how | 3–5 attributes with do/don't pairs | Tone spectrum per context |

## Defining voice attributes

Pick 3–5 adjectives. For each, write a "this means" and a "this doesn't mean."

```
Voice attribute: Direct
This means: We say what we mean in as few words as possible.
This doesn't mean: We're rude, curt, or dismissive.

Voice attribute: Helpful
This means: Every message points to a next step.
This doesn't mean: We're patronizing or assume users are lost.

Voice attribute: Human
This means: We sound like a smart coworker, not a corporation.
This doesn't mean: We use slang, swear, or try to be funny in serious moments.
```

## Tone spectrum

Map tone to context:

| Context | Tone | Example |
|---|---|---|
| Success | Quiet, matter-of-fact | "Changes saved." |
| Error | Specific, supportive | "Couldn't connect — check your network and retry." |
| Onboarding | Warm, encouraging | "You're all set. Let's build something." |
| Destructive action | Direct, clear consequences | "Delete this project and all 47 files permanently." |
| Empty state | Inviting, action-oriented | "No projects yet. Create one to get started." |
| Loading | Informative if > 2s | "Setting up your workspace..." |

## Do/don't table template

| Do | Don't |
|---|---|
| "Couldn't save — connection lost" | "Oops! Something went wrong!" |
| "Changes saved" | "Success! Your changes have been saved successfully!" |
| "Delete project" (button label) | "Yes" |
| "3 items moved to trash. Undo" | "Are you sure you want to delete 3 items?" |
| Write in sentence case | Write In Title Case |
| Front-load the information | Bury the key info at the end |

## AI copy guardrails

When AI generates UI copy, it drifts toward generic patterns ("Oops!", "Something went wrong", "Click here to learn more"). Define banned phrases:

**Banned list (adapt per brand):**
- "Oops!" / "Whoops!" / "Uh oh!"
- "Something went wrong"
- "Please try again later"
- "Click here"
- "Welcome back!" (unless you know them by name)
- "We're sorry for the inconvenience"
- Exclamation marks in errors
- "Leverage" / "utilize" / "empower" / "unlock"

## Audit checklist

- [ ] 3–5 voice attributes defined with do/don't pairs
- [ ] Tone spectrum covers success, error, onboarding, destructive, empty, loading
- [ ] Banned phrase list exists
- [ ] Button labels follow `canon-ux-writing` (verbs, sentence case)
- [ ] Error messages follow `canon-ux-writing` (what/why/how)
- [ ] Copy reviewed against voice attributes before shipping

## Sources

- Nielsen Norman · "Voice and Tone in UX Writing"
- Mailchimp Content Style Guide (voice/tone framework)
- Shopify Polaris · Voice and tone
- `canon-ux-writing` for execution-level rules
