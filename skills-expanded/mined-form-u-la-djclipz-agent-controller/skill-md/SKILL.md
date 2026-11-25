# DJCLIPZ Agent Controller browser skill

Build an agent. Load a set. Perform in the browser.

Use this operating guide only from a browser-capable agent that can interact with the live DJCLIPZ page. DJCLIPZ is experimental and human-authorized. This guide is not an MCP skill, an A2A service, a remotely installable control service, or a claim of universal agent compatibility or full autonomy.

## Common setup for Controller v1.1.0

1. Open DJCLIPZ in normal Chrome.
2. Complete the existing email and consent flow.
3. Attach a browser-capable agent to that same Chrome tab.
4. The human clicks **Start Agent Performance**.
5. Choose exactly one of the control modes below according to the agent's verified browser capabilities.
6. The human retains **Pause Agent**, **Resume Agent**, **Take Over**, and **Stop Performance**.

The measured OpenAI/Codex route is normal Chrome with the ChatGPT/Codex browser extension attached to the active DJCLIPZ tab. The separate Codex in-app browser is not a supported DJCLIPZ playback runtime for this release. This is a measured Controller v1.1.0 compatibility result, not a permanent claim about future runtimes. See the [official OpenAI browser-extension documentation](https://developers.openai.com/codex/chrome-extension).

## Mode A — Visible UI control

Use this path when the browser agent operates the rendered DJCLIPZ interface. It does not require access to page-owned JavaScript.

1. Wait for the human to select **Start Agent Performance**.
2. Continue only while the visible Agent Performance status reads **active**.
3. Operate only visible DJCLIPZ controls and observe their rendered state.
4. Stop issuing commands immediately if the visible status changes to **agent paused**, **human takeover**, **stopped**, or **inactive**, or if the page reloads.
5. Do not simulate, bypass, or replace the human Start, Pause Agent, Resume Agent, Take Over, or Stop Performance controls.

## Mode B — Direct controller access

Use this path only when the browser agent has verified access to page-owned JavaScript.

1. Wait for the human to select **Start Agent Performance**.
2. Confirm that `window.DJCLIPZ.controller` exists.
3. Inspect `controller.version` and `controller.capabilities` before issuing commands.
4. Read `controller.session.getState()` and continue only when `state === "active"`.
5. Check every command result before reading its value or issuing a dependent command.
6. Stop immediately on `agent-paused`, `human-takeover`, `stopped`, `inactive`, `AGENT_PAUSED`, `HUMAN_TAKEOVER`, `SESSION_STOPPED`, `CONTROLLER_INACTIVE`, or reload.

The public controller deliberately has no agent-callable `session.start()` method. Never attempt to call, simulate, or bypass human activation.

Use one result-checking pattern throughout:

```javascript
function requireOk(result) {
  if (!result || result.ok !== true) {
    throw new Error(result?.error || "DJCLIPZ_COMMAND_FAILED");
  }
  return result.value;
}

const controller = window.DJCLIPZ?.controller;
if (!controller) throw new Error("DJCLIPZ_CONTROLLER_UNAVAILABLE");
if (controller.version !== "1.1.0") throw new Error("DJCLIPZ_CONTROLLER_VERSION_MISMATCH");
if (!controller.capabilities?.deck?.includes("play")) {
  throw new Error("DJCLIPZ_CONTROLLER_CAPABILITY_MISSING");
}

const session = controller.session.getState();
if (session?.state !== "active") throw new Error("DJCLIPZ_CONTROLLER_NOT_ACTIVE");
```

## Discover and queue validated media

```javascript
const searchValue = requireOk(await controller.media.search({
  query: "instrumental visual mix",
  maxResults: 5,
}));
if (!Array.isArray(searchValue?.results) || !searchValue.results[0]) {
  throw new Error("DJCLIPZ_NO_VALIDATED_MEDIA");
}

const mediaId = searchValue.results[0].platform_media_id;
const inspectedValue = requireOk(controller.media.inspect(mediaId));
const addedValue = requireOk(controller.queue.add(inspectedValue));
const queueItemId = addedValue.queueItemId;

requireOk(controller.queue.move(queueItemId, 0));
requireOk(controller.queue.setNext(queueItemId));
requireOk(await controller.deck.load("a", queueItemId));
```

Keep the returned stable `queueItemId`; do not substitute a media ID when a queue method requires a queue item ID.

## Perform and observe

```javascript
const handler = (event) => console.log(event.type, event.source, event.reasonCode || "");
requireOk(controller.events.subscribe(handler));

requireOk(controller.deck.setCue("a", "intro", 8));
requireOk(controller.deck.triggerCue("a", "intro"));
requireOk(controller.deck.setBpm("a", 124));
requireOk(controller.deck.setDownbeat("a", 8));
requireOk(await controller.deck.play("a"));
requireOk(controller.mixer.crossfade(100, 4000));

requireOk(controller.events.unsubscribe(handler));
```

Monitor `controller.session.getState()`, `controller.deck.getState("a")`, `controller.deck.getState("b")`, `controller.mixer.getState()`, checked command results, and `controller.events.getRecent()`. On `deck-buffering`, wait and inspect state. On unavailable or stale media, remove or replace the affected stable queue item with another inspected, validated result. A search failure must not interrupt media already playing.

## Stop authority and safety boundaries

- The visible human **Stop Performance** control remains authoritative and immediately ends delegated authority.
- While authority is active, a direct-controller agent may terminate its own performance with `requireOk(controller.session.stop())`. This cannot start or resume a session.
- Respect Pause Agent, Resume Agent, Take Over, and Stop Performance as human authority actions. Do not retry a terminal authority rejection.
- Never load an arbitrary URL, mutate the page DOM as a control mechanism, control another tab or browser session, or attempt remote DJCLIPZ control.
- Use only YouTube results returned or validated through `controller.media`.
- Human mixer UI beat-loop controls are visible but disabled and read **OFFLINE** for YouTube playback.
- Agent beat-loop activation is unavailable. `controller.deck.setBeatLoop(...)` rejects with `BEAT_LOOP_TEMPORARILY_UNAVAILABLE`; do not retry it.
- BPM entry, Tap Tempo, `setDownbeat`, and beat-grid nudge remain available. Typed BPM still requires `setDownbeat`; Tap Tempo in the visible UI establishes a provisional grid after four valid taps.
- Raw-seconds loop methods remain compatibility-only and are not the normal player workflow.
