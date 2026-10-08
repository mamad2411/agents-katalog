---
name: qsetup
description: Connect this machine to a session-viz workspace by signing in through the browser — the only way in; no token is ever typed, pasted or shown in the terminal.
disable-model-invocation: true
---

# qsetup

Sign in in the browser, and a token arrives on disk. Three commands read that file —
`/qcontrib`, `/qshare` and `/qfeed`, the ones that talk to the hosted side. `/qteam` needs
the hosted side too but authenticates its own MCP connection and never opens the file. The
six local commands never open it either: they parse transcripts already on this disk and
send nothing anywhere.

## Why nobody types a token

A token is a long opaque bearer string. Every way of moving one by hand leaves a copy
somewhere: shell history, a screenshot, a scrollback buffer, the wrong window. Pasting it
into a local page was already better than typing it into a shell, but it still asked
somebody to hold the secret for a moment, and holding it is the part that goes wrong.

So the secret is never held. This is the RFC 8252 native-app flow:

1. this process mints a random `code_verifier` and keeps it to itself
2. its SHA-256 goes to `/authorize` through the browser
3. the person approves in a session they already have — the browser proves who they are,
   rather than a string they carry
4. a single-use `code` comes back to a loopback port here
5. this process exchanges code + verifier for the token, out of band

The code that crosses the browser is worthless without the verifier, which never left this
process. What arrives is an ordinary `svt_…` token: same list in the workspace, same
revoke button, attributed to whoever approved it.

The listener is deliberately small: bound to `127.0.0.1` only, on an ephemeral port the
kernel picks, `state` required on the callback and compared in constant time, shut down
after one callback, abandoned after five minutes.

The token is checked against the server **before** it is written. Storing an unverified
string is how a typo becomes a confusing bug in a different component three days later.

## Steps

### 1. Run it

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/qsetup.mjs
```

A browser opens on the consent screen. Sign in there if you are not already — by emailed
code, passkey, GitHub or Google, whichever that deployment offers. Approve, and the
terminal finishes on its own.

If the machine is headless, the printed URL works from anywhere that can reach its
loopback — which is to say, from that machine.

Two scopes exist, they are not equally available, and one is strictly the wider of the two:

| scope | for | who can approve |
|---|---|---|
| `contrib` | sending findings — plane A, person-blind aggregates | any member |
| `collab` | vaults, task handoff and the MCP — plane B, identity-bearing | admins only |

`contrib` is the default, and it is the default because any active member can approve one:
connecting a machine must not be an admin-only act. A `collab` token is accepted at the
plane A door as well, so an admin who already holds one does not need a second token to run
`/qcontrib`. The reverse does not hold — a `contrib` token is refused at plane B.

Ask for the wider one explicitly:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/qsetup.mjs --scope collab
```

The browser is sent on to the workspace once the token is written, so the last thing the
user sees is a console that already shows this machine as connected — not a dead loopback
tab.

### 2. Report what happened

One line: the scope and workspace it verified against, and the config path. Do not print
the token, not even partially — it is on the user's screen already and does not need to be
in the transcript too.

If the output carries a `note` about the preferred location not being writable, say which
path it settled on — that is a sandboxed harness, and the next command needs to find the
same file.

A non-zero exit means nothing was written: declining the consent screen, the five-minute
deadline, a failed exchange, and a host with no browser sign-in all end that way. Say which
happened and offer to run it again. Never report a connection the output does not show.

## Other flags

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/qsetup.mjs --show     # current config, token redacted
node ${CLAUDE_PLUGIN_ROOT}/scripts/qsetup.mjs --forget   # delete it
```

There is no flag that takes a token. A machine is connected by signing in, or not at all: a
token typed into a box is one that can be read over a shoulder, filed by a password manager
that thinks it is a password, pasted into the wrong window, or held by somebody who never
signed in — and the page asking for it has to be trusted before the token can be checked. A
host that does not offer browser sign-in cannot connect this machine, and setup says so and
stops rather than asking for a secret it cannot verify.

`--show` reads the file, which is now the only place a credential lives. When there is none
it prints the paths it looked in.

## A deployment that is not the public one

Setup signs in against `SESSION_VIZ_URL` when it is set, the `url` already in the config
when it is not, and `https://cloud.session-viz.com` otherwise:

```bash
SESSION_VIZ_URL=https://sv.example.internal node ${CLAUDE_PLUGIN_ROOT}/scripts/qsetup.mjs
```

Set it for that one run. The host it verified against is written into `config.json`, so
every later command reads the destination from there — and leaving the variable exported
afterwards is what breaks them, for the reason under **What it writes** below.

## What it writes

One `config.json`, mode `0600` in a `0700` directory:

```json
{
  "url": "https://cloud.session-viz.com",
  "token": "svt_…",
  "scope": "contrib",
  "tenant": "t_9b874215460c5c93",
  "actor": "claude-code",
  "savedAt": "…"
}
```

`tenant` comes back from the server, keyed to the token, and is opaque on purpose: `t_` and
sixteen hex characters of a hash of the address that signed up. It was derived from the
email domain once, which put two strangers who shared a domain in one workspace. Read it
back as an identifier, never as a company name, and never tell a user that a colleague on
the same domain will land in this workspace — an invite is what puts them there.

`actor` is whichever harness ran setup, or `SESSION_VIZ_ACTOR` when that is set. It travels
as the `x-actor` header on later calls, and in the browser flow it is also the label the new
token carries in the workspace list — otherwise four machines arrive as four rows called
"plugin". It is the one optional field: absent when no harness could be identified.

The location is not tied to any one harness — this plugin runs under Codex and others
too, and a machine that never had Claude Code installed has no `~/.claude` to write to.
Candidates, best first:

| path | when |
|---|---|
| `$SESSION_VIZ_HOME/config.json` | set — wins outright, see below |
| `$XDG_CONFIG_HOME/session-viz/` | `XDG_CONFIG_HOME` is set |
| `~/.config/session-viz/` | the default |
| `~/.claude/session-viz/` | honoured, never preferred — installs predating this |

Reads take the first that exists, so an existing token keeps working. Writes go to the
one already in use, or to the default when there is none.

**Sandboxed harnesses.** Codex and friends confine writes to the workspace, so every
path above fails with `EPERM` and no amount of retrying helps. Point
`SESSION_VIZ_HOME` at a directory inside the workspace — it beats every other candidate,
including a config that already exists somewhere unreachable.

**There is no credential in the environment.** `SESSION_VIZ_TOKEN` is gone: a token in a
shell profile is a token in a CI variable, a process listing and every child process that
inherited it, held by whoever copied it there rather than by the person the workspace issued
it to. A machine that cannot open a browser is connected by signing in on one that can and
carrying the `config.json` — `SESSION_VIZ_HOME` says where it may live.

`SESSION_VIZ_URL` still names the host **setup** signs in against, and after that the file
decides: if the variable is still set and names a different host than the file, every
command that would send something stops and says so rather than putting this workspace's
token in a request to whatever the variable happens to name. `SESSION_VIZ_ACTOR` decides a
label, not a credential.

The MCP server needs none of this. `.mcp.json` carries a bare URL and no `env` block, so
there is nothing to export — nothing on that path reads those variables at all.

And today the client gets no further than asking. It does the first half itself: 401,
discovery, registration. Then `/authorize` issues codes to one hardcoded client id — the
CLI's own `session-viz-cli` — so a client that registered a moment earlier is turned away
with `unknown client_id` on the server's own error page, not a consent screen. It refuses
the advertised scopes too: discovery offers `vault:read`, `task:write` and the rest, while
the consent screen accepts only `contrib` and `collab`. Registration succeeds and buys
nothing.

Say that plainly. It fails every time, not sometimes, so do not tell anyone to watch for a
browser prompt or to try again: they will wait on a prompt that is never coming and then go
looking for a tool that never appeared. Until the allowlist widens, browser sign-in to the
hosted MCP server does not complete. Leave the MCP out of setup, and say its OAuth path is
not live yet rather than walking someone into a refusal.
