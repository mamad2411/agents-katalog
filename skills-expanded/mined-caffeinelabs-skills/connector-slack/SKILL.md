---
name: connector-slack
description: >-
  EXPERIMENTAL, UNTESTED recipe for posting messages to a Slack workspace from a
  Caffeine canister via the `slack-client` mops package (Slack Web API). Use it
  when the user wants their app to send a message to a Slack channel — "post to
  Slack", "notify a channel", "send a Slack message", or equivalent. The client
  is a pre-release 0.1.0 drop (bot `xoxb-` or user `xoxp-` token): its request path is verified against the live
  Slack API (a real message posts), but the success-response decode is not yet
  runtime-confirmed, so treat it as a starting point and do NOT present Slack as
  a fully supported platform feature yet. Hand-rolling `ic.http_request` calls to `slack.com/api` is still the wrong
  move — prefer the generated client so bearer auth, percent-encoding, and JSON
  parsing come for free.
version: 0.1.1
caffeineai-subscription: [none]
compatibility:
  mops:
    slack-client: "0.1.0"
    caffeineai-authorization: "~1.0.1"
---

# Slack Connector (experimental)

Post messages to a Slack workspace from a Caffeine canister.

> ⚠️ **Experimental (`slack-client@0.1.0`).** **Verified against live Slack:** the
> request path — a real `chat.postMessage` posts (the earlier query-vs-form bug is
> resolved; POST params go in an `application/x-www-form-urlencoded` body).
> **Implemented in 0.1.0 but not yet exercised live:** the success-response decode
> (`{"ok":true,…}` → the success schema) and the `{"ok":false}` error-envelope
> routing (see *Known limitations* for what each does). The response side is
> therefore code-complete but unproven — `diagnostics` is on, so a decode failure
> surfaces the raw Slack body. Don't present Slack as a fully supported platform
> feature until **one live run confirms a decoded success reply**; that condition,
> not a version number, is the gate.

## Orchestrator routing notes

Load this skill when the user, spec, or a prior task mentions Slack, posting to a
channel, or notifying a Slack workspace. The generated `slack-client` package is
the preferred path; raw `ic.http_request` to `https://slack.com/api/*` is an
anti-pattern that re-implements auth, percent-encoding, and JSON parsing by hand.

Intent → capability mapping:

| User intent | Capability |
| --- | --- |
| Post a message to a Slack channel as the app | `slack-client` `chatPostMessage` with a bot token (`xoxb-`) |
| Post to Slack *as a named person* | `slack-client` `chatPostMessage` with a user token (`xoxp-`) |

Before generating code, **report the token choice back to the prompting user**
(bot vs user — see *Auth model* for the one-line rule and the trade-offs) and
tell them where to obtain it. They cannot proceed without pasting a token, so
surfacing this early avoids an app that traps on first use.

The token is something a **human has to go and create**, so the build is not
done when the backend compiles. It is done when the app itself tells the admin
how to get a token and gives them somewhere to paste it — see *Obtaining a bot
token* for the steps, *Scopes to request* for what to tick, *Addressing a
channel* for the channel ID, and *Frontend* for the page that MUST ship. Repeat
those steps in the completion message too; the chat outlives neither the app nor
the admin's memory.

Scope of this generated drop: the messaging-core families `chat`,
`conversations`, `users`, `files`, `reactions`, and `pins` (10 API modules) —
see *Available API surface* for the per-module breakdown.
Other Slack methods are out of scope until the spec is regenerated.

## Auth model — bot token (`xoxb-`) or user token (`xoxp-`)

Both are bearer credentials and the client treats them identically, but they
differ in *who* the workspace sees acting. **Ask the prompting user which one they
want before writing code, and state the trade-off** — the answer changes what
their app looks like in Slack, and it cannot be swapped later without a
re-install.

| The user wants messages to appear as… | Token | Consequences to report back |
| --- | --- | --- |
| **the app itself** (posts show the app's name with an `APP` badge) | **`xoxb-`** *(default — prefer this)* | One workspace-wide credential, independent of any employee. The bot must be invited to every channel it posts in (`/invite @YourApp`), else Slack answers `not_in_channel`. Cannot see private channels or DMs it isn't in. |
| **a specific person** (posts show that human's name and avatar) | **`xoxp-`** | Every action is attributed to, and audited as, that person. Reaches whatever they can reach, no channel invite needed. Dies when they leave the workspace or revoke the app. Required for a few user-only APIs (e.g. `search.messages`). |

If the request is "post notifications/alerts from my app", that is `xoxb-`. Only
choose `xoxp-` when the user explicitly wants messages to look like they came
from a human, or needs a user-only API. Say which you picked and why.

### Obtaining a bot token (`xoxb-`)

1. <https://api.slack.com/apps> → **Create New App** → *From scratch*, pick the
   workspace.
2. **OAuth & Permissions** → *Scopes* → **Bot Token Scopes**: add the scopes the
   build needs — `chat:write` at minimum; see *Scopes to request* below for the
   rest, and get the list right now (a later addition forces a reinstall).
3. **Install to Workspace** → authorize → copy the **Bot User OAuth Token**,
   which starts with `xoxb-`.
4. In Slack, invite the app to each target channel: `/invite @YourApp`. Skipping
   this is the most common first failure (`not_in_channel`).

### Scopes to request

Step 2 above decides what the app can do — the admin cannot guess the list, so
**derive it from the features the build actually uses** and show exactly those in
the settings UI (see *Frontend*). Bot-token scopes:

| The app needs to… | Bot scope |
| --- | --- |
| Post to a channel the bot has been invited to | `chat:write` |
| Post to **any public** channel with no invite | `chat:write.public` |
| Resolve a channel name → ID, list public channels | `channels:read` |
| List the private channels the bot is in | `groups:read` |
| Read messages (`conversationsHistory` / `conversationsReplies`) | `channels:history`, plus `groups:history` for private |
| List / look up users | `users:read`, plus `users:read.email` for `usersLookupByEmail` |
| DM a person (`conversationsOpen` → `chatPostMessage`) | `im:write` |
| Add emoji reactions | `reactions:write` |
| Pin messages | `pins:write` |
| Upload / read files | `files:write`, `files:read` |

> ⚠️ **Adding a scope later invalidates the token.** Slack requires a
> **reinstall** after any scope change, and the reinstall issues a *new* `xoxb-`
> — the old one keeps working for existing scopes but never gains the new one,
> so the app fails with `missing_scope` until the admin pastes the new token.
> Get the scope list right the first time, and make the settings page
> re-pasteable rather than one-shot.

### Obtaining a user token (`xoxp-`)

1. Same app → **OAuth & Permissions** → *Scopes* → **User Token Scopes** (a
   *separate* list from bot scopes): add e.g. `chat:write`, `search:read`.
2. **Install to Workspace** (or *Reinstall*, if the app already exists) and
   authorize — the token represents **whoever clicks Allow**.
3. Copy the **User OAuth Token**, which starts with `xoxp-`.

A single admin-supplied `xoxp-` is supported by this recipe: it goes through the
same setter and the same `config.auth`. What is **out of scope** here is per-user
OAuth, i.e. each end-user authorising their own account — that needs a full
redirect + code-exchange + refresh flow, for which no Slack helper exists yet.
Do not attempt to hand-roll it.

### Handing the token to the canister

Whichever flavour, the workspace admin pastes it into the canister through an
**admin-gated** setter — gated on
`AccessControl.hasPermission(state, caller, #admin)`. The token is held by the
canister only and is **never** returned to the frontend.

> ⚠️ **Never gate the setter on a first-caller-claims-ownership scheme.** On the
> IC every unauthenticated caller is the *same* anonymous principal, so if an
> anonymous call claims ownership first, every anonymous caller passes the
> `caller == owner` check and can overwrite the workspace token. Use the
> authorization component's `#admin` permission, as the example below does.

The canister then hands that token to the client **only** through
`config.auth = ?#bearer(token)`, which every method turns into an
`Authorization: Bearer …` header. No method takes a token argument and no method
puts the credential in the URL, so it cannot leak through a logged query string.

## Outcalls are already non-replicated

`defaultConfig` ships `is_replicated = ?false`, so anything derived from it with
record update is correct as-is — nothing to remember, nothing to add.

Do not override it to `?true` or `null`. A replicated outcall repeats the request
from every node in the subnet, which for Slack means the message is posted once
per replica (~13 duplicates), the `Authorization: Bearer xoxb-…`/`xoxp-…` header
leaves every node, and consensus fails anyway because Slack's reply carries a
per-request `ts`.

# Backend

## Add dependencies

The admin gate in the recipe below needs the authorization component alongside
the client:

```bash
mops add slack-client@0.1.0
mops add caffeineai-authorization@1.0.1
```

The generated function is
`ChatApi.chatPostMessage(config, channel, asUser, attachments, blocks,
iconEmoji, iconUrl, linkNames, mrkdwn, parse, replyBroadcast, text, threadTs,
unfurlLinks, unfurlMedia, username)`. Pass empty strings / `false` for the
options you don't use. The token is **not** an argument — it travels only in
`config.auth` (see *Auth model* above); this holds for every method in the
client.

```motoko filepath=src/backend/main.mo
import AccessControl "mo:caffeineai-authorization/access-control";
import MixinAuthorization "mo:caffeineai-authorization/MixinAuthorization";
import MixinSlackConfig "mixins/slack-config";
import MixinSlackMessaging "mixins/slack-messaging";

actor {
  let accessControlState : AccessControl.AccessControlState;
  include MixinAuthorization(accessControlState, null);

  // Admin-held Slack token, `xoxb-…` or `xoxp-…` — never returned to the frontend.
  let slackConfig : { var token : Text };
  include MixinSlackConfig(accessControlState, slackConfig);
  include MixinSlackMessaging(slackConfig);
};
```

The migration chain head:

```motoko filepath=src/backend/migrations/00000000_000000.mo
import AccessControl "mo:caffeineai-authorization/access-control";

module {
  type NewActor = {
    accessControlState : AccessControl.AccessControlState;
    slackConfig : { var token : Text };
  };

  public func migration(_old : {}) : NewActor {
    {
      accessControlState = AccessControl.initState();
      slackConfig = { var token = "" };
    };
  };
};
```

```motoko filepath=src/backend/mixins/slack-config.mo
import AccessControl "mo:caffeineai-authorization/access-control";
import Runtime "mo:core/Runtime";

mixin (
  accessControlState : AccessControl.AccessControlState,
  slackConfig : { var token : Text },
) {
  public query func isSlackConfigured() : async Bool {
    slackConfig.token.size() > 0;
  };

  // Admin-only; accepts either token flavour. NOTE: `#admin` — never a
  // first-caller-claims-ownership check,
  // which the shared anonymous principal would defeat.
  public shared ({ caller }) func setSlackToken(token : Text) : async () {
    if (not AccessControl.hasPermission(accessControlState, caller, #admin)) {
      Runtime.trap("Unauthorized: Only admins can set the Slack token");
    };
    slackConfig.token := token;
  };
};
```

```motoko filepath=src/backend/mixins/slack-messaging.mo
import Principal "mo:core/Principal";
import Runtime "mo:core/Runtime";
import { chatPostMessage } "mo:slack-client/Apis/ChatApi";
import { defaultConfig; type Config } "mo:slack-client/Config";

mixin (slackConfig : { var token : Text }) {
  // Token rides `config.auth`; `defaultConfig` is already non-replicated.
  func slackClientConfig(token : Text) : Config {
    {
      defaultConfig with
      auth = ?#bearer(token);
      max_response_bytes = ?(1_000_000 : Nat64);
    };
  };

  // Post `text` to `channel` (channel ID like "C012AB3CD" or "#general").
  // Returns the posted message timestamp (`ts`).
  public shared ({ caller }) func postSlackMessage(channel : Text, text : Text) : async Text {
    if (caller.isAnonymous()) Runtime.trap("Sign in to post to Slack");
    if (slackConfig.token.size() == 0) {
      Runtime.trap("Slack is not configured (an admin must set the token)");
    };
    let res = await* chatPostMessage(
      slackClientConfig(slackConfig.token), // token rides config.auth — never a URL param
      channel,
      "", "", "", "", "", // asUser, attachments, blocks, iconEmoji, iconUrl
      false, // linkNames
      true, // mrkdwn
      "", // parse
      false, // replyBroadcast
      text, // text
      "", // threadTs
      false, // unfurlLinks
      false, // unfurlMedia
      "", // username
    );
    res.ts;
  };
};
```

## Addressing a channel — an ID, and the bot must be in it

`chatPostMessage`'s first argument is a **channel ID**: `C…` for a public or
private channel, `D…` for a DM, `G…` for a legacy group. A `#general`-style name
still resolves for *public* channels but is deprecated and never works for
private ones — prefer the ID and store it, don't hardcode a name.

**Where a human finds an ID** (put these words in the UI, not just in the
completion message):

- Open the channel → click its name in the header → **About** tab → the ID sits
  at the bottom of the panel (`C012AB3CD`), with a copy button.
- Or right-click the channel in the sidebar → *Copy link* → the ID is the last
  path segment of `…/archives/C012AB3CD`.

**Where the canister gets one:** `ConversationsApi.conversationsList` and match
on `name` (needs `channels:read`). Resolve once and cache the ID in a stable
variable — do not resolve on every post; it doubles the outcalls and the cycles.

**The bot must be a member**, or `chatPostMessage` answers `not_in_channel` —
the single most common first failure. Three ways out, in order of preference:

1. the admin runs `/invite @YourApp` in the target channel;
2. grant `chat:write.public`, which lets the bot post to any *public* channel
   with no invite at all;
3. call `conversationsJoin` (public channels only, needs `channels:join`).

**To DM a person:** `usersLookupByEmail` (needs `users:read.email`) or
`usersList` → user ID → `conversationsOpen` → post to the `D…` channel it
returns. Needs `im:write`.

## Available API surface

The drop ships **10 API modules / ~140 operations**. Only `chatPostMessage` is
runtime-verified (see *Known limitations*); the rest are generated from the same
spec and typecheck, but treat their response decode as unproven.

| Module | For | Representative functions |
| --- | --- | --- |
| `ChatApi` | posting, editing, deleting, permalinks | `chatPostMessage`, `chatUpdate`, `chatDelete`, `chatPostEphemeral`, `chatScheduleMessage`, `chatGetPermalink` |
| `ChatScheduledMessagesApi` | scheduled-message queue | `chatScheduledMessagesList` |
| `ConversationsApi` | channels: list, read, membership, lifecycle | `conversationsList`, `conversationsHistory`, `conversationsReplies`, `conversationsInfo`, `conversationsOpen`, `conversationsJoin`, `conversationsInvite`, `conversationsCreate` |
| `UsersApi` | directory lookups, presence | `usersList`, `usersInfo`, `usersLookupByEmail`, `usersConversations`, `usersGetPresence` |
| `UsersProfileApi` | profile fields | `usersProfileGet`, `usersProfileSet` |
| `ReactionsApi` | emoji reactions | `reactionsAdd`, `reactionsRemove`, `reactionsList` |
| `PinsApi` | pinned messages | `pinsAdd`, `pinsRemove`, `pinsList` |
| `FilesApi` | file listing / metadata / sharing | `filesList`, `filesInfo`, `filesDelete` |
| `FilesCommentsApi` | file comments | `filesCommentsDelete` |
| `FilesRemoteApi` | external-file registry | `filesRemoteAdd`, `filesRemoteInfo`, `filesRemoteList` |

Binary upload/download is **not** usable from this client (multipart bodies are
outside the generated JSON/form surface). `filesRemoteAdd`, which registers a
file that lives at an external URL, is the supported alternative.

# Frontend

Slack needs **no OAuth callback**: the credential is a long-lived token the
admin pastes, so there is no redirect URI, no `/connect/slack` route, and no
per-user handshake. Do not build one. What a Slack build MUST ship is the page
that lets the admin *get* and *enter* the token — these are **acceptance
criteria, not suggestions**, and a build missing them is **broken, not merely
incomplete**:

- **The token page exists and is reachable.** A "post to Slack" feature with no
  page to enter a token is unusable. A signed-in admin must reach
  `/settings/slack` from the nav or from the not-configured prompt.
- **The token-generation steps are in the UI**, not only in the agent's chat
  reply. The admin returns to this page weeks later, after the chat is gone.
- **The exact scope list is displayed.** The admin cannot infer which scopes
  this app needs; show the ones the build actually uses (*Scopes to request*).

1. **A login flow — required.** `setSlackToken` gates on `#admin`, so the app
   needs non-anonymous callers. Take login, `useInternetIdentity` / `useActor`
   plumbing, and the admin-role gate from
   [`extension-authorization`](../extension-authorization/SKILL.md).

2. **An admin settings page** — `/settings/slack` (admin-gated). Required:
   - A "How to get your Slack bot token" panel **above** the input, framed as a
     one-time ~5-minute setup, with these numbered steps (the agent's completion
     message must repeat them verbatim):
     1. open <https://api.slack.com/apps> → **Create New App** → *From
        scratch* → name it and pick the workspace;
     2. **OAuth & Permissions** → *Scopes* → **Bot Token Scopes** → add the
        scopes listed on this page;
     3. **Install to Workspace** → *Allow* → copy the **Bot User OAuth Token**
        (it starts with `xoxb-`);
     4. paste it below and save;
     5. in Slack, run `/invite @YourApp` in every channel the app posts to.
     Include a convenience link that opens <https://api.slack.com/apps>.
   - The scope list rendered as copyable text — exactly the scopes this build
     uses, not the whole table.
   - One **password input** bound to `setSlackToken(token)`. Submit on enter,
     clear on success, and keep it re-pasteable: a scope change forces a
     reinstall and a new token, so this is not a one-shot form.
   - Status driven by `isSlackConfigured()` (`Bool`) — "Configured" / "Not
     configured". **Never** render the token back, not even masked-with-suffix.
   - If the app posts to a fixed channel, its ID belongs on this page too:
     extend the config mixin to `{ var token : Text; var channel : Text }` with
     an admin-gated `setSlackChannel`, and put the "where to find a channel ID"
     hint (see *Addressing a channel*) inline next to the field. Do not make
     users type a raw ID with no explanation of where it comes from.
   - **Make the page reachable.** The shared Layout nav MUST link here when
     `isCallerAdmin` is true and hide it otherwise. Add the link where the nav
     is defined, not inside this page.

3. **Empty-state nudges.** When `isSlackConfigured()` is `false`, never render a
   dead "Send to Slack" button: admins get a "Set up Slack" link to
   `/settings/slack`; non-admins get an explanation — e.g. "Slack isn't set up
   yet — an administrator needs to add the workspace token in Settings."

4. **Translate Slack's errors.** Logical failures arrive as *rejected* calls
   whose message carries Slack's own `error` string (see *Known limitations*).
   Map at least these three to an action instead of showing the raw reject:
   - `not_in_channel` → "Invite the app to the channel: `/invite @YourApp`"
   - `invalid_auth` / `not_authed` → "The Slack token is invalid — paste a new
     one in Settings" (admins get the link)
   - `channel_not_found` → "Check the channel ID" (with the how-to-find hint)
   - `missing_scope` → "The app needs another Slack scope — add it, reinstall,
     and paste the new token"

Suggested route layout:

```
/                →  Main UI (any signed-in user; empty-state when unconfigured)
/settings/slack  →  Admin token + default channel (admin-only)
# No /connect/slack: Slack uses a pasted long-lived token, not a redirect flow.
```

## What the composer must tell the Caffeine user

The app cannot work until a human creates a Slack app and pastes a token, so the
**completion message in the composer is part of the deliverable**, not a summary
of it. It MUST contain, in this order:

1. **That a token is required, and who enters it** — an admin, on
   `/settings/slack`, reachable from the nav once signed in.
2. **The five numbered steps verbatim** from *Frontend* item 2: create the app at
   <https://api.slack.com/apps>, add the bot scopes, *Install to Workspace*, copy
   the `xoxb-…` token, paste it, then `/invite @YourApp` in each target channel.
3. **The exact scope list this build needs**, from *Scopes to request* — as text
   the user can copy straight into Slack's scope picker, not a description of it.
4. **Where to find a channel ID** — the *About*-tab / copy-link recipe from
   *Addressing a channel* — whenever the user has to name a channel.
5. **The failure map, one line each**: `not_in_channel` → invite the app;
   `invalid_auth` → re-paste the token; `channel_not_found` → check the ID;
   `missing_scope` → add the scope, reinstall, paste the new token.

Do not compress this to "configure Slack in Settings", and do not substitute a
link to Slack's documentation. The user is mid-build, has very likely never seen
the Slack app dashboard, and the composer is where they are looking. Use the
same wording here as in the settings-page panel so the two cannot drift.

## Known limitations (experimental)

- **`{"ok": false}` is reported, as a rejected call.** Slack signals logical
  failures (bad token, missing scope, channel not found) as
  `{"ok": false, "error": "…"}` over HTTP **200**. Since 0.1.0 the client detects
  that and routes it through the error path, so the reject message names Slack's
  own `error` string — e.g. `not_authed`, `invalid_auth`, `channel_not_found` —
  instead of a decode failure. Handle it as a rejected call:
  `try { … } catch (e) { Error.message(e) }`. Do **not** write `if (res.ok) …`: a
  returned value has already decoded, so `ok` is always `true` there and the check
  is dead code. Turning these into `#ok`/`#err` return *values* would change every
  method's signature, so that waits for a major.
- **Reachability (IPv4) — no proxy needed.** `slack.com` is IPv4-only, which used
  to put it out of reach of IC HTTPS outcalls. Since **2025-08-04** the IC tries a
  direct (IPv6) connection and automatically retries through an IC-managed SOCKS
  proxy when that fails, so IPv4-only hosts work: leave `config.baseUrl` at the
  default `https://slack.com/api`. The TLS session is end-to-end between node and
  Slack, so the proxy sees only ciphertext. Expect some added latency on the
  fallback path (non-replicated outcalls are also the slower path — see above).
- **Auth is header-based, for every method.** The token rides the
  `Authorization: Bearer` header only — never in the URL, so it cannot land in a
  logged query string, and it is never a method argument.
- **Partial runtime verification.** The request shape is proven against live Slack
  (a real post lands); the success-response decode is not yet runtime-confirmed —
  `diagnostics` is on, so any decode failure surfaces the raw Slack body. The
  schema is also generated from an archived (~2020) spec revision.

## Related

- [`mops add slack-client@0.1.0`](https://mops.one/slack-client) — the generated Slack Web API bindings.
- [Slack Web API reference](https://api.slack.com/methods) — every method, its scopes, and its error strings.
- [`chat.postMessage`](https://api.slack.com/methods/chat.postMessage) — the one runtime-verified path; its `channel`/`text`/`blocks` semantics.
- [Slack token types](https://api.slack.com/concepts/token-types) — bot (`xoxb-`) vs user (`xoxp-`), and what a reinstall does to them.
- [Slack app management](https://api.slack.com/apps) — where the admin creates the app, sets scopes, and installs to the workspace.
- [extension-authorization](../extension-authorization/SKILL.md) — **required prerequisite**. Internet Identity login, `useInternetIdentity` / `useActor` plumbing, and the `#admin` role gate the token setter needs.
