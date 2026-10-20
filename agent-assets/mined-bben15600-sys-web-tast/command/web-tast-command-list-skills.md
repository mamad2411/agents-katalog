# List Skills

## Role
You are a skills discovery agent. Find every installed skill and present it as a clear, categorized reference table.

## Instructions

1. **Discover all skill sources** in parallel:
   - Glob `.claude/commands/*.md` — project-level slash commands
   - Glob `.claude/plugins/**/SKILL.md` — plugin-bundled skills

2. **Read each file's YAML frontmatter** (lines between the opening and closing `---`):
   - Extract `name` (fall back to the filename stem if absent)
   - Extract `description`

3. **Deduplicate**: if the same skill name appears in both `commands/` and `plugins/`, keep only one entry (prefer the `commands/` version).

4. **Categorize** each skill by scanning keywords in its description:

   | Category | Keywords |
   |----------|----------|
   | ⚙️ Config & Environment | config, settings, hook, permission, env, loop |
   | 📝 Code & Refactoring | refactor, scaffold, simplify, feature, boilerplate |
   | 🤖 Skill Building | skill, build-skill, converter, research |
   | 📚 Documentation | doc, markdown, style-guide, drift, init, CLAUDE.md |
   | 🔬 Research & Planning | research, prompt, deploy-research, process-card |
   | 🔧 Git & DevOps | commit, git, template, cleanup |
   | 🔍 Review & Security | review, security, audit |
   | 📊 Monitoring & Info | debug, cost, context, insights, heapdump, batch, onboarding |

   Skills that fit none of the above go under **🗂️ Other**.

5. **Output** a grouped Markdown table per category.

6. **Output the Built-in Skills section** — hardcoded, Claude Code loads these at runtime with no
   SKILL.md in the repository:

   ```
   ## 🔌 Claude Code Built-ins
   | Skill | Description |
   |-------|-------------|
   | `batch` | Run multiple sub-agent tasks in parallel batches. |
   | `claude-api` | Build, debug, and optimize Claude API / Anthropic SDK apps. Trigger: code imports `anthropic`/`@anthropic-ai/sdk`, or you need to tune caching, tool use, or model config. |
   | `debug` | Debug issues in the current session or codebase. |
   | `fewer-permission-prompts` | Scan transcripts for common read-only tool calls and add an allowlist to project settings to reduce permission prompts. |
   | `init` | Initialize a new CLAUDE.md file with codebase documentation. |
   | `keybindings-help` | Customize keyboard shortcuts and rebind keys in `~/.claude/keybindings.json`. |
   | `loop` | Run a prompt or slash command on a recurring interval. Use for polling, repeated tasks, or self-paced loops. |
   | `review` | Review a pull request — reads the diff and posts structured feedback. |
   | `security-review` | Complete a security review of the pending changes on the current branch. |
   | `session-start-hook` | Create and develop startup hooks for Claude Code on the web. |
   | `simplify` | Review changed code for reuse, quality, and efficiency, then fix issues found. |
   | `update-config` | Configure the Claude Code harness via settings.json — hooks, permissions, env vars, and automated behaviors. |
   ```

7. **Footer** — combined count:
   `> **N skills found** — X from repository (commands + plugins), 12 Claude Code built-ins.`

## Notes
- Read only frontmatter — stop at the second `---`.
- Skip files with no frontmatter silently.
- Read-only: do not modify any files.
