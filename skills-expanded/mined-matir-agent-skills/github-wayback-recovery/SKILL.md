---
name: github-wayback-recovery
description: Recover deleted GitHub content using the Wayback Machine and Archive.org APIs.
metadata:
  version: 0.2.0
  category: oss-forensics
---
# GitHub Wayback Recovery

## Quick Start
```bash
# Check if a repository page was archived
curl -s "https://archive.org/wayback/available?url=github.com/owner/repo" | jq

# Search for all archived URLs under a repository
curl -s "https://web.archive.org/cdx/search/cdx?url=github.com/owner/repo/*&output=json&collapse=urlkey"
```

## Workflow
1. **Discovery**: Use the availability API to check if the target URL has any snapshots.
2. **Indexing**: Use the CDX API with `matchType=prefix` to find all archived URLs for the repository.
3. **Retrieval**: Access specific snapshots using the `https://web.archive.org/web/{TIMESTAMP}/{URL}` pattern.
4. **Extraction**: Manually extract text from rendered pages or use tools like `waybackpack` for bulk recovery.
5. **Verification**: Check identified fork usernames to see if the full git history persists elsewhere.

## Rules & Constraints
- **RULE-1**: Archive.org captures web pages (HTML), NOT git repositories; you cannot `git clone` from them.
- **RULE-2**: Private repositories are never crawled and cannot be recovered.
- **RULE-3**: Respect Archive.org rate limits (~100 requests/minute).
- **RULE-4**: Focus on `blob` (files) and `issues`/`pull` URLs for content recovery.

## When to Use
- Repository has been deleted and you need README, wiki, or metadata.
- Issues or PRs were deleted and original conversation is needed.
- Investigating the historical state of a repository.

## When NOT to Use
- Need to reconstruct full git commit history (use `github-commit-recovery` if SHAs are known).
- Private repository content.
- Content behind authentication.

## References
- [Skill Manual](references/github-wayback-recovery-manual.md)
- [Wayback Machine CDX API](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server)
