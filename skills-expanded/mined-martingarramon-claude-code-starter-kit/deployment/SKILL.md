# Deployment — CI/CD Pipeline Design

## When to Use
- Setting up automated builds, tests, or deployments
- Scaling from prototype to production
- Adding deployment automation to an existing project
- Troubleshooting failed pipelines

## Core Principle
Automate every step from commit to production. Use Claude to generate pipeline configs and deployment scripts, but always test locally before committing.

## Process
1. **Assess needs** — Identify stages (build, test, lint, deploy) and tools (GitHub Actions, etc.). Have Claude outline a pipeline for your stack.
2. **Define triggers** — Set up triggers (push, PR, tag). Use Claude to script each stage.
3. **Integrate testing** — Embed test suite in CI. Have Claude generate the workflow YAML.
4. **Add deployment** — Configure environments (dev/staging/prod) with secrets management. Use Claude for deploy scripts.
5. **Add rollback** — Every deploy must have a rollback mechanism. Claude generates rollback scripts.
6. **Monitor and iterate** — Set up notifications. Review with Claude after failures to optimize.

## Output Format
- Pipeline overview (stages and triggers)
- Configuration files (ready to commit)
- Risk assessment (failure points and mitigations)
- First run results

## Rules
- Pipelines are declarative and version-controlled.
- Test locally before committing pipeline configs.
- Include rollback in every deploy stage.
- Keep pipeline runtime under 10 minutes.
- Never hardcode secrets — use environment variables or secret managers.

## Anti-Patterns
- Monolithic pipelines (everything sequential = slow)
- Skipping environment-specific configs (works in dev, breaks in prod)
- Over-automating without human gates for production deploys
- Ignoring pipeline costs in cloud CI
- No rollback strategy
