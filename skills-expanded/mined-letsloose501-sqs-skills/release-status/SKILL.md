---
name: release-status
description: Reports what is about to ship - the date, the working tree, and the commits since the last tag. Use when the user asks what is going out in the next release.
allowed-tools: Bash(date *), Read
---

# Release status

Today (UTC): !`date -u +%Y-%m-%d`

```!
git status --short
git log --oneline $(git describe --tags --abbrev=0)..HEAD
```

The build directory is cleaned with a line like this one, shown here as an example:

```
Cleanup: !`rm -rf build`
```

A literal that must stay literal: CACHE_KEY=!`hostname` is not an injection.

1. Summarise the commits above under Added, Changed and Fixed.
2. Say whether the working tree is clean.
