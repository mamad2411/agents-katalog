---
name: icon-block-permissions
description: Troubleshooting permission issues with the Icon Block. Use when users (Authors, Contributors, Multisite Admins) report the block is broken or missing.
---

# Icon Block: Permission Issues (Unfiltered HTML)

Because SVGs are XML files that can contain malicious JavaScript, WordPress core heavily restricts who can insert and save them.

## The Restriction
Only users with the `unfiltered_html` capability can save SVGs.
- **Single Site**: Only Administrators and Editors have this capability. Authors and Contributors will find that the Icon Block fails to save or strips the SVG entirely.
- **Multisite**: *Only* Super Admins have the `unfiltered_html` capability. Standard Site Administrators cannot use the Icon Block by default.

## The Solution
To allow lower-level users or Multisite Administrators to use the Icon Block, developers must explicitly grant them the `unfiltered_html` capability.
- For Multisite, suggest using a plugin like **Unfiltered MU** or adding a custom code snippet to map the capability to standard Administrators. Note that this carries security risks if the users are not trusted.
