---
name: trip-map-builder
description: >
  End-to-end trip planning: gather user constraints, build itinerary, research
  locations via 小红书 (OpenCLI + Chrome CDP), then generate an interactive
  mobile-first map page (Leaflet + timeline) and optionally deploy to Vercel.
  Use when user asks to plan a trip, create an itinerary, research restaurants
  on 小红书, build a trip map page, or says "行程规划", "行程地图", "trip map",
  "plan my trip", "做个行程". Covers the full pipeline from scattered inputs
  (screenshots, wishlists) to a deployable single-page app with Google Maps
  links, 小红书 links, payment info, and reservation buttons.
---

# Trip Map Builder

Three-phase pipeline: **Plan → Research → Build**.

## Phase 1: Plan the itinerary

Read `references/trip-planning.md` for the full methodology.

Core sequence:

1. **Extract hard constraints** — dates, flight times, terminals, hotel location
2. **Group user's wishlist** — city-easy / needs-reservation / far-suburbs / pass-through
3. **Cut high-risk items first** — too far, holiday-crowded, weather-dependent. Say what was cut and why.
4. **Arrange by area** — one main area per day, first day light, last day close to airport
5. **Fill in meals** — route-proximity first, vibe second, fame last. Always give main + backup.
6. **Add tickets & transport** — only critical ones (museum tickets, airport transfer)
7. **Write executable doc** — conclusion first, then daily plan, then what was cut

Key principles:
- Not everything the user listed fits. Delete for them.
- One area per day. One reservation-required spot per day max.
- Itineraries should be smooth, not packed.
- All user-facing questions follow the **4-beat format**: Re-ground → Simplify → Recommend → Options. See `references/trip-planning.md` § 用户交互 for examples and anti-patterns.

## Phase 2: Research via 小红书

Read `references/xhs-research.md` for the full OpenCLI + CDP workflow.

Core sequence:

1. Launch Chrome with `--remote-debugging-port=9223`
2. Connect via OpenCLI's `CDPBridge`
3. Navigate to `xiaohongshu.com/search_result?keyword=<encoded>` (never simulate input box)
4. Intercept `POST /api/sns/web/v1/search/notes` response
5. Pick top 2-3 notes by relevance, open detail pages
6. Extract via DOM: `#detail-title`, `#detail-desc`, `.author-container .username`
7. Compress to one decision-useful sentence per store, write back to local `.md`

Filtering rules:
- Keep: specific store name, address, dish, personal experience, repeated keywords
- Drop: generic area roundups, reposts, pure emotion, "氛围很好" x3
- Output: store name + one representative link + 2-3 sentence verdict

## Phase 3: Build the map page

1. Copy `assets/template.html` → `index.html`
2. Fill `HOTEL` object and `DAYS` array with structured data from Phase 1+2
3. Each location needs: name, lat/lng, type, time, desc; optional: budget, detail, pay, xhs, reserve, gmap
4. Fill `overviewContent()` with trip summary, payment warnings
5. Apply design system — default template uses Apple style, but can switch to any style from awesome-design-md

Location types: `food` | `spot` | `drink` | `hotel` | `transport`

Payment chip values: `1` = confirmed yes (green), `0.5` = maybe (orange), omit = not shown

### Design system (optional)

Default template uses Apple design system (SF Pro, light theme, frosted glass).

To use a different style, grab a `DESIGN.md` from [awesome-design-md](https://github.com/VoltAgent/awesome-design-md):

```bash
# Browse available design systems
# Apple, Vercel, Linear, Stripe, Notion, Airbnb, Nike, Spotify, etc.
curl -O https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/<brand>/DESIGN.md
```

Then adjust `template.html`'s `:root` CSS variables (colors, fonts, spacing, border-radius) to match the chosen DESIGN.md tokens.

### Deploy (optional)

```bash
git init && git add . && git commit -m "trip map"
gh repo create REPO --public --source=. --push
# Import from vercel.com/new — auto-deploys on push
```

## Dependencies

| Tool | Purpose | Install |
|------|---------|---------|
| [OpenCLI](https://github.com/jackwener/OpenCLI) | Chrome CDP bridge for 小红书调研 | `npm install -g @jackwener/opencli` |
| Chrome/Chromium | 浏览器 + 远程调试 | 已有 |
| [Leaflet.js](https://leafletjs.com) | 地图渲染（CDN 引入，无需安装） | template.html 内置 |
| [gh CLI](https://cli.github.com) | GitHub 仓库创建（可选） | `brew install gh` |

## Resources

- `references/trip-planning.md` — itinerary planning methodology, input/output templates, selection principles, common pitfalls
- `references/xhs-research.md` — OpenCLI installation, Chrome CDP setup, 小红书 search workflow, API details, filtering criteria
- `assets/template.html` — single-file HTML map template (Leaflet + Apple design system)
- [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — 60+ brand design systems (Apple, Vercel, Stripe, Linear, etc.) for alternative styling
