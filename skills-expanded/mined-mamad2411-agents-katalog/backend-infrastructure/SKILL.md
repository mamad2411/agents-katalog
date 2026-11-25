---
name: backend-infrastructure
description: "Use when setting up or deploying backend infrastructure — configuring a Supabase project or Vercel pipeline, wiring Apple sign-in and APNs, managing secrets and environments, or standing up CI/CD."
---

# Backend Infrastructure

## Overview

Full backend infrastructure setup, configuration, and deployment pipeline for Corey's projects using Supabase + Vercel + Apple platforms.

## Infrastructure Stack

| Service | Purpose |
|---------|---------|
| Supabase | Database, Auth, Storage, Edge Functions, Realtime |
| Vercel | Web hosting, serverless functions, preview deploys |
| Apple Developer | Sign in with Apple, APNs, App Store Connect |
| Google Cloud | Firebase (push), Google Sign-In |
| Stripe | Payments, subscriptions, Connect |
| EAS | Expo build and submit pipeline |

## Environment Strategy

### Three Environments
1. **Development** — Local Supabase + localhost
2. **Staging** — Separate Supabase project + Vercel preview
3. **Production** — Production Supabase + Vercel production

### Environment Variables
```
# Supabase
SUPABASE_URL=https://[project].supabase.co
SUPABASE_ANON_KEY=[anon-key]
SUPABASE_SERVICE_ROLE_KEY=[service-role-key]

# Stripe
STRIPE_SECRET_KEY=sk_[env]_[key]
STRIPE_WEBHOOK_SECRET=whsec_[secret]
STRIPE_PUBLISHABLE_KEY=pk_[env]_[key]

# Apple
APPLE_CLIENT_ID=[bundle-id]
APPLE_TEAM_ID=[team-id]
APPLE_KEY_ID=[key-id]

# App
APP_URL=[environment-url]
```

## Supabase Project Setup

### Checklist
1. Create project in correct organization
2. Configure auth providers (Email, Apple, Google)
3. Set up database schema + migrations
4. Enable RLS on all tables
5. Configure storage buckets with policies
6. Set up Edge Functions
7. Configure SMTP for transactional emails
8. Set up database webhooks if needed
9. Configure realtime subscriptions

### Edge Functions
- Use Deno runtime
- Deploy via Supabase CLI: `supabase functions deploy [name]`
- Secrets via: `supabase secrets set KEY=value`
- Test locally: `supabase functions serve`

## Vercel Deployment

### Setup
1. Link GitHub repo
2. Configure build settings (framework preset)
3. Set environment variables per environment
4. Configure custom domains
5. Set up preview deployment rules

### CI/CD Flow
```
Push to branch → Vercel Preview Deploy → Review
Merge to main → Vercel Production Deploy → Monitor
```

## Apple Platform Configuration

### Sign in with Apple
1. Register App ID with Sign in with Apple capability
2. Create Services ID for web auth
3. Create private key for token generation
4. Configure return URLs in Apple Developer Console
5. Add credentials to Supabase Auth settings

### APNs (Push Notifications)
1. Create APNs key in Apple Developer Console
2. Note Key ID and Team ID
3. Configure in Expo push notification setup
4. Test with Expo push tool

### App Store Connect
1. Create app record
2. Configure app information (description, screenshots, etc.)
3. Set up TestFlight for beta testing
4. Configure in-app purchases if applicable
5. Submit for review

## Webhooks

### Stripe Webhooks
- `checkout.session.completed` — Process successful payments
- `customer.subscription.updated` — Handle plan changes
- `invoice.payment_failed` — Handle failed payments

### Supabase Database Webhooks
- Trigger Edge Functions on database events
- Use for: sending notifications, syncing external systems, audit logging

## Monitoring

### Key Metrics
- API response times (Supabase dashboard)
- Error rates (Vercel logs + Sentry)
- Database connection count
- Storage usage
- Auth event logs

### Alerting
- Set up Supabase email alerts for database issues
- Vercel deployment failure notifications
- Stripe webhook failure alerts

## Secrets Management

### Rules
- Never commit secrets to git
- Use platform-specific secret storage (Vercel env vars, Supabase secrets, EAS secrets)
- Rotate keys on any suspected compromise
- Use different keys per environment
- Document which secrets are needed for each service

## Rules

- Always set up staging before production
- Test deployments in staging first
- Use migrations for all database changes
- Document all infrastructure decisions
- Keep environment parity (staging mirrors production config)
- Monitor costs across all services monthly
