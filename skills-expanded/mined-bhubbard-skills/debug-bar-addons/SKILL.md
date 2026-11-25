---
name: debug-bar-addons
description: Information about extending the Debug Bar plugin with add-ons.
---

# Debug Bar Addons

The Debug Bar is extensible. You can install add-ons such as "Debug Bar Console" to run PHP/MySQL right from the bar.

Many add-ons exist in the WordPress repository for:
- Registered Post Types
- Shortcodes
- WP Cron
- Language file loading
- Actions and Filters

To add functionality to the Debug Bar, you typically hook into `debug_bar_panels` and provide a custom class extending `Debug_Bar_Panel`.
