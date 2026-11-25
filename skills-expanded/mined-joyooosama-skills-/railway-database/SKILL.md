---
name: railway-database
description: Add official Railway database services (Postgres, Redis, MySQL, MongoDB). Use when user wants to add a database, says "add postgres", "add redis", "add database", "connect to database", or "wire up the database". For other templates (Ghost, Strapi, n8n), use the railway-templates skill.
version: 1.0.0
author: Railway
license: MIT
tags: [Railway, Database, Postgres, Redis, MySQL, MongoDB, Infrastructure, Deployment, Template]
dependencies: [railway-cli]
allowed-tools: Bash(railway:*)
---

# railway database

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- User asks to "add a database", "add Postgres", "add Redis", etc.
- User needs a database for their application
- User asks about connecting to a database
- User says "add postgres and connect to my server"
- User says "wire up the database"
- `ghcr.io/railway/postgres*` or `postgres:*` 鈫?Postgres
- `ghcr.io/railway/redis*` or `redis:*` 鈫?Redis
- `ghcr.io/railway/mysql*` or `mysql:*` 鈫?MySQL

## Available sections

- Railway Database
- When to Use
- Decision Flow
- Check for Existing Databases
- Available Databases
- Prerequisites
- Adding a Database
- Step 1: Fetch Template
- Step 2: Deploy Template
- Connecting to the Database
- Backend Services (Server-side)
- Frontend Applications

