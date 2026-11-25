---
name: unbounce-caching-tracking
description: Troubleshooting Unbounce conversion tracking issues. Use when A/B testing stats are broken or page variants are not rotating due to server caching.
---

# Unbounce: Caching & Conversion Tracking

A very common issue when running Unbounce Landing Pages through WordPress is that conversion tracking (A/B testing stats) drops to zero or behaves erratically.

## The Problem: Page Caching
Unbounce relies on dynamic HTTP headers and cookies to assign unique identifiers to visitors and serve different A/B page variants. Aggressive WordPress caching plugins (like WP Rocket, W3 Total Cache, or server-level Varnish) will cache the HTML output of the first variant served, completely breaking the testing rotation and analytics tracking for all subsequent visitors.

## The Solution: Header Exclusions
To fix this, you must configure your caching plugin or server rules to completely bypass caching for any page served by Unbounce.

- The Unbounce plugin injects a specific HTTP header into all of its landing pages: `X-Unbounce-Plugin: 1`.
- Add an exclusion rule in your caching system to bypass caching whenever the `X-Unbounce-Plugin` header is detected.
