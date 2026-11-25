---
name: managing-aws-codecommit
description: |
  Use when working with Aws Codecommit — aWS CodeCommit repository management
  and analysis. Covers repository inventory, branch details, pull request
  status, commit history, approval rules, and trigger configurations. Use when
  inspecting repositories, reviewing pull requests, auditing branch policies, or
  analyzing commit activity.
connection_type: aws
preload: false
---

# AWS CodeCommit Management Skill

Analyze and manage AWS CodeCommit repositories, branches, and pull requests.

## MANDATORY: Discovery-First Pattern

**Always list repositories before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== CodeCommit Repositories ==="
aws codecommit list-repositories --output text \
  --query 'repositories[].[repositoryName,repositoryId]'

echo ""
echo "=== Repository Details ==="
for repo in $(aws codecommit list-repositories --output text --query 'repositories[].repositoryName'); do
  aws codecommit get-repository --repository-name "$repo" --output text \
    --query 'repositoryMetadata.[repositoryName,defaultBranch,cloneUrlHttp,lastModifiedDate]' &
done
wait

echo ""
echo "=== Branches Per Repository ==="
for repo in $(aws codecommit list-repositories --output text --query 'repositories[].repositoryName'); do
  {
    branches=$(aws codecommit list-branches --repository-name "$repo" --output text --query 'branches[]' | wc -w)
    printf "%s\t%s branches\n" "$repo" "$branches"
  } &
done
wait
```

### Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== Open Pull Requests ==="
for repo in $(aws codecommit list-repositories --output text --query 'repositories[].repositoryName'); do
  for pr_id in $(aws codecommit list-pull-requests --repository-name "$repo" --pull-request-status OPEN --output text --query 'pullRequestIds[]' 2>/dev/null); do
    aws codecommit get-pull-request --pull-request-id "$pr_id" --output text \
      --query "pullRequest.[pullRequestId,title,authorArn,pullRequestStatus,creationDate]" &
  done
done
wait | head -20

echo ""
echo "=== Recent Commits (default branch) ==="
for repo in $(aws codecommit list-repositories --output text --query 'repositories[].repositoryName'); do
  {
    branch=$(aws codecommit get-repository --repository-name "$repo" --output text --query 'repositoryMetadata.defaultBranch')
    if [ -n "$branch" ] && [ "$branch" != "None" ]; then
      aws codecommit get-branch --repository-name "$repo" --branch-name "$branch" --output text \
        --query "branch.[\"$repo\",branchName,commitId]" 2>/dev/null
    fi
  } &
done
wait

echo ""
echo "=== Approval Rule Templates ==="
aws codecommit list-approval-rule-templates --output text \
  --query 'approvalRuleTemplateNames[]' 2>/dev/null

echo ""
echo "=== Repository Triggers ==="
for repo in $(aws codecommit list-repositories --output text --query 'repositories[].repositoryName'); do
  aws codecommit get-repository-triggers --repository-name "$repo" --output text \
    --query "triggers[].[\"$repo\",name,destinationArn]" 2>/dev/null &
done
wait
```

## Output Format

- Target ≤50 lines per output
- Use `--output text --query` for all commands
- Tab-delimited fields: RepoName, Branch, PRId, Status
- Limit commit history to last 5 per repository
- Never dump full diffs -- show commit metadata only

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Default branch**: Not all repos have a default branch set -- check for None/empty before querying
- **Pull request IDs**: List returns IDs only -- need separate `get-pull-request` call for details
- **Approval rules**: Templates must be associated with repos to take effect -- check associations
- **Triggers**: Support SNS and Lambda destinations -- verify destination ARN is valid
- **Repository size**: No direct API for repo size -- use `get-repository` metadata for last modified date
- **CodeCommit deprecation**: AWS has announced CodeCommit is no longer accepting new customers -- consider migration paths
