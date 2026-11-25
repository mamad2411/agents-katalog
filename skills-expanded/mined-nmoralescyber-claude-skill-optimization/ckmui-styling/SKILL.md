---
name: ckmui-styling
description: Designs and implements production-grade web UI for security/cybersecurity products using shadcn/ui, Tailwind CSS, and Radix primitives. Make sure to use this skill whenever the user says design a page, build a UI, create a dashboard, style this component, build a landing page UI, design a security dashboard, build a trust page, build a status page, design the auth flow, style the SOC 2 trust center, or describes any web interface work for a public-facing or product-internal page. Specializes in patterns that build trust for security buyers — clean technical authority, deliberate use of color (avoiding panic-coded reds where possible), evidence-forward layouts, accessibility-by-default, and dark-mode parity. Includes templates for landing pages, marketing site components, product dashboards, security trust centers, status pages, auth/MFA flows, alert/incident UI, and admin consoles. Do NOT use for: full multi-page site information architecture (describe to Claude directly), brand identity/logo work (use ckmdesign), presentation slides (use ckmslides), banner ads (use ckmbanner-design), or interactive demos (use create-workflow-demo).
---

# Web UI Styling (Cybersecurity-First)

Production-grade web UI for security products — landing pages, dashboards, trust centers, status pages, auth flows. Built on shadcn/ui + Tailwind + Radix.

## When to use vs. adjacent design skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Building or styling a web page or component | Designing a logo or brand identity → `ckmdesign` |
| Output is HTML/JSX/CSS code | Building a presentation deck → `ckmslides` |
| Cybersec product UI specifically | Designing a banner ad → `ckmbanner-design` |
| Dashboard, trust center, status page, auth flow | Conversion landing page (no security context) → `create-landing-page` |
| Component library, design tokens, dark mode | Visual mockup with no implementation → describe to Claude directly |

## Core stack defaults

```
- shadcn/ui     for primitives (built on Radix UI)
- Tailwind CSS  for utility styling
- Radix UI      for accessibility primitives shadcn doesn't expose
- lucide-react  for iconography (consistent, security-friendly aesthetic)
- Framer Motion ONLY when motion serves comprehension, never for decoration
```

If the user has a different stack, ASK before assuming. Never silently swap to a different stack.

## Cybersecurity UI design principles

Security buyers are sophisticated and skeptical. Your UI either earns trust or actively undermines the product. The principles:

### 1. Calm > Alarm
Default UI state should feel **steady**. Pages that scream "10 critical alerts!" the second they load condition users to alert fatigue and tune you out. Reserve red for genuine criticality. Use color hierarchy:

- **Neutral / surface** — default state, healthy
- **Blue / informational** — events, notices, neutral actions
- **Yellow / amber** — warnings, anomalies needing review
- **Red** — only for active critical states (active breach, system down, data loss in progress)
- **Green** — confirmation/success, NOT background "all is well" coloring (overuse devalues it)

### 2. Evidence > Assertion
Every claim needs a way to drill in. "12 events detected" is a button to the events. "SOC 2 compliant" links to the trust center. "Encrypted at rest" hovers to AES-256-GCM with KMS key reference. Sophisticated buyers test claims; non-evidenced claims fail the test.

### 3. Density with hierarchy
Security dashboards have a lot to show. Cramming it into one screen = noise. The discipline:

- **Primary plane** — 3-7 things, each a hero
- **Secondary plane** — accessed via tab or expansion
- **Tertiary plane** — accessed via search or detail page

Never put 20 KPIs above the fold. Show 3-5; the rest are clicks away.

### 4. Status legibility from 10 feet
Operators look at security dashboards from across the room (NOC walls, ambient screens). Status indicators must read at distance:

- Large traffic-light coloring for system-wide states
- Heavy fonts for top-line numbers
- Severity badges in standardized positions

### 5. Dark mode is not an afterthought
Security operators run dark mode. Dashboards live on dark backgrounds. Build dark-first or build both in parallel; do NOT ship light-mode-only.

### 6. Empty state is a UX, not a placeholder
"No data yet" is a moment to teach. Empty states should:
- Confirm the system is working (not broken)
- Show what will appear here
- Provide the next action to populate it

### 7. Accessibility by default
- Keyboard navigation full coverage
- Focus rings visible (don't suppress them for "cleanliness")
- Color is never the only signal (icons + text alongside colored badges)
- Contrast ratio minimum WCAG AA (4.5:1 normal text, 3:1 large)
- Screen reader labels on all interactive elements
- Form errors announced via aria-live

## Page-type templates

### Trust center / security page
The single most important public-facing page for a security product after the homepage.

```
Hero
  - Headline: positioning statement of trust (NOT "we take security seriously")
  - Sub: specific commitment ("SOC 2 Type II certified annually since X, available on request")

Compliance row
  - Logos / badges: SOC 2, ISO 27001, HIPAA, PCI, FedRAMP, GDPR, CCPA
  - Each clickable to detail (report request, audit scope, attestation date)

Security architecture summary
  - Diagram: data flow, encryption layers, deployment options
  - Bullets: encryption at rest (algorithm), in transit (TLS version), key management (BYOK option?)

Sub-processor list
  - Table: vendor, purpose, location, data category
  - Update notification subscription

Vulnerability disclosure
  - How to report (email, security.txt link, bug bounty if any)
  - Response SLA commitment
  - Hall of fame (if applicable)

Pen test attestation
  - Most recent date, scope, summary findings (high-level)
  - Annual or more-frequent cadence stated

Customer security resources
  - Customer-only documentation links (gated)
  - Audit report request flow
  - Security questionnaire status (some companies pre-publish CAIQ/SIG responses)

Footer
  - Security contact (specific email/PGP key, not generic)
  - Status page link
  - Updates subscription
```

### Status page (incident transparency)
Public commitment to operational transparency. Must be honest or it backfires.

```
Top banner
  - Current overall status: Operational | Degraded | Partial Outage | Major Outage
  - Last updated timestamp

Component grid
  - Per-service status indicator (healthy / degraded / down)
  - Each click-through to historical uptime

Active incidents
  - Open by severity, with last update and ETA

Past 90 days
  - Calendar grid: each day colored by incident severity
  - Uptime % calculation

Subscribe section
  - Email / SMS / RSS / webhook for incident notifications

Footer
  - Maintenance window calendar
  - Component dependency map (advanced — when you're ready)
```

### Security product dashboard (logged-in)
The hero workspace for security operators using your product.

```
Top bar
  - Org switcher / environment selector (prod/staging clearly labeled)
  - Global search
  - Alert/notification icon with count badge
  - User menu

Left nav
  - Workspace sections (max 7 at top level)
  - Collapsed by default for density

Main content area (3-region default)
  - Region 1 (top): KPI hero (3-5 numbers, large font, with trend indicator)
  - Region 2 (middle): primary work surface (table, kanban, timeline, chart)
  - Region 3 (bottom): contextual info (recent activity, related alerts, suggested actions)

Right rail (optional, contextual)
  - Detail panel for selected item
  - Action buttons for selected item
  - Notes / collaboration if multi-user

Empty states everywhere
  - Each region has a tested empty-state design
```

### Auth / MFA / login flow
Security UI starts at the front door. This must be flawless.

```
Login page
  - Single primary input (email or username)
  - SSO buttons above password (preferred path)
  - "Sign in with passkey" if WebAuthn supported
  - Forgot password / new account links UNDER the form (not above)
  - Trust signals visible (compliance row in footer)
  - NO marketing copy on the login page itself

MFA challenge page
  - Method options shown clearly (TOTP, push, hardware key, SMS as last resort)
  - Backup code path always available
  - Don't auto-submit on 6th digit (gives user time to verify)
  - Clear "lost device" recovery flow

Account recovery
  - Multi-factor recovery (don't make email the only path)
  - Time-delayed recovery for sensitive accounts (admin recovery should take 24+ hours)
  - Notification to all known channels when recovery initiated

Post-login landing
  - Surface anything pending (alerts, pending approvals, expiring sessions)
  - Don't drop them on a generic dashboard if they have urgent items
```

### Marketing landing page (top-of-funnel security product)
Prospect arrives from ad / referral / search.

```
Hero (above fold)
  - Headline: outcome (NOT feature)
  - Sub: who it's for + how (one sentence)
  - Hero CTA: book demo / start trial / talk to sales (ONE primary)
  - Visual: product screenshot or threat-data viz, NOT stock photo
  - Trust row: 4-6 customer logos (in their industry if possible)

Problem framing
  - 3-column: the cost of inaction, in their language

Solution
  - 3 capability cards with icon, headline, 2-line description
  - Each links to deeper page

Proof
  - Customer story with quote, photo, quantified outcome
  - Optional: 2-3 logos with metrics ("Reduced X by Y% at Z")

Compliance / trust
  - Badge row (SOC 2, ISO, etc.)
  - Link to trust center

Pricing teaser
  - Show pricing model OR clearly state "contact for pricing" with reason
  - Don't make security buyers fill a 14-field form to learn pricing

Final CTA
  - Same as hero, restated

Footer
  - Comprehensive (contact, social, resources, legal, security)
```

## Component patterns specific to security UI

### Alert / event card
```
[Severity badge] [Time] [Source]
[Headline — what happened, in plain English]
[Affected entity — IP, user, host, system]
[Body — context, indicators, related events count]
[Action row: investigate | acknowledge | escalate | suppress]
[Footer: assignee | last updated]
```

### Compliance control card
```
[Framework badge] [Control ID] [Status icon]
[Control name]
[Owner avatar + name]
[Last evidenced: date] [Next due: date]
[Action: view evidence | upload | reassign]
```

### Vulnerability finding
```
[Severity badge — CVSS color] [CVE ID] [First seen]
[Headline]
[Affected: hosts/services count, click for list]
[CVSS vector summary]
[Remediation status: open | patching | mitigated | accepted]
[Action: details | acknowledge | assign | suppress]
```

### Trust / certification badge
```
[Logo of standard]
[Standard name]
[Status: certified | in-progress | renewal-due]
[Valid through: date]
[Click: view report / attestation]
```

## Design tokens (Tailwind config defaults for security UI)

```js
// tailwind.config.js extension
{
  colors: {
    // Severity scale (use sparingly)
    critical: '#dc2626',  // red-600 — only for active critical
    high:     '#ea580c',  // orange-600
    medium:   '#ca8a04',  // yellow-600
    low:      '#0891b2',  // cyan-600
    info:     '#475569',  // slate-600
    healthy:  '#16a34a',  // green-600 — confirmation only

    // Surface scale (dark-mode-first)
    surface: {
      0: '#0a0a0a',  // background
      1: '#171717',  // card
      2: '#262626',  // elevated card
      3: '#404040',  // border / divider
    },
    
    // Brand (override per security company)
    brand: {
      DEFAULT: '#3b82f6',  // blue-500 — trustworthy default
      hover:   '#2563eb',
      muted:   '#1e3a8a',
    },
  },
  fontFamily: {
    sans: ['Inter', 'system-ui'],
    mono: ['JetBrains Mono', 'SF Mono', 'Menlo'],  // for IDs, hashes, IPs
  },
}
```

## Anti-patterns specific to security product UI

- **Marketing fluff in product UI** — security ops want to work, not be sold to
- **Excessive animation** — busy interfaces signal toy product
- **Stock-photo people on the trust page** — instant credibility kill
- **Vague status ("running")** — say what's actually true ("ingesting at 1.2K events/sec")
- **Dark patterns on consent / cookie / tracking** — sophisticated buyers spot these instantly
- **Marketing-spec compliance claims** — "HIPAA compliant" without nuance is a flag
- **Hidden fine print** — security buyers READ the fine print; if you hide it, you're hiding something
- **Flashing red across the top** — even when there IS a critical alert, the design should communicate severity calmly
- **Light mode default for an ops product** — operators run dark mode 14 hours a day
- **Cluttered first-launch state** — overwhelm = bounce
- **Skeleton loaders forever** — set timeouts; show actual error states past 5 seconds
- **Disabled-button hell** — disabled buttons with no explanation; show what's missing

## Output

Depending on prompt:
- **Component:** JSX/TSX with Tailwind classes, accessible markup, dark-mode supported
- **Page:** Full HTML or Next.js page component, responsive, accessible
- **Design system:** Tokens (colors, spacing, typography, radii) in Tailwind config
- **Spec:** Annotated wireframe in Markdown if implementation isn't yet ready
- **Always include:** dark mode, mobile breakpoint, accessibility notes, what state(s) the component handles (loading, empty, error, success)
- **Always exclude:** stock imagery references, marketing language, vague color usage
