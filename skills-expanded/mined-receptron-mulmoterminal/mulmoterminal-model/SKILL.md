---
name: mulmoterminal-model
description: Run MulmoTerminal sessions on something other than Anthropic's default, three ways — register an Anthropic-compatible backend (OpenRouter, Moonshot, a local Ollama bridge, a company gateway) as a `providers` entry in `~/.mulmoterminal/config.json` (also added in Settings → Models and backends); pin a `provider` / `model` per project in its `.mulmoterminal.json`; or add a `customAgents` entry, your OWN command line for starting Claude Code (`ollama launch claude --model … --`, a wrapper script, a pinned binary), which then appears in the Agent Picker beside Claude / Codex / Antigravity / Grok / Shell and gets Claude Code's own arguments appended. Knows the measured pass rates of the built-in model list, and the misconfigurations that break a session in ways that are hard to diagnose from inside it (a trailing `/v1`, too small an output budget, an API key written to disk, a provider named but never registered, a custom agent that swallows the arguments it is handed). Use when the user wants to use OpenRouter, Kimi, GLM, DeepSeek, Qwen, a local or self-hosted model, a cheaper model, a different Anthropic model for one project, or to launch Claude Code through a command of their own, or to run some cells on a second Claude Code / Codex subscription (`accounts`) — or when a session refuses to start, returns empty replies, or 404s after they changed models.
---

# Run on another model

The keys, and the job each one does:

- **`~/.mulmoterminal/config.json` → `providers`** — register a backend once. Also added and
  removed in Settings → Models and backends, which refuses a `/v1` base URL and a key in place of the
  variable's name.
- **`<project>/.mulmoterminal.json` → `provider` / `model`** — what this project launches on.
  Both are defaults; the launch form can override them for a single session. Also a select in
  Settings → Directory settings → Change here, which offers the models of the registered providers.
- **`~/.mulmoterminal/config.json` → `customAgents`** — the user's own COMMAND for starting Claude
  Code, offered in the Agent Picker. For when the model is reached by running something else
  (`ollama launch claude …`, a wrapper script, a second Claude Code install) rather than by an
  HTTP endpoint. Also added and removed in Settings → Models and backends.
- **`~/.mulmoterminal/config.json` → `accounts`** — a SECOND LOGIN for Claude Code or Codex (another
  subscription), kept in its own config directory and picked per cell in the launch form. Also added
  and removed in Settings → Models and backends.
- **`~/.mulmoterminal/config.json` → `tokenRotation`** — several Claude subscriptions behind the ONE
  default config directory, with MulmoTerminal choosing which one each new session runs on so the
  weekly windows drain evenly. config.json only (beta).
- **`~/.mulmoterminal/config.json` → `defaultAgent`** (or `--agent <id>` on the command line) —
  which of the seven agent CLIs a NEW cell starts as, and the only thing that relaxes the
  Claude-Code-required check at start-up (#2082). Also a select in Settings → Models and backends.

None is needed to use Anthropic's default. Only do this when the user asked for another model.


## `defaultAgent` — which agent a new cell opens on

Start-up requires Claude Code **unless this is set**. Declaring an agent does two things and only
two: the start-up check looks for THAT agent's binary instead of `claude`, and a new cell's Agent
Picker starts on it.

```json
{ "defaultAgent": "codex" }
```

`--agent codex` does the same for one launch and is NOT written back to the file. Settings →
Models and backends → Default agent writes the same key, and offers an agent that is not installed only disabled.
Valid ids: `claude`, `codex`, `antigravity`, `grok`, `muse`, `copilot`, `cursor`.

**It does not re-point anything that already exists.** A grid cell records its agent only when it
is not Claude, so a saved Claude cell is stored as the ABSENCE of that field — which means Claude
permanently, whatever `defaultAgent` later says. A browser that has already used the Agent Picker
also keeps its remembered choice. This key seeds new things; it never rewrites old ones.

**Do not confuse it with `customAgents`.** `defaultAgent` picks among the seven built-in agents.
`customAgents` adds a NEW Agent Picker entry that runs Claude Code through a command of your own.

**Which one.** A backend that speaks the Anthropic API over HTTP is a `providers` entry — that is
the smaller change and it composes with the model picker. Reach for `customAgents` only when the
thing that runs the model is a **command**, and the user cannot express it as a base URL and a
token.

## Registering a backend

```json
{
  "providers": [
    {
      "id": "openrouter",
      "label": "OpenRouter",
      "baseUrl": "https://openrouter.ai/api",
      "tokenEnv": "OPENROUTER_API_KEY",
      "maxOutputTokens": 16000
    }
  ]
}
```

Each rule below was measured against a working setup, and each breaks the session in a way that is
hard to diagnose from inside it:

- **`baseUrl` must not end in `/v1`.** Claude Code appends `/v1/messages` itself, so a trailing
  `/v1` produces `/v1/v1/messages` and every request 404s.
- **Never write the API key into a config or skill file.** `tokenEnv` is the **name** of an
  environment variable, not the value: the key reaches the server through its environment. Put it
  in the shell that starts the server, or in a `.env` in the directory it is started from — and if
  you write a `.env`, check it is gitignored before you do. If the user pastes a key at you, tell
  them where it goes; do not store it anywhere yourself.
- **Keep `maxOutputTokens` at 16000 or above.** A thinking model given less spends the whole budget
  thinking and returns empty visible text, which reads as a hung session.
- **`models` is REQUIRED under any `id` other than `openrouter`.** Every preset in
  `common/modelPresets.ts` carries `provider: "openrouter"`, and they are matched by that id — so a
  backend registered as `deepseek`, `moonshot` or a company gateway starts with **no models at
  all**, and a provider with no models is not offered in the picker (it cannot start a session
  either: naming a provider without a model is refused at spawn). Ask which model ids the user
  wants to run and list them.
- **Under the id `openrouter`, do not write a `models` array** unless the user names a model outside
  the built-in list — every preset appears in the picker on its own, with its measured pass rate,
  and `models` there exists only to ADD ids nobody has measured.
- **A model id is letters, digits and `. _ : / - ~`, optionally ending in `[1m]`.** Anything else in
  `models` — an object like `{"id": "…"}`, a value with a space, a `models` that is not an array — is
  dropped when the config loads, leaving a backend that lists models in the file and offers none in
  the picker. The server log names what it dropped; check it after writing.
- **`[1m]` is Claude Code's extended-context syntax, and the only bracketed suffix there is.** It
  goes to `claude --model` verbatim — Claude Code strips it before the id reaches the backend, so
  nothing on this side interprets it. Valid on an alias or a full name (`opus[1m]`, `opusplan[1m]`,
  `claude-opus-5[1m]`), refused anywhere but the end, and refused in invented forms like `[2m]` or
  `[200k]`. A **provider** `id` may not carry it. Only suggest it when the user asks for the 1M
  window: on Opus 5 / Sonnet 5 the Anthropic API already runs 1M, so it changes nothing there —
  the models it decides for are Opus 4.6 / 4.8 and Sonnet 4.6, and a gateway serving Sonnet 5.
  <https://code.claude.com/docs/en/model-config#extended-context>
- This is a **partial `POST /api/config` merge** — write only `providers`. Send the array **complete**
  (existing entries included): it replaces rather than appends.
- The server reads the environment **at startup**: after adding a key, it has to be restarted.

## Your own way of starting Claude Code — `customAgents`

For a model that is reached by **running a command** rather than by calling an endpoint. The entry
becomes a button in the **Agent Picker** — the Claude / Codex / Antigravity / Grok / Shell toggle at the
top of an empty cell — and picking it starts a real session: resumable transcript, cost and
context, "waiting for you", GUI tools. Global only. Settings → Models and backends adds and removes
entries (the id comes from the name there); write the file yourself for anything it does not cover.

```json
{
  "customAgents": [
    {
      "id": "nemotron",
      "label": "Nemotron",
      "agent": "claude",
      "command": "ollama launch claude --model nemotron-3-ultra:cloud --"
    }
  ]
}
```

| Key | Meaning |
|---|---|
| `id` | Lowercase slug (`[a-z0-9][a-z0-9_-]*`, ≤ 32 — letters, digits, `-` and `_`). It keys the wire and the session's memory, so **renaming it later is a different agent**; the label is the free one to change. Must not be `claude` / `codex` / `antigravity` / `grok` / `shell` — those are the built-in buttons. |
| `label` | The button's text, ≤ 24 chars. It shares one row with the four built-ins, and that row already wraps in a narrow cell. |
| `agent` | Which agent this launches AS — whose arguments get appended. **`"claude"` is the only value today**, and it is **required**. |
| `command` | The command line, ≤ 500 chars. Run as the program, with that agent's own argv appended. |

Eight entries maximum.

### What actually runs

MulmoTerminal appends **Claude Code's entire argv** to `command`, unchanged — the same one the
`claude` binary would have received:

```
ollama launch claude --model nemotron-3-ultra:cloud -- \
  --session-id <uuid> --settings <hooks JSON> --permission-mode … \
  [--model …] [--mcp-config …] [--allowedTools …] [--add-dir …] [--append-system-prompt …]
```

So the command must **end where Claude Code's own arguments begin**. A wrapper that takes flags of
its own needs the `--` (or whatever it uses) to stop parsing, exactly as in the example above:
`ollama` consumes `--model nemotron-3-ultra:cloud`, and everything after `--` is passed through.

Two consequences worth stating to the user:

- **`--model` is not a conflict.** The wrapper's own `--model` sits before the `--` and is consumed
  by the wrapper; the launch form's model choice arrives after it, for Claude Code. They are
  different arguments to different programs.
- **A wrapper that swallows or reorders what follows breaks the session**, and it breaks it
  quietly: no `--session-id` means no resumable transcript, no `--settings` means the hooks never
  fire so the cell never shows working / waiting, no `--mcp-config` means no GUI tools. If a custom
  agent starts but the cell stays grey and cannot be resumed, this is why — test the command by
  hand with a `--version` after it and check it reaches Claude Code.

### `agent` is required, and why

Nothing in `ollama launch claude --model … --` tells MulmoTerminal which CLI is on the far side of
that `--`. It is declared, never guessed — an entry that omits `agent`, or names one whose argv
this app cannot build, is **dropped on load**, which looks exactly like never having written it.
Audit with `/api/config` rather than assuming a write landed.

### This is not a launcher chip

The two look alike in Settings and are opposites in behaviour. Say which one the user wants:

| | Custom agent (Agent Picker) | Launch command (`launchers`, a chip) |
|---|---|---|
| Runs | your command **+ Claude Code's arguments** | your command, **verbatim** |
| Session | a real agent session — resume, cost, context, waiting status | a plain terminal; recorded as a shell |
| GUI tools / MCP | as any Claude cell | only what your own command asks for |
| Shell syntax | **no** — argv only, no `$VAR`, no pipes, quotes honoured | yes, run through the login shell |

If the user wants a command run and nothing added, that is `launchers` — a Settings section, not
this key.

### Practical notes

- **A partial `POST /api/config` merge**, like `providers`: send `customAgents` **complete**, it
  replaces rather than appends.
- **No restart needed** — the list is read at every spawn, so an added entry reaches the next
  session. But an existing browser tab needs a **reload** to show the new button.
- **A missing program is reported by the child**, not pre-flighted: `CLAUDE_BIN` cannot fix a
  command the user wrote, so the terminal shows the shell's own "command not found" rather than
  this app's binary diagnosis. Check the command exists on `PATH` when a cell dies instantly.
- **Which agent a session was started on is remembered on disk**
  (`~/.mulmoterminal/custom-agent-sessions.jsonl`), so it survives the cell closing, the session
  exiting and a server restart. Resuming a conversation months later still runs it the way it was
  being run.
- **Resuming a conversation keeps the agent it started on, whatever the picker currently says.**
  Picking a custom agent and then clicking a row under *OR RESUME HERE* continues that session as
  it was; the picker only decides what a NEW session starts as. Same rule as the provider/model
  pick. To run an existing conversation on a different agent, start a new session instead.
- Deleting an entry that a live session was started from leaves that session running; the next
  start falls back to plain `claude`.

## A second subscription — `accounts` (beta)

This is a BETA feature: tell the user so when setting one up. The step-by-step procedure (first
`/login`, and accepting the trust prompt in the workspace so its usage gauge can appear) is the guide
page https://receptron.github.io/mulmoterminal/guide/en/accounts.html (Japanese: `/guide/ja/accounts.html`).

For a user with more than one Claude Code or Codex subscription who wants cells on each. Every
account is its own config directory — its own login, transcripts, history and settings — and the
launch form of an empty cell offers it in an ACCOUNT select under the model; the cell's header then
names it. A user with no entries sees nothing change.

```json
{
  "accounts": [
    { "id": "work", "label": "Work", "agent": "claude", "home": "~/.claude-work" },
    { "id": "personal", "label": "Personal", "agent": "codex", "home": "~/.codex-personal" }
  ]
}
```

| Key | Meaning |
|---|---|
| `id` | Lowercase slug (`[a-z0-9][a-z0-9_-]*`, ≤ 32). Sessions are remembered by it, so **renaming it later is a different account**; the label is the free one to change. |
| `label` | What the launch form and the cell show, ≤ 24 chars. |
| `agent` | `"claude"` or `"codex"`. |
| `home` | The config directory: absolute, or starting with `~/`. A relative path is dropped. Claude Code is started with `CLAUDE_CONFIG_DIR`, Codex with `CODEX_HOME`, set to it. |

Eight entries maximum.

### Signing in

The first cell on a new account starts the CLI in an EMPTY config directory, so it asks for a login
inside that cell (`/login` for Claude Code). That login is kept in that directory from then on.
Settings, your own MCP servers and the trust answers per project start empty too — they belong to
the default login. What MulmoTerminal provides does follow the account: the bundled
`mulmoterminal-*` skills are installed into its directory (at startup, and when an account is added
through the config API), and a cell on it gets the directory's GUI tool groups — the launcher's
switches — handed to it at launch.

### How a session keeps its account

- **The account applies to a NEW session only.** A session is bound to its account when it first
  starts, and that is remembered on disk (`~/.mulmoterminal/account-sessions.jsonl`). Resuming it —
  after closing the cell, after a restart, months later — runs it on the same account, whatever the
  launch form says now. Its transcript is in that account's directory; it cannot move.
- **Lists show every account's sessions**, each row carrying the account it belongs to.
- **The toolbar shows each account's 5h / 7d usage**, named, beside the default login's. A Claude
  account is measured like the default — a short hidden session on that login, so a tiny query on
  that subscription, and only once it is signed in; a Codex account is read from its own rollouts.
- **Do not point an account at the default directory** (`~/.claude`, `~/.codex`). Claude Code keys
  its login on the variable being set at all, even to `~/.claude`, so MulmoTerminal treats such an
  account as the default login: its cells get no variable added, and it has no gauge of its own. A
  cell with no account gets no such variable added either.
- **Where not to put it**: not in a custom agent's `command` (`env CLAUDE_CONFIG_DIR=… claude`), and
  not in `providers`' `env`. MulmoTerminal then reads the default directory while the session writes
  elsewhere, so the session list, resume, cost and history all come back empty.
- A partial `POST /api/config` merge like the others: send `accounts` **complete**.

## Several subscriptions, chosen per session — `tokenRotation` (beta)

For a user with more than one Claude subscription who wants them used EVENLY without picking one
per cell. Unlike `accounts`, every conversation stays in the default `~/.claude`, so any session can
be resumed on any subscription — the same as switching with `/login`, done automatically.

1. For each subscription, the user runs `claude setup-token` in their OWN terminal (it signs in
   through the browser) and stores the printed token, e.g. in the macOS keychain:
   `security add-generic-password -a mulmoterminal -s mulmoterminal-token-a -w` (with nothing after
   `-w` it prompts, so the token never reaches the shell history). **Never ask the user to paste a
   token into the chat, and never write one into config.json** — an entry names where it is kept.
2. Add the key:

```json
"tokenRotation": {
  "enabled": true,
  "includeDefaultLogin": true,
  "tokens": [
    { "id": "a", "label": "Personal", "email": "me@example.com", "keychain": "mulmoterminal-token-a" },
    { "id": "b", "label": "Work", "email": "me@work.example", "file": "~/.mulmoterminal/tokens/b" }
  ]
}
```

- `keychain` is read with `security find-generic-password -a <keychainAccount> -s <keychain> -w`;
  `keychainAccount` defaults to `mulmoterminal`. Off macOS, use `file` (a file holding only the
  token). It must be `chmod 600` and owned by the user: a file anyone else can read is refused,
  with the reason in the server log. Exactly one of the two per entry; an entry with both or neither is dropped.
- `email` is what the user signs in with — shown beside that token's usage so they can tell which
  subscription is which. MulmoTerminal cannot read it from the token.
- `reserveWeeklyPercent` (optional, above 0 up to 99): part of that subscription's week rotation never
  spends — for a subscription the user also needs outside MulmoTerminal. With `5` it counts as full at
  95%: no new session starts on it, a running one moves off at the end of its turn, and it is not used
  even when every other subscription is out. Any other value is ignored.
- `includeDefaultLogin` (default `true`): the `/login` credential is one more candidate. Once EVERY
  subscription is a token, advise `false`: the `/login` account is always one of them, so it would be
  counted twice, and which one it duplicates changes whenever the user runs `/login` again.
- **How it chooses**: by the 7-day window's remaining percent per hour until it resets, highest first
  — room that is about to reset is used before it is lost — divided by one plus the sessions already
  running on it, so cells opened together spread over several subscriptions. A token whose 5-hour window is at 90% or
  more, or whose 7-day window is at 98% or more, is skipped; so is one whose usage probe found it at
  its limit. Each token's usage is measured by a short probe
  under that token, and appears as its own gauge beside the header's usage gauge.
- **Which cells rotate**: a plain Claude cell on the default directory only. A provider, a custom
  agent or an `accounts` login already says whose subscription it runs on and is never rotated.
- A token is chosen when a session's process STARTS (new, or resumed after it exited). A running
  session keeps its token; reconnecting to it changes nothing.
- **At 98%**: a session that ends a turn on a subscription at 98% (either window) moves to another one
  then, between turns.
- **When a running session hits its limit**, it moves by itself: that subscription is held out, the
  cell reconnects and resumes the same conversation on the next choice, and prints one line naming
  both. The prompt that hit the limit is NOT re-sent — the user sends it again. If every other
  subscription is held out too, the session stays where it is with Claude Code's own limit message.
  Only sessions rotation started are moved; a provider's 429 never is.
- The cell's header names the subscription it runs on. Claude Code's own `/status` may still name the
  `/login` account — only a display; usage is counted against the header's subscription.
- A token that cannot be read is skipped for that spawn, with a warning in the server log naming the
  entry (never the value).

## Choosing a model — never invent an id

Read `common/modelPresets.ts` in the MulmoTerminal repo and offer what is listed there, **with its
measured pass rate**.

Those numbers are the point. Each entry records how many attempts of a real tool-using task the
model completed — a model can answer fluently, in good prose, and never once call a tool, and that
is indistinguishable from working until you try to get something done. `3/3` and `0/4` are the
difference between a usable session and a broken one, so quote the ratio when you offer a model.

- Prefer entries whose `trials.status` is `measured` with `passed === of`.
- `status: "unreachable"` is **not** a defect in the model — it means the account that ran the
  measurement couldn't reach it (OpenRouter answers 404 when privacy settings exclude every
  provider serving a model). Another account may run it fine; say that rather than hiding it.
- `status: "unmeasured"` means the user added it themselves. Say it is untested.
- If the user names a model that isn't listed, add it to that provider's `models` array rather than
  silently trusting it — and tell them it is unmeasured.
- `medianSeconds` is worth quoting when they care about latency: the same probe ran in 11s on one
  model and 69s on another.

## Pinning a project

```json
{ "provider": "openrouter", "model": "moonshotai/kimi-k2" }
```

| Key | Meaning |
|---|---|
| `provider` | The `id` of a backend registered in `providers`. **Omit to stay on Anthropic.** |
| `model` | Passed to `claude --model`. With no `provider`, this picks a different **Anthropic** model. May end in `[1m]` for the 1M context window (see above). |

**A directory naming a `provider` that isn't registered, or whose key is missing, does not fall
back — its sessions refuse to start.** Check the provider exists in the global config before writing
this, and check the environment variable is actually set in the shell that will run the server.

`.mulmoterminal.json` applies live: writing it with your Write/Edit tool is itself the reload
signal (there is no filesystem watcher). But a **running** session keeps the model it launched with
— reopen the cell to see the change.

## When it doesn't work

Work down this list; each maps to one of the rules above.

| Symptom | Look at |
|---|---|
| Every request 404s | A trailing `/v1` on `baseUrl` |
| Session starts, replies are empty | `maxOutputTokens` below 16000 on a thinking model |
| Session refuses to start | A `provider` id that isn't registered, or `tokenEnv` naming a variable that isn't set in the server's shell |
| The backend is missing from the MODEL dropdown | It has no models to pick — presets exist only under the id `openrouter`, so list `models`. Open "Needs attention" beside the MODEL label for the sentence naming what is missing |
| `models` is in the config and the picker still offers none | Every id in it was refused by the shape rule above. The server's log names them |
| Worked yesterday, not today | The key was in a shell that's gone. The server reads the environment at startup |
| Model answers but never edits files | Not a config problem — check the model's pass rate in `modelPresets.ts` |
| A custom agent's button never appears | The entry was dropped on load — most often no `agent: "claude"`, an `id` that is not a lowercase slug, or one clashing with a built-in. Audit `/api/config`, then reload the tab |
| A custom agent's cell starts but stays grey, or cannot be resumed | The command is swallowing the appended arguments — see "What actually runs" |
| A custom agent's cell dies instantly | The program is not on the server's `PATH`. There is no pre-flight check for a command you wrote; the terminal shows the child's own error |
