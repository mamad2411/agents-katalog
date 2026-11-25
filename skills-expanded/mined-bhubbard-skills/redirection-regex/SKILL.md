---
name: redirection-regex
description: Guidance on using Regular Expressions in the Redirection plugin. Use when troubleshooting complex URL matching or setting up wildcard redirects.
---

# Redirection: Regular Expressions (Regex)

The Redirection plugin supports full regular expressions, allowing you to match a limitless number of URLs with a single rule.

## Common Use Cases
- **Wildcard redirects**: Redirecting an entire directory to a new one.
  - Source: `^/old-folder/(.*)`
  - Target: `/new-folder/$1`
  - Ensure the "Regex" checkbox is checked!

## Troubleshooting Regex
- **Trailing Slashes**: A common mistake is not accounting for trailing slashes. Use `/?` at the end of the source pattern to make the trailing slash optional (e.g., `^/old-page/?$`).
- **Escaping Characters**: Ensure special characters in the URL (like `.` or `?`) are properly escaped with a backslash `\` if they are meant to be matched literally.
- **Search Regex Integration**: The plugin is compatible with the `Search Regex` plugin, making bulk updates to database redirects easier.
