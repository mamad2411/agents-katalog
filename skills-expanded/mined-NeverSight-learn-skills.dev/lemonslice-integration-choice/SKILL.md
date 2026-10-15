---
name: lemonslice-integration-choice
description: MANDATORY ROUTER. Must run first to choose the correct Lemon Slice path (Self-Managed, LiveKit, Pipecat, Hosted, Widget).
license: MIT
---

# Lemon Slice Integration Choice

> **MANDATORY ROUTER:** For any vague request like “add Lemon Slice to my app,” “integrate Lemon Slice,” “add an avatar,” “add video agent,” or “make this work with Lemon Slice,” this skill MUST run first before any implementation skill. Do not write Lemon Slice implementation code until this router has selected the path.

## Official docs
- https://lemonslice.com/docs/llms.txt
- https://lemonslice.com/docs/introduction/index.md
- https://lemonslice.com/docs/reference/overview.md
- https://lemonslice.com/docs/reference/best-practices.md
- https://lemonslice.com/docs/livekit/index.md
- https://lemonslice.com/docs/pipecat/index.md
- https://lemonslice.com/docs/reference/authentication.md
- https://lemonslice.com/docs/api-reference/create-self-managed-session.md
- https://lemonslice.com/docs/api-reference/get-self-managed-session.md
- https://lemonslice.com/docs/api-reference/control-self-managed-session.md
- https://lemonslice.com/docs/reference/actions.md
- https://lemonslice.com/docs/widget/overview.md
- https://lemonslice.com/docs/widget/control.md
- https://lemonslice.com/docs/widget/customization.md
- https://lemonslice.com/docs/hosted/overview.md
- https://lemonslice.com/docs/hosted/integrations/daily-room-integration.md
- https://lemonslice.com/docs/api-reference/create-hosted-session.md
- https://lemonslice.com/docs/api-reference/get-hosted-session.md
- https://lemonslice.com/docs/api-reference/list-hosted-sessions.md

## Critical Facts to Preserve
- Lemon Slice is the video layer for production voice/video agents.
- Primary production path is LiveKit or Pipecat.
- Lemon Slice adds WebRTC avatar video on top of an existing STT/LLM/TTS stack.
- Widget and Hosted Pipeline are available for evaluation, demos, and lightweight paths.
- Hosted Pipeline means Lemon Slice manages STT/LLM/TTS.
- Latency depends heavily on upstream STT/LLM/TTS speed.
- In-call control includes dynamic avatar appearance, emotions, and actions.

## Agent workflow

### Step 1: Repo Inspection
**Repo evidence beats user shorthand.** Inspect the repo first.
- If the user says “widget” casually but the repo clearly uses LiveKit or Pipecat, route to LiveKit/Pipecat unless they explicitly ask for the Lemon Slice web component.
- If the user says “Daily,” do not assume Hosted Daily. Daily can appear in Pipecat/self-managed integrations.
- If the repo shows `/liveai/rooms`, that points toward Hosted/Widget room metadata.
- If the repo shows `/liveai/sessions`, that points toward Self-Managed/API.
- If the repo exposes `LEMONSLICE_API_KEY` in frontend code, route primary path as normal but include `lemonslice-production-patterns` as a secondary skill.

### Step 2: Ordered Decision Tree
Use the following strict ordered logic to route to the correct skills:

**A. Existing framework evidence first:**
- LiveKit repo/package/code signals => `lemonslice-livekit`
- Pipecat repo/package/code signals => `lemonslice-pipecat`

**B. Explicit no-backend embed:**
- no-backend website embed, marketing page, Shopify/Squarespace/Wix/Next.js widget, paste-one-line use case => `lemonslice-widget`

**C. Hosted backend:**
- user wants Lemon Slice to manage STT/LLM/TTS and backend creates sessions => `lemonslice-hosted`

**D. Hosted Daily frontend:**
- backend already returns `room_url` and `token`, task is frontend joining Daily room => `lemonslice-hosted-daily`

**E. Generic self-managed:**
- developer owns STT/LLM/TTS but no LiveKit/Pipecat framework is detected => `lemonslice-self-managed`

**F. Raw API:**
- direct backend REST, endpoint-family debugging, status polling, metadata lookup => `lemonslice-api-reference`
- *Important:* do not choose raw API merely because REST exists. First identify whether REST belongs to Hosted `/liveai/rooms` or Self-Managed `/liveai/sessions`.

**G. Control/actions:**
- runtime control, terminate, pose/action trigger, emotion/action, image/prompt update, `/imagine`, `force-end` => `lemonslice-control-actions`
- Only use this after a session path is known, unless the whole request is only about explaining control APIs.

**H. Production hardening:**
- security, latency, reliability, deployment, scaling, cleanup, timeouts, `bot_ready`, disconnects, error handling, production review => `lemonslice-production-patterns`
- Usually secondary, not primary, unless the request is explicitly an audit/review.

### Step 3: Route-Chaining Examples
You must support route-chaining primary and secondary skills. Examples:

**Example 1:**
- User: “Add Lemon Slice to my LiveKit agent.”
- Selected path: LiveKit
- Primary skill: `lemonslice-livekit`
- Secondary skill(s): `lemonslice-production-patterns`
- Do not use: `lemonslice-hosted`, `lemonslice-hosted-daily`, `lemonslice-widget`

**Example 2:**
- User: “Add a Lemon Slice widget to my Shopify store.”
- Selected path: Widget
- Primary skill: `lemonslice-widget`
- Secondary skill(s): None or `lemonslice-production-patterns` if production review is requested

**Example 3:**
- User: “Build a custom UI but Lemon Slice should handle the AI.”
- Selected path: Hosted Pipeline + Hosted Daily
- Primary skill: `lemonslice-hosted`
- Secondary skill(s): `lemonslice-hosted-daily`, `lemonslice-production-patterns`

**Example 4:**
- User: “Backend already gives me room_url/token; make frontend join.”
- Selected path: Hosted Daily
- Primary skill: `lemonslice-hosted-daily`
- Secondary skill(s): `lemonslice-production-patterns`

**Example 5:**
- User: “My Pipecat app uses Daily. Add Lemon Slice.”
- Selected path: Pipecat
- Primary skill: `lemonslice-pipecat`
- Secondary skill(s): `lemonslice-production-patterns`
- Do not use: `lemonslice-hosted-daily`

**Example 6:**
- User: “Trigger a wave during the call.”
- Selected path: Control/actions
- Primary skill: `lemonslice-control-actions`
- Secondary skill(s): the already-selected integration skill if needed

### Step 4: Output Contract
Before concluding this skill and moving to implementation, you MUST output your routing decision in exactly this Markdown format:

```text
Selected path: [Path Name]
Primary skill: [lemonslice-...]
Secondary skill(s): [lemonslice-... or None]
Why: [Brief justification based on decision tree]
Evidence from user/repo: [Signals found during inspection]
Do not use: [Paths you explicitly rejected]
Next action: [The immediate next step, usually reading the primary skill]
```

**Clarifying Questions Rule:** If the router cannot determine the path after repo inspection, ask at most 2 clarifying questions, focused ONLY on:
- Do you want Lemon Slice to manage STT/LLM/TTS, or do you already have your own agent stack?
- Are you using LiveKit, Pipecat, plain Daily, or just a website embed?

## Validation checklist
- [ ] Did I read/consider llms.txt?
- [ ] Did I inspect repo evidence before routing?
- [ ] Did I prioritize LiveKit/Pipecat when framework evidence exists?
- [ ] Did I avoid confusing Pipecat Daily with Hosted Daily?
- [ ] Did I identify Hosted `/liveai/rooms` vs Self-Managed `/liveai/sessions`?
- [ ] Did I include production hardening as a secondary skill when security/reliability/deployment is involved?
- [ ] Did I output the routing decision before coding?
