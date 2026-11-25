---
name: cli-scanning
description: Use Unlighthouse CLI to run full-site Lighthouse scans. Use this skill when the user wants to audit an entire website for performance, accessibility, best practices, and SEO using Unlighthouse.
---

# Unlighthouse CLI Scanning

Unlighthouse provides a powerful CLI to scan an entire website using Google Lighthouse. 

## Basic Usage

To scan a website, you can run Unlighthouse directly using `npx`:

```bash
npx unlighthouse --site <your-website-url>
```

This will discover all the routes on your site and run Lighthouse audits on them.

## Common CLI Options

- `--site <url>`: The base URL of the site to scan.
- `--root <path>`: The root directory of your project (useful if you have a config file there).
- `--debug`: Enable verbose logging to troubleshoot issues during the scan.

## Example
If you are developing locally on `http://localhost:3000` and want to scan it:
```bash
npx unlighthouse --site http://localhost:3000
```
