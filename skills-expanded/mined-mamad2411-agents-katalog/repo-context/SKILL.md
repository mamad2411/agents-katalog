---
name: repo-context
description: >-
  Describes the demo-service repository context, including its technology stack,
  critical files, test and lint commands, and known failure modes.
---

# Repository Context: demo-service

This skill describes the tech stack, files, and commands for the microservice under triage.

## Stack Information
- **Runtime**: Node.js
- **Framework**: Express.js
- **Database**: Postgres (connected via a pool from `pg`)
- **Pool Settings**: Max pool size of 5 connections

## Commands
- **Test Command**: `npm test`
- **Lint Command**: `npm run lint`

## Architecture & Code Map
- **Critical File**: `demo-service/src/orders.js`

## Known Failure Modes
- **Connection Leak**: Connections not released back to the pool in error handling paths (specifically in validation blocks).
