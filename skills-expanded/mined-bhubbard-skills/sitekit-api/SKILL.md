---
name: sitekit-api
description: Utilizing the Site Kit JS and PHP APIs for custom metric retrieval. Use when building custom dashboard widgets or fetching specific Google data programmatically.
---

# Site Kit Developer APIs

Site Kit utilizes a robust internal API for managing data stores and fetching metrics.

## JavaScript Data Stores
Site Kit uses Redux-like data stores (via `@wordpress/data`) to manage state. Developers can tap into these stores if they are building custom UI elements in the WordPress admin.
```javascript
// Example: Selecting data from the Analytics store
const { getReport } = wp.data.select( 'modules/analytics-4' );
```

## PHP Custom Metrics
While Site Kit does not heavily advertise a public PHP API for fetching arbitrary metrics (it prefers the JS layer), you can interact with the underlying Google API client classes if necessary, though it is highly recommended to use the standard Google API PHP Client independently if you need complex, server-side data manipulation, as Site Kit's internal methods are subject to change.

## Webhooks and Cron
Site Kit relies on WordPress cron for some background tasks (like checking verification status). If the site's cron is broken, Site Kit setup may stall.
