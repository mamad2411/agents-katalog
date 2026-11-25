---
name: jetpack-boost-critical-css
description: Troubleshoot and configure Jetpack Boost's Critical CSS generation to improve Core Web Vitals (FCP, CLS) and resolve layout shifts.
---

# Jetpack Boost - Critical CSS Optimization

This skill provides guidelines for working with the **Optimize CSS Loading** feature in Jetpack Boost.

## When to use this skill
- When configuring Critical CSS generation in Jetpack Boost.
- When troubleshooting Flash of Unstyled Content (FOUC).
- When investigating layout shifts (CLS) caused by deferred CSS.
- When FCP (First Contentful Paint) needs improvement via CSS optimization.

## Guidelines
1. **Critical CSS Generation**: Jetpack Boost attempts to automatically determine the most important CSS required to display the site's initial content quickly. Ensure the generation completes successfully.
2. **Troubleshooting Display Issues**: If the site looks broken during initial load (FOUC), it means the generated Critical CSS might be missing essential styles. Try regenerating the Critical CSS from the Jetpack Boost dashboard.
3. **Compatibility**: Check for conflicts with other caching plugins that also minify or defer CSS. Only one plugin should handle CSS deferral to prevent display issues.
