---
name: sitekit-reader-revenue
description: Managing the Google Reader Revenue Manager integration within Site Kit. Use when dealing with paywalls, subscriptions, or reader contributions.
---

# Site Kit Reader Revenue Manager

Reader Revenue Manager is a newer module in Site Kit that allows publishers to add paywalls, contributions, and subscription models directly from Google.

## Configuration Requirements
To use Reader Revenue Manager, the user must have an active Google Publisher Center account and publication.
- If the module fails to connect, ensure the user has completed the Publisher Center onboarding.
- The site must be served over HTTPS.

## Snippet Placement
Site Kit handles placing the required Reader Revenue Manager snippet on all pages. If the paywall or contribution dialog isn't appearing, check for:
- Caching plugins aggressively caching pages before the snippet was added.
- JavaScript errors in the theme preventing the Google scripts from initializing.

## Syncing Subscribers
Currently, Reader Revenue Manager manages the financial transactions and access on Google's end. If a user needs deeply integrated local WordPress user roles (e.g., assigning a specific WP Role when someone subscribes via Google), they would need a custom integration via webhooks, as Site Kit's primary role is snippet insertion.
