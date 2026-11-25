---
name: agent-analytics
description: Web analytics your AI agent can read. Drop a script tag on any site, then just ask "how's my site doing?" — no dashboards, no logins. One account for all your projects. Use when adding analytics to a site, checking traffic/events, or when the user wants to ask their agent instead of opening a dashboard.
version: 1.0.0
author: dannyshmueli
repository: https://github.com/Agent-Analytics/agent-analytics-core
tags:
  - analytics
  - tracking
  - web
  - events
---

# Agent Analytics — Analytics your AI agent can actually read

You are setting up analytics that the agent queries directly — no dashboards, no logins. One script tag per site, one API key for all projects. The user asks "how's my site doing?" and you answer with real data.

## Philosophy

You are NOT Mixpanel. Don't track everything. Track only what answers: **"Is this project alive and growing?"**

For a typical site, that's 3-5 custom events max on top of automatic page views. The magic isn't in collecting data — it's that YOU (the agent) can query it and report back instantly.

## First-time setup

If the project doesn't have tracking yet:

```bash
# 1. Login (one time — uses your API key)
npx agent-analytics login --token aak_YOUR_API_KEY

# 2. Create the project (returns a project write token)
npx agent-analytics init my-site --domain https://mysite.com

# 3. Add the snippet (Step 1 below) using the returned token
# 4. Deploy, click around, verify:
npx agent-analytics events my-site
```

The `init` command returns a **project write token** — use it as `data-token` in the snippet below. This is separate from your API key (which is for reading/querying).

## Step 1: Add the tracking snippet

Add before `</body>`:

```html
<script src="https://api.agentanalytics.sh/tracker.js"
  data-project="PROJECT_NAME"
  data-token="PROJECT_WRITE_TOKEN"></script>
```

This auto-tracks `page_view` events with path, referrer, browser, OS, device, screen size, and UTM params. You do NOT need to add custom page_view events.

## Step 1b: Discover existing events (existing projects)

If tracking is already set up, check what events and property keys are already in use so you match the naming:

```bash
npx agent-analytics properties-received PROJECT_NAME
```

This shows which property keys each event type uses (e.g. `cta_click → id`, `signup → method`). Match existing naming before adding new events.

## Step 2: Add custom events to important actions

Use `onclick` handlers on the elements that matter:

```html
<a href="..." onclick="window.aa?.track('EVENT_NAME', {id: 'ELEMENT_ID'})">
```

The `?.` operator ensures no error if the tracker hasn't loaded yet.

### Standard events for 80% of SaaS sites

Pick the ones that apply. Most sites need 2-4:

| Event | When to fire | Properties |
|-------|-------------|------------|
| `cta_click` | User clicks a call-to-action button | `id` (which button) |
| `signup` | User creates an account | `method` (github/google/email) |
| `login` | User returns and logs in | `method` |
| `feature_used` | User engages with a core feature | `feature` (which one) |
| `checkout` | User starts a payment flow | `plan` (free/pro/etc) |
| `error` | Something went wrong visibly | `message`, `page` |

### What to track as `cta_click`

Only buttons that indicate conversion intent:
- "Get Started" / "Sign Up" / "Try Free" buttons
- "Upgrade" / "Buy" / pricing CTAs
- Primary navigation to signup/dashboard
- "View on GitHub" / "Star" (for open source projects)

### What NOT to track
- Every link or button (too noisy)
- Scroll depth (not actionable)
- Form field interactions (too granular)
- Footer links (low signal)

### Property naming rules

- Use `snake_case`: `hero_get_started` not `heroGetStarted`
- The `id` property identifies WHICH element: short, descriptive
- Name IDs as `section_action`: `hero_signup`, `pricing_pro`, `nav_dashboard`
- Don't encode data the page_view already captures (path, referrer, browser)

## Step 3: Test immediately

After adding tracking, verify it works:

```bash
# Option A: Browser console on your site:
window.aa.track('test_event', {source: 'manual_test'})

# Option B: Click around, then check:
npx agent-analytics events PROJECT_NAME

# Events appear within seconds.
```

## Querying the data (the whole point)

This is why Agent Analytics exists — you query it, not a human in a dashboard:

```bash
# How's the project doing?
npx agent-analytics stats my-site --days 7

# What events are coming in?
npx agent-analytics events my-site

# What property keys exist per event type?
npx agent-analytics properties-received my-site

# Direct API (for agents without npx):
curl "https://api.agentanalytics.sh/stats?project=my-site&days=7" \
  -H "X-API-Key: $AGENT_ANALYTICS_KEY"
```

## What this skill does NOT do

- No dashboards — your agent IS the dashboard
- No complex funnels or cohort analysis
- No PII collection — no cookies, no IP addresses, privacy-first by design
- No per-project accounts — one API key covers everything

## Examples

### Landing page with pricing

```html
<!-- Hero CTAs -->
<a href="/signup" onclick="window.aa?.track('cta_click',{id:'hero_get_started'})">
  Get Started Free
</a>
<a href="#pricing" onclick="window.aa?.track('cta_click',{id:'hero_see_pricing'})">
  See Pricing →
</a>

<!-- Pricing CTAs -->
<a href="/signup?plan=free" onclick="window.aa?.track('cta_click',{id:'pricing_free'})">
  Try Free
</a>
<a href="/signup?plan=pro" onclick="window.aa?.track('cta_click',{id:'pricing_pro'})">
  Get Started →
</a>
```

### SaaS app with auth

```js
// After successful signup
window.aa?.track('signup', {method: 'github'});

// When user does the main thing your app does
window.aa?.track('feature_used', {feature: 'create_project'});

// On checkout page
window.aa?.track('checkout', {plan: 'pro'});

// In error handler
window.aa?.track('error', {message: err.message, page: location.pathname});
```
