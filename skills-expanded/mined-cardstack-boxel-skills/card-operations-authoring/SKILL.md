---
name: card-operations-authoring
description: 'Use when adding an operation to a card — "let users add a comment / invite a guardian / create a linked X from this card", "batch create and link", "append to a log without loading the card", "a saved search on this card type", "hide the button if they can''t". Covers declaring `@operation` as data (the base operations, `params`, the typed references, the sugar clauses and the `bxl` escape hatch, `links`, `html`, `label`), `callApi` requests with credential slots, invoking through `operations()` and `atomic()`, `nonGrantable`, what a policy does to a batch and to a search, hiding a control with `@context.canInvoke` and `_capabilities`, what lowering refuses, and the refusals a caller sees. Activates on `@operation`, `callApi`, `google-service-account`, "Google Sheets API", `{{userKey}}`, `{{apiKey}}`, `binding-not-approved`, `operations(`, `atomic(`, `appendContainsMany`, `appendLine`, `nonGrantable`, `operation-not-permitted`, `policyScopedRealms`, `canInvoke`, `_capabilities`, "card operation", "named operation".'
boxel:
  kind: skill
---

# Authoring card operations

An operation is a named action on a card — "escalate this event", "record
vitals", "request a consult" — declared by the author as **plain data** rather
than as JavaScript. The realm reads the declaration out of its definition cache
and carries it out itself, so no code from the card's module runs on the write
path.

```ts
import StringField from '@cardstack/base/string';
import {
  actor,
  operation,
  params,
  type OperationDeclaration,
} from '@cardstack/base/operations';

export class ExternalReport extends CardDef {
  @field comments = containsMany(CommentField);

  @operation static addComment = {
    base: 'transform',
    params: { body: StringField },
    append: {
      to: 'comments',
      value: { body: params('body'), postedBy: actor() },
    },
  } satisfies OperationDeclaration;
}
```

```ts
await operations(report).addComment({ body: 'Reviewed.' });
```

Keep `satisfies OperationDeclaration` in author code. It type-checks the
declaration in place and preserves the literal types (`base: 'transform'` rather
than `base: string`) that the payload and bucket types read. Without it the
declaration is invisible to those types and the payload goes unchecked.

## 1. When an operation is the right tool

| You want                                                | Reach for                                      |
| ------------------------------------------------------- | ---------------------------------------------- |
| A user edits a field in the card's own editor            | A plain field — no operation                   |
| A value derived from other fields on the same card       | `computeVia` — no operation                    |
| A named action that writes the card, invocable from a template, another card, or an agent | **An operation**        |
| Several cards changed all-or-nothing                     | **An operation** inside `atomic()`             |
| A request to an outside API that needs no key of the user's or the realm's | **A `callApi` operation** (§2) |
| A request to an outside API with the user's or the realm's key | **A `callApi` operation with a slot**, sent by a pipeline the platform runs (nothing in a card or realm schedules one), or from the card when its key's owner approves interactive use ([`api-integrations`](../api-integrations/SKILL.md)) |
| Work that needs an LLM, host services, or logic around a fetch | A command — operations run no author JavaScript |

The dividing line is that an operation is *data the realm executes*. That buys
concurrency safety an author cannot write by hand — two callers titrating the
same dose compose rather than overwrite — and costs the ability to run arbitrary
code. A request to an outside service is the one kind of network access an
operation has: the card declares it as data and the realm server sends it. A
model call, a host service, or code around a fetch is a command.

**No card code reaches a key the user or the realm holds.** A `callApi`
credential slot is filled by the realm server, from an approval its key's
owner gave in the secure window (§2), and the free-form proxy
(`SendRequestViaProxyCommand`) never fills one. Never put a key in card code.

## 2. Declaring

`@operation static <name> = { base, … }` on a `CardDef`. The `base` names the
built-in behavior the operation builds on; the name is what a caller invokes.
The two are read separately, so a `delete` declared on `transform` is a soft
delete: asking that card to delete itself archives it.

### The base operations

| Base                  | What it does                                                        | Carried by |
| --------------------- | ------------------------------------------------------------------- | ---------- |
| `read`                | Serves the card's indexed document                                   | cards, files |
| `readSource`          | Serves the bytes stored at the URL                                   | cards, files |
| `create`              | Mints a new card — type-scoped                                       | cards      |
| `update`              | Merges field values and replaces links                               | cards, files |
| `delete`              | Removes the card                                                     | cards      |
| `query`               | A saved search, run by the search engine                             | cards      |
| `transform`           | Runs a program over the card's stored document                       | cards      |
| `appendContainsMany`  | Appends into a `containsMany` by editing stored JSON, without loading the document | cards |
| `appendLine`          | Appends one newline-terminated line to a text file                   | files      |
| `explain`             | Answers what a realm's policy decides for an actor, card and operation, invoking nothing | a card that declares it (a `RealmPolicy`) |
| `validate`            | Answers what a policy card compiles to                               | a card that declares it (a `RealmPolicy`, a `RealmConfig`) |
| `callApi`             | Sends a declared request to an outside service and answers with its response | a card that declares it |

A def carries `explain` and `validate` only where a card declares an
operation on them, and each must be `nonGrantable` (`realm-policy-authoring`
§9, §10, §11).

`readSource` is **not declarable** under any name or as any `base`: the realm
answers it before it would consult a stored definition, so a declaration under
it would never be reached.

**A file's operations are the ones its class declares, and its class comes from
its extension.** The platform maps each file extension to a base file class, and
a realm does not configure it. Two of those classes carry a declared operation:
every stored `.log` is `LogFile` and every stored `.jsonl` is `JSONLFile`, and
each declares `record`, an `appendLine` whose line the realm composes rather
than the caller:

```ts
// @cardstack/base/log-file-def
export class LogFile extends TextFileDef {
  @operation static record = {
    base: 'appendLine',
    params: { what: StringField },
    input: bxl`. + { line: (TEXT(NOW(); "yyyy-mm-dd hh:mm:ss") + " " + actor() + " " + params("what")) }`,
  } satisfies OperationDeclaration;
}
```

`JSONLFile.record` takes the same `what` and appends
`{"at": …, "actor": …, "what": …}` as one line, so the file stays parseable
entry by entry. Link the file with the class that declares the operation, and
invoke it by name on the linked instance:

```ts
@field auditLog = linksTo(LogFile);
```

```ts
b.on(this.record.auditLog).record({ what: 'transferred to intensive care' });
```

The linked instance is a `LogFile` because its extension says so, whatever
class the field names. Naming `LogFile` (not `TextFileDef` or `FileDef`) on the
field is what types `record` on the linked value and keeps the file picker to
`.log` files. The base `update` and `appendLine` stay available on every file
alongside it.

**A declaration on your own `FileDef` subclass is unreachable rather than
broken.** No stored file resolves to an author's subclass, so an operation
declared on one lowers, indexes, and is never found by name — and the instance
carries no such member either, so the call throws before any request is made.
For an append-only record, store it as a `.log` or `.jsonl` and use `record`;
for anything the realm must compute on a card, declare the operation on the
card.

The names `atomic`, `on`, `find`, `parallel` and `serial` belong to the
invocation surface and cannot name an operation. Nor can `query`: it is the
name an ad-hoc search is invoked and granted under, so a saved search declared
under it would share that grant with every filter a caller writes over the
type — the `query` base is declarable, under any other name. Neither can a name
that already
resolves on the class, such as `displayName` — except an inherited operation of
the same name, which is how a subclass overrides one.

### `callApi` — a request to an outside service

The request is data. The realm server builds it from the declaration and the
invocation and sends it through its guarded outbound client. Nothing of the
card runs at call time.

```ts
import StringField from '@cardstack/base/string';
import {
  bxl,
  instance,
  operation,
  params,
  type OperationDeclaration,
} from '@cardstack/base/operations';

export class Repository extends CardDef {
  @field owner = contains(StringField);
  @field name = contains(StringField);

  @operation static openIssues = {
    base: 'callApi',
    label: 'List the open issues in this repository',
    params: { label: StringField },
    url: 'https://api.github.com/repos/{owner}/{repo}/issues',
    path: { owner: instance('owner'), repo: instance('name') },
    query: { state: 'open', labels: params('label') },
    headers: { accept: 'application/vnd.github+json' },
    output: bxl`{status: .status, issues: .body}`,
  } satisfies OperationDeclaration;
}
```

```ts
let { status, issues } = await operations(repo).openIssues({ label: 'bug' });
```

| Key        | What it is                                                                 |
| ---------- | -------------------------------------------------------------------------- |
| `url`      | Absolute `https:`, one host written out in full (no `*`). A whole path segment written `{name}` is filled from `path`; nothing else in the URL is filled |
| `path`     | The value for each `{name}` segment. Each fills exactly one segment, encoded, so `../x` stays one segment |
| `query`    | Query-string parameters, appended and encoded                              |
| `headers`  | Header values. `X-Boxel-*` headers are never sent                          |
| `json`     | A JSON body, sent as `application/json`                                    |
| `graphql`  | `{ document, variables }`: a fixed document string, every value passed as a variable |
| `form`     | A form body, `{ name: value }`, sent as `application/x-www-form-urlencoded`, for an API that takes only that (Twilio, Stripe). See below |
| `method`   | `GET`, `POST`, `PUT`, `PATCH` or `DELETE`. Absent: `GET`, or `POST` when there is a body |
| `perInstance` | Optional. `true` when each card needs its own approval (one webhook URL per channel card). Approved from the card (`cardId`), never the type; `keyReadiness` on the type answers `undefined` |
| `keyKind`  | Optional. The kind of key the slots take: `'static'` (a key or token pasted as it is), `'google-service-account'` (a Google service account's key file, from which Boxel mints Google access tokens) or `'oauth'` (an account connected through a sign-in app), for every slot or by slot name (`{ token: 'oauth' }`; an unnamed slot is `userKey` or `apiKey`). Only a key of that kind is approved for the slot, and the secure window asks for that kind when the user adds one. Absent, any kind may be approved — see [`api-integrations`](../api-integrations/SKILL.md) |
| `output`   | Optional. Maps the response, `{status, headers, body}`, to the object the caller gets back — an object, never a list or a bare value |

A request carries one body: `json`, `graphql` or `form`. The body's content
type is set for you unless `headers` sets one.

**A form body** maps each field name to its value. A value may be text, a
number, a boolean, a typed reference, or objects and lists of those, and
objects and lists are named the way Stripe and Twilio read them:

```ts
import { JsonField } from '@cardstack/base/json-field';
import {
  actor,
  operation,
  params,
  realmConfig,
  type OperationDeclaration,
} from '@cardstack/base/operations';

@operation static startCheckout = {
  base: 'callApi',
  label: 'Start a checkout for the chosen prices',
  params: { lines: JsonField },
  url: 'https://api.stripe.com/v1/checkout/sessions',
  headers: { authorization: 'Bearer {{apiKey}}' },
  form: {
    mode: 'payment',
    success_url: realmConfig('checkoutDoneURL'),
    line_items: params('lines'), // [{price, quantity}, …]
    metadata: { buyer: actor() },
    'expand[]': ['line_items'],
  },
} satisfies OperationDeclaration;
```

| Value                         | Sent as                                                   |
| ----------------------------- | --------------------------------------------------------- |
| text, a number or a boolean   | `name=value`                                              |
| an object                     | `name[member]=…` for each member                          |
| a field's list of text, numbers or booleans | the name once per item: `MediaUrl=a&MediaUrl=b`; name the field `expand[]` for an API that wants `expand[]=a&expand[]=b` |
| a list of objects             | numbered: `line_items[0][price]=…&line_items[0][quantity]=…` |
| a list inside an object or a list | numbered, whatever its items are: `line_items[0][tax_rates][0]=…&line_items[0][tax_rates][1]=…` |
| `null`, an empty list or an empty object | left out                           |

A param can hold a list of any length, so one operation covers every length
rather than one operation per length. A form has no way to send an empty list,
so a card should not call with one where the API requires the field. No name
in a form, a field's or a member's, holds a slot: names are sent as written.
Fields, and an object's members, are sent in the order of their names, not the
order they are written in; a list keeps its order.

Values are the typed references (`params()`, `actor()`, `realmConfig()`,
`instance()`). Invoked on an instance, `instance('field')` reads the card's
indexed fields, computed ones included. Invoked on the type —
`operations(Repository).openIssues(…, { realm })` — there is no card, so only
the payload, the caller and the realm's settings are in scope, and an
`instance()` is refused.

**A request goes to `https:`.** The realm server refuses to send one over
plain `http:` — `guard-refused` — except to a local host in development.

**Where the request goes is its destination**: the URL's origin and its path
up to the last `/` before the first `{name}` segment (or the path's last `/`
when it has none), written the way the URL parser writes it — host
lower-cased, default port dropped, `..` resolved. `url:
'https://api.github.com/repos/{owner}/{repo}/issues'` goes to
`https://api.github.com/repos/`. Every request the operation builds must stay
under its destination, so put the fixed part of the path before the first
`{name}`: the destination then says as much as it can about where the request
goes.

**The answer is the vendor's response, whatever its status.** A 404 or a 500
from the API comes back as `{status, headers, body}` for the card to read, not
as a refusal. `body` is parsed JSON when the API sends JSON and text
otherwise. `headers` carries only the ones that describe the body
(`content-type`, `etag`, `cache-control`, `link`, `location`, `retry-after`,
rate-limit headers and the like), never `set-cookie`.

**A request that needs a key is sent only as its key's owner approved.** The
declaration grammar has credential slots — `{{userKey}}` for the invoking
user's key, `{{apiKey}}` for one the realm holds, `{{apiKey:name}}` for a named
one, `|basic` for the HTTP Basic form — written inside a header, query, `path`,
JSON body or form value string. A slot is filled only from an **approval**: the key's
owner approves the operation, in this realm, in Boxel's secure window (every
operation on the card at once; see [`api-keys`](../api-keys/SKILL.md)), naming
which of their keys fills it. Until then the operation is refused
`binding-not-approved` and nothing is sent. The approval also says where the
operation runs: **On a schedule only** (the default), or **On a schedule and when the card is opened**, which lets a card, the AI assistant or the CLI invoke it
too, within the key's limits. Approved for pipelines only, an invocation from
a card, the assistant or the CLI is refused `interactive-use-not-approved`. A
pipeline is run by the realm server, and nothing a card author writes — no
card, field, operation or `realm.json` setting — schedules one. A card that
calls the operation itself is a live card, and any card the user opens, from
any realm, can invoke an operation approved for interactive use and read the
response, since card code is not sandboxed per realm origin. So private data
takes the pipeline shape: the card renders fields a pipeline would write.
[`api-integrations`](../api-integrations/SKILL.md) §2 shows both shapes. An
operation with no slot works without any approval. The slot rules lowering
enforces are in §4.

**A user keeps their own keys in Boxel's secure window or the Boxel CLI,
never in a card.** Not in a field, a card's source, `realm.json` or the chat.
In the app, a card or the assistant opens the secure window with the
`open-secure-window` tool ([`api-keys`](../api-keys/SKILL.md)). A key belongs to the user,
not to a realm. The realm server stores it sealed and never hands the value
back; `replace` swaps in a new value. A share puts a reference to one of the
user's keys into a realm they write to:

```sh
boxel keys sign-in                                   # once: lets this CLI change keys
boxel keys status                                    # whether it can
boxel keys add <name>                                # masked prompt; --stdin or --key-file without a terminal; --anonymous [--anonymous-cap <calls>] [--anonymous-monthly-cap <calls>] lets people who aren't signed in use it
boxel keys anonymous <name> on|off [--cap <calls>] [--monthly-cap <calls>]   # whether people who aren't signed in may use the key, where a workspace's policy opens calls to them
boxel keys add <name> --kind google-service-account --key-file <file> --scope <scope>  # a Google service account
boxel keys share <name> --realm <url> [--as <label>] # into a realm they write to; where its policy opens calls to visitors, warns they will use the key, and refuses a key that doesn't allow it
boxel keys list                                      # their keys, never a value
boxel keys show <name>                               # one key and the shares it's in
boxel keys shares --realm <url>                      # a realm's shares, for its writers
boxel keys add <name> --kind oauth-client --client-id <id> --authorize-url <url> --token-url <url> --scopes <scope> --api-host <url>  # an OAuth app
boxel keys clients [--realm <url>]                   # the OAuth apps they can connect through
boxel keys connect <name> --client <app> [--realm <url>]  # sign in at the service in the browser
```

`replace`, `delete` (`--yes` without a terminal), `unshare` and `swap` (put
one of their keys into a realm's suspended share) work alike.

**A stored or shared key fills nothing by itself.** Approving the operation in
the secure window is what names a key for a slot. Storing or sharing a key
without that approval leaves a slotted operation refused
`binding-not-approved`.

**Changing a key needs the CLI signed in to manage keys.** A profile added
with `boxel profile add` through the browser already is; otherwise
`boxel keys sign-in` opens Boxel's sign-in in the browser and waits. Run at a
terminal, a change that finds no sign-in opens it itself; run without one, it
refuses and says to run `boxel keys sign-in`. `boxel keys status` says which.

**Who types the value.** Never ask for a key's value, repeat it, or put it in
a command line.

- In Claude Code, have the user run `boxel keys add <name>` (or `replace`) in
  their own terminal, or run it yourself with `--key-file <path>` for a file
  the user names. The other commands you can run.
- In the app, open the secure window with the `open-secure-window` tool
  ([`api-keys`](../api-keys/SKILL.md)); the user types the value there.

**A Google service account is a key whose token is what gets sent.** The
slot rules above apply unchanged: an operation carrying a slot is sent only
as its approval allows. What a service account changes is
what the slot would hold. The user stores the account's JSON key file as a
key of its own kind, and Google's API is sent a short-lived access token made
from it, never the file. So a Google request is declared like any other, with
the slot where Google takes a bearer token:

```ts
@operation static readRange = {
  base: 'callApi',
  label: 'Read a range of this spreadsheet',
  params: { range: StringField },
  url: 'https://sheets.googleapis.com/v4/spreadsheets/{id}/values/{range}',
  path: { id: instance('spreadsheetId'), range: params('range') },
  headers: { authorization: 'Bearer {{userKey}}' },
  output: bxl`{status: .status, values: .body.values}`,
} satisfies OperationDeclaration;
```

- **Each Google host is its own destination.** `sheets.googleapis.com` and
  `drive.googleapis.com` are different destinations, and nothing covers
  `*.googleapis.com`, so a card that calls both declares an operation for
  each.
- **Scopes belong to the key, not the card.** Say in the card which scopes it
  needs (`https://www.googleapis.com/auth/spreadsheets.readonly`, …) so the
  user enters a key that has them. A token without the scope gets Google's own
  403, which comes back as the response.
- **Never call the token endpoint yourself.** An operation addressed to
  `https://oauth2.googleapis.com/token` is refused `guard-refused`, with or
  without a key.
- **Where the slot is filled from a service account, a key Google refuses**
  (revoked, deleted, a disabled account, a subject the service account can't
  act as) is refused `credential-rejected`, and nothing reaches the API; the
  message says the owner replaces the key, and `err.meta.reason` is
  `rejected`. The same code comes when Google's token endpoint kept failing,
  with `err.meta.reason` `unavailable`, and the message says asking again
  later may work. Branch on the code and the reason; show the message.
- **Entering one.** In the secure window, the user chooses the key file under
  **Google service account**, which a card that declares
  `keyKind: 'google-service-account'` asks for without a choice. From a terminal:
  `boxel keys add <name> --kind google-service-account --key-file <path>
--scope <scope> [--scope <scope>] [--subject <email>]`. `replace` takes a new
  key file with `--scope` (and `--subject`) the same way. The key file is read
  from a file or `--stdin`, never typed.

**Never during a render.** A template that invokes a `callApi` while the card
renders is refused `not-during-render`: a render is replayed and shared, so it
may not send requests for whoever is looking. Invoke one from an action — a
click, a command, an agent.

A `callApi` travels on a write request, so the caller needs write permission
on the realm or a policy grant for the operation. It takes no
`transformations`.

### `params` — the payload schema

Field classes for scalars, `linkTo(CardClass)` for a card identity:

```ts
params: {
  question: StringField,
  deltaMg: NumberField,
  clinician: linkTo(Clinician),
}
```

The schema is the single source for the payload's TypeScript type, for checking
`params('…')` references, and for the endpoint's validation. That validation
checks presence, not type: every declared param must be in the payload or be
supplied by `input` (send `null` for an optional scalar), and a scalar is never
checked against its field class. A transform also refuses an undeclared key and
a non-JSON value; a create or append ignores extra keys and writes whatever
value it was given.

A `linkTo` param accepts a saved card's URL, or — inside a batch — the handle
of a card the same batch is minting. On a create or transform it is never
`null` (400 `invalid-params`), so keep an optional link out of the declaration
and set it afterwards; a `null` inside an `appendContainsMany` item is stored
as an empty link.

Only JSON crosses the wire (as of 2026-10): a `Date` passed for a `DateField`
param arrives as `{}` inside `atomic()` and as an ISO datetime outside it, and
`DateField`'s `yyyy-MM-dd` parser rejects both, so the card breaks at render.
Declare a date param as `StringField` and pass `'YYYY-MM-DD'`; `fill` copies it
into the `DateField`.

### The typed references

Values known only at invocation are written as markers. They are ordinary
function calls, not interpolation syntax:

| Marker                | Resolves to                                                      |
| --------------------- | ----------------------------------------------------------------- |
| `params('key')`       | That member of the request payload                                 |
| `actor()`             | The caller's Matrix user id — **only** that                        |
| `instance()`          | The target's own stored values — its `id` and its attributes      |
| `realmConfig('key')`  | A setting from the realm's `config` on `realm.json`                |
| `card(…)`             | A link identity, from a URL or another marker                      |

`actor()` takes no argument and **is not a card**. It belongs in text fields and
query filters. A link to the person acting is a `params` member declared
`linkTo(Person)` — an `actor()` where a card identity belongs is refused.

`realmConfig` is what lets one card type read a value that differs per realm — an
approver, a threshold, a default — without hard-coding it. A realm that
configures no such setting refuses the invocation rather than resolving the
marker to nothing.

### The sugar clauses

Each base accepts its own:

```ts
// transform: append, assert, set
@operation static addConsultant = {
  base: 'transform',
  params: { clinician: linkTo(Clinician) },
  assert: {
    unique: 'consultTeam',
    by: params('clinician'),
    snapshot: true,
    message: 'That clinician is already on this consult team',
  },
  append: { to: 'consultTeam', value: card(params('clinician')) },
} satisfies OperationDeclaration;

// create: of (required), fill
@operation static requestConsult = {
  base: 'create',
  of: ConsultRequest,
  params: { specialty: StringField, question: StringField },
  fill: {
    specialty: params('specialty'),
    status: 'requested',
    requestedBy: actor(),
    patient: instance('id'),
  },
} satisfies OperationDeclaration;

// appendContainsMany: field + item, or fields mapping each name to its item
@operation static recordVitals = {
  base: 'appendContainsMany',
  field: 'vitals',
  params: { heartRate: NumberField },
  item: { heartRate: params('heartRate'), recordedBy: actor() },
} satisfies OperationDeclaration;

// query: query (required)
@operation static admittedOnUnit = {
  base: 'query',
  params: { careUnit: StringField },
  query: {
    filter: {
      on: () => PatientRecord,
      eq: { careUnit: params('careUnit'), status: 'admitted' },
    },
    sort: [{ on: () => PatientRecord, by: 'patientName', direction: 'asc' }],
  },
} satisfies OperationDeclaration;
```

A class that filters on itself takes the thunk form `() => PatientRecord`,
because the class binding is not initialized while its own statics are built.
`of` and `linkTo()` take the same form (`of: () => Launch`) for a class
declared later in the module.

`append` adds to a collection; cardinality comes from the field type, so the
declaration names the field and the value and nothing else. `set` writes field
values. `assert` guards **data state** — it is never an authorization check.

`fill` and `set` differ only in which base carries them: `fill` populates a new
card, `set` writes an existing one.

### `input` — a value the caller cannot forge

`input` runs first, over the payload the caller sent, and produces the payload
the operation uses — so a value it supplies satisfies a declared param the
caller left out. It reads `.` (that payload), `params()`, `actor()` and
`realmConfig()`.

That is the difference between a log the caller writes and a log the realm
keeps. An `appendLine` declaring a `line` param hands the whole line to the
caller, including the part naming who wrote it; an `input` program composes the
line where a caller cannot reach it.

Two things to get right, both quiet when wrong:

- **`. +` merges into the payload; a bare object replaces it.** Writing
  `{ line: … }` on its own drops every declared param.
- **`NOW()` answers a spreadsheet serial, not a timestamp.** Format it —
  `TEXT(NOW(); "yyyy-mm-dd hh:mm:ss")` — or the line carries a number like
  `46023.518`.

`input` is accepted on every base, including the two appends and a file's
`update`, which carry no `transformations` program at all. So it is the only
stage that can stamp a realm-supplied value into an appended line.

### The raw escape hatch

For work the clauses do not express, a `transformations` program:

```ts
@operation static titrateDose = {
  base: 'transform',
  params: { medication: StringField, deltaMg: NumberField },
  transformations: bxl`
    assert(
      .status == "admitted";
      "A dose is titrated only while the patient is admitted"
    );
    (.medications[] | select(.name == params("medication")) | .doseMg)
      |= . + params("deltaMg");
  `,
} satisfies OperationDeclaration;
```

`|= . + …` reads the value the realm holds and moves it, so two callers
titrating at once compose instead of the second overwriting the first. Removing
an item needs a program too — `del(… | select(…))` — since no clause expresses
it.

The `bxl` tag **takes no substitutions**. A program reads the payload, the
caller and the target through the `params()`, `actor()`, `instance()` and
`realmConfig()` builtins rather than having values spliced into its text.

A declaration expresses its work with clauses **or** with a program, never both.
The two appends and a file's `update` edit stored bytes rather than running a
program over a document, so they carry no `transformations` at all. A create
runs none either (as of 2026-10): `of` + `transformations` lowers with no
finding and the program is stored but never reached, and an `input` program
cannot `assert`. To guard a new record, create it as a draft
(`fill: { status: 'draft' }`) and put the rules on a named `transform` that
asserts over the stored card and then sets the status — both in one `atomic()`
batch when they must land together.

### `links` — how much of the link graph an answer carries

A `read` or a `query` may declare how much of the card's link graph its answer
carries. Absent means `full`.

| `links`          | The answer                                                                                         | Declarable on    |
| ---------------- | -------------------------------------------------------------------------------------------------- | ---------------- |
| `full` (default) | Relationships name their targets, and the transitive closure of linked cards is assembled into `included` — with the results of the query-backed fields of the card the document is about | `read`, `query`  |
| `ids`            | Relationships name their targets and nothing is assembled; a consumer fetches each target on its own request | `read`, `query`  |
| `none`           | No relationship data at all, named or assembled                                                     | `query` only     |

```ts
@operation static read = {
  base: 'read',
  links: 'ids',
} satisfies OperationDeclaration;

@operation static rosterNames = {
  base: 'query',
  links: 'none',
  query: { filter: { on: () => Roster, eq: { term: 'fall' } } },
} satisfies OperationDeclaration;
```

**`none` is a query's strategy, never a read's.** A read's strategy governs the
card's plain `GET` too, and that is what the host loads a card with to render
and edit it. Under `none` the host would show the card's link fields empty, and
an edit to one would save what the editor showed **over the stored links** it
was never shown — a `linksToMany` edit replaces the whole list. `ids` is the
value to reach for to narrow a read: it still names each target, so the host
shows and edits the links and fetches each target itself. A query's `none` rows
carry no such risk, because the host never adopts them as live cards: each is
marked `meta.relationshipsWithheld: true` and renders from its HTML or loads
the card through its own read.

**On a `read`, a strategy governs only reads rooted at the declaring card.** A
linked card's own declaration is never consulted: a `full` read carries a
linked card whole — its relationships and what they link to — even when that
card's type declares `ids` for itself.

**On a `query`, it governs every result row alike**, whatever each row's type
says in its own `read`. It narrows each row's card, never the entry the row is
delivered in: the row still names its card and still carries its prerendered
HTML, which draws the links whatever the strategy. A search run by a render is
exempt and keeps each row's stored links, because what it draws becomes part of
the rendering card's own HTML.

**An ad-hoc search has no declaration, so nothing narrows it below what the
request asks for.** No declaration narrows a `_search` or
`_federated-search`; only a declared, named query does.

**The request may narrow further, never wider.** When the realm sheds load, or
a consumer asks for links only, the request asks for `ids`; the realm serves
whichever of the request and the declaration withholds more.

`links` governs **assembly, not derivation**. A computed value that derives
from a linked card is computed when the card is indexed, lives in the card's
own attributes, and is served under every strategy.

### `html` — formats served data-only

A `read` or a `query` may mark prerendered formats `unshareable`. Absent, every
format is shareable.

```ts
@operation static read = {
  base: 'read',
  html: { isolated: 'unshareable', embedded: 'unshareable' },
} satisfies OperationDeclaration;
```

The formats are `embedded`, `fitted`, `atom`, `head` and `isolated`, each
`shareable` or `unshareable`; a format left out is shareable. An unshareable
format serves that row **data-only, to every caller**: its prerendered HTML is
withheld, its data is not, and a consumer renders the card from its data.

**This can't be per-caller.** Prerendered HTML is rendered once per card and
format, under the realm's own authority, and shared by every viewer. A format
whose template draws a linked card bakes that card's content into the one
shared markup, so serving it hands the linked content to whoever receives it.
Nothing is rendered a second time or per caller; the format's markup is simply
withheld.

- **On a `read`** — the type's operation named `read`; an `html` on any other
  `read`-based operation is never consulted — it governs reads rooted at the
  card: its single-card HTML
  read, the last-known-good markup an errored read carries, and the markup a
  host-mode page for the card is served with.
- **On a `query`** it governs every row alike, whatever each row's type
  declares — the rule `links` follows. An ad-hoc search declares nothing and
  serves every format's markup. A search run by a render is exempt.

It is a claim about what a format draws, not a mechanism. An edit that starts
drawing a linked card in a format left shareable falsifies it silently — the
realm's policy reach warnings are what notice (see
[`realm-policy-authoring`](../realm-policy-authoring/SKILL.md) §9).

**A declaration applies uniformly.** The same request answers a realm writer
and a caller a policy grant admitted with the same document: `links` and `html`
are properties of the operation, never of how the caller was authorized.

### `label` — what a person sees

Any declaration, on any base, may carry a `label`: a short, plain-text phrase
for people. It is stored on the operation's definition as data, for anything
that presents the operation to a person to read.

```ts
@operation static listOpenPRs = {
  base: 'query',
  label: 'List your open pull requests',
  query: { filter: { on: () => PullRequest, eq: { state: 'open' } } },
} satisfies OperationDeclaration;
```

Write it as what the person is agreeing to, or about to do: "List your open
pull requests", "Archive this inbox", "Add a line to the audit log". Keep it
short and plain, and make it true of the request. A label changes nothing
about what an operation does.

**When your card shows an operation to someone, show its label beside the
request, never instead of it.** The label is the author's description, so show
what the operation does as well; a label that makes a write sound like a read
only teaches the person to distrust it.

An operation without a label reads as its name split into words, with
acronyms kept together: `listOpenPRs` is "List open PRs", `getURL` is
"Get URL". `operationDisplayLabel` from `@cardstack/runtime-common` gives
either answer. Read the operation through `getOperations`, which merges what
every ancestor declared; a plain static read sees only the nearest class:

```ts
import { operationDisplayLabel } from '@cardstack/runtime-common';
import { getOperations } from '@cardstack/base/operations';

let shown = operationDisplayLabel(
  'listOpenPRs',
  getOperations(PullRequestInbox).listOpenPRs,
);
```

A label is refused, by the decorator when the class is defined and as
`invalid-label` when the module is indexed (§4), when it is:

- not a string, or nothing visible: empty, or only whitespace and invisible
  formatting characters;
- longer than 80 characters, counted as a person sees them, so a flag or an
  emoji sequence counts once;
- carrying markup (`<` or `>`);
- more than one line, or carrying any other control character;
- carrying a bidirectional control, which reorders how the text around it
  displays;
- not well-formed text: half of a surrogate pair with no other half.

### `optimistic`

A declaration may carry `optimistic`, and it is validated and stored on the
lowered operation. Nothing reads it, so setting it changes no behavior — write
it only to record an intent, never expecting an effect.

### `nonGrantable` — out of every policy grant

`nonGrantable: true` keeps an operation out of reach of every grant in a
realm's policy:

```ts
@operation static addToCareTeam = {
  base: 'transform',
  params: { memberId: StringField },
  append: { to: 'careTeamIds', value: params('memberId') },
  nonGrantable: true,
} satisfies OperationDeclaration;
```

The realm's own permissions are untouched: a realm writer still invokes it,
and so does a reader when it reads. Only a caller the realm admits through a
grant is refused, with the refusal a grant that does not hold gets (§5). A
policy grant naming it records `grants-authorization-infrastructure` and is
left out.

Mark an operation this way when it does either of two things:

- **It edits authorization-bearing state** — a field a policy's `where` reads
  to decide access, such as a care-team list. A grant on it would let whoever
  it admits widen their own access, and anyone else's.
- **Its answer should not reach a caller the realm admits only through a
  grant.** `explain` and `validate`, which answer what a policy decides and
  what it compiles to, always carry it; the decorator refuses either declared
  without it.

**The flag sticks.** It holds on the type that declares it and on every
subtype, and a subclass that redeclares the operation without it does not
make it grantable. Lowering keeps it on a declaration with findings too, so a
broken declaration never becomes grantable by breaking.

**A built-in is marked by redeclaring it under its own name:**

```ts
@operation static update = { base: 'update', nonGrantable: true };
```

A redeclaration with no clauses is the built-in behavior, so `update` and
`delete` (and a clause-free `appendContainsMany`) can be marked this way. The
built-in `create` can't: the decorator requires `of` on every `create`, and a
`create` with `of` is a declared create of that type, not the built-in one.
Any `update`, `create` or `delete` a type declares also takes the card+json
verb of that name away from a caller the realm admits through a grant, since a
verb reaches the built-in only (§6). `readSource` and the name `query` cannot
be declared, so neither can be marked.

The value must be a boolean. Anything else is refused by the decorator when
the class is defined.

## 3. Invoking

```ts
import { operations } from '@cardstack/base/operations';

let result = await operations(report).addComment({ body: 'Reviewed.' });
let created = await operations(Report).create({ headline: 'From class' });
```

Nothing hangs off the instance itself — a card's property namespace belongs to
its author's fields — so a card is passed to a function the way it is to
`isSaved(instance)`.

**Typing an instance call.** TypeScript cannot read a class's statics through an
instance type, so name the class to get typed members:

```ts
get ops() {
  return operations<typeof PatientRecord>(this.record);
}
```

A call that names no class still works and still reaches every operation; its
members simply take any payload.

### What a write answers

```ts
{
  id: string,
  version: string,
  generation: number | null,
  indexPending?: true,
  lastModified: number,
}
```

plus `lid` on a create **that a batch staged** — a single
`operations(Class).create(…)` names no local id, so none comes back. A write
reports identity and version rather than reprinting the document: the caller
supplied the state, and reconciling against the version is the common case. A
`read` answers its document. A `delete` answers `null`.

`generation` is the index generation the write landed on. It is `null`, with
`indexPending: true`, when the realm answered before indexing the write — see
below. The write has landed either way; `indexPending` is about reading it back
through the index, not about whether it happened.

### Waiting for indexing — or not

By default a write waits for the realm to index it before answering, so that a
search straight afterwards finds it. Indexing renders each card it visits, so
the wait is bounded: past a few seconds the realm answers anyway, with
`indexPending: true`, and indexing finishes afterwards.

A card that does not need to read its own write back through the index can skip
the wait. The option goes where the bucket is built, and covers every write
that bucket makes — a single call and an `atomic()` batch alike:

```ts
await operations(this.classroom, { skipIndexWait: true }).update({
  attributes: { teacherIds },
});

await operations(report, { skipIndexWait: true }).delete();

await operations<typeof PatientRecord>(this.record, {
  skipIndexWait: true,
}).atomic((b) => {
  /* … */
});
```

The answer comes as soon as the write is stored, with `indexPending: true`.

**What skipping costs.** Reads that go through the search index can miss the
write until its index event arrives — normally moments later, longer when the
realm is busy indexing. That includes `operations(card).read()`. Opening the
card, or loading it through the store, waits a little for the writer's own
pending indexing (up to about ten seconds) and then reads whatever the index
holds, so treat even those as eventually consistent when indexing is slow.
Other users and other sessions see the write when its index event reaches them,
as they would anyway.

**When to skip.** Skip when nothing after the write reads back or searches for
what it just wrote:

- the write's answer (`id`, `version`) is all the caller reads;
- the card re-renders from the index event the write produces (the usual case
  for a button on the card's own template);
- a saved search or `searchResultsComponent` that refreshes itself as the realm
  indexes, rather than a one-off search issued straight after the write.

Keep the default when the next step is a search that has to include the write,
such as creating a card and then listing "all cards of this type" with a
one-shot `_search` in the same handler.

The store takes the same option for a card save and a card delete:
`store.add(card, { skipIndexWait: true })` and
`store.delete(id, { skipIndexWait: true })`. The `invoke-card-operation` tool
takes it as a `skipIndexWait` input and reports `indexPending` in its result.

### Batches

`atomic()` commits several operations all-or-nothing, in one realm:

```ts
await this.ops.atomic((b) => {
  let consult = b.requestConsult({ specialty, question });
  b.addConsult({ consult });
  b.on(this.record.auditLog).record({ what: 'consult requested' });
});
```

`b.create()` and every declared operation answer a **handle**. A create's handle
is the local id a later entry links the new card by — the one spelling of a link
to a card that has no URL yet.

- `b.on(card)` targets another card in the same realm. A card in another realm is
  refused: a batch commits under one realm's write lock.
- `b.find(filter, { field, expect })` targets whatever the realm matches.
- `b.parallel((p) => …)` and `p.serial((s) => …)` nest to any depth. The top
  level is serial, and results mirror the nesting.
- Returning handles from the builder types and orders the results; returning
  nothing answers every entry's result positionally.

**No read-your-own-writes.** A read entry sees pre-batch state. Two members of
one parallel group that write the same card are a `conflicting-targets` refusal,
because members are evaluated against the state the group started from — two
entries touching one target belong in serial order. A `b.find` filter runs
against the index as the batch found it, so a card an earlier entry creates is
not one it can match.

**Every entry is gated, and one refusal refuses the batch.** Each entry is
judged on its own target, an `expect: 'many'` target card by card, and a single
refusal answers the whole batch with that entry's error and zero writes. An
entry the realm's policy decides is judged inside the write lock, against what
the entries before it in a serial run left (in a parallel group, against what
the group started from), so a write that follows another to the same card is
judged by the card that write leaves. A create against a type is judged by the
card it would mint; a create anchored on a card is judged by that card.

Under a policy, for a caller the realm's permissions decline:

- **A `b.find` filter is an ad-hoc search**, authorized as `query` on its type
  with that type's `query` grants composed into it, so it finds only the cards
  those grants admit. With no such grant it finds nothing: `expect: 'one'`
  answers 400 "matched no card", the answer a filter matching nothing gets,
  and `expect: 'many'` runs against `[]`. The entry's own operation is then
  gated on each card found, so a batch that finds its targets needs both
  grants.
- **A found card the entry's operation refuses answers a 404
  `target-not-found` that names no card**: no `id`, the detail
  `no such target`, and the entry only by position — its own position (`0`
  for a top-level entry) for `expect: 'one'`, `[0].boxel:target[n]` for the
  nth card an `expect: 'many'` found.
- **For one who may not read the realm, it mints the ids of the cards the
  batch creates.** A `lid` still links cards within the batch and comes back
  beside the minted id as `{ lid, id }`, but it does not name the file (§6). A
  caller who may read the realm names their own, as any writer does.

### Saved searches

A declared `query` is **the one member that is not awaited**. It answers a live
entries resource that re-runs as realms index:

```ts
@cached
get onThisUnit() {
  return operations(PatientRecord).admittedOnUnit.query({
    careUnit: this.args.model.unitName ?? '',
  });
}
```

```hbs
<@context.searchResultsComponent @query={{this.onThisUnit}} @mode='hover' />
```

Calling it answers the resource; `.query()` answers the wire query, which is what
a card hands to `@context.searchResultsComponent` to render the rows itself.

Every call builds an **independent** search with its own realm subscriptions, so
make the call **once** and hold what it answers: a field, a one-time assignment,
never an uncached getter and never during render.

A field is the plain form, and it fixes the payload at construction. Where the
payload arrives later — `@model` is typed with every field optional, because a
template renders a card that may still be loading — a `@cached` getter is the
variant that lets it through, at the cost of building a fresh search whenever
what it reads changes. A payload whose values are tracked moves an existing
search without a second call, so reach for the getter only when the payload
itself is not.

**A search that compares against the caller answers nothing when the session
cannot supply one** — nobody signed in, or a render, which authenticates as
itself. That is the one silent case, and it applies only to a declaration that
reads `actor()` — which is the search worth guarding:

```hbs
{{#if this.myPatients}}
  <@context.searchResultsComponent @query={{this.myPatients}} @mode='hover' />
{{/if}}
```

The search component treats an absent query as idle, so a card may hand it over
either way; the guard is what lets the surrounding markup say something else
instead. A search that names no `actor()` always answers, so guarding one buys
nothing. Everything else — a payload the declaration cannot resolve, a realm
scope that will not resolve — is raised at the call rather than swallowed.

**A saved search is as fresh as the index.** It reads the search index, which
lags a write until that write is indexed. To read a card just written, read the
card.

### A saved search on the wire

`.query()` answers the search this side lowered, plus three members that name
it — `operation`, `on` (the declaring type's code ref) and `params`:

```ts
{
  operation: 'admittedOnUnit',
  on: { module: '…/patient-record', name: 'PatientRecord' },
  params: { careUnit: '4 West' },
  filter: { … },  // lowered here; the realm replaces it
  sort: [ … ],
  realms: ['https://example.com/hospital/'],
}
```

**The realm runs its own resolution, never the caller's.** It reads the
declaration from its own definition of `on` and lowers it again with `params`
and the user it authenticated, so `actor()` comes from the token, whatever the
payload says about anyone. The declared filter replaces the caller's — even
where the declaration writes none — and a declared `sort` or `page` stands over
the caller's. The caller still supplies the fieldset, `cardUrls`, `scope`, the
`htmlQuery` binding in its filter, and `sort` / `page` where the declaration
names none; which rows match is never theirs to choose. The host ignores the
filter, sort and page lowered here; what this side's lowering still decides is
which realms the request names, so a stale definition on the client can change
which realms are searched, never which rows they return.

**Only the realms the request names are searched.** A declaration that names
its own `realms` is narrowed to the ones the request names; one that names none
searches the request's. A realm's own `_search` searches that realm alone.

**`query` is not a saved search's name.** It is reserved: `@operation` refuses
it, and lowering records `reserved-name`. A grant on `query` is the grant for
ad-hoc searches — see
[`realm-policy-authoring`](../realm-policy-authoring/SKILL.md) §7.

| Request                                                              | Answer                      |
| -------------------------------------------------------------------- | --------------------------- |
| An operation the type does not declare                               | 404 `unknown-operation`     |
| An `on` the realm cannot resolve                                     | 404 `target-not-found`      |
| An operation that is not a query, the bare base name `query` included | 400 `invalid-params`, or the refusal invoking it would get (405 `operation-not-allowed` for one the type doesn't carry, 404 `unknown-operation` for one it doesn't declare) |
| A declaration carrying lowering findings                             | 422 `invalid-operation`     |
| No `on`, `params` that is not an object, a declared param left out   | 400 `invalid-params`        |
| A declaration reading `actor()`, and nobody authenticated or a render the realm runs as itself | 401 `actor-required` |
| The declaration's realms and the request's share none                | 400 `invalid-params`; the detail does not list the declaration's realms |

**None of these applies when no realm the request names could contribute a
row.** On `_federated-search`, when every named realm is archived, or is one the
caller cannot read whose policy could not admit them, the declaration is never
read: the answer is 200 with no rows, even for an unknown operation or a
malformed request.

**A declaration that cannot be read is a realm that did not answer.** The realm
reads it through one the caller reads, or failing that one their policy
reaches, passing over any that will not mount. When none mounts, the answer is
200 with no rows and `meta.incomplete: true`.

### What a policy does to a search

**Each realm applies its own policy to its own rows.** A caller the realm's
permissions let read it is served every matching row, and no policy is loaded.
For a caller they decline, the realm composes the grants its policy holds for
the search into it and serves the rows those admit, or none. What a realm named
in `_federated-search` contributes:

| Realm                                                   | Contributes                                                  |
| ------------------------------------------------------- | ------------------------------------------------------------ |
| One the caller reads                                    | Every matching row; no policy is loaded                      |
| Unreadable, with a policy but no grant for this search  | No rows, 200 — byte-identical to a grant that matches nothing |
| Unreadable, with no policy                              | No rows; the realm is not mounted, and its `realm.json` is read from disk |
| Unreadable, and its policy cannot be judged — the realm won't mount, the policy won't load or compile, or a compiled grant filter throws when the search runs (a grant recording `policy-not-filterable` just contributes nothing) | Counted failed: its rows are withheld, the other realms answer, and the result carries `meta.incomplete: true` |
| Archived                                                | No rows                                                      |
| Not public, from an anonymous caller                    | The rows its anonymous `query` grants admit where its policy opens `query` to callers who aren't signed in, or counted failed (`meta.incomplete: true`) once the caller is over its anonymous rate limit; no rows where it doesn't. When none of the named realms the caller can't otherwise read admits them, 401 for the whole request |
| A URL the registry does not know                        | 404 `Realms not found`                                       |

**A realm's own `_search` differs from `_federated-search`.** A realm with no
policy answers a caller who cannot read it with the permissions' 403, where
`_federated-search` answers no rows. A realm whose policy won't load or compile
refuses such a caller with a 500 "Policy unavailable", where
`_federated-search` counts it failed. An archived realm that names a policy
answers a caller its policy reaches with the archived 403 whenever their grant
would return a row, where `_federated-search` answers no rows.

**What a search is authorized as.** A saved search is invoked under its own
name, on the type that declares it. An ad-hoc search is invoked as `query` on
the type its filter targets:

- A filter anchored on one type (`type`, or a predicate's `on`) consults that
  type's `query` grants.
- An `every` consults the type of each anchored branch.
- An `any` whose every branch is anchored is judged type by type, each type's
  grants admitting only that type's cards (`{ on: Type, any: [...] }`). One
  unanchored branch leaves the whole `any` unanchored.
- A filter with no anchor, or one naming a type the realm cannot resolve,
  consults no grant: the permissions alone decide, so a caller only a grant
  reaches gets no rows, not a refusal.

A grant-reached caller never finds file rows — `query` is carried by card types
only — and a `read` grant never lets anyone enumerate a type.

**Revocation reaches search at reindex.** A search judges a grant against the
index, so a card whose edit takes a caller out of a grant (their id removed from
the field it reads) still lists for them until the card is reindexed. A direct
`GET` judges the stored card and refuses at once.

**A filter and a grant on one path into a list must meet in one element.** The
caller's filter and the grants run as one query, so when both test the same
path into a list (the list itself, or the same field of the cards it links to),
one element of the list must satisfy both. Conditions on different fields of a
list's items are each met by any element, not necessarily the same one. A
teacher whose grant reads `.teacherIds | any(. == actor())` finds every
classroom they teach by searching `teacherIds` for themselves, and none of those
classrooms by searching `teacherIds` for a colleague, not even one that lists
them both. A classroom another of their `query` grants admits, such as one they
own, is still found. Write such a search against another field. A saved search's
own filter is composed the same way. The limit only ever removes rows; it never
admits one the grant does not.

**A render the realm runs as itself is never scoped to a viewer.** Its search
consults no policy, and a realm it cannot read contributes no rows, so the
prerendered HTML is the same for everyone. That is also why a saved search
reading `actor()` answers nothing there.

### `meta.policyScopedRealms`

A result some policy shaped carries `meta.policyScopedRealms`: a list of realm
URLs, not a flag. It lists every realm the caller does not read outright,
whatever that realm contributed, and on a saved search every realm the request
named. It reads the same whether a grant admitted rows or none, so it never
says whether the caller holds a grant.

It matters to a card that merges cards it holds into a result. Of the search
surfaces, only `getCards` with `isLive: true` does that itself, through its
client-side arm, and that arm never adds a card from a listed realm that the
server did not return, and never adds one from a realm no completed search has
answered unless the session reads that realm. Listed realms' returned rows
still narrow as cards change; they never widen. `getSearchEntriesResource`,
`@context.searchResultsComponent` and saved searches run no client-side arm. A
card doing its own merge follows the same rule: a card from a listed realm that
the result did not return may be one the realm withheld.

### Asking first: `@context.canInvoke`

A control for an operation the caller may not use should not render. Rendering
every control and letting the refusal arrive after the click is the failure
this API exists to prevent. `@context.canInvoke` asks the realm what its gate
would decide:

```gts
import { on } from '@ember/modifier';
import { tracked } from '@glimmer/tracking';
import { CardDef, Component, contains, field } from '@cardstack/base/card-api';
import StringField from '@cardstack/base/string';
import {
  operation,
  operations,
  OperationsError,
  params,
  type OperationDeclaration,
} from '@cardstack/base/operations';

export class Classroom extends CardDef {
  @field title = contains(StringField);

  @operation static rename = {
    base: 'transform',
    params: { title: StringField },
    set: { title: params('title') },
  } satisfies OperationDeclaration;

  static isolated = class Isolated extends Component<typeof Classroom> {
    @tracked refusal: string | undefined;

    get record(): Classroom {
      return this.args.model as Classroom;
    }

    // Only `false` is the realm saying no. `undefined` is no answer yet, and
    // it is also all a render with no `canInvoke` ever gets.
    get hideRename(): boolean {
      return this.args.context?.canInvoke?.('rename', this.record) === false;
    }

    rename = async () => {
      this.refusal = undefined;
      try {
        await operations<typeof Classroom>(this.record).rename({
          title: 'Renamed',
        });
      } catch (err) {
        this.refusal =
          err instanceof OperationsError
            ? (err.detail ?? err.message)
            : String(err);
      }
    };

    <template>
      <h1>{{@model.title}}</h1>
      {{#unless this.hideRename}}
        <button type='button' {{on 'click' this.rename}}>Rename</button>
      {{/unless}}
      {{#if this.refusal}}
        <p role='alert'>{{this.refusal}}</p>
      {{/if}}
    </template>
  };
}
```

`canInvoke(operation, target, { realm }?)` answers `boolean | undefined`,
synchronously, and the template re-renders when the answer lands. A target is
a saved card, its URL, or a card class. A class asks whether a card of that
type may be created, or a `query` it declares run, in `realm` — by default the
session's default writable realm, where a create that names no realm lands.

- **Guard for its absence.** Operator mode and host mode provide it. A
  prerender and freestyle do not, so read it as
  `this.args.context?.canInvoke?.(…)`. Inside the prerender app it answers
  `undefined` even where something provides it: that render authenticates as
  itself, and its answer would bake one identity's permissions into HTML
  everyone is served. The live render that follows asks for itself.
- **Hide on `false`, never on `undefined`.** `undefined` covers a pair still
  being asked, a request that failed, an unsaved card, a card in a realm the
  session does not know, and a class with no realm to ask. A failed request is
  left unanswered rather than denied, and nothing retries it until a later read
  asks again — so a control disabled on `undefined` can stay disabled. Leave it
  visible and let the call's own refusal speak.
- **It is advisory.** The invocation is gated again, against the state as it is
  then, so `true` is what the answer was a moment ago. Handle the refusal
  anyway, as the `catch` above does, and never skip anything on a `true`.
- **Reads are coalesced.** A read enrols its pair rather than fetching. Every
  pair first read in one render pass goes out on the microtask after it, as one
  `POST {realm}/_capabilities` per realm, split into requests of at most 100
  pairs. Thirty cards gating three controls each cost one request.
- **Answers follow their inputs.** A held answer is asked again when a realm
  index event names its card; every type pair in the realm is asked again on
  any of its index events; every pair in the realm is asked again on a full
  reindex or a change to the realm's config. What no event carries — a policy
  card in another realm, a permission change — is caught by staleness: the
  first read of an answer at least 5 seconds old asks again. That re-ask
  happens on a read, so it lands when the template next renders. The held
  answer is served while the realm is re-asked, so the control does not
  flicker. A session ending drops every answer.

### What the answers mean

**Every pair is asked of the realm**, callers its permissions allow included;
the realm answers those from its permissions without loading a policy. Never
answer locally from `canWrite` instead: it says yes to an operation the type
does not carry and to a card that is gone, where the gate says no, and it is
no answer at all for an operation built on a read.

**`canInvoke` surfaces no `conditional`.** It answers `allowed`, so a
conditional answer reads as `true`. On the raw `_capabilities` answer,
`conditional: true` appears only for a create against a type whose matched
grant has a `where`, and only for a caller who may read the realm: the
predicate still runs on the card the create mints. A write on a stored card is
decided definitely, by running the predicate against the card as stored.

**In a realm that names a policy, a signed-in caller who may not read it gets
a bare boolean** — no `reason`, no `conditional` — so a card no grant admits
answers exactly as a card that is not there. Their create against a type whose
grant has a predicate answers a bare `true`. In a realm with no policy, such a
caller's whole request is refused with the permissions' 403, and `canInvoke`
stays `undefined` for every pair.

**An operation built on `query` is asked with the type that declares it** as
the target; a card target answers `false`, as invoking the query on a card is
refused. A caller who may read the realm is told `true`. A signed-in caller who
may not is judged as the search that runs the query judges them: `true` where
the realm's policy holds a grant on it for that type that compiles to a search
filter (see [`realm-policy-authoring`](../realm-policy-authoring/SKILL.md) §7),
otherwise `false`. That `true` says the search will run, not that it will match
anything: a caller the filter matches no rows for is told `true` and sees an
empty list. A request that authenticated nobody, from a caller who may not
read the realm, is refused whole with 401 (`actor-required` under a policy),
so `canInvoke` answers `undefined`.

### `POST {realm}/_capabilities`

What `canInvoke` sends, for a command or a script that asks directly. The
request authenticates as any realm request does.

```json
{
  "checks": [
    { "target": "https://example.com/school/Classroom/7b2", "operation": "rename" },
    { "target": { "module": "https://example.com/school/classroom", "name": "Classroom" }, "operation": "create" }
  ]
}
```

A target is a card URL or a type `{ module, name }`. A request carrying more
than 100 pairs, a body that is not JSON, or a pair missing its `operation` or
`target` is refused whole with 400 `invalid-params` — a truncated answer would
read as a list of denials.

```json
{
  "checks": [
    { "operation": "rename", "target": "https://example.com/school/Classroom/7b2", "allowed": false, "reason": "policy-predicate-failed" },
    { "operation": "create", "target": { "module": "https://example.com/school/classroom", "name": "Classroom" }, "allowed": true, "conditional": true }
  ]
}
```

Answers are positional, each echoing its question, served as JSON with
`cache-control: no-store`. A pair sent twice is decided once. `reason` is the
code the invocation itself would carry — for example
`operation-not-permitted`, `policy-predicate-failed`, `operation-not-allowed`,
`invalid-operation`, `unknown-operation`, `target-not-found`,
`wrong-entry-point`, or, for a reader, `internal-error` for a pair the realm
could not decide.
A write no policy may judge is refused without asking one: `actor-required`
when nobody is signed in, `operation-not-permitted` for a signed-in caller
whose session may only read or whose realm names no policy. A caller who may
not read the realm never gets a `reason`.

A check runs the gate and nothing past it: it stages nothing, takes no lock,
enqueues no index job and broadcasts no event.

## 4. What lowering refuses

These are recorded when the module is indexed, not thrown. An operation carrying
findings has no runnable form, and invoking it is refused with
`invalid-operation`.

| Finding                   | What it means                                                      |
| ------------------------- | ------------------------------------------------------------------- |
| `unknown-field`           | A clause names a field the type does not have                       |
| `not-a-collection`        | Appending to, or asserting over, a single-value field               |
| `undeclared-param`        | `params('x')` for a key `params` does not declare                   |
| `computed-write`          | A write into a computed field — the next read overwrites it         |
| `read-only-write`         | A write into a query-resolved field, or the card's `id`             |
| `link-collection-replace` | A `set` replacing a whole link collection — use `append`            |
| `path-crosses-collection` | A dotted path crossing a collection addresses nothing               |
| `link-requires-identity`  | A link position holding something that is not a card identity       |
| `write-through-link`      | A write whose path crosses a `linksTo` / `linksToMany`              |
| `unsearchable-read`       | Reading across a link not marked `searchable`                       |
| `unsnapshotted-assert`    | An `assert` over a computed or linked path without `snapshot: true` |
| `unresolved-type`         | A class no module exports under a name                              |
| `actor-not-a-card`        | An `actor()` where a card identity belongs                          |
| `invalid-program`         | A raw program that does not parse                                   |
| `invalid-query`           | A declared query the query grammar refuses                          |
| `reserved-name`           | An operation named `readSource` or `query`, or built on `readSource` |
| `base-not-carried`        | A base the def type does not carry                                  |
| `unrunnable-program`      | A program on a base that runs none                                  |
| `incomplete-append`       | An `appendContainsMany` that does not say what to append where      |
| `instance-out-of-scope`   | An `instance()` in a declared append, which never loads the document |
| `links-without-assembly`  | `links` on a base other than `read` or `query`, which assembles no link closure |
| `invalid-link-strategy`   | A `links` value its base can't apply — including `none` on a `read` (§2) |
| `html-without-rendering`  | `html` on a base other than `read` or `query`, which serves no prerendered HTML |
| `invalid-html-declaration`| `html` that isn't an object naming prerendered formats, each `shareable` or `unshareable` |
| `invalid-label`           | A `label` that isn't a single short line of plain text (§2)         |
| `invalid-request`         | A `callApi` request that can't be sent as written: a relative URL, a `*` in the host, a `path` value no `{name}` takes, an object where text is sent, a `form` that isn't an object of named fields, two bodies, a body on `GET` |
| `invalid-slot`            | Something that looks like a slot and isn't — `{{apiKey\|rot13}}`     |
| `slot-placed-twice`       | One slot in two places in a request                                  |
| `slot-name-reused`        | One name for a `userKey` slot and an `apiKey` slot                   |
| `slot-out-of-place`       | A slot in the URL as written, a header, query or form field name, a member name in a body, or a GraphQL document |
| `unencoded-path-parameter`| A value put into the URL other than as a whole `{name}` segment filled from `path` |
| `string-built-graphql`    | A GraphQL document built from values rather than written as one fixed string |
| `lowering-failed`         | Lowering itself threw on this operation — a fault in the realm, not the declaration |

The decorator refuses several of these where the class is defined — a
reserved name, a base the def type does not carry,
a `links`, `html` or `label` it can't apply — so a module that declares one throws as
it evaluates, and author code rarely records them. Lowering checks
them again because a stored definition outlives the code that built it. A
`read` whose declaration carries findings serves every format data-only.
`lowering-failed` costs only the operation it hit: the entry stays stored,
invalid and with its `nonGrantable` kept, so its name never falls back to a
grantable built-in.

Three of these account for most first attempts:

**An operation binds only to the target card's own stored values.** A linked card
is a separate document with its own operations, so a write whose path crosses a
link is refused — change the other card with its own entry in a batch.

**Reading across a link requires that link to be `searchable`.** A filter reaches
a linked card's fields only when the link that gets there says so:

```ts
@field attending = linksTo(Clinician, { searchable: true });
```

**An `assert` over a computed or linked value needs `{ snapshot: true }`.** A
program reads the card's stored document, which holds a link's target as a
reference rather than as the linked card and holds no computed value at all, so
the values the check compares have to be gathered first. That costs reads, which
the author opts into rather than paying invisibly. There is no non-snapshot form
of that check.

**An append has no `instance()` in scope.** An append edits stored bytes without
ever assembling the document, which is the whole reason the behavior exists;
offering `instance()` would mean the read the operation avoids. `params()`,
`actor()` and `realmConfig()` work. An item that needs the card's own values
belongs on a `transform`.

In an `appendContainsMany` item this is caught as `instance-out-of-scope` when
the module is indexed. An `input` program is not read that way, so an
`instance()` inside one fails at invocation instead — in an `appendLine`, which
has no clause and composes its line there, that is the only form it takes.

## 5. Refusals a caller sees

Thrown as `OperationsError`, whose `detail` carries the sentence:

```ts
import { OperationsError } from '@cardstack/base/operations';

try {
  await this.ops.escalateRhythmEvent({ eventId, findings });
} catch (err) {
  this.refusal =
    err instanceof OperationsError ? (err.detail ?? err.message) : String(err);
}
```

| Code                       | Meaning                                                      |
| -------------------------- | ------------------------------------------------------------- |
| `assertion-failed`         | A precondition did not hold — carries the author's `message`  |
| `invalid-params`           | The payload does not satisfy `params`, or a marker cannot resolve |
| `invalid-operation`        | The declaration has findings, so there is no runnable form    |
| `unknown-operation`        | No operation of that name                                     |
| `operation-not-allowed`    | The target's def type does not carry that behavior            |
| `target-not-found`         | Nothing at the target's URL                                   |
| `target-not-indexed`       | Written but not yet indexed — waiting resolves it             |
| `target-errored`           | The target's index row is an error row                        |
| `actor-required`           | The operation reads the caller, or the realm names a policy and its permissions want someone, and the request authenticated nobody |
| `operation-not-permitted`  | The realm's permissions declined the caller and no policy grant admits the operation |
| `policy-predicate-failed`  | No grant admitted the operation and a policy predicate threw  |
| `conflicting-targets`      | Two members of a parallel group write the same file           |
| `version-conflict`         | A conditional write whose base version had moved              |
| `precondition-unverifiable`| A conditional write the realm could not decide                |
| `payload-too-large`        | Over the realm's ceiling for a card or file                   |
| `wrong-entry-point`        | Reached the operation core with a `query`, or sent a `callApi` in a read-only (`QUERY`) batch |
| `binding-not-approved`     | A `callApi` carrying a credential slot that no approval fills for this caller in this realm (never approved, or its key or grant was removed) — nothing was sent. The key's owner approves it in the secure window ([`api-keys`](../api-keys/SKILL.md)) |
| `share-suspended`          | A slot filled from a workspace's share that is suspended (its owner lost write access, a writer suspended it, or its key was deleted) — nothing was sent; a direct writer resumes it or swaps a key in |
| `binding-needs-reapproval` | The operation sends something other than what was approved for a slot — nothing is sent until its key's owner reviews the change in the secure window |
| `interactive-use-not-approved` | A slotted `callApi` invoked from a card, the assistant or the CLI whose approval is for scheduled pipelines only — nothing was sent. The key's owner can allow it in the secure window's `approve` mode, under **On a schedule and when the card is opened** |
| `credential-rejected`      | The key a `callApi` slot sends can't be used. Either the service rejected it (it answered 401), after which calls with that key to that service aren't sent except a periodic retry; or a key that mints its tokens couldn't get one, and nothing was sent: an OAuth connection or a Google service account (see the Google recipe above), and `err.meta.reason` says why (`rejected`: the key's owner reconnects or replaces it; `needs-admin`: the OAuth client needs its administrator; `unavailable`: try later). Stop polling; see [`api-keys`](../api-keys/SKILL.md) |
| `not-during-render`        | A `callApi` invoked while a card renders — nothing was sent   |
| `guard-refused`            | The realm server refused the `callApi`'s destination: not https, a private address, a request outside its declared destination, or a token endpoint such as Google's, which only the platform calls, so nothing was sent; or a redirect hop that was refused or one too many (the request had already reached the vendor) |
| `upstream-timeout`         | The outside service did not answer in time                    |
| `response-too-large`       | The outside service's response was larger than the realm server carries (10 MiB by default, counted after decompression). The card gets none of the body, never a truncated one; the error's `detail` names the host and the limit, and `err.meta.cap` is the limit in bytes, so ask the service for less (a smaller page, fewer fields) |
| `internal-error`           | Not the caller's — an unreadable definition, a failing executor, a policy that won't load |

An author writes the `assertion-failed` text, so write it as the sentence a user
should read: "That rhythm event is not open, so there is nothing to escalate."

A batch is all-or-nothing, so a refused batch answers one error and no results —
nothing was written, whichever entry was wrong. `OperationsError.entry` says
which: an index at the top level, or a path such as `[2].boxel:operations[0]` to
a member of a group.

`OperationsError.meta` holds the refusal's details a card can branch on, each
only on its own code: `reason` on `credential-rejected` from a key that mints
its tokens, and `cap` on `response-too-large`. It is always an object, so
`err.meta.reason` reads `undefined` rather than throwing on a refusal that has
none, such as a stored key the service answered 401 to. The realm's other
refusal details (which credential slot, the destination, which guard rule
refused it) are not on it; the `detail` sentence names what a user needs. The
type is `OperationsErrorMeta`, from `@cardstack/base/operations`.

```ts
if (err instanceof OperationsError && err.code === 'credential-rejected') {
  this.problem =
    err.meta.reason === 'unavailable'
      ? 'The service is having trouble. Try again in a few minutes.'
      : (err.detail ?? err.message); // names who fixes it
}
```

### Under a realm policy

In a realm that names a policy, what a caller the realm's permissions declined
is told turns on one thing: whether those permissions let them read the realm.
The same table holds through `operations()` (the `_operations` envelope) and
the card+json routes:

| Situation                                              | Caller who may read the realm                    | Caller who may not |
| ------------------------------------------------------ | ------------------------------------------------ | ------------------ |
| No grant holds                                         | 403 `operation-not-permitted`                    | 404 `target-not-found` |
| The target's def type does not carry the operation     | 405 `operation-not-allowed`                      | 404 `target-not-found` |
| No such operation, a declaration with findings, an unresolvable type, nothing at the URL | Its own refusal — 404 `unknown-operation`, 422 `invalid-operation`, 404 `target-not-found` | 404 `target-not-found` |
| A predicate threw and no other grant held              | 500 `policy-predicate-failed`                    | 404 `target-not-found` |
| The policy won't load or compile                       | 500 `internal-error`, "Policy unavailable"       | 500 `internal-error`, "Policy unavailable" |
| A create whose `meta.realmURL` names another realm     | 400 `invalid-params`                             | 404 `target-not-found` |
| A create naming its type by a relative module          | 400 `invalid-params`                             | 400 `invalid-params` |

A caller who may read the realm reaches the policy only by writing — their
reads are the permissions' to allow — so a policy that won't load is a 500 to
them on writes alone. A realm writer never reaches the policy at all.

**A caller who may not read the realm learns nothing about what exists from
the answer.** Every refusal that depends on what the realm holds — the target,
its type, the declaration, a grant, a predicate — resolution failures
included, answers the same bytes a target that isn't there does. A request malformed on its face
(a relative module, a bad envelope) and an unloadable policy are refused as
the table shows.
Over `_operations` that is `title: 'Not found'`, `detail: 'no such target'`,
and nothing of `meta` beyond `meta.entry`; over card+json it is the route's own
not-found. Until a write's grant is decided, anything else the realm would
answer about the write is masked the same way, unless the grant's predicate
holds against the card as stored: a card+json write's 400 for a body it can't
use, its 405, its 412 for a conditional write whose version moved, its 415.
A predicate that throws is hidden from such a caller behind that 404; the
policy's author finds it by explaining the decision, which answers
`predicate-threw` (see
[`realm-policy-authoring`](../realm-policy-authoring/SKILL.md)), or as a
caller who may read the realm, who gets the 500.

**Timing is not concealed.** A target that isn't there is refused before any
grant is matched, while one refused because a matching grant's predicate
didn't hold had that predicate evaluated against it. A caller who measures
carefully can tell the two apart, so the bytes hide which cards exist and the
timing does not.

**Nobody signed in.** On the routes that consume the outcome of the realm's
permissions — the ones a grant can reach — in a realm that names a policy, a
request that authenticated nobody, where the permissions want someone, gets
401 `actor-required` as a JSON:API error, whatever the path names. Elsewhere, and in a realm with no policy, it
gets the realm's plain-text 401 `Missing Authorization header`.

**A relative `adoptsFrom` is refused** with 400 `invalid-params` through
`_operations` for every caller, realm owner included, and through a card+json
`POST` for every caller the realm's permissions decline: a card that isn't
stored yet has no location for a relative module to resolve against. Name the
type by URL or registered prefix.

**A card+json error body carries a status and a title, and no `code`.** Over
those routes the status is the whole answer.

[`realm-policy-authoring`](../realm-policy-authoring/SKILL.md) §13 states the
same refusals from the policy author's side.

## 6. Access posture

**The realm's own read/write permissions come first.** Any caller who can write
the realm can invoke any mutating operation on it, a `nonGrantable` one
included; any caller who can read it can invoke any read the card carries,
except an `explain` or `validate`, which also need read on every other realm
they consult. An operation that failed to lower refuses every caller, realm
writers included: 422 `invalid-operation` for a caller who may read the realm,
and the not-found answer for one who may not (§5). A realm that names a policy is consulted only for what those
permissions declined: everything, for a caller with no permission on the
realm; writes, for one who may read it.

**A policy only widens.** It admits callers the permissions declined, one
operation and card type at a time, and never narrows what the permissions
allow. Writing one is
[`realm-policy-authoring`](../realm-policy-authoring/SKILL.md).

**A caller who isn't signed in is admitted only by a grant that opts in.** For
such a caller `actor()` is `"anonymous"`, and a grant whose `where` names it
(`actor() == "anonymous"`) on an operation, a named one included (never a named
query), admits a visitor, rate-limited and blockable by the grant's own
`rateLimitRequests`, `rateLimitWindowSeconds` and `blocklist`. An anonymous
write is made as the user the grant's `actingUser` expression names. Every
other grant admits signed-in callers alone
([`realm-policy-authoring`](../realm-policy-authoring/SKILL.md) §12).

**A write's predicate is judged under the write lock, against the state before
the write.** The card the grant reads is the one the write changes, as it
stands when the lock is taken — inside a batch, as the entries before it leave
it. So a caller a list admits can take themselves off that list, and a grant
on an operation that writes the list lets whoever it admits put anyone on it:
mark such an operation `nonGrantable` (§2). A create against a type is judged
by the card it would mint, after `fill` and `input` have run; a named create
anchored on an existing card is judged by that card.

**For a caller who may not read the realm, the realm mints every created
card's id.** A chosen path would tell them which paths hold a card. Their
`lid` still links the cards of one batch to each other and comes back beside
the minted id as `{ lid, id }`, but names no file, so a create sent again with
the same `lid` mints a second card. Their card+json `POST` targets the realm
root; one aimed at a directory beneath it answers 404. A caller who may read
the realm names their own cards, as any writer does.

**The card+json verbs reach the built-in behavior only.** For a caller the
realm admits through a grant, a `PATCH` merges and a `DELETE` removes whatever
the type declares under those names, so a type that redeclares `update`,
`create` or `delete` has that verb refused to such a caller, and the grant is
used through `operations()`. A card+json write that side-loads cards in
`included` is refused to them too.

**An `output` projection shapes an operation's answer and nothing more.** A
field left out of one is still reachable through the card's plain read, its
stored source, or a search. A granted `read` serves the card's whole
representation, as the type's `read` declaration shapes it (§2 covers how far
its links reach). A granted `create` or `update` over card+json answers with
the whole card it wrote, unprojected, whatever `read` grant the caller holds,
and a `PATCH` that changes nothing still answers with it.
**Leave a value out because a consumer does not need it, never because a
caller may not have it.**

A card whose buttons carry real consequence should say so in its own visible
text.

## 7. Worked reference

`packages/experiments-realm/clinical/` is a realm driven entirely by named
operations: a program-guarded `transform`, an arithmetic one, a declarative
`assert` over a link collection, a named `create` that links back through
`instance('id')`, an `appendContainsMany` vitals log, base `LogFile`'s `record`
on a linked `.log` audit file, whose `input` program stamps the timestamp and
the actor, a create-and-link `atomic` batch, a parallel transfer across three
cards, and two saved searches rendered through
`@context.searchResultsComponent`.
`packages/experiments-realm/clinical/patient-record.gts` is the file to copy
from.
