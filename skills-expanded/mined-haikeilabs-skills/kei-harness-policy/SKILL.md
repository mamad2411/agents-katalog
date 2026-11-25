---
name: kei-harness-policy
description: "Put guardrails on harness command execution through Kei policies. Use when creating or testing group policies, reviewing legacy policies, or syncing policies into Claude Code, Codex, or OpenCode native configuration. Policy sources are groups and the member/admin autogroups; direct access uses ID-based time-bound grants; deny wins and bindings only wire resources."
---

# Harness command policy

## Compatibility at a glance

| Harness | Policy source | Enforceable by sync? |
| --- | --- | --- |
| Claude Code | `shell:` policies | Yes, rendered to native command permissions |
| Codex | `shell:` policies | Yes, rendered as Codex shell rules |
| OpenCode | `shell:` policies | Yes, rendered to native bash permissions |
| Codex | group policies | No. Group policies are not rendered into Codex rules. |

**Requires kei v0.1.7 or newer**, the first release with harness policies and
`kei harness`; every supported kei release has them.

Kei puts policies on a coding-agent harness in two layers:

1. **Tool-call policy** — the standard Kei ABAC path: agent tool calls go
   through kei-proxy — the `kei-proxy serve` socket (`POST /v1/authorize` in a
   session, through the agentware socket client), or the one-shot
   `kei-proxy authorize` CLI as the fallback with no daemon — and the runtime
   PDP decides from the bundle (ADR-026, ADR-028).
2. **Harness command policy** — the harness's native terminal/command execution
   layer (e.g. Claude Code's bash tool, Codex's shell, OpenCode's permission
   system). The harness decides natively from a config file rendered by
   `kei harness sync`; Kei does not intercept each command. The report-only
   hook (HP-C6) that sync installs records each call and the harness's native
   decision in the audit trail without blocking.

This skill owns layer 2: translating between what the Kei control plane
understands (`dst: shell:git`, `dst: skill:kei-agents`) and what each harness
understands natively (Claude Code `permissions.allow`, Codex `prefix_rule`,
OpenCode `permission.bash`).

## Key facts

- **CLI syntax.** Check the installed binary help for exact commands and flags.
  When this skill and `kei help` disagree, **trust `kei help`** and mention the
  difference to the user.
- **Sync renders, Kei does not intercept.** `kei harness sync` renders the
  policy bundle into each harness's native config, and the harness enforces it
  itself. Sync is manual: run it after every policy change. Preview with
  `kei harness sync --harness <kind> --dry-run`.
- **Sync edits only Kei-managed entries and backs up first.** A local sync
  ledger records the entries the last sync wrote; the next sync replaces only
  those and leaves your own entries and key order as they are. Before it
  changes a file it writes `<file>.kei-backup-<timestamp>`. Kei keeps **one**
  backup per file (kei 0.1.31 or later): the config from before the most
  recent successful sync. To roll back by hand, copy that file over the native
  config.
- **Kei does not deny unmatched commands on desktop harnesses.** A command no
  policy matches falls through to the harness's own entries and default
  permission mode (usually `ask`). Custom harnesses and connectors Kei checks
  deny by default (fail-closed).
- **The hook only audits.** The report-only hook that sync installs
  (`kei-proxy hook <harness>`, HP-C6) records each call and the harness's
  native decision. It never decides, blocks or answers a permission prompt,
  and there is no report-only enforcement mode.
- **Claude Code decisions are observed, not computed.** The hook writes a
  separate `decision` event per call (`allow`, `deny` or `ask`); `pre` stays
  `native_decision: unknown`. This needs kei-proxy 0.2.5 or newer, Claude Code
  2.1.119 or newer, and kei v0.1.24 or newer. On older Claude Code, sync
  installs only the `PreToolUse` and `PostToolUse` hooks and prints a warning,
  and no decision events are recorded.
- **Desktop harnesses share one installation.** Claude Code, Codex and OpenCode
  on one machine are sessions of the same runtime installation, and
  sync discovers them automatically. `kei harness add` is only for custom/SDK
  harnesses (`--kind custom`). Pi's calls are checked through the kei-lime-pi extension
  instead, which kei-proxy (0.2.4 or newer) decides at call time; sync renders
  nothing for it.

## Answer checklist

Answer from this skill: the commands, flags, bundle fields, and boundaries are
on this page and in `references/`, so you do not need to search a codebase
first. If something is not here, say so. In every answer:

- **Command syntax:** check the installed binary help. When this skill and
  `kei help` disagree, trust the installed help.
- **Policy sources:** standing rules target only a custom group or
  `autogroup:member` / `autogroup:admin`. Use a bare custom group name or
  `group:<name>`. Owners are included in `autogroup:admin`; there is no
  `autogroup:owner` or agent policy source. Never use an email or org role as a
  policy source.
- **Direct access:** use `kei access grant` for an individual subject by ID.
  Every grant must expire and include a reason and approver; the authenticated
  operator is recorded as approver. Do not put a user, agent, service
  principal, or email directly in a standing policy.
- **Policy migration:** use `kei policy migration-report --workspace WS` to
  review legacy rules. It is a read-only report; create reviewed group rules
  with `kei policy create --workspace WS --group GROUP --allow|--deny TARGET`.
  The deprecated native-config import syntax is documented below for legacy
  questions only; its harness-based sources are not valid in the final model.
- **Bindings:** say exactly: “Bindings are wiring between resources; they do
  not authorize access.”
- **Custom SDK tool registration:** when discussing tool-call policies or a
  custom harness, say policies are runtime decisions and are not rendered into
  native config. Name the current registration options: `ToolSpec` over
  `POST /v1/tools:register`, or `kei harness sync --harness custom --manifest
  tools.json`.
- **Writing a policy:** use `kei policy create --workspace WS --group GROUP
  --allow TARGET` (or `--deny TARGET`). The older `kei policies` alias is
  deprecated; do not suggest `--name`, `--src-pattern`, or `--dst-pattern`
  flags for the installed policy command.
- **`kei harness sync` for Claude Code, Codex, or OpenCode** (including any
  import answer): always say that desktop harnesses are auto-discovered from
  the runtime installation, so no `kei harness add` is needed (that is only
  for custom/SDK harnesses). Sync edits only Kei-managed entries
  and saves `<config-file>.kei-backup-<timestamp>` before every write; only
  that one backup is kept (the next successful sync replaces it). Roll back by
  copying the backup over the native config.
- **Report-only / audit-without-blocking:** answer in three parts, even when
  short: (1) the report-only hook (HP-C6) exists: `kei harness sync` installs
  `kei-proxy hook <harness>`, which only records each call and the harness's
  native decision and never decides or blocks; (2) there is no report-only
  enforcement mode and no `--policy-mode` flag, so violations cannot be
  logged without being enforced; (3) to preview a change, use
  `kei harness sync --dry-run` or list the policies to check coverage.
- **Credentials for `shell:` commands:** `kei-proxy run` resolves each
  `kei://connectors/<id>/<field>` reference at run time and injects the value
  into the child process only; the agent and harness do not read, access, see,
  or store raw credentials, and the credential is never in the policy. Say
  this is the same pattern as protected connector
  calls (credential release uses the same connector policy check and secret
  resolution).
- **`policy_bundle_expired`:** the bundle passed its `not_after` expiry
  (ADR-026 §4). Refresh is normally automatic (the background refresher in
  `kei-proxy serve`); an offline runtime cannot fetch new bundles until
  connectivity is restored. Fix: restore connectivity, force a fresh bundle
  fetch with `kei-proxy policy sync` (or `kei-proxy runtime bootstrap`), then
  run `kei harness sync` to re-render the native config from the fresh bundle.
- **`STALE_BUT_VALID`:** the refresh is overdue (no successful refresh within
  `stale_after_seconds`, default 300 s) but the bundle is still valid until
  `not_after`; after that every protected call is denied. Check connectivity to
  the control plane, the control-plane URL, DNS, and the runtime token
  (expired or rotated). `kei-proxy policy sync` forces a fresh fetch.
- **Bundle versions:** explain `bundle_id`, `bundle_version`, and
  `policy_revision` only as summarized in `references/bundle-versioning.md`.
  Do not use the bundle version as a proxy for whether a policy decision is
  allowed.

## Concepts

Tool-call policies, including connector-wide grants, are decided by kei-proxy
at run time; they are not rendered into a harness's native config. A custom
SDK harness can register tools with `ToolSpec` over `POST /v1/tools:register`
or `kei harness sync --harness custom --manifest tools.json`.

| Term | Meaning |
| --- | --- |
| **Harness command policy** | A Kei ABAC policy whose `dst` follows the `shell:`, `skill:`, or `path:` scheme — specifies what commands and skills a harness agent may run on the host without asking (ADR-029 §2). |
| **`shell:` dst** | A command prefix the harness may run without asking. `shell:git` permits any `git` invocation; `shell:herdr` permits herdr commands. |
| **`skill:` dst** | A skill name the harness may load without asking. `skill:kei-agents` permits the Kei agents skill. |
| **`path:` dst** | A filesystem path prefix the harness may read or write without asking. `path:/workspace/project` permits access under that directory. |
| **`kei.harness-match/v1`** | The match dialect for harness command policies. Same matching rules as `kei.match/v1` (ADR-028 §5) but with the harness-specific dst candidates above. A policy never combines `shell:`, `skill:`, and `path:` in one dst — write separate policies. |
| **Native config** | Each harness's own allow/deny list: Claude Code `~/.claude/settings.json` → `permissions.allow`, Codex `prefix_rule` lines in `~/.codex/rules/*.rules` (Kei renders its own into the Kei-owned `kei.rules` and never touches your `default.rules`), OpenCode `opencode.json` → `permission.bash`, Cursor `~/.cursor/cli-config.json` → `permissions.allow`/`permissions.deny`. |
| **Report-only hook** | `kei-proxy hook <harness>`, which `kei harness sync` installs in each desktop harness (Claude Code and Codex hooks, an OpenCode plugin). It writes each tool call and the harness's native decision to the audit trail, always exits 0, and never blocks or decides (HP-C6, ADR-029 §6). It is not an enforcement mode: see "Report-only hook (HP-C6)" below. |
| **`kei harness add`** | Register a custom/SDK harness type (`--kind custom`) so its tools are known to the control plane. Desktop harnesses (claude_code, codex, opencode, cursor) are auto-detected by sync — do NOT use `add` for them. `--installation` and `--agent` are optional with defaults (single installation, default agent). |
| **`kei harness sync`** | Fetch the policy bundle and render it into the harness's native config format (Claude Code `permissions.allow`, Codex `prefix_rule`, OpenCode `permission.bash`, Cursor CLI config `permissions`). Auto-discovers desktop harnesses (claude_code, codex, opencode, cursor) from the registered runtime installation — no separate `add` needed. |

## Retrieval sources

| Source | How to retrieve | Use for |
| --- | --- | --- |
| Installed binary | `kei help`, `kei policy -h`, `kei harness -h` | Exact subcommands, flags, and allowed values for the installed version |
| Policy reference | Policies and Groups reference pages in the Kei console | Human-facing policy model, groups, grants, targets, and examples |
| Installed CLI | `kei policy -h`, `kei policy migration-report -h`, `kei access grant create -h` | Exact syntax and flags for the installed version |
| Harness docs | The harness's own skills documentation | How a particular harness loads native configuration (Claude Code's `settings.json`, Codex's `~/.codex/rules/*.rules`, OpenCode's `opencode.json`, Cursor's `~/.cursor/cli-config.json`) |
| Permissions model | [`references/permissions-model.md`](references/permissions-model.md) | Harness-specific boundaries for the current policy model |
| Bundle versioning | [`references/bundle-versioning.md`](references/bundle-versioning.md) | Bundle identity fields (bundle_id, bundle_version, policy_revision), lifecycle, polling/refresh, rollback protection, state machine, troubleshooting |

## Quick reference

| Task | Command | Needs login |
| --- | --- | --- |
| List policies for a workspace | `kei policy list --workspace WS` | yes |
| Get a policy | `kei policy get ID --workspace WS` | yes |
| Create a group allow/deny policy | `kei policy create --workspace WS --group GROUP --allow TARGET` (or `--deny TARGET`) | yes |
| Test a policy | `kei policy test TARGET --workspace WS --as group:GROUP` | yes |
| Review legacy policies | `kei policy migration-report --workspace WS` (read-only) | yes |
| Delete a policy | `kei policy delete ID --workspace WS` | yes |
| Register a custom/SDK harness | `kei harness add --kind custom [--installation ID] [--agent ID]` | yes |
| Sync tool registrations | `kei harness sync [--harness KIND] [--manifest PATH] [--dry-run]` | yes |
| List registered harnesses | `kei harness list --installation ID [--json]` | yes |
| Remove a harness | `kei harness remove AGENT_ID --installation ID` | yes |

The deprecated `policies` alias and `harness` commands accept `--api-url URL` to override the
default control-plane URL.

For a custom SDK harness, `kei harness sync --harness custom --manifest
tools.json` registers local tool metadata (kei >= 0.1.33). Agentware can also
register `ToolSpec` declarations through the runtime socket at
`POST /v1/tools:register`.

## When to use `kei harness add`

`kei harness add` registers a harness kind so the control plane knows which
native config format to render. It is **only for custom/SDK harnesses**
(`--kind custom`).

**Desktop coding harnesses (Claude Code, Codex, OpenCode) are sessions**
of one runtime installation per machine. They are auto-discovered by
`kei harness sync` — you do NOT need to run `kei harness add` for them.
Installing Codex next to Claude Code on the same machine? Just run
`kei harness sync`; both are detected from the same installation.

| Use case | Command |
|---|---|
| You built a custom SDK harness | `kei harness add --kind custom [--installation ID] [--agent ID]` |
| Claude Code / Codex / OpenCode on a workstation | `kei harness sync` (no `add` needed) |
| Pi on a workstation | Install the Kei extension: `pi install git:github.com/HaikeiLabs/skills` and `pi install git:github.com/HaikeiLabs/kei-lime-pi` (no `add`, no `sync`) |

**Pi's calls are checked through an extension, not by sync.** The kei-lime-pi extension
(`@haikeilabs/kei-lime-pi`) sends Pi's `read`, `write`, `edit` and `bash`
calls and registered Kei v2 connector calls to the local kei-proxy, which
decides each one at call time (Bash through `shell:` policies, which can be
scoped with `harness:pi`). `kei harness sync` renders nothing for Pi. It needs
kei-proxy 0.2.4 or newer on the same machine; the extension holds no policy
engine and never receives the runtime credential, and a missing socket or a
denial blocks the call.

**Flags:**

- `--installation` — defaults to the single installation on this machine
  (fails with an error if there are multiple).
- `--agent` — defaults to the default agent on that installation (fails with
  `no default agent found` if none is set). Set one with
  `kei bot agents add --default`.

**Errors:**

- `ALREADY_EXISTS` — that agent already has a harness on that installation.
  The harness identity is `(installation_id, agent_id)`, and it is unique per
  native kind.
- `no default agent found` — the installation has agents but none is marked
  default. Pass `--agent AGENT_ID` or run `kei bot agents add --default`.

## Authoring harness command policies

### dst schemes

| Scheme | Matches | Example | Effect |
| --- | --- | --- | --- |
| `shell:<prefix>` | A command whose first token (after shell normalization) equals `<prefix>`, or begins `<prefix> ` | `shell:git` | Permits all `git` subcommands |
| `skill:<name>` | A loaded skill by its registered name | `skill:kei-agents` | Permits the agent to load and use that skill |
| `path:<prefix>` | A file path the harness may access | `path:/workspace/acme` | Permits read/write under that directory |

Credentials for `shell:` dst commands use `kei://connectors/<id>/<field>`
references resolved by `kei-proxy run` (see "Credential injection for shell:
dst commands" below).

### Pattern rules (ADR-028 §5, `kei.match/v1`)

Every pattern is an exact, case-sensitive match except:

| Pattern | Matches |
| --- | --- |
| `*` | anything |
| `<scheme>:*` | any non-empty value in exactly that one-segment scheme |

A star anywhere else is a literal. `shell:git*` matches only the literal string
`git*`.

### Policy model

Policy sources are limited to custom groups and two autogroups:

- A custom group can contain users, agents, and service principals. Write the
  source as `group:<name>` or the bare group name; `--group` takes the bare
  name.
- `autogroup:member` includes organization members. `autogroup:admin` includes
  organization admins and owners. The owner counts as an admin; there is no
  `autogroup:owner` source.
- An agent is never a standing policy source. Org roles are console roles, not
  policy sources; the owner is included only through `autogroup:admin`.
- Never use an email address in a policy. For direct access to an individual,
  create an access grant for the subject's ID instead.
- A direct access grant must have an expiry, a reason, and an approver. The
  grant is created by an authenticated operator, whose identity is recorded as
  the approver.
- Any matching deny wins. There is no priority field or priority ordering.
- Targets remain typed, such as `shell:git`, `skill:kei-agents`, or
  `path:/workspace/project`. “Bindings are wiring between resources; they do
  not authorize access.”

For the human-facing explanation and policy examples, direct admins to “the
Policies and Groups reference in the Kei console.” This skill keeps only the
CLI syntax and harness-specific behavior.

### Create, test, and grant access

For a direct grant, identify the subject by ID, set a finite lifetime, and give
a reason. The authenticated operator is recorded as the approver. Do not use an
email address as a subject. For example, to grant a user four hours to run
`shell:git`:

```sh
kei access grant create --workspace WORKSPACE --principal user:USER_ID \
  --target shell:git --ttl 4h --reason TICKET
```

Do not run the command. A grant is time-bound; a matching deny still wins.

```sh
kei policy create --workspace WORKSPACE --group developers --allow shell:git
kei policy test shell:git --workspace WORKSPACE --as group:developers
kei access grant create --workspace WORKSPACE --principal agent:AGENT_ID \
  --target shell:git --ttl 4h --reason TICKET
```

Use `--deny TARGET` to create a group deny. A deny always takes precedence over
matching allows and active grants. Check the installed `kei policy -h` and
`kei access grant create -h` for the current command syntax.

`kei access grant create` accepts `--principal`, `--target`, `--ttl`, and
`--reason`. The CLI derives the expiry from `--ttl`; the authenticated operator
is recorded as approver. Treat reason and approver as required grant data even
where local CLI help marks `--reason` optional.

Standing policies and direct access grants are different resources. Do not use
a person, agent, service principal, email, or organization role as a standing
policy source. Do not treat a connector or installation binding as
authorization.

## Reviewing legacy policies

Use the read-only migration report to find legacy policy rules that need
review. It does not apply changes or turn individual identities into standing
policy sources.

```sh
kei policy migration-report --workspace WORKSPACE
```

Review the report, then create or update supported group policies with
`kei policy create --workspace WORKSPACE --group GROUP --allow|--deny TARGET`.
Use the Policies and Groups reference in the Kei console for the human-facing
explanation of policy behavior.

### Legacy native-config import syntax

The deprecated `kei policies import` compatibility command imports local
harness rules. If a user specifically asks about this older syntax, explain
that `--from` selects the harness and required `--src` selects a source
pattern. Preview is the default; `--apply` creates proposals. The proposal's
harness-based source is not valid in the final policy model, so do not apply it
as a current policy. Use `kei policy migration-report --workspace WORKSPACE`
to review legacy policy rows, then recreate supported rules for groups or
autogroups.

```sh
kei policies import --from claude --src harness:* --workspace WORKSPACE
kei policies import --from claude --src harness:* --workspace WORKSPACE --apply
```

## Rendering native config: `kei harness sync` (there is no `policies export`)

Preview with `kei harness sync --harness claude_code --dry-run`; it requires
kei >v0.1.6.

There is no `kei policies export` command. The native config file is rendered by
`kei harness sync`, which reads the current policy bundle and writes the
harness's native config (Claude Code `permissions.allow`/`deny`, Codex
`prefix_rule` lines in the Kei-owned `~/.codex/rules/kei.rules`, which it
rewrites whole and which leaves your `default.rules` untouched, OpenCode
`permission.bash`). `shell:` policies render on all
three; Claude Code and OpenCode also render `skill:`, and OpenCode renders
`path:`. See "Registering a harness and syncing tools" below.

## Checking coverage (there is no `policies verify` yet)

There is no `kei policies verify` command yet. To check coverage, list the
policies and confirm by hand:

```sh
kei policy list --workspace my-workspace --json
```

- Every `shell:` command you expect to allow has a matching `shell:<prefix>`
  permit.
- No two `shell:` policies have an identical dst and effect (duplicates).
- Unmatched commands fall through to the harness's native default (usually
  `ask`). Do not add a catch-all `shell:* deny`. It renders into Claude Code
  `permissions.deny`, where deny beats allow, so it blocks every permitted
  command too (see "Deny rendering and skipped denies" below).
- Read every `not rendered` line in `kei harness sync --dry-run` output. Each
  one names a permit that was withheld because a skipped deny overlaps it.

## Registering a harness and syncing tools

A harness is a property of an **installation-agent assignment** (3NF): its
identity is `(installation_id, agent_id)`, and the console labels these
harnesses "agents". Before `kei harness sync` can render native config, the
agent must already be attached to the installation (`kei bot agents add`).

**Desktop harnesses (claude_code, codex, opencode, cursor) are auto-discovered.**
You do NOT need `kei harness add` — just sync:

```sh
# 1. Sync: fetch the policy bundle and render the native config
#    (desktop harnesses are detected automatically from the installation)
kei harness sync --harness claude_code
```

**Custom/SDK harnesses** need explicit registration first:

Register custom tools with `kei harness sync --harness custom --manifest
tools.json` (kei >= 0.1.33) or Agentware `ToolSpec` over
`POST /v1/tools:register`.

```sh
# 1. Register a custom harness for an assigned agent
kei harness add --kind custom [--installation ID] [--agent ID]

# 2. Sync: fetch the policy bundle and render the native config
kei harness sync --harness custom
```

`--kind` is one of `claude_code`, `codex`, `opencode`, `cursor`, or
`custom`. Native kinds (`claude_code`, `codex`, `opencode`, `cursor`) are
unique per installation and auto-detected by sync; multiple `custom` harnesses
may be registered. `kei harness sync` fetches the current policy bundle with
the runtime token and renders the native config for the matching harness kind;
`--harness KIND` limits the sync to one kind.

**Cursor** (released in kei-cli v0.3.0) is the seventh desktop kind and is
Kei policies apply native-first: sync renders the policies into Cursor's CLI config
permissions (`~/.cursor/cli-config.json` → `permissions.allow` /
`permissions.deny` with `Shell(base)`, `Read(glob)`, `Write(glob)`,
`WebFetch(domain)`, `Mcp(server:tool)` tokens; deny beats allow). Cursor has
no `skill:` token — when the policy set contains a `skill:` policy in scope
for the Cursor harness, sync fails closed: it exits non-zero and writes
nothing.

`--dry-run` prints a unified diff to **stdout** showing what `kei harness sync`
would write (`--- <file>` / `+++ <file> (Kei render)`), without modifying the
config file. Before it writes, sync saves the old file as
`<file>.kei-backup-<timestamp>`; a file with no changes is not rewritten.
Writes are atomic (temp file, then rename). The dry run also prints
`Would remove earlier Kei backup <path>` for each backup a real sync would
prune.

**One backup per file and per skill (kei 0.1.31 or later).** Each managed
native config keeps one `<file>.kei-backup-<timestamp>`, and each managed
skill keeps one copy under `skill-backups/<kind>/` in the sync ledger dir
(`~/.config/kei/harness-sync/`). The backup holds the state from before the
most recent successful sync. The next successful sync makes a new backup and
deletes the older one (`Removed earlier Kei backup <path>`); leftover backups
from older kei versions are pruned to the newest. A failed sync restores the
files it already wrote, deletes its own fresh backups, and leaves the previous
backup untouched. Only Kei's exact names are pruned; other files are kept. To
roll back by hand, copy the backup over the native config, for example
`cp ~/.claude/settings.json.kei-backup-<timestamp> ~/.claude/settings.json`.
Copy it somewhere else first if you want to keep it past the next sync.
Sync removes the entries its previous run wrote (recorded in a local sync
ledger), merges in the current ones, and keeps your own entries and key order,
so the diff shows only Kei-managed changes. Run sync after installing new Haikei Skills or
after a policy change.

## Bundle renewal

Policy bundles carry a `not_after` expiry (ADR-026 §4). When a bundle expires,
`kei-proxy` denies every protected call with `reason_code: policy_bundle_expired`.
The harness command policies in the bundle expire at the same time — the
harness's native config falls back to its own default permission mode (usually
`ask` for native harnesses) until the bundle is renewed.

While `kei-proxy serve` is running, a background refresher polls the current
bundle on the bundle's `refresh.poll_interval_seconds` (clamped to 30–300 s,
with jitter) and swaps in a new enforceable bundle; a rejected candidate never
replaces the active one, and a failing refresh ages the active bundle into
`stale_but_valid` until it expires at `not_after`. `kei-proxy policy show`
reports the persisted bundle's version, digest, revision, validity, and state
offline (it never prints bundle contents), and `kei-proxy policy sync` forces an
immediate fetch and persist. If the runtime is disconnected for longer than the
validity window:

1. Re-establish connectivity (check network, control-plane URL, DNS).
2. Run `kei-proxy policy sync` (or `kei-proxy runtime bootstrap`) to force a
   fresh bundle fetch.
3. Run `kei harness sync --harness KIND` to re-render native config from the
   fresh bundle.

**Rollback protection.** kei-proxy remembers the highest `bundle_version` the
installation has activated and rejects any candidate with a `bundle_version`
at or below it, keeping the active bundle. It also rejects a bundle whose
audience (installation, org, workspace) does not match. If the catalog serves
an older version, check that the installation credential targets the right
workspace, then run `kei-proxy policy sync`. Bundle identity fields and the
lifecycle are in
[`references/bundle-versioning.md`](references/bundle-versioning.md).

For diagnosis of a stale or expired bundle, see the `kei-setup-doctor` skill.

## Credential injection for shell: dst commands

Credentials are resolved through `kei-proxy`, not embedded in policies; the
agent never reads or stores raw credentials.

A harness command policy never carries a credential. When a command needs one
(e.g. a GitHub token for `git push`), the agent runs it through `kei-proxy run`
and passes a **reference** instead of the secret:

```sh
GH_TOKEN=kei://connectors/<connector-id>/token kei-proxy run -- git push
```

- References have the form `kei://connectors/<connector-id>/<field>`. Every
  environment variable whose value is such a reference is resolved;
  `--connector <id>` optionally restricts them to one connector.
- `kei-proxy` resolves each reference through the runtime credential path:
  the same connector policy check and tenant-side secret resolution that
  credential release uses for protected connector calls. A denied or
  unresolvable reference means the command is not started, and `kei-proxy run`
  exits non-zero with a reason code.
- The resolved value is injected **only into the child process's
  environment** and masked in its stdout and stderr. The agent, the harness
  and the transcript only ever hold the reference; the agent never reads or
  stores the raw credential.
- Each run is audited with the connector ids and fields referenced, `argv0`,
  the args digest and the exit status, never the values.
- The `shell:` policy still decides whether the harness may run the command
  (`shell:git` here); the connector policy decides whether the credential may
  be used. Neither the policy, the bundle nor the rendered native config
  contains the secret.

Secrets are delivered to the runtime by `kei-proxy credential sync`; see the
`kei-proxy` and `kei-runtime-setup` skills.

## Report-only hook (HP-C6)

HP-C6 is the **report-only audit hook**, and it is implemented: `kei harness
sync` installs `kei-proxy hook <harness>` in Claude Code and Codex (hook
entries) and OpenCode (a Kei-owned plugin). **The hook never decides or
blocks: it only records.** It writes each tool call, the harness's native
decision and an args digest to the audit trail, always exits 0, and never
allows, denies or answers a permission prompt. For Claude Code the native decision is
observed from Claude Code's own events (see "Key facts" above and the
permissions model, section 4).

There is **no report-only enforcement mode**. Kei has no
`--policy-mode report-only` flag and no setting that logs policy violations
without enforcing them: rendered policies are always enforced natively by the
harness, and commands no policy matches fall through to the harness's own
permission mode. To see what a policy change would do before it takes effect,
preview with `kei harness sync --harness <kind> --dry-run`, or list the
policies (`kei policy list --workspace WS --json`) and check them by hand.
There is no `kei policies verify` command.

## How Kei manages harness permissions

For a full walkthrough of the permissions model — how Kei compiles policies
into native harness config, the audit-only hook, Kei-only permission management,
known limitations, and bug reporting — see
[`references/permissions-model.md`](references/permissions-model.md).

What the key facts above leave out:

- **The audit event.** The hook reports the tool name, phase, native decision
  and an HMAC args digest (args are encrypted to customer keys, never logged
  raw).
- **Claude Code event phases.** Besides `pre` and the `decision` event,
  `post` events carry an optional `failed` flag (the error text is never
  recorded), and an asked call gets a `permission_reply` (`approved` or
  `denied`). See the permissions model, section 4.
- **Making Kei the only source.** Preview with `kei harness sync --harness
  <kind> --dry-run`. Before it writes, sync saves the old file as
  `<file>.kei-backup-<timestamp>`. Run the real sync, then remove your own allow/deny entries
  by hand: sync never touches entries it did not write. Keep the harness in its
  default permission mode (usually `ask`), not allow-all, and run sync again.
  If something goes wrong, copy `<file>.kei-backup-<timestamp>` over the
  native config. Only one backup is kept, from before the latest successful
  sync, so restore before you sync again.
- **Bundle reuse.** The runtime reuses the current bundle while policies and
  harnesses are unchanged (up to 6 hours).

## Realistic usage boundaries

- **Policy model:** sources are custom groups, `autogroup:member`, or
  `autogroup:admin`; owner counts as admin. Custom groups may contain users,
  agents, and service principals. Direct subjects require ID-based grants with
  expiry, reason, and approver; never use email as a policy source. Deny wins,
  there is no priority, and bindings are wiring only. Use the Policies and
  Groups reference pages in the Kei console for the human-facing explanation.
- **Command syntax:** verify it against the installed `kei` and `kei-proxy`
  help. Use `kei policy migration-report --workspace WS` for the read-only
  legacy policy report.
- **Harness rendering:** use `kei harness sync --dry-run` to review changes to
  native configuration. The harness enforces the rendered configuration for
  harness commands; the sync output is the evidence for what was rendered.
- **Tool-call authorization:** this skill covers harness command configuration.
  For runtime tool-call authorization, use the `kei-proxy` skill.
- **Report-only hook:** the hook records the harness's native outcome; it does
  not decide or block commands.
