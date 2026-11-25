---
name: pre-deployment
description: "Group skill: Pre-deployment checklist — code quality, security audit, dependency scan, performance, accessibility, SEO, build verification, Docker, environment config, and final commit."
risk: medium
source: self
---

# 🚀 Pre-Deployment Checklist

> **Group Skill** — Orchestrates sub-skills for thorough pre-deployment verification.
> Activate by saying: "Run pre-deployment checks" or "pre-deploy checklist"

## When to Use

- About to deploy to production
- Need to verify code quality, security, and performance
- Final gate before shipping

## Step-by-Step Workflow

### Step 1: Code Quality
**Skill**: `code-reviewer`
- Review for bugs, anti-patterns, readability
- Check error handling and edge cases
- Verify naming conventions

### Step 2: Security Audit
**Skill**: `security-auditor`
- Scan for vulnerabilities
- Check for exposed secrets
- Review authentication flows

### Step 3: Dependency Scan
**Skill**: `security-scanning-security-dependencies`
- Check for outdated/vulnerable packages
- Review dependency tree for bloat
- Update critical dependencies

### Step 4: Performance
**Skill**: `performance-engineer`
- Profile slow code paths
- Check memory usage
- Verify database query efficiency

### Step 5: Accessibility
**Skill**: `ui-a11y`
- WCAG 2.2 AA compliance check
- Screen reader compatibility
- Keyboard navigation

### Step 6: SEO
**Skill**: `seo-audit`
- Meta tags and descriptions
- Broken link check
- Crawlability verification

### Step 7: Build Verification
**Skill**: `vercel-deployment`
- Verify build passes
- Check build output size
- Review deployment config

### Step 8: Docker Check
**Skill**: `docker-expert`
- Review container layers
- Check for secrets exposure
- Optimize image size

### Step 9: Environment Config
**Skill**: `secrets-management`
- Verify no hardcoded secrets
- Check environment variables
- Review vault configuration

### Step 10: Final Commit
**Skill**: `git-pr-review`
- Clean PR description
- Verify all tests pass
- Confirm changelog updated

## Completion

All pre-deployment checks pass. Ready to deploy! 🚀

## Sub-Skills Referenced

1. `code-reviewer`
2. `security-auditor`
3. `security-scanning-security-dependencies`
4. `performance-engineer`
5. `ui-a11y`
6. `seo-audit`
7. `vercel-deployment`
8. `docker-expert`
9. `secrets-management`
10. `git-pr-review`
