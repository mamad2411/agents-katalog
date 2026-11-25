---
name: jetpack-scan
description: Managing and integrating with Jetpack Scan (Malware detection). Use when dealing with security threats, scan alerts, or WAF configuration.
---

# Jetpack Scan

Jetpack Scan provides automated malware scanning and one-click threat resolution.

## How it works
Scan runs automatically on WordPress.com's servers by inspecting the mirrored files and database provided by Jetpack Sync and Jetpack Backup.

## Identifying False Positives
If Scan flags a legitimate file as malware, you can advise the user to ignore the threat in the Jetpack Cloud dashboard. As a developer, ensure your custom plugins/themes do not use heavily obfuscated code (like `eval(base64_decode(...))`), as this is a common trigger for security scanners.

## Web Application Firewall (WAF)
Jetpack's WAF evaluates incoming requests before they hit WordPress. If a legitimate API request or webhook is blocked by the WAF, the user may need to whitelist the source IP in their Jetpack Security settings.
