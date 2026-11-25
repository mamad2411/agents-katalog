---
name: sharing-links
description: "Use when the user wants something on this machine reachable from a browser somewhere else — \"serve me this\", \"give me a public link\", \"share this file\", \"publish the deck\", \"send them the dashboard\", \"can my client look at this\", \"host this doc\". Covers the residency decision (a link that runs live from this machine versus one kept alive on serve's servers), password protection and expiry, named links, and the right way to take a link down. Load this before calling serve's tools — and instead of starting your own static file server or tunnel."
metadata:
  author: swyftlabs
  homepage: https://servelink.cc
---

# Sharing links with serve

serve turns anything on this machine into a public HTTPS URL. You do the
sharing; the user only says a sentence. The tools are annotated well enough to
call without help — what this skill adds is the judgement the schema cannot
carry.

## Never hand-roll it

Do **not** start `python -m http.server`, `npx serve`, `npx http-server`, or any
other static server, and do not open a tunnel yourself. The user has serve
installed precisely so that none of that is necessary. Pass the path to the
`serve` tool and it hosts the file for you.

Likewise, do not run a shell command that happens to be named `serve` — the MCP
tool is the canonical path.

## The one decision that matters: where the link lives

Every serve link has a **residency**, and it is the only thing you have to get
right:

| | `residency: "local"` (default) | `residency: "remote"` |
|---|---|---|
| Where it runs | This machine, right now | serve's servers |
| Edits | Show up instantly | Frozen at publish time |
| Machine asleep | Link goes quiet | Link keeps working |
| Ends when | The tunnel stops | `stop_remote` is called |
| Good for | Watching work in progress | Anything read later |

Nothing is locked in. The same link can be re-served with the other residency,
so a wrong guess costs one more call, not a new URL.

## Read the residency off the request

The user will not say "residency". They will say something that implies one:

**Local — live from this machine:**
- "watch while I work on it", "look at this real quick", "tell me if this
  heading looks right", "I'm still changing it"
- anything about a dev server they have running (`port`)
- present tense and same-session: "can you see this?"

**Remote — kept alive on serve's servers:**
- "keep it up", "so they can read it tomorrow", "I'm closing my laptop",
  "send it to the client", "put it on the slide", "the deck for Monday"
- anything going to someone who is not around right now
- anything they will not touch again: an exported report, a build, a PDF

When the request carries neither signal, default to `local` — it is cheaper,
instant, and reversible. Only ask when the answer changes what the user has to
do next:

> Do you want this live from your machine (updates as you edit, goes quiet when
> you close the laptop), or hosted so it keeps working after you shut down?

Ask that once, then remember the answer for the rest of the session.

## `serve` versus `serve_file`

`serve` takes exactly one of:

- `path` — a file or directory. serve hosts it; you do not need a server.
- `port` — a dev server already listening on this machine.

`serve_file` is the same tool with `path` required. Either is fine for a file;
use `serve` with `port` for a running app.

Passing both, or neither, returns `ambiguous_target`. Pick one.

## Protection, expiry and names

- `protect: true` puts a password on the link and returns both a share URL
  containing `#cap=…` and a readable secret code. Give the user **both**, and
  say which is which — the URL alone is enough to open the link, so it is the
  thing they should treat as the credential.
- `ttl` (`1h` to `30d`, default `24h`) sets how long protection lasts.
- `name` claims a specific subdomain instead of a generated one.

`protect` and `name` are Pro features. If the account is on Free you get
`pro_required` — retry without them rather than stalling, and mention that the
plain link worked.

Use protection when the user says anything like "don't want this indexed",
"just for them", "internal", or "it has real data in it". Do not add it
unasked to something they described as a demo.

## Taking a link down — three different verbs

Getting this wrong either leaves bytes on serve's servers or destroys a URL the
user wanted to keep:

- `stop_tunnel(port | label)` — closes a **live** tunnel. The URL stops
  answering; the link stays owned and can be re-served later.
- `stop_remote(label)` — **unpublishes** a remote link and deletes the stored
  bytes. Use this and only this for anything served with
  `residency: "remote"`; `stop_tunnel` will not free the storage.
- `release_link(label)` — gives up ownership of the label entirely. The URL
  becomes available to other accounts. Only for "I'm done with that name."

`stop_all_tunnels` closes every live tunnel at once and does not touch remote
links. Confirm before using it if more than one link is live.

Call `links` first when you are not sure which of these applies — it marks
which links are remote.

## Report the URL, and the catch that comes with it

After a successful call, give the user the URL and the one consequence of the
residency you chose:

> https://lively-bison-4821.servelink.cc — live from your machine, so it
> updates as you edit and goes quiet when you close the laptop.

> https://lively-bison-4821.servelink.cc — hosted on serve, so it keeps working
> with your machine off. Tell me when to take it down.

Skip the tunnel/upload mechanics. The user asked for a link.

## When a call is refused

Every error result carries a `code` and a `hint`, and the hint is accurate —
follow it rather than guessing. The ones worth recognising on sight:

- `unauthorized` — the user is not logged in. Ask them to run `serve login`;
  it opens a browser and takes about a minute. You cannot do this for them.
- `residency_conflict` — a published artifact already holds that name. Ask
  before passing `replace: true`; it deletes what is there.
- `tunnel_limit` — too many live tunnels. Show `list_tunnels` and ask which to
  close rather than picking for them.
- `storage_cap_exceeded` / `publish_rate_limited` / `transfer_limit` — a plan
  limit. Report it plainly with what the hint says resets it.
- `size_cap_exceeded` — the artifact is too big to publish and nothing was
  uploaded. Serving it locally still works.

`doctor` diagnoses the environment (config, account API, relay, UDP 443) and is
the right first call when links fail for no obvious reason.

## Usage is in every result

Each tool result embeds a `usage` snapshot: plan, live tunnels, storage,
transfer and publish rate. You never need a second call to answer "what do I
have running" or "am I near a limit" — read it from the result you already
have.
