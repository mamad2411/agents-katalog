---
name: elementor-popup-builder
description: Guides designing, triggering, and managing advanced popups using the Elementor Popup Builder.
---

# Elementor Popup Builder

This skill provides comprehensive instructions on designing, configuring, and optimizing popups using Elementor's Popup Builder.

## Core Features

### 1. Popup Design & Layout
Popups are built using the standard Elementor editor, allowing for limitless design possibilities.
- **Types:** Modals, slide-ins, bottom bars, full-screen overlays, and notification banners.
- **Positioning:** Control the exact alignment (center, corners, edges) and sizing (viewport height/width).
- **Overlay & Close Button:** Customize the background overlay and the style/position of the close button.

### 2. Publishing Settings
The true power of Elementor Popups lies in its publishing rules.
- **Conditions:** Determine *where* the popup can appear (e.g., Entire Site, Specific Pages, WooCommerce Product pages).
- **Triggers:** Determine *when* the popup appears based on user action.
  - On Page Load
  - On Scroll (e.g., down 50%)
  - On Scroll to Element
  - On Click (can also be linked dynamically to buttons)
  - After Inactivity
  - On Page Exit Intent
- **Advanced Rules:** Fine-tune the audience and frequency.
  - Show after X page views or sessions
  - Show up to X times per user
  - Hide for logged-in users
  - Show on specific devices
  - Show from specific referral URLs

## Advanced Implementations

- **Dynamic Content:** Use Elementor's dynamic tags within popups to show personalized data (e.g., user name, current post title).
- **Form Integration:** Embed Elementor Forms inside popups for newsletter signups, lead generation, or contact requests. Use actions after submit to automatically close the popup.
- **Menu Triggers:** Trigger a popup from a WordPress navigation menu item by using the dynamic tag for the URL field.

## Best Practices

- **User Experience (UX):** Avoid immediate full-screen popups on page load, as they frustrate users and can harm SEO (Google's intrusive interstitial penalty). Use Exit Intent or scroll triggers instead.
- **Accessibility:** Ensure popups can be closed easily via the `Esc` key and that focus is trapped within the popup while it is open.
- **Z-Index:** Be mindful of Z-index values to ensure popups appear above all other page content, including sticky headers.
