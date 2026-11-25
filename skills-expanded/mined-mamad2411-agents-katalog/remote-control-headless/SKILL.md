---
name: "remote-control-headless"
description: "Claude Code Remote Control: manage headless Claude Code sessions from anywhere, CI/CD integration, remote orchestration from mobile/laptop, session attach/detach, and remote execution patterns"
---

# Remote Control — Headless Session Management

## When to activate
- Running Claude Code on a remote server (cloud VM, CI runner) and controlling from a laptop or mobile
- Integrating Claude Code into CI/CD pipelines as an autonomous agent step
- Managing long-running sessions that outlive your local terminal connection
- Orchestrating multiple Claude Code instances across different machines
- Starting a session on one device and resuming from another
- Running Claude Code as a service that accepts commands via API

## When NOT to use
- Local interactive sessions where you're sitting at the same machine
- Quick one-off tasks that don't need remote access overhead
- When SSH + tmux/screen is simpler and sufficient
- Development tasks that require real-time visual feedback (UI work, design)

## Instructions

### 1. Remote Control Architecture

```
┌──────────────┐         ┌──────────────────┐         ┌────────────────┐
│  Controller  │────────▶│  Remote Session  │────────▶│  Target Repo   │
│  (laptop/    │  HTTPS/ │  (headless)      │  exec   │  (workspace)   │
│   mobile/CI) │◀────────│  Claude Code     │◀────────│                │
└──────────────┘  stream └──────────────────┘  result └────────────────┘
      │                    │
      │ attach/detach      │ auto-suspend on disconnect
      ▼                    ▼
  Resume anywhere     Session state persisted to disk
```

### 2. Headless Session Setup

**Starting a remote session:**
```bash
# On the remote server
claude --headless --session-id "remote-dev-2026-06-13" \
  --workspace /home/deploy/project \
  --listen 0.0.0.0:8765 \
  --auth-token "$CLAUDE_AUTH_TOKEN"

# Session runs in background, accepts commands via HTTP
```

**Connecting from a controller:**
```bash
# From laptop
claude remote attach \
  --host dev-server.example.com:8765 \
  --auth-token "$CLAUDE_AUTH_TOKEN" \
  --session-id "remote-dev-2026-06-13"

# Now you can interact with the remote session as if local
```

### 3. CI/CD Integration Patterns

**GitHub Actions step:**
```yaml
# .github/workflows/claude-review.yml
jobs:
  claude-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Claude Code Review
        uses: anthropic/claude-code-action@v1
        with:
          prompt: |
            Review the changes in this PR. Focus on:
            1. Security vulnerabilities
            2. Performance regressions
            3. Test coverage gaps
            Post your review as a PR comment.
          auth_token: ${{ secrets.CLAUDE_AUTH_TOKEN }}
```

**GitLab CI step:**
```yaml
# .gitlab-ci.yml
claude-analysis:
  stage: analyze
  script:
    - claude --headless --prompt "Analyze code changes in $CI_MERGE_REQUEST_DIFF_BASE_SHA..HEAD"
      --output-format json > analysis.json
    - claude --headless --prompt "Summarize findings from analysis.json and post to MR"
  artifacts:
    reports:
      codequality: analysis.json
```

### 4. Session Attach/Detach

**Detach (leave session running):**
```bash
# Press Ctrl+B then D (like tmux) or:
claude remote detach --session-id "remote-dev-2026-06-13"
# Session continues running in background
# State is auto-saved every 30 seconds
```

**Reattach (from same or different device):**
```bash
# From phone, another laptop, or after network reconnect:
claude remote attach --session-id "remote-dev-2026-06-13"
# Full context restored: conversation history, file state, tool results
```

**Session list (see all running sessions):**
```bash
claude remote list
# remote-dev-2026-06-13   running  47m   dev-server:8765
# ci-review-abc123         idle     2h    ci-runner:8765
# data-pipeline-run        complete 12m   ml-server:8765
```

### 5. Remote Command Execution

**Send commands to a headless session:**
```bash
# Simple prompt
claude remote exec --session-id "remote-dev" --prompt "Run the test suite and report failures"

# With file upload
claude remote exec --session-id "remote-dev" \
  --prompt "Review this spec and implement it" \
  --attach spec.md

# With structured output
claude remote exec --session-id "remote-dev" \
  --prompt "List all TODO comments with file paths" \
  --output-format json
```

### 6. Multi-Machine Orchestration

Coordinate Claude Code instances across multiple machines:

```yaml
orchestration:
  machines:
    - host: "dev-server-1"
      session: "backend-refactor"
      task: "Refactor authentication module to use JWT"
      
    - host: "dev-server-2"
      session: "frontend-update"
      task: "Update login flow to match new JWT API"
      
    - host: "test-runner"
      session: "integration-tests"
      task: "Wait for both refactor and update, then run integration tests"
      depends_on: ["backend-refactor", "frontend-update"]
  
  coordinator:
    on_all_complete: "Generate cross-machine change summary"
    on_failure: "Halt dependent tasks, report which machine failed"
```

### 7. Security & Access Control

```yaml
remote_security:
  authentication:
    method: "token"          # or "ssh-key", "oauth"
    token_env: "CLAUDE_AUTH_TOKEN"
    rotation: "every-24h"
  
  network:
    bind: "127.0.0.1"       # localhost only (recommended)
    # bind: "0.0.0.0"       # all interfaces (requires firewall)
    tls: true               # encrypt in transit
    allowed_ips: []         # empty = any; or ["10.0.0.0/8"]
  
  authorization:
    read_only: false         # true = can observe but not execute
    allowed_tools: ["read", "grep", "bash"]  # restrict tool access
    blocked_paths: ["/etc", "/root"]          # prevent access to sensitive dirs
  
  audit:
    log_all_commands: true
    log_file: "/var/log/claude-remote.log"
```

## Example

**Running a headless session for overnight refactoring:**

```
1. Start session on cloud VM before leaving office:
   claude --headless --session-id "overnight-refactor"
   
2. Send initial task:
   claude remote exec --prompt "Refactor all database queries in src/api/ 
   to use parameterized statements. Write tests for each. 
   Commit to branch refactor/parameterized-queries."

3. Detach and close laptop.

4. Next morning, check from phone:
   claude remote list
   → overnight-refactor  running  8h  cloud-vm:8765
   
5. Attach and review:
   claude remote attach --session-id "overnight-refactor"
   → 47 files changed, 12 new test files, 3 files need manual review
   → Branch pushed, PR ready for review
```

## Anti-Patterns

- **No auth token:** Running headless without authentication exposes Claude Code to anyone on the network
- **Binding to 0.0.0.0 without TLS:** Remote sessions on public interfaces without encryption leak all data in transit
- **No timeout:** Headless sessions running forever consume resources — set idle timeout to auto-suspend
- **State loss on disconnect:** Not enabling auto-save means a network blip loses the entire session state
- **Over-privileged tools:** Giving remote sessions full bash + filesystem access when they only need read + grep — always scope tools to minimum needed
- **Zombie sessions:** Completed sessions not cleaned up accumulate on the server — use `--auto-cleanup` or periodic `claude remote prune`
