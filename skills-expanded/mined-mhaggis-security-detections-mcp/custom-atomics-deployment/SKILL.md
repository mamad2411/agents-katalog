---
name: Custom Atomics Deployment
description: Create, deploy, and execute custom Atomic Red Team tests (T9999.XXX series) for detection validation. Covers YAML authoring, Ansible deployment, and manual alternatives.
---

# Custom Atomics Deployment Skill

## Overview

When no standard Atomic Red Team test covers your detection scenario, create a **custom atomic** using the T9999.XXX numbering scheme. This avoids collisions with upstream technique IDs while giving you full control over the test payload.

## Configuration

Required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `$ATOMICS_PATH` | Path to atomic-red-team atomics directory | `/opt/atomic-red-team/atomics` |
| `$CUSTOM_ATOMICS_PATH` | Path to your custom atomics repo/directory | `/opt/custom-atomics` |
| `$ATTACK_RANGE_PATH` | Path to Attack Range (if using AR for deployment) | `/opt/attack-range` |
| `$ATTACK_RANGE_VENV` | Attack Range Python venv | `/opt/attack-range/.venv` |
| `$ANSIBLE_INVENTORY` | Path to Ansible inventory file | `/etc/ansible/hosts` |

Target placeholders:
- `<TARGET_IP>` — IP address of the test endpoint
- `<TARGET_NAME>` — Hostname of the test endpoint (e.g., `ar-win-1`)

## T9999.XXX Numbering Convention

| Range | Purpose | Example |
|-------|---------|---------|
| T9999.001–T9999.099 | Windows endpoint tests | T9999.001: Encoded PowerShell download cradle |
| T9999.100–T9999.199 | Linux endpoint tests | T9999.100: Cron persistence via echo |
| T9999.200–T9999.299 | Cloud / SaaS tests | T9999.200: AWS IAM key rotation abuse |
| T9999.300–T9999.399 | Network / protocol tests | T9999.300: DNS TXT record exfiltration |
| T9999.400–T9999.499 | macOS tests | T9999.400: LaunchAgent persistence |

## YAML Authoring

### Directory Structure

```
$CUSTOM_ATOMICS_PATH/
  T9999.001/
    T9999.001.yaml
    src/
      payload.ps1    (optional supporting files)
  T9999.002/
    T9999.002.yaml
```

### YAML Template

```yaml
attack_technique: T9999.001
display_name: "Custom - Suspicious Encoded PowerShell Download"
atomic_tests:
  - name: "PowerShell download cradle with Net.WebClient and encoding"
    auto_generated_guid: <generate-a-uuid>
    description: |
      Simulates an encoded PowerShell download cradle using Net.WebClient.
      Maps to T1059.001 (PowerShell) + T1105 (Ingress Tool Transfer).
      Designed to trigger detections for encoded command execution.
    supported_platforms:
      - windows
    input_arguments:
      target_url:
        description: URL to download from
        type: url
        default: "http://127.0.0.1:8080/test.txt"
    dependency_executor_name: powershell
    dependencies:
      - description: "PowerShell must be available"
        prereq_command: "Get-Command powershell.exe"
        get_prereq_command: "echo 'PowerShell not found'"
    executor:
      command: |
        $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes("(New-Object Net.WebClient).DownloadString('#{target_url}')"))
        powershell.exe -EncodedCommand $encoded
      cleanup_command: |
        echo "No cleanup required"
      name: powershell
      elevation_required: false
```

### YAML Authoring Tips

- **Always include `auto_generated_guid`** — Generate with `uuidgen` or any UUID tool
- **Use `input_arguments`** — Makes tests reusable across environments
- **Include `dependencies`** — Prerequisite checks prevent confusing failures
- **Include `cleanup_command`** — Even if it's just a no-op, document it
- **Map to real techniques** — Note which ATT&CK technique(s) the custom atomic simulates in the description

## Deployment Methods

### Method 1: Ansible (Recommended)

Ansible provides idempotent, repeatable deployment to one or many targets.

**Deploy custom atomic to Windows target:**

```bash
ansible <TARGET_NAME> -m win_copy \
  -a "src=$CUSTOM_ATOMICS_PATH/T9999.001/ dest=C:\\AtomicRedTeam\\atomics\\T9999.001\\" \
  --extra-vars "ansible_host=<TARGET_IP>"
```

**Deploy to Linux target:**

```bash
ansible <TARGET_NAME> -m copy \
  -a "src=$CUSTOM_ATOMICS_PATH/T9999.100/ dest=/opt/atomic-red-team/atomics/T9999.100/ mode=0755" \
  --extra-vars "ansible_host=<TARGET_IP>"
```

**Deploy all custom atomics at once:**

```bash
ansible <TARGET_NAME> -m win_copy \
  -a "src=$CUSTOM_ATOMICS_PATH/ dest=C:\\AtomicRedTeam\\atomics\\" \
  --extra-vars "ansible_host=<TARGET_IP>"
```

### Method 2: SCP / WinRM (Manual)

For one-off deployments without Ansible:

```bash
# Linux target
scp -r "$CUSTOM_ATOMICS_PATH/T9999.100" user@<TARGET_IP>:/opt/atomic-red-team/atomics/

# Windows target (via PowerShell remoting)
$session = New-PSSession -ComputerName <TARGET_IP> -Credential (Get-Credential)
Copy-Item -Path "$env:CUSTOM_ATOMICS_PATH\T9999.001" -Destination "C:\AtomicRedTeam\atomics\" -ToSession $session -Recurse
```

### Method 3: Attack Range (if using AR)

```bash
cd "$ATTACK_RANGE_PATH"
source "$ATTACK_RANGE_VENV/bin/activate"

# Use AR's simulate with custom atomics path
python attack_range.py simulate -t T9999.001 --target <TARGET_NAME>
```

**Note:** Attack Range may need configuration to recognize custom atomics paths.

### Alternatives to Ansible

| Tool | Use Case | Notes |
|------|----------|-------|
| **Ansible** | Multi-target, repeatable | Best for lab environments |
| **SCP/WinRM** | Single target, quick | Fine for one-off testing |
| **Terraform provisioner** | Part of lab build | Deploy atomics during infra setup |
| **Salt/Puppet/Chef** | Existing config management | Use if already in your stack |
| **Git clone on target** | Self-service | Target pulls from atomics repo |

## Execution

### On Windows Target (PowerShell)

```powershell
# Import module (if not already loaded)
Import-Module "C:\AtomicRedTeam\invoke-atomicredteam\Invoke-AtomicRedTeam.psd1"

# List custom atomic tests
Invoke-AtomicTest T9999.001 -ShowDetailsBrief

# Run prerequisites
Invoke-AtomicTest T9999.001 -TestNumbers 1 -GetPrereqs

# Execute
Invoke-AtomicTest T9999.001 -TestNumbers 1

# Cleanup
Invoke-AtomicTest T9999.001 -TestNumbers 1 -Cleanup
```

### On Linux Target (Bash)

If using the Go-based atomic runner (`goart`):

```bash
./goart run T9999.100
```

Or execute manually based on the YAML's `command` field.

### Remote Execution via Ansible

```bash
# Windows
ansible <TARGET_NAME> -m win_shell \
  -a "Import-Module C:\\AtomicRedTeam\\invoke-atomicredteam\\Invoke-AtomicRedTeam.psd1; Invoke-AtomicTest T9999.001 -TestNumbers 1" \
  --extra-vars "ansible_host=<TARGET_IP>"

# Linux
ansible <TARGET_NAME> -m shell \
  -a "/opt/goart/goart run T9999.100" \
  --extra-vars "ansible_host=<TARGET_IP>"
```

## Validation Checklist

After deploying and executing a custom atomic:

- [ ] YAML passes syntax validation (`yamllint T9999.XXX.yaml`)
- [ ] `auto_generated_guid` is present and unique
- [ ] Atomic deploys to target without errors
- [ ] `Invoke-AtomicTest -ShowDetailsBrief` lists the test correctly
- [ ] Prerequisites pass or install successfully
- [ ] Execution completes without errors
- [ ] Expected telemetry appears in SIEM (check after appropriate delay)
- [ ] Detection rule fires on the generated telemetry
- [ ] Cleanup command runs without errors

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Atomic not found on target | Path mismatch | Verify atomics folder matches Invoke-AtomicRedTeam config |
| YAML parse error | Indentation or special characters | Run `yamllint`; escape special chars in commands |
| Test fails with "prereq not met" | Missing dependency | Run `-GetPrereqs` or install manually |
| No telemetry in SIEM | Forwarder issue or wrong sourcetype | Check forwarder status, verify index/sourcetype |
| Detection doesn't fire | Field mismatch or time window | Widen search window; check field names |
