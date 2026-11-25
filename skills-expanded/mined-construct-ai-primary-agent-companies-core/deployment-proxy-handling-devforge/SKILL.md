---
name: deployment-proxy-handling-devforge
description: >
  Use when deployment issues occur with reverse proxies (Traefik, Nginx, AWS ALB),
  keepAliveTimeout mismatches cause Failed to fetch errors, or server configuration
  needs adjustment for containerized/HA environments. Handles Node.js server timeout config.
---

# Deployment Proxy Handling - DevForge AI

## Overview
Handles deployment and reverse proxy configuration issues in the Paperclip codebase. Resolves Node.js keepAliveTimeout mismatches with reverse proxies, configures server timeouts for containerized/HA environments, and ensures reliable connectivity through proxy layers.

## When to Use
- When UI throws random `Failed to fetch` errors after 5 seconds of idle time
- When deploying behind Traefik, Nginx, AWS ALB, or similar reverse proxies
- When Node.js `server.keepAliveTimeout` (default 5s) is shorter than proxy timeout
- When ECONNRESET or 502 errors occur on reused connections
- When configuring server for Easypanel, Docker, or Kubernetes deployment
- **Don't use when:** It's a general server startup issue (use devcore-devforge-core-development)

## Core Procedures
### Proxy Timeout Fix Workflow
1. **Identify Timeout Mismatch** - Check proxy keepAliveTimeout vs Node.js keepAliveTimeout
2. **Configure Server Timeouts** - Set `server.keepAliveTimeout` and `server.headersTimeout` in server/src/index.ts
3. **Test Under Load** - Verify no Failed to fetch errors after idle periods
4. **Document Configuration** - Add deployment guide for common proxy configurations

### Common Timeout Values
- Node.js default: 5 seconds (5000ms)
- Traefik default: 180 seconds
- AWS ALB default: 60 seconds
- Recommended: 185 seconds (outlives all common proxy defaults)

## Agent Assignment
**Primary Agent:** cloudops-devforge-cloud-operations
**Company:** DevForge AI
**Role:** Deployment Proxy Specialist
**Reports To:** cloudops-devforge-cloud-operations
**Backup Agents:** forge-devforge-system-architecture, devcore-devforge-core-development

## Success Metrics
- No Failed to fetch errors under normal proxy usage
- Server timeouts exceed all common proxy defaults
- Deployment documentation covers proxy configuration

## Error Handling
- **Error:** Timeout too long causes resource exhaustion
  **Response:** Monitor connection count, adjust timeout based on load
- **Error:** Proxy ignores server timeout hints
  **Response:** Configure proxy directly, add connection-level health checks

## Cross-Team Integration
**Gigabrain Tags:** devforge, deployment, proxy, traefik, keepalive, timeout, ha
**Related Skills:** cloudops-devforge-cloud-operations, forge-devforge-system-architecture, devcore-devforge-core-development
**Last Updated:** 2026-04-07