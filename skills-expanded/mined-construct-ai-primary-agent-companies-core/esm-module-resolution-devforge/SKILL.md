---
name: esm-module-resolution-devforge
description: >
  Use when ESM/CommonJS module resolution errors occur, dependency conflicts with
  top-level await, or Node.js module loading issues prevent server startup. Handles
  cssstyle, html-encoding-sniffer, @asamuzakjp/css-color and similar ESM compatibility issues.
---

# ESM Module Resolution - DevForge AI

## Overview
Handles ESM/CommonJS module resolution issues in the Paperclip codebase. Resolves dependency conflicts where ESM modules with top-level await are incorrectly required by CommonJS code, a recurring issue with cssstyle, html-encoding-sniffer, and similar packages.

## When to Use
- When `require() cannot be used on an ESM graph with top-level await` error occurs
- When server fails to start due to module resolution errors
- When transitive dependencies resolve to incompatible ESM versions
- When Windows/macOS specific module loading issues occur
- **Don't use when:** It's a runtime logic bug (use fixer-devforge-bug-fixing)

## Core Procedures
### Module Resolution Fix Workflow
1. **Identify Failing Module** - Parse error stack to find the require() chain
2. **Trace Dependency Tree** - Find which package pulls in the incompatible version
3. **Pin Compatible Version** - Use package.json overrides/resolutions to pin working version
4. **Test Across Platforms** - Verify fix works on Node 20, 22, 24 and Windows/macOS/Linux
5. **Document Resolution** - Add comment explaining why the pin is needed

### Common Patterns
- `cssstyle` → `@asamuzakjp/css-color` v5 (ESM with TLA) → pin to v4.x
- `jsdom` → `html-encoding-sniffer` ESM → ensure compatible jsdom version
- Use `"overrides"` in package.json for transitive dependency pinning

## Agent Assignment
**Primary Agent:** devcore-devforge-core-development
**Company:** DevForge AI
**Role:** Module Resolution Specialist
**Reports To:** devcore-devforge-core-development
**Backup Agents:** fixer-devforge-bug-fixing, forge-devforge-system-architecture

## Success Metrics
- Server starts without module errors on all supported Node versions
- No regression in dependency resolution after fixes
- Fix documented with root cause analysis

## Error Handling
- **Error:** Override causes other conflicts
  **Response:** Test full dependency tree, use selective overrides
- **Error:** Upstream package updates break pin
  **Response:** Re-evaluate, update pin or switch to fixed upstream version

## Cross-Team Integration
**Gigabrain Tags:** devforge, esm, module-resolution, dependency-management, nodejs
**Related Skills:** devcore-devforge-core-development, fixer-devforge-bug-fixing, forge-devforge-system-architecture
**Last Updated:** 2026-04-07