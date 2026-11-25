---
name: tokenstash
description: Put API keys and other secrets into this project's env file with the tokenstash CLI, without the user pasting them in chat. Use whenever code needs a credential env var (OPENAI_API_KEY, STRIPE_SECRET_KEY, DATABASE_URL and the like), when a provider rejects a key with 401, for a step only the user can do (a DNS record, a dashboard toggle, an OAuth consent screen), or when tokenstash itself misbehaves.
---

# tokenstash

The user keeps their API keys in tokenstash. You run its CLI. A key goes from the user's stash into this project's env file (`.env.local` unless configured otherwise), and you get back a status line, never the value. Whatever the user has to do (paste a key, approve this folder, do a manual step) happens on a card in the tokenstash inbox, a page in their browser.

## Rules

These hold whether or not tokenstash is installed or working.

- Never ask the user to paste a key, token, password or connection string into the chat. Request it with `tokenstash need`.
- Never read the env file into your context (`cat`, an editor, `grep` for values), and never print, quote or summarize what it holds, even if the user asks. Load it with the runtime.
- Never reveal any part of a secret value, from anywhere.
- Never invent a stand-in value by any route (env file, environment variable, shim, shadowed module, default in code), whether the key is pending, declined, expired or missing. Continue with what does not need it, make the feature optional, or say what is blocked.
- Never answer, approve or decline a card on the user's behalf. Never create accounts or sign up for services for them.

## Get a key

```
tokenstash need OPENAI_API_KEY RESEND_API_KEY
```

Run it from the project. The project is the git repository's root (or the current directory outside a repository), and the env file is written there. Ask for every key a feature needs in one call: stored keys waiting for this folder's approval share one card, each missing key gets a card of its own, and the user gets one notification for all of them. Pass what you know, so the card is precise:

```
tokenstash need TAVUS_API_KEY --why "POST /v2/videos needs auth" --url https://platform.tavus.io/api-keys --step "Sign in" --step "API Keys, then Create"
```

tokenstash already knows the signup page and key format for about 80 providers (`tokenstash registry` lists them), so `--url` and `--step` matter most for the rest.

Each key gets a status line and a `next:` line saying what to do. Follow `next`. With `--json` you get one object: `results[]`, each with `status` (`injected`, `pending`, `denied`, `expired`), `name`, `identity` and `next`, and for a pending key `task_id` and `inbox` (the card link).

| Exit | Meaning | What to do |
|---|---|---|
| 0 | Every key is in the env file | Load it and continue |
| 10 | At least one key waits on the user | Give them the link from `next`, keep working on what does not need it, check later |
| 20 | The user declined | Do not ask again; make the feature optional or say what is blocked |
| 30 | The card expired unanswered | Say what is blocked and stop |
| 1 | Error | Read the message, then `troubleshooting.md` |

## While a key is pending

A pending key has a card, and `next` says which kind:

- **Missing key.** The user opens the link, gets the key from the provider (the card links to the right page) and pastes it. The link works as it is.
- **Approval.** The key is stored, but this folder has not received it before, or it is a sensitive key (live payment keys, cloud and deploy credentials, any key tokenstash does not recognise), which every folder asks for separately. The link you get shows the card but cannot approve it, so an agent can never approve its own request. The user approves from the link in the desktop notification; if they opened your link instead, the card has a button that sends that notification again.
- **Replace.** The provider rejected the stored key. The user pastes a new one, and every folder that had the old key gets the new one.

Tell the user in a sentence or two what the card is for and give the link. Then keep working. If `next` says the user may be on another computer (an SSH login, a machine with no desktop), the link points at this machine's 127.0.0.1 and will not open there: ask them, and if so run `tokenstash remote tailscale` (when Tailscale is set up on both machines) and give them the new link. Check with `tokenstash tasks` (this project's open cards), or run the same `tokenstash need` again: it never files a second card or notifies twice. Use `--blocking --timeout 600` only when nothing else can proceed.

## Use the key

The value is in the env file and nowhere else. Frameworks that read `.env.local` (Next.js, Vite, Nuxt, Remix) pick it up by themselves; restart a dev server that was already running. Otherwise use the runtime's dotenv support, or run the program through tokenstash:

```
tokenstash run -- npm run dev
```

`run` loads the env file into the program's environment. If the program exits non-zero and its output names a known key that is not set, `run` files a card for it (always a fresh approval, since the program's output chose the key), waits, and restarts the program, up to `--retries` times (default 3).

## When a provider rejects a key

If an API call fails with 401 (or the provider's documented bad-key status) and the request was well-formed, the same shape as one that worked and with the auth header exactly as the provider documents, tell tokenstash instead of the user:

```
tokenstash report-bad OPENAI_API_KEY --status 401
tokenstash need OPENAI_API_KEY
```

tokenstash re-checks the key with the provider. A dead key comes back from `need` as a pending Replace card: give the user the link. If `need` writes the key again, the provider accepted it, so look at your request. 400, 404 and 422 are not key problems. 403 means the key works but lacks a permission: tell the user which one. Report once per failure, not in a loop.

Usually you will not see the 401 at all. Before handing over a key it has not checked in the last day, tokenstash checks it with the provider, and a dead key comes back as a Replace card instead.

## Steps only the user can do

```
tokenstash ask "Add a TXT record for resend.dev" --url https://dash.cloudflare.com --step "DNS, then Add record" --step "Type TXT, name @, value v=spf1 include:resend.dev ~all"
```

Same exit codes and the same kind of card. `--expects text` gets an answer back, in the `note` field of `tokenstash tasks --history --json`. The user is told the answer reaches you word for word, so ask for things like a region or a project id, never a secret; secrets go through `need`.

## Work and personal accounts

Each key is stored under an identity, `default` unless chosen. `tokenstash need STRIPE_SECRET_KEY --identity work` requests the `work` copy; if there is none, the card asks the user for it.

## When the user asks you to change something

Some commands act for the user. Run them only when the user asks, and pass `--why` with what they said, so the card shows it:

| The user asks you to | Run |
|---|---|
| Replace a key that still works | `tokenstash rotate NAME` |
| Delete a stored key | `tokenstash forget NAME` |
| Always use another identity for a key in this project | `tokenstash bind NAME --identity work` |
| Ask again for a key they declined | `tokenstash need NAME --force` (once per key and identity until the "no" expires) |
| Stop agents loading this skill on their own, or let them again | `tokenstash init --mode explicit`, `tokenstash init --mode auto` |
| Register or remove the MCP server | `tokenstash init --mcp`, `tokenstash init --no-mcp` |
| Take tokenstash out of their agents | `tokenstash init --undo` |

Each one files a card and exits 10. Nothing changes until the user confirms it from their own inbox link; declining it changes nothing. Give the user the link from `next`, as for any card. `rotate` files a Replace card: the old key keeps working until the user pastes the new one.

## When something goes wrong

Run `tokenstash doctor` first. It checks the stash, the database, the inbox, the agent setup and this folder, and its last line names the binary in use. Then look up the symptom in `troubleshooting.md`, beside this file. Two common ones:

- `... is for a person at a terminal, not an agent`: a few commands are the user's alone (`open`, approving with `answer`, `tasks --all`, `workspaces`, `export`, `import`). `troubleshooting.md` lists what to do instead.
- The link does not open for the user: the inbox listens on this machine's localhost unless remote access is on. If the user is on another computer, see "The user cannot open the link" in `troubleshooting.md`.

`reference.md`, beside this file, lists every command, flag, exit code, JSON field, setting and file location.
