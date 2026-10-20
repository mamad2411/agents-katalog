---
description: CRITICAL - Essential AI assistant guidelines and workflows
alwaysApply: true
tags: [critical, ai-assistant, workflow, rules]
priority: 1
version: 1.0.0
---

# CRITICAL: AI Assistant Guidelines

## ⚠️ MANDATORY RULE: Rule Access via MCP

### ACCESS RULES VIA MCP SERVER

**CRITICAL**: 
- ✅ **ALWAYS** access rules via MCP server tools (`list_mcp_resources`, `fetch_mcp_resource`)
- ✅ **ALWAYS** use MCP tools to read rule files from the Git repository
- ✅ **ALWAYS** verify rules are available via MCP before using them
- ❌ **NEVER** assume rules are available without checking MCP server
- ❌ **NEVER** try to access rules from local `.cursor/rules/` directory (rules are in Git repository)
- ✅ **ALWAYS** use MCP resource URIs (e.g., `rule://00-critical/ai-assistant-guidelines`)

**Why**: Rules are stored in a Git repository and accessed via MCP server. Local file system access is not available.

### MCP Rule Access Workflow

**When Reading Rules:**
1. Use `list_mcp_resources` to see available rules
2. Use `fetch_mcp_resource` with rule URI (e.g., `rule://00-critical/ai-assistant-guidelines`)
3. Never assume rules are cached - always fetch via MCP

**When Updating Rules (Repository Maintainers Only):**
1. Rules are updated in the Git repository
2. Use `read_file` to read current content from repository
3. Use `search_replace` or `write` to modify files in repository
4. Commit changes to Git repository
5. MCP server automatically refreshes from Git

**When Creating New Rules (Repository Maintainers Only):**
1. Use `write` tool to create new `.mdc` files in `.cursor/rules/` in repository
2. Verify file was created using `list_dir` or `read_file`
3. Commit to Git repository
4. MCP server will make new rules available automatically

---

## Rule File Structure

### Location
- All rules are stored in Git repository: `https://github.com/mattcknight/cursor-rules-mcp.git`
- Rules are in `.cursor/rules/` directory in the repository
- Rules are `.mdc` files (Markdown with frontmatter)
- Rules are organized by category in subdirectories

### Accessing Rules via MCP
- ✅ Use `list_mcp_resources` to list all available rules
- ✅ Use `fetch_mcp_resource` with rule URI to read specific rules
- ✅ Rule URIs follow pattern: `rule://{category}/{rule-name}` (e.g., `rule://00-critical/ai-assistant-guidelines`)
- ❌ Never try to access rules from local file system

### Updating Rules (Repository Maintainers)
- ✅ Use `read_file` to read rule files from repository
- ✅ Use `search_replace` for partial updates in repository
- ✅ Use `write` for complete rewrites in repository
- ✅ Commit changes to Git repository
- ✅ MCP server automatically refreshes from Git

---

## Critical Workflow Rules

### ALWAYS
- ✅ Access rules via MCP server tools
- ✅ Use `list_mcp_resources` to discover available rules
- ✅ Use `fetch_mcp_resource` to read specific rules
- ✅ Verify rules are available via MCP before using

### NEVER
- ❌ Try to access rules from local `.cursor/rules/` directory
- ❌ Assume rules are available without checking MCP server
- ❌ Use local file system tools for rule access (rules are in Git)
- ❌ Skip MCP server when accessing rules

---

**Last Updated:** 2025-11-21  
**Version:** 2.0.0  
**Rule Type:** CRITICAL - AI Assistant Workflow  
**Priority:** HIGHEST  
**Access Method:** MCP Server (Model Context Protocol)
