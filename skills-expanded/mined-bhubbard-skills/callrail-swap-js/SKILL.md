---
name: callrail-swap-js
description: Using CallRail Swap.js for Dynamic Number Insertion (DNI) to track user sources.
---

# CallRail Swap.js (Dynamic Number Insertion)

## Overview
Swap.js is the JavaScript library used by CallRail for Dynamic Number Insertion (DNI). It detects phone numbers on your website and dynamically swaps them with the correct tracking number based on the visitor's source (e.g., Google Ads, Organic Search).

## Installation
Add the CallRail tracking snippet to the `<head>` of your website:
```html
<script type="text/javascript" src="//cdn.callrail.com/companies/{company_id}/a/{account_id}/tracker.js" async></script>
```

## How It Works
- The script looks for elements on the page containing the "Swap Target" number (usually your main business number).
- It analyzes the visitor's HTTP referrer and URL parameters.
- It swaps the text (and `href` of `tel:` links) to the tracking number assigned to that source.
- It stores a cookie so returning visitors see the same tracking number.

## Customization
You can programmatically interact with Swap.js using the `CallRail` global object.
Example: Manually swap numbers if they are loaded dynamically via AJAX:
```javascript
CallRail.swap();
```

## Best Practices
- Ensure the destination number on your site exactly matches the Swap Target configured in CallRail.
- Avoid modifying the DOM in ways that conflict with Swap.js after the initial load, or ensure you call `CallRail.swap()` again.
- Use CSS classes to specifically target numbers for swapping if global swapping is problematic.
