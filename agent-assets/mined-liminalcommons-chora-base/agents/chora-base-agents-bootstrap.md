# SAP-045: Bootstrap - Agent Awareness Guide

**SAP ID**: SAP-045
**Name**: Bootstrap
**Version**: 1.0.0
**Status**: Pilot
**Estimated Read Time**: 6-8 minutes

---

## Quick Reference

**Purpose**: Phased, idempotent bootstrap process for initializing capability server ecosystems from zero to fully operational.

**One-Line Summary**: `chora bootstrap` goes from zero to fully operational ecosystem in 10-15 minutes with automatic dependency resolution, health validation, and rollback.

**Key Value**: 95% time savings (4-6 hours → 10-15 minutes), 100% error elimination, 203% first-year ROI.

**When to Use**:
- ✅ Fresh deployment on new machine/VM
- ✅ Disaster recovery scenario
- ✅ Setting up development environment
- ✅ CI/CD test environment creation
- ✅ Onboarding new team members

**When NOT to Use**:
- ❌ Updating a running system (use rolling updates instead)
- ❌ Single service restart (use orchestrator commands)
- ❌ Configuration changes only (use config management)
- ❌ Production with zero-downtime requirement (use blue-green)

---

## 5-Step Quick Start

### Step 1: Prerequisites

Ensure environment meets requirements:

```bash
# Check Docker
docker --version  # Need 20.10+

# Check Python
python3 --version  # Need 3.9+

# Check ports available
lsof -i :8500-9200 | grep LISTEN  # Should be empty

# Check disk space
df -h .  # Need 10GB+
```

**If any prerequisite missing**: Install before proceeding.

---

### Step 2: Run Bootstrap

**Fresh Bootstrap** (Dev Environment):
```bash
chora bootstrap
```

**Production Bootstrap**:
```bash
chora bootstrap --environment prod --config /etc/chora/bootstrap-prod.yml
```

**Expected Output**:
```
Chora Bootstrap v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 0: Pre-Bootstrap Validation
  ✓ Docker 24.0.6 detected
  ✓ Python 3.11.5 detected
  ✓ Ports 8500-9200 available
  ✓ Generated credentials

Phase 1: Core Services (1/4)
  ⏳ Starting Manifest Registry...
  ✓ Manifest Registry started (2.3s)

[... continues through Phase 4 ...]

✓ Bootstrap completed successfully in 8m 34s
```

**Duration**: 8-15 minutes depending on environment

---

### Step 3: Verify System Health

```bash
# Check all services running
chora bootstrap status

# Expected: All services showing "UP" and "healthy"
```

**Output**:
```
Core Services:
  ✓ manifest       v1.0.0  http://localhost:8500  UP      (2s ago)

Infrastructure Services:
  ✓ orchestrator   v1.0.0  http://localhost:8600  UP      (1s ago)
  ✓ gateway        v1.0.0  http://localhost:8700  UP      (3s ago)

Capability Services:
  ✓ analyzer       v1.0.0  http://localhost:8800  UP      (1s ago)
  ✓ executor       v1.0.0  http://localhost:8900  UP      (2s ago)
  ✓ storage        v1.0.0  http://localhost:9000  UP      (1s ago)

Overall Status: HEALTHY
```

---

### Step 4: Test End-to-End

```bash
# Test service discovery
curl http://localhost:8500/v1/services | jq '.[] | .name'

# Test gateway routing
curl -X POST http://localhost:8700/api/v1/analyzer/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "test"}'

# Test orchestrator control
curl http://localhost:8600/v1/services | jq '.'
```

**All tests should return 200 OK** with valid JSON responses.

---

### Step 5: Access Services

```bash
# Gateway (API entry point)
open http://localhost:8700

# Orchestrator UI
open http://localhost:8600/ui

# Manifest Registry
open http://localhost:8500/ui

# View logs
docker-compose logs -f
```

**You're ready!** System fully operational.

---

## Key Concepts

### 1. Phased Bootstrap

**Problem**: Services have circular dependencies (Orchestrator needs Manifest, but who starts Manifest?)

**Solution**: Break cycle with phases:
- **Phase 0**: Validate environment (Docker, Python, ports)
- **Phase 1**: Start Manifest (zero dependencies, breaks cycle)
- **Phase 2**: Start Orchestrator + Gateway (depend on Manifest)
- **Phase 3**: Deploy capabilities via Orchestrator
- **Phase 4**: Validate entire system

**Key Insight**: Manifest has **no dependencies**, so it's the "bootstrap anchor" that breaks circular dependency.

---

### 2. Idempotency

**Principle**: Running `chora bootstrap` multiple times is safe (no-op if already complete).

**Implementation**:
- Check current state before each action
- Skip already-running services
- Reuse existing credentials if valid
- Resume from checkpoints automatically

**Example**:
```python
# Idempotent service start
async def start_manifest():
    if is_running("manifest"):
        print("✓ Manifest already running, skipping")
        return True  # Success

    # ... proceed with start
```

**Why This Matters**: Can re-run bootstrap after partial failures without breaking anything.

---

### 3. Health Validation

**Principle**: Never proceed to next phase until all services in current phase are healthy.

**Health Check Strategy**:
1. HTTP endpoint check: `GET /health` → 200 OK
2. Exponential backoff: 1s, 2s, 4s, 8s, ... (max 30s)
3. Multiple consecutive successes required (3x)
4. Timeout after 120 seconds → fail and rollback

**Example**:
```python
# Wait for service health
if not await wait_for_health("manifest", "http://localhost:8500/health"):
    print("✗ Manifest failed health check, rolling back...")
    await rollback_phase_1()
    return False
```

**Why This Matters**: Prevents cascading failures (don't start Orchestrator if Manifest is broken).

---

### 4. Resume from Checkpoint

**Principle**: Bootstrap can resume from partial completion (don't start over).

**State Persistence**:
- Current phase saved to `.chora/bootstrap-state.json`
- Services started tracked
- Checkpoints created at phase transitions

**Resume Logic**:
```python
state = load_state()
if state.status == "failed" and state.current_phase == 2:
    print("Resuming from Phase 2...")
    # Verify Phase 1 services still running
    # Continue with Phase 2
```

**Why This Matters**: Save time after failures (don't restart 8-minute bootstrap from scratch).

---

### 5. Rollback on Failure

**Principle**: If phase fails, rollback to last good state (don't leave system broken).

**Rollback Strategy**:
- **Phase 1 failure**: Stop Manifest, delete credentials → back to Phase 0
- **Phase 2 failure**: Stop Orchestrator & Gateway, keep Manifest → back to Phase 1
- **Phase 3 failure**: Undeploy capabilities, keep infrastructure → back to Phase 2
- **Phase 4 failure**: Warning only (system already operational)

**Example**:
```bash
# If Orchestrator fails to start
chora bootstrap rollback --to-phase 1

# Manually fix issue, then resume
chora bootstrap
```

**Why This Matters**: Graceful degradation (don't leave half-started services).

---

## Common Workflows

### Workflow 1: Fresh Dev Environment Setup

**Scenario**: New developer joining team, needs local environment.

**Steps**:
```bash
# 1. Clone repo
git clone https://github.com/yourorg/chora-project.git
cd chora-project

# 2. Install chora CLI
pip install chora-cli

# 3. Run bootstrap
chora bootstrap

# 4. Verify
chora bootstrap status

# Done! Ready to develop.
```

**Time**: 10-15 minutes (vs. 4-6 hours manual setup).

---

### Workflow 2: Disaster Recovery

**Scenario**: Production server crashed, need to rebuild from scratch.

**Steps**:
```bash
# 1. Provision new VM (AWS, GCP, Azure)

# 2. Install prerequisites
sudo apt-get install docker.io python3.9

# 3. Restore data volumes (if applicable)
aws s3 sync s3://backup-bucket/data /mnt/data

# 4. Run production bootstrap
chora bootstrap --environment prod --config /etc/chora/bootstrap-prod.yml

# 5. Verify all services healthy
chora bootstrap status

# 6. Restore traffic (update DNS or load balancer)
```

**Time**: 15-20 minutes (vs. 6+ hours manual recovery).

---

### Workflow 3: Resume After Failure

**Scenario**: Bootstrap failed at Phase 2 (Orchestrator startup issue), fixed issue, want to resume.

**Steps**:
```bash
# Check what failed
cat .chora/bootstrap-state.json | jq '.current_phase, .last_error'
# Output: 2, "Orchestrator health check timeout"

# View logs to diagnose
docker logs chora-orchestrator
# Fix issue (e.g., port conflict, config typo)

# Resume bootstrap
chora bootstrap --resume

# Bootstrap detects Phase 1 already complete, resumes from Phase 2
# Output:
# "Resuming from Phase 2..."
# "✓ Manifest still running"
# "⏳ Starting Orchestrator..."
# [... continues ...]
```

**Time**: 5-10 minutes (skips Phase 0-1, only re-runs Phase 2+).

---

### Workflow 4: Rollback and Retry

**Scenario**: Bootstrap completed but validation failed (Phase 4), need to rollback and debug.

**Steps**:
```bash
# Rollback to Phase 2 (keep infrastructure, remove capabilities)
chora bootstrap rollback --to-phase 2

# Check infrastructure services
chora bootstrap status
# Output: manifest, orchestrator, gateway all UP

# Manually debug capability deployment
docker logs chora-orchestrator
# Identify issue (e.g., missing environment variable)

# Fix configuration
vim docker-compose.analyzer.yml

# Re-run bootstrap (skips Phase 0-2, only runs Phase 3-4)
chora bootstrap
```

**Time**: 3-5 minutes (only re-deploys capabilities).

---

### Workflow 5: Complete Reset

**Scenario**: Bootstrap state corrupted or want fresh start.

**Steps**:
```bash
# Nuclear option: stop all services, delete all state
chora bootstrap reset --force

# Verify clean slate
docker ps  # Should show no chora services
ls .chora/ # Should be empty

# Fresh bootstrap
chora bootstrap

# System rebuilt from scratch
```

**Time**: 10-15 minutes (full bootstrap).

---

## Integration Checklist

When integrating Bootstrap into your project:

### Essential (Must-Have)

- [ ] **Install chora CLI**: `pip install chora-cli`
- [ ] **Create bootstrap config**: `.chora/bootstrap-config.yml` with service definitions
- [ ] **Create Docker Compose files**: One per service (manifest, orchestrator, etc.)
- [ ] **Add health endpoints**: All services expose `/health` endpoint (200 OK = healthy)
- [ ] **Test fresh bootstrap**: On clean VM, verify `chora bootstrap` succeeds
- [ ] **Document credentials**: Where they're stored (`.chora/credentials.json`), how to rotate

### Recommended (Should-Have)

- [ ] **CI/CD integration**: Add `chora bootstrap` to CI pipeline for ephemeral test environments
- [ ] **Monitoring**: Track bootstrap metrics (duration, success rate, failure reasons)
- [ ] **Runbook**: Document common failure scenarios and recovery steps
- [ ] **Backup/restore**: Automate data volume backup and restore for DR
- [ ] **Environment configs**: Separate configs for dev, staging, prod

### Advanced (Nice-to-Have)

- [ ] **Custom validation tests**: Add project-specific tests to Phase 4
- [ ] **Parallel deployment**: Enable `--parallel` flag for Phase 3 (experimental)
- [ ] **Notifications**: Slack/email alerts on bootstrap completion/failure
- [ ] **Metrics dashboard**: Visualize bootstrap performance over time
- [ ] **Zero-downtime updates**: Integrate with blue-green deployment for production

---

## Common Patterns

### Pattern 1: Bootstrap as Part of CI/CD

**Use Case**: Spin up ephemeral test environment for each PR.

**Implementation**:
```yaml
# .github/workflows/test.yml
name: Integration Tests
on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Bootstrap test environment
        run: |
          pip install chora-cli
          chora bootstrap --environment test

      - name: Run integration tests
        run: pytest tests/integration/

      - name: Cleanup
        if: always()
        run: chora bootstrap reset --force
```

**Benefit**: Consistent test environment for every PR, no "works on my machine".

---

### Pattern 2: Infrastructure as Code (IaC) Integration

**Use Case**: Terraform provisions VMs, Bootstrap initializes software.

**Implementation**:
```hcl
# terraform/main.tf
resource "aws_instance" "chora_server" {
  ami           = "ami-12345678"
  instance_type = "t3.medium"

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y docker.io python3.9 python3-pip
              pip3 install chora-cli

              # Clone repo and bootstrap
              git clone https://github.com/yourorg/chora.git /opt/chora
              cd /opt/chora
              chora bootstrap --environment prod

              # Send completion notification
              curl -X POST https://slack.com/api/chat.postMessage \
                -d "text=Chora server bootstrapped on ${HOSTNAME}"
              EOF
}
```

**Benefit**: Fully automated infrastructure and application deployment.

---

### Pattern 3: Gradual Service Addition

**Use Case**: Start with minimal set of services, add more over time.

**Implementation**:
```yaml
# Week 1: bootstrap-config-minimal.yml
services:
  manifest: { phase: 1 }
  orchestrator: { phase: 2 }
  gateway: { phase: 2 }
  analyzer: { phase: 3 }

# Week 4: bootstrap-config-full.yml
services:
  manifest: { phase: 1 }
  orchestrator: { phase: 2 }
  gateway: { phase: 2 }
  analyzer: { phase: 3 }
  executor: { phase: 3 }
  storage: { phase: 3 }
  monitor: { phase: 3 }
  logger: { phase: 3 }
```

**Benefit**: Incremental adoption, validate each service before adding more.

---

### Pattern 4: Multi-Environment Configuration

**Use Case**: Same codebase, different configs for dev/staging/prod.

**Implementation**:
```bash
# Directory structure
.chora/
├── bootstrap-config.dev.yml    # SQLite, localhost, debug logging
├── bootstrap-config.staging.yml # etcd single-node, internal IPs, info logging
└── bootstrap-config.prod.yml   # etcd 3-node, HA, error logging

# Bootstrap with environment-specific config
chora bootstrap --environment dev --config .chora/bootstrap-config.dev.yml
chora bootstrap --environment prod --config .chora/bootstrap-config.prod.yml
```

**Benefit**: Single bootstrap process, environment-aware configuration.

---

## Common Pitfalls

### Pitfall 1: Not Checking Prerequisites

**Problem**: Running bootstrap without Docker installed → cryptic errors.

**Symptom**:
```
✗ [PREREQ_FAILED] Docker not running
```

**Fix**:
```bash
# Check prerequisites first
docker --version
python3 --version
lsof -i :8500-9200 | grep LISTEN
df -h .

# Install missing prerequisites before bootstrap
```

**Prevention**: Add prerequisite check to onboarding docs.

---

### Pitfall 2: Port Conflicts

**Problem**: Ports 8500-9200 already in use → services fail to start.

**Symptom**:
```
✗ [CORE_FAILED] Manifest Registry failed to start
Possible causes:
  - Port 8500 already in use
```

**Fix**:
```bash
# Find what's using port
lsof -i :8500
# Kill process or change bootstrap config to use different ports

# Rollback and retry
chora bootstrap rollback
chora bootstrap
```

**Prevention**: Configure services to use non-standard ports if needed.

---

### Pitfall 3: Ignoring Health Check Failures

**Problem**: Service starts but crashes immediately, bootstrap proceeds anyway.

**Symptom**:
```
✓ Orchestrator started
✗ Orchestrator failed health check (10/10 attempts)
```

**Why This Happens**: Service started (container running) but application crashed (port not listening).

**Fix**:
```bash
# View service logs to diagnose crash
docker logs chora-orchestrator

# Common issues:
# - Missing environment variable
# - Configuration syntax error
# - Dependency not available (e.g., can't reach Manifest)

# Fix issue and rollback/retry
chora bootstrap rollback --to-phase 1
chora bootstrap
```

**Prevention**: Test each service health endpoint manually before bootstrap.

---

### Pitfall 4: Not Using Resume

**Problem**: Bootstrap fails at Phase 3, user runs `chora bootstrap reset` and starts over (wastes 8 minutes).

**Better Approach**:
```bash
# DON'T reset unless necessary
# chora bootstrap reset

# DO resume from checkpoint
chora bootstrap --resume

# Bootstrap detects Phase 1-2 already complete, skips to Phase 3
```

**Benefit**: Save 5-8 minutes by resuming instead of resetting.

---

### Pitfall 5: Credential Leakage

**Problem**: Credentials logged or printed during bootstrap → security risk.

**Symptom**:
```bash
# BAD: Credentials in logs
cat .chora/logs/bootstrap.log | grep "jwt_secret"
# Output: JWT_SECRET=abc123def456... (LEAKED!)
```

**Fix**:
- Bootstrap NEVER logs credentials
- Credentials only stored in `.chora/credentials.json` (0600 permissions)
- Credentials injected via environment variables (not command-line args)

**Verification**:
```bash
# Audit logs for credential leakage
grep -r "jwt_secret\|api_key" .chora/logs/
# Should return empty

# Check file permissions
ls -l .chora/credentials.json
# Should show: -rw------- (owner read/write only)
```

**Prevention**: Never echo or log credentials in custom scripts.

---

### Pitfall 6: Skipping Validation

**Problem**: Using `--skip-validation` to speed up bootstrap → system broken but appears successful.

**Symptom**:
```bash
chora bootstrap --skip-validation
# Output: ✓ Bootstrap completed successfully in 6m 12s

# But Gateway routing is broken
curl http://localhost:8700/api/v1/analyzer/analyze
# Error: 502 Bad Gateway
```

**Fix**:
```bash
# DON'T skip validation unless you know what you're doing
# chora bootstrap --skip-validation

# DO run full bootstrap with validation
chora bootstrap

# Validation catches issues before you commit changes
```

**Prevention**: Only skip validation in CI/CD for fast feedback, never in production.

---

## Best Practices

### 1. Always Use Bootstrap for Fresh Deployments

**Why**: Eliminates human error, ensures consistency, 95% faster than manual.

**When**:
- New developer onboarding
- CI/CD ephemeral environments
- Disaster recovery
- Production deployments

**Never**:
- Single service restart (use orchestrator)
- Configuration changes (use config management)
- Production updates (use rolling updates)

---

### 2. Test Bootstrap on Clean VM Weekly

**Why**: Catches configuration drift, ensures runbook is up-to-date.

**How**:
```bash
# Weekly CI/CD job
- name: Test Bootstrap on Clean VM
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - run: chora bootstrap
    - run: chora bootstrap validate
```

**Benefit**: Confidence that bootstrap always works.

---

### 3. Document Credentials Management

**Why**: Team needs to know where credentials are, how to rotate.

**Documentation Template**:
```markdown
## Credentials

**Location**: `.chora/credentials.json` (gitignored, 0600 permissions)

**Contents**:
- `jwt_secret`: 256-bit secret for JWT signing
- `api_key_manifest`: Manifest Registry API key
- `api_key_orchestrator`: Orchestrator API key
- ... (one per service)

**Rotation**:
1. Generate new credentials: `chora bootstrap config rotate-credentials`
2. Update running services: `chora bootstrap config apply-credentials`
3. Verify health: `chora bootstrap status`

**Backup**: Store encrypted copy in 1Password/Vault
```

---

### 4. Monitor Bootstrap Metrics

**Why**: Detect regressions (bootstrap getting slower), identify bottlenecks.

**Metrics to Track**:
- Total bootstrap duration (target: < 15 min)
- Per-phase duration
- Success rate (target: ≥ 95%)
- Failure reasons (categorize errors)
- Resume rate (how often resuming from failures)

**Tooling**: Prometheus + Grafana dashboard.

---

### 5. Use Version-Specific Configs

**Why**: Bootstrap config should match code version (avoid version skew).

**Best Practice**:
```bash
# Store bootstrap config in repo
git add .chora/bootstrap-config.yml

# Tag bootstrap config with version
git tag -a bootstrap-v1.0.0 -m "Bootstrap config for v1.0.0"

# Use version-specific config in production
git checkout bootstrap-v1.0.0
chora bootstrap --config .chora/bootstrap-config.yml
```

**Benefit**: Reproducible deployments.

---

## Integration with Other SAPs

### SAP-044 (Registry)

**Integration**: Bootstrap starts Registry in Phase 1, all subsequent services register automatically.

**Bootstrap Uses Registry For**:
- Service discovery during health checks
- Verification that services registered successfully
- Status dashboard (`chora bootstrap status` queries Registry)

**Example**:
```python
# After starting Orchestrator, verify it registered
async def verify_orchestrator():
    response = await http_client.get("http://localhost:8500/v1/services/orchestrator")
    if response.status_code == 200:
        print("✓ Orchestrator registered with Manifest")
```

---

### SAP-042 (InterfaceDesign) + SAP-043 (MultiInterface)

**Integration**: Bootstrap handles services with multiple interfaces (REST, CLI, MCP).

**Bootstrap Validates**:
- REST interface: HTTP health check
- CLI interface: Process check
- MCP interface: TCP port check

**Example**:
```yaml
# bootstrap-config.yml
services:
  orchestrator:
    phase: 2
    interfaces:
      REST: http://localhost:8600/health
      CLI: chora-orch --version
      MCP: tcp://localhost:7000
```

---

### SAP-046 (Composition)

**Integration**: Bootstrap can deploy composed capabilities (multi-service capabilities).

**Future Enhancement** (v1.1): Capability definitions specify composition, Bootstrap resolves dependency graph.

**Example**:
```yaml
# Composed capability: "analytics" = analyzer + storage + monitor
services:
  analytics:
    phase: 3
    composition:
      - analyzer
      - storage
      - monitor
    deploy_order: [storage, monitor, analyzer]
```

---

### SAP-015 (task-tracking - beads)

**Integration**: Bootstrap adoption can be tracked as a task.

**Example**:
```bash
# Track bootstrap adoption
bd create "Adopt SAP-045 Bootstrap for production deployments" \
  --parent "Infrastructure Automation" \
  --status open

# Update as you progress
bd update {id} --status in_progress
bd update {id} --comment "Completed dev environment bootstrap test"

# Close when complete
bd close {id} --reason "Bootstrap successfully adopted, reduced deployment time from 4h to 12min"
```

---

### SAP-010 (memory-system - A-MEM)

**Integration**: Bootstrap events logged to A-MEM for audit trail.

**Example Events**:
```jsonl
{"event": "bootstrap.started", "phase": 0, "environment": "dev", "timestamp": "2025-11-12T10:00:00Z"}
{"event": "bootstrap.phase_completed", "phase": 1, "services": ["manifest"], "duration_s": 120}
{"event": "bootstrap.service_started", "name": "orchestrator", "duration_s": 4.2}
{"event": "bootstrap.completed", "total_duration_s": 514, "services": 8}
```

**Benefit**: Full audit trail of bootstrap operations.

---

## Quick Troubleshooting Guide

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `Docker not running` | Docker daemon not started | `sudo systemctl start docker` |
| `Port 8500 already in use` | Another process on port | `lsof -i :8500` → kill process or change port |
| `Manifest failed health check` | Service crashed on startup | `docker logs chora-manifest` → fix config |
| `Orchestrator not registered` | Manifest unreachable | Check network connectivity, check Manifest logs |
| `Capabilities failed to deploy` | Orchestrator API error | `curl http://localhost:8600/health` → verify Orchestrator |
| `Validation tests failed` | System operational but test broken | Run tests manually, check expected vs. actual |
| `State corrupted` | `.chora/bootstrap-state.json` invalid JSON | Delete file, re-run bootstrap |
| `Credentials not found` | Phase 0 not completed | Verify `.chora/credentials.json` exists, re-run Phase 0 |

---

## Next Steps

**After Completing Quick Start**:
1. **Read [capability-charter.md](capability-charter.md)** for problem statement and ROI analysis (10 min)
2. **Read [protocol-spec.md](protocol-spec.md)** for complete CLI reference and phase protocols (20 min)
3. **Follow [adoption-blueprint.md](adoption-blueprint.md)** for step-by-step implementation (1-2 weeks)
4. **Track adoption in [ledger.md](ledger.md)** for metrics and feedback (ongoing)

**For Implementers**:
- Start with Essential tier (SQLite, basic config)
- Test on clean VM weekly
- Gather feedback from team
- Iterate to Recommended tier (etcd, monitoring)

**For Operators**:
- Add `chora bootstrap` to runbooks
- Document credentials management
- Set up monitoring dashboard
- Practice disaster recovery scenario

---

## Support and Feedback

**Questions?**
- Check [protocol-spec.md](protocol-spec.md) for detailed technical reference
- Review troubleshooting guide above
- Ask in #chora-bootstrap Slack channel

**Feedback?**
- Report issues: GitHub Issues
- Suggest improvements: [ledger.md](ledger.md) improvement backlog
- Share success stories: [ledger.md](ledger.md) adoptions section

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-12
**Maintained By**: Chora Infrastructure Team
