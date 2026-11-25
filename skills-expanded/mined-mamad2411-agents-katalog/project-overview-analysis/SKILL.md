---
name: project-overview-analysis
description: "Generate a high-level overview of a git repository to establish context for threat modeling. Use when: (1) Starting threat modeling on an unfamiliar codebase, (2) Understanding project scope, purpose, and technology stack, (3) Identifying key stakeholders, deployment targets, and security posture, (4) Creating executive summaries for security assessments, (5) Establishing baseline context before deeper architectural analysis."
---

# Project Overview Analysis for Threat Modeling

Generate a comprehensive high-level overview of a git repository to establish context and scope for threat modeling activities.

## Analysis Workflow

```
1. Project identity          → Name, purpose, ownership, licensing
2. Technology stack          → Languages, frameworks, runtime
3. Project structure         → Organization, modules, components
4. Build & deployment        → Build system, containerization, targets
5. Documentation review      → README, docs, API specs
6. Dependency overview       → External dependencies, supply chain
7. DevOps & CI/CD           → Pipelines, automation, environments
8. Security indicators       → Existing security measures, configs
9. Output generation         → Executive summary for threat modeling
```

## Step 1: Project Identity

### Basic Project Information

```bash
# Repository name (from git or directory)
basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Git remote origin (ownership indicator)
git remote -v 2>/dev/null | head -2

# Last commit info (activity indicator)
git log -1 --format="%ai %an - %s" 2>/dev/null

# Commit count and contributors (project maturity)
echo "Total commits: $(git rev-list --count HEAD 2>/dev/null || echo 'N/A')"
echo "Contributors: $(git shortlog -sn 2>/dev/null | wc -l)"

# Repository age
echo "First commit: $(git log --reverse --format="%ai" 2>/dev/null | head -1)"
echo "Latest commit: $(git log -1 --format="%ai" 2>/dev/null)"
```

### Project Metadata Files

```bash
# Package metadata
cat package.json 2>/dev/null | grep -E '"name"|"description"|"version"|"author"|"license"' | head -10
cat pyproject.toml 2>/dev/null | grep -E "^name|^description|^version|^authors|^license" | head -10
cat setup.py 2>/dev/null | grep -E "name=|description=|version=|author=|license=" | head -10
cat pom.xml 2>/dev/null | grep -E "<groupId>|<artifactId>|<version>|<name>|<description>" | head -10
cat go.mod 2>/dev/null | head -5
cat Cargo.toml 2>/dev/null | grep -E "^name|^description|^version|^authors|^license" | head -10
cat *.gemspec 2>/dev/null | grep -E "name|description|version|author|license" | head -10

# License
cat LICENSE* license* License* 2>/dev/null | head -5
```

### Ownership and Maintenance

```bash
# CODEOWNERS file
cat .github/CODEOWNERS CODEOWNERS .gitlab/CODEOWNERS 2>/dev/null

# Maintainers
cat MAINTAINERS* maintainers* AUTHORS* authors* CONTRIBUTORS* 2>/dev/null | head -20

# Contact information
grep -r "contact\|support\|security" README* readme* 2>/dev/null | head -10
```

## Step 2: Technology Stack

### Primary Language Detection

```bash
# File extension analysis
echo "=== FILE TYPE DISTRIBUTION ==="
find . -type f -not -path '*/\.*' -not -path '*/node_modules/*' -not -path '*/vendor/*' -not -path '*/__pycache__/*' -not -path '*/dist/*' -not -path '*/build/*' -not -path '*/target/*' 2>/dev/null | \
  sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20

# Lines of code estimate (if cloc available, otherwise file count)
echo "=== CODE FILES BY LANGUAGE ==="
find . -name "*.py" -not -path "*/node_modules/*" 2>/dev/null | wc -l | xargs echo "Python:"
find . -name "*.js" -not -path "*/node_modules/*" 2>/dev/null | wc -l | xargs echo "JavaScript:"
find . -name "*.ts" -not -path "*/node_modules/*" 2>/dev/null | wc -l | xargs echo "TypeScript:"
find . -name "*.go" -not -path "*/vendor/*" 2>/dev/null | wc -l | xargs echo "Go:"
find . -name "*.java" -not -path "*/target/*" 2>/dev/null | wc -l | xargs echo "Java:"
find . -name "*.rb" -not -path "*/vendor/*" 2>/dev/null | wc -l | xargs echo "Ruby:"
find . -name "*.cs" -not -path "*/bin/*" -not -path "*/obj/*" 2>/dev/null | wc -l | xargs echo "C#:"
find . -name "*.rs" -not -path "*/target/*" 2>/dev/null | wc -l | xargs echo "Rust:"
find . -name "*.php" -not -path "*/vendor/*" 2>/dev/null | wc -l | xargs echo "PHP:"
```

### Framework Detection

```bash
echo "=== FRAMEWORK INDICATORS ==="

# Node.js/JavaScript frameworks
grep -l "express\|fastify\|koa\|hapi\|nest\|next\|nuxt\|react\|vue\|angular\|svelte" package.json 2>/dev/null && echo "Node.js framework detected"

# Python frameworks
grep -l "django\|flask\|fastapi\|tornado\|pyramid\|bottle\|starlette" requirements.txt pyproject.toml setup.py 2>/dev/null && echo "Python framework detected"

# Java frameworks
grep -l "spring\|quarkus\|micronaut\|dropwizard\|jakarta\|javax" pom.xml build.gradle 2>/dev/null && echo "Java framework detected"

# Go frameworks
grep -l "gin\|echo\|fiber\|chi\|gorilla\|beego" go.mod 2>/dev/null && echo "Go framework detected"

# Ruby frameworks
grep -l "rails\|sinatra\|hanami\|grape" Gemfile 2>/dev/null && echo "Ruby framework detected"

# .NET frameworks
grep -l "Microsoft.AspNetCore\|Microsoft.EntityFramework" *.csproj 2>/dev/null && echo ".NET framework detected"
```

### Runtime Environment

```bash
echo "=== RUNTIME INDICATORS ==="

# Node.js version
cat .nvmrc .node-version 2>/dev/null
grep -E '"node":|"engines"' package.json 2>/dev/null

# Python version
cat .python-version 2>/dev/null
grep -E "python_requires|requires-python" pyproject.toml setup.py setup.cfg 2>/dev/null

# Java version
grep -E "sourceCompatibility|targetCompatibility|java.version" build.gradle pom.xml 2>/dev/null

# Go version
grep "^go " go.mod 2>/dev/null

# Ruby version
cat .ruby-version 2>/dev/null
grep "ruby" Gemfile 2>/dev/null | head -1

# .NET version
grep "TargetFramework" *.csproj 2>/dev/null
```

## Step 3: Project Structure

### Directory Organization

```bash
# Top-level structure
echo "=== TOP-LEVEL STRUCTURE ==="
ls -la | grep "^d" | awk '{print $NF}' | grep -v "^\."

# Common architectural directories
echo "=== ARCHITECTURAL COMPONENTS ==="
find . -maxdepth 2 -type d \( \
  -name "src" -o -name "lib" -o -name "app" -o -name "api" -o \
  -name "services" -o -name "controllers" -o -name "models" -o \
  -name "views" -o -name "routes" -o -name "handlers" -o \
  -name "middleware" -o -name "utils" -o -name "helpers" -o \
  -name "config" -o -name "core" -o -name "domain" -o \
  -name "infrastructure" -o -name "adapters" -o -name "ports" -o \
  -name "entities" -o -name "repositories" -o -name "tests" -o \
  -name "test" -o -name "spec" -o -name "docs" -o -name "scripts" \
\) 2>/dev/null | sort
```

### Monorepo Detection

```bash
echo "=== MONOREPO INDICATORS ==="

# Lerna/npm workspaces
cat lerna.json 2>/dev/null && echo "Lerna monorepo"
grep -l "workspaces" package.json 2>/dev/null && echo "npm/yarn workspaces"

# Nx workspace
cat nx.json workspace.json 2>/dev/null | head -10

# Turborepo
cat turbo.json 2>/dev/null && echo "Turborepo"

# Multiple package.json files
echo "package.json count: $(find . -name "package.json" -not -path "*/node_modules/*" 2>/dev/null | wc -l)"

# Multiple go.mod files
echo "go.mod count: $(find . -name "go.mod" 2>/dev/null | wc -l)"

# packages/apps directories
ls -d packages/* apps/* services/* modules/* 2>/dev/null | head -20
```

### Entry Points

```bash
echo "=== ENTRY POINTS ==="

# Main files
find . -maxdepth 3 \( \
  -name "main.*" -o -name "index.*" -o -name "app.*" -o \
  -name "server.*" -o -name "application.*" -o -name "Program.*" \
\) -not -path "*/node_modules/*" -not -path "*/dist/*" 2>/dev/null | head -20

# Package.json scripts entry
grep -E '"main":|"start":' package.json 2>/dev/null

# Python entry points
grep -E "entry_points|console_scripts" setup.py pyproject.toml 2>/dev/null

# Dockerfile ENTRYPOINT/CMD
grep -E "ENTRYPOINT|CMD" Dockerfile* */Dockerfile 2>/dev/null | head -10
```

## Step 4: Build & Deployment

### Build System

```bash
echo "=== BUILD CONFIGURATION ==="

# Node.js
cat package.json 2>/dev/null | grep -E '"build"|"compile"|"bundle"' | head -10

# Python
ls setup.py pyproject.toml setup.cfg MANIFEST.in 2>/dev/null

# Java
ls pom.xml build.gradle build.gradle.kts settings.gradle 2>/dev/null

# Go
ls Makefile go.mod 2>/dev/null

# .NET
ls *.csproj *.sln 2>/dev/null

# Rust
ls Cargo.toml 2>/dev/null

# Generic
ls Makefile makefile CMakeLists.txt BUILD.bazel WORKSPACE 2>/dev/null
```

### Containerization

```bash
echo "=== CONTAINER CONFIGURATION ==="

# Dockerfiles
find . -name "Dockerfile*" -o -name "*.dockerfile" 2>/dev/null | head -10

# Docker Compose
find . -name "docker-compose*.yml" -o -name "docker-compose*.yaml" -o -name "compose*.yml" 2>/dev/null

# Container registries referenced
grep -rh "FROM\|image:" Dockerfile* docker-compose*.yml 2>/dev/null | sort | uniq | head -20

# Kubernetes manifests
find . -type f \( -name "*.yaml" -o -name "*.yml" \) -exec grep -l "apiVersion:\|kind:" {} \; 2>/dev/null | head -10

# Helm charts
find . -name "Chart.yaml" 2>/dev/null
```

### Deployment Targets

```bash
echo "=== DEPLOYMENT INDICATORS ==="

# Cloud provider configs
ls serverless.yml serverless.yaml 2>/dev/null && echo "Serverless Framework"
find . -name "*.tf" 2>/dev/null | head -1 && echo "Terraform IaC"
find . -name "*.bicep" -o -name "azuredeploy.json" 2>/dev/null | head -1 && echo "Azure deployment"
find . -name "cloudformation*.yml" -o -name "template.yaml" 2>/dev/null | head -1 && echo "AWS CloudFormation"
ls app.yaml 2>/dev/null && echo "Google App Engine"
ls Procfile 2>/dev/null && echo "Heroku"
ls vercel.json netlify.toml 2>/dev/null && echo "JAMstack platform"
ls fly.toml render.yaml railway.json 2>/dev/null && echo "PaaS platform"

# Cloud SDK configs
ls .aws .gcloud .azure 2>/dev/null
```

## Step 5: Documentation Review

### README Analysis

```bash
echo "=== README CONTENT ==="

# Find README
README_FILE=$(find . -maxdepth 1 -iname "readme*" | head -1)

if [ -n "$README_FILE" ]; then
    # Extract sections
    echo "Sections found:"
    grep -E "^#{1,3}\s" "$README_FILE" 2>/dev/null | head -20
    
    # Project description (first paragraph)
    echo ""
    echo "Description:"
    sed -n '/^[^#]/p' "$README_FILE" | head -10
fi
```

### API Documentation

```bash
echo "=== API DOCUMENTATION ==="

# OpenAPI/Swagger
find . -name "openapi*.json" -o -name "openapi*.yaml" -o -name "swagger*.json" -o -name "swagger*.yaml" 2>/dev/null

# API docs directories
find . -type d -name "api-docs" -o -name "apidoc" -o -name "swagger" 2>/dev/null

# GraphQL schema
find . -name "*.graphql" -o -name "schema.gql" 2>/dev/null | head -5

# gRPC proto files
find . -name "*.proto" 2>/dev/null | head -10
```

### Architecture Documentation

```bash
echo "=== ARCHITECTURE DOCS ==="

# ADRs (Architecture Decision Records)
find . -type d -name "adr" -o -name "decisions" -o -name "architecture" 2>/dev/null
find . -name "*.md" -path "*/adr/*" -o -name "*.md" -path "*/decisions/*" 2>/dev/null | head -10

# Design documents
find . -name "ARCHITECTURE*" -o -name "DESIGN*" -o -name "CONTRIBUTING*" 2>/dev/null

# Diagrams
find . \( -name "*.drawio" -o -name "*.puml" -o -name "*.plantuml" -o -name "*.mermaid" \) 2>/dev/null | head -10
```

## Step 6: Dependency Overview

### Direct Dependencies Summary

```bash
echo "=== DEPENDENCY SUMMARY ==="

# Node.js
if [ -f "package.json" ]; then
    echo "NPM Dependencies:"
    echo "  Production: $(cat package.json | grep -c '"' | head -1 || echo 'N/A')"
    jq -r '.dependencies | keys[]' package.json 2>/dev/null | wc -l | xargs echo "  Production:"
    jq -r '.devDependencies | keys[]' package.json 2>/dev/null | wc -l | xargs echo "  Dev:"
fi

# Python
if [ -f "requirements.txt" ]; then
    echo "Python Dependencies: $(grep -c "^[^#]" requirements.txt)"
fi
if [ -f "pyproject.toml" ]; then
    echo "Python (pyproject.toml) dependencies detected"
fi

# Java
if [ -f "pom.xml" ]; then
    echo "Maven Dependencies: $(grep -c "<dependency>" pom.xml)"
fi
if [ -f "build.gradle" ]; then
    echo "Gradle dependencies detected"
fi

# Go
if [ -f "go.mod" ]; then
    echo "Go Dependencies: $(grep -c "^\t" go.mod || echo 'N/A')"
fi

# Ruby
if [ -f "Gemfile" ]; then
    echo "Ruby Gems: $(grep -c "^gem " Gemfile)"
fi
```

### Security-Relevant Dependencies

```bash
echo "=== SECURITY-RELATED DEPENDENCIES ==="

# Authentication/Authorization
grep -rh "passport\|jwt\|jsonwebtoken\|oauth\|oidc\|auth0\|keycloak\|cognito\|firebase-admin\|bcrypt\|argon2\|session" package.json requirements.txt Gemfile go.mod pom.xml 2>/dev/null | head -20

# Encryption/Crypto
grep -rh "crypto\|sodium\|nacl\|openssl\|tls\|ssl\|gpg" package.json requirements.txt Gemfile go.mod pom.xml 2>/dev/null | head -10

# Validation
grep -rh "validator\|joi\|yup\|zod\|ajv\|class-validator\|pydantic" package.json requirements.txt Gemfile go.mod pom.xml 2>/dev/null | head -10

# Security headers/middleware
grep -rh "helmet\|cors\|csp\|rate-limit\|express-rate\|slowapi" package.json requirements.txt Gemfile go.mod pom.xml 2>/dev/null | head -10
```

### Dependency Lock Files

```bash
echo "=== LOCK FILES (Supply Chain) ==="

# Check for lock files (good practice)
ls package-lock.json yarn.lock pnpm-lock.yaml 2>/dev/null
ls Pipfile.lock poetry.lock 2>/dev/null
ls Gemfile.lock 2>/dev/null
ls go.sum 2>/dev/null
ls Cargo.lock 2>/dev/null

# Check for pinned versions
echo ""
echo "Version pinning check:"
grep -c "==" requirements.txt 2>/dev/null | xargs echo "  Pinned Python deps:"
grep -c '"^' package.json 2>/dev/null | xargs echo "  Exact npm versions:"
```

## Step 7: DevOps & CI/CD

### CI/CD Configuration

```bash
echo "=== CI/CD PIPELINES ==="

# GitHub Actions
find .github/workflows -name "*.yml" -o -name "*.yaml" 2>/dev/null

# GitLab CI
ls .gitlab-ci.yml 2>/dev/null

# Jenkins
ls Jenkinsfile jenkins/* 2>/dev/null

# CircleCI
ls .circleci/config.yml 2>/dev/null

# Travis CI
ls .travis.yml 2>/dev/null

# Azure DevOps
ls azure-pipelines.yml .azure-pipelines/* 2>/dev/null

# Bitbucket
ls bitbucket-pipelines.yml 2>/dev/null

# AWS CodeBuild
ls buildspec.yml 2>/dev/null

# Generic
ls .drone.yml .woodpecker.yml .buildkite/* 2>/dev/null
```

### Pipeline Analysis

```bash
echo "=== PIPELINE STAGES ==="

# Extract job/stage names from common CI files
grep -E "^\s+\w+:|jobs:|stages:|steps:" .github/workflows/*.yml .gitlab-ci.yml azure-pipelines.yml 2>/dev/null | head -30

# Security scanning in CI
grep -rih "snyk\|trivy\|sonar\|codeql\|semgrep\|bandit\|brakeman\|safety\|npm audit\|dependabot\|renovate" .github/workflows/* .gitlab-ci.yml Jenkinsfile 2>/dev/null | head -20
```

### Environment Configuration

```bash
echo "=== ENVIRONMENT CONFIGURATION ==="

# Environment files
find . -maxdepth 2 \( -name ".env*" -o -name "*.env" \) -not -name ".env.example" 2>/dev/null

# Environment examples (safe to analyze)
cat .env.example .env.sample .env.template env.example 2>/dev/null | head -30

# Config files
find . -maxdepth 2 -name "config.*" -o -name "settings.*" -o -name "*.config.*" 2>/dev/null | head -20
```

## Step 8: Security Indicators

### Security Configuration Files

```bash
echo "=== SECURITY CONFIGURATION ==="

# Security policies
ls SECURITY.md .github/SECURITY.md security.txt .well-known/security.txt 2>/dev/null

# Dependabot/Renovate
ls .github/dependabot.yml renovate.json .renovaterc* 2>/dev/null

# Code scanning config
ls .github/codeql codeql-config.yml .semgrep.yml .snyk sonar-project.properties 2>/dev/null

# Git security
ls .gitignore .dockerignore .npmignore 2>/dev/null

# Secrets patterns
cat .gitignore 2>/dev/null | grep -i "secret\|key\|credential\|password\|token\|env" | head -10
```

### Authentication/Authorization Config

```bash
echo "=== AUTH CONFIGURATION ==="

# Auth config files
find . -maxdepth 3 \( -name "*auth*" -o -name "*security*" -o -name "*permission*" \) \
  \( -name "*.json" -o -name "*.yml" -o -name "*.yaml" -o -name "*.config.*" \) \
  -not -path "*/node_modules/*" 2>/dev/null | head -20

# OAuth/OIDC config
grep -rln "client_id\|client_secret\|oauth\|oidc\|redirect_uri\|issuer" --include="*.json" --include="*.yml" --include="*.yaml" 2>/dev/null | grep -v node_modules | head -10
```

### Existing Security Measures

```bash
echo "=== SECURITY MEASURES DETECTED ==="

# HTTPS/TLS
grep -rn "https\|tls\|ssl\|certificate" --include="*.yml" --include="*.yaml" --include="*.json" --include="*.ts" --include="*.js" --include="*.py" 2>/dev/null | grep -v node_modules | wc -l | xargs echo "TLS/HTTPS references:"

# CORS
grep -rn "cors\|Access-Control" --include="*.ts" --include="*.js" --include="*.py" --include="*.java" --include="*.go" 2>/dev/null | grep -v node_modules | wc -l | xargs echo "CORS references:"

# CSP
grep -rn "Content-Security-Policy\|helmet\|csp" --include="*.ts" --include="*.js" --include="*.py" 2>/dev/null | grep -v node_modules | wc -l | xargs echo "CSP references:"

# Rate limiting
grep -rn "rate.limit\|ratelimit\|throttle" --include="*.ts" --include="*.js" --include="*.py" --include="*.java" --include="*.go" 2>/dev/null | grep -v node_modules | wc -l | xargs echo "Rate limiting references:"

# Input validation
grep -rn "validate\|sanitize\|escape" --include="*.ts" --include="*.js" --include="*.py" --include="*.java" --include="*.go" 2>/dev/null | grep -v node_modules | wc -l | xargs echo "Validation references:"
```

### Test Coverage

```bash
echo "=== TEST COVERAGE ==="

# Test directories
find . -type d \( -name "test" -o -name "tests" -o -name "spec" -o -name "__tests__" \) -not -path "*/node_modules/*" 2>/dev/null | head -10

# Test file count
find . \( -name "*test*" -o -name "*spec*" \) \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.java" -o -name "*.go" \) -not -path "*/node_modules/*" 2>/dev/null | wc -l | xargs echo "Test files:"

# Security-specific tests
find . \( -name "*security*" -o -name "*auth*" \) \( -name "*test*" -o -name "*spec*" \) -not -path "*/node_modules/*" 2>/dev/null | head -10
```

## Step 9: Output Generation

### Executive Summary Template

```markdown
# Project Overview: [Repository Name]

## Executive Summary
| Attribute | Value |
|-----------|-------|
| Project Name | [Name] |
| Primary Purpose | [Brief description] |
| Primary Language | [Language] |
| Framework | [Framework] |
| License | [License type] |
| Last Active | [Date] |
| Contributors | [Count] |

## Technology Stack
| Layer | Technology |
|-------|------------|
| Language | [Primary language(s)] |
| Framework | [Web/app framework] |
| Database | [If detected] |
| Cache | [If detected] |
| Message Queue | [If detected] |
| Container | [Docker/K8s] |
| Cloud | [AWS/GCP/Azure/etc] |

## Project Classification
| Aspect | Assessment |
|--------|------------|
| Type | [Web App | API | Library | CLI | Mobile | etc] |
| Architecture | [Monolith | Microservices | Serverless | etc] |
| Deployment | [Cloud | On-prem | Hybrid | SaaS] |
| Maturity | [POC | Development | Production] |
| Sensitivity | [Public | Internal | Confidential] |

## Security Posture Overview
| Control | Status |
|---------|--------|
| Authentication | [Detected | Not detected] |
| Authorization | [Detected | Not detected] |
| Input Validation | [Detected | Not detected] |
| Encryption | [Detected | Not detected] |
| Logging | [Detected | Not detected] |
| CI/CD Security | [Detected | Not detected] |
| Dependency Scanning | [Detected | Not detected] |
| Security Tests | [Detected | Not detected] |

## Components Identified
| Component | Location | Purpose |
|-----------|----------|---------|
| [Component 1] | [Path] | [Purpose] |
| [Component 2] | [Path] | [Purpose] |

## External Interfaces
| Interface | Type | Direction |
|-----------|------|-----------|
| [Interface 1] | [REST/GraphQL/gRPC] | [Inbound/Outbound] |
| [Database] | [Type] | [Internal] |

## Key Files for Deep Analysis
| Category | Files |
|----------|-------|
| Entry Points | [List main files] |
| Config | [List config files] |
| Security | [List security-related] |
| API Specs | [List API docs] |

## Threat Modeling Scope Recommendations
- **In Scope**: [Components/features to analyze]
- **Out of Scope**: [Third-party, infrastructure, etc]
- **Priority Areas**: [Based on findings]

## Next Steps
1. [ ] Architectural analysis (repo-architecture-analysis)
2. [ ] Database analysis (database-security-analysis)
3. [ ] IaC analysis (iac-security-analysis)
4. [ ] Abstraction mapping (abstraction-security-analysis)
```

### Quick Assessment Indicators

```markdown
## Risk Indicators Summary

### Positive Indicators ✓
- [ ] Lock files present (supply chain)
- [ ] Security policy exists
- [ ] Dependency scanning configured
- [ ] Tests present
- [ ] Documentation exists
- [ ] CI/CD pipeline exists
- [ ] Environment examples provided
- [ ] Gitignore includes secrets patterns

### Warning Indicators ⚠
- [ ] No lock files
- [ ] No security policy
- [ ] No dependency scanning
- [ ] Limited tests
- [ ] Sparse documentation
- [ ] No CI/CD
- [ ] Hardcoded configuration
- [ ] Large dependency count

### Red Flags 🚩
- [ ] Credentials in repository
- [ ] No .gitignore
- [ ] Very old dependencies
- [ ] No recent activity
- [ ] Single contributor (bus factor)
- [ ] No input validation patterns
- [ ] No authentication patterns
```

## Quick Reference Command

### One-liner Project Overview

```bash
# Comprehensive quick overview
echo "=== PROJECT: $(basename $(pwd)) ===" && \
echo "=== LANGUAGES ===" && find . -type f -not -path '*/\.*' -not -path '*/node_modules/*' -not -path '*/vendor/*' | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -5 && \
echo "=== STRUCTURE ===" && ls -d */ 2>/dev/null | head -10 && \
echo "=== BUILD ===" && ls Dockerfile* docker-compose* package.json requirements.txt go.mod pom.xml Makefile 2>/dev/null && \
echo "=== CI/CD ===" && ls .github/workflows/*.yml .gitlab-ci.yml Jenkinsfile 2>/dev/null && \
echo "=== SECURITY ===" && ls SECURITY.md .github/dependabot.yml .snyk 2>/dev/null && \
echo "=== TESTS ===" && find . -type d \( -name "test" -o -name "tests" \) -not -path "*/node_modules/*" 2>/dev/null | wc -l | xargs echo "Test directories:" && \
echo "=== COMMITS ===" && git log --oneline 2>/dev/null | wc -l | xargs echo "Total:"
```

## Additional References

For deeper analysis after overview, use these complementary skills:

- **[repo-architecture-analysis]**: Application code patterns and entry points
- **[database-security-analysis]**: Database and data layer analysis
- **[iac-security-analysis]**: Infrastructure-as-Code analysis
- **[abstraction-security-analysis]**: Software abstractions and relationships