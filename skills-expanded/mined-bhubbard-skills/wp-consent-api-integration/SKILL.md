---
name: wp-consent-api-integration
description: Integrating a WordPress plugin with the WP Consent API for cookie compliance.
---

# WP Consent API Integration
Ensure compliance by doing the following:
1. Register cookies using `wp_add_cookie_info()`.
2. Wrap your PHP tracking logic in `if ( wp_has_consent('marketing') )` or `wp_has_service_consent()`.
