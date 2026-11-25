---
name: create-workflow-demo
description: Generates structured product walkthroughs and demo scripts — interactive product tours, screencast scripts, sandbox guided experiences, sales demo scripts, or self-serve onboarding flows. Make sure to use this skill whenever the user says build a demo for [feature/product], create a walkthrough, write a demo script for [meeting], scripted product tour, build an interactive demo, demo for [prospect], or describes wanting to walk someone through a product capability sequentially. Includes scene-by-scene structure, intent per scene, narration script, screen actions, and trust-building moments for security/cybersec products. Do NOT use for: written multi-slide presentations (use create-deck), single-page collateral (use create-one-pager), prospect landing pages (use create-landing-page), or technical documentation/runbooks (use runbook). Defining characteristic: "sequential walkthrough of a product or workflow, with narration, often live or recorded."
---

# Create Workflow Demo

Structured product walkthroughs and demo scripts — live, recorded, or interactive.

## When to use vs. adjacent asset skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Output is a sequential walkthrough with narration | Static slides → `create-deck` |
| Designed to show a product in motion | Static one-page handout → `create-one-pager` |
| Live demo, screencast, or interactive tour | Standalone web landing page → `create-landing-page` |
| Sales / marketing intent | Internal operational procedure → `runbook` |

## Demo types this skill handles

### Live sales demo (synchronous, with prospect)
Audience: prospect on a video call with you driving the product.

Standard structure (15-30 min):
1. **Pre-demo discovery recap** (1 min) — confirm what you heard about their problem
2. **Demo agenda** (30 sec) — what you'll show, what you won't
3. **Setup the scenario** (1 min) — "imagine you're [their role] doing [their task]"
4. **Show the workflow end-to-end** (10-15 min) — 3-5 capabilities, each tied to a stated need
5. **Pause for objections** (planned at 2-3 points) — "does this match how you think about it?"
6. **Specific question they raised** (3-5 min) — answer the question they pre-asked
7. **Wrap with next steps** (2 min) — pilot scope, evaluation criteria, decision timeline

Output: scripted "say this when you click here" with branching for likely questions.

### Recorded demo (async, prospect/lead consumes alone)
Audience: prospect watching unsupervised, often during evaluation.

Standard structure (5-10 min):
1. **Hook** (30 sec) — what they'll learn, why it matters in their language
2. **Problem framing** (1 min) — without their input, mirror the buyer persona
3. **Product walkthrough** (3-5 min) — narration over screen recording
4. **Outcome demonstration** (1 min) — show the result that matters to them
5. **Optional deeper dive** — "to see X capability, jump to chapter [N]"
6. **CTA** (15 sec) — book a call, start trial, request follow-up

Output: scene-by-scene script with narration, screen actions, and timing.

### Interactive product tour (in-app, self-serve)
Audience: trial user or first-time logged-in user.

Standard structure (3-5 steps usually):
1. **Welcome / orientation** — "here's what you'll do in the next 2 minutes"
2. **Tour anchor #1** — point to a UI element, explain its role
3. **Tour anchor #2** — guide to a key action; let them do it
4. **Validation** — confirm they did it; show the outcome
5. **Wrap** — "you've now seen X; here's where to go next"

Output: tour spec in a format compatible with Pendo, Appcues, WalkMe, Userpilot, or similar (or vanilla DOM-targeted JS for custom).

### Sandbox guided experience (interactive demo without live human)
Audience: prospect who clicks "try it" on a marketing site, gets a guided product environment.

Standard structure:
1. **Cold start state** — meaningful pre-populated data (not "lorem ipsum")
2. **Persona setup** — "you're playing [role] at [company type]"
3. **Mission 1** — narrow task with clear success state
4. **Mission 2** — building on the first
5. **Mission 3** — capstone showing differentiated capability
6. **Optional exploration** — "now try [these other things]"
7. **CTA out** — "ready to see what your data looks like?"

Output: data setup + scripted missions + UI prompts + exit CTA.

### Customer onboarding walkthrough (post-purchase)
Audience: new customer in first 7 days.

Standard structure (varies, often 4-6 micro-tours over first week):
- Day 0: account setup
- Day 1: first integration
- Day 3: first value-realizing action
- Day 7: report/dashboard surfacing outcomes

Output: tour spec + email triggers + success criteria per stage.

## Cybersecurity demo overlay

Security product demos require additional trust-building moments:

- **Show the data, not just the UI.** When demoing a security product, sample data should look real (real-ish IPs, real domain names, plausible alerts) — fake-looking data signals "toy product"
- **Show the empty state.** What does a clean environment look like? This is reassuring.
- **Show the alert-fatigue answer.** Security buyers fear noise. Demonstrate filtering/prioritization explicitly.
- **Show a sample false positive.** Acknowledging FPs builds credibility more than pretending they don't happen.
- **Show the audit trail.** Auditors and CISOs want to see who-did-what-when.
- **Show the compliance mapping.** Map demo capabilities back to SOC 2 / ISO / HIPAA controls if relevant.
- **Show RBAC.** Demonstrate that not everyone sees everything; least-privilege visibility.
- **Show export.** Reports / SIEM / SOAR exports. Buyers don't want lock-in.

## Demo principles (apply to all types)

**Lead with the outcome, then show the workflow.** "Here's what your team will see at 9 AM after a quiet night" is better than "first you log in, then you click here."

**Tie every step to a stated need.** "Earlier you mentioned X — here's how that's handled" beats "and here's another feature."

**Pause after dense moments.** When you've shown something complex, stop talking. Let it land. Watch their reaction.

**Don't show what you can't deliver.** Vaporware in demos = legal exposure + lost trust.

**Show, don't tell.** "Here's the alert" beats "we have alerts."

**Skip the dashboard navigation tour.** Nobody cares which menu the settings are in. Show the work.

## Anti-patterns

- **Tour every menu item** — marathon UI tour with no narrative
- **Demo in a vacuum** — no pre-discovery, generic to all prospects
- **Show error states by accident** — practice runs prevent this
- **Sample data is "lorem ipsum"** — signals product is unfinished
- **Reading from a script** — sounds robotic in live demos; outline + improvise
- **Going too fast on the differentiated capability** — the one moment that wins the deal needs to breathe
- **Tech audience demo for business audience** (or vice versa) — calibrate to the person in the room
- **Demo IS the sales meeting** — demo is a tool, not the meeting; discovery and ROI conversation come first

## Output

Depending on demo type:
- **Live demo:** scripted talking points + branching for objections + click-by-click flow
- **Recorded demo:** scene-by-scene script with timing, narration, on-screen actions
- **Interactive tour:** tour spec in chosen tool format (Pendo / Appcues / custom)
- **Sandbox:** data setup spec + mission script + UI prompts
- **Onboarding:** week-by-week tour spec + trigger conditions + success metrics
- **Common to all:** suggested follow-up CTA + measurement (conversion rate, completion rate, etc.)
