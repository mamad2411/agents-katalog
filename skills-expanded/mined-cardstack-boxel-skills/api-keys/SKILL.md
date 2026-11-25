---
name: api-keys
description: 'Use when a card or the AI assistant needs a user''s API key, or a key shared into a workspace — "this card needs my GitHub token", "the forecast operation was refused binding-not-approved", "let the user add their key", "share my key with this workspace", "add a key button". Also "sign in to GitHub from this card", "connect my account", "the operation was refused credential-rejected", "the service rejected my key", "should I register a GitHub App or an OAuth App". Covers getting a key from the user only through Boxel''s secure window, with the open-secure-window tool: opening it from a card through `@context.toolContext` or from the assistant, its modes (enter a key, replace the key an operation sends, share a key, connect an account through OAuth, approve a card''s requests for scheduled pipelines or also for when the card is opened, review what changed in them), passing only the operation the card is blocked on and letting the window gather the card''s other operations into one approval, what the tool answers, the blocked-popup fallback, telling the user to check the address bar, what to do when the service rejects a key (stop polling, offer Try again, and Reconnect, which opens the window to replace the key), OAuth clients and connections (when to use a connection rather than a static key, what the card declares, opening connect mode, `credential-rejected` and its reasons, sharing a client into a workspace, and why GitHub takes a GitHub App), and never asking for a credential in the chat or building a form for one. Also covers asking first with `@context.keyReadiness` — the answers (`ready`, `needs-connect`, `needs-approval`, `needs-reapproval`, `needs-admin`, `needs-sign-in`, `rate-limited`, `over-budget`), what a card shows for each and what the secure window can fix, and treating `undefined` as "not known yet" so prerendered HTML never shows Connect. Also covers a call refused for the key owner''s limits (`rate-limited`, `over-budget`, `rate-limit-unavailable`): backing off by `retryAfterSeconds` and saying the limit is reached without naming a budget. Activates on "approve", "Allow", "review changes", `needs-approval`, `needs-reapproval`, `open-secure-window`, `OpenSecureWindowTool`, `keyReadiness`, "secure window", "API key", "enter a key", "replace a key", "share a key", "OAuth", "connect", "Reconnect", "GitHub App", `{{userKey}}`, `{{apiKey}}`, `binding-not-approved`, `interactive-use-not-approved`, `anonymous-use-not-approved`, "On a schedule and when the card is opened", "people who aren''t signed in", "anonymous cap", `credential-rejected`, `rate-limited`, `over-budget`.'
boxel:
  kind: skill
  tools:
    - codeRef:
        module: "@cardstack/boxel-host/tools/open-secure-window"
        name: default
---

# Getting a key from the user

A user's API key is typed in exactly one place: **Boxel's secure window**, a
popup whose address bar shows Boxel's secure address (`secure.boxel.ai` in
production). Never in the app page, a card, a field, a form, a file or the
chat. Card code runs in the app page and can read everything there, so a key
typed anywhere else is exposed to every card the user opens. A card can draw
a look-alike form; it can't forge another window's address bar.

So there is one way to start key entry, used by cards, the app and the AI
assistant alike: the **`open-secure-window`** host tool. It opens the window
on the right page, says what the key is for, and gives nothing back but
whether the window opened. The window signs in on its own, stores the key
sealed on the realm server, and closes when the user is done.

## The tool

`@cardstack/boxel-host/tools/open-secure-window` (default export,
`OpenSecureWindowTool`). Its input:

| Field                     | Holds                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mode`                    | `enter-key` (add a key), `replace-key` (replace the key an operation sends), `share-key` (share one of the user's keys into a workspace), `swap-key` (put one of the user's keys into a workspace's suspended share), `connect` (sign in at a service through OAuth, see [below](#oauth-connections)), `approve` (approve the card's requests, see [Approving](#approving-a-cards-requests)) or `review-changes` (approve again what changed in them). Required |
| `cardId`                  | `enter-key`, `replace-key`, `connect`, `approve`, `review-changes`: the card instance whose operation needs the key, as a URL or prefix-form id                                                                                                                                                                                                                                     |
| `module`, `name`, `realm` | The same modes, for an operation on a card **type** instead of an instance: the type's module, its export name, and the workspace it is used in                                                                                                                                                                                                                                     |
| `operation`               | The same modes: the name of the operation that needs the key. Needs `cardId`, or `module` + `name` + `realm`. Required for `replace-key`, `approve` and `review-changes`                                                                                                                                                                                                            |
| `realm`, `share`          | `share-key`: the workspace the key is shared into (`realm`). Required. `swap-key`: the workspace and its suspended share (`share`, the share's id). `connect`, on its own: offers the clients shared into that workspace                                                                                                                                                                                                                                                   |
| `reason`                  | One short line the window shows, labelled as written by whoever opened it ("Weather Station needs your forecast service key")                                                                                                                                                                                                                                                       |

Every field **names** something; none carries a value. Never pass a key, a
token, a destination URL or anything secret. The window asks the realm server
what each name refers to and shows that, so a card can't make the window say
something the server doesn't.

It answers `status`:

- **`opened`** — the window is open.
- **`blocked`** — the browser's popup blocker stopped it. The app shows the
  user a small dialog with an **Open the secure window** button, which opens
  the same window on their click, and names the address to check. Nothing else
  for the caller to do.

It never says whether the user entered or shared a key, and nothing the app
can call does: the window has no handle back to the page, and a stored key
doesn't by itself change how the card's operation answers (see the last
section). Open the window once for what it is needed for; never reopen it in a
loop.

The tool refuses on a Boxel deployment that doesn't sign users in on the
secure origin, where the window would have no session. Say so to the user
rather than retrying.

## From a card

Give the user a button; on click, run the tool with the card's own
`toolContext`. A click is a user gesture, so the popup is usually let through.

```gts
import { on } from '@ember/modifier';
import { tracked } from '@glimmer/tracking';
import { CardDef, Component, contains, field } from '@cardstack/base/card-api';
import StringField from '@cardstack/base/string';
import OpenSecureWindowTool from '@cardstack/boxel-host/tools/open-secure-window';

export class WeatherStation extends CardDef {
  static displayName = 'Weather Station';
  @field city = contains(StringField);

  static isolated = class Isolated extends Component<typeof this> {
    @tracked problem: string | undefined;

    addKey = async () => {
      let toolContext = this.args.context?.toolContext;
      if (!toolContext || !this.args.model.id) {
        return; // not in the app (prerender, a published page), or not saved
      }
      this.problem = undefined;
      try {
        await new OpenSecureWindowTool(toolContext).execute({
          mode: 'enter-key',
          cardId: this.args.model.id,
          operation: 'forecast',
          reason: 'Weather Station needs your forecast service key',
        });
      } catch (e) {
        // e.g. a Boxel deployment that offers no secure window
        this.problem = e instanceof Error ? e.message : String(e);
      }
    };

    <template>
      <button type='button' {{on 'click' this.addKey}}>
        Add your forecast service key
      </button>
      {{#if this.problem}}<p role='alert'>{{this.problem}}</p>{{/if}}
    </template>
  };
}
```

- `execute` throws when the window can't be opened for what it was given (a
  deployment with no secure window, a card that isn't saved yet); show the
  message rather than leaving the click silent.
- Name the card and the operation, not the service's URL: the window shows the
  destination from the operation's declaration on the server.
- Don't render your own "blocked" message: the app already shows the fallback
  button.
- Don't read anything back from the window. There is no value to read, and the
  window has no handle back to the page.
- Whether people who aren't signed in may use a key is a setting on the key
  itself, its owner's to make: the **People who aren't signed in** checkbox
  when adding it (`enter-key`), or later from the key's page in the secure
  window, each with two optional anonymous caps, the calls a day and the calls
  a month all visitors together may make with the key across every workspace
  it is shared into. An empty cap field means no cap, and turning anonymous
  use off clears both. Visitors are always limited by their address, and
  together spend at most half of each share's daily budget and half of its
  monthly one, so signed-in readers keep the rest. Only a static
  key, a Google service account, or an OAuth client with grant type
  `client_credentials` takes the setting; a sign-in app and a connection are
  each person's own sign-in and never serve visitors. Where visitors can use
  it is the workspace policy's to say. A
  card for visitors is in [`api-integrations`](../api-integrations/SKILL.md)
  §2: tell the key's owner to allow anonymous use on the key.
- To share a key into a workspace, pass `mode: 'share-key'` and `realm`. The
  window offers no choice about visitors; it reflects the workspace's policy.
  Where the policy opens nothing to people who aren't signed in, it is for
  signed-in people only. Where the policy opens a call that sends a shared key
  (`{{apiKey}}`) to them, sharing a key there means they **will** use it: the
  window says so in bold, and a key that doesn't allow anonymous use isn't
  shared there until its owner allows it on the key's page. `swap-key`
  follows the same rule: the window says visitors will use the key swapped
  in, and refuses a key that doesn't allow them. Before opening the
  window for such a workspace, warn the user in your reply that sharing means
  people who aren't signed in — anyone on the internet who opens its cards —
  will use the key, on the key owner's quota and bill, and that the key must
  allow it. Tell by the workspace's `realm.json` `policy` card: a grant whose
  `where` is `actor() == "anonymous"` on a `callApi` operation whose every
  credential slot is `{{apiKey}}` ([`api-integrations`](../api-integrations/SKILL.md) §2).
- The other way round, a policy saved after keys were shared, asks first.
  Writing such a grant into a workspace's policy, where shared keys are
  approved for the operation it opens, makes Boxel show the person a list of
  the keys visitors will start using and the ones that will refuse them until
  their owners allow it. Only the person confirms it. Owners of keys that
  don't allow it yet are asked, on their keys page, to approve anonymous use
  or decline. Say so in your reply. If they choose
  **Don't save**, report that the policy wasn't saved; writing it again when
  they ask asks them again
  ([`realm-policy-authoring`](../realm-policy-authoring/SKILL.md) §12).
- To replace the key an operation sends, pass `mode: 'replace-key'` with the
  same `cardId` and `operation` (see the last section).
- To have the user sign in at the service instead of pasting a key, pass
  `mode: 'connect'` with the same card and operation (see
  [OAuth connections](#oauth-connections)).

## Asking first: `keyReadiness`

A card shouldn't render a control that is only going to be refused. Before
it calls an operation that carries a credential slot, it asks
**`@context.keyReadiness(operation, target)`** whether the call would have
its key, and shows what would fix it if not. `target` is the card (or its
URL), or a card class with `{ realm }` for an operation on a type, as for
`@context.canInvoke`. It is asked on the same request as `canInvoke` and
answers the same way: synchronously, from what the app already knows, and
re-rendering when the answer lands.

| Answer                | Means                                                                                                          | The card shows                                                                                                                                                              |
| --------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ready`               | The call will have its key                                                                                     | The data; call the operation                                                                                                                                                |
| `needs-connect`       | None of the user's keys may be sent where the operation sends                                                  | A **Connect** button that opens the secure window in `approve` mode for this operation; its key choice adds a key, and `connect` mode is for a service the user signs in to |
| `needs-approval`      | The user has a key that could be sent there, but the operation isn't approved here, or not for use from a card | An **Allow** button that opens the secure window in `approve` mode for this operation                                                                                       |
| `needs-reapproval`    | What the operation sends changed since it was approved                                                         | A **Review changes** button that opens the secure window in `review-changes` mode for this operation                                                                        |
| `needs-admin`         | A key the workspace provides isn't set up for this, and the user can't set it up                               | "An administrator of this workspace needs to set this up", no button                                                                                                        |
| `needs-sign-in`       | Nobody is signed in, and the key the operation needs isn't available to signed-out visitors                    | Sign in. A card meant for visitors shows it when the share's key doesn't allow people who aren't signed in, or the slot takes the user's own key (`api-integrations` §2)                          |
| `credential-rejected` | The service rejected the key, and the realm server is holding it back until its next retry                     | That the service rejected the key, with Try again and Reconnect (`replace-key`)                                                                                             |
| `rate-limited`        | The user has made as many calls with this key as its owner's limit allows for now                              | The last data, and "Try again in a moment"; don't call until the limit refills                                                                                             |
| `over-budget`         | The key has served its owner's daily or monthly budget of calls                                                | The last data, and "This workspace's limit for this service is reached" ("your limit" for a `{{userKey}}` slot); no calls until the budget resets                          |
| `undefined`           | **Not known yet**                                                                                              | Nothing                                                                                                                                                                     |

**One button per answer the window fixes, for the one operation.** Pass the
operation the card is blocked on, never a list: the window gathers every
other operation on the card that needs the user's approval in this workspace
and approves them together ([Approving](#approving-a-cards-requests)). So a
card with six operations opens the window once, for whichever one it is
showing, and never loops over its operations. Open it once per click; the
answer the user comes back to is readiness asked again, not anything the
window says.

**Where the approval lets the key run.** The user approves an operation for
scheduled pipelines only (the default), or also for when a card is opened
(see [Approving](#approving-a-cards-requests)). Approved for pipelines only, a
call the card itself makes is refused, so readiness asked from the card keeps
answering `needs-approval`, and **Allow** opens the page where the user can
allow it from the card too. Approved for both, readiness answers `ready` and
the card calls the operation. A pipeline-shaped card renders what a pipeline
would write and offers setup as an action that is always there rather than
one gated on readiness; a live card calls the operation on `ready`. Which to
build, and why private data takes the pipeline, is in
[`api-integrations`](../api-integrations/SKILL.md) §2 and §4.

**`undefined` is never "not ready".** It is the answer while the realm is
being asked, where nothing can answer (a caller who may not invoke the
operation at all, a realm that sends no outside requests), and **always in
prerendered HTML**. Prerendered HTML is rendered once and served to every
viewer, so a Connect button in it would be shown to people who are already
connected. Branch on the named answers and render nothing for `undefined`.

An operation that carries no credential slot is `ready`. The answer names
what to show, never whose key fills a slot: a reader is never told who owns a
workspace's key, its name or its budget numbers: `over-budget` says only that
the limit is reached. See [When a call is over a limit](#when-a-call-is-over-a-limit).
A key the service rejected reads `credential-rejected` while
the realm server is holding it back; show what
[When the service rejects the key](#when-the-service-rejects-the-key) shows.

```gts
import { on } from '@ember/modifier';
import { tracked } from '@glimmer/tracking';
import { eq } from '@cardstack/boxel-ui/helpers';
import { CardDef, Component, contains, field } from '@cardstack/base/card-api';
import StringField from '@cardstack/base/string';
import OpenSecureWindowTool from '@cardstack/boxel-host/tools/open-secure-window';

export class WeatherStation extends CardDef {
  static displayName = 'Weather Station';
  @field city = contains(StringField);

  static isolated = class Isolated extends Component<typeof this> {
    @tracked problem: string | undefined;

    get readiness() {
      return this.args.context?.keyReadiness?.('forecast', this.args.model);
    }

    // The one operation the card is blocked on; the window approves every
    // other operation on the card with it.
    openWindow = async (mode: 'approve' | 'review-changes') => {
      let toolContext = this.args.context?.toolContext;
      if (!toolContext || !this.args.model.id) {
        return;
      }
      this.problem = undefined;
      try {
        await new OpenSecureWindowTool(toolContext).execute({
          mode,
          cardId: this.args.model.id,
          operation: 'forecast',
          reason: 'Weather Station reads the forecast for your city',
        });
      } catch (e) {
        this.problem = e instanceof Error ? e.message : String(e);
      }
    };
    allow = () => this.openWindow('approve');
    review = () => this.openWindow('review-changes');

    <template>
      {{#if (eq this.readiness 'ready')}}
        {{! nothing in the way: call it from an action and render the answer }}
      {{else if (eq this.readiness 'needs-connect')}}
        <button type='button' {{on 'click' this.allow}}>
          Connect your forecast service
        </button>
      {{else if (eq this.readiness 'needs-approval')}}
        <button type='button' {{on 'click' this.allow}}>Allow</button>
      {{else if (eq this.readiness 'needs-reapproval')}}
        <p>The forecast changed what it sends.</p>
        <button type='button' {{on 'click' this.review}}>Review changes</button>
      {{else if (eq this.readiness 'needs-admin')}}
        <p>An administrator of this workspace needs to set this up.</p>
      {{/if}}
      {{#if this.problem}}<p role='alert'>{{this.problem}}</p>{{/if}}
    </template>
  };
}
```

- **The card learns what changed only through readiness.** When the user
  comes back to the app from the secure window, every readiness answer on the
  page is asked again, and the template re-renders with the new one. Don't
  poll it, and don't read anything from the tool's result beyond `opened` /
  `blocked`.
- **Advisory, like `canInvoke`.** The call checks its approval again, so a
  `ready` card still handles a refusal from the call itself.
- Guard on `keyReadiness` being there (`?.`): it is absent where nothing can
  answer.

## Approving a card's requests

`approve` opens the window for one operation; the window shows **every
`callApi` operation on that card definition, in that workspace, that needs the
user's approval**, one confirmation for all of them. It leaves out what is
already approved and unchanged, and never mixes in another card's operations
or another workspace's, even another card calling the same service.

- **Grouped by where they send**: the service's domain in large type once per
  group, its full host and path beneath, then one line per operation, led by
  its `label` (or its name split into words), with its method, path and where
  the key goes, expanding to the full request. Write each `label` as what the
  user is agreeing to ("List your open pull requests"); it is shown beside the
  request, never instead of it.
- **One key choice per slot** covers the whole batch. Keys already allowed to
  go where the batch sends come first, and one that fits is chosen already;
  "Add a new key" is beside them, so `needs-connect` needs no separate
  `enter-key` first.
- **A key's first send to a host** — a key with no grant where a group sends —
  is said in that group, by the full host: "Work GitHub token hasn't been sent
  to uploads.github.com before." The Approve button is the one confirmation,
  and beside it a line sums up each host a key goes to for the first time.
- The user can untick an operation to leave it unapproved.
- **Approval is once, not per call.** The window calls the card's requests
  "calls". An approval covers every card of that type in the workspace (one
  card, for an operation approved `perInstance`), and from then on the
  platform makes those calls without asking, until the card changes a call,
  which brings `needs-reapproval`. The key's limits bound the calls day to
  day.
- **When calls run**: **On a schedule only**, the default, or **On a
  schedule and when the card is opened**, which lets a card, the AI
  assistant or the CLI invoke the operations too. Choosing the second shows
  one warning for the whole batch. For the user's own key (`{{userKey}}`):
  "Any card you open can make these calls as you and read what comes back."
  For a workspace's share (`{{apiKey}}`): "Any card a reader of this realm
  opens, from any realm, can make these calls with this key and read the
  responses. Allow this only for a key whose responses aren't private, and
  that the service limits to reading." A share's first approval for
  interactive use also asks for the share's daily budget. There is no choice
  here for people who aren't signed in: the workspace's policy and the key's
  own setting decide (above). Where the policy opens a ticked operation to
  visitors and the chosen share's key allows them, its group says "Anyone can
  use it for requests to <domain> (<host and path>), including people who
  aren't signed in.", and the confirmation says anyone on the internet who
  opens the card can make these calls; where the key doesn't allow them, it
  notes that people who aren't signed in are asked to sign in. Card
  code is not sandboxed per realm origin, which is why the window warns:
  [`api-integrations`](../api-integrations/SKILL.md) §2 has the whole of it.
- **`review-changes`** is the same flow with only the operations whose request
  changed since they were approved, each showing what changed, field by field.
  Changing an operation's `label` or `output` changes nothing that needs
  approving again; changing its URL, headers, body, or where the key goes does.
- The user can also approve a key for a card ahead of time, from the key's
  page in the window (**Use with a card…**), or from a terminal with
  `boxel keys approve` (see
  [`api-integrations`](../api-integrations/SKILL.md) §8), which confirms a
  key's first send to a host in this window too.

## In the AI assistant

The tool is declared in this skill and in the index, so it is callable from
the first step.

- **When you learn the user's key is needed, call it once.** The signal is an
  operation refused "Binding not approved" whose message names a credential
  slot "for the invoking user's own key", or a card that says it needs the
  user's key. A slot "for the realm's key" is filled by a key the workspace
  holds, so it is never a reason to open the window. Use
  `approve` with the card and the one operation (the window gathers the rest),
  `review-changes` for an operation refused "Binding needs re-approval",
  `connect` when the card says the user signs in at the service, or
  `share-key` with the workspace.
  Call it once per card in a conversation: the window gathers the card's other
  operations, so a refusal of another of them, or the same refusal coming back
  after the user approved, is not a reason to open it again.
- **"Interactive use not approved"** means the operation is approved for
  scheduled pipelines only, so a call from the assistant is refused and
  nothing is sent. If the window hasn't been opened for this card in the
  conversation, call the tool once with `approve` and the card and that
  operation, and say in the same reply what you opened and why. If it's the
  user's own key, they can allow it there under **On a schedule and when the card is opened**, after which the assistant can run it. For a key shared into the
  workspace, whoever shared it allows it, and the window tells the user
  there's nothing for them to approve. If the window was already opened for
  the card, don't open it again: say the operation stays refused from the
  chat unless it is allowed under **On a schedule and when the card is opened**.
- **In the same reply, say what you opened and why**: which card needs which
  key, that the user enters it in Boxel's secure window, and that the window's
  address bar should show Boxel's secure address. If the tool answered
  `blocked`, tell them to use the **Open the secure window** button.
- **Never ask for a credential in the chat.** No "paste your API key here", no
  "send me your token". If the user pastes one anyway, don't use or repeat it;
  tell them to enter it in the secure window instead, and to replace the key
  with the service, since it has been exposed.
- **Never build something that collects a key**: no field, form, card or file
  for one, and no suggestion to make one.

## What a stored key does

Entering a key stores it for the user; sharing one puts a reference to it into
a workspace. Neither fills an operation's credential slot (`{{userKey}}`,
`{{apiKey}}`): an approval of the operation in that workspace does, given in
the window's `approve` mode. So:

- A pipeline the realm server runs sends the key once the key's owner has
  approved the operation there.
- A card, the assistant or the CLI invoking the same operation sends it only
  when the approval allows interactive use (**On a schedule and when the card is opened**).
  Approved for pipelines only, the call is refused
  `interactive-use-not-approved`; before any approval, `binding-not-approved`.
  Either way nothing is sent, and `@context.keyReadiness` reads
  `needs-approval` for it.

Once the user has approved for pipelines only, tell them it is set up for
scheduled runs, rather than retrying from the card. See
[`card-operations-authoring`](../card-operations-authoring/SKILL.md) §2 for
slotted operations and [`api-integrations`](../api-integrations/SKILL.md) for
the card-plus-pipeline shape.

From a terminal, `boxel keys` adds and shares keys, and connects accounts
through OAuth, too (same section, and [OAuth connections](#oauth-connections)).

## When a call is over a limit

A key's owner sets how much of it anyone may spend: a number of calls each
person may make at once, refilled over time, and a daily and a monthly budget
of calls for the key across everyone. A key nobody set limits on gets
Boxel's defaults (25 calls at once, then 15 a minute; 2,400 calls a day). Only
calls from a card, the AI assistant or the CLI count; a scheduled pipeline's
don't. A share's first approval for interactive use asks its owner for the
share's daily budget, since every reader of the workspace can then spend it. A share whose key allows people who aren't signed in limits each visitor by their address, keeps visitors together to at most half of its daily budget and half of its monthly one so signed-in readers keep the rest, and the key's daily and monthly anonymous caps, when set, bound what visitors together spend a day and a month across every workspace the key is shared into. A call over a limit is refused before anything is sent:

| `code`                   | Status | Means                                                     | What to do                                                                                   |
| ------------------------ | ------ | --------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `rate-limited`           | 429    | This user's calls with the key are over its limit for now | Wait `retryAfterSeconds`, then call again; never retry sooner                                |
| `over-budget`            | 429    | The key's budget for the day or month is used up          | Stop calling and say the limit is reached; resume after `retryAfterSeconds`                  |
| `rate-limit-unavailable` | 503    | Boxel couldn't count the call, so it didn't send it       | Wait `retryAfterSeconds` and call again once                                                 |

Budgets reset at midnight UTC, and the monthly one on the 1st of the month,
UTC, so `retryAfterSeconds` on `over-budget` can be hours or days. The wait is
the error's `retryAfterSeconds`:

```gts
import { OperationsError } from '@cardstack/base/operations';

try {
  this.result = await this.load();
  this.limitReached = false;
} catch (err) {
  if (err instanceof OperationsError) {
    let wait = err.retryAfterSeconds ?? 60;
    if (err.code === 'rate-limited' || err.code === 'rate-limit-unavailable') {
      this.nextPollAt = Date.now() + wait * 1000; // back off, keep the last data
      return;
    }
    if (err.code === 'over-budget') {
      // Say the limit is reached, and poll again only once the budget resets;
      // the next successful load clears the message.
      this.limitReached = true;
      this.nextPollAt = Date.now() + wait * 1000;
      return;
    }
  }
  throw err;
}
```

A refusal through a workspace's key (an `{{apiKey}}` slot) never says whose
key it is or what its budget is; don't guess one in the message. Only the key's owner changes its limits, and should check
their vendor plan's own limit when they raise them.

## When the service rejects the key

An operation refused **`credential-rejected`** (424, "Credential rejected")
sends a key the service rejected: it answered 401 at the address the key is
sent to. The call that got the 401 did reach the service. From then on the
realm server holds that key back from that address, and refuses calls with
it there without sending them, except for **one call every 15 minutes or
so**, which it lets through as a retry. A retry the service accepts brings the
key back, and so does its owner replacing the key. The owner is told once,
and for a key shared into a workspace, so are the workspace's writers. The
refusal's message names the credential slot and the address. While a call
would be held back, `@context.keyReadiness` reads `credential-rejected` for it,
and `ready` again once the retry is due. This is a stored key's refusal; a
connection's has its own reasons, under [OAuth connections](#oauth-connections).

- **A card stops polling on its own** and says the service rejected the key,
  with a **Try again** button. A timer that keeps calling only collects the
  same refusal. A call the user starts after the interval (a click, or
  opening the card again) is the retry, so a key the service accepts again is
  picked up the next time the card is used. Read the refusal's `code`:

  ```gts
  import { OperationsError } from '@cardstack/base/operations';

  // in the component, around the operation call
  try {
    this.result = await this.load();
    this.rejected = false;
  } catch (err) {
    if (err instanceof OperationsError && err.code === 'credential-rejected') {
      this.rejected = true; // stop the polling loop; show the message
      return;
    }
    throw err;
  }
  ```

  ```gts
  {{#if this.rejected}}
    <p>The forecast service rejected your key.</p>
    <button type='button' {{on 'click' this.tryAgain}}>Try again</button>
  {{/if}}
  ```

- **The key is replaced in Boxel's secure window, from a Reconnect button.**
  Replacing the key clears the rejection at once, without waiting for a
  retry the service accepts, so show **Reconnect** beside Try again, and have
  it open the window with `mode: 'replace-key'`, naming the card and the
  operation as `enter-key` does. The card never names a key: the
  window finds the key from the user's approval of that operation and offers
  to replace it. When the slot is filled by a key someone else shared into the
  workspace, there is nothing for this user to replace, so the window says
  only the person who shared it can. It names that person to the workspace's
  direct writers, and tells anyone else to ask one of them. When no key is
  approved for the operation, it says there is nothing to replace. Don't open
  `enter-key` for this refusal: it adds a **new** key and leaves the rejected
  one in place. From a terminal, `boxel keys replace <name>` replaces it too.

  ```gts
  reconnect = async () => {
    let toolContext = this.args.context?.toolContext;
    if (!toolContext || !this.args.model.id) {
      return;
    }
    this.problem = undefined;
    try {
      await new OpenSecureWindowTool(toolContext).execute({
        mode: 'replace-key',
        cardId: this.args.model.id,
        operation: 'forecast',
        reason: 'The forecast service rejected your key',
      });
    } catch (e) {
      // e.g. a Boxel deployment that offers no secure window
      this.problem = e instanceof Error ? e.message : String(e);
    }
  };
  ```

  ```gts
  {{#if this.rejected}}
    <p>The forecast service rejected your key.</p>
    <button type='button' {{on 'click' this.reconnect}}>Reconnect</button>
    <button type='button' {{on 'click' this.tryAgain}}>Try again</button>
    {{#if this.problem}}<p role='alert'>{{this.problem}}</p>{{/if}}
  {{/if}}
  ```

  As for `enter-key`, the tool says only whether the window opened. The card
  learns the key works again the next time a call succeeds, so Try again after
  the window closes is the way to check.

- **In the AI assistant**, on an operation refused "Credential rejected", call
  `open-secure-window` once with `mode: 'replace-key'`, the card and the
  operation. In the same reply, tell the user which service rejected the key
  (the message names it) and that they replace it in the window that opens.
  Never ask for the key in the chat.
- A **403** from the service is not this refusal. It arrives as the
  operation's answer (`status: 403`), because a service also uses 403 for a
  missing permission on one resource or for a rate limit. Read the body.

## OAuth connections

Many services sign a person in through OAuth instead of handing out a key. Two
kinds of key carry it, and both live in the secure window like any other:

- An **OAuth client** is an app registered with the service: its client id and
  secret, its sign-in and token addresses, the permissions (scopes) it asks
  for and the API hosts it serves. Whoever registered it adds it in the secure
  window (`enter-key`, kind **Sign-in app (OAuth)**). Most clients are for people to sign
  in through; a `client_credentials` client gets tokens for itself, with no
  person signing in.
- An **OAuth connection** is one person's sign-in through a client. It is a
  personal key: it fills a `{{userKey}}` slot as a pasted key does, and its
  owner approves the operations that use it as for any key of theirs. The
  realm server mints a short-lived access token from it, reuses it until it
  is due, and refreshes it; no token reaches the app page, the card or the
  chat.

**A connection or a static key.** Prefer a connection when the service offers
OAuth: the user approves the permissions the client asks for on the service's
own page, can revoke
the sign-in there, and never handles a long-lived token. Use a static key when
the service only issues API keys. The card can't tell which fills its slot and
doesn't need to, unless only one of them works for the service: then declare
it with `keyKind` (`'oauth'` or `'static'`), and only a key of that kind can
be approved for the slot; see
[`card-operations-authoring`](../card-operations-authoring/SKILL.md).

**What a slot looks like** for a connection is no different from a pasted
key: a `{{userKey}}` slot where the service expects its token. Whether to
write a slotted operation at all is governed by
[`card-operations-authoring`](../card-operations-authoring/SKILL.md) §2 and
[What a stored key does](#what-a-stored-key-does): a slotted operation is
sent from a scheduled pipeline the realm server runs, and from a card, the
assistant or the CLI only when it is approved for interactive use. A
connection changes what fills the slot, not those rules. The slot reads:

```ts
@operation static profile = {
  base: 'callApi',
  label: 'Read your GitHub profile',
  url: 'https://api.github.com/user',
  headers: {
    accept: 'application/vnd.github+json',
    authorization: 'Bearer {{userKey}}',
  },
  output: bxl`{status: .status, login: .body.login}`,
} satisfies OperationDeclaration;
```

The declaration names no client, client id, scope or token address: the
window picks the client from the operation's destination.

**Opening connect mode.** Use the button from [From a card](#from-a-card) with
`mode: 'connect'` and the same card and operation, and a `reason` such as
"Pull Request Inbox signs in to GitHub to read your pull requests". Open it
when the operation is refused for the user's own key (as above) and the card
signs in rather than taking a pasted key. Connect mode always makes a **new**
connection; signing an existing one in again is its **Reconnect** button on
the user's key page in the secure window, which keeps its approvals. The window lists the clients that serve the operation's
destination — those shared into the workspace, or Boxel's own when the
workspace shares none for that service, then the user's own — each with the
permissions it asks for. When the list leads with the workspace's one client
for the service, or Boxel's one, or offers only one client, that client starts
out chosen; otherwise the user picks one. The user signs in with the chosen
client on the service's page; the service sends them back to the realm server, never
to the app. With no client to offer, the window says who can set one up.

**When a connection stops working**, a call through it is refused
**`credential-rejected`** (424) and nothing is sent. The
`OperationsError`'s `meta.reason` says why: `rejected` (the service no longer accepts the sign-in;
its owner reconnects from their key page), `needs-admin` (the client itself
was refused or is gone: its secret was rejected, or its share in the
workspace was removed or suspended; the client's owner or a workspace writer
fixes it) or `unavailable` (the service's token endpoint kept failing; a
later call may succeed). A stored key the service answered 401 to has no
`meta.reason`; `err.meta` is always there, so reading it is safe either way:

```gts
if (err instanceof OperationsError && err.code === 'credential-rejected') {
  this.rejected = true; // stop polling
  this.tryLater = err.meta.reason === 'unavailable';
  this.canReconnect = err.meta.reason === 'rejected'; // the connection's owner signs in again
  this.problem = err.detail ?? err.message; // names who fixes it
}
```

A call from a card or the assistant to an operation
approved for pipelines only never sees this refusal: it is refused
`interactive-use-not-approved` before any token is minted (see
[What a stored key does](#what-a-stored-key-does)).

**Sharing a client into a workspace.** A workspace writer registers one app
with the service, adds it in the secure window, and shares it into the
workspace with `share-key`, like any key. Connect mode then offers it to
everyone who can read the workspace, and each teammate signs in with their own
account. The client secret is stored once and nobody else sees it; replacing it
reaches every connection made through the client. Where the workspace shares
a client for a service, connect mode offers it in place of Boxel's own client
for that service; Boxel's clients for other services are still offered.

**Registering the app with the service** needs two things from its settings
there: the **callback (redirect) URL**, which is the realm server's
`/_oauth/callback` (for example `https://app.boxel.ai/_oauth/callback`),
since a service refuses a sign-in that returns anywhere it wasn't told; and,
for a GitHub App, an **installation** on the account or organization whose
repositories it reads, since a connection reaches only repositories the app is
installed on.

**From a terminal**, `boxel keys` adds a client, shares it into a workspace
and connects an account through it; registering the app with the service, as
above, comes first. The client secret is typed at a masked prompt in the
user's own terminal (or read from a file they name with `--key-file`), never
given as an argument or passed through the chat, and no command prints a
token. Who runs which command, and the browser sign-in these need, are in
[`card-operations-authoring`](../card-operations-authoring/SKILL.md) §2:

```bash
# Add the app you registered with the service, then share it in
boxel keys add forge-app --kind oauth-client --client-id <id> \
  --authorize-url https://forge.example/oauth/authorize \
  --token-url https://forge.example/oauth/token \
  --scopes read:user --api-host https://api.forge.example/
boxel keys share forge-app --realm <workspace-url> --as "Forge"

# What you can connect through: Boxel's own, yours, and the workspace's
boxel keys clients --realm <workspace-url>

# Sign in at the service in the browser; the result is your connection
boxel keys connect my-forge --client Forge --realm <workspace-url>
boxel keys connect my-github --client platform:github
```

`--api-host` names the API addresses the client serves, so the secure window
offers it for operations sent there. `connect` names a shared client by its
label with `--realm`, one of your own by its key name, and one of Boxel's as
`platform:<name>`. It opens the service's sign-in page and waits. The service
sends the browser back through the realm server's `/_oauth/callback` to a
page of Boxel's secure window, which asks the user to **Continue in the
terminal** and hands the sign-in back to the CLI; the CLI finishes it with
its own sign-in, so the browser needn't be signed in to Boxel. The command
ends once the connection is saved. Like a connection made in the secure
window, it doesn't by itself let an operation send it (see
[What a stored key does](#what-a-stored-key-does)).

**For GitHub, a card that only reads uses Boxel's app.** Boxel registers its
own GitHub App, **Boxel (read-only)**, which reads pull requests, code
(contents), checks, issues and repository metadata and can write nothing.
Where Boxel's deployment has it set up, connect mode offers it for
`https://api.github.com/` wherever no GitHub client is shared into the
workspace, so a card that only reads from GitHub needs no client of the
workspace's and no registration of its own. Its operations target
`api.github.com` with a `{{userKey}}` slot, and run as any slotted operation
does (see [What a stored key does](#what-a-stored-key-does)); the card's
Connect button opens connect mode. Each person signs in with their own GitHub
account and reads only what that account can.

**Each account installs Boxel's app once.** A GitHub App's sign-in reaches
private repositories only on accounts where the app is installed: the
person's own account as much as an organization. Without the install, those
private repositories answer as if they don't exist (an empty list, or 404).
The install is at `https://github.com/apps/boxel-read-only/installations/new`:

- **For their own repositories**, the person installs it on their personal
  account.
- **For an organization's**, a member picks the organization. Someone who
  can't install it there gets **Request**, which goes to the organization's
  owners (unless the organization has turned requests off), and an owner
  approves it once. That install covers every Boxel use of the app in the
  organization.

A card that lists repositories or pull requests and finds none should say so
and link there, rather than show an empty list as if there were nothing.

**Register your own GitHub App when the card writes** (comments, labels,
merges, issues), or reads something Boxel's app doesn't (organization
members, Actions), and share it into the workspace. A client shared into the
workspace takes Boxel's app's place in connect mode there. Make it a GitHub
App, not an OAuth App: an OAuth App's only scope that reaches private
repositories, `repo`, can also write to them, so every connection through it
could, while a GitHub App asks for exactly the permissions it needs.

Token endpoints are the realm server's alone: no `callApi` can send a
credential to one, so a card never refreshes or exchanges a token itself.
