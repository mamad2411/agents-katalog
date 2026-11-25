---
name: cli-interface-design
description: Design the public CLI that wraps a developer platform's API - which commands exist (curated commands plus a raw api escape hatch, not a 1:1 REST mirror), grammar, flag/env/config precedence, a frozen --json and exit-code contract, TTY behavior, login and CI tokens, pagination and --wait, errors, help, flag deprecation, telemetry, and safe use by scripts and coding agents. Use whenever the user mentions designing or reviewing a CLI for their API, CLI command naming, --json output, exit codes, CLI login, or an agent-friendly CLI - even without saying "CLI design". Not for API-less tools or parser code. Do NOT use for whether to offer a CLI (samber/developer-platform-skills@api-integration-surface-strategy) or a skill shipped with it (samber/developer-platform-skills@agent-skill-offering).
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.3"
---

# CLI Interface Design

You are a CLI interface designer for a developer platform. Design the command-line surface that wraps the platform's API - what it exposes, what it freezes as a contract, and how it behaves for a human at a terminal, a CI script and a coding agent - and write it down as one CLI design spec.

This is the design layer. Argument-parser libraries and per-language CLI-building skills sit one altitude below and implement what this specifies. Whether the platform offers a CLI at all is decided one altitude above, by `samber/developer-platform-skills@api-integration-surface-strategy`.

**Memory (advised):** When memory lives in a file, consider using `developer-platform-context.md`; if a different memory system is in use, rely on that instead. Read it before the questions below. Record the chosen command layers, the frozen contract surface, the exit-code table and the deprecation window, so a later run extends the spec instead of re-deriving it.

## Clarifying questions

Ask these before designing; each answer changes a later step. Batch them - this is a tactical design task. When the user cannot answer, write an assumption per question, with what it changes, into the spec's Assumptions section and continue.

1. Who runs the CLI, in what share: developers at a terminal, CI pipelines, coding agents? Which one breaks the business if it breaks?
2. What does the API look like: a complete OpenAPI spec checked in CI, or hand-maintained; roughly how many endpoints; uniform verbs across resources or resource-specific actions?
3. Which jobs need more than one API call or something only a local process can do (log tailing, webhook forwarding to localhost, deploy-and-wait, scaffolding)? Does the API expose an event or request-log stream to build them on?
4. What auth exists: an OAuth server, API keys only, SSO? Are tokens scoped and expiring? Is there a test mode separate from live?
5. Which operations are asynchronous, which are destructive or irreversible, and does the API accept idempotency keys?
6. Does a CLI already ship? If yes, which outputs and flags do customer scripts already parse?
7. Where do users sit (EU share, regulated or enterprise buyers)? This decides the telemetry posture in step 11.
8. The date the first release must land, whether this is a one-off launch or a compounding product surface, and the effort ceiling (engineers, maintenance appetite). These re-rank the layer menu in step 2.

## Workflow

1. Name the jobs and audiences.
2. Choose the command layers and grammar.
3. Declare the contract surface.
4. Set flags, configuration and profiles.
5. Design output, streams and exit codes.
6. Design auth and credential storage.
7. Handle lists, long-running operations and retries.
8. Write errors and help.
9. Make it safe without a terminal.
10. Make it agent-ready.
11. Set versioning, deprecation, updates and telemetry.

Write the result with [references/cli-design-spec-template.md](references/cli-design-spec-template.md). Each step has a section below, in order.

## Gates

Five binary gates, self-set from the rules below (no industry body defines a pass bar for CLI design). Iterate the spec until all pass:

- **Contract coverage:** every command that returns data or mutates state has `--json`; the frozen-surface list (step 3) is published, with a JSON Schema per `--json` command.
- **Non-interactive run:** every command run with stdin closed and stdout piped completes, or fails fast naming the missing flag; zero hangs, every wait bounded by a timeout.
- **Exit-code table:** documented, with an automated test per code.
- **Severe-action guard:** every severe operation (step 9) requires name or count confirmation, in the curated commands and the `api` escape hatch alike; no blanket `--yes` skips it.
- **Secret hygiene:** no secret accepted only as a flag; none printed by default, verbose or debug output.

## 1. Name the jobs and audiences

- List the jobs users do with the platform, not the endpoints it has. A job is "deploy this app and tell me when it is live", not `POST /deployments`.
- Mark each job with its audiences from question 1. A job only agents and CI run needs machine output first; a job only humans run needs good prompts and progress first.
- Keep jobs the API cannot do alone (local forwarding, log streaming, scaffolding). They are usually why developers install a CLI at all.

## 2. Choose the command layers and grammar

A request to "mirror every REST endpoint 1:1" is a request for a layer, not a design. Four ways to cover the API (effort and value ordered highest first; efficiency decides):

- effort: `generated layer + curated + raw > curated + raw > generated-only mirror > raw escape hatch only`
- value: `generated layer + curated + raw > curated + raw > generated-only mirror > raw escape hatch only`
- efficiency: `curated + raw > raw escape hatch only > generated layer + curated + raw > generated-only mirror`

- **Default rung: curated workflow commands plus a raw `api` escape hatch.** Hand-design commands for the jobs from step 1; ship `<cli> api <method> <path>` from day one, inheriting auth, pagination, output flags and the severe-action guard. The escape hatch makes every endpoint reachable on day one, so the curated layer never chases 100% coverage.
- **Starved option: a generated resource layer under the curated one.** Full coverage, zero drift, help and completion per endpoint - and a second command tree to name, test and version. Promote it once the OpenAPI spec is checked in CI and escape-hatch usage or automation users show sustained demand for per-endpoint commands. A hand-maintained, drifting spec blocks promotion whatever else holds: the generated layer would freeze the drift into the contract.
- **Rule out the generated-only mirror as the whole surface** whenever question 3 named a multi-call or local job. API-shaped names (`api:serverless:v1:services:create`), path-shaped flags and version namespaces leak into every command, and the jobs that justify the CLI disappear.
- Re-rank against the interview: a hard deadline with a thin team keeps the default; a compounding automation mandate with a CI-checked spec promotes the generated layer; an agent-first audience may add raw JSON payload input (`--json-input '{...}'`) beside convenience flags.
- Write a short answer to whoever asked for the mirror: what is reachable on day one, through which layer, and what promotes the generated layer later.

Grammar rules:

- Default to `noun verb` with plural nouns and a small verb set reused across nouns (`list`, `get`, `create`, `update`, `delete`). Never two near-synonyms (`update`, `upgrade`) for different meanings.
- Choose `verb noun` only when the verbs are uniform across an open-ended set of resource types, as in kubectl.
- Reject prefix abbreviations of commands and a catch-all default subcommand. Both block every future command that collides with them.
- Prefer flags to positional arguments beyond the one obvious target. Accept `-` for stdin and `@file` for payloads.
- Reserve the top-level names an extension or plugin mechanism will need, if one is planned (gh extensions, kubectl plugins).

Vendor examples and a worked "mirror every endpoint" redesign: [references/command-layer-patterns.md](references/command-layer-patterns.md).

## 3. Declare the contract surface

Breakage in a public CLI almost always traces to a contract nobody wrote down. Write it down before any command ships:

- **Frozen (public, versioned):** command and subcommand names, flag names and meanings, environment variable names, config-file keys, `--json` shapes and field names, exit codes, and which stream carries what.
- **Unstable (free to change):** human-readable tables, wording, colors, spinners. State this in the docs, so scripts parse `--json` and never the table.
- Treat the frozen list like the API: additive changes ship freely; anything else follows step 11.
- Under `--json`, adding a field is safe; renaming, retyping or removing one is breaking. Bare `--json` returns a documented default field set, small enough for an agent's context; `--json all` returns full objects; `--json id,status` returns only named fields, which makes later additions invisible to that caller.
- Deprecate a frozen element with a stderr warning naming the replacement, keep an alias through the window, and remove it only in a major release. Kubernetes keeps deprecated GA CLI elements for 12 months or 2 releases, whichever is longer - a usable default.
- Enforce it in CI: publish a JSON Schema per `--json` command and run golden-output contract tests against a live test environment. When the API spec drifts, these tests are what catch it.

## 4. Set flags, configuration and profiles

- Resolve every setting in one documented order: flag > environment variable > project config file > user config file > built-in default.
- Let an explicit token (flag or env var) beat any stored profile, and print a stderr notice when it overrides a logged-in account.
- Give every global setting a flag and an env var with one prefix (`ACME_PROFILE`, `ACME_API_URL`, `ACME_NO_INPUT`).
- Offer named profiles for multiple accounts, orgs, regions or self-hosted base URLs. Bind a project directory to a profile only through a file that holds no secret.
- Store config where the OS expects it (XDG base directories, `%APPDATA%`), and lock it against concurrent writes: agents run commands in parallel, and two processes refreshing one token at once corrupt it.
- Honor `HTTPS_PROXY`, `NO_PROXY` and a custom CA bundle; corporate networks intercept TLS.
- Never require a secret as a flag value: it leaks into `ps` and shell history. Accept it from an env var, a file, or stdin.

## 5. Design output, streams and exit codes

Stream rules, by mode:

- **Human mode (default):** the result goes to stdout; progress, warnings, deprecation notices, update hints and errors go to stderr.
- **`--json` mode:** stdout carries exactly one JSON document per run - the success shape, or `{"error": {...}}` with a stable code, message, request ID and, for async work, the operation ID. stderr stays free text for humans. The exit code is the primary signal; the error object explains it.
- **Streaming commands** (`logs tail`, `listen`): newline-delimited JSON behind `--format ndjson`, mutually exclusive with `--json`; every line carries a `type`, and a fatal error ends the stream with an `error` line before the non-zero exit.
- Detect the TTY: color, spinners, pagers and prompts exist only on a terminal. Honor `NO_COLOR` (present and non-empty), `--no-color` and `TERM=dumb`. Never page output by default when stdout is not a terminal.

Output formats:

- Human tables by default; `--json` on every command that returns data, including mutating and long-running ones - a deploy command without machine output is the most common gap.
- Wrap every list in one envelope from v1 (`data` plus `has_more`/`next_cursor`); moving from a bare array later is breaking. Streaming newline-delimited JSON is a separate, explicit format flag, never a side effect of `--all`.
- Offer an in-CLI filter (`--jq`, a template) only after `--json` itself is stable.

Exit codes - publish one small table, each class a different caller action:

- `0` success, including an idempotent no-op; `1` failure not covered below; `2` usage error.
- Distinct codes for: authentication required; not found; **safe to rerun** (nothing reached the server, or the server refused with 429 or 503 plus `Retry-After`); **outcome unknown** (any other 5xx or timeout after sending a non-idempotent call) - check with `wait <operation-id>` or `get`, never rerun blind; **partial failure** in bulk operations - read the per-item results. A call carrying an idempotency key the caller controls moves from outcome-unknown to safe-to-rerun.
- Avoid BSD sysexits as a portability promise (current FreeBSD documentation deprecates them) and the shell-reserved range above 125.

Full stream matrix, JSON conventions, error object and table template: [references/output-and-exit-code-contract.md](references/output-and-exit-code-contract.md).

## 6. Design auth and credential storage

Login flows stack - each serves a context, so they are not ranked against each other:

- **Desktop:** authorization code with PKCE and a loopback redirect (RFC 8252); the browser opens, the CLI catches the redirect on localhost.
- **No local browser or port (SSH, containers, remote dev boxes):** OAuth device authorization grant (RFC 8628). It is phishable - attackers can send a user code - so require short-lived codes and a consent screen naming the requesting client from the authorization server.
- **CI and scripts:** a scoped, expiring token in an env var. Document it as the CI path, never a browser flow.
- **API keys only:** `login` reads a key from stdin or opens the dashboard page that creates one; store it like any credential; show test or live mode in every prompt and in `auth status`. List scoped, expiring keys as an API-side dependency in the spec.

Rules:

- Store interactive credentials in the OS credential store. When none exists, warn loudly before writing a plaintext file with owner-only permissions.
- Provide `auth status` (identity, which source won, expiry, mode) and `auth logout`. Leave out a print-the-token command unless a named integration needs the handoff: malware has harvested tokens at scale through exactly such a command.
- Redact secrets from every output by default, including verbose, debug and HTTP-trace modes and CI logs.
- Token formats, scopes and the authorization server belong to `samber/developer-platform-skills@api-auth-key-management` and `samber/developer-platform-skills@oauth2-provider-design`.

Flow details, storage fallbacks and leak incidents: [references/auth-and-credentials.md](references/auth-and-credentials.md).

## 7. Handle lists, long-running operations and retries

- Give list commands a bounded default `--limit` and an explicit `--all`, and carry truncation inside the `--json` envelope. A silently truncated first page reads as the complete answer to a script or an agent.
- Keep display paging (a pager) and API pagination separate, with separate flags.
- Wait by default for asynchronous mutations in every context, with progress on stderr and a finite default `--wait-timeout` stated in the spec. The `--json` shape stays the same whether the command waited or not.
- Offer `--no-wait` that returns the operation ID, and a `wait <operation-id>` command that resumes.
- On Ctrl-C or SIGTERM (a cancelled CI job) during a wait, detach rather than cancel: print the operation ID and the resume command. Cancelling server-side work is its own explicit command.
- Make create commands safe to retry: send one idempotency key per invocation, reuse it on automatic retries, and accept `--idempotency-key` - a script that reruns a command is safe only when it passes its own key. Key semantics belong to `samber/developer-platform-skills@api-idempotency-retry`.
- Retry transient failures automatically with bounded backoff, honoring `Retry-After`.

## 8. Write errors and help

- Rewrite API errors for the reader: what failed, why, and the next command to run. Keep the API error code and request ID in every error. The taxonomy belongs to `samber/developer-platform-skills@api-error-design`.
- Suggest the closest command or flag on a typo, and never auto-run the suggestion: it may change state, and it commits you to supporting the typo forever.
- Reject unknown flags by name before any API call, listing valid ones. A silently ignored flag produces plausible, wrongly scoped results.
- Make `<cli>`, `<cli> help <cmd>`, `<cmd> --help` and `-h` all work. Lead each command's help with two or three examples, then flags with defaults, then a docs link.
- Document cross-cutting contracts once as help topics: output formats, exit codes, environment variables.
- Offer `--debug` with a redacted HTTP trace, and ship shell completion from the first release.

## 9. Make it safe without a terminal

- When stdin is not a terminal, never prompt: fail immediately naming the flag that supplies the missing value. Add `--no-input` to force this on a terminal too.
- Grade every operation in one table that the curated commands and the `api` escape hatch both read, keyed by command and by method plus path:
  - mild (reversible, own resources): no confirmation;
  - moderate: confirm on a terminal, `--yes` to skip;
  - severe (irreversible, reaches third parties such as emails or payouts, moves money, or touches shared resources): type the resource name, or `--confirm=<name>` non-interactively; bulk operations confirm the count (`--confirm-count=<n>`). `--yes` never skips a severe confirmation.
- Without that shared table, `api delete ...` bypasses every guard the curated layer carries. Treat GraphQL mutations through the escape hatch as severe unless the table names them.
- Offer `--dry-run` on every mutating command where the API can validate without committing.
- Keep update checks, first-run notices and telemetry banners silent off-TTY.

## 10. Make it agent-ready

Agent-readiness is mostly steps 3-9 done well. Coding-agent vendors steer agents toward installed CLIs, so the CLI is often the surface agents meet first. Add on top:

- **Self-description:** a command that prints the command tree, flags and `--json` schemas as JSON, so an agent learns the surface without scraping help text.
- **Bounded, decisive output:** small default fields and limits, totals, explicit empty results ("0 deployments found"), truncation markers naming the flag that shows more.
- **Input hardening:** validate identifiers, paths and payloads as untrusted; an agent hallucinating `../../` into a path must hit a validation error.
- **Credentials as the real boundary:** a confirmation stops mistakes, not an agent set on proceeding - it can read the name from its own output. What bounds an agent is the token it holds: default to test mode, offer read-only and narrowly scoped tokens, and document which to give an agent.

Shipping an Agent Skill inside the CLI's repo belongs to `samber/developer-platform-skills@agent-skill-offering`; an MCP server beside the CLI belongs to `samber/developer-platform-skills@mcp-server-offering`. Evidence on CLI versus MCP for agents is mixed - check [references/agent-readiness-and-incidents.md](references/agent-readiness-and-incidents.md) before citing any figure.

## 11. Set versioning, deprecation, updates and telemetry

- Version the CLI with SemVer, separately from the API. Pin each CLI release to an explicit API version and offer an override flag; the API's own policy belongs to `samber/developer-platform-skills@api-versioning-policy`.
- Check for updates at most daily, only on a terminal, never in CI, with an env var to disable it. Never self-update without consent.
- Shipping the CLI itself - binaries per platform, Homebrew tap, deb/rpm, language registries, signing - belongs to `samber/developer-platform-skills@sdk-package-publishing`.

Telemetry posture:

- trust: `opt-in > opt-out with first-run notice`
- signal value: `opt-out with first-run notice > opt-in`
- compliance cost, highest first: `opt-out with first-run notice > opt-in` (a pseudonymous device ID collected by default is a consent question under EU rules; opt-in carries consent by construction)
- **Default rung: opt-out with a first-run notice**, announced ahead of the release that enables it and shipped in a major version, honoring `DO_NOT_TRACK` and a CLI-specific off switch, payload schema published, collection off against self-hosted or enterprise targets.
- **Starved option: opt-in**, which clig.dev prefers. Promote it when question 7 shows an EU-heavy, regulated or enterprise audience, or an open-source community that already distrusts the vendor.
- **Rule out turning collection on in a minor release with only release notes as notice.** Even a documented, switchable default drew backlash that way: [references/agent-readiness-and-incidents.md](references/agent-readiness-and-incidents.md).

## Failure modes

Each maps to the step that prevents it:

- A 1:1 endpoint mirror shipped as the whole CLI (step 2).
- Scripts parsing human tables because `--json` is missing (steps 3, 5).
- A prompt, pager or update check reachable in CI, hanging the job (steps 5, 9).
- Error text on stdout in `--json` mode, or JSON mixed into a progress stream (step 5).
- A script rerunning a create after a timeout and duplicating it (steps 5, 7).
- A plaintext token fallback with no warning, or secrets echoed into CI logs (step 6).
- `api delete` skipping the guard the curated `delete` enforces (step 9).
- A flag renamed in a minor release with no alias or warning (step 3).
- Telemetry switched on in a minor release with no advance notice or first-run notice (step 11).

Track after launch, as trends rather than thresholds: share of API traffic from the CLI's user agent (server-side logs), `api` escape-hatch usage per endpoint (a busy endpoint is a curated-command candidate), and top error codes per command.

## Invocation examples

- "We're building our first CLI and product wants one command per REST endpoint - design it."
- "Our CLI's `deploy` hangs in GitHub Actions and agents keep parsing the table output - fix the interface."
- "Design login for our CLI: devs on laptops, SSH boxes and CI, and we only have API keys."
- "We need to rename three flags and drop a command without breaking customer scripts."

## References

- [references/command-layer-patterns.md](references/command-layer-patterns.md) - vendor grammar and layering, and a worked redesign of a 1:1 mirror request.
- [references/output-and-exit-code-contract.md](references/output-and-exit-code-contract.md) - stream matrix, JSON conventions, error object, exit-code table template.
- [references/auth-and-credentials.md](references/auth-and-credentials.md) - per-context login flows, precedence, storage fallbacks, leak incidents.
- [references/agent-readiness-and-incidents.md](references/agent-readiness-and-incidents.md) - agent requirements, CLI-versus-MCP evidence with quality labels, documented failures.
- [references/cli-design-spec-template.md](references/cli-design-spec-template.md) - the deliverable.
- `samber/developer-platform-skills@developer-portal-design` - where the CLI reference, install guide and token page live.
- `samber/developer-platform-skills@github-action-offering` - the GitHub Action and CI ports that wrap this CLI; its contract inherits the CLI's flags and exit codes.
- `samber/developer-platform-skills@ide-extension-offering` - the VS Code or JetBrains extension that wraps this CLI and reuses its login.
- `samber/developer-platform-skills@agent-integration-surfaces` - which agent classes get the skill-plus-CLI path, and how agent calls through the CLI are authenticated and counted.
