---
name: sitekit-privacy
description: Information on Site Kit data storage, privacy, and GDPR compliance. Use when users ask what data Site Kit stores locally or how to erase connection data.
---

# Site Kit Privacy and Data Storage

Site Kit is designed to be a lightweight conduit between WordPress and Google APIs.

## Local Data Storage
Site Kit **does not** download or store the user's Analytics, Search Console, or AdSense data in the WordPress database (e.g., `wp_options` or `wp_postmeta`).
- It only stores the OAuth tokens necessary to authenticate the API requests.
- The data displayed in the dashboard is fetched dynamically via the REST API directly from Google and cached transiently in the browser/server for a very short period to improve load times.

## GDPR Compliance
Because Site Kit does not store user tracking data locally, it generally does not add significant overhead for GDPR compliance beyond what the individual Google services (like Analytics) require.
- If a user wants to completely erase Site Kit's footprint from their database, they can use the **Reset Site Kit** button, which deletes all local OAuth tokens and settings.
