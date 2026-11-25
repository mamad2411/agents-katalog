---
name: hermesfusion-multi-model-panel
description: Run multi-model consensus panels (Lite or Heavy) with your own agent backends—no hosted middleware, your models, your rules.
triggers:
  - set up a hermesfusion panel with multiple models
  - run a multi-model consensus check
  - configure hermesfusion lite or heavy mode
  - use hermesfusion to get second opinions from different models
  - set up a model panel for code review or architecture decisions
  - run hermesfusion with local and cloud models
  - create a fusion panel with custom agent backends
  - validate my hermesfusion configuration
---

# HermesFusion Multi-Model Panel

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

HermesFusion is a model-agnostic, provider-agnostic orchestration framework that runs consensus panels using multiple LLM backends. Inspired by OpenRouter's Fusion API, it lets you bring your own models (local via Ollama, cloud via OpenAI/Anthropic, or custom CLI agents) and run structured panels in two modes:

- **HF Lite**: 2 models in parallel → judge → synthesizer (~4 calls total)
- **HF Heavy**: 3 models in parallel → judge → synthesizer (~5 calls total)

Each panel member is just a configured shell command (`hermes`, `ollama run`, `openai chat`, or your own). No hosted middleware, no per-call markup. Use for code review, architecture decisions, security audits, or any task where you want multi-model consensus before shipping.

## Installation

```bash
pip install hermesfusion
```

Or from source:

```bash
git clone https://github.com/GiannoKlein9/HermesFusion.git
cd hermesfusion
pip install -e .
```

Requires Python 3.9+. You'll also need the CLIs/APIs for whichever models you wire up (e.g., `hermes`, `ollama`, `openai` CLI, etc.).

## Quick Start

### Interactive Setup

```bash
hermesfusion setup
```

The wizard will:
1. Ask for provider IDs (e.g., `fast`, `strong`, `local`)
2. Let you pick a recipe (`hermes`, `ollama`, `openai`, or `custom`)
3. Wire models into Lite and Heavy modes
4. Create `~/.hermesfusion/config.yaml`

Re-run any time to add more providers.

### Non-Interactive Setup (CI/Scripted)

```bash
hermesfusion setup --non-interactive \
  --provider fast --recipe hermes --label "Fast" \
  --hermes-provider openai --hermes-model gpt-4o-mini \
  --provider strong --recipe hermes --label "Strong" \
  --hermes-provider anthropic --hermes-model claude-3-5-sonnet \
  --lite-participants fast,strong --lite-judge strong --lite-synthesizer strong \
  --heavy-participants fast,strong --heavy-judge strong --heavy-synthesizer strong
```

### Manual Config

Create `~/.hermesfusion/config.yaml`:

```yaml
version: 1

providers:
  fast:
    label: Fast Analyst
    provider: openai
    model: gpt-4o-mini
    role: Quick analyst providing rapid insights.
    command:
      - hermes
      - -z
      - "{prompt}"
      - --provider
      - openai
      - --model
      - gpt-4o-mini
    timeout_seconds: 60
    passthrough_env: true

  strong:
    label: Deep Thinker
    provider: anthropic
    model: claude-3-5-sonnet
    role: Senior engineer with deep domain expertise.
    command:
      - hermes
      - -z
      - "{prompt}"
      - --provider
      - anthropic
      - --model
      - claude-3-5-sonnet
    timeout_seconds: 120
    passthrough_env: true

  local:
    label: Local Model
    provider: ollama
    model: llama3.1:8b
    role: Local privacy-focused analyst.
    command:
      - ollama
      - run
      - llama3.1:8b
      - "{prompt}"
    timeout_seconds: 180
    passthrough_env: false

modes:
  lite:
    display_name: HF Lite
    max_participants: 2
    max_calls_per_run: 4
    participants: [fast, strong]
    judge: strong
    synthesizer: strong

  heavy:
    display_name: HF Heavy
    max_participants: 3
    max_calls_per_run: 5
    participants: [fast, strong, local]
    judge: strong
    synthesizer: strong
```

Validate your config:

```bash
hermesfusion validate
hermesfusion show
```

## Core Commands

### Run a Panel

```bash
# Lite mode (2 models)
hermesfusion run --mode lite --prompt "Should we ship this feature on Friday?"

# Heavy mode (3 models)
hermesfusion run --mode heavy --prompt "Review this architecture for security issues"

# From file
hermesfusion run --mode lite --prompt-file ~/.hermesfusion/inputs/plan.md

# Dry run (see what would execute)
hermesfusion run --mode lite --prompt "..." --dry-run

# JSON output
hermesfusion run --mode heavy --prompt "..." --json
```

### Configuration Management

```bash
# Validate config
hermesfusion validate

# Show current config (obfuscates sensitive data)
hermesfusion show

# Check environment and dependencies
hermesfusion doctor
```

## Configuration Reference

### Provider Definition

```yaml
providers:
  my_provider:
    label: Human-Friendly Name           # shown in output
    provider: logical_name               # used in 'disabled' map
    model: gpt-4o-mini                   # free-form model ID
    role: Quick analyst.                 # role description for prompt
    command:                             # shell command array
      - hermes
      - -z
      - "{prompt}"                       # {prompt} is substituted
      - --provider
      - openai
      - --model
      - gpt-4o-mini
    timeout_seconds: 60                  # per-call timeout
    env:                                 # extra env vars for this provider
      CUSTOM_VAR: value
    passthrough_env: true                # inherit parent env (API keys)
```

### Mode Definition

```yaml
modes:
  lite:
    display_name: HF Lite
    max_participants: 2                  # hard cap
    max_calls_per_run: 4                 # hard cap (participants + judge + synthesizer)
    participants: [fast, strong]         # provider IDs
    judge: strong                        # provider ID for judging
    synthesizer: strong                  # provider ID for synthesis
```

### Safety & Execution Options

```yaml
output:
  dir: ~/.hermesfusion/runs             # where run artifacts are saved
  keep_last_n: 50                       # auto-prune old runs (future)

input:
  allowed_roots_extra: []               # extra paths for --prompt-file sandbox

safety:
  max_prompt_bytes: 200000              # refuse prompts bigger than this
  max_child_output_chars: 50000         # truncate child output
  allow_recursive: false                # allow nested HermesFusion calls

execution:
  parallel_participants: true           # run participants in parallel
  participant_timeout_seconds: 180      # fallback timeout
  passthrough_env_keys: []              # specific keys to forward when passthrough_env: false
  workdir: null                         # cwd for child processes (default: user home)

templates:
  participant: null                     # override bundled participant template
  judge: null                           # override bundled judge template
  synthesizer: null                     # override bundled synthesizer template
```

### Disabling Providers

```yaml
disabled:
  openai: "out of credits"              # disable by logical provider name
  ollama: "maintenance"
```

## Recipes

Built-in recipes for `hermesfusion setup`:

### Hermes Recipe

```yaml
command:
  - hermes
  - -z
  - "{prompt}"
  - --provider
  - openai
  - --model
  - gpt-4o-mini
```

### Ollama Recipe

```yaml
command:
  - ollama
  - run
  - llama3.1:8b
  - "{prompt}"
```

### OpenAI CLI Recipe

```yaml
command:
  - openai
  - chat
  - --model
  - gpt-4o-mini
  - "{prompt}"
```

### Custom Recipe

You provide the full command with `{prompt}` as a placeholder:

```yaml
command:
  - python
  - /path/to/my_agent.py
  - --prompt
  - "{prompt}"
  - --output
  - json
```

## Common Patterns

### Code Review Panel

```bash
# Create input file
mkdir -p ~/.hermesfusion/inputs
cat > ~/.hermesfusion/inputs/pr_review.md << 'EOF'
Review this PR for:
- Security issues
- Performance concerns
- Code style violations
- Missing tests

```diff
+ async def process_payment(amount: float, user_id: str):
+     await db.execute(f"INSERT INTO payments VALUES ({amount}, {user_id})")
```
EOF

# Run heavy panel
hermesfusion run --mode heavy --prompt-file ~/.hermesfusion/inputs/pr_review.md
```

### Architecture Decision Panel

```python
#!/usr/bin/env python3
"""Script to run architecture decisions through HermesFusion."""
import subprocess
import sys

def run_architecture_review(question: str, mode: str = "heavy"):
    """Run an architecture question through HermesFusion panel."""
    result = subprocess.run(
        ["hermesfusion", "run", "--mode", mode, "--prompt", question, "--json"],
        capture_output=True,
        text=True,
        check=False
    )
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return None
    
    import json
    return json.loads(result.stdout)

if __name__ == "__main__":
    question = """
    We're deciding between:
    A) Monolithic PostgreSQL with careful sharding
    B) Microservices with dedicated databases per service
    
    Context:
    - Team of 8 engineers
    - Expected 10k users in year 1, 100k in year 2
    - Budget for 2 full-time ops engineers
    - Current stack: Python/FastAPI, React
    
    Which approach should we choose and why?
    """
    
    panel = run_architecture_review(question)
    if panel:
        print("\n=== SYNTHESIS ===")
        print(panel["synthesis"]["output"])
```

### Hybrid Local + Cloud Setup

```yaml
providers:
  local_fast:
    label: Local Llama
    provider: ollama
    model: llama3.1:8b
    role: Fast local model for privacy-sensitive content.
    command: [ollama, run, llama3.1:8b, "{prompt}"]
    timeout_seconds: 120
    passthrough_env: false

  cloud_strong:
    label: Cloud GPT-4
    provider: openai
    model: gpt-4o
    role: Strong cloud model for complex reasoning.
    command: [hermes, -z, "{prompt}", --provider, openai, --model, gpt-4o]
    timeout_seconds: 180
    passthrough_env: true
    env:
      OPENAI_API_KEY: $OPENAI_API_KEY

modes:
  lite:
    participants: [local_fast, cloud_strong]
    judge: cloud_strong
    synthesizer: cloud_strong
```

### Custom Python Agent Integration

```yaml
providers:
  custom_agent:
    label: My Custom Agent
    provider: custom
    model: custom-v1
    role: Custom business logic agent.
    command:
      - python
      - /home/user/agents/my_agent.py
      - --input
      - "{prompt}"
      - --format
      - text
    timeout_seconds: 300
    passthrough_env: false
    env:
      AGENT_CONFIG: /home/user/agents/config.json
```

Corresponding agent:

```python
#!/usr/bin/env python3
"""my_agent.py - Custom agent compatible with HermesFusion."""
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--format", default="text")
    args = parser.parse_args()
    
    # Detect if running inside HermesFusion
    if os.getenv("HERMESFUSION_CHILD") == "1":
        # Write to stdout only (HermesFusion captures this)
        response = process_prompt(args.input)
        print(response, end="")
    else:
        # Standalone mode
        response = process_prompt(args.input)
        print(response)

def process_prompt(prompt: str) -> str:
    """Your custom logic here."""
    # Load config from env
    config_path = os.getenv("AGENT_CONFIG")
    # ... your agent logic ...
    return f"Analysis of prompt: {prompt[:50]}..."

if __name__ == "__main__":
    main()
```

## Output Artifacts

Every run saves to `~/.hermesfusion/runs/<timestamp>_<mode>.json`:

```json
{
  "timestamp": "20260614T120000Z",
  "mode": "lite",
  "task": "Should we ship this on Friday?",
  "participants": {
    "fast": {
      "provider_id": "fast",
      "label": "Fast Analyst",
      "model": "gpt-4o-mini",
      "output": "I recommend shipping. The feature is...",
      "duration_seconds": 2.3,
      "exit_code": 0
    },
    "strong": {
      "provider_id": "strong",
      "label": "Deep Thinker",
      "model": "claude-3-5-sonnet",
      "output": "Caution advised. While the feature works...",
      "duration_seconds": 4.1,
      "exit_code": 0
    }
  },
  "judge": {
    "provider_id": "strong",
    "output": "Participant 'strong' raises valid concerns about...",
    "duration_seconds": 3.2
  },
  "synthesis": {
    "provider_id": "strong",
    "output": "**Recommendation**: Delay until Monday. While 'fast' is optimistic...",
    "duration_seconds": 3.8
  },
  "total_duration_seconds": 13.4
}
```

Inspect with `jq`:

```bash
# Get synthesis
jq '.synthesis.output' ~/.hermesfusion/runs/20260614T120000Z_lite.json

# Get all participant outputs
jq '.participants[] | {label, output}' ~/.hermesfusion/runs/*.json

# Find runs that took > 10s
jq 'select(.total_duration_seconds > 10) | {timestamp, mode, duration: .total_duration_seconds}' ~/.hermesfusion/runs/*.json
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `HF_HOME` | Override `~/.hermesfusion` (where config, runs, inputs, lock live) |
| `HF_CONFIG` | Override config file path (default: `$HF_HOME/config.yaml`) |
| `HF_ALLOW_RECURSIVE=1` | Allow HermesFusion to run from inside a child invocation (debugging only) |
| `HERMESFUSION_CHILD=1` | Set automatically on child invocations; do not export manually |

Example:

```bash
export HF_HOME=/data/hermesfusion
export HF_CONFIG=/data/hermesfusion/production.yaml
hermesfusion run --mode heavy --prompt "..."
```

## Troubleshooting

### "Provider X command failed with exit code 1"

- Check that the CLI/binary exists: `which hermes`, `which ollama`
- Run the command manually to see the error: `hermes -z "test" --provider openai --model gpt-4o-mini`
- Verify API keys are in the environment: `echo $OPENAI_API_KEY`
- Check `passthrough_env: true` if your command needs parent env vars

### "Prompt file not in allowed sandbox"

HermesFusion restricts `--prompt-file` to:
- `~/.hermesfusion/inputs/`
- `/tmp/hermesfusion/`
- Paths in `input.allowed_roots_extra` config

Move your file or add the directory to config:

```yaml
input:
  allowed_roots_extra:
    - /home/user/projects/my-app/docs
```

### "Timeout waiting for provider X"

Increase timeout in config:

```yaml
providers:
  slow_model:
    timeout_seconds: 300  # 5 minutes
```

Or globally:

```yaml
execution:
  participant_timeout_seconds: 300
```

### "Recursive invocation detected"

You tried to run HermesFusion from inside a child command. This is blocked by default to prevent cost bombs.

If you really need nested panels (e.g., for meta-evaluation):

```bash
export HF_ALLOW_RECURSIVE=1
hermesfusion run --mode lite --prompt "..."
```

### Output truncated

Child output is capped at 50k chars by default:

```yaml
safety:
  max_child_output_chars: 100000  # raise to 100k
```

### Checking your setup

```bash
# Validate config syntax
hermesfusion validate

# Show current config (obfuscates secrets)
hermesfusion show

# Check environment, lock, dependencies
hermesfusion doctor
```

## Best Practices

1. **Use Lite for fast feedback**: Code style, quick decisions, sanity checks
2. **Use Heavy for high-stakes**: Architecture, security, production changes
3. **Mix local + cloud**: Keep sensitive data local, use cloud for complex reasoning
4. **Version control your config**: Store `config.yaml` in your team repo (without API keys)
5. **Use env vars for secrets**: Never hardcode API keys in config
6. **Test with --dry-run**: Verify what will execute before spending credits
7. **Monitor run artifacts**: Keep `~/.hermesfusion/runs/` for audit trail

## Integration Examples

### CI Pipeline

```yaml
# .github/workflows/architecture-review.yml
name: Architecture Review
on:
  pull_request:
    paths:
      - 'docs/architecture/**'

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install HermesFusion
        run: pip install hermesfusion
      
      - name: Setup config
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          hermesfusion setup --non-interactive \
            --provider fast --recipe hermes --label "Fast" \
            --hermes-provider openai --hermes-model gpt-4o-mini \
            --provider strong --recipe hermes --label "Strong" \
            --hermes-provider anthropic --hermes-model claude-3-5-sonnet \
            --heavy-participants fast,strong --heavy-judge strong --heavy-synthesizer strong
      
      - name: Run panel
        run: |
          hermesfusion run --mode heavy \
            --prompt-file docs/architecture/proposal.md \
            --json > panel.json
      
      - name: Post comment
        uses: actions/github-script@v6
        with:
          script: |
            const panel = require('./panel.json');
            const body = `## Architecture Panel Review\n\n${panel.synthesis.output}`;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
```

### Python Library Usage

```python
#!/usr/bin/env python3
"""Library usage example."""
import subprocess
import json
from pathlib import Path

def run_panel(prompt: str, mode: str = "lite") -> dict:
    """Run HermesFusion panel programmatically."""
    result = subprocess.run(
        ["hermesfusion", "run", "--mode", mode, "--prompt", prompt, "--json"],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)

def get_synthesis(prompt: str, mode: str = "lite") -> str:
    """Get just the synthesis output."""
    panel = run_panel(prompt, mode)
    return panel["synthesis"]["output"]

def save_decision(prompt: str, decision: str):
    """Save decision with panel provenance."""
    panel = run_panel(prompt, mode="heavy")
    
    Path("decisions").mkdir(exist_ok=True)
    decision_file = Path("decisions") / f"{panel['timestamp']}.md"
    
    decision_file.write_text(f"""# Decision: {prompt[:50]}...

## Prompt
{prompt}

## Panel Synthesis
{panel['synthesis']['output']}

## Participants
{json.dumps(panel['participants'], indent=2)}

## Decision
{decision}
""")
    
    return decision_file

# Example usage
if __name__ == "__main__":
    prompt = "Should we migrate to Rust for our API server?"
    synthesis = get_synthesis(prompt, mode="heavy")
    print(f"Panel recommends:\n{synthesis}")
    
    decision = "Proceeding with Rust migration based on panel consensus."
    saved = save_decision(prompt, decision)
    print(f"Decision saved to {saved}")
```

## Advanced Configuration

### Custom Templates

Override the bundled Jinja2 templates:

```yaml
templates:
  participant: /home/user/.hermesfusion/templates/participant.j2
  judge: /home/user/.hermesfusion/templates/judge.j2
  synthesizer: /home/user/.hermesfusion/templates/synthesizer.j2
```

### Selective Environment Passthrough

```yaml
providers:
  secure_model:
    passthrough_env: false
    env:
      ONLY_THIS_KEY: value
    
execution:
  passthrough_env_keys:
    - OPENAI_API_KEY
    - ANTHROPIC_API_KEY
    # Only these keys are forwarded to children with passthrough_env: false
```

### Multi-Stage Panels

Run two panels in sequence (Lite for quick filter, Heavy for deep dive):

```bash
#!/bin/bash
PROMPT="$1"

# Stage 1: Lite panel for quick filter
LITE_RESULT=$(hermesfusion run --mode lite --prompt "$PROMPT" --json)
LITE_SYNTHESIS=$(echo "$LITE_RESULT" | jq -r '.synthesis.output')

# Check if Lite panel flags concerns
if echo "$LITE_SYNTHESIS" | grep -qi "caution\|concern\|risk\|warning"; then
    echo "Lite panel flagged concerns. Running Heavy panel..."
    hermesfusion run --mode heavy --prompt "$PROMPT"
else
    echo "Lite panel approved. No Heavy panel needed."
    echo "$LITE_SYNTHESIS"
fi
```

---

HermesFusion gives you OpenRouter Fusion-style consensus without vendor lock-in. Wire up any models, keep your API keys, control your costs.
