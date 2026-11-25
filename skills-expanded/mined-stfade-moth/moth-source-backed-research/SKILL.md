---
name: moth-source-backed-research
description: Research bug fixes with credible sources before guessing. Use when an error may depend on a framework, library, version, changelog, GitHub issue, pull request, release note, official documentation page, or accepted Stack Overflow answer.
---

# Moth Source Backed Research

## Source Order

Prefer sources in this order:

1. Official framework, language, package, or vendor docs.
2. Official changelogs and release notes for the installed or targeted version.
3. Maintainer-authored GitHub issues, discussions, and pull requests.
4. Accepted Stack Overflow answers when official sources do not cover the exact symptom.
5. Blog posts only when they cite primary sources and match the project version.

## Workflow

1. First decide whether local error output and provided context are enough.
2. If research is needed, identify the package, framework, error code, command, and version.
3. Search narrowly with the package name, version, and exact error text.
4. Prefer primary sources and verify dates/versions for fast-moving packages.
5. Turn the finding into the smallest change that explains the local error.
6. Cite source names or links in the fix brief when available.

## Guardrails

- Do not research just to research.
- Do not rely on random snippets that do not match the installed version.
- Do not quote long source passages.
- Do not use external research when local context already explains the fix.