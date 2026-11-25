---
name: dockhand
description: Dockhand documentation and resources. Use this skill when working with Dockhand or when the user mentions dockhand.
metadata:
  source: llms.txt
  source_url: https://mintlify.wiki/Finsys/dockhand/llms.txt
  generated: 2026-05-21T06:48:29.049Z
---

# Dockhand

## Available Resources

### Docs

- **Authentication**: Secure your Dockhand API access with session-based authentication and enterprise SSO
  - URL: https://mintlify.wiki/Finsys/dockhand/api/authentication.md

- **Configure Auto-Update**
  - URL: https://mintlify.wiki/Finsys/dockhand/api/auto-update/configure.md

- **Container Exec**: Execute commands and create interactive terminal sessions in containers
  - URL: https://mintlify.wiki/Finsys/dockhand/api/containers/exec.md

- **Inspect Container**: Get detailed information about a specific container
  - URL: https://mintlify.wiki/Finsys/dockhand/api/containers/inspect.md

- **Container Lifecycle**: Control container lifecycle operations - start, stop, restart, pause, and unpause
  - URL: https://mintlify.wiki/Finsys/dockhand/api/containers/lifecycle.md

- **List Containers**: Retrieve a list of Docker containers from a specific environment
  - URL: https://mintlify.wiki/Finsys/dockhand/api/containers/list.md

- **Container Logs**: Retrieve and stream container logs
  - URL: https://mintlify.wiki/Finsys/dockhand/api/containers/logs.md

- **Container Statistics**: Get real-time resource usage statistics for containers
  - URL: https://mintlify.wiki/Finsys/dockhand/api/containers/stats.md

- **Create Environment**: Create a new Docker environment in Dockhand
  - URL: https://mintlify.wiki/Finsys/dockhand/api/environments/create.md

- **List Environments**: Retrieve all Docker environments configured in Dockhand
  - URL: https://mintlify.wiki/Finsys/dockhand/api/environments/list.md

- **Update Environment**: Update an existing Docker environment configuration
  - URL: https://mintlify.wiki/Finsys/dockhand/api/environments/update.md

- **List Images**: Retrieve all Docker images in an environment
  - URL: https://mintlify.wiki/Finsys/dockhand/api/images/list.md

- **Prune Images**: Remove unused Docker images to free disk space
  - URL: https://mintlify.wiki/Finsys/dockhand/api/images/prune.md

- **Pull Image**: Download Docker images from registries with optional vulnerability scanning
  - URL: https://mintlify.wiki/Finsys/dockhand/api/images/pull.md

- **Push Image**: Upload Docker images to container registries with authentication
  - URL: https://mintlify.wiki/Finsys/dockhand/api/images/push.md

- **Scan Image**: Run vulnerability scans on Docker images using Grype or Trivy
  - URL: https://mintlify.wiki/Finsys/dockhand/api/images/scan.md

- **Create Network**: Create a new Docker network in a specific environment
  - URL: https://mintlify.wiki/Finsys/dockhand/api/networks/create.md

- **List Networks**: Retrieve all Docker networks for a specific environment
  - URL: https://mintlify.wiki/Finsys/dockhand/api/networks/list.md

- **API Overview**: Complete reference for the Dockhand REST API
  - URL: https://mintlify.wiki/Finsys/dockhand/api/overview.md

- **Create Schedule**
  - URL: https://mintlify.wiki/Finsys/dockhand/api/schedules/create.md

- **List Schedules**
  - URL: https://mintlify.wiki/Finsys/dockhand/api/schedules/list.md

- **Delete Stack**: Remove a compose stack and its resources
  - URL: https://mintlify.wiki/Finsys/dockhand/api/stacks/delete.md

- **Deploy Stack**: Create and deploy a new compose stack
  - URL: https://mintlify.wiki/Finsys/dockhand/api/stacks/deploy.md

- **Git Stack Sync**: Sync and deploy a Git-managed compose stack
  - URL: https://mintlify.wiki/Finsys/dockhand/api/stacks/git-sync.md

- **List Stacks**: Retrieve all compose stacks for an environment
  - URL: https://mintlify.wiki/Finsys/dockhand/api/stacks/list.md

- **Update Stack**: Update a stack compose file and optionally restart
  - URL: https://mintlify.wiki/Finsys/dockhand/api/stacks/update.md

- **Create Volume**: Create a new Docker volume in a specific environment
  - URL: https://mintlify.wiki/Finsys/dockhand/api/volumes/create.md

- **List Volumes**: Retrieve all Docker volumes for a specific environment
  - URL: https://mintlify.wiki/Finsys/dockhand/api/volumes/list.md

- **Architecture**: Technical architecture of Dockhand including SvelteKit frontend, Bun runtime, Drizzle ORM, Docker API integration, and Wolfi-based OS
  - URL: https://mintlify.wiki/Finsys/dockhand/architecture.md

- **Two-Factor Authentication**: Add TOTP-based 2FA with backup codes for enhanced security
  - URL: https://mintlify.wiki/Finsys/dockhand/auth/2fa.md

- **LDAP/Active Directory**: Authenticate users against LDAP directories (Enterprise)
  - URL: https://mintlify.wiki/Finsys/dockhand/auth/ldap.md

- **Local Users**: Manage local user accounts with password authentication
  - URL: https://mintlify.wiki/Finsys/dockhand/auth/local-users.md

- **OIDC/SSO Integration**: Single Sign-On with any OpenID Connect provider
  - URL: https://mintlify.wiki/Finsys/dockhand/auth/oidc.md

- **Authentication Overview**: Secure your Dockhand instance with flexible authentication options
  - URL: https://mintlify.wiki/Finsys/dockhand/auth/overview.md

- **Role-Based Access Control**: Fine-grained permissions with environment-scoped roles (Enterprise)
  - URL: https://mintlify.wiki/Finsys/dockhand/auth/rbac.md

- **Changelog**: Release history and version updates for Dockhand
  - URL: https://mintlify.wiki/Finsys/dockhand/changelog.md

- **Configuration**: Environment variables and advanced configuration options
  - URL: https://mintlify.wiki/Finsys/dockhand/configuration.md

- **Contributing**: Guide for contributing to Dockhand development
  - URL: https://mintlify.wiki/Finsys/dockhand/contributing.md

- **Database Configuration**: Configure SQLite or PostgreSQL for Dockhand
  - URL: https://mintlify.wiki/Finsys/dockhand/deployment/database.md

- **Docker Deployment**: Run Dockhand with Docker
  - URL: https://mintlify.wiki/Finsys/dockhand/deployment/docker.md

- **Docker Compose Deployment**: Deploy Dockhand with Docker Compose
  - URL: https://mintlify.wiki/Finsys/dockhand/deployment/docker-compose.md

- **Environment Variables**: Configuration options for Dockhand
  - URL: https://mintlify.wiki/Finsys/dockhand/deployment/environment-variables.md

- **TLS Configuration**: Configure TLS/HTTPS for Docker connections
  - URL: https://mintlify.wiki/Finsys/dockhand/deployment/tls.md

- **FAQ**: Frequently asked questions about Dockhand
  - URL: https://mintlify.wiki/Finsys/dockhand/faq.md

- **Features**: Comprehensive guide to all Dockhand features including containers, stacks, images, volumes, networks, and more
  - URL: https://mintlify.wiki/Finsys/dockhand/features.md

- **Containers**: Manage Docker containers with real-time monitoring, control, and advanced features
  - URL: https://mintlify.wiki/Finsys/dockhand/features/containers.md

- **Environments**: Connect to Docker hosts via socket, TCP, or Hawser for multi-environment management
  - URL: https://mintlify.wiki/Finsys/dockhand/features/environments.md

- **File Browser**: Browse, edit, and manage files inside containers and Docker volumes with a web-based file manager
  - URL: https://mintlify.wiki/Finsys/dockhand/features/file-browser.md

- **Git Integration**: Automate stack deployments with Git repository synchronization, webhooks, and continuous deployment
  - URL: https://mintlify.wiki/Finsys/dockhand/features/git-integration.md

- **Images**: Manage Docker images with pulling, building, tagging, scanning, and registry operations
  - URL: https://mintlify.wiki/Finsys/dockhand/features/images.md

- **Monitoring & Metrics**: Real-time container statistics, performance metrics, and resource utilization tracking
  - URL: https://mintlify.wiki/Finsys/dockhand/features/monitoring.md

- **Networks**: Create and manage Docker networks with bridge, host, overlay, and custom drivers
  - URL: https://mintlify.wiki/Finsys/dockhand/features/networks.md

- **Notifications**: Configure alerts and notifications for container events, updates, and system activities
  - URL: https://mintlify.wiki/Finsys/dockhand/features/notifications.md

- **Scheduling & Automation**: Automate container updates, cleanups, and maintenance tasks with cron-based scheduling
  - URL: https://mintlify.wiki/Finsys/dockhand/features/scheduling.md

- **Stacks**: Deploy and manage Docker Compose applications with Git integration and real-time monitoring
  - URL: https://mintlify.wiki/Finsys/dockhand/features/stacks.md

- **Container Terminal**: Execute commands and access interactive shell sessions directly in your browser with xterm.js integration
  - URL: https://mintlify.wiki/Finsys/dockhand/features/terminal.md

- **Volumes**: Manage Docker volumes for persistent data storage with browsing, backup, and cloning
  - URL: https://mintlify.wiki/Finsys/dockhand/features/volumes.md

- **Installation**: Install Dockhand using Docker Run or Docker Compose
  - URL: https://mintlify.wiki/Finsys/dockhand/installation.md

- **Hawser Agent**: Secure edge agent for connecting Docker hosts behind NAT and firewalls
  - URL: https://mintlify.wiki/Finsys/dockhand/integrations/hawser.md

- **Container Registries**: Connect to Docker Hub, GHCR, and private container registries
  - URL: https://mintlify.wiki/Finsys/dockhand/integrations/registries.md

- **Remote Hosts**: Connect to Docker hosts anywhere with TLS, mTLS, and SSH tunnels
  - URL: https://mintlify.wiki/Finsys/dockhand/integrations/remote-hosts.md

- **Git Webhooks**: Automate deployments with GitHub, GitLab, and Gitea webhooks
  - URL: https://mintlify.wiki/Finsys/dockhand/integrations/webhooks.md

- **Introduction to Dockhand**: Modern Docker management application with real-time container orchestration, Compose stacks, and multi-environment support
  - URL: https://mintlify.wiki/Finsys/dockhand/introduction.md

- **License**: Dockhand licensing information and terms
  - URL: https://mintlify.wiki/Finsys/dockhand/license.md

- **Quick Start**: Get started with Dockhand in minutes
  - URL: https://mintlify.wiki/Finsys/dockhand/quickstart.md

- **Troubleshooting**: Common issues and solutions for Dockhand
  - URL: https://mintlify.wiki/Finsys/dockhand/troubleshooting.md

## How to Use This Skill

Reference these resources when working with Dockhand.