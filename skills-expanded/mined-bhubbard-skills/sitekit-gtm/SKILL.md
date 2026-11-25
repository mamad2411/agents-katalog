---
name: sitekit-gtm
description: Using Site Kit to deploy Google Tag Manager. Use when resolving conflicts between GTM and hardcoded Analytics scripts.
---

# Site Kit Google Tag Manager (GTM)

Site Kit can automatically insert the GTM container snippets.

## Analytics vs. GTM
If a user is using GTM to deploy Google Analytics, they should *not* also have Site Kit deploy the Analytics snippet, as this causes double-tracking.
- In Site Kit > Settings > Analytics, they can toggle off "Let Site Kit place code on your site" if they are managing GA via GTM.

## AMP Containers
If the site uses the official AMP plugin, Site Kit asks for both a Web container ID and an AMP container ID, as GTM requires different configurations for AMP pages. Ensure the user has created an AMP-specific container in their GTM account.
