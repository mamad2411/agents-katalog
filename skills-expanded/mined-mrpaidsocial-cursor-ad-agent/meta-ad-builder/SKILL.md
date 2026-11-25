---
name: meta-ad-builder
description: >-
  Research, prepare, and deploy finished creatives to Meta (Facebook/Instagram)
  through the Marketing API. Lists destinations, optionally creates PAUSED
  campaign structure, uploads images or videos, creates multi-copy
  TEXT_LIQUIDITY ads in PAUSED state, records lineage, and hands deployed IDs to
  the read-only performance loop. Use for Meta destination selection, campaign
  or ad-set setup, ad deployment, activation with an explicit safety gate,
  account winner research, or competitor Ad Library research.
---

# Meta ad builder

Turn a finished creative into a Meta ad through this controlled sequence:

**research → copy → destination selection → structure (optional) → dry run →
PAUSED deploy → separate explicit activation → performance-loop handoff**

No creation command in this skill has an ACTIVE option. Deployment creates
PAUSED ads. Activation is a separate command with a stronger confirmation gate.

## When to use this skill

Trigger on phrases like:
- "deploy this video to Meta" / "publish this as a Facebook ad"
- "build/launch a Meta ad" / "push this creative into <ad set>"
- "create a Meta ad with this image and copy"
- "create a paused campaign/ad set" / "show my Meta destinations"
- "activate/pause/archive this Meta ad, ad set, or campaign"
- "pull my top-performing ads" / "what are my best ads by ROAS"
- "research competitor ads" / "pull <brand>'s ads from the Ad Library"

Do **not** use this skill to *generate* creative — that's `pixar-style-ad`,
`claymation-ad`, `generate-youtube-thumbnail`, `uni1-image-ad`, etc. This skill
owns direct Meta Marketing API research, structure, deployment, and gated status
changes. It does not write to Airtable or another creative database.

## Read order

1. **This file** — workflow, decision tree, safety rules.
2. Invoke **`human-ad-copy`**, then read
   **[prompting/copy-guide.md](prompting/copy-guide.md)** for the `copy.json`
   handoff.
3. **[reference/deploy-patterns.md](reference/deploy-patterns.md)** — creative
   spec, upload, lineage, structure, and retry mechanics.
4. **[reference/meta-api-cheatsheet.md](reference/meta-api-cheatsheet.md)** — the
   full Meta Marketing API reference (campaigns, ad sets, ads, enums, gotchas,
   Ad Library). Consult as needed; don't read end-to-end.

## Prerequisites

- **Env** (in `.env` — see your repo's `.env.example`):
  - `META_ACCESS_TOKEN` (required) — long-lived token with `ads_management` scope
  - `META_AD_ACCOUNT_ID` (required) — with or without the `act_` prefix
  - `META_PAGE_ID`, `META_IG_USER_ID`, `META_PIXEL_ID` (optional defaults for deploy)
  - `META_API_VERSION` (optional, default `v23.0`)
- **Python deps:** `python3 -m pip install -r shared/skills/meta-ad-builder/scripts/requirements.txt`
- **A target ad set.** Select an existing one, or explicitly create PAUSED
  structure with `create-campaign-structure.py`.
- **The finished creative on disk** — an image or video file path. Chat-pasted
  files are not accessible; ask the user for a real path.

`check-meta-env.sh` makes a live read call. Run it only when credential
validation is needed, never as part of an offline dry run.

## Workflow

### Phase 1 — Research (optional, when copy should model winners)

```bash
# Rank the account's ads and pull the winning copy
python3 shared/skills/meta-ad-builder/scripts/pull-top-ads.py \
  --date-preset last_30d --min-spend 100 --limit 15

# Pull a competitor's ads from the Ad Library
python3 shared/skills/meta-ad-builder/scripts/pull-competitor-ads.py \
  --pages "BrandName" --limit 50
```

Both write JSON under `OUTPUT_BASE` (or `./outputs/meta-ads/`). Read the top-ad
`copy` fields to identify winning hook/proof/CTA patterns before writing new copy.

### Phase 2 — Copy

Invoke the **`human-ad-copy`** skill. Give it the offer, audience, creative,
voice, verified receipts, destination, and any winning-copy research. Write
`copy.json` with 5 genuinely different bodies, 5 titles, and 3 descriptions.
Save it under `outputs/`, then run the deterministic validator:

```bash
python3 skills/human-ad-copy/scripts/validate_copy.py copy.json
```

Fix every `HARD` finding. Review `REVIEW` findings in context; the validator
cannot verify truth, brand voice, or strategic fit.

### Phase 3 — Select the destination

List accessible accounts first. Add `--ad-account` to inspect that account's
ACTIVE/PAUSED campaigns and ad sets; add `--campaign-id` to narrow ad sets:

```bash
python3 shared/skills/meta-ad-builder/scripts/list-meta-destinations.py
python3 shared/skills/meta-ad-builder/scripts/list-meta-destinations.py \
  --ad-account <ACCOUNT_ID>
python3 shared/skills/meta-ad-builder/scripts/list-meta-destinations.py \
  --ad-account <ACCOUNT_ID> --campaign-id <CAMPAIGN_ID>
```

This script is read-only. Confirm the account, campaign, ad set, destination URL,
Page, Instagram identity, pixel, objective, and any Special Ad Category with the
user before a mutation.

### Phase 4 — Create structure (optional)

Use explicit inputs. The command supports:

- **CBO:** `--daily-budget` is placed on a newly created campaign and omitted
  from the ad set.
- **ABO:** campaign budget is omitted and `--daily-budget` is required on the
  ad set.
- `--daily-budget` uses account minor units (for USD, cents).
- Targeting is broad geo/age/gender only. No interests or custom audiences are
  inferred.
- `OFFSITE_CONVERSIONS` requires a pixel and adds `promoted_object`.

Dry-run first:

```bash
python3 shared/skills/meta-ad-builder/scripts/create-campaign-structure.py --dry-run \
  --campaign-name "Creative Test" --adset-name "Broad US 18-65" \
  --budget-mode CBO --daily-budget 10000 \
  --country US --age-min 18 --age-max 65 --gender all \
  --pixel-id <PIXEL_ID>
```

After payload review and explicit approval, remove `--dry-run`. New campaigns
and ad sets are always **PAUSED**. There is no ACTIVE creation option. To create
an ad set in an existing campaign, use `--campaign-id` instead of
`--campaign-name`.

### Phase 5 — Dry-run the ad deployment

This writes the complete planned payload to `deployment_results.json`, makes
zero API calls, and appends no lineage:

```bash
python3 shared/skills/meta-ad-builder/scripts/deploy-ad.py --dry-run \
  --ad-account <ACCOUNT_ID> --adset-id <ADSET_ID> \
  --copy-file copy.json --link <DESTINATION_URL> \
  --image path/to/creative.png \
  --run-id <RUN_ID> --concept-id <CONCEPT_ID> \
  --source-id <SOURCE_ID> --arcads-asset-id <ARCADS_ASSET_ID> \
  --hypothesis "What this creative is testing"
```

`--image` and `--video` are repeatable. Review the account, ad set, destination,
identity, status, copy pool, each creative payload, and the selected video
upload mode.

### Phase 6 — Deploy PAUSED

Only after explicit approval, repeat the reviewed command without `--dry-run`:

```bash
python3 shared/skills/meta-ad-builder/scripts/deploy-ad.py \
  --ad-account <ACCOUNT_ID> --adset-id <ADSET_ID> \
  --copy-file copy.json --link <DESTINATION_URL> \
  --video clip-a.mp4 --video clip-b.mp4 \
  --cta SIGN_UP --pixel-id <PIXEL_ID> --run-id <RUN_ID>
```

- Every ad is created **PAUSED**.
- Videos over 90 MiB automatically use Meta's chunked upload protocol.
- `--ad-account` overrides `META_AD_ACCOUNT_ID` for this call.
- With `--run-id`, every successfully created ad appends an `ad.deployed`
  event through `scripts/lib/ad_agent_lineage.py`. `--lineage-file` can override
  the default ledger. Without `--run-id`, deployment remains compatible but no
  lineage event can be associated.
- Results, failures, payloads, provenance, account/ad-set IDs, and lineage event
  IDs are written to `deployment_results.json` under `OUTPUT_BASE`.

### Phase 7 — Activate separately (optional)

Creation and activation are intentionally separate. The status tool previews by
default:

```bash
python3 shared/skills/meta-ad-builder/scripts/set-entity-status.py \
  --entity-type ad --entity-id <AD_ID> --status ACTIVE
```

A backward-compatible standalone ACTIVE mutation (no orchestrator `--run-id`
and no gate receipt) requires both flags, including the exact confirmation:

```bash
python3 shared/skills/meta-ad-builder/scripts/set-entity-status.py \
  --entity-type ad --entity-id <AD_ID> --status ACTIVE \
  --execute --confirm ACTIVATE
```

When deployment used `--run-id`, activation is orchestrated. Pass the same ID
and the latest approved G9 receipt so the tool can verify the receipt and its
hashed scope before calling Meta, then append `ad.activated` after success:

```bash
python3 shared/skills/meta-ad-builder/scripts/set-entity-status.py \
  --entity-type ad --entity-id <AD_ID> --status ACTIVE \
  --execute --confirm ACTIVATE \
  --run-id <RUN_ID> --gate-receipt-id <G9_RECEIPT_ID> \
  --lineage-file outputs/ad-agent/lineage.jsonl
```

- If either orchestration field is supplied for an ACTIVE execution, both
  `--run-id` and `--gate-receipt-id` are required. Missing, unknown,
  wrong-gate, non-latest, unapproved, or drifted G9 receipts fail before
  credentials or HTTP are touched.
- With neither field, the standalone activation path remains available but no
  `ad.activated` event is written.
- `--lineage-file` overrides the default `outputs/ad-agent/lineage.jsonl` and
  requires `--run-id`.
- If Meta reports success but the required lineage append fails, the command
  exits non-zero with “activation may have succeeded; reconcile before retry.”
  Do not blindly retry or attempt an automatic rollback.

PAUSED or ARCHIVED mutations require `--execute` but not the activation phrase.
Support is limited to `ad`, `adset`, and `campaign`. Confirm the full hierarchy:
an ACTIVE ad still cannot deliver if its ad set or campaign remains PAUSED.

### Phase 8 — Hand off to the performance loop

Invoke **`meta-performance-loop`** after delivery begins. It is read-only and
requires operator-set thresholds:

```bash
python3 skills/meta-performance-loop/scripts/poll_meta_performance.py \
  --deployment-results <path>/deployment_results.json \
  --min-spend 50 --winner-roas 2 --loser-roas 1 \
  --winner-min-purchases 2
```

When deployment used `--run-id`, that ID is present in results and the
performance loop can resolve the `ad.deployed` lineage association.

## Decision tree

| User intent | Phases |
|---|---|
| "Show me where I can deploy" | Phase 3 |
| "Deploy this creative" + validated copy and existing ad set | Phases 3 → 5 → 6 |
| "Create the campaign/ad set too" | Phases 3 → 4 → 5 → 6 |
| "Build a Meta ad, write the copy too" | Phases 2 → 3 → 5 → 6 |
| "Make ads modeled on my winners" | Phases 1 → 2 → 3 → 5 → 6 |
| "Activate this paused entity" | Phase 7 only, with explicit confirmation |
| "Measure the deployed ads" | Phase 8 |
| "What are my best ads / competitor research" | Phase 1 only |

## Safety rules

- **Campaigns, ad sets, and ads are created PAUSED.** Never add an ACTIVE
  creation option.
- **Activation is a separate mutation.** It requires `--execute`, and ACTIVE
  additionally requires exact `--confirm ACTIVATE`.
- **Dry-run before every real deploy.** Show the payload; get a go-ahead.
- **Dry runs make zero API calls and append no lineage.**
- **Confirm the target account, campaign/ad set, and destination URL** before
  mutating Meta. The wrong hierarchy spends against the wrong budget.
- **Deploying ads is a shared-state, money-adjacent action.** Treat the live
  structure, deployment, and status runs as actions to confirm, not assume.
- Never print, persist, or pass `META_ACCESS_TOKEN` on the command line.

## Quirks and pitfalls

- **Video processing is async.** `deploy-ad.py` polls the uploaded video until
  Meta finishes processing before creating the ad — a video deploy can take a
  few minutes. See [deploy-patterns.md](reference/deploy-patterns.md).
- **Large video upload.** Files above 90 MiB use start/transfer/finish chunking;
  smaller files use one multipart request.
- **Transient and rate-limit errors.** Requests use bounded retry/backoff. There
  is no infinite retry or poll.
- **`act_` prefix** is added automatically for env and per-call account IDs.
- **Account-specific data stays out of git.** All output routes through
  `outputs/` (gitignored): ad IDs, pulled spend/revenue, competitor data.
- **Special Ad Categories** (credit, employment, housing, social issues) change
  ad-set targeting rules — flag to the user; see cheatsheet §3.5.

## Offline verification

These tests use mocks, temporary files, and fixtures. They make no Meta calls:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s shared/skills/meta-ad-builder/tests \
  -p "test_*.py" -v
```

## Cost note

The Meta Marketing API itself is free to call. **Ad spend is real money** — but
because every ad deploys PAUSED, nothing spends until the user separately
activates the required hierarchy. There are no per-call credits to estimate.
