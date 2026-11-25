---
name: astrale-cli
description: Reference for the Astrale CLI (binary `astrale`, package `@astrale-os/cli`) - setup, graph reads and mutations, kernel calls, instances, domains, identities, delegation, journals, views, output, debugging, and local storage.
---

# Astrale CLI

`astrale` connects to existing Astrale Kernels. It selects an instance and
identity, performs graph reads and mutations, invokes callables, installs
running domains, reads the Kernel journal, and opens authenticated views.

The rendered command help is authoritative for flags and defaults:

```bash
astrale --help
astrale <command> --help
```

- Binary: `astrale`
- Package: `@astrale-os/cli`
- Runtime: Node 22 or newer; source development defaults to Node 26 and also supports Node 24 and Bun
- Dev entrypoint: `bun cli/bin/astrale.ts <command>`

## Command Surface

Primary commands:

```bash
astrale status
astrale whoami
astrale use <name>
astrale get <target>
astrale query [sources...]
astrale introspect <origin-or-path>
astrale mutate
astrale call <path> [key=value...]
astrale token
astrale logs
astrale view [target-or-view]
astrale ui ...
astrale instance ...
astrale domain ...
astrale identity ...
astrale auth ...
astrale idp ...
astrale admin ...
```

Kernel-touching commands share `--format`, `--json`, `--raw`, `--url`,
`-i/--instance`, `--timeout`, `--as`, `--creds`, `--anonymous`, and `--debug` where
applicable. The CLI creates one public Kernel `Call`, and its Client session owns
remote routing, fresh credentials, and one safe stale-route retry.

`astrale ui` is local project tooling and takes no Kernel, instance, identity,
or credential options, except `astrale ui request`, which is an authenticated
Kernel command and takes the shared Kernel options.

Use `--anonymous` to omit a caller credential even when a local or bookmark-default identity exists.
It cannot be combined with `--as` or `--creds`; required callables reject anonymous requests.

## UI Projects

Astrale UI is one tree-shakeable runtime package plus consumer-owned pattern,
block, and theme source. Initialize a React and Tailwind CSS v4 project with the exact
published UI release:

```bash
astrale ui init --preset astrale
astrale ui search "editable chart with export"
astrale ui request "accessible async combobox with creation"
astrale ui add pattern/chart/line-basic
astrale ui add theme/observatory
astrale ui add ./my-playground-export.css
astrale ui doctor
astrale ui doctor --project ./apps/web
astrale ui preset apply compact
```

Initialization writes Base UI + Nova shadcn configuration, theme and preset CSS
imports, and `astrale-ui.lock.json`. The lock records the exact package version,
Git tag, resolved commit SHA, shadcn version, Base UI version, preset, and hashes
of installed source. Registry metadata, included manifests, and item files are
always read from that single commit snapshot.

Run `astrale ui add` without item arguments for an interactive picker. In CI,
provide canonical addresses explicitly. Ordinary add refuses locally edited
installed files; review those files, then use `--overwrite --yes` only when
replacement is intentional. `--dry-run` leaves project files and the lock
unchanged. Use `astrale ui search <free-text> --json` to receive a short ranked candidate list with
exact demo code and its `command` or runtime `packageImport`.

Use `astrale ui request <free-text>` when search does not satisfy the need. It calls
`/:ui.astrale.ai:function.request` on the selected instance with one bounded intent (1-512
characters) and prints the returned receipt: `{ state: "submitted", requestId, collaborationUrl }`
or `{ state: "pending" | "outcome-unknown" | "failed" | "conflict", requestId }`.

Patterns, blocks, and themes are application-owned source after installation. A
theme is copied to `components/astrale/theme/` and activated through one relative
import in the configured host stylesheet; local playground exports require no
registry fetch or shadcn invocation. Composition root
`className`, inline `style`, controlled values/actions, and stable `data-slot`
anatomy remain open to the host. The package owns reusable runtime behavior;
neither the CLI nor the SDK embeds the UI package or Base UI.

## Paths

Use canonical Kernel Paths:

| Form | Example |
|---|---|
| Domain root | `/:notes.example.dev` |
| Class | `/:notes.example.dev:class.Note` |
| Static callable | `/:notes.example.dev:class.Note:list` |
| Instance callable | `@node-id::notes.example.dev:class.Note.method.archive` |
| Node ID | `@node-id` |
| Active caller shorthand | `@self` |

Static dispatch uses one colon before the method. Instance dispatch uses `::` followed by the complete Domain-qualified Method key.
Discover methods with `astrale introspect <origin> --bundle`. Introspection can use a Class
receiver to inspect an instance contract; calling it requires an observed instance Path.
`@self` is expanded by the CLI before signing when it appears at the head of a
call Path or a bare `key=@self` value. It is not rewritten inside `--data`,
stdin JSON, URLs, or arbitrary substrings.

```bash
astrale get @self --json
astrale introspect /:notes.example:class.Note::notes.example:class.Note.method.archive
astrale call /:blog.example:class.Author:list limit=10
astrale call /:admin.astrale.ai:core.fleet::admin.astrale.ai:class.Fleet.method.listInstances
```

## Instances And Domains

`astrale instance` combines admin-provisioned instances and local bookmarks:

```bash
astrale instance create my-app
astrale instance root import development --yes
astrale instance invite my-app person@example.com
astrale instance invitation status @invitation-id
astrale instance status my-app
astrale instance status staging --bookmarked
astrale instance list --include-retired --admin-only --json
astrale instance use my-app
astrale instance bookmark staging --url https://kernel.example.com
astrale instance forget staging
```

Use explicit `-i <instance>` in scripts. `instance delete` affects an
admin-managed instance; `instance forget` removes only the local bookmark.
`instance status` reports Admin-owned lifecycle by default; add `--bookmarked`
to probe one local bookmark's exact issuer, JWKS, and TLS trust instead.
`instance invite` requires authority to manage the exact Instance and grants
only Instance member access. It returns the durable Invitation immediately;
Admin automatically materializes child Shell access after WorkOS acceptance.
`instance invitation status <id>` performs one read-only observation of the
retained Invitation. `completed` means access is materialized; `accepted`,
`registering`, and `registered` are intermediate states, not completed access.
The command requires the exact Invitation id and does not change its state.
`instance invitation reconcile <id>` is diagnostic recovery, not the normal
invitation journey.
Without a deployed Admin Domain, `astrale instance list` cannot fetch managed
instances (key-backed identities have no Admin token). Use
`astrale instance list --bookmarked`.

Fleet administrators may add `--include-retired` to the ordinary Admin inventory. The default
excludes retired tombstones; included retired Instances use the same output shape and
are identified by terminal `state: "deleted"`. The optional `issuer` is present only when Admin has
retained exact evidence. Unreachable does not mean retired. Add `--admin-only` when local bookmarks
should be omitted from the machine-readable envelope.

`instance create` provisions through the configured Admin Domain with a WorkOS caller; Admin owns
Host placement. Neither `instance create` nor `instance root import` accepts `--host`.

`instance root import <slug-or-id>` retrieves the target owned Instance's root signing identity
through Admin over an end-to-end encrypted, one-use transfer. It imports that identity locally as
`<slug>-root`, not the Admin or Host root identity. Use `--admin <bookmark>` or `--admin-url <url>`
to select another Admin endpoint. Recovery requires `--yes` in automation, replaces an existing
key-backed identity with that name, and refuses to overwrite an IdP-backed identity.

Root import preserves the active instance and keeps the human Admin identity as the Instance
bookmark's default. Select the imported root explicitly with `--as`:

```bash
astrale instance root import development --yes
astrale get @self -i development --as development-root --json
```

Use an authorized human identity for the import; `development-root` is available for subsequent
Instance calls after recovery. Root success proves execution, not an application user's access Policy.

The CLI is connect-only: it does not build or run domains. The SDK's
`astrale-domain` binary owns `dev`, `build`, `deploy`, `lint`, `package`, and test workflows. Project Environments select
exact deployment and optional installation targets; they do not use the CLI's active instance.

`astrale domain install` has two modes:

- Default: install a published catalog origin or URL through the admin control
  plane onto an admin-managed instance.
- `--direct`: call the public Kernel install syscall with a running domain URL.
  This works for any instance you can authenticate to and owns the explicit
  identity-override consent prompt.

```bash
astrale domain install crm.example -i staging
astrale domain install https://crm.example --direct -i staging
astrale domain uninstall crm.example -i staging
astrale domain uninstall app.example shared.example --destructive -i staging
```

A replacement cannot change an installed Domain issuer. If that identity
change is intentional, uninstall the origin first and then install it again.
Uninstall accepts one or more origins and removes the complete selected set atomically, so
dependencies inside that set are allowed. Safe mode is the default and never deletes application
data. `--destructive` deletes application facts whose concrete Class belongs to a selected Domain;
it does not cascade into unselected Domains. Surviving dependents and surviving foreign Edges that
reference selected Nodes still block the complete operation. Type the canonical Domain list
interactively, or pass `--yes` in automation.

Bookmarks retain their own TLS trust (`--ca`). `instance use` probes OIDC and
JWKS with that exact CA. If two bookmarks point to the same normalized URL with
different CA settings, the CLI warns and `instance list --bookmarked --json`
shows each bookmark's `caFile`, issuer, and default identity.

A deployment-only Publication change does not require reinstalling the Domain.
Reinstall only when installation or Schema intent changes.

## Identity And Delegation

`astrale auth login` stores an IdP-backed identity. `astrale identity create`
creates a local key identity. Registration targets an existing Identity Node;
it never creates a Node, changes business properties, assigns a Group, or replaces
the local identity or its keypair:

```bash
astrale identity create alice
astrale identity register alice \
  --node @existing-user-id \
  -i staging
```

The Kernel assigns Node IDs. They are returned by reads and creation results
and can be reused through the `@node-id` Path form; do not derive application
meaning from their contents. The primary self credential is signed for the target
Kernel audience. Register checks the caller's authority on the existing Node.
When a Domain callable supplies that authority, optionally name it with `--via`;
the CLI sends the same request and verifies the returned Node and Authentication.
No Domain callback is required when the direct caller already has authority:

```bash
astrale identity register operator \
  --node @existing-operator-id \
  --via /:operations.example:function.registerOperator \
  -i staging
```

`astrale token` issues an audience-bound credential for the selected authenticated identity. When
the audience is the target Kernel issuer (the default), it mints a top-level Grant credential that
can be reused with `--creds`. A different `--audience` creates a delegated service envelope for that
receiver instead. TTL defaults to 240 seconds so ordinary tokens remain short beneath the one-hour
local operator proof; an explicit TTL still cannot outlive the selected source credential. Use
`--raw` for shell assignment.

```bash
TOKEN=$(astrale token --raw -i staging)
astrale call /:notes.example:class.Note:list --creds "$TOKEN" -i staging
```

`astrale auth token` is different: it prints the cached upstream IdP token.

## Graph Reads

### `get`

`get` reads one exact canonical Node:

```json
{ "id": "node-id", "class": "notes.example:class.Note", "props": {} }
```

The structured Node result is exactly `{ id, class, props }`.

```bash
astrale get @note --json
astrale get /:notes.example:class.Note
astrale get /:kernel.astrale.ai --schema
```

Method Paths identify callables rather than Nodes; use `call` to invoke them or
`introspect` to inspect their Schema. Schema-valued properties are omitted
unless `--schema` is passed.

### `introspect`

`introspect` reads the Kernel Schema syscall for one installed Domain.

```bash
astrale introspect kernel.astrale.ai
astrale introspect /:kernel.astrale.ai --bundle
astrale introspect /:kernel.astrale.ai:class.Identity:whois
astrale introspect @note::notes.example:class.Note.method.archive
```

A method or Function Path projects its input/output from the installed bundle.
An instance Method's qualified key selects the schema even with an `@id` receiver;
introspection neither reads nor invokes that receiver. A bare `@id` has no schema origin.

### `query`

`query` executes canonical `astrale.graph.query/v6`. Its structured result is
`{ kind: "graph", graph: { nodes, edges }, page?: { next } }`; pass the opaque
`page.next` value to `--cursor` until it is absent.

- Positional Paths create Path source terms.
- `--class <path>` selects Nodes implementing one exact Class.
- `--edge <class>` adds one exact expansion; direction is `outgoing`,
  `incoming`, or `incident`.
- `--limit` is finite and defaults to 100.
- `--cursor` resumes the same caller-bound query scope.
- `--ast` and `--file` admit a complete canonical Query V6 document.

```bash
astrale query /:notes.example:class.Note --limit 50 --json
astrale query --class /:notes.example:class.Note --limit 50 --json
astrale query @note \
  --edge /:notes.example:class.references \
  --direction outgoing --limit 25 --json
astrale query --file query.v6.json --cursor "$CURSOR"
```

Use `query` with `--edge` for an exact neighborhood.

## Mutations

`astrale mutate` accepts canonical `astrale.graph.mutation/v3` or its exact
`{ preconditions, operations }` authoring input from `--data`, `--file`, or
stdin. The transition is atomic. `--dry` admits and prints the canonical
document without opening a Kernel connection. The result is `{ createdNodes }`.

```bash
astrale mutate --file mutation.v3.json --dry
astrale mutate --file mutation.v3.json
```

## Calls

`astrale call` creates one Path-targeted Call. Input priority is `--data`,
`key=value`, piped stdin, then `{}`. `--dry-run` admits the Path and prints
the call input. Value, binary, and stream results are handled explicitly, and
`--output` writes binary data. A streaming binary is drained with backpressure
while the command-scoped Client session is live, then presented through the same
raw/file/JSON paths as buffered binary. JSON preserves application status and
encodes the body as text or base64. Callable input/output is
`astrale introspect <path>`.

```bash
astrale call /:blog.example:class.Author:list limit=10
astrale call /:blog.example:class.Author:create \
  --data '{"name":"Ada"}' --json
astrale call /:assets.example:class.Asset:render id=123 --output asset.png
```

Top-level `key=value` values coerce booleans, null, numbers, arrays, and
objects. Use `--data` for nested or digits-only string values.

## Journal

`astrale logs` reads the public Kernel journal syscall and returns
`{ records, cursor? }`. Filters match exact values; use `--topic-prefix` for
prefix matching:

```bash
astrale logs -i staging --limit 50
astrale logs --topic op:function.failed
astrale logs --topic-prefix op:function. --follow
```

Use `--principal`, `--since`, `--until`, or an opaque `--cursor` as needed.
`--follow` retains one Client session and advances only with returned cursors.
Structured output retains the admitted `correlation` object, including invocation root and
parent identifiers, and includes `correlationId` as a projection of `invocationId`.
With `--json`, `--follow` emits NDJSON with one complete admitted record per line; combining
`--format yaml` with `--follow` is rejected.

## Views And Browser Sessions

`astrale view` opens one resolved View through a local browser shell:

```bash
astrale view @customer --list
astrale view @customer --snapshot
astrale view /:crm.example:view.dashboard --target @customer
astrale view --sessions
astrale view --close <session-id>
```

`astrale browser` prepares a persistent authenticated GUI browser profile.
Use `astrale browser --check` to verify it, then drive the printed profile with
`agent-browser`.

## Output And Automation

- TTY defaults are human-readable.
- `--json` emits one JSON document for finite commands; `logs --follow` emits an NDJSON stream.
- `--raw` unwraps scalars and writes raw binary bytes.
- `--format yaml|json` selects finite structured rendering; `logs --follow` supports JSON/NDJSON only.
- Use `--ci --no-prompt` for automation.
- Use explicit `-i`, `--as`, and `--timeout` rather than ambient state.
- Pipe large JSON through stdin; command-line argument size is limited by the
  operating system.

## Debugging

Start with:

```bash
astrale status
astrale instance active
astrale auth status
astrale whoami
```

Add `--debug` for full Kernel error diagnostics. Missing and authorization-masked
Nodes are intentionally indistinguishable. A Path also needs access to its
intermediate nodes and edges: an observed Node may be readable by `@id` or a
Class query while its Domain-rooted Path is unavailable. Check `-i` and `--as`;
this alone does not prove corrupt data. Use `introspect` for callable schemas.

## Storage

State lives under `ASTRALE_HOME`, or `~/.astrale` by default:

```text
config.json
instances.json
identities.json
idps/
idp-sessions/
keys/
browser.json
browser/
```

Optional roots are `ASTRALE_HOME`, `ASTRALE_KEYS_DIR`, and
`ASTRALE_DATA_DIR`.

## Source Map

- Entry: `cli/bin/astrale.ts`
- Program and shared options: `cli/src/program/`
- Public Kernel connection boundary: `cli/src/connection/`
- Query/Mutation document preparation: `cli/src/graph/`
- Commands: `cli/src/commands/`
- Shared presentation and local stores: `cli/src/lib/`
- Studio bridge: `cli/studio/server/`
- Tests: owner-local `__tests__/` directories
