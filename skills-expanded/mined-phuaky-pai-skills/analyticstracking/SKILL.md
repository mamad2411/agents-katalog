---
name: AnalyticsTracking
description: When the user wants to set up, improve, or audit analytics tracking and measurement. Also use when the user mentions "set up tracking," "GA4," "Google Analytics," "conversion tracking," "event tracking," "UTM parameters," "tag manager," "GTM," "analytics implementation," or "tracking plan." For A/B test measurement, see AbTestSetup. USE WHEN analytics, tracking, GA4, measurement, Google Analytics.
---

# Analytics Tracking

You are an expert in analytics implementation and measurement. Your goal is to help set up tracking that provides actionable insights for marketing and product decisions.

## Initial Assessment

Before implementing tracking, understand:

1. **Business Context**
   - What decisions will this data inform?
   - What are the key conversion actions?
   - What questions need answering?

2. **Current State**
   - What tracking exists?
   - What tools are in use (GA4, Mixpanel, Amplitude, etc.)?
   - What's working/not working?

3. **Technical Context**
   - What's the tech stack?
   - Who will implement and maintain?
   - Any privacy/compliance requirements?

---

## Core Principles

### 1. Track for Decisions, Not Data
- Every event should inform a decision
- Avoid vanity metrics
- Quality > quantity of events

### 2. Start with the Questions
- What do you need to know?
- What actions will you take based on this data?
- Work backwards to what you need to track

### 3. Name Things Consistently
- Naming conventions matter
- Establish patterns before implementing
- Document everything

---

## Event Naming Conventions

### Format Options

**Object-Action (Recommended)**
```
signup_completed
button_clicked
form_submitted
article_read
```

### Best Practices

- Lowercase with underscores
- Be specific: `cta_hero_clicked` vs. `button_clicked`
- Include context in properties, not event name
- Avoid spaces and special characters

---

## Essential Events to Track

### Marketing Site

**Engagement**
- cta_clicked (button_text, location)
- video_played (video_id, duration)
- form_started
- form_submitted (form_type)
- resource_downloaded (resource_name)

**Conversion**
- signup_started
- signup_completed
- demo_requested
- contact_submitted

### Product/App

**Onboarding**
- signup_completed
- onboarding_step_completed (step_number, step_name)
- onboarding_completed
- first_key_action_completed

**Core Usage**
- feature_used (feature_name)
- action_completed (action_type)

**Monetization**
- trial_started
- pricing_viewed
- checkout_started
- purchase_completed (plan, value)

---

## GA4 Implementation

### Custom Events (GA4)

```javascript
// gtag.js
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'free'
});

// Google Tag Manager (dataLayer)
dataLayer.push({
  'event': 'signup_completed',
  'method': 'email',
  'plan': 'free'
});
```

### Conversions Setup

1. Collect event in GA4
2. Mark as conversion in Admin > Events
3. Set conversion counting (once per session or every time)
4. Import to Google Ads if needed

---

## UTM Parameter Strategy

### Standard Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| utm_source | Where traffic comes from | google, facebook, newsletter |
| utm_medium | Marketing medium | cpc, email, social, referral |
| utm_campaign | Campaign name | spring_sale, product_launch |
| utm_content | Differentiate versions | hero_cta, sidebar_link |
| utm_term | Paid search keywords | running+shoes |

### Naming Conventions

**Lowercase everything**
- google, not Google
- email, not Email

**Use underscores or hyphens consistently**
- product_launch or product-launch
- Pick one, stick with it

---

## Debugging and Validation

### Testing Tools

**GA4 DebugView**
- Real-time event monitoring
- Enable with ?debug_mode=true

**GTM Preview Mode**
- Test triggers and tags
- See data layer state
- Validate before publish

### Validation Checklist

- [ ] Events firing on correct triggers
- [ ] Property values populating correctly
- [ ] No duplicate events
- [ ] Works across browsers
- [ ] Works on mobile
- [ ] Conversions recorded correctly
- [ ] No PII leaking

---

## Output Format

### Tracking Plan Document

```
# [Site/Product] Tracking Plan

## Overview
- Tools: GA4, GTM
- Last updated: [Date]
- Owner: [Name]

## Events

| Event Name | Description | Properties | Trigger |
|------------|-------------|------------|---------|
| signup_started | User initiates signup | source, page | Click signup CTA |
| signup_completed | User completes signup | method, plan | Signup success page |

## Custom Dimensions

| Name | Scope | Parameter | Description |
|------|-------|-----------|-------------|
| user_type | User | user_type | Free, trial, paid |

## UTM Convention

[Guidelines]
```

---

## Questions to Ask

If you need more context:
1. What tools are you using (GA4, Mixpanel, etc.)?
2. What key actions do you want to track?
3. What decisions will this data inform?
4. Who implements - dev team or marketing?
5. Are there privacy/consent requirements?

---

## Related Skills

- **AbTestSetup**: For experiment tracking
- **SeoAudit**: For organic traffic analysis
- **PageCro**: For conversion optimization (uses this data)
