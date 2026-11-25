---
name: cookie-policy
description: "Writes cookie consent policies with category descriptions, opt-out mechanisms, and GDPR/CCPA compliance. Use when creating or updating your website's cookie policy."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Cookie Policy

## When to Use This Skill

Use this skill when you need to:
- Create a cookie policy for your website
- Describe cookie categories and their purposes for visitors
- Comply with GDPR, CCPA, or ePrivacy cookie consent requirements
- Design opt-in/opt-out mechanisms for different cookie types

**DO NOT** use this skill for full privacy policies, data processing agreements, or technical cookie implementation. This is for the cookie policy document itself.

---

## Core Principle

A COOKIE POLICY MUST BE TRANSPARENT, SPECIFIC, AND ACTIONABLE — VISITORS SHOULD UNDERSTAND WHAT COOKIES DO AND HAVE GENUINE CONTROL OVER THEM.

---

## Phase 1: Cookie Audit

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Website URL** | "What is your website?" | No default — must be provided |
| **Analytics tools** | "What analytics do you use? (Google Analytics, Plausible, Fathom)" | Google Analytics |
| **Advertising** | "Do you run retargeting or ad pixels? (Meta Pixel, Google Ads, TikTok)" | Meta Pixel |
| **Third-party tools** | "What other tools set cookies? (chat widgets, video embeds, payment)" | None |
| **Audience location** | "Do you serve EU visitors? (requires GDPR compliance)" | Yes — global audience |
| **Cookie consent banner** | "Do you have a cookie consent tool installed?" | Not yet |

**GATE: Do not proceed without knowing which tools and pixels are on the site.**

---

## Phase 2: Cookie Inventory

```
## Cookie Inventory

### Strictly Necessary Cookies
These cookies are essential for the website to function. They cannot be disabled.

| Cookie | Provider | Purpose | Duration |
|--------|----------|---------|----------|
| session_id | [Your site] | Maintains user session | Session |
| csrf_token | [Your site] | Security — prevents cross-site request forgery | Session |
| cookie_consent | [Your site] | Remembers cookie consent preferences | 12 months |

### Analytics Cookies
These cookies help us understand how visitors use our website.

| Cookie | Provider | Purpose | Duration |
|--------|----------|---------|----------|
| _ga | Google Analytics | Distinguishes unique users | 2 years |
| _ga_[ID] | Google Analytics | Maintains session state | 2 years |
| _gid | Google Analytics | Distinguishes unique users | 24 hours |

### Marketing/Advertising Cookies
These cookies track visitors across websites for advertising purposes.

| Cookie | Provider | Purpose | Duration |
|--------|----------|---------|----------|
| _fbp | Meta (Facebook) | Identifies browsers for ad delivery | 3 months |
| _fbc | Meta (Facebook) | Stores click identifier for ad attribution | 2 years |

### Functional Cookies
These cookies enable enhanced functionality and personalization.

| Cookie | Provider | Purpose | Duration |
|--------|----------|---------|----------|
| [cookie] | [Provider] | [Purpose] | [Duration] |
```

---

## Phase 3: Policy Document

```
## Cookie Policy

**Last updated:** [Date]

### What Are Cookies

Cookies are small text files placed on your device when you visit our
website. They help us provide you with a better experience and allow
certain features to function properly.

### How We Use Cookies

We use cookies for the following purposes:

**Strictly Necessary:** These cookies are required for the website to
work. They include session management and security cookies. You cannot
opt out of these cookies.

**Analytics:** We use [Google Analytics / other] to understand how
visitors interact with our website. This helps us improve content and
user experience. These cookies collect anonymous, aggregated data.

**Marketing:** We use [Meta Pixel / Google Ads / other] to deliver
relevant advertisements and measure ad campaign effectiveness. These
cookies may track your activity across other websites.

**Functional:** These cookies remember your preferences and settings
to enhance your experience.

### Your Cookie Choices

When you first visit our website, you will see a cookie consent banner
that allows you to:

- **Accept all cookies** — enables all cookie categories
- **Reject non-essential cookies** — only strictly necessary cookies are set
- **Customize preferences** — choose which categories to enable

You can change your cookie preferences at any time by [clicking the
cookie settings link in our website footer / visiting this page].

### How to Control Cookies in Your Browser

You can also control cookies through your browser settings:
- **Chrome:** Settings > Privacy and Security > Cookies
- **Firefox:** Settings > Privacy & Security > Cookies
- **Safari:** Preferences > Privacy > Cookies
- **Edge:** Settings > Cookies and Site Permissions

Note: Blocking all cookies may impact website functionality.

### Third-Party Cookies

Some cookies are set by third-party services that appear on our pages.
We do not control these cookies. Please review the privacy policies of
these third parties:

- [Google Analytics Privacy Policy](https://policies.google.com/privacy)
- [Meta Privacy Policy](https://www.facebook.com/privacy/policy)

### Updates to This Policy

We may update this cookie policy periodically. The "Last updated" date
at the top reflects the most recent revision.

### Contact Us

If you have questions about our use of cookies, contact us at:
[Email address]
```

---

## Phase 4: Compliance Checklist

```
## Cookie Compliance Checklist

### GDPR (EU Visitors)
- [ ] Cookie consent obtained BEFORE non-essential cookies are set
- [ ] Consent is freely given (no pre-checked boxes)
- [ ] Consent is specific (per cookie category)
- [ ] Consent is informed (policy explains each category)
- [ ] Users can withdraw consent as easily as they gave it
- [ ] Consent records are stored

### CCPA (California Visitors)
- [ ] "Do Not Sell My Personal Information" link available
- [ ] Cookie policy discloses categories of personal information collected
- [ ] Opt-out mechanism for sale of personal information

### General
- [ ] Cookie banner appears on first visit
- [ ] Cookie policy is linked from website footer
- [ ] Cookie inventory is accurate and up-to-date
- [ ] Third-party cookie providers are listed with privacy policy links
- [ ] Policy is reviewed and updated at least annually
```

---

## Example: E-commerce Store

**Cookies:** Session cookie (necessary), Google Analytics (analytics), Meta Pixel + Google Ads (marketing), Shopify cookies (functional). **Consent approach:** Banner with Accept All / Customize / Reject Non-Essential. Analytics and marketing cookies blocked until consent given.

---

## Anti-Patterns

- **Cookie wall (blocking access until consent)** — GDPR considers this coercive. Allow access with necessary cookies only.
- **Pre-checked consent boxes** — GDPR requires opt-in, not opt-out. All non-essential categories must be unchecked by default.
- **"By using this site you agree" banners** — this is not valid consent under GDPR. Provide actual choices.
- **Setting cookies before consent** — analytics and marketing cookies must not fire until the visitor actively consents.
- **Never updating the cookie list** — every time you add a new tool or pixel, update the cookie inventory and policy.

---

## Recovery

- **No cookie consent tool:** Implement one immediately. Options: CookieYes, Cookiebot, OneTrust, or built-in features in WordPress plugins.
- **Cookies firing before consent:** Configure your tag manager to only fire analytics/marketing tags after consent is recorded.
- **Unsure which cookies your site uses:** Run a cookie scan using a tool like Cookiebot or manually inspect with browser developer tools (Application > Cookies).
- **Received a GDPR complaint:** Implement proper consent immediately. Consult a data privacy attorney if the complaint comes from a regulatory authority.
