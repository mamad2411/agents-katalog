---
name: tag-assistant-gtm
description: "Guidelines for utilizing Google Tag Assistant to debug Google Tag Manager (GTM) implementations, focusing on the dataLayer and event triggers."
---

# Google Tag Assistant & GTM

When debugging a Google Tag Manager (GTM) container, the Google Tag Assistant serves as the primary "Preview Mode" interface.

## Debugging Workflow

### 1. The Summary Timeline
The left-hand sidebar of Tag Assistant shows every event pushed to the `dataLayer` in chronological order (e.g., `Container Loaded`, `DOM Ready`, `Window Loaded`, `Click`, `Custom Event`).

### 2. Inspecting the dataLayer
Clicking on any specific event in the timeline allows you to inspect the state of the `dataLayer` at that exact moment.
*   **DataLayer Tab:** Shows what key/value pairs were pushed (e.g., `ecommerce` objects, user IDs, custom parameters).
*   **Variables Tab:** Shows the resolved value of every GTM Variable during that event.

### 3. Verifying Triggers
To understand *why* a tag did or did not fire:
1. Click the Tag in question under the "Tags Fired" or "Tags Not Fired" section.
2. Scroll down to the **Firing Triggers** section.
3. Tag Assistant will show a green checkmark next to conditions that were met, and a red X next to conditions that failed. 
4. **Resolution:** If a tag failed to fire, use the red X to identify exactly which Variable or Condition in GTM is misconfigured.
