---
name: docker-bench-expert
description: 'Specialised skill for the AMT Docker Bench — a multi-container simulation of a T264 autonomous truck. Use when asked about docker_bench containers (rpk1, rpk2, rpk3, platform-sim, avi-radio, test-manager, vas-aht), Docker Compose configuration, network topology (onboard/offboard/CAN/local-fms-network), NAT setup, CIC/RPK version selection, T264 simulator, VAS:AHT integration, DDS QoS profiles, IP address remapping, overlay files, run_tests.sh, Docker Bench version compatibility, compatible FMS/AMT version pairs, or any issue involving the Docker Bench environment. Also use for debugging container startup failures, networking problems, build errors, image pull failures, version mismatch issues, or service readiness issues in the bench. Can fetch the Docker Bench Versions Compatibility Matrix from Confluence to determine compatible version combinations.'
---

# Docker Bench Expert

A specialised skill for understanding, maintaining, and debugging the AMT Docker Bench environment — a collection of Docker containers that emulate the separate physical computers on a T264 autonomous haul truck for testing and validation purposes.

This skill extends the `docker-expert` skill with domain-specific knowledge of the Docker Bench architecture, its containers, networking, and configuration.

## When to Use This Skill

- Understanding how the Docker Bench containers fit together
- Debugging container build failures, startup issues, or service readiness problems
- Analysing or modifying the `docker-compose.yml`, Dockerfiles, or overlay configuration
- Diagnosing networking issues between containers (onboard, offboard, CAN, FMS)
- Understanding or modifying the NAT setup (avi-radio)
- Selecting or changing CIC/RPK/T264 Sim versions
- Determining compatible FMS and AMT Docker Bench version combinations
- Resolving image pull failures or version mismatch errors
- Understanding the IP address remapping system
- Troubleshooting DDS communication or QoS profile issues
- Working with `run_tests.sh` or the test-manager container
- Understanding the relationship between Docker Bench and the real truck hardware

## FX-8520 Refuel Dispatch Playbook (Validated)

Use this workflow when a Docker Bench refuel scenario reaches `Dispatched` but the
asset does not move, or the assignment is quickly cancelled.

### High-signal checks

Run these checks together so geometry, mode, and dispatch state are evaluated in
the same time window:

- TM area state: `GET /areas/{areaId}/state` (Traffic Manager)
- Robot mode/restrictions: `GET /RobotControl/AssetIdentifier/{asset}`
- Assignment list: `GET /Assignments` (Assignment Aggregator)
- TM logs: search for `DispatchCancelledEvent`, `No MoveToArea instruction found`,
  `LoadAreaId`, `DumpAreaId`

### Copy/paste diagnostic command (local Imperium + Docker Bench)

Use this one-liner to capture the key state in one snapshot:

```bash
TOKEN=$(curl -s -X POST http://localhost:4020/Auth/locallogin -H "Content-Type: application/json" -d '{"username":"641693","password":"Autonomy@1"}' | python3 -c "import json,sys; print(json.load(sys.stdin)['tokenResponse']['token'])") && \
echo '--- TM area state ---' && \
curl -s "http://localhost:7100/areas/e387c3ae-8bc4-4278-8fdf-83943f6be9ea/state" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool && \
echo '--- RobotControl AHT002 ---' && \
curl -sk "https://robot-control-service.dev.localhost/RobotControl/AssetIdentifier/AHT002" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool && \
echo '--- Assignment Aggregator ---' && \
curl -s -o /tmp/aa_root.out -w "%{http_code}\n" "http://localhost:5660/Assignments" -H "Authorization: Bearer $TOKEN" && \
head -c 1200 /tmp/aa_root.out && echo && \
echo '--- traffic-manager relevant logs ---' && \
docker logs traffic-manager 2>&1 | grep -Ei "AHT002|ELI_REFUEL|no route|route|assignment|Dispatched|DispatchCancelled|MoveToArea|LoadAreaId|DumpAreaId" | tail -120
```

Interpret this snapshot before making geometry changes.

### Known failure signature

If TM logs show both of the following, treat it as a dispatch/assignment
interpretation failure (not only a mode problem):

- `No MoveToArea instruction found for "LoadAreaId"` (and/or `DumpAreaId`)
- `Handling "DispatchCancelledEvent" ...` immediately after dispatch is added

### Lane-aligned spawn guidance

For scripted spawn positions, derive pose from the lane geometry instead of map
eyeballing:

1. Get the lane segment id from TM `entryPathPoint.laneSegmentId`.
2. Query Mine Model `GET /PathSegment` and select the matching segment.
3. Use the midpoint `PathSegmentPoint` (index `count//2`) for `X` and `Y`.
4. Derive heading from midpoint neighbors (`mid-1` -> `mid+1`) with `atan2`.

Using the midpoint centerpoint avoids truck overhang at lane ends and gives more
stable initial routing.

### Important note for debugging priorities

If midpoint lane-aligned spawn and autonomy mode are both correct but cancellation
persists, prioritise assignment payload/dispatch contract checks over further spawn
angle tuning.

## Communication Style

- **Default**: Provide concise, plain-language explanations. Focus on what is happening, why it matters, and how to fix it. Do not assume the reader has deep Docker or networking knowledge.
- **When asked for more detail**: Give in-depth explanations covering the underlying Docker and networking mechanisms.
- Always provide actionable solutions — not just descriptions of problems.

## Docker Bench Architecture Overview

The Docker Bench simulates a T264 autonomous haul truck using seven containers, each representing a physical computer or network device on the real truck:

| Container | Role | What It Emulates |
|-----------|------|------------------|
| **rpk1** | Autonomy Management Toolkit (AMT) | The main onboard management computer running the RTK launcher, diagnostics watchdog, mine model adapter, blob sync, and FMS bridge |
| **rpk2** | Compute IC (CIC) | The control computer running the Control IC software with a web interface on port 8009 |
| **rpk3** | Robot Perception Kernel (RPK) | The perception computer running obstacle detection and point cloud processing |
| **vas-aht** | Vehicle Awareness System (VAS:AHT) | The Motium unit running VAS for position/heading reporting, notifications, and sound management via DDS |
| **platform-sim** | T264 Simulator | Simulates the vehicle dynamics and CAN bus of the physical truck, with a web interface on port 8123 |
| **avi-radio** | NAT Gateway | Emulates the AVI radio that bridges the truck's internal network to the external FMS/OT network using iptables NAT rules |
| **test-manager** | Test Automation (optional) | Runs ARCU automation tests; enabled via `--profile test-manager` |

### Multi-Asset Support

Docker Bench supports running multiple instances simultaneously, each representing a different truck. The `ASSET_ID` variable in `.env` (default: `AHT000`) controls:

- **Compose project name**: `amt-docker-bench-${ASSET_ID_LOWER}` (e.g., `amt-docker-bench-aht000`)
- **Container names**: `<service>-${ASSET_ID}` (e.g., `rpk1-AHT000`)
- **Network names**: `<network>-${ASSET_ID}` (e.g., `onboard-AHT000`, `offboard-AHT000`)

Two conventions exist for running commands inside containers:

- **Primary**: `docker exec <service>-AHT000 <command>` (e.g., `docker exec rpk1-AHT000 bash`)
- **Alternative**: `docker compose exec <service> <command>` (e.g., `docker compose exec rpk1 bash`)

The primary convention uses the full container name (service + asset ID). The alternative uses Compose service names and is useful when you do not know or want to type the asset ID. Both are valid; the documentation uses the primary convention.

### Key Files

| File | Purpose |
|------|---------|
| [docker_bench/docker-compose.yml](docker_bench/docker-compose.yml) | Orchestrates all containers, networks, volumes, and build arguments |
| [docker_bench/.env](docker_bench/.env) | Environment variables: versions, IPs, asset ID, patterns |
| [docker_bench/run_tests.sh](docker_bench/run_tests.sh) | Automated test orchestration script |
| [docker_bench/utils/helpers.sh](docker_bench/utils/helpers.sh) | Shell utility functions for logging, Docker version checks, container readiness |
| [docker_bench/dockerfile-rpk1](docker_bench/dockerfile-rpk1) | AMT container Dockerfile |
| [docker_bench/dockerfile-rpk2](docker_bench/dockerfile-rpk2) | CIC container Dockerfile |
| [docker_bench/dockerfile-rpk3](docker_bench/dockerfile-rpk3) | RPK container Dockerfile |
| [docker_bench/dockerfile-vas-aht](docker_bench/dockerfile-vas-aht) | VAS:AHT container Dockerfile |
| [docker_bench/dockerfile-platform-sim](docker_bench/dockerfile-platform-sim) | T264 Simulator Dockerfile |
| [docker_bench/dockerfile-test-manager](docker_bench/dockerfile-test-manager) | Test manager Dockerfile |
| [docker_bench/dockerfile-avi-radio](docker_bench/dockerfile-avi-radio) | NAT gateway Dockerfile |
| [docs/docker_bench/index.md](docs/docker_bench/index.md) | User-facing documentation for Docker Bench |

## Network Architecture

The Docker Bench uses four networks to mirror the real truck's network topology:

### Networks

| Network | Subnet | Purpose | Real-World Equivalent |
|---------|--------|---------|----------------------|
| **onboard** (`onboard-${ASSET_ID}`) | `10.10.10.0/24` | Internal communication between onboard computers | The truck's internal Ethernet connecting all RPKs |
| **offboard** (`offboard-${ASSET_ID}`) | `10.10.1.0/24` | Connects onboard computers to the AVI radio | The link from onboard computes to the external-facing radio |
| **local-fms-network** | `172.18.0.0/16` | External FMS/cloud connectivity | The OT (Operational Technology) mine network |
| **can** (`can-${ASSET_ID}`) | Docker CAN plugin | CAN bus between RPK2 and platform-sim | Physical CAN bus on the truck |

### IP Address Assignments

| Container | Onboard (eno1) | Offboard (eno2) | Other |
|-----------|---------------|-----------------|-------|
| rpk1 | `10.10.10.110` | `10.10.1.110` | — |
| rpk2 | `10.10.10.111` | `10.10.1.111` | CAN network |
| rpk3 | `10.10.10.112` | `10.10.1.112` | — |
| vas-aht | — | `10.10.1.115` | — |
| platform-sim | `10.10.10.55` | `10.10.1.55` | CAN network |
| test-manager | `10.10.10.56` | `10.10.1.56` | local-fms-network |
| avi-radio | — | `10.10.1.2` | `172.18.50.1` (primary), plus dedicated IPs per container |

### NAT and Port Forwarding (avi-radio)

The avi-radio container performs Network Address Translation using per-container dedicated IPs on the local-fms-network. Each onboard container has its own external IP, so traffic is routed per-container rather than requiring port-specific forwarding:

| Container | Offboard IP | Dedicated FMS IP |
|-----------|-------------|------------------|
| rpk1 | `10.10.1.110` | `172.18.50.110` |
| rpk2 | `10.10.1.111` | `172.18.50.111` |
| rpk3 | `10.10.1.112` | `172.18.50.112` |
| vas-aht (motium) | `10.10.1.115` | `172.18.50.115` |
| platform-sim | `10.10.1.55` | `172.18.50.55` |
| test-manager | `10.10.1.56` | `172.18.50.56` |

For each container, SNAT rewrites the source address of outgoing traffic to its dedicated FMS IP, and DNAT rewrites the destination of incoming traffic to its offboard IP.

Explicit port forwarding is additionally set up for web interfaces and SSH access (especially for Windows users who cannot directly access local-fms-network):

| Port | Protocol | Destination | Service |
|------|----------|-------------|---------|
| 8009 | TCP | rpk2 | CIC web interface |
| 8123 | TCP | platform-sim | T264 Sim web interface |
| 2020 | TCP | rpk1:22 | SSH |
| 2021 | TCP | rpk2:22 | SSH |
| 2022 | TCP | rpk3:22 | SSH |
| 2025 | TCP | motium:22 | SSH |

## Interface Naming System

Docker assigns default interface names like `eth0`, `eth1` to containers. The RTK service `apply-systemd-networkd-config.service` (part of the base images) runs at container boot to rename these interfaces to match the systemd-networkd configuration files in `/etc/systemd/network/`.

The script (`/usr/bin/apply_systemd_networkd_config.py`) works by:
1. Reading all `.network` files in `/etc/systemd/network/`
2. Extracting `[Match] Name=` as the **target interface name**
3. Finding the existing Docker interface (`eth0`, etc.) by matching the `[Network] Address=` IP
4. Renaming the Docker interface to the target name using `ip link set`

### Interface Name Convention

| Container | Onboard Interface | Offboard Interface |
|-----------|------------------|--------------------|
| rpk1 | `eno1` | `eno2` |
| rpk2 | `eno1` | `eno2` |
| rpk3 | `eno1` | `eno2` |
| vas-aht | — | `enp0s29f1` |
| platform-sim | `eno1` | `eno2` |

### Important: Glob Patterns in Name= Are Not Supported

The `apply-systemd-networkd-config.service` script reads `Name=` values **literally**. On real hardware, `systemd-networkd` treats `Name=enp*` as a glob pattern. In Docker Bench, the script would rename the interface to the literal string `enp*` (with asterisk). This was the root cause of FX-8560.

All Docker Bench network configs must use **exact** interface names (e.g. `Name=eno2`, `Name=enp0s29f1`), not glob patterns. The RPK containers handle this by removing the base image's `20-wired.network` (which contains `Name=enp*`) and replacing it with exact-name configs (`10-eno1.network`, `20-eno2.network`). The VAS AHT Dockerfile patches `20-wired.network` in place with `sed` to set `Name=enp0s29f1` (matching site configuration).

## IP Address Remapping System

Each container runs an `overwrite-ip-address-config.service` at boot that rewrites IP addresses in configuration files. This allows the bench to work with different subnet configurations without manually editing every config file.

- Controlled by [overlay/common/etc/overwrite_ip_address_config/overwrite_ip_address_config.xml](docker_bench/overlay/common/etc/overwrite_ip_address_config/overwrite_ip_address_config.xml)
- Executed by [overlay/common/usr/bin/overwrite_ip_address_config.py](docker_bench/overlay/common/usr/bin/overwrite_ip_address_config.py)
- Searches through `/etc/systemd/network/`, `/etc/systemd/system/`,
  `/opt/amt/resources/`, `/opt/vas/config/`, `/opt/vas/share/`,
  `/opt/lme/cic/`, `/opt/lme/rpk/`, `/usr/share/t264_simulator/`,
  and `/persistent/`
- Explicitly excludes `/opt/field-commissioning/`,
  `/opt/field-sync/`, `/opt/field-signal/`, and
  `/opt/field-telemetry/` (field services use DDS on localhost only;
  no IP rewriting needed)
- Replaces default IPs with actual container IPs using environment variables

## Version Selection

### CIC Version (rpk2)

- CIC tarballs are stored in `docker_bench/overlay/rpk2/persistent/`
- The `.env` variable `CIC_FIND_PATTERN` controls which version is installed (e.g. `cic*0.65*.tgz`)
- Set to `cic*.tgz` to always install the latest available version
- The `upgradeCIC.sh` script in the overlay handles installation

### RPK Version (rpk3)

- RPK tarballs are stored in `docker_bench/overlay/rpk3/persistent/`
- The `.env` variable `RPK_FIND_PATTERN` controls which version is installed (e.g. `rpk*FS65*.tgz`)
- Set to `rpk*.tgz` to always install the latest available version

### VAS:AHT Version (vas-aht)

- The `.env` variable `VAS_AHT_DOCKER_BENCH_VERSION` controls the VAS:AHT base image version
- VAS uses a separate base image (`rtk_os_docker_bench_vas_aht`) built by the VAS repository, independent of the AMT base images
- Default: pinned to a specific version (e.g. `4.2.1-master.6-0.x1a79a05d`)

### T264 Sim Version (platform-sim)

- The `.env` variable `T264_SIM_VERSION` forces a specific version (in DPKG format)
- If unset, the version bundled with the base image is used

### Docker Bench Compatibility Matrix

The authoritative source for compatible version combinations is the Confluence page:
[Docker Bench Versions Compatibility Matrix](https://fmgl-autonomy.atlassian.net/wiki/spaces/AFSENG/pages/1226080308/Docker+Bench+Versions+Compatibility+Matrix)

**Important ordering note:** The newest compatible combinations are at the **bottom** of the "Master" table, not the top. When scanning manually, verify this by checking that version numbers increase as you go down.

#### How to Fetch and Use the Compatibility Matrix

When a user asks about version compatibility, version selection, or encounters image pull/startup errors related to version mismatches, fetch the matrix from Confluence using the Atlassian MCP tool:

```
mcp_com_atlassian_getConfluencePage(
    cloudId: "fmgl-autonomy.atlassian.net",
    pageId: "1226080308",
    contentFormat: "markdown"
)
```

The response contains a markdown table under the "## Master:" heading with these columns:

| Column | Description |
|--------|-------------|
| **FMS Version** | Imperium Docker image tag (e.g. `4.1.0-master.776-0.xe4bdb8fd`) |
| **Imperium Repo Commit Hash** | Git commit to check out the Imperium repo at |
| **AMT Version** | AMT Docker Bench image tag (e.g. `0.33.0-master.47-0.x531ee13b`) |
| **AMT Repo Commit Hash** | Git commit to check out the AMT repo at |
| **T264 Sim Version** | T264 Simulator version (DPKG format); "(default)" means use the version bundled in the base image |
| **CIC Version** | CIC tarball filename pattern; "(default)" means use the latest in `overlay/rpk2/persistent/` |
| **RPK Version** | RPK tarball filename pattern; "(default)" means use the latest in `overlay/rpk3/persistent/` |
| **Workarounds/Comments** | Known issues, required workarounds, or empty if clean |

There is also a "## Release Candidates:" table with the same columns for RC builds.

#### Version Compatibility Queries

When the user asks a version-related question, fetch the page and answer using these patterns:

**"What is the latest compatible version pair?"**
- Look at the **last row** of the Master table.
- Prefer rows where the Workarounds/Comments column is empty or contains only minor notes (not "can't get the truck to move" or similar blockers).
- Report the FMS Version, AMT Version, and any default component versions (T264 Sim, CIC, RPK).

**"Is FMS version X compatible with AMT version Y?"**
- Search the table for a row matching both the FMS and AMT versions.
- If found, report the row and any workarounds.
- If not found, report that the combination is not in the matrix and suggest the nearest compatible pair(s).

**"What AMT version works with FMS version X?"**
- Search the table for rows matching the FMS version.
- There may be multiple rows (same FMS version paired with different AMT versions).
- Report all matches, noting which has the fewest workarounds.

**"What FMS version works with AMT version X?"**
- Search the table for rows matching the AMT version.
- Report all matches with their workarounds.

**"Give me a clean version pair with no workarounds"**
- Scan from the bottom of the table upward.
- Return the first (newest) row where the Workarounds/Comments column is empty.

#### Version String Anatomy

Understanding version strings helps identify compatibility:

- **FMS**: `4.1.0-master.776-0.xe4bdb8fd` → major.minor.patch-branch.buildNumber-0.xCommitHash
- **AMT**: `0.33.0-master.47-0.x531ee13b` → same pattern
- **T264 Sim**: `0.0.0~master.58~0.x83d258a2` → uses `~` instead of `-` (Debian package format)
- **CIC**: `cic_0.62.0.tgz` → tarball filename
- **RPK**: `rpk-533_20260301-175657-release-63152_FS62.1.tgz` → tarball with date and FS (Functional Safety) version

The commit hash suffix (after `0.x`) can be used to check out the corresponding Git repository at the exact commit that was tested.

#### Applying Versions

Once a compatible pair is identified, apply them as follows:

**FMS version** (Imperium side):
```powershell
# In imperium/Tools/local-environment/
./setVersion.ps1 <FMS_VERSION>
# e.g. ./setVersion.ps1 4.2.1-master.207-0.xc5d2f714
```

**AMT Docker Bench version** (AMT side):
- Set `AMT_DOCKER_BENCH_VERSION` in `docker_bench/.env`, OR
- Pass `-dockerBenchVersion <AMT_VERSION>` to Imperium's `startAsset.ps1`

**T264 Sim version** (if not "(default)"):
- Set `T264_SIM_VERSION` in `docker_bench/.env`

**CIC/RPK versions** (if not "(default)"):
- Ensure the correct tarball exists in `overlay/rpk2/persistent/` (CIC) or `overlay/rpk3/persistent/` (RPK)
- Set `CIC_FIND_PATTERN` / `RPK_FIND_PATTERN` in `docker_bench/.env` to match

**Imperium repo commit** (if the matrix specifies a different commit from the FMS version tag):
- Some rows list an Imperium Repo Commit Hash that differs from the hash in the FMS version string. This means the Docker images are from one commit but the local tooling scripts (PowerShell scripts, compose files) must be from a different commit for compatibility.
- Check out the specified commit: `cd ~/workspace/imperium && git checkout <commit_hash>`

#### Common Version Mismatch Symptoms

| Symptom | Likely Cause |
|---------|-------------|
| Image pull fails ("manifest not found") | FMS version tag doesn't exist in Artifactory for one or more services. Check the matrix for a version that has all images published. |
| Truck won't move / map sync fails | FMS↔AMT version incompatibility. The matrix notes often describe this (e.g. "can't get the truck to move"). |
| `ALL_POSE_TIMEOUT` in FMS Bridge | Known issue with several version pairs. Restart `amt.service` or `asset-dds-gateway`. Check the matrix Workarounds column. |
| RPK MAP LANE BREACH fault on startup | Known RPK issue with some versions. Clear via CIC Test Page or RCS Health Reset. |
| Path permission / hash faults (797, 849) | Do a Health Reset in RCS and delete remaining diagnostic IDs with controlled stop latched. |
| `DEADLINE_MISSED_PATH_SEGMENT_PERMISSIONS` | Restart `mine-model-distributor` and `mine-model-service`. |

## Container Capabilities and Permissions

The containers require elevated Linux capabilities to function:

| Capability | Used By | Why |
|------------|---------|-----|
| `CAP_NET_ADMIN` | All RPKs, vas-aht, platform-sim, test-manager | Network configuration, IP remapping, interface management |
| `CAP_SYS_MODULE` | All RPKs, vas-aht, platform-sim, test-manager | Kernel module loading (CAN drivers) |
| `CAP_SYS_PTRACE` | rpk1 | Process tracing for diagnostics |
| `CAP_IPC_LOCK` | rpk2, rpk3, vas-aht, platform-sim | Lock memory for real-time performance |
| `CAP_SYS_NICE` | rpk2, rpk3, vas-aht, platform-sim | Set real-time scheduling priorities |
| `CAP_SYS_TIME` | vas-aht | System time modification (required by chrony) |
| `NET_ADMIN` | avi-radio | NAT and iptables rules |
| `NET_RAW` | avi-radio | Raw socket access for network translation |

## DDS Communication

The bench uses RTI Connext DDS for inter-container communication.

### DDS Domain IDs

| Domain | Name | Used By |
|--------|------|--------|
| 20 | CIC | FMS Bridge (rpk1), CIC (rpk2), RPK (rpk3), ARCU tests |
| 30 | VAS | VAS Bridge (vas-aht), field-sync, field-signal |
| 50 | IAI | Asset Shadow (Imperium), VAS Bridge telemetry route |
| 51 | Field | field-commissioning, field-sync, field-signal, field-telemetry |

### DDS Configuration

- QoS profiles are defined in [overlay/common/persistent/USER_QOS_PROFILES.xml](docker_bench/overlay/common/persistent/USER_QOS_PROFILES.xml)
- FMS Bridge communicates externally via unicast through the avi-radio NAT
- The `ASSET_SHADOW_DDS_PARTICIPANT_ID` environment variable configures the FMS Bridge participant
- VAS:AHT communicates via DDS over the offboard network interface (UDP, no TCP ports required)
- Field services bind DDS to `127.*` (localhost) only, routing through VAS Bridge

## Spoof Scripts

Located in `docker_bench/overlay/common/persistent/`, these scripts simulate data that would come from real truck sensors or systems:

| Script | What It Simulates |
|--------|-------------------|
| `spoof_aci_pose.sh` | Vehicle position and attitude (published every 100ms) |
| `spoof_aci_robot_mode.sh` | Robot operational mode |
| `spoof_health_event_*.sh` | Various health/diagnostic events |
| `spoof_actioned_diagnostics_perception_stop.sh` | Perception system diagnostic actions |
| `spoof_health_reset_perception_stop.sh` | Perception health status reset |

## VAS:AHT Container

The `vas-aht` container runs the Vehicle Awareness System for Autonomous Haul Trucks. On the real truck, VAS:AHT runs on the Motium unit (`10.10.1.115`). It acts primarily as a network bridge — receiving commands and publishing status via DDS, with the centralised OCS handling all positioning and decision-making.

### VAS:AHT Key Details

- **Base image**: `rtk_os_docker_bench_vas_aht` (built by the VAS repository, not AMT)
- **Version variable**: `VAS_AHT_DOCKER_BENCH_VERSION` (independent of `AMT_DOCKER_BENCH_VERSION`)
- **Network**: Offboard only (`10.10.1.115`) — not connected to onboard or CAN
- **No exposed ports**: VAS:AHT communicates exclusively via DDS over UDP
- **IP remapping**: `overwrite-ip-address-config.service` scans `/opt/vas/config/` and `/opt/vas/share/` for hardcoded IPs

### Disabled Imperium Field Services

One Imperium Field .NET service is pre-installed in the VAS base OS image but is disabled in `dockerfile-vas-aht` because it is not required in Docker Bench:

| Service | Why Disabled |
|---------|-------------|
| `field-commissioning-ui.service` | Web UI for commissioning; confirmed not required in Docker Bench context (Craig Brogle) |

### Enabled Imperium Field Services

`field-commissioning.service` is enabled in Docker Bench to support manned mode commissioning workflows. It is a .NET service providing an HTTP API and DDS participant for calibration, survey import, and operator login.

**Communication path**:

- DDS domain 51 bound to `127.*` (localhost) - routes through VAS Bridge in the same container
- HTTP (Kestrel) bound to `localhost:4050` - not externally reachable
- The `172.18.*` entry in `AllowInterfacesList` is a no-op (no matching interface in Docker Bench)
- `/opt/field-commissioning/` is explicitly excluded from IP address remapping

**Verification**:

```bash
docker exec vas-aht-AHT000 systemctl status field-commissioning.service
docker exec vas-aht-AHT000 curl -s -w "\n%{http_code}" http://localhost:4050/Health/liveness
docker exec vas-aht-AHT000 curl -s http://localhost:4050/Health/version
docker exec vas-aht-AHT000 journalctl -u field-commissioning --no-pager -n 30
```

`field-sync.service` is enabled in Docker Bench to support manned mode mine model and asset data synchronisation. It provides a DDS participant for distributing mine model, area, zone, and asset state data to the in-cab display (Centurion).

**Communication path**:

- DDS domain 51 bound to `127.*` (localhost) - routes through VAS Bridge in the same container
- DDS domain 30 (additional VAS domain bridge participant)
- HTTP (Kestrel) bound to `localhost:5510` - not externally reachable
- Redis connection to `localhost:6379` (port corrected from base image default of 6380)
- `/opt/field-sync/` is explicitly excluded from IP address remapping

**Expected warnings (non-fatal in standalone Docker Bench)**:

- gRPC `Unavailable` errors for Asset Shadow and Mine Model Distributor (FMS Core not reachable)
- RabbitMQ connection warnings (no AMQP broker in container)

**Verification**:

```bash
docker exec vas-aht-AHT000 systemctl status field-sync.service
docker exec vas-aht-AHT000 curl -s -o /dev/null -w "%{http_code}" http://localhost:5510/
docker exec vas-aht-AHT000 journalctl -u field-sync --no-pager -n 30
```

`field-signal.service` is enabled in Docker Bench to support manned mode real-time data delivery to Centurion (the in-cab display). It hosts a SignalR hub serving operational data (assignments, materials, notifications, asset state, etc.) from Redis to connected SignalR clients.

**Communication path**:

- DDS domain 51 bound to `127.*` (localhost) - routes through VAS Bridge in the same container
- DDS domain 30 (additional VAS domain bridge participant)
- HTTP (Kestrel) bound to `localhost:5000` (default, not externally reachable)
- Redis connection to `localhost:6379` (default port, no fix needed)
- SignalR hub hosted on the Kestrel port (Centurion connects here)
- `/opt/field-signal/` is explicitly excluded from IP address remapping

**Dependencies**: `redis-server.service` (hard), `field-sync.service` (ordering only)

**Expected behaviour (normal in standalone Docker Bench)**:

- No connected SignalR clients (Centurion is not running)
- Redis reads return empty data (until field-sync populates it)
- No gRPC or RabbitMQ errors (field-signal does not connect to external services)

**Verification**:

```bash
docker exec vas-aht-AHT000 systemctl status field-signal.service
docker exec vas-aht-AHT000 curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/
docker exec vas-aht-AHT000 journalctl -u field-signal --no-pager -n 30
```

`field-telemetry.service` is enabled in Docker Bench to support the health event pipeline from vehicle telemetry to the in-cab display. It subscribes to telemetry data via DDS (domain 51), extracts health events, and stores them in Redis for consumption by field-signal.

**Communication path**:

- DDS domain 51 bound to `127.*` (localhost) - subscribes to `/telemetry` topic on the field domain
- HTTP (Kestrel) bound to `localhost:4200` (set via systemd drop-in to avoid port 5000 conflict with field-signal)
- Redis connection to `localhost:6379` - stores health events at `LocalAsset:FieldHealth`
- `/opt/field-telemetry/` is explicitly excluded from IP address remapping

**Operating mode**: DDS input mode (`UseDdsForTelemetryData: true`) is the production default. No RaptorCore hardware required.

**Dependencies**: `redis-server.service` (hard)

**Expected behaviour (normal in standalone Docker Bench)**:

- DDS participant on domain 51 subscribes to `/telemetry` topic
- Redis key `LocalAsset:FieldHealth` exists but is empty
  (ZCARD = 0) because telemetry data arrives on VAS domain 30 via
  VAS Bridge but field-telemetry subscribes on field domain 51; no
  domain 30→51 bridge exists in standalone Docker Bench
- Health events would be populated when running with Imperium
  local-env (which bridges telemetry to domain 51)
- No hardware errors, no gRPC errors, no RabbitMQ dependency

**Verification**:

```bash
docker exec vas-aht-AHT000 systemctl status field-telemetry.service
docker exec vas-aht-AHT000 curl -s -o /dev/null -w "%{http_code}" http://localhost:4200/
docker exec vas-aht-AHT000 journalctl -u field-telemetry --no-pager -n 30
```

The remaining disabled service (`field-commissioning-ui`) is not required in Docker Bench.

In Imperium, the FMS-to-VAS integration path is: FMS Core -> Asset Shadow (separate container) -> DDS via avi-radio NAT -> VAS:AHT. Field services are handled externally by dedicated Imperium containers on `local-fms-network`.

### VAS:AHT Dockerfile Setup

1. Installs Netskope CA certificates
2. Copies shared overlay files (SSH keys, QoS profiles, spoof scripts)
   to `/persistent/`
3. Sets up SSH access for `root` and `rtkuser` accounts
4. Installs and enables `overwrite-ip-address-config.service`
5. Patches `20-wired.network` to replace glob `Name=enp*` with exact
   `Name=enp0s29f1` (FX-8560 — the base image uses a glob that
   `apply-systemd-networkd-config.service` reads literally)
6. Sets `registration_state="Measured"` in
   `/etc/robot_model/robot_model.xml` (base image ships with
   `"Default"`, causing nodes to exit)
7. Sets `robot_class="DumpTruck"` in
   `/etc/robot_model/robot_model.xml` (base image ships with
   `"Undefined"`)
8. Disables `field-commissioning-ui.service` (not required in Docker
   Bench)
9. Fixes field-sync Redis port (base image uses 6380, VAS:AHT Redis
   runs on 6379)
10. Fixes field-telemetry Kestrel port (base image defaults to 5000,
    conflicts with field-signal; set to 4200 via systemd drop-in)

## Troubleshooting Workflows

### Bench Won't Start

1. Check Docker version: requires >= 27.0.3. Run `docker --version`.
2. Verify the Docker CAN plugin is installed: `docker plugin ls`. The `run_tests.sh` script installs it automatically.
3. Check that base images are available: `docker images | grep rtk_os_docker_bench`.
4. Verify `.env` has valid `AMT_DOCKER_BENCH_VERSION` (e.g. `latest-master`).
5. Check for port conflicts on the host: `ss -tlnp | grep -E '8009|8123|2020|2021|2022'`.

### Container Crashes or Won't Stay Running

1. Check logs: `docker compose logs <service>` (e.g. `docker compose logs rpk1`).
2. Check exit code: `docker inspect <container> --format='{{.State.ExitCode}}'`.
3. Verify the `overwrite-ip-address-config` service ran successfully — IP mismatches cause failures downstream.
4. For rpk2/rpk3: check that the CIC/RPK tarball matched the `FIND_PATTERN` and installed correctly.
5. Shell into a failed container interactively: `docker run -it --entrypoint /bin/bash <image>`.

### Services Not Ready (run_tests.sh Timeout)

The test script waits for these processes:

**rpk1**: `rtk_launcher`, `rtk_log_recorder`, `amt_diagnostics_watchdog`, `mine_model_adapter`, `task_spooler`, `blob_sync_node`, `fms_bridge`

**platform-sim**: `/usr/bin/t264_simulator`

If the readiness check times out:
1. Shell into the container: `docker compose exec rpk1 bash`.
2. Check `systemctl status amt.service` (rpk1) or the relevant service.
3. Check `journalctl -u amt.service --no-pager -n 50` for errors.
4. Verify DDS licence is present and valid (RTI Connext).

### Networking Issues Between Containers

1. Verify containers are on the correct networks: `docker network inspect <network>`.
2. Test connectivity: `docker compose exec rpk1 ping 10.10.10.111` (rpk2 onboard).
3. Check that applications bind to `0.0.0.0`, not `127.0.0.1`.
4. For DDS issues: verify QoS profiles match across containers and domain ID is consistent.
5. For FMS connectivity: check avi-radio NAT rules with `docker compose exec avi-radio iptables -t nat -L -n`.
6. If an interface has an unexpected name (e.g. `enp*` with a literal asterisk), check `/etc/systemd/network/` for glob patterns in `Name=`. The `apply-systemd-networkd-config.service` reads `Name=` literally — use exact names only. See the Interface Naming System section.

### CAN Bus Issues

1. Verify the Docker CAN plugin is running: `docker plugin ls`.
2. Check CAN interfaces inside containers: `docker compose exec rpk2 ip link show`.
3. Decode CAN messages from platform-sim:
   ```bash
   docker compose exec platform-sim bash -l -c "candump vcan10 | cantools decode --single-line /t264-sim/libraries/dbc/DBW_OAL.dbc"
   ```

### Build Failures

1. Check if base images exist: the Dockerfiles expect pre-built `rtk_os_docker_bench_*` images.
2. Before changing `AMT_DOCKER_BENCH_VERSION`, consult the Docker Bench Compatibility Matrix section above. Fetch the matrix from Confluence and pick a known-compatible combination (newest compatible entries are at the bottom of the table).
3. Verify Netskope CA certificate is accessible (used for SSL in all containers).
4. For test-manager: ensure `USER_GITHUB_PAT` is set and the GitHub token has `repo`, `read:org`, `read:user` permissions with SSO enabled.
5. Check that overlay files referenced in `COPY` directives exist at the expected paths.

## Useful Commands

| Task | Command |
|------|---------|
| Start the bench | `cd docker_bench && docker compose up --build -d` |
| Start (force pull latest images) | `cd docker_bench && docker compose up --build --pull always -d` |
| Start with test-manager | `docker compose --profile test-manager up --build -d` |
| Stop the bench | `docker compose down` |
| View all logs | `docker compose logs -f` |
| View one service's logs | `docker compose logs -f rpk1` |
| Run automated tests | `./run_tests.sh` |
| SSH into rpk1 | `ssh -p 2020 rtkuser@localhost` or `docker compose exec rpk1 bash` |
| SSH into rpk2 | `ssh -p 2021 rtkuser@localhost` |
| SSH into rpk3 | `ssh -p 2022 rtkuser@localhost` |
| SSH into vas-aht (motium) | `ssh -p 2025 rtkuser@localhost` or `docker compose exec vas-aht bash` |
| CIC web UI | Open `http://localhost:8009` |
| T264 Sim web UI | Open `http://localhost:8123` |
| Run ARCU tests manually | `docker exec -itu rtkuser rpk1-AHT000 /opt/amt/bin/arcu -d 20 -i /opt/amt/share/arcu/arcu_config.xml` |
| Check container readiness | `docker ps --format 'table {{.Names}}\t{{.Status}}'` |
| Inspect NAT rules | `docker exec avi-radio-AHT000 iptables -t nat -L -n` |

## Imperium Integration

Docker Bench can integrate with the Imperium local environment for end-to-end testing:

- Use `startAsset.ps1 -useDockerBench` to connect Imperium to the bench
- The asset ID must be configured in `.env` to match the Imperium environment (e.g., `ASSET_ID=AHT001`) with `IsAutonomousAsset` set to `true`
- The Imperium startup script (`startAssetDockerBench.ps1`) generates an `.env-asset-{ASSET_ID}-docker-bench` file with asset-specific network settings from `assets.json`
- An **Asset Shadow** container (on `local-fms-network`) bridges FMS Core services to Docker Bench via DDS through avi-radio
- VAS:AHT integrates via the same avi-radio NAT path — its offboard IP (`OFFBOARD__MOTIUM__IP`) is SNAT/DNAT'd to a dedicated FMS IP (`LOCAL_FMS_NETWORK__AVI_RADIO_MOTIUM__IP`)
- SSH access to VAS:AHT is available on port 2025 via avi-radio port forwarding

## Known Bugs

### RPK Map Lane Breach Stuck / Unclearable (APADA-14702)

**Details**: https://fmg-lme-autonomy.atlassian.net/browse/APADA-14702

**Observed with**: FMS 4.1.0-rc.130 (April 2026)

**Symptom**: CIC raises a repeated "RPK map lane breach" diagnostic that activates and deactivates repeatedly while the truck is driving manually inside a locked AOZ. Once the AOZ is unlocked, the diagnostic clears from CIC — but the FMS retains the health event as unclearable (`IsClearable = false`, event type `BOUNDARY_INTERACTION`). The "RPK map lane breach" persists in the Asset Details panel and survives mode transitions (Manual → Autonomy). Standard RCS Health Reset and latching/unlatching do not clear it.

**Root cause**: Under investigation. The health event published by CIC/RPK is recorded in RCS with `IsClearable = false`. Once in this state, the normal "Clear to Proceed" action is not available in the RCS UI.

**Workaround** (requires FMS database access):

1. Stop the RCS service:
   ```bash
   docker service scale fms_robot-control-service=0
   ```

2. Clear restrictions in the RCS database:
   ```sql
   UPDATE [RobotHealth_Eli_Int].[dbo].[RobotControls]
   SET [RestrictionState] = N'{"Restrictions":[]}'
   WHERE [AssetIdentifier] = '<ASSET_ID>';
   ```

3. Clear health events in the RCS database:
   ```sql
   UPDATE [RobotHealth_Eli_Int].[dbo].[HealthEvents]
   SET [IsClearable] = 1
   WHERE [AssetIdentifier] = '<ASSET_ID>'
     AND [EventType] = 'BOUNDARY_INTERACTION';
   ```

4. Restart the RCS service:
   ```bash
   docker service scale fms_robot-control-service=1
   ```

**Notes**:
- Replace `<ASSET_ID>` with the actual asset identifier (e.g. `DT5395`)
- A simpler but less targeted alternative is to spoof a clearable diagnostic via RCS with `"isResettable": true` and `"responseAction": "Proceed"` — but this was observed to not work for this specific event
- This issue may also appear during Docker Bench integration testing with Imperium when AOZ locking scenarios are tested

## FMS Integration Lessons (FX-8520)

Lessons learned from the FX-8520 refuelling integration test development, relevant to any Docker Bench + FMS testing:

### Eliwana Seed Data Issues

The Eliwana mine model seed data (`seedFMS.ps1`) has several problems for refuelling tests:

| Problem | Impact | Workaround |
|---------|--------|------------|
| ELI_REFUEL area type is `RefuelBay` (enum=1) | TM's `IsDynamicArea()` filter ignores it entirely | Delete and recreate as `Refuel` (enum=6) |
| Entry/exit lanes share the same endpoint (co-located) | Drive-through path planning is mathematically impossible | Create new N→S drive-through lanes via mine model DEBUG API |
| Area polygon ~52 m × 26 m | Fails minimum inscribed circle requirement (20 m radius) for `Refuel` type | Use 120 m × 120 m boundary |

### Coordinate System

All mine model coordinates are in **centimetres** (mine grid). NTS geometry functions divide by 100 internally when computing metric distances. When creating lanes or boundaries via the API, all coordinate values must be in centimetres.

### Traffic Manager Seeding Behaviour

* TM seeds its area read model **once on startup** using Polly retry (exponential backoff, 15s cap)
* TM's health check passes **independently** of seeding completion — a healthy TM does NOT mean areas are loaded
* If `seedFMS.ps1` runs AFTER TM starts, TM never ingests the areas. Always restart TM after bulk seeding:
  ```bash
  docker restart traffic-manager
  ```
* Poll `GET /areas/{areaId}/state` for up to 180s to confirm ingestion

### Spatial Association Requires State Change

The spatial-association-service only fires entry/exit events on position **changes**. If an asset was already at the target coordinates from a previous run:

1. Teleport asset **outside** the area (offset by ≥ 200 m)
2. Wait 3-5 seconds for the exit event
3. Teleport asset to the target position inside the area
4. Wait for the entry event

Without this pattern, the asset is never detected in the area.

### Mine Model DEBUG API Notes

* `POST /DEBUG/Lane` creates a lane AND auto-generates child LaneSegment(s)
* The response structure is `.lane.segments[]` — NOT `.laneSegments[]`
* Lane segment IDs in the response are what you pass to `POST /Area` as entry/exit segment references
* `NTS Polygon.Contains()` uses DE-9IM Interior model: points exactly on the boundary are **excluded**. Queue points must be offset ≥ 1 m (100 cm) from edges.
* `POST /Area` requires `controlBehaviors` as a JSON-encoded string field within the request body, not a nested object

### PowerShell Serialization Gotchas

When scripting mine model REST calls from PowerShell:

* `Invoke-RestMethod` auto-deserializes and flattens nested JSON (GeoJSON, lane segments). Use `Invoke-WebRequest` + `ConvertFrom-Json` for complex responses.
* GeoJSON coordinate arrays must be built as here-strings, NOT via `ConvertTo-Json` (which double-serializes nested arrays).
* The `contentType` parameter must be `"application/json"` — PowerShell does not default to this.

### `-dockerBenchUseLatest` Artifactory Risk

The `-dockerBenchUseLatest` parameter queries the Artifactory **Storage REST API**, not the Docker registry. `docker login` success does NOT guarantee Storage API access (different backends). The API frequently returns **504 Gateway Timeout** during CI load.

**Recommendation:** Always use hardcoded default versions from the compatibility matrix.

### ACI V1.0 → V1.1 Breaking Change Boundary

| FMS Version Threshold | Minimum AMT Version | ACI Version |
|----------------------|---------------------|-------------|
| < `4.2.1-master.278` | Any AMT version | V1.0 |
| >= `4.2.1-master.278` | `0.34.0-master.24` | V1.1 |

FMS and AMT versions **must** be updated together when crossing this boundary. The default test versions (FMS `.207` + AMT `.16`) are below the threshold (V1.0).

### VAS:AHT Mode-Gated Telemetry

VAS:AHT only forwards fuel telemetry to FMS when the truck is in **MANUAL** mode:

* In AUTONOMY mode: fuel telemetry is processed but NOT forwarded (mode gate blocks it)
* In MANUAL mode: fuel telemetry flows VAS:AHT → DDS domain 50 → Asset Shadow → FMS

This is intentional — autonomous refuelling detection requires the truck to be stationary in MANUAL mode. If fuel telemetry never appears in FMS, verify the truck's robot mode state is MANUAL.

### SQL Workarounds for Docker Bench FMS

* `seedFMS.ps1` does NOT reliably set `PasswordHash` — write it directly via SQL UPDATE
* `SET QUOTED_IDENTIFIER ON` is required before any UPDATE on `AspNetUsers` (filtered indexes)
* `stopAll.ps1` does NOT remove Docker networks — orphaned `local-fms-network` blocks subsequent `startSql.ps1`. Clean up with `docker network rm local-fms-network`

## References

- [Docker Bench Documentation](docs/docker_bench/index.md)
- [AMT T264 Docker Bench (Confluence)](https://fmgl-autonomy.atlassian.net/wiki/spaces/PROJ/pages/889520682/AMT+T264+Docker+Bench#START-HERE)
- [Imperium Local Environment](https://github.com/fmgl-autonomy/imperium/tree/master/Tools/local-environment)
- [Docker official documentation](https://docs.docker.com/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Docker Compose reference](https://docs.docker.com/compose/compose-file/)

<!-- Copyright 2026 Fortescue Ltd. All rights reserved. -->
