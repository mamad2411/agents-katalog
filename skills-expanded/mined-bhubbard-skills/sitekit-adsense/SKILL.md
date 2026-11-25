---
name: sitekit-adsense
description: Managing Google AdSense placements and account linking in Site Kit. Use when dealing with auto-ads snippets, account status issues, and caching conflicts.
---

# Site Kit AdSense

Site Kit connects to AdSense, places the Auto Ads snippet, and pulls revenue data into the WordPress dashboard.

## "Site Not Ready" or "Needs Attention"
If AdSense refuses to show ads, it is almost always an issue on the AdSense account side, not the plugin.
- Advise the user to log directly into `adsense.google.com` to check the Policy Center for violations (e.g., low-value content, scraped content).

## Snippet Placement Issues
Site Kit places the AdSense script in the `<head>` of the site.
- **Optimization Plugins**: Aggressive JS minification or deferral plugins (like Autoptimize or WP Rocket) can sometimes break the AdSense script or delay it too much. Advise excluding `adsbygoogle.js` from minification/deferral.

## ads.txt
Site Kit does not natively manage the `ads.txt` file (though some hosts or other plugins might). If AdSense warns about a missing `ads.txt`, the user must create it in the root directory of their WordPress installation.
