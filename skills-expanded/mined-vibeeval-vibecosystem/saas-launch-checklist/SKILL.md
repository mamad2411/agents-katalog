---
name: saas-launch-checklist
description: Pre-launch verification across infrastructure, security, legal, payment, email, analytics, and performance. Day-1 monitoring, rollback plan, incident response skeleton, and post-launch week-1 checklist.
---

# SaaS Launch Checklist

A structured checklist for shipping a SaaS product to production with confidence. Every item exists because someone skipped it and regretted it.

## Pre-Launch Checklist (28 Items)

### Infrastructure (5 items)

- [ ] **SSL/TLS** -- Certificate installed, auto-renewal configured (Let's Encrypt / ACM), HSTS header present
- [ ] **CDN** -- Static assets served through CDN, cache-control headers set, origin shielding enabled
- [ ] **Backup** -- Database backup scheduled (daily minimum), tested restore procedure, off-site copy
- [ ] **Monitoring** -- Health check endpoint returns 200 when healthy and 503 when degraded, uptime monitor pings every 60s
- [ ] **Alerting** -- PagerDuty/Opsgenie configured, on-call rotation set, escalation policy defined (5 min ack SLA)

### Security (5 items)

- [ ] **Penetration test** -- Run OWASP ZAP or equivalent against staging, fix all HIGH/CRITICAL findings
- [ ] **Dependency audit** -- `npm audit` / `pip-audit` / `trivy` shows zero critical CVEs
- [ ] **Secret rotation** -- All production secrets differ from staging, rotation schedule documented
- [ ] **Rate limiting** -- API endpoints rate-limited (e.g., 100 req/min per user), auth endpoints stricter (10 req/min)
- [ ] **Headers** -- CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy all configured

### Legal (4 items)

- [ ] **Terms of Service** -- Reviewed by legal counsel, published at `/terms`, acceptance recorded at signup
- [ ] **Privacy Policy** -- GDPR/CCPA compliant, published at `/privacy`, covers data collection, retention, and third parties
- [ ] **Cookie consent** -- Banner shown to EU visitors, non-essential cookies blocked until consent, preferences stored
- [ ] **DPA (Data Processing Agreement)** -- Template available for enterprise customers, sub-processor list published

### Payment (4 items)

- [ ] **Test transactions** -- Full purchase flow tested with test cards (success, decline, 3DS), subscription upgrade/downgrade verified
- [ ] **Webhook verification** -- Stripe/Paddle webhook signature verified, replay attacks prevented with idempotency keys
- [ ] **Invoice generation** -- Invoices auto-generated with correct tax info, downloadable as PDF, emailed on payment
- [ ] **Dunning flow** -- Failed payment retry schedule configured (day 1, 3, 5, 7), grace period before cancellation

### Email (4 items)

- [ ] **SPF/DKIM/DMARC** -- DNS records configured, DMARC policy set to `quarantine` or `reject`, verified with mail-tester.com
- [ ] **Transactional templates** -- Welcome, password reset, invoice, and trial expiry emails tested across Gmail/Outlook/Apple Mail
- [ ] **Unsubscribe** -- One-click unsubscribe header present (RFC 8058), `/unsubscribe` endpoint works, preference center available
- [ ] **Sender reputation** -- Dedicated IP warmed up (if >10k emails/day), bounce handling configured, complaint feedback loop active

### Analytics (3 items)

- [ ] **Core events** -- Signup, activation, purchase, and churn events tracked with user ID and properties
- [ ] **Funnels** -- Signup-to-activation and trial-to-paid funnels configured in analytics dashboard
- [ ] **Dashboards** -- Real-time dashboard shows active users, revenue (MRR), error rate, and response time

### Performance (3 items)

- [ ] **Load test** -- k6/Artillery run at 2x expected peak traffic, p95 latency under 500ms, zero errors
- [ ] **CDN cache** -- Cache hit ratio above 90% for static assets, proper `Cache-Control` and `ETag` headers
- [ ] **Image optimization** -- All images served as WebP/AVIF with responsive srcset, lazy loading below the fold

## Day-1 Monitoring Dashboard

Build this dashboard before launch. Every panel answers a specific question.

```
+-----------------------------------------------------+
|                  SaaS Launch Dashboard               |
+---------------------------+-------------------------+
| Request Rate (req/s)      | Error Rate (%)          |
| Normal: 10-50/s           | Target: < 1%            |
| Alert: > 200/s            | Alert: > 2%             |
+---------------------------+-------------------------+
| p95 Latency (ms)          | Active Users (real-time) |
| Target: < 200ms           | Shows WebSocket/polling  |
| Alert: > 500ms            | count                    |
+---------------------------+-------------------------+
| Signup Rate (/hr)         | Payment Success Rate (%) |
| Compare to projection     | Target: > 95%            |
| Alert: 0 for 30min        | Alert: < 90%             |
+---------------------------+-------------------------+
| CPU / Memory              | Database Connections      |
| Alert: > 80%              | Alert: > 80% pool        |
+---------------------------+-------------------------+
```

### Dashboard as Code (Prometheus Queries)

```yaml
# monitoring/launch-dashboard.yml
panels:
  - title: Request Rate
    query: sum(rate(http_requests_total[5m]))
    alert_threshold: 200

  - title: Error Rate
    query: |
      sum(rate(http_requests_total{status_code=~"5.."}[5m]))
      / sum(rate(http_requests_total[5m])) * 100
    alert_threshold: 2

  - title: p95 Latency
    query: |
      histogram_quantile(0.95,
        sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
    alert_threshold: 0.5

  - title: Signup Rate
    query: sum(increase(user_signups_total[1h]))
    alert_threshold: 0  # alert if zero for 30 min

  - title: Payment Success Rate
    query: |
      sum(rate(payment_completed_total[5m]))
      / sum(rate(payment_attempted_total[5m])) * 100
    alert_threshold: 90  # alert if below
```

## Rollback Plan Template

Complete this before you deploy. If you cannot fill every field, you are not ready to launch.

```markdown
# Rollback Plan: [Product Name] v[X.Y.Z]

## Decision Criteria
Trigger rollback if ANY of these occur within 60 minutes of deploy:
- [ ] Error rate exceeds 5%
- [ ] p95 latency exceeds 2 seconds for 5 consecutive minutes
- [ ] Payment processing fails for 3+ consecutive attempts
- [ ] Data integrity issue detected (mismatched records)

## Rollback Steps
1. Set feature flag `launch_v1` to OFF (immediate, <30 seconds)
2. Revert DNS/load balancer to previous deployment
3. Run: `kubectl rollout undo deployment/api --to-revision=PREV`
   OR: `docker compose -f docker-compose.prod.yml up -d --force-recreate`
4. Verify health check returns 200 on previous version
5. Notify #incidents channel: "Rollback executed, investigating"

## Data Migration Rollback
- [ ] Database migration has a DOWN migration
- [ ] Tested: `npm run migrate:down` or `python manage.py migrate APP PREVIOUS`
- [ ] New columns are NULLABLE (old code ignores them)
- [ ] No destructive changes (column drops, renames) in this release

## Communication
- Engineering: #incidents Slack channel
- Support: Pre-drafted message in support tool
- Customers: Status page update (only if downtime > 5 min)

## Owner
- Rollback decision: [On-call engineer name]
- Execution: [DevOps engineer name]
- Communication: [Support lead name]
```

## Incident Response Playbook Skeleton

```markdown
# Launch Day Incident Playbook

## Severity Levels
| Level | Definition                  | Response  | Example                    |
|-------|-----------------------------|-----------|----------------------------|
| SEV-1 | Service down, data loss     | 5 min     | Database unreachable       |
| SEV-2 | Major feature broken        | 15 min    | Payments failing           |
| SEV-3 | Minor feature broken        | 1 hour    | Email delivery delayed     |
| SEV-4 | Cosmetic issue              | Next day  | Alignment bug on Safari    |

## On-Call Roster (Launch Day)
| Role               | Primary        | Secondary      | Contact        |
|--------------------|----------------|----------------|----------------|
| Incident Commander | [Name]         | [Name]         | [Phone/Slack]  |
| Backend Engineer   | [Name]         | [Name]         | [Phone/Slack]  |
| Frontend Engineer  | [Name]         | [Name]         | [Phone/Slack]  |
| DevOps/SRE         | [Name]         | [Name]         | [Phone/Slack]  |

## Response Flow
1. DETECT  - Alert fires or user reports issue
2. TRIAGE  - Assign severity, open incident channel (#inc-YYYYMMDD-NN)
3. CONTAIN - Feature flag OFF, rollback, or scale up
4. FIX     - Root cause fix, deploy to staging, verify
5. DEPLOY  - Push fix to production with monitoring
6. REVIEW  - Post-incident review within 48 hours

## Pre-Written Status Page Messages
- Investigating: "We are aware of an issue affecting [X] and are investigating."
- Identified: "The issue has been identified. A fix is being deployed."
- Resolved: "The issue has been resolved. All systems are operational."
```

## Post-Launch: First 7 Days Checklist

### Day 1 (Launch Day)

- [ ] All-hands monitoring: dashboard on a shared screen or TV
- [ ] Respond to every support ticket within 2 hours
- [ ] Track signup funnel: landing page visits -> signups -> activation
- [ ] Check error logs every hour for new error patterns
- [ ] Verify email deliverability (check spam folders with seed accounts)

### Day 2-3

- [ ] Review Day 1 analytics: signup count, activation rate, bounce rate
- [ ] Fix any P1/P2 bugs discovered by real users
- [ ] Check payment reconciliation: Stripe dashboard matches your records
- [ ] Send first-day cohort a "how's it going?" email (personal, from founder)
- [ ] Monitor server costs: actual vs projected infrastructure spend

### Day 4-5

- [ ] Analyze user behavior: where do users drop off? Heatmaps, session recordings
- [ ] Run second load test if traffic patterns differ from projections
- [ ] Review and tune alerting thresholds (reduce noise, catch real issues)
- [ ] Check SEO: is Google indexing your pages? robots.txt correct?
- [ ] Backlog grooming: prioritize bugs and feature requests from real users

### Day 6-7

- [ ] Week 1 retrospective: what worked, what did not, what to change
- [ ] Publish week 1 metrics: signups, activation, retention, revenue
- [ ] Plan week 2 priorities based on actual user data (not assumptions)
- [ ] Thank early adopters (personal email, discount, or swag)
- [ ] Remove launch-specific feature flags and temporary monitoring

## Contrast: Phased Rollout vs Big Bang Launch

### BAD: Big Bang Launch

```
Monday 9:00 AM:
  - Mass email to 50,000 person waitlist
  - ProductHunt launch post goes live
  - Hacker News submission
  - All social media posts scheduled simultaneously
  - Full feature set available to everyone

Monday 9:15 AM:
  - 3,000 concurrent users hit the app
  - Database connections exhausted
  - Payment webhook queue backs up
  - Support inbox: 200 tickets in 30 minutes
  - Error rate: 15%
  - Team panics

Monday 10:00 AM:
  - Emergency rollback
  - Status page: "We are experiencing issues"
  - ProductHunt comments: "This doesn't work"
  - First impression destroyed
```

### GOOD: Phased Rollout

```typescript
// Feature flag configuration for phased rollout
const LAUNCH_PHASES = {
  phase1: {
    name: 'Team and Friends',
    startDate: '2025-01-06',
    criteria: { userList: 'internal-testers' },  // 50 users
    goal: 'Find critical bugs before anyone else sees them',
  },
  phase2: {
    name: 'Beta Waitlist (10%)',
    startDate: '2025-01-08',
    criteria: { percentage: 10 },                 // 500 users
    goal: 'Validate onboarding flow and payment',
  },
  phase3: {
    name: 'Beta Waitlist (50%)',
    startDate: '2025-01-10',
    criteria: { percentage: 50 },                 // 2,500 users
    goal: 'Load test with real traffic patterns',
  },
  phase4: {
    name: 'Full Waitlist + Public',
    startDate: '2025-01-13',
    criteria: { percentage: 100 },                // everyone
    goal: 'General availability',
  },
} as const
```

```
Week 1 Monday:    50 internal users     -> Find showstoppers
Week 1 Wednesday: 500 beta users        -> Validate payment flow
Week 1 Friday:    2,500 beta users      -> Verify infrastructure holds
Week 2 Monday:    Full public launch    -> Confidence backed by data

Each phase gate:
  [x] Error rate < 1%
  [x] p95 latency < 300ms
  [x] Payment success > 98%
  [x] NPS from phase users > 30
  [x] Zero data integrity issues
  -> Only then proceed to next phase
```

### Why Phased Rollout Wins

| Dimension         | Big Bang               | Phased Rollout           |
|-------------------|------------------------|--------------------------|
| Risk              | All-or-nothing         | Contained per phase      |
| Feedback          | Overwhelming, chaotic  | Manageable, actionable   |
| Infrastructure    | Guess and hope         | Scale based on real data |
| Recovery          | Public failure         | Private fix              |
| First impression  | One shot               | Refined over 4 attempts  |
| Team stress       | Maximum                | Distributed              |

**Key principle**: Launch is not a single moment -- it is a process. Every item you skip is a bet that nothing will go wrong in that area. The checklist exists to make the boring stuff automatic so you can focus on users.
