---
name: apply-prefill
description: Drive a browser to pre-fill a job application - form fields, screening answers, the tailored CV - then stop and hand the keyboard back for human review. Never clicks Submit, Apply, or Send under any circumstances. Halts rather than guessing on any field it cannot answer from verified facts.
---

# Apply Prefill

Fills the form. Never sends it.

> ## HARD RULE
>
> **Never click Submit, Apply, Send, or Postuler. Ever.**
>
> This skill fills forms, prepares everything, and then stops with the completed form on screen
> for the human to review and send. No exceptions, even when asked to "just submit them all".
>
> This protects against terms-of-service bans, corrupted CAPTCHAs, and burned relationships with
> schools and partners that took years to build. An auto-submit path was added to an earlier
> version of this system once and removed the following day. It stays removed.

## Why halting matters more than filling

An agent that guesses on a form field is worse than no agent. A wrong self-assessed language
level, a fabricated salary expectation, or a fuzzy-matched dropdown becomes a written claim on a
real application, under a real person's name.

So this skill is built around the halts, not the fills.

## Load first

- `facts.md` — identity, education, experience. **Never invent a metric.**
- `profile.yml` — target roles, work authorisation wording, comp expectations
- The **`human-voice`** skill — any free-text the human "writes" must sound like them
- The `jd-analyser` positioning brief for this specific role

## Steps

### 1. Confirm the posting is live

Open the apply page in the user's real browser session, so their existing logins are used. A
page with only a navbar and footer means the role is closed. Stop and mark it discarded.

### 2. Read the whole form before typing anything

Enumerate every field, its type, whether it is required, and what would satisfy it. Produce a
plan. Show the plan before filling. A form read end-to-end first produces far fewer halts than
one filled top to bottom.

### 3. Fill what you can answer from verified facts

Standard fields come from `profile.yml`: name, email, phone, location, work authorisation,
languages, school. Attach the tailored CV built by `cv-tailor`.

Write screening answers and any motivation field in the human's voice, per `human-voice` Part 1.
**Surface every drafted answer to the user inline before typing it into the form.**

### 4. Halt on anything you cannot answer honestly

These halts exist to prevent fabrication. Do not weaken them.

| Halt | Fires when |
|---|---|
| `language_self_assessment` | A language level field. Never let a bot round A1 up to B2 |
| `salary_required` | A compensation field. The human's number, not an estimate |
| `low_confidence_answer` | A required question with no confident answer in `facts.md` |
| `photo_requested` | A photo upload. A photo is not a CV |
| `unclassified_upload` | A file field whose purpose is unclear |
| `ambiguous_select` | A dropdown with no exact match. **Never take a fuzzy first hit** |
| `unclassified_checkbox` | A checkbox whose meaning is not certain |
| `fill_verification_failed` | Wrote a value, read it back, got something else |
| `no_form_found` | No form on the page |
| `long_freetext` | A long motivation field. That is the human's voice, not the bot's |

On a halt: stop, name the halt, say exactly what you need, and wait.

### 5. Stop and hand over

Leave the completed form on screen. Tell the user precisely what is filled, what is not, and
what needs their input. They review. They send.

### 6. Log only after they confirm

Add the tracker row with status `Applied` only after the human confirms they sent it. Never
mark something applied because the form was filled.

## Credentials

**Never create a credentials file.** Use the user's existing logged-in browser profile. A YAML
of portal passwords sitting in a project directory is a worse answer than typing a password
once, and a far worse answer if that directory is ever committed.

If a persistent browser profile directory is used to keep sessions alive between runs, it must
be in `.gitignore` before the first run, not after.

## Honest limits

- Anti-bot protection on major boards can block automated fill entirely. Fall back to guiding
  the user click by click rather than forcing it.
- CAPTCHAs mean immediate hand-off. Do not attempt them.
- Quality beats volume. Five sharp applications beat fifty generic ones, and the part that
  converts is the fit narrative, which is the human's job.
