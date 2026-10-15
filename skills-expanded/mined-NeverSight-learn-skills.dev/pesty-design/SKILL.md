---
name: pesty-design
description: Use this skill to generate well-branded interfaces and assets for Pesty Marketing (the #1 pest control marketing agency — SEO, PPC & web design), either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping. This is the default Pesty design system for all new frontend work.
user-invocable: true
---

Read the `readme.md` file within this skill, and explore the other available files.
If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.
If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Quick reference

- **Brand:** Pesty Marketing — pest control marketing agency. Voice is confident, aggressive, results-obsessed ("dominate your market," lead with real numbers). See readme.md → CONTENT FUNDAMENTALS.
- **Colors:** Pesty Red `#D90429` (primary/CTAs/accents, used sparingly), Deep Teal `#002330` (dark surfaces/headings), white canvas. Full token set in `tokens/colors.css`.
- **Type:** Epilogue (display, 700–800), Montserrat (body), JetBrains Mono (data). See `tokens/typography.css`. These are Pesty's actual brand fonts (loaded from Google Fonts).
- **Foundations:** link `styles.css` to inherit every token. Cards 16px radius + soft cool shadow; buttons/badges/tags are pills; motion is quick with no bounce; primary buttons glow red on hover.
- **Icons:** Lucide-based set in `components/core/Icon.jsx` (24px, 2px stroke). No emoji.
- **Assets:** `assets/brand/` — logo (light/dark) + mark/favicon.
- **Components:** React primitives under `components/` — Button, IconButton, Icon, Badge, Tag, Stat, Card, Avatar, Input, Textarea, Select, Checkbox. Each has a `.prompt.md`.
- **Dashboards / data-dense UI** (internal tools, admin panels, analytics dashboards, client reports): the same light system tuned for density. Components — DataTable, KpiTile, KpiGrid, StatusPill, DeltaPill, Tabs, Chip, SectionHeader, DashboardShell (+ Sidebar, Topbar). Rules + density spec in readme.md → DASHBOARDS & DATA-DENSE INTERFACES; density tokens in `tokens/dashboard.css`. Copy the working example at `ui_kits/dashboard/index.html`.
- **UI kits:** `ui_kits/marketing-site/` — interactive recreation of pestymarketing.com; `ui_kits/dashboard/` — self-contained dense-dashboard example. Copy patterns from either.
- **Templates:** `templates/` — ready-to-seed starting points.

When building static artifacts, copy the assets and the relevant CSS into your output folder and link `styles.css` (or inline the tokens you need).

> Maintained by [Pesty Marketing](https://pestymarketing.com) · Browse the [full skill catalog](https://pestymarketing.com/agent-skills/).
