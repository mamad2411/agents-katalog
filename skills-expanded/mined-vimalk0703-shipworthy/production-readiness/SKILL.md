---
name: production-readiness
description: Pre-launch checklist covering security, performance, reliability, legal, SEO, monitoring, backups, and custom domains. Each item has both a plain-language explanation and technical implementation detail. Ensures nothing critical is missed before going live.
invoke_when: Use when preparing to launch, deploying to production, going live, or evaluating whether an app is ready for production.
---

# Production Readiness

## How to Use This Checklist

Go through each section before your first production deployment. Items are marked:

- **MUST** — Do this before launch. Skipping it creates real risk (security holes, data loss, legal exposure).
- **SHOULD** — Do this within the first week. Your app works without it, but you're flying blind or leaving value on the table.
- **NICE** — Do this when you can. Improves quality of life but won't break anything if delayed.

---

## 1. Security Checklist

### MUST: Secrets Are in Environment Variables, Not in Code

**Plain language:** None of your passwords, API keys, or secret tokens should be written directly in your code files. They should be in your `.env` file (which never gets uploaded to GitHub) and set in your hosting provider's settings for the live site.

**Technical detail:**
- Grep your codebase for hardcoded secrets: `grep -r "sk_live\|sk_test\|password\|secret" --include="*.ts" --include="*.js" --include="*.tsx" --include="*.jsx" src/`
- Verify `.env` is in `.gitignore`
- Check git history for accidentally committed secrets: `git log --all --oneline -- .env`
- If secrets were ever committed, rotate ALL of them immediately
- Use `lib/env.ts` validation pattern (see environment-setup skill)

### MUST: Authentication Is Working Correctly

**Plain language:** People can sign up, log in, and log out. Pages that should be private (like dashboards or settings) can't be seen by someone who isn't logged in. If someone types in a URL for a page they shouldn't see, they get redirected to the login page.

**Technical detail:**
- Test login flow end-to-end (email/password and each social provider)
- Test logout clears session completely
- Verify middleware protects all private routes
- Test that API endpoints reject unauthenticated requests with 401
- Test that API endpoints reject unauthorized requests with 403
- Test password reset flow
- Verify session expiry works (sessions don't last forever)
- If using JWT: tokens have reasonable expiry (not 30 days)
- If using cookies: `httpOnly`, `secure`, `sameSite` flags are set

### MUST: Payments Go Through Stripe (or Equivalent) Properly

**Plain language:** If you're charging money, payments work correctly. Test with Stripe's test cards. Make sure customers get receipts. Make sure you get the money. Make sure refunds work.

**Technical detail:**
- Switch Stripe keys from `sk_test_` / `pk_test_` to `sk_live_` / `pk_live_`
- Verify webhook endpoint is configured for production URL
- Webhook signature verification is enabled (not skipping verification in production)
- Test with Stripe's test cards before switching to live: `4242 4242 4242 4242` (success), `4000 0000 0000 0002` (decline)
- Verify idempotency keys are used for payment creation
- Confirm webhook events are being processed: `checkout.session.completed`, `invoice.paid`, `customer.subscription.updated`, `customer.subscription.deleted`
- Error states handled: declined cards, expired cards, insufficient funds, network errors
- Receipts are sent (Stripe can do this automatically — enable in Dashboard > Settings)

### MUST: HTTPS Is Enforced

**Plain language:** Your site address starts with `https://` (with the padlock icon), not `http://`. This encrypts everything between your users and your site.

**Technical detail:**
- If using Vercel, Netlify, or Railway: HTTPS is automatic. You're already done.
- If self-hosting: configure SSL/TLS certificates (Let's Encrypt is free)
- Redirect all HTTP requests to HTTPS
- Set `Strict-Transport-Security` header
- All API calls use HTTPS URLs (no mixed content)

### SHOULD: Rate Limiting on Auth Endpoints

**Plain language:** If someone tries to guess passwords by trying thousands of combinations rapidly, your app slows them down after a few attempts.

**Technical detail:**
- Implement rate limiting on `/api/auth/*` endpoints
- Suggested limits: 5 login attempts per minute per IP, 3 password reset requests per hour per email
- Use a library like `rate-limiter-flexible` or Vercel's Edge rate limiting
- Return 429 status code with `Retry-After` header

### SHOULD: Input Validation and Sanitization

**Plain language:** When users type things into forms, your app checks that the input makes sense (email looks like an email, numbers are actually numbers) and removes anything dangerous before saving it.

**Technical detail:**
- Validate all user input on the server side (client validation is for UX, not security)
- Use Zod schemas for request body validation on all API endpoints
- Sanitize HTML input if accepting rich text (use DOMPurify or similar)
- Parameterized database queries (Supabase/Prisma handle this, but verify raw queries)
- File uploads: validate file type, enforce size limits, don't trust client-provided filenames

---

## 2. Performance Checklist

### MUST: Images Are Optimized

**Plain language:** Large, unoptimized photos make your site load slowly — especially on phones. Your images should be compressed and sized appropriately.

**Technical detail:**
- Use Next.js `<Image>` component (automatic optimization, lazy loading, responsive sizing)
- Serve images in modern formats (WebP/AVIF) — Next.js Image handles this automatically
- Set explicit `width` and `height` on images to prevent layout shift
- For hero images or above-the-fold content: add `priority` prop
- Compress uploaded images before storage (consider a service like Cloudinary or imgix)
- Maximum image size guideline: hero images under 200KB, content images under 100KB

### SHOULD: Lazy Loading Is Implemented

**Plain language:** Your site only loads what's visible on screen. Content further down the page loads as the user scrolls to it. This makes the initial page load much faster.

**Technical detail:**
- Use `next/dynamic` for heavy components that aren't immediately visible
- Native lazy loading on images: `loading="lazy"` (Next.js Image does this automatically)
- Code split routes (Next.js App Router does this automatically)
- Defer loading of third-party scripts (analytics, chat widgets): use `next/script` with `strategy="lazyOnload"`
- Check bundle size: `npx next build` shows page sizes. Flag any page over 200KB

### SHOULD: API Responses Are Fast

**Plain language:** When someone clicks a button or loads a page, they shouldn't wait more than a second or two. If your site feels slow, people leave.

**Technical detail:**
- Target: API responses under 200ms for simple queries, under 1s for complex operations
- Add database indexes for frequently queried columns
- Use `select()` to fetch only needed columns (don't `SELECT *`)
- Implement pagination for list endpoints (never return unlimited results)
- Cache frequently-read, rarely-changed data (React Server Components cache by default in Next.js)
- Monitor with Vercel Analytics (built-in) or a custom timing solution

---

## 3. Reliability Checklist

### SHOULD: Error Tracking Is Set Up

**Plain language:** When something goes wrong on your live site, you need to know about it immediately — not when a user emails you. An error tracking service catches errors and notifies you.

**Technical detail:**
- Recommended: [Sentry](https://sentry.io) (free tier: 5K errors/month)
- Install: `npx @sentry/wizard@latest -i nextjs`
- Configure source maps for readable stack traces
- Set up alert rules: email/Slack notification on new errors
- Add user context to errors (user ID, not PII) for debugging
- Test that errors are captured: throw a test error, verify it appears in Sentry dashboard
- Alternative: [LogRocket](https://logrocket.com) (session replay + error tracking)

### SHOULD: Health Check Endpoint Exists

**Plain language:** A simple page on your site that monitoring tools can check every few minutes to make sure your site is still running. If it stops responding, you get alerted.

**Technical detail:**
- Create `app/api/health/route.ts`:
```typescript
export async function GET() {
  try {
    // Check database connection
    // await db.query('SELECT 1');
    return Response.json({ status: 'healthy', timestamp: new Date().toISOString() });
  } catch (error) {
    return Response.json({ status: 'unhealthy', error: 'Database connection failed' }, { status: 503 });
  }
}
```
- Health check should verify critical dependencies (database, cache)
- Return 200 for healthy, 503 for unhealthy
- Keep it fast (under 100ms) — don't run expensive checks

### SHOULD: Meaningful Logging Is in Place

**Plain language:** Your app keeps a record of important things that happen — who signed up, what payments were processed, what errors occurred. When something goes wrong, these logs help you figure out what happened.

**Technical detail:**
- No `console.log` in production — use structured logging
- Log important events: user signup, payment processed, subscription changed, error occurred
- Include context: user ID (not email/PII), request ID, timestamp
- Use Vercel's built-in logging (Vercel > Project > Logs) or a service like Axiom/Datadog
- Log levels: `error` (something broke), `warn` (something unexpected), `info` (important business event)

---

## 4. Legal/Compliance Checklist

### MUST: Privacy Policy Exists

**Plain language:** A page on your site that tells users what data you collect, why you collect it, and what you do with it. This is legally required in most jurisdictions if you collect any personal information (emails, names, payment info).

**Technical detail:**
- Create a `/privacy` page
- Cover: what data you collect, why, how it's stored, how users can request deletion
- If you use analytics (Google Analytics, Plausible), disclose it
- If you process payments, note that Stripe handles card data (you don't store it)
- Free generator: [Termly](https://termly.io) or [PrivacyPolicies.com](https://privacypolicies.com) — customize the generated policy to be accurate
- Link to it from your footer on every page
- Link to it from your sign-up form

### MUST: Terms of Service Exists (If Charging Money)

**Plain language:** If you're selling something, you need a page that covers the rules — what users get, refund policy, what's not allowed, limitation of liability. This protects you legally.

**Technical detail:**
- Create a `/terms` page
- Cover: service description, acceptable use, payment terms, refund policy, liability limitations
- Required before you start charging money
- Link from footer and checkout page
- Free generator: [Termly](https://termly.io) — customize for your specific product

### SHOULD: Cookie Consent (If Serving EU Users)

**Plain language:** If people from Europe use your site and you use cookies for analytics or tracking, you need to show a banner asking for their permission. This is required by GDPR/ePrivacy law.

**Technical detail:**
- Required if you: use Google Analytics, run ads, use tracking pixels, or set non-essential cookies
- NOT required for: essential cookies (session cookies, auth tokens, CSRF tokens)
- Simple implementation: cookie consent banner that blocks analytics until accepted
- Libraries: `cookie-consent-banner` or build a simple one
- Store consent preference in a cookie (ironic but correct)
- Respect "Do Not Track" browser settings
- If you use Plausible Analytics (privacy-focused), you may not need a cookie banner since Plausible is cookieless

---

## 5. SEO Checklist

### SHOULD: Meta Tags Are Set

**Plain language:** When someone shares your site on social media or finds it on Google, the title, description, and image that appear are controlled by meta tags. Without them, your links look blank and unprofessional.

**Technical detail:**
- Set in `app/layout.tsx` or per-page:
```typescript
export const metadata = {
  title: 'Your App Name',
  description: 'One sentence describing what your app does',
  openGraph: {
    title: 'Your App Name',
    description: 'One sentence describing what your app does',
    url: 'https://yourapp.com',
    siteName: 'Your App Name',
    images: [{ url: 'https://yourapp.com/og-image.png', width: 1200, height: 630 }],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Your App Name',
    description: 'One sentence describing what your app does',
    images: ['https://yourapp.com/og-image.png'],
  },
};
```
- Test with: [opengraph.xyz](https://opengraph.xyz) (shows how your link looks when shared)

### SHOULD: OG Image Exists

**Plain language:** The preview image that shows when someone shares your link on Twitter, LinkedIn, Slack, or iMessage. A good image makes people more likely to click.

**Technical detail:**
- Size: 1200x630 pixels (standard OG image size)
- Create with: Figma, Canva, or programmatically with `@vercel/og`
- Include: app name, brief tagline, branded visuals
- Save as `public/og-image.png`
- Test by sharing your URL in Slack or using [opengraph.xyz](https://opengraph.xyz)

### NICE: Sitemap and robots.txt

**Plain language:** Files that tell Google which pages on your site exist and which ones it should index. Helps your site appear in search results.

**Technical detail:**
- Sitemap: Create `app/sitemap.ts`:
```typescript
export default function sitemap() {
  return [
    { url: 'https://yourapp.com', lastModified: new Date() },
    { url: 'https://yourapp.com/pricing', lastModified: new Date() },
    // Add all public pages
  ];
}
```
- Robots.txt: Create `app/robots.ts`:
```typescript
export default function robots() {
  return {
    rules: { userAgent: '*', allow: '/', disallow: ['/api/', '/dashboard/'] },
    sitemap: 'https://yourapp.com/sitemap.xml',
  };
}
```
- Submit sitemap to Google Search Console after launch

---

## 6. Monitoring Checklist

### SHOULD: Uptime Monitoring Is Configured

**Plain language:** A service that checks your site every few minutes and texts/emails you if it goes down. You'll know about problems before your users do.

**Technical detail:**
- Free options:
  - [Better Stack (formerly Better Uptime)](https://betterstack.com) — free tier: 5 monitors, email + Slack alerts
  - [UptimeRobot](https://uptimerobot.com) — free tier: 50 monitors, 5-minute intervals
- Configure to check your `/api/health` endpoint every 5 minutes
- Set up alert channels: email (minimum), Slack or SMS (recommended)
- Monitor both the main URL and the health endpoint
- Set expected response: HTTP 200, response time under 5 seconds

---

## 7. Backup Checklist

### MUST: Database Backups Are Configured

**Plain language:** If your database breaks, gets corrupted, or you accidentally delete important data, backups let you restore everything. Without backups, data loss is permanent.

**Technical detail:**
- **Supabase:** Automatic daily backups on Pro plan. Free plan: export manually via Dashboard > Database > Backups. Consider upgrading to Pro ($25/mo) before launch for automatic backups.
- **PlanetScale:** Automatic daily backups included.
- **Self-hosted Postgres:** Configure `pg_dump` cron job, store backups in S3/R2.
- Test restore procedure BEFORE you need it (a backup you can't restore is not a backup)
- For critical data: consider Point-in-Time Recovery (Supabase Pro includes this)

### SHOULD: Backup Verification

**Plain language:** Periodically check that your backups actually work by restoring one to a test environment. Backups that silently fail are worse than no backups because you think you're safe.

**Technical detail:**
- Monthly: download a backup and verify it's not empty/corrupted
- Quarterly: restore a backup to a test database and verify data integrity
- Document the restore procedure so anyone on the team can do it in an emergency

---

## 8. Custom Domain Checklist

### SHOULD: Custom Domain Is Connected

**Plain language:** Your app runs on `your-app.vercel.app` by default. To use `yourapp.com`, you need to buy a domain and point it at your hosting.

**Technical detail:**

**Step 1: Buy a domain**
- Recommended registrars: [Namecheap](https://namecheap.com), [Cloudflare Registrar](https://www.cloudflare.com/products/registrar/) (cheapest renewals), [Google Domains](https://domains.google)
- Cost: $10-15/year for a .com

**Step 2: Configure DNS (Vercel example)**
1. In Vercel: go to your project > Settings > Domains
2. Add your domain (e.g., `yourapp.com`)
3. Vercel will show you DNS records to add
4. Go to your domain registrar's DNS settings
5. Add the records Vercel provides:
   - Type: `A`, Name: `@`, Value: `76.76.21.21`
   - Type: `CNAME`, Name: `www`, Value: `cname.vercel-dns.com`
6. Wait 5-30 minutes for DNS to propagate
7. Vercel automatically provisions an SSL certificate (HTTPS)

**Step 3: Verify**
- Visit `https://yourapp.com` — should load your app with HTTPS
- Visit `http://yourapp.com` — should redirect to HTTPS
- Visit `https://www.yourapp.com` — should redirect to `yourapp.com` (or vice versa, pick one canonical URL)

**Troubleshooting:**
- "DNS not configured" — wait 30 minutes, DNS propagation takes time
- "SSL certificate pending" — usually resolves in 10 minutes
- Use [dnschecker.org](https://dnschecker.org) to verify DNS records are propagating

---

## Pre-Launch Final Checklist

Run through this condensed list before clicking "deploy to production":

### Security (MUST)
- [ ] All secrets in environment variables (not in code)
- [ ] `.env` is in `.gitignore`
- [ ] Production environment variables set in hosting provider
- [ ] Auth flows tested (sign up, log in, log out, protected routes)
- [ ] Payments tested with Stripe test cards
- [ ] HTTPS enforced

### Functionality (MUST)
- [ ] All critical user flows tested end-to-end
- [ ] Error pages exist (404, 500)
- [ ] Forms validate input and show clear error messages
- [ ] Email sending works (test welcome email, password reset)

### Performance (SHOULD)
- [ ] Images optimized
- [ ] Build completes without errors
- [ ] Page load feels fast on mobile

### Legal (MUST if charging money)
- [ ] Privacy policy page exists and is linked
- [ ] Terms of service page exists and is linked
- [ ] Cookie consent banner (if serving EU users with tracking)

### SEO (SHOULD)
- [ ] Page title and meta description set
- [ ] OG image created and configured
- [ ] Sitemap generated

### Monitoring (SHOULD)
- [ ] Error tracking set up (Sentry)
- [ ] Uptime monitoring configured
- [ ] Health check endpoint exists

### Data (MUST)
- [ ] Database backups configured
- [ ] Backup restore procedure tested

### Domain (SHOULD)
- [ ] Custom domain connected
- [ ] HTTPS working on custom domain
- [ ] www redirect configured
