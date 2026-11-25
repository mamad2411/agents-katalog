---
name: project-plugin-management
description: 初始化和维护项目级 Claude 插件管理规则。Use when starting or onboarding any project, selecting Claude plugin marketplace plugins, deciding 常驻 vs 按需 plugin usage, writing plugin enable/disable policy into CLAUDE.md/AGENTS.md/project memory, or reminding users to install, enable, disable, or cautiously authorize plugins based on project context.
---

# Project Plugin Management

## Objective

Initialize a project-specific plugin management policy, not a generic plugin list. Reduce the user's cognitive and memory load by letting the agent decide, remind, and, when authorized, execute plugin installation and enable/disable actions based on actual project needs.

This skill covers plugins listed in the Claude plugin marketplace. Do not imply every plugin is made by Anthropic.

## Required Workflow

1. Inspect the project before recommending plugins.
   - Read available project context: README, package files, lockfiles, build/test config, deployment config, current git status, CLAUDE.md, AGENTS.md, and existing memory files.
   - Identify project goal, tech stack, framework, package manager, tests, deployment path, current phase, current task, collaboration tools, external services, and sensitive-data boundaries.

2. Ask questions if context is insufficient.
   - Do not recommend plugins from guesswork.
   - Ask the fewest necessary questions.
   - Do not ask for facts already available in project files.

3. Load `references/plugin-catalog.md` when choosing plugins.
   - Use the catalog for default 常驻/按需 recommendations, trigger scenarios, overlap notes, and cautious-authorization rules.
   - Prefer narrow, task-driven recommendations over broad installation.

4. Output four recommendation groups.
   - 必装且建议常驻: default-on plugins for this project and why.
   - 建议安装但按需开启: plugins to install but enable only for specific tasks.
   - 暂不建议安装: plugins that are irrelevant now and why.
   - 需要谨慎授权: plugins involving browser control, web crawling, GitHub, external services, finance, legal, or sensitive data.

5. For each recommended plugin, include:
   - plugin name
   - Claude marketplace URL
   - problem solved
   - 常驻 or 按需 decision
   - typical user prompt
   - overlaps, conflicts, or substitution notes

6. Generate a project plugin management memory rule.
   - Make it executable by future agents.
   - Include triggers for new feature development, frontend work, PR review, bug fixing, pre-release checks, long-term memory, project-rule maintenance, web crawling, GitHub work, legal/finance/sensitive-data handling, and high-permission tools.
   - Include when to install, enable, disable, or request authorization.
   - Include plugin overlap rules so future agents do not enable everything by default.

7. Write memory only after showing the target and proposed content.
   - Prefer existing CLAUDE.md, AGENTS.md, or established memory files.
   - If no suitable file exists, propose a location and wait for confirmation.
   - Merge with existing rules; do not overwrite team conventions.

8. Install or configure only with clear authorization.
   - If installation/configuration is supported, show commands and impact first.
   - Wait for confirmation unless the user explicitly authorized automatic execution.
   - After changes, report what was installed, enabled, disabled, or written.

## Memory Rule Template

Use this structure when writing project memory:

```markdown
## Claude Plugin Management

- Always-on plugins: <plugins and reasons>.
- On-demand plugins: <plugin -> exact trigger scenario>.
- Cautious plugins: <plugin -> authorization risk and confirmation requirement>.
- Overlap rules: <which plugins substitute or overlap, and preferred order>.
- Agent behavior:
  - When <scenario>, remind the user to install/enable <plugin>.
  - When <task finishes>, remind the user to disable <high-permission plugin>.
  - If authorized and environment supports it, install/configure required plugins before the task.
  - If project context is insufficient, ask concise questions before recommending plugins.
```

## Output Shape

Start with the conclusion. Keep explanations concrete.

```markdown
## 插件管理结论

### 必装且建议常驻
- `<plugin>`: <why>. Typical use: `<prompt>`.

### 建议安装但按需开启
- `<plugin>`: enable when <scenario>. Typical use: `<prompt>`.

### 暂不建议安装
- `<plugin>`: <why not now>.

### 需要谨慎授权
- `<plugin>`: <risk and confirmation rule>.

## 建议写入项目记忆的规则
<proposed memory block>

## 下一步
<install/configure/write-memory commands or confirmation questions>
```