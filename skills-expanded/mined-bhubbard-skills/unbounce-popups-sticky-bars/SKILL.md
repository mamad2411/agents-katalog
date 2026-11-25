---
name: unbounce-popups-sticky-bars
description: Guidance on integrating Unbounce Popups and Sticky Bars. Use when needing to embed dynamic conversion tools natively into a WordPress site.
---

# Unbounce: Popups & Sticky Bars

While Unbounce is famous for standalone landing pages, it also offers Popups and Sticky Bars that can be embedded directly onto existing WordPress content.

## Implementation Methods
There are two ways to deploy Popups and Sticky Bars to WordPress:
1. **Site-wide (The easy way)**: You can paste the Unbounce embed script into the WordPress header (using a plugin like Insert Headers and Footers or `wp_head` hooks). Unbounce's dashboard then controls which pages the popups trigger on via URL targeting rules.
2. **Specific Pages (The manual way)**: You can paste the embed script into the HTML block of a specific page or post.

## Troubleshooting Trigger Issues
If a popup isn't firing:
- Ensure the Unbounce embed script is placed directly before the closing `</head>` or `</body>` tag.
- Check if your WordPress site uses asynchronous script loading (defer/async) or JavaScript minification plugins (like Autoptimize), as these can prevent the Unbounce script from executing correctly.
