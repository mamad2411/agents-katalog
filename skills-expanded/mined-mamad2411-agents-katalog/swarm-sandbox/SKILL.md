---
name: "swarm-sandbox"
description: "Safe isolated testing environment for multi-agent swarm topologies before production deployment"
---

# Swarm Sandbox Simulator

## When to activate
- Before deploying multi-agent swarms with council.js to production
- Testing agent interaction patterns, message flows, and error handling
- Validating swarm topology configurations (2-agent, 5-agent, council-style)
- Experimenting with new agent communication protocols
- Sandboxing edge cases and failure scenarios in isolated environments
- Validating safety guardrails and rate limits before live deployment

## When NOT to use
- Single-agent operations without inter-agent communication
- Production deployments — use this for testing only, then migrate to live
- Simple sequential agent pipelines — standard agent-construction skill is sufficient
- One-off quick experiments without formal validation needs
- Legacy monolithic systems without agent-based architecture

## Instructions

### Core concept
Swarm Sandbox creates an isolated, dry-run environment for testing multi-agent topologies. It validates:
1. **Topology structure** — agent count, relationships, message flow
2. **Communication paths** — request routing, response handling, cycles
3. **Safety guardrails** — rate limits, timeout handling, resource isolation
4. **Error propagation** — failure modes, recovery strategies, circuit breakers
5. **Integration readiness** — environment compatibility before production

### Sandbox topology templates

#### 2-Agent Pair (Simple Request-Response)
```javascript
// Mock environment for bilateral agent communication
const sandbox2Agent = {
  agents: [
    {
      id: "agent-primary",
      role: "orchestrator",
      model: "claude-opus-4-20250514",
      capabilities: ["task_decomposition", "delegation", "synthesis"],
      timeout_ms: 30000,
      rate_limit: { requests_per_minute: 60 }
    },
    {
      id: "agent-specialist",
      role: "specialist",
      model: "claude-opus-4-20250514",
      capabilities: ["analysis", "execution"],
      timeout_ms: 30000,
      rate_limit: { requests_per_minute: 120 }
    }
  ],
  communication: {
    topology: "bilateral",
    message_protocol: "json-rpc",
    max_queue_depth: 1000,
    retry_policy: {
      max_attempts: 3,
      backoff_ms: [100, 250, 500],
      circuit_breaker: { threshold: 5, reset_ms: 60000 }
    }
  },
  isolation: {
    context_isolation: true,
    memory_limit_mb: 512,
    cpu_quota_percent: 50,
    network_restricted: true
  },
  monitoring: {
    log_level: "debug",
    trace_enabled: true,
    metrics: ["latency_ms", "error_rate", "queue_depth", "token_usage"]
  }
};

// Mock simulation environment
const mock2AgentEnv = {
  // Agent-primary sends task to agent-specialist
  scenario_1: {
    name: "Standard delegation",
    steps: [
      {
        actor: "agent-primary",
        action: "message",
        target: "agent-specialist",
        payload: {
          type: "task",
          id: "task-001",
          instruction: "Analyze market sentiment for tech stocks",
          context: { data_url: "mock://data/sentiment.json" }
        },
        expected_latency_ms: [500, 3000]
      },
      {
        actor: "agent-specialist",
        action: "response",
        target: "agent-primary",
        payload: {
          task_id: "task-001",
          status: "completed",
          result: { sentiment_score: 0.72, confidence: 0.94 }
        },
        expected_latency_ms: [300, 2000]
      }
    ]
  },
  
  // Failure mode: specialist timeout
  scenario_2: {
    name: "Timeout recovery",
    steps: [
      {
        actor: "agent-primary",
        action: "message",
        target: "agent-specialist",
        payload: {
          type: "task",
          id: "task-002",
          instruction: "Process large dataset",
          timeout_override_ms: 5000
        }
      },
      {
        actor: "agent-specialist",
        action: "timeout",
        duration_ms: 6000,
        expected_behavior: "circuit_breaker_activates"
      },
      {
        actor: "agent-primary",
        action: "retry_with_backoff",
        target: "agent-specialist",
        backoff_attempt: 1,
        delay_ms: 100
      }
    ]
  },
  
  // Failure mode: resource exhaustion
  scenario_3: {
    name: "Rate limit enforcement",
    steps: [
      {
        actor: "agent-primary",
        action: "burst_messages",
        count: 150,
        target: "agent-specialist",
        rate_limit_quota: 120
      },
      {
        actor: "sandbox",
        action: "enforce_limit",
        expected_behavior: "reject_excess_requests",
        rejected_count: 30
      }
    ]
  }
};
```

#### 5-Agent Council (Hub-and-Spoke)
```javascript
// Council topology with central orchestrator
const sandbox5AgentCouncil = {
  agents: [
    {
      id: "council-orchestrator",
      role: "orchestrator",
      model: "claude-opus-4-20250514",
      responsibilities: ["task_routing", "synthesis", "final_decision"]
    },
    {
      id: "researcher-agent",
      role: "researcher",
      model: "claude-opus-4-20250514",
      responsibilities: ["data_gathering", "fact_checking", "source_validation"]
    },
    {
      id: "analyst-agent",
      role: "analyst",
      model: "claude-opus-4-20250514",
      responsibilities: ["pattern_detection", "trend_analysis", "anomaly_detection"]
    },
    {
      id: "risk-agent",
      role: "risk_assessor",
      model: "claude-opus-4-20250514",
      responsibilities: ["risk_evaluation", "mitigation_planning", "compliance_check"]
    },
    {
      id: "writer-agent",
      role: "writer",
      model: "claude-opus-4-20250514",
      responsibilities: ["report_generation", "communication_formatting", "audience_adaptation"]
    }
  ],
  topology: {
    pattern: "hub-and-spoke",
    hub: "council-orchestrator",
    spokes: ["researcher-agent", "analyst-agent", "risk-agent", "writer-agent"],
    broadcast_enabled: false,
    direct_peer_communication: false
  },
  coordination: {
    phase_1: {
      name: "parallel_research",
      duration_target_ms: 5000,
      participants: ["researcher-agent"],
      synchronization: "gather_all_results"
    },
    phase_2: {
      name: "parallel_analysis",
      duration_target_ms: 3000,
      participants: ["analyst-agent"],
      depends_on: ["phase_1"]
    },
    phase_3: {
      name: "risk_assessment",
      duration_target_ms: 2000,
      participants: ["risk-agent"],
      depends_on: ["phase_1", "phase_2"]
    },
    phase_4: {
      name: "synthesis_and_write",
      duration_target_ms: 2000,
      participants: ["writer-agent"],
      depends_on: ["phase_2", "phase_3"]
    }
  },
  validation_checkpoints: {
    after_phase_1: { check: "validate_data_quality", failure_action: "retry" },
    after_phase_2: { check: "validate_analysis_completeness", failure_action: "retry" },
    after_phase_3: { check: "validate_risk_coverage", failure_action: "escalate" },
    after_phase_4: { check: "validate_output_format", failure_action: "reject" }
  }
};

// Dry-run scenarios for 5-agent council
const mock5AgentScenarios = {
  scenario_healthy: {
    name: "All agents operational",
    expected_flow: [
      "orchestrator → researcher",
      "orchestrator → analyst",
      "orchestrator → risk",
      "researcher → orchestrator (complete)",
      "analyst → orchestrator (complete)",
      "risk → orchestrator (complete)",
      "orchestrator → writer",
      "writer → orchestrator (complete)",
      "orchestrator → user"
    ],
    expected_time_ms: 12000,
    expected_status: "success"
  },
  
  scenario_one_agent_slow: {
    name: "Analyst agent slow response",
    delays: { "analyst-agent": 8000 },
    expected_behavior: "orchestrator_waits_then_retries",
    expected_time_ms: 15000,
    expected_status: "degraded_success"
  },
  
  scenario_one_agent_failed: {
    name: "Risk agent unreachable",
    failures: { "risk-agent": "connection_timeout" },
    expected_behavior: "orchestrator_detects_failure_and_branches_to_fallback",
    fallback_path: "skip_phase_3_warn_in_output",
    expected_status: "partial_success"
  },
  
  scenario_orchestrator_overload: {
    name: "Orchestrator under message load",
    concurrent_tasks: 25,
    queue_depth: 500,
    expected_behavior: "enforce_rate_limits_and_queue_backpressure",
    expected_rejected_tasks: 5,
    expected_status: "rate_limited"
  }
};
```

#### Council-Style (Peer Collaboration with Router)
```javascript
// Peer-to-peer with central message router
const sandboxPeerCouncil = {
  agents: [
    {
      id: "peer-1-sdr",
      role: "sales_development",
      model: "claude-opus-4-20250514",
      peer_topics: ["lead_qualification", "outreach_strategy"]
    },
    {
      id: "peer-2-marketing",
      role: "marketing_specialist",
      model: "claude-opus-4-20250514",
      peer_topics: ["campaign_analysis", "content_strategy"]
    },
    {
      id: "peer-3-product",
      role: "product_owner",
      model: "claude-opus-4-20250514",
      peer_topics: ["feature_analysis", "roadmap_planning"]
    }
  ],
  router: {
    type: "message_router",
    routing_rules: [
      { topic: "lead_qualification", route_to: "peer-1-sdr" },
      { topic: "campaign_analysis", route_to: "peer-2-marketing" },
      { topic: "feature_analysis", route_to: "peer-3-product" },
      { topic: "cross_functional_review", route_to: "all" }
    ],
    message_queue: { max_size: 5000, ttl_ms: 300000 },
    deduplication: true
  },
  peer_communication: {
    allowed_patterns: [
      { from: "peer-1-sdr", to: "peer-2-marketing", topic: "lead_context" },
      { from: "peer-2-marketing", to: "peer-3-product", topic: "feature_request" },
      { from: "peer-3-product", to: "peer-1-sdr", topic: "capability_update" }
    ],
    cycle_detection: {
      enabled: true,
      max_hops: 4,
      detection_action: "break_cycle"
    }
  }
};
```

### Mock environment variables and dry-run flags

```bash
# Sandbox configuration file: .swarm-sandbox.env
SWARM_MODE=sandbox
SANDBOX_ISOLATION_LEVEL=strict          # strict | moderate | permissive
SANDBOX_NETWORK_ACCESS=none             # none | local_only | restricted_urls
SANDBOX_TIMEOUT_OVERRIDE_MS=10000       # Override all agent timeouts for testing
SANDBOX_RATE_LIMIT_MULTIPLIER=0.5       # Reduce rate limits for stress testing

# Model configuration
SANDBOX_MODEL_PRIMARY=claude-opus-4-20250514
SANDBOX_MODEL_FALLBACK=claude-sonnet-4-20250514
SANDBOX_TOKEN_LIMIT_OVERRIDE=50000      # Dry-run token budget

# Failure injection (chaos engineering)
SANDBOX_INJECT_FAILURES=false           # Enable chaos mode
SANDBOX_FAILURE_RATE_PERCENT=10         # Random failure injection rate
SANDBOX_FAILURE_MODES=timeout,malformed_response,no_route  # Which failures to inject

# Monitoring and validation
SANDBOX_TRACE_ENABLED=true
SANDBOX_VALIDATE_SCHEMA=true
SANDBOX_COLLECT_METRICS=true
SANDBOX_METRICS_OUTPUT=./sandbox-metrics.json

# Safety guardrails
SANDBOX_MAX_CONCURRENT_AGENTS=10
SANDBOX_MAX_MESSAGE_SIZE_BYTES=1048576  # 1MB
SANDBOX_MAX_TOTAL_REQUESTS_PER_RUN=5000
SANDBOX_CIRCUIT_BREAKER_THRESHOLD=5
SANDBOX_CIRCUIT_BREAKER_RESET_MS=60000
```

### Isolation validation checklist

```markdown
## Pre-Deployment Validation Checklist

### Topology & Structure
- [ ] All agent IDs are unique and non-conflicting
- [ ] Agent role assignments align with responsibilities
- [ ] Communication topology matches documented design (hub-spoke, peer, linear)
- [ ] No circular dependencies in phase sequencing (if applicable)
- [ ] All agents have reachable endpoints in sandbox mock

### Communication & Messaging
- [ ] Message protocol defined and validated (JSON-RPC, gRPC, etc.)
- [ ] Serialization/deserialization tested for all message types
- [ ] Maximum message size limits enforced
- [ ] Routing rules tested for all agent pairs
- [ ] Cycle detection working for peer-to-peer topologies
- [ ] Message queuing and backpressure mechanisms validated

### Safety & Guardrails
- [ ] Rate limits enforced per agent and globally
- [ ] Timeout handling tested (graceful degradation vs. failure)
- [ ] Circuit breakers activate after N consecutive failures
- [ ] Memory isolation per agent sandboxed
- [ ] Resource limits (CPU, memory, token budget) enforced
- [ ] Network access restricted to mock endpoints only

### Error Handling & Recovery
- [ ] Retry logic tested with backoff (exponential, jitter)
- [ ] Fallback paths exist and are validated for critical failures
- [ ] Partial failure scenarios handled (e.g., 1 of 5 agents fails)
- [ ] Error messages logged with sufficient context
- [ ] No sensitive data in error outputs

### Performance & Scale
- [ ] Baseline latency measured for each agent
- [ ] Load test: validate behavior at 2x expected concurrent tasks
- [ ] Load test: validate behavior at 5x expected message rate
- [ ] Queue depth remains within limits under stress
- [ ] No memory leaks observed in extended runs

### Integration Readiness
- [ ] All external dependencies mocked (APIs, databases, file systems)
- [ ] Production environment variables documented
- [ ] Secrets management (API keys, auth tokens) not embedded in configs
- [ ] Agent discovery mechanism (if dynamic) tested in sandbox
- [ ] Graceful shutdown sequence verified

### Compliance & Audit
- [ ] All agent actions logged for audit trail
- [ ] Sensitive data (user IDs, PII) masked in logs
- [ ] Audit retention policy defined and enforced
- [ ] Compliance violations detected and reported
- [ ] Sandbox run reports generated automatically
```

### Safety guardrails and validation steps

#### Built-in safety mechanisms
```python
# Safety validator for sandbox configurations
class SwarmSandboxValidator:
    """Validate swarm topology before deployment."""
    
    def __init__(self, topology_config: dict):
        self.config = topology_config
        self.errors = []
        self.warnings = []
    
    def validate_all(self) -> bool:
        """Run all validation checks."""
        self.validate_topology_structure()
        self.validate_communication_graph()
        self.validate_resource_limits()
        self.validate_safety_guardrails()
        self.validate_error_handling()
        return len(self.errors) == 0
    
    def validate_topology_structure(self):
        """Verify agent IDs are unique, roles defined, etc."""
        agent_ids = set()
        for agent in self.config.get("agents", []):
            if agent["id"] in agent_ids:
                self.errors.append(f"Duplicate agent ID: {agent['id']}")
            agent_ids.add(agent["id"])
            
            if not agent.get("role"):
                self.errors.append(f"Agent {agent['id']} missing role")
            if not agent.get("model"):
                self.warnings.append(f"Agent {agent['id']} using default model")
    
    def validate_communication_graph(self):
        """Check for cycles, unreachable agents, malformed routes."""
        agents_map = {a["id"]: a for a in self.config.get("agents", [])}
        
        # Cycle detection (DFS)
        visited = set()
        rec_stack = set()
        
        def has_cycle(node, graph):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor, graph):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        # Build adjacency list from topology
        graph = {}
        for agent_id in agents_map:
            graph[agent_id] = []
        
        # Add edges based on communication rules
        for rule in self.config.get("communication", {}).get("allowed_patterns", []):
            from_agent = rule.get("from")
            to_agent = rule.get("to")
            if from_agent in graph and to_agent in agents_map:
                graph[from_agent].append(to_agent)
        
        for agent_id in graph:
            if agent_id not in visited:
                if has_cycle(agent_id, graph):
                    self.errors.append(f"Cycle detected involving {agent_id}")
    
    def validate_resource_limits(self):
        """Verify rate limits, timeouts, memory allocations."""
        for agent in self.config.get("agents", []):
            timeout = agent.get("timeout_ms", 30000)
            if timeout < 1000:
                self.errors.append(f"Agent {agent['id']} timeout too low: {timeout}ms")
            if timeout > 300000:
                self.warnings.append(f"Agent {agent['id']} timeout very high: {timeout}ms")
            
            memory = agent.get("memory_limit_mb", 512)
            if memory < 128:
                self.errors.append(f"Agent {agent['id']} insufficient memory: {memory}MB")
    
    def validate_safety_guardrails(self):
        """Check circuit breakers, isolation, network restrictions."""
        isolation = self.config.get("isolation", {})
        if not isolation.get("context_isolation"):
            self.warnings.append("Context isolation disabled — agents may see each other's internal state")
        if not isolation.get("network_restricted"):
            self.errors.append("Network access not restricted — only localhost/mock allowed in sandbox")
    
    def validate_error_handling(self):
        """Ensure retry logic, fallbacks, and error logging configured."""
        comm = self.config.get("communication", {})
        retry = comm.get("retry_policy", {})
        
        if not retry:
            self.warnings.append("No retry policy defined")
        else:
            if not retry.get("circuit_breaker"):
                self.warnings.append("Circuit breaker not configured")
            
            max_attempts = retry.get("max_attempts", 0)
            if max_attempts < 1:
                self.errors.append("max_attempts must be >= 1")
    
    def report(self) -> str:
        """Generate validation report."""
        lines = []
        if self.errors:
            lines.append(f"ERRORS ({len(self.errors)}):")
            for err in self.errors:
                lines.append(f"  ✗ {err}")
        if self.warnings:
            lines.append(f"WARNINGS ({len(self.warnings)}):")
            for warn in self.warnings:
                lines.append(f"  ⚠ {warn}")
        if not self.errors and not self.warnings:
            lines.append("✓ All validation checks passed")
        return "\n".join(lines)
```

#### Runtime validation during dry-run
```python
# Monitor and validate swarm behavior in real-time
class SwarmMonitor:
    """Track metrics and validate swarm health during sandbox execution."""
    
    def __init__(self, config):
        self.config = config
        self.metrics = {
            "agent_latencies": {},
            "message_counts": {},
            "error_counts": {},
            "queue_depths": {},
            "circuit_breaker_trips": {}
        }
        self.alerts = []
    
    def record_message(self, from_agent: str, to_agent: str, latency_ms: float):
        """Record message delivery."""
        if from_agent not in self.metrics["message_counts"]:
            self.metrics["message_counts"][from_agent] = 0
        self.metrics["message_counts"][from_agent] += 1
        
        if to_agent not in self.metrics["agent_latencies"]:
            self.metrics["agent_latencies"][to_agent] = []
        self.metrics["agent_latencies"][to_agent].append(latency_ms)
    
    def record_error(self, agent_id: str, error_type: str):
        """Track errors per agent."""
        key = f"{agent_id}:{error_type}"
        self.metrics["error_counts"][key] = self.metrics["error_counts"].get(key, 0) + 1
    
    def validate_health(self) -> dict:
        """Continuous health check during execution."""
        health = {"status": "healthy", "issues": []}
        
        # Check latency SLAs
        for agent, latencies in self.metrics["agent_latencies"].items():
            if latencies:
                avg_latency = sum(latencies) / len(latencies)
                max_latency = max(latencies)
                
                expected_max = self.config.get("agents", [{}])[0].get("timeout_ms", 30000)
                if max_latency > expected_max * 0.8:
                    health["status"] = "degraded"
                    health["issues"].append(f"Agent {agent} latency high: {max_latency}ms")
        
        # Check error rates
        total_errors = sum(self.metrics["error_counts"].values())
        total_messages = sum(self.metrics["message_counts"].values())
        if total_messages > 0:
            error_rate = total_errors / total_messages
            if error_rate > 0.05:  # > 5% errors
                health["status"] = "unhealthy"
                health["issues"].append(f"Error rate too high: {error_rate:.1%}")
        
        return health
```

## Example

### Complete sandbox setup and validation

```python
#!/usr/bin/env python3
"""
Swarm Sandbox Simulator: End-to-end example.
Setup a 5-agent council, validate topology, run dry-run scenario,
and generate deployment report.
"""

import json
from pathlib import Path
from swarm_sandbox import (
    SwarmSandboxValidator,
    SwarmMonitor,
    DryRunSimulator,
    SandboxEnvironment
)

# 1. Define swarm topology
COUNCIL_TOPOLOGY = {
    "name": "customer_analysis_council",
    "agents": [
        {
            "id": "orchestrator",
            "role": "orchestrator",
            "model": "claude-opus-4-20250514",
            "timeout_ms": 30000,
            "rate_limit": {"requests_per_minute": 60}
        },
        {
            "id": "researcher",
            "role": "researcher",
            "model": "claude-opus-4-20250514",
            "timeout_ms": 20000,
            "rate_limit": {"requests_per_minute": 120}
        },
        {
            "id": "analyst",
            "role": "analyst",
            "model": "claude-opus-4-20250514",
            "timeout_ms": 20000,
            "rate_limit": {"requests_per_minute": 120}
        },
        {
            "id": "risk_assessor",
            "role": "risk_assessor",
            "model": "claude-opus-4-20250514",
            "timeout_ms": 15000,
            "rate_limit": {"requests_per_minute": 80}
        },
        {
            "id": "writer",
            "role": "writer",
            "model": "claude-opus-4-20250514",
            "timeout_ms": 15000,
            "rate_limit": {"requests_per_minute": 60}
        }
    ],
    "communication": {
        "topology": "hub-and-spoke",
        "hub": "orchestrator",
        "retry_policy": {
            "max_attempts": 3,
            "backoff_ms": [100, 250, 500],
            "circuit_breaker": {"threshold": 5, "reset_ms": 60000}
        }
    },
    "isolation": {
        "context_isolation": True,
        "memory_limit_mb": 512,
        "network_restricted": True
    }
}

# 2. Validate topology
print("Step 1: Validating topology structure...")
validator = SwarmSandboxValidator(COUNCIL_TOPOLOGY)
if not validator.validate_all():
    print("\n❌ Validation FAILED:")
    print(validator.report())
    exit(1)
print("✓ Validation passed:")
print(validator.report())

# 3. Setup sandbox environment
print("\nStep 2: Initializing sandbox environment...")
env = SandboxEnvironment(
    topology=COUNCIL_TOPOLOGY,
    isolation_level="strict",
    network_access="none"
)
print(f"✓ Sandbox environment ready (isolation: {env.isolation_level})")

# 4. Create monitor for real-time tracking
print("\nStep 3: Setting up monitoring and metrics...")
monitor = SwarmMonitor(COUNCIL_TOPOLOGY)
print("✓ Monitor initialized")

# 5. Run dry-run scenario
print("\nStep 4: Running dry-run scenario (healthy council)...")
simulator = DryRunSimulator(
    topology=COUNCIL_TOPOLOGY,
    monitor=monitor,
    sandbox_env=env
)

# Simulate a successful run
scenario = {
    "name": "analyze_customer_cohort",
    "objective": "Analyze Q2 customer churn patterns and recommend retention strategy",
    "expected_sequence": [
        {"actor": "orchestrator", "action": "route_task", "targets": ["researcher"]},
        {"actor": "researcher", "action": "complete", "latency_ms": 2500},
        {"actor": "orchestrator", "action": "route_task", "targets": ["analyst"]},
        {"actor": "analyst", "action": "complete", "latency_ms": 1800},
        {"actor": "orchestrator", "action": "route_task", "targets": ["risk_assessor"]},
        {"actor": "risk_assessor", "action": "complete", "latency_ms": 1200},
        {"actor": "orchestrator", "action": "route_task", "targets": ["writer"]},
        {"actor": "writer", "action": "complete", "latency_ms": 1500},
    ]
}

result = simulator.run_scenario(scenario)
health = monitor.validate_health()

print(f"\n📊 Dry-run Results:")
print(f"  Status: {health['status']}")
print(f"  Total latency: {result['total_latency_ms']}ms")
print(f"  Messages sent: {result['message_count']}")
print(f"  Errors: {result['error_count']}")

# 6. Generate deployment report
print("\nStep 5: Generating deployment report...")
report = {
    "topology": COUNCIL_TOPOLOGY["name"],
    "validation": {
        "status": "passed",
        "errors": len(validator.errors),
        "warnings": len(validator.warnings)
    },
    "dry_run": {
        "scenario": scenario["name"],
        "status": health["status"],
        "total_latency_ms": result["total_latency_ms"],
        "message_count": result["message_count"],
        "error_rate": f"{(result['error_count'] / result['message_count'] * 100):.2f}%" if result['message_count'] > 0 else "0%"
    },
    "readiness": "green" if health["status"] == "healthy" else "yellow" if health["status"] == "degraded" else "red",
    "next_steps": [
        "1. Review this report and address any warnings",
        "2. Run production environment setup script",
        "3. Enable monitoring and logging in production",
        "4. Deploy council.js controller",
        "5. Start with single task, then scale concurrency"
    ]
}

report_path = Path(".swarm-sandbox-report.json")
report_path.write_text(json.dumps(report, indent=2))
print(f"✓ Report written to {report_path}")

print("\n" + "="*70)
print("DEPLOYMENT READINESS: " + report["readiness"].upper())
print("="*70)
print("\nNext steps:")
for step in report["next_steps"]:
    print(f"  {step}")
print()

# 7. Exit with appropriate code
exit(0 if report["readiness"] == "green" else 1)
```

### Running the sandbox validator from CLI

```bash
# Initialize sandbox environment
source .swarm-sandbox.env
export SANDBOX_MODE=true

# Run topology validation
python3 swarm_sandbox_validator.py \
  --topology ./council-topology.json \
  --isolation-level strict \
  --output ./validation-report.json

# Run specific dry-run scenario
python3 swarm_sandbox_simulator.py \
  --topology ./council-topology.json \
  --scenario healthy_council \
  --metrics-output ./metrics.json \
  --trace-enabled

# Run chaos test (failure injection)
python3 swarm_sandbox_simulator.py \
  --topology ./council-topology.json \
  --chaos-mode true \
  --failure-rate-percent 10 \
  --failure-modes timeout,malformed_response \
  --output ./chaos-report.json

# Generate deployment readiness report
python3 swarm_sandbox_report.py \
  --validation ./validation-report.json \
  --metrics ./metrics.json \
  --output ./deployment-readiness.md
```

### Integration with council.js

After sandbox validation passes, migrate to production:

```javascript
// council.js controller integration
const council = require('council.js');
const sandboxReport = require('./.swarm-sandbox-report.json');

// Verify sandbox validation before deploying
if (sandboxReport.readiness !== 'green') {
  throw new Error('Sandbox validation failed. Fix issues before deployment.');
}

// Load production topology (same config as sandbox-validated)
const productionTopology = require('./council-topology.json');

// Initialize with guardrails from sandbox testing
const swarmController = council.create({
  topology: productionTopology,
  
  // Apply safety limits from sandbox
  rate_limits: productionTopology.agents.map(a => ({
    agent_id: a.id,
    requests_per_minute: a.rate_limit.requests_per_minute
  })),
  
  // Use timeout values from sandbox
  timeouts: productionTopology.agents.map(a => ({
    agent_id: a.id,
    timeout_ms: a.timeout_ms
  })),
  
  // Circuit breaker settings from sandbox
  circuit_breaker: productionTopology.communication.retry_policy.circuit_breaker,
  
  // Monitoring from sandbox metrics
  monitoring: {
    enabled: true,
    log_level: 'info',
    metrics_output: './production-metrics.json'
  }
});

// Deploy swarm
swarmController.start();
```

### Checklist: From sandbox to production

```markdown
## Pre-Production Deployment Checklist

- [ ] Sandbox validation report shows "green" readiness
- [ ] All topology errors resolved (0 errors in report)
- [ ] Warnings reviewed and accepted
- [ ] Dry-run scenario executed successfully
- [ ] Chaos test (failure injection) passed with acceptable recovery
- [ ] Load test: 2x concurrency passed
- [ ] Load test: 5x message rate passed
- [ ] Production environment variables configured
- [ ] Secrets (API keys) injected at runtime
- [ ] Production database/external services ready
- [ ] Monitoring dashboards configured
- [ ] Alerting thresholds set based on sandbox metrics
- [ ] Runbook for common failure scenarios prepared
- [ ] Team trained on council operation and debugging
- [ ] Rollback plan documented (fallback to single agent)
- [ ] Start with canary: deploy to 10% of traffic first
- [ ] Monitor production metrics for first 24 hours
- [ ] Gradually increase load to 100% over 1 week
```
