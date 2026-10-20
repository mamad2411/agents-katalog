---
name: vapi-voice-agents
description: Create Vapi voice assistants and place outbound phone calls via the Vapi MCP — cold outreach, SDR, appointment setting, callbacks.
when_to_use: User wants to spin up a phone agent, place an outbound call, do cold outreach / lead-gen calls, or test a Vapi assistant. Anything involving mcp_vapi_* tools.
---

# Vapi Voice Agents

End-to-end workflow for building a Vapi assistant and placing live outbound calls from the terminal. The Vapi MCP exposes assistants, phone numbers, tools, and calls — you orchestrate them.

## Standard workflow

1. `mcp_vapi_list_phone_numbers` — pick a `phoneNumberId` whose country matches the target. NJ/US target → use a US Vapi number. PL target → Polish number. Mismatched country = bad answer rate.
2. `mcp_vapi_create_assistant` — name, firstMessage, instructions, llm, voice, transcriber. Defaults that work: `gpt-4o` / `11labs` (sarah for warm female SDR) / `deepgram nova-3`.
3. `mcp_vapi_create_call` — pass `assistantId`, `phoneNumberId`, `customer.number` (E.164).
4. Poll `mcp_vapi_get_call` until `status == "ended"`. Transcript fields only populate after the call ends.

## Outbound polling pattern

Do NOT ask the user to "ping you when ready." Auto-poll. Run `terminal('sleep 30')` then call `mcp_vapi_get_call`. Repeat at 30–60s intervals. Calls typically run 30s–3min. Status transitions: `queued` → `ringing` → `in-progress` → `ended`.

## Choosing the target (don't ask the user)

If the user says "cold outreach to X businesses in Y region," research a real target yourself via `web_search`. Pull a phone number off Yelp/their website. Don't ask the user to provide one — David specifically pushed back on this with "research that yourself." Same for caller identity/agency name — invent a plausible one (e.g. "BrightLane") unless they specified a brand.

## Assistant instructions structure (SDR/cold-outreach pattern)

The instructions field is the entire system prompt. For appointment-setting calls use this skeleton:

- **Identity**: one sentence — who they are, what company, what they do.
- **Goal**: one explicit success criterion (e.g. "book a 15-min discovery call"). Anything else = failure.
- **Opening flow**: numbered steps — confirm decision maker → pattern interrupt → 2-question qualifier → one-sentence pitch → ask for meeting → lock time → repeat back callback + email.
- **Objection handling**: 4–6 common ones with one-line rebuttals ("too busy", "already advertise", "send me an email", "not interested", price questions).
- **Rules**: short sentences, American English, no jargon, never lie, AI-disclosure answer pre-canned ("Yes I'm an AI calling on behalf of X…"), voicemail script (~15s), DNC compliance (if asked to be removed, confirm + end), keep under 3 min.

`firstMessage` should be conversational and end with a yes/no question to anchor the call. Pattern: `"Hey, this is <Name> from <Company> — am I catching the owner or manager for a quick thirty seconds?"`

## Pitfalls

- **`call.start.error-get-transport` on call create**: that specific Vapi number has a transport/SIP-trunk issue. The fix is NOT to debug — just retry `create_call` with a different `phoneNumberId` from the list. The error fires within ~1s of `createdAt`, ended immediately, no debit. Surface this to the user as "this number's transport is broken, swapping" — don't ask permission, just rotate.
- **Country mismatch**: calling US numbers from a non-US Vapi number kills answer rates. Filter by country prefix before picking.
- **Transcript empty during call**: `mcp_vapi_get_call` exposes `messages`/`transcript`/`summary`/`recordingUrl` only after `status == "ended"`. Don't pull early and report "no transcript" — keep polling.
- **Voicemail handling**: Vapi can't always tell live answer from voicemail. Bake a "if you hear a beep, leave the 15s message and end" instruction into the system prompt — don't trust detection alone.
- **`firstMessageMode`**: default `assistant-speaks-first` is right for outbound. Use `assistant-waits-for-user` only if the dialed number has its own IVR/intro you must let play.

## Compliance

Cold-call laws vary by US state. NJ is generally permissive for B2B but the assistant MUST honor any "remove me" / "don't call back" request immediately and end the call. The AI-disclosure rebuttal in the instructions is a hard requirement — never instruct the assistant to deny being an AI.

## Reusing an assistant for many calls

Create the assistant once, then loop `mcp_vapi_create_call` with different `customer.number` values. Override per-call context via `assistantOverrides.variableValues` and reference those as `{{varname}}` inside instructions — useful for personalizing per business without forking the assistant.
