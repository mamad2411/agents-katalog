---
name: team-log
description: Create a team-facing work log from a development task and push it directly to a shared GitHub repository via gh CLI. Collects git context automatically and asks 2–3 focused questions for weekly team review. Use when the user wants to share what they worked on with their team.
---

# Team Log Skill

Turn a completed task into a team-facing work log and push it to the team's shared GitHub repository using `gh` CLI. Designed for weekly review — concise, factual, and easy to scan.

## Configuration

```
TEAM_REPO = the-swing/fe-work-logs
```

- `TEAM_REPO`: GitHub repository in `org/repo` format
- File path inside the repo is automatically set to `{git user.name}/{YYYY-MM-DD}-{task-name}.md`

## Prerequisites

- `gh` CLI must be installed and authenticated (`gh auth status`)

## Workflow

### Step 0 — Check configuration

Check if `TEAM_REPO` is still set to the placeholder value `the-swing/fe-work-logs`.

If it is:
1. Ask the user: "팀 로그를 올릴 GitHub 레포를 설정해주세요. (예: your-org/work-logs)"
2. Once the user provides the repo, update this SKILL.md file — replace the placeholder with the actual value
3. Confirm the repo is set and proceed

If `TEAM_REPO` is already configured, skip this step silently.

### Step 1 — Receive task input

The user provides:
- **Task name**: a short label for the task

If missing, ask for it before proceeding.

### Step 2 — Collect context automatically

Without asking the user, run:

```bash
git config user.name
git config user.email
git log --oneline -10
git diff HEAD~1 HEAD --stat
git status
gh pr view
```

Extract:
- **작업자**: from `git config user.name`
- **변경 파일 및 커밋**: from git log/diff
- **PR 링크**: from `gh pr view` if available

Do not ask the user about things you can derive from git.

### Step 3 — Interview the user

Ask exactly 3 questions, all at once:

1. 왜 이 방식을 선택했나요? (핵심 결정 한두 줄로)
2. 어려웠던 점이나 예상 밖이었던 것이 있었나요?
3. 팀원이 알아야 할 것이 있나요? (영향 범위, 주의사항, 의존성 등)

### Step 4 — Write and upload the log

Use the **obsidian-markdown skill** for structure — frontmatter and headings.

Use the **human-writer skill** for all prose content within each section. Apply its vocabulary, structural, and voice rules to every sentence written. The text should sound like the user wrote it, not like an AI summarized it.

Generate the markdown file and upload to the team repo via `gh` CLI:

```bash
# Write to temp file
cat > /tmp/team-log-output.md << 'EOF'
{file content}
EOF

# Upload to team repo
AUTHOR=$(git config user.name)
FILE_PATH="$AUTHOR/{YYYY-MM-DD}-{task-name}.md"

SHA=$(gh api repos/{TEAM_REPO}/contents/$FILE_PATH --jq '.sha' 2>/dev/null)

gh api repos/{TEAM_REPO}/contents/$FILE_PATH \
  --method PUT \
  -f message="team-log: {task-name}" \
  -f content="$(base64 -i /tmp/team-log-output.md)" \
  ${SHA:+-f sha="$SHA"}

# Clean up
rm /tmp/team-log-output.md
```

## Output Structure

```markdown
---
title: {Task Name}
date: {YYYY-MM-DD}
author: {git user.name}
tags:
  - team-log
status: done
---

# {Task Name}

| 항목 | 내용 |
|------|------|
| 작업자 | {git user.name} |
| 날짜 | {YYYY-MM-DD} |
| PR | {PR link or 없음} |

## 작업 내용

{변경된 파일과 커밋 요약. 짧은 bullet list.}

## 고민한 흔적

{핵심 결정 이유와 어려웠던 점. 1인칭으로, 2~4문장.}

## 영향 범위 및 팀 공유

{팀원이 알아야 할 것. 없으면 "없음".}

## 다음 액션

{이어질 작업이나 블로커. 없으면 생략.}
```

> You MUST write the entire log in Korean, regardless of the language the user used. Keep it concise — this is a team scan document, not a personal retrospective.
