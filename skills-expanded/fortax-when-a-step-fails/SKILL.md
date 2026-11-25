---
name: fortax-when-a-step-fails
description: When a portal rejects something, an upload bounces, a submit times out, a figure will not tie, the engine returns an error, or a step that worked last month breaks - stop, keep the exact error text, find the cause on a triage ladder (did it fail, session, input, portal, data, us), fix the cause, change the approach instead of retrying blind, and never touch a submit or payment that may have gone through. Typical asks - "error aa raha hai", "upload nahi ho raha", "submit ke baad page atak gaya", "figure tie nahi ho raha", "pichhle mahine chal gaya tha, ab nahi".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "Stop-the-line and triage-ladder discipline adapted from the debugging skill in addyosmani/agent-skills, https://github.com/addyosmani/agent-skills (MIT)"
---

# When a step fails

## Stop the line

The moment something does not go as expected:

1. **Pause.** Do not retry blindly, do not move to the next client, do not carry on with the rest of
   the job until you know why.
2. **Keep the evidence.** A screenshot of the screen as it is, and the portal's (or the engine's)
   error text quoted exactly, in its own words. Paraphrasing an error destroys the one clue you have.
3. **Work out the cause** using the ladder below.
4. **Fix the cause**, not the symptom.
5. **Write the trap down** so the next run does not hit it.
6. **Only then carry on.**

A blind retry is the most expensive thing you can do here. On a government portal the same action
twice is not harmless: it can produce two applications, two challans, or a second return against a
period that already has one.

## The rule that outranks everything else

**If the failed step was a Submit, a File, a Pay, or anything after the CA's authentication (OTP,
EVC, DSC), do not touch it again. At all.**

You do not know from the error whether it went through. A timeout after a submit very often means the
filing succeeded and only the response was lost. Retrying produces a duplicate, and a duplicate return
or a duplicate payment takes a letter and weeks to undo.

Stop, and tell the CA in plain words:

> The submit for GSTR-1, Sharma Traders, August 2026, timed out. It may or may not have gone through.
> Please check the return status on the portal before anything else is done for this client.

Then wait. This is one of the few places where the right answer is to do nothing. (The final click
is the CA's anyway — see `fortax-portal-work` — but the same holds when the CA clicked and the page
hung: nobody clicks it again until the status is checked.)

## The ladder

Work down it. Each rung is a fact you can confirm, not a theory.

| Check | How you confirm it |
|---|---|
| **Did it actually fail?** | Some portals print a red banner on success, or show a validation warning that is not an error. Read the page, not the colour. |
| **Has the session gone?** | The commonest cause by far. A page that suddenly asks for login, or silently empties a form, has timed out. Ask the CA to sign in again and start that screen fresh. |
| **Is it the input?** | Date format, a character the field rejects, a file over the size cap, a wrong extension, a PAN in lower case, a decimal where the field wants a whole number. For the engine: a column not recognised (the summary names it — rerun with `--map`), `--fp` not MMYYYY, a file over 25 MB, a PDF or old binary .xls where CSV/xlsx is needed. |
| **Is it the portal (or the service)?** | Maintenance windows, due-date load, a known outage. Try a different page on the same site. If nothing loads, it is them, and the answer is to wait, not to retry in a loop. "Could not reach the Fortax engine" is the same rung: check the connection, then wait. |
| **Is it the data?** | The department holds something different: a cancelled GSTIN, an address that does not match, a return for a period already filed, a supplier who has not filed. A 2B for another GSTIN or month, which the engine refuses or flags. |
| **Is it us?** | Wrong field, wrong tab, wrong client folder, a figure read off the wrong row, the wrong period. Check this before blaming the portal, not after. |

Stop at the first rung that explains what you saw. Do not stack two explanations.

## Try another way, never the same way

Where the ladder gives you a cause you can fix without the CA — a date format, a file that needs
converting, a column map — fix it and take the step again. An expired session needs the CA to sign in
again; ask, then continue.

If it fails again, do not repeat the attempt. **Change the approach**: a different menu path to the
same screen, a fresh sign-in by the CA, the portal's offline utility or JSON upload instead of the
online form, the other tab, waiting out a maintenance window and coming back. Each attempt must
differ from the last in a way you can name. Keep going until the job is done or the CA stops you.

Three genuinely different routes that all land on the same wall means the wall is not the portal:
you are missing an input, and the CA needs to hear exactly which one. Repeating the same click is not
persistence; on a portal it is how an account gets locked and how a second application gets filed.

A figure that will not tie is the same discipline: do not force it with a plug entry or a rounding.
Find the rung (wrong period, missing rows, a credit note sign, a duplicate) or report the exact
difference and where it sits.

## Write the trap down

A cause you found and did not record will cost the same hour next month. When the portal task has a
procedure, add the trap to it as an instruction, not as a story:

> Upload the rent agreement as a PDF under 1 MB. The portal accepts a larger file and then fails
> silently at the next step.

(An illustration of the form of a trap note; record what the site actually did.) If the portal has no
procedure yet, write one as described in `fortax-portal-work` (learn a portal).

## What the CA gets

Not "it failed". A short note they can act on:

- The step, the client and the period.
- The portal's or engine's own words, quoted.
- What you checked and ruled out.
- What you think the cause is, and how sure you are.
- The one thing you need from them, if anything.

And if there is any chance a filing or a payment went through, that goes **first**, in its own
sentence, before anything else in the message.

## Attribution

The stop-the-line and triage-ladder discipline is adapted from the debugging skill in
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT), rewritten here for portal
and filing work. No code from that project is used.
