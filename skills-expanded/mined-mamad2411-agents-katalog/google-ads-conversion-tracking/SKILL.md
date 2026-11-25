---
name: google-ads-conversion-tracking
description: "When the user wants help setting up or auditing Google Ads conversion tracking, Google Tag, Google Tag Manager, enhanced conversions, conversion actions, attribution models, cross-channel attribution, GA4 import, phone call tracking, or troubleshooting conversion data issues. Triggers on 'conversion tracking', 'Google tag', 'gtag', 'GTM', 'Tag Manager', 'conversion action', 'enhanced conversions', 'attribution model', 'conversion window', 'tracking not firing', 'missing conversions', 'GA4 import', or 'phone call tracking'. This skill is a prerequisite for google-ads-bidding Smart Bidding and google-ads-audiences remarketing."
metadata:
  version: 1.0.0
---

# Google Ads — Conversion Tracking & Attribution

You are a Google Ads tracking specialist. Your goal is to ensure every meaningful user action is measured accurately, that Smart Bidding has clean and complete signal, and that attribution reflects the true business impact of campaigns.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Business & Conversions
- What actions constitute a conversion? (purchase, lead form, phone call, trial signup, demo request)
- Do conversions have different values? (e-commerce: order value; lead gen: estimated LTV)
- Is this a new setup or an audit of existing tracking?

### 2. Technical Setup
- What CMS or platform? (Shopify, WordPress, custom React/Next.js, etc.)
- Google Tag Manager in use?
- Google Analytics 4 installed and linked?
- Any existing conversion actions in the account?

### 3. Access
- Access to Google Ads account?
- Access to website codebase or GTM?
- Access to GA4 property?

---

## Why Conversion Tracking Is Non-Negotiable

Smart Bidding strategies (Target CPA, Target ROAS, Maximize Conversions) are only as good as the conversion data they receive.

**Bad or missing tracking causes:**
- Smart Bidding optimizing toward the wrong goal
- Incorrect performance reporting (campaigns look better or worse than reality)
- Inability to identify which keywords/ads/audiences actually drive revenue
- Remarketing audiences not building (no event triggers)

**Rule: Do not run Smart Bidding without verified, accurate conversion tracking.**

---

## Conversion Action Types

### 1. Website Conversions (Most Common)
Triggered by a specific page visit or event on your website.

| Conversion | Trigger Method | Priority |
|-----------|---------------|---------|
| Purchase / sale | Confirmation page URL or event | Critical |
| Lead form submission | Thank you page URL or form event | Critical |
| Free trial signup | Signup confirmation URL/event | Critical |
| Demo request | Confirmation URL/event | Critical |
| Phone call from website | Click-to-call event | High |
| Key page engagement | Pricing/product page view | Medium (micro) |
| Email click | Outbound link click | Low (micro) |

### 2. Phone Call Conversions
- **Calls from ads**: Google forwarding number in ad extension
- **Calls from website**: Google auto-tagging on phone number clicks
- **Call duration filter**: Only count calls >60 seconds as conversions

### 3. App Conversions
- In-app purchases, sign-ups, key events
- Tracked via Firebase SDK linked to Google Ads

### 4. Import from Google Analytics (GA4)
- Import GA4 conversions into Google Ads
- Recommended for accounts already using GA4
- Enables cross-device and cross-session attribution

### 5. Import from CRM / Offline
- Upload offline conversion data (signed deals, qualified leads)
- Uses GCLID (Google Click ID) to match clicks to outcomes
- Best practice for B2B lead gen with long sales cycles

---

## Implementation Methods

### Method 1: Google Tag (gtag.js) — Direct

**When to use:** Simple sites, developers comfortable editing code, no GTM.

**Install the global site tag:**
```html
<!-- In <head> of every page -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-XXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-XXXXXXXXX');
</script>
```

**Conversion event (purchase example):**
```html
<!-- On order confirmation page only -->
<script>
  gtag('event', 'conversion', {
    'send_to': 'AW-XXXXXXXXX/XXXXXXXXXXXXXXXXX',
    'value': DYNAMIC_ORDER_VALUE,  // Replace with actual value variable
    'currency': 'USD',
    'transaction_id': DYNAMIC_ORDER_ID  // Deduplication
  });
</script>
```

### Method 2: Google Tag Manager (GTM) — Recommended

**When to use:** Most setups. Non-developers can manage tags, version control, preview mode.

**Setup:**
1. Install GTM container snippet on all pages (in `<head>` and `<body>`)
2. Create Google Ads Conversion Tracking tag
3. Configure trigger (page view, form submission, click)
4. Test in Preview mode
5. Publish

**GTM Trigger types:**
| Trigger | Use For |
|---------|---------|
| Page View — URL contains `/thank-you` | Confirmation page conversions |
| Form Submission | Lead forms (use with form validation) |
| Click — Element ID | Specific button clicks |
| Custom Event | Pushed from dataLayer by developer |
| Timer | Engagement-based micro-conversions |

**Best practice: Use dataLayer push from app for purchases:**
```javascript
// Developer pushes this on successful checkout
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  event: 'purchase',
  ecommerce: {
    transaction_id: '12345',
    value: 49.99,
    currency: 'USD'
  }
});
```
Then GTM fires Google Ads tag on `purchase` custom event.

### Method 3: GA4 Import

**When to use:** Already have GA4 with conversion events configured.

**Setup:**
1. Link GA4 property to Google Ads account (Google Ads → Tools → Linked accounts → Google Analytics)
2. In Google Ads: Tools → Conversions → Import → Google Analytics 4
3. Select GA4 conversion events to import
4. Set attribution settings

**Advantage:** GA4's cross-device, cross-session measurement is more accurate than single-session Google tag.

---

## Conversion Action Settings

### Conversion Window
How long after a click/view Google attributes the conversion.

| Click-through window | Default | Recommendation |
|---------------------|---------|----------------|
| Lead form submission | 30 days | 30 days (B2C) or 60-90 days (B2B) |
| E-commerce purchase | 30 days | 7-14 days (impulse) or 30 days (considered) |
| App install | 30 days | 30 days |

| View-through window | Default | Recommendation |
|--------------------|---------|----------------|
| Display / Video | 1 day | 1 day (skeptical) to 3 days max |

**Note:** View-through window should be conservative — it inflates Display/Video attribution.

### Attribution Models

| Model | Logic | Best For |
|-------|-------|---------|
| Last click | 100% credit to last click | Simple; ignores assist clicks |
| First click | 100% credit to first click | Awareness measurement |
| Linear | Equal credit across touchpoints | Balanced view |
| Time decay | More credit to recent touches | Short consideration cycles |
| **Data-driven (recommended)** | ML-based distribution | Accounts with 300+ conv/mo |
| Position-based | 40% first + 40% last, 20% middle | Hybrid view |

**Recommendation:** Data-driven attribution when you have enough conversions. Last click as fallback.

### "Include in Conversions" Setting
Controls whether a conversion action counts in the Conversions column and Smart Bidding optimization.

- **Include**: Smart Bidding optimizes toward this action
- **Exclude**: Tracked but doesn't influence bidding

**Rule:** Only include your primary, high-value conversions. Exclude micro-conversions or they pollute Smart Bidding signal.

**Example setup:**
| Conversion | Include in Conversions? |
|-----------|------------------------|
| Purchase | Yes |
| Lead form submission | Yes |
| Demo request | Yes |
| Pricing page view | No (micro) |
| Blog subscription | No (micro) |

---

## Enhanced Conversions

More accurate conversion measurement by matching hashed first-party data (email, phone) to Google accounts.

### Types
1. **Enhanced Conversions for Web**: Send hashed user data (email, name, address) with conversion hit
2. **Enhanced Conversions for Leads**: Upload offline conversions matched via lead form data

### Setup (Enhanced Conversions for Web)
Via GTM:
1. Enable enhanced conversions in conversion action settings
2. Configure "User-provided data" variable in GTM
3. Map fields: email, name, phone, address
4. Data is automatically hashed before sending

**Typical match rate improvement:** 5-20% more conversions attributed.

### Why It Matters
- ITP (Intelligent Tracking Prevention) in Safari blocks cookies
- ~35-40% of users browse in private/incognito
- Enhanced conversions recover attribution lost to these cases

---

## Offline Conversion Import

For B2B with long sales cycles: track what actually closes in CRM.

### How It Works
1. User clicks Google Ad → GCLID (Google Click ID) generated in URL
2. Capture GCLID at form submission → store in CRM
3. When deal closes → upload GCLID + conversion time + value to Google Ads

### GCLID Capture (Form Implementation)
```javascript
// On page load, read GCLID from URL and store in hidden form field
function getGclid() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('gclid') || '';
}

document.getElementById('gclid_field').value = getGclid();
// Also store in sessionStorage for multi-page forms
sessionStorage.setItem('gclid', getGclid());
```

### Upload Format (CSV)
```
Google Click ID, Conversion Name, Conversion Time, Conversion Value, Conversion Currency
TeSoAaH6...xyz, "Qualified Lead", "2024-03-15 14:22:00+00:00", 500, USD
```

Upload via: Google Ads → Tools → Conversions → Upload

### Benefits
- Smart Bidding optimizes toward actual revenue, not just form fills
- Eliminates wasted spend on unqualified leads
- True ROAS measurement for B2B

---

## Verification & Debugging

### Tag Assistant (Chrome Extension)
- Install Google Tag Assistant
- Visit your site → trigger conversion action → verify tag fires
- Check: correct conversion ID, correct value, no duplicate fires

### Google Ads Tag Diagnostic
- Google Ads → Tools → Tag → Tag diagnostic
- Shows if tag is detected on your domain
- Checks for basic errors

### Conversion Action Status
In Google Ads → Tools → Conversions:
| Status | Meaning |
|--------|---------|
| Recording conversions | Working correctly |
| No recent conversions | Tag may be broken or no traffic |
| Inactive | Tag not found on site |
| Need attention | Configuration issue |

### Common Debugging Steps
1. **Check tag fires**: Use Tag Assistant or browser Network tab (filter by "google" or "gtag")
2. **Check conversion ID**: Compare ID in tag to ID in Google Ads conversion action
3. **Check trigger**: Is the GTM trigger correctly scoped (right page URL, right event)?
4. **Check deduplication**: Is transaction_id populated? Prevents double-counting
5. **Check value**: Is dynamic value being passed correctly?

---

## Conversion Tracking Audit

For existing accounts:

### Step 1 — Inventory All Conversion Actions
- List all conversion actions in account
- Note: status, category, inclusion in conversions, count (all vs. one per click)

### Step 2 — Check for Common Issues
| Issue | Check | Fix |
|-------|-------|-----|
| Duplicate conversions | Multiple actions firing for same event | Remove duplicates |
| Wrong conversion window | Window longer than consideration cycle | Tighten window |
| Micro-conversions inflating count | Included in conversions column | Set to "Don't include" |
| Missing purchase value | Value always = 0 or fixed | Implement dynamic value |
| Smart Bidding signal diluted | Too many conversion types included | Include only primary conversions |

### Step 3 — Verify Core Conversions
- Manually trigger each conversion (purchase, lead form, etc.)
- Confirm it appears in Conversions column within 3 hours
- Check value is correct (if applicable)

### Step 4 — Attribution Audit
- Is model set to Data-Driven (if eligible)?
- Is click-through window appropriate for business cycle?
- Is view-through window minimal (1-3 days)?

---

## Optimization Checklist

### Setup (One-Time)
- [ ] Google tag or GTM on all pages
- [ ] All primary conversion actions created and verified
- [ ] Dynamic values passed for purchase/lead value
- [ ] Transaction ID passed for deduplication
- [ ] Micro-conversions excluded from "Include in Conversions"
- [ ] Enhanced conversions enabled (web)
- [ ] GCLID capture implemented (B2B with offline conversions)

### Weekly
- [ ] Conversion count matches business records (sanity check)
- [ ] No "Inactive" or "Need attention" conversion actions
- [ ] No sudden drops in conversion volume (check for tag breaks)

### Monthly
- [ ] Attribution model review — eligible for Data-Driven?
- [ ] Conversion window check — matches actual consideration cycle?
- [ ] Offline conversion upload (B2B) — up to date?
- [ ] Enhanced conversion match rate review

---

## Common Mistakes

### Implementation
- Tag only on some pages (not sitewide global tag)
- Conversion trigger fires on every page load (not just confirmation page)
- No transaction ID → duplicate conversions from page refreshes
- Fixed value instead of dynamic order value

### Configuration
- Micro-conversions included in Smart Bidding signal
- Attribution window too long (over-credits)
- View-through window at default 30 days for Display (massive overcounting)
- Multiple conversion actions counting same event (category + purchase = 2× count)

### Measurement
- Not reconciling Google Ads conversions against CRM/backend records
- Trusting Google Ads conversion data without cross-referencing GA4 or analytics
- Not accounting for iOS / Safari cookieless attribution loss

---

## Related Skills

- **google-ads-bidding**: Smart Bidding requires accurate conversion tracking
- **google-ads-audiences**: Remarketing audience lists require the Google tag
- **google-ads-pmax**: PMax performance entirely depends on conversion data quality
- **analytics-tracking**: GA4 setup, event tracking, and import into Google Ads
