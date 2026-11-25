```markdown
# everything-claude-code Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill documents the core development patterns, coding conventions, and workflows used in the `everything-claude-code` JavaScript repository. It is designed to help contributors understand how to add new skills, agents, commands, install targets, and maintain the codebase according to established conventions. The repository is framework-agnostic, uses conventional commits, and supports modular extension via skills, agents, and command workflows.

## Coding Conventions

- **File Naming:**  
  Use `camelCase` for JavaScript files (e.g., `installManifests.js`), and descriptive names for markdown/config files (e.g., `SKILL.md`, `install-modules.json`).

- **Import Style:**  
  Use relative imports for modules:
  ```js
  const registry = require('../lib/install-targets/registry');
  ```

- **Export Style:**  
  Both CommonJS (`module.exports = ...`) and ES module (`export default ...`) styles may be used, depending on file context.

- **Commit Messages:**  
  Follow [Conventional Commits](https://www.conventionalcommits.org/) with prefixes such as `fix`, `feat`, `docs`, `chore`.  
  Example:
  ```
  feat: add Gemini install target support
  ```

- **Test Files:**  
  Test files follow the `*.test.js` pattern and are colocated with the code under test or in a `tests/` directory.

## Workflows

### Add New Install Target
**Trigger:** When supporting a new IDE, platform, or environment for ECC installation  
**Command:** `/add-install-target`

1. Create a new install target script, e.g., `scripts/lib/install-targets/{target}-project.js`, `.{target}/install.sh`, or `.{target}/install.js`.
2. Add documentation for the new target, such as `.{target}/README.md`, `.{target}/README.zh-CN.md`, or `.{target}/GEMINI.md`.
3. Update `manifests/install-modules.json` to register the new target.
4. Update schemas:  
   - `schemas/ecc-install-config.schema.json`  
   - `schemas/install-modules.schema.json`
5. Update logic in:  
   - `scripts/lib/install-manifests.js`  
   - `scripts/lib/install-targets/registry.js`
6. Add or update tests in `tests/lib/install-targets.test.js`.
7. Update `README.md` if public-facing install instructions change.

**Example:**
```js
// scripts/lib/install-targets/gemini-project.js
module.exports = function installGemini() {
  // Installation logic for Gemini
};
```

---

### Add New Skill or Agent
**Trigger:** When introducing a new capability, workflow, or agent persona  
**Command:** `/add-skill`

1. Create a new `SKILL.md` in `skills/{skill-name}/` or `.agents/skills/{skill-name}/`.
2. For agents, add definitions in `agents/{agent-name}.md` or `.codex/agents/{agent-name}.toml`.
3. Update `manifests/install-modules.json` if the skill is installable.
4. Update `AGENTS.md` and/or `README.md` to document the new skill/agent.
5. Add supporting files as needed (e.g., `rules/`, `prompts/`, orchestration scripts).
6. If orchestration is needed, add a shell or JS orchestrator (e.g., `scripts/{skill-name}.sh`).

**Example:**
```markdown
# skills/mySkill/SKILL.md

## Overview
Describes the "mySkill" capability for ECC.

## Usage
...
```

---

### Add or Update Command Workflow
**Trigger:** When adding or improving CLI commands or workflows  
**Command:** `/add-command`

1. Create or modify a command markdown file in `commands/{command-name}.md` or `.claude/commands/{command-name}.md`.
2. Add YAML frontmatter and sections for Purpose, Usage, and Output.
3. Iterate based on review feedback (fix placeholders, add error handling, clarify protocol).
4. Update related commands or documentation if part of a workflow.
5. Document artifact storage locations if applicable.

**Example:**
```markdown
---
name: install
description: Install a new ECC module
---

## Purpose
...

## Usage
...
```

---

### Agent or Skill Bundle Import
**Trigger:** When bulk importing conventions, agent definitions, or skill documentation  
**Command:** `/import-bundle`

1. Add multiple files in `.claude/commands/`, `.claude/enterprise/`, `.claude/team/`, `.claude/research/`, `.claude/rules/`, `.codex/agents/`, `.claude/skills/`, `.agents/skills/`, etc.
2. Include team config, identity, guardrails, research playbook, and skills documentation.
3. No code/test changes—just documentation and config import.

---

### Dependency Update via Dependabot
**Trigger:** When Dependabot creates a PR for a new dependency version  
**Command:** `/update-dependencies`

1. Update versions in `package.json`, `package-lock.json`, or `yarn.lock`.
2. Update `.github/workflows/*.yml` for GitHub Actions if needed.
3. Commit with a standard Dependabot message.
4. Update `.github/dependabot.yml` for configuration if necessary.

---

### Refactor or Fix Skill or Agent
**Trigger:** When a skill/agent needs to be removed, merged, or reworked  
**Command:** `/remove-skill`

1. Remove or modify `SKILL.md` in `skills/{skill-name}/` or `agents/{agent-name}.md`.
2. Update `manifests/install-modules.json` and documentation.
3. Restore or remove associated files as needed.
4. Document the reason for the change (e.g., security, redundancy).

---

## Testing Patterns

- **Test Files:**  
  All test files use the `*.test.js` pattern.
- **Framework:**  
  No specific testing framework detected; use standard Node.js assertions or your preferred test runner.
- **Location:**  
  Tests are typically placed in a `tests/` directory or alongside the source files.

**Example:**
```js
// tests/lib/install-targets.test.js
const installGemini = require('../../scripts/lib/install-targets/gemini-project');

test('Gemini install target works', () => {
  expect(installGemini()).toBeDefined();
});
```

## Commands

| Command             | Purpose                                                      |
|---------------------|--------------------------------------------------------------|
| /add-install-target | Add support for a new install target (IDE/platform)          |
| /add-skill          | Add a new skill or agent to the ECC system                   |
| /add-command        | Add or update a CLI command or workflow                      |
| /import-bundle      | Bulk import agent/skill bundles or conventions documentation |
| /update-dependencies| Update dependencies via Dependabot                           |
| /remove-skill       | Refactor, remove, or revert a skill or agent                 |
```
