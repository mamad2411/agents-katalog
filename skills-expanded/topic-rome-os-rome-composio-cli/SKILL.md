---
name: composio-cli
description: Help users operate the published Composio CLI to find the right tool, connect accounts, inspect schemas, execute tools, subscribe to trigger events with `composio listen`, script workflows with `composio run`, and call authenticated app APIs with `composio proxy`. Use when the user asks how to do something with `composio`, wants to run a known tool slug, needs to discover a slug with `composio search`, fix a missing connection with `composio link`, inspect tool inputs with `--get-schema` or `--dry-run`, troubleshoot top-level CLI flows, or explicitly needs `composio dev` guidance.
---

# Composio CLI

## Preflight: Is The User Logged In?

**Before running any toolkit command, confirm the user is logged in. If they are not, stop and tell them to log in — do not improvise.**

```bash
composio whoami   # exits non-zero when there is no session
```

If `whoami` fails (no Composio session), the user is logged out. **Stop here.** Do not:

- run `composio login` yourself,
- look for an alternate toolkit, slug, or `proxy` route,
- ask the user to paste a key, or
- attempt any other workaround.

Respond directly to the user with one message: they need to log in to Composio first, via the **"Log in with Composio"** action on the Composio app's dashboard. Then end your turn and wait — the request cannot proceed until they have logged in.

Only once `whoami` succeeds do you continue to the workflow below.

## Connection Invariant: One Account Per Toolkit

Rome operates **exactly one connected account per toolkit**. This is load-bearing
because `execute`, `proxy`, and `run` have **no flag to choose an account** — they
act on the toolkit's single connected account, and when more than one exists
Composio silently resolves a non-deterministic default. You cannot tell, and
cannot control, which account a tool ran as. A second Gmail means a "send email"
might go out from the wrong account with no signal.

To keep every tool call deterministic:

- **Never create a second account for a toolkit.** Do not pass `--alias` to
  `composio link` to add an additional account, and do not enable the
  `multi_account` experimental feature. The alias buys you nothing on execution —
  there is no `--alias`/`--account` on `execute` — it only lets you accumulate
  ambiguous accounts.
- **Check before linking.** `composio link <toolkit> --list` shows existing
  accounts. If one is `ACTIVE`, you are connected — retry `execute`, do not link
  again.
- **If `--list` shows more than one account for a toolkit, stop and surface it.**
  Tell the user the toolkit has duplicate accounts and tool calls are ambiguous
  until the extras are removed. Do not guess which one to use.

## Default Workflow

1. Start with `composio execute <slug>` whenever the slug is known.
2. If several independent tool calls must happen at once, use `composio execute -p/--parallel` with repeated `<slug> -d <json>` groups.
3. If `execute` says the toolkit is not connected, run `composio link <toolkit>` and retry.
4. If the arguments are unclear, run `composio execute <slug> --get-schema` or `--dry-run` before guessing.
5. Reach for `composio search "<task>"` only when the slug is unknown. `search` accepts one or more queries, so batch related discovery work into a single command when useful.

## `execute` - Run A Tool

Use `execute` when the tool slug is already known.

```bash
composio execute GITHUB_GET_THE_AUTHENTICATED_USER -d '{}'
```

Inspect required inputs without executing:
```bash
composio execute GITHUB_CREATE_AN_ISSUE --get-schema
```

Preview safely:
```bash
composio execute GITHUB_CREATE_AN_ISSUE --skip-connection-check --dry-run -d '{ owner: "acme", repo: "app", title: "Bug report", body: "Steps to reproduce..." }'
```

Pass data from a file or stdin:
```bash
composio execute GITHUB_CREATE_AN_ISSUE -d @issue.json
cat issue.json | composio execute GITHUB_CREATE_AN_ISSUE -d -
```

Upload a local file:
```bash
composio execute SLACK_UPLOAD_OR_CREATE_A_FILE_IN_SLACK \
  --file ./image.png \
  -d '{ channels: "C123" }'
```

Run independent tool calls in parallel:
```bash
composio execute --parallel \
  GMAIL_SEND_EMAIL -d '{ recipient_email: "a@b.com", subject: "Hi" }' \
  GITHUB_CREATE_AN_ISSUE -d '{ owner: "acme", repo: "app", title: "Bug" }'
```

Key flags:
- `--get-schema`: Inspect required arguments without executing the tool.
- `--dry-run`: Preview the request shape without performing the action.
- `--file`: Inject a local file path into a tool that exposes exactly one uploadable file argument.
- `--parallel`: Execute multiple independent tool calls in the same invocation.

There is **no flag to pick an account** — `execute` uses the toolkit's single
connected account (see "Connection Invariant" above). Keep one account per
toolkit so this is unambiguous.

- `--file` only works when the tool exposes a single uploadable file input. Otherwise use explicit `-d` JSON.

## `search` - Find The Slug

Use `search` only when the tool slug is not already known.

```bash
composio search "create a github issue"
composio search "send an email" --toolkits gmail
composio search "send an email" "create a github issue"
composio search "my emails" "my github issues" --toolkits gmail,github
```

- Batch related discovery work into one `search` invocation, then move back to `execute` once the correct slugs are known.

## `link` - Connect An Account

Use `link` when `execute` reports that a toolkit is not connected, or when the user explicitly wants to authorize an account.

```bash
composio link gmail
composio link gmail --list          # inspect existing accounts before linking
composio link googlecalendar --no-browser
```

Key flags:
- `--list`: List the toolkit's existing connected accounts instead of linking. Run
  this first — if an account is already `ACTIVE`, retry `execute` rather than linking.
- `--alias`: Names an additional account for a toolkit (requires the
  `multi_account` experimental feature). **Avoid it** — Rome keeps one account per
  toolkit, and extra accounts make `execute` ambiguous (see "Connection Invariant").

- Retry the original `execute` command after linking succeeds.

## `proxy` - Raw API Access

Use `proxy` when a toolkit supports a raw API operation that is easier than finding a dedicated tool slug.

```bash
composio proxy https://api.github.com/user --toolkit github --method GET </dev/null
```

## `run` - Scripting, LLMs, and Programmatic Workflows

For programmatic calls, loops, output plumbing, or anything beyond a single tool call, prefer `composio run`.

`composio run` executes an inline ESM JavaScript/TypeScript snippet with authenticated `execute()`, `search()`, `proxy()`, and the experimental `experimental_subAgent()` helper pre-injected. No SDK setup required.

Chain multiple tools:
```bash
composio run '
  const me = await execute("GITHUB_GET_THE_AUTHENTICATED_USER");
  const emails = await execute("GMAIL_FETCH_EMAILS", { max_results: 1 });
  console.log({ login: me.data.login, fetchedEmails: !!emails.data });
'
```

Fan out with Promise.all:
```bash
composio run '
  const [me, emails] = await Promise.all([
    execute("GITHUB_GET_THE_AUTHENTICATED_USER"),
    execute("GMAIL_FETCH_EMAILS", { max_results: 5 }),
  ]);
  console.log({ login: me.data.login, emailCount: emails.data.messages?.length });
'
```

Feed tool output into an LLM and get structured JSON back:
```bash
composio run --logs-off '
  const emails = await execute("GMAIL_FETCH_EMAILS", { max_results: 5 });
  const brief = await experimental_subAgent(
    `Summarize these emails and count them.\n\n${emails.prompt()}`,
    { schema: z.object({ summary: z.string(), count: z.number() }) }
  );
  console.log(brief.structuredOutput);
'
```

- Use top-level `execute --parallel` instead when the user only needs a few independent tool calls and does not need script logic.

## Bundled Scripts

Reusable scripts ship in `rome_apps/composio/scripts/` and are invoked via `composio run -f`.

### `gmail-parse-markdown.ts` — Gmail → Markdown

`GMAIL_FETCH_EMAILS` returns each body as raw HTML — a single 50-message page is typically ~200k tokens, dominated by HTML markup and tracking URLs. This script fetches messages and converts each body to clean Markdown using `@mozilla/readability` (with a turndown fallback when readability mis-fires on transactional emails). Cuts a 50-message page to ~3-15k tokens depending on content.

Reach for it any time the user wants Gmail content fed to an LLM, summarized, or otherwise processed as text — not when they need raw HTML.

```bash
# One-time setup (deps live alongside the script, not in the workspace):
(cd rome_apps/composio/scripts && npm install)

# Default: drop tracking URLs, keep anchor text, strip images
composio run -f rome_apps/composio/scripts/gmail-parse-markdown.ts -- --max 20

# Keep links inline (use only when downstream needs the URLs)
composio run -f rome_apps/composio/scripts/gmail-parse-markdown.ts -- \
  --query "is:unread newer_than:1d" --max 50 --include-links
```

Flags:
- `--query "<gmail-query>"` — Gmail search query (e.g. `"is:unread newer_than:1d"`)
- `--max <N>` — max_results (default 10, max 500)
- `--page-token <token>` — pagination cursor from a prior `nextPageToken`
- `--include-links` — keep inline links (default strips URLs but preserves anchor text; ~3x token savings)
- `--raw` — also return the original `messageText` alongside `markdown` (debugging only)

Output is JSON on stdout: `{ messages: [{ messageId, threadId, sender, subject, markdown, bodyFormat, ... }], nextPageToken, resultSizeEstimate, options }`.

## Auth

```bash
composio whoami   # check current session — run this first (see Preflight above)
```

When `whoami` fails the user is logged out. **Do not run `composio login` on
their behalf and do not work around the missing session.** Tell the user to log
in via the dashboard and stop — see "Preflight: Is The User Logged In?" above.

The **Composio Rome app** reads the key live from the CLI session
(`~/.composio/user_data.json`) — that session is the single source of truth; the
app stores no copy of its own. Its dashboard exposes Composio login as one
explicit browser action: "Log in with Composio" (or "Re-authorize" once logged
in) opens Composio in a new tab to authorize Rome, which writes the issued key
into the CLI session. The dashboard deliberately hides the CLI mechanics — the
guardian just sees the button.

Because the app reads the CLI session directly, a `composio login` **you (the
agent)** run in this terminal is picked up automatically — there is no separate
"import" step.
