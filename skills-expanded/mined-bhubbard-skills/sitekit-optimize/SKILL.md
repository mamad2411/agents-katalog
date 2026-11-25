---
name: sitekit-optimize
description: Handling questions about Google Optimize in Site Kit. Use when users ask how to run A/B tests or deal with legacy Optimize snippets.
---

# Site Kit & Google Optimize

**Google Optimize was officially sunset by Google on September 30, 2023.**

## Legacy Snippets
Because Optimize is deprecated, Site Kit no longer supports deploying the Optimize snippet or running A/B tests.
- If a user has an old site with the Optimize module still showing as active in their Site Kit database, it will no longer function.
- Advise the user to remove any hardcoded Optimize snippets (`optimize.js`) from their theme, as they may negatively impact site performance (especially the anti-flicker snippet) while providing no benefit.

## Alternatives
If a user is looking for A/B testing via Site Kit, you must inform them that Site Kit does not currently integrate with third-party A/B testing platforms natively. They will need to use alternative plugins or inject third-party scripts (like VWO or Optimizely) manually or via Google Tag Manager.
