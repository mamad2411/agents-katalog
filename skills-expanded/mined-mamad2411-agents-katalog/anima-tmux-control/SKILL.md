# /anima-tmux-control — Remote Control Claude Agents in tmux

**Purpose:** Launch, monitor, and send messages to Claude agents running in tmux sessions on the GPU server.

---

## LAUNCH an agent with a prompt

```bash
# Write prompt to file
ssh datai_srv7_development "cat > /tmp/prompt_{MODULE}.txt << 'PROMPT'
{full prompt here}
PROMPT"

# Start tmux + claude with the prompt
ssh datai_srv7_development "tmux new-session -d -s {MODULE} -c /mnt/forge-data/modules/project_{module} 'claude --dangerously-skip-permissions -p \"\$(cat /tmp/prompt_{MODULE}.txt)\"'"
```

## SEND a message to a running agent

```bash
# The agent must be running claude in the tmux session
# Send keystrokes to its stdin
ssh datai_srv7_development "tmux send-keys -t {MODULE} 'your message here' Enter"
```

## READ agent output

```bash
# Capture last N lines from the tmux pane
ssh datai_srv7_development "tmux capture-pane -t {MODULE} -p -S -50"
```

## CHECK if agent is still working

```bash
ssh datai_srv7_development "tmux capture-pane -t {MODULE} -p | tail -5"
```

## KILL an agent

```bash
ssh datai_srv7_development "tmux kill-session -t {MODULE}"
```

## LAUNCH 2 AGENTS IN PARALLEL (split GPUs)

```bash
# Agent 1: GPUs 0-3
ssh datai_srv7_development "cat > /tmp/prompt_A.txt << 'PROMPT'
export CUDA_VISIBLE_DEVICES=0,1,2,3
{prompt A}
PROMPT
tmux new-session -d -s MODULE_A -c /mnt/forge-data/modules/project_a 'claude --dangerously-skip-permissions -p \"\$(cat /tmp/prompt_A.txt)\"'"

# Agent 2: GPUs 4-7
ssh datai_srv7_development "cat > /tmp/prompt_B.txt << 'PROMPT'
export CUDA_VISIBLE_DEVICES=4,5,6,7
{prompt B}
PROMPT
tmux new-session -d -s MODULE_B -c /mnt/forge-data/modules/project_b 'claude --dangerously-skip-permissions -p \"\$(cat /tmp/prompt_B.txt)\"'"
```

## FORCE INTERRUPT + MESSAGE (most important pattern)

When an agent is stuck, sleeping, or doing the wrong thing:
```bash
# 1. Esc interrupts current tool call immediately
# 2. Wait for agent to process the interrupt
# 3. Send the message
# 4. Enter to submit
ssh datai_srv7_development "tmux send-keys -t {MODULE} Escape; sleep 2; tmux send-keys -t {MODULE} 'your urgent message here' Enter"
```

## FORCE INTO PLAN MODE (when agent is lost)

If the agent is going in circles or stuck, force it to stop and plan:
```bash
# Esc → /plan → forces the agent to think before acting
ssh datai_srv7_development "tmux send-keys -t {MODULE} Escape; sleep 2; tmux send-keys -t {MODULE} '/plan fix the issue — describe what is wrong and what needs to happen' Enter"
```
After the agent outputs a plan, accept it so it executes:
```bash
ssh datai_srv7_development "tmux send-keys -t {MODULE} 'yes, execute this plan' Enter"
```

## NUDGE PATTERNS

```bash
# Status check (gentle)
ssh datai_srv7_development "tmux send-keys -t {MODULE} 'status update — what step are you on?' Enter"

# Training crash recovery (urgent — use Esc)
ssh datai_srv7_development "tmux send-keys -t {MODULE} Escape; sleep 2; tmux send-keys -t {MODULE} 'Training crashed. Check the log, fix the issue, restart with nohup+disown.' Enter"

# GPU reassignment (when another agent frees GPUs)
ssh datai_srv7_development "tmux send-keys -t {MODULE} Escape; sleep 2; tmux send-keys -t {MODULE} 'GPUs X,Y,Z,W are now free. Use them.' Enter"

# Force plan when stuck
ssh datai_srv7_development "tmux send-keys -t {MODULE} Escape; sleep 2; tmux send-keys -t {MODULE} '/plan figure out why training is not progressing and fix it' Enter"
```

## MONITOR ALL AGENTS

```bash
# Quick status of all running agents
ssh datai_srv7_development "for s in \$(tmux list-sessions -F '#S'); do echo \"=== \$s ===\"; tmux capture-pane -t \$s -p | tail -3; echo; done"

# Check actual GPU usage (are they really training?)
ssh datai_srv7_development "nvidia-smi --query-compute-apps=pid,name,used_memory --format=csv,noheader"

# Check training logs are progressing
ssh datai_srv7_development "for m in cornucopia frigg; do latest=\$(ls -t /mnt/artifacts-datai/logs/project_\$m/*.log 2>/dev/null | head -1); echo \"=== \$m ===\"; [ -n \"\$latest\" ] && tail -2 \"\$latest\" || echo 'NO LOG'; done"

# Full watcher check
ssh datai_srv7_development "echo '=== GPUs ==='; nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader; echo '=== DISK ==='; df -h /mnt/artifacts-datai /mnt/forge-data /dev/root | tail -3; echo '=== TMUX ==='; tmux list-sessions"
```

## KEY RULES

1. **Always Esc before urgent messages** — interrupts whatever tool the agent is running
2. **Use /plan when agent is lost** — forces structured thinking before action
3. **Check GPU processes, not just tmux output** — agent may show "thinking" but training actually crashed
4. **Check training logs directly** — `tail -5 /mnt/artifacts-datai/logs/project_{module}/*.log`
5. **Disk >90% = alert user immediately** — training will crash if disk fills
6. **Both agents idle GPUs = something crashed** — investigate and nudge
