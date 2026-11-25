---
name: linkedin-onboard
description: Build the user's linkedin-brief.md in one pass so the whole engine runs in their voice and their market. Use first, before running any other skill.
argument-hint: "[your business + who you sell to + your offer + a paste of past posts/DMs]"
---

# LinkedIn Onboard

The setup pass. This skill assembles the one file every other skill reads: linkedin-brief.md. Run it once, in the user's own words and evidence, and the whole engine knows the voice, the market, and the offer.

## Inputs
- The user's business, who they sell to, their offer, and a paste of their past posts and DMs (the more real text, the better): $ARGUMENTS
- Nothing loads automatically yet. This skill is what creates the brief that loads from now on.

## Do this
1. Run /linkedin-icp-definer on the business and buyer details. Capture the ICP it returns: who, role, company shape, the trigger that makes them a fit.
2. Run /linkedin-voice-profiler on the pasted posts and DMs. Capture the voice profile: cadence, sentence length, words they reach for, words they never use.
3. Capture the offer in the user's language: one sentence (what it is), the outcome it produces, the proof behind it, and the risk reversal (the guarantee or the safety net).
4. Capture the top three to five buyer pains in the buyer's words, pulled from the paste where possible, not paraphrased into jargon.
5. Assemble all of it into one file and write it to linkedin-brief.md in the project root, with clear sections: ICP, Voice profile, Offer, Pains.

## Output
The assembled linkedin-brief.md (ICP, voice profile, offer, pains), shown in full for the user to confirm. End with a one-line note: the SessionStart hook will load this file into every session from now on, so no other skill will ask for this context again.

## Rules
- Build only from the user's real evidence and real words. If a section is thin because the paste was thin, say so and ask for more text rather than inventing it.
- The offer positions the user as a Revenue Partner who uses AI to do the heavy lifting. Never "AI consultant" or "AI agency".
- This is the file every other skill reads. Get it right before running anything else.
- No em-dashes. Draft first: show the assembled brief, the user confirms, then it is saved.
