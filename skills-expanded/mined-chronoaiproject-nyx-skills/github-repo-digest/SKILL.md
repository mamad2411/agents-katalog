---
name: github-repo-digest
description: "Given an owner repo rank recent GitHub activity into an actionable digest."
metadata:
  category: runtime-based
  tag:
    - "github"
    - "digest"
  output-type: text
  runtime:
    - "aevatar-workflow"
version: "0.1"
---


# GitHub repo digest

This skill runs a prebuilt aevatar workflow (`github_repo_digest`) that turns one GitHub
repository into a single ranked, **most-actionable-first** digest. It is the native aevatar
re-expression of the common GitHub "triage signal" pattern — *read recent activity, surface
what a maintainer should look at first* — distilled to a **read-only** capability (no labeling,
no merging, no writes; see *Scope* below).

A run does three things, in order:

1. **Fetch** — three `nyxid_proxy` GET calls against `api-github`: open issues, open PRs, and
   recent releases for the target repo. All read-only; `owner`/`repo` go in the URL path.
2. **Rank** — one batched `llm_call` (triager role) folds the three lists into one ranked digest,
   most-actionable-first (breaking/security/bug signals, review-ready or stale PRs, latest release).
3. **Digest** — the ranked result is the workflow output and is watchable in the observatory.

There is no write back to GitHub and no per-run database write — **the run is the record**.


## Protocol (follow in order)

1. **Confirm the connector is connected.** This instance is wired to the nyxid connector
   `api-github` (GitHub REST API, `https://api.github.com`, bearer injected by NyxID). Call
   `nyxid_services` `{"action":"list"}` and confirm that slug is present and `allowed`. If it is
   missing, stop — connect GitHub before running.
2. **Supply the repository in the prompt.** The engine has **no clock** and the workflow has no UI
   form, so the run prompt is the only input. Provide the target on its own line as
   **`owner/repo: <owner>/<repo>`** (e.g. `owner/repo: facebook/react`). The workflow splits this on
   `/` to fill the GitHub path. You may add a recency note ("focus on the last 7 days") — it shapes
   ranking only; the fetch already returns the freshest items first (`sort=updated`).
3. **Run it.** Call `aevatar_start_workflow` with `workflow_id: "github_repo_digest"` and
   `inputs.prompt` set to the `owner/repo: …` line (plus any note). A clean `run_finished` with no
   `run_error` means it executed end to end; then scan the digest output for error-shaped content
   (e.g. a GitHub `"message":"Not Found"` body would mean a bad owner/repo or an unauthorized repo).
4. **Report honestly.** Return the ranked digest and the observatory link. State that you verified
   it ran **structurally**; the ranking is a best-effort read, not an objective priority order.

### Scheduling

The engine does not schedule itself. "Recurring" means an **external trigger** (a scheduled agent
or any cron caller) invokes `aevatar_start_workflow` on an interval, each time passing the same
`owner/repo: …` line. Set that trigger up separately; this skill is the thing it calls.


## Inputs

| Input | Where | Purpose |
|---|---|---|
| `prompt` | `inputs.prompt` | Must contain `owner/repo: <owner>/<repo>` on its own line. Required — it is the only place the target repo (and any recency window) can enter; the engine has no clock and no form. |
| source (connector slug) | hardcoded in the YAML | Wired to `api-github` → `https://api.github.com`. Three read-only GETs: `/repos/{owner}/{repo}/issues`, `/pulls`, `/releases`. Edit the `fetch_*` bodies to retarget another GitHub-shaped connector. |

## Output

A single ranked digest (text), grouped **Top signals → Open issues → Open PRs → Latest release**,
one line per item: `<#number> — <title> — <why it matters / staleness note> — <url>`. Empty sections
are stated explicitly. Also persisted as the run record in the observatory.


## Scope (what this draft deliberately does and does not do)

- **Does:** read-only fetch of three activity streams for one repo, deterministic owner/repo parse,
  one batched ranking pass, a most-actionable-first digest, observatory visibility.
- **Does not (v1):**
  - **Any write to GitHub.** No labeling, commenting, merging, closing, releasing, or re-running CI.
    The ECC source does all of those via the `gh` CLI; this skill is intentionally **read-only**
    (a connector with a read-scoped token cannot do more, and a digest should not mutate the repo).
    Write actions belong in a separate, explicitly write-capable skill.
  - **CI / Actions, Dependabot, and secret-scanning signal.** Those need additional GitHub endpoints
    (and often elevated scopes); kept out so the first run stays read-light and unprivileged.
  - **Cross-run dedup / "only new since last time".** That needs state that outlives a run, which in
    aevatar belongs to an **actor / read-model**, not a stateless workflow. Do not fake it with
    in-workflow memory. v1 relies on `sort=updated` + the recency note in the brief.
  - **Hard counts.** Any exact total ("12 open issues") must come from a `transform`, never the LLM
    (engine rule). v1 describes volume qualitatively and avoids asserting counts.
  - **Pagination beyond the first page.** `per_page` caps each list (10 issues, 10 PRs, 5 releases);
    busy repos are truncated to the most-recently-updated window by design.

See `DESIGN.md` for the full ECC → aevatar mapping, connector dependency, verification checklist
(incl. "connector active but not live-probed"), how `owner/repo` is parsed, and scope cuts.
