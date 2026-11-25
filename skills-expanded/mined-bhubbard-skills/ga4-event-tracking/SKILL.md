---
name: ga4-event-tracking
description: Implement Google Analytics 4 (GA4) event tracking, including recommended and custom events. Use when adding tracking to web or app interactions.
---

# Google Analytics 4 Event Tracking

When the user requests to implement or debug GA4 event tracking, follow these guidelines:

## 1. Use the `gtag.js` API
For standard web tracking, use the `gtag()` function:
```javascript
gtag('event', 'event_name', {
  'parameter_name': 'parameter_value'
});
```

## 2. Prefer Recommended Events
Always check if a user action fits a [Recommended Event](https://developers.google.com/analytics/devguides/collection/ga4/reference/events) (e.g., `login`, `search`, `share`, `sign_up`) before creating a custom event name. This ensures better reporting and built-in features in GA4.

## 3. Custom Events
If a recommended event does not fit:
- Use clear, descriptive names using `snake_case`.
- Keep parameter names consistent across events.

## 4. Debugging
Remind the user to use the Google Analytics Debugger extension or the `debug_mode` parameter:
```javascript
gtag('event', 'custom_action', {
  'debug_mode': true
});
```
