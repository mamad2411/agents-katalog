---
name: debug-optimization-detective-api
description: Troubleshoot Optimization Detective REST API accessibility issues and blocked metrics collection.
---

# Debug Optimization Detective API

Optimization Detective relies on the WordPress REST API being accessible to unauthenticated frontend visitors to collect real user metrics about page rendering.

## Troubleshooting Missing Metrics

1. **Check the Site Health Test**: Optimization Detective provides a Site Health test to detect blocked REST API endpoints. Go to **Tools > Site Health** and look for warnings regarding the Optimization Detective REST API endpoint.
2. **Review Security Plugins**: If the API is blocked, check security plugins or firewalls (like Wordfence, iThemes Security) that might be restricting unauthenticated REST API access.
3. **Check Browser Console**: Visit the frontend of the site as a guest, open the browser console, and look for failed network requests to `/wp-json/optimization-detective/v1/url-metrics`.
4. **Ensure HTTPS**: Metrics collection uses beacon requests; ensure your site is running over HTTPS.

If the REST API cannot be made public, Optimization Detective will short-circuit and will not collect data or optimize the site.
