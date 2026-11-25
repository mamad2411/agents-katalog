---
name: publish-flitz-bundle
description: Publish a Flitz bundle of the Flutter app in the current project with `flitz publish` and return the install link. Use when someone asks for a Flitz bundle, preview build, or install link of the app, in Claude Tag or locally.
argument-hint: "[project dir]"
---

# Publish a Flitz bundle

Run `flitz publish` in the project directory, as it is, and hand back the link. Do not clone,
check out, stash, or otherwise change the working tree: the bundle is built from whatever is in
the directory, uncommitted changes included.

## Find the project

The project is the directory holding `flitz.yaml`; the CLI reads the pinned SDK from there. Use
the current directory when it has one. Otherwise look for `flitz.yaml` in the repository: with one
match, use it; with several, pick the one the request names, or ask. With none, the app has not
been set up with `flitz sdk use`; say so, point at https://docs.flitz.dev/getting-started, and
stop.

## Run it

```bash
cd <project dir> && flitz publish --yes --json
```

- `--yes` lets a fresh machine download the pinned SDK without a terminal to confirm on.
- `--json` makes stdout one JSON document, so the link is never parsed from progress output.
- Flags the request asks for go on the same line, for example
  `--target lib/main_dev.dart --dart-define=ENV=dev`. Write a dart-define with `=` or
  `-D KEY=VALUE` with a space, because the CLI reads a `v` inside an attached `-DKEY=value` as
  `--verbose`.

When `flitz` is not on `PATH`, install it with `curl -fsSL https://download.flitz.dev/install.sh | sh`
(it lands in `~/.local/bin`). The installer verifies the binary's SHA-256.

**Claude Tag:** the Agent Proxy swaps the organization API key into requests to `api.flitz.dev`
after they leave the sandbox, but the CLI refuses to send anything without a non-empty
`FLITZ_APIKEY`. When `FLITZ_APIKEY` is unset and there is no stored `flitz login`
(`~/.config/flitz/credentials.json`, or under `$XDG_CONFIG_HOME` when that is set), prefix the
command with `FLITZ_APIKEY=injected-by-agent-proxy`. Never set it over a real login: inside the
CLI a set `FLITZ_APIKEY` wins over the login.

A first publish on a machine downloads the pinned SDK (several hundred MB) and resolves pub
packages, so it takes a few minutes; a warm one takes about a minute. Run it with a timeout of at
least 15 minutes. In a local Claude Code sandbox the run writes to `~/.local/bin`,
`~/.cache/flitz`, and `~/.pub-cache`, and reaches `*.flitz.dev` and `pub.dev`; when the sandbox
refuses one of those, re-run outside it.

## Report the result

On success, stdout is one JSON document: `id`, `page_url`, `deeplink`, `bundle_url`. Lead with
`page_url`: it opens in any browser and shows the QR code and an install button, which is what a
teammate on a phone needs. Add the `deeplink` only when someone asks for it.

The link does not expire and cannot be revoked, and anyone holding it can download the bundle.
Post it where it was asked for, not somewhere wider.

## When it fails

| Exit | Meaning | What to do |
|---|---|---|
| 1 | Bad input or project state, such as a missing `pubspec.yaml` | Fix it from the message; nothing was published |
| 2 | Local or unexpected: filesystem permissions, a held lock, an interrupted run, or a malformed `flitz.yaml` | Report the message; in a local sandbox, check the paths above are writable |
| 3 | Credential or license | With the placeholder key (Claude Tag), the channel's bundle has no working Flitz connector; tell the requester, since it is an admin fix. With a key from the environment, unset it to fall back to the login. Otherwise `flitz login`. An inactive license is for the organization's Owner to restore |
| 4 | Flitz service or network, including the 30-second upload limit | Re-run once; a re-run starts a fresh publish |
| 5 | The app does not compile | Report the compiler error; it is the code, not the setup |

The full contract is at https://docs.flitz.dev/cli/exit-codes. A failed publish never prints
JSON, so never guess a link from partial output.

Do not ask anyone for the API key or accept one pasted into a chat: Slack keeps it forever.
Credential setup belongs to the plugin `README.md`.
