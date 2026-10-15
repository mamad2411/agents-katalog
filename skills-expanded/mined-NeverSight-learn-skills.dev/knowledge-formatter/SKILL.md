---
name: knowledge-formatter
description: Transform raw markdown into structured, vector-search-optimized team knowledge documents. Use when user wants to refactor, format, or structure documentation for team knowledge base.
---

# Knowledge Formatter Skill

Transform raw markdown into structured team knowledge documents.

**Rules:**
- Document content in Korean (한글), Skill metadata in English
- Filename: lowercase with hyphens (e.g., `lambda-ecr-permission-error.md`)
- Remove non-essential content, keep it concise

## Document Types

| Type | Purpose |
|------|---------|
| `problem` | Issue encountered and resolved |
| `decision` | Why we chose option A over B |
| `howto` | Step-by-step guide for doing X |
| `rule` | Team standard or process |

## Frontmatter Structure

```yaml
---
type: problem | decision | howto | rule
project: project-name
tags: [tag1, tag2, tag3]
date: YYYY-MM-DD
---
```

## Templates

### problem
```markdown
# 제목
## 문제 상황
## 원인
## 해결 방법
```

### decision
```markdown
# 제목
## 배경
## 선택지
## 결정
```

### howto
```markdown
# 제목
## 개요
## 방법
## 주의사항
```

### rule
```markdown
# 제목
## 목적
## 규칙
```

## Guidelines

- **Split if**: Over 3000 chars or mixed types
- **Title (# heading)**: Be specific and match filename
  - Bad: `문제 해결` → Good: `Lambda ECR 권한 문제`
  - Filename and title must match (file: `lambda-ecr-permission-error.md` → title: `# Lambda ECR 권한 문제`)
- **Project**: Fill with current project name
- **Tags**: 3-7 items, use specific tech names (e.g., `lambda`, `ecr`, `permission`)
- **Error messages**: Include verbatim