---
description: "Setup or reconfigure AI dispatch backends. Run when dispatch fails or to add new API keys."
---

# AI Dispatch Setup

Run the setup script to install `dispatch`/`dcheck` and configure API keys.

```bash
bash $SKILL_DIR/../../scripts/setup.sh
```

After setup, verify:
```bash
dispatch --list
```

If the user wants to add a new backend, show them the config file format and help edit `~/.config/ai-dispatch/config.json`.
