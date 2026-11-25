---
name: wreck-personas
description: Derive realistic user personas (the app's ideal customers plus built-in normal-user, rushed-beginner and chaos-monkey) and their missions for wreck-it testing, saved to .wreck-it/personas.md. Use as stage 3 of a wreck-it run, or when the user asks "who would use my app", "make test personas", or wants to edit the personas used for testing.
---

# wreck-personas

`WRECK` means `npx @miyanishar/wreck-it`.

Output: `.wreck-it/personas.md`. The user may edit this file. If it already exists, **reuse it unchanged** and just summarize it. Regenerate only when the user asks.

## Inputs

Read these. Skim them, don't study them.
- `README*`, landing/home page copy (open the home page in the browser), `package.json` description
- `.wreck-it/discovery.json`: pages, API routes, forms, auth
- The database schema, if one exists (`prisma/schema.prisma`, `drizzle/`, `supabase/migrations`, `models/`, SQL files). Entity names reveal what users actually do.

## Write 2–3 ICP personas

Base each on who the product is clearly for. Give each one these fields:

```markdown
## <slug, e.g. busy-freelancer>
- **Who:** one line
- **Goal:** what they came to do
- **Tech-savviness:** low | medium | high
- **Patience:** low | medium | high   (low = abandons after ~2 failed attempts or 10 s spinners)
- **Device/viewport:** desktop 1280x800 | mobile 390x844 | tablet 820x1180
- **Network:** fast | slow-3g | flaky
- **Priority features:** routes/flows they care about (use real routes from discovery)
- **Missions:**
  1. "<concrete task phrased like a user, e.g. Sign up and create your first invoice for $120>"
  2. …(3–5 missions, mixing core flows with the persona's priority features)
```

## Always add the built-ins

```markdown
## normal-user
- **Who:** an ordinary user who reads labels and follows the intended path
- **Goal:** complete every core flow once, correctly
- **Tech-savviness:** medium · **Patience:** high · **Device:** desktop 1280x800 · **Network:** fast
- **Missions:** every core flow from discovery: sign up, log in, create/read/update/delete each main entity, search, checkout/payment (with test data), settings, and (with a throwaway account, never the shared saved one) log out and back in

## rushed-beginner
- **Who:** first-time user on a phone, in a hurry, doesn't read instructions
- **Tech-savviness:** low · **Patience:** low · **Device:** mobile 390x844 · **Network:** slow-3g
- **Behaviors:** double-clicks buttons; types phone numbers, dates and prices in the wrong format; leaves required fields empty; hits back mid-flow; abandons and returns; pastes text with trailing spaces
- **Missions:** the two most important ICP missions, done carelessly

## chaos-monkey
- **Who:** an adversarial tester who is curious, not malicious
- **Tech-savviness:** high · **Patience:** high · **Device:** desktop
- **Behaviors:** every chaos technique from the wreck-chaos skill
- **Missions:** break each form and each multi-step flow
```

Note: `chaos-monkey` is run by the **wreck-chaos** stage, not by wreck-explore.

## Finish

Write the file, then print a short table: persona, device, top mission. Tell the user they can edit `.wreck-it/personas.md` and it will be reused on the next run. Mark the stage with `WRECK run stage personas done`.
