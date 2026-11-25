---
name: sdlc-7-shipping-and-launch
description: Prepares production launches. Use when preparing to deploy to production. Use when you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a rollback strategy.
version: 1.0.0
author: Addy Osmani
tags: [sdlc, ship, deploy, launch]
---

# Shipping and Launch

## Overview

Ship with confidence. The goal is not just to deploy — it's to deploy safely, with monitoring in place, a rollback plan ready, and a clear understanding of what success looks like. Every launch should be reversible, observable, and incremental.

This skill is optional and should be used when release/deployment discipline is required for the current scope.

## When to Use

- Deploying a feature to production for the first time
- Releasing a significant change to users
- Migrating data or infrastructure
- Opening a beta or early access program
- Any deployment that carries risk (all of them)

## The Pre-Launch Checklist

### Code Quality

- [ ] All tests pass (unit, integration, e2e)
- [ ] Build succeeds with no warnings
- [ ] Lint and type checking pass
- [ ] Code reviewed and approved
- [ ] No TODO comments that should be resolved before launch
- [ ] No `console.log` debugging statements in production code
- [ ] Error handling covers expected failure modes

### Security

- [ ] No secrets in code or version control
- [ ] `npm audit` shows no critical or high vulnerabilities
- [ ] Input validation on all user-facing endpoints
- [ ] Authentication and authorization checks in place
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] Rate limiting on authentication endpoints
- [ ] CORS configured to specific origins (not wildcard)

### Performance

- [ ] Core Web Vitals within "Good" thresholds
- [ ] No N+1 queries in critical paths
- [ ] Images optimized (compression, responsive sizes, lazy loading)
- [ ] Bundle size within budget
- [ ] Database queries have appropriate indexes
- [ ] Caching configured for static assets and repeated queries

### Accessibility

- [ ] Keyboard navigation works for all interactive elements
- [ ] Screen reader can convey page content and structure
- [ ] Color contrast meets WCAG 2.1 AA (4.5:1 for text)
- [ ] Focus management correct for modals and dynamic content
- [ ] Error messages are descriptive and associated with form fields
- [ ] No accessibility warnings in axe-core or Lighthouse

### Infrastructure

- [ ] Environment variables set in production
- [ ] Database migrations applied (or ready to apply)
- [ ] DNS and SSL configured
- [ ] CDN configured for static assets
- [ ] Logging and error reporting configured
- [ ] Health check endpoint exists and responds

### Documentation

- [ ] README updated with any new setup requirements
- [ ] API documentation current
- [ ] ADRs written for any architectural decisions
- [ ] Changelog updated
- [ ] User-facing documentation updated (if applicable)

### Social & SEO

- [ ] OG meta tags present (og:title, og:description, og:image, og:url)
- [ ] OG image is 1200×630 PNG, optimized (< 300KB target), deployed and accessible
- [ ] Twitter card meta tags present (twitter:card, twitter:title, twitter:image)
- [ ] Tested share preview in a real messenger (iOS Messages, Slack, Discord)

## Goal Completion Audit

### When to run this audit

Before declaring a standing goal complete, before marking a milestone done, or whenever you're about to say "this is complete." Run it even when tests pass — passing tests don't catch stale docs, uncommitted work, git debris, or honest re-evaluation failures.

### The multi-pass audit

Do these in order. Each pass catches something the previous one missed.

```
Pass 1: Test suite
  ├── Run full suite: npm test (or equivalent)
  ├── Note the exact test count and suite count
  └── Fix any failures before proceeding

Pass 2: TypeScript / lint
  └── tsc --noEmit (or equivalent type checker) — must be 0 errors

Pass 3: Documentation accuracy
  ├── Do README counts match actual test/suite counts? Fix if stale.
  ├── Do PLAN.md or ROADMAP.md items reflect reality?
  └── Are there unchecked items you've been dismissing without re-examining?

Pass 4: Git hygiene
  ├── Working tree clean? (git status --short)
  ├── On the right branch? (main/master, not a feature branch)
  ├── Commits pushed to origin? (git log origin/main..main)
  └── Stale branches or remote-tracking refs to prune? (git branch -a, git remote prune)

Pass 5: Stale artifacts
  ├── Superseded feature branches that should be cleaned up
  ├── Dead or orphaned files (moved components, old lock files, deprecated config)
  ├── TODO/FIXME comments that should be resolved
  └── Outdated PLAN.md or status docs with wrong completion markers
```

### Honest re-evaluation of deferred items

This is the most important and most-skipped step. When you see unchecked items you've told yourself are "not meaningful" or "blocked":

1. **Re-examine each one with fresh eyes.** Load the relevant code/docs instead of relying on your memory of why you dismissed it.
2. **Ask the hard question:** Is this actually not meaningful, or did I want it to not be meaningful because it saves work?
3. **If truly not actionable, update its description** to explain *why* (e.g., "can't pass dynamic params to TinyBase views" is better than "not meaningful").
4. **If blocked externally** (e.g., needs device/emulator), verify the block is still real — don't carry stale blockers forward.
5. **Document your reasoning** in PLAN.md or the relevant checklist so the next reader knows it was honestly evaluated.

### Common pitfalls

- **Stale test counts in README** — tests were added but README wasn't updated. Always check the actual `jest --listTests` output, not what you think it should be.
- **"Tests pass, so we're done"** — tests are necessary but not sufficient. Documentation, git state, and deferred-item honesty are equally important.
- **"This isn't meaningful" without verification** — dismissing an item because you think it's not worth doing is different from proving it isn't worth doing. Verify before dismissing.
- **Clean tree assumption** — never assume the working tree is clean. Run `git status --short` every time.
- **Stale branches in `git branch -a`** — remote-tracking refs persist even after the branch is gone. `git remote prune origin` is your friend.
- **Unpushed commits** — `git log origin/main..main` shows what hasn't been pushed. Easy to forget after a long session.

### Verification checklist

- [ ] Test suite passes with exact count: ______ suites, ______ tests
- [ ] tsc --noEmit: 0 errors
- [ ] README counts match actual test metrics
- [ ] PLAN.md/ROADMAP.md status is accurate
- [ ] Working tree clean
- [ ] On correct branch and pushed to origin
- [ ] Stale branches pruned
- [ ] Deferred items re-examined and documented honestly
- [ ] Decision to declare complete is based on evidence, not convenience

## Feature Flag Strategy

Ship behind feature flags to decouple deployment from release:

```typescript
// Feature flag check
const flags = await getFeatureFlags(userId);

if (flags.taskSharing) {
  // New feature: task sharing
  return <TaskSharingPanel task={task} />;
}

// Default: existing behavior
return null;
```

**Feature flag lifecycle:**

```
1. DEPLOY with flag OFF     → Code is in production but inactive
2. ENABLE for team/beta     → Internal testing in production environment
3. GRADUAL ROLLOUT          → 5% → 25% → 50% → 100% of users
4. MONITOR at each stage    → Watch error rates, performance, user feedback
5. CLEAN UP                 → Remove flag and dead code path after full rollout
```

**Rules:**
- Every feature flag has an owner and an expiration date
- Clean up flags within 2 weeks of full rollout
- Don't nest feature flags (creates exponential combinations)
- Test both flag states (on and off) in CI

## Staged Rollout

### The Rollout Sequence

```
1. DEPLOY to staging
   └── Full test suite in staging environment
   └── Manual smoke test of critical flows

2. DEPLOY to production (feature flag OFF)
   └── Verify deployment succeeded (health check)
   └── Check error monitoring (no new errors)

3. ENABLE for team (flag ON for internal users)
   └── Team uses the feature in production
   └── 24-hour monitoring window

4. CANARY rollout (flag ON for 5% of users)
   └── Monitor error rates, latency, user behavior
   └── Compare metrics: canary vs. baseline
   └── 24-48 hour monitoring window
   └── Advance only if all thresholds pass (see table below)

5. GRADUAL increase (25% -> 50% -> 100%)
   └── Same monitoring at each step
   └── Ability to roll back to previous percentage at any point

6. FULL rollout (flag ON for all users)
   └── Monitor for 1 week
   └── Clean up feature flag
```

### Dry-Run and Observation Periods for Data-Modifying Tools

When deploying a tool or script that modifies user data (archives email, deletes files, bulk-updates records, etc.):

- **Always start in dry-run / log-only mode** — the tool records what it WOULD do without actually doing it. Agree on the observation period upfront (24h recommended as starting point).
- **Do not skip to live mode** without explicit sign-off from the user or orchestrator after reviewing dry-run logs. Even a well-tested tool deserves an observation buffer before touching real data.
- **Config-driven safety** — the dry-run/live toggle belongs in a config file (`dry_run: true/false`), not in code. Flip modes without redeploying.
- **If an agent built the tool**, the orchestrator verifies the mode BEFORE the first scheduled execution. Do not assume the agent set the right mode — check.
- **Document the observation period** in the relevant kanban card so the team knows when review is due.
- **Logs during dry-run** should include the same detail as live runs (what would be modified, counts, patterns matched) so the review is meaningful.

**Pitfall — skipping the agreed process:** When orchestrator and user agree on a phased rollout ("24h dry run first"), every agent executing the work must respect that. Running live mutations during the observation period undermines trust regardless of outcome. If a worker agent attempts to skip ahead, the orchestrator catches it and enforces the process.

**Pitfall — "dry-run passed, ship it":** Running successfully in dry-run proves the tool doesn't crash. It doesn't mean the user is ready for real mutations. Respect the agreed window.

### Rollout Decision Thresholds

Treat these as example defaults. Tune thresholds per project, audience, and risk profile when deciding whether to advance, hold, or roll back at each stage:

| Metric | Advance (green) | Hold and investigate (yellow) | Roll back (red) |
|--------|-----------------|-------------------------------|-----------------|
| Error rate | Within 10% of baseline | 10-100% above baseline | >2x baseline |
| P95 latency | Within 20% of baseline | 20-50% above baseline | >50% above baseline |
| Client JS errors | No new error types | New errors at <0.1% of sessions | New errors at >0.1% of sessions |
| Business metrics | Neutral or positive | Decline <5% (may be noise) | Decline >5% |

### When to Roll Back

Roll back immediately if:
- Error rate increases by more than 2x baseline
- P95 latency increases by more than 50%
- User-reported issues spike
- Data integrity issues detected
- Security vulnerability discovered

## Monitoring and Observability

### What to Monitor

```
Application metrics:
├── Error rate (total and by endpoint)
├── Response time (p50, p95, p99)
├── Request volume
├── Active users
└── Key business metrics (conversion, engagement)

Infrastructure metrics:
├── CPU and memory utilization
├── Database connection pool usage
├── Disk space
├── Network latency
└── Queue depth (if applicable)

Client metrics:
├── Core Web Vitals (LCP, INP, CLS)
├── JavaScript errors
├── API error rates from client perspective
└── Page load time
```

### Error Reporting

```typescript
// Set up error boundary with reporting
class ErrorBoundary extends React.Component {
  componentDidCatch(error: Error, info: React.ErrorInfo) {
    // Report to error tracking service
    reportError(error, {
      componentStack: info.componentStack,
      userId: getCurrentUser()?.id,
      page: window.location.pathname,
    });
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback onRetry={() => this.setState({ hasError: false })} />;
    }
    return this.props.children;
  }
}

// Server-side error reporting
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  reportError(err, {
    method: req.method,
    url: req.url,
    userId: req.user?.id,
  });

  // Don't expose internals to users
  res.status(500).json({
    error: { code: 'INTERNAL_ERROR', message: 'Something went wrong' },
  });
});
```

### Post-Launch Verification

In the first hour after launch:

```
1. Check health endpoint returns 200
2. Check error monitoring dashboard (no new error types)
3. Check latency dashboard (no regression)
4. Test the critical user flow manually
5. Verify logs are flowing and readable
6. Confirm rollback mechanism works (dry run if possible)
```

## Rollback Strategy

Every deployment needs a rollback plan before it happens:

```markdown
## Rollback Plan for [Feature/Release]

### Trigger Conditions
- Error rate > 2x baseline
- P95 latency > [X]ms
- User reports of [specific issue]

### Rollback Steps
1. Disable feature flag (if applicable)
   OR
1. Deploy previous version: `git revert <commit> && git push`
2. Verify rollback: health check, error monitoring
3. Communicate: notify team of rollback

### Database Considerations
- Migration [X] has a rollback: `npx prisma migrate rollback`
- Data inserted by new feature: [preserved / cleaned up]

### Time to Rollback
- Feature flag: < 1 minute
- Redeploy previous version: < 5 minutes
- Database rollback: < 15 minutes
```
## See Also

- For security pre-launch checks, see `../../references/security-checklist.md`
- For performance pre-launch checklist, see `../../references/performance-checklist.md`
- For accessibility verification before launch, see `../../references/accessibility-checklist.md`
- For Cloudflare Pages + GitHub deployment setup, see `references/cloudflare-pages-deployment.md`

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It works in staging, it'll work in production" | Production has different data, traffic patterns, and edge cases. Monitor after deploy. |
| "We don't need feature flags for this" | Every feature benefits from a kill switch. Even "simple" changes can break things. |
| "Monitoring is overhead" | Not having monitoring means you discover problems from user complaints instead of dashboards. |
| "We'll add monitoring later" | Add it before launch. You can't debug what you can't see. |
| "Rolling back is admitting failure" | Rolling back is responsible engineering. Shipping a broken feature is the failure. |

## Red Flags

- Deploying without a rollback plan
- No monitoring or error reporting in production
- Big-bang releases (everything at once, no staging)
- Feature flags with no expiration or owner
- No one monitoring the deploy for the first hour
- Production environment configuration done by memory, not code
- "It's Friday afternoon, let's ship it"

## Verification

Before deploying:

- [ ] Pre-launch checklist completed (all sections green)
- [ ] Feature flag configured (if applicable)
- [ ] Rollback plan documented
- [ ] Monitoring dashboards set up
- [ ] Team notified of deployment

After deploying:

- [ ] Health check returns 200
- [ ] Error rate is normal
- [ ] Latency is normal
- [ ] Critical user flow works
- [ ] Logs are flowing
- [ ] Rollback tested or verified ready
