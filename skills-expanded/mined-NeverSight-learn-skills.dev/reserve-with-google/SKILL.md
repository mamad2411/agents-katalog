---
name: reserve-with-google
description: >
  Book reservations through Google Maps using browser automation. Searches for
  businesses, checks availability, and completes bookings via "Reserve with Google"
  or 3rd-party providers (OpenTable, Resy, Vagaro). Supports restaurants (primary),
  salons, fitness, healthcare. Use when user wants to book, reserve, or schedule
  at a business found on Google Maps.
license: MIT
compatibility: Requires agent-browser CLI (npx agent-browser), internet access
metadata:
  author: eliehabib
  version: "1.0"
  category: booking
allowed-tools: Bash(agent-browser:*)
---

# Reserve with Google

Automate restaurant reservations and business bookings through Google Maps using browser automation.

## Quick Reference

| Provider | Booking URL Pattern | Special Notes |
|----------|---------------------|---------------|
| **SevenRooms** | `sevenrooms.com/reservations/{venue}` | See [SEVENROUNDS.md](references/SEVENROOMS.md) |
| OpenTable | opentable.com | Use `--headed` for best results |
| Resy | resy.com | Often requires phone verification |
| Yelp | yelp.com/reservations | Login usually required |

**Common Issues:**
- Title dropdown: Use `find text "Mr." click`
- Policy checkbox: Use `find text "I agree..." click`

## Prerequisites

- `agent-browser` installed: `npm install -g agent-browser`
- Internet access
- Optional: Pre-authenticated Google profile (see Profile Setup below)
- Optional: Proxy server for authenticated routing (see Proxy Setup below)

## Before Starting

Collect from the user:
1. **Search query** — what/where to book (e.g., "Italian restaurants in downtown Chicago")
2. **Date** — desired reservation date
3. **Time** — preferred time
4. **Party size** — number of guests (restaurants)
5. **Name** — for the reservation
6. **Phone** — contact number
7. **Email** — confirmation email
8. **Special requests** — optional (e.g., "window seat", "high chair needed")

## Profile Setup (One-Time)

For best results, set up a persistent browser profile with a logged-in Google account:

```bash
agent-browser --headed --profile ~/.reservegoogle open "https://accounts.google.com"
```

The user logs in manually once. The profile persists across sessions. If no profile exists, fall back to guest mode.

Alternative: Use state save/load for portable auth:

```bash
# After logging in:
agent-browser state save ~/.reservegoogle-auth.json

# In future sessions:
agent-browser state load ~/.reservegoogle-auth.json
agent-browser open "https://www.google.com/maps"
```

## Proxy Setup

Route traffic through an authenticated proxy to avoid rate limits, geo-restrictions, or use residential IPs:

```bash
agent-browser --proxy http://user:pass@proxy.example.com:8080 open "https://www.google.com/maps"
agent-browser --proxy socks5://user:pass@proxy.example.com:1080 open "https://www.google.com/maps"
```

The proxy flag only needs to be passed on the `open` command that starts the session. Subsequent commands in the same session reuse the proxy.

Combine with profile for authenticated + proxied sessions:

```bash
agent-browser --headed --profile ~/.reservegoogle --proxy http://user:pass@proxy.example.com:8080 open "https://accounts.google.com"
```

Set via environment variable to avoid passing on every command:

```bash
export AGENT_BROWSER_PROXY="http://user:pass@proxy.example.com:8080"
agent-browser open "https://www.google.com/maps"
```

## Core Workflow

**CRITICAL**: Always use `snapshot` before every interaction. Refs change on every page update. Never hardcode element references.

### Step 1: Open Google Maps & Search

```bash
agent-browser --profile ~/.reservegoogle open "https://www.google.com/maps"
agent-browser snapshot -i
```

Find the search box in the snapshot, then:

```bash
agent-browser fill @<searchBoxRef> "<user's search query>"
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser snapshot -i
```

Parse the results list. Present places to the user with indicators of which ones have booking available (look for "Reserve a table", "Book online", or similar text in results).

### Step 2: Select a Place

After user picks a place:

```bash
agent-browser click @<resultRef>
agent-browser wait --load networkidle
agent-browser snapshot -i
```

Look for booking buttons in the snapshot. Common text patterns:
- "Reserve a table"
- "Book online"
- "Book an appointment"
- "Schedule"
- "Find a table"

If NO booking button found: inform the user this place doesn't support online booking. Suggest nearby alternatives from the search results.

### Step 3: Initiate Booking

```bash
agent-browser click @<bookButtonRef>
agent-browser wait --load networkidle
```

Detect what happened:

**Check URL** with `agent-browser get url`:
- Still on `google.com/maps` → Google-native widget or iframe
- `opentable.com` → OpenTable flow (see [THIRD-PARTY-PROVIDERS.md](references/THIRD-PARTY-PROVIDERS.md))
- `resy.com` → Resy flow
- `vagaro.com` → Vagaro flow
- `yelp.com/reservations` → Yelp flow
- `toasttab.com` → Toast flow
- Other domain → Generic 3rd-party flow

**Check for iframes**: If the booking widget loaded in an iframe:
```bash
agent-browser snapshot -i
```
If you see an iframe element in the snapshot, identify its CSS selector (e.g., `id` or `name` attribute), then switch into it:
```bash
agent-browser frame "#booking-iframe"
agent-browser snapshot -i
```
To return to the main frame after interacting with the iframe:
```bash
agent-browser frame main
```

### Step 4: Select Date, Time & Party Size

Take a snapshot to identify the booking form elements:

```bash
agent-browser snapshot -i
```

For restaurants, look for:
- **Date picker**: calendar widget or date dropdown
- **Time slots**: buttons or dropdown with available times
- **Party size**: number input, dropdown, or +/- buttons

Fill in the user's preferences:

```bash
agent-browser click @<datePickerRef>
# Navigate to correct date in calendar
agent-browser click @<targetDateRef>
agent-browser click @<timeSlotRef>
agent-browser fill @<partySizeRef> "<count>"
```

If the preferred time is unavailable, snapshot again and present available alternatives to the user.

### Step 5: Fill Personal Information

```bash
agent-browser snapshot -i
agent-browser fill @<nameFieldRef> "<user's name>"
agent-browser fill @<phoneFieldRef> "<user's phone>"
agent-browser fill @<emailFieldRef> "<user's email>"
```

If there's a special requests field:
```bash
agent-browser fill @<specialRequestsRef> "<user's requests>"
```

Snapshot to verify all fields are populated correctly.

### Step 6: Confirm Before Submitting

**MANDATORY**: Before clicking the final booking button, present the user with a summary:

```
Booking Summary:
- Place: [restaurant name]
- Date: [date]
- Time: [time]
- Party size: [count]
- Name: [name]
- Special requests: [if any]

Confirm this booking?
```

Only proceed after user confirms.

### Step 7: Complete Booking

```bash
agent-browser click @<confirmButtonRef>
agent-browser wait --load networkidle
agent-browser snapshot -i
```

Look for confirmation indicators:
- "Reservation confirmed"
- "Booking confirmed"
- Confirmation number/code
- "You're all set"

Take a screenshot for the user's records:
```bash
agent-browser screenshot confirmation.png
```

Report to the user:
- Confirmation status
- Confirmation number (if shown)
- Date/time/party size confirmed
- Any special instructions from the restaurant

## Error Handling

### CAPTCHA Detected
Inform the user: "Google is showing a CAPTCHA. Please complete it manually." Wait for user to resolve, then continue.

### Slot No Longer Available
Re-snapshot, show remaining available slots, ask user to pick another.

### Payment Required
Inform the user: "This booking requires payment. I cannot enter payment details. Please complete payment manually." Take a screenshot showing the payment page.

### No Availability
Suggest: different date/time, nearby similar restaurants, or trying again later.

### Multiple Booking Options
If the place offers multiple booking types (dine-in, takeout, waitlist), ask the user which one before proceeding.

## Session Management

Use `--session` for parallel searches:
```bash
agent-browser --session search1 --profile ~/.reservegoogle open "https://www.google.com/maps"
```

## Reference Files

- [Detailed element patterns & flow docs](references/REFERENCE.md)
- [Form templates by business type](references/FORMS.md)
- [3rd-party provider specific flows](references/THIRD-PARTY-PROVIDERS.md)

---

# Lessons Learned (Feb 2026)

## SevenRooms-Specific Patterns

The SevenRooms booking system (used by many restaurants) has unique quirks:

### Title Dropdown Issue
**Problem:** Clicking the select button (`@e2`) doesn't always reveal options in a way `agent-browser` can interact with.

**Solution:** Use text-based selection instead:
```bash
agent-browser find text "Mr." click
```

For ambiguous matches (multiple "Mr." elements):
```bash
agent-browser find text --exact "Mr." click
```

### Policy Checkbox Detection
**Problem:** The "I agree to the venue's required policy *" checkbox element isn't exposed in snapshots as a standard checkbox.

**Solution:** Click the policy text directly:
```bash
agent-browser find text "I agree to the venue's required policy" click
```

### Form Session Timeout
**Problem:** Many booking systems (including SevenRooms) hold a table for ~20 minutes. If you take too long filling forms, the hold expires and you must re-select.

**Solution:**
- Fill forms quickly without overthinking
- Re-selection flow: Back → re-select time → Continue as Guest → title → fill fields → policy → Submit

### Form Field Reset Behavior
**Observation:** Title may persist across session resets, but First Name, Last Name, Email, and Phone fields typically clear.

**Solution:** Always verify and refill all form fields before final submission.

### Faster Booking Script
For repeat bookings at the same venue:
```bash
# Open booking page
agent-browser open "https://www.sevenrooms.com/reservations/restaurantname"

# Select date/time/guests → SEARCH
agent-browser snapshot -i
agent-browser click @<dateRef>
agent-browser click @<timeRef>
agent-browser fill @<partySizeRef> "3"
agent-browser click @<searchButtonRef>
agent-browser snapshot -i

# Click desired time slot
agent-browser click @<timeSlotRef>

# Quick guest flow
agent-browser find text "Continue as guest" click
agent-browser click @<selectTitleRef>
agent-browser find text "Mr." click

# Fill and submit
agent-browser fill @<firstNameRef> "John"
agent-browser fill @<lastNameRef> "Doe"
agent-browser fill @<emailRef> "john.doe@example.com"
agent-browser fill @<phoneRef> "+1234567890"
agent-browser find text "I agree to the venue's required policy" click
agent-browser click @<submitRef>
```

### Element Reference Changes
**Critical:** Element references (`@e1`, `@e2`, etc.) change on EVERY page load or interaction. Always run `snapshot` immediately before clicking.

### Error Recovery Patterns
If submit fails or hold expires:
1. Check console logs: `agent-browser console`
2. Look for "Released hold" messages (indicates timeout)
3. Back out to time selection: `agent-browser click @<backRef>`
4. Re-select same time slot
5. Continue from guest flow
