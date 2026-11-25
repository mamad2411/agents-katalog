# Skill Health Monitor

Scans the skills directory for structural compliance and environmental dependencies.
Use when you suspect skills are broken, missing metadata, or want to audit the workspace.

## Usage
```bash
node skills/skill-health-monitor/index.js
```

## Features
- Checks for `SKILL.md` (documentation)
- Checks for `package.json` or `index.js` (entry point)
- **Dependency Check:** Validates presence of declared environment variables in `SKILL.md`.
- Reports total count, healthy, and broken skills.
- Generates `health_report.json` and `dependency_report.json` for programmatic consumption.
