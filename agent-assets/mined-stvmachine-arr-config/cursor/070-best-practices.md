---
description: Best practices for the project
alwaysApply: true
---
# Best Practices

- Never commit secrets (.env files, *.ini files with keys)
- Always verify .gitignore before committing
- Document new services in README.md with ports and descriptions
- Use environment variables for user IDs and paths
- Keep docker-compose.yml services organized by category
- When adding a new service, update README.md with port and description
- When modifying docker-compose.yml, verify environment variables are set
- When updating Python scripts, ensure they follow the project structure
