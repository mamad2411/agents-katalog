# CI Doctor Skill

Diagnoses and fixes common CI/CD pipeline issues automatically.

## Trigger Phrases

- "CI failing"
- "workflow broken"
- "pipeline error"
- "GitHub Actions not working"
- "build failed"
- "CI not passing"
- "fix CI"
- "debug pipeline"

## What This Skill Does

1. **Version Consistency Checks**
   - Compares Node.js versions across .nvmrc, package.json, Dockerfile, and CI workflows
   - Flags any mismatches that could cause build failures

2. **CI Anti-Pattern Detection**
   - Command failures masked with `|| true`
   - npm ci without caching configured
   - Errors suppressed without documentation
   - Duplicate build steps that waste resources

3. **Workflow Validation**
   - Checks for common GitHub Actions configuration issues
   - Validates job dependencies and artifact sharing

## Usage

### Automatic Invocation
Simply mention any trigger phrase in your request, and the skill will analyze your CI configuration.

### Manual Invocation
```bash
# Run all CI health checks
npx tsx scripts/index.ts

# Output as JSON
npx tsx scripts/index.ts --json

# Check specific directory
npx tsx scripts/index.ts /path/to/project
```

## Requirements

- Node.js 18+
- TypeScript (tsx for execution)
- Project must have .github/workflows/ directory
