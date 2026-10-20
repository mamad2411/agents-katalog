---
name: outbound-phone-operations
description: "Use when placing outbound AI phone calls to businesses."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [phone, outbound-calls, vapi, ivr, voicemail, verification]
    related_skills: [himitsu]
---

# Outbound Phone Operations

## Overview

This skill governs end-to-end outbound AI calls for pricing inquiries, appointment coordination, confirmations, vendor support, and similar administrative work. The deliverable is not “a call was queued.” It is the requested fact or completed interaction, verified from a terminal call state and full transcript.

Keep provider-independent discipline in this file. Load `references/vapi-provider.md` for the tested Vapi API recipe and environment wiring. Use `templates/vapi-outbound-call.json` as a safe transient-assistant starting point. `references/cvac-pricing-example.md` is a dated worked example of IVR and voicemail recovery; never treat its price as permanently current.

## When to Use

Use this skill when the user asks to:

- call a published business or service-provider number;
- obtain a quote, price, availability, policy, or lead time;
- confirm, cancel, or reschedule an existing administrative arrangement;
- navigate an IVR to reach the correct department;
- leave a purposeful voicemail and track whether a human answer is still required.

Do not use it for:

- emergency services;
- unsolicited marketing campaigns or bulk dialing;
- purchases, contracts, payment, disclosure of sensitive records, or irreversible commitments unless the user separately and explicitly authorized that exact action;
- calls where identity, legal authority, or consent requirements are unresolved.

## Definition of Done

Classify the requested outcome before dialing:

| User’s ask | Done when |
|---|---|
| “Find out…” / “Ask how much…” | A live representative supplies the answer, or every reasonable published route is exhausted and the user is told that only follow-up is pending. A voicemail alone is not success. |
| “Leave a message…” | The voicemail system confirms or accepts the saved message; merely speaking before a timeout is not enough. |
| “Confirm/cancel/reschedule…” | The counterparty explicitly confirms the new state and any reference number or effective date is captured. |
| “Reach out…” with no narrower outcome | The substantive message reaches a person or is saved successfully, and the response/follow-up state is clear. |

Never let a provider’s generated `successEvaluation` override this table. Judge success against the user’s requested outcome and the actual transcript.

## Safety and Disclosure Boundary

### Identity

Be transparent that the caller is an AI assistant acting for the user. Do not imitate the user or imply the assistant is human. Use a short identity line and move to the task.

### Recording and transcription

Before substantive conversation with a live person, disclose recording or transcription when the provider captures it and obtain the consent required for the relevant jurisdictions and context. A robust opening is:

> Hi, I’m an AI assistant calling on behalf of [name]. This call is transcribed for note-taking—is that okay?

If consent is refused, apologize and end the call. Configure the assistant to distinguish an IVR from a live person so it does not ask a menu for consent or talk over the menu.

### Scope

Write explicit negative authority into the call brief. For an information inquiry, that normally means:

- no purchase or reservation;
- no contract or appointment commitment;
- no payment information;
- no unrelated personal information;
- no invented answer, quote, callback promise, or tool result.

A call-specific assistant should know only the minimum contact details required for this call.

## Assistant Isolation

**Default to a transient, call-specific assistant.** Reusing a broad saved personal assistant can silently bring unrelated addresses, payment cards, PINs, private tools, and standing permissions into a routine vendor call.

When a saved assistant is unavoidable:

1. inspect only selected safe metadata such as ID, name, model name, voice, and status;
2. never print the full assistant object or all system messages into tool output;
3. verify whether call overrides replace or merge standing instructions;
4. prefer a fresh transient assistant if replacement semantics are uncertain.

The transient assistant should contain:

- one narrow goal;
- the disclosure/consent flow;
- IVR instructions and a DTMF tool;
- a voicemail branch;
- an `endCall` tool;
- permitted fallback contact details only;
- explicit prohibitions on commitments and sensitive data.

## Workflow

### 1. Ground the target

1. Read the business’s official contact page or another first-party source.
2. Record the primary number, one alternate number, department names, timezone, and current business hours.
3. Prefer a published sales or customer-service line for the first attempt; keep the corporate/general number as the recovery route.
4. Define the exact answer fields before calling. For a price inquiry, use:
   - product/model;
   - exact base or retail price;
   - exclusions such as shipping, installation, tax, or required accessories;
   - recurring fees or maintenance requirements;
   - warranty;
   - lead time;
   - representative name.

**Completion criterion:** the target and fallback routes are verified from first-party information, and the answer schema is explicit.

### 2. Resolve credentials without leakage

1. Retrieve provider credentials through the configured secret manager.
2. Keep service-account and API tokens in process-local variables.
3. Never print, write, interpolate into chat, or place tokens in request artifacts.
4. Probe only safe resource metadata before dialing: HTTP status, caller-number resource status, assistant name/ID if applicable.

If the credential is indirectly stored—for example, a 1Password service-account token in Himitsu—load the service token first and use it only to retrieve the final provider credential. See `references/vapi-provider.md`.

**Completion criterion:** provider authentication succeeds and the outbound caller-number resource is active, with no secret value in logs.

### 3. Build the call brief

Use short, operational instructions rather than a conversational essay:

1. classify IVR, voicemail, or live person;
2. navigate to the correct human;
3. disclose AI identity and transcription to the human;
4. obtain consent;
5. ask the primary question first;
6. ask at most a few secondary questions;
7. repeat or spell ambiguous product names and numeric answers;
8. end once the answer is complete.

For prices, have the assistant confirm the number once in plain language when audio or transcription is ambiguous. Do not make the representative repeat every detail.

Use a wait-first mode when available. It lets the assistant hear “hello,” an IVR greeting, or a voicemail prompt before choosing the correct branch.

**Completion criterion:** the prompt contains a goal, consent branch, IVR branch, voicemail branch, boundaries, and a clear stopping condition.

### 4. Place the call

Submit the provider request with:

- active outbound phone-number ID;
- destination in E.164 format;
- transient assistant configuration;
- DTMF and end-call tools;
- transcriber and voice;
- bounded maximum duration and silence timeout;
- non-sensitive metadata identifying the purpose.

Save the provider’s call ID immediately. Do not expose full destination numbers in the user-facing report unless needed.

**Completion criterion:** the provider accepted the request and returned a durable call ID.

### 5. Poll through artifact completion

Poll the call endpoint until the call reaches a terminal state. Report status changes sparingly. After `ended`, re-fetch until the transcript appears or a small bounded artifact grace period expires; some providers finalize transcripts after telephony has ended.

Capture:

- call ID;
- terminal status and ended reason;
- start/end timestamps;
- full transcript;
- provider summary/evaluation, if any;
- recording link only when needed and appropriately protected.

A generated summary is secondary evidence. The transcript is primary evidence.

**Completion criterion:** the call is terminal and the full available transcript has been retrieved, or the no-answer/failure reason is explicit.

### 6. Recover instead of stopping early

Use this bounded recovery ladder when the user asked for a factual answer:

1. **Desired department answers:** finish normally.
2. **Desired department goes to voicemail:** leave a concise message only if useful, save it using the voicemail prompts, then call the alternate published number or general operator.
3. **Main line has an IVR:** listen to the complete menu, use DTMF, and prefer a live general operator after a department mailbox dead-end.
4. **No answer or immediate disconnect:** verify the number and business hours, then try the alternate route once.
5. **Quote-only policy:** ask for a realistic range and the factors that determine the formal quote.
6. **Still unresolved:** report the attempts and pending callback honestly; do not call voicemail “success.”

Avoid repeated calls to the same person or mailbox. A small number of distinct, reasonable routes is enough.

### 7. Verify the answer

Read the transcript around each requested field. Distinguish:

- what the representative explicitly stated;
- what was not answered;
- what the assistant or provider summary inferred.

Examples:

- If the representative describes low maintenance and an annual filter change but gives no dollar amount, report “no recurring fee amount was quoted,” not “there are no recurring fees.”
- If the representative says a retail price excludes freight, installation, and tax, list each exclusion rather than reporting only the headline price.
- If transcription mangles a brand name but the called business and context are unambiguous, normalize the brand in the report while preserving uncertainty about any genuinely unclear facts.

**Completion criterion:** every reported factual field maps to an explicit transcript statement or is labeled unknown.

### 8. Report concisely

Lead with the requested result. A useful format is:

- **Price/result:** …
- **Not included or conditions:** …
- **Maintenance/recurring cost:** …
- **Warranty:** …
- **Lead time:** …
- **Source:** representative name and direct phone confirmation date

Mention recovery attempts in one sentence only when they explain how the result was obtained or what remains pending. Do not dump raw API objects or sensitive assistant configuration.

## IVR and Voicemail Technique

### IVR

- Wait for all options before pressing a key.
- Use DTMF without speaking simultaneously.
- Prefer department → general operator → alternate published line.
- If the menu repeats, retry once with a delayed DTMF sequence or a spoken department name.
- Do not enter personal or payment data into an IVR unless explicitly authorized.

### Voicemail

- Keep the message under roughly 20 seconds.
- State AI identity, caller’s first name, exact question, and one callback channel.
- Prefer a callback number over a hard-to-transcribe email address; if email is necessary, spell it slowly.
- After speaking, listen for save/review prompts and use DTMF—often `1`—to save.
- Confirm acceptance or a clean hang-up behavior before marking the message delivered.

## Common Pitfalls

1. **Stopping at `queued`.** Fix: poll through `ended` and transcript finalization.
2. **Treating voicemail as the requested answer.** Fix: use an alternate line or operator when the user asked to “find out.”
3. **Speaking a voicemail but not saving it.** Fix: follow the post-recording DTMF prompts.
4. **Loading an unrelated saved assistant.** Fix: use a transient assistant with least-privilege context.
5. **Dumping assistant configuration to inspect it.** Fix: select safe fields only; full prompts may contain payment or identity data.
6. **Asking consent before recognizing an IVR.** Fix: use wait-first mode and classify the answer first.
7. **Reporting inference as fact.** Fix: map every conclusion to the transcript and label unanswered fields.
8. **Letting secondary questions obscure the main ask.** Fix: ask price/status first, then exclusions and timing.
9. **Garbled brands, emails, or numbers.** Fix: spell the brand, prefer callback numbers, and confirm critical numerics once.
10. **Over-calling.** Fix: use a bounded route ladder and stop after distinct reasonable routes are exhausted.

## Verification Checklist

- [ ] Official target number and alternate route verified
- [ ] Business timezone/hours checked
- [ ] User’s requested outcome translated into explicit answer fields
- [ ] Transient assistant used, or saved-assistant isolation verified
- [ ] AI identity and transcription/recording disclosure included
- [ ] No purchase, payment, or sensitive-data authority implied
- [ ] DTMF and end-call tools available
- [ ] Call ID saved
- [ ] Terminal status and ended reason retrieved
- [ ] Full available transcript retrieved after end
- [ ] Voicemail, if used, was actually saved
- [ ] Recovery ladder used when a live answer was required
- [ ] Final report separates explicit facts from unknowns and inferences
