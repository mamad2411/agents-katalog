---
name: terms-of-use-app
description: "Creates terms of use specifically for mobile apps with license grants, restrictions, and app store compliance. Use when launching or updating a mobile application."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Terms of Use — Mobile App

## When to Use This Skill

Use this skill when you need to:
- Create terms of use for a mobile application (iOS, Android, or both)
- Draft license grants, usage restrictions, and user obligations
- Ensure compliance with Apple App Store and Google Play policies
- Establish subscription, refund, and data handling terms for app users

**DO NOT** use this skill for website terms of service, SaaS agreements (use saas-agreement), or privacy policies. This is specifically for mobile app terms of use. Have an attorney review before publishing.

---

## Core Principle

APP TERMS MUST COMPLY WITH BOTH YOUR BUSINESS NEEDS AND APP STORE REQUIREMENTS — APPLE AND GOOGLE HAVE SPECIFIC MANDATES THAT OVERRIDE YOUR PREFERENCES.

---

## Phase 1: App Details

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **App name** | "What is your app called?" | No default — must be provided |
| **App description** | "What does the app do?" | No default — must be provided |
| **Platforms** | "iOS, Android, or both?" | Both |
| **Monetization** | "Free, freemium, paid, or subscription?" | Freemium with subscription |
| **User data collected** | "What user data does the app collect?" | Account info, usage data |
| **User-generated content** | "Can users create or upload content in the app?" | No |
| **In-app purchases** | "Are there in-app purchases or subscriptions?" | Yes |
| **Minimum age** | "Is there a minimum age requirement?" | 13+ |

**GATE: Do not proceed without app name, platforms, and monetization model.**

---

## Phase 2: Terms Document

```
## [App Name] Terms of Use

**Last Updated:** [Date]

Please read these Terms of Use ("Terms") carefully before using the
[App Name] mobile application ("App") operated by [Company Legal Name]
("Company," "we," "us").

By downloading, installing, or using the App, you agree to be bound
by these Terms. If you do not agree, do not use the App.

### 1. License Grant

We grant you a limited, non-exclusive, non-transferable, revocable
license to download, install, and use the App on a mobile device that
you own or control, strictly in accordance with these Terms.

### 2. Restrictions

You shall NOT:
- Copy, modify, or distribute the App or its content
- Reverse engineer, decompile, or disassemble the App
- Rent, lease, lend, sell, or sublicense the App
- Use the App for any illegal, harmful, or unauthorized purpose
- Circumvent any security or access controls
- Use automated scripts, bots, or scraping tools
- Impersonate another person or misrepresent your affiliation
- Interfere with or disrupt the App's servers or networks
- Remove or alter any copyright, trademark, or proprietary notices

### 3. Account Registration

[If applicable:]
- You must provide accurate and complete information during registration
- You are responsible for maintaining the security of your account credentials
- You are responsible for all activity under your account
- You must notify us immediately of any unauthorized access
- We reserve the right to suspend or terminate accounts that violate these Terms
- You must be at least [13/16/18] years old to create an account

### 4. Subscriptions and In-App Purchases

[If applicable:]

**4.1 Subscription Plans**
| Plan | Price | Billing Cycle |
|------|-------|--------------|
| [Plan name] | $[X] | [Monthly / Annual] |

**4.2 Billing.** Subscriptions are billed through [Apple App Store /
Google Play]. Payment will be charged to your App Store account.

**4.3 Auto-Renewal.** Subscriptions automatically renew unless
canceled at least 24 hours before the end of the current billing
period. You can manage and cancel subscriptions in your device's
account settings.

**4.4 Refunds.** Refund requests are handled by [Apple / Google]
according to their respective refund policies. We do not process
refunds directly for App Store or Google Play purchases.

**4.5 Price Changes.** We may change subscription prices. Changes
take effect at the start of the next billing period after notice.

### 5. User Content

[If applicable:]
- You retain ownership of content you create or upload
- You grant [Company] a worldwide, non-exclusive, royalty-free license
  to use, display, and distribute your content within the App
- You represent that your content does not infringe third-party rights
- We may remove content that violates these Terms without notice
- We are not responsible for content posted by other users

### 6. Intellectual Property

The App, including all content, features, and functionality, is owned
by [Company] and protected by copyright, trademark, and other
intellectual property laws. Our trademarks may not be used without
prior written consent.

### 7. Privacy

Your use of the App is also governed by our Privacy Policy, available
at [URL]. By using the App, you consent to the collection and use of
information as described in the Privacy Policy.

### 8. Third-Party Services

The App may contain links to or integrations with third-party
services. We are not responsible for the content, privacy practices,
or terms of third-party services. Your use of third-party services
is at your own risk.

### 9. Disclaimers

THE APP IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES
OF ANY KIND, EXPRESS OR IMPLIED. WE DO NOT WARRANT THAT THE APP WILL
BE UNINTERRUPTED, ERROR-FREE, OR FREE OF HARMFUL COMPONENTS.

### 10. Limitation of Liability

TO THE MAXIMUM EXTENT PERMITTED BY LAW, [COMPANY] SHALL NOT BE
LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL
DAMAGES ARISING FROM YOUR USE OF THE APP. OUR TOTAL LIABILITY SHALL
NOT EXCEED THE AMOUNT YOU PAID FOR THE APP OR SUBSCRIPTIONS IN THE
[12] MONTHS PRECEDING THE CLAIM.

### 11. Indemnification

You agree to indemnify and hold [Company] harmless from claims,
damages, and expenses arising from your use of the App, violation
of these Terms, or infringement of third-party rights.

### 12. Termination

We may terminate or suspend your access immediately, without notice,
for conduct that we determine violates these Terms or is harmful to
other users or the App. Upon termination, your license to use the
App is revoked.

### 13. Changes to Terms

We may update these Terms at any time. We will notify users of
material changes through [in-app notification / email / App Store
update notes]. Continued use after changes constitutes acceptance.

### 14. App Store Compliance

**Apple App Store:**
These Terms are between you and [Company], not Apple. Apple has no
obligation to provide maintenance or support. Apple is not responsible
for any claims related to the App. In the event of a conflict between
these Terms and Apple's terms, Apple's terms prevail.

**Google Play:**
Google is not a party to these Terms and has no responsibility for
the App. Google Play's terms apply to your use of the Google Play store.

### 15. Governing Law and Disputes

These Terms are governed by the laws of [State]. Any disputes shall
be resolved through [binding arbitration / litigation] in [jurisdiction].

### 16. Contact

For questions about these Terms, contact us at:
[Email]
[Address]
```

---

## Phase 3: App Store Compliance Checklist

```
## App Store Requirements

### Apple App Store
- [ ] Terms of Use accessible within the app
- [ ] Privacy Policy accessible within the app
- [ ] Subscription terms clearly displayed before purchase
- [ ] Auto-renewal terms disclosed per Apple guidelines
- [ ] "Restore Purchases" button available for subscriptions
- [ ] Apple acknowledged as not a party in the terms
- [ ] EULA submitted during App Store Connect setup

### Google Play
- [ ] Terms of Use linked in Google Play listing
- [ ] Privacy Policy linked in Google Play listing
- [ ] Subscription billing through Google Play (if applicable)
- [ ] Cancellation instructions reference Google Play settings
- [ ] Data safety section completed in Play Console
```

---

## Phase 4: Delivery

Publish the terms at a stable URL accessible from within the app and from the app store listing page.

---

## Example: Productivity App with Subscription

**App:** TaskFlow (iOS + Android). **Monetization:** Free tier + $9.99/month Pro subscription. **Terms highlights:** Auto-renewal with 24-hour cancellation window, refunds through App Store/Play Store, no user-generated content, data collected per privacy policy, minimum age 13+.

---

## Anti-Patterns

- **Ignoring app store requirements** — Apple and Google reject apps with non-compliant terms. Follow their guidelines precisely.
- **Processing refunds outside the app store** — for in-app purchases made through Apple/Google, refunds must go through them
- **No subscription auto-renewal disclosure** — Apple requires specific language about auto-renewal. Missing it risks rejection.
- **Terms only on a website** — terms must be accessible from within the app, not just on your website
- **No age gate when required** — if your app collects data from users under 13, COPPA compliance is mandatory

---

## Recovery

- **App rejected for terms issues:** Review Apple/Google's specific rejection reason. Update terms to meet their requirements and resubmit.
- **Need to update terms post-launch:** Push an app update with in-app notification of new terms. Users must accept before continuing.
- **User dispute over subscription charges:** Direct them to the app store's refund process. Document your cancellation policy clearly.
- **COPPA concerns (under-13 users):** If under-13 users may use the app, implement COPPA-compliant data practices or restrict access to 13+.
