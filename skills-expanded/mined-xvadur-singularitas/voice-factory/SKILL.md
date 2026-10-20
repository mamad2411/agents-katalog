---
name: voice-factory
description: Create, configure, deploy, and manage AI voice agents across ElevenLabs and Vapi with a repeatable delivery pipeline. Use when Adam wants to build a new voice agent, update agent behavior, prepare prompts, define handoff logic, set intake rules, map tool flows, run QA, standardize a voice-agent build process, or turn one-off agent work into a reusable factory system. For current Xvadur state, use this as the production subsystem for narrow phone-first pilot deployments, especially realtor-first Vapi agents. Use n8n as the separate automation skill when workflow implementation or debugging is required.
---

# Voice Factory

Use this skill as the main production pipeline for Xvadur voice-agent delivery and agent operations.

Voice Factory is a **deployment subsystem** inside Xvadur Agent Deploy Studio.
It is not a separate business identity.
Its default job is to produce **narrow phone-first pilot deployments** that can be repeated reliably.

This skill owns:
- agent intake and deployment planning
- scope definition for the pilot surface
- deployment-pack definition
- conversation design and prompt structure
- ElevenLabs voice layer decisions
- Vapi agent configuration decisions
- QA, launch readiness, and change control

This skill does **not** replace `n8n`.
Use `n8n` as the separate skill for workflow creation, execution debugging, and automation implementation.

## Current Xvadur operating context

Treat these as current source-of-truth defaults unless the user says otherwise:
- Xvadur = **agent deployment studio**
- first offer = **phone-first pilot setup**
- current wedge = **realty**
- default buyer = **owner / founder**
- V1 scope rule = **one problem surface**
- build order = **primitives -> deployment pack -> client instance**

Default problem surface for realtor V1:
- missed inbound / weak first contact handling

If a requested build exceeds a narrow pilot, call that out explicitly and split V1 from later expansion.

## Non-negotiable scope rules

- Build **one problem surface** per pilot.
- Do not smuggle multi-surface complexity into V1.
- If a requirement does not help validate the pilot, keep it out of current scope.
- Do not present broad custom AI work as if it were the default offer.
- Do not imply capabilities that are not actually deployed.
- Treat callback / lead capture / safe next-step routing as more important than sounding impressive.

## Platform split

- **Voice Factory** = design, create, configure, and manage the agent across Vapi + ElevenLabs
- **Vapi inside Voice Factory** = assistant inspection, runtime setup, call behavior, tool routing, phone assistant configuration
- **ElevenLabs inside Voice Factory** = voices, speech assets, cloning, dialogue, audio generation
- **n8n** = automation workflows, webhooks, data writes, downstream orchestration

## Required access

Set:
- `VAPI_API_KEY`
- `ELEVENLABS_API_KEY`

Preferred auth pattern for Vapi:
- `Authorization: Bearer $VAPI_API_KEY`

Base URLs:
- Vapi: `https://api.vapi.ai`
- ElevenLabs: `https://api.elevenlabs.io`

## Vapi core endpoints

### List assistants
```bash
curl -sS https://api.vapi.ai/assistant \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Get one assistant
```bash
curl -sS https://api.vapi.ai/assistant/<assistant-id> \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Create assistant
```bash
curl -sS https://api.vapi.ai/assistant \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @assistant.json
```

### Update assistant
```bash
curl -sS -X PATCH https://api.vapi.ai/assistant/<assistant-id> \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @assistant-patch.json
```

## Default operating workflow

1. **Capture intake brief**
   - business type
   - location and language
   - call types to handle
   - booking or lead destination
   - business hours
   - escalation and human transfer rules
   - forbidden actions / compliance constraints

2. **Define the pilot scope**
   - what the agent must do in V1
   - what the agent must not do in V1
   - what counts as success on a call
   - what data must be captured every time
   - what stays out of scope until expansion

3. **Define the deployment pack**
   - caller lanes
   - minimum required fields per lane
   - lead scoring policy
   - allowed next-step outcomes
   - handoff triggers
   - placeholders / unknown business rules
   - QA pack

4. **Design the conversation system**
   - greeting
   - qualification logic
   - booking or lead capture flow
   - objection / confusion handling
   - fallback behavior
   - handoff triggers

5. **Choose the voice/runtime setup**
   - ElevenLabs voice strategy
   - Vapi runtime and tool behavior
   - latency / quality tradeoffs
   - language and tone constraints

6. **Map integrations**
   - what Vapi sends
   - what n8n receives
   - what systems are updated
   - what confirmation must return to caller

7. **Run QA before go-live**
   - normal path
   - edge cases
   - unclear caller speech
   - after-hours flow
   - escalation path
   - failed tool / failed webhook behavior

8. **Prepare launch packet**
   - final prompt
   - tool map
   - voice/runtime config
   - QA report
   - known limitations
   - next optimization sprint

## Output contract

Always deliver:
- deployment summary
- defined V1 scope
- deployment-pack summary
- final prompt or prompt changes
- firstMessage
- Vapi field map when the build is serious enough for deployment
- tool/workflow map
- handoff logic
- QA results
- open risks / known limitations
- next optimization actions

Default quality bar:
- output should be polished enough to go into Vapi with minor or no style cleanup
- prompts should read like runtime instructions, not documentation
- spoken behavior should be concise, natural, and operational

## Test suites are part of the deployment

For serious assistants, treat Vapi Test Suites as part of the deliverable.
A production-grade assistant is not just prompt + config.
It is prompt + config + regression tests.

Minimum QA pack:
1. one happy-path test
2. one edge-case / guardrail test
3. one ambiguity / vague-intent test

For Marek-class realtor assistants, the default baseline is:
- LISTING_SPECIFIC happy path
- SELLER pricing / valuation guardrail
- GENERAL_INQUIRY vague-intent fallback

When working with test suites:
- keep scripts concrete and phone-like
- test one real behavior at a time
- make rubrics behavior-specific, not vague
- do not test undeployed capabilities as if they exist
- if tools do not exist, reward safe fallback behavior instead
- review transcript + scorer reasoning after every failure
- update stale tests when the assistant changes segment or scope

## Realtor-first target pattern

For the current Xvadur wedge, prefer the realtor pattern unless the user explicitly requests another vertical.

Read these references as needed:
- Vapi build system / reusable factory flow: `references/vapi-build-system.md`
- Prompt block order / construction logic: `references/prompt-construction-framework.md`
- Prompt polishing rules for live-ready output: `references/polish-rules.md`
- Vapi test suite workflow and API patterns: `references/vapi-test-suites.md`
- Realtor vertical playbook: `references/realtor-playbook.md`
- Concrete target pattern for the current Brex Reality-style assistant: `references/realtor-target-agent-brex-reality.md`
- Golden reference baseline for output quality and live Vapi shape: `references/marek-baseline-spec.md`
- Cross-segment validation before backend work: `references/segment-test-framework.md`
- Dentist vertical playbook: `references/dentist-playbook.md`

If the deployment is outside those verticals, still follow the same factory sequence and adapt the intake + QA logic to the business.

## Deterministic helper

```bash
python3 /Users/_xvadur/singularitas/skills/voice-factory/scripts/new_brief.py --vertical dentist
python3 /Users/_xvadur/singularitas/skills/voice-factory/scripts/new_brief.py --vertical realtor
```

## Rules

- Never claim an agent is live-ready without QA evidence.
- Always define explicit human handoff triggers.
- Keep prompts concise, bounded, and operational.
- Polish prompts until they sound like runtime behavior, not operator notes.
- Prefer short, sharp spoken phrasing over explanatory wording.
- Treat callback as a valid primary outcome, not as a weak fallback, when the segment warrants it.
- Prevent custom chaos: define scope before implementation.
- Separate agent design decisions from n8n workflow implementation.
- Prefer repeatable patterns over one-off bespoke setups.
- Prefer read-first inspection before Vapi mutation.
- Patch only what you intend to change.
- Verify writes by reading the assistant back.
- Preserve voice/transcriber/tool config unless intentionally changing them.
- Record assistant id, purpose, tools, model, transcriber, voice provider, and any active analysis/structured-data plan for each deployment.
- Change one runtime variable at a time when debugging Vapi behavior.
- Do not promise booking availability, listing details, or pricing facts without system support.
- Stop asking questions once the minimum useful qualification data has been captured.
- Remove duplicated caution language that does not improve runtime behavior.
