---
name: script-video-generate
description: Preflight, price, submit, monitor, and preserve one approved generative video job. Use only after a shot packet and spend boundary have been approved.
---

# Script Video Generate

One call of this skill handles one approved paid job. Duplicate prevention is part of production quality.

## Required packet

Require shot ID, attempt ID, model, duration, resolution, aspect ratio, start/end/continuation references, exact prompt, sound instruction, live quote, and pass criteria.

## Workflow

1. Read the current shot tracker, continuity records, and provider runbook.
2. For Higgsfield work, read the current `higgsfield` root skill and its routed model, prompt,
   audio, and stack guidance, then inspect the live model schema and quote through the official CLI.
3. Compare them with the approved packet. Stop on any material drift.
4. Create a unique local job ledger entry before submission.
5. Confirm no matching job or provider ID already exists.
6. Submit exactly once after explicit approval tied to the final quote.
7. Record provider job ID, submission time, settings, prompt hash, reference hashes, and quote.
8. Monitor the existing job. Never resubmit merely because status is slow or unclear.
9. Download the raw result into `footage/raw/` without overwriting.
10. Hash and probe it, then update the ledger.
11. Send the take to `$script-video-review`.

If the result contains a useful approved range followed by a local failure, preserve the raw take
and let review decide whether a deterministic hold, insert, crop, or retime can cover the interval.
Do not spend on a retry before salvage is evaluated.

## Prompt shape

Describe subject, single primary action, environment, camera, lighting, temporal progression, constraints, and native diegetic SFX. Keep narration and music separate unless the approved model workflow explicitly requires them.

## Stop conditions

Stop before submission if the quote changed, required references are missing, duration is unsupported, the prompt conflicts with the shooting script, or approval is ambiguous.

Do not approve the take, edit it, upscale it, or create a retry. Review decides the next action.
