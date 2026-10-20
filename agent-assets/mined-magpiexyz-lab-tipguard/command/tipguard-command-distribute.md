---
description: "Generate distribution campaign config from experiment.yaml. Requires a deployed MVP."
type: code-writing
reads:
  - experiment/experiment.yaml
  - experiment/EVENTS.yaml
  - experiment/ads.yaml
stack_categories: [analytics, hosting, distribution, ui, framework]
requires_approval: true
references:
  - .claude/patterns/verify.md
  - .claude/patterns/branch.md
  - .claude/patterns/observe.md
  - .claude/patterns/messaging.md
branch_prefix: chore
modifies_specs: true
---
Generate a distribution campaign configuration from experiment.yaml and implement distribution tracking.

> If `experiment/ads.yaml` already exists from a previous run, this skill reads it and presents it for approval. Delete `experiment/ads.yaml` to regenerate from scratch.

This skill generates `experiment/ads.yaml` with targeting, ad creative, budgets, and thresholds, then adds UTM/click ID capture and a feedback widget to the deployed app. The channel is selected at runtime — each channel has a stack file at `.claude/stacks/distribution/<channel>.md` with format constraints, targeting model, policy restrictions, and config schema.

## Arguments

`/distribute` is Phase-1-only. It generates standardized Playbook settings (manual CPC, phrase match, search only, $20/day under a $250 MAX cap, 7-day nominal window set as the End date, stop at 100 clicks or the cap, 2 RSAs, 1 ad group, 50 universal negative keywords) for Google Ads.

## Lifecycle

1. Run `bash .claude/scripts/lifecycle-init.sh distribute`
2. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh distribute)`
   b. If NEXT is "FINALIZE" → skill complete
   c. If NEXT starts with "EMBED_COMPLETE:" → parse the suffix as `<skill>:<state>`, run `bash .claude/scripts/advance-state.sh <skill> <state>`, then return to step 2a
   d. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   e. Read the state file at $NEXT and execute its ACTIONS section
   f. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   g. Return to step 2a

## Do NOT

- Create a campaign via API without showing the approval preview (Step 9d) — real money is at stake. Exception: Phase 1 campaigns with standardized Playbook settings skip 9d (settings are pre-validated by the Playbook)
- Create a campaign if `campaign_id` already exists in `experiment/ads.yaml` — campaigns are idempotent
- Skip credential setup — if credentials are missing, guide the user through setup; do not fall back to manual campaign creation
- Hardcode credential file paths — read from the channel's stack file "Credential Files" subsection
- Modify experiment.yaml — this skill reads it but does not change it
- Add new packages — the feedback widget uses existing shadcn components and the analytics library
- Skip the config approval step (Step 6) — the operator must review targeting, ad creative, and budget before proceeding
- Hardcode analytics import paths or provider names — always read the analytics stack file for the correct imports
- Hardcode channel-specific constraints (char limits, click ID params, UTM values) — always read the distribution stack file for the selected channel

---

## Shared Algorithms

### 6-Adapter Reference

The distribution system supports 6 adapters across paid and organic channels:

| # | Adapter | Stack File | Config Output | Type |
|---|---------|-----------|---------------|------|
| 1 | twitter-organic | `distribution/twitter-organic.md` | `organic.yaml` | Organic |
| 2 | reddit-organic | `distribution/reddit-organic.md` | `organic.yaml` | Organic |
| 3 | email-resend | `distribution/email-campaign.md` | `campaign.yaml` | Organic |
| 4 | google-ads | `distribution/google-ads.md` | `ads.yaml` | Paid |
| 5 | meta-ads | `distribution/meta-ads.md` | `ads.yaml` | Paid |
| 6 | twitter-ads | `distribution/twitter.md` | `ads.yaml` | Paid |

> Note: `reddit.md` (Reddit Ads) exists as a stack file but is not in the 6-adapter list. It can be used as a 7th channel if needed.

### Channel Selection Logic

Channel availability depends on the experiment's plan tier and budget:

**Free / PAYG plans** — organic channels only:
- twitter-organic — post threads and value content
- reddit-organic — community-first posts in target subreddits
- email-resend — batch email to signup/waitlist audience

**Pro / Team plans** — all 6 channels:
- All organic channels above, plus:
- google-ads — search intent targeting (CPC)
- meta-ads — interest-based targeting (CPM)
- twitter-ads — audience-based targeting (CPE/CPM)

**Selection factors:**
- Experiment type: B2B → LinkedIn (manual) + Google Ads + email; B2C → Meta Ads + Reddit + Twitter
- Target audience: developer tools → Reddit + Twitter organic; consumer → Meta Ads + email
- Budget constraints: <$100 → organic only; $100-500 → 1-2 paid channels; larger budgets → multi-channel

### Budget Allocation

When running multiple channels simultaneously, allocate budget across paid channels:

**Default split (no historical data):**

| Channel | Allocation | Rationale |
|---------|-----------|-----------|
| Google Ads | 40% | Highest intent (search-based) |
| Meta Ads | 30% | Broadest reach (interest-based) |
| Twitter Ads | 15% | Engagement-focused |
| Organic channels | 15% | Time investment, not budget |

**Organic-only split (time allocation):**

| Channel | Allocation | Rationale |
|---------|-----------|-----------|
| Twitter organic | 40% | Highest potential reach per post |
| Reddit organic | 35% | Community trust, long-tail engagement |
| Email campaign | 25% | Direct to known audience |

**AI-suggested adjustments:**
- If experiment targets developers: shift 10% from Meta to Reddit organic
- If experiment is B2B SaaS: shift 10% from Twitter to Google Ads (higher intent)
- If experiment is consumer app: shift 10% from Google to Meta (broader reach)
- After first iteration: reallocate toward channels with lowest cost-per-activation

### Config Generation

Each adapter generates its corresponding config file from experiment data:

1. Read experiment.yaml for `name`, `description`, `target_user`, `thesis`, `variants`
2. Read the adapter's stack file for Config Schema section
3. Generate targeting research (Step 2) appropriate to the channel type
4. Generate ad creative / post content (Step 3) following the channel's format constraints
5. Calculate thresholds (Step 4) based on the channel's cost model
6. Write the config file (`ads.yaml`, `organic.yaml`, or `campaign.yaml`)

When running `/distribute` multiple times for different channels, each config file is versioned: `ads.yaml` (first), `ads-v2.yaml` (second paid channel), `organic.yaml` (first organic), `organic-v2.yaml` (second organic), etc.
