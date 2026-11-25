---
name: openclawforge-ai-config-manager
description: >
  Use when managing environment variables, configuration files, .env files, or secrets
  for the OpenClaw platform applications running on the Hostinger VPS.
---

# Config Manager - OpenClaw AI Configuration Management

## Overview
Manages environment variables, application configuration files, .env files, deployment configs, and secrets for the OpenClaw platform. All configuration is deployed to and managed on the Hostinger VPS at `srv1628373.hstgr.cloud` (SSH port 65002).

## When to Use
- When managing or updating environment variables for applications on the VPS
- When creating, updating, or backing up `.env` files on `srv1628373.hstgr.cloud`
- When handling API keys, database credentials, or other secrets
- When maintaining deployment configuration files (Docker, PM2, systemd, nginx)
- When reviewing or auditing configuration settings for the OpenClaw platform

## VPS Context
- **Hostname**: `srv1628373.hstgr.cloud`
- **SSH Port**: 65002
- See `infrastructure/vps-infrastructure.md` for detailed knowledge