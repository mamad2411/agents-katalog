---
name: privacy-policy
description: "Writes GDPR and CCPA-compliant privacy policies for websites, apps, and online businesses with plain-language annotations explaining each section. Use when a user is launching a website, setting up e-commerce, collecting customer data, or needs to update an outdated privacy policy."
---

# Privacy Policy Generator

## When to Use This Skill

- Launching a new website, app, or online store
- Adding email collection, payment processing, or analytics to a site
- Selling to EU customers (GDPR) or California residents (CCPA)
- Updating an outdated privacy policy after adding new tools or features
- Setting up a SaaS product or membership site

**IMPORTANT: This skill generates starting-point privacy policies based on common practices. It is NOT legal advice. Always have a qualified attorney review the final policy before publishing.**

## Workflow

### Step 1: Gather Business Details

Ask the user:

1. What type of business? (e-commerce, SaaS, blog, service business, app)
2. What data do you collect? (names, emails, payment info, browsing behavior, location)
3. What tools process that data? (Stripe, Mailchimp, Google Analytics, Meta Pixel, etc.)
4. Do you sell to EU customers? (triggers GDPR requirements)
5. Do you sell to California residents? (triggers CCPA requirements)
6. Do you sell or share data with third parties?
7. What's your business name and website URL?

**Minimum needed: questions 1, 2, and 3.**

### Step 2: Determine Required Sections

| Business Type | Required Sections |
|--------------|-------------------|
| All businesses | Data collected, how it's used, how it's protected, contact info |
| E-commerce | Payment processing, order data retention, shipping data sharing |
| SaaS / App | Account data, usage analytics, data export/deletion |
| Email list / Blog | Email collection, cookies, analytics, unsubscribe process |
| EU customers | GDPR: legal basis, data rights, DPO contact, cross-border transfers |
| CA residents | CCPA: right to know, right to delete, right to opt-out, non-discrimination |

### Step 3: Draft the Policy

Write these sections in order:

1. **Introduction** — Who you are, what this policy covers
2. **Information We Collect** — Personal data, automatically collected data, third-party data
3. **How We Use Your Information** — Specific purposes tied to specific data types
4. **How We Share Your Information** — Third-party processors, legal requirements
5. **Cookies and Tracking** — What cookies, what they do, how to opt out
6. **Data Retention** — How long you keep data and why
7. **Your Rights** — Access, correction, deletion, portability
8. **GDPR Rights** (if applicable) — Legal basis, EU-specific rights, DPO contact
9. **CCPA Rights** (if applicable) — CA-specific disclosures and opt-out
10. **Children's Privacy** — COPPA compliance statement
11. **Security** — How data is protected (general terms, not technical specifics)
12. **Changes to This Policy** — How users are notified of updates
13. **Contact Information** — How to reach you about privacy concerns

For each section, add a **plain-language annotation** in italics explaining what it means in simple terms.

### Step 4: Review & Deliver

1. Verify all third-party tools mentioned are covered in the sharing section
2. Check that every data type collected has a stated purpose
3. Confirm retention periods are specified
4. Ensure contact method is included
5. Add "Last Updated: [date]" at the top
6. Remind the user to have an attorney review before publishing

## Examples

### Example 1: Shopify E-commerce Store

**Business:** Handmade jewelry store on Shopify
**Data collected:** Names, emails, shipping addresses, payment info, browsing behavior
**Tools:** Shopify, Stripe, Mailchimp, Google Analytics, Meta Pixel
**EU customers:** Yes | **CA residents:** Yes

**Output (excerpt — Introduction + Information We Collect):**

> **Privacy Policy**
> Last Updated: [Current Date]
>
> **1. Introduction**
>
> LunaStone Jewelry ("we," "us," or "our") operates lunastonejewelry.com. This Privacy Policy explains how we collect, use, and protect your personal information when you visit our website, make a purchase, or interact with us.
>
> *In plain language: This document tells you what information we collect about you, why we collect it, and what we do with it. We try to collect only what we need and keep it safe.*
>
> **2. Information We Collect**
>
> **Information you provide directly:**
> - Name and email address (when you create an account, place an order, or subscribe to our newsletter)
> - Shipping and billing address (when you place an order)
> - Payment information (credit card number, expiration date — processed securely by Stripe; we never store your full card number)
> - Product reviews and messages (when you contact us or leave a review)
>
> **Information collected automatically:**
> - Browsing behavior on our site (pages visited, products viewed, time on page) via Google Analytics
> - Device information (browser type, operating system, screen size)
> - IP address and approximate location
> - Cookies and tracking pixels (see Section 5)
>
> *In plain language: We collect what you type in (name, address, payment) plus some technical info about how you browse our site. We use Stripe for payments — we never see or store your full credit card number.*

**GDPR section (excerpt):**

> **8. Your Rights Under GDPR (EU Customers)**
>
> If you are located in the European Economic Area, you have the following rights:
>
> - **Right to Access** — Request a copy of all personal data we hold about you
> - **Right to Rectification** — Ask us to correct inaccurate data
> - **Right to Erasure** — Ask us to delete your data ("right to be forgotten")
> - **Right to Restrict Processing** — Ask us to limit how we use your data
> - **Right to Data Portability** — Receive your data in a machine-readable format
> - **Right to Object** — Opt out of marketing communications at any time
>
> **Legal Basis for Processing:**
> - Contract performance (processing orders, shipping products)
> - Legitimate interest (improving our website, fraud prevention)
> - Consent (marketing emails, non-essential cookies)
>
> To exercise any of these rights, email privacy@lunastonejewelry.com. We will respond within 30 days.
>
> *In plain language: If you're in the EU, you can ask us to show you what data we have, fix it, delete it, or send it to you in a file. Email us and we'll handle it within 30 days.*

### Example 2: SaaS Project Management App

**Business:** Cloud-based project management tool
**Data collected:** Names, emails, company info, project data, usage analytics
**Tools:** AWS hosting, Stripe billing, Intercom chat, Mixpanel analytics

**Output (excerpt — Data Retention + Security):**

> **6. Data Retention**
>
> | Data Type | Retention Period | Reason |
> |-----------|-----------------|--------|
> | Account information | Duration of account + 30 days after deletion | Service delivery and account recovery |
> | Project data | Duration of account + 30 days after deletion | You can export all project data before deleting your account |
> | Payment records | 7 years after transaction | Tax and legal compliance |
> | Usage analytics | 24 months (anonymized after 12 months) | Product improvement |
> | Support chat transcripts | 24 months | Quality assurance and training |
>
> *In plain language: We keep your stuff while you use our product plus 30 days after you leave (in case you change your mind). Payment records stay longer because the law requires it. Analytics data gets anonymized after a year.*
>
> **11. Security**
>
> We protect your data using:
> - Encryption in transit (TLS 1.2+) and at rest (AES-256)
> - Regular security audits and penetration testing
> - Role-based access controls for our team
> - SOC 2 Type II compliance (audit report available on request)
> - Automated backups with geographic redundancy
>
> No system is 100% secure. If we discover a data breach that affects your personal information, we will notify you within 72 hours as required by applicable law.
>
> *In plain language: We use industry-standard security to protect your data. If something goes wrong, we'll tell you within 72 hours.*

## Common Patterns by Business Type

| Business Type | Key Considerations |
|--------------|-------------------|
| E-commerce (Shopify, WooCommerce) | Payment processors, shipping partners, abandoned cart tracking, review platforms |
| SaaS / Web App | User-generated content ownership, API data access, sub-processors, data export |
| Blog / Content Site | Cookies, analytics, email subscription, comment data, ad networks |
| Coaching / Services | Intake forms, session recordings, scheduling tools, payment platforms |
| Membership / Course | Student data, progress tracking, community platform data, certificate records |

## Recovery & Fallbacks

- **User doesn't know what tools they use:** Ask them to check their website footer, admin dashboard, and email platform. Common stack: Google Analytics + Mailchimp + Stripe covers most small businesses.
- **User operates internationally but doesn't know which laws apply:** Default to including both GDPR and CCPA sections. It's better to over-comply than under-comply.
- **User wants a "simple" one-page policy:** Write the shortest compliant version, but warn that brevity should not come at the cost of required disclosures.
- **Policy needs to cover an app + website:** Write one combined policy that covers both, with sections clearly noting which applies to the app vs. website.

## Constraints

- **ALWAYS include the legal disclaimer** — this is not legal advice
- **NEVER claim compliance** — say "designed to address requirements of" not "compliant with"
- List every third-party tool by name — don't hide behind "third-party services"
- Include a real contact method (email at minimum)
- Date every policy with "Last Updated"
- Use plain language annotations for every section
