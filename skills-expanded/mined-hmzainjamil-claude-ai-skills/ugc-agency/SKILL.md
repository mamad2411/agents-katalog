# UGC Agency — Arcads AI Actor Pipeline
## Triggers: ugc ads, ugc agency, arcads, ai actors, ai ugc, generate ugc, ugc video, ugc brief, generate 20 ads, lipsync ads

## SETUP
- Repo: ~/installed-repos/ads-creative/arcads-claude-code/
- Setup: cd ~/installed-repos/ads-creative/arcads-claude-code && ./scripts/setup.sh
- Key: ARCADS_API_KEY (set after arcads.ai signup)

## BRIEF TEMPLATE (3 sentences → 20 MP4s)
"Product is [X]. Audience is [Y who care about Z]. Offer is [price/CTA].
Generate 20 UGC ads — different hooks, different actors, different angles."

## PIPELINE
1. Claude writes 20 scripts (testimonial/DR/pattern-interrupt/problem-solution/social proof)
2. Actor matched per script (age/vibe/energy)
3. All 20 jobs fired to Arcads API in parallel
4. MP4s → ~/ugc-output/ named by hook type

## AGENCY MATH
$1,500/mo revenue · ~$150/mo tools · 90% gross margin
Niche targets: supplements, skincare, fitness, DTC food, pet products

## ARCADS API
Base: https://api.arcads.ai/v1
Auth: Bearer $ARCADS_API_KEY
Endpoints: POST /videos/generate · GET /videos/{job_id} · GET /actors
