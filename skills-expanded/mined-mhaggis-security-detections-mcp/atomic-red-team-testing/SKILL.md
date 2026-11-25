---
name: Atomic Red Team Testing
description: Execute and validate adversary emulation tests using Atomic Red Team. Covers standard atomics, custom atomics (T9999.XXX), deployment workflows, and detection validation.
---

# Atomic Red Team Testing Skill

## Configuration

Required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `$SIEM_PLATFORM` | Target SIEM for validation | `splunk`, `sentinel`, `elastic` |
| `$ATTACK_RANGE_PATH` | Path to Attack Range installation | `/opt/attack-range` |
| `$ATTACK_RANGE_VENV` | Path to Attack Range Python venv | `/opt/attack-range/.venv` |
| `$ATOMICS_PATH` | Path to atomic-red-team atomics folder | `/opt/atomic-red-team/atomics` |
| `$CUSTOM_ATOMICS_PATH` | Path to custom atomics (T9999.XXX) | `/opt/custom-atomics` |

Target placeholders used in this guide:
- `<TARGET_IP>` — IP address of the test endpoint
- `<TARGET_NAME>` — Hostname of the test endpoint (e.g., `ar-win-1`)

## Pragmatic Testing Philosophy

Detection engineering is iterative. The goal is NOT to run every atomic against every target — it is to generate the **specific telemetry** your detection needs and confirm the detection fires.

**Core principles:**

1. **Test what you're detecting.** Pick atomics that produce the exact event your SPL/Sigma/KQL query looks for.
2. **One technique at a time.** Isolate variables. Run one atomic, check for logs, validate the detection, then move on.
3. **Fast feedback loops.** Deploy → Execute → Wait → Validate. If something breaks, fix it and re-run — don't over-plan.
4. **Custom atomics fill gaps.** When no standard atomic covers your detection scenario, write a T9999.XXX custom atomic instead of forcing a bad fit.
5. **Validate telemetry first, detection second.** If the right events aren't reaching your SIEM, the detection can't fire. Always confirm log ingestion before blaming the query.

## Running Standard Atomics

### Via Invoke-AtomicRedTeam (PowerShell on target)

```powershell
# List available tests for a technique
Invoke-AtomicTest T1059.001 -ShowDetailsBrief

# Run a specific test number
Invoke-AtomicTest T1059.001 -TestNumbers 1

# Run with prerequisite check and install
Invoke-AtomicTest T1059.001 -TestNumbers 1 -GetPrereqs
Invoke-AtomicTest T1059.001 -TestNumbers 1

# Cleanup after test
Invoke-AtomicTest T1059.001 -TestNumbers 1 -Cleanup
```

### Via Attack Range (remote execution)

```bash
cd "$ATTACK_RANGE_PATH"
source "$ATTACK_RANGE_VENV/bin/activate"

# Run a standard atomic remotely
python attack_range.py simulate -t T1059.001 --target <TARGET_NAME>

# Run specific test number
python attack_range.py simulate -t T1059.001 -tn 1 --target <TARGET_NAME>
```

### Via Ansible (direct SSH/WinRM)

```bash
ansible <TARGET_NAME> -m win_shell -a "Invoke-AtomicTest T1059.001 -TestNumbers 1" \
  --extra-vars "ansible_host=<TARGET_IP>"
```

## Custom Atomics (T9999.XXX)

When no standard atomic exists for your detection scenario, create a custom atomic using the T9999.XXX numbering scheme. This avoids collisions with upstream Atomic Red Team technique IDs.

### Numbering Convention

| Range | Purpose |
|-------|---------|
| T9999.001–T9999.099 | Windows endpoint atomics |
| T9999.100–T9999.199 | Linux endpoint atomics |
| T9999.200–T9999.299 | Cloud / SaaS atomics |
| T9999.300–T9999.399 | Network / protocol atomics |

### Custom Atomic YAML Structure

```yaml
attack_technique: T9999.001
display_name: "Custom - Suspicious PowerShell Download Cradle"
atomic_tests:
  - name: "PowerShell download cradle with Net.WebClient"
    auto_generated_guid: <generate-a-uuid>
    description: |
      Simulates a PowerShell download cradle using Net.WebClient.
      Designed to trigger detections for T1059.001 + T1105.
    supported_platforms:
      - windows
    executor:
      command: |
        powershell.exe -NoProfile -Command "(New-Object Net.WebClient).DownloadString('http://127.0.0.1/test')"
      name: command_prompt
      elevation_required: false
```

### Deploying Custom Atomics

1. Place YAML in `$CUSTOM_ATOMICS_PATH/T9999.XXX/T9999.XXX.yaml`
2. Copy to target's atomics folder or use Ansible:

```bash
ansible <TARGET_NAME> -m win_copy \
  -a "src=$CUSTOM_ATOMICS_PATH/T9999.001/ dest=C:\\AtomicRedTeam\\atomics\\T9999.001\\" \
  --extra-vars "ansible_host=<TARGET_IP>"
```

3. Execute on target:

```powershell
Invoke-AtomicTest T9999.001 -TestNumbers 1
```

## Validation Workflow

The standard workflow is: **Deploy → Execute → Wait → Validate**

### Step 1: Deploy (if needed)

Ensure the target has Invoke-AtomicRedTeam installed and any custom atomics are synced.

### Step 2: Execute

Run the atomic test (see above). Note the exact execution time.

### Step 3: Wait for Ingestion

Telemetry takes time to reach your SIEM. Typical delays:

| Data Source | Expected Delay |
|-------------|---------------|
| Sysmon (via UF) | 30–90 seconds |
| Windows Security Events | 30–120 seconds |
| EDR telemetry | 15–60 seconds |
| Cloud audit logs | 1–5 minutes |
| Network flow data | 1–5 minutes |

**Recommendation:** Wait at least 2 minutes before querying, then retry at 5 minutes if nothing appears.

### Step 4: Validate

Check for telemetry first, then run the detection. Commands differ by SIEM:

**Splunk (SPL):**
```spl
// Check raw telemetry arrived
index=* sourcetype=* "<expected_process_name>" earliest=-15m

// Run the actual detection search
| your_detection_search_here
```

**Sentinel (KQL):**
```kql
// Check raw telemetry arrived
DeviceProcessEvents
| where Timestamp > ago(15m)
| where FileName == "<expected_process_name>"

// Or for SecurityEvent-based logs
SecurityEvent
| where TimeGenerated > ago(15m)
| where Process == "<expected_process_name>"
```

**Elastic (EQL in Dev Tools or Discover):**
```eql
// Check raw telemetry arrived (via Security → Timelines or Discover)
process where process.name == "<expected_process_name>"
  and @timestamp > "now-15m"
```

**Sigma (compile first, then test in target SIEM):**
```bash
# Compile to your backend
sigma convert -t splunk -p sysmon rule.yml
sigma convert -t microsoft365defender rule.yml
sigma convert -t elasticsearch rule.yml
```

### Decision Tree

```
Atomic executed
  └─ Telemetry in SIEM? 
       ├─ NO → Check: UF running? Correct sourcetype? Parsing errors?
       └─ YES → Detection fires?
            ├─ NO → Check: Field names? Time window? Logic errors?
            └─ YES → Document result ✓ → Move to next test
```

## Troubleshooting

### No telemetry after execution

1. **Verify the atomic actually ran** — Check exit code and target process list
2. **Check forwarder/agent status:**
   - Splunk: Universal Forwarder (`splunk status`)
   - Elastic: Elastic Agent (`elastic-agent status`)
   - Sentinel: Azure Monitor Agent or MDE sensor health in portal
   - Generic: Winlogbeat/Filebeat (`systemctl status filebeat`)
3. **Check sourcetype/index/table** — Events may land in an unexpected location
4. **Check time sync** — Clock skew between target and SIEM causes missed windows

### Atomic fails to execute

1. **Prerequisites missing** — Run `-GetPrereqs` first
2. **Execution policy** — `Set-ExecutionPolicy Bypass -Scope Process`
3. **AV/EDR blocking** — May need exclusions for test atomics (document any exclusions!)
4. **Elevation required** — Some atomics need admin; check `elevation_required` field

### Detection doesn't fire despite telemetry

1. **Field mapping mismatch** — CIM fields vs raw fields vs ECS fields
2. **Time window too narrow** — Widen the search window
3. **Filter too aggressive** — Temporarily remove filters and re-run
4. **Threshold not met** — Some detections require N events; run atomic multiple times

### Custom atomic not found on target

1. **Path mismatch** — Atomics folder must match Invoke-AtomicRedTeam's expected path
2. **YAML syntax** — Validate YAML before deploying (`yamllint T9999.XXX.yaml`)
3. **GUID missing** — Every test needs a unique `auto_generated_guid`

## Integration with Detection Engineering Workflow

```
1. Identify coverage gap (technique with no detection)
2. Write detection rule (SPL / Sigma / KQL)
3. Find or create atomic test for the technique
4. Deploy atomic to test environment
5. Execute atomic
6. Validate telemetry arrives
7. Validate detection fires
8. Document results (log_decision in knowledge graph)
9. Submit detection PR with test evidence
```

This workflow ensures every detection is **tested before merge** — not just syntactically valid but actually capable of catching the behavior it claims to detect.
