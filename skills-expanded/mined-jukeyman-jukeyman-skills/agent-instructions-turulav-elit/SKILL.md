---
name: agent-instructions--turulav--elit
description: # 🔥 AGENT INSTRUCTIONS — TURULAV → ELIT
---

# # 🔥 AGENT INSTRUCTIONS — TURULAV → ELIT

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **# 🔥 AGENT INSTRUCTIONS — TURULAV → ELIT**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/images may26/images/personal/practice/TuruLav Main File/TuruLav Documentation/# 🔥 AGENT INSTRUCTIONS — TURULAV → ELIT.md`

## 🧠 Master Agent Prompt & Capabilities

---
trigger: always_on
---

# 🔥 AGENT INSTRUCTIONS — TURULAV → ELITE WHITE-LABEL ENGINE
**Base Template: TuruLav by LabArtisan | RJ Business Solutions | 2026-02-22**

---

## 🎯 MISSION

You are scanning, enhancing, and converting the **TuruLav React dating template** (LabArtisan) into a production-grade, white-label, multi-niche community platform. TuruLav is your UI foundation — its existing screens, components, routing, and JSON data system are your starting point. You do NOT rebuild from scratch. You scan every file, upgrade every layer, wire every feature end-to-end, and make the entire thing switchable to any niche via one config file. No placeholders. No MVPs. Full production output only.

---

## 📋 PHASE 1 — FULL TEMPLATE SCAN

**Scanner Agent: execute this on the TuruLav `/buyer-file` directory first.**

Scan and inventory every file in the project. Produce `scan-output/inventory.json` with the following structure:

```json
{
  "pages": [],        
  "components": [],   
  "jsonDataFiles": [], 
  "colorTokens": {},  
  "fontImports": [],  
  "hardcodedStrings": [],
  "routeMap": {},     
  "dependencyList": [],
  "missingFeatures": [],
  "brandingTargets": []
}
```

**What to flag as `brandingTargets`:** Any hardcoded color hex, any logo `src` path, any app name string like "TuruLav", any copyright text, any JSON file containing profile/member data, any Google Font import URL, any title tag content, and any map embed coordinates.

**What to flag as `missingFeatures`:** Real-time chat (TuruLav uses static UI only), swipe physics (TuruLav has no drag gestures), match animation, Stripe payments, auth system, backend API connections, AI matching, push notifications, admin dashboard, profile photo upload, and geolocation filtering.

---

## 📋 PHASE 2 — INFRASTRUCTURE UPGRADES

After scan, Upgrade Agent executes these in order. Do not skip any.

**2A. Upgrade React version**
TuruLav ships on an older CRA (Create React App) setup. Migrate to **Next.js 15 App Router**. Preserve all existing page routes and component names. Map CRA routes to Next.js `app/` directory. Keep all existing component logic intact — only change the routing layer and build system.

**2B. Add Framer Motion to every existing component**
TuruLav has no animations. Add Framer Motion to every component without breaking existing layout:
- All page transitions: `initial opacity 0 y 20` → `animate opacity 1 y 0`, duration 0.4s
- All cards: `whileHover scale 1.02`, `whileTap scale 0.98`
- Profile photo gallery: crossfade on photo change
- Any list/grid items: staggered children, delay 0.05s per item
- Sidebar/drawer: slide in from left, spring config stiffness 300 damping 30
- Modals: scale from 0.9 + fade, spring physics

**2C. Replace JSON data system with live API layer**
TuruLav uses static JSON files for member data, profiles, and content. Keep the JSON file structure as the **mock/seed data format** but add a data layer that fetches from the real backend when `NEXT_PUBLIC_API_URL` is set. When env var is absent, fall back to local JSON. This means zero breaking changes during development but instant live-data capability when backend is connected.

```typescript
// lib/data-layer.ts
export async function fetchProfiles(filters?: ProfileFilters) {
  if (process.env.NEXT_PUBLIC_API_URL) {
    return await fetch(`${process.env.NEXT_PUBLIC_API_URL}/profiles/discover`)
      .then(r => r.json())
  }
  // fallback to local JSON
  return await import('../data/members.json').then(m => m.default)
}
```

**2D. Upgrade font system**
TuruLav uses Jost + Roboto via Google Fonts CSS import. Replace with Next.js `next/font/google` for zero CLS and self-hosting. Make font family a brand token so the Branding Agent can swap it per niche.

```typescript
// lib/fonts.ts — generated per niche by Branding Agent
import { Jost, Roboto } from 'next/font/google'
export const heading = Jost({ subsets: ['latin'], variable: '--font-heading' })
export const body    = Roboto({ weight: ['300','400','500','700'], subsets: ['latin'], variable: '--font-body' })
```

**2E. Add CSS variable token layer over existing styles**
TuruLav's `style.css` has hardcoded colors. Do not rewrite the CSS. Instead, prepend a `:root {}` block at the top of `globals.css` with all brand tokens as CSS variables, then do a find-replace pass converting every hardcoded color to its corresponding variable. This preserves all existing layout/spacing while making colors fully overridable.

---

## 📋 PHASE 3 — NEW FEATURES TO BUILD ON TOP OF TURULAV

These are features TuruLav does NOT have. Build them as new components/routes that slot into the existing structure.

**3A. Swipe Deck (Core Tinder Mechanic)**
TuruLav has a member browse grid. ADD a `/discover` route with full swipe deck on top of it. User can toggle between swipe mode and grid mode. Swipe deck behavior:

- `useMotionValue` x and y tracking
- `useTransform` rotate: x `[-300,300]` maps to `[-30deg,30deg]`
- `useTransform` opacity: x `[-300,-100,0,100,300]` maps to `[0,1,1,1,0]`
- Spring: stiffness 300, damping 30
- Swipe threshold: `Math.abs(offset.x) > 120` OR `Math.abs(velocity.x) > 500`
- Superlike threshold: `offset.y < -120`
- LIKE stamp top-left, green, opacity tied to rightward drag
- NOPE stamp top-right, red, opacity tied to leftward drag
- SUPER stamp top-center, blue, opacity tied to upward drag
- Card stack: render top 3 cards, z-indexed, cards 2+3 scaled 0.95/0.90
- After swipe, call `POST /profiles/swipe` with `{swiped_id, action}`
- If response returns `{match: true}`, fire Match Modal

**3B. Match Modal**
Does not exist in TuruLav. Build as global overlay component mounted in root layout:

- Triggered by Zustand `matchStore.setMatch(profile)`
- Full screen dark overlay, `backdrop-blur-sm`
- Both profile photos side by side with animated ring pulse using brand accent color
- "It's a Match!" headline in brand gradient
- Confetti burst (use `canvas-confetti` package)
- Two buttons: "Send Message" → routes to chat, "Keep Swiping" → dismisses
- Auto-dismiss after 8 seconds if no action
- Framer Motion: overlay fades in, content scales from 0.5 with spring

**3C. Real-Time Chat**
TuruLav has a static chat UI layout. Wire it to Supabase Realtime:

- Supabase channel subscription: `conversations:${conversationId}`
- Optimistic message insert before server confirmation
- Message types: text, image, gif
- Typing indicator via Supabase broadcast channel, debounced 500ms
- Read receipts: update `read_at` when message scrolls into viewport
- Auto-scroll to bottom on new message
- Media upload button → Cloudinary direct upload → insert media message
- Empty state: show 3 icebreaker prompt buttons populated from niche config

**3D. Premium / Paywall Screen**
TuruLav has no payments. Add `/premium` route:

- 3-column pricing cards (Free, Gold, Platinum) — pricing from niche config JSON
- "Most Popular" badge on Gold tier
- Feature comparison checklist per tier
- Stripe Checkout button calls `POST /payments/checkout`
- After successful payment, Supabase subscription record updated via webhook
- Locked features show a gold lock icon overlay — clicking routes to `/premium`
- Boost purchase: modal with pack options, one-time Stripe payment intent

**3E. Admin Dashboard**
TuruLav has no admin. Add `/(admin)` route group, protected by role check:

- `/admin/users` — searchable table, status toggle (active/suspended), view profile
- `/admin/moderation` — reported content queue, approve/remove actions
- `/admin/analytics` — charts: signups over time, DAU, match rate, revenue
- `/admin/branding` — live editor: change app name, colors, logo URL, preview in real time, export updated niche config JSON

**3F. Onboarding Wizard**
TuruLav has a basic signup. Replace with 4-step wizard:

- Step 1: Upload photos (drag-reorder, min 1 required, Cloudinary upload)
- Step 2: Bio + prompts (3 prompts from niche config question bank, 150 char each)
- Step 3: Preferences (age range slider, distance slider, gender/orientation, niche-specific fields)
- Step 4: Phone verification via Twilio OTP
- Progress bar at top showing current step
- Back/forward navigation, validation before advancing
- Profile completion score calculated and stored on submit

---

## 📋 PHASE 4 — BRANDING AGENT INSTRUCTIONS

The Branding Agent runs after every phase and whenever a new niche config is loaded. It reads `.config/niches/{NICHE_ID}.json` and writes the following files. It touches nothing else.

**Files written by Branding Agent:**

```
frontend/styles/brand-tokens.css   ← all CSS variables
frontend/lib/brand.ts              ← typed brand constants
frontend/lib/features.ts           ← feature flag booleans
frontend/lib/copy.ts               ← all user-facing strings
frontend/lib/fonts.ts              ← next/font imports
frontend/tailwind.config.ts        ← colors, fonts, animations
.env.example                       ← env vars with app name populated
public/manifest.json               ← PWA manifest with app name + colors
README.md                          ← branded readme with RJ Business logo
```

**CSS token set written to `brand-tokens.css`:**

```css
:root {
  --color-primary:      {primaryColor};
  --color-secondary:    {secondaryColor};
  --color-accent:       {accentColor};
  --color-bg:           {backgroundColor};
  --color-surface:      {surfaceColor};
  --color-text:         {textColor};
  --color-text-muted:   {mutedColor};
  --gradient-brand:     {gradient};
  --gradient-card:      linear-gradient(180deg,transparent 50%,{backgroundColor}ee 100%);
  --font-heading:       '{fontHeading}', sans-serif;
  --font-body:          '{fontBody}', sans-serif;
  --radius:             {borderRadius};
  --shadow-card:        {shadowStyle};
  --color-like:         #22c55e;
  --color-pass:         #ef4444;
  --color-superlike:    #3b82f6;
  --color-match:        {accentColor};
}
```

**Rule:** `--color-like`, `--color-pass`, `--color-superlike` are NEVER overridden by niche config. These are universal swipe action colors that users recognize. All other tokens are fully niche-controlled.

---

## 📋 PHASE 5 — NICHE CONFIG FORMAT

Every niche is one JSON file. Branding Agent reads this. Nothing else drives the white-label system.

```json
{
  "id":          "niche-id",
  "name":        "App Name",
  "tagline":     "One line value prop",
  "audience":    "Who this is for",
  "branding": {
    "appName":          "App Name",
    "logo":             "https://cdn.com/logo.svg",
    "favicon":          "/favicon.ico",
    "primaryColor":     "#HEX",
    "secondaryColor":   "#HEX",
    "accentColor":      "#HEX",
    "backgroundColor":  "#HEX",
    "surfaceColor":     "#HEX",
    "textColor":        "#HEX",
    "mutedColor":       "#HEX",
    "gradient":         "linear-gradient(...)",
    "fontHeading":      "Google Font Name",
    "fontBody":         "Google Font Name",
    "borderRadius":     "1rem",
    "shadowStyle":      "0 20px 40px rgba(0,0,0,0.3)"
  },
  "features": {
    "swipeEnabled":       true,
    "gridBrowse":         true,
    "videoProfiles":      false,
    "voiceMessages":      false,
    "communityFeed":      true,
    "events":             true,
    "groups":             false,
    "forums":             false,
    "aiMatchmaking":      true,
    "incognitoMode":      false,
    "boostProfile":       true,
    "superLike":          true,
    "rewind":             false,
    "nicheField1":        false,
    "nicheField2":        false
  },
  "content": {
    "heroHeadline":       "Your headline here",
    "heroSubline":        "Your subline here",
    "onboardingQuestions": [],
    "matchPrompts":        [],
    "icebreakerSuggestions": [],
    "emptyStateMessages": {
      "noMatches":   "",
      "noMessages":  "",
      "noEvents":    ""
    },
    "notificationCopy": {
      "newMatch":    "🔥 You matched with {{name}}!",
      "newMessage":  "💬 {{name}} sent you a message",
      "profileLike": "❤️ Someone liked your profile!"
    }
  },
  "monetization": {
    "currency":   "USD",
    "freeTier":   { "dailyLikes": 20, "superlikesPerWeek": 3 },
    "premiumTiers": [
      {
        "name":            "Gold",
        "price":           29.99,
        "period":          "month",
        "stripeProductId": "",
        "features":        []
      },
      {
        "name":            "Platinum",
        "price":           49.99,
        "period":          "month",
        "stripeProductId": "",
        "features":        []
      }
    ]
  }
}
```

---

## 📋 PHASE 6 — BACKEND API (FastAPI)

Connect to TuruLav's existing JSON data structure. The backend mirrors the exact same data shape TuruLav already uses so the frontend data layer drops in with zero changes.

**Core routes:**
```
POST  /auth/register         → create user, generate embedding, return JWT
POST  /auth/login            → verify credentials, return JWT + refresh token
POST  /auth/refresh          → rotate refresh token
POST  /auth/otp/send         → Twilio OTP send
POST  /auth/otp/verify       → Twilio OTP confirm
GET   /profiles/discover     → paginated deck, filter by location+prefs+vector
POST  /profiles/swipe        → record action, check mutual, return match status
GET   /matches               → all matches for auth user
GET   /conversations         → all conversations with last message
GET   /conversations/{id}    → messages paginated
POST  /conversations/{id}    → send message
POST  /media/upload          → signed Cloudinary upload URL
GET   /community/feed        → paginated posts
POST  /community/posts       → create post
GET   /events                → events by proximity
POST  /events/{id}/rsvp      → RSVP to event
POST  /payments/checkout     → Stripe session creation
POST  /webhooks/stripe       → subscription lifecycle events
GET   /admin/users           → user list with filters (admin only)
PUT   /admin/users/{id}      → update status (admin only)
GET   /admin/analytics       → platform stats (admin only)
```

**AI matching:** On every `GET /profiles/discover`, run:
```sql
SELECT * FROM profiles
WHERE ST_DWithin(location, ST_MakePoint($lon,$lat)::geography, $radius_meters)
AND age BETWEEN $age_min AND $age_max
AND id NOT IN (SELECT swiped_id FROM swipes WHERE swiper_id = $user_id)
ORDER BY ai_embedding <=> $user_embedding
LIMIT 20
```

---

## 📋 PHASE 7 — DEPLOY AGENT

After every build completes:

```bash
git init
git config user.name "Rick Jefferson"
git config user.email "rjbizsolution23@gmail.com"
git add .
git commit -m "feat: {appName} — TuruLav white-label build | RJ Business Solutions | 2026-02-22"
git branch -M main
gh repo create rjbizsolution23-wq/{niche-id}-platform --public --source=. --remote=origin
git push -u origin main --force
```

Token: `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`

README header on every repo:
```
![RJ Business Solutions](https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg)
Built by RJ Business Solutions | 1342 NM 333, Tijeras, NM 87059
rickjeffersonsolutions.com | 2026-02-22
Base: TuruLav (LabArtisan) → Enhanced & White-Labeled
```

---

## ✅ DEFINITION OF DONE

```
□ TuruLav scan inventory.json complete — zero files missed
□ All hardcoded colors converted to CSS variables
□ All hardcoded strings moved to copy.ts
□ All JSON data files connected to live API with fallback
□ Framer Motion on all existing TuruLav components
□ Swipe deck live on /discover with correct spring physics
□ Match modal fires on mutual like with confetti
□ Real-time chat wired to Supabase Realtime
□ Onboarding 4-step wizard with Twilio OTP
□ Premium screen with Stripe checkout end-to-end
□ Admin dashboard with moderation + analytics
□ Branding agent writes all 9 files from niche config
□ Feature flags respected — disabled features invisible
□ Backend API all routes live, authenticated, rate-limited
□ AI vector matching returning scored results
□ GitHub repo deployed under rjbizsolution23-wq
□ Vercel frontend + Railway backend live
□ Zero console errors in production build
□ New niche deployable in under 10 minutes
```


