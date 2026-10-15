---
name: llmem-setup
description: >
  Install and configure LLMem for an agent harness. Handles CLI install, plugin
  deployment, skill registration, and provider setup. Triggers on: "install llmem",
  "set up memory", "configure memory", "add llmem to harness", "memory setup".
license: MIT
---

# LLMem Setup

Install, configure, and integrate LLMem into an agent's harness so it can use structured memory.

## When to Run

- Setting up memory for a new agent
- Adding memory to an existing agent harness
- After cloning LLMem and before first use
- When an agent asks "how do I get llmem working?"

## Installation Philosophy

**Plugin-first, zero-config instructions.** LLMem uses platform plugins to inject memory context automatically at session start, extract memories on idle/end, and preserve context during compaction. This means:

- **No manual instruction editing required.** The plugin handles automatic lifecycle hooks.
- **Skills provide on-demand behavioral guidance.** When the agent encounters a memory-related situation, it loads the skill. No need to paste 80 lines of instructions into AGENTS.md.
- **One line in config enables everything.** Add the plugin and you're done.

## Procedure

### Step 1: Install LLMem CLI

```bash
# Option A: Install from source (Go binary)
git clone https://github.com/MichielDean/LLMem.git
cd LLMem && make build
# Binary at ~/.local/bin/llmem, symlinked to /usr/local/bin/llmem

# Option B: One-liner
curl -sSL https://raw.githubusercontent.com/MichielDean/LLMem/main/setup.sh | bash
```

Verify:
```bash
llmem --help
llmem stats
```

### Step 2: Initialize

```bash
llmem init          # Interactive — detects providers
llmem init --non-interactive  # Script-friendly — uses defaults
```

This creates `~/.config/llmem/config.yaml` and `~/.config/llmem/memory.db`.

### Step 3: Configure Provider

Choose one:

**Ollama (local, free):**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull nomic-embed-text
ollama pull qwen2.5:1.5b
# Config auto-detected
```

**OpenAI (cloud, needs API key):**
```bash
export OPENAI_API_KEY=sk-...
llmem init --non-interactive
```

**Local (sentence-transformers, no server):**
```bash
pip install ".[local]"
# Set provider.default: local in config.yaml
```

**None (FTS5-only mode):** Works without any provider. Semantic search disabled.

### Step 4: Install Plugin and Skills

**The recommended approach — fully automatic:**

The npm postinstall script deploys everything: skills, platform plugin, and tools.

```bash
cd LLMem && npm install
```

This runs `install.js` which:
1. Copies 4 skill directories to `~/.agents/skills/`
2. Auto-detects your platform (OpenCode, Claude Code, Copilot CLI)
3. Deploys the correct plugin to the right location
4. Deploys OpenCode custom tools to `.opencode/tools/` (if OpenCode detected)

**Manual plugin deployment:**

If you can't use npm install, deploy manually:

| Platform | Plugin file | Target |
|----------|------------|--------|
| OpenCode | `plugins/opencode/llmem.js` | `~/.config/opencode/plugins/llmem.js` |
| Claude Code | Entire `plugins/agent/` directory | `~/.claude/plugins/llmem/` |
| Copilot CLI | Entire `plugins/agent/` directory | `~/.copilot/installed-plugins/_direct/llmem/` |

**Force a specific platform:**

```bash
node install.js --platform opencode    # OpenCode only
node install.js --platform claude-code # Claude Code only
node install.js --platform copilot     # Copilot CLI only
node install.js --platform all         # All platforms
node install.js --platform none         # Skills only, no plugins
```

### Step 5: Configure Agent (Platform-Specific)

#### OpenCode

Add the plugin to your `opencode.json`:

```json
{
  "plugin": ["llmem"]
}
```

Or, if using local plugin deployment (the file was already copied by install.js), no config needed — OpenCode auto-discovers plugins in `~/.config/opencode/plugins/`.

**Custom tools** (`.opencode/tools/`) are auto-discovered by OpenCode when working in the LLMem repo. For other projects, copy the `.opencode/tools/` directory or reference it via `OPENCODE_CONFIG_DIR`.

**Instructions in AGENTS.md — optional.** The plugin injects context at session start. The `llmem` skill loads on-demand. If you want a persistent reminder, add this minimal line:

```markdown
## Memory

Plugin-managed. Search when uncertain: `llmem search "topic"`. Add when you learn: `llmem add --type fact --content "..."`.
```

#### Claude Code

The plugin is installed at `~/.claude/plugins/llmem/`. Enable it:

```bash
claude plugin install ~/.claude/plugins/llmem
# Or use --plugin-dir for testing:
claude --plugin-dir ~/.claude/plugins/llmem
```

The plugin provides:
- **`SessionStart` hook**: Injects `llmem stats` + behavioral patterns + proposed procedures at session start
- **`SessionEnd` hook**: Runs `llmem hook ending` for memory extraction + introspection
- **`PreCompact` hook**: Injects key memories before compaction
- **Skills**: `llmem`, `llmem-setup`, `introspection`, `introspection-review-tracker` — loaded on-demand

**Instructions in CLAUDE.md — optional.** The `SessionStart` hook injects context. If you want a persistent reminder:

```markdown
## Memory

Plugin-managed. Search when uncertain: `llmem search "topic"`. Add when you learn: `llmem add --type fact --content "..."`.
```

#### Copilot CLI

The plugin is installed at `~/.copilot/installed-plugins/_direct/llmem/`. Enable it:

```bash
copilot plugin install ~/.copilot/installed-plugins/_direct/llmem
# Or install directly from the GitHub repo:
copilot plugin install MichielDean/LLMem:plugins/agent
```

Copilot CLI uses the same plugin format as Claude Code (`.claude-plugin/plugin.json`) but installs to `~/.copilot/` instead of `~/.claude/`. The hooks and skills are identical.

**Instructions in COPILOT.md — optional.** If you want a persistent reminder:

```markdown
## Memory

Plugin-managed. Search when uncertain: `llmem search "topic"`. Add when you learn: `llmem add --type fact --content "..."`.
```

### Step 6: Verify

```bash
# CLI works
llmem --help
llmem stats

# Can add and search
llmem add --type fact --content "test memory"
llmem search "test"

# Skills are discoverable
ls ~/.agents/skills/llmem ~/.agents/skills/introspection

# Plugin deployed
# OpenCode:
ls ~/.config/opencode/plugins/llmem.js
# Claude Code:
ls ~/.claude/plugins/llmem/.claude-plugin/plugin.json
# Copilot CLI:
ls ~/.copilot/installed-plugins/_direct/llmem/.claude-plugin/plugin.json

# Optional: verify OpenCode tools
ls .opencode/tools/llmem-*.ts
```

### Step 7: Dream Timer (Optional)

For automatic memory consolidation:

```bash
# Copy and enable systemd timer
cp harness/llmem-dream.service ~/.config/systemd/user/
cp harness/llmem-dream.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable llmem-dream.timer
systemctl --user start llmem-dream.timer
```

Runs nightly at 3am by default. Configure in `~/.config/llmem/config.yaml` under `dream:`.

## Architecture

```
Agent Session
    │
    ├── Plugin (auto, no instructions needed)
    │   ├── session.created/start → llmem stats + search behavioral/proposed → inject context
    │   ├── session.idle/end      → llmem hook idle/ending → extract + introspect
    │   └── session.compacting    → llmem context --compacting → preserve key memories
    │
    ├── Skills (on-demand, loaded by trigger)
    │   ├── llmem                      → CLI reference, memory types, commands
    │   ├── llmem-setup                → This file
    │   ├── introspection              → Self-assessment framework, error taxonomy
    │   └── introspection-review-tracker → Review outcome tracking
    │
    └── Custom Tools (structural, zero-instruction)
        ├── llmem-search   → Search memories
        ├── llmem-add      → Add a memory
        ├── llmem-context  → Get context for a topic
        ├── llmem-invalidate → Soft-delete a memory
        ├── llmem-stats    → Show memory statistics
        └── llmem-hook     → Run extraction hook
```

The plugin handles everything the agent physically cannot do itself (inject context before the first message, extract on idle). The skills provide behavioral guidance when the agent needs it. Custom tools provide typed access to memory operations without requiring skill loading.

## Troubleshooting

**`llmem: command not found`** — Binary not on PATH. Check `which llmem` or `ls ~/.local/bin/llmem`. May need `ln -s ~/.local/bin/llmem /usr/local/bin/llmem`.

**`Ollama not reachable`** — Start Ollama (`ollama serve`), pull models (`ollama pull nomic-embed-text`), or switch providers. LLMem falls back: Ollama → OpenAI → Anthropic → local → none (FTS5-only).

**Plugin not loading** — Verify the plugin file exists at the expected path. For OpenCode, check `~/.config/opencode/plugins/llmem.js`. For Claude Code, check `~/.claude/plugins/llmem/`.

**Skills not discovered** — Verify skill directories: `ls ~/.agents/skills/llmem/`. If missing, re-run `node install.js`.

**Context not injected at session start** — Check the plugin log. For OpenCode, run `llmem stats` and `llmem search behavioral --type self_assessment --limit 5` manually to verify the commands work. The plugin runs these same commands.