---
name: onboard-tenant
description: Set up a new tenant in TenantFlow. Creates the Clerk organization, Stripe customer, and seeds initial data.
---

# Onboard Tenant

Walks through the full tenant onboarding workflow for TenantFlow.

## When to use
- Setting up a new freelancer workspace during development
- Testing the full registration flow
- Debugging tenant creation issues

## Workflow

1. **Create Clerk organization** — set up the organization in Clerk with the tenant's name and admin user
2. **Create Stripe customer** — create a Stripe Customer record linked to the tenant, set default subscription to Free tier
3. **Create database records** — insert Tenant row in Prisma with `clerkOrgId` and `stripeCustomerId`
4. **Seed initial data** — create default invoice template, default time entry categories, and sample client (optional)
5. **Verify** — confirm tenant can log in, sees their empty dashboard, and subscription shows as Free

## Project specifics
- Clerk org ID maps to `tenant.clerkOrgId` in Prisma
- Stripe customer ID maps to `tenant.stripeCustomerId` in Prisma
- Free tier limits: 3 clients, 1 user, basic invoice template
- All seed data must include the correct `tenantId` foreign key
