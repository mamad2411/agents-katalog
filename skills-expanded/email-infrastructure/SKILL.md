---
name: email-infrastructure
description: Email delivery infrastructure - DNS authentication (SPF/DKIM/DMARC), subdomain isolation, provider abstraction, template systems, bounce handling, warmup strategy, and deliverability monitoring.
---

# Email Infrastructure

Production email delivery requires DNS authentication, domain isolation, and provider-agnostic architecture. A single misconfiguration can land your entire domain in spam.

## GOOD vs BAD: Domain Strategy

```
BAD:  Send bulk marketing from example.com
      → Spam complaints tank your main domain reputation
      → Transactional emails (password reset, receipts) start landing in spam
      → Recovery takes weeks of warmup

GOOD: Subdomain isolation with separate reputations
      → mail.example.com        for transactional (password reset, receipts, 2FA)
      → notify.example.com      for product notifications (comments, mentions)
      → marketing.example.com   for bulk campaigns (newsletters, promotions)
      → Each subdomain has independent reputation — one bad campaign does not poison the rest
```

## DNS Authentication: SPF + DKIM + DMARC

```
# SPF — declare which servers can send from your domain
mail.example.com     TXT  "v=spf1 include:_spf.provider.com ~all"

# DKIM — cryptographic signature on every email
selector._domainkey.mail.example.com  TXT  "v=DKIM1; k=rsa; p=MIGf..."

# DMARC — policy for failed authentication (progressive rollout)
# Week 1-2: monitor only
_dmarc.mail.example.com  TXT  "v=DMARC1; p=none; rua=mailto:dmarc@example.com"

# Week 3-4: quarantine suspicious emails
_dmarc.mail.example.com  TXT  "v=DMARC1; p=quarantine; pct=25; rua=mailto:dmarc@example.com"

# Week 5+: reject after confidence builds
_dmarc.mail.example.com  TXT  "v=DMARC1; p=reject; rua=mailto:dmarc@example.com"
```

Never jump straight to `p=reject`. The progressive rollout catches misconfigurations before they block legitimate mail.

## Email Provider Abstraction

```typescript
// Swap Resend, SES, Postmark, or Mailgun without touching business logic

interface EmailProvider {
  send(message: EmailMessage): Promise<EmailResult>
  sendBatch(messages: EmailMessage[]): Promise<EmailResult[]>
}

interface EmailMessage {
  from: string
  to: string | string[]
  subject: string
  html: string
  text?: string
  replyTo?: string
  headers?: Record<string, string>
  tags?: Record<string, string>
}

interface EmailResult {
  id: string
  status: 'sent' | 'queued' | 'failed'
  error?: string
}

// Factory selects provider from config — no hardcoded vendor
function createEmailProvider(config: { provider: string }): EmailProvider {
  switch (config.provider) {
    case 'resend':    return new ResendProvider()
    case 'ses':       return new SESProvider()
    case 'postmark':  return new PostmarkProvider()
    default:          throw new Error(`Unknown email provider: ${config.provider}`)
  }
}
```

## Transactional vs Marketing Separation

```typescript
interface EmailService {
  sendTransactional(message: EmailMessage): Promise<EmailResult>
  sendMarketing(message: EmailMessage): Promise<EmailResult>
}

class ProductionEmailService implements EmailService {
  constructor(
    private transactional: EmailProvider,  // high-deliverability provider
    private marketing: EmailProvider       // bulk-optimized provider
  ) {}

  async sendTransactional(message: EmailMessage): Promise<EmailResult> {
    // Transactional: password reset, receipts, 2FA — must arrive instantly
    // Use mail.example.com subdomain, high-priority provider
    return this.transactional.send({
      ...message,
      from: `noreply@mail.example.com`,
      headers: { 'X-Priority': '1' }
    })
  }

  async sendMarketing(message: EmailMessage): Promise<EmailResult> {
    // Marketing: newsletters, promotions — rate-limited, includes unsubscribe
    // Use marketing.example.com subdomain, bulk provider
    return this.marketing.send({
      ...message,
      from: `hello@marketing.example.com`,
      headers: { 'List-Unsubscribe': `<https://example.com/unsubscribe>` }
    })
  }
}
```

## Template System (MJML)

```typescript
// MJML compiles to responsive HTML that works across all email clients
// Compile at build time, not runtime

import mjml2html from 'mjml'

const mjmlTemplate = `
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="system-ui, -apple-system, sans-serif" />
      <mj-text font-size="16px" line-height="1.5" color="#1a1a1a" />
    </mj-attributes>
    <mj-style>
      @media (prefers-color-scheme: dark) {
        .dark-bg { background-color: #1a1a1a !important; }
        .dark-text { color: #e5e5e5 !important; }
      }
    </mj-style>
  </mj-head>
  <mj-body>
    <mj-section css-class="dark-bg">
      <mj-column>
        <mj-text css-class="dark-text">Hello {{name}},</mj-text>
        <mj-text css-class="dark-text">{{body}}</mj-text>
        <mj-button href="{{actionUrl}}" background-color="#2563eb">
          {{actionLabel}}
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
`

function escapeHtml(str: string): string {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
}

function compileTemplate(mjml: string, vars: Record<string, string>): string {
  let compiled = mjml
  for (const [key, value] of Object.entries(vars)) {
    compiled = compiled.replaceAll(`{{${key}}}`, escapeHtml(value))
  }
  const { html, errors } = mjml2html(compiled)
  if (errors.length > 0) {
    throw new Error(`MJML compilation errors: ${errors.map(e => e.message).join(', ')}`)
  }
  return html
}
```

## Bounce and Complaint Handling

```typescript
// Webhook handler for provider callbacks (bounces, complaints, deliveries)

interface BounceEvent {
  type: 'bounce' | 'complaint' | 'delivery'
  email: string
  reason?: string
  timestamp: string
}

async function handleEmailWebhook(event: BounceEvent): Promise<void> {
  switch (event.type) {
    case 'bounce':
      // Hard bounce: address does not exist — never send again
      await db.emailSuppression.upsert({
        where: { email: event.email },
        create: { email: event.email, reason: 'hard_bounce', suppressedAt: new Date() },
        update: { reason: 'hard_bounce', suppressedAt: new Date() }
      })
      break

    case 'complaint':
      // Spam complaint: user marked as spam — suppress immediately
      await db.emailSuppression.upsert({
        where: { email: event.email },
        create: { email: event.email, reason: 'complaint', suppressedAt: new Date() },
        update: { reason: 'complaint', suppressedAt: new Date() }
      })
      // Alert if complaint rate exceeds 0.1% (ISP threshold)
      await checkComplaintRate()
      break

    case 'delivery':
      await db.emailLog.update({
        where: { email: event.email },
        data: { deliveredAt: new Date() }
      })
      break
  }
}

// Always check suppression list before sending
async function isSuppressed(email: string): Promise<boolean> {
  const entry = await db.emailSuppression.findUnique({ where: { email } })
  return entry !== null
}
```

## Domain Warmup Strategy

```
New domain/IP starts with zero reputation. Send too fast and ISPs block you.

Week 1:     50 emails/day   → Send to your most engaged users only
Week 2:    200 emails/day   → Expand to users who opened in last 30 days
Week 3:    500 emails/day   → Include 90-day active users
Week 4:  1,000 emails/day   → General audience, monitor bounce rate
Week 5:  5,000 emails/day   → Scale up if bounce < 2% and complaints < 0.1%
Week 6: 10,000 emails/day   → Full volume if metrics stay clean
Week 8+: Full send           → Maintain list hygiene going forward

CRITICAL THRESHOLDS:
  Bounce rate  > 5%   → STOP sending, clean your list
  Complaint rate > 0.1% → STOP sending, review content and targeting
  Open rate    < 10%  → Re-evaluate subject lines and audience
```

## Deliverability Monitoring

```typescript
interface DeliverabilityMetrics {
  sent: number
  delivered: number
  bounced: number
  complained: number
  opened: number
  clicked: number
}

async function getDailyMetrics(date: string): Promise<DeliverabilityMetrics> {
  const metrics = await db.emailLog.aggregate({
    where: { sentAt: { gte: new Date(date), lt: new Date(date + 'T23:59:59Z') } },
    _count: { id: true },
    // Group by status for each metric
  })
  return metrics
}

async function checkHealthThresholds(metrics: DeliverabilityMetrics): Promise<void> {
  if (metrics.sent === 0) return

  const bounceRate = metrics.bounced / metrics.sent
  const complaintRate = metrics.complained / metrics.sent
  const deliveryRate = metrics.delivered / metrics.sent

  if (bounceRate > 0.05) {
    await alertOps('Bounce rate critical', `${(bounceRate * 100).toFixed(1)}% — pause sending`)
  }
  if (complaintRate > 0.001) {
    await alertOps('Complaint rate critical', `${(complaintRate * 100).toFixed(2)}% — review content`)
  }
  if (deliveryRate < 0.95) {
    await alertOps('Delivery rate low', `${(deliveryRate * 100).toFixed(1)}% — check DNS and reputation`)
  }
}
```

## Pre-Send Checklist

```
Before every send, verify:
  1. Recipient is not on suppression list (bounces + complaints)
  2. SPF/DKIM/DMARC records are valid for the sending subdomain
  3. Unsubscribe link is present (CAN-SPAM, GDPR requirement)
  4. Plain text version exists alongside HTML
  5. From address matches the authenticated subdomain
  6. List-Unsubscribe header is set for bulk sends
  7. Subject line is not empty and under 78 characters
```

**Key principle**: Treat email infrastructure like a reputation system. Subdomain isolation protects your core domain. Progressive DMARC rollout catches issues before they block mail. Always check the suppression list before sending. Monitor bounce and complaint rates daily — by the time you notice spam folder placement, the damage is already done.
