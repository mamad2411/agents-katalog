---
name: localwp-log-retrieval
description: Retrieve and analyze logs from LocalWP, including router, site, and PHP logs.
---

# LocalWP Log Retrieval

Use this skill to locate and read log files for troubleshooting LocalWP environments.

## Site-Specific Logs
Each site in LocalWP has its own logs for PHP, Nginx/Apache, and MySQL.
- **Location**: `~/Local Sites/{site-name}/logs/`
- **PHP Logs**: Look for `php/error.log` for fatal errors and warnings.
- **Web Server Logs**: Found in `nginx/` or `apache/`. Helpful for debugging 502 Bad Gateway errors.
- **Database Logs**: MySQL error logs are in `mysql/error.log`.

## Local Router Logs
The Local router handles mapping site domains (e.g., `.local`) to the correct container.
- **macOS**: `~/Library/Logs/local-lightning-router.log`
- **Windows**: `%AppData%\Roaming\Local\run\router\nginx\logs\`
- Use these logs if you encounter "Local Router Error" messages in the browser.

## Application Logs
For issues with the LocalWP app itself (starting, creating sites):
- **macOS**: `~/Library/Logs/local-lightning.log`
- **Windows**: `%AppData%\Roaming\Local\logs\local-lightning.log`
