---
name: sitekit-pagespeed
description: Using the PageSpeed Insights module in Site Kit. Use when analyzing Core Web Vitals and resolving API quota issues.
---

# Site Kit PageSpeed Insights

This module brings Google PageSpeed Insights and Core Web Vitals directly into the WordPress dashboard.

## API Quota Errors
Site Kit uses the Google PageSpeed Insights API. If a user has a highly trafficked dashboard or clicks refresh frequently, they might hit the free API quota limit (`quotaExceeded`).
- This usually resolves itself after a few minutes/hours.
- For high-usage environments, developers can obtain their own API key from the Google Cloud Console and define it, though Site Kit's default key is usually sufficient for standard use.

## Interpreting Results
- **Lab Data**: Metrics calculated on the fly during the API request (simulating a mobile/desktop device).
- **Field Data**: Real-world data from the Chrome User Experience Report (CrUX). This requires the site to have enough traffic to be included in the CrUX database. If the site is new, Field Data will be unavailable.
