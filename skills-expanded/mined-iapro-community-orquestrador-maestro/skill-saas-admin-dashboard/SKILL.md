---
name: skill-saas-admin-dashboard
description: Build or improve SaaS admin dashboards, internal admin panels, user/customer screens, tenant/workspace screens, plan/payment/log views, sidebar layouts, metrics, filters, tables, support tools, and onboarding administration.
category: frontend
risk: low
source: local-project-patterns
---

# skill-saas-admin-dashboard

## Workflow

1. Inspect existing route groups, layout shells, component library, icons, table patterns, data fetching, auth checks, loading states, and error states.
2. Map the operational questions the admin must answer: users, tenants, plans, payments, logs, support, onboarding, abuse, or billing recovery.
3. Design dense screens for repeated work: metrics, filters, paginated tables, detail drawers, and audit history.
4. Fetch only the fields each screen renders. Add backend endpoints, indexes, or migrations when dashboards query large or cross-tenant tables.
5. Verify route gating, responsive behavior, empty/error/loading states, and the project build/typecheck.

## Admin Surface

Prefer this baseline navigation unless the project already has a stronger one:
- Dashboard
- Users or Customers
- Tenants or Workspaces when multi-tenant
- Plans
- Payments
- Logs or Audit
- Settings
- Help or Onboarding

## Guardrails

1. Reuse the project layout, route structure, component library, icons, table patterns, and loading/error states.
2. Keep admin UIs dense, calm, and scannable. Avoid hero sections, marketing copy, decorative cards, and one-off visual systems.
3. Gate admin routes with backend/session role checks. Hidden navigation is not an access-control mechanism.
4. Use explicit filters for tenant, user, status, date range, provider, plan, and risk state where relevant.
5. Show payment, subscription, and entitlement states as operational statuses with timestamps, provider IDs, and audit history.
6. Make manual plan, payment, entitlement, and user-block changes auditable with actor, reason, before/after, and timestamp.

## Data Rules

- Prefer explicit Supabase selects and stable DTOs.
- Keep admin views server-side or service-role-backed when they cross tenant boundaries.
- Normalize legacy table shapes in backend/services, not scattered across UI components.
- Paginate large tables and add indexes for common filters before claiming the dashboard is production-ready.
- Avoid rendering PII or secrets unless the admin workflow explicitly needs them.

## Validation

- Run the project typecheck/build/lint when available.
- Check at least one authorized and one unauthorized admin route path.
- Inspect mobile and desktop layouts for table overflow, clipped text, and broken navigation.

