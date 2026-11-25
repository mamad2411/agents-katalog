---
name: supplement-stack
category: health
description: Design, research, source, and document a comprehensive personal supplement stack. Covers requirement gathering, supplement research, bulk/retail sourcing (Alibaba + domestic + premium), cost calculation, and GitHub-hosted documentation with cost calculators.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [supplements, health, wellness, sourcing, cost-tracking]
    triggers: [supplement stack, supplement regimen, supplement sourcing, supplement cost calculation, bulk buying supplements]
---

# Supplement Stack Planning

Design a complete personal supplement stack for a user — from requirements to documented GitHub repo with cost tracking.

## Trigger
User asks to plan, build, or optimize a supplement regimen. Or mentions supplements, stacking, sourcing, or bulk buying.

## Workflow

### Phase 1: Requirements Gathering
Ask targeted questions in this order:
1. **Primary goals** — longevity, athletic performance, brain health, general health, or a mix
2. **Existing stack** — what they currently take (brand, form, dosage)
3. **Past stack** — what they've taken before and liked/disliked
4. **Bloodwork** — any recent labs, known deficiencies, or flagged markers
5. **Diet** — omnivore, carnivore, keto, vegetarian, etc.
6. **Health conditions + meds** — anything that affects supplementation
7. **Preferences** — forms (capsules vs powders vs pouches), taste sensitivity, budget
8. **Sourcing preference** — bulk (Alibaba), premium domestic (Thorne/ND), convenience retail

### Phase 2: Stack Design
Organize into tiers:
- **Already taking** — keep, potentially upgrade brand
- **Foundation** — essentials (magnesium, D3+K2, omega-3, zinc, B-complex, creatine)
- **Longevity** — NMN, GlyNAC, CoQ10, berberine, astragaloside IV, resveratrol
- **Performance** — beta-alanine, citrulline malate, collagen
- **Brain** — L-theanine, lion's mane, alpha GPC, adaptogens
- **Daily carry** — pouches, gummies, or on-the-go formats

For each supplement specify: dosage, timing, form, cycling needs, and sourcing tier.

### Phase 3: Certification Evaluation
Before sourcing, assess the user's certification requirements. Common hierarchy:

| Level | What It Means | Who Has It |
|---|---|---|
| **NSF Certified for Sport** | 🥇 Gold standard. 270+ banned substance tests + GMP audit + label claim verified. Pro sports standard. | Thorne (most of their line) |
| **USP Verified** | 🥇 Highest US purity/potency standards. Audited manufacturing + label accuracy. | Some Life Extension products |
| **Third-Party GMP** (NSF GMP, UL GMP, SGS GMP) | ✅ Independent audit of manufacturing facility and practices. Real certification. | NOW Foods, Life Extension |
| **HPLC Batch Tested** | 🔬 Every batch tested for identity + purity (internal lab, not 3rd party). | Nootropics Depot standard |
| **FDA cGMP** | ⚠️ Legal minimum. ALL supplement companies must comply by law. Means nothing as a differentiator. | Everyone (required) |
| **"GMP Certified" (no auditor named)** | ❌ Could be meaningless self-claim. Always verify WHO certified them. | Red flag if unverifiable |

**Important:** Correct the user if needed — GMP is the floor (required by law), NOT the ceiling. NSF Certified for Sport or USP Verified are the actual highest certifications.

### Phase 4: Sourcing Research — Dual Tier
Build **three tiers side by side** as the standard output format. Show all three so the user can decide their mix:

1. **Premium NSF/GMP** — Thorne, Nootropics Depot, Life Extension. Highest certs, capsules, zero taste, no fillers. For everything that matters.
2. **Budget GMP** — NOW Foods, BulkSupplements. GMP-certified facilities, same molecule, fraction of price. For simple standalone molecules.
3. **Alibaba Bulk** — Raw powder from Chinese manufacturers. Lowest price, user handles QC (3rd party testing ~$150-300/sample). Only worth it at 5kg+ volumes.

**Search strategy:**
- Premium brands: `"Thorne <supplement> price"`, `"Nootropics Depot <supplement> capsules price"`
- Budget GMP: `"NOW Foods <supplement> price 2026"`
- Alibaba: `"<supplement> bulk powder price"` on Alibaba
- Reddit: `"site:reddit.com r/Nootropics <supplement> supplier"` and `"site:reddit.com r/Supplements <supplement> brand"`

**Standard recommendation:** the operator Hybrid — premium (NSF/GMP) for critical supplements (creatine, omega-3, NMN, CoQ10, berberine, mag glycinate), budget GMP for simple molecules (chlorophyll, glycine, NAC, sea moss). This typically saves ~35-40% over all-premium.

### Phase 5: Pricing & Cost Calculation — Dual Tier Format
Build a cost calculator (Python) with **three columns** as the standard output format:

```
Premium NSF/GMP | Budget GMP | Alibaba Bulk
```

For each supplement, compute per-day and per-month cost for all three tiers. The calculator should:

- Show per-supplement monthly costs side-by-side in a table
- Aggregate: core stack total, + training extras total
- Apply buffer (default 10% for premium, prices change)
- Compute annual totals
- **Highlight a "the operator Hybrid" row** — premium for critical items, budget GMP for simple molecules — with the hybrid total and savings vs all-premium
- Include initial setup cost (first purchase of all bottles)

**Critical:** Run the calculator, capture the output, and present it in the conversation. **Verify with an ad-hoc script** written to a tempfile under `~/AppData/Local/Temp/hermes-verify-*.py` — assertions on total count, cost ranges, and buffer math.

**Verification script pattern (Python):**
```python
exec(open('scripts/cost-calculator.py').read())
assert len(supplements) == 15
assert 300 < prem_core < 500
assert 100 < budg_core < 200
assert hybrid_core < prem_core
# tempfile, run, capture, os.unlink
```

### Phase 6: Documentation — Dual Tier Edition
Create a structured repo with. Standard output format should show BOTH the budget and premium options side-by-side in a comparison table:

- `README.md` — overview, dual-tier summary, the operator Hybrid recommendation
- `PLAN-v2.md` — the user's actual plan (v2 if preferences revised it)
- `docs/sourcing/00-dual-tier-comparison.md` — FULL side-by-side of premium vs budget vs bulk for EVERY supplement, with certifications labeled
- `docs/supplements/00-master-list.md` — master table with ALL supplements, doses, timing, cycling
- `docs/supplements/XX-<supplement>.md` — individual dossiers (one per supplement)
- `docs/protocols/01-daily-routine.md` — schedule by time of day
- `docs/protocols/02-cycling-protocol.md` — which supplements to cycle and when
- `docs/protocols/03-stacking-warnings.md` — interactions, contraindications
- `docs/sourcing/01-alibaba-pricing.md` — bulk pricing reference
- `docs/sourcing/02-reddit-suppliers.md` — brand intelligence from Reddit
- `docs/sourcing/03-price-comparison.md` — Alibaba vs domestic vs retail
- `scripts/cost-calculator.py` — runnable dual-tier cost calculator

### Phase 7: GitHub Repo Setup
1. `git init` in the supplement directory
2. `gh repo create <user>/<name> --private`
3. Commit with conventional commit format: `feat:`, `docs:`, `plan-v2:`
4. Push after each meaningful batch

## the operator-Specific Preferences (Embed These)
- **No taste tolerance** — everything must be capsules or truly tasteless powder. If it tastes like ass, it goes in a capsule. Period.
- **Dual-tier presentation required** — ALWAYS show BOTH budget bulk AND premium GMP/NSF options side-by-side. the operator wants to see the comparison. Single-tier recommendations will be sent back.
- **Premium brands only for his personal use** — Thorne (NSF Sport), Nootropics Depot (HPLC batch), Life Extension (3P GMP). No Alibaba bulk for his own stack unless the powder is tasteless.
- **No fillers** — no maltodextrin, silicon dioxide, magnesium stearate, or proprietary blends. Single-ingredient or verified-clean formulations only.
- **Zennies pouches** — daily carry that covers: caffeine, Alpha GPC, L-Theanine, L-Tyrosine, Lion's Mane, Cordyceps, Reishi, Taurine. ~$0.50/pouch, Walmart/Amazon.
- **Documentation must be thorough** — commit often, track everything.

## Tips & Techniques
- **Reading user supplement photos** — users often send images of their current or past stacks. Use `pytesseract.image_to_string()` (via `terminal` or `execute_code`) to OCR the image. On Windows: `python -c "from PIL import Image; import pytesseract; print(pytesseract.image_to_string(Image.open(path)))"`. This is more reliable than vision_analyze.
- **Hybrid recommendation output** — after building the full dual-tier comparison, always compute and present a "the operator Hybrid" mix: premium (NSF/GMP) for critical/core supplements, budget GMP for simple standalone molecules. Pros: saves 35-40% over all-premium on simple stuff, same quality where it counts. Format as a table showing which tier each supplement falls under.
- **Certification labeling in tables** — label each product in comparison tables with its cert badge: 🧪 NSF Sport, 🏭 3P GMP, 🔬 HPLC, 🟢 Bulk. Users process cert info faster when it's inline.

## Pitfalls
- **Don't assume bulk Alibaba powders are OK** — user may hate the taste. Always ask about taste tolerance first.
- **Don't suggest powders for bitter supplements** — berberine, NMN, NAC, citrulline malate, beta-alanine all taste bad in bulk powder form. Default to capsules for these.
- **Don't skip the "have you taken this before?" question** — past experience (likes/dislikes) is the strongest signal for what will stick.
- **Don't forget Zennies/on-the-go format** — many users want a convenient daily carry option alongside home dosing.
- **Cost calculator must be run, verified, and output captured** before presenting numbers. Use ad-hoc tempfile verification with assertions.
- **Update docs to match user's FINAL preferences** — if they revise mid-session, use v2/v3 markers rather than leaving stale docs as the truth.
- **Don't present a single-tier stack** — always show both budget and premium side-by-side unless the user explicitly says "just give me the premium option." Three-column format (Premium | Budget GMP | Alibaba Bulk) is the standard output shape.
- **Memory is not enough for user preferences** — embed taste/hate/brand/preference patterns in the skill body so future sessions load them automatically.
- **Don't recite GMP as the top cert** — if the user says "GMP is the highest", gently correct: NSF Certified for Sport or USP Verified are the actual gold standards. GMP is the legally-required floor.
