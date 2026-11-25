---
name: Test Environment Builder
description: Build and manage adversary emulation lab environments for any SIEM. Covers Splunk Attack Range, Elastic Security labs, Azure Sentinel labs, and Docker-based setups. Maps data source requirements to infrastructure components.
---

# Test Environment Builder Skill

## Overview

Detection engineering requires test infrastructure that produces the right telemetry. This skill covers building environments that generate the exact log sources your detections need — with options for every major SIEM platform.

**Set `$SIEM_PLATFORM`** to focus guidance: `splunk`, `sentinel`, `elastic`, `sigma`

## Lab Options by SIEM

| SIEM Platform | Primary Lab Tool | Alternatives |
|--------------|-----------------|-------------|
| **Splunk** | [Attack Range](https://github.com/splunk/attack_range) (Terraform + Ansible) | DetectionLab (Vagrant) |
| **Elastic Security** | [Elastic Detection Lab](https://github.com/elastic/detection-rules) + Docker Compose | Custom Terraform + Elastic Agent |
| **Microsoft Sentinel** | [Azure Sentinel Training Lab](https://github.com/Azure/Azure-Sentinel/tree/master/Solutions/Training) (ARM/Bicep) | Azure VMs + Log Analytics Workspace |
| **Sigma (any backend)** | Any of the above | Docker-based minimal setup |

## Configuration

Environment variables (set what applies to your stack):

| Variable | Description | Example |
|----------|-------------|---------|
| `$SIEM_PLATFORM` | Target SIEM platform | `splunk`, `sentinel`, `elastic` |
| `$ATTACK_RANGE_PATH` | Path to Attack Range repo (Splunk) | `/opt/attack-range` |
| `$ATTACK_RANGE_VENV` | Python venv for Attack Range | `/opt/attack-range/.venv` |
| `$ATTACK_RANGE_CONFIG` | Path to `attack_range.conf` | `/opt/attack-range/attack_range.conf` |
| `$AWS_PROFILE` | AWS profile for cloud builds | `attack-range` |
| `$AZURE_SUBSCRIPTION_ID` | Azure subscription for Sentinel labs | (optional) |
| `$AZURE_RESOURCE_GROUP` | Azure RG for Sentinel labs | (optional) |
| `$ELASTIC_CLOUD_ID` | Elastic Cloud deployment ID | (optional) |

Target placeholders:
- `<TARGET_NAME>` — Hostname of a lab machine (e.g., `ar-win-1`)
- `<TARGET_IP>` — IP address of a lab machine

## Data Source to Infrastructure Mapping

This is the core planning table. Before building, identify which data sources your detection needs, then select the infrastructure that produces them.

| Data Source | Required Infrastructure | Attack Range Config Key |
|-------------|------------------------|------------------------|
| Windows Security Events (4688, 4624, etc.) | Windows Server/Workstation | `windows_servers` |
| Sysmon (EventID 1, 3, 7, 11, etc.) | Windows + Sysmon installed | `install_sysmon: "1"` |
| PowerShell Script Block Logging (4104) | Windows + PS logging GPO | `windows_servers` (enabled by default) |
| Linux auditd | Linux server | `linux_servers` |
| Zeek/Suricata network logs | Network sensor | `install_zeek: "1"` or `install_suricata: "1"` |
| AWS CloudTrail | AWS account + CloudTrail | `cloud_attack_range: "1"` |
| Azure AD sign-in logs | Azure AD tenant | Azure lab config |
| Kubernetes audit logs | K8s cluster | `kubernetes: "1"` |
| EDR telemetry (CrowdStrike, etc.) | EDR agent on endpoint | Manual install post-build |

## Build Workflow

### Step 1: Determine Required Data Sources

From your detection rule, identify every field and data source referenced:

**Splunk (SPL):**
```spl
`sysmon` EventCode=1 ParentImage=*\\cmd.exe Image=*\\powershell.exe
```
This needs: Sysmon process creation events → Windows host + Sysmon + Splunk UF.

**Sentinel (KQL):**
```kql
DeviceProcessEvents
| where FileName == "powershell.exe"
| where InitiatingProcessFileName == "cmd.exe"
```
This needs: Microsoft Defender for Endpoint agent → Log Analytics Workspace.

**Elastic (EQL):**
```eql
process where process.name == "powershell.exe"
  and process.parent.name == "cmd.exe"
```
This needs: Elastic Agent with Endpoint integration → Elasticsearch.

### Step 2: Select Configuration

```bash
cd "$ATTACK_RANGE_PATH"
source "$ATTACK_RANGE_VENV/bin/activate"

# Show current config
python attack_range.py show
```

### Step 3: Build

```bash
# Build the environment
python attack_range.py build

# Check status
python attack_range.py show

# Destroy when done (saves cost)
python attack_range.py destroy
```

### Build Time Estimates

| Configuration | Components | Approximate Build Time |
|--------------|------------|----------------------|
| Minimal (Splunk + 1 Windows) | 2 VMs | 15–25 minutes |
| Standard (Splunk + Win + Linux) | 3 VMs | 20–35 minutes |
| Full (Splunk + Win + Linux + Zeek) | 4 VMs | 30–45 minutes |
| Cloud (AWS CloudTrail + GuardDuty) | Cloud resources | 10–15 minutes |
| Kitchen sink | 5+ VMs + cloud | 45–60 minutes |

**Cost note:** AWS `t3.xlarge` instances (~$0.17/hr each). A standard 3-VM lab costs ~$0.50/hr. Always destroy when not actively testing.

## Example Configurations

### Minimal: Windows Endpoint Detection

For testing process creation, PowerShell, registry, and file system detections:

```ini
[global]
attack_range_password = <STRONG_PASSWORD>

[splunk_server]
s3_bucket_url = https://attack-range-appbinaries.s3-us-west-2.amazonaws.com

[windows_servers]
windows_server_1_os = "Windows Server 2022"
windows_server_1_sysmon = "1"
windows_server_1_atomic_red_team = "1"
```

### Standard: Windows + Linux

For cross-platform detection testing:

```ini
[windows_servers]
windows_server_1_os = "Windows Server 2022"
windows_server_1_sysmon = "1"
windows_server_1_atomic_red_team = "1"

[linux_servers]
linux_server_1_os = "Ubuntu 22.04"
linux_server_1_atomic_red_team = "1"
```

### Network: With Zeek

For network-based detections (DNS, HTTP, TLS):

```ini
[windows_servers]
windows_server_1_os = "Windows Server 2022"
windows_server_1_sysmon = "1"

[zeek_server]
install_zeek = "1"
```

## Configuration Schema Reference

Key sections in `attack_range.conf`:

| Section | Key Fields | Purpose |
|---------|-----------|---------|
| `[global]` | `attack_range_password`, `key_name` | Credentials and SSH keys |
| `[splunk_server]` | `s3_bucket_url`, `splunk_apps` | SIEM configuration |
| `[windows_servers]` | `*_os`, `*_sysmon`, `*_atomic_red_team` | Windows endpoints |
| `[linux_servers]` | `*_os`, `*_atomic_red_team` | Linux endpoints |
| `[zeek_server]` | `install_zeek` | Network monitoring |
| `[cloud]` | `cloud_attack_range`, `aws_region` | Cloud resources |

## SIEM-Specific Lab Guides

### Splunk: Attack Range (Detailed Above)

Attack Range is the most mature option for Splunk-based detection testing. See the configuration examples and build workflow above.

### Elastic Security: Docker Compose Lab

The fastest way to stand up an Elastic detection testing lab:

```bash
# Clone Elastic's detection-rules repo (includes Docker setup)
git clone https://github.com/elastic/detection-rules.git
cd detection-rules

# Or use a standalone Elastic stack via Docker Compose
mkdir elastic-lab && cd elastic-lab
cat > docker-compose.yml << 'COMPOSE'
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.15.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=changeme
    ports:
      - "9200:9200"
    mem_limit: 4g

  kibana:
    image: docker.elastic.co/kibana/kibana:8.15.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=elastic
      - ELASTICSEARCH_PASSWORD=changeme
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
COMPOSE

docker compose up -d
# Kibana available at http://localhost:5601
# Install Elastic Agent on endpoints to forward telemetry
```

**Adding endpoints:**
1. In Kibana → Fleet → Add agent
2. Install Elastic Agent on Windows/Linux test VMs
3. Enable "Endpoint Security" integration for process, file, and network telemetry
4. Install Atomic Red Team on the endpoint for testing

**Pros:** Free, fast startup (~2 min), full Elastic Security features
**Cons:** Single-node (not production-representative), manual endpoint setup

### Microsoft Sentinel: Azure Lab

**Option 1: Training Lab Solution (ARM template)**

Deploy the [Azure Sentinel Training Lab](https://github.com/Azure/Azure-Sentinel/tree/master/Solutions/Training) which provisions a Log Analytics workspace with sample data:

```bash
# Via Azure CLI
az deployment group create \
  --resource-group $AZURE_RESOURCE_GROUP \
  --template-uri "https://raw.githubusercontent.com/Azure/Azure-Sentinel/master/Solutions/Training/Package/mainTemplate.json"
```

**Option 2: Custom Lab with Azure VMs**

```bash
# Create resource group
az group create --name detection-lab --location eastus

# Create Log Analytics workspace
az monitor log-analytics workspace create \
  --resource-group detection-lab \
  --workspace-name sentinel-lab-ws

# Enable Microsoft Sentinel on the workspace
az sentinel onboarding-state create \
  --resource-group detection-lab \
  --workspace-name sentinel-lab-ws

# Create Windows VM with Defender for Endpoint
az vm create \
  --resource-group detection-lab \
  --name win-target-1 \
  --image Win2022Datacenter \
  --admin-username labadmin \
  --admin-password '<STRONG_PASSWORD>' \
  --size Standard_B2ms

# Install the Azure Monitor Agent (AMA) on the VM
az vm extension set \
  --resource-group detection-lab \
  --vm-name win-target-1 \
  --name AzureMonitorWindowsAgent \
  --publisher Microsoft.Azure.Monitor

# Create data collection rule for Sysmon/Security events
# (Use Azure Portal → Data Collection Rules for easier setup)
```

**Pros:** Native Sentinel environment, real KQL testing, integrates with Defender
**Cons:** Requires Azure subscription, costs ~$2-5/hr for VMs + ingestion

### DetectionLab (Multi-SIEM Friendly)

```bash
cd /opt/DetectionLab/Vagrant
vagrant up
# Builds: DC, WEF, Win10, Fleet server, Splunk
# Pre-configured logging pipeline
```

**Pros:** All-in-one, great defaults, includes Fleet for osquery
**Cons:** Heavy (4+ VMs), Vagrant/VirtualBox only, Splunk-focused logging

**Adapting for Elastic:** After build, install Elastic Agent alongside or instead of Splunk UF.
**Adapting for Sentinel:** Forward events via Azure Monitor Agent to a Log Analytics workspace.

### Custom Terraform (Any SIEM)

For teams with existing IaC, build a module that:
1. Provisions compute (EC2, Azure VM, GCP CE)
2. Installs the appropriate logging agent:
   - **Splunk:** Universal Forwarder
   - **Elastic:** Elastic Agent
   - **Sentinel:** Azure Monitor Agent or Microsoft Defender for Endpoint
   - **Any (via Sigma):** Any agent that produces standard logs
3. Configures log forwarding to your SIEM
4. Installs Atomic Red Team for testing

## Tips

- **Start small.** Build the minimal config that produces the telemetry you need. Add components as requirements grow.
- **Snapshot before testing.** If your cloud provider supports it, snapshot VMs before running destructive atomics.
- **Automate destroy.** Set a cron job or CI timeout to destroy labs after N hours to avoid cost surprises.
- **Tag everything.** Use consistent tags (`project=detection-testing`, `owner=<you>`) for cost tracking.
- **Match your production SIEM.** Test in the same platform you deploy to. A detection validated in Splunk may behave differently in Sentinel due to field mapping differences.
