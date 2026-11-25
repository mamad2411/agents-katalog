---
name: cloudflare-artifacts-interface
description: Operate Cloudflare Artifacts, Cloudflare's Git-compatible versioned storage for agents, from an agent session through the REST API, Wrangler, a Worker binding, or plain git. Use when someone wants a repo per agent, session, task, or user; wants to create, fork, import, list, read, or delete Artifacts repos or namespaces; needs a read or write token for git clone/push; wants to hand a workspace to another agent or reviewer; wants to read files from a repo without cloning; wants to clean up stale repos or check cost; or mentions "Artifacts", "artifacts.cloudflare.net", "art_v1_" tokens, "env.ARTIFACTS", or "wrangler artifacts". Supplies the three-credential model (API token for control, repo token for git, binding inside a Worker), safety tiers that put deletes, namespace jurisdictions, and long-lived write tokens behind a confirmation, token hygiene (never persist a token in .git/config), naming that avoids collisions, and the billing and size limits that make bulk creation a decision.
---

# Cloudflare Artifacts Interface

> **Status: Draft (2026-10-25).** Built from Cloudflare's Artifacts docs
> (pages last updated between 2026-04-25 and 2026-10-22). Artifacts is in
> **open beta** (since 2026-10-01). **Tested live 2026-10-25:** token
> verification; listing and getting namespaces; listing and creating repos;
> minting write tokens; header-auth push from a local clone; Worker-side
> clone, commit, and concurrent push with isomorphic-git; REST log reads; and
> the credential behavior in [Gotchas](#gotchas). **Not yet tested:** fork,
> import, delete, and token revocation. Anything marked
> *(verify)* is a belief to confirm on first use. When
> a live call disagrees with this file, the live call wins. Fix the file.

**Artifacts is Git hosting built for agents.** Each repo is an isolated Git
service with its own remote URL, its own tokens, and durable, replicated
storage. You can make one repo per agent, session, task, or user, millions
of them, and any git client can clone and push.

> *"Give this agent its own workspace"*, *"fork the baseline for this
> session"*, *"let the reviewer read it but not push"*, *"what's in that
> repo's README?"*, *"clean up last week's session repos"*.

## 0. Resolve the account first

Read `config/private.json` (gitignored; shape in `config/private.example.json`).
It says which Cloudflare account to use, which environment variables hold
the account ID and API token and where they're loaded from, which namespaces
exist and what each is for, and the repo naming pattern.

- **If the file or the account entry is missing, say so and ask. Don't
  guess.** Repos created in the wrong account are billed to it and visible
  to it.
- Never copy a value from that file into this one. This skill is public.
- Never print a token. To check one exists, print the variable's *name*.

## The model

| Thing | What it is |
|---|---|
| **Namespace** | Top-level container. Groups repos by environment, tenant, or shard. Created implicitly by the first repo that names it, or explicitly (needed to set a jurisdiction). Name: 2–63 chars, starts with a letter or digit, then letters, digits, `.`, `_`, `-` |
| **Repo** | One isolated Git service. Address = namespace + name, unique **within** the namespace. APIs also return an opaque repo `id` |
| **Remote** | `https://<ACCOUNT_ID>.artifacts.cloudflare.net/git/<namespace>/<repo>.git`. **Use the `remote` returned by the API**, never a hand-built one |
| **Repo token** | `art_v1_<40 hex>?expires=<unix seconds>`. Scoped to **one repo**, `read` or `write`, TTL 60 s to 1 year |
| **Fork** | A new repo starting from another's history, then diverging, with its own tokens. `read_only` and `default_branch_only` options |
| **Read-only repo** | A repo flagged `read_only` at create, fork, or import: a fixed baseline nobody can push to |

Three surfaces reach the same repos ([`references/api-map.md`](references/api-map.md)):

- **Control plane:** the REST API, Wrangler, or a Worker binding. Creates,
  lists, forks, imports, deletes, mints tokens, reads files.
- **Data plane:** plain git over HTTPS (smart HTTP). Clone, fetch, pull, push.

## Three credentials, never interchangeable

| Credential | Used for | Where it comes from |
|---|---|---|
| **Cloudflare API token** | REST control plane, as `Authorization: Bearer` | Cloudflare dashboard, with **Artifacts → Read** (reads) and **Artifacts → Edit** (writes) |
| **Repo token** (`art_v1_…`) | git clone/fetch/pull (`read`), push (`write`) | Minted by the control plane, per repo |
| **Worker binding** (`env.ARTIFACTS`) | Control plane from inside a Worker, no token in code | `artifacts` block in the Wrangler config, bound to one namespace |

An API token never works for git, and a repo token never works for REST.
Wrangler uses its own login (`wrangler login`, or an API token in CI).

## Ground yourself before anything else

1. Load the credentials named in config, then **check the token** with
   `GET /accounts/$ACCOUNT_ID/tokens/verify` (see Gotchas for why not
   `/user/tokens/verify`).
2. **List namespaces** (`GET /accounts/$ACCOUNT_ID/artifacts/namespaces`).
   If it fails with code `10000`, the token lacks Artifacts permission, or
   the account isn't on Workers Paid. Stop and say which to fix. Don't
   retry other routes hoping one works.
3. Before creating anything, **list repos** in the target namespace
   (`?search=` narrows it). Names collide within a namespace; an
   `ALREADY_EXISTS` (10201) is a sign you were about to reuse someone's
   workspace.

## Safety — four tiers

| Tier | What | Rule |
|---|---|---|
| **0 · Read** | list/get namespaces and repos, log, commit, tree, blob, file reads, list tokens, `read` tokens with short TTL, git clone/fetch | Free to do. Reads still count as billed operations, so don't poll in a loop |
| **1 · Create and write** | create a repo, fork, import, push to a repo this session owns, mint a `write` token of a few hours or less | Fine within the task the person asked for. Name repos per the naming rule. Tell the person what was created and where |
| **2 · Destructive** | **delete a repo** (no restore is documented), delete a namespace, force-push or delete refs on a repo you didn't create, revoke a token another agent may be using | **Propose, then wait for a yes.** List exactly what goes. For cleanups, show the table (name, created, last push) first |
| **3 · Account-level or lasting** | create a namespace **with a jurisdiction** (permanent: it can't be changed later), mint a `write` token longer than a day, bulk-create repos in a loop, import into a shared baseline | Ask first and say why it's lasting. A jurisdiction namespace is permanent. A long write token is a standing credential. Bulk creation is billed |

Billing started 2026-10-14 (Workers Paid only): the first 10,000 operations
and 1 GB-month are included each month, then **$0.15 per 1,000 operations**
and **$0.50 per GB-month**. Operations include create, push, pull, and clone.
Repos stay stored, and billed, **until deleted**. A script that makes a repo
per item is a cost decision. Say the expected count before running it.

## Tokens: handle them like passwords

- **Mint the narrowest token, for the shortest time.** `read` unless the
  client must push. Re-mint per session rather than sharing one.
- **Always pass `scope` explicitly.** `POST /tokens` **defaults to `write`**
  with a 24-hour TTL. Create, fork, and import responses also return a token.
  Treat it as write-capable *(verify the scope)* and don't hand it to a
  reader.
- **Never put a token in a remote URL that persists.**
  `git clone https://x:<token>@…` writes the token into `.git/config`, where
  it outlives the session and gets copied with the folder. Use the header
  form, which keeps it out of config:

  ```sh
  git -c http.extraHeader="Authorization: Bearer $ARTIFACTS_TOKEN" clone "$ARTIFACTS_REMOTE" work
  git -C work -c http.extraHeader="Authorization: Bearer $ARTIFACTS_TOKEN" push origin HEAD:main
  ```

  Bearer takes the **full** token string, `?expires=` included. The Basic
  (URL) form takes the token **without** the `?expires=…` suffix. Use the URL
  form only for a one-shot command into a throwaway directory.
- **Read expiry from the token.** The unix timestamp after `?expires=` is the
  expiry. Check it before a long job rather than failing halfway through.
- **Revoke when done** (`DELETE …/tokens/:id`). Tokens are listable per repo
  with `state=active|expired|revoked|all`.
- Never log a token, echo it, or paste it into a doc, a handoff, or a commit.

## Naming: unique, and parseable later

Repo names are unique only within a namespace, so a short shared name like
`docs-site` will collide. Use a pattern with stable identifiers, by default
`<agent>-<session-or-task>-<purpose>` (the config may set another). The name
is also how cleanup finds things later: a name that says whose and when is
what makes "delete last week's session repos" safe.

Namespaces separate **lifecycles and traffic**, not units of work: e.g.
`staging` vs `prod`, or one per tenant. The rate limit is per namespace
(2,000 control-plane requests per 10 s), so a hot workload gets its own.

## Recurring jobs

### A. Give an agent or session its own workspace

1. Pick the namespace from config. Build the name from the naming pattern.
2. If a baseline exists, **fork** it (`default_branch_only: true` unless
   other branches are needed). Otherwise **create**.
3. Mint a `write` token with a TTL matching the session (hours, not days).
4. Clone with the header form, work, commit, push.
5. Record the repo's **namespace/name and remote** (never the token) wherever
   the work is tracked: a handoff doc, a PR, the task.

### B. Let someone read without pushing

Mint a `read` token with a short TTL (minutes to hours) for that repo only.
For a frozen snapshot that must not change under the reader, fork with
`read_only: true` and give a read token on the fork.

### C. Bring in an existing repo

- **Public HTTPS remote:** `POST …/repos/<name>/import` with `url`, and
  optionally `branch` and `depth`. Import is **asynchronous**: follow-up calls
  can return `409` or `IMPORT_IN_PROGRESS` (10302). Retry with a short delay.
  Don't create a second repo.
- **Private remote:** import returns `REMOTE_AUTH_REQUIRED` (10106); it only
  pulls public remotes. Instead, create an empty repo, then push from a local
  clone with a write token: `git push <remote> --all` and `--tags`.
- For a template, import once into a baseline, mark it read-only, and
  **fork** from it per session.

### D. Read a file without cloning

`GET …/repos/<name>/file?ref=main&path=README.md` returns the raw bytes. So
does `…/raw/<ref>/<path>`, with a guessed `Content-Type`. `…/log?ref=main&limit=10`
gives history. Cheaper than a clone for one file, and needs only the API token.

### E. Clean up

1. List repos sorted by `last_push_at` (or `created_at`), filtered with
   `search` on the naming prefix.
2. Propose a table: name, created, last push, why it's stale.
3. On a yes, delete (`202 Accepted`; the repo disappears asynchronously). A
   namespace can only be deleted once it's empty (`409` otherwise).
4. Revoke any active tokens you minted for those repos.

### F. Keep agent context with the work

Attach prompts, model output, and run IDs to commits with **git notes**
rather than files in the tree:

```sh
git notes add -m 'user: <prompt>' HEAD
git notes append -m 'assistant: <summary>' HEAD
git push origin 'refs/notes/*'
```

Notes live on their own refs and **don't travel unless pushed and fetched
explicitly**.

## Gotchas

- **Missing permission looks like bad auth.** Tested 2026-10-25: a valid,
  active account-owned token with no Artifacts permission got
  `{"code":10000,"message":"Authentication error"}` from the Artifacts
  routes, while the same token read Workers fine. Add **Artifacts →
  Read/Edit** to the token. Don't rotate it.
- **Account-owned tokens do work for Artifacts.** Tested 2026-10-25: a
  `cfat_…` account API token (Manage Account → Account API tokens) listed
  Artifacts namespaces, even though Artifacts is missing from Cloudflare's
  account-token compatibility list. Prefer an account token for automation:
  it isn't tied to a person who might leave.
- **An account token also gives R2 S3 credentials.** The token's `id` is the
  S3 Access Key ID, and the secret access key is the SHA-256 hex of the token
  value. That's a quick local check that a copied token and secret belong
  together.
- **Account-owned tokens fail the user verify endpoint.** Tested 2026-10-25:
  `GET /user/tokens/verify` answers `Invalid API Token` (code 1000) for an
  account-owned token that
  `GET /accounts/$ACCOUNT_ID/tokens/verify` reports as `active`. Verify on the
  account route first.
- **Old URLs in early posts.** The April 2026 beta announcement shows
  `https://artifacts.cloudflare.net/v1/api/namespaces/…` for REST and remotes
  without the account subdomain. Current docs use
  `https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/artifacts/…` and
  `https://<ACCOUNT_ID>.artifacts.cloudflare.net/git/…`. Use the current
  ones, and the `remote` the API returns.
- **1 GB per repo** for repos created on or after 2026-09-29 (older repos
  keep 10 GB). 1 TB per account, raisable. Large binaries belong in R2, not
  here.
- **Wrangler can't do everything.** `wrangler artifacts` lists and gets
  namespaces, and creates, lists, gets, deletes, and issues tokens for repos.
  It **doesn't create namespaces (so no jurisdiction), fork, or import**: use
  REST or the binding for those. `repos delete` prompts for confirmation
  unless `--force`/`-y`. Don't pass `-y` without a yes from the person.
- **Push is git protocol v1 only**, and some optional v1 fetch capabilities
  (`filter`, `include-tag`) aren't supported. So `git clone --filter=…`
  partial clones may not work *(verify)*. For large repos in sandboxes, use
  ArtifactFS (below).
- **Error codes**: `NOT_FOUND` 10200, `ALREADY_EXISTS` 10201,
  `INVALID_INPUT` 10100, `INVALID_REPO_NAME` 10101, `INVALID_TTL` 10103,
  `INVALID_URL` 10104, `REMOTE_AUTH_REQUIRED` 10106, `IMPORT_IN_PROGRESS`
  10302, `FORK_IN_PROGRESS` 10303, `INTERNAL_ERROR` 10400,
  `UPSTREAM_UNAVAILABLE` 10401, `MEMORY_LIMIT` 10402. The `…_IN_PROGRESS`
  codes and `UPSTREAM_UNAVAILABLE` are retryable; the rest aren't.
- **Writing from a Worker means isomorphic-git, and Cloudflare's example
  filesystem is incomplete.** The binding can create repos and mint tokens but
  can't write files, so a Worker clones into memory, commits, and pushes with
  `isomorphic-git`. Tested 2026-10-25 with isomorphic-git 1.44.4: the
  `MemoryFS` helper in Cloudflare's isomorphic-git example fails on clone with
  `Cannot read properties of undefined (reading 'bind')`, because
  isomorphic-git binds `readlink` and `symlink` on every fs and the helper
  lacks both. Its errors also carry no `code`, and isomorphic-git checks
  `err.code === "ENOENT"`. Add both methods, and throw errors with a Node-style
  `code`. Reference implementation: `self-host-stack/hubs/event-hog-mcp/src/memory-fs.ts`.
- **Concurrent pushes from a Worker: retry from a fresh clone.** Tested
  2026-10-25: two simultaneous writes to one repo both landed when each
  rejected push re-cloned and re-applied its change. Design writes to add
  files or append, so a retry can't clobber a teammate's work.
- **Jurisdiction is per namespace and permanent** (`eu` or `us`; omit it for
  unrestricted). A client with data-residency needs gets its own namespace,
  created explicitly before the first repo. A repo created first makes the
  namespace implicitly, *without* a jurisdiction.

## Large repos: ArtifactFS

`artifact-fs` (`go install github.com/cloudflare/artifact-fs/cmd/artifact-fs@latest`)
mounts a repo through FUSE after a blobless clone; file contents hydrate as
they're read. Use it when sandbox startup time matters more than a full
clone. It needs FUSE on the host and an authenticated remote. Use a
short-lived read token, since that URL form embeds the token. For small repos
a normal clone is simpler.

## Relationship to Cloudflare's own skills

Wrangler offers `--install-skills` to install Cloudflare's agent skills, and
the Artifacts docs ship a copy-paste setup prompt for coding agents. **If
both are present, they may fire on the same requests** *(verify whether an
Artifacts-specific Cloudflare skill exists)*. Theirs is the map of the API.
This one is the operating layer: credentials, tiers, token hygiene, naming,
cleanup, and cost. Where they disagree on a **fact** (a route, a field, a
limit), theirs and the live docs win. Where they disagree on **what to do**,
this one does.

## See also

- [`references/api-map.md`](references/api-map.md): every operation across REST, Wrangler, and the Worker binding, tiered
- Docs index (markdown, agent-readable): `https://developers.cloudflare.com/artifacts/llms.txt`. Any page is fetchable as markdown with `Accept: text/markdown`
- Events (repo created/deleted/forked/imported, pushed/cloned/fetched, token created/revoked): `developers.cloudflare.com/artifacts/guides/event-subscriptions/`
- Build and deploy a Worker on push: `developers.cloudflare.com/artifacts/guides/build-and-deploy-on-push/`
