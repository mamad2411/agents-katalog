---
name: tag-assistant-troubleshooting
description: "Guidelines for using the Google Tag Assistant Companion extension to troubleshoot unverified tags and conversion tracking issues."
---

# Google Tag Assistant Troubleshooting

The Google Tag Assistant Companion extension enables deep debugging for Google tags (Google Analytics 4, Google Ads, Floodlight, etc.) by connecting your browser session to `tagassistant.google.com`.

## Core Features

### 1. Connection and Verification
*   **The Companion Extension:** While you can use `tagassistant.google.com` natively, installing the Chrome extension allows Tag Assistant to connect across multiple tabs, handle iframes correctly, and debug sites without requiring you to inject a debug parameter into the URL explicitly.
*   **Connecting:** Navigate to `tagassistant.google.com`, enter the target URL, and click "Connect". The extension injects the necessary hooks to open a debug window.

### 2. Identifying Tag Issues
*   **Hits Sent:** Verify that the correct tags (e.g., `G-XXXXXXX` or `AW-XXXXXXX`) have fired on the page load.
*   **Errors/Warnings:** The assistant will flag issues such as:
    *   **Invalid format:** Malformed tracking IDs.
    *   **Duplicate tags:** The same tag firing multiple times on the same page.
    *   **HTTP response issues:** A tag firing but failing to hit Google's servers (e.g., blocked by AdBlockers or CORS).

## Troubleshooting Flow
1. Open Tag Assistant and connect to the URL.
2. Perform the desired user journey (e.g., adding to cart, submitting a lead form).
3. Switch back to the Tag Assistant tab and verify that the specific Conversion or Event tag fired immediately after the user action. If it did not fire, check the triggering logic in Google Tag Manager or the hardcoded script placement.
