---
description: Docker Compose configuration guidelines
globs: **/docker-compose.yml, **/docker-compose.*.yml
---
# Docker Compose Guidelines

- Use version-agnostic docker-compose.yml format
- Keep service definitions organized and commented
- Use environment variables for configuration
- Document port mappings and volume mounts
- Use `restart: unless-stopped` for services
- Group related services together (VPN, torrent, *arr services, etc.)
