---
name: wp-consent-api-js-listeners
description: Using JavaScript listeners for WP Consent API to dynamically load scripts.
---

# WP Consent API JS Listeners
For clientside tracking scripts, listen for consent changes to dynamically initialize:
```javascript
document.addEventListener("wp_listen_for_consent_change", function (e) {
  // Check e.detail for category changes
});
```
