---
name: twilio-voice-conversation-relay
version: 1.0.0
description: Build low-latency voice AI agents on Twilio using ConversationRelay, streaming your own LLM over a WebSocket while Twilio handles STT and TTS.
author: matrixx0070
tags: [twilio, voice, conversationrelay, websocket, ai]
capabilities: []
---

## When to use

Use this when you want a real-time, barge-in-capable voice agent on a phone call and you want to bring your own LLM. Twilio's `<Connect><ConversationRelay>` verb offloads speech-to-text and text-to-speech to Twilio and streams structured events to your WebSocket server; you reply with text tokens and Twilio speaks them. This is the right tool for conversational IVR replacement, AI receptionists, and outbound voice bots.

**Not for:** raw audio processing where you need the media frames yourself (use `<Connect><Stream>` Media Streams instead — see the aside below); multi-party bridging (see twilio-conference-calls); or recording flows (see twilio-call-recordings).

## Method

1. Point your incoming-call webhook (Voice URL on the number) at an endpoint that returns TwiML containing `<Connect><ConversationRelay>`.
2. Set `url` to your `wss://` endpoint. Decide TTS/STT: pick `ttsProvider` (e.g. `ElevenLabs`, `Amazon`, `Google`) and `voice`, plus `transcriptionProvider` and `language`. Decide interruption behavior with `interruptible` and DTMF capture with `dtmfDetection`.
3. On WebSocket connect, Twilio sends a `setup` message (callSid, from, to, custom parameters). Cache session state keyed by `callSid`.
4. On each caller utterance Twilio sends a `prompt` message with the transcribed `voicePrompt`. Feed it to your LLM.
5. Stream the LLM output back as `text` token messages. Set `last: true` on the final token so Twilio knows the turn is complete and can flush TTS.
6. Decision point — barge-in: if the caller speaks while TTS is playing and `interruptible` is on, Twilio sends an `interrupt` event with `utteranceUntilInterrupt`. Stop generating, discard the truncated turn, and wait for the next `prompt`.
7. Decision point — DTMF: if `dtmfDetection` is on, key presses arrive as `dtmf` events. Route to menu logic instead of the LLM when appropriate.
8. Handoff / end: send an `end` message (or a live-agent transfer) to hand control back to TwiML. You can return new TwiML via a `<Redirect>` handoff to dial a human.
9. Handle `error` events: log and gracefully close.

## Example

TwiML returned by your Voice webhook:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <ConversationRelay
      url="wss://example.com/relay"
      welcomeGreeting="Hi, how can I help you today?"
      ttsProvider="ElevenLabs"
      voice="21m00Tcm4TlvDq8ikWAM"
      transcriptionProvider="Deepgram"
      language="en-US"
      dtmfDetection="true"
      interruptible="true" />
  </Connect>
</Response>
```

WebSocket handler sketch (Node):

```js
import { WebSocketServer } from "ws";
const wss = new WebSocketServer({ port: 8080 });

wss.on("connection", (ws) => {
  let callSid;
  ws.on("message", async (raw) => {
    const msg = JSON.parse(raw);
    switch (msg.type) {
      case "setup":
        callSid = msg.callSid;
        break;
      case "prompt": {
        const stream = await llm.stream(msg.voicePrompt);
        for await (const token of stream) {
          ws.send(JSON.stringify({ type: "text", token, last: false }));
        }
        ws.send(JSON.stringify({ type: "text", token: "", last: true }));
        break;
      }
      case "interrupt":
        llm.abort(); // caller barged in; drop the rest of this turn
        break;
      case "dtmf":
        handleKeypad(msg.digit);
        break;
      case "error":
        console.error("relay error", msg.description);
        break;
    }
  });
});
```

## Pitfalls

- Forgetting `last: true` on the final text message leaves Twilio waiting; the caller hears silence until the turn times out.
- Not aborting your LLM stream on `interrupt` causes stale audio to play after the caller has moved on.
- The WebSocket must be `wss://` (TLS). Plain `ws://` is rejected.
- Custom parameters are passed via `<Parameter>` children and arrive only in the `setup` event — not on later messages.
- `welcomeGreeting` plays before the first `prompt`; do not also send an opening line from your LLM or the caller hears it twice.
- One `<ConversationRelay>` per `<Connect>`; `<Connect>` is terminal — TwiML after it does not execute until relay ends.

## Output format

Your WebSocket sends JSON messages: `{ type: "text", token, last }` for speech, plus optional control messages (`{ type: "end" }`, language switch, or a play/DTMF instruction). Twilio sends you `setup`, `prompt`, `interrupt`, `dtmf`, and `error` messages. All are UTF-8 JSON text frames.

## Reference

- TwiML verb: `<Connect><ConversationRelay>`. Key attributes: `url` (wss, required), `welcomeGreeting`, `ttsProvider`, `voice`, `transcriptionProvider`, `language` (BCP-47, default `en-US`), `dtmfDetection`, `interruptible`, `hints`, `profanityFilter`. Add `<Parameter name="" value=""/>` children for custom setup data.
- Inbound WS message types: `setup`, `prompt`, `interrupt`, `dtmf`, `error`. Outbound: `text` (with `token`, `last`), `end`, `play`, `sendDigits`, language switch.
- ConversationRelay is billed on top of standard voice per-minute rates plus the chosen STT/TTS provider usage. Twilio handles the media path; you never touch raw audio.
- Aside — raw media: `<Connect><Stream url="wss://...">` (Media Streams) streams base64-encoded audio frames (mulaw, 8000 Hz, 20 ms chunks) in both directions. Use it only when you need the PCM/mulaw yourself; you then own STT/TTS. ConversationRelay is the higher-level, lower-effort path.
- Media/event delivery is real-time over a single persistent WebSocket per call; Twilio closes it when the call ends or `<Connect>` is redirected.
