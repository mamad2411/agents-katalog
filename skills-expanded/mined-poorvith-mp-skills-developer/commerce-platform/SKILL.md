---
name: commerce-platform
last_reviewed: 2026-09-06
group: Domain-specific
description: >-
  Architect CMS commerce: cart pipeline, checkout, payment gateways and PCI boundaries. Use when
  developing Shopify apps, Liquid themes, or Headless commerce.
---

# Commerce Platform

Designs, implements, and secures e-commerce workflows, shopping carts, checkout funnels, payment gateways, and inventory management for content management systems.

## Phased Workflow

### Phase 1: Architecture & Data Modeling
1. Model product catalog schemas (simple, variable, bundled products, tax categories, stock keeping units).
2. Design cart state synchronization (guest sessions, persistent user carts, Redis session caching).

### Phase 2: Checkout & Payment Integration
1. Implement PCI-DSS compliant payment integration (Stripe Elements, PayPal SDK, Apple/Google Pay).
2. Ensure idempotent webhook handling for asynchronous order state transitions (`charge.succeeded`, `payment_intent.failed`).
3. Optimize checkout UX: reduce friction, enable 1-click checkout, simplify shipping calculation.

### Phase 3: Performance, Security & Caching
1. Configure selective caching (exclude cart, checkout, account pages from Varnish/CDN cache).
2. Implement inventory locking during checkout to prevent double-selling under high concurrency.

## Verification & Quality Checklist
- [ ] Payment credentials and webhook signing secrets stored in environment variables.
- [ ] Checkout forms validate inputs strictly and handle network drops gracefully.
- [ ] Cart endpoints protected against automated card testing (rate limiting + CAPTCHA).

## Anti-Patterns & Constraints
- NEVER handle raw credit card numbers on your server (always use client-side tokenization / Hosted Fields).
- NEVER cache authenticated user checkout or cart responses on public CDNs.

## References

Load these only when the task needs them:

- [references/pci-dss-checklist.md](references/pci-dss-checklist.md)
