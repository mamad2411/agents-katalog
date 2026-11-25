---
name: analytics
description: "Analytics tracking and measurement setup or audit. Use when setting up GA4, GTM, event or conversion tracking, UTM parameters, or a tracking plan, or when events are not firing."
metadata:
  version: 2.0.1
---

# Analytics Tracking

Set up or audit tracking that informs marketing and product decisions.

If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or legacy `product-marketing-context.md`), read it first and ask only what it does not cover. Otherwise establish: the decisions the data will inform and the key conversions; existing tracking and tools (GA4, Mixpanel, ...); tech stack and who implements (dev or marketing); privacy and consent requirements.

## Principles

- Start from the questions: what you need to know and which action follows, then work backwards to the events. Every event serves a decision.
- Fewer, cleaner events beat more events; validated data beats volume.
- Fix naming before implementing, and document it.

## Naming

Object-action, lowercase with underscores: `signup_completed`, `form_submitted`, `checkout_payment_completed`. Be specific (`cta_hero_clicked` over `button_clicked`) and put context in properties, not the event name. No spaces or special characters.

Tracking-plan structure, starter events, standard properties, the document template and UTM conventions: [references/tracking-plan-template.md](references/tracking-plan-template.md). Full event lists by business type: [references/event-library.md](references/event-library.md).

## GA4

1. Create the property and data stream. 2. Install gtag.js or GTM. 3. Enable enhanced measurement. 4. Configure custom events. 5. Mark conversions in Admin.

```javascript
gtag('event', 'signup_completed', { method: 'email', plan: 'free' });
```

Detail: [references/ga4-implementation.md](references/ga4-implementation.md).

## GTM

Tags (code that runs), triggers (when), variables (dynamic values). Push events through the data layer:

```javascript
dataLayer.push({ event: 'form_submitted', form_name: 'contact', form_location: 'footer' });
```

Detail: [references/gtm-implementation.md](references/gtm-implementation.md).

## UTMs

`utm_source`, `utm_medium`, `utm_campaign` always; `utm_content` and `utm_term` when versions or paid keywords need separating. Lowercase everything and log every UTM in a spreadsheet (conventions in the template file).

## Debug and validate

Tools: GA4 DebugView (real-time events), GTM Preview mode (triggers before publish), Tag Assistant and dataLayer Inspector extensions.

Check that events fire on the right triggers, property values populate, nothing fires twice, desktop and mobile both work, conversions record, and no PII leaks.

| Symptom | Check |
|---|---|
| Event not firing | Trigger configuration, GTM container loaded |
| Wrong values | Variable path, data layer structure |
| Duplicate events | Multiple containers, trigger firing twice |

## Privacy

Cookie consent is required in the EU, UK and CA. Use consent mode (collect after consent), IP anonymization and a consent management platform; collect only what is needed; keep PII out of properties; set data retention and support user deletion.

## Output

A tracking plan document (template in the references) with events, custom dimensions and conversions.

## Related skills

`ab-testing`, `attribution` (models and reconciling numbers once tracking is live), `seo-audit`, `cro`, `revops`, `google-search-console`.
