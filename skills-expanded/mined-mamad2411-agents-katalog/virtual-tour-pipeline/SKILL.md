---
name: virtual-tour-pipeline
description: Generate immersive scroll-through virtual tours from Zillow listing data. Scrape listings, classify rooms, build tour sites, upsell agents.
version: 1.0.0
author: the operator
license: MIT
metadata:
  hermes:
    tags: [virtual-tour, market-lead, zillow, scroll-world, 3dgs, lead-gen, agent-outreach]
    triggers:
      - virtual tour
      - house tour
      - zillow tour
      - real estate tour
      - listing walkthrough
      - scroll world real estate
      - agent outreach
      - property visualization
    related_skills:
      - website-landlord-astro-builder
      - scroll-world
      - scroll-world-site-builder
---

# Virtual Tour Pipeline

Generate immersive scroll-through virtual tour websites from real estate listing data, then reach out to listing agents to sell them the service.

## Architecture

```
Zillow Scraper API → Property JSON + Photos → Vision room classifier → Floor plan parser → Scroll-tour HTML → Deploy → Agent outreach
```

## Pricing Tiers (sell to agents)

| Tier | What they get | Our cost | Sell price |
|------|-------------|----------|------------|
| Standard | Photo scroll tour from Zillow photos + floor plan + agent CTA | ~$0.01 | $197 |
| Plus | Above + Higgsfield camera-flight walkthrough (room-to-room) | ~$9-11 | $297 |
| Premium | Above + full 3DGS navigable walkthrough (on-site capture) | ~$10-17 | $497 |
| Elite | Premium + drone exterior GS + social cutdowns | ~$15-25 | $997 |

## Zillow Data Pipeline

### Recommended Scraper: Zillow Scraper API (zillowscraperapi.com)
- **Free tier:** 1,000 requests, no credit card — covers months of dev
- **Pro tier:** $49/mo, 82K requests
- **Data:** full property JSON, photos (20-30), agent name/brokerage, floor plan URL
- **Endpoint:** REST API, returns structured JSON

**Alternatives:**
- Apify Zillow actors (~$2/1K results, $5 free credits)
- Bright Data Zillow scraper ($1.50/1K, 5K free/mo)
- HasData (has MCP server integration)
- APIllow ($54/yr, limited data)

### Room Classification
Zillow photos come with captions but they're not always reliable. Run through a vision model (GPT-4o/Gemini/Claude) to:
1. Classify each photo by room type (living_room, kitchen, master_bed, bedroom, bathroom, exterior, backyard)
2. Deduplicate — group multiple photos of same room
3. Order rooms into logical tour flow: exterior → entrance → living → kitchen → bedrooms → outdoor
4. Identify best primary photo per room

### Floor Plan Parsing
If the listing has a floor plan image:
- Use vision to extract room labels, dimensions, adjacency
- Build spatial map for tour order and camera path
- Embed as navigable overlay that highlights current room during scroll

## Tour Generation Rules (CRITICAL)

1. **NO FABRICATION** — Only rooms that actually exist in the photos. Only descriptions backed by listing data. No AI-generated rooms or furniture.
2. **Real data first** — Every section must use actual listing photos, not stock or generated images.
3. **Logical flow** — Room order must follow actual house layout (from floor plan or photo sequence).
4. **Agent info prominent** — Always include agent name/brokerage/phone as floating card.
5. **Upsell built in** — Last section pitches the paid service: "Want this for your listing?"

## 3D Reconstruction (Premium Tier)

### FOSS Tools

| Tool | Use | Cost | Notes |
|------|-----|------|-------|
| NoPoSplat (github.com/cvg/NoPoSplat) | Feed-forward 3DGS from sparse unposed photos | Free (local GPU) | Best for Zillow's ~20 photos — no poses needed |
| Splatt3R (github.com/btsmart/splatt3r) | Zero-shot GS from image pairs | Free | HF demo available |
| Nerfstudio/gsplat | Full GS training (CUDA) | Free | Needs 100+ photos with poses |
| DUSt3R/MASt3R (NAVER) | 3D from image pairs, no poses | Free | Foundation model |
| Postshot (Jawset, jawset.com) | Desktop GS trainer, Windows | €0 (Indie tier, commercial) | Drag-and-drop, zero-code |
| GaussianSplats3D (npm) | Three.js GS web viewer | Free | Embed in tour pages |

### Capture (on-site upsell)
- iPhone + Polycam/SplatKing: 10-min walkthrough, free
- Postshot: train GS locally, export .ply/.splat
- Embed: mkkellogg/GaussianSplats3D npm package

## Cost Model (per house, Tier 2 Plus)

| Item | Cost |
|------|------|
| Zillow API call (search + detail + agent) | ~$0.01 |
| Higgsfield Seedance 2.0 (11 clips, 275 cr) | ~$9-11 (Ultra plan) |
| Web hosting | $0 |
| **Total** | **~$9-11** |

The Ultra plan ($99/mo, 3,000 credits) covers ~11 houses/month at Tier 2.

## References
- `references/zillow-scraper-comparison.md` — Full scraper comparison with pricing
- `references/cost-analysis.md` — Detailed per-house economics
- `references/foss-3d-tools.md` — Open-source 3D reconstruction tools inventory
- `references/competitor-landscape.md` — What else exists in the space
