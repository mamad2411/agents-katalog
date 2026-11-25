---
name: user-story-generator
description: >
  A skill that generates user stories based on backlog items. When the PO provides a backlog (e.g., implement account-related features),
  it analyzes the current codebase and generates specific user stories as markdown files.
  Use this skill when user story writing, backlog analysis, feature specification, or requirements documentation is requested.
---

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

# User Story Generator

Analyzes backlog items and generates codebase-based user stories.

## Workflow

### 1. Receive Backlog Input

Receive backlog items from the PO.

```
Example input:
- "Implement account-related features"
- "Improve product search functionality"
- "Refactor the payment process"
```

### 2. Codebase Analysis

Explore relevant code based on backlog keywords:

1. Keyword extraction: Identify core keywords from the backlog
2. File exploration: Search for related files using Glob/Grep
3. Structure understanding: Analyze existing implementation patterns and domain models

```
Example: "Account-related features" → Search keywords: user, account, auth, login, signup
```

### 3. Generate User Stories

Write user stories based on the analysis results.

#### Writing Format

```markdown
## [Major Feature Category]

### US-001: [Story Title]
**Story**: As a [user type], I can [feature/action].

**Acceptance Criteria**: (optional)
- [ ] [Specific condition 1]
- [ ] [Specific condition 2]
```

#### Writing Principles

- **Conciseness**: Express clearly in a single sentence
- **User-centric**: Use the format "As a [user type], I can [action]"
- **Hierarchical structure**: Organize as Major Feature (Depth 1) → Sub-feature (Depth 2)
- **Omit Why**: Omit the reason if the purpose is self-evident from the feature

### 4. File Output

Save the generated stories as a markdown file:

```
{project-root}/docs/{backlog-keyword}/user-stories.md
```

> **Directory Rule**: All artifacts are stored under the backlog-keyword directory.

## Output Example

Input: "Implement account-related features"

```markdown
# Account Features - User Stories

## 1. Sign Up

### US-001: New User Sign-up
**Story**: As an unregistered user, I can sign up with an email and password.

**Acceptance Criteria**:
- [ ] Email format validation
- [ ] Password at least 8 characters with special characters
- [ ] Duplicate email check

### US-002: Social Sign-up
**Story**: As an unregistered user, I can sign up easily using a social account (Google, Kakao).

## 2. Login

### US-003: Email Login
**Story**: As a registered user, I can log in with my email and password.

### US-004: Auto Login
**Story**: As a user, I can stay logged in.

## 3. Password Management

### US-005: Forgot Password
**Story**: As a user, I can reset my password via email verification.
```

## Acceptance Criteria Generation Guide

Include acceptance criteria only when the user requests them. Detailed guide: [references/acceptance-criteria.md](references/acceptance-criteria.md)

## References

- User Story Writing Guide: [references/user-story-guide.md](references/user-story-guide.md)
