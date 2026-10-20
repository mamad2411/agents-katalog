# GitHub Manager - Full Command Reference

> Loaded on-demand. Header: [../github-manager.md](../github-manager.md)

## 1. GitHub Status Dashboard

```bash
gh status                    # 전체 상태 (이슈, PR, 리뷰, 멘션)
gh status -o <org-name>      # 특정 org만
gh status -e owner/repo      # 특정 repo 제외
```

## 2. Issue Management

```bash
# List
gh issue list
gh issue list --state open --assignee @me
gh issue list --label "bug" --limit 20
gh issue list --json number,title,state,labels

# Create
gh issue create --title "Title" --body "Body" --label "bug,priority:high" --assignee @me
gh issue create --template bug_report.md

# View
gh issue view <number>
gh issue view <number> --web
gh issue view <number> --json title,body,comments

# Branch from issue (GitHub Flow)
gh issue develop <number> --checkout
gh issue develop <number> --name feature/my-feature --checkout

# Close/Reopen
gh issue close <number> --reason completed
gh issue close <number> --reason "not planned"
gh issue reopen <number>

# Comment
gh issue comment <number> --body "Comment text"
```

## 3. Pull Request Management

```bash
# List
gh pr list [--state all] [--author @me] [--json number,title,state,reviewDecision]

# Create
gh pr create --title "feat: feature" --body "Description" --base main --label "enhancement"
gh pr create --draft --title "WIP: feature"
gh pr create --title "Fix #123: bug description"  # 이슈 연결

# Review
gh pr edit <number> --add-reviewer user1,user2
gh pr review <number> --approve
gh pr review <number> --request-changes --body "Please fix X"

# Merge
gh pr merge <number> [--squash|--rebase]
gh pr merge <number> --auto --squash  # CI 통과 후 자동

# Checks
gh pr checks <number> [--watch]
```

## 4. CI/CD Monitoring

```bash
# List runs
gh run list [--workflow=ci.yml] [--branch main] [--status failure]

# View details
gh run view <run-id> [--log] [--log-failed] [--web]

# Watch (real-time)
gh run watch [<run-id>]

# Rerun
gh run rerun <run-id> [--failed]

# Workflows
gh workflow list
gh workflow run <name> [--ref main] [-f environment=production]
```

## 5. Release Management

```bash
# List
gh release list [--limit 10]

# Create
gh release create v1.0.0 --title "v1.0.0" --notes "Notes"
gh release create v1.0.0 ./dist/*.zip --notes-file CHANGELOG.md
gh release create v1.0.0 --draft
gh release create v1.0.0-beta.1 --prerelease
gh release create v1.0.0 --generate-notes  # 자동 릴리스 노트

# View/Download
gh release view v1.0.0 [--web]
gh release download v1.0.0 [--pattern "*.zip"]
```

## 6. Repository Management

```bash
gh repo view [--web] [--json name,description,stargazerCount]
gh repo clone owner/repo [-- --depth 1]
gh repo fork owner/repo [--clone]
gh repo create my-repo --public --description "My repo"
```

## 7. Search

```bash
gh search issues "bug auth" --repo owner/repo
gh search prs "review:required" --author @me
gh search code "function authenticate" --repo owner/repo
gh search repos "react component library" --language typescript
```

## 8. Labels Management

```bash
gh label list
gh label create "priority:high" --color FF0000 --description "High priority"
gh label edit "bug" --color 00FF00
```

## 9. Integration with cc-initializer

```bash
# Sprint → Issue
gh issue create --title "[Sprint-1] Task" --label "sprint:1,task" --milestone "Sprint 1"

# Phase → Milestone
gh api repos/{owner}/{repo}/milestones --method POST --field title="Phase 1" --field due_on="2026-02-01T00:00:00Z"

# CI failure analysis
gh run view --log-failed | grep -A 5 "Error:"
```

## Output Templates

### Status Report
```markdown
## GitHub Status Report
**Repository**: owner/repo

### Open Issues: 12
| Priority | Count |
|----------|-------|
| High | 3 | Medium | 5 | Low | 4 |

### Open PRs: 4
| Status | Count |
|--------|-------|
| Review Required | 2 | Approved | 1 |

### Action Items
- [ ] Review PR #456
- [ ] Respond to mention in #789
```

### CI Failure Report
```markdown
## CI Failure Analysis
**Run**: #12345 | **Branch**: feature/new-feature

### Failed Jobs
1. **test** - Error: Test "auth.test.ts" failed

### Suggested Actions
1. Check authentication test mocks
2. Run locally: `npm test -- auth.test.ts`
Quick: `gh run rerun 12345`
```

## Best Practices
1. Always check auth: `gh auth status`
2. Use JSON output for parsing: `--json field1,field2`
3. Use `--web` to quickly open in browser
4. Auto-merge with `--auto` for CI-gated merges
5. Generate notes with `--generate-notes` for releases
