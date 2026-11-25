title: Orchestrator Agent Skill
description: Create strategic swarm manager that uses agent rotation (Monitor, Admin, Validation, Notification) to optimize parallel execution and handle complex situations

## Context

Tasks 1-10 have created a complete orchestration, monitoring, and swarm management system. Now we need an Orchestrator Agent that strategically manages the entire swarm by rotating between specialized agents based on current situation and needs.

## Objectives

Create orchestrator agent with strategic swarm management:

1. **orchestrator-agent.sh script** - Strategic agent rotation system
2. **Agent rotation logic** - Switch between Monitor, Admin, Validation, Notification agents
3. **Swarm health analysis** - Detect situations and choose appropriate agent
4. **Parallelism optimization** - Identify and enable parallel execution opportunities
5. **Skill documentation** - Orchestrator agent usage guide

## Success Criteria

- [ ] orchestrator-agent.sh created with all functions
- [ ] Agent rotation working (4 agent types)
- [ ] Swarm health analysis operational
- [ ] Situation detection implemented
- [ ] Parallelism optimization functional
- [ ] State management with JSON
- [ ] Skill documentation complete
- [ ] Integration with all agents (Monitor, Admin, Validation, Notification)
- [ ] All functions exported

## Implementation Details

### 1. orchestrator-agent.sh Script

**Location**: `.agents/scripts/utils/orchestrator-agent.sh`

**Functions to implement**:

1. **init_orchestrator()** - Initialize orchestrator state
   - Create JSON state file: /tmp/orchestrator-state.json
   - Track current agent, swarm sessions, rotation time
   - Initialize metrics

2. **decide_agent()** - Choose agent based on situation
   - Input: situation (normal, blocked, validation_needed, emergency)
   - Output: agent name (monitor, admin, validation, notification)
   - Logic: Map situations to appropriate agents

3. **switch_agent()** - Switch to different agent
   - Activate new agent
   - Update state file
   - Log agent rotation
   - Track rotation time

4. **analyze_swarm()** - Analyze swarm health
   - Count sessions by status (pending, active, blocked, completed, failed)
   - Detect blockages (1 blocked = warning, 2+ = emergency)
   - Detect completion (all active done = validation needed)
   - Return situation assessment

5. **optimize_parallelism()** - Find parallelization opportunities
   - Find pending sessions with dependencies
   - Check if dependencies are met
   - Send start signals to ready sessions
   - Enable parallel execution

6. **orchestrate()** - Main orchestration loop
   - Initialize orchestrator
   - Continuous loop: analyze → decide → switch → execute
   - 10-second cycle
   - Agent-specific actions per cycle

**Script Structure**:

```bash
#!/bin/bash
# orchestrator-agent.sh - Strategic swarm orchestration

set -euo pipefail

ORCHESTRATOR_STATE="/tmp/orchestrator-state.json"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source required agents
source "${SCRIPT_DIR}/orchestration-agent.sh"  # Monitor Agent (Task 2)
source "${SCRIPT_DIR}/admin-agent.sh"          # Admin Agent (Task 10)
source "${SCRIPT_DIR}/orchestration.sh"        # Notification Agent (Task 5)
# Validation Agent would be here (future implementation)

# Initialize orchestrator
init_orchestrator() {
  cat > "$ORCHESTRATOR_STATE" <<EOF
{
  "current_agent": "monitor",
  "swarm_sessions": [],
  "last_rotation": $(date +%s),
  "intervention_count": 0,
  "optimization_score": 100
}
EOF

  echo "🎯 Orchestrator initialized"
}

# [Implement all 6 functions]

# Export functions
export -f init_orchestrator decide_agent switch_agent
export -f analyze_swarm optimize_parallelism orchestrate
```

### 2. Agent Rotation System

**Four Agent Modes**:

1. **Monitor Mode** (default)
   - Uses orchestration-agent.sh from Task 2
   - Continuous surveillance
   - Metric collection
   - Status tracking
   - Dashboard updates

2. **Admin Mode** (emergency/blocked)
   - Uses admin-agent.sh from Task 10
   - Unblock stuck sessions
   - Force interventions
   - Emergency cleanup
   - System audit

3. **Validation Mode** (completion check)
   - Quality checks
   - Progress validation
   - Completion verification
   - Test result analysis

4. **Notification Mode** (active communication)
   - Uses orchestration.sh from Task 5
   - Broadcast updates
   - Status reports
   - Alert management
   - Multi-session messaging

**Rotation Logic**:

```bash
decide_agent() {
  local situation=$1

  case $situation in
    blocked)
      echo "admin"      # 1 blockage = admin intervention
      ;;
    emergency)
      echo "admin"      # 2+ blockages = emergency
      ;;
    validation_needed)
      echo "validation" # All done = validate
      ;;
    normal)
      echo "monitor"    # Default = monitor
      ;;
  esac
}
```

### 3. Swarm Health Analysis

**Situation Detection**:

```bash
analyze_swarm() {
  echo "📊 Analyzing swarm health..."

  local total_sessions=$(tmux ls 2>/dev/null | wc -l)
  local blocked=0
  local active=0
  local completed=0

  # Count sessions by status
  find /tmp/tmux-sessions-metadata/ -name "*.info" | while read meta; do
    source "$meta"
    case $status in
      blocked) blocked=$((blocked + 1)) ;;
      active|in_progress) active=$((active + 1)) ;;
      completed) completed=$((completed + 1)) ;;
    esac
  done

  # Detect situation
  if [ $blocked -gt 2 ]; then
    echo "🚨 Multiple blockages detected: $blocked"
    echo "emergency"
  elif [ $blocked -gt 0 ]; then
    echo "⚠️  Blockage detected: $blocked"
    echo "blocked"
  elif [ $active -eq 0 ] && [ $completed -gt 0 ]; then
    echo "✅ All tasks complete, validation needed"
    echo "validation_needed"
  else
    echo "✓ Normal operation"
    echo "normal"
  fi
}
```

**Health Metrics**:
- Total sessions
- Blocked count (triggers admin)
- Active count (monitors progress)
- Completed count (triggers validation)
- Failed count (triggers admin)

### 4. Parallelism Optimization

**Dependency Resolution**:

```bash
optimize_parallelism() {
  echo "⚡ Analyzing parallelization opportunities..."

  # Find pending sessions
  local sessions=$(find /tmp/tmux-sessions-metadata/ -name "*.info" \
    -exec grep -l "^status=pending$" {} \; | xargs -I {} basename {} .info)

  for session in $sessions; do
    local meta="/tmp/tmux-sessions-metadata/${session}.info"
    source "$meta"

    # Check if dependencies are met
    local can_start=true
    if [ -n "$dependencies" ]; then
      for dep in ${dependencies//,/ }; do
        local dep_meta="/tmp/tmux-sessions-metadata/${dep}.info"
        if [ -f "$dep_meta" ]; then
          source "$dep_meta"
          if [ "$status" != "completed" ]; then
            can_start=false
            break
          fi
        fi
      done
    fi

    # Send start signal if ready
    if [ "$can_start" = "true" ]; then
      echo "  🚀 Can start in parallel: ${session}"
      ./tmux-claude-helper.sh send "$session" \
        "🚀 [ORCHESTRATOR] Dependencies met - you can start"
    fi
  done
}
```

**Parallelism Features**:
- Dependency checking
- Automatic start signals
- Parallel execution enablement
- Bottleneck detection

### 5. Orchestrator Agent Skill Documentation

**Location**: `.claude/skills/orchestrator-agent/skill.md`

**Sections to include**:

1. **Introduction** - Strategic swarm manager
2. **Capabilities** - What orchestrator can do
3. **Agent Rotation** - 4 agent modes explained
4. **When to Use** - Complex multi-session orchestration
5. **Usage Examples** - How to activate and use
6. **Integration** - With all other agents
7. **State Management** - JSON state tracking

**Structure**:

```markdown
# Orchestrator Agent Skill

Strategic swarm manager that uses other agents in rotation.

## Capabilities

- Monitors using Monitor Agent (Task 2)
- Escalates to Admin Agent when needed (Task 10)
- Validates with Validation Agent
- Communicates via Notification Agent (Task 5)
- Optimizes parallelism
- Detects bottlenecks
- Rebalances workload

## Agent Rotation

### 1. Monitor Mode (default)
- Continuous surveillance
- Metric collection
- Status tracking

### 2. Admin Mode (when needed)
- Unblock stuck sessions
- Force interventions
- Emergency actions

### 3. Validation Mode (periodic)
- Quality checks
- Progress validation
- Completion verification

### 4. Notification Mode (active)
- Broadcast updates
- Status reports
- Alert management

## Usage

```bash
# Activate orchestrator
source .agents/scripts/utils/orchestrator-agent.sh

# Initialize
init_orchestrator

# Start orchestration loop
orchestrate
```

## Situation Handling

- **normal**: Monitor agent (default)
- **blocked**: Admin agent (1 blockage)
- **emergency**: Admin agent (2+ blockages)
- **validation_needed**: Validation agent (all complete)

## State Management

State tracked in: `/tmp/orchestrator-state.json`

```json
{
  "current_agent": "monitor",
  "swarm_sessions": [],
  "last_rotation": 1234567890,
  "intervention_count": 0,
  "optimization_score": 100
}
```

## Integration

Uses all agents:
- orchestration-agent.sh (Task 2)
- admin-agent.sh (Task 10)
- orchestration.sh (Task 5)
- validation-agent.sh (future)
```

### 6. Validation Plan

**Function testing**:

```bash
# Test init_orchestrator
source .agents/scripts/utils/orchestrator-agent.sh
init_orchestrator
cat /tmp/orchestrator-state.json
# Should show JSON with current_agent=monitor

# Test decide_agent
decide_agent "normal"     # Should output: monitor
decide_agent "blocked"    # Should output: admin
decide_agent "emergency"  # Should output: admin
decide_agent "validation_needed"  # Should output: validation

# Test analyze_swarm
analyze_swarm
# Should output situation assessment

# Test switch_agent (would need agent files)
# switch_agent "admin" "blocked"

# Test orchestrate (background)
# orchestrate &
# Should run continuously
```

## Deliverables

1. `.agents/scripts/utils/orchestrator-agent.sh` (orchestrator functions)
2. `.claude/skills/orchestrator-agent/skill.md` (skill documentation)
3. All functions tested and working
4. Agent rotation validated
5. State management functional
6. Integration with all agents confirmed

## Validation Checklist

### Script Quality
- [ ] All 6 functions implemented
- [ ] Agent rotation logic working
- [ ] State management with JSON
- [ ] All functions exported
- [ ] Error handling robust

### Functionality
- [ ] init_orchestrator creates state file
- [ ] decide_agent maps situations correctly
- [ ] switch_agent updates state
- [ ] analyze_swarm detects situations
- [ ] optimize_parallelism finds opportunities
- [ ] orchestrate runs continuous loop

### Documentation
- [ ] Skill.md complete
- [ ] Agent rotation explained
- [ ] Usage examples clear
- [ ] Integration documented
- [ ] State format defined

## Integration Points

- **orchestration-agent.sh** (Task 2) - Monitor Agent
- **admin-agent.sh** (Task 10) - Admin Agent
- **orchestration.sh** (Task 5) - Notification Agent
- **swarm-manager.sh** (Task 9) - Swarm hierarchy
- **session-communication.sh** (Task 1) - Metadata system
- **Task 12** (Multi-Channel Comm) - Will use orchestrator coordination

## Quality Standards

- Strategic decision making based on situation
- Automatic agent switching
- Continuous optimization
- State persistence
- Professional error handling

## Expected Impact

- **Strategic Management**: Intelligent agent selection based on needs
- **Automatic Escalation**: Admin agent when blockages occur
- **Parallelism**: Automatic dependency resolution
- **Validation**: Quality checks when work completes
- **Efficiency**: Right agent for the right situation

## Notes

- Orchestrator is the top-level strategic manager
- Uses all other agents as specialized tools
- Continuous loop with 10-second cycles
- State persisted in JSON for reliability
- Agent rotation based on real-time situation analysis
