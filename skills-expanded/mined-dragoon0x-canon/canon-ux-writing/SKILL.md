---
name: canon-ux-writing
description: Use when writing or auditing interface copy, button labels, error messages, empty states, onboarding, microcopy, tooltips, or any text inside an interface. Covers tone, voice, button-label patterns, error-message construction, empty state copy, and the most common UX writing anti-patterns. Trigger when the user mentions copy, microcopy, button text, error message, empty state, onboarding, tone, or voice.
---

# CANON · UX Writing

Interface copy is design. A 4-word button label is a design decision. A confusing empty state breaks an otherwise polished product. The rules below produce copy that disappears into use.

## Core Principles

1. **Verbs over nouns.** Buttons describe actions: "Create account", not "Account creation".
2. **Specific over generic.** "Send invoice" beats "Submit". "Email is required" beats "Invalid input".
3. **Active voice over passive.** "We sent your invoice" beats "Your invoice has been sent".
4. **Plain words over jargon.** "Sign in" beats "Authenticate". "Try again" beats "Retry operation".
5. **User's language over yours.** "Posts" not "Resources" if your users say "posts".
6. **Sentence case over Title Case.** Reads faster, feels modern. Use Title Case only for proper nouns and product names.

## Button Labels

| Bad | Good |
|---|---|
| Submit | Send message / Create account / Save changes |
| OK | Got it / Continue / Done |
| Cancel | Cancel (this one is fine) / Discard / Keep editing |
| Click here | (link should describe destination) |
| Learn more | Read the security guide |
| Yes / No | Save changes / Discard |
| Continue | Continue to payment |

**Rule: button label = verb + object when possible.** "Save", "Save profile", "Save and continue".

### Button Pairs (confirm/cancel)

| Context | Primary | Secondary |
|---|---|---|
| Saving | Save changes | Cancel |
| Discarding | Discard changes | Keep editing |
| Destructive | Delete project | Cancel |
| Confirming | Yes, sign me out | No, stay signed in |

**Destructive actions always require explicit confirmation language.** "Delete" alone, with the user already on a delete confirmation modal, is acceptable. "Delete project" is better.

### Button Tone by Context

| Context | Tone |
|---|---|
| Marketing CTA | Bold, benefit-focused: "Start free trial" |
| App primary action | Direct, action-focused: "Save changes" |
| Destructive | Clear and confirming: "Delete forever" |
| Loading state | Present continuous: "Saving…", "Sending…" |
| Success state | Past tense: "Saved", "Sent" |

## Error Messages

Three parts: **what happened, why, how to fix.**

```
What:  "We couldn't send your message."
Why:   "Your internet connection dropped."
Fix:   "Check your connection and try again."
```

Concatenated for short use: "We couldn't send your message. Check your connection and try again."

| Bad | Good |
|---|---|
| Error | We couldn't load your projects. Try refreshing. |
| Invalid input | Enter a valid email. Example: name@example.com. |
| Failed | Couldn't save changes. Check your connection and retry. |
| Required | Email is required. |
| Wrong | Password must be at least 8 characters. |
| Network error | We're having trouble reaching our servers. Try again in a moment. |
| 500 | Something went wrong on our end. We're looking into it. |
| 404 | We couldn't find that page. It may have been moved or deleted. |

**Error tone rules:**
- Don't blame the user. "You entered an invalid email" → "Enter a valid email".
- Don't catastrophize. "Fatal error" → "Something went wrong".
- Don't be apologetic past necessity. "We're so sorry, this is terrible" → "Something went wrong".
- Be specific about the cause when you know it. "Invalid input" hides what's wrong.

## Empty States

Every list, table, search, and dashboard has an empty state. Plan for it.

| Empty type | Pattern |
|---|---|
| First-time empty (no data ever) | Brief explanation + CTA to create first item |
| User-cleared empty (deleted everything) | Confirmation that the area is empty + restore option if applicable |
| Search empty (no results) | "No results for '[query]'" + suggestions to refine |
| Filter empty (filters too narrow) | "No results match your filters" + "Clear filters" button |
| Loading empty (data still fetching) | Skeleton, not "No data" |

```
Empty state structure:
  1. Visual (illustration, icon, or just typography)
  2. Headline (4-8 words, what's empty)
  3. Description (1 sentence, why and what next)
  4. Primary action (button to fix or create)
  5. Optional secondary (learn more, alternative)
```

### Empty State Examples

**No projects yet (first-time):**
```
[icon]
You don't have any projects yet
Projects help you organize work into separate spaces.
[+ Create your first project]
[Read the guide]
```

**No search results:**
```
No results for "octopus"
Try a different search, or check your spelling.
[Clear search]
```

**No notifications:**
```
You're all caught up.
```

(Sometimes one line is enough.)

## Loading States

| Wait | Copy |
|---|---|
| < 400ms | (none — instant feels best) |
| 400ms–2s | "Loading…" or skeleton |
| 2s–10s | "Loading [thing]…" with what specifically |
| > 10s | "This is taking longer than usual…" + estimated remaining if known |

**Use "…" (ellipsis character) or "...".** Be consistent. Don't mix.

## Confirmation and Success

| Action | Confirmation |
|---|---|
| Save | "Saved" (toast, dismisses in 3s) |
| Send | "Message sent" |
| Delete | "Project deleted" + "Undo" (5s window) |
| Copy | "Copied to clipboard" |

**Always offer Undo for destructive actions.** A 5-second toast with Undo is more humane than a confirmation dialog before the action.

## Tone and Voice

### Voice (consistent across product)

Pick a position and stay there:
- **Direct and minimal.** Apple, Linear, Vercel. Few words, no exclamation marks, no emojis.
- **Warm and human.** Mailchimp, Slack, Notion. Conversational, occasionally playful, careful with humor.
- **Helpful and educational.** Stripe docs, GitHub. Patient, thorough, links to deeper context.
- **Bold and confident.** Notion-pre-2020, Superhuman. Strong opinions, brief.

### Tone (varies with context)

| Context | Tone |
|---|---|
| Onboarding | Welcoming, encouraging |
| Routine actions | Neutral, efficient |
| Errors | Calm, reassuring, concrete |
| Destructive confirmations | Serious, clear |
| Success | Brief, satisfying |
| Marketing | Persuasive, benefit-focused |

**Rule: tone bends to context, voice stays constant.** Your error messages and your marketing copy should sound like the same product.

## Microcopy Patterns

### Form Hints

| Bad | Good |
|---|---|
| (none) | We'll never share your email. |
| Password | At least 8 characters with one number. |
| Phone | Include country code, e.g., +1 555 555 1234. |
| Name | (often no hint needed) |

### Permission Requests

| Bad | Good |
|---|---|
| Allow notifications? | Get notified when someone replies to your post |
| Use camera? | Take a photo to add to your profile |
| Access location? | Show events near you |

**Explain the benefit before the prompt.** Most users deny generic permission requests; specific benefit increases acceptance.

### Onboarding Copy

| Bad | Good |
|---|---|
| Welcome to our platform | (use product name) |
| Let's get started! | (skip, just start) |
| Tell us about yourself | Help us personalize your experience (with explanation of what's used) |

**Onboarding rule: every step justifies itself.** "We need this because…" or skip the step entirely.

## Accessibility Considerations

- Don't say "click here" — screen reader users navigate by link text out of context.
- Don't use color or icon alone for status — pair with text.
- Use plain English at a 7th–9th grade reading level (Hemingway, Flesch-Kincaid).
- Don't use idioms or culturally-specific references in international products.

## Numbers, Dates, Currency

| Pattern | Example |
|---|---|
| Currency | $1,299.00 (en-US), 1.299,00 € (de-DE) |
| Large numbers | "1.2M users" preferred to "1,234,567 users" in dashboards |
| Dates (relative, recent) | "2 hours ago", "yesterday" |
| Dates (absolute, distant) | "Mar 14, 2026" not "03/14/26" (ambiguous) |
| Time | "2:30 PM" (US) or "14:30" (24-hour) — match user locale |
| Percentages | Round to 1 decimal in dashboards: "12.4%" |

**Use Intl APIs for formatting:** `Intl.NumberFormat`, `Intl.DateTimeFormat`. Never hardcode locale formats.

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| "Submit" button | Generic | Use the verb |
| "Click here" link | Useless out of context | Describe destination |
| "Error" with no detail | User stuck | What/why/how |
| "Invalid input" | Doesn't say what's invalid | Specific |
| All caps for emphasis | Reads as shouting | Use weight or color |
| Multiple exclamation marks | Childish | Maximum one, sparingly |
| Emojis in error messages | Wrong tone | Save for celebrations |
| "Please" before everything | Verbose | "Save" not "Please save" |
| "Sorry for the inconvenience" | Empty apology | Fix the issue, brief acknowledgement |
| Title Case Buttons | Slow to read | Sentence case |
| ALLCAPS HEADINGS | Slow to read | Use weight |
| "We" voice from a single-user product | Confusing | Match voice to product |
| Marketing tone in error messages | Off-key | Calm, helpful |
| Truncated text without context | User can't tell what's hidden | Tooltip on hover/focus or "more" link |
| "Coming soon" with no date | Frustrating | Date or remove the mention |

## Decision Tree

```
Writing a button label?
├─ Verb + object: "Save changes", "Send message", "Delete project"
├─ Sentence case
├─ Loading state: present continuous ("Saving…")
└─ Success state: past tense ("Saved")

Writing an error?
├─ What happened (in the user's terms)
├─ Why (if helpful)
├─ How to fix (most important)
├─ Tone: calm, not alarming
└─ Don't blame the user

Writing an empty state?
├─ Headline: 4-8 words, what's empty
├─ Description: 1 sentence why
├─ Primary action: how to fix or create
└─ Skip if "You're all caught up" suffices
```

## Audit Checklist

1. List every button label. Replace "Submit", "OK", "Click here" with verbs.
2. List every error message. Each has what + how to fix? Tone calm?
3. List every empty state. Each has headline + description + action?
4. Check for "click here" anywhere. Replace with descriptive link text.
5. Check sentence case vs Title Case. Consistent?
6. Check loading copy. Present continuous? Indicates what's loading?
7. Check destructive actions. Have Undo or explicit confirmation?
8. Check tone consistency. Marketing copy and error copy sound like same product?
9. Check exclamation marks. Maximum one per page?
10. Check Intl formatting for dates, numbers, currency.

## Citations

- Apple HIG Writing: https://developer.apple.com/design/human-interface-guidelines/writing
- Material Design 3 Writing: https://m3.material.io/foundations/content-design/style-guide/writing-principles
- GOV.UK Style Guide: https://www.gov.uk/guidance/style-guide
- Mailchimp Content Style Guide: https://styleguide.mailchimp.com
- Microsoft Writing Style Guide: https://learn.microsoft.com/en-us/style-guide/welcome/
- Nielsen Norman Group, Microcopy: https://www.nngroup.com/articles/microcopy/
- Strunk and White, *The Elements of Style*
- Sarah Richards, *Content Design*
