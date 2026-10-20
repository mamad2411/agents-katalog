---
name: permissions-allow
description: Apply standard development permissions to the current project by creating .claude/settings.local.json with pre-approved tools and bash commands. Use when setting up a new project or when the user wants to configure Claude permissions.
allowed-tools: Write, Read
user-invocable: true
---

# Apply Standard Development Permissions

Create or update `.claude/settings.local.json` with pre-approved tools for efficient development.

## Instructions

Create `.claude/` directory if needed, then write `settings.local.json` with:

```json
{
  "permissions": {
    "allow": [
      "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch",
      "NotebookEdit", "Task", "Skill", "TodoWrite",
      "mcp__ide__getDiagnostics", "mcp__ide__executeCode",
      "mcp__context7__resolve-library-id", "mcp__context7__query-docs",
      "mcp__plugin_context7_context7__resolve-library-id",
      "mcp__plugin_context7_context7__query-docs",
      "mcp__brave-search__brave_web_search", "mcp__brave-search__brave_local_search",
      "mcp__firecrawl__firecrawl_scrape", "mcp__firecrawl__firecrawl_map",
      "mcp__firecrawl__firecrawl_search", "mcp__firecrawl__firecrawl_crawl",
      "mcp__firecrawl__firecrawl_check_crawl_status", "mcp__firecrawl__firecrawl_extract",
      "mcp__firecrawl__firecrawl_agent", "mcp__firecrawl__firecrawl_agent_status",
      "mcp__claude-in-chrome__javascript_tool", "mcp__claude-in-chrome__read_page",
      "mcp__claude-in-chrome__find", "mcp__claude-in-chrome__form_input",
      "mcp__claude-in-chrome__computer", "mcp__claude-in-chrome__navigate",
      "mcp__claude-in-chrome__resize_window", "mcp__claude-in-chrome__gif_creator",
      "mcp__claude-in-chrome__upload_image", "mcp__claude-in-chrome__get_page_text",
      "mcp__claude-in-chrome__tabs_context_mcp", "mcp__claude-in-chrome__tabs_create_mcp",
      "mcp__claude-in-chrome__update_plan", "mcp__claude-in-chrome__read_console_messages",
      "mcp__claude-in-chrome__read_network_requests", "mcp__claude-in-chrome__shortcuts_list",
      "mcp__claude-in-chrome__shortcuts_execute",
      "mcp__supabase__search_docs", "mcp__supabase__list_organizations",
      "mcp__supabase__get_organization", "mcp__supabase__list_projects",
      "mcp__supabase__get_project", "mcp__supabase__get_cost",
      "mcp__supabase__confirm_cost", "mcp__supabase__create_project",
      "mcp__supabase__pause_project", "mcp__supabase__restore_project",
      "mcp__supabase__list_tables", "mcp__supabase__list_extensions",
      "mcp__supabase__list_migrations", "mcp__supabase__get_logs",
      "mcp__supabase__get_advisors", "mcp__supabase__get_project_url",
      "mcp__supabase__get_publishable_keys", "mcp__supabase__generate_typescript_types",
      "mcp__supabase__list_edge_functions", "mcp__supabase__get_edge_function",
      "mcp__supabase__deploy_edge_function", "mcp__supabase__create_branch",
      "mcp__supabase__list_branches", "mcp__supabase__merge_branch",
      "mcp__supabase__reset_branch", "mcp__supabase__rebase_branch",
      "mcp__exa__web_search_exa",
      "Bash(dev-browser:*)",
      "Bash(pnpm:*)", "Bash(npm:*)", "Bash(node:*)", "Bash(npx:*)",
      "Bash(git:*)", "Bash(gh:*)", "Bash(docker:*)",
      "Bash(cat:*)", "Bash(ls:*)", "Bash(pwd:*)", "Bash(cd:*)", "Bash(mkdir:*)",
      "Bash(cp:*)", "Bash(mv:*)", "Bash(touch:*)", "Bash(chmod:*)", "Bash(echo:*)",
      "Bash(curl:*)", "Bash(which:*)", "Bash(env:*)", "Bash(export:*)", "Bash(source:*)",
      "Bash(open:*)", "Bash(code:*)", "Bash(supabase:*)", "Bash(vercel:*)",
      "Bash(playwright:*)", "Bash(tsc:*)", "Bash(eslint:*)", "Bash(prettier:*)",
      "Bash(tail:*)", "Bash(head:*)", "Bash(wc:*)", "Bash(sort:*)", "Bash(uniq:*)",
      "Bash(diff:*)", "Bash(grep:*)", "Bash(find:*)", "Bash(sed:*)", "Bash(awk:*)",
      "Bash(xargs:*)", "Bash(ps:*)", "Bash(kill:*)", "Bash(lsof:*)", "Bash(netstat:*)",
      "Bash(ping:*)", "Bash(ssh:*)", "Bash(scp:*)", "Bash(tar:*)", "Bash(zip:*)",
      "Bash(unzip:*)", "Bash(brew:*)", "Bash(python:*)", "Bash(python3:*)",
      "Bash(pip:*)", "Bash(pip3:*)"
    ],
    "ask": [
      "Edit(../)**", "Edit(~/**)", "Edit(//**)",
      "Write(../)**", "Write(~/**)", "Write(//**)",
      "Bash(cd ..)", "Bash(cd /*)", "Bash(cd ~)",
      "Bash(rm:*)", "Bash(rmdir:*)", "Bash(rm -rf:*)", "Bash(rm -r:*)", "Bash(rm -f:*)",
      "Bash(*rm *)", "Bash(*rmdir *)", "Bash(*:> *)", "Bash(shred:*)", "Bash(unlink:*)",
      "mcp__supabase__execute_sql", "mcp__supabase__apply_migration",
      "mcp__supabase__delete_branch"
    ]
  }
}
```

## What's Included

### Allowed (no confirmation)
- **Core tools**: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Task, Skill, TodoWrite
- **IDE integration**: getDiagnostics, executeCode
- **Context7**: Library documentation lookup
- **Search**: Brave Search, Exa
- **Firecrawl**: Web scraping, crawling, extraction, agent
- **Claude-in-Chrome**: Browser automation, screenshots, form filling, navigation
- **dev-browser**: Headless browser automation via Playwright (sandboxed scripts)
- **Supabase**: All read operations + project/branch management
- **Bash commands**: pnpm, npm, node, git, docker, curl, and many more utilities

### Ask-list (requires confirmation)
- Editing/writing files outside project directory
- Directory navigation outside project (cd .., cd /*, cd ~)
- Destructive commands (rm, rmdir, shred, unlink)
- Supabase write operations (execute_sql, apply_migration, delete_branch)
