---
name: hermes-agentmesh-async-bus
description: Build cross-device async multi-agent systems using Redis message bus with 0-SSH deployment
triggers:
  - set up async message bus for multi-agent systems
  - deploy Hermes AgentMesh across devices
  - configure Redis-backed agent communication
  - fix agent timeout issues with async messaging
  - run cross-device agent collaboration without SSH
  - build peer-to-peer agent mesh network
  - orchestrate multi-agent debate asynchronously
  - troubleshoot AgentMesh worker deployment
---

# Hermes AgentMesh Async Bus

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## What It Does

Hermes-AgentMesh is a **Redis-backed async message bus** that solves HTTP timeout crashes for long-running multi-agent tasks. Instead of synchronous `requests.post()` calls that timeout after 5-10 minutes, agents communicate via Redis queues ("mailboxes") that persist tasks indefinitely.

**Key capabilities:**
- **0-SSH cross-device deployment** — workers run as systemd/LaunchAgent daemons
- **Timeout elimination** — 15-minute+ agent tasks work reliably
- **Framework agnostic** — works with Hermes, OpenClaw, LangGraph, AutoGen, CrewAI, custom agents
- **Natural persistence** — tasks survive server restarts
- **Decoupled architecture** — sender doesn't block waiting for receiver

**Architecture:**
```
Mac mini (central hub)          Remote nodes (X230i, Pi, WSL)
├── Redis :6379 (0.0.0.0)      └── worker_node.py (systemd)
├── Hermes LLM API :8642           └── reads inbox:nodename
├── HTTP file server :8080         └── writes outbox:orchestrator
└── worker_macmini (LaunchAgent)
```

## Installation

### Prerequisites

- 1 central machine (Mac mini recommended) running Redis + Hermes Gateway
- 1+ remote nodes (Linux/Mac/WSL) on same LAN
- Python 3.8+ with `redis`, `requests`, `python-dotenv`

### Step 1: Mac Mini (Central Hub)

```bash
# Make Redis accessible across LAN
sudo sed -i.bak \
  -e 's/^bind 127.0.0.1 ::1$/bind 0.0.0.0/' \
  -e 's/^protected-mode yes$/protected-mode no/' \
  /opt/homebrew/etc/redis.conf
brew services restart redis

# Verify cross-device access
redis-cli ping  # PONG

# Install Python dependencies
pip3 install redis requests python-dotenv

# Clone repository
git clone https://github.com/seleman66eeddwegger3-art/hermes-agentmesh.git
cd hermes-agentmesh

# Create config directory
mkdir -p ~/.hermes/async_bus

# Configure environment
cp .env.example ~/.hermes/async_bus/.env_common
nano ~/.hermes/async_bus/.env_common
```

**Edit `.env_common`:**
```bash
REDIS_HOST=192.168.1.100  # Your Mac mini LAN IP
REDIS_PORT=6379
REDIS_DB=0
REDIS_PROTOCOL=2  # Critical: avoids redis-py 5.x RESP3 bugs

API_URL=http://192.168.1.100:8642/chat
API_KEY=your_hermes_api_key_from_~/.hermes/.env

# Node-specific (override per machine)
NODE_NAME=macmini
```

```bash
# Copy worker scripts
cp worker_node.py ~/.hermes/async_bus/
cp orchestrator_async.py ~/.hermes/async_bus/

# Install LaunchAgent for persistent worker
cp deploy/macos-launchd-worker.plist ~/Library/LaunchAgents/ai.hermes.async_bus_worker.plist
sed -i '' 's/<NODE_NAME>/macmini/g' ~/Library/LaunchAgents/ai.hermes.async_bus_worker.plist

# Start worker daemon
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.hermes.async_bus_worker.plist
launchctl kickstart gui/$UID/ai.hermes.async_bus_worker

# Verify worker is running
launchctl print gui/$UID/ai.hermes.async_bus_worker | grep state
# Expected: state = running

# Install file server for 0-SSH deployment
cp deploy/macos-launchd-serve.plist ~/Library/LaunchAgents/ai.hermes.async_bus_serve.plist
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.hermes.async_bus_serve.plist
```

### Step 2: Remote Nodes (Linux/WSL)

```bash
# On remote node (e.g. ubuntu@192.168.1.101)
mkdir -p ~/.hermes/async_bus ~/.config/systemd/user

# Pull files from Mac mini HTTP server (no SSH/SCP needed)
MAC_MINI_IP=192.168.1.100
curl -s http://$MAC_MINI_IP:8080/worker_node.py -o ~/.hermes/async_bus/worker_node.py
curl -s http://$MAC_MINI_IP:8080/orchestrator_async.py -o ~/.hermes/async_bus/orchestrator_async.py
curl -s http://$MAC_MINI_IP:8080/.env_common -o ~/.hermes/async_bus/.env_common

# Override NODE_NAME for this machine
echo "NODE_NAME=node99" >> ~/.hermes/async_bus/.env_common

# Install systemd unit
curl -s http://$MAC_MINI_IP:8080/deploy/linux-systemd-worker.service \
  -o ~/.config/systemd/user/async_bus_worker.service
sed -i 's/<NODE_NAME>/node99/g' ~/.config/systemd/user/async_bus_worker.service

# Enable persistent worker (survives logout)
systemctl --user daemon-reload
systemctl --user enable --now async_bus_worker

# Verify worker
systemctl --user status async_bus_worker
journalctl --user -u async_bus_worker -f
```

## Core Concepts

### Message Bus Protocol

**4-step async protocol:**
1. **Task push** — Orchestrator pushes to `inbox:<NODE_NAME>`
2. **Worker poll** — Node's worker daemon blocks on `BRPOP inbox:<NODE_NAME>`
3. **LLM execution** — Worker calls Hermes API with task payload
4. **Result return** — Worker pushes to `outbox:orchestrator`

**Task JSON format:**
```json
{
  "turn": 1,
  "node": "node99",
  "messages": [
    {"role": "system", "content": "You are agent 99 in a debate."},
    {"role": "user", "content": "What's your position on topic X?"}
  ]
}
```

### Mailbox Naming Convention

```python
inbox:<NODE_NAME>   # Where orchestrator sends tasks TO this node
outbox:orchestrator # Where all nodes send results BACK to orchestrator
```

## Key Usage Patterns

### Pattern 1: Run Multi-Agent Debate

```python
# orchestrator_async.py - edit configuration
TOPIC = "Should AI agents use async messaging over HTTP?"
MAX_TURNS = 3
NODES = ["macmini", "node99", "nodepi"]

# Run orchestrator (blocks until all turns complete)
cd ~/.hermes/async_bus
source .env_common
python3 orchestrator_async.py
```

**What happens:**
1. Orchestrator pushes tasks to `inbox:macmini`, `inbox:node99`, `inbox:nodepi`
2. Each node's worker daemon picks up task via `BRPOP`
3. Workers call Hermes LLM API (5-15 min per turn)
4. Workers push responses to `outbox:orchestrator`
5. Orchestrator collects results, starts next turn
6. Final report written to `async_debate_<timestamp>.md`

### Pattern 2: Custom Agent Integration

**For non-Hermes frameworks (LangGraph, AutoGen, etc.):**

```python
import redis
import json
import os

# Connect to shared Redis
r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=int(os.getenv("REDIS_DB")),
    protocol=2  # CRITICAL: avoid RESP3 bugs
)

# Listen for tasks (blocking)
def worker_loop(node_name):
    inbox = f"inbox:{node_name}"
    while True:
        # Block until task arrives
        _, task_raw = r.brpop(inbox, timeout=0)
        task = json.loads(task_raw)
        
        # Execute with your framework
        result = your_agent_framework.run(
            messages=task["messages"],
            context=task.get("context", {})
        )
        
        # Return result
        response = {
            "turn": task["turn"],
            "node": node_name,
            "response": result
        }
        r.lpush("outbox:orchestrator", json.dumps(response))
```

### Pattern 3: Push Task from Orchestrator

```python
import redis
import json
import os

r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=int(os.getenv("REDIS_DB")),
    protocol=2
)

def dispatch_task(node_name, turn, messages):
    task = {
        "turn": turn,
        "node": node_name,
        "messages": messages
    }
    inbox = f"inbox:{node_name}"
    r.lpush(inbox, json.dumps(task))
    print(f"✓ Pushed turn {turn} to {inbox}")

# Example usage
dispatch_task("node99", 1, [
    {"role": "system", "content": "You are a code reviewer."},
    {"role": "user", "content": "Review this function: def foo(): pass"}
])
```

### Pattern 4: Collect Results

```python
import redis
import json
import time

r = redis.Redis(host=os.getenv("REDIS_HOST"), protocol=2)

def collect_results(expected_count, timeout=600):
    results = []
    start = time.time()
    
    while len(results) < expected_count:
        remaining = timeout - (time.time() - start)
        if remaining <= 0:
            break
        
        # Block for result (max remaining time)
        item = r.brpop("outbox:orchestrator", timeout=int(remaining))
        if item:
            _, result_raw = item
            results.append(json.loads(result_raw))
    
    return results

# Collect 3 agent responses
responses = collect_results(3, timeout=900)
for resp in responses:
    print(f"{resp['node']}: {resp['response'][:100]}...")
```

## Configuration

### Environment Variables

**Required in `.env_common`:**

```bash
# Redis connection
REDIS_HOST=192.168.1.100      # Mac mini LAN IP
REDIS_PORT=6379
REDIS_DB=0
REDIS_PROTOCOL=2              # MUST be 2 (RESP2) not 3

# Hermes LLM API
API_URL=http://192.168.1.100:8642/chat
API_KEY=${HERMES_API_KEY}     # From ~/.hermes/.env

# Node identity (override per machine)
NODE_NAME=macmini             # Or node99, nodepi, etc.
```

### LaunchAgent Configuration (macOS)

**`~/Library/LaunchAgents/ai.hermes.async_bus_worker.plist`:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.hermes.async_bus_worker</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>source ~/.hermes/async_bus/.env_common && exec /usr/local/bin/python3 -u ~/.hermes/async_bus/worker_node.py</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/Users/youruser/.hermes/async_bus/worker_macmini.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/youruser/.hermes/async_bus/worker_macmini.err</string>
</dict>
</plist>
```

### Systemd Configuration (Linux)

**`~/.config/systemd/user/async_bus_worker.service`:**

```ini
[Unit]
Description=Hermes AgentMesh Worker (node99)
After=network.target

[Service]
Type=simple
WorkingDirectory=%h/.hermes/async_bus
EnvironmentFile=%h/.hermes/async_bus/.env_common
ExecStart=/usr/bin/python3 -u %h/.hermes/async_bus/worker_node.py
Restart=always
RestartSec=10

StandardOutput=append:%h/.hermes/async_bus/worker_node99.log
StandardError=append:%h/.hermes/async_bus/worker_node99.err

[Install]
WantedBy=default.target
```

## Troubleshooting

### Worker Not Starting

```bash
# macOS: Check LaunchAgent status
launchctl list | grep async_bus
launchctl print gui/$UID/ai.hermes.async_bus_worker

# Linux: Check systemd status
systemctl --user status async_bus_worker
journalctl --user -u async_bus_worker -n 50

# Common fix: Reload after config changes
launchctl bootout gui/$UID/ai.hermes.async_bus_worker
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.hermes.async_bus_worker.plist
```

### Redis Connection Refused

```bash
# Verify Redis is bound to 0.0.0.0
redis-cli CONFIG GET bind
# Expected: 0.0.0.0

# Test from remote node
redis-cli -h 192.168.1.100 ping
# Expected: PONG

# Fix: Edit redis.conf
sudo nano /opt/homebrew/etc/redis.conf
# Change: bind 127.0.0.1 → bind 0.0.0.0
# Change: protected-mode yes → protected-mode no
brew services restart redis
```

### RESP3 Protocol Errors

**Symptom:** `ResponseError: wrong number of arguments` or connection hangs

**Cause:** redis-py 5.x defaults to RESP3, which has bugs with certain commands

**Fix:**
```bash
# Force RESP2 in .env_common
echo "REDIS_PROTOCOL=2" >> ~/.hermes/async_bus/.env_common

# Update worker code
sed -i 's/protocol=3/protocol=2/g' ~/.hermes/async_bus/worker_node.py
```

### Tasks Stuck in Queue

```bash
# Check queue lengths
redis-cli LLEN inbox:macmini
redis-cli LLEN inbox:node99
redis-cli LLEN outbox:orchestrator

# Inspect stuck task
redis-cli LINDEX inbox:node99 0

# Flush queue if corrupted
redis-cli DEL inbox:node99

# Restart worker
systemctl --user restart async_bus_worker
```

### Long Task Timeout (HTTP API)

**Not a bug** — AgentMesh is designed for 15-min+ tasks. If Hermes API itself times out:

```python
# worker_node.py — increase API timeout
response = requests.post(
    API_URL,
    json=payload,
    headers={"X-API-Key": API_KEY},
    timeout=1800  # 30 minutes
)
```

### Worker Stops After SSH Logout (Linux)

**Cause:** systemd user services stop when session ends

**Fix:** Enable lingering
```bash
sudo loginctl enable-linger $USER

# Verify
loginctl show-user $USER | grep Linger
# Expected: Linger=yes
```

### File Server 404 (Cross-Device Deploy)

```bash
# Verify HTTP server is running on Mac mini
launchctl list | grep serve
curl http://localhost:8080/worker_node.py

# Restart server
launchctl kickstart gui/$UID/ai.hermes.async_bus_serve

# Check firewall (macOS)
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
```

## Advanced Patterns

### Custom Timeout Per Task

```python
# orchestrator_async.py — add timeout metadata
task = {
    "turn": 1,
    "node": "node99",
    "timeout": 600,  # Custom 10-min timeout
    "messages": [...]
}
r.lpush("inbox:node99", json.dumps(task))
```

```python
# worker_node.py — respect timeout
task = json.loads(task_raw)
timeout = task.get("timeout", 1800)
response = requests.post(API_URL, json=payload, timeout=timeout)
```

### Multi-Round Deliberation

```python
# orchestrator pattern for N-round debate
for turn in range(1, MAX_TURNS + 1):
    # Dispatch to all nodes
    for node in NODES:
        dispatch_task(node, turn, build_messages(turn, history))
    
    # Collect all responses
    results = collect_results(len(NODES), timeout=1800)
    
    # Aggregate into history for next round
    history.extend(results)
    write_checkpoint(turn, results)
```

### Priority Queues

```python
# Use separate queues for priority
r.lpush("inbox:node99:high", json.dumps(urgent_task))
r.lpush("inbox:node99:low", json.dumps(batch_task))

# Worker polls high-priority first
while True:
    item = r.brpop(["inbox:node99:high", "inbox:node99:low"], timeout=0)
    _, task_raw = item
    process(task_raw)
```

### Health Monitoring

```python
# Heartbeat pattern
def worker_with_heartbeat(node_name):
    while True:
        r.setex(f"heartbeat:{node_name}", 60, "alive")
        
        item = r.brpop(f"inbox:{node_name}", timeout=30)
        if item:
            _, task = item
            process(task)

# Orchestrator checks health
def check_node_alive(node_name):
    return r.exists(f"heartbeat:{node_name}") == 1
```

## Performance Notes

- **Latency:** Redis BRPOP typically <1ms on LAN
- **Throughput:** 1000+ tasks/sec with pipelining
- **Durability:** Redis AOF persistence recommended for critical tasks
- **Scalability:** Tested with 5 nodes, 50+ concurrent tasks

## Further Reading

- [Full deployment guide](https://github.com/seleman66eeddwegger3-art/hermes-agentmesh/blob/main/docs/plan-b-naming-governance.md)
- [Real-world case study](https://test-github-repo.vercel.app/detail.html?id=cross-device-async-bus-99-operator-manual-2026-06-09)
- [Redis RESP2 vs RESP3 pitfalls](https://github.com/redis/redis-py/issues/2715)
