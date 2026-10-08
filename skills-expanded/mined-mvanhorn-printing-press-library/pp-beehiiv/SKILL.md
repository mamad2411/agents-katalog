---
name: pp-beehiiv
description: "Sync your Beehiiv audience to a local database and answer growth questions offline in one command. Trigger phrases: `check my beehiiv growth`, `subscriber sources`, `which send time works best`, `compare my publications`, `lookup subscriber email`, `use beehiiv`, `run beehiiv`."
author: "Kevin Magnan"
license: "Apache-2.0"
argument-hint: "<command> [args] | install cli|mcp"
allowed-tools: "Read Bash"
metadata:
  openclaw:
    requires:
      bins:
        - beehiiv-pp-cli
---

# Beehiiv — Printing Press CLI

## Prerequisites: Install the CLI

This skill drives the `beehiiv-pp-cli` binary. **You must verify the CLI is installed before invoking any command from this skill.** If it is missing, install it first:

1. Install via the Printing Press installer. It defaults binaries to `$HOME/.local/bin` on macOS/Linux and `%LOCALAPPDATA%\Programs\PrintingPress\bin` on Windows:
   ```bash
   npx -y @mvanhorn/printing-press-library install beehiiv --cli-only
   ```
2. Verify: `beehiiv-pp-cli --version`
3. Ensure the reported install directory is on `$PATH` for the agent/runtime that will invoke this skill.

If the `npx` install fails (no Node, offline, etc.), fall back to a direct Go install (requires Go 1.26.6 or newer). This installs into `$GOPATH/bin` (default `$HOME/go/bin`), so add that directory to `$PATH` instead:

```bash
go install github.com/mvanhorn/printing-press-library/library/marketing/beehiiv/cmd/beehiiv-pp-cli@latest
```

If `--version` reports "command not found" after install, the runtime cannot see the binary directory on `$PATH`. Do not proceed with skill commands until verification succeeds.

Beehiiv-pp-cli mirrors publications, subscribers, segments, posts, podcasts, and more into SQLite. Insights commands compute source attribution, churn sources, send-time performance, and cross-publication comparisons with zero API calls. The full v2 surface, including 2026-09 additions like podcasts, exports, and complimentary access, ships as typed commands with dry-run and agent output.

## When to Use This CLI

Use this CLI for offline audience analytics, bulk subscriber operations, scripting, and CI pipelines. Use it when you want agent-ready JSON output with select/compact/quiet modes and a local store that answers growth questions without API calls.

## Anti-triggers

Do not use this CLI for:
- Do not use this CLI for beehiv documentation search; use the official docs MCP at developers.beehiiv.com/_mcp/server
- Do not use this CLI for OAuth app authorization flows; it is an API-key client
- Creating a post with confirmed status and no scheduled_at publishes (sends) immediately; use --dry-run first to inspect the request

## Unique Capabilities

These capabilities aren't available in any other tool for this API.

### Growth answers from the local store
- **`insights subscriber-sources`** — See exactly where new subscribers come from: UTM, channel, and referring site, grouped in one call.

  _Reach for this when a growth question needs source attribution without paging the full subscriber list through the API._

  ```bash
  beehiiv-pp-cli insights subscriber-sources pub_477b0b68-0ab1-4b3f-954e-d1f6302b58a7 --limit 20 --agent
  ```
- **`insights post-performance`** — Review recent sends with status, timing, and expanded stats in one compact table.

  _Reach for this after a send to review performance without burning per-post API calls._

  ```bash
  beehiiv-pp-cli insights post-performance pub_477b0b68-0ab1-4b3f-954e-d1f6302b58a7 --limit 10 --agent
  ```
- **`insights referral-health`** — Check referral-program config and how many subscribers actually carry referral codes.

  _Reach for this when tuning referral loops to see configuration versus real coverage._

  ```bash
  beehiiv-pp-cli insights referral-health pub_477b0b68-0ab1-4b3f-954e-d1f6302b58a7 --agent
  ```
- **`insights subscriber-lookup`** — Find one subscriber by email or subscription ID and get a compact record instantly.

  _Reach for this for support questions about a single subscriber when offline speed matters._

  ```bash
  beehiiv-pp-cli insights subscriber-lookup pub_477b0b68-0ab1-4b3f-954e-d1f6302b58a7 reader@example.com --agent --select subscription.email,subscription.status
  ```
- **`insights churn-sources`** — See which sources, channels, and campaigns drive unsubscribes.

  _Reach for this when unsubscribes spike and you need the offending channel fast._

  ```bash
  beehiiv-pp-cli insights churn-sources pub_477b0b68-0ab1-4b3f-954e-d1f6302b58a7 --limit 20 --agent
  ```
- **`insights send-times`** — Find your best send slot: open rate by weekday and hour from your own history.

  _Reach for this when scheduling the next send and you want evidence over habit._

  ```bash
  beehiiv-pp-cli insights send-times pub_477b0b68-0ab1-4b3f-954e-d1f6302b58a7 --agent
  ```
- **`insights compare-publications`** — Side-by-side growth and engagement across every synced publication.

  _Reach for this when managing several publications and a client report needs one comparison table._

  ```bash
  beehiiv-pp-cli insights compare-publications --agent --select publications.name,publications.net_growth
  ```

## Command Reference

**advertisement-opportunities** — Manage advertisement opportunities

- `beehiiv-pp-cli advertisement-opportunities <publicationId>` — Get advertisement opportunities <Badge intent='info' minimal outlined>OAuth Scope: posts:read</Badge>

**authors** — Manage authors

- `beehiiv-pp-cli authors index` — Retrieve a list of authors available for the publication.
- `beehiiv-pp-cli authors show` — Retrieve a single author from a publication.

**automations** — Manage automations

- `beehiiv-pp-cli automations index` — List automations <Badge intent='info' minimal outlined>OAuth Scope: automations:read</Badge>
- `beehiiv-pp-cli automations show` — Get automation <Badge intent='info' minimal outlined>OAuth Scope: automations:read</Badge>

**bulk-subscription-updates** — Manage bulk subscription updates

- `beehiiv-pp-cli bulk-subscription-updates index` — List subscription updates <Badge intent='info' minimal outlined>OAuth Scope: subscriptions:read</Badge>
- `beehiiv-pp-cli bulk-subscription-updates show` — Get subscription update <Badge intent='info' minimal outlined>OAuth Scope: subscriptions:read</Badge>

**bulk-subscriptions** — Manage bulk subscriptions

- `beehiiv-pp-cli bulk-subscriptions <publicationId>` — Bulk create subscription <Badge intent='info' minimal outlined>OAuth Scope: subscriptions:write</Badge>

**complimentary-access** — Manage complimentary access

- `beehiiv-pp-cli complimentary-access index` — Retrieve complimentary access objects for the publication.
- `beehiiv-pp-cli complimentary-access show` — Retrieve a single complimentary access object.

**condition-sets** — Manage condition sets

- `beehiiv-pp-cli condition-sets index` — Retrieve all active condition sets for a publication.
- `beehiiv-pp-cli condition-sets show` — Retrieve a single active dynamic content condition set for a publication.

**custom-fields** — Manage custom fields

- `beehiiv-pp-cli custom-fields create` — Create custom field <Badge intent='info' minimal outlined>OAuth Scope: custom_fields:write</Badge>
- `beehiiv-pp-cli custom-fields delete` — Delete custom field <Badge intent='info' minimal outlined>OAuth Scope: custom_fields:write</Badge>
- `beehiiv-pp-cli custom-fields index` — List custom fields <Badge intent='info' minimal outlined>OAuth Scope: custom_fields:read</Badge>
- `beehiiv-pp-cli custom-fields patch` — Update custom field <Badge intent='info' minimal outlined>OAuth Scope: custom_fields:write</Badge>
- `beehiiv-pp-cli custom-fields put` — Update custom field <Badge intent='info' minimal outlined>OAuth Scope: custom_fields:write</Badge>
- `beehiiv-pp-cli custom-fields show` — Get custom field <Badge intent='info' minimal outlined>OAuth Scope: custom_fields:read</Badge>

**data-privacy** — Manage data privacy

- `beehiiv-pp-cli data-privacy data-deletion-create` — <Warning>This is a gated feature that requires enablement.
- `beehiiv-pp-cli data-privacy data-deletion-index` — <Warning>This is a gated feature that requires enablement.
- `beehiiv-pp-cli data-privacy data-deletion-show` — <Warning>This is a gated feature that requires enablement.

**email-blasts** — Manage email blasts

- `beehiiv-pp-cli email-blasts index` — List email blasts <Badge intent='info' minimal outlined>OAuth Scope: posts:read</Badge>
- `beehiiv-pp-cli email-blasts show` — Get email blast <Badge intent='info' minimal outlined>OAuth Scope: posts:read</Badge>

**engagements** — Manage engagements

- `beehiiv-pp-cli engagements <publicationId>` — Retrieve email engagement metrics for a specific publication over a defined date range and granularity.

**exports** — Manage exports

- `beehiiv-pp-cli exports subscription-create` — Start a subscription export. Returns an existing in-progress export instead of starting a duplicate.
- `beehiiv-pp-cli exports subscription-index` — List subscription exports for the publication, newest first.
- `beehiiv-pp-cli exports subscription-show` — Get a subscription export. Poll until status is completed, then read download_url. Gated feature requiring enablement.

**newsletter-lists** — Manage newsletter lists

- `beehiiv-pp-cli newsletter-lists index` — <Note title='Currently in beta' icon='b'> Newsletter Lists is currently in beta, the API is subject to change.
- `beehiiv-pp-cli newsletter-lists show` — <Note title='Currently in beta' icon='b'> Newsletter Lists is currently in beta, the API is subject to change.

**podcasts** — Manage podcasts

- `beehiiv-pp-cli podcasts index` — List podcasts for the publication.
- `beehiiv-pp-cli podcasts show` — Retrieve a single podcast.

**polls** — Manage polls

- `beehiiv-pp-cli polls index` — Retrieve all polls belonging to a specific publication. Poll choices are always included.
- `beehiiv-pp-cli polls show` — Retrieve detailed information about a specific poll belonging to a publication.

**post-templates** — Manage post templates

- `beehiiv-pp-cli post-templates <publicationId>` — Retrieve a list of post templates available for the publication.

**posts** — Manage posts

- `beehiiv-pp-cli posts aggregate-stats` — Get aggregate stats <Badge intent='info' minimal outlined>OAuth Scope: posts:read</Badge>
- `beehiiv-pp-cli posts create` — <Note title='Currently in beta' icon='b'> This feature is currently in beta, the API is subject to change
- `beehiiv-pp-cli posts delete` — Delete or Archive a post. Any post that has been confirmed will have it's status changed to `archived`.
- `beehiiv-pp-cli posts index` — List posts <Badge intent='info' minimal outlined>OAuth Scope: posts:read</Badge>
- `beehiiv-pp-cli posts show` — Get post <Badge intent='info' minimal outlined>OAuth Scope: posts:read</Badge>
- `beehiiv-pp-cli posts update` — <Note title='Currently in beta' icon='b'> This feature is currently in beta, the API is subject to change

**publications** — Manage publications

- `beehiiv-pp-cli publications index` — List publications <Badge intent='info' minimal outlined>OAuth Scope: publications:read</Badge>
- `beehiiv-pp-cli publications show` — Get publication <Badge intent='info' minimal outlined>OAuth Scope: publications:read</Badge>

**referral-program** — Manage referral program

- `beehiiv-pp-cli referral-program <publicationId>` — Get referral program <Badge intent='info' minimal outlined>OAuth Scope: referral_program:read</Badge>

**segments** — Manage segments

- `beehiiv-pp-cli segments create` — Create a new segment.
- `beehiiv-pp-cli segments delete` — Delete a segment. Deleting the segment does not effect the subscriptions in the segment.
- `beehiiv-pp-cli segments index` — List segments <Badge intent='info' minimal outlined>OAuth Scope: segments:read</Badge>
- `beehiiv-pp-cli segments show` — Get segment <Badge intent='info' minimal outlined>OAuth Scope: segments:read</Badge>

**subscriptions** — Manage subscriptions

- `beehiiv-pp-cli subscriptions bulk-updates-patch` — Update subscriptions <Badge intent='info' minimal outlined>OAuth Scope: subscriptions:write</Badge>
- `beehiiv-pp-cli subscriptions bulk-updates-patch-status` — Update subscriptions' status <Badge intent='info' minimal outlined>OAuth Scope: subscriptions:write</Badge>
- `beehiiv-pp-cli subscriptions bulk-updates-put` — Update subscriptions <Badge intent='info' minimal outlined>OAuth Scope: subscriptions:write</Badge>
- `beehiiv-pp-cli subscriptions bulk-updates-put-status` — Update subscriptions' status <Badge intent='info' minimal outlined>OAuth Scope: subscriptions:write</Badge>
- `beehiiv-pp-cli subscriptions create` — Create subscription <Badge intent='info' minimal outlined>OAuth Scope: subscriptions:write</Badge>
- `beehiiv-pp-cli subscriptions delete` — <Warning>This cannot be undone. All data associated with the subscription will also be deleted.
- `beehiiv-pp-cli subscriptions get-by-email` — <Info>Please note that this endpoint requires the email to be URL encoded.
- `beehiiv-pp-cli subscriptions get-by-id` — <Info>In previous versions of the API, another endpoint existed to retrieve a subscription by the subscriber ID.
- `beehiiv-pp-cli subscriptions get-by-subscriber-id` — Get subscription by subscriber ID <Badge intent='info' minimal outlined>OAuth Scope: subscriptions:read</Badge>
- `beehiiv-pp-cli subscriptions index` — Retrieve all subscriptions belonging to a specific publication.
- `beehiiv-pp-cli subscriptions patch` — Update subscription by ID <Badge intent='info' minimal outlined>OAuth Scope: subscriptions:write</Badge>
- `beehiiv-pp-cli subscriptions put` — Update subscription by ID <Badge intent='info' minimal outlined>OAuth Scope: subscriptions:write</Badge>
- `beehiiv-pp-cli subscriptions update-by-email` — Update subscription by email <Badge intent='info' minimal outlined>OAuth Scope: subscriptions:write</Badge>

**tiers** — Manage tiers

- `beehiiv-pp-cli tiers create` — Create a tier <Badge intent='info' minimal outlined>OAuth Scope: tiers:write</Badge>
- `beehiiv-pp-cli tiers index` — List tiers <Badge intent='info' minimal outlined>OAuth Scope: tiers:read</Badge>
- `beehiiv-pp-cli tiers patch` — Update a tier <Badge intent='info' minimal outlined>OAuth Scope: tiers:write</Badge>
- `beehiiv-pp-cli tiers put` — Update a tier <Badge intent='info' minimal outlined>OAuth Scope: tiers:write</Badge>
- `beehiiv-pp-cli tiers show` — Get tier <Badge intent='info' minimal outlined>OAuth Scope: tiers:read</Badge>

**users** — Manage users

- `beehiiv-pp-cli users` — Identify user <Badge intent='info' minimal outlined>OAuth Scope: identify:read</Badge>

**webhooks** — Manage webhooks

- `beehiiv-pp-cli webhooks create` — Create a webhook <Badge intent='info' minimal outlined>OAuth Scope: webhooks:write</Badge>
- `beehiiv-pp-cli webhooks delete` — Delete a webhook <Badge intent='info' minimal outlined>OAuth Scope: webhooks:write</Badge>
- `beehiiv-pp-cli webhooks index` — List webhooks <Badge intent='info' minimal outlined>OAuth Scope: webhooks:read</Badge>
- `beehiiv-pp-cli webhooks show` — Get webhook <Badge intent='info' minimal outlined>OAuth Scope: webhooks:read</Badge>
- `beehiiv-pp-cli webhooks update` — Update webhook <Badge intent='info' minimal outlined>OAuth Scope: webhooks:write</Badge>

**workspaces** — Manage workspaces

- `beehiiv-pp-cli workspaces identify` — Identify workspace <Badge intent='info' minimal outlined>OAuth Scope: identify:read</Badge>
- `beehiiv-pp-cli workspaces permissions-show` — Retrieve the permissions granted to the OAuth or API token for this workspace.
- `beehiiv-pp-cli workspaces publications-by-subscription-email` — Retrieve all publications in the workspace that have a subscription for the specified email address.


### Finding the right command

When you know what you want to do but not which command does it, ask the CLI directly:

```bash
beehiiv-pp-cli which "<capability in your own words>"
```

`which` resolves a natural-language capability query to the best matching command from this CLI's curated feature index. Exit code `0` means at least one match; exit code `2` means no confident match — fall back to `--help` or use a narrower query.

## Recipes

### Mirror the audience

```bash
beehiiv-pp-cli sync --resources publications,subscriptions,segments,posts --max-pages 100
```

Cursor-paginated sync of the four growth-critical entities into SQLite.

### Agent-ready growth snapshot

```bash
beehiiv-pp-cli insights growth-summary pub_477b0b68-0ab1-4b3f-954e-d1f6302b58a7 --agent
```

Single read-only health summary computed from the local store.

### Narrow a deep lookup

```bash
beehiiv-pp-cli insights subscriber-lookup pub_477b0b68-0ab1-4b3f-954e-d1f6302b58a7 reader@example.com --agent --select subscription.email,subscription.status
```

Pair --agent with --select dotted paths to return only the fields an agent needs.

### Attribute a churn spike

```bash
beehiiv-pp-cli insights churn-sources pub_477b0b68-0ab1-4b3f-954e-d1f6302b58a7 --limit 20
```

Group unsubscribes by source, channel, UTM, and referrer offline.

### Ship a subscriber CSV

```bash
beehiiv-pp-cli search "@example.com" --type subscriptions --limit 1000 --csv > subscribers.csv
```

Every list and search command emits CSV for spreadsheets.

## Auth Setup

Create an API key at app.beehiiv.com (Settings > API Keys) and export BEEHIIV_API_KEY. The key is a bearer token scoped to your organization; 180 requests per minute are shared per org.

Run `beehiiv-pp-cli doctor` to verify setup.

## Agent Mode

Add `--agent` to any command. Expands to: `--json --compact --no-input --no-color`.

- **Pipeable** — JSON on stdout, errors on stderr
- **Filterable** — `--select` keeps a subset of fields. Dotted paths descend into nested structures; arrays traverse element-wise. Critical for keeping context small on verbose APIs:

  ```bash
  beehiiv-pp-cli advertisement-opportunities mock-value --agent --select advertisement_kind,advertiser_name,id
  ```
- **Previewable** — `--dry-run` shows the request without sending
- **Offline-friendly** — sync/search commands can use the local SQLite store when available
- **Non-interactive** — never prompts, every input is a flag
- **Explicit confirmation** — `--agent` does not imply `--yes`; pass `--yes` separately only after the target, arguments, and side effects are clear
- **Explicit retries** — use `--idempotent` only when an already-existing create should count as success, and use `--ignore-missing` only when a missing delete target should count as success

### Response envelope

Commands that read from the local store or the API wrap output in a provenance envelope:

```json
{
  "meta": {"source": "live" | "local", "synced_at": "...", "reason": "..."},
  "results": <data>
}
```

Parse `.results` for data and `.meta.source` to know whether it's live or local. A human-readable `N results (live)` summary is printed to stderr only when stdout is a terminal AND no machine-format flag (`--json`, `--csv`, `--compact`, `--quiet`, `--plain`, `--select`) is set — piped/agent consumers and explicit-format runs get pure JSON on stdout.

## Paths and state

Agents should treat the CLI's path resolver as part of the runtime contract:

- Use `--home <dir>` for one invocation, or set `BEEHIIV_HOME=<dir>` to relocate all four path kinds under one root.
- Use per-kind env vars only when a specific kind must diverge: `BEEHIIV_CONFIG_DIR`, `BEEHIIV_DATA_DIR`, `BEEHIIV_STATE_DIR`, `BEEHIIV_CACHE_DIR`.
- Resolution order is per-kind env var, `--home`, `BEEHIIV_HOME`, XDG (`XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, `XDG_CACHE_HOME`), then platform defaults.
- `config` contains settings like `config.toml` and profiles. `data` contains `credentials.toml`, `data.db`, cookies, and auth sidecars. `state` contains persisted queries, jobs, and `teach.log`. `cache` contains regenerable HTTP/cache files.
- Stored secrets live in `credentials.toml` under the data dir. Existing legacy `config.toml` secrets are read for compatibility and leave `config.toml` on the first auth write.
- Run `beehiiv-pp-cli doctor --fail-on warn` to surface path and credential-location warnings. `agent-context` exposes a schema v4 `paths` block for agents that need the resolved dirs.
- For MCP, pass relocation through the MCP host config. The MCP binary does not inherit CLI flags:

  ```json
  {
    "mcpServers": {
      "beehiiv": {
        "command": "beehiiv-pp-mcp",
        "env": {
          "BEEHIIV_HOME": "/srv/beehiiv"
        }
      }
    }
  }
  ```

Fleet precedence: an inherited per-kind env var overrides an explicit `--home` for that kind. Use `BEEHIIV_HOME` or per-kind vars as durable fleet levers, and use `--home` only for a single invocation. Relocation is not reversible by unsetting env vars; move files manually before clearing `BEEHIIV_HOME`, or `doctor` will not find credentials left under the former root.

## Automatic learning

This CLI ships a self-capturing learning loop. The CLI does its own bookkeeping: every invocation is journaled locally, a failed flag followed by a corrected retry auto-derives a `flag_alias` candidate, and a `teach` on a query family without a playbook auto-synthesizes a `playbook_candidate` from the session's journal. Your job is judgment only: `recall` first, act on surfaced candidates, `teach` the final answer, `playbook amend` when you observe a correction. You never record failures by hand.

### Step 1: `recall` before any discovery

Before list/search/drill commands on a new user question, run:

```bash
beehiiv-pp-cli recall "<user's question>" --agent
```

The response envelope:

```json
{
  "query": "...",
  "normalized": "<normalized form>",
  "query_entities": ["..."],
  "found": true | false,
  "match_score": 0.0,
  "results": [
    { "resource_id": "...", "resource_type": "...", "venue": "...",
      "confidence": 2, "entity_match": "exact|partial|unknown",
      "source": "taught|preseed|pattern", "warnings": ["..."] }
  ],
  "mismatches": [ /* only when --debug-mismatches */ ],
  "warnings": [ /* top-level */ ],
  "candidates": [
    { "id": 12, "class": "flag_alias | playbook_candidate",
      "summary": "...", "sightings": 3, "last_seen": "...",
      "rationale": "...",
      "next_action": ["<trial command>", "beehiiv-pp-cli learnings confirm 12"] }
  ],
  "playbook": {
    "query_family": "...",
    "playbook": {
      "steps": [ { "cmd": "<command with {slot} substitution>", "purpose": "..." } ],
      "entity_slots": ["$ENTITY"],
      "expected_tool_calls": 3
    },
    "slots_resolved": { "$ENTITY": { "token": "<live token>", "canonical": "<canonical>" } },
    "notes": "<workarounds + gotchas for this query family>"
  },
  "notes": "<duplicate surface for non-playbook callers>"
}
```

Empty-store short-circuit: if the store has no learnings, playbooks, or candidates yet (recall finds nothing and `learnings list` and `learnings candidates` are both empty), skip recall for the rest of this session instead of taxing every query; resume recall-first once something has been taught.

### Step 2: decision tree

Read `candidates`, `playbook`, `notes`, `results[0]`, and warnings in that order:

```
if Candidates present (warnings include "candidates_present"):
    -> candidates are try-then-confirm, never facts. Follow each candidate's
       two-step next_action verbatim: run the trial command first, then run
       `learnings confirm <id>` only after the trial verified the behavior.
       Reject a wrong candidate with `learnings reject <id>`.
    -> NEVER re-teach something recall surfaced as a candidate; confirm or
       reject that candidate instead of teaching a duplicate.
    -> candidates ride alongside playbooks and resource hits, not instead of
       them; continue with the branches below after acting on them.

if Playbook present:
    -> READ Playbook.notes verbatim FIRST (workarounds + gotchas the CLI surface doesn't expose)
    -> replay Playbook.steps in order, substituting Playbook.slots_resolved entries
       for the entity slot tokens. If a step's slot is unresolved, fall back to
       discovery for that step only.
    -> the Playbook's expected_tool_calls is a budget; if you find yourself running
       materially more, record the divergence via `beehiiv-pp-cli playbook amend`
       at end-of-session.

elif Notes present (no Playbook):
    -> read Notes verbatim before any discovery step; they carry known gotchas
       for this query family even when no structured choreography exists yet.

elif Found AND Results[0].EntityMatch == "exact" AND Results[0].Confidence >= 2:
    -> skip discovery; fetch live data for Results[*].ResourceID in parallel

elif Found AND Results[0].EntityMatch == "partial":
    -> candidate hint, NOT a hit; read the resource title to validate before trusting

elif (any row in Mismatches[] when --debug-mismatches was passed):
    -> treat as cold start; the stored learning is for a different entity
       (different canonical resolved from query_entities)

else:  // Found == false, no playbook, no notes
    -> cold start; run discovery normally; teach the answer afterward (Step 4).
       If the family has no playbook yet, that teach auto-synthesizes a
       playbook candidate from this session's journal - you do not need to
       record one by hand.
```

Playbook and Notes are orthogonal to the per-resource path. A recall response can carry both a Playbook AND a `Results[]` hit - use both: the Playbook tells you which choreography to run; the resource hits short-circuit specific steps. Default to skipping `mismatches`; pass `--debug-mismatches` only when investigating cold-start surprises.

Candidate judgment details: `learnings confirm <id>` prints the candidate's full payload before materializing it - check that the printed payload matches the behavior you verified. `learnings reject <id>` tombstones the derivation signature so the same candidate does not resurface. The envelope carries only the few candidates worth acting on now; `beehiiv-pp-cli learnings candidates` lists the full open set.

Graceful degradation: if `learnings confirm` is an unknown command, you are driving an older binary - ignore the candidates guidance and follow the rest of the protocol.

### Step 3: always read `warnings`

- `low_confidence`: row exists at `confidence<2`. Treat as a hint, not a skip-discovery hit.
- `resource_not_in_store`: the local store doesn't have the resource the learning points at. The match validator couldn't classify entities — direct-fetch and re-evaluate.
- `cross_alias_match` (per-result): the row was taught under a different alias and matched the live query's canonical via `entity_lookups` (e.g., a "USA" teach satisfying a "United States" recall). Trust the resource_id.
- `similar_shape_different_entity:<canonical>` (top-level): a structurally matching row exists but its canonical entity differs from the live query's. Treated as cold start; the warning carries the conflicting canonical as a hint, but the row is NOT promoted into Results.
- `ambiguous_alias` (top-level): a single query entity resolved to multiple canonicals (e.g., "Cards" → Arizona Cardinals + St. Louis Cardinals). Surface the ambiguity from context before committing to a resource.
- `candidates_present` (top-level): the envelope carries a `candidates` section. Handle it via the candidates branch in Step 2 before anything else.
- `lookup_refresh_available` (top-level): an entity in the query has no lookup row yet, but synced data could provide one. Run `beehiiv-pp-cli sync` to refresh entity lookups.
- Top-level `no_learnings_for_query_family`: the table had no rows above the Jaccard floor. Pure cold start.

### Step 4: `teach &` after finalizing your response - always

Teaching is unconditional. After resolving a query the store could not answer, background-teach the final resource mapping - no call-count threshold, no judging whether it was "worth" learning. The teach is the anchor of the loop: it triggers playbook synthesis for a family without a playbook, and same-referent phrasings fold into one family so near-duplicate teaches do not fragment the store. Fire it after assembling your user-facing response but BEFORE emitting it, with a shell `&` so the call returns immediately:

```bash
beehiiv-pp-cli teach --query "<user's question>" --resource-type <type> --resource <id1> --resource <id2>
# (append shell `&` to background it)
```

Silent on success. Errors only land in `teach.log` under the resolved state dir. Teach the **most specific** resource - if the user asked a broad question and you walked through parent records to find the specific answer, teach the leaf id, not the parent. The CLI uses seeded `entity_lookups` for cross-alias resolution at recall time, so a teach under one alias (e.g., "Niners") satisfies future queries under another alias (e.g., "49ers", "San Francisco") automatically.

PII rule: teach the structural question with identifiers stripped - never include names, emails, phone numbers, account ids, or other personal identifiers in taught queries or notes. The CLI scans teach queries for obvious email/phone shapes and warns, but does not block; strip before teaching rather than relying on the warning.

### Step 5: playbooks - optional flags, automatic synthesis

You do not need to decide whether a session "deserves" a playbook: a teach on a family without one auto-synthesizes a `playbook_candidate` from the session's journal, and the next session judges it via confirm/reject. Attach explicit playbook flags only when you already hold choreography worth recording verbatim - workarounds the CLI didn't surface (silently-dropped flags, undocumented params, pagination tricks, payload gotchas). Prefer the **integrated one-call form** - record the resource learning and the playbook in the same `teach` invocation:

```bash
# Common case: record both the resource learning AND the playbook in one call.
beehiiv-pp-cli teach \
  --query "<user's question>" \
  --resource <id> \
  --playbook-file ~/playbooks/<shape>.json \
  --playbook-notes-file ~/playbooks/<shape>-notes.md
# (append shell `&` to background it)

# Alternate: playbook-only (no resource to record alongside).
beehiiv-pp-cli teach-playbook \
  --query "<user's question>" \
  --playbook-file ~/playbooks/<shape>.json \
  --notes-file ~/playbooks/<shape>-notes.md
```

Playbook files are JSON with `steps`, `entity_slots`, `expected_tool_calls`. Notes files are markdown carrying the gotchas verbatim. File-free callers (MCP-only agents) pass the same content inline: `--playbook-json` and `--playbook-notes` on the integrated `teach` form, `--playbook-json` and `--notes` on `teach-playbook`. On the integrated `teach` form, the playbook flags are optional - omit them entirely for a resource-only teach. On the standalone `teach-playbook` form, at least one of the playbook and notes flags must be set; both empty is rejected. Playbooks are keyed on the structural query family (entities stripped) so a recipe taught from one entity-shaped query applies to every other query of the same shape, with `slots_resolved` binding the live query's canonical at recall time.

When you DO find a playbook on a future recall, treat it as ground truth: replay the steps with `slots_resolved` substitutions, skip the discovery that the choreography already documents, and read `notes` before any step.

### Step 6: `playbook amend &` when your debug response identifies a correction

If your debug-protocol response identifies a concrete correction the notes or playbook should know — a workaround, an undocumented endpoint shape, a stale field name, observed schema drift, an empty-payload fallback — fire `playbook amend` BEFORE emitting your user-facing response. Same fire-and-forget posture as `teach`.

```bash
beehiiv-pp-cli playbook amend \
  --query "<exact recall query string>" \
  --add-note "<your concrete correction>"
# (append shell `&` to background it)
```

What counts as worth amending: a behavior you OBSERVED this session that future-you would benefit from knowing. Examples worth amending:

- A workaround for a CLI surface that silently drops or misorders a flag.
- An undocumented endpoint shape (response wrapped in `{meta, results}`, payload nested two levels deeper than the docs claim).
- Observed schema drift (a field renamed, an index that shifted between seasons, a category label that the API now returns lower-cased).

What does NOT belong in notes:

- The year-specific or entity-specific answer to the user's question. That's the response, not a learning.
- Per-team / per-athlete / per-row data the playbook already retrieves at runtime.
- Statements that paraphrase what the existing notes already say.

The amend command appends to the family's existing notes with a timestamped marker (`[amend YYYY-MM-DDTHH:MMZ]: <text>`). Multiple amends accumulate; the audit trail is visible. If no playbook exists yet for the family, amend creates a notes-only one (so cold-start corrections still land).

#### PII discipline for amend notes

`playbook amend` notes are designed to potentially flow upstream as shared knowledge in future versions of the Printing Press. Keep them clean of user-identifying content so the upstream-contribution path stays open without retroactive scrubbing:

- **Do NOT embed** paths to user filesystems, personal API keys or tokens, user email addresses, user GitHub handles, or specific query histories tied to a single user.
- **Acceptable**: endpoint shapes, undocumented field names, API gotchas, observed schema drift, workarounds for CLI surfaces, generalizable pagination or retry tactics.

If a correction is only meaningful with user-specific context, it belongs in a personal note, not in the playbook amend.

### Measuring the loop

`beehiiv-pp-cli learnings stats` reports recall hit rate, teach-to-reuse, playbook resolution rate, and candidate confirm/reject counts from the local `learn_events` table. Rates are null until they have a denominator; everything stays on this machine. Use it to check whether the loop is earning its keep for this CLI.

### Disabling learning

- `--no-learn` on a single command short-circuits both `recall` and the `teach` write path. Use for deterministic agent flows or tests that must not be affected by accumulated learnings.
- `BEEHIIV_NO_LEARN=true` in the environment globally disables the pipeline.

## Agent Feedback

When you (or the agent) notice something off about this CLI, record it:

```
beehiiv-pp-cli feedback "the --since flag is inclusive but docs say exclusive"
beehiiv-pp-cli feedback --stdin < notes.txt
beehiiv-pp-cli feedback list --json --limit 10
```

Entries are stored locally as `feedback.jsonl` under the resolved data dir. They are never POSTed unless `BEEHIIV_FEEDBACK_ENDPOINT` is set AND either `--send` is passed or `BEEHIIV_FEEDBACK_AUTO_SEND=true`. Default behavior is local-only.

Write what *surprised* you, not a bug report. Short, specific, one line: that is the part that compounds.

## Output Delivery

Every command accepts `--deliver <sink>`. The output goes to the named sink in addition to (or instead of) stdout, so agents can route command results without hand-piping. Three sinks are supported:

| Sink | Effect |
|------|--------|
| `stdout` | Default; write to stdout only |
| `file:<path>` | Atomically write output to `<path>` (tmp + rename) |
| `webhook:<url>` | POST the output body to the URL (`application/json` or `application/x-ndjson` when `--compact`) |

Unknown schemes are refused with a structured error naming the supported set. Webhook failures return non-zero and log the URL + HTTP status on stderr.

## Named Profiles

A profile is a saved set of flag values, reused across invocations. Use it when a scheduled or recurring agent reuses the same saved flags while providing different input each run.

```
beehiiv-pp-cli profile save briefing --json
beehiiv-pp-cli --profile briefing advertisement-opportunities mock-value
beehiiv-pp-cli profile list --json
beehiiv-pp-cli profile show briefing
beehiiv-pp-cli profile delete briefing --yes
```

Explicit flags always win over profile values; profile values win over defaults. `agent-context` lists all available profiles under `available_profiles` so introspecting agents discover them at runtime.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Usage error (wrong arguments) |
| 3 | Resource not found |
| 4 | Authentication required |
| 5 | API error (upstream issue) |
| 7 | Rate limited (wait and retry) |
| 10 | Config error |

## Argument Parsing

Parse `$ARGUMENTS`:

1. **Empty, `help`, or `--help`** → show `beehiiv-pp-cli --help` output
2. **Starts with `install`** → ends with `mcp` → MCP installation; otherwise → see Prerequisites above
3. **Anything else** → Direct Use (execute as CLI command with `--agent`)

## MCP Server Installation

Install the MCP binary from this CLI's published public-library entry or pre-built release, then register it:

```bash
claude mcp add beehiiv-pp-mcp -- beehiiv-pp-mcp
```

Verify: `claude mcp list`

## Direct Use

1. Check if installed: `which beehiiv-pp-cli`
   If not found, offer to install (see Prerequisites at the top of this skill).
2. Match the user query to the best command from the Unique Capabilities and Command Reference above.
3. Execute with the `--agent` flag:
   ```bash
   beehiiv-pp-cli <command> [subcommand] [args] --agent
   ```
4. If ambiguous, drill into subcommand help: `beehiiv-pp-cli <command> --help`.
