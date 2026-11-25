---
name: sshepherd
description: Use this skill whenever the user mentions "sshepherd" by name, or wants to check on a remote server (health, disk, memory, CPU, ports, OOM history), inspect or restart docker/systemd services, tail remote logs, read or write remote config files, deploy a project via a named recipe, introspect a remote Postgres database, or audit SSH/security posture on a box — while keeping the agent zero-knowledge about credentials (no password, private key, or host/user/port ever reaches the agent's context or a tool response). Covers all 9 registry-driven command groups (hosts, check, logs, services, deploy, config, db, files, security) via a single compiled Bun/TypeScript CLI that shells out to the system `ssh` binary — the agent only ever passes an ssh alias, a pg-target name, or a recipe name, never a credential. `setup` is a separate group (deliberately not one of the 9) that writes sshepherd's own local config files; every `setup` action is agent-invocable, with one narrow exception — `setup ssh-alias install` opens a one-shot browser form that only a human can type a password into.
---

# sshepherd

`sshepherd` is a compiled Bun/TypeScript CLI for server operations over SSH — health
checks, service/container control, log tailing, config edits, Postgres introspection, and
declarative deploys — built so an agent can drive a real server without ever seeing a
password, private key, host, user, or port. Every op resolves through an ssh alias already
configured in `~/.ssh/config` (or a `db`-group pg-target / `deploy`-group recipe name that
itself resolves to an alias); OpenSSH does the actual authentication, entirely outside this
process.

**Binary:** `/Users/macbook/Documents/PROJECT_MISPAQUL_ATTORIQ/sshepherd/dist/sshepherd`

If the binary is missing, build it first:

```bash
cd /Users/macbook/Documents/PROJECT_MISPAQUL_ATTORIQ/sshepherd && just build
```

Call the binary by its absolute path — it is not on `PATH`. Every example below uses the
bare `sshepherd` name for brevity; substitute the absolute path when invoking.

**Deep references (read on demand, not upfront):**

- `references/transport.md` — the zero-knowledge SSH model, ControlMaster lifecycle,
  the error classification enum, why stderr is discarded entirely.
- `references/recipes.md` — the TOML deploy-recipe format, every step kind, `depends_on`
  ordering, the `[rollback]` block, `--dry-run` plan shape, a complete worked recipe.
- `references/db.md` — the pg-target model, read-only enforcement layers, the `db` ops'
  output shapes, why `db query` rejects multi-statement SQL.
- `references/output-shapes.md` — the `Envelope` shape, log-line objects, verdict fields,
  the `ErrorInfo` shape — read this before parsing any command's `data`.

## The zero-knowledge model

The agent never types, sees, or passes a hostname, IP, username, port, password, or private
key through sshepherd — not as an argument, not in a response — with one narrow, scoped
exception noted below.

- The agent passes only a **name**: an ssh alias (`web-01`), a pg-target name (`prod`),
  or a recipe name (`demo`). Every alias/target/recipe is declared once, ahead of time, in
  `~/.ssh/config`, `~/.config/sshepherd/targets.toml`, or a recipe TOML — never on the
  command line.
- OpenSSH resolves the real connection tuple (`HostName`/`User`/`Port`/`IdentityFile`)
  internally; sshepherd shells out to the system `ssh` binary (never the `ssh2` npm
  library) so credential handling stays entirely inside OpenSSH's own trusted code path.
- Every response `Envelope` echoes back only the `alias` it was given — there is no
  host/user/port/ip field anywhere in the response shape, structurally.
- The one scoped exception: `setup ssh-alias status <alias>` echoes that alias's own
  `host`/`user`/`port` (plus `hasKey`) back in `data` — not new exposure, since the caller
  already supplied those same values to `register` in the first place. `setup ssh-alias
  list` stays name-only, and every other command in the tool, including all 10 registry
  groups, still returns only the alias/target/recipe name.
- ssh's own stderr is discarded entirely (never surfaced, never logged) — it's classified
  into a small error enum instead, because OpenSSH's stderr phrasing varies by
  version/locale and can leak a hostname no redaction allowlist would catch.
- `hosts list` and `setup ssh-alias list` return alias *names* only, never
  `HostName`/`User`/`Port`.
- Every `files` op (`ls`/`cat`/`tail`/`download`/`disk-usage`/`upload`) refuses any remote
  path not pre-declared for that alias in `~/.config/sshepherd/files-allowlist.toml` —
  fail-closed, same rule as `config get`/`put`/`validate` and `config-allowlist.toml`. See
  Gotchas #11.
- `.env`-shaped files (`files cat`) are masked by default (`KEY=***MASKED***`); an agent
  must pass `--reveal KEY1,KEY2` to unmask specific keys, and each key must clear a
  hardcoded secret-pattern denylist (`PASSWORD`, `SECRET`, `TOKEN`, `PRIVATE_KEY`,
  `CREDENTIAL`, `API_KEY`, ...) *and* be pre-declared in
  `~/.config/sshepherd/reveal-allowlist.toml` — the denylist wins even over a mistaken
  allowlist entry. See Gotchas #11.
- `files download` writes the remote file straight to a local destination path and never
  returns its content in the JSON envelope — the safe way to pull any secrets-bearing file
  to disk (see Gotchas #10 for the incident this closed).
- Every mutating op writes an audit line (`~/.local/state/sshepherd/audit.jsonl`) —
  timestamp, alias, command, an arg hash (not raw args), and outcome — success or failure.
- `tunnel open`'s `--remote`/`--local` flags describe the forward target/exposed service as seen from
  the alias's own network (almost always `localhost:<port>`) — they are NOT the alias's own connection
  identity, so accepting them as free text doesn't weaken the zero-knowledge boundary; the response
  still never carries `HostName`/`User`/`Port`.

## Command shape

```
sshepherd <group> <action> [positionals...] [--flag value]
```

```bash
sshepherd --help                # lists 10 registry groups + the setup group
sshepherd <group> --help        # lists that group's actions + args/flags
sshepherd <group> <action> --help   # shows one action's args
```

The **first positional** differs by group:

| Group | First positional | Resolves via |
|---|---|---|
| `db` (except `list`) | `<target>` — a pg-target name from `targets.toml` | `targets.ts` |
| `deploy` (all actions) | `<recipe>` — a recipe name | `recipes.ts` |
| `hosts list`, `db list` | *(none — host-local, no ssh)* | — |
| `tunnel list`, `tunnel close` | *(none — `list` is host-local; `close` takes `<id>` instead)* | — |
| every other group | `<alias>` — an ssh alias from `~/.ssh/config` | — |

## Global flags

| Flag | Effect |
|---|---|
| `--yes` | confirm a mutating op — required; sshepherd never prompts interactively |
| `--dry-run` | `deploy run` only: print the resolved plan, execute nothing, no `--yes` needed |
| `--pretty` | render a human table/key-value view instead of JSON |
| `--reveal <keys>` | `files cat` only: comma-separated env-var keys to unmask |
| `--from <path>` | `config put` only: local file to read + base64-encode (instead of typing `--content-base64` by hand) |

Output is JSON to stdout by default (one `Envelope` per call — see `references/output-shapes.md`).
Exit codes: `0` success, `1` the op ran and failed (transport/command error, or a refused
`CONFIRMATION_REQUIRED`), `2` a usage error (unknown group/action, missing required
argument — no ssh connection was attempted).

## Quick reference — 10 registry-driven groups (55 ops) + 1 `setup` group (6 sub-groups, 12 actions)

```bash
# hosts
sshepherd hosts list
sshepherd hosts test web-01
sshepherd hosts info web-01

# check
sshepherd check overview web-01
sshepherd check mem web-01
sshepherd check disk web-01
sshepherd check cpu web-01
sshepherd check ports web-01
sshepherd check oom-history web-01
sshepherd check kernel web-01

# logs
sshepherd logs docker web-01 myapp --tail 100
sshepherd logs service web-01 nginx --tail 100
sshepherd logs docker-daemon web-01 --tail 100
sshepherd logs nginx web-01 error --tail 100

# services
sshepherd services ps web-01
sshepherd services stats web-01
sshepherd services inspect web-01 myapp
sshepherd services compose-ps web-01 /opt/myapp/docker-compose.yml
sshepherd services healthcheck web-01 myapp
sshepherd services systemctl-status web-01 nginx
sshepherd services restart web-01 myapp --yes
sshepherd services systemctl-start web-01 nginx --yes
sshepherd services systemctl-stop web-01 nginx --yes
sshepherd services systemctl-restart web-01 nginx --yes
sshepherd services systemctl-reload web-01 nginx --yes

# files
sshepherd files ls web-01 /opt/myapp
sshepherd files cat web-01 /opt/myapp/.env --reveal DB_HOST
sshepherd files tail web-01 /var/log/syslog --n 100
sshepherd files download web-01 /opt/myapp/backup.sql ./backup.sql
sshepherd files disk-usage web-01 /var/lib/docker
sshepherd files upload web-01 ./local.conf /opt/myapp/local.conf --yes

# config
sshepherd config get web-01 /etc/nginx/nginx.conf
sshepherd config validate web-01 /etc/nginx/nginx.conf
sshepherd config put web-01 /etc/nginx/nginx.conf --from ./nginx.conf --yes
sshepherd config reload web-01 nginx --yes

# db
sshepherd db list
sshepherd db tables prod
sshepherd db activity prod
sshepherd db connections prod
sshepherd db slow prod
sshepherd db size prod
sshepherd db query prod "SELECT count(*) FROM users"

# deploy
sshepherd deploy run demo --dry-run
sshepherd deploy run demo --yes
sshepherd deploy status demo
sshepherd deploy rollback demo --yes
sshepherd deploy logs demo --tail 100
sshepherd deploy migrate demo --yes

# security
sshepherd security harden web-01 --yes
sshepherd security ssh-audit web-01
sshepherd security listeners web-01
sshepherd security authorized-keys web-01
sshepherd security fail2ban web-01

# tunnel
sshepherd tunnel open web-01 --kind local --remote localhost:5432 --duration 1800 --yes
sshepherd tunnel list
sshepherd tunnel close t-a1b2c3d4 --yes

# setup — agent-invocable; install's credential boundary is the one exception (see Gotchas #9)
sshepherd setup ssh-alias register myserver --host 1.2.3.4 --user deploy --yes
sshepherd setup ssh-alias keygen myserver --yes
sshepherd setup ssh-alias install myserver --yes
sshepherd setup ssh-alias list
sshepherd setup ssh-alias status myserver
sshepherd setup ssh-alias update myserver --host 5.6.7.8 --port 2222 --yes
sshepherd setup ssh-alias remove myserver --yes
sshepherd setup db-target scaffold prod --alias myserver --user app --database appdb --container app_db --yes
sshepherd setup config-allowlist scaffold myserver --paths /etc/nginx/nginx.conf,/opt/app/.env --yes
sshepherd setup deploy-recipe scaffold demo --alias myserver --workdir /opt/app --yes
sshepherd setup files-allowlist scaffold myserver --paths /opt/app/backup.sql,/opt/app/.env --yes
sshepherd setup reveal-allowlist scaffold myserver --keys NODE_ENV,APP_REGION --yes
```

## Gotchas

1. **Zero-knowledge is not optional per-call.** There is no flag to pass a raw host/user/
   port/password — the only way to reach a server is to declare it as an ssh alias (or a
   pg-target/recipe pointing at one) ahead of time, outside this tool.
2. **Every mutating op needs `--yes`, always writes an audit line.** sshepherd never
   prompts interactively (agent-first design) — without `--yes` a mutating op returns a
   `CONFIRMATION_REQUIRED` envelope and refuses before touching ssh. Success *and* failure
   both get an audit line in `~/.local/state/sshepherd/audit.jsonl`.
3. **No raw exec, ever.** There is no `sshepherd exec "<any command>"`. A genuinely novel
   need is authored as a named, versioned recipe step (`references/recipes.md`) —
   reviewable, not a free-text shell escape hatch. `plain ssh <alias>` remains the
   intentional human break-glass for one-off exploration.
4. **`deploy rollback` refuses without a `[rollback]` block.** A recipe that doesn't
   declare one has no inferred rollback — sshepherd never guesses.
5. **`config put` backs up before writing, always.** The existing file is copied to
   `<path>.bak-<UTC-timestamp>` in the same remote round trip, before the overwrite.
   `config put` also refuses any path not declared on that alias's allowlist
   (`~/.config/sshepherd/config-allowlist.toml`) — a local refusal, before any ssh call.
6. **`db` is Postgres-only, read-only, v1.** `db query` takes a single `SELECT` — a bare
   `;` is rejected before the SQL is even parsed (multi-statement guard), on top of a
   parser check and a `BEGIN TRANSACTION READ ONLY` wrapper. The real boundary is the
   read-only DB role declared on the target (`references/db.md`) — treat the client-side
   checks as UX guardrails, not the security boundary.
7. **A deploy failure names the step that failed.** `deploy run`/`deploy migrate` surface
   `data.failed_step` (`{index, kind, name}`) on a `COMMAND_FAILED` error, recovered from a
   marker each step echoes on non-zero exit — never guess which step broke from the raw
   output alone.
8. **`security harden` won't lock out the current session unless told to.** Directives
   that could disable the session's own auth method (`PermitRootLogin`,
   `PasswordAuthentication`) are only applied when `--keep-session=false` is passed
   explicitly; the safe subset always applies.
9. **`setup`'s only wall is `install`'s credential entry — and even that has a smart bypass
   first.** `register`, `keygen`, `remove`, `list`, `status`, `update`, `install`, and the
   five scaffolders (`db-target`, `config-allowlist`, `deploy-recipe`, `files-allowlist`,
   `reveal-allowlist`) are all agent-invocable, gated by `--yes` the same way as every other
   mutating op — none of them needs a human at the keyboard, except the one narrow case
   below. Before `install` ever opens a browser form, it runs two cheap, non-interactive
   pre-checks in order: a raw-socket Tailscale-SSH banner peek (a Tailscale-fronted target
   refuses key install outright — `TAILSCALE_SSH_DETECTED`, since Tailscale SSH doesn't use
   `authorized_keys`), then an already-trusted probe with zero new credentials (if the key
   is already authorized, `install` short-circuits with `data.method: 'already_trusted'`
   and no form ever opens). Only when both pre-checks come back negative does `install`
   open a one-shot local browser form, and a *human*, not the agent, supplies the
   credential there — either a password, or a pasted existing private key (rejected with
   `INVALID_PRIVATE_KEY` if it doesn't parse, or `PASSPHRASE_PROTECTED_KEY_UNSUPPORTED` if
   it's passphrase-protected). The agent may trigger `install` and wait on it, but it
   structurally cannot see, log, or relay either credential — both go straight from the
   browser submission into the install flow and never cross back into the agent's context;
   the agent only ever receives the resulting `SetupResult` (success or a typed error
   code), never the password or key itself.
10. **`files download` used to inline the whole file as base64 in the JSON envelope —
    fixed, but treat any `dist/sshepherd` built before this fix as unsafe on secrets.** A
    real incident: an
    agent ran `files download <alias> <remote .env.docker path> /tmp/dest.tmp` expecting
    scp-like behavior (write to `/tmp/dest.tmp`, never see the bytes). The old
    implementation took only one positional (`<path>`, remote-only) — the local
    destination the agent typed was silently discarded (`mapArgsToCtx` ignores extra
    positionals with no error), and the entire file was base64-encoded into
    `data.content_base64` in the envelope printed to stdout, i.e. straight into the
    agent's tool-result context, in a trivially-reversible encoding (`base64 -d`, no
    special access needed). Unlike `files cat`, the old `files download` applied **no**
    `.env` masking at all — it inlined any file's raw bytes regardless of shape, up to the
    10 MiB `DOWNLOAD_MAX_BYTES` guard (above that it refused with `truncated: true`, not a
    partial leak). This defeated the zero-knowledge promise for exactly the op whose name
    most strongly implies "goes to disk, not to you." Fixed in `src/registry.ts`
    (`filesDownload`): the op now takes **two** required positionals — `<path>` (remote
    source) `<local_path>` (local destination) — and `shape()` decodes the base64 and
    `writeFileSync`s it straight to `local_path` inside the CLI process; the envelope's
    `data` is now `{found, truncated, size_bytes, written, local_path}` with **no**
    `content_base64` field, ever. The raw bytes still transit the ssh channel and briefly
    sit in local process memory to decode — that's the same local-process exposure
    `files cat` already has before masking runs, not a new one; what changed is that the
    content never crosses back into the envelope the agent reads. If a script or an older
    compiled `dist/sshepherd` binary predates this fix, do not point `files download` at
    any `.env`-shaped, key, or credential file until confirmed rebuilt — check the
    envelope's `data` keys: `content_base64` present means the vulnerable version is
    running.
11. **`files` and `--reveal` are fail-closed as of v0.2.2 — a fresh install can't `files
    ls`/`cat`/`download`/`upload`/etc. anywhere until an allowlist exists.** Before v0.2.2,
    `files download`/`upload` had no allowlist at all (any remote path, in or out) and
    `--reveal` could unmask any key name the agent typed, including an actually-secret one
    (`DB_PASSWORD`, `AWS_SECRET_ACCESS_KEY`) — flagged by an external code review and
    closed the same way `config`'s allowlist already worked. Now every `files` op checks
    the path against `~/.config/sshepherd/files-allowlist.toml` (missing file = every path
    refused, same fail-closed rule as `config-allowlist.toml`), and `files cat --reveal`
    additionally checks each key against a hardcoded, non-overridable secret-pattern
    denylist (`PASSWORD`, `PASSWD`, `SECRET`, `TOKEN`, `PRIVATE_KEY`, `CREDENTIAL`,
    `API_KEY`, trailing `_KEY`/`_PASS`) *before* checking
    `~/.config/sshepherd/reveal-allowlist.toml` — the denylist wins even if a key was
    mistakenly added to the allowlist. Run `setup files-allowlist scaffold` and, if
    `--reveal` is needed, `setup reveal-allowlist scaffold` before using the `files` group
    on a fresh alias. The gate lives in exactly one place — `enforceAllowlist()` in
    `registry.ts`, called from `executeOp()` before any op's `buildRemote` runs — not
    hand-copied per op.
12. **`tunnel open` self-expires via a re-invoked hidden supervisor process, not an external `timeout`
    binary — and `tunnel list` is NOT side-effect-free.** GNU `timeout` isn't reliably present on macOS,
    so `--duration` is enforced by `sshepherd` re-invoking itself in a hidden `tunnel __supervise` mode
    that holds the expiry timer in-process and force-kills the real `ssh -N -L/-R/-D` process (and its
    own process group) when the timer fires — no new external dependency, portable across every release
    target. Calling `tunnel list` can itself terminate a tunnel: while scanning for active tunnels, it
    force-kills (and removes the state record for) any tunnel that's past its expiry but whose
    supervisor's own timer hasn't fired yet, rather than reporting a stale entry as still active — treat
    `tunnel list` as a mutating, potentially process-killing call, not a pure read, even though it needs
    no `--yes` (it's still `mutating: false` at the `OpSpec` level — the confirm gate the mutating flag
    controls is a separate axis from "is idempotent"). **Known limitation, deliberately not hardened
    against:** a tunnel's local process-tracking state is keyed on PID alone. If a tunnel's supervisor
    process exits and, in a since-widened window, the OS reuses that same PID for an unrelated
    process-group leader, `tunnel close`/`tunnel list`'s cleanup could in principle signal the wrong
    process group. This requires reused-PID-happens-to-be-a-group-leader, which is a low-probability
    edge case for a single-operator local dev tool — tracked as a known limitation of the PID-only state
    schema rather than solved with start-time/cmdline verification, which was judged out of scope for
    this build. Also: `tunnel open` returning `ok: true` confirms only that the supervisor process was
    spawned — NOT that `ssh` actually bound the port or that the target is reachable; a failure at that
    stage surfaces later (the next `tunnel list` prunes the now-dead entry), not in the `open` call's own
    response.

## Errors

| Code | Meaning |
|---|---|
| `UNKNOWN_ALIAS` | the ssh alias isn't defined in `~/.ssh/config` |
| `CONNECT_TIMEOUT` | couldn't reach the host within the connect timeout |
| `AUTH_FAILED` | SSH authentication failed for this alias |
| `HOST_KEY_MISMATCH` | the remote host key doesn't match the known-hosts entry |
| `SSH_TRANSPORT_ERROR` | ssh failed before the remote command could run, unclassified |
| `COMMAND_FAILED` | the remote command exited non-zero (`error.remote_exit` carries the code) |
| `COMMAND_TIMEOUT` | the remote command exceeded its timeout |
| `CONFIRMATION_REQUIRED` | a mutating op ran without `--yes` — refused before any ssh call |

Exit codes: `0` on `ok: true`; `1` when the envelope's `ok` is `false` (any code above);
`2` on a usage error (unknown group/action, missing required argument) — no ssh connection
is ever attempted for an exit-`2`.
