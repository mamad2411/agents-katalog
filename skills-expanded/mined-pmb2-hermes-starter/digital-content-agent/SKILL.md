---
name: digital-content-agent
description: >-
  Full lifecycle digital product creation and sales automation agent. Research
  trending niches, generate premium PDF products, then deploy across Reddit,
  Pinterest, Quora, TikTok, Facebook, and Gumroad via dedicated API tooling.
  Runs as a weekly cycle with full platform automation.
version: 1.0.1
license: MIT
metadata:
  hermes:
    tags: [digital-product, content-creation, sales-automation, social-media, marketing]
    triggers: [digital product, create digital product, weekly product cycle, content agent pipeline, research niche product, deploy content, publish product, auth setup, configure platforms]
    related_skills: [social-media-automation, business-voice-outreach]
---

# Digital Content Agent

**Repo:** `pmb2/digital-content-agent` on GitHub (private)

## Verification

Before delivering content agent output, verify:
- **Product is launchable** — all runtime scripts present and imports resolve
- **Auth configured** — required API keys (Gumroad token, etc.) in environment
- **Pricing confirmed** — product price set in listing config
- **Post-launch check** — listing is live on target platform before delivering summary

## Reference files in this skill:
- `references/pdf-generation.md` — WeasyPrint/pydyf version compatibility, template substitution system, fontconfig fixes, known pitfalls
- `references/niche-research.md` — Scored niche opportunity database (12 top picks, pricing, demand data) from deep forum/Etsy/Reddit/Trends research
- `references/platform-tooling.md` — API endpoints, auth methods, rate limits, optimal posting times, and key configuration for all 6 platform tools

## Directory
```bash
cd ${USER_HOME}/digital-content-agent
```

## Platform Automation Tooling

Every platform has a dedicated tool module in `tools/` with full API integration:

| Platform | Module | Capabilities |
|----------|--------|-------------|
| **Reddit** | `tools/reddit_tool.py` | Post text/link/image, comment, monitor subreddits, search, DM, analytics |
| **Pinterest** | `tools/pinterest_tool.py` | Create pins, manage boards, bulk create, analytics, search |
| **Quora** | `tools/quora_tool.py` | Answer questions, search questions, track performance (browser auto) |
| **TikTok** | `tools/tiktok_tool.py` | Upload video, schedule, analytics, trending hashtags |
| **Facebook** | `tools/facebook_tool.py` | Post to pages/groups, manage comments, analytics, schedule |
| **Gumroad** | `tools/gumroad_tool.py` | Create/update products, sales data, affiliates, revenue analytics |

**Central infrastructure:**
- `tools/auth_manager.py` — API credentials for all platforms (saves to `config/auth_config.json`)
- `tools/content_scheduler.py` — Unified queue, scheduling, campaign management
- `scripts/setup_auth.py` — Interactive credential setup (`--interactive`, `--status`, `--env-template`)
- `scripts/deploy_content.py` — Cross-platform publishing engine (`--publish-due`, `--status`, `--campaign`)
- `scripts/analytics_report.py` — Aggregate analytics from all platforms (`--overview`, `--export-json`)

## Weekly Cycle Steps

### Phase 1: Market Research
```bash
python scripts/market_research.py --output-dir output/research
```

### Phase 2: Product Creation
1. Create product directory: `mkdir -p products/{niche-slug}`
2. Create `config.json` following `products/adhd-focus-system/config.json`
3. Generate cover: `python scripts/cover_generator.py --title "Title" --subtitle "Subtitle" --style {planner|workbook|template|ebook} --output products/{slug}/cover.png`
4. Generate PDF: `python scripts/generate_ebook.py --config products/{slug}/config.json --output products/{slug}/product.pdf`

### Phase 3: Marketing Assets
```bash
python scripts/marketing_content.py --config products/{slug}/config.json --output-dir output/marketing
```

### Phase 4: Queue & Deploy
1. **Check auth status first:** `python scripts/setup_auth.py --status`
2. **Configure platforms if needed:** `python scripts/setup_auth.py --interactive`
3. **Queue content for publishing** via the content scheduler
4. **Publish due posts:** `python scripts/deploy_content.py --publish-due`
5. **Check status:** `python scripts/deploy_content.py --status`
6. **View analytics:** `python scripts/analytics_report.py --overview`

### Phase 5: Report
Deliver: product name, price, USP, all file paths, which platforms deployed to, engagement stats, and specific next steps.

## Quick Commands Reference

```bash
# Auth
python scripts/setup_auth.py --interactive    # Interactive credential setup
python scripts/setup_auth.py --status         # Check which platforms are ready
python scripts/setup_auth.py --env-template   # Print env var template

# Publishing
python scripts/deploy_content.py --publish-due    # Publish all queued posts
python scripts/deploy_content.py --status         # Full queue + auth status
python scripts/deploy_content.py --dry-run        # Preview without publishing

# Analytics
python scripts/analytics_report.py --overview     # Full platform analytics
python scripts/analytics_report.py --export-json  # Export to JSON
```

## Important Notes

### PDF Generation (WeasyPrint)
- WeasyPrint must be installed: `pip install weasyprint`
- **CRITICAL**: Pin pydyf to exactly 0.8.0 for compatibility with WeasyPrint 60.x
  - `pip install pydyf==0.8.0`
  - pydyf 0.11+ changed `PDF.__init__()` signature, breaking WeasyPrint's internal call
  - If you get `TypeError: PDF.__init__() takes 1 positional argument but 3 were given`, it's this version mismatch
- The HTML template uses `__VAR__` style placeholders (NOT `.format()` curly braces) to avoid CSS `{}` conflicts
  - Template file: `templates/ebook_template.html`
  - Substitution in `scripts/generate_ebook.py` via `_load_template()` + `_fill_template()` using `.replace()`
- Fontconfig errors on Windows are cosmetic — PDFs still generate correctly
- Falls back to HTML output if WeasyPrint import fails

### Product Config Format
- `generate_ebook.py` expects config.json with `title` (not `name`) for the product name
- `marketing_content.py` CLI expects `--product-name` NOT `--config` for the product name when called standalone
  - Config JSON uses `title` key but marketing script reads `name` key — use CLI args for standalone calls

### Marketing Content Script
- When running `marketing_content.py --config`, the config MUST have a `name` key (not just `title`)
- Workaround: `python scripts/marketing_content.py --product-name "Name" --niche "niche" --price XX`

### Platform Credentials
- Config auth in `config/auth_config.json` — this file is gitignored, keep it secure
- Or use `DCA_*` environment variables (see `python scripts/setup_auth.py --env-template`)
- First product reference: ADHD Focus System sample at `products/adhd-focus-system/`

### Gap Analysis to Revenue
When asked "what's blocking money" or "how to make first $500":
1. Check product is generated (PDF + cover exist)
2. Check Gumroad account exists (fastest path — manual upload bypasses API)
3. Check platform credentials configured
4. Identify distribution gaps: Reddit value posts, Pinterest pins, Quora answers
5. Rank blockers by revenue impact: accounts > upload > traffic > optimization
6. For manual posting path: generate exact posts/pins ready for copy-paste
