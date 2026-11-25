# Feishu Evolver Wrapper

A lightweight wrapper for the `capability-evolver` skill.
It injects the Feishu reporting environment variables (`EVOLVE_REPORT_TOOL`) to enable rich card reporting in the Master's environment.

## Usage

```bash
# Run the evolution loop
node skills/feishu-evolver-wrapper/index.js

# Generate Evolution Dashboard (Markdown)
node skills/feishu-evolver-wrapper/visualize_dashboard.js
```

## Features

- **Evolution Loop**: Runs the GEP evolution cycle with Feishu reporting.
- **Dashboard**: visualizing metrics and history from `assets/gep/events.jsonl`.
- **Export History**: Exports raw history to Feishu Docs.
