---
name: chaos-engineering
description: Design chaos experiments to test system resilience. Outputs failure scenarios, blast radius controls, and automated chaos testing.
argument-hint: [system criticality, failure tolerance, recovery requirements]
allowed-tools: Read, Write, Bash
---

# Chaos Engineering

Design experiments that intentionally break systems to verify resilience. Not random destruction — controlled failures with hypothesis, blast radius limits, and automated rollback.

## Process

1. **Define steady state.** Normal system metrics (latency, error rate, throughput).
2. **Hypothesize impact.** "System survives 1 node failure with < 5s disruption".
3. **Design experiment.** What to break, how, for how long.
4. **Set blast radius.** Limit to staging, single region, or 1% production traffic.
5. **Run experiment.** Execute failure injection, monitor metrics.
6. **Analyze results.** Did system behave as hypothesized?
7. **Fix weaknesses.** Add redundancy, improve failover, update runbooks.

## Output Format

### Chaos Experiment: [System Name]

**Hypothesis:** System tolerates 50% instance failures  
**Experiment:** Terminate 3 of 6 instances randomly  
**Blast Radius:** Staging environment only  
**Result:** ✅ Passed - p95 latency 180ms → 220ms (< 300ms threshold)  
**Findings:** Auto-scaling kicked in within 45 seconds

---

## Chaos Engineering Principles

### 1. Build a Hypothesis Around Steady State
```
Steady state: p95 latency < 200ms, error rate < 0.1%

Hypothesis: "When we terminate 1 instance, 
p95 latency stays < 300ms and error rate < 1%"

NOT: "Let's kill a server and see what happens"
```

### 2. Vary Real-World Events
```
Network failures:
- Packet loss (1-10%)
- Latency injection (100-1000ms)
- Connection drops

Instance failures:
- CPU spike (100%)
- Memory exhaustion (OOM)
- Disk full
- Process crash

Dependency failures:
- Database slow query (5s timeout)
- External API 503 errors
- Message queue backlog
```

### 3. Run Experiments in Production
```
Staging: Test infrastructure
Production (limited blast radius): Test real system

Why production?
- Real traffic patterns
- Real dependencies
- Real data volumes
- Real configurations
```

### 4. Automate Experiments
```
Manual chaos: One-time learning
Automated chaos: Continuous verification

GameDays → Chaos Pipelines → Continuous Chaos
```

### 5. Minimize Blast Radius
```
Start small:
1. Single service in staging
2. Single instance in production
3. 1% of production traffic
4. Entire service (if 1-3 passed)
5. Multi-service experiment
```

---

## Chaos Toolkit

### Experiment Definition

```yaml
# experiment.yaml
version: 1.0.0
title: "Instance Termination Resilience"
description: "Verify system survives random instance termination"

steady-state-hypothesis:
  title: "Application is healthy"
  probes:
  - name: "app-responds-to-requests"
    type: probe
    provider:
      type: http
      url: "https://api.example.com/health"
      timeout: 3
      expected_status: 200
  
  - name: "p95-latency-under-threshold"
    type: probe
    provider:
      type: python
      module: prometheus_probes
      func: query_latency
      arguments:
        query: "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
        threshold: 0.2  # 200ms

method:
- type: action
  name: "terminate-random-instance"
  provider:
    type: python
    module: chaosaws.ec2.actions
    func: terminate_instances
    arguments:
      filters:
        - Name: "tag:Environment"
          Values: ["production"]
      az: "us-east-1a"
      instance_count: 1

rollbacks:
- type: action
  name: "ensure-min-instances"
  provider:
    type: python
    module: chaosaws.asg.actions
    func: set_desired_capacity
    arguments:
      asg_name: "my-asg"
      desired_capacity: 6
```

### Run Experiment

```bash
# Install Chaos Toolkit
pip install chaostoolkit chaostoolkit-aws

# Run experiment
chaos run experiment.yaml --journal-path results.json

# Report
chaos report --export-format=pdf results.json report.pdf
```

---

## Litmus Chaos (Kubernetes)

### Install Litmus

```bash
# Install Litmus operator
kubectl apply -f https://litmuschaos.github.io/litmus/litmus-operator-v2.0.0.yaml

# Verify
kubectl get pods -n litmus
```

### Pod Delete Experiment

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: pod-delete-chaos
  namespace: default
spec:
  appinfo:
    appns: 'default'
    applabel: 'app=myapp'
    appkind: 'deployment'
  
  engineState: 'active'
  chaosServiceAccount: litmus-admin
  
  experiments:
  - name: pod-delete
    spec:
      components:
        env:
        - name: TOTAL_CHAOS_DURATION
          value: '60'  # Run for 60 seconds
        
        - name: CHAOS_INTERVAL
          value: '10'  # Delete pod every 10 seconds
        
        - name: FORCE
          value: 'false'  # Graceful shutdown
        
      probe:
      - name: "app-health-check"
        type: "httpProbe"
        httpProbe/inputs:
          url: "http://myapp-service/health"
          insecureSkipVerify: false
          responseTimeout: 3000
        mode: "Continuous"
        runProperties:
          probeTimeout: 5
          interval: 2
          retry: 1
```

### Network Chaos

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: network-chaos
spec:
  appinfo:
    appns: 'default'
    applabel: 'app=myapp'
    appkind: 'deployment'
  
  experiments:
  - name: pod-network-latency
    spec:
      components:
        env:
        - name: NETWORK_LATENCY
          value: '2000'  # 2 second latency
        
        - name: TOTAL_CHAOS_DURATION
          value: '60'
        
        - name: DESTINATION_IPS
          value: '10.0.1.5'  # Database IP
```

---

## Gremlin (Commercial)

```python
from gremlin import GremlinAPIClient

client = GremlinAPIClient(api_key='YOUR_API_KEY')

# CPU attack
attack = client.create_attack(
    target={
        'type': 'Random',
        'exact': 1,
        'tags': {
            'env': 'production',
            'service': 'api'
        }
    },
    impact={
        'type': 'cpu',
        'percent': 80,
        'length': 300  # 5 minutes
    }
)

# Network attack
attack = client.create_attack(
    target={
        'type': 'Exact',
        'hosts': ['api-server-1']
    },
    impact={
        'type': 'latency',
        'ms': 500,
        'length': 600
    }
)

# Monitor attack
status = client.get_attack(attack['id'])
print(f"Attack status: {status['state']}")

# Halt attack
client.halt_attack(attack['id'])
```

---

## Failure Injection Library (Python)

```python
import random
import time
from functools import wraps

class ChaosMonkey:
    """Inject failures into application"""
    
    def __init__(self, failure_rate=0.01):
        self.failure_rate = failure_rate  # 1% failure rate
        self.enabled = True
    
    def random_failure(self, func):
        """Randomly fail function calls"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.enabled and random.random() < self.failure_rate:
                raise Exception("Chaos Monkey: Random failure injected")
            return func(*args, **kwargs)
        return wrapper
    
    def latency(self, min_ms=100, max_ms=1000):
        """Inject random latency"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if self.enabled:
                    delay = random.uniform(min_ms, max_ms) / 1000
                    time.sleep(delay)
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def error_rate(self, rate=0.05):
        """Inject errors at specified rate"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if self.enabled and random.random() < rate:
                    return {'error': 'Service unavailable'}, 503
                return func(*args, **kwargs)
            return wrapper
        return decorator

# Usage
chaos = ChaosMonkey(failure_rate=0.01)

@app.route('/api/data')
@chaos.latency(min_ms=200, max_ms=500)  # Add latency
@chaos.error_rate(rate=0.05)  # 5% error rate
def get_data():
    return {'data': 'value'}

# Disable chaos in production
if os.getenv('CHAOS_ENABLED') != 'true':
    chaos.enabled = False
```

---

## Experiment Examples

### 1. Database Failover

```yaml
title: "Database Failover Test"

hypothesis:
  "When primary database fails, application switches to replica 
   within 30 seconds with < 1% data loss"

method:
- name: "stop-primary-database"
  action: stop_instance
  arguments:
    instance_id: "db-primary"

- name: "wait-for-failover"
  action: wait
  arguments:
    duration: 30

probes:
- name: "app-still-responsive"
  query: "SELECT 1"
  expected: success

- name: "replication-lag"
  query: "SELECT pg_last_wal_replay_lsn()"
  threshold: "< 1MB"
```

### 2. Dependency Failure

```python
# External API timeout
experiment = {
    'title': 'Payment API Timeout',
    'hypothesis': 'App degrades gracefully when payment API times out',
    'method': [
        {
            'type': 'action',
            'name': 'inject-network-delay',
            'target': 'payment-api.example.com',
            'delay': '10s'  # Longer than app timeout
        }
    ],
    'steady-state': {
        'checkout_success_rate': '> 95%',
        'fallback_payment_method_used': True
    }
}
```

### 3. Resource Exhaustion

```yaml
title: "Memory Leak Simulation"

method:
- name: "inject-memory-leak"
  action: memory_stress
  arguments:
    percent: 90
    duration: 300  # 5 minutes

probes:
- name: "app-oom-killed"
  expected: false

- name: "kubernetes-restarts-pod"
  expected: true
  max_restarts: 1
```

---

## GameDay Runbook

### Pre-GameDay (1 week before)
```
1. Define objectives
   - Test failover?
   - Verify monitoring?
   - Practice incident response?

2. Prepare experiments
   - Write experiment specs
   - Test in staging
   - Set blast radius limits

3. Notify stakeholders
   - Engineering team
   - On-call
   - Leadership (if prod)

4. Setup monitoring
   - Dashboards ready
   - Alerts configured
   - Recording tools ready
```

### During GameDay (2-4 hours)
```
9:00 AM: Kickoff
- Review objectives
- Confirm blast radius
- Verify rollback procedures

9:30 AM: Experiment 1 - Instance Termination
- Run experiment
- Monitor metrics
- Document observations
- Rollback if needed

10:30 AM: Experiment 2 - Network Partition
...

12:00 PM: Wrap-up
- Review findings
- Identify action items
- Schedule fixes
```

### Post-GameDay
```
1. Write report
   - What broke
   - What worked
   - Surprises

2. Create tickets
   - Critical issues: P0 (fix this week)
   - High issues: P1 (fix this month)
   - Medium issues: P2 (backlog)

3. Update runbooks
   - New failure modes discovered
   - Actual vs expected behavior
   - Recovery procedures
```

---

## Continuous Chaos

```yaml
# Jenkins pipeline
pipeline {
  agent any
  
  triggers {
    cron('0 2 * * *')  # Run daily at 2 AM
  }
  
  stages {
    stage('Chaos Experiment') {
      steps {
        script {
          // Run chaos experiment
          sh 'chaos run experiments/pod-delete.yaml'
          
          // Check if passed
          def result = readJSON file: 'chaostoolkit.log'
          if (!result.steady_state_met) {
            error("Chaos experiment failed")
          }
        }
      }
    }
    
    stage('Alert on Failure') {
      when {
        expression { currentBuild.result == 'FAILURE' }
      }
      steps {
        slackSend(
          message: "🚨 Chaos experiment failed: ${env.JOB_NAME}",
          channel: '#chaos-engineering'
        )
      }
    }
  }
}
```

---

## Safety Controls

### Blast Radius Limits

```python
class BlastRadiusControl:
    """Prevent chaos from affecting too much"""
    
    def __init__(self, max_affected_instances=1):
        self.max_affected = max_affected_instances
    
    def check_safety(self, target_instances):
        """Verify experiment is safe to run"""
        
        total_instances = get_total_instances()
        
        if len(target_instances) > self.max_affected:
            raise Exception(f"Blast radius too large: {len(target_instances)} > {self.max_affected}")
        
        if len(target_instances) / total_instances > 0.25:
            raise Exception("Cannot affect > 25% of instances")
        
        return True

# Usage
control = BlastRadiusControl(max_affected_instances=2)
control.check_safety(target_instances=['i-123', 'i-456'])
```

### Automatic Rollback

```python
def run_chaos_with_safety(experiment):
    """Run experiment with automatic rollback on metrics degradation"""
    
    baseline_metrics = get_current_metrics()
    
    try:
        # Start experiment
        chaos_id = start_chaos(experiment)
        
        # Monitor for 5 minutes
        for i in range(30):  # 30 iterations, 10s each
            time.sleep(10)
            
            current_metrics = get_current_metrics()
            
            # Check if metrics degraded
            if current_metrics['error_rate'] > baseline_metrics['error_rate'] * 2:
                raise Exception("Error rate doubled")
            
            if current_metrics['p95_latency'] > baseline_metrics['p95_latency'] * 1.5:
                raise Exception("Latency increased 50%")
        
        # Experiment passed
        stop_chaos(chaos_id)
        return {'success': True}
    
    except Exception as e:
        # Rollback
        stop_chaos(chaos_id)
        restore_system()
        alert(f"Chaos experiment aborted: {e}")
        return {'success': False, 'error': str(e)}
```

## Rules

- Start with hypothesis, not random destruction — "system survives X failure with Y impact".
- Limit blast radius initially — staging first, then 1% production, then expand.
- Monitor steady state metrics — error rate, latency, throughput define success.
- Automate rollback on degradation — don't manually watch dashboards, set thresholds.
- Run in production eventually — staging tests infrastructure, production tests system.
- GameDays for team practice — coordinated chaos builds confidence and uncovers gaps.
- Document all experiments — findings, surprises, action items create institutional knowledge.
- Fix what breaks — chaos without fixing teaches nothing, creates alert fatigue.
- Continuous chaos as regression tests — prevent reintroduction of known failure modes.
- Get stakeholder buy-in before production chaos — unexpected downtime damages trust.
