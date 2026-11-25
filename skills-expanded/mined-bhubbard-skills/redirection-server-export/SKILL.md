---
name: redirection-server-export
description: Exporting redirects to server-level configurations. Use when optimizing performance by bypassing PHP and handling redirects via Apache or Nginx.
---

# Redirection: Server-Level Export (Apache/Nginx)

By default, the Redirection plugin processes redirects using WordPress and PHP. For sites with thousands of redirects, this can negatively impact Time To First Byte (TTFB).

## Exporting for Performance
You can export your redirects so they are handled directly by the web server, which is significantly faster.

### Apache
The plugin can automatically write redirects to your `.htaccess` file.
1. Go to Redirection > Options.
2. Configure it to save to the `.htaccess` file.

### Nginx
Nginx doesn't read `.htaccess` files.
1. Go to Redirection > Import/Export.
2. Export the rules as "Nginx rewrite rules".
3. Manually include the generated file in your server's Nginx configuration block and reload Nginx.

**Note**: When relying on server-level exports, Redirection's built-in "hit counter" and logging will no longer track those specific redirects.
