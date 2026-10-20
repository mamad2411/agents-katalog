---
description: CRITICAL - Rules are accessed via MCP server from Git repository
globs: "**/*"
tags: [critical, mcp, onboarding]
priority: 1
version: 2.0.0
---

# CRITICAL: Rules Access via MCP Server

## ⚠️ READ THIS FIRST ⚠️

**Rules are accessed via MCP (Model Context Protocol) server from this Git repository. You do NOT need to copy rules to your project.**

### What This Repository Is

This repository contains **reusable `.cursor/rules` templates** that are accessed via an MCP server. Rules are automatically fetched from this Git repository and made available to Cursor AI through the MCP server.

### How to Use Rules via MCP

1. **Configure MCP Server in Cursor**
   - Open Cursor Settings → Features → MCP
   - Add the cursor-rules-mcp server pointing to this repository
   - The server automatically fetches rules from Git

2. **Access Rules via MCP**
   - Rules are automatically available when the MCP server is configured
   - Use `@mcp` or MCP tools to access specific rules
   - Rules are cached and refreshed automatically

3. **Select Relevant Personas**
   - All 19 personas are available via MCP
   - Access them through the MCP server interface
   - No local file copying required

4. **Start Using Personas**
   ```markdown
   @persona-developer
   
   I need to implement [feature]. Please review requirements and propose approach.
   ```

### What This Template Provides

1. **19 Specialized AI Personas**
   - Developer, Architect, QA Engineer, Security Analyst, etc.
   - Pre-configured for production code development
   - Ready to use immediately

2. **Production-Ready Standards**
   - Git workflow standards (commit messages, branch naming)
   - Code style guidelines
   - Testing standards
   - Documentation standards
   - All designed for production code

3. **Best Practices**
   - Industry-standard patterns
   - Cross-project learnings
   - Proven workflows

### Important Notes

- ✅ **Rules accessed via MCP** - No local copying required, rules are fetched from Git
- ✅ **Automatic updates** - Rules are refreshed from Git repository automatically
- ✅ **Centralized management** - All rules maintained in this Git repository
- ✅ **Focus on your code** - Use personas to help write, review, and maintain your production code

### MCP Server Benefits

- ✅ **No local files** - Rules don't need to be copied to each project
- ✅ **Always up-to-date** - Rules are fetched from Git, ensuring latest versions
- ✅ **Centralized updates** - Rule changes propagate to all projects automatically
- ✅ **Easy maintenance** - Update rules once in Git, all projects benefit

### Available via MCP

- ✅ All persona files (`personas/*.mdc`) - Access via MCP server
- ✅ Development standards (`development/*.mdc`) - Available through MCP
- ✅ Documentation standards (`documentation/*.mdc`) - Fetched from Git
- ✅ AI guidelines (`ai-guidelines/*.mdc`) - Accessible via MCP resources

---

## For Repository Maintainers

**If you are maintaining this rules repository:**

This repository is a **centralized rules repository** that:
- Aggregates learnings from multiple AI-assisted development projects
- Provides reusable `.cursor/rules` templates via MCP server
- Documents best practices and patterns
- Serves rules to multiple projects through MCP

See `.cursor/rules/README.md` for maintenance guidelines.

---

**Last Updated:** 2025-11-21  
**Version:** 2.0.0  
**Access Method:** MCP Server (Model Context Protocol)  
**Primary Purpose:** Enable AI-assisted production code development via centralized rules repository
