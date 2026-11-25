---
name: show-diff
description: Render git diff as a beautiful HTML5 page and return the generated HTML file directly for visual review.
---

# Show Git Diff as HTML

Convert raw `git diff` output into a styled standalone HTML5 page and return the generated file directly to the user.

## Prerequisites

- Git repository in current directory
- Python 3.x (for the conversion script)
- No external dependencies needed

## Steps

1. **Generate and convert diff to HTML**
   ```bash
   cd /home/chihmin/Assetsentry/AssetSentry
   python3 /home/chihmin/.hermes/skills/devops/show-diff/scripts/diff2html.py
   ```
   Or with a specific diff file:
   ```bash
   python3 /home/chihmin/.hermes/skills/devops/show-diff/scripts/diff2html.py /tmp/my-diff.patch
   ```

2. **Return the HTML file directly**
   - The converter writes `/tmp/git-diff.html`.
   - In the final response, attach it with the required outbox marker:
     ```text
     [[file: /tmp/git-diff.html]]
     ```
   - Do not start an HTTP server or return a hosted URL unless the user explicitly requests hosting.

## Notes

- The HTML output uses GitHub-dark theme styling
- Syntax highlighting for additions (green) and deletions (red)
- File sections are collapsible
- Print-friendly layout included
- Always attach the generated HTML file directly with `[[file: /tmp/git-diff.html]]`
- Server runs on port 8899 (change if needed)

## Script Location

The conversion script is at `scripts/diff2html.py` within this skill directory.