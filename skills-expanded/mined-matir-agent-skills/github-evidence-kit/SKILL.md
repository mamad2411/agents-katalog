---
name: github-evidence-kit
description: Forensic evidence kit for GitHub and local git repositories. Specializes in recovering dangling commits and verifying history integrity.
metadata:
  version: 0.2.0
  category: oss-forensics
---
# GH Evidence Kit

## Quick Start
```python
from assets.src.collectors import GitHubAPICollector, LocalGitCollector
from assets.src import EvidenceStore

# Collect from API and Local Git
github = GitHubAPICollector()
local = LocalGitCollector("/path/to/repo")

commit = github.collect_commit("owner", "repo", "sha")
dangling = local.collect_dangling_commits()

# Store and Export
store = EvidenceStore()
store.add(commit)
store.add_all(dangling)
store.save("evidence.json")
```

## Workflow
1. **Collection**: Use specialized collectors (API, Local Git, GH Archive, Wayback) to gather evidence.
2. **Storage**: Add collected evidence to an `EvidenceStore` for centralized management.
3. **Filtering**: Query the store by observation type, source, repository, or timestamp.
4. **Verification**: Re-verify collected evidence against original sources to ensure integrity.
5. **Export**: Save the evidence collection to JSON for archival or forensic reporting.

## Rules & Constraints
- **RULE-1**: Use `LocalGitCollector` for "dangling" commits to find force-pushed or deleted history.
- **RULE-2**: GH Archive queries require `GOOGLE_APPLICATION_CREDENTIALS` for BigQuery.
- **RULE-3**: Respect GitHub API rate limits (5,000/hr authenticated).
- **RULE-4**: Maintain forensic integrity by keeping evidence IDs unique and immutable.

## When to Use
- Creating verifiable evidence objects from GitHub activity.
- Analyzing local git forensics (dangling commits, reflog).
- Recovering deleted content from GH Archive or Wayback Machine.

## When NOT to Use
- Real-time intrusion prevention (use EDR/SIEM).
- General project management or git workflow automation.

## References
- [Skill Manual](references/github-evidence-kit-manual.md)
- [GH Archive](https://www.gharchive.org/)
- [Wayback Machine](https://archive.org/web/)
