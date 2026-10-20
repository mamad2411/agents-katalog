---
name: inno-ship
description: "Use when the user is ready to release an app: pushes, waits for the safety checks, cuts the v* release tag that actually deploys, and reports the live URL. Use after inno-safety-preflight is clean (gates AND guardrails)."
---

# inno-ship

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

Deploys are **release-driven**: a push to the default branch runs the safety
gates and deploys nothing; **tagging a `v*` release is what deploys**. This
skill makes that seamless: for a less-technical user, "shipping" is one
conversation and the versioning just happens.

Run `inno-safety-preflight` first if it hasn't passed in this session. Its
verdict covers BOTH the safety gates and the guardrails policy review: if
the guardrails review flagged an unresolved violation, **do not ship**, even
with green gates, until it's resolved or the user has an admin exception.

## 0. Precondition: the app must actually be built

If `app/.needs-build` still exists in the repo, STOP: this app is still the
untouched template scaffold. Tell the user plainly, e.g. "This app hasn't
been built yet; let's add your actual app before shipping," and hand back to
`inno-new-app`/`inno-migrate-app` (or help them build it). Do not delete the
marker just to force a release of an empty scaffold.

```bash
test -f app/.needs-build && echo "BLOCKED: app/.needs-build present, build the app first" || echo "OK: no scaffold marker"
```

For a function-shaped app (`function`, `mcp-function`), also confirm the
lockfile. The push checks do catch its absence, in the `app-deps` job; the
rule they enforce is `inno-platform-conventions`' **Node apps** paragraph.
Check it here anyway, as belt, to save a round trip through CI:

```bash
if [ -f app/package.json ] && [ ! -f app/package-lock.json ]; then echo "BLOCKED: commit app/package-lock.json (run npm install inside app/)"; else echo "OK: lockfile present, or no app/package.json"; fi
```

Then, only when `app/package.json` exists, install from the lockfile exactly as
the `app-deps` job does. A function app with no `app/package.json` has no
dependencies and nothing to install; do not create one to satisfy npm. The
install creates `app/node_modules/`, which must be gitignored before §1's
`git add -A` (template repos already ignore it; a migrated repo may not):

```bash
if [ -f app/package.json ]; then
  (cd app && npm ci --ignore-scripts --omit=dev) && { git check-ignore -q app/node_modules/ || echo "BLOCKED: add node_modules/ to .gitignore before git add -A"; }
else
  echo "OK: no app/package.json, so nothing to install"
fi
```

Every package the code imports must be declared under `dependencies` in
`app/package.json`; the rule is the contract's §1.1 **Dependencies** bullet
(`get_app_contract` with `sections: ["1.1"]`). If `get_app_contract` refuses
the arguments, or the platform is older than v0.16.14, call it with no
arguments and read the sections needed from the whole contract.

### Declared variables, if the app has any

If the repo has `app/inno-variables.json`, read it before tagging: nothing
in CI validates or applies it before the tag's `deploy` job finalizes, so
this is the only check that helps before the first deploy. Check it against
the contract's §2.3 **Secrecy.** and **Declaring what an app wants**
paragraphs (`get_app_contract` with `sections: ["2.3"]`): the name rule and
the reserved names from the first, the three allowed fields with their
defaults and their types, and the 32-entry cap, from the second. A file
that breaks them never fails the deploy, and the platform keeps its previous
declarations; the reason shows in one of two places:

- a file the platform refuses: on the `deploy-complete:` line in this
  run's log;
- a file that is not valid JSON, cannot be read, or is over 32 KB, which
  never reaches the platform: a `::warning title=Declared variables::`
  annotation naming the reason. The `deploy-complete:` line still appears,
  just with no `variables_refused` field on it, so look for the warning
  annotation, not for a missing line.

For every name marked `required: true`, call `list_app_variables` (or read
`app_status`, which names an unset required one on its own line) and tell
the user before you tag if it has no value yet: the platform never blocks a
deploy or fails a gate over a missing required variable, so this is the
only warning the user gets before finding out at runtime. Whether to set it,
or fix the file, before tagging is the user's decision, never a reason for
you to refuse the tag; `inno-safety-preflight` §1b states the same rule.

## 1. Commit, push, and wait for green checks

**Confirm the branch before pushing**, exactly as `inno-safety-preflight` §2
says (the gates run only on pushes to the repository's default branch).

```bash
git add -A
git commit -m "<short, why-focused message>"
git push origin HEAD
```

Between the `git add -A` and the commit, run the **directory-symlink check**
from `inno-safety-preflight` §2. It has one copy in this plugin and lives
there; a committed directory link fails `config-integrity` with no policy
toggle, and it has to run after `git add -A` so the index covers both
already-tracked links and the ones you are about to commit.

This runs the eight gate jobs (`config-integrity`, `secrets`, `sast`, `deps`,
`dep-age`, `container`, `scaffold-check`, `app-deps`) plus the `policy` fetch
that resolves the admin gate configuration, and then **stops**: the deploy
job runs only on release tags. The `container` job is skipped for
`function` and `mcp-function` apps, which have no image to build. Watch with
`gh run watch` or the `get_ci_status` MCP tool, and read `get_ci_status`
(which run it is, its annotations, its refusals) as `inno-safety-preflight`
§2 says. If a gate fails, follow the failure guidance below and re-push;
never tag on top of red checks.

The `container` job also writes the accessibility, response-header and
Dockerfile reports; `inno-safety-preflight` §1c says where they are and how
to read them. In the default `report` mode their findings never block a
push or a tag, so do not hold a release for them, and do not read a green
`container` job as a clean report either. Only when an admin has set the
app's `safety.a11y.mode` to `enforce` can the accessibility report fail the
job: the `Accessibility check failed` row below.

## 2. Cut the release: this is the deploy

Pick the version, then tag:

```bash
git fetch --tags
git tag --list 'v*' --sort=-v:refname | head -3   # what's the latest release?
git tag v<X.Y.Z>
git push origin v<X.Y.Z>
gh release create v<X.Y.Z> --verify-tag --title "v<X.Y.Z>: <short description>" \
  --notes "<one bullet per commit subject since the last tag>"
```

A bare tag deploys but leaves the repo's **Releases** page empty, so always
create the GitHub Release too (after the tag push; creating a release on an
already-pushed tag does not re-trigger the deploy).

Version selection: default to a **patch** bump of the latest `v*` tag; use a
**minor** bump when this ships a user-visible feature; `v1.0.0` for a first
release. Only ask the user if it's genuinely ambiguous; otherwise just tell
them what you're doing ("shipping v1.2.0"). The tag push re-runs the gates on
the tagged commit and then deploys.

## 3. Watch the release run

```bash
gh run watch    # or poll get_ci_status
```

If you poll `get_ci_status` instead, wait at least 30 seconds between calls,
and never poll the same run from several subagents at once: the platform's
call budget is per person, not per agent. The rule is `inno-manage-app`'s
**Call budget** section.

### On failure: fix quietly, report plainly

The user is not necessarily a developer. **Do not paste raw CI logs, stack
traces, or job internals into the conversation.** The same goes for
technology names: say "the security check", "the database", "file storage",
per the plugin README's **House style** section. Read the logs yourself
(`gh run view <run-id> --log-failed`) but keep that output to yourself. To
the user, one plain sentence: "The security check found an out-of-date
dependency; I'm updating it and re-shipping." Fix the **root cause**, push,
and cut the next patch tag (a tag is immutable: never force-move one).
The exception: before any fix that moves, deletes or replaces the user's
files, or edits anything under `.github/workflows/`, show the user the change
and ask first, whether or not the row below says so.

| Failing job | Likely cause | Fix via |
|---|---|---|
| `config-integrity` | the repo carries a platform-owned or forbidden path, or `CLAUDE.md` lacks a required header. The failure message names each path; the full list, with the reason for each, is `inno-platform-conventions`' **Files you must not touch** section | **stop and ask; this is not a quiet fix.** Files under `src/` and a root `package.json` can be the user's own code: show the user every flagged path first. Only with their okay, move author code and manifests under `app/` (for example `app/src/`), update the Dockerfile `COPY` paths and the code's imports to match, and delete only what they confirm is not theirs (such as `src/gateway/` or `src/node_modules/`). Never move or delete author code unprompted before a tagged deploy. See `inno-platform-conventions` |
| `secrets` | gitleaks found a committed credential | rotate + scrub history, then set the new value as an app Variable (`set_app_variable`) |
| `sast` | a semgrep OWASP finding anywhere the gate scans, which is the whole repository and not just `app/` (the scope is `inno-platform-conventions`' **Rendering** section; the log names the file). A `secrets: inherit` line in `.github/workflows/deploy.yml` (older template copies carry one) is a blocking finding too | `inno-platform-conventions` (escaping, SQL); for `secrets: inherit`, tell the user and, with their okay, delete the line (the platform workflow needs no caller secrets) |
| `deps` | a CVE in `app/requirements.txt` or a production npm dependency (what the audit covers is the contract's R8) | bump the pinned dep |
| `dep-age` | a pinned dep is **too new** for the platform's release-age cooldown (`safety.min_release_age_days`; `get_config app=<name>` gives the value in force and its meaning), or `app/package.json` ships with no committed, parseable `app/package-lock.json` so there is nothing to date | **not** a version bump: bumping to the newest release makes it worse. Wait out the cooldown, pin an older vetted version, commit `app/package-lock.json`, or ask a platform admin for an app-scope `safety.min_release_age_days: 0` |
| `container` | Trivy CVE, a `USER` the non-root gate refuses (the forms it accepts are the contract's R1; `inno-containerize` item 2 applies them), missing `EXPOSE 8080`, or the image never answered `GET /healthz` | `inno-containerize` |
| `container` fails with `Accessibility check failed` (only when the app's `safety.a11y.mode` is `enforce`) | the accessibility report found something that blocks in `enforce` mode: an unwaived critical or serious violation, or a landing page `/` (or every page) the app left unscannable. Exactly what blocks, and what only warns, is the `enforce` row of the mode table `get_app_accessibility` serves | read what the report marks as blocking (`inno-safety-preflight` §1c) and fix it, push, confirm the gates are green, then cut the next patch tag. A failing `/` has to render in CI, where there is no stored data, as a real page (an empty state, not an error or a redirect off the app): `app/inno-a11y.json` adds pages that render without stored data, but it never stands in for `/`. A rule that is wrong for this app: name its rule id and have the user ask a platform admin for a time-limited waiver, `safety.ignore.a11y.<rule-id>` with an expiry date as its value |
| `scaffold-check` | not a failure: it suppresses `deploy` while `app/.needs-build` exists (see §0) | build the app, remove the marker |
| `deploy` fails with `app_stopped` | the app was stopped by the lifecycle (or deliberately), and **stopped apps cannot be deployed**. Only the release tag's `deploy` job fails this way; a push to the default branch still runs every gate green on a stopped app, so a clean preflight is not evidence that the app can deploy | `inno-manage-app`: `start_app` first, then cut the next patch tag |
| `app-deps` fails with `Missing app/package-lock.json` (function-shaped apps) | `app/package.json` exists but no lockfile is committed (the contract's §1.1 **Dependencies** bullet). This job runs on pushes too, so the failure blocks before any tag exists | run `npm install` inside `app/`, commit `app/package-lock.json`, push, confirm `app-deps` is green, then tag |
| `app-deps` fails in `npm ci` (on pushes as well as tags), or the `deploy` bundle step reports `Could not resolve "<package>"` with the titled error `Undeclared import` (function-shaped apps), or reports it with the titled error `devDependency imported at runtime` | the lockfile no longer matches `app/package.json`, or the code imports a package not declared anywhere (nothing is installed at the repo root), or the code imports at runtime a package declared only under `devDependencies` (`app-deps` installs `--omit=dev`, so that tree was never installed) | for an undeclared package: declare it in `app/package.json`, run `npm install` inside `app/`, commit both files, push, confirm `app-deps` is green, then cut the next patch tag. For a devDependency: move it as **Moving a devDependency into dependencies**, below this table, says; then commit `app/package.json` and `app/package-lock.json`, push, confirm `app-deps` is green, then cut the next patch tag |
| `deploy` fails with `app_not_deployable` | the app was stopped, or its repo lost the platform GitHub App, while this deploy was starting | if the repo was unlinked, have the user reinstall the GitHub App on it first (re-linking leaves the app stopped); then `start_app` (`inno-manage-app`) and cut the next patch tag |
| `deploy` fails at the token request (`deploy-token request failed (HTTP 409)`) with a message about this deploy's gateway and its capability, naming a platform admin's fix (`gateway_too_old`; the log shows the message, not the code, and its wording may change between releases) | every browser app (`container`, `function`) deploys only on a gateway of capability 1 or more, which asks the platform who may use the app, and the gateway this deploy would ship is older (`register_app`'s and `sync_gateway_ref`'s descriptions state the rule). So any browser app's deploy meets this until a platform admin has promoted the platform's gateway. It is never a code bug, and nothing was deployed | not the owner's to fix. Tell the user plainly: "The platform needs an update from its operator before your app can go live; nothing on your side needs to change." A platform admin moves `gateway.ref` to a gateway of capability 1 or more (`sync_gateway_ref`) or removes the app's own `gateway.ref` override (`remove_config`), as `inno-fleet-admin` describes; then cut the next patch tag, which is what the refusal means when it asks for the tag again |
| `deploy` fails at finalize with `app_not_deploying` | the app was stopped or purged while the deploy ran; nothing went live | `app_status` to see which; if stopped, `start_app`, then cut the next patch tag |

The rarer `deploy` and broker failures and warnings, each with its fix, are
in `references/deploy-failures.md`. Read it when the run shows any of
these: `No scanned image recorded`; `Image mismatch` or `image_mismatch`;
a `deploy-sbom failed (403)` line naming `app_mismatch` or saying the app is
no longer linked to its repository, `Gate policy unavailable`, or
`Gateway not promoted` (the broker refusing `app_mismatch` or
`repo_unlinked`); `policy` failing with `Invalid app name`; or a
`Gateway dependency advisory` or `Cloudflare not ready` warning (either can
appear on a run that succeeded; neither is about the app's code, so change
nothing in the app before reading the row). On a push, a
`deploy-sbom failed (403)` line reading `deploy_denied:ref` is normal.

A gate failure is real signal; there is no override or admin bypass. A
finding that's a false positive gets a **central admin ignore** (see
`inno-safety-preflight`), never an in-code workaround. Gitleaks is the one
exception: it has no central ignore family, so a false-positive `secrets`
finding is suppressed with a `.gitleaksignore` entry in the app's own repo.

#### Moving a devDependency into dependencies

When the deploy reports `devDependency imported at runtime` for a package,
that package's entry moves from `devDependencies` to `dependencies` exactly
as it stands, specifier and locked version unchanged. The error's own
`Move it:` line carries the command, with the package already named. Read
`references/devdependency-move.md` before you run it: it has the same
command for a move by hand, what it changes in `app/package.json` and
`app/package-lock.json` and how to check that, and the look-alike command
that ships a version the author never chose.

### When you're stuck: offer to build a support bundle

If the same gate still fails after **two** genuine root-cause fix attempts,
stop retrying. Summarize plainly, then **ask permission** to create a
diagnostics **support bundle** via the **`create_support_bundle`** MCP tool
(`app`, plus a plain-language `description`). Give the user the download link
it returns and tell them to attach the zip to a ticket in the support
system: the platform team triages there, not in the platform.
The caps and refusals are `inno-manage-app`'s support-bundle section; the one
to expect here is `bundle_limit_reached`, and the answer to it is to attach
the most recent existing bundle rather than retrying.

## 4. On success: provenance, then the live URL

The `deploy` job (tag runs only) exchanges a GitHub OIDC token with the
platform's deploy broker for a scoped deploy token. The broker issues one
only to the pinned reusable workflow, the `CI workflow:` line of the status
you read in the Version gate (keep `deploy.yml`'s `uses:` reference exactly
as `register_app` returned it), running for a `refs/tags/v*` release tag. A
push to any branch, a fork, or a `deploy.yml` edited to skip gates gets
`403 deploy_denied`: there is no code path where removing the gates yields a
working deploy. The release tag is recorded on the deployment, and the
safety sweep's auto-respin rebuilds at exactly that tag; a container app's
deploy ships exactly the image the `container` job scanned. The served
account is `get_platform_docs`' **Releases** and **CI gates** sections and
the contract's R7 and R9.

On success, report:

```
Shipped v<X.Y.Z>: <the app URL, as reported by app_status / register_app>
```

and note that the app is **Okta-gated**: the first visit prompts an Okta
login (Cloudflare Access), and only the owner plus anyone granted access via
`inno-manage-app`'s `grant_access` can reach it, unless the app has been
opened to every SSO user with `set_app_access` (`inno-manage-app`). On a
browser app, anyone else who signs in sees a plain "No access" page.

For a `container` app, add one plain line with the tag run's accessibility
report counts: critical, serious, moderate and minor findings, and how many
pages could not be checked (`inno-safety-preflight` §1c says where to read
them). In `report` mode say that they did not block this release, and that
they are what a tool detected, not a verdict that the app is accessible. If
the report did not run, or `safety.a11y.mode` is `off`, say that instead of
quoting zeros.

For an **mcp-function** or **mcp-container** app, report the **MCP endpoint** (`…/mcp`, as returned by
`app_status` / `register_app`) instead of a browser URL, and tell the user to
add it as an MCP server in their client (Claude Code, claude.ai): the first
connection runs an OAuth authorization (consent + Okta) rather than a browser
SSO redirect. Access is still the app's member list, or every SSO user
once the app is opened with `set_app_access`.

**On a brand-new app's first-ever deploy, warn about the propagation window
when you hand over the URL or endpoint; don't just paste a bare link.** The
same DNS propagation window covered below (up to roughly a minute) applies
to the *user's* first click, not just to an agent-run lookup. Say something
like: "it can take up to a minute to resolve; if it doesn't load on the
first try, wait a minute before retrying rather than refreshing or
re-clicking repeatedly." Repeated clicks inside that window are exactly what
get the negative (NXDOMAIN) result cached on the user's own machine for
minutes, even after the app is actually live. This caveat doesn't apply to
redeploys of an already-live app: the hostname already resolves.

Container-shape redeploys (`container`, `mcp-container`): a deploy replaces the
image, but an instance that is actively serving keeps running the OLD image
until it recycles (idle sleep or `restart_app`). If the user redeployed a fix
to a busy app and it still shows old behavior, run `restart_app`: the next
request cold-starts on the new image.

### Do not curl, dig, or otherwise resolve the hostname to "verify" success

Never look up the app's hostname (the `App host pattern:` line of the status
you read in the Version gate, with the app's name in place of `{app}`;
`register_app` reports the real one) yourself, via `curl`, `dig`,
`nslookup`, a browser navigation or the like, as a way to confirm the deploy
worked, above all right after a brand-new app's first deploy. The DNS
record for a freshly deployed hostname can take up to roughly a minute to
propagate, and any command you run executes on the user's own machine,
sharing their real network stack, not an isolated sandbox. A lookup that
lands in that window gets a negative (NXDOMAIN or SERVFAIL) answer, which
can be cached independently in several places (the user's router-level DNS
resolver, such as AdGuard Home or Pi-hole, and their OS's local resolver
cache, such as macOS `mDNSResponder`) for minutes. The app then looks broken
to the user long after it went live, and it won't self-correct until each
cache's negative TTL expires or someone flushes it by hand.

The `deploy` job's success or failure and the `app_status` MCP tool's
deployment timestamp are the authoritative, side-effect-free signals: use
those. If the user wants to see the app for themselves, let them visit it
in their own browser; don't pre-check it for them.

### Right after a deploy, health may read `re-probe pending`, which is not a verdict

Right after a deploy, `app_status` can read `Health: re-probe pending (not
answering yet: <what the probe saw>, checked again within the hour)`,
followed by `; last recorded: <status>` when an earlier probe recorded one.
The probe a deploy fires never judges a failure: it defers every unhealthy
result to an hourly pass and notifies no one, while a healthy answer is
recorded at once. The rule and its clocks are the contract's R2
(`get_app_contract` with `sections: ["2"]`), and `inno-containerize` item 4
is the plugin's home for them. What that means for you:

- The last-recorded status is from before this deploy and says nothing
  about it. On a brand-new app a pending line is normal while a container
  finishes cold-starting, and one failing answer right after any deploy can
  be transient.
- A broken deploy alarms only when an hourly pass judges it, within about
  70 minutes, never at once: do not tell the user a broken deploy would
  already have alarmed, and do not read a pending line, or an old
  `healthy`, as proof the new deploy works.
- `restart_app` does **not** re-fire the probe or update the deployment
  record, so it will not clear or refresh a pending status.
- Re-running the whole tag run (`gh run rerun <run-id>`, without `--job`: a
  container deploy needs the image that same run's `container` job scanned,
  kept for only one day) finalizes another deploy, whose probe records a
  healthy answer at once but defers a failing one again and restarts the 10
  minutes in which an hourly pass defers. A re-run can confirm a fix sooner
  than the next hourly pass, but it never surfaces a failure sooner, and it
  can delay the alarm.
