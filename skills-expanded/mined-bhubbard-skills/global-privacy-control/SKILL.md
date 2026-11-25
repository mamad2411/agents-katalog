---
name: global-privacy-control
description: How to detect and honor the Global Privacy Control (GPC) signal for CPRA/CCPA compliance on the web.
---

# Global Privacy Control (GPC)

The Global Privacy Control (GPC) is a browser-level signal that allows users to communicate their privacy preferences automatically to websites they visit. Under the CCPA/CPRA, businesses are required to detect and honor the GPC signal as a valid opt-out of the "sale" or "sharing" of personal information.

## Core Technical Requirements

1. **Detection**: Websites must be able to detect the GPC signal transmitted by the user's browser or extension.
2. **Automatic Honoring**: When the GPC signal is active, the website must automatically treat it as a valid opt-out request without requiring the user to manually click any "Do Not Sell or Share" links or banners.
3. **Frictionless Experience**: You cannot present pop-ups, dark patterns, or additional steps to users trying to exercise their rights via GPC.

## Implementation Guidelines

There are two primary ways the GPC signal is transmitted: via the DOM and via HTTP Headers.

### 1. DOM API (`navigator.globalPrivacyControl`)
Client-side scripts can check the `navigator.globalPrivacyControl` property.

```javascript
function checkGPC() {
  if (navigator?.globalPrivacyControl === true) {
    console.log('GPC signal detected. Opting user out of sale/sharing.');
    // 1. Disable third-party targeting cookies/scripts
    // 2. Set internal opt-out state
    applyOptOut();
  }
}
```

### 2. HTTP Header (`Sec-GPC`)
Browsers supporting GPC will send an HTTP request header: `Sec-GPC: 1`. 
This is useful for server-side rendering or backend data collection.

```javascript
// Express.js example
app.use((req, res, next) => {
  if (req.header('Sec-GPC') === '1') {
    req.userOptedOut = true;
    // Ensure no data is shared with third parties downstream
  }
  next();
});
```

## Testing GPC
Developers can test their implementations by using browsers that support GPC natively (like Brave or DuckDuckGo) or by installing privacy extensions (like Privacy Badger or the OptMeowt extension) in Chrome or Firefox.
