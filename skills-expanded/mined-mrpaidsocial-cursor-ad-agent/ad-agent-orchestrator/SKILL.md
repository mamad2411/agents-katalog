---
name: ad-agent-orchestrator
description: >-
  Orchestrates human-approved, end-to-end Meta ad campaigns from competitor
  research through test concepts, Arcads image/video generation or cloning,
  human ad copy, PAUSED deployment, explicit activation, and threshold-based
  performance review. Applies when a user asks to build, launch, test, or
  iterate a complete Facebook or Instagram ad campaign rather than one isolated
  research, creative, copy, deployment, or reporting phase.
---

# Ad agent orchestrator

This is the canonical top-level workflow. It owns sequencing, approval gates,
lineage, and recovery; component skills own their phase implementations.

Read [run-contract.md](run-contract.md) before opening a run and
[test-plan.md](test-plan.md) before proposing concepts or thresholds.

## Non-negotiable rules

1. A human approves every gate for its exact hashed scope. Approval at one gate
   never implies approval at another. Any scoped change invalidates approval.
2. Never create spend-capable Meta entities as ACTIVE. Deploy ads PAUSED.
   Activation is separate, optional, and requires the exact confirmation
   `ACTIVATE` after reviewing the account, hierarchy, and budgets.
3. Never run unattended generation, deployment, activation, or delivery
   mutation. Performance polling is read-only and finite or separately
   scheduled by the human.
4. Regeneration requires approval except for bounded still-image QA-fix
   retries. After G4, component skills may auto-retry visible image defects
   with a revised prompt — up to **2** retries per originally requested still
   (**3** attempts total). Disclose possible retry credit exposure at G4 before
   the first call; each retry is billed. Failed calls, G5 rejection,
   creative-direction changes, video assets, exhausted QA caps, strategic
   "try again" requests, and recommendation-driven work need a revised plan,
   incremental estimate, and fresh applicable gates — never unbounded
   auto-retry.
5. Never invent a claim, receipt, Arcads price, Meta metric, threshold, result,
   or causal explanation. Unverified copy uses explicit placeholders and cannot
   be deployed until resolved and approved.
6. Meta Ad Library longevity is an adaptation-readiness proxy only. It is not
   evidence of spend, conversions, ROAS, profitability, or creative performance.
7. Keep credentials in environment files. Never put secrets, token-bearing
   URLs, or authorization headers in prompts, artifacts, commands, or lineage.
8. Lineage is append-only. Never edit prior JSONL records or hand-edit a
   compiled manifest.

## Component routing

Read and follow the selected component skill at its phase:

| Need | Component |
|---|---|
| Competitor evidence and local clone inputs | [`competitor-ad-research`](../competitor-ad-research/SKILL.md) |
| Typography-heavy or UI-mimicry still | [`chatgpt-image-ad`](../chatgpt-image-ad/SKILL.md) |
| Photoreal, lifestyle, or multi-reference still | [`nano-banana-image-ad`](../nano-banana-image-ad/SKILL.md) |
| Reverse-engineer a selected image ad | [`image-ad-clone`](../image-ad-clone/SKILL.md) |
| Fresh Arcads video or other Arcads asset | [`arcads-external-api`](../arcads-external-api/SKILL.md) |
| Reverse-engineer a selected video ad | [`clone-ad`](../arcads-external-api/prompting/clone-ad/SKILL.md) |
| Primary text, headlines, descriptions, claim ledger | [`human-ad-copy`](../human-ad-copy/SKILL.md) |
| Meta destination, dry run, PAUSED deploy, activation | [`meta-ad-builder`](../../shared/skills/meta-ad-builder/SKILL.md) |
| Read-only measured performance | [`meta-performance-loop`](../meta-performance-loop/SKILL.md) |

Do not invoke a clone component until gate G1 identifies the exact local source.
Do not invoke more than one generator merely to explore options; model, count,
prompt, and cost scope must be approved first.

## State machine and gates

Only move forward through the following states. A rejected gate leaves the run
in its current state. `not_applicable` is allowed only with a recorded reason.

| State | Work and required exit |
|---|---|
| S0 `SCOPED` | Confirm product, offer, objective, audience, destination, account context, constraints, and success question. Initialize lineage, creating `run.created`. |
| S1 `RESEARCHED` | Run research or document a user-brief/no-competitor path. **G1 RESEARCH_SELECTION:** human selects exact source IDs/local files or explicitly approves no source. Then append `research.completed`. |
| S2 `PLANNED` | Build the concept/test matrix. **G2 TEST_MATRIX:** human approves hypothesis, cells, variable under test, constants, routes, and counts. Append one `concept.created` per approved cell. |
| S3 `GENERATION_READY` | Prepare prompts and settings. **G3 DIALOGUE:** separately approve exact numbered dialogue and timing for every speaking video; otherwise record why N/A. **G4 ARCADS_CREDITS:** separately approve an estimate-only per-model/config/count breakdown and variable factors. |
| S4 `ASSETS_READY` | Execute only the approved Arcads calls, log them per the component skill, QA outputs, and append `asset.generated` per completed output. **G5 ASSET_SELECTION:** human selects exact local assets. Rejection stops; it never triggers regeneration. |
| S5 `COPY_READY` | Use `human-ad-copy`, its claim ledger, and validator. Resolve all placeholders and `HARD` findings. **G6 COPY_APPROVAL:** human approves the exact copy file. Append `copy.approved`. |
| S6 `META_PLAN_READY` | Confirm account, campaign/ad set, Page/Instagram identity, pixel, destination, CTA, creative, copy, and special-category handling. **G7 META_DRY_RUN:** human authorizes the exact offline dry-run command. |
| S7 `DRY_RUN_REVIEWED` | Run `meta-ad-builder --dry-run` and inspect its complete `deployment_results.json`. **G8 PAUSED_DEPLOY:** human approves that exact payload for a real PAUSED deploy. |
| S8 `DEPLOYED_PAUSED` | Run the same reviewed command without `--dry-run`; it must include `--run-id`. The builder appends `ad.deployed`. This is the default safe terminal state. |
| S9 `ACTIVATED` | Optional. Preview status changes first. **G9 ACTIVATE:** human confirms exact entity IDs, full hierarchy state, budgets, schedule, and `ACTIVATE`. Execute the approved status commands, then append `ad.activated` only after success. |
| S10 `MEASURED` | **G10 PERFORMANCE_THRESHOLDS:** human supplies the exact conversion action type, windows, minimum spend, winner/loser ROAS, winner purchase count, and any CPA/frequency/CTR rules. Poll read-only; the poller appends `performance.snapshot`. |
| S11 `REVIEWED` | Cite measured snapshot fields in every recommendation. Append `recommendation.created`. Never pause, scale, activate, or regenerate from a recommendation. The human may approve a new matrix or close the run with `run.completed`. |

G3 and G4 are separate even when shown in one conversation turn. G8 never
authorizes G9. G9 does not authorize performance thresholds. A run may be
completed at S8 with ads PAUSED and zero delivery spend.

## Research and selection

Use the competitor skill's objective ranking and full-copy preservation. Show
the ranked brief and exact local creative paths. The human may choose:

- one or more exact local sources to adapt;
- a user-provided source;
- a from-scratch concept with no competitor source; or
- to stop the run.

Record the choice and disclaimer in `research.completed`. Never auto-select the
highest longevity score, infer motifs without visual inspection, or hand a
remote URL to a clone skill.

## Concept and test matrix

Follow [test-plan.md](test-plan.md). When the goal is learning, each comparison
changes exactly one declared variable while audience, budget, optimization,
placement, destination, offer, and every non-tested creative/copy element remain
constant. If multiple variables change, mark the work `explore`, not an A/B test,
and make no causal claim.

Meta `TEXT_LIQUIDITY` is a composite copy pool. For a creative test, keep the
entire approved pool identical. For a copy-pool test, treat the whole pool as
the one variable; do not attribute results to an individual line.

## Arcads generation gates

For a speaking video, present dialogue as a numbered beat list with silent beats,
word count, target duration, and fit assessment. Wait for explicit dialogue
approval before presenting the credit gate.

For every Arcads call, show:

- model, mode, duration/resolution/aspect ratio, references, audio, and count;
- estimate per call and total, with the source of each number;
- variable factors and the statement that this is an estimate;
- for still-image routes, possible QA-fix retry exposure (up to 2 additional
  billed attempts per requested image if defects appear);
- a reminder to confirm exact pricing in the Arcads platform if precision
  matters.

If logs and `MASTER_CONTEXT.md` do not provide a price, ask the human. Do not
guess. Generation starts only after G3 when applicable and G4. Prompt, settings,
references, dialogue, or count changes invalidate the relevant gates.

After generation, visually inspect the asset per the component skill. Log each
completed output — including bounded QA-fix retries — even when the human later
rejects it, but deploy only G5-selected local paths. User-directed or
strategic retries, failed calls, and post-cap defects are a new generation plan
with a new incremental estimate and approvals.

## Copy gate

Build a claim ledger from product facts and receipts. Draft copy that matches
the selected creative, then run:

```bash
python3 skills/human-ad-copy/scripts/validate_copy.py "$COPY_FILE"
```

Fix every `HARD` finding. Human review must verify truth, voice, destination,
pairwise compatibility of liquidity fields, and any compliance constraints.
Only then record G6 and append `copy.approved`.

## Meta safety gates

Use canonical scripts under `shared/skills/meta-ad-builder/scripts/`. Run one
concept cell per deployment command so `--concept-id`, `--source-id`,
`--arcads-asset-id`, and `--hypothesis` remain accurate.

The dry run makes no Meta calls and appends no lineage. Hash its inputs and
result for G8. A live deploy must use the same scoped values, omit only
`--dry-run`, include `--run-id "$RUN_ID"`, and create PAUSED ads. If anything
else changes, return to G7.

Activation is never part of deployment. Preview each status command without
`--execute`; after G9, execute with `--execute --confirm ACTIVATE`,
`--run-id "$RUN_ID"`, and the latest approved `--gate-receipt-id`. The status
tool verifies G9 and its scope before Meta is called. Confirm the campaign and
ad set are intentionally ACTIVE too; an ACTIVE ad alone may not deliver.
Conversely, activating the hierarchy can expose other ads to spend. If Meta
succeeds but activation lineage fails, reconcile before retrying; never resend
or roll back automatically.

## Performance gate and loop

Never supply default economics. At G10 the human must set the exact Meta
`action_type`, primary window, optional comparison window, and thresholds. The
performance component is read-only and classifies only from the primary window.

Every recommendation must cite snapshot ID, ad ID, window, metric value,
operator, and approved threshold. Aggregate results rank ads but do not prove
which creative element caused them. A recommendation is a proposal only; it
cannot trigger regeneration or a Meta mutation.

## Exact lineage CLI

From the repository root, use the canonical helper and event payload files
defined in [run-contract.md](run-contract.md):

```bash
python3 scripts/lib/ad_agent_lineage.py init \
  --run-id "$RUN_ID" --product "$PRODUCT" --objective "$OBJECTIVE"

python3 scripts/lib/ad_agent_lineage.py event \
  --run-id "$RUN_ID" --type research.completed \
  --data-file "$EVENT_DIR/research.completed.json"

python3 scripts/lib/ad_agent_lineage.py event \
  --run-id "$RUN_ID" --type concept.created \
  --data-file "$EVENT_DIR/concept.created.json"

python3 scripts/lib/ad_agent_lineage.py event \
  --run-id "$RUN_ID" --type asset.generated \
  --data-file "$EVENT_DIR/asset.generated.json"

python3 scripts/lib/ad_agent_lineage.py event \
  --run-id "$RUN_ID" --type copy.approved \
  --data-file "$EVENT_DIR/copy.approved.json"

python3 scripts/lib/ad_agent_lineage.py event \
  --run-id "$RUN_ID" --type recommendation.created \
  --data-file "$EVENT_DIR/recommendation.created.json"

python3 scripts/lib/ad_agent_lineage.py event \
  --run-id "$RUN_ID" --type run.completed \
  --data-file "$EVENT_DIR/run.completed.json"
```

`init` appends `run.created`. Live `meta-ad-builder` deploys with `--run-id`
append `ad.deployed`; do not duplicate it manually. Successful
`meta-performance-loop` polls append `performance.snapshot`; do not duplicate
those. After either component, refresh the compiled manifest because both append
through the Python module rather than the lineage CLI:

```bash
python3 scripts/lib/ad_agent_lineage.py manifest --run-id "$RUN_ID"
```

After a successful activation, append its non-secret receipt explicitly:

```bash
python3 scripts/lib/ad_agent_lineage.py event \
  --run-id "$RUN_ID" --type ad.activated \
  --data-file "$EVENT_DIR/ad.activated.json"
```

## Resume and recovery

At every resume, compile from the ledger first:

```bash
python3 scripts/lib/ad_agent_lineage.py manifest --run-id "$RUN_ID"
python3 scripts/lib/ad_agent_lineage.py show --run-id "$RUN_ID"
```

Read `outputs/ad-agent/runs/$RUN_ID.json`, verify artifact existence and gate
scope hashes, then derive the next state from the table above. Never infer a
missing approval from a later event.

Do not repeat a side effect merely because the prior process lost its terminal.
Reconcile Arcads logs/asset IDs, Meta `deployment_results.json`/`ad.deployed`
events, and performance `snapshot_id`s first. If the outcome remains uncertain,
stop and ask the human; never blindly regenerate or redeploy.

Append-only correction uses a new event with a revision/supersedes reference.
Do not delete history. Complete a run only when the human chooses an outcome
(`deployed_paused`, `activated_and_measured`, `cancelled`, or `failed`) and all
known side effects are reconciled.

## Offline verification

These checks make no external calls:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s skills/ad-agent-orchestrator/tests -p "test_*.py" -v
```
