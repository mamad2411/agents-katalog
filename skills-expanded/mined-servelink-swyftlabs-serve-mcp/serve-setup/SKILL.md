---
name: serve-setup
description: "Use when serve is not working yet: a tool returned `unauthorized`, the user has just installed this plugin, they say they are not logged in, or they ask how to set serve up / get an account / log in. Walks through account creation, `serve login`, and verifying the connection. Also the right skill when links fail for no obvious reason and you need to check the environment."
---

# Setting up serve

serve is a hosted service, so it needs an account and one login. This takes
about a minute and only happens once per machine.

**You cannot finish this for the user.** Login opens a browser and requires a
human to confirm. Run the commands, then say plainly what they need to click.

## 1. Is anything actually wrong?

Check before instructing. Call the `account_status` tool — if it returns a plan
and usage, setup is already done and the problem is elsewhere (try `doctor`).

`unauthorized` from any tool means exactly one thing: no valid token on this
machine. Go to step 3.

## 2. The binary

This plugin's `.mcp.json` runs `npx -y @servelink/serve`, so npm fetches the
binary on first use and there is nothing to install. `npx` needs Node.js.

For a `serve` command on the user's own PATH — needed for `serve login`, and
worth having anyway:

```bash
npm i -g @servelink/serve
```

or

```bash
brew install servelink-swyftlabs/tap/serve
```

Confirm it landed:

```bash
serve --version
```

An old binary cannot connect at all — the transport was upgraded rather than
deprecated in place. If the version looks stale, upgrade before debugging
anything else.

## 3. Log in

```bash
serve login
```

This opens the browser at the activation page with the code already filled in.
The user confirms there, and the CLI stores a token.

It also prints a URL and an `XXXX-XXXX` code as a fallback. Use those when
there is no browser — SSH, a container, a headless box — or pass
`--no-browser` to skip the launch attempt entirely.

Signing up happens in that same browser flow, so a user with no account does
not need a separate step. Free tier is enough for everything in this plugin.

Tell the user what to expect rather than just running the command:

> Run `serve login` — it'll open your browser to confirm, and you can create
> the account there if you don't have one.

## 4. Confirm it worked

```bash
serve doctor
```

That checks config and identity, the account API, the relay, and outbound
UDP 443. From MCP, `account_status` is the equivalent one-call check.

After a successful login the MCP server picks up the token automatically —
there is nothing to paste into a config file, and no API key to manage.

## When it still doesn't work

- **`serve doctor` reports UDP 443 blocked.** serve is QUIC-only with no TCP
  fallback, so a network that blocks outbound UDP 443 cannot be worked around
  from this end. Corporate networks and some VPNs do this. The user needs a
  different network or an admin exception.
- **Login opens the browser but nothing confirms.** The code expires. Re-run
  `serve login` for a fresh one.
- **`unauthorized` returns after a successful login.** The token was revoked,
  or the MCP server is a different install than the CLI that logged in. Run
  `serve login` again and re-check `account_status`.
- **Everything passes but links are refused.** That is a plan limit, not
  setup. The error's `code` and `hint` say which one and what resets it.

Persistent trouble: `serve@servelink.cc`, with the output of `serve doctor`
and `serve --version`.

## What the user gets on Free

Unlimited owned links, 3 simultaneous live tunnels, 100 MB per published
artifact, 1 GB stored, 2 GB of tunnel transfer per month. Password protection
and named subdomains are Pro. Free links are public to anyone holding the URL —
say so if the user is about to share something sensitive.
