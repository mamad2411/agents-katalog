---
name: marketplace-ecosystem-design
description: Design the Package Marketplace and creator ecosystem for the Software Synthesis OS — the economic flywheel that drives billion-dollar network effects. Package discovery, creator revenue share, package analytics, trust tier enforcement, private enterprise registries, featured packages, package reviews, SDK for third-party developers, and the monetization architecture that makes the platform self-reinforcing.
triggers: [marketplace, package marketplace, creator economy, revenue share, package discovery, ecosystem design, third-party packages, package SDK, package ratings, package analytics, private registry, package monetization, network effects, ecosystem flywheel, package store]
---

# SKILL: Marketplace & Ecosystem Design

## Core Principle
The marketplace is not a feature — it is the economic engine of the entire OS. More packages → more capabilities → more users → more revenue → more package authors → more packages. This flywheel is what separates a product from a platform. The technical registry (package-system-design skill) handles installation. This skill handles discovery, economics, trust, and growth.

---

## 1. Marketplace Data Model

```sql
-- migrations/marketplace_schema.sql

-- Package listings (what the marketplace shows)
create table marketplace_listings (
  id uuid primary key,
  package_id uuid not null references capability_packages(id) on delete cascade,
  publisher_id uuid not null references users(id),
  publisher_org_id uuid references organizations(id),
  
  -- Discovery metadata
  display_name text not null,
  tagline text not null,                -- one-line pitch (max 80 chars)
  description_markdown text,           -- full description
  category text not null,              -- see MARKETPLACE_CATEGORIES
  tags text[] not null default '{}',
  screenshots_urls text[] default '{}',
  demo_url text,
  docs_url text,
  source_url text,                     -- for open source packages
  
  -- Trust & quality
  trust_level text not null default 'community',   -- first_party | verified_partner | community
  featured boolean not null default false,
  verified_by_staff boolean not null default false,
  
  -- Pricing
  pricing_model text not null default 'free',      -- free | paid | freemium | usage_based
  price_usd_monthly numeric(10,2),
  price_usd_per_run numeric(10,4),
  free_tier_runs_per_month integer,
  
  -- Stats (materialized, updated async)
  install_count integer not null default 0,
  active_workspaces integer not null default 0,
  avg_rating numeric(3,2),
  review_count integer not null default 0,
  
  status text not null default 'draft',            -- draft | published | delisted
  published_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Package reviews
create table package_reviews (
  id uuid primary key,
  listing_id uuid not null references marketplace_listings(id) on delete cascade,
  reviewer_id uuid not null references users(id),
  rating integer not null check (rating between 1 and 5),
  title text,
  body text,
  verified_install boolean not null default false,  -- reviewer has the package installed
  helpful_count integer not null default 0,
  status text not null default 'published',
  created_at timestamptz not null default now()
);

-- Revenue share tracking
create table marketplace_revenue_events (
  id uuid primary key,
  listing_id uuid not null references marketplace_listings(id),
  workspace_id uuid not null references workspaces(id),
  event_type text not null,    -- subscription | run_charge | refund
  gross_usd numeric(12,4) not null,
  platform_fee_usd numeric(12,4) not null,
  creator_payout_usd numeric(12,4) not null,
  stripe_payment_intent_id text,
  recorded_at timestamptz not null default now()
);

-- Creator payouts
create table creator_payout_batches (
  id uuid primary key,
  publisher_id uuid not null references users(id),
  period_start date not null,
  period_end date not null,
  total_payout_usd numeric(12,4) not null,
  status text not null default 'pending',   -- pending | processing | paid | failed
  stripe_transfer_id text,
  created_at timestamptz not null default now()
);

-- Package analytics (per workspace, per package)
create table package_usage_metrics (
  id uuid primary key,
  package_id uuid not null references capability_packages(id),
  workspace_id uuid not null references workspaces(id),
  metric_date date not null,
  nodes_executed integer not null default 0,
  artifacts_created integer not null default 0,
  total_run_cost_usd numeric(12,4) not null default 0,
  unique (package_id, workspace_id, metric_date)
);
```

---

## 2. Marketplace Categories

```typescript
// packages/marketplace-types/src/categories.ts

export const MARKETPLACE_CATEGORIES = [
  // By function
  { key: 'documents',      label: 'Documents & Writing',    icon: '📄' },
  { key: 'data',           label: 'Data & Analytics',       icon: '📊' },
  { key: 'automation',     label: 'Automation & Workflows', icon: '⚡' },
  { key: 'ai',             label: 'AI & Intelligence',      icon: '🤖' },
  { key: 'communication',  label: 'Communication',          icon: '💬' },
  { key: 'media',          label: 'Media & Creative',       icon: '🎨' },
  { key: 'finance',        label: 'Finance & Billing',      icon: '💳' },
  { key: 'crm',            label: 'CRM & Sales',            icon: '🤝' },
  { key: 'hr',             label: 'HR & People Ops',        icon: '👥' },
  { key: 'legal',          label: 'Legal & Compliance',     icon: '⚖️' },
  { key: 'devtools',       label: 'Developer Tools',        icon: '🔧' },
  { key: 'marketing',      label: 'Marketing',              icon: '📣' },
  { key: 'ecommerce',      label: 'E-commerce',             icon: '🛒' },
  { key: 'education',      label: 'Education & Training',   icon: '🎓' },
  { key: 'operations',     label: 'Operations',             icon: '🏗️' },
  // By type
  { key: 'engines',        label: 'Engines',                icon: '⚙️' },
  { key: 'connectors',     label: 'Connectors',             icon: '🔌' },
  { key: 'templates',      label: 'Templates',              icon: '📋' },
  { key: 'apps',           label: 'Full Applications',      icon: '📱' },
] as const;
```

---

## 3. Creator SDK & Submission Flow

```typescript
// packages/sdk-core/src/publish.ts

export interface PackageSubmission {
  manifest: PackageManifest;
  readme: string;                 // markdown
  screenshots: File[];            // max 5
  demoUrl?: string;
  changelog: string;
  listingConfig: {
    displayName: string;
    tagline: string;
    category: string;
    tags: string[];
    pricingModel: 'free' | 'paid' | 'freemium' | 'usage_based';
    priceUsdMonthly?: number;
  };
}

// CLI command: `npx @os/sdk publish`
export async function publishPackage(submission: PackageSubmission): Promise<PublishResult> {
  // 1. Validate manifest
  const manifestErrors = validateManifest(submission.manifest);
  if (manifestErrors.length > 0) throw new PublishError('Invalid manifest', manifestErrors);

  // 2. Run automated checks
  const checks = await runPublishChecks(submission);
  if (checks.blocking.length > 0) throw new PublishError('Publish blocked', checks.blocking);

  // 3. Sign the package
  const signature = await signPackage(submission.manifest);

  // 4. Upload to registry
  const packageId = await registryClient.uploadPackage(submission, signature);

  // 5. Submit for review (required for verified_partner tier)
  if (submission.listingConfig.pricingModel !== 'free') {
    await marketplaceClient.submitForReview(packageId);
  }

  return { packageId, status: 'submitted', reviewEta: '2-3 business days' };
}

// Automated publish checks
async function runPublishChecks(submission: PackageSubmission): Promise<CheckResult> {
  const blocking: string[] = [];
  const warnings: string[] = [];

  // Required: all nodes have ui.label and ui.description
  for (const nodeDef of submission.manifest.nodes) {
    if (!nodeDef) { blocking.push('All node keys in manifest must resolve to node definitions'); break; }
  }

  // Required: README has at least 100 words
  const wordCount = submission.readme.split(/\s+/).length;
  if (wordCount < 100) blocking.push('README must have at least 100 words');

  // Required: at least one screenshot
  if (submission.screenshots.length === 0) warnings.push('Screenshots strongly recommended for discovery');

  // Required: tagline max 80 chars
  if (submission.listingConfig.tagline.length > 80) blocking.push('Tagline must be 80 characters or less');

  // Required for paid packages: demo URL
  if (submission.listingConfig.pricingModel !== 'free' && !submission.demoUrl) {
    blocking.push('Paid packages must provide a demo URL');
  }

  return { blocking, warnings };
}
```

---

## 4. Revenue Share Architecture

```typescript
// marketplace-service/revenue/RevenueEngine.ts

// Platform takes 20% of all paid package revenue (80% to creator)
const PLATFORM_FEE_RATE = 0.20;
const CREATOR_PAYOUT_RATE = 0.80;

export class RevenueEngine {

  async recordInstallRevenue(
    listingId: string,
    workspaceId: string,
    stripePaymentIntentId: string,
    grossUsd: number,
  ): Promise<void> {
    const platformFee = grossUsd * PLATFORM_FEE_RATE;
    const creatorPayout = grossUsd * CREATOR_PAYOUT_RATE;

    await db.marketplaceRevenueEvents.create({
      listingId,
      workspaceId,
      eventType: 'subscription',
      grossUsd,
      platformFeeUsd: platformFee,
      creatorPayoutUsd: creatorPayout,
      stripePaymentIntentId,
    });

    await this.updateListingStats(listingId);
  }

  async processMonthlyPayouts(): Promise<void> {
    const unpaidRevenue = await db.marketplaceRevenueEvents
      .where('status', 'unpaid')
      .groupBy('listing.publisher_id')
      .sum('creator_payout_usd');

    for (const [publisherId, totalUsd] of Object.entries(unpaidRevenue)) {
      // Minimum $20 payout threshold
      if (totalUsd < 20) continue;

      const publisher = await db.users.findById(publisherId);
      if (!publisher.stripeConnectedAccountId) continue;

      await stripe.transfers.create({
        amount: Math.floor(totalUsd * 100),   // cents
        currency: 'usd',
        destination: publisher.stripeConnectedAccountId,
        description: `OS Marketplace payout — ${new Date().toISOString().slice(0, 7)}`,
      });

      await db.creatorPayoutBatches.create({
        publisherId,
        periodStart: firstDayOfMonth(),
        periodEnd: lastDayOfMonth(),
        totalPayoutUsd: totalUsd,
        status: 'paid',
      });
    }
  }
}
```

---

## 5. Marketplace Discovery API

```typescript
// marketplace-service/routes/discovery.ts

// GET /marketplace/listings
// Supports: category, tag, pricing_model, trust_level, q (search), sort
router.get('/listings', async (req, res) => {
  const {
    category,
    tag,
    pricing_model,
    trust_level,
    q,
    sort = 'popular',
    page = 1,
    per_page = 24,
  } = req.query;

  let query = db.marketplaceListings
    .where('status', 'published');

  if (category) query = query.where('category', category);
  if (tag) query = query.whereRaw('? = ANY(tags)', [tag]);
  if (pricing_model) query = query.where('pricing_model', pricing_model);
  if (trust_level) query = query.where('trust_level', trust_level);

  if (q) {
    // Full-text search on display_name + tagline + description
    query = query.whereRaw(
      "to_tsvector('english', display_name || ' ' || tagline || ' ' || coalesce(description_markdown, '')) @@ plainto_tsquery('english', ?)",
      [q]
    );
  }

  const ORDER_BY: Record<string, string> = {
    popular:   'install_count DESC',
    newest:    'published_at DESC',
    rating:    'avg_rating DESC NULLS LAST',
    trending:  'active_workspaces DESC',
  };

  const listings = await query
    .orderByRaw(ORDER_BY[String(sort)] ?? ORDER_BY.popular)
    .paginate({ perPage: Math.min(Number(per_page), 48), currentPage: Number(page) });

  res.json(listings);
});
```

---

## 6. Trust Tier Enforcement

```typescript
// package-registry/trust/TrustEnforcer.ts

export const TRUST_TIER_RULES = {
  first_party: {
    description: 'Built and maintained by the OS team',
    requirements: ['signed_by_platform_key', 'all_tests_passing', 'security_audited'],
    canRunWithoutApproval: true,
    autoInstallAllowed: true,
    badgeColor: '#1a6cf5',
  },
  verified_partner: {
    description: 'Reviewed and verified by the OS team',
    requirements: ['signed_by_partner_key', 'staff_code_review', 'demo_tested', 'paid_if_needed'],
    canRunWithoutApproval: true,
    autoInstallAllowed: true,
    badgeColor: '#16a34a',
  },
  community: {
    description: 'Published by the community — use with discretion',
    requirements: ['signed_by_author_key'],
    canRunWithoutApproval: false,    // workspace owner must approve first install
    autoInstallAllowed: false,
    badgeColor: '#9333ea',
  },
  untrusted: {
    description: 'Not reviewed. Install at your own risk.',
    requirements: [],
    canRunWithoutApproval: false,
    autoInstallAllowed: false,
    requiresExplicitOrganizationAllowlist: true,
    badgeColor: '#dc2626',
  },
} as const;

export function enforceInstallTrust(
  pkg: CapabilityPackage,
  workspace: Workspace,
  organization: Organization,
): TrustCheckResult {
  const tier = TRUST_TIER_RULES[pkg.trustLevel];

  // Enterprise: check allowlist
  if (organization.plan === 'enterprise') {
    const allowlisted = organization.packageAllowlist?.includes(pkg.packageKey);
    if (!allowlisted && pkg.trustLevel !== 'first_party') {
      return { allowed: false, reason: 'Package is not on this organization\'s allowlist.' };
    }
  }

  // Community packages require workspace owner approval on first install
  if (pkg.trustLevel === 'community' && !workspace.approvedCommunityPackages?.includes(pkg.packageKey)) {
    return {
      allowed: false,
      requiresApproval: true,
      reason: 'Community package requires workspace owner approval before first install.',
    };
  }

  // Untrusted packages require organization-level allowlist
  if (pkg.trustLevel === 'untrusted') {
    return { allowed: false, reason: 'Untrusted packages cannot be installed.' };
  }

  return { allowed: true };
}
```

---

## 7. Network Effects Strategy

| Lever | Mechanism | Target Metric |
|---|---|---|
| Creator onboarding | SDK + docs + publish CLI | Time-to-first-publish < 2 hours |
| Discovery quality | Full-text search + category browse + AI recommendations | Package found in < 3 searches |
| Social proof | Reviews, install count, featured badges | 30% of installs influenced by reviews |
| Creator revenue | 80/20 revenue share + monthly payouts | Creator earns > $500/month by 100 installs |
| Enterprise pull | Private registries + org allowlists + SLA support | 1 enterprise = 10 avg workspaces |
| First-party as benchmark | All first-party packages are open-source and exemplary | Community packages match first-party quality |
| Viral loop | Client portals drive external users back to OS | Portal visitor → workspace conversion |

---

## 8. Checklist

- [ ] `marketplace_listings`, `package_reviews`, `marketplace_revenue_events` tables created
- [ ] All 18 marketplace categories defined and seeded
- [ ] Marketplace discovery API supports search, filter, sort, and pagination
- [ ] Full-text search uses PostgreSQL `tsvector`/`tsquery`
- [ ] Creator SDK (`npx @os/sdk publish`) validates and uploads packages
- [ ] Automated publish checks enforce quality gates before submission
- [ ] Revenue engine records events with 80/20 split
- [ ] Monthly payout batch runs on first of each month via cron
- [ ] Trust tier rules enforced at install time
- [ ] Enterprise package allowlist enforced at organization level
- [ ] Community packages require workspace owner approval on first install
- [ ] Package usage metrics updated daily via background job
- [ ] Review system requires verified install for reviews
- [ ] Creator dashboard shows installs, revenue, and usage analytics
