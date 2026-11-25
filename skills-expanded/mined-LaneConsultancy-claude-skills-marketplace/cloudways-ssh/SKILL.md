---
name: cloudways-ssh
description: SSH into Cloudways WordPress servers to run WP-CLI commands, manage files, check logs, and administer WordPress installations. Use when the user asks to check WordPress, run WP-CLI, manage plugins/themes, check server logs, or do anything on the Cloudways server.
user-invocable: true
---

# Cloudways SSH Skill

Connect to Cloudways-hosted WordPress installations via SSH to run WP-CLI commands, manage files, check logs, and administer sites.

## Usage

```
/cloudways-ssh
```

Or Codex will automatically use this skill when you ask about WordPress admin tasks, WP-CLI, server logs, plugin management, or Cloudways server operations.

## Connection Details

SSH is configured via `~/.ssh/config` with the alias `thames-boilers-wp`:

```bash
ssh thames-boilers-wp
```

- **Host:** 159.65.187.71
- **User:** master_jhvvtrenyd
- **Key:** ~/.ssh/id_rsa_cloudways
- **Port:** 22

## WordPress Applications on This Server

| App ID | Site Name | URL |
|--------|-----------|-----|
| exszcqrefg | Thames Boilers Blog | wordpress-1405378-6246321.cloudwaysapps.com |
| qcprhzwcpk | Thames Boilers (main) | thamesboilers.co.uk |
| epwfvjxaqw | Invicta Boilers | invictaboilers.co.uk |
| hbrxafvwcu | Boiler Champs | boilerchamps.co.uk |
| bubagkjweb | Lane Consultancy | laneconsultancy.com |
| mfkjwufbkh | Local Trade Customers | localtradecustomers.co.uk |
| murhtgveyu | Plumber Greenhithe | plumbergreenhithe.co.uk |
| shamvpvukt | Rating Rocket | ratingrocket.co.uk |
| fgwfspynjk | James Lane | jameslane.org |
| ztvrppctjp | The Healing Lane | healinglane.co.uk |
| ugdgmuhbja | Proptrest Backend | wordpress-1405378-6186514.cloudwaysapps.com |

## Key Paths

Each WordPress installation lives at:
```
~/applications/{app_id}/public_html/
```

**Thames Boilers Blog** (primary for this project):
```
~/applications/exszcqrefg/public_html/
```

## Common Commands

### WP-CLI (always specify --path)

```bash
# Post count
ssh thames-boilers-wp "cd ~/applications/exszcqrefg/public_html && wp post list --post_type=post --post_status=publish --format=count"

# List recent posts
ssh thames-boilers-wp "cd ~/applications/exszcqrefg/public_html && wp post list --post_type=post --post_status=publish --fields=ID,post_title,post_date --format=table --orderby=date --order=DESC --posts_per_page=10"

# Check plugins
ssh thames-boilers-wp "cd ~/applications/exszcqrefg/public_html && wp plugin list --format=table"

# Check theme
ssh thames-boilers-wp "cd ~/applications/exszcqrefg/public_html && wp theme list --format=table"

# Database search/replace (dry-run first!)
ssh thames-boilers-wp "cd ~/applications/exszcqrefg/public_html && wp search-replace 'old-url' 'new-url' --dry-run"

# Export database
ssh thames-boilers-wp "cd ~/applications/exszcqrefg/public_html && wp db export -"

# Check site health
ssh thames-boilers-wp "cd ~/applications/exszcqrefg/public_html && wp option get siteurl && wp option get home"
```

### Server / Logs

```bash
# Nginx error log (Cloudways path)
ssh thames-boilers-wp "tail -50 ~/applications/exszcqrefg/logs/error.log"

# PHP error log
ssh thames-boilers-wp "tail -50 ~/applications/exszcqrefg/logs/php-fpm-error.log 2>/dev/null"

# Disk usage
ssh thames-boilers-wp "du -sh ~/applications/exszcqrefg/public_html/wp-content/uploads/"
```

### Working with Other Sites

Replace `exszcqrefg` with the app ID from the table above. Example for the main Thames Boilers site:
```bash
ssh thames-boilers-wp "cd ~/applications/qcprhzwcpk/public_html && wp post list --post_status=publish --format=count"
```

## Notes

- The master user has access to ALL applications on the server
- WP-CLI is available at `/usr/local/bin/wp`
- WordPress version: 6.9.1 (as of March 2026)
- Thames Boilers Blog has 417 published posts
- The blog app (`exszcqrefg`) uses a Cloudways staging URL — it's the headless CMS backend for the Astro frontend
