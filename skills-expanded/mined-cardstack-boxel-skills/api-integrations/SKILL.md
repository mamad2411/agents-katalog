---
name: api-integrations
description: 'Use when a card needs data from, or sends data to, a third-party API — "show my GitHub pull requests in a card", "pull my open issues", "a card that calls the weather API with my key", "integrate with Stripe/Twilio/OpenAI", "how often can this card poll", "build a PR inbox". Takes a card author from "I want data from this vendor" to a working card: classifying the integration (no key, a key the workspace shares, the user''s own key, a key that can write), choosing a live card or a scheduled pipeline (and why private data takes the pipeline), declaring the `callApi` operations with labels and credential slots, estimating polling cost, and recipes for GitHub (GraphQL, a GitHub App or a read-only fine-grained token, the PR inbox as a pipeline and as a live card), for a plain API key sent in a header, and for images from an AI vendor called with the user''s own key (an automation run''s own AI requests carry text only). Activates on "third-party API", "vendor API", "integration", "pipeline", "live card", "On a schedule and when the card is opened", "poll", "GitHub API", "GraphQL", `callApi`, `{{userKey}}`, `{{apiKey}}`, "image generation", "AI vendor key", "automation image".'
boxel:
  kind: skill
---

# Integrating a third-party API

A card never holds or sends a key itself. It declares each request as a
**`callApi` operation**: data the realm server builds and sends, with any key
filled in by the realm server from an approval the key's owner gave in Boxel's
secure window. This skill decides the shape of an integration; the operation
grammar is in [`card-operations-authoring`](../card-operations-authoring/SKILL.md)
§2, and getting the key from the user is in [`api-keys`](../api-keys/SKILL.md).

## 1. Classify the integration

Ask what the vendor needs before writing anything.

| The API takes                                   | Declare                                                                 | Who sets it up                                                                                     |
| ----------------------------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **No key** (a public endpoint)                  | A `callApi` with no slot. Works from a card at once                     | Nobody                                                                                             |
| **A key the workspace shares** (one account for everyone, a team's API key) | A `{{apiKey}}` slot (`{{apiKey:name}}` when one request needs two)       | A direct writer of the workspace shares one of their keys into it and approves the card's requests |
| **The user's own key** (each person's data)     | A `{{userKey}}` slot                                                    | Each user approves the card's requests with their own key                                          |
| **A key that can write** (post, delete, pay)    | As above, but say so in the `label` and keep these operations few       | As above; ask the user to give the key the fewest permissions the card needs                       |

Prefer a key the vendor lets the user scope down (read-only, one
repository, one project). The window shows every request exactly as it will
be sent, but the vendor decides what a key can do.

## 2. Live card or pipeline

A request carrying a slot is sent in one of two shapes. The key's owner
picks which when they approve it in the secure window, under **When calls run**:

- **Pipeline.** A pipeline the realm server runs calls the vendor on a
  schedule, as whoever approved it, and writes what cards need into the
  realm: one card per pull request, say. Readers open those cards and never
  call the vendor, so the card shows the same data in the app, in a search
  result and in prerendered HTML, and its own code never reaches the key.
  **On a schedule only** is the default.
- **Live card.** The card invokes the operation itself while it is open and
  renders the answer. That takes an approval with **On a schedule and when the card is opened**. An operation approved for pipelines only refuses a call from a
  card, the AI assistant or the CLI with `interactive-use-not-approved`, and
  nothing is sent.

An operation with no slot needs no approval, so it is always a live card.
Invoke any `callApi` from an action (a click, opening a panel), never during a
render: that is refused `not-during-render`.

**Prefer the pipeline for private data.** Card code runs in the app page with
the viewer's session, so a call carries that session whichever card makes it.
Once an operation is approved for interactive use, any card the user opens,
from any realm, can invoke it and read the response:

- For a `{{userKey}}` slot, that card calls as the user, with their key, and
  reads whatever the key can read.
- For an `{{apiKey}}` share, any reader of the realm can do it, through any
  card they open, with the share's key.

Card code is not sandboxed per realm origin, which is what would close this.
So approve interactive use only for responses that aren't private, with a key
scoped read-only at the vendor. Private data comes through a pipeline: readers
get only what it wrote into the realm, behind the realm's own read
permissions. The secure window says this in the one confirmation it asks for
when the user picks **On a schedule and when the card is opened**.

**Interactive calls count against the key's limits** (§5): a rate limit per
caller, and a daily and a monthly budget of calls for the key. A share's first
approval for interactive use asks its owner for the share's daily budget.

**Public cards: visitors who aren't signed in.** A published card can call a
service for anyone who opens it, such as a weather widget, but only with a key
shared into the workspace, never a `{{userKey}}`: a visitor has no key of
their own. The card's part is an operation that sends only shared keys
(`{{apiKey}}`), invoked on a card, not on its type. Three more things are
other people's to set, and a visitor is served only when all three hold:

- the workspace's policy opens the operation to visitors, with a grant whose
  `where` names `"anonymous"`
  ([`realm-policy-authoring`](../realm-policy-authoring/SKILL.md) §12);
- the key's owner allows people who aren't signed in to use the key: a
  setting on the key itself, made when adding it (the **People who aren't
  signed in** checkbox in the window's add-key page, or `boxel keys add …
  --anonymous`) or later from the key's page in the secure window or
  `boxel keys anonymous <name> on` ([`api-keys`](../api-keys/SKILL.md), §8);
- the operation is approved for **On a schedule and when the card is
  opened**, and the share's limits have room.

So the key's owner decides whether visitors may use the key, and the
workspace's policy decides where. Tell the key's owner to allow anonymous use
on the key, when adding it or from the key's page, and the workspace's policy
author to open the operation to visitors.

Sharing the key and approving the card's calls make no choice about visitors;
they only reflect those two. Sharing a key into a workspace whose policy opens
a call that sends a shared key to visitors means visitors **will** use it, so
the window's **Share a key** page says so in bold, and `boxel keys share`
prints the same warning. A key that doesn't allow anonymous use isn't shared
there at all: the page links to the key's page to allow it first, and the CLI
says to run `boxel keys anonymous <name> on`. Where the policy opens nothing to
visitors, sharing is for signed-in people only. Swapping a key into a share
follows the same rule: in such a workspace the **Swap** page says visitors
will use this key, `boxel keys swap` warns, and a key that doesn't allow
anonymous use is refused (400).

Only a key that can serve visitors takes the setting: a static key, a Google
service account, or an OAuth client whose grant type is `client_credentials`.
A sign-in app (an `authorization_code` client) and a connection are each
person's own sign-in and never serve visitors, so they can't be set to allow
anonymous use, and sharing or swapping one has no anonymous check.

When you, the AI assistant, are about to open the window's `share-key` mode
for a workspace, read the workspace's policy first (its `realm.json`
`policy` card; see
[`realm-policy-authoring`](../realm-policy-authoring/SKILL.md) §12). If a
grant there has a `where` of `actor() == "anonymous"` on a `callApi`
operation whose every credential slot is `{{apiKey}}`, warn
the user in the same reply, before the window opens: sharing a key into this
workspace means people who aren't signed in will use it — anyone on the
internet who opens its cards — with their calls counted against the key
owner's quota and bill; and the key must allow anonymous use on its own page,
or the window won't share it there. If you can't read the policy, say the
window will tell them whether that applies.

The approve window has no choice for visitors either: where the policy
opens a ticked operation to visitors and the chosen share's key allows them,
that operation's group says "Anyone can use it for requests to <domain>
(<host and path>), including people who aren't signed in.", and where the key
doesn't, it notes that people who aren't signed in are asked to sign in.
`boxel keys approve --interactive` prints the equivalent lines (§8).

Visitors together spend at most half of each share's daily budget and half
of its monthly one (the platform's setting), so signed-in readers always keep the rest, whatever caps
the key's owner set, or none. The key's owner can also set its **anonymous
caps**, each optional: the most calls a UTC day, and the most calls a UTC
month, all visitors together make with it, each counted once across every
workspace it is shared into. Visitors' calls spend the share's
daily and monthly budgets like anyone's.
Either way, each visitor is limited by their address, at the share's
per-person rate; nobody sets that. Allow anonymous use only for responses
anyone may see, from a key scoped read-only at the service: anyone on the
internet can make these calls.

The order of the steps doesn't matter. A key already shared into a workspace
whose policy later opens calls to visitors serves them if the key allows
anonymous use, and otherwise they are asked to sign in.

What a visitor gets meanwhile depends on what is missing:

| What is missing                                                   | The call is refused            | `keyReadiness`                             |
| ----------------------------------------------------------------- | ------------------------------ | ------------------------------------------ |
| The policy doesn't open the operation to visitors                 | `operation-not-permitted`      | no answer; `canInvoke` is `false`          |
| The share isn't approved yet, or only for scheduled pipelines     | `binding-not-approved` / `interactive-use-not-approved` | `needs-admin`, as for any reader |
| The share's key doesn't allow people who aren't signed in         | `anonymous-use-not-approved` (401) | `needs-sign-in`                        |
| The operation sends the caller's own key (`{{userKey}}`)          | `actor-required`               | `needs-sign-in`                            |
| Room under the visitor's address rate, their part of the share's daily or monthly budget, or the key's daily or monthly anonymous cap | `rate-limited` / `over-budget` | `rate-limited` / `over-budget`             |

Show `needs-sign-in` as a sign-in prompt, not an error (§4), and
`rate-limited` / `over-budget` as anyone over a limit is shown them (§5).

**Nothing a card author writes schedules a pipeline.** No card, field,
`realm.json` setting or operation declares one, and no operation turns a
`callApi`'s answer into cards on its own. So a pipeline-shaped integration is
its declarations and its card: the user can approve the requests in the
secure window, and the card renders fields that only a pipeline the platform
runs would fill. Say so to the user rather than promising data. Shape the card
this way even though nothing in the realm runs the pipeline, and don't make a
card over private data live to get the data sooner.

## 3. Declare the `callApi` operations

```ts
import {
  bxl,
  instance,
  operation,
  type OperationDeclaration,
} from '@cardstack/base/operations';

@operation static listPRs = {
  base: 'callApi',
  label: 'List your open pull requests',
  url: 'https://api.github.com/graphql',
  headers: { authorization: 'Bearer {{userKey}}' },
  graphql: {
    document:
      'query($login: String!) { user(login: $login) { pullRequests(states: OPEN, first: 50) { nodes { title url updatedAt } } } }',
    variables: { login: instance('login') },
  },
  output: bxl`{status: .status, pullRequests: .body.data.user.pullRequests.nodes}`,
} satisfies OperationDeclaration;
```

- **A `label` on every operation**, written as what the user agrees to or is
  about to do: "List your open pull requests", not "listPRs". It is shown
  beside the request in the approval, never instead of it, and changing it
  asks nobody to approve again.
- **Unnamed slots** (`{{userKey}}`, `{{apiKey}}`) unless one request carries two
  credentials; then name them (`{{apiKey:token}}`, `{{apiKey:secret}}`).
- **`perInstance: true`** when each card needs its own key (one webhook URL per
  channel card); each card is approved on its own. Its approval is reached by
  opening the window with the card (`cardId`), never the type, and
  `keyReadiness` asked about it on the type answers `undefined`.
- **Say what kind of key the slot takes** with `keyKind` when only one works:
  `'static'` for a key or token the user pastes, `'google-service-account'`
  for a Google service account's key file, `'oauth'` for an account the user
  connects through a sign-in app. Give one kind for every slot, or one per
  slot by its name (`keyKind: { token: 'oauth' }`); an unnamed slot's name is
  `userKey` or `apiKey`. Only a key of that kind can be approved for the
  slot, and a key approved before the declaration is asked to be approved
  again. When the user adds a key for the card, the secure window asks for
  that kind without making them choose, or goes straight to connecting an
  account for `'oauth'`. Left out, any kind of key can be approved, and the
  window offers every kind that can work: all three, except that a `|basic`
  slot takes only a pasted key, and a Google service account only a request
  to Google's own services (`googleapis.com`, `firebaseio.com`).
- **Put the key in a header.** Never in a body field the vendor stores (a
  comment, a description), and avoid the query string, which vendors log.
- **GraphQL takes variables.** A fixed `document`, every value passed in
  `variables`; never build a query string from values.
- **One operation per request the card makes.** Never a passthrough that takes
  a URL, a path or a body from the caller: the approval shows what is sent, and
  a passthrough would show nothing.
- **Put the fixed part of the path first.** The request's destination is its
  URL up to the first `{name}` segment, or up to the path's last `/` when it
  has none; a key is granted for that destination. So
  `https://api.github.com/repos/{owner}/{repo}/issues` grants
  `api.github.com/repos/`, while `https://api.github.com/graphql` and
  `https://storage.example.com/{bucket}/…` grant the whole host, and the
  window says any request to that host can be sent with the key.

**All of a card's operations are approved together.** When a card asks for
one, the secure window shows every operation on the card that needs approving,
grouped by where it sends, with one key choice and one confirmation. Editing
one operation's request later asks the user about that one again; editing its
`label` or `output` asks nothing.

## 4. Getting the key: what the card shows

Follow [`api-keys`](../api-keys/SKILL.md) → *Asking first: `keyReadiness`*. In
short:

- Ask `@context.keyReadiness(operation, target)` for the one operation the
  card is about to need, and treat `undefined` as "not known yet": render
  nothing for it, so prerendered HTML never shows a button.
- One button per answer the window fixes: **Connect** (`needs-connect`) and
  **Allow** (`needs-approval`) open the window in `approve` mode, **Review
  changes** (`needs-reapproval`) in `review-changes` mode, each for that one
  operation. The window gathers the rest; never loop over operations. An
  operation approved for pipelines only reads `needs-approval`, and its
  **Allow** opens the page where the user can choose **On a schedule and when the card is opened**.
- `needs-admin`: "An administrator of this workspace needs to set this up".
  `needs-sign-in`: a sign-in prompt. `credential-rejected`: the service
  rejected the key, with Try again.
- Don't wait for a message from the window. Readiness is asked again when the
  user comes back to the app.

**In a live card, readiness is the gate.** It answers `ready` once a call from
the card will be served: for a `{{userKey}}` slot, once that viewer approved
the operation with **On a schedule and when the card is opened**; for an `{{apiKey}}` slot,
once the share's owner did, for every reader. Call the operation only on
`ready`.

**In a pipeline-shaped card, readiness can't tell whether the pipeline is
set up.** It answers for a call from the card, per viewer, and an approval
for pipelines only doesn't serve that call:

- A `{{userKey}}` slot reads `needs-connect` or `needs-approval` for every
  viewer, including the one who approved it for pipelines.
- An `{{apiKey}}` slot reads `needs-admin` for everyone but the share's owner,
  even once it is approved for pipelines, and reads `needs-admin` to the owner
  too until the first approval.

So don't gate the card's data on readiness. Render the fields the pipeline
writes whenever they hold something. Offer setup as a plain action that is
always there: **Set up** opens the window in `approve` mode for one
operation. When nothing needs approving, the window says so. A share's owner
can also approve its requests from their key page (**Use with a card…**).

## 5. Polling cost

Estimate calls per day before choosing a schedule:
`viewers × runs per day × operations per run`. Every call counts against the
key owner's vendor rate limit, and for a shared key against everyone's. Calls
from a live card also count against the limits the key's owner sets in Boxel:
by default 25 calls at once per viewer, refilled at 15 a minute, and 2,400
calls a day for the key across every viewer. A card refreshing 25 calls every
5 minutes fits one viewer's rate limit, but not the daily budget all day: that
is 300 calls an hour, so one tab open for 8 hours spends the 2,400, and one
left open around the clock spends 7,200. Keep the per-day estimate under the
key's daily budget, or the card stops for every viewer until it resets at
midnight UTC. Pausing while the tab is hidden is what keeps a live card within
it. A pipeline's calls don't count against these.

Check how close a key is to these, and change them, from the terminal
(§8).

- **Batch.** One GraphQL query for everything the card shows beats one REST
  call per item.
- **A pipeline polls once for everyone** who reads its cards; a live card polls
  once per viewer. Prefer the pipeline for anything a team looks at.
- In a live card, fetch only in the `isolated` view, never in `embedded` or
  `fitted` (a search result lists dozens), and pause while the tab is hidden
  (`document.visibilityState`).
- On `credential-rejected` or `over-budget`, stop polling until the user acts
  or the budget resets; on `rate-limited`, wait the refusal's
  `retryAfterSeconds` before calling again ([`api-keys`](../api-keys/SKILL.md)
  → *When a call is over a limit*). On a vendor's own rate-limit answer (a 429
  or a `retry-after` header in the response), wait before calling again.

## 6. Recipes

### GitHub

- **Authenticate with a GitHub App or a fine-grained token**, read-only, for
  the repositories the card reads. A classic token or an OAuth App's `repo`
  scope can also write to every private repository. Where Boxel offers its own
  read-only GitHub App, prefer connecting through it (`connect` mode in
  [`api-keys`](../api-keys/SKILL.md) → *OAuth connections*); otherwise the
  user pastes a fine-grained token as a key.
- **Use GraphQL** (`https://api.github.com/graphql`): one request returns
  pull requests, reviews and comments together. Its destination is the whole
  host, `api.github.com/`, so one approval of the card and one grant cover
  every GraphQL operation on it.
- The key goes in `authorization: 'Bearer {{userKey}}'`.

The PR Inbox, in the pipeline shape: a pipeline would run the operations below
for the user who approved them and write one `PullRequest` card per result;
the inbox card lists those and always offers **Set up**. Nothing in the realm
runs that pipeline, so the list stays empty until the platform does.

```ts
import { CardDef, contains, field, linksToMany } from '@cardstack/base/card-api';
import StringField from '@cardstack/base/string';
import {
  bxl,
  instance,
  operation,
  type OperationDeclaration,
} from '@cardstack/base/operations';

export class PullRequest extends CardDef {
  static displayName = 'Pull Request';
  @field title = contains(StringField);
  @field url = contains(StringField);
  @field updatedAt = contains(StringField);
}

const GITHUB = 'https://api.github.com/graphql';
const AUTH = { authorization: 'Bearer {{userKey}}' };

export class PRInbox extends CardDef {
  static displayName = 'PR Inbox';
  @field login = contains(StringField);
  // Written by the pipeline, read by everyone who opens the inbox.
  @field pullRequests = linksToMany(PullRequest);

  @operation static listPRs = {
    base: 'callApi',
    label: 'List your open pull requests',
    url: GITHUB,
    headers: AUTH,
    graphql: {
      document:
        'query($login: String!) { user(login: $login) { pullRequests(states: OPEN, first: 50) { nodes { title url updatedAt } } } }',
      variables: { login: instance('login') },
    },
    output: bxl`{status: .status, nodes: .body.data.user.pullRequests.nodes}`,
  } satisfies OperationDeclaration;

  @operation static listReviewRequests = {
    base: 'callApi',
    label: 'List pull requests waiting for your review',
    url: GITHUB,
    headers: AUTH,
    graphql: {
      document:
        'query($q: String!) { search(type: ISSUE, query: $q, first: 50) { nodes { ... on PullRequest { title url updatedAt } } } }',
      variables: { q: 'is:pr is:open review-requested:@me' },
    },
    output: bxl`{status: .status, nodes: .body.data.search.nodes}`,
  } satisfies OperationDeclaration;
}
```

The inbox's isolated view renders `pullRequests` and, beside them, the
**Set up** button from §4 for `listPRs`; the window approves
`listReviewRequests` in the same confirmation.

The same inbox as a live card, in `live-pr-inbox.gts`: the card calls
`listPRs` itself while it is open and renders the answer, with no
`PullRequest` cards in between. Each viewer approves it with their own key and
**On a schedule and when the card is opened**. It suits responses that aren't private, such
as a key scoped read-only to public repositories; for private repositories,
keep the pipeline shape (§2).

```gts
import { on } from '@ember/modifier';
import { tracked } from '@glimmer/tracking';
import { eq } from '@cardstack/boxel-ui/helpers';
import { CardDef, Component, contains, field } from '@cardstack/base/card-api';
import StringField from '@cardstack/base/string';
import {
  bxl,
  instance,
  operation,
  operations,
  OperationsError,
  type OperationDeclaration,
} from '@cardstack/base/operations';
import OpenSecureWindowTool from '@cardstack/boxel-host/tools/open-secure-window';

interface PR {
  title: string;
  url: string;
  updatedAt: string;
}

class LivePRInboxIsolated extends Component<typeof LivePRInbox> {
  @tracked pullRequests: PR[] | undefined;
  @tracked problem: string | undefined;

  // The component's model, as the card it is.
  get record(): LivePRInbox {
    return this.args.model as LivePRInbox;
  }

  get readiness() {
    return this.args.context?.keyReadiness?.('listPRs', this.record);
  }

  // Loaded once, even when the list came back empty.
  get loaded() {
    return this.pullRequests !== undefined;
  }

  load = async () => {
    this.problem = undefined;
    try {
      // An operation with an `output` answers what the mapping makes,
      // which the type doesn't know.
      let { status, nodes } = (await operations<typeof LivePRInbox>(
        this.record,
      ).listPRs()) as { status: number; nodes: PR[] | null };
      if (status !== 200) {
        this.problem = `GitHub answered ${status}`;
        return;
      }
      this.pullRequests = nodes ?? [];
    } catch (err) {
      // rate-limited, over-budget, credential-rejected: see api-keys
      this.problem =
        err instanceof OperationsError ? (err.detail ?? err.message) : String(err);
    }
  };

  openWindow = async (mode: 'approve' | 'review-changes' | 'replace-key') => {
    let toolContext = this.args.context?.toolContext;
    if (!toolContext || !this.record.id) {
      return;
    }
    try {
      await new OpenSecureWindowTool(toolContext).execute({
        mode,
        cardId: this.record.id,
        operation: 'listPRs',
        reason: 'PR Inbox lists your open pull requests when you open it',
      });
    } catch (e) {
      this.problem = e instanceof Error ? e.message : String(e);
    }
  };
  allow = () => this.openWindow('approve');
  review = () => this.openWindow('review-changes');
  replace = () => this.openWindow('replace-key');

  <template>
    {{#if (eq this.readiness 'ready')}}
      <button type='button' {{on 'click' this.load}}>
        {{if this.loaded 'Refresh' 'Show my pull requests'}}
      </button>
    {{else if (eq this.readiness 'needs-connect')}}
      <button type='button' {{on 'click' this.allow}}>Connect GitHub</button>
    {{else if (eq this.readiness 'needs-approval')}}
      <button type='button' {{on 'click' this.allow}}>Allow</button>
    {{else if (eq this.readiness 'needs-reapproval')}}
      <button type='button' {{on 'click' this.review}}>Review changes</button>
    {{else if (eq this.readiness 'credential-rejected')}}
      <p>GitHub rejected your key.</p>
      <button type='button' {{on 'click' this.replace}}>Replace key</button>
    {{else if (eq this.readiness 'rate-limited')}}
      <p>Too many refreshes. Try again in a minute.</p>
    {{else if (eq this.readiness 'over-budget')}}
      <p>This key has used today's calls. The list below is the last one.</p>
    {{else if (eq this.readiness 'needs-sign-in')}}
      <p>Sign in to see your pull requests.</p>
    {{/if}}
    {{! the last list loaded stays while readiness moves to a limit }}
    {{#each this.pullRequests as |pr|}}
      <p><a href={{pr.url}}>{{pr.title}}</a></p>
    {{/each}}
    {{#if this.problem}}<p role='alert'>{{this.problem}}</p>{{/if}}
  </template>
}

export class LivePRInbox extends CardDef {
  static displayName = 'Live PR Inbox';
  @field login = contains(StringField);

  @operation static listPRs = {
    base: 'callApi',
    label: 'List your open pull requests',
    url: 'https://api.github.com/graphql',
    headers: { authorization: 'Bearer {{userKey}}' },
    graphql: {
      document:
        'query($login: String!) { user(login: $login) { pullRequests(states: OPEN, first: 50) { nodes { title url updatedAt } } } }',
      variables: { login: instance('login') },
    },
    output: bxl`{status: .status, nodes: .body.data.user.pullRequests.nodes}`,
  } satisfies OperationDeclaration;

  static isolated = LivePRInboxIsolated;
}
```

- **`listPRs` runs from an action**, like any `callApi`, and never from the
  template while it renders. The template only reads `pullRequests`.
- **Readiness decides what shows.** A viewer who approved for pipelines only
  reads `needs-approval`, and **Allow** opens the approve page, where they
  pick **On a schedule and when the card is opened**. Readiness is asked again when they come
  back to the app, so the list's button appears without a reload.
- **Every readiness answer shows something**, and the last list loaded
  stays while readiness moves to `rate-limited` or `over-budget`. The same
  codes can also come back as refusals from a click, which `load` shows from
  the error's detail. [`api-keys`](../api-keys/SKILL.md) has the full
  readiness table.

### A plain API key in a header

For a vendor that issues one API key per account:

```ts
@operation static current = {
  base: 'callApi',
  label: 'Read the current weather for this city',
  url: 'https://api.weather.example/v1/current',
  query: { city: instance('city') },
  headers: { 'x-api-key': '{{userKey}}' },
  output: bxl`{status: .status, temperature: .body.temperature}`,
} satisfies OperationDeclaration;
```

Use `{{apiKey}}` instead when the workspace pays for one account everyone
shares, and `authorization: 'Basic {{userKey|basic}}'` for a vendor that takes
the key as HTTP Basic credentials.

### Images from an AI vendor

An automation run's own AI requests, which Boxel bills in credits, carry text
only. Boxel refuses a run's AI request that sends or asks for images, audio or
files: Boxel can't work out what such a request costs before sending the
request, so the request could spend past the automation's AI spending limit.

To generate an image, call the AI vendor directly through a `callApi`
operation with the user's own key. The vendor bills the key's owner, not
Boxel, and the call spends none of Boxel's credits:

```ts
@operation static drawCover = {
  base: 'callApi',
  label: 'Draw a cover image for this post with OpenAI',
  url: 'https://api.openai.com/v1/images/generations',
  headers: { authorization: 'Bearer {{userKey}}' },
  json: {
    model: 'gpt-image-1',
    prompt: instance('coverPrompt'),
    size: '1024x1024',
    output_format: 'jpeg',
    output_compression: 80,
  },
  output: bxl`{status: .status, image: .body.data[0].b64_json, error: .body.error.message}`,
} satisfies OperationDeclaration;
```

- **A `callApi` sends JSON and reads text.** Pick an endpoint that takes a
  JSON body and returns the media as base64 inside JSON, as image generation
  does. An endpoint that takes a multipart upload (OpenAI's transcription and
  file upload) or returns raw binary (OpenAI's speech) can't be called this
  way.
- **In an automation, the key belongs to the payer.** An automation's run acts
  as the person who turned the automation on, so `{{userKey}}` takes that
  person's key. Add the type and operation to the automation's **Outside
  services**, and have that person approve the operation in Boxel's secure
  window ([`api-keys`](../api-keys/SKILL.md)). **On a schedule only** is
  enough for an automation. Until that person approves, Boxel refuses every
  call with `binding-not-approved`.
- **Which limits apply.** The automation's **Outside calls** and **Data
  received** limits bound these calls. **AI spending** doesn't apply, since
  Boxel doesn't bill the calls. Boxel refuses any single `callApi` response
  over 10 MiB, so ask for a compressed format (`output_format: 'jpeg'`), and
  set **Data received** to cover every image a run asks for.
- **The vendor's limit is the only spending limit on these calls.** Ask for a
  key the vendor lets the key's owner cap, such as an OpenAI project key with
  **Enforce a hard limit** turned on. An OpenAI monthly budget alone only
  sends alerts.
- **Read the vendor's refusal.** `error` carries the vendor's message when the
  vendor refuses the request, for example over a spending limit or a content
  policy.

## 7. Testing locally

A local Boxel stack sends `http:` requests only to local hosts, so point the
operation's `url` at a local stub while developing, approve it in the secure
window at `https://localhost:4208/secure`, and switch the URL to the vendor's
before sharing the card. Changing the URL changes the request, so the
operation is approved again. A live card's calls are served once the
operation is approved with **On a schedule and when the card is opened**, so it can be
checked end to end against the stub. For a pipeline-shaped card, what can be
checked locally is the approval: the window's batch, the grant it creates, and
the refusal codes the card handles.

## 8. From the terminal

`boxel lint` (and `boxel file lint`) checks every `callApi` declaration the
way indexing does, so a declaration mistake shows before the module is
indexed rather than as `invalid-operation` on the first call. Each problem
is reported with the code lowering gives it (`slot-out-of-place`,
`unencoded-path-parameter`, `undeclared-param`, and the rest in
`card-operations-authoring`). It also warns on an operation without a
`label` and on a URL that isn't `https:` (a local stub's, while
developing).

The user approves and checks the operations from the CLI too. For the PR
inbox in §6, defined in `pr-inbox.gts` in the workspace (`--operation` takes
the module relative to `--realm`, or its full URL):

```bash
# Approve every operation on the card that needs it, with one of your keys.
# Every request is printed first, then one confirmation approves them.
boxel keys approve "Work GitHub token" --operation pr-inbox#PRInbox --realm <workspace-url>
# Or just one of them.
boxel keys approve "Work GitHub token" --operation pr-inbox#PRInbox.listPRs --realm <workspace-url>
# Approve the live inbox for when you open it, too.
boxel keys approve "Work GitHub token" --operation live-pr-inbox#LivePRInbox --realm <workspace-url> --interactive

boxel keys pending      # approvals that won't send as approved
boxel keys revoke "Work GitHub token" --operation pr-inbox#PRInbox.listPRs --realm <workspace-url>
boxel keys ungrant "Work GitHub token" --destination https://api.github.com/

# Invoke an operation on a card, or on a type as <module URL>#<Class>.
boxel operations invoke <card-url> <operation> --params '<its params, as JSON>'
```

- **A `{{userKey}}` slot takes one of your keys by its name; an `{{apiKey}}`
  slot takes your share in the workspace by its label**, so for an operation
  written with `{{apiKey}}` the first argument is the label the workspace
  knows the share by. `--slot` picks one slot when an operation has several.
- **One confirmation approves up to a batch's worth.** A card with very many
  operations says how many are left, and running it again approves the rest.
- **A key's first send to a host is confirmed in the secure window.** When
  approving would send a key somewhere it has never been sent, the CLI opens
  the window's approval for that batch and finishes when the window does, so
  it needs someone at the browser and can't run in a script, `--yes` or not.
  An approval that only reuses where the key already goes finishes in the
  terminal. `boxel keys swap` works the same way. Run without a terminal,
  any approval needs `--yes`. The window approves every slot of an
  operation, so `--slot` works only where the key already goes.
- **`pending`** lists the approvals that need approving again: one whose
  request changed since it was approved (even before any call has found it),
  and one whose operation can't be read now. `revoke` and `ungrant` take
  approvals away entirely, so those aren't listed: approve again to put
  them back.
- **The CLI invokes interactively**, as a card or the assistant does, so
  `boxel operations invoke` sends a keyless operation and answers with what
  the vendor answered. One that sends a key, such as `listPRs`, is sent once
  it is approved for interactive use, and refused
  `interactive-use-not-approved` while it is approved for pipelines only. A
  type is named by its module's full URL here, not one relative to a
  workspace.
- **`--interactive` on `approve`** approves interactive use as well as
  pipelines, as **On a schedule and when the card is opened** does. A share's first
  interactive approval also takes `--daily-budget <calls>`, the share's daily
  budget. When the approval needs a new grant, the secure window it opens
  starts on interactive use. Re-approving an operation that is approved for
  interactive use takes `--interactive` too: without it the CLI refuses,
  rather than returning a live card to pipelines only. For each operation
  the workspace's policy opens to visitors, it prints the lines the approve
  window shows: "Anyone on the internet who opens this card, including
  people who aren't signed in, can make … with <share>[, up to <its caps>
  all together].", where the caps read "N calls a day", "M calls a month"
  or "N calls a day and M a month", whichever the key has; or, where the
  share's key doesn't allow them, that they're asked to sign in.
- **`approve` has no option for visitors.** Whether people who aren't
  signed in can use a key is the key's own setting, and where they can is the
  workspace policy's; `approve --anonymous` is listed in its help only to say
  so, and the realm server refuses it.
- **`boxel keys add <name> … --anonymous [--anonymous-cap <calls>]
  [--anonymous-monthly-cap <calls>]`** adds a key that people who aren't
  signed in may use, wherever a workspace's policy opens an operation that
  sends it to them (§2). **`boxel keys anonymous <name> on|off [--cap <calls>]
  [--monthly-cap <calls>]`** changes that later. The caps are the calls a UTC
  day and a UTC month all visitors together may make with the key, across
  every workspace it is shared into; each is optional. `on` keeps a cap it
  isn't given, `--cap none` or `--monthly-cap none` removes that cap while
  anonymous use stays on, and `off` clears both. `add --anonymous` is refused for an OAuth client; turn
  it on afterwards with `boxel keys anonymous <name> on` for a
  `client_credentials` client. A sign-in app never takes it.
- **`boxel keys share <name> --realm <url>`** makes no choice about visitors;
  it reflects the workspace's policy, as the window does. Where the policy
  opens a call that sends a shared key to visitors, it warns that sharing
  means people who aren't signed in will use the key, and it refuses a key
  that doesn't allow them (so does the realm server, 400), pointing to
  `boxel keys anonymous <name> on`. `boxel keys swap` does the same.
- `ungrant` lists the approvals removing the grant would revoke before it
  asks.

How much of a key the calls spend (§5) is checked and changed from the
terminal too:

```bash
# Today's and this month's calls against the budgets, the last use, the top
# callers and the refusals by reason.
boxel keys usage "Work GitHub token"
boxel keys usage "<share label>" --realm <workspace-url>

# The key's owner sets its limits: per caller, at once/refilled a minute,
# and the daily and monthly budgets. `default` puts one back.
boxel keys limits "Work GitHub token" --rate 25/15 --daily 2400 --monthly default
boxel keys limits "<share label>" --realm <workspace-url> --daily 1000
```

A share's usage is for anyone who writes to the workspace; only the key's
owner changes its limits.
