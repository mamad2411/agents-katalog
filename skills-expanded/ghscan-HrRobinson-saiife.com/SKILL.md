---
title: the openclaw skill
description: the CLI an openclaw agent uses to drive one granted saiife environment.
---

saiife ships an openclaw skill that lets an openclaw agent drive the one environment it has been
granted: list panes, create panes, navigate and inspect browser panes, prompt terminal panes, read
their output, and record checkpoints.

it lives in the saiife repository at `openclaw/skills/saiife/`. it is not bundled inside the
installed app.

two files:

| file                     | what it is                                                                                                                                                   |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `SKILL.md`               | the skill manifest — `name`, `description`, and `metadata.openclaw.requires` declaring `node` under `bins` and `SAIIFE_ENDPOINT`, `SAIIFE_TOKEN` under `env` |
| `bin/saiife-control.mjs` | the CLI. maps one verb to one control-API request and prints the JSON response                                                                               |

## wiring it up

1. in saiife, grant operator access to an environment. that mints a loopback endpoint and a bearer
   token scoped to that one environment.
2. make both available to the openclaw agent process.

if `~/.openclaw/openclaw.json` already exists, saiife does step 2 for you. on grant it writes the
credentials into `skills.entries.saiife.env`; on revoke it removes exactly that entry again.

it is deliberately conservative about that file, because the file is yours:

- it never creates it. no config, no writing.
- it touches no key other than `skills.entries.saiife.env`. sibling keys you keep under `saiife`
  survive a revoke.
- a container that exists with a non-object shape is never replaced — the write fails instead.
- every failure is non-fatal. the grant itself still succeeds, and the failure shows up as a
  console warning and an entry in the environment's action log. token values are never logged.

it also drops the pre-rebrand `skills.entries.localflow.env` block if it finds one, so an old grant
cannot sit there holding a stale token nothing reads.

panes launched from saiife's own openclaw agent preset additionally get `SAIIFE_ENDPOINT` and
`SAIIFE_TOKEN` injected as process env.

if you have no config file, or you would rather wire it yourself, set the two variables by hand —
either as process env or under that same `skills.entries.saiife.env` block.

`SAIIFE_OPENCLAW_CONFIG` points saiife at a different config file. see
[environment variables](/docs/reference/environment-variables).

## running it

```
node "$SKILL_DIR/bin/saiife-control.mjs" <verb> [args...]
```

it reads `SAIIFE_ENDPOINT` and `SAIIFE_TOKEN` from the environment and fails immediately if either
is missing. every response is the control API's JSON body, printed to stdout. a non-2xx response
still prints the body and also exits non-zero.

## verbs

| verb                                           | request                                                |
| ---------------------------------------------- | ------------------------------------------------------ |
| `panes`                                        | `GET /panes`                                           |
| `navigate <handle> <url>`                      | `POST /panes/<handle>/navigate`                        |
| `screenshot <handle>`                          | `POST /panes/<handle>/screenshot`                      |
| `cookies <handle>`                             | `GET /panes/<handle>/cookies`                          |
| `network <handle>`                             | `GET /panes/<handle>/network`                          |
| `act <handle> <selector> <click\|type> [text]` | `POST /panes/<handle>/act`                             |
| `prompt <handle> <text...>`                    | `POST /panes/<handle>/prompt`                          |
| `output <handle> [maxLines]`                   | `GET /panes/<handle>/output`, `maxLines` defaults to 5 |
| `create-pane browser <url> [groupId]`          | `POST /panes`                                          |
| `create-pane terminal <agentId> <groupId>`     | `POST /panes`                                          |
| `checkpoint <watchpointId> [--halt]`           | `POST /captures`                                       |

an unknown verb, or a `create-pane` kind that is neither `browser` nor `terminal`, fails locally
before any request is made.

### screenshots

`screenshot` returns a `{path}` on the target project's own disk. it does not return pixels. hand
the image to a coding agent by referencing that path in a following `prompt`.

### creating panes

`create-pane` adds a pane to this environment and nowhere else.

a browser pane's `groupId` is optional — omit it for a standalone pane. a terminal pane's `groupId`
is required, and its working directory is derived from an existing member of that group; the caller
never supplies a cwd. an unknown or foreign-environment `groupId` is rejected.

terminal `agentId` is limited to `claude`, `codex` and `gemini` — the presets that carry their own
tool-permission gates. `shell` and `openclaw` are rejected with `invalid pane request`.

## scoping and auth

one grant covers one environment. the bearer token selects it, so a handle belonging to any other
environment simply does not resolve — a foreign handle is a 404, not a leak.

a missing or unknown token is a 403 with `{"error":"no grant"}`. revoking the grant in saiife
invalidates the token immediately, and every route starts returning 403.

## checkpoints

there is no separate checkpoint-authoring API. a checkpoint is a `command` step in your own lobster
workflow YAML that calls the `checkpoint` verb:

```yaml
- command: node "$SKILL_DIR/bin/saiife-control.mjs" checkpoint wp1 --halt
```

`--halt` marks the capture as halted; omit it for a non-halting checkpoint.

the `watchpointId` must already exist. it comes from saiife's own watchpoint registration, not from
this skill.
