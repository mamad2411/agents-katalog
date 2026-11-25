---
name: npm-research
description: Research npm packages with bundle size, vulnerability scanning, and download trends via MCP. Use when comparing or auditing packages.
---

# npm Package Research via MCP

Use this skill for in-depth npm package research: bundle sizes, vulnerability scanning, download comparisons, and dependency trees. No API keys needed.

## Available Tools

| Tool                | What it does                                            |
| ------------------- | ------------------------------------------------------- |
| `search`            | Search npm packages by query                            |
| `package_info`      | Detailed info: description, license, repo, dependencies |
| `downloads`         | Download stats for a package                            |
| `compare_downloads` | Compare download counts across multiple packages        |
| `bundle_size`       | Bundle size (minified + gzip) via Bundlephobia          |
| `vulnerabilities`   | Known vulnerability info and advisory links             |
| `dependency_tree`   | Show direct dependencies as a tree                      |
| `download_trends`   | Daily breakdown with sparkline visualization            |

## Workflow

1. For "which library?" questions: `compare_downloads` + `bundle_size` for each candidate
2. For security audits: `vulnerabilities` on each dependency
3. For adoption analysis: `download_trends` to see growth patterns
4. For dependency footprint: `dependency_tree` before adding a new package

## Key Patterns

- `bundle_size` calls Bundlephobia — some packages may not be analyzable (native modules, very large packages)
- `compare_downloads` accepts multiple package names — ideal for "zustand vs jotai vs valtio" comparisons
- `vulnerabilities` checks npm audit advisories — always run this before recommending a package
- `download_trends` includes a text sparkline for quick visual trend assessment
