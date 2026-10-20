---
description: Project status briefing — codebase, history, deployments, last changes
allowed-tools: Bash, Read, Glob, Grep, Agent
---

# Project Status Briefing

You are a project analyst. Your job is to give the user a complete situational awareness briefing so they can get up to speed on this project in 30 seconds.

## Instructions

Gather information from ALL the sources below, then produce a single structured briefing. Use subagents to parallelize the research.

### 1. Codebase Analysis

- **Tech stack**: languages, frameworks, key dependencies (check package.json, requirements.txt, pyproject.toml, *.csproj, Cargo.toml, go.mod, pom.xml, etc.)
- **Folder structure**: high-level tree (max 2 levels deep), explain what each top-level folder contains
- **Key files**: entry points, config files, main modules
- **Architecture patterns**: monolith/microservices, API style (REST/GraphQL/gRPC), state management, key abstractions
- **Size**: approximate number of source files and lines of code

### 2. Project History — What We've Done

- Read `AGENT.md` for project overview and objectives
- Read the project's durable wiki / knowledge page if your team maintains one
- Read auto-memory files (`.claude/` project memory or `MEMORY.md`) for session history
- Summarize git log: total commits, contributors, major milestones
- Run: `git log --oneline --since="2 weeks ago"` for recent activity
- Run: `git log --oneline --all | tail -5` for the earliest commits

### 3. Last Modifications

- Run: `git log -5 --format="%h %s (%ar)" ` for the last 5 commits with relative dates
- Run: `git diff --stat HEAD~3` to show what files changed recently (if enough commits exist)
- Check `git status` for any uncommitted work in progress
- Check for any open branches: `git branch -a`

### 4. Deployment Status

Check for deployment indicators and report what you find:

- **Azure (azd)**: check for `azure.yaml`, `.azure/` folder, `infra/` folder with Bicep files
- **GitHub Actions**: check `.github/workflows/` for CI/CD pipelines
- **Docker**: check for `Dockerfile`, `docker-compose.yml`
- **Other CI/CD**: check for `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`, `bitbucket-pipelines.yml`
- **Git tags**: run `git tag --sort=-creatordate | head -5` for release/deploy tags
- **Last deploy**: if azd is used, check `.azure/` for environment state. If GitHub Actions, note the workflow files and what they do.
- If NO deployment config is found, say "No deployment configuration detected"

### 5. Current State

- Current branch and how it relates to main/master
- Any uncommitted changes or stashed work (`git stash list`)
- Open TODO items in code: search for `TODO`, `FIXME`, `HACK` in source files (report count, not each one)

## Output Format

Produce a briefing in this exact format:

```
## 🔍 Project Status: {project name}

### Tech Stack
{languages, frameworks, key deps — one line each}

### Architecture
{folder structure overview + patterns — keep it brief}

### History
- **Created:** {first commit date}
- **Total commits:** {count}
- **Recent activity:** {last 2 weeks summary}

### Last 5 Changes
{table: hash | message | when}

### Deployment
{deployment status, last deploy if known, CI/CD setup}

### Current State
- **Branch:** {current branch}
- **Uncommitted work:** {yes/no + summary}
- **Open TODOs:** {count}

### Key Takeaways
{2-3 bullet points: what's the most important thing to know right now}
```

Keep the entire briefing concise and scannable. No fluff. The user wants to read this in 30 seconds and know exactly where things stand.
