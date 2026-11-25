---
name: inno-new-app
description: Use when the user wants to create a new app on the Innovation Platform ("new app", "create an app", "start a project on inno-platform"). Guides intake, creates a repo from the instance's template repo in the user's own account, calls register_app, commits the proof-of-control file it names and has them install the platform GitHub App, calls register_app again to provision + bind it, then scaffolds app/ per platform-conventions.
---

# inno-new-app

## Version gate: do this first

Before anything else in this skill, do these five steps in order.

1. If no `inno-platform` tools are available at all, the platform address is
   probably unset. Tell the user to open their platform's panel, copy the
   configure command from its Connect Claude Code card, run it in a terminal,
   and restart Claude Code. Then STOP.
2. Read the `version` field of `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`
   and call the `get_platform_status` MCP tool with it as `plugin_version`.
3. If the `Plugin:` line says `OUTDATED`, `version not reported`, or
   `reported version is not a MAJOR.MINOR.PATCH triple`, STOP. Tell the user
   to run the commands that line gives, then restart Claude Code and start
   again. Do not continue on a stale plugin: its guidance may describe
   platform behavior that no longer exists. If there is no `Plugin:` line at
   all, the platform sets no minimum version: go on to the next step.
4. If the `Plugin:` line says `current` and adds that a newer version
   `is available`, that is advice, not a block. Mention it once, with the
   commands from the `Update commands:` line, and go on to the next step.
5. If the status has no `Template repo:` line, the platform is older than
   v0.15.8. Say so, ask the user's admin to upgrade it, and STOP before any
   step that needs an instance value. Never fall back to a literal value.

Carry on.

Creates a new Innovation Platform app end to end: intake -> the user creates a
repo **they own** from the platform template -> `register_app` (first call)
-> commit the proof-of-control file it names + install the platform GitHub App
-> `register_app` (second call) provisions + binds it -> pull + scaffold. Requires the
`inno-platform` MCP server (ships with this plugin's `.mcp.json`) to be
connected. The first call to any `inno-platform` tool triggers an Okta browser
login. That's expected, not an error: wait for it to complete. **If the
connector wasn't already authorized when the session started, waiting isn't
enough**: mid-session authorization alone does not expose the tools (the MCP
client enumerates tools at startup); the user must authorize it AND you must
restart the session before calling any `inno-platform` tool.

**The repo is the USER's.** There is no platform-owned repo model anymore. The
repo lives in the user's **own** account or org, created from the instance's public
template repo (the `Template repo:` line of the status you read in the Version
gate), with the platform's GitHub App installed on it; `register_app`
finishes the job. The platform never creates a repo on the user's behalf.

**What is genuinely user-only.** Exactly two steps in this flow require the user
personally: **installing the platform GitHub App** (§3: a third-party token
cannot install a GitHub App on someone's account) and any **browser SSO login**.
Everything else (creating the repo, committing the registration proof file,
cloning, scaffolding, committing, pushing, tagging, setting variables) you can
do with the user's own authenticated CLI and MCP tools. Never tell the user something "can't be done from here" unless it
is one of those two. Where the reason is judgment rather than capability, say
which: setting a *secret* variable is a **should not** (it would put the secret
in the conversation transcript), not a **cannot**.

**Already have an existing repo?** If the user wants to put a repo/codebase they
*already* have on the platform (not create a fresh one from the template), use
the `inno-migrate-app` skill instead: it registers the existing repo in place
and adapts it to the contract, with no scaffolding from the template.

**Speak the user's language.** Plain terms with the user, no provider or
product names unless they have shown technical fluency. The full rule is the
plugin README's **House style** section, and it applies to every user-facing
sentence in this flow.

## 1. Intake: ask the user for five things

1. **App name**: lowercase letters, digits, hyphens only, 3-29 chars,
   starting with a letter. This drives the app's **hostname** on the platform
   domain (the `App host pattern:` line of the status you read in the Version gate, with the app's name in place of `{app}`; `register_app`'s answer gives the real hostname), so keep it short and DNS-safe. It is NOT
   the repo name, which is the user's choice (see below). A handful of
   names are reserved server-side; `check_name` reports those, so don't
   enumerate or guess. A name ending in **`-app`** is rejected as well: the
   server returns `invalid_name` for `todo-app`, so propose `todo` instead.
   Steer the user off that suffix before you check the name.

   **Verify availability before you settle on a name: never recommend or
   confirm a name without checking it first.** (This step is the plugin's one
   home for the name rules and the registration-time active-app check, whose
   rule is `inno-manage-app`'s; `inno-migrate-app` points here.) Call the **`check_name`** MCP
   tool (read-only; provisions nothing) on the candidate. Only proceed with a
   name it reports as **available**. If it comes back in-use, reserved, or
   invalid, ask the user for a different one; a name it refuses as unusable is
   echoed back inside `«»` guillemets, which fence it as untrusted text rather
   than marking it as quoted by the user. If it says the name **was
   recently purged and is held until** a UTC time, nobody, admins included,
   can register it before then: offer a different name or wait. If it's the
   caller's *own* existing app, tell them that (a stopped app is brought back
   with `start_app`, not by re-registering it). `list_apps` cannot prove a
   name is free, since an ordinary user sees only their own apps there: use
   `check_name`.

   **Active-app limit.** `check_name` also warns when the user is at their
   active-app limit. At the cap, `register_app` WILL fail with
   `app_limit_reached`, so resolve this BEFORE any build work. Report the
   limit factually and name the remedies, the rule `inno-manage-app` sets for
   `start_app`: the user stops one of their own apps when THEY choose to, or
   a platform admin raises their limit (`apps.max_active`, user scope). **Do
   NOT propose or offer to stop specific apps to make room**; that trade-off
   is the user's to initiate. If the user asks to stop one, `stop_app` it
   only with their explicit confirmation by name (stopping detaches the app's
   domain and starts its purge countdown). Otherwise stop here: an admin
   raising the limit, or not building the app, are the remaining options.
2. **Repo**: the `owner/repo` slug of the GitHub repo the user will create
   from the template (§2). The **owner is the user's** account or org, and the
   repo name is **their choice**: suggest the app name itself, but it
   is not required and can be anything. The repo may be public or private.
3. **One-line purpose**: becomes the app's `description` (at most 500
   characters; the tool schema rejects a longer one).
4. **Initial members' emails** (optional, can be empty): Okta emails to grant
   access alongside the owner. The list can be added to later with the
   `inno-manage-app` skill's `grant_access`.
5. **Does the app need to reach another service *as each person using it*?**
   Not the app's own sign-in (every app gets that for free): this is about
   your app calling out to some *other* system that also tells its own users
   apart (a departmental system, a niche tool, a per-user account on some
   outside service). If yes, note it now: today that only works for an MCP
   server built the container way (affects the type choice in §1b below), and
   once the app is registered you'll set it up with the `inno-add-connection`
   skill.

## 1a. Guardrails check: HARD STOP on conflict

Before confirming anything, call the **`get_guardrails`** MCP tool and evaluate
the proposed **name** and **purpose** against the platform's acceptable-use
policy. This is qualitative judgment (impersonation, misleading authority,
offensive names, prohibited purposes, data handling): apply the policy's
spirit, not just its examples. `register_app` requires you to pass
`accept_guardrails: true`, which asserts the app will follow these guardrails,
so do not pass it until you've actually done this review.

- **Clean** → proceed; no need to mention it unless the user asks.
- **Conflict** → do NOT call `register_app`. Name the specific policy line,
  explain the problem in one plain sentence, and help the user pick a compliant
  name/purpose. If they believe their use is legitimate anyway (e.g. sanctioned
  research), direct them to a platform admin for an explicit exception first:
  you cannot grant one, and you must not register the app without it.

Confirm the name, repo, purpose, and members back to the user before going
further: registration provisions real resources (a database and file
storage, and for a browser app a sign-in in front of its address) and binds
them to the user's repo.

## 1b. Design the app before registering

Before registering, produce and present a real design. The approval gate at the
end of this section is a hard one: `register_app` provisions real resources.

**Fetch the contract first:** call the `get_app_contract` MCP tool with
`sections: ["1", "1.1", "1.2", "1.3", "3", "4", "5"]`. Those sections carry
the four deployment **types** and their requirement deltas (§1.1 to §1.3),
the recommendations (§3), the stack policy (§4), and the deployment patterns
with what the platform does NOT support (§5: background jobs,
machine-to-machine APIs, guaranteed long-lived connections); the answer
opens with the contract version and the current recommended base images.
If `get_app_contract` refuses the arguments, or the platform is older than
v0.16.14, call it with no arguments and read the sections needed from the
whole contract. Evaluate the user's idea against it before designing; a
not-supported requirement surfaces HERE, not after registration.

For an app people will open in a browser (a `container` or `function`
design), **fetch `get_app_accessibility` beside it.** It serves the
platform's accessibility notes (WCAG 2.2 AA as the target; a school's own
policy governs where it has one), and its defaults shape the design's
Accessibility line below and the scaffold in §4. The two MCP types have no
browser UI, so it does not apply to them.

Invoke the **`superpowers:brainstorming`** skill to design the app: what it does,
its data model (what it stores: tables, files), its routes/pages, and its
access model (who can see and edit). If that skill isn't available in the
session, run an equivalent inline pass over the same points yourself. Either
way, the design still has to be written into your reply and approved (see
"Present the design, THEN ask for approval" below); the skill's absence is not a
reason to skip that.

The design includes three contract-informed choices that are **the user's to
make, with your recommendation**:

- **Deployment type**: `function`, `container`, `mcp-function`, or
  `mcp-container` (passed to `register_app`; the server defaults to
  container, but for a **greenfield** app you recommend and default to
  **`function`**, or **`mcp-function`**/**`mcp-container`** when the product
  is an MCP server). Pass only these four names. The four types:

  - **`function` (recommend for greenfield):** the app is its own Cloudflare
    Worker (JS/TS) behind the gateway: ms cold starts and no Dockerfile. This
    is the right fit for the common citizen-dev shape (a small web UI + JSON
    API in TS/JS).
  - **`container`:** choose this when the description gives a **clear signal**
    for it: an explicit **non-TS/JS stack** (Python, Go, Ruby, ...), **native
    dependencies** or system binaries, **long-running / heavy compute**, or a
    port of existing non-JS code (that's `inno-migrate-app`, which defaults to
    container). Absent such a signal, prefer function.
  - **`mcp-function`:** choose when the product is an **MCP server for AI
    assistants** (Claude Code, claude.ai) rather than a browser UI. It is
    function-shaped (JS/TS, no Dockerfile) and serves MCP at `POST /mcp`;
    users add the app's MCP address (the `App MCP address pattern:` line, with
    the app's name in place of `{app}`) as an MCP server in their client.
    **Stateless only** (§1.2): tools work normally, but server-initiated
    features (notifications, sampling, elicitation, long-lived subscriptions)
    do not; if the design needs those, it does not fit this type today, so
    surface that HERE, not after registration. Access is given and taken away
    with the same tools as the other types (`grant_access`, `revoke_access`,
    `set_app_access`); there is no browser SSO, and §1.2 says what admits a
    caller. **One hard constraint:** if §1 flagged that the app must reach
    another service *as each person using it* (a per-user **Connection**),
    this type **cannot**: only `mcp-container` can consume a Connection in
    v1. Choose `mcp-container` instead; do not land such an app on
    `mcp-function` and discover the gap after registration (the type is
    fixed at registration).
    **Idle clock:** an MCP app that is built and then left connected but
    unused is warned and then stopped like any idle app. What counts as use
    is served from one place, the **Lifecycle (idle clock)** section of
    `get_platform_docs`, and `inno-manage-app`'s lifecycle section points to
    it: fetch and quote that sentence rather than describing the rule in your
    own words. Tell the user when you hand the app over (`inno-manage-app`).
  - **`mcp-container`:** choose when the product is an **MCP server** that
    needs the **container** shape instead: a **non-TS/JS stack**, **native
    dependencies**, **heavy/long-running compute** a Cloudflare Worker can't
    give it, **or an MCP server that must consume a per-user Connection**
    (this is the only type that can, in v1; see `inno-add-connection`). It
    is `mcp-function`'s MCP contract (`POST /mcp`, **stateless only**, no
    browser SSO) on the container baseline (§1.3). Default stack: **Python +
    the official MCP Python SDK** (FastMCP).
    CRITICAL (Python SDK): keep the starter's `transport_security` setting,
    which `get_app_contract` §1.3 states and explains; changing it breaks every
    gateway-forwarded `/mcp` request. Also: after deploying a fix to a RUNNING
    mcp-container app, `restart_app`, because a live instance keeps serving
    the old image until it recycles.
    Note the idle **cold start**: a sleeping container wakes on request, so
    expect a seconds-scale delay on the first `POST /mcp` after idle (how
    long it stays up with no requests is the `container.sleep_after`
    setting, which `get_config app=<name>` shows once the app exists).
    Mention this if responsiveness matters to the user. The idle-clock rule
    under `mcp-function` applies here too, from the same served home.
  - State your recommendation and the reason, and go with the user's call.
- **Deployment pattern** (contract §5): server-rendered is the default for
  internal tools; SPA+API when rich client interactivity is the point. It
  applies to either browser type.
- **Stack** follows from the type: a **function** or **mcp-function** app is
  TS/JS (that is what Cloudflare Workers run; an mcp-function app builds on
  the MCP TypeScript SDK). A **container** app defaults to Python/Starlette
  (the tested container stack, with a working reference app; contract §4),
  or the user's chosen stack: any language is supported. An
  **mcp-container** app defaults to **Python + the official MCP Python SDK**
  (FastMCP), but any language is equally supported.

### Present the design, THEN ask for approval

The user deserves to see what they're approving. **Write the full design into
your visible reply as a structured section, never a one-line summary buried
inside a tool-approval prompt.** An approval question that references "the
design as described" when no design appears in the conversation is a defect,
not a shortcut: the user cannot approve what they have not seen.

The written design covers, at minimum:

- **What the app does**: in the user's own terms, a short paragraph
- **Deployment type** and why (and the Connection constraint if §1 flagged it)
- **Data model**: the tables and files it will store
- **Routes / pages**: what the user can actually open and do
- **Access model**: who can see what, and who can edit, decided per request
  for each of the three kinds of caller contract R3 names (`get_app_contract`
  with `sections: ["2"]`). A member is only one of them: never design as if
  every caller is one, and give per-person data and roles only to a caller
  with an identity. The platform manages only membership:
  `X-Forwarded-Groups` carries at most this app's own two
  groups (the `App groups:` line of the status you read in the Version gate,
  with the app's name in place of `{app}`). Any finer role (an editor, an
  admin view) needs the app's own role table keyed on `X-Forwarded-User`,
  the caller's email address, which can change for one person and pass to
  another; do not design around reading other groups from the header. The
  header rule is `inno-platform-conventions`' **Identity** section.
- **Accessibility** (a browser-facing app): who will use it, the main flows
  a person has to complete, and how each one works from the keyboard alone
  and with a screen reader. For an MCP app, say it does not apply.
- **Deployment pattern and stack**
- **Name** (confirmed available via `check_name`) and the exact hostname it
  produces
- **Initial members**, if any

Only after that design is in your reply: **stop and get explicit user
approval** (of the design *and* the name) before §2. Ask the approval question
in your own words referencing the design the user can now read; put genuinely
separate decisions (name choice, deployment type, members) in their own
questions rather than folding them into the approval. Registration provisions
real resources (a database and file storage, and for a browser app a
sign-in in front of its address) and binds them to the user's repo; the
type is fixed at registration.

The type and design seed the scaffolding in §4.

## 2. Create the repo from the template

The repo must land in the **user's own** ownership: the platform has no
create-on-behalf path and never creates a repo itself. That constrains *whose
account* it lands in, not *who runs the command*.

**Preferred: do it for them with `gh`.** Run `gh auth status`; an authenticated
account with `repo` scope is the user's **own** credential, so a repo it creates
lands in their ownership exactly as the browser path does. Confirm the name and
visibility with them, then:

```sh
gh repo create {owner}/{repo} --template <template repo> --private
```

Here `<template repo>` is the owner/name on the `Template repo:` line of the
status you read in the Version gate.

- Suggest the app name itself; public or private is fine. Ask which they want, or run
  `gh repo list --limit 5 --json name,isPrivate` and match what their recent repos use, rather than
  assuming.
- Template copying is **asynchronous**: an immediate `git clone` can land an
  empty repo. Poll `git fetch` until `origin/main` exists before checking out.

**Fallback: walk them through the browser** when `gh` is absent or
unauthenticated, the account it holds is not theirs, or they simply prefer it:

1. Open the `new repo:` link on the `Template repo:` line of the status you
   read in the Version gate (it ends in `/generate`). It is GitHub's
   "Use this template" page for the instance's public template repo. (You can also reach
   it from the template repo's green **"Use this template" → "Create a new
   repository"** button.)
2. Set the **owner** to their own account or org, and the **repository name** to
   their choice (suggest the app name itself). Public or private is fine.
3. Click **Create repository**. The repo lands in **their** ownership, already
   scaffolded from the template.

Note the resulting `owner/repo` slug: that's the `repo` argument for
`register_app`.

## 3. Register the app (two calls)

`register_app` is a **two-step** flow with two things in between: committing a
proof-of-control file to the repo, and the App install. Call it, commit the
proof file it names, give the user the install link, wait for them to install,
then call it again.

### Call 1: start registration, commit the proof file, get the install link

```
register_app({ app, repo, description, type, members, accept_guardrails: true, connections })
```

- `app`: the app name from §1 (drives the hostname). The wire parameter is
  `app`; no tool names the target app `name` (the variable tools use `name`
  for the *variable's* name).
- `repo`: the `owner/repo` slug from §2 (a **slug, not a URL**). `app` and
  `repo` are the only two the schema requires; everything below is optional to
  the schema, though the handler still refuses the call without
  `accept_guardrails: true`.
- `type`: from the design decision (§1b): `"function"` for the greenfield
  default, `"container"` when the description warranted it, `"mcp-function"` for
  an MCP server, `"mcp-container"` for an MCP server that needs the container
  shape. Omit for container. The type is fixed at registration and can't be
  switched later (register a new app to change it).
- `accept_guardrails: true`: required; you must have done the §1a review.
- `members` is an optional list of Okta emails (at most 50). Each address is
  added to the app's member list and notified that the app was shared with
  them, in-platform plus email per their own notification settings, so name
  only people who should hear about it now. An address Okta does not know
  is still added but not notified, and call 2's answer names it under
  `Warnings:`. Check its spelling with the user, and if it is
  mistyped, remove it with `revoke_access` (`inno-manage-app`). An address
  the platform could not check in Okta is added too, with its own warning.
  From platform v0.16.12 each added address is pinned to an account as
  `grant_access` pins it (`inno-manage-app`), and the owner's own row to the
  account that registers the app. A member whose address resolves to an
  account the list already holds under another address (such as the owner's
  own alias) gets no second row and is not notified, and the answer names it
  among the warnings.

  On a platform that lists allowed email domains, an address outside them
  refuses the whole call with `email_domain_not_allowed` before anything is
  created. That includes the user's own address, because the caller becomes
  the app's owner (**Reading register_app's responses** below says what to
  tell them).
- `connections`: optional list of names, when §1 step 5 flagged a per-user
  backend. Pass what you plan to set up; it **creates nothing** (only
  `set_app_connection` can) and is echoed back in the response as a reminder
  to configure each one. A badly-shaped name is noted in the response and
  never fails the registration. The schema bounds the list (at most 16
  names, each at most 64 characters); add any beyond that afterwards with
  `set_app_connection`.

The first call returns text beginning **`Registration started for "{name}" ←
{repo}.`** It carries, in this order: (a) the template link again, in case the
repo doesn't exist yet; (b) a **proof-of-control file**: a `path:` under
`.inno-platform/` and the exact `contents:` (a 64-character hex string), with a
sample command; and (c) an **App install link**
(`https://github.com/apps/…/installations/new?state=…`).

**Commit the proof file first.** Installing the GitHub App proves the platform
can SEE the repo; this file proves the caller can CHANGE it, and nothing binds
until it checks out. Use the path and contents exactly as the response prints
them; never derive or shorten them. Commit it on the repository's **default
branch** (`main` for a template copy) and push:

```bash
git clone <the user's repo>   # skip if §2 already cloned it
cd <repo>
git fetch origin && git checkout main && git pull --ff-only   # fails until the template copy has landed: wait and retry
mkdir -p .inno-platform
printf '%s\n' '<contents from the response>' > '<path from the response>'
git add '<path from the response>'
git commit -m "platform registration proof"
git push origin HEAD
```

This is not a user-only step: do it with the user's own authenticated `git` or
`gh`. Only when you have no write credential for the repo, walk the user through
GitHub's web UI (**Add file** > **Create new file**, the exact path as the file
name, the exact contents, committed directly to the default branch).
Surrounding whitespace (such as the newline `printf` adds) is tolerated;
everything else must match exactly. Leave the file in place: call 2 re-checks it
immediately before provisioning. After that nothing reads it again, and keeping
it is harmless. The push may start a CI run in the repo; it deploys nothing (the
app isn't built yet), so there is nothing to act on in its result. Never commit
the proof on an empty clone (template copying is asynchronous, so
`git checkout main` fails until `origin/main` exists) and never force-push it:
a forced push over the template copy wipes the scaffold, and call 2 then has
nothing to prune.

**Then give the user the install link verbatim** and ask them to:

1. Open it, and **install the platform GitHub App** on the account/org that owns
   `repo`, granting it access to that repository (repo-only access is fine; they
   can scope it to just this repo). If the App is already installed there with
   access to this repo (including "All repositories"), they can skip the link:
   call 2 verifies access directly.
2. Save the configuration. GitHub redirects them to the platform's verification
   page, which says **Repository verified** once the App can reach the repo AND
   the proof file matches. If it says **Proof file not found**, the file is
   missing, on the wrong branch, or has the wrong contents: fix it, then reopen
   the link or simply run call 2 (it re-checks without the redirect). If it
   says **GitHub App installed** instead (GitHub's configure flow, for an
   account that already had the App), that page carries no registration: just
   run call 2.

The link expires in 24 hours. Re-running `register_app` while the registration
is still pending reuses it, with the same proof path; once it has expired, the
response names a NEW proof path, and that new file is the one to commit.

### Call 2: finish provisioning, get the deploy.yml

Once the proof file is pushed to the default branch AND the user confirms
they've installed the App (or the App already covered the repo), call
`register_app` **again with the same arguments**. This re-checks the proof file,
then finishes the job server-side: it prunes the template scaffold to the
chosen type in a new commit on the repo's default branch, provisions the
app, and binds the repo. It returns text beginning
**`App "{name}" registered from {repo}`** and containing:

- `URL (after first deploy): https://<app host>`: **quote
  this from the response, never construct it** (the host and domain are
  the instance's). For an **mcp-function** or **mcp-container** app the
  response surfaces the **MCP endpoint** (`…/mcp`) instead; same rule: quote
  it from the response. The URL 404s until the first successful `inno-ship`.
  A browser app's first deploy needs the platform's newer gateway: until a
  platform admin has promoted it, the deploy is refused `gateway_too_old`,
  which is not the user's to fix (`inno-ship`'s failure table). Tell them
  plainly: "The platform needs an update from its operator before your app
  can go live; nothing on your side needs to change."
- A `.github/workflows/deploy.yml`: the thin caller workflow that wires the
  repo to the platform's reusable CI. **Overwrite the repo's copy with the
  snippet the response returned** (an older template may still carry one). The template ships no `deploy.yml`: this file
  always comes from `register_app`'s second call. It carries the explicit
  `with: app: {name}` input and is correct for any repo name, so write it in
  every case. This is a real step, not a hands-off one. Keep the
  `workflow_dispatch` trigger (the platform re-dispatches it for security
  respins). The snippet has no `secrets:` line, and the file must not gain one:
  `secrets: inherit` is a blocking finding for the `sast` gate, and the
  platform workflow needs no caller secrets.

### Reading register_app's responses: branch, don't assume

`register_app`'s description states what each refusal means. What to do next:

- **`Registration started …`** on call 1: commit the proof file, hand over the
  install link, and wait (above). The same text on call 2 means the platform
  still cannot see the repo through the App (not installed yet, installed
  without access to this repo, or a transient GitHub failure), or the 24-hour
  registration expired. Compare the proof `path:` with the one you committed:
  if it changed, commit the new file. Then have the user install the App on the
  repo (or widen its repository access) and call again.
- **`App "{name}" registered …`**: call 2 succeeded; proceed to §4.
- **`guardrails_not_accepted`**: do the §1a review, then pass
  `accept_guardrails: true`.
- **`invalid_name` / reserved**: pick another name (you should have caught
  this with `check_name`).
- **`name_unavailable`**: an app with that name already exists and is not the
  caller's own partial registration; pick another name.
- **`invalid_type`**: pass one of the four type names.
- **`invalid_repo`**: pass an `owner/repo` slug, not a URL or a bare name.
- **`repo_control_unproven`**: the error text repeats the exact path and
  contents: commit that file (call 1 above) and call again. It can come back
  at call 2 even after the setup page said verified, because call 2 re-checks
  the file right before provisioning, so never delete it early.
- **`name_quarantined`**: the name is held after a purge until the UTC time
  the message names, with no admin bypass: pick another name (check it with
  `check_name`), or wait until that time.
- **`repo_unreachable`**: have the user reinstall the App on the repo, then
  call again.
- **`repo_identity_changed`**: confirm the repo's current `owner/repo` slug
  with the user and call again with it; a new slug starts a fresh
  registration with a new proof file and a new install link (have the user
  open that link and save). The very next call starts clean: there is no
  window to wait out.
- **`invalid_member_email`**: one of `members` is not a plain email address.
  Fix or drop it and call again.
- **`email_domain_not_allowed`**: the message names the address and the
  domains. Either call can answer it, and nothing was created.
  - **An address in `members`**: fix or drop that address and call again.
  - **The user's own address** (this holds even for a call that repeats a
    registration they already finished, which then hands back no
    `deploy.yml`): nothing on their side fixes it. The list is the instance
    manifest's `identity.allowedEmailDomains`, which only the platform's
    operator can change, by editing the manifest and redeploying. Tell the
    user plainly that their address cannot own an app on this platform, and
    stop.
- **`host_in_use`**: nothing was created. Choose another name, or have the
  record removed if it is unused.
- **`host_check_failed`**: nothing was created, and this is not the user's to
  fix: an operator must grant the platform's Cloudflare token Zone DNS read.
- **`upstream_error`** (could not re-check the repository with GitHub): a
  transient GitHub failure during call 2's re-check. Wait a moment and call
  again with the same arguments.
- **More than 50 `members`**: the tool's schema refuses the list before the
  tool runs, with an argument-validation error on `members`. Register with a
  shorter list and add the rest afterward with `grant_access`.
- **`app_limit_reached`**: the user is at their active-app limit; resolve per
  §1 (the user chooses to stop one of their own apps, or an admin raises the
  limit; never propose which to stop).
- **`repo_already_registered`**: that GitHub repo is already bound to an app
  (one repo binds to at most one app). Use a different repo, or manage the
  existing app via `inno-manage-app`. (`repo_id_conflict` is the audit action
  the platform records for this refusal; callers never see it as an error code.)
- **`repo_owner_claimed`**: the message names who holds that GitHub account:
  ask them or a platform admin to register on the user's behalf, or use a
  repo under an account of the user's own. Platform admins bypass this check,
  so an admin can register under a shared-org account directly without going
  through the first user.
- **`repo_mismatch`**: a partially-finished registration exists for this name
  with a *different* repo; finish it with the original repo, or start over with
  a consistent `repo`.
- **`github_app_not_configured`**: the platform's GitHub App isn't set up on
  this deployment; nobody can register until an admin configures it.
- **Repo wasn't template-derived.** The user registered a repo that didn't
  come from §2's "Use this template" flow (a blank GitHub "New repository" is
  the common way this happens), so the server had nothing to prune. There are
  two real cues, and they differ by type. A **container** registration says
  nothing about it: the response does not mention the scaffold step at
  all. A **function**, **mcp-function** or **mcp-container**
  registration warns, naming the overlay it could not find, in a warning
  beginning `no scaffold/<preset>/ overlay found in <repo>`. The
  second cue is the one that holds for every type: after call 2 finishes, the
  repo shows none of the type-specific files described in §4. This is not an
  error to retry. Treat it as the empty-repo path in §4 below.
- **`registration_disabled`**: a platform admin must re-enable self-service
  registration (`registration.enabled`).
- Any other non-empty error: surface it verbatim rather than retrying
  blindly. The refusals any platform tool can give are explained once, in
  `inno-platform-conventions`' **Refusals every tool shares** section.

## 4. Pull and scaffold

You cloned the repo in §3 to commit the proof file. Call 2 then pushed the
platform's scaffold prune to the repo's default branch as a new commit from
the server side, so bring the clone up to date before touching anything (a
push from the stale clone would be rejected as non-fast-forward):

```bash
cd <repo>
git pull --ff-only   # picks up the registration's "scaffold: <type>" commit, if it applied one
```

If the proof file was committed through GitHub's web UI instead, clone now:
`git clone <the user's repo>` (e.g. `git@github.com:<owner>/<repo>.git`), then
`cd <repo>`.

After call 2, the repo has been **pruned to the deployment type you chose**:
the template carries every scaffold and the platform rewrote the repo at
registration. No type ships `.github/workflows/deploy.yml`: you write it
from call 2's snippet per §3. A
**function** repo has the TS reference (`app/index.ts`),
an **mcp-function** repo the MCP-server TS reference (also `app/index.ts`), and
a **container** repo the Python/Starlette reference (`app/`, incl. `main.py`,
`storage.py`, `templates/`, `requirements.txt`, plus `Dockerfile` and `lib/`).
An **mcp-container** repo ships **its own overlay** (`scaffold/mcp-container/`):
a stateless FastMCP starter for `app/main.py`, plus its own `README.md`,
`CLAUDE.md`, and `app/requirements.txt`, applied over the container root
(see the bullet below); `Dockerfile`, `lib/`, and `app/storage.py` stay as
the container reference's. The platform owns a fixed set of other paths (a
repo-root `src/`, the root build files, any wrangler config, and the rest
contract R7 lists: `get_app_contract` with `sections: ["2"]`), and none of
them may be in the repo: don't create any. `get_platform_docs`'
**Environment & config integrity** section lists them too; the plugin's
copy, with what to do when a migrated repo already carries one, is
`inno-platform-conventions`' **Files you must not touch** section. Load
that skill before writing any application code (stack policy, storage,
identity, the do-not-touch file list), and, for a container or
mcp-container app, the `inno-containerize` skill before editing the
Dockerfile.

**The empty-repo path: if the repo wasn't template-derived, there's nothing
to prune, so author the layout by hand.** A repo created via GitHub's blank
"New repository" flow (instead of §2's "Use this template") arrives with no
scaffold, so call 2 leaves it as-is. Recognize this early: the repo is
missing the type-specific files described above. Then read
`references/hand-authored-layout.md`, which says what to copy from the
template repo for each type and why `CLAUDE.md` is copied rather than
written, and write `.github/workflows/deploy.yml` from call 2's response.

**Scaffold by the deployment type you chose in §1b.** The contract sections
you read in §1b (§1.1 to §1.3) are the authority for each type's deltas.

- **`function` app (greenfield default):** the entry is **`app/index.ts`**
  exporting `export default { fetch(request, env, ctx) }`; extend it rather
  than re-scaffolding. Read the caller with `currentUser(request.headers)`
  from the scaffold's `app/identity.ts`, handling no user (`null`) first in
  each route that needs a person and never defaulting it into a value
  (`inno-platform-conventions`' **Identity** section), serve **`GET /healthz` as a
  route** returning **exactly 200** (a 204 or a redirect to `/healthz/` fails
  both the CI smoke gate and the runtime probe), and reach storage through
  the app's **own bindings** `env.DATA` (D1) and `env.FILES` (R2), not
  `storage.internal`. Declare every npm package the code imports in a
  **non-root** `app/package.json`, and commit the `app/package-lock.json`
  that `npm install` (run inside `app/`) produces, kept in sync with
  `package.json`. The install rule and everything it refuses have one home,
  `inno-platform-conventions`' **Node apps** paragraph; the short of it is
  that a runtime import must sit under `dependencies`, because CI installs
  `--omit=dev`. Never interpolate user data into hand-built HTML: even
  escaped, the SAST gate blocks it; return dynamic data as JSON (like the
  scaffold's `/me`) or use an auto-escaping template library. Do NOT create
  `wrangler.jsonc`/`app-worker.jsonc`: those are platform-injected. Include
  the required **sign-out link** (R4), a static link whose URL is the
  `Sign-out URL (all apps):` line of the status you read in the Version gate
  (see `inno-platform-conventions`' **Sign out** section for the exact
  convention); nothing in this type's scaffold provides it for you.
- **`mcp-function` app:** everything in the function bullet applies except
  the sign-out link (there is no browser session); the scaffold ships both
  `app/package.json` and its lockfile. Serve MCP at `POST /mcp` with the MCP
  TypeScript SDK's `WebStandardStreamableHTTPServerTransport`, constructed
  **without a `sessionIdGenerator`** (stateless), and implement **no auth of
  any kind**: never route `/.well-known/oauth-protected-resource` yourself
  (§1.2 says why). The app refuses inside MCP (a tool result marked as an
  error, or a JSON-RPC error), never with an HTTP status: a MUST of §1.2
  from contract 32.
- **`container` app, tested stack (Python):** start from the reference app
  (`app/main.py` + `Dockerfile`) and extend it; don't regenerate from scratch.
  Read the caller with `current_user(request)` from `app/storage.py`,
  handling no user (`None`) first in each route that needs a person.
- **`container` app, another stack:** replace `app/` and the `Dockerfile`
  wholesale for that stack, honoring the contract (port 8080, `/healthz`,
  identity headers, the `storage.internal` endpoints, sign-out link). A JS
  or TS container reads the caller with `currentUser` from `lib/storage.js`;
  any other stack reads the headers by the same contract, an empty or
  missing `X-Forwarded-User` being no user.
- **`mcp-container` app:** pruning applied the template's
  `scaffold/mcp-container/` overlay: its `.scaffold-remove` deleted
  `app/templates/` (this type has no use for it), and its `app/main.py`,
  `README.md`, `CLAUDE.md`, and `app/requirements.txt` replaced the container
  root's; `Dockerfile`, `lib/`, and `app/storage.py` stay as the container
  reference's. `app/main.py` already speaks Streamable HTTP at `POST /mcp`
  with two example tools (`whoami`, `echo`) and already answers non-POST
  `/mcp` requests with 405: extend it rather than adapting a Starlette demo
  into an MCP server, and keep it stateless (§1.3). `app/storage.py`
  carries the storage **and `Connections` helpers** your tools consume (see
  `inno-add-connection`).
  Identity is §1.2's: implement no auth of your own, read the caller with
  `current_user(ctx.request_context.request)` from `app/storage.py` (as
  `whoami` does), handling no user first, never route
  `/.well-known/oauth-protected-resource` yourself, and add no sign-out link.
  The app refuses inside MCP (a tool result marked as an error, or a
  JSON-RPC error), never with an HTTP status: a MUST of §1.3 from contract
  32.
  **Keep the starter's `transport_security` setting**, which
  `get_app_contract` §1.3 states and explains; changing it breaks every
  gateway-forwarded `/mcp` request. The starter pins FastMCP below `mcp` 2 in
  `app/requirements.txt` (2 renamed the `FastMCP` API the starter uses);
  build the container image per `inno-containerize`. Expect a seconds-scale
  cold start on the first request after the container has been idle for the
  app's `container.sleep_after`, which `get_config app=<name>` shows.

**Delete the scaffold marker as you build.** The template repo ships
`app/.needs-build`, which makes CI skip deployment until it's removed. Once you
begin writing the real app (per the approved design), delete it:

```bash
rm -f app/.needs-build
```

Leaving it in place means `inno-ship` will refuse to deploy, by design.

Typical scaffolding steps for a new feature (Python **container** reference
shown; a **function** app does the equivalent inside `app/index.ts`'s `fetch`
handler: route on the URL, read the caller with the identity helper and
handle no user first in each route that needs a person, read/write
`env.DATA`/`env.FILES`):
- Add routes to `app/main.py` (container) or `app/index.ts` (function); split into
  modules under `app/` as it grows.
- (Container, Python) add templates under `app/templates/`; never delete the
  directory while the reference Dockerfile is in use (a missing `templates/` is
  a common runtime 500, see `inno-containerize`).
- Add pinned dependencies to the stack's manifest (`app/requirements.txt` for
  the Python container; `app/package.json` for a function or a Node container).
  For a function or mcp-function app, also run `npm install` inside `app/` and
  commit the updated `app/package-lock.json` in the same commit (see the
  function bullet above).

**Browser-facing apps (`container`, `function`): accessible pages and
response headers from the first commit.** Scaffold every page with
`<html lang>`, a real `<title>`, a visible label on each form control, and
visible focus styles, and add one middleware that sets the response headers
`get_app_security` §9 lists, with the starting Content-Security-Policy it
gives for the deployment pattern you chose. For an SPA, also handle route
changes: update `document.title` and move focus to the new view. The detail
lives in the served notes (`get_app_accessibility`, `get_app_security` §9);
take it from there, not from this list. The plugin's summary of both is
`inno-platform-conventions`' **Accessibility** section and **Response
headers** paragraph.

**Container apps: the storage endpoints cap request bodies.** Contract R5
(fetch `get_app_contract` with `sections: ["2"]`) gives the SQL body cap, the
file `PUT` cap, and the refusal of a `PUT` with no `Content-Length`. So a
route that writes in bulk sends batches, and an upload route checks the size
itself, with its own message, and sends the body with its length. The codes
and the reasoning are
`inno-platform-conventions`' **Persistence** section. A function app reaches
`env.DATA`/`env.FILES` directly and has neither cap.

**Rewrite `README.md`: this is required, not optional.** The template's README
is the template's own ("Use this template…", template internals) and describes
nothing about this app. Replace it with a **high-level overview of the user's
app**: what it does, who it's for, and the app's URL. Keep it short (a few
paragraphs is right); the platform mechanics (identity, storage, CI) already live
in `CLAUDE.md` and don't belong here. The README is the user's file from then
on: they can deepen it to whatever level of detail they prefer, and later
features should keep it truthful.

## 5. Hand off

Once scaffolding is in place, tell the user the app was registered (their repo +
future URL; for an **mcp-function** or **mcp-container** app, the `/mcp`
endpoint their MCP client will use), and that the next steps are: write the
app, run
`inno-safety-preflight` (it pushes to the default branch, which runs the real
gates and deploys nothing), then `inno-ship`. Beyond the registration
proof file (§3), don't push anything yet unless asked: `inno-new-app`'s job is
registration + scaffolding, not deploying.

If §1 flagged that the app needs to reach another service as each person using
it, do that setup now, before writing the rest of the app: run the
`inno-add-connection` skill (requires the `mcp-container` type from §1b).

If the app needs an app-level key or config value instead (one API key the
whole app shares, a base URL), set it after registration with
`set_app_variable`: it reaches the app as a plain environment variable.
Never put it in the repo; gitleaks fails the build on the full history. A
route that spends an app-level key needs the limits `get_app_security` §5
sets, per client and globally.

If the app will read platform Variables, consider declaring them in
`app/inno-variables.json` (contract §2.3 gives the format) so an owner
without your source can see what it needs (see `inno-platform-conventions`).
