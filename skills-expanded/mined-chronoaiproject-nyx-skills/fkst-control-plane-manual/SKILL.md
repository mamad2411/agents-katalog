---
name: fkst-control-plane-manual
description: >-
  Operator manual for the fkst-hosted control plane — how to start, drive, monitor, and
  stop autonomous fkst-substrate coding sessions through GitHub issues (the source of
  truth; the dashboard/REST API reads and writes those same issues). Use whenever you need
  to: (a) launch a session by opening an `fkst-substrate-trigger` issue with the exact
  `### Session Name` / `### Packages` / `### Manifest` / `### Work Label` / optional
  `### Environment` / `### Auto-merge` / `### FKST Contributors` (alias: `### Log Access
  Allowlist`) / `### Session Collaborators` / `### Output Language` / `### Engine Config`
  body; (b) queue tasks by opening issues that carry the session's work labels;
  (c) interpret the session's status comments and labels (registered / picked-up /
  degraded / retired / invalid / config-rejected / unauthorized) and the dashboard's
  typed recovery states; (d) download a session's redacted logs (whole-session or
  per-run) from the identity-gated `/api/v1/logs/{session_id}` endpoint; or (e) stop or
  idle a session by closing issues. Covers the package-reference grammar
  `owner/repo@ref:path`, manifest expansion, work-label auto-discovery, config
  immutability, the idle-vs-permanent lifecycle, the one-work-label-per-trigger rule,
  and control-plane availability (`/ready`, restart/failover 503 windows).
version: "0.2"
homepage: https://github.com/ChronoAIProject/fkst-hosted
user-invocable: /fkst-control-plane-manual
metadata:
  category: plain
  tag:
    - fkst-hosted
    - control-plane
    - substrate
    - github-issues
    - manual
lastUpdated: 2026-07-22
---

# fkst-hosted control plane — operator manual

**fkst-hosted** is a GitHub-App-driven control plane on Kubernetes that runs autonomous
**fkst-substrate** coding sessions. **GitHub issues are the source of truth**: you start a
session by opening an issue, queue work by opening more issues, watch progress through the
comments/labels the control plane writes back, and stop it by closing issues. A web
dashboard and REST API exist as first-class front-ends — `POST
/api/v1/repos/{owner}/{name}/sessions` opens a trigger issue as the signed-in user and
`DELETE …/sessions/{issue_number}` closes it — but they read and write those same issues;
there is no session state that lives anywhere else. The control plane reconciles the
declared state (open trigger issues) toward reality (one Kubernetes pod per live session).

## Mental model

| Concept | Is a… | You control it by… |
|---|---|---|
| **Session** | one long-lived substrate agent (one K8s pod) | opening/closing a **trigger issue** |
| **Trigger issue** | the session's declaration (its name, packages, work labels) | an issue labeled `fkst-substrate-trigger` |
| **Work item** | one task for the session to pick up | an issue carrying one of the session's **work labels** |
| **Session id** | stable UUID = `derive_session_id(installation, owner, repo, trigger#)` | derived — stable across idle→revive |

One trigger issue ⇒ one session. Open work-label issues ⇒ the queue that session works,
each as its own PR. The reconciler polls open issues, so actions land within a sweep
(seconds), not instantly.

## 1. Start a session — open a trigger issue

Open a GitHub issue **labeled `fkst-substrate-trigger`** whose **body** has these `### `
sections (matched by exact heading; a duplicate `### ` heading → the issue is flagged
invalid). Intro text before the first heading is ignored.

| Section | Required | Rule |
|---|---|---|
| `### Session Name` | **yes** | exactly one non-empty line; `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$`, 1–40 chars, so it composes into K8s object names |
| `### Packages` | one of Packages / Manifest | zero or more lines, each a fully-qualified ref `owner/repo@ref:path` (see grammar below). May be omitted entirely when `### Manifest` supplies the packages |
| `### Manifest` | one of Packages / Manifest | zero or more refs in the **same grammar**, each whose `path` points at a **fkst-manifest JSON file** (`{"schemaVersion":1, "packages":[…]}`, ≤64 packages). Expanded on every reconcile pass, **fail-closed**: an unreachable/unparseable manifest, wrong schemaVersion, empty or oversized package list, or any malformed entry flags the trigger `fkst-substrate-invalid`. Effective packages = explicit `### Packages` ++ each manifest's expansion, deduped by full `(owner,repo,ref,path)`, explicit-first |
| `### Work Label` | optional | when present: exactly one non-empty line, a valid GitHub label, **≤ 50 chars, no comma** (the substrate reads it from a comma-separated env var). When absent, wake labels are **auto-discovered** from the effective packages' declared `[github].work_labels` (walked transitively through package `[event_deps]`). A session whose *effective* label set ends up empty is flagged `fkst-substrate-invalid` — add a `### Work Label` or use packages that declare work labels |
| `### Environment` | optional | one pre-provisioned environment name to inject (or blank → none). **Never put secret values here** — this only *selects* a profile provisioned out-of-band |
| `### Auto-merge` | optional | `true`/`yes`/`on`/`enabled`/`1` (case-insensitive) → mergeable PRs authored by the App bot are auto-merged and the linked work issue auto-closed; anything else → off. **Scope is per-repo:** if any open session on the repo enables it, all of the bot's mergeable PRs on that repo are auto-merged — not just this session's |
| `### FKST Contributors` | optional | the session's TRUSTED USERS (author always included): (1) the substrate only acts on issues/comments from these logins — injected as `FKST_GITHUB_AUTHORIZED_LOGINS` into the session for the packages' github author policy; (2) they may also download the session's redacted logs. Whitespace/comma/newline separated; leading `@` stripped; numeric ids work for log download only (the author policy matches logins). Legacy heading `### Log Access Allowlist` is still accepted as an alias (both headings may coexist — tokens merge, deduped case-insensitively). **Frozen at registration** |
| `### Session Collaborators` | optional | logins granted **work-item authority** alongside the trigger author. Only matters when the deployment enables the work-issue authority gate (`FKST_ENFORCE_WORK_ISSUE_AUTHZ=true`, default off): then only the **author ∪ Session Collaborators ∪ repo admins / org owners** may raise, label, or comment work issues — anyone else's work-label issue is visibly rejected once (durable `fkst-unauthorized` label + comment) and not picked up. On an admin-lookup error, author ∪ collaborators stay enforced for that pass — only the admin tier is temporarily unavailable (never a full fail-open). Same tokenization as FKST Contributors; **frozen at registration** |
| `### Output Language` | optional | one locale tag (`^[a-z]{2,3}([-_][A-Za-z0-9]{2,8})?$`, e.g. `en`, `zh`, `zh-CN`) → the session's packages emit user-visible prose (issue/PR comments) in that locale via `FKST_OUTPUT_LANG`. The value must **exactly** match a `locales/<value>.lua` file shipped by the session's package (case- and separator-sensitive); a mismatch silently falls back to English. Absent/blank → English |
| `### Engine Config` | optional | advanced engine tunables, one `KEY=value` per line from a strict allowlist: `FKST_CODEX_PERMIT_SLOTS` (1–32), `FKST_QUEUE_CAPACITY` / `FKST_MAX_IN_FLIGHT_PER_DEPT` / `FKST_DURABLE_ADMISSION_BURST_PER_DEPT` (1–1024), `FKST_RETRY_DEFAULT_MAX_ATTEMPTS` (1–100), the four duration keys `FKST_RETRY_DEFAULT_BASE` / `FKST_RETRY_DEFAULT_CAP` / `FKST_DEPARTMENT_DEFAULT_STALL_WINDOW` / `FKST_SUBSCRIBER_ABSENT_DELIVERY_BUDGET` (`<n>s\|m\|h`, 1s–7d normalized; effective retry `CAP >= BASE`, defaults 60s/30m), and `FKST_RATE_POOL_<NAME>=<burst>,<refill/min>` (`NAME` must match `^[A-Z0-9_]+$`, `ROOT` reserved; platform pool defaults can only be TIGHTENED, never widened). A repeated key, `FKST_OUTPUT_LANG` (use its own section), or any other key → `fkst-substrate-invalid` with the rule in the comment |

### Package reference grammar — `owner/repo@ref:path`
Split greedily on the **first `@`** (`owner/repo` vs `ref:path`), then the **first `:`**
(`ref` vs `path`).
- `owner`, `repo`: `^[A-Za-z0-9_.-]+$`, exactly one `/` between them.
- `ref`: branch/tag/SHA, `^[A-Za-z0-9_./-]+$`, no `..` segment.
- `path`: repo-relative, `^[A-Za-z0-9_./-]+$`, not absolute, no `..` segment.

`### Manifest` lines use the byte-identical grammar; the only difference is what `path`
points at — the manifest JSON file itself, not a package directory.

Example — a devloop session against `ChronoAIProject/fkst-packages@dev`:
```
### Session Name
sitebuilder

### Packages
ChronoAIProject/fkst-packages@dev:packages/github-devloop
ChronoAIProject/fkst-packages@dev:packages/github-devloop-pr
ChronoAIProject/fkst-packages@dev:packages/github-devloop-ops
ChronoAIProject/fkst-packages@dev:packages/consensus

### Work Label
site-build

### Auto-merge
true
```

Minimal manifest-driven trigger (valid as-is — no `### Packages`, no `### Work Label`;
the label set auto-discovers from the manifest's packages). The control plane's
install-seeder generates this shape, additionally setting `### Auto-merge` `true` and
`### FKST Contributors` to the installing owner:
```
### Session Name
default-workflows

### Manifest
ChronoAIProject/fkst-packages@fkst-hosted:manifests/default-workflows.json
```

Create it with the CLI:
`gh issue create --repo <owner>/<repo> --title "[session] sitebuilder" --body-file body.md --label fkst-substrate-trigger`

> ⚠️ The App must be **installed on the repo** and able to **reach every package and
> manifest ref** (public, or in a repo the App can read). An unreachable ref, a failed
> manifest expansion, a malformed body, an empty effective label set, or losing a
> work-label collision (see Rules of thumb) makes the reconciler flag the trigger
> `fkst-substrate-invalid` with a comment explaining the fix — fix the cause and the flag
> clears on the next sweep.

## 2. Queue work — open work-label issues

Open one issue **per task**, labeled with one of the session's **work labels** (the
explicit `### Work Label` or any package-discovered label — the registration comment
lists the full effective set). Give each a clear title, the **exact files** to change,
real acceptance criteria, and enough spec to be worked in isolation (the agent sees that
one issue + the repo, not the sibling backlog). The session picks them up, opens a PR per
issue, and (if `Auto-merge` is on) merges + closes them. Admission is **exact-label**:
only the session's work labels admit work — package lifecycle-prefix labels never do.

With the authority gate on (`FKST_ENFORCE_WORK_ISSUE_AUTHZ=true`), a work issue from
anyone outside author ∪ `### Session Collaborators` ∪ repo admins/org owners is rejected
visibly — a one-time comment plus a durable `fkst-unauthorized` label — and not picked up;
it also does not count as pending work (it neither wakes nor keeps a session alive). The
latch self-heals: if the author later passes the gate (e.g. becomes a repo admin), the
label is cleared and the issue is worked. During a transient admin-lookup failure the
admin tier is unavailable for that pass — author and collaborators are still honored, but
a repo admin outside both may be temporarily rejected until a later pass recovers.

## 3. Read the status the control plane writes back

| Signal | Where | Meaning |
|---|---|---|
| 🟢 `session … registered` comment | trigger issue | session accepted; lists the **full effective work-label set**, a hidden config-hash marker, and (when the deployment configures a public base URL) the **📥 Logs:** URL |
| 👀 pick-up comment | work issue | the control plane admitted this work item to the session's queue (it proves admission, not that the pod has started it). With the authority gate off, only explicit-`### Work Label` issues are acked — discovered-label issues are worked without the ack; with the gate on, the full label set is acked |
| PR by the App bot | repo PRs | the session's output for a work item |
| `fkst-degraded` label + comment | trigger issue | the pod looks unhealthy: a restart/bad pod phase, a **single error-level framework line** (including package bootstrap failures — the comment quotes the structured failure), or a warning recurring ≥3×; cleared when it reads healthy again |
| `fkst-session-retired` label + comment | still-open work issues | the trigger was closed → session retired; the item is no longer worked |
| `fkst-substrate-invalid` label + comment | trigger issue | the body failed to parse, a package/manifest ref is unreachable or its expansion failed, the effective label set is empty, or this trigger lost a work-label collision — fix and it clears |
| `fkst-config-rejected` label + comment | trigger issue | you edited the config of an already-registered session (see immutability) |
| `fkst-unauthorized` label + comment | work issue | the author is outside the session's work-item authority (only with `FKST_ENFORCE_WORK_ISSUE_AUTHZ=true`); rejected once, not picked up while the latch stands (self-heals if the author later passes the gate) |

### Label glossary
`fkst-substrate-trigger` (you apply, to declare a session) · **your work labels** (you
apply, to queue work) · `fkst-substrate-active` (latched once announced) · `fkst-picked-up`
(latched on a claimed work issue) · `fkst-session-retired` · `fkst-degraded` ·
`fkst-substrate-invalid` · `fkst-config-rejected` · `fkst-unauthorized`. The `fkst-*`
status labels are managed by the control plane — you don't set them.

### Dashboard recovery states
The dashboard (and canvas API) additionally projects a typed per-session recovery state —
`normal` / `idle` / `recovering` / `degraded` / `unknown` / `retired` / `invalid` — with a
reason and a runtime sub-state. Two are easy to misread: `recovering` with reason
`runtime_absent` is **normal** during idle→revive (the pod is being respawned), and
`unknown` with `runtime_observation_unavailable` means the backend can't observe the
runtime right now — **not** that the session is dead. The GitHub labels above remain the
durable record; the projection is a read-side convenience.

## 4. Lifecycle — idle vs. permanent

- **Close the trigger issue = stop.** The session is retired and the pod cleaned up; a
  closed trigger is never re-registered **while it stays closed** — but reopening the
  issue revives the same session under its original frozen config, so close-and-leave-closed
  is the permanent stop. When a running session is retired, its still-open work issues get
  `fkst-session-retired` + a comment and any stale `fkst-picked-up` label is removed (a
  trigger closed while the session is already idle, or work opened after retirement, may
  not receive the marker).
- **Trigger open + no open work = idle.** The pod is killed to save resources, but the
  session **auto-revives** (re-spawns) the moment a new matching work issue appears — no new
  trigger needed. So: to pause, close/merge all work; to resume, open a work issue.
- **An open work issue keeps the pod alive** — on any of the session's effective labels,
  discovered ones included. Merge/close finished work to let a session idle down.

## 5. Config immutability

Once a session has registered, its config (`### Session Name` / `### Packages` /
`### Manifest` refs / `### Work Label` / `### Environment` / `### Auto-merge` /
`### FKST Contributors` / `### Session Collaborators` / `### Output Language` /
`### Engine Config`) is **frozen**. Editing the trigger body does **not** re-launch — the
control plane posts a one-time `fkst-config-rejected` comment. **To change config, close
the trigger and open a new one.** (This is why `### FKST Contributors` can't be widened
after the fact to grant retroactive log access.)

One deliberate exception: `### Manifest` entries are frozen **by reference**, not by
content. Editing the referenced manifest JSON upstream changes the effective package set
on the next reconcile pass with no config-rejection — pin manifests to an immutable ref
(tag/SHA) if you don't want that.

## 6. Download a session's logs

Sessions **auto-stream their redacted logs** to storage (when the deployment configures
log storage); the 📥 Logs URL in the
registration comment is `…/api/v1/logs/{session_id}`. Access is **identity-gated, deny by
default**, authorized if the requester is the **trigger author**, on the **`### FKST
Contributors` allow-list**, or a **global admin**. Two ways in:
- **Browser** — just open the URL; it redirects through GitHub login, then the redacted
  `.tar.gz` downloads. (No S3 URL is ever exposed; the control plane streams the bytes.)
- **Agent/API** — `GET …/api/v1/logs/{session_id}` with `Authorization: Bearer <github-token>`;
  the token is traded for your identity and the redacted `.tar.gz` streams back.

The default download is the session's latest bundle. `GET
…/api/v1/logs/{session_id}/runs` (same identity tiers, plus the deployment access
allowlist, which can 403 independently) lists the session's runs, and `?run=<run_id>` on
the download URL selects that run's bundle — **API/Bearer mode only**: a browser download
always serves the latest bundle regardless of `?run=`. Completed runs' bundles are
immutable; the current run's is still being flushed.

Logs are the latest flush — refreshed every ~20 s / 256 KB by default (deployment-tunable
via `FKST_LOG_FLUSH_SECS` / `FKST_LOG_FLUSH_BYTES`) and on pod exit; downloads may lag up
to ~30 s behind (server-side bundle cache). They are **redacted** (secrets masked) — safe
to share with an authorized user, but treat them as session-sensitive.

Deployments may configure `FKST_GLOBAL_ADMINS` with comma-separated GitHub logins
(or rename-safe numeric IDs). A verified global admin's dashboard spans every account
and repository where the deployment's GitHub App is installed, and the admin may read
the associated session details, outcomes, logs, and observe snapshots. The legacy
`FKST_LOG_ADMINS` list remains log/observe-only and does not widen the dashboard.

## 7. Control-plane availability — `/ready` and 503 windows

`GET /ready` (unauthenticated) is the recovery diagnostic: `200` with `status: "ready"`
once the latest full discovery pass has completed, else `503` with `status: "recovering"`
(startup/failover resync in progress — wait) or `"degraded"` (the latest pass failed or
was partial — investigate), plus `startup_resync_complete` and leader fields. `/health` is
pure process liveness and says nothing about recovery.

In the canonical high-availability deployment (two replicas,
`FKST_LEADER_ELECTION_ENABLED=true`), **every `/api/v1/*` endpoint — logs, observe,
dashboard API — and the webhook return a bare `503`** until one replica holds the Lease,
has completed a full startup resync, and has published the leader routing label. During a
restart, deploy, or failover this window is normally seconds to a couple of minutes —
retry. A *persistent* 503 means the discovery pass keeps failing (`/ready` shows
`degraded`; a failed periodic resync re-opens the gate mid-operation) — investigate. A
follower replica probed directly always answers `/ready` `503` with `leader: false` — that
is its normal state, not a fault. With leader election disabled (single-replica dev
deployments) there is no API gate and the API serves throughout startup.

A trigger opened right after a deploy is registered as the recovery pass enumerates its
repo; `/ready` reaching `200` means that discovery pass has finished — so if nothing has
happened one sweep after `/ready` is `200`, investigate rather than keep waiting.

## Rules of thumb (learned the hard way)

- **One work label per open trigger, per repo.** If two open triggers share a label
  (explicit or package-discovered), the control plane resolves the collision
  authoritatively: the **lowest-numbered trigger owns the queue** and every other holder
  is demoted `fkst-substrate-invalid` with a comment (auto-clearing once the collision is
  resolved). You still want distinct labels — the loser's session simply doesn't run.
- **Wave the backlog by dependency.** Land foundational work issues, **merge them**, *then*
  open the issues that build on them. A dependent issue worked before its foundation merges
  can yield an empty diff or reference files not yet on the branch. Dependency ordering — not
  wording — is the usual failure mode.
- **One feature per work issue**, named in the title, with exact files + checkable acceptance
  criteria.
- **Never put secrets, tokens, or env *values* in an issue.** Use `### Environment` to *select*
  a pre-provisioned profile; values are supplied out-of-band, never read from the issue.
- **Give it a sweep.** Actions are reconciled on a poll; expect seconds, and re-check the
  issue's comments/labels rather than expecting instant effect. Two slower cases: the
  **first trigger on a repo with no existing registration** is discovered by a webhook
  nudge or the periodic full resync (default ~10 min) — everything after that lands within
  the ~30 s sweep; and right after a control-plane restart/failover, check `/ready` first
  (§7).

## Observe a session's engine state

`GET /api/v1/sessions/{session_id}/observe?limit=N` (identity authorization as for the
log download — trigger author / `### FKST Contributors` / deployment global admins /
legacy log admins — **plus** the deployment's access allowlist, which can 403
independently; GitHub Bearer token) returns the engine's live observe snapshot as raw
JSON — per-queue depth / pending / in-flight / retrying, oldest-pending age, subscriber
status, DLQ tombstones, and codex-run records. It never contains payload bodies. `limit`
is clamped to 1..=10000 (default 500). A `409` means the session's packages declare no
reliable subscriptions (nothing to observe); a `404` means the session or its runtime is
unknown; a `503` means the control plane can't reach the runtime right now (pod dispatch
disabled, or the in-pod query failed) — retry or check the dashboard's recovery state.
