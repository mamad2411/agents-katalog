---
name: make-integration
description: Build a new Piomio integration (a plugin that connects a service or adds an ability, listed in the Plugins catalog) and install it on this hub. Use when the user wants something no existing integration does, asks to connect a service, or asks you to make a plugin.
---

# Making an integration

An integration is a plugin: one folder with a manifest, English and Russian texts, a server module with tools,
and optionally a card that shows results in the chat. This folder is a complete working one (sunrise and sunset
from sunrise-sunset.org): copy it and change what it does, keep its shape.

```
<id>/
  .piomio-plugin/plugin.json         manifest: id, name, the catalog card, permissions, tools, widgets, settings
  .piomio-plugin/locales/en.json     every text a person reads (English is the source and the fallback)
  .piomio-plugin/locales/ru.json     the same keys in Russian
  server/index.ts                    the tools, and the signals if there are any (TypeScript run directly by Node: no build)
  ui/src/index.tsx                   the card (widget) drawn in the chat, optional
  test/<id>.test.ts                  tests against a fake of the service (in the Piomio repository)
  package.json                       the folder's npm name; `dependencies` only if truly needed
```

## Before you build

1. Call hub_integrations_list: if something already does it, turn it on (hub_integration_connect) instead.
2. Ask the user only what you cannot find out: which service, and whether it needs their account or a key.
   Prefer services that work without a key. Never ask for a key in the chat as text: a key goes into the vault
   through the setup card (see Secrets).

## Steps

1. Pick an id: lowercase letters, digits and dashes, 2–41 characters (e.g. `air-quality`). Tools are exposed as
   `<id with _ for ->_<tool name>`.
2. Copy this skill's folder into your workspace as `integrations/<id>/`, without this SKILL.md.
3. `.piomio-plugin/plugin.json`:
   - `id`; `name` and `description` stay `"%name%"` / `"%description%"` (the texts live in the locales);
   - delete `"builtin"` and `"defaultEnabled"`: an integration installed on a hub is turned on when it is installed;
   - `integration`: `category` (everyday, travel, money, work, reading, communication, home, assistant), `icon`
     (a Lucide icon name, e.g. `cloud-sun`, `plane`, `wallet`), `logo` for a real service (`"./logo.png"`: its logo
     as a 128×128 PNG in the folder, at most 64 KB; the catalog draws it on a white tile instead of the icon),
     `connect` (`none`; `setup` when it needs a key or setup; `signin` for a service's own MCP server with a browser
     sign-in, see below), `summary` and `example` (`"%integration.summary%"`, `"%integration.example%"`); no `popular`;
     `"localApp": true` when its tools drive an app on the hub's own computer (Blender): a task whose brain runs on
     another computer then does not get them and uses that computer's own app;
   - `permissions.network`: the exact hosts it calls (`api.example.com`, `*.example.com`); never `"*"` unless the
     user gives the addresses at run time;
   - `contributes.widgets`: the card kinds the tools show (`[]` and no `ui` when there is no card);
   - `contributes.signals`: only if the service can start the person's triggers (see Signals); when it has none,
     delete it along with the `sunrise` provider in `server/index.ts` and its `signal.sunrise.title` texts;
   - `contributes.settings`: a JSON Schema of the person's settings, only if there are any.
4. `locales/en.json` and `locales/ru.json`: the same keys, natural text in each language. Tool descriptions and tool
   results are for the model: English, in the code, not in the locales.
5. `server/index.ts`: register the tools in `activate(ctx)`.
   - A tool has a `name`, a `description` that tells the model when to use it and what to pass, an `inputSchema`,
     and an `effect`: `read` (looks something up), `local-write` (changes something on the hub), `external` (acts in
     the world: sends, books, pays; the user approves each call). Set `source: true` when the result comes from
     outside (web pages, APIs).
   - Validate the input and answer mistakes with `isError` text the model can act on. Catch network errors; use
     `AbortSignal.timeout(…)` on every request; send a User-Agent naming Piomio.
   - To show a card: `ctx.widgets.show(call, "<kind>", data)` with plain JSON (under 64 KB), and say in the result's
     text that a card is shown so the model does not repeat it.
   - Read settings from `ctx.settings` and `ctx.onSettingsChange`. Keep an address setting (`apiUrl`) for tests.
   - Only erasable TypeScript: no enums, namespaces or parameter properties; `import type` for types. No npm
     packages unless unavoidable (then list them in package.json `dependencies`; they install without scripts).
6. `ui/src/index.tsx`: one file that imports only `react` and `@piomio/ui` (and `import type` from the server). It
   draws each widget kind with `ui.widgets.add(kind, Component)`; texts come from `ui.i18n.t`. Style with inline
   styles and the page's CSS variables (`var(--muted)`, `var(--border)`, `var(--surface-2)`, `var(--accent)`). The hub
   compiles it when installing.
7. Check it: `node --check` cannot read TypeScript, so run `node server/index.ts` from the folder: it must exit with
   no error. Read your manifest and both locale files once more: every `"%key%"` must exist in both.
8. Install: call hub_plugin_install with `source: "integrations/<id>"`. The user sees what it asks for and allows
   it. Then tell them in a sentence what it does and suggest the example to try. To change it, edit the folder and
   install again: the new version replaces the old one.

## Secrets

A key or token never goes into the code, the settings or the chat. Declare it and the hub asks for it on a setup
card, straight into the vault:

```json
"contributes": { "setup": { "secrets": [ { "vault": "<id>_api_key", "setting": "apiKey", "title": "%setup.key.title%",
  "hint": "%setup.key.hint%", "link": "https://example.com/account/keys", "required": true } ] } },
"permissions": { "vault": ["<id>_api_key"] }
```

and set `"connect": "setup"` in `integration`. In the code: `const { value } = await ctx.vault.get("vault://<id>_api_key")`
when a tool needs it; when it is missing, answer that the user should connect the integration (hub_plugin_setup shows
the card).

A secret the integration makes itself (the session key of an account it signs in to, not a key the person pastes) goes
into the vault too: `await ctx.vault.put("vault://<id>_session", { value }, { name })`, and `ctx.vault.remove(ref)` when
the account is signed out. List the id in `permissions.vault`; the item can then be read by this integration alone.
Such an integration has `"connect": "setup"`, its own card (a settings section in `ui/`, which the setup card shows)
and says how it stands with a catalog entry under its own id: `ctx.catalog.update([{ id: ctx.pluginId, status:
"connected" | "needs-setup" | "broken", connect: "setup", account? }])` (see `integrations/telegram-account`).

## Signals

A signal is something that happened, which can start the person's triggers (a new feed item, a sensor reading, a
sunrise). Declare one when the service has events the person would want an agent to react to, not for every fact a
tool can look up: a lookup is a tool. The hub shows each source to the agents as `<id>.<type>` (`sun.sunrise`), and
a trigger subscribes to it with `on: [{ type: "sun.sunrise", config: { … } }]`.

```json
"contributes": { "signals": [ {
  "type": "sunrise", "mode": "subscribe", "title": "%signal.sunrise.title%",
  "description": "The sun rose at a place (English, for the model).",
  "config": { "type": "object", "properties": { "lat": { "type": "number" } }, "required": ["lat"] },
  "data": { "type": "object", "properties": { "place": { "type": "string" } }, "required": ["place"] },
  "sample": { "place": "Lisbon" }, "external": true } ] }
```

- `type`: lowercase letters, digits and `_`, starting with a letter; one declaration per type. `title` goes through the
  locales (`"%key%"`); `description` is English, for the model.
- **Broadcast** (`"mode": "broadcast"`, the default): the plugin sends a signal whenever something happens, from
  anywhere in its code: `ctx.signals.emit("alert", data, { key, subject })`. Use it when the plugin is already
  listening (a webhook it serves, a socket it keeps) whatever the triggers do.
- **Subscribe** (`"mode": "subscribe"`): the plugin works only while a trigger listens. It gives a provider,
  `ctx.signals.provide("sunrise", { subscribe(sub, emit) { …; return { stop() { … } }; } })`. The hub calls
  `subscribe` once per distinct config (`sub.config` is the person's config, checked against the `config` schema),
  and `stop` when no enabled trigger uses it. It calls `subscribe` again when the plugin restarts, so keep the state
  that matters (what was seen) in `ctx.storage`, keyed by the whole config so two subscriptions never share it, and
  never hold a timer, socket or poll after `stop`. Use it for polling or watching something for the person
  (`integrations/_template` waits for the sunrise; the `web` plugin's `rss_item` reads a feed). Check the config in
  `subscribe` and throw with a clear reason when it cannot work (the hub logs it and tries again later). Do the first
  network call without making `subscribe` wait for it, tell failures to `ctx.log` and try again at the next interval,
  never ask the service again at once in a loop, catch every rejection of your own async work, and never send a
  signal for something you could not read. Take the poll interval from the config only: never from a setting (an
  agent can change settings), and never more often than every 10 minutes.
  When a subscription can no longer work after it was taken (the account it reads was signed out), call the
  third argument, `subscribe(sub, emit, fail)`, with the reason: its handle is stopped and the hub tries it again
  later.
- `emit(data, { key, subject })`: `key` is the event's identity (a feed item's id, a date); the hub drops a second
  signal with the same key to the same trigger within 24 hours, so a repeat poll or a restart does not wake the agent
  twice. `subject` is a short line naming the event for people and the model (the item's title). Neither is
  required; without a key every signal counts.
- `data` schema: a JSON Schema of what `emit` sends, at most 16 KB and 32 levels deep; the hub refuses a signal that
  does not match it, or whose data is over 256 KB, and the plugin's log says why. Keep it plain, since it runs on the
  hub against outside content:
  - patterns run on V8's linear-time engine and without flags: no backreferences, lookahead or lookbehind; no counted
    repeat over 16 (`{17}`, `{1,20}`, `{0,200}`, `{17,}`) and none inside another counted repeat (for a length, use
    `minLength` / `maxLength` and a plain `+` or `*` in the pattern); no `\p{…}` classes or `\u{…}` escapes (write
    `\uXXXX`); no case-insensitive match (write `[Aa]`);
  - no `uniqueItems`, no `$ref` or `$dynamicRef` (write the schema out), no `$async`, no enum of more than 1000
    values, at most 100 patterns;
  - `format` is not checked: say it in the `description` and check it in your code.

  A source with a schema that breaks these is refused whole: it is left out of trigger_sources' list and shown in its
  `Refused` part with why, the plugin's log says why, and the testkit's `startPlugin` fails with the same reason. The
  `config` schema follows the same rules; give each field a `description` so an agent can fill it, and `minimum` for
  intervals (poll no more often than every 10 minutes). A trigger whose config the schema refuses is not made.
- `external`: whether the signal's text comes from outside (the internet, other people, a service's API). Triggers
  treat an external signal's text as untrusted: it is not shown in notes, and the agent it wakes is marked tainted.
  Declare `true`. A plugin the person or an agent installs is always external, whatever its manifest says: only the
  hub's own built-in plugins may declare `false`, for data that no stranger could have written.
- Only types in `contributes.signals` can be emitted; the hub allows a plugin 600 signals a minute.
- Test with the testkit: `h.subscribeSignal("sunrise", config)` starts the provider (and rejects a config the
  `config` schema refuses, as the hub would not subscribe), `h.signals` lists what it sent, `h.stopSignal(id)` stops it
  (see `test/sun.test.ts`). The testkit checks every signal as the hub does: what the hub refuses is not in
  `h.signals`, and `h.logs` says why.
- After installing, call trigger_sources: your source must be in the list, not under `Refused`.

## A service with its own MCP server

When the service runs an official MCP server (Streamable HTTP, often with a browser sign-in: Granola, for one), the
integration needs no code: a manifest, the locales and an `.mcp.json` beside `.piomio-plugin/` (see
`integrations/granola`):

```json
{ "mcpServers": { "<id>": { "type": "http", "url": "https://mcp.example.com/mcp" } } }
```

Name the server like the integration's id, so its tools are `<id>_<tool>`. With `"connect": "signin"` the hub signs in
for the person (OAuth discovery, client registration, PKCE; the tokens go into the vault): the catalog and its card in
the chat show a Sign in button. A built-in integration may list the server's tools that only read in `"readTools"`
(they then run without asking); other tools ask the person each time.

A server that runs on this computer (stdio) is a `command` instead of a `url`. `${PIOMIO_NODE}` is the hub's own Node
(a launcher written in TypeScript runs on it, nothing to install), `${PIOMIO_PLUGIN_ROOT}` the integration's folder and
`${PIOMIO_PLUGIN_DATA}` its data folder; the server reaches only the hosts in `permissions.network`. When it cannot
start, it says why on stderr and exits: its last line is what the person sees on the integration. `integrations/blender`
is one: its launcher finds the app, prepares the official server and relays MCP to it.

```json
{ "mcpServers": { "<id>": { "command": "${PIOMIO_NODE}", "args": ["${PIOMIO_PLUGIN_ROOT}/mcp/launch.ts"], "env": { "DATA": "${PIOMIO_PLUGIN_DATA}" } } } }
```

## Several apps through one outside service

An integration that connects many apps through a hosted service (`integrations/composio`: Slack, GitHub, Gmail… via
Composio) lists each app as a catalog entry of its own, and says which outside service they go through:

```json
"integration": {
  "category": "other", "icon": "plug", "connect": "setup", "summary": "%integration.summary%",
  "via": { "name": "Composio", "about": "%via.about%", "link": "https://composio.dev" },
  "entries": [{ "id": "slack", "name": "Slack", "summary": "%entry.slack%", "category": "work", "icon": "message-square", "example": "%example.slack%" }]
}
```

- Entries show in the catalog as `<id>:<entry>` (`composio:slack`), even while the integration is off. `via` puts the
  service's badge on each; its `about` (`{name}` is the entry's name) is the note the badge opens: say plainly who
  keeps the account's keys and who sees the calls.
- The running plugin reports every entry's state, and entries it adds, with `ctx.catalog.update([{ id, status, connect,
  account?, detail? }])` (`status`: `connected`, `needs-setup` or `broken`; `connect`: `setup` while its own key is
  missing, else `signin`). Added entries carry `name`, `summary`, `category`, `icon` too; keep them in `ctx.storage`
  and report them again on start.
- `ctx.catalog.onSignIn(entry => ({ url }))` gives the address of the entry's Sign in button; report the entry
  `connected` once it works (poll the service: nothing comes back to the hub, so a phone can sign in too), and the
  chat that asked hears it. `ctx.catalog.onSignOut(entry => …)` signs it out; `ctx.tools.unregister(name)` takes back
  its tools.

## In the Piomio repository

Built-in integrations live in `integrations/` (this template is `integrations/_template`). People adding one work only
in its folder:

- `npm run new:integration -- <id>` copies this template to `integrations/<id>/` with the id filled in;
- built-in ones keep `"builtin": true` and `"defaultEnabled": false` (they wait in the catalog until turned on);
  `"popular": <n>` puts one among the catalog's popular picks;
- test with `@piomio/testkit`'s `startPlugin` against a fake of the service (see `test/sun.test.ts`), then
  `npx vitest run integrations/<id>`, `npm run typecheck` and `npm run build:ui-plugins`;
- every text a person reads goes through the locales; `packages/core/test/i18n.test.ts` checks both languages.

The plugin API in full: `docs/plugins.md` in the repository.
