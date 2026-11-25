---
name: monitoring
description: "Periodic page monitoring via Brijio: read authenticated pages on a schedule, extract specific data, compare to previous state, and notify on changes — designed for Hermes cron jobs."
---

# Periodic Page Monitoring

Monitor authenticated web pages on a schedule by reading page data, extracting
specific values, comparing to a known baseline, and reporting changes. This
skill is designed to work with Hermes cron jobs for ongoing monitoring tasks.

## When to Use

- Price monitoring on authenticated e-commerce sites
- Availability checks (stock, tickets, appointments)
- Content change alerts on dashboards or internal tools
- Status page monitoring behind authentication
- Any scenario where you need to check a page periodically and alert on changes

## Cron Job Setup

Use the Hermes `cronjob` tool to set up a recurring monitoring task:

```
cronjob action=create \
  name="price-monitor-product-x" \
  schedule="every 2h" \
  prompt="Check the price of Product X on the authenticated page at https://shop.example.com/product-x. Use list_browsers to confirm connection, read_current_page to get the price, compare to the last known price stored in memory, and report if the price has changed."
```

Load the `using-brijio` and `monitoring` skills in the cron job so the
agent knows how to use Brijio tools:

```
skills: ["using-brijio", "monitoring"]
```

## Workflow

### 1. Check Connection

```
list_browsers → Confirm browser is connected
```

If no browser is connected, the cron job cannot proceed. Report this as an
error — do not silently fail.

### 2. Read the Target Page

```
read_current_page(includeContent: true) → Full page context
```

If the page requires navigation from the current URL, use the
[navigation](skill://brijio/navigation) skill to reach the target page
first.

### 3. Extract Target Data

From the page context, extract the specific data points you're monitoring:

**Price monitoring:**

```
Find the price element in forms/links/actions or content
Extract numeric value, currency, and any discount information
```

**Availability monitoring:**

```
Look for "In Stock", "Out of Stock", "Available", "Sold Out" text
Check for disabled "Add to Cart" actions
Check for "Coming Soon" or "Notify Me" links
```

**Content change monitoring:**

```
Extract specific sections of text (headings, table data, status indicators)
Compare structure and content to the previous reading
```

**Status monitoring:**

```
Check for status indicators (green/red icons, "Operational" / "Degraded" text)
Extract status text and component names
```

### 4. Compare to Baseline

Retrieve the last known state from memory:

```
memory action=read target="memory" → Get last known values
```

If this is the first run, store the current values and report "baseline
established" — do not report a change yet.

Compare current values to stored values:

| Match                   | Action                                              |
| ----------------------- | --------------------------------------------------- |
| Same as baseline        | No change — report "no change" and exit             |
| Different from baseline | Report the change with old and new values           |
| No previous baseline    | Store current values, report "baseline established" |

### 5. Report Changes

When a change is detected, report clearly:

```markdown
🔔 **Price Change Detected**

**Product:** Premium Widget (SKU: PW-100)
**Previous price:** $49.99
**Current price:** $39.99
**Change:** -$10.00 (-20%)
**Page:** https://shop.example.com/product-x
**Checked at:** 2026-05-28 14:30 UTC
```

For availability changes:

```markdown
🔔 **Availability Change**

**Product:** Concert Tickets - Section A
**Previous status:** Sold Out
**Current status:** Available (12 remaining)
**Page:** https://tickets.example.com/event/123
**Checked at:** 2026-05-28 14:30 UTC
```

### 6. Update Baseline

After reporting a change, update the stored baseline:

```
memory action=add target="memory"
  content="Product X price: $39.99 (as of 2026-05-28)"
```

This prevents reporting the same change repeatedly.

## Monitoring Strategies

### Simple Value Monitoring

Extract a single value (price, status, count) and compare to the previous
value. Best for:

- Price changes
- Stock availability
- Status page updates

### Structural Monitoring

Compare the page structure (forms, links, actions) to detect any changes.
Best for:

- New features appearing on a page
- UI changes on internal tools
- New links or buttons added

### Keyword Monitoring

Scan page content for specific keywords. Best for:

- Error messages ("maintenance", "degraded", "down")
- Feature announcements ("new", "beta", "launch")
- Policy changes ("updated terms", "effective date")

## Scheduling Recommendations

| Frequency       | Use Case                                           |
| --------------- | -------------------------------------------------- |
| Every 5 min     | Critical status pages, high-value availability     |
| Every 15 min    | Stock alerts, limited-availability events          |
| Every 1 hour    | Price monitoring on stable e-commerce pages        |
| Every 2-4 hours | Content change detection on dashboards             |
| Daily           | Low-priority status checks, policy page monitoring |

## Pitfalls

### Authenticated Pages

Brijio monitors pages through the user's real browser session. The
browser must be connected when the cron job runs. If the connection fails:

- Report the failure clearly
- Do not cache stale data as "unchanged"
- Suggest the user check their browser connection

### Dynamic Content

Pages with live data (countdown timers, live feeds) will always show changes.
Focus on specific data points rather than full-page comparison. Use the
[data-extraction](skill://brijio/data-extraction) skill for targeted
extraction instead of comparing entire page snapshots.

### Rate Limiting

Frequent page reads may trigger anti-bot protections. If you encounter
rate-limit errors:

1. Reduce the monitoring frequency
2. Add a small delay between reads
3. Focus on the specific data, not the entire page

### Session Expiration

Authenticated sessions expire. If `read_current_page` shows a login page
instead of the expected content, the session has expired. Report this as
"session expired" — do not attempt to log in automatically.

### Element ID Changes

Element IDs change between page loads. Never store element IDs (`e5`, `f2`) as
stable references — store the data values (text content, prices, labels)
instead.

### Multiple Checks in One Run

To monitor multiple pages in a single cron run:

1. Read Page A, extract data, compare to baseline A
2. Read Page B, extract data, compare to baseline B
3. Report all changes in a single summary message

This is more efficient than separate cron jobs for each page.
