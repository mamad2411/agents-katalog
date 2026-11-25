---
name: team-brain-sync
description: "Regenerate BRAIN.md and optionally generate .cursorrules and AGENTS.md from team brain entries. Use when user says 'sync', 'regenerate', 'update brain', or '/team-brain sync'."
allowed-tools: Bash, Read
---

# Team Brain Sync

Regenerate all auto-generated files from team brain entries.

## Process

1. Regenerate BRAIN.md:
```bash
node "${CLAUDE_SKILL_DIR}/../../scripts/generator.js" generate
```

2. Check config for additional generation targets:
```bash
node -e "
  const store = require('${CLAUDE_SKILL_DIR}/../../scripts/store');
  const gen = require('${CLAUDE_SKILL_DIR}/../../scripts/generator');
  const root = store.findProjectRoot();
  const config = store.loadConfig(root);

  gen.generateBrain(root);
  console.log('BRAIN.md regenerated.');

  if (config.inject_into_claude_md) {
    gen.injectIntoClaude(root);
    console.log('CLAUDE.md updated with team brain section.');
  }

  if (config.generate_cursorrules) {
    gen.generateCursorrules(root);
    console.log('.cursorrules generated.');
  }

  if (config.generate_agents_md) {
    gen.generateAgentsMd(root);
    console.log('AGENTS.md generated.');
  }
"
```

3. Show the updated stats:
```bash
node "${CLAUDE_SKILL_DIR}/../../scripts/stats.js"
```

4. Remind the user to commit changes if any files were generated/updated.

## Subcommands

### `/team-brain sync cursorrules`
Enable and generate .cursorrules:
```bash
node -e "
  const store = require('${CLAUDE_SKILL_DIR}/../../scripts/store');
  const gen = require('${CLAUDE_SKILL_DIR}/../../scripts/generator');
  const root = store.findProjectRoot();
  const config = store.loadConfig(root);
  config.generate_cursorrules = true;
  store.saveConfig(root, config);
  gen.generateCursorrules(root);
  console.log('.cursorrules generated and enabled in config.');
"
```

### `/team-brain sync agents`
Enable and generate AGENTS.md:
```bash
node -e "
  const store = require('${CLAUDE_SKILL_DIR}/../../scripts/store');
  const gen = require('${CLAUDE_SKILL_DIR}/../../scripts/generator');
  const root = store.findProjectRoot();
  const config = store.loadConfig(root);
  config.generate_agents_md = true;
  store.saveConfig(root, config);
  gen.generateAgentsMd(root);
  console.log('AGENTS.md generated and enabled in config.');
"
```
