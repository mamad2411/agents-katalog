---
name: catch
description: Persistent, shared reverse-shell catcher for authorized pentesting and CTF — both the operator and the agent can drop in and out of the same caught shell, with built-in upload/download. Use after finding an RCE/command-injection to receive a reverse shell that survives either party detaching, drive it together, and move files. Triggers on "catch a shell", "set up a listener", "reverse shell handler", "pwncat", "I need a shell catcher", "upload/download to the target", "stage a tool onto the target".
---

# Shell catcher (persistent, shared)

A reverse-shell catcher that **both you (operator) and the agent can drive**, that
**survives either of you dropping out**, and that does file **upload/download** out
of the box. Driven by `./roo catch`. The engine is **pwncat-cs** (platform
detection + transfer commands) running inside a **tmux** session inside a detached,
tunnel-bound `net-toolbox` container — so the listener sits at the tunnel IP and
reverse shells come back over the VPN.

## Scope guardrail

Authorized targets only — CTF boxes, lab ranges, signed-scope hosts. Catching a
shell means you already have (operator-approved) code execution on the target;
this skill is the handler, not the exploit.

## Why it's built this way

- **Persistent** — the catcher is a *detached* container running a tmux session.
  Closing your terminal, or the agent finishing a turn, does **not** kill it.
- **Shared (drop-in/drop-out)** — one tmux session, two drivers. You attach a real
  TTY (`roo catch attach`); the agent drives non-interactively (`send`/`capture`).
  Same session, same caught shell — like the **browse** skill's shared browser.
- **Bound to the tunnel** — the listener is in the VPN namespace, so revshells
  return over the engagement tunnel and bind the tunnel IP (your LHOST).

## Use it

```bash
./roo catch up                 # listen on a random ephemeral port
./roo catch up 4444            # ...or a specific port (e.g. 443/53 if egress is filtered)
```
`up` prints your **tunnel IP + the port**, plus paste-ready reverse-shell
one-liners. Set one on the target (via your RCE); when it connects, pwncat catches
it.

```bash
./roo catch attach             # YOU: drop into the shared session (detach: Ctrl-b d)
./roo catch enter              # AGENT: drop into the target PTY (do this once a shell lands)
./roo catch send <cmd...>      # AGENT: run a command in the caught shell
./roo catch capture            # AGENT: print the current session output
./roo catch status             # is it up? + recent output
./roo catch down               # stop the catcher (teardown also sweeps it)
```

**`enter` first, or `send` talks to the wrong thing.** pwncat boots at its own
**local** command prompt (`(local) pwncat$`), so a fresh `send <cmd>` is parsed by
*pwncat*, not the target (you'll see `error: <cmd>: unknown command`). `./roo catch
enter` sends Ctrl-D to toggle into the target's PTY (`(remote) user@host$`); after
that `send`/`capture` drive the real shell. `enter` toggles — run it again to pop
back to the local prompt (e.g. for `upload`/`download`). `capture` shows the current
prompt, so check it if a `send` looks like it went nowhere.

Multiple catchers can run at once (different ports); `attach`/`enter`/`status`/`down`
take an optional port to pick one. `send`/`capture` can't (the rest is the command) —
select one with `ROO_CATCH_PORT=<port>`, and otherwise they assume a single catcher.
Sweep strays first (`roo catch down` / the **teardown** skill): a leftover catcher
from a past session makes `send`/`capture` ambiguous, and a port typed into `send`
positionally is swallowed into the command, not used to pick.

## Shared-session etiquette (don't fight the operator)

Same rule as the browse skill — you're co-driving a live session a human may be
using:

- **Announce before you act**, and **report what you found** (the `capture`
  output) so the operator can follow.
- Don't spam input while the operator is typing; interleaved keystrokes collide in
  a shared tmux pane.
- Leave the session in a sane state; **don't run destructive commands** without
  operator approval — this is real code execution on the target.

## Upload / download (pwncat)

`upload` and `download` are **pwncat local-prompt** commands (run `./roo catch
enter` to toggle back from the target PTY to `(local) pwncat$`). They **auto-pick a
transfer method** based on the target's platform (curl/wget/base64/…):

- **download** (target → host): lands in **`.roo/catch/`** on the host by default
  (git-ignored, host-visible). Override the local name with a second argument.
- **upload** (host → target): stage a local file (e.g. from `.roo/`) onto the box —
  drop a privesc helper, exfil a config, etc.

Loot pulled down is on your host immediately; tools you want to push are read from
the host side. (Linux/Windows enumeration helpers like linpeas/winpeas/pspy are a
natural thing to `upload`.)

## Hand-off

- Caught a shell as a service/user account → enumerate, then loop creds back into
  the recon/**ad** flow; pull hashes down and hand to the **hashcat** skill.
- Need to stage a Windows .NET tool first → grab it with the **wintools** skill
  (`/tools` is mounted in the catcher too), then `upload` it.

## Notes for the operator

- The catcher is a container named `roorecon-catch-<port>` — killable directly and
  swept by the **teardown** skill (no orphaned listeners hammering the target).
- Container-only, tunnel-bound; needs the VPN sidecar up (`roo vpn up`). First run
  builds/refreshes the net-toolbox image (pwncat-cs lives there).
- A reverse shell is one connection per listener; for a second target, start
  another `roo catch up` on a different port.
