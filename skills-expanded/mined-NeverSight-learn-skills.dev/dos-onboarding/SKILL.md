---
name: dos-onboarding
description: Directive OS client onboarding workflow, lead email system, dashboard access, payment flow, and post-payment setup steps. Use when the user asks about onboarding a new client, activating Sarah for a client, setting up a nominated email, explaining the workflow, or removing the DEMO banner from a client landing page.
---

# Directive OS — Client Onboarding & Seat Billing

> **Related skills:** Read `directive-os-system` for full product catalog, pricing, tech stack, and business plan.

---

## The Two User Types

### 1. Agency Owner (Client)
- Created by Jayson via admin Fleet Manifest (`POST /api/admin/clients`)
- Login: `directiveos.com.au/dashboard/login` — email + temp password (emailed on creation)
- JWT payload: `{ type: "agency", agencyId, email }`
- Full access: leads, transcripts, listings, staff management, billing, settings

### 2. Staff Member
- Invited by agency owner from dashboard → Seat Management page
- Login: same `/dashboard/login` — email + self-chosen password
- JWT payload: `{ type: "staff", staffId, agencyId, email, role }`
- Role-based access (see Roles & Access below)

---

## Roles & Access

| Role | Value | Dashboard Tabs |
|------|-------|----------------|
| Principal | `principal` | All tabs — Command Centre, Leads, Transcripts, Listings, Billing, Seat Management, Protocols |
| Admin | `admin` | Command Centre, Leads, Transcripts, Listings, Billing |
| Sales Executive | `sales_executive` | Command Centre, Leads, Transcripts, Listings |
| Sales Support | `sales_support` | Command Centre, Leads, Transcripts |

Agency owner (`type: "agency"`) always has full access regardless of role.
Principal staff members also get full access including Seat Management and Protocols.

---

## Onboarding Flow — Agency Owner (Client)

```
STEP 1 — Jayson creates client in Fleet Manifest (/admin/clients)
  POST /api/admin/clients (x-admin-secret header)
  Body: { name, abn, contactEmail, contactPhone, subscriptionStatus }

STEP 2 — System auto-generates temp password
  bcrypt.hash(tempPassword, 10) → saved to agencies.password_hash
  Welcome email → client email CC: jayson + adwordpress2012

STEP 3 — Client logs in
  directiveos.com.au/dashboard/login
  Email + temp password → JWT stored in localStorage.clientToken

STEP 4 — Client invites agents (optional)
  → Each invite triggers Stripe +1 seat + invite email to agent
```

---

## Onboarding Flow — Staff Agent Invite

```
STEP 1 — Agency owner: Dashboard → Staff → "Invite Agent"
  POST /api/staff (x-clerk-org-id header)
  Body: { name, email, role }

STEP 2 — System:
  - Inserts staff record (status: "invited")
  - Generates 48hr secure token (crypto.randomBytes(32))
  - Saves token + tokenExpiry to staff table
  - Increments seat_count on agencies table
  - Calls Stripe → adds 1 seat (prorated immediately) via adjustStripeSeats()
  - Sends invite email to agent CC: jayson + adwordpress2012

STEP 3 — Agent receives email
  "You've been invited to [Agency Name] — Set your password"
  Link: directiveos.com.au/dashboard/set-password?token=TOKEN
  Link expires in 48 hours

STEP 4 — Agent sets password
  POST /api/staff/verify-token { token } → validates, returns name + agencyName
  POST /api/staff/activate { token, password } → bcrypt hash saved, token cleared
  staff.status → "active"

STEP 5 — Agent logs in
  directiveos.com.au/dashboard/login → email + new password
  Sees agency Command Centre with limited tabs
```

---

## Staff Removal

```
Agency owner removes agent → DELETE /api/staff/:id
→ seat_count decremented
→ Stripe subscription updated: -1 seat (prorated credit)
```

---

## Key API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/client/login` | Public | Unified login — checks agencies then staff |
| GET | `/api/client/me` | JWT Bearer | Returns user type, agency + staff data |
| POST | `/api/staff` | x-clerk-org-id | Invite agent → Stripe +1 → invite email |
| DELETE | `/api/staff/:id` | x-clerk-org-id | Remove agent → Stripe -1 |
| POST | `/api/staff/verify-token` | Public | Validate 48hr set-password token |
| POST | `/api/staff/activate` | Public | Set password, activate account |
| POST | `/api/admin/clients` | x-admin-secret | Create agency + auto welcome email |
| POST | `/api/admin/quote` | x-admin-secret | Generate Stripe Checkout link (any tier) |
| POST | `/api/admin/clients/:id/reset-password` | x-admin-secret | Reset + email new password |
| POST | `/api/admin/clients/:id/set-password` | x-admin-secret | Manually set password |

---

## Database Schema — Key Fields

### agencies table
| Column | Type | Purpose |
|--------|------|---------|
| `contact_email` | text | Login username for owner |
| `password_hash` | text | bcrypt hash (null = no login yet) |
| `seat_count` | int | Total seats (owner + agents) |
| `stripe_customer_id` | text | Stripe customer for billing |

### staff table
| Column | Type | Purpose |
|--------|------|---------|
| `agency_id` | int | FK to agencies |
| `email` | text | Login username |
| `password_hash` | text | bcrypt hash (null until activated) |
| `password_set_token` | text | 48hr activation token |
| `token_expiry` | timestamptz | Token expiry time |
| `status` | text | "invited" \| "active" |
| `role` | text | "principal" \| "admin" \| "sales_executive" \| "sales_support" |

---

## JWT Token Structure

```
Agency: { type: "agency", agencyId: number, email: string }
Staff:  { type: "staff", staffId: number, agencyId: number, email: string, role: string }
```
- Secret: `CLIENT_JWT_SECRET` env var
- Expiry: 30 days
- Storage: `localStorage.clientToken`

---

## Pricing Tiers

| Tier | Setup | Monthly Base | Per Seat |
|------|-------|--------------|----------|
| Small | A$1,800 | A$299/mo | A$89/mo |
| Medium | A$2,500 | A$399/mo | A$99/mo |
| Large | A$4,500 | A$599/mo | A$119/mo |

Defined in `TIERS` constant in `artifacts/api-server/src/routes/admin.ts`.

---

## Quote Builder

Location: `/admin/quote` — Captain's Bridge nav → "QUOTE BUILDER"

1. Select tier (Small/Medium/Large)
2. Enter seats, agency name, contact name, email
3. Click "Generate Payment Link"
4. Calls `POST /api/admin/quote` → returns Stripe Checkout URL
5. Copy and send to prospect

---

## Email Flows

| Trigger | To | CC | Content |
|---------|----|----|---------|
| Agency created (admin) | Client email | jayson + adwordpress2012 | Welcome + temp credentials |
| Password reset | Client email | jayson + adwordpress2012 | New password |
| Agent invited | Agent email | jayson + adwordpress2012 | Set-password link (48hr) |

From: `Directive OS <leads@directiveos.com.au>`
Support: `support@directiveos.com.au`

---

## Frontend Pages

| Page | Path | Auth Required |
|------|------|---------------|
| Client/Staff Login | `/dashboard/login` | Public |
| Set Password (agents) | `/dashboard/set-password?token=TOKEN` | Public (token-gated) |
| Command Centre | `/dashboard` | JWT |
| Staff Management | `/dashboard/staff` | JWT + agency owner only |
| Billing | `/dashboard/billing` | JWT + agency owner only |
| Quote Builder | `/admin/quote` | Admin secret |

---

## Admin Credentials
- URL: `directiveos.com.au/admin`
- Username: `captainjaze` (ADMIN_USERNAME env var)
- Password: `M@gdalena2050` (ADMIN_PASSWORD env var)
- Header used: `x-admin-secret: <ADMIN_PASSWORD>`

## Test Client (Production DB — ID 19)
- Email: `jayson@directiveos.com.au`
- Password: `ocampo`
- Agency: "Directive OS (Test)"

---

## Legacy Onboarding (Clerk-based — pre April 2025)

The original flow used Clerk org-based auth. Now replaced by email+password JWT auth. Clerk org IDs still stored in `clerk_org_id` column for backwards compatibility with existing dashboard routes that use `x-clerk-org-id` header.

---

## Stripe Seat Billing — How It Works

`adjustStripeSeats(agency, delta)` in `artifacts/api-server/src/routes/staff.ts`:
1. Looks up active Stripe subscription for the agency's `stripe_customer_id`
2. Finds the `STRIPE_PRICE_PER_SEAT` line item (if any)
3. +1 seat: creates or increments the seat item with `proration_behavior: "create_prorations"`
4. -1 seat: decrements or deletes the seat item with prorated credit
5. Stripe immediately charges (or credits) the prorated amount

---

## Adding a New Client Page

1. Create artifact: `createArtifact({ slug: "agency-slug", kind: "web", title: "Agency Name" })`
2. Copy `artifacts/c21-rana` (light theme) or `artifacts/nidus-re` (dark theme)
3. Update: agency name, PHONE constant, brand colours, nav links → client's real site
4. Add DEMO banner (copy from c21-rana landing.tsx)
5. Add `GetStartedCTA` component with agency slug + name
6. Deploy → directiveos.com.au/agency-slug/
7. Onboard the client via admin Fleet Manifest → creates login credentials automatically

---

## Required Environment Variables

| Variable | Purpose |
|----------|---------|
| `CLIENT_JWT_SECRET` | JWT signing secret |
| `DOS_RESEND_KEY` or `RESEND_API_KEY` | Email sending via Resend |
| `STRIPE_KEY_ACTIVE` | Stripe API key |
| `STRIPE_PRICE_ONBOARDING` | Stripe price ID for setup fee |
| `STRIPE_PRICE_PER_SEAT` | Stripe price ID for per-seat billing |
| `ADMIN_USERNAME` | Admin login username (`captainjaze`) |
| `ADMIN_PASSWORD` | Admin login password + x-admin-secret |
