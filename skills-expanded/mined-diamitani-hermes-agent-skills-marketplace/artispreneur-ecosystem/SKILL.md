---
name: artispreneur-ecosystem
description: Build and deploy Artispreneur-branded sites (landing, academy, directory) using the shared dark luxury design system. Covers the design DNA, deployment flow, cross-linking, and adding new sites.
---

# Artispreneur Ecosystem

Multi-site brand platform for Artispreneur — a dark premium aesthetic used across landing pages, course academies, and directories. All sites share one design system and deploy to Vercel under the `artispreneur` team.

## Design DNA

Every Artispreneur site uses this exact design language:

| Token | Value |
|---|---|
| Background | `oklch(0.08 0.005 250)` |
| Foreground | `oklch(0.98 0 0)` |
| Card | `oklch(0.12 0.005 250)` |
| Border | `oklch(0.22 0.005 250)` |
| Gold accent | `oklch(0.72 0.19 85)` |
| Muted text | `oklch(0.55 0 0)` |
| Font - sans | Inter |
| Font - serif | Playfair Display (via `variable: "--font-serif"`) |
| Font - mono | Geist Mono |

**Reference files**: `references/globals.css` (full design CSS), `references/video-player.tsx` (YouTube+HeyGen player)\n\n**globals.css essentials** — full reference at `references/globals.css`:
- `@import "tailwindcss"` + `@import "tw-animate-css"`
- CSS custom properties block (`:root { ... }`) with all color tokens
- `@theme inline { ... }` mapping vars to Tailwind
- `@layer base { * { @apply border-border } body { @apply bg-background text-foreground } }`
- `::selection` with gold tint
- Custom scrollbar (gold on hover)
- `body::after` grain noise SVG overlay at `opacity: 0.04`
- Keyframes: `fade-up`, `blink`, `pulse-dot`, `scanner`, `waveform`, `rotate-slow`, `float-up`, `card-shuffle`
- Utility classes: `.magnetic-btn`, `.glass-card`, `.glass-dark`, `.text-gradient-accent`, `.section-divider`

**layout.tsx essentials**:
```tsx
import { Inter, Playfair_Display } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
const inter = Inter({ subsets: ["latin"] })
const playfair = Playfair_Display({ subsets: ["latin"], variable: "--font-serif" })
// body: className={`${inter.className} ${playfair.variable} font-sans antialiased`}
```

**package.json minimal set**: next, react, react-dom, @vercel/analytics, lucide-react, tailwindcss, tw-animate-css, typescript, @types/react, @types/node.

## Live Sites (July 2026)

| Site | URL | Type | Purpose |
|---|---|---|---|
| **Platform Hub** | `artispreneur-platform.vercel.app` | Static HTML | Product overview — describes all 5 products with user-friendly language |
| **Landing + Workspace** | `artispreneur-landing.vercel.app` | Static HTML | Public storefront + agent workspace dashboard + signup + chat UI |
| Academy | `academy-build.vercel.app` | Next.js | 16 courses, 307 modules, video lessons |
| Directory | `directory-artispreneur.vercel.app` | Next.js | 13 categories, 78K+ contacts, searchable, dark luxury SaaS design |
| Agency | `artispreneur-agency.vercel.app` | Next.js | Project mgmt, kanban, KPIs |
| Agency | `artispreneur-agency.vercel.app` | Next.js | Project mgmt, kanban, KPIs |
| **Rostr Contracts** | `contractagent-artispreneur.vercel.app` | Next.js | AI contract agent — 21 music contract templates, AI chat + form generation, localStorage auth, 3-step onboarding. Source: `diamitani/contract_agent`. Deployed July 2026. |

**All deploy under the `artispreneur` Vercel team.**

**Directory deploy note:** The canonical directory source repo is `diamitani/artispreneurconnect` but the Vercel project `artispreneurconnect` may be rate-limited from rapid CLI deploys. The working Vercel project is `adb-deploy` aliased to `directory-artispreneur.vercel.app`. If the original project's rate limit clears, redeploy there; otherwise deploy from a fresh project and re-alias. See `vercel-deploy` skill for the rate-limit workaround pattern.

### Platform Hub (NEW — v2.0+)

The platform hub (`artispreneur-platform`) is the main marketing site that describes all products in plain language. It has 4 pages: `index.html` (landing), `academy.html`, `directory.html`, `signup.html`. The landing page uses empathetic, conversational language — NOT technical jargon. Key sections: "Sound Familiar?" (pain points), "What We Do" (solutions in plain English), "Pick Your Stage" (interactive career stage selector), embedded chat widget.

**Academy**: 8 courses, 136 YouTube video lessons across Business, Legal, Marketing, Distribution, Royalties, Licensing categories. Source: `music_business_videos.csv` (curated YouTube playlist, 136 entries grouped by search_query tag into 8 courses).

**Directory**: 6 categories, 183 contacts — venues (45), radio stations (40), music blogs (35), press (25), podcasts (20), community resources (18). Full-text search at `/search`. **CSV monetization**: See `references/directory-csv-monetization.md` for the paid export pattern (JSON → CSV, Stripe one-time $20 checkout, download page).

## Landing Page Architecture

**The landing page (`artispreneur-landing`) is NOT Next.js** — it's standalone static `.html` files with embedded CSS. Zero build step, zero dependencies. Vercel deploys them as static assets instantly. Full page inventory and cross-linking matrix at `references/landing-pages.md`.

### Page inventory (10 pages, all cross-linked):

| File | Route | Content |
|------|-------|---------|
| `index.html` | `/` | Redesigned landing — hero with chat UI, 6 agents, tools section, pricing, CTA |
| `about.html` | `/about` | Mission, 3 pillars, ecosystem map, tech stack |
| `pricing.html` | `/pricing` | Free / BYOK / Pro tiers with FAQ, links to signup flow |
| `academy.html` | `/academy` | 16 courses from spreadsheet data, filterable by category, cross-linked to `rostr-academy.vercel.app` |
| `contact.html` | `/contact` | Contact form, ecosystem links, 6 directory categories |
| `blog.html` | `/blog` | 5 articles on music business topics |
| `privacy.html` | `/privacy` | Data handling, BYOK, Signal/Wire encryption |
| `terms.html` | `/terms` | Usage terms, agent liability, BYOK policy |
| `directory.html` | `/directory` | 74 contacts, 6 categories, live search, pagination, grid view |
| `signup.html` | `/signup` | 5-step onboarding wizard: Who Are You → Your Story → Current Situation → Experience → Goals + Links. PAL bio generation, link scraping, S3 provisioning. `onboarding.html` redirects here. |
| `login.html` | `/login` | Email/password + Google OAuth, redirects to workspace on success |
| `skills.html` | `/skills` | Skill Builder — create custom agent skills, YAML manifest export, PDF generation (EPK, splitsheet, contracts, release plan via jsPDF) |
| `profile.html` | `/profile` | Auto-generated artist profile from onboarding data |
| `workspace.html` | `/workspace` | Claude Code-level agent workspace with chat, skills, command palette, context panel |
| `courses/*.html` | `/courses/{slug}` | 16 course detail pages with full module breakdowns (307 modules total)

### Rostr Agent Rebrand (v2.17+) + Rostr Academy (v2.0)

The ecosystem now uses "Rostr" as the product brand under the Artispreneur parent:

- 🏠 **Artispreneur** — parent brand (landing, pricing, directory)
- ◈ **Rostr Agent** — the agent workspace product (powered by Artispreneur)
- 🎓 **Rostr Academy** — the course platform (powered by Artispreneur)

Both Rostr-branded products use the same header pattern: product name with gold-accented "Rostr" prefix + "Powered by Artispreneur" subtext in 8px uppercase.

**Next.js header pattern (Rostr Academy):**
```tsx
<div>
  <div className="font-serif font-bold text-sm" style={{ color: "oklch(0.98 0 0)" }}>
    Rostr<span style={{ color: "oklch(0.72 0.19 85)" }}>Academy</span>
  </div>
  <div style={{ fontSize: "8px", fontWeight: 700, letterSpacing: "1px",
    textTransform: "uppercase", color: "oklch(0.45 0 0)" }}>
    Powered by Artispreneur
  </div>
</div>
```

**Academy is now Supabase-free (v2.0).** All 16 courses are served from static `lib/courses.ts`. No auth, no database — guest-friendly viewing. AWS-ready stubs at `lib/media.ts` and `lib/course-transcripts.ts` for future backend integration. Full removal recipe at `references/supabase-removal-recipe.md`.

**Workspace header pattern:**
```html
<div class="sidebar-header">
  <img src="logo.png" alt="A">
  <div>
    <div style="font-family:'Playfair Display',serif;font-size:13px;font-weight:800">
      Rostr<span style="color:var(--gold)">Agent</span>
    </div>
    <div style="font-size:8px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--text-dim)">
      Powered by Artispreneur
    </div>
  </div>
</div>
```

**Affected files**: workspace.html (title, sidebar header, toolbar title, chat empty state)
**Page title**: `<title>Rostr Agent — Powered by Artispreneur</title>`

## Shimmer Heading Animation

Gold gradient shimmer on the chat empty state heading:
```css
.chat-empty h2 {
  background: linear-gradient(90deg, var(--text) 0%, var(--gold) 50%, var(--text) 100%);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shimmer 3s linear infinite;
}
@keyframes shimmer { 0% { background-position: -400px 0; } 100% { background-position: 400px 0; } }
```
Also add `@keyframes blink` for cursor effects: `0%,100%{opacity:1}50%{opacity:0}`

## Pricing (v2.17+)

New pricing model: Free/BYOK, Pro $9.99 (100 chats), Unlimited $19.99. All LLMs routed through AWS Bedrock DeepSeek V3. Full budget model in `references/pricing-model.md`.

Pricing page at `/pricing.html` with three-tier comparison, trust banner, FAQ, and plan-pre-selection via URL params (`?plan=free|pro|unlimited`).

`workspace.html` is the core product — a premium agent harness designed for musicians. Pattern: 3-panel layout (sidebar | chat | context panel).

**Layout**: `display:grid;grid-template-columns:240px 1fr 0px` with `.context-open` class expanding to `240px 1fr 320px`. Sidebar has top-section nav items (Chat, Agents, Skills, Outputs) + middle library (Prompts, Knowledge, Academy, Directory) + bottom account. Every nav item is a `<button>` or `<a>` with `.active` class for gold highlighting.

**Chat UI**: Messages with agent avatars (color-coded: gold=PRO, green=Distribution, purple=Licensing, blue=Legal, cyan=Finance, orange=Manager), typing indicators (CSS bounce dots), auto-resizing textarea, Enter to send / Shift+Enter for newline. Agent switching is contextual — asking about royalties auto-routes to PRO Agent, playlist questions to Distribution, legal to Legal.

**Skills Marketplace**: Overlay panel with search. 15 skills across PRO/Distribution/Licensing/Legal/Finance/Manager categories. Each skill card has install/uninstall toggle. Rendered client-side from JS data array.

**Command Palette (⌘K)**: `position:fixed` overlay with blurred backdrop, search input, results list. Searches across agents, skills, prompts, and actions. Arrow keys navigate, Enter selects, Escape closes. Items have icons + names + type badges.

**Prompt Library**: 15 prompts across 5 categories (Release, Promotion, Legal, Finance, Creative). Click any prompt to populate the chat input and auto-navigate to chat view.

**Context Panel**: Right sidebar toggle — shows active project, recent outputs, quick action buttons. Toggleable via toolbar button or command palette.

**Key features**: Agent contextual switching (auto-detects intent from message), ⌘1-6 keyboard shortcuts for agent switching, real markdown rendering in chat bubbles, Geist Mono font for code/pre blocks, smooth CSS animations on message appearance.

**The full message flow**: User types → message appears right-aligned in gold bubble → typing indicator appears → agent response with contextual routing → message appears left-aligned with agent avatar. After 3+ messages in demo mode, a CTA suggests creating a workspace.

### Backend architecture

Three architectures are available:

**v2 (Supabase — Free tier, $0/month):** Full schema and stack at `references/backend-schema.md`. Single Supabase PostgreSQL, pgvector for RAG, RLS on every table.

**v3 (AWS-Native — Production, $1.62/month):** Full Terraform IaC and Bedrock DeepSeek V3 backend at `references/aws-architecture.md`. RDS PostgreSQL + pgvector, shared compute.

**v4 (AWS Multi-Tenant — Production, per-user Lightsail):** Full infrastructure at `references/aws-architecture-v4.md` and source code at `~/artispreneur-infra/`. DynamoDB single-table, per-user Lightsail instances, CloudWatch Bedrock credit monitoring, Composio integrations. Complete provisioning pipeline and bootstrap script at `references/multi-tenant-provisioning.md`. This is the current target architecture (July 2026).

**Modular backend pattern:** 13 files, 291 lines, 22 avg lines/file. Clean separation into config/auth/agents/db/routes. See `references/modular-backend.md`. Also see `references/contract-agent-backend.md` for the Rostr Contracts variant (contract-specific AI agent routes, Bedrock DeepSeek fallback, 14 pre-registered templates). Replaces Supabase with Cognito (auth), RDS PostgreSQL + pgvector (DB), S3 (storage), Lambda + API Gateway (compute), Bedrock DeepSeek V3 (LLM), ElastiCache Redis (cache), CloudFront (CDN). Complete `terraform/` directory with main.tf, variables.tf, outputs.tf. Lambda backend at `backend/main.py` (FastAPI + Mangum).

- **Unified nav bar**: Every page has the same `<nav class="navbar">` with links to all internal pages + academy/directory
- **Footer cross-links**: Footer links to internal pages (`pricing.html`, `blog.html`) AND external live sites (`rostr-academy.vercel.app`, `directory-build.vercel.app`)
- **Real data integration**: Academy page pulls 17 courses directly from `knowledge-base/sites/academy/lib/courses.ts`. Contact page references directory categories and counts from `MASTER.md`.
- **No dead links**: Every CTA, pricing button, and footer link resolves to a real page or external site. Verify with href check — there should be exactly zero `href="#"` anywhere.

### Nav unification (ECOSYSTEM-LEVEL)

Every page MUST have the same ecosystem nav that links across all Artispreneur sites:
```
🏠 Platform | ◈ Workspace | 🎓 Academy | ◉ Directory | Login | Get Started Free
```

On the landing site (`artispreneur-landing`), the Platform link points to `https://artispreneur-platform.vercel.app`. On the platform hub, the Workspace link points to `https://artispreneur-landing.vercel.app/workspace.html`. The footer's first column should be labeled "Ecosystem" with links to all four sites.

Every page MUST have the same nav bar with these 8 links: Agents, Tools, How It Works, Pricing, Academy, Directory, About, Contact. On the index page itself, use same-page anchors (`#agents`). On subpages, use cross-page anchors (`index.html#agents`). The `<nav>` block must be identical in structure across ALL pages — including `privacy.html` and `terms.html` (they need the full 8-link nav, not just a logo).

### VERIFICATION LOOP (MANDATORY)

NEVER claim a page is fixed or deployed until you have run a real QA check against the deployed URL. This is the single highest-priority rule for this project.

Before any claim of completion:
1. `curl -sI` every page on the deployed domain — all must return HTTP/2 200
2. Check that nav links exist on privacy.html and terms.html (they are the most fragile)
3. Check that internal links resolve to existing `.html` files (no 404s)
4. Check that academy course links use correct paths
5. Write a small verification script and run it — do not just visually scan

### Domain Management (Route 53 + Vercel)

**Current production domain**: `rostragent.com` — points to the master v217 platform. DNS managed via AWS Route 53.

Setup pattern:
```bash
# 1. Add domain to Vercel team (if not in another account)
vercel domains add rostragent.com

# 2. Link to project
vercel domains add rostragent.com artispreneur-v217

# 3. Add Route 53 A records (Vercel IPs: 216.198.79.1, 64.29.17.1)
aws route53 change-resource-record-sets --hosted-zone-id Z01563512IZP6LAC0BEYZ ...

# 4. Verify + redeploy (SSL auto-provisions)
vercel domains verify rostragent.com
vercel --prod --yes
```

**If domain exists in another Vercel account**: must remove it there first. Error: "The domain already exists under a different context."

### Academy Sign-Up Page (LEGACY — Supabase removed in v2.0)

**This section is historical reference only.** The academy no longer uses Supabase. See `references/supabase-removal-recipe.md` for the migration steps.

`artispreneur-academy` (`diamitani/artispreneur-academy`) — Next.js 15 app with Supabase auth. Edit `app/auth/sign-up/page.tsx`:
- Keep Supabase integration (existing auth backend)
- Hex colors: `#09090b` (bg), `#c9a227` (gold), `#18181b` (card), `#27272a` (border)
- Add plan selector: Free (BYOK), Pro ($9.99/mo), Unlimited ($19.99/mo)
- Add `plan` column to `academy_profiles` Supabase insert
- Link to `rostragent.com` in footer
- Hero: "You make the music. We handle the rest."
- Build locally first: `npm install && npx next build` — must pass

### Post-Deploy Confirmation (CRITICAL)

After EVERY deploy, do exactly this:
1. Confirm with the user: "Deployed: <hash-url>"
2. Send the **fresh production hash URL** from the Vercel output — NOT just the alias. Example: `https://artispreneur-v217-abc123xyz-artispreneur.vercel.app`
3. Never make the user search for the deployment link.

The user has explicitly stated this preference multiple times: "whenever you finish and send to git and deploy always confirm with me and send new link so i don't have to search."

The hash URL is in the Vercel output line `Production: https://<name>-<hash>-<team>.vercel.app`. Copy it verbatim. Do NOT substitute the alias.

### Master Marketing Site (`diamitani/Artispreneur`)

The master brand site at `artispreneur-theta.vercel.app` is a standalone static HTML page that showcases all 5 ecosystem products with a single unified hero + product grid + footer. Pattern: one page, links out to all sub-sites, same dark gold design DNA. Repo: `diamitani/Artispreneur` (capital A).

```html
<!-- Product grid pattern — 3 columns, featured card for primary product -->
<div class="pgrid">
  <div class="pcard featured">Rostr Agent (6 agents, 30 tools)</div>
  <div class="pcard">Academy (16 courses)</div>
  <div class="pcard">Directory (74+ contacts)</div>
  <div class="pcard">Contracts (PDF generation)</div>
  <div class="pcard">EPK Builder</div>
  <div class="pcard">Platform (profile + KB + S3)</div>
</div>
```

Nav links: Products, How It Works, Pricing, Login, Get Started Free. All CTAs point to `rostragent.com`.

### v217 Master Repo (Unified Platform)

The canonical agent repo is `diamitani/artispreneur-v217` — combines landing, workspace, signup, academy, directory, backend, and Terraform into one unified codebase. Deploy at `rostragent.com` (primary domain).

### Repo Structure
```
artispreneur-v217/
├── index.html              # Landing page with chat UI
├── workspace.html          # Agent workspace dashboard
├── signup.html             # 5-step onboarding wizard (canonical)
├── onboarding.html         # Redirects to signup.html
├── login.html              # Email/password + Google OAuth
├── academy.html            # 16 courses, 307 modules
├── directory.html          # 74 contacts, searchable
├── profile.html            # Auto-generated artist profile
├── skills.html             # Skill Builder + PDF generation
├── courses/*.html          # 16 course detail pages
├── platform.html           # Platform hub (product overview)
├── platform-academy.html   # Platform academy page
├── platform-directory.html # Platform directory page
├── platform-signup.html    # Platform signup
├── backend/                # Full AWS backend
├── terraform/              # AWS IaC
└── directory-data.js       # Contact data
```

### Deploy
```bash
cd /tmp
git clone https://github.com/diamitani/artispreneur-v217.git artispreneur-v217
cd artispreneur-v217
# Edit files...
git add -A && git commit -m "..." && git push origin main
vercel --prod --yes
# Confirm: "Deployed: https://artispreneur-v217-XXXXX.vercel.app"
```

### Previous Repos (legacy, kept for reference)
- `diamitani/artispreneur-landing` — original landing + agent platform
- `diamitani/artispreneur-platform` — original platform hub

```bash
# For artispreneur-landing:
cd /tmp/artispreneur-landing         # ⚠️ always /tmp, never Desktop
git add -A && git commit -m "..." && git push origin main
vercel --prod --yes

# For artispreneur-platform:
cd /tmp/artispreneur-platform        # same pattern — static HTML, no build step
git add -A && git commit -m "..." && git push origin main
vercel --prod --yes
```

Both repos use the same Vercel team (`artispreneur`) and the same static deploy pattern. The platform hub's `vercel.json` needs `{"buildCommand":"","outputDirectory":".","framework":null}` to prevent Next.js auto-detection.

### Verification (all 10 pages):

```bash
for page in "" "about.html" "pricing.html" "academy.html" "contact.html" "blog.html" "privacy.html" "terms.html"; do
  curl -sI "https://artispreneur-landing.vercel.app/$page" | head -1
done
# All must return HTTP/2 200
```

## Deploy Workflow (Next.js sites — Academy, Directory)

To deploy or update an Artispreneur Next.js site:

```bash
# 1. Clone the repo
git clone --depth 1 https://github.com/diamitani/artispreneur-academy.git /tmp/build-dir
cd /tmp/build-dir

# 2. Make changes (edit lib/courses.ts, components, pages, etc.)

# 3. Build locally FIRST to catch errors before deploying
npm install
npm run build

# 4. Deploy to production
npx vercel --yes --prod
```

**Critical**: Always build locally before deploying Next.js sites. Vercel build failures consume time and show up as production errors.

## Adding a New Site to the Ecosystem

The canonical scaffolding pattern (proven 4x: Agency, Forge, Label HQ, Label Site):

### Step 1: Clone and strip
```bash
git clone --depth 1 https://github.com/diamitani/artispreneur-academy.git /tmp/artispreneur-{name}
cd /tmp/artispreneur-{name}

# Strip ALL academy-specific content — be thorough
rm -rf lib/courses.ts app/courses app/course app/auth app/certificates \
       app/dashboard app/media app/verify lib/supabase proxy.ts \
       components/course-card.tsx components/video-player.tsx \
       components/artispreneur-chat.tsx components/header.tsx \
       components/footer.tsx components/hero-section.tsx \
       components/agents-section.tsx components/courses-section.tsx \
       components/features-section.tsx components/membership-section.tsx \
       components/philosophy-section.tsx components/protocol-section.tsx \
       components/transcription.tsx components/module-sidebar.tsx \
       components/media-card.tsx components/theme-provider.tsx

# Also clean lib files that reference supabase/courses
rm -f lib/course-transcripts.ts lib/constants.ts lib/utils.ts lib/media.ts
```

### Step 2: Verify what survived
```bash
ls app/        # should be: globals.css layout.tsx page.tsx (only)
ls lib/        # should be empty or only your new data files
ls components/ # should be: ui/ (only the shadcn UI primitives)
```

### Step 3: Keep the design DNA intact
- `app/globals.css` — NEVER modify (dark theme, oklch tokens, grain overlay, animations)
- `app/layout.tsx` — modify metadata + children wrapper only; keep font imports + Analytics
- `package.json` — the academy's full dep set works fine; the Supabase packages don't break builds unless their CODE is imported
- **LocalStorage auth migration**: Full recipe at `references/auth-migration-localstorage.md`. Covers: stripping Supabase/Cosmos deps, fixing AuthProvider union types, adding `hasSupabaseSessionCookie` stub, optional profile field types, 10-step migration, localStorage key schema, and common type errors table.

### Step 4: Build pages using the design tokens
Use inline `style={{}}` with oklch values for custom colors — do NOT add Tailwind color classes. The `globals.css` already defines `--background`, `--foreground`, `--card`, `--border`, `--accent`, `--muted`, `--muted-foreground`, `--secondary`.

### Step 5: Build locally FIRST, then deploy
```bash
npm install
npm run build        # MUST pass with zero errors before deploying
vercel --yes --prod  # use the global vercel CLI, not npx
```

### Step 6: Verify ALL routes (MANDATORY)
```bash
# Use the bundled verification script:
python3 ~/.hermes/skills/web-development/artispreneur-ecosystem/scripts/verify-deploy.py \
  https://{site}.vercel.app "" "/route1" "/route2" ...
```
Every route must return HTTP/2 200 with the correct page title. Wrong title = project name collision — redeploy under a different Vercel project name.

### Dual-Face Pattern (Label Architecture)

When building a record label presence, split into TWO sites:
- **Backend ops site** (e.g. Label HQ) — internal dashboard with sidebar nav, data tables, kanban. Uses the `flex h-screen` sidebar layout pattern.
- **Public marketing site** (e.g. Label Site) — customer-facing storefront with fixed top nav, hero sections, artist grids, demo submission form. Uses the `pt-16` top-nav layout pattern.

This separation keeps internal operations data off the public internet and allows different design densities (data-dense tables vs marketing layouts).

## User-First Design Voice (CRITICAL)

When building ANY Artispreneur page for the PUBLIC (landing, platform hub), use plain language. An independent artist does NOT know what "ROSTR Framework," "PAL compiler," "NPAO orchestration," or "BYOK" means. They just want help.

**Rules:**
- **Start with empathy.** Use quotes from real artist frustrations: "I don't know what a PRO is," "I just want my music on playlists."
- **Explain jargon inline.** Don't say "PRO Agent registers with BMI/ASCAP" — say "We register your music so you actually get paid when it's played."
- **Show outcomes, not features.** "Get your music on Spotify playlists" > "Distribution Agent manages DSP presence."
- **One clear CTA.** Don't present 6 product cards to choose from. Give them one button: "Start for free."
- **Interactive stage picker.** Let users self-identify their career stage and show personalized next steps.

### Platform Hub Landing Page Pattern

```html
Hero: "You make the music. We handle the rest." (not "Music Business Operating System")
  → Chat widget: "Ask anything about your music career"
  → "Sound Familiar?" section with relatable pain points
  → "What We Do" section — 6 solutions in plain English
  → "Pick Your Stage" — 4 career stages with personalized paths
  → One CTA: "Start for free"
```

## Signup Flow Pattern (5-Step Onboarding Wizard)

The `signup.html` page is a 5-step immersive wizard that feeds into soul.md generation. `onboarding.html` redirects to `signup.html` (canonical URL).

**Step 1: Account** — Username, first name, last name, email, password. Google OAuth button (future Supabase). Divider with "or use email."

**Step 2: Artist Profile** — Artist/stage name, artist type (Solo/Producer/Band/Songwriter/DJ/Beatmaker/Composer/Other), primary genre (12 options), career stage (4 options), PRO status, LLC status.

**Step 3: Goals** — 10 checkbox goals (Register with PRO, Get on playlists, License music, Set up LLC, Copyright music, Handle taxes, Build brand, Find contacts, Learn business, All of above). Free-text notes field. Auto-generated soul.md preview that updates live as the user fills in details.

On submit: show success with "Your workspace is ready!" and link to the workspace dashboard.

## 7th Agent: ROSTR PAL Compiler

The ROSTR PAL Agent (`backend/app/agents/rostr_agent.py`) is the 7th agent in the system — it compiles raw onboarding data into structured output packages. Unlike the 6 specialist agents (PRO, Distribution, Licensing, Legal, Finance, Manager), the ROSTR agent doesn't chat — it runs the PAL pipeline:

```
EXTRACT → INJECT → ENHANCE → COMPILE → ROUTE
(intent)  (context) (expand)   (manifest) (assign agent)
```

**5 tools**: compile, generate_soul, generate_bio, generate_plan, generate_manifest

**Routing keywords**: "compile", "rostr", "pal", "manifest", "soul", "build package"

**What it produces**: soul.md, PAL-generated bio, 3-phase business plan, agent YAML manifests for all 6 specialists, skill packages based on goals

**Location**: `backend/app/agents/rostr_agent.py` — extends `BaseAgent`, registers with `registry.add(RostrAgent())`

The agent is called automatically during onboarding (`finishOnboarding()` in `signup.html`) and can be invoked anytime via chat: "Compile my profile", "Build my agent packages", "Generate my soul.md"

## Hermes Agent Provisioning (Production)

Per-user Hermes Agent instances on AWS EC2 — automated via Lambda + Terraform. Full provisioner at `backend/hermes_provisioner.py`.

**Flow**: Signup → `POST /provision-user` → Lambda launches EC2 → user-data script installs Hermes Agent from GitHub (`nousresearch/hermes-agent`) → downloads user's `soul.md` from S3 → starts as systemd service → returns endpoint `http://{ip}:8080`

**Terraform**: EC2 launch template (`t3.micro`, Ubuntu 24.04 AMI), security group (8080 + 22), IAM role with S3 access for user bucket, `aws_launch_template` resource.

**User-data script**: Installs Python venv, clones Hermes Agent, configures systemd unit with user-specific `HERMES_PROFILE` env var, starts service. Full script at `references/hermes-provisioning.md`.

**Cost**: ~$8.50/month per instance (t3.micro, 24/7). Can be started/stopped on-demand via Lambda to reduce costs.

## Resemble AI Voice Integration

TTS module at `backend/tts.py` — integrates Resemble AI's REST API for voiceover generation using Remy's voice (UUID: `31f74317`).

**Tool**: `generate_voiceover` on the Manager Agent (tool #7, total now 38 tools across 7 agents)

**Flow**: User asks "Generate a voiceover for my EPK intro" → calls `POST p.cluster.resemble.ai/synthesize` with voice UUID + text → downloads audio from Resemble S3 → re-uploads to `s3://artispreneur-outputs/voiceovers/remy/` → returns 24hr pre-signed URL

## Skill Builder + PDF Generation

The `skills.html` page allows artists to create custom agent skills and generate downloadable PDFs — all client-side, no backend needed.

### Skill Creation
- Name, description, category selector
- Tool picker (8 chips: Bio Generator, Link Scraper, EPK Builder, Splitsheet, Contract, Metadata, Revenue, Playlist Finder)
- On build: generates YAML manifest preview, saves to localStorage as `artispreneur_skills`

### PDF Generation (jsPDF)
Four document types generate instantly in-browser:
- **EPK** — Electronic Press Kit with bio, genre, location, links, press
- **Splitsheet** — Track ownership percentages and collaborator details
- **Producer Agreement** — Standard production contract template
- **Release Plan** — 8-week timeline with milestones

Pattern: `const { jsPDF } = window.jspdf; const doc = new jsPDF(); doc.setFont(...); doc.save(filename);`

### Webhook (Backend PDF)
For complex PDFs requiring server-side generation: `POST /v1/skills/generate` → Lambda handler at `backend/skills_webhook.py` → generates PDF via reportlab → saves to S3 → returns pre-signed URL. The webhook endpoint and payload are displayed on the skills page for integration.

The soul.md template:
```
# Artist: {artistName}
# Type: {artistType}
# Genre: {genre}
# Stage: {stage}
# PRO: {proStatus}
# Business: {hasLLC}
# Goals:
# - {goal1}
# - {goal2}
# Notes:
# {notes}
```

## Onboarding Wizard + PAL Bio Pipeline (v2.3)

The `onboarding.html` page is a 5-step immersive wizard that feeds into automated profile generation:

**Step 1 — Who Are You?**: Real name, artist/stage name, hometown, current city, years in music, primary genre (12 options)
**Step 2 — Your Story**: Why music, biggest influences, personal story (3-5 sentences), message/theme
**Step 3 — Current Situation**: Employment status (6 options), monthly budget (5 tiers), living situation, gear/setup
**Step 4 — Experience**: Performance history (9 chip options), show count estimate, press/features/notable moments
**Step 5 — Goals + Links**: 10 goal chips (PRO, playlists, licensing, LLC, brand, shows, press, deals, taxes, releases), 6 music link fields (Spotify, Apple Music, SoundCloud, YouTube, Instagram, Press + custom), profile photo upload

**Design**: Card-based with progress bar (5 segments, green=done, gold=active). Each step has an emoji, title, subtitle, and form fields styled with dark input boxes (`background:var(--card);border:1px solid var(--border)`). Chip groups for multi-select with toggle behavior.

**On submit**: Hides all steps, builds summary with:
- Stats row (links scraped, goals count, monthly listeners)
- soul.md preview (monospace card with full profile dump)
- PAL-generated bio (formatted card with gold heading)

The wizard saves profile data to `localStorage` as `artispreneur_profile` so the `/profile.html` page can display it without a backend.

### PAL Bio Generator

The bio generator uses tiered templates based on years in music:
- **Emerging** (<3 years): "{name} is an emerging {genre} artist {location}making waves..."
- **Established** (3-5 years): "{name} is a {genre} artist {location}with {years} of experience..."
- **Veteran** (5+ years): "With {years} in the game, {name} has established themselves as a force in {genre}..."

Each template incorporates story excerpts, influences (first 3), genre-appropriate adjectives (raw/soulful/immersive/powerful etc.), experience highlights, and goals. The production version lives at `backend/onboarding.py` as `PALBioGenerator` class.

### Link Scraper

`LinkScraper` class in `backend/onboarding.py` — regex-based extraction of platform IDs from URLs:
- Spotify: `spotify\.com/artist/(\w+)`
- YouTube: `youtube\.com/(@|channel/)([\w-]+)`
- Instagram: `instagram\.com/([\w.]+)`

In production, extends to call platform APIs for follower counts, track data, and monthly listeners. In demo mode, generates simulated stats.

### S3 Provisioning

`S3Provisioner` class creates per-user bucket structure:
```
s3://artispreneur-outputs/users/{username}/
├── .rostr/state/
├── outputs/contracts/
├── outputs/epks/
├── outputs/analysis/
├── catalog/
└── profile/
```

Triggered on onboarding completion — creates empty folder objects to establish the structure.

### Full Pipeline (`process_onboarding`)

1. Parse onboarding data → `ArtistProfile` dataclass
2. Provision S3 bucket structure
3. Scrape music/press links
4. Build knowledge base (soul.md + profile.json)
5. Generate PAL bio
6. Save everything to S3
7. Return summary with S3 path

### Auto-Generated Profile Page

`/profile.html` reads `localStorage.getItem('artispreneur_profile')` and displays:
- Profile avatar (first letter of artist name), name, location
- Stats row (years, shows, goals count)
- PAL-generated bio section with formatted text
- Goals and Experience as tag grids
- Platform links as styled cards with icons
- Soul.md as monospace code block
- CTA to complete onboarding if no data exists

### Curriculum Instructor Agent (`build_all_courses.py`)

Reads the Academy spreadsheet (`.xlsx` with 16 course sheets) and generates course HTML pages. Also, the newer **course extraction pipeline** at `references/course-extraction-recipe.md` extracts 19 courses (300+ lessons) from `courses-data.js` and generates `lib/courses.ts` for Next.js.

```bash
# Run when new courses are added to the spreadsheet:
/tmp/venv/bin/python3 build_all_courses.py
```

Output: `courses/{slug}.html` with styled module cards showing module number, title, chapter context, and full educational content.

### Directory Ingestion Agent (`build_directory.py` + node extraction)

Parses `directory-data.ts` (TypeScript with DirectoryCategory/DirectorySection/DirectoryEntry interfaces) and extracts contacts into `directory-data.js` as `const DIRECTORY_DATA = [...]`. The node script uses regex to extract entry objects, matches them to sections by position in source, and writes the JS file. The HTML directory page loads this data and renders with client-side search, category filters, and pagination (20 per page).

```bash
node << 'NODEEOF'
# Extract entries, sections, categories from directory-data.ts
# Write directory-data.js
NODEEOF
```

### Re-Deploy After Data Changes

After running either ingestion agent, re-deploy the static site:
```bash
cd /tmp/artispreneur-landing
git add -A && git commit -m "..." && git push origin main
vercel --prod --yes
# Confirm with user: "Deployed: https://artispreneur-landing-XXXXX.vercel.app"
```

```ts
export interface Course {
  id: string; title: string; slug: string; modules: Module[]
  category: string; description: string
}
export interface Module {
  id: string; number: string; videoUrl: string; videoId: string
  title: string; chapterTitle: string; content: string; duration: string
}
```

YouTube videos use `https://www.youtube.com/watch?v=<VIDEO_ID>` format. The `VideoPlayer` component auto-detects YouTube vs HeyGen by checking if `videoId` matches `/^[a-zA-Z0-9_-]{11}$/` (YouTube) — otherwise routes to HeyGen embed.

When adding courses from a CSV, group by `search_query` tag into logical course buckets. Use `re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')` for slug generation.

## AI Chat Component

For interactive AI agent interfaces within Artispreneur projects, use `ArtispreneurChat` (template at `templates/artispreneur-chat.tsx`). It blends the Artispreneur dark luxury design DNA with 21st.dev/shadcn tool-UI patterns.

**Features**: Agent selector (Creative/Builder/Researcher/Curator with color-coded icons), model selector, message bubbles with markdown, streaming indicator, copy-to-clipboard, auto-resizing input, welcome screen with agent picker grid.

**Design**: Dark background `oklch(0.08 0.005 250)`, gold accent `oklch(0.72 0.19 85)`, 13px body text, 8px radius, subtle borders. Agent colors map to the category palette from the directory pattern. Zero glassmorphism on the chat itself — clean 21st.dev flatness for the tool surface.

**Integration**: Drop into any Artispreneur Next.js project. Requires `lucide-react` (already in ecosystem deps). Pass `onSend` to connect a real AI backend; built-in simulated responses per agent for demo mode.

**Page setup** (`app/ai/page.tsx`):
```tsx
"use client";
import { ArtispreneurChat } from "@/components/ui/artispreneur-chat";

export default function AIChatPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-background p-4">
      <div className="h-[calc(100vh-6rem)] w-full max-w-3xl">
        <ArtispreneurChat />
      </div>
    </main>
  );
}
```

## Video Creation with HyperFrames (HeyGen)

When the user asks to create an Artispreneur-branded **animated video, course video, educational video, or lyric video**, use **HyperFrames by HeyGen** — NOT Remotion, NOT Manim. HyperFrames is HeyGen's HTML-based video composition framework: single `index.html` + GSAP timeline + `data-*` attributes, rendered through headless Chrome.

**Routing rule:** "hyperframes" always means HeyGen HyperFrames CLI, not a generic concept. If the user says "hyperframes" and you don't know what it is, check `which hyperframes` — it's likely installed. If not, `npm install -g hyperframes@latest`.

### Quick Start

```bash
hyperframes init my-video --non-interactive
cd my-video
npm run dev          # hot-reload preview (background it!)
npm run check        # lint + validate + inspect
npm run render       # → MP4
```

### Architecture

- **`index.html`** — single composition with `data-composition-id`, `data-start`, `data-duration`, `data-width`, `data-height` on the root div
- **`meta.json`** — `{id, name, createdAt}`
- **`hyperframes.json`** — registry config
- **`compositions/`** — sub-compositions (optional, via `data-composition-src`)
- **`assets/`** — audio, images, data files

### Key Rules

1. Every timed element needs `data-start`, `data-duration`, `data-track-index`
2. Visible timed elements MUST have `class="clip"` — the framework manages visibility
3. GSAP timelines must be paused and registered on `window.__timelines`:
   ```js
   window.__timelines = window.__timelines || {};
   window.__timelines["main"] = gsap.timeline({ paused: true });
   ```
4. Only deterministic logic — no `Date.now()`, `Math.random()`, or network fetches
5. GSAP is loaded via CDN: `<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>`

### Artispreneur Design DNA (HyperFrames flavor)

Apply these in the `<style>` block of the HyperFrames HTML:

| Token | Value |
|---|---|
| Background | `#09090b` |
| Gold accent | `#c9a227` |
| White text | `#fafafa` |
| Muted text | `rgba(250,250,250,0.5)` |
| Font sans | `'Inter', 'Helvetica Neue', 'Arial'` via `@font-face { font-family: 'Sans'; src: local('Inter'), ... }` |
| Font serif | `'Playfair Display', 'Georgia'` via `@font-face { font-family: 'Serif'; ... }` |
| Dimensions | `width: 1920px; height: 1080px` |

**Background effects**: Radial gold glow with sine-wave opacity pulse, corner accent marks (`50x1px` and `1x50px` gold lines), bottom gold hairline gradient.

### Programmatic Slide Generation (proven pattern)

For course/educational videos with many modules, generate DOM elements + GSAP timelines programmatically rather than hand-writing each slide. Full template at `references/hyperframes-template.html`.

Pattern:
```js
modules.forEach(function(m, i) {
  var wrap = el("div", "mod-wrap clip", {
    "data-start": cursor, "data-duration": MOD_DUR, "data-track-index": 60 + i
  }, root);
  // ... build badge, title, line, bullets, footer, counter ...
  // GSAP staggered entrance:
  tl.from(badge, {opacity:0, x:-25, duration:0.4, ease:"power2.out"}, cursor);
  tl.from(title, {opacity:0, y:18, duration:0.45, ease:"power2.out"}, cursor + 0.12);
  bullets.forEach(function(b, bi) {
    tl.from(b, {opacity:0, x:-18, duration:0.35, ease:"power2.out"}, cursor + 0.5 + bi * 0.22);
  });
  tl.to(wrap, {opacity:0, duration:0.3, ease:"power2.in"}, cursor + MOD_DUR - 0.3);
  cursor += MOD_DUR;
});
```

### Timing Budget (4-minute educational video)

| Segment | Duration |
|---|---|
| Title card | 5s |
| Chapter divider (each) | 2.5s |
| Module slide (each) | 8.5s |
| Outro card | 6.5s |

For N modules across C chapters: `total = 5 + C*2.5 + N*8.5 + 6.5` seconds.

### Verification (MANDATORY — same standard as site deploys)

After building, always run the full check before claiming done:
```bash
npm run check  # = hyperframes lint && hyperframes validate && hyperframes inspect
```
All three must pass: 0 lint errors, no console errors in headless Chrome, 0 layout issues across timeline samples.

### Pitfalls

- **Wrong tool routing**: When the user says "hyperframes" or "video", reach for HyperFrames first, not Remotion/Manim. Remotion is for React-based video (needs Node.js build), Manim is for mathematical animations (3Blue1Brown style). HyperFrames is for HTML+GSAP marketing/educational videos.
- **Disk space**: HyperFrames rendering uses headless Chrome which needs ~500MB+ temp space. If ENOSPC, clear `~/Library/Caches/com.openai.codex` and `npm cache clean --force`.
- **`npm run dev` is long-running**: Always run it with `background=true` or it will time out and die.
- **Sub-composition variables**: `data-composition-variables` on `<html>` defines the schema; `data-variable-values` on the host element provides per-instance overrides. Use `window.__hyperframes.getVariables()` to read them.

## Shared Assets

- Logo: `public/images/artispreneur-20logo.png` (32x32 rounded)
- Course category images live in `public/` — dark moody photography
- `ArtispreneurChat` component template: `templates/artispreneur-chat.tsx`
- HyperFrames composition template: `references/hyperframes-template.html`

## Directory Data Pattern\n\nDirectory sites use a typed data file at `lib/directory.ts`:\n\n```ts\nexport interface DirectoryCategory {\n  id: string; title: string; slug: string; description: string\n  icon: string; count: number; sections: DirectorySection[]\n}\nexport interface DirectorySection {\n  title: string; slug: string; description: string\n  entries: DirectoryEntry[]\n}\nexport interface DirectoryEntry {\n  name: string; location?: string; url?: string; email?: string\n  phone?: string; notes?: string; tags?: string[]; genre?: string\n}\n```\n\n**Category colors** for color-coded icons on the homepage grid:\n```ts\nconst categoryColors: Record<string, string> = {\n  venues: \"oklch(0.75 0.15 25)\",      // warm red\n  radio: \"oklch(0.65 0.15 200)\",       // blue\n  blogs: \"oklch(0.7 0.15 300)\",        // purple\n  press: \"oklch(0.65 0.15 150)\",       // green\n  podcasts: \"oklch(0.75 0.12 85)\",     // gold variant\n  community: \"oklch(0.6 0.15 180)\",    // teal\n}\n```\n\n**Search**: Make a client component at `app/search/page.tsx` that imports `searchDirectory()` from the data file. Use `\"use client\"` with `useState` for query/result state. The search function does case-insensitive matching across name, location, tags, and notes.\n\n**Category detail pages**: Dynamic route at `app/category/[slug]/page.tsx` with `params: Promise<{ slug: string }>`. Use `getCategoryBySlug(slug)` — return `notFound()` if undefined. Render each section with its entries as cards with hover-reveal visit buttons.\n\n## Sidebar Navigation (CRITICAL)

Workspace sidebar items MUST use `window.location.href='...'` for page navigation, NOT `switchView()`. The `switchView()` function toggles in-page `<div>` visibility — it only works for in-page tabs (chat, agents, outputs, prompts, knowledge). Academy, Directory, Profile, and Skill Builder are separate pages and need real navigation.

```html
<!-- CORRECT — Academy/Directory are separate pages -->
<button class="nav-item" onclick="window.location.href='academy.html'">🎓 Academy</button>
<button class="nav-item" onclick="window.location.href='directory.html'">◉ Directory</button>

<!-- WRONG — this does nothing (no view-academy div exists) -->
<button class="nav-item" onclick="switchView('academy')">🎓 Academy</button>
```

Fix applies to any sidebar link that points to a separate `.html` file. In-page tabs (Chat, Agents, Outputs, Prompts, Knowledge) keep `switchView()`. External pages (Academy, Directory, Profile, Skill Builder) use `window.location.href`.

## Onboarding → Workspace Data Flow

The onboarding wizard saves ALL data to `localStorage` as `artispreneur_profile`. The workspace reads it on init and replaces the hardcoded "Midnight" demo data with the real artist profile.

**Onboarding (`signup.html` — `finishOnboarding()`):**
```js
const profile = {
  first_name: getVal('firstName'), last_name: getVal('lastName'),
  stage_name: getVal('artistName') || getVal('firstName'),
  hometown: ..., genre: ..., why_music: ..., story: ..., message: ...,
  experience: getSelected('experienceChips'), goals: getSelected('goalChips'),
  links: scrapeLinks(), bio: generateBio(), soul: generateSoul(),
  created_at: new Date().toISOString(),
};
localStorage.setItem('artispreneur_profile', JSON.stringify(profile));
localStorage.setItem('artispreneur_logged_in', 'true');
```

**Workspace (`workspace.html` — init):**
```js
(function initProfile() {
  const p = JSON.parse(localStorage.getItem('artispreneur_profile') || 'null');
  if (!p) return;
  const name = p.stage_name || p.first_name || 'Artist';
  document.getElementById('sidebarAvatar').textContent = name[0];
  document.getElementById('sidebarName').textContent = name;
  document.getElementById('chatEmpty').innerHTML = `<h2>Welcome, ${name}</h2>...`;
})();
```

**Login (`login.html` — `doLogin()`):**
```js
const profile = JSON.parse(localStorage.getItem('artispreneur_profile') || 'null');
if (!profile || password.length < 8) {
  err.textContent = 'No account found. Please sign up first.';
  return;
}
localStorage.setItem('artispreneur_logged_in', 'true');
window.location.href = 'workspace.html';
```

Without this flow, the workspace shows hardcoded "Midnight" and the login accepts any 8-character password. This is the #1 thing that makes the product feel fake. Full pattern at `references/onboarding-data-flow.md`.

## AI-Quality Bio Generation

Use genre-specific headline hooks + natural paragraphs instead of a single template string:

```js
const hooks = {
  'R&B/Soul': `${name}'s voice doesn't ask for attention. It commands it.`,
  'Hip-Hop/Rap': `${first} doesn't just make music — ${first} builds worlds.`,
  // ... 11 genre-specific hooks
};
parts.push(hooks[genre] || hooks['Other']);

// Natural paragraphs: identity → story → influences → experience → goals → CTA
if (influences) {
  const il = influences.split(/[,\n]/).map(s=>s.trim()).filter(s=>s.length>1).slice(0,5);
  const verbs = ['drawing from','shaped by','moving between','channeling','blending'];
  parts.push(`${first}'s sound is ${verbs[il.length%verbs.length]} ${ilStr}...`);
}
```

The old pattern was a single template string: `**${name}** is an ${genre} artist from ${hometown}...` — this produces robotic, same-sounding bios for every artist. The new pattern uses genre-specific hooks, weaves actual influence names naturally, and reads like something a music journalist would write. Full pattern at `references/bio-generation.md`.

## Pitfalls

- **Sidebar links broken**: If sidebar items don't navigate, check whether they use `switchView()` for external pages. Academy/Directory/Profile/Skill Builder must use `window.location.href`. This is the #1 sidebar bug.
- **Onboarding data lost**: If the workspace shows "Midnight" instead of the user's name, the onboarding `finishOnboarding()` function isn't saving to `localStorage.setItem('artispreneur_profile', ...)`. Check both the save side (signup.html) and the read side (workspace.html init).
- **Login accepts anything**: If login lets any password through, `doLogin()` isn't checking `localStorage.getItem('artispreneur_profile')`. The fix: check for stored profile before accepting credentials.
- **iCloud Desktop stubs**: Files in `~/Desktop/` are iCloud-synced and frequently become 0-byte placeholders. Verify with `cat file | head` before trusting. Prefer GitHub clones and `/tmp/` for build work. If a Desktop repo "disappears," it was evicted.
- **Master Knowledge Base**: The canonical source of truth is `~/Desktop/Master Artispreneur/knowledge-base/` containing `MASTER.md` (ecosystem blueprint), academy source clone, directory data, course CSV, and branding assets. When in doubt about the current state, check `MASTER.md` first.
- **Do NOT copy components/header.tsx from academy** — it imports `@/lib/supabase/client` which will break builds on sites without Supabase. Build inline headers instead.
- **Lucide icons reject `style` prop** in Next.js 16 + Turbopack. Wrap in `<div style={{ color }}><Icon /></div>` instead.
- **ENOSPC on macOS (disk full during npm install/build)**: This is the #1 deployment blocker. When `npm install` or `next build` fails with "No space left on device", clear caches in this order: (1) `npm cache clean --force && rm -rf ~/.npm/_cacache` (frees 100-500MB), (2) `rm -rf ~/Library/Caches/com.openai.codex ~/Library/Caches/com.openai.atlas` (can be 10GB+), (3) `rm -rf ~/Library/Caches/SiriTTS ~/Library/Caches/Homebrew ~/Library/Caches/electron ~/Library/Caches/pip ~/Library/Caches/node-gyp ~/Library/Caches/go-build ~/Library/Caches/ms-playwright-go` (500MB-2GB), (4) `rm -rf /tmp/other-projects` (old clones), (5) check `du -sh ~/Library/Caches/*/ | sort -rh | head -10` for any remaining large caches. After clearing, verify with `df -h / | tail -1`. Target: at least 1.5GB free for a typical Next.js 16 install + build. If still too tight after all clears, push to GitHub and let Vercel build server-side — verify the deployed URLs with curl instead.
- **Vercel GitHub linking errors** (400) are non-blocking — the deploy proceeds fine without the GitHub connection.
- **Vercel CLI version sensitivity**: Node v25 requires `vercel@56.1.0` or later. Older versions (41.x, 47.x) fail with "Invalid Version" or "endpoint requires version 47.2.2" errors. Install globally: `npm install -g vercel@latest`. Use `vercel` directly (not `npx vercel`) after installing globally.
- **Vercel build hangs on "Building…"**: The CLI may appear stuck but the build often completes on Vercel's side. If the CLI sits on "Building…" for >3 minutes, kill the process and curl the deployment URL directly — it may already be live. The preview URL (hash-based) works first, then the alias propagates.
- **Vercel project name collisions**: If a subagent deploys to an existing Vercel project with the same name, it picks up whatever was there before. ALWAYS verify post-deploy content with: `curl -s <url> | grep -o '<title>[^<]*</title>'`. If the title is wrong, the project name collided — deploy under a different name.
- **Subagent deploy verification**: Never trust a subagent's deploy claim without independent verification. Subagents may report success while deploying to a wrong/collided Vercel project. After any delegated deploy, curl every route yourself and confirm both HTTP 200 AND correct content titles.
- **Vercel SSO protection on new projects**: New Vercel projects have Deployment Protection (SSO) enabled by default. Hash URLs and `.vercel.app` aliases return HTTP 302 to `vercel.com/sso-api?...` — the build is fine but public access is blocked. Disable immediately after first deploy: `vercel project protection disable <project> --sso --scope artispreneur`. Custom domains bypass SSO even when enabled.
- **Vercel project rate-limiting**: Too many rapid `vercel --prod` deploys (~5+ in <10 min) rate-limits the project. New deploys show `readyState: "BLOCKED"` and fail silently. Workaround: deploy to a fresh project (copy source to new dir, strip `.vercel/`, deploy). The original project recovers after ~30 min. Prefer `--no-wait` for rapid iteration to avoid hanging on blocked builds.
- **Vercel build stuck in UNKNOWN/queued state**: After `vercel --prod`, the CLI prints the hash URL but the build never starts (status UNKNOWN, 0ms build time, `curl` returns "Deployment is building" indefinitely). This is a server-side queue stall — Vercel accepted the deploy but hasn't allocated a builder. Check with `vercel inspect <hash-url> --scope artispreneur | grep status`. If status is UNKNOWN for >5 min, the build is stalled. Fix: wait 10 min (it may auto-recover), or deploy to a fresh project name via `vercel link --project <new-name>` then `vercel --prod`. Do NOT keep re-deploying to the same stalled project — it compounds the queue.
- **Supabase import cleanup**: The academy template has `@/lib/supabase/` imports in many files (auth pages, certificates, dashboard, verify, proxy middleware). After stripping academy pages, ALSO run `grep -rn "supabase" app/ lib/ components/` and delete any remaining files that import supabase — they will fail at build time.
- **Node.js DNS resolution failure in Hermes runtime (ENOTFOUND on npm/pnpm/git)**: Node.js processes in the Hermes runtime can fail DNS resolution even when `curl` and `nslookup` work. This blocks `npm install`, `pnpm install`, `git push`, and `vercel` CLI. Verify with `npm ping` — if it times out, Node.js DNS is down. No reliable workaround — wait for recovery or push from outside the session.
- **Middleware crash on missing env vars**: When the Next.js middleware uses `createServerClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, ...)` with non-null assertions (`!`), deploying without those env vars set causes `MIDDLEWARE_INVOCATION_FAILED` (HTTP 500 on all routes). Fix: guard against missing env vars — if `!supabaseUrl || !supabaseAnonKey`, skip Supabase init and allow public routes through. See `references/middleware-env-guard.md`.
- **Next.js 16 duplicate JSX props**: `style={fadeIn} className="..." style={{...}}` on the same element passes webpack but fails TypeScript (`JSX elements cannot have multiple attributes with the same name`). Combine into one `style={{ ...fadeInStyles, ...otherStyles }}` or use `animation` CSS property in the single style object.
- **Auth migration (Supabase/Cosmos → localStorage)**: When converting a backend-heavy Next.js app to a frontend-only Artispreneur site, three type hazards recur: (a) `AuthUser` interfaces from different modules diverge — add `"local"` to `AuthProvider` union type, (b) `proxy.ts` imports `hasSupabaseSessionCookie` — add a stub returning `false`, (c) profile type guards need optional chaining for fields like `artistType`. Full migration recipe at `references/auth-migration-localstorage.md`.
