---
name: callrail-wp-setup
description: "Guidelines for installing and configuring the official CallRail Phone Call Tracking plugin in WordPress."
---

# CallRail WordPress Plugin Setup

The CallRail Phone Call Tracking plugin enables Dynamic Number Insertion (DNI) and form tracking directly within WordPress.

## Setup Instructions

1. **Install:** Install the `callrail-phone-call-tracking` plugin from the WordPress repository.
2. **Authenticate:** 
   * Navigate to the CallRail settings in the WordPress dashboard.
   * Input the CallRail API Key. The plugin will automatically trim surrounding whitespace.
   * *Note:* The tracking script (`swap.js`) will not be inserted into the DOM if the API key is missing or invalid.
3. **Configuration:** Select the appropriate Company from the CallRail dropdown menu.
4. **Validation:** Check the HTML source of the frontend site. The plugin injects a specific HTML comment near the `swap.js` script tag to indicate that it was successfully loaded via WordPress.
