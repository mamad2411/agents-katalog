---
name: better-writing
description: "Interface copy: buttons, errors, empty states, confirmations, onboarding, microcopy. Use when adding or auditing UI text for clarity and consistency."
---

# Interface writing

Clear and brief beats clever; consistent beats varied. The best error message is an interaction redesigned so the error can't happen.

Read the nearby copy first: terminology, voice, localization conventions, any style guide. The product's existing voice wins. A deliberate brand voice is not a defect; flag it only when it causes inconsistency, ambiguity, translation risk, or a tone the stakes don't support. Rendering (capitalization via CSS, truncation) belongs to `better-typography`; error markup to `better-accessibility`.

## Tone follows the stakes

| Context | Tone |
| --- | --- |
| Success, onboarding, empty states | Warm, can be light |
| Routine actions, settings | Neutral, minimal |
| Errors, destructive confirmations | Calm, plain, no playfulness |
| Data loss, security | Serious, explicit |

## Defaults

- **One term per thing.** If the menu says "Archive", the toast doesn't say "Move to storage". A flow uses one vocabulary: "Get started", then "Continue" or "Next" (pick one), then "Done".
- **Address the reader as "you".** In errors, avoid "we" (reads as deflection): "Unable to load content". Possessives sparingly: "Favorites" over "Your Favorites".
- **Plain words** a tired reader gets on first pass. No idioms or humor that won't translate. Skip unneeded gender. Match the device: "tap" on touch, "click" with a pointer, "select" for both.
- **Buttons start with a verb**: "Save draft", "Delete project". No "OK!", "Let's go!", or bare "Yes"/"No" on consequential actions. A confirmation button repeats the consequence: "Delete this project?" offers `Delete project` and `Cancel`.
- **Links name their destination** and make sense out of context: "Read the billing docs", not "Click here". Multiple "Learn more" links get a suffix: "Learn more about exports".
- **One capitalization policy per element type.** Sentence case is the safer default. "Save Changes" next to "Discard changes" reads as sloppy.
- **Toggles describe the ON state**: "Send read receipts", not "Don't send read receipts". Link directly to a referenced setting instead of describing the path.
- **Placeholders are examples** (`name@example.com`, `DD/MM/YYYY`), never the only label.

## Errors

An error is an instruction placed beside the field that failed. Say how to fix it, phrase it positively, and show hints before the mistake when you can.

| Bad | Good |
| --- | --- |
| That password is too short | Choose a password with at least 8 characters |
| Invalid name | Use only letters for your name |
| Oops! Something went wrong. | Unable to save. Check your connection and try again. |

No blame, no "oops", no exclamation marks. If the same error keeps firing, redesign the interaction instead of rewording it.

## Empty states

Say what the place is, how it fills, and offer one next action: "No projects yet. Projects keep your tasks and files together. [Create a project]". Search and filter empties name the query and offer an exit: "No results for 'quarterly'. Clear filters". Don't park persistent information there; it disappears once content exists.

## Localization

Never build sentences from fragments around a variable (`"You have " + n + " new messages"`); word order changes per language. Use full templated strings with proper plural rules.

## Reporting

Severity: `HIGH` misleads or hides how to recover from an error; `MEDIUM` breaks voice, terminology or capitalization consistency; `LOW` is wording polish. Source alone is enough to verify. One row per root cause, ordered by severity:

| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |

End with `Block` if any `HIGH` remains, otherwise `Approve`. With nothing to report, say "No actionable writing findings".
