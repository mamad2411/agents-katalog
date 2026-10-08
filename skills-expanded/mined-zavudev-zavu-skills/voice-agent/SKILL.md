---
name: voice-agent
description: Build AI voice agents that answer and place phone calls — declared in code with defineAgent, deployed to Zavu Cloud, with tools, transcripts and human handoff.
---

# Voice Agents

A voice agent answers a phone call, holds a conversation, calls your code when
it needs to do something, and hands off to a person when it should. It is the
same agent object as a messaging agent, with a `voice` block on it.

Zavu runs the whole pipeline: speech recognition, the agent's model, speech
synthesis, and interruption handling. You supply the prompt and the skills.

**One thing to know before anything else:** voice is the channel where tools
actually run. On plain text the model is not offered tools at all (see
`ai-agent`). If your agent has to *do* something, voice and flows are where
that works today.

---

## Senders vs accounts (one paragraph)

A **Sender** is the API handle you pass as `Zavu-Sender`; **accounts** (a WhatsApp Business Account, a Facebook Page, a Telegram bot, a phone number) are the connections it routes — and what bills. Senders are free. Connecting an account in the dashboard auto-creates its sender; find it with `GET /v1/senders` and trust its `channels` array for what it can send. See the `channel-setup` skill for the full model.

## Fastest path: take a factory agent

Zavu ships working voice agents. Talking to one on zavu.dev and then owning its
code is the same agent.

```bash
npx zavudev agents catalog                     # what's available
npx zavudev agents pull kepler --dir kepler    # scaffold it locally
# booking agents: add --calendar calcom for a working Cal.com client
cd kepler
npm install                             # types + local runs
npx zavudev senders list                       # find your sender id
npx zavudev fn secrets set SENDER_ID <senderId>
npx zavudev deploy
npx zavudev agents list                        # confirm what actually landed
```

An agent can answer on more than one number. Connect them by id:

```bash
npx zavudev agents senders connect --agent <agentId> --sender <senderId>
```

`agents pull` writes a real TypeScript project: `index.ts` with the agent and
its skills, a `tsconfig.json`, and a local stand-in for `@zavudev/functions` so the
project typechecks and runs on your machine. Edit it freely — the file is yours,
and `npx zavudev deploy` reconciles whatever it declares.

---

## Declaring a voice agent in code

```ts
import { defineAgent, defineTool } from "@zavudev/functions"

defineAgent({
  senderId: process.env.SENDER_ID!,
  name: "Kepler",
  provider: "zavu",
  model: "openai/gpt-5.6-luna",
  channels: ["voice", "whatsapp"],
  voice: {
    enabled: true,
    model: "openai/gpt-4o",
    greeting: "Hi, I'm Kepler. What day would you like to book?",
    // Per-language greeting, used when the caller's language differs.
    greetings: { es: "Hola, soy Kepler. ¿Qué día querés reservar?" },
    // language: "es",           // omit to follow the caller's language
    interruptible: true,         // caller can talk over the agent
    maxCallDurationMinutes: 12,
    voiceSpeed: 1.15,
  },
  prompt: `# Personality
You book meetings. One idea per turn.

# Environment
You are on a phone call. They can hear you, they cannot see a screen.
Never read a URL or a code block aloud.`,
})
```

### The `voice` block

| Field | What it does |
|---|---|
| `enabled` | Whether the agent answers calls. **Required.** `false` means the number is not answered and outbound calls are rejected. |
| `greeting` | First line spoken when the call connects. Omit to let the caller speak first. |
| `greetings` | Per-language greeting, keyed by language tag: `{ es: "Hola…" }`. |
| `language` | BCP-47 tag (`en`, `es`, `pt-BR`). **Omit to follow the caller's language.** |
| `model` | Model driving the conversation. Can differ from the text model. |
| `ttsProvider` / `ttsVoiceId` | Which synthesized voice speaks. Omit for a neutral default. |
| `sttProvider` / `sttModel` | Speech recognition. Omit for the default. |
| `voiceSpeed` | 0.5–1.5. Only honoured by voices that support rate control. |
| `interruptible` | Barge-in. `true` (default) lets the caller cut the agent off. |
| `maxCallDurationMinutes` | Hard cap, 1–120. The call ends when reached. |
| `maxIdleSeconds` | Silence before the agent hangs up. 5–300. |
| `voicemailAction` | `hangup` (default) or `leave_message` when an answering machine picks up. |
| `voicemailMessage` | Spoken when `voicemailAction` is `leave_message`. Falls back to `greeting`. |
| `transferPhoneNumber` | E.164 number for human handoff. Setting it gives the agent a transfer tool. |

`channels` and `voice` are separate: `channels: ["voice"]` routes calls to this
agent, `voice.enabled` configures how it behaves on them. **You need both.** An
agent routed for voice with no `voice` block will not answer properly.

### Human handoff

The headline claim is "answer, resolve, and hand off to a person." The handoff
is `transferPhoneNumber`: set it, and the agent is given a transfer tool it can
decide to use. Say when to use it in the prompt.

```ts
voice: {
  enabled: true,
  transferPhoneNumber: "+14155551234",
},
prompt: `Transfer to a human when the caller asks for one, is upset,
or asks something about their account that you cannot answer.`,
```

---

## Booking without writing a backend

A voice agent that books meetings needs no code at all: add `check_availability`
and `book_meeting` from the dashboard (agent, **Tools**, **Library**) and
connect a Cal.com or Google calendar in the same place. Zavu hosts both skills.

Use this instead of scaffolding a booking function when the only thing the agent
has to do is read a calendar and put something on it. Reach for
`npx zavudev agents pull kepler --calendar calcom` when the booking logic is yours:
qualifying first, routing to different hosts, writing to your own system too.

## Skills the agent can call

Tools run on voice. Declare them next to the agent; they execute in your
function, in Zavu Cloud.

```ts
defineTool({
  name: "check_availability",
  description: "Find open meeting slots. Call before offering a time.",
  parameters: {
    type: "object",
    properties: {
      preferred_time: { type: "string", description: "What the caller asked for" },
    },
    required: ["preferred_time"],
  },
  handler: async (args, ctx) => {
    const res = await fetch(`https://api.example.com/slots?q=${args.preferred_time}`)
    if (!res.ok) return { ok: false, reason: "lookup_failed", slots: [] }
    return { ok: true, slots: (await res.json()).slots }
  },
})
```

Run one locally without deploying:

```bash
npx zavudev fn invoke --tool check_availability --args '{"preferred_time":"tomorrow 3pm"}'
```

**Never return a fake success.** A handler that answers `{ booked: true,
confirmationCode: "ABC-123" }` when it did nothing makes the agent tell a real
caller their meeting exists. Return `{ ok: false, reason: "not_configured" }`
and let the prompt handle it — the agent can say it cannot book right now, which
is recoverable. A false confirmation is not.

---

## Placing and inspecting calls

```bash
npx zavudev calls create --to +14155551234        # outbound. COSTS MONEY.
npx zavudev calls list --status completed
npx zavudev calls get <callId>                    # includes the transcript
npx zavudev calls hangup <callId>
```

`calls get` prints the conversation turn by turn, including tool calls. It is
the only record of what the agent actually said, and the first place to look
when a call went wrong.

From the SDK (`@zavudev/sdk` 0.56.0+; earlier versions have no `calls` resource — call the REST endpoints directly):

```ts
const { call } = await zavu.calls.create({
  to: "+14155551234",
  greeting: "Hi, this is Acme calling about your appointment.",
  language: "es-ES",            // or "auto" to follow the caller
  metadata: { campaign: "reminders" },
})
```

---

## Testing before you spend money

There is no way to hear the agent without a phone or a browser. But you can
test everything upstream of the audio, for free:

```bash
# The agent's brain: prompt, model, knowledge base. Nothing is delivered.
npx zavudev agents test --agent <agentId> --message "do you have anything Tuesday?"

# A skill's handler, locally.
npx zavudev fn invoke --tool check_availability --args '{"preferred_time":"Tuesday"}'
```

`agents test` runs the **text** path, so it will not exercise tool calling even
though voice would — it warns you when that applies. Use it for the prompt, and
`fn invoke` for the handlers.

To actually hear it, you need a phone number and a real call. There is no way
to listen to the agent for free: `agents test` is text-only, and it says so on
every run. Everything before the call is verifiable (config, prompt, handlers);
the audio itself is not. Budget for that before promising a delivery date.

Inbound requires owning a number:

```bash
npx zavudev phone-numbers search --country US
```

Do not decide from the `capabilities` column alone. It is carrier-reported and
has been wrong in both directions: numbers that place and answer calls have
listed `["sms"]`, and numbers listing `voice` have failed to complete a call.
Every number sold through Zavu is provisioned for calls when you buy it. The
check that actually answers the question is the sender's own channel list:

```bash
npx zavudev senders get <senderId>    # channels includes "voice" once it can call
```

---

## Requirements and cost

- The sender's agent needs `voice.enabled: true`, or `POST /v1/calls` returns
  `400 "The sender's agent does not have voice enabled"`.
- **Not available with test-mode API keys.**
- Inbound needs a phone number with the `voice` capability.
- Billed per connected minute plus telephony, from your prepaid balance. A short
  estimate is reserved when the call starts; you are charged the real duration
  when it ends. `402` means insufficient balance.

## Webhook events

Every voice event carries `callId`, `direction`, `from`, `to`, `status`,
`durationSeconds`, `endReason` and `transcriptAvailable`.

| Event | When |
|---|---|
| `call.initiated` | Outbound dialing, or inbound received. `status: ringing` |
| `call.answered` | Connected, the agent is live. `status: in_progress` |
| `call.completed` | Ended after a conversation |
| `call.failed` | Busy, no answer, canceled, or an error |

```bash
npx zavudev senders update <senderId> \
  --webhook-url https://api.example.com/hooks/zavu \
  --webhook-events call.completed,call.failed
```

---

## Getting it wrong

- **Agent answers but says nothing useful.** Check the knowledge base. A prompt
  that says "only state what retrieval returned" with no documents attached will
  invent answers instead of refusing. Verify with `agents test` — it reports how
  many knowledge chunks were used.
- **The number rings and the agent does not pick up.** Check the sender first:

  ```bash
  npx zavudev senders get <senderId>    # channels must be non-empty
  ```

  An empty `channels` array means the sender is not wired to anything and cannot
  send or receive on any channel, voice included. That is the cause people miss,
  because the agent, `voice.enabled`, and the number all look correct while it is
  true. Attach a number your project owns and turn voice on:

  ```bash
  npx zavudev phone-numbers update <phoneNumberId> --sender <senderId>
  npx zavudev senders update <senderId> --enable-voice
  ```

  Only once `channels` includes `voice` is it worth checking `voice.enabled` and
  that the agent itself is enabled.
- **A field you set has no effect.** `voiceSpeed` is only honoured by voices
  that support rate control. `greetings` needs a language tag that matches what
  the caller actually speaks.
- **Deploy said it synced but nothing changed.** Read the lines above the ✓,
  and do not trust the exit code. `npx zavudev deploy` prints its warnings
  before the success line, but it still exits 0 for cases that leave your agent
  unreachable — two agents on one sender, for instance, where only one answers.
  A green checkmark means the deploy ran, not that your agent will be reached.
  If you gate CI on this, gate it on the warning lines, not on the exit status.

## Prompting for voice

Voice punishes prose. What matters, in order:

1. **One idea per turn.** Two sentences maximum. They cannot skim.
2. **Lead with the answer**, then offer detail.
3. **Never read URLs, code, or JSON aloud.** Say what it does and where it is.
4. **Read numbers and codes one character at a time.**
5. **Expect the transcription to mangle names**, including your own product's.
   Tell the agent what it might sound like and to assume it means you.
6. **Say what is out of scope** and what to do in one sentence when it comes up.
