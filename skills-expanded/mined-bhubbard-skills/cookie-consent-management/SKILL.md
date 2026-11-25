---
name: cookie-consent-management
description: Guidelines and technical implementation details for CPRA/CCPA compliant cookie consent banners and script management.
---

# CPRA/CCPA Cookie Consent Management

Under the California Consumer Privacy Act (CCPA) and the California Privacy Rights Act (CPRA), websites must provide a "Notice at Collection" to users regarding the personal information being collected, including via cookies and trackers.

## Core Technical Requirements

1. **Notice at Collection**: Provide a clear, conspicuous notice at or before the point of data collection. Usually implemented as a banner on the user's first visit.
2. **Cookie Categorization**: Group cookies into logical categories (e.g., Strictly Necessary, Analytics, Marketing/Targeting, Preferences).
3. **Prior Consent / Opt-Out**: While GDPR requires explicit opt-in before non-essential cookies are dropped, CCPA/CPRA operates heavily on an opt-out model for the "sale" or "sharing" of personal information. However, you must still inform the user and provide an accessible mechanism to opt-out of cookies that constitute a sale or share (like third-party advertising cookies).
4. **Link to Privacy Policy**: The consent banner must include a direct link to the full privacy policy.

## Implementation Guidelines

- **Script Blocking**: Ensure that third-party scripts (like Google Analytics, Meta Pixel) are configurable and can be disabled if a user exercises their right to opt out of the "sale or sharing" of their data.
- **State Management**: Persist the user's consent preferences (usually in a first-party cookie or local storage) so they aren't asked repeatedly, and so their preferences are respected across the site.
- **Accessibility**: Ensure the cookie banner is accessible (WCAG compliant), navigable via keyboard, and readable by screen readers.

## Example: Checking Consent State before loading a script
```javascript
function loadMarketingScripts() {
  const userPreferences = JSON.parse(localStorage.getItem('privacy_preferences') || '{}');
  if (userPreferences.marketing !== false) {
    // Load tracking pixel or marketing scripts here
  }
}
```
