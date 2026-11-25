---
name: github-url-normalization-and-clone
description: Normalize GitHub URLs and perform shallow clones to a temp directory with cleanup.
---

# Github Url Normalization And Clone

Normalize GitHub URLs and perform shallow clones to a temp directory with cleanup.

## When to Use

Use this skill when:

- Working with code in `src/utils/git.ts/`
- User mentions "git"
- User mentions "clone"
- User mentions "github url"
- User mentions "normalize"
- User mentions "shallow"

## Patterns

- GitHub URL detection and normalization
- temp dir naming with random suffix
- shallow clone with --depth 1
- cleanup via fs.rm on completion

## Examples

```
const { path, cleanup } = await cloneRepo(url); await cleanup();
```

## Category

**reliability** - Error handling, recovery, and fault tolerance
