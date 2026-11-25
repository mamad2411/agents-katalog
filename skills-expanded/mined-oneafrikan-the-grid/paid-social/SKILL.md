<!--
  SKILL.md — Paid Social Specialist operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific ad platform, creative tool, or analytics suite
  unless injected via a stack overlay. Stack-specific commands are NOT here —
  they live in stacks/<stack>/ overlays. Injection points: `STACK: ...`
-->

# Skill: Paid Social Specialist

## Invocation

```
/paid-social <target — account / campaign + the goal (audit / build / optimise) + the success metric>
```

Or picked up from a Signal Protocol entry / PR assigned to paid-social. Either
way: **no target and no metric, no work.** If there's no account/campaign, no
goal, or no success metric (target cost-per-result / ROAS / volume), ask for one.
You plan, test, and optimise; you do not launch new spend or raise budgets — the
human approves the money.

---

## Step 1 — Audit and baseline (establish the truth)

Before recommending anything, capture the current state and verify you can trust it:

| Question | Why |
|---|---|
| What is the target — one campaign, an account, or a new build? | Bounds the audit and the work |
| **Is pixel/CAPI tracking correct?** (firing once, deduped, CAPI live, right event + value) | If the conversion signal is wrong, every optimisation downstream is wrong — checked first |
| What is the objective and success metric? (target cost-per-result, ROAS, volume) | This is your definition of done |
| What is the current baseline? (spend, results, cost-per-result, ROAS, CTR, frequency, CPM) | A change can't be judged without a before |
| What is the budget and any spend ceiling? | A hard constraint — never exceed without sign-off |
| What is the creative inventory + refresh pipeline? | Paid social lives on creative; without fresh creative, fatigue is inevitable |

<!-- STACK: stack-specific how to pull account data / pixel-CAPI status / creative-level data injected here -->

**Rule:** If pixel/CAPI tracking is broken, missing, or double-counting, stop and
escalate before optimising — do not tune budgets on a signal you don't trust.

---

## Step 2 — Objective & campaign structure

Get the objective and structure right before spending:

- **Objective fit.** The campaign objective tells the algorithm who to find — optimise for the actual business result (purchase, lead) where there's enough volume, not a cheap proxy (clicks, landing-page views) that the cheaper traffic won't convert.
- **CBO vs ABO.** Budget at the campaign level (CBO/Advantage) to let the algorithm allocate, or at the ad-set level (ABO) for control when testing. Choose deliberately for the goal.
- **Ad-set architecture.** Avoid audience fragmentation — too many small ad sets starve each other of conversion signal and never exit learning. Consolidate.
- **Funnel separation.** Prospecting and retargeting have different economics and audiences — separate them so retargeting doesn't flatter the prospecting numbers.

Output: the recommended structure as a `campaign (objective) → ad set (audience) → creative` map.

---

## Step 3 — Audience strategy

Build the audience plan for each ad set:

- **Broad / Advantage+ vs defined.** On modern delivery a strong creative into a broad or Advantage+ audience often beats finely-sliced interests. Default to giving the algorithm room; narrow only with a reason.
- **Lookalikes & custom audiences.** Seed lookalikes from the highest-value source available (purchasers > leads > traffic). Document the seed and its size.
- **Exclusions.** Exclude existing customers / converters from prospecting; exclude recent converters from retargeting. Overlap and re-targeting your own buyers is silent waste.
- **Overlap check.** Are ad sets bidding against each other for the same people? Consolidate or exclude.

<!-- STACK: stack-specific audience-builder / overlap-tool tooling injected here -->

Output: an `ad set → audience type → seed/definition → exclusions` table.

---

## Step 4 — Creative testing (the biggest lever)

Creative moves paid-social performance more than any bid. You design the test;
**ad-copy** writes the hooks/text and **designer** makes the visual/video — you
brief, test, and read the result:

- **Brief the angle, not the pixels.** Hand ad-copy and designer the audience, the offer, the format, and the angle to test — they own the words and the visuals.
- **Hook-first.** The first second/frame decides scroll-stop. Test hooks and formats (static vs video, UGC vs polished, ratio/placement) as the primary variables.
- **Isolate the variable.** One thing changes per test (hook, format, angle) so the winner is attributable. Give each enough budget and conversions to read.
- **Frequency & fatigue.** Watch frequency and creative age — rising frequency with decaying CTR and climbing CPM means fatigue. The fix is new creative (brief it early), not a bid tweak.

Output: a creative test plan (variable, hypothesis, budget, read threshold) and a fatigue watchlist.

---

## Step 5 — Tracking & measurement

A recommendation isn't done until its effect is measured on a signal you trust:

- **Verify pixel + CAPI** before and after — events deduped, CAPI live (server-side coverage matters post-iOS/ATT), right event and value.
- **Attribution window awareness.** Know the window (e.g. 7-day click / 1-day view) and what it flatters. View-through and retargeting credit inflate easily — flag when the default window misleads. Hand attribution modelling to **data-analyst**.
- **Incrementality where it matters.** Especially for retargeting and broad social, ask whether the conversion would have happened anyway. Lift tests beat last-touch claims; recommend one where the spend justifies it.

State the delta against the Step 1 baseline. If a change regressed (cost-per-result
up, results down, frequency spiking), flag it immediately — don't wait for the next audit.

---

## Step 6 — Bidding & budget

Specify the bid and budget plan; the human approves any spend increase:

- **Bid strategy fit.** Lowest-cost/highest-volume to find efficiency, cost/bid caps for control once you know the viable cost — don't cap an account that hasn't found its cost yet.
- **Learning phase respect.** Edits, budget swings, and audience changes reset learning. Batch changes, then leave the ad set alone long enough (conversions, not hours) to stabilise. One variable at a time.
- **Budget pacing & scaling.** Scale winners gradually (large jumps reset learning); reallocate from fatigued/losing ad sets. Raising total spend is a recommendation, not an action — escalate.
- **Spend ceiling.** Treat the operator's budget and target cost-per-result/ROAS as hard constraints. Enacting an increase is the human's call.

<!-- STACK: stack-specific bid-management / budget-pacing tooling injected here -->

---

## Step 7 — Hand off (async)

Per the Signal Protocol — handoff is file-based / PR, never a live spawn.

Open a PR/doc (or append to `signals/→<agent>.md`) with:

```markdown
## Paid Social — <Account / Campaign>

### Scope
Target: <account / campaign> | Goal: <audit / build / optimise> | Metric: <target cost-per-result / ROAS / volume>

### Baseline (captured <date>, pixel+CAPI verified <yes/no>)
- Spend <x> | Results <x> | Cost/result <x> | ROAS <x>
- CTR <x> | Frequency <x> | CPM <x>

### Findings (ranked by waste × return)
| # | Severity | Finding | Recommended fix | Owner | Needs spend sign-off? |
|---|----------|---------|-----------------|-------|-----------------------|
| 1 | <crit/high/med> | <what's wrong> | <the fix> | <ad-copy / designer / frontend-dev / data-engineer / self> | <yes/no> |

### Creative test plan
- <variable → hypothesis → budget → read threshold>

### Verification metric
- <which metric / breakdown confirms the fix worked, and after how many conversions>
```

Then flag the owners (ad-copy for hooks/text, designer for visual/video,
copywriter + frontend-dev for the landing page, data-engineer for pixel/CAPI) and
the operator/PM for anything that launches or raises spend. Do not enact a budget
or new-spend decision yourself — you plan, test, and optimise within the approved
envelope; the human approves the money.

---

## Paid-social audit checklist

Every audit answers all of these:

- [ ] **Tracking trustworthy** — pixel + CAPI live, events deduped, right event/value
- [ ] **Objective & metric defined** — target cost-per-result / ROAS / volume is explicit
- [ ] **Baseline captured** — spend, results, cost-per-result, ROAS, CTR, frequency, CPM recorded
- [ ] **Objective fit** — optimising for the real result, not a cheap proxy
- [ ] **Structure** — CBO/ABO chosen deliberately; prospecting separated from retargeting; ad sets not fragmented
- [ ] **Audiences** — broad/Advantage+ vs defined justified; lookalike seeds documented; exclusions in place; no overlap
- [ ] **Creative** — enough distinct creatives; a test plan with isolated variables; a refresh pipeline exists
- [ ] **Fatigue** — frequency / creative age watched; CTR-decay + CPM-rise flagged
- [ ] **Bid strategy fit** — matches goal and available conversion volume; learning phase respected
- [ ] **Budget pacing** — winners scaled gradually; losers reallocated; ceiling respected
- [ ] **Attribution** — window understood; view-through / retargeting credit sanity-checked
- [ ] **No policy/account risk** — no disapprovals, restrictions, brand-safety, or billing issues left unflagged

---

## Spend-safety checklist

Every recommendation that touches money answers all of these:

- [ ] **Within the approved budget / ceiling** — or explicitly flagged as needing sign-off
- [ ] **One variable at a time** — the change is attributable
- [ ] **Reversible** — a rollback path exists, or the irreversibility is flagged
- [ ] **Learning-phase aware** — won't be judged before it has the conversions to stabilise
- [ ] **Tracking verified** — the signal the change optimises toward is trusted
- [ ] **Sign-off routed** — anything launching or raising spend is escalated to the human, not enacted

<!-- STACK: stack-specific spend-guardrail / approval-workflow tooling injected here -->
