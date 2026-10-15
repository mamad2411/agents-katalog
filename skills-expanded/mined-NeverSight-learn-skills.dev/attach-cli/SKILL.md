---
name: attach-cli
description: "Uploads PR and validation media to a self-hosted attach Worker via the installed attach CLI (`attach` or `gh attach`): device-flow login with ATTACH_GITHUB_CLIENT_ID, put/delete/logout of screenshots and artifacts, preview `/p/…` URLs, raw `/o/…` embeds via `--markdown`, and `--json`/`--url` output; or GitHub App JWT enroll then `att_` PUT for agents. Use when the user asks to attach a screenshot, upload PR media, put an image on attach.uinaf.dev (or ATTACH_API_BASE), share a validation screenshot URL, run attach login/put/delete/logout, use gh attach, host validation media, take down attach media, or enroll an App agent for attach. Do not use for Worker deploy, vault, Cloudflare ops, or inventing a second upload client."
---

# attach-cli

Upload media to an attach Worker and return public URLs. Prefer the installed
CLI for humans; use JWT enroll only for GitHub App agents.

## Require the CLI (humans)

```bash
command -v attach || command -v gh
attach --help 2>/dev/null || gh attach --help 2>/dev/null || true
```

If `attach` is missing, stop and ask the user to install via their approved
path (`brew install uinaf/tap/attach`, `npm i -g @uinaf/attach-cli`, or
`gh extension install uinaf/gh-attach`).
Do not download installers from this skill. Do not invent curl/fetch upload
scripts. Treat `gh attach …` as the same binary; never modify `gh auth`.

## Human workflow

Details: [references/human.md](references/human.md).

`ATTACH_GITHUB_CLIENT_ID` is the Attach GitHub App **client id** (operator /
GitHub App settings) — if unset, stop and ask. Optional `ATTACH_API_BASE`
(default `https://attach.uinaf.dev`).

1. `attach login`
2. `attach put <file> [--repo owner/name] [--pr N]` — default preview `/p/…`;
   `--markdown` for raw `/o/…`; `--json` / `--url` as needed
3. `attach delete <url-or-key>` then `curl -sI <url>` → 404/410 before success
4. `attach logout` when done with credentials

On allowlist rejection or login failure: report the blocker and stop.

## Agent workflow (GitHub App)

JWT claims, header-file HTTP, and secret handling:
[references/agent.md](references/agent.md). Requires App **public** key in Worker
`AGENT_REGISTRY`; App PEM stays in the agent secret store (never chat).

1. Sign JWT: `iss=attach:<app_id>`, `aud` = public host, `exp≤120s`, fresh `jti`
2. `POST /v1/enroll/agent` with Authorization via a **header file** (never argv);
   parse JSON in-process — keep `token` only in memory / secret store
3. `PUT /v1/objects` the same way — success only when JSON includes both `url`
   and `preview_url`
4. On put **401**: re-enroll once (new `jti`) and put again; further failure → hard-fail

## Hard rules

- Upload only with `att_` keys — never GitHub tokens / PATs / `ghs_` / install tokens
- Never print App PEMs, device codes, or `att_` values (including enroll JSON)
- Prefer preview URLs; `--markdown` / raw `url` only when the consumer needs embeds

Stop when put returned URLs, delete verified gone, or blocked on install / client
id / allowlist / registry / auth — reply with the URL or precise blocker only.
