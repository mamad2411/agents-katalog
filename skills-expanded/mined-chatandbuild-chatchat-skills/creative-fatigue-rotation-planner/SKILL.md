---
id: creative-fatigue-rotation-planner
name: creative-fatigue-rotation-planner
description: "Read-only TikTok creative fatigue detector + rotation plan — compares each running ad's recent click-rate (and, for conversion ads, conversion-rate) against its own 30-day baseline to catch decaying creatives, then returns a ranked Retire / Scale / Watch plan with the size of the drop, the spend at risk, and an optional shortlist of fresh library assets to swap in. Triggers: creative fatigue, are my ads fatiguing, which creatives to refresh, ad fatigue, creatives getting tired, CTR dropping, rotate my creatives, which ads to retire, refresh ads, declining ad performance, creative rotation plan, spend at risk on old creatives. ❌ Do NOT use this skill for: actually swapping, uploading, pausing, or appealing a creative (use manage-creative); a full multi-dimensional performance report (use get-performance-report); whole-campaign delivery diagnosis like rejections / budget / bids (use diagnose-campaign-health); cross-campaign budget reallocation (use optimize-budget). This skill never writes — it plans and routes."
category: TikTok
version: 1.1.0
---

# Creative Fatigue & Rotation Planner (read-only)

A **read-only** skill. It reads ad-level performance over two time windows, measures how far each
creative has decayed from its own baseline, and prints a ranked rotation plan. **It never swaps,
uploads, pauses, or appeals anything** — the actual rotation is handed to `manage-creative`.

**Tool chain (verified against the live MCP):**
```
Stage 0: resolve advertiser (paste advertiser_id/bc_id, or auth_advertiser_get / bc_get) → advertiser_info_get
Stage 1: confirm windows (recent 3d vs baseline 30d) + ask if a library scan is wanted
Stage 2 (read-only):
  ① report_integrated_get (ad level, recent 3 days: ctr / conversion_rate / spend / impressions)   → sync
  ② report_task_create → report_task_check → report_task_download (ad level, last 30 days)          → async
  ③ smart_plus_ad_get / ad_get                                                                       → ad ↔ creative names
  ④ (optional) file_video_ad_search / file_image_ad_search                                          → fresh candidates
Stage 3: compute decay per creative → classify Retire / Scale / Watch → spend at risk
Stage 4: render the rotation plan (+ optional swap-in shortlist) → route the swap out
```

---

## 🔒 Read-only scope (one-strike rule)

This skill must **NEVER** call any write tool — no `ad_update`, `smart_plus_ad_update`,
`*_status_update`, `*_material_status_update`, `file_*_upload`, `adgroup_appeal`, `*_create`
(except `report_task_create`, a read-only report task), or `*_delete`. Only the read tools in the
dispatcher table below plus `tool_execute` / `tool_get`. If asked to *plan AND swap*, produce the
plan, then **refuse the swap** and route to `manage-creative`. A silent write = catastrophic failure.

---

## What this skill is NOT for (route elsewhere)

| Out-of-scope intent | Route to |
|---|---|
| Actually swap / upload / pause / appeal a creative | `manage-creative` |
| A full multi-dimensional performance report | `get-performance-report` |
| Whole-campaign delivery diagnosis (rejected / budget / bid / no-impressions) | `diagnose-campaign-health` |
| Move budget across campaigns and execute it | `optimize-budget` |

> It sounds like what you really want is [to execute a swap / a full report / a delivery diagnosis]
> — there's a dedicated skill for that. Want me to switch to `<skill>`?

---

## MCP backend (dispatcher)

Runs through the TikTok Ads MCP. **layer** (`tt-ads-mcp-layer`: ~40 tools + `tool_execute`/`tool_get`
dispatcher) or **flat** (`tt-ads-mcp-flat`: all ~400 callable directly). Mapping below names each
real tool; under flat, call it directly.

| Mechanism | When | Call shape |
|---|---|---|
| **L0 direct tool** | on the layer L0 allowlist (or flat) | call by name directly |
| **`tool_execute` dispatch** | other grouped tools on layer | `tool_execute(tool_name="<tool>", params={...})`; unsure → `tool_get(["<tool>"])` first |

Complete tool mapping (**single source of truth**). All READ-ONLY:

| Purpose | Real tool | Mechanism (layer) |
|---|---|---|
| Stage 0 authorized ad accounts | `auth_advertiser_get` | **L0 direct** |
| Stage 0 Business Centers | `bc_get` | `tool_execute` |
| Stage 0 advertiser details (currency/timezone) | `advertiser_info_get` | **L0 direct** |
| Stage 2 ① recent ad report (sync) | `report_integrated_get` | **L0 direct** |
| Stage 2 ② baseline ad report (async) | `report_task_create` / `report_task_check` / `report_task_download` | `tool_execute` |
| Stage 2 ③ Smart+ ad list | `smart_plus_ad_get` | **L0 direct** |
| Stage 2 ③ legacy ad list | `ad_get` | `tool_execute` |
| Stage 2 ④ library videos (optional) | `file_video_ad_search` | `tool_execute` |
| Stage 2 ④ library images (optional) | `file_image_ad_search` | `tool_execute` |
| (optional, allowlist-only) dedicated fatigue signal | `creative_fatigue_get` | `tool_execute` |

> Metric values come back as **strings** — parse to numbers. The conversion metric is **`conversion`**
> (singular); conversion rate is **`conversion_rate`**. There is a dedicated `creative_fatigue_get`
> tool, but it is **allowlist-only** — if it errors (not allowlisted), fall back to the report-metric
> method below, which is the primary path. The optional library scan (④) is **off the critical path**:
> if it errors or is empty, say "No unused library assets found" and continue — never block.
> ⚠️ Paywalled (`n/a`) metrics → show `n/a`, never guess.

---

## Error codes

| Code | Trigger | What this skill does |
|---|---|---|
| `E101_NO_ACCOUNT` | Can't list or resolve any advertiser and no id given | Ask the user to paste an `advertiser_id`/`bc_id`; note `auth_advertiser_get`/`bc_get` were empty |
| `E102_NO_PERMISSION` | API returns `40001 No permission to operate advertiser` | Tell the user this token isn't authorized on that advertiser; ask them to authorize it or give another id |
| `E103_NO_ADS` | No ad clears the data floor | Honestly report "not enough creative data to assess fatigue yet," stop — don't fabricate |
| `E104_ASYNC_FAILED` | The baseline async report came back `FAILED` | Surface the raw error, suggest narrowing the range, ask to retry |
| `E105_API_4XX` | 4xx (e.g. `40002` invalid field) | Surface raw `code` + `message`; fix the param or skip that slice |
| `E106_API_5XX` | 5xx | Surface the error, ask whether to retry (max 1) |

> Honest layering: `E101 / E103` are skill states; `E102 / E104 / E105 / E106` wrap real platform
> errors (`40001`, FAILED, `40002`, 5xx) and MUST surface the raw `code` + `message`.

---

# ═══════════════════════════════════════════
# STAGE 0 — Resolve the advertiser
# ═══════════════════════════════════════════

**Fast path (preferred):** if the user gives an `advertiser_id` (or `bc_id`), use it directly — some
tokens can't enumerate accounts:
```
Paste the advertiser ID whose creatives I should check (a long numeric string).
```
**Else try to list:** `auth_advertiser_get`; if empty, `bc_get`; if both empty and no id →
**E101_NO_ACCOUNT**, ask for an id. **Confirm:** `advertiser_info_get([advertiser_id])` →
keep `currency`, `timezone`; `40001` → **E102_NO_PERMISSION**.

---

# ═══════════════════════════════════════════
# STAGE 1 — Confirm windows + options
# ═══════════════════════════════════════════

```
Creative fatigue settings:
  Recent window:   last 3 days (default)
  Baseline window: the 30 days BEFORE the recent window (default; NON-overlapping)
  Library scan:    suggest fresh videos/images to swap in?  (yes / no, default yes)
Default: 3-day recent vs prior-30-day baseline, library scan on. Tell me if you want to change it.
```
Store `recent_days` (3), `baseline_days` (30), `library_scan`. **Date sanity:** baseline `end_date`
≤ today; reject future dates before any call.

---

# ═══════════════════════════════════════════
# STAGE 2 — Pull data (read-only)
# ═══════════════════════════════════════════

```
Checking your creatives for fatigue, this usually takes 20–40 seconds...
```

**① Recent report (sync)** — `report_integrated_get` (L0): `advertiser_id`, `report_type = BASIC`,
`data_level = AUCTION_AD`, `dimensions = ["ad_id"]`,
`metrics = ["spend","impressions","clicks","ctr","conversion","conversion_rate","cpm","video_play_actions","ad_name","campaign_name"]`,
recent date range. Parse string metrics to numbers. `cpm` + `video_play_actions` are **required** — many
accounts are video-views/reach ads whose only valid engagement metric is cost-per-view or CPM (verified
live: most ads on `7415418166391832593`, `7595534274158903297`, `7631551715865657362` are video-views).

**② Baseline report (async)** — ad level over the **prior non-overlapping baseline window** (default
the 30 days ending the day before the recent window), **same `metrics` as ①** → `report_task_create` → poll
`report_task_check` → on success `report_task_download`. On `FAILED` → **E104**.

**③ Ad ↔ creative names** — `smart_plus_ad_get` (L0) and/or `ad_get` (`tool_execute`) to map `ad_id`
→ ad/creative name + material id.

**④ (optional) Library scan** — only if `library_scan = yes`: `file_video_ad_search` /
`file_image_ad_search`. If it errors or is empty → "No unused library assets found," continue.

If no ad clears the data floor (Stage 3) → **E103_NO_ADS**, stop honestly.

---

# ═══════════════════════════════════════════
# STAGE 3 — Measure decay + classify (two complementary signals)
# ═══════════════════════════════════════════

> 📎 Exact thresholds, formulas, exclusions, and the creative-churn fallback live in
> [fatigue-criteria.md](references/fatigue-criteria.md). Summary contract below.

**0. Data floor + engagement metric by objective:** an ad needs volume to judge (Signal A:
`baseline impressions ≥ 1000`; Signal B: `recent impressions ≥ 1000`). Below both → "thin data," skipped.
Pick each ad's **engagement metric by objective**: conversion ad (conversion objective or records
conversions) → **CVR / CPA**; `TRAFFIC` / `BRAND_CONSIDERATION` / `ENGAGEMENT` → **CTR**; `VIDEO_VIEWS` →
**cost-per-view** (`spend / video_play_actions`) or view-rate; `REACH` → **CPM**. **Never judge a
VIDEO_VIEWS / REACH ad on CTR** (they have ~0 clicks by design — verified live: NUXE / vivo / CP video ads),
and never a CVR an awareness ad lacks. **One advertiser often mixes objectives** (traffic + video-views +
live-conversion ads together — verified live: `7119328366494220289`, `7591834723639656465`), so pick the
metric **per ad**, not per account — but **anchor on the campaign** (group by `campaign_name`, already in
the pull): all ads in one campaign share an objective. If you didn't fetch the campaign objective, infer it
from the metric signature: `conversion > 0` → conversion ad (CVR/CPA); `video_play_actions ≫ clicks` and
`ctr ≈ 0` → video-views/reach (cost-per-view / CPM, never CTR); `video_play_actions = 0` with real clicks →
click objective (CTR / CPC). **⚠️ A near-zero-CTR ad inside a click/consideration campaign (where *other*
ads earn real CTR) is a bottom-tier-CTR Retire candidate, NOT a "cheap view"** — only treat an ad as
video-views/reach when its **whole campaign** optimizes for views/reach. Verified live: Keyshu consideration
campaign spans CTR 0.05%→4.10% across same-objective ads (the 0.05% ad is a Retire, not a cheap view).

**1. Signal A — time-decay (preferred, precise):** for an ad present in BOTH windows —
**engagement-metric fatigue** = the ad's engagement metric (step 0) worsened ≥ 40% vs its baseline
(CTR or view-rate ↓ ≥ 40%, or cost-per-view / CPM ↑ ≥ 40%); CVR fatigue (conversion ads) =
`recent_cvr < baseline_cvr × 0.7`.

**2. Signal B — vs current peers (always available; handles creative churn):** many advertisers rotate
creatives fast (e.g. flash-sale bursts), so few ads persist across windows and Signal A finds little.
For each CURRENT ad (`recent impressions ≥ 1000`), rank it against the account's **current
same-objective ads** on its **engagement metric** (CTR / view-rate / CPM per step 0) plus `recent_cvr` /
recent CPA for conversion ads.

**3. Coverage + mode (report honestly):** count ads assessable by Signal A (cross-window history) vs
only by Signal B (fresh). If most ads are fresh → say *"this account rotates creatives quickly — showing
current winners/losers rather than time-decay."*

**4. Classify each live ad into ONE bucket (tag the WHY):**
   - **Retire** 🔴 — time-decay fatigue (A) **OR** a conversion ad with meaningful spend + clicks but
     `conversion = 0` (clicks that don't convert) **OR** bottom-third vs current same-objective peers
     (B: its engagement metric — and CVR/CPA for conversion ads — well below the median); AND `recent_spend ≥ floor`.
   - **Scale** 🟢 — top-third vs current peers (strong engagement metric; conversion ads: high CVR / low CPA), not decaying.
   - **Watch** 🟡 — mild decline, mid-pack, or thin data.

**5. Spend at risk** = `Σ recent_spend` over Retire ads. Zero Retire → "No creatives to rotate right now."
Tag each Retire with its reason: *decayed* / *underperforms current peers* / *clicks-don't-convert*.

---

# ═══════════════════════════════════════════
# STAGE 4 — Render the rotation plan
# ═══════════════════════════════════════════

```
🎬 Creative Fatigue & Rotation Plan — {advertiser_name} ({advertiser_id})  ·  {currency}
Recent {recent_days}d vs baseline {baseline_days}d  ·  Ads analyzed: {N}  ·  Skipped (thin data <1000 impr): {M}
Mode: {time-decay ({A} ads have cross-window history)  /  current winners-losers (this account rotates creatives fast)}

★ Spend at risk (recent {recent_days}d on Retire creatives): {spend_at_risk}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 🔴 Retire — fatiguing, rotate out soon
  #  Ad / creative   Why (decayed / underperforms peers / no-conversions)   Recent CTR/CVR   vs baseline-or-peer   {recent}d spend  → manage-creative
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 🟢 Scale — still winning, put more behind these → optimize-budget
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 🟡 Watch — early decline / keep an eye on
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ♻️ Fresh candidates to rotate in (optional, from your library)
  {if off/empty → "No unused library assets found."}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Assumptions & limits
  · Fatigue = recent CTR < 60% of the 30-day baseline; for conversion ads also recent CVR < 70% of baseline.
    Awareness ads (no conversions) are judged on CTR only.
  · Excluded: ads with < 1000 baseline impressions ({M} skipped). "Spend at risk" is recent-window
    spend on Retire ads, not a guaranteed loss. Candidate list is suggestion-only and may be empty.
    Paywalled metrics show n/a.

🔍 Next steps (this skill changes nothing itself):
  · Swap / retire / upload creatives → manage-creative   · Budget behind winners → optimize-budget
  · Full creative numbers → get-performance-report        · Delivery issues → diagnose-campaign-health
```
Sort Retire by `recent_spend` desc (★ on the biggest). If every bucket is empty, say so and still
show analyzed/skipped counts + limits.

---

## Worked examples
- Happy path (clear fatigue, real spend-at-risk): [examples/01-happy-path.md](references/examples/01-happy-path.md)
- "Plan and swap" redline (must route the swap out): [examples/02-scope-redline-swap-attempt.md](references/examples/02-scope-redline-swap-attempt.md)
- Thin data (no fabrication): [examples/03-insufficient-data.md](references/examples/03-insufficient-data.md)

## Additional resources
- Fatigue thresholds, formulas, exclusions: [fatigue-criteria.md](references/fatigue-criteria.md)
- Report parameters / real metric names / sync-vs-async: [params-quickref.md](references/params-quickref.md)
- Test suite (eval contract + cases): [evals/README.md](evals/README.md), [evals/cases.jsonl](evals/cases.jsonl)
