---
name: vendor-risk-assessment
description: Use when integrating third-party services, APIs, SDKs, or SaaS platforms to evaluate their security posture, compliance certifications, data handling practices, and operational reliability before adoption.
invoke_when: Use when adding a third-party API integration, evaluating a SaaS platform, connecting to external payment processors, adopting a BaaS/PaaS provider, or reviewing existing vendor integrations for compliance.
---

# Vendor Risk Assessment

## Core Rule

**Every third-party integration is a trust boundary extension.** When you integrate a vendor's API, SDK, or service, their security posture becomes part of your security posture. Assess before adopting.

## Risk Assessment Framework

### Tier 1: Critical Vendors (Data Processors)

Vendors that process, store, or have access to your users' data:

| Category | Examples | Risk Level |
|----------|---------|------------|
| Authentication providers | Auth0, Okta, Firebase Auth, Clerk | Critical |
| Payment processors | Stripe, Braintree, Adyen | Critical |
| Database services | PlanetScale, Supabase, MongoDB Atlas | Critical |
| Email services (with user data) | SendGrid, Postmark, Mailgun | Critical |
| Analytics with PII | Mixpanel, Amplitude (if tracking PII) | Critical |
| AI/ML APIs (with user data) | OpenAI, Anthropic, Google AI (if sending user content) | Critical |

**Required before adoption:**
- [ ] SOC 2 Type II report available and current (within 12 months)
- [ ] Data Processing Agreement (DPA) signed
- [ ] GDPR compliance documented (if EU users)
- [ ] Data residency options (can data stay in required region?)
- [ ] Breach notification SLA defined (72 hours for GDPR)
- [ ] Subprocessor list available and reviewed
- [ ] Data deletion API available (for GDPR right to erasure)
- [ ] Encryption at rest and in transit confirmed

### Tier 2: Operational Vendors (Infrastructure)

Vendors that affect availability but do not process user data directly:

| Category | Examples | Risk Level |
|----------|---------|------------|
| CDN / Edge | Cloudflare, Fastly, Vercel | High |
| Monitoring / APM | Datadog, New Relic, Sentry | High |
| CI/CD | GitHub Actions, CircleCI, Buildkite | High |
| DNS | Cloudflare DNS, Route 53, DNSimple | High |
| Feature flags | LaunchDarkly, Unleash, Flagsmith | High |

**Required before adoption:**
- [ ] SLA documented (99.9%+ for production dependencies)
- [ ] Status page available (public incident history)
- [ ] Fallback/degradation strategy defined (what happens when this vendor is down?)
- [ ] Secret management (how are API keys rotated?)
- [ ] No vendor lock-in without escape hatch (data export, standard protocols)

### Tier 3: Development Vendors (Tooling)

Vendors used in development but not in production:

| Category | Examples | Risk Level |
|----------|---------|------------|
| Code hosting | GitHub, GitLab, Bitbucket | Medium |
| Package registries | npm, PyPI, crates.io | Medium |
| Development tools | Figma, Linear, Notion | Low |

**Required before adoption:**
- [ ] Supply chain attack surface understood (see `shipworthy:supply-chain-security`)
- [ ] Access controls configured (least privilege)
- [ ] SSO/SAML available for team accounts

## Integration Security Checklist

When writing code that integrates with any vendor:

### API Key Management
```typescript
// BAD — key in source code
const client = new VendorSDK({ apiKey: 'sk-live-abc123' });

// GOOD — key from environment, validated at startup
const apiKey = process.env.VENDOR_API_KEY;
if (!apiKey) throw new Error('VENDOR_API_KEY is required');
const client = new VendorSDK({ apiKey });
```

### Request/Response Validation
```typescript
// GOOD — validate vendor responses, do not trust blindly
const vendorResponse = await client.getUser(userId);
const validated = VendorUserSchema.safeParse(vendorResponse);
if (!validated.success) {
  logger.error({ error: validated.error }, 'Vendor response schema mismatch');
  throw new Error('Unexpected vendor response format');
}
```

### Circuit Breaker Pattern
```typescript
// GOOD — vendor failures should not cascade
const circuitBreaker = new CircuitBreaker(vendorClient.call, {
  timeout: 5000,           // 5s timeout per request
  errorThresholdPercentage: 50,
  resetTimeout: 30000,     // 30s before retrying
});

// Fallback when vendor is unavailable
circuitBreaker.fallback(() => cachedResponse ?? DEFAULT_RESPONSE);
```

### Data Minimization
```typescript
// BAD — sending full user object to vendor
await analytics.track({ user: fullUserObject });

// GOOD — send only what the vendor needs
await analytics.track({
  userId: user.id,           // pseudonymous ID
  event: 'page_view',
  properties: { page: '/home' },
  // NO: email, name, IP, or other PII
});
```

### Webhook Verification
```typescript
// GOOD — always verify webhook signatures
app.post('/webhooks/vendor', (req, res) => {
  const signature = req.headers['x-vendor-signature'];
  const isValid = verifyHmac(
    req.rawBody,
    signature,
    process.env.VENDOR_WEBHOOK_SECRET
  );

  if (!isValid) {
    logger.warn('Invalid webhook signature — possible tampering');
    return res.status(401).json({ error: 'Invalid signature' });
  }

  // Process verified webhook...
});
```

## Vendor Failure Planning

For every vendor integration, document:

| Question | Required Answer |
|---------|----------------|
| What happens if this vendor is down for 1 hour? | Graceful degradation strategy |
| What happens if this vendor is down for 24 hours? | Fallback or manual process |
| What happens if this vendor is breached? | Incident response: rotate keys, assess data exposure |
| What happens if this vendor shuts down? | Migration plan to alternative (data export, API compatibility) |
| What happens if this vendor raises prices 10x? | Budget impact; alternative evaluation |
| What is the vendor's data deletion timeline? | Must meet your GDPR/compliance requirements |

## Vendor Review Cadence

| Vendor Tier | Review Frequency | Trigger for Off-Cycle Review |
|------------|-----------------|------------------------------|
| Critical | Quarterly | Breach disclosure, SOC 2 expiry, major version change |
| Operational | Semi-annually | SLA violation, major outage, pricing change |
| Development | Annually | Security incident, team access changes |

## Code Review Checklist

- [ ] Vendor API keys stored in environment variables, not source code
- [ ] Vendor responses validated against a schema (do not trust blindly)
- [ ] Circuit breaker or timeout configured for all vendor API calls
- [ ] Data sent to vendor minimized (no unnecessary PII)
- [ ] Webhook signatures verified for all incoming vendor webhooks
- [ ] Fallback behavior defined for vendor unavailability
- [ ] Vendor's compliance certifications match your requirements
- [ ] Data Processing Agreement signed (for data-processing vendors)
- [ ] Vendor added to project's vendor inventory with tier classification
