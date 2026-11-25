---
name: imperium-docker-bench-expert
description: 'Specialised skill for running and troubleshooting Docker Bench within the Imperium FMS local development environment. Use when asked about Imperium Docker Bench, AMT Docker Bench in the context of Imperium, startAssetDockerBench, startAsset -useDockerBench, asset-docker-compose files, .env-asset-AHT001-docker-bench, .env-asset-AHT002-docker-bench, Docker Bench networking in Imperium, AVI radio NAT in Imperium local-environment, CIC/RPK version selection for Imperium assets, DDS configuration for Docker Bench assets, diagnosing Docker Bench assets, testEliwanaCrusherDockerBench, or any issue combining Docker Bench containers with FMS services. Explains at any level from non-technical to highly technical.'
---

# Imperium Docker Bench Expert

Specialised skill for understanding, configuring, running, and troubleshooting the AMT Docker Bench within the Imperium FMS local development environment. This skill combines domain knowledge from the `imperium-expert`, `docker-expert`, and `docker-bench-expert` skills, focused specifically on how Docker Bench integrates with Imperium's tooling and services.

## When to Use This Skill

* User asks about running Docker Bench assets in Imperium's local environment
* User asks about `startAssetDockerBench.ps1`, `startAsset.ps1 -useDockerBench`, or `stopAssetDockerBench.ps1`
* User has networking issues between Docker Bench containers and FMS services
* User asks about `.env-asset-AHT001-docker-bench`, `.env-asset-AHT002-docker-bench`, or asset-docker-compose files
* User wants to understand how the Docker Bench containers communicate with FMS Core services
* User asks about diagnosing Docker Bench assets (`diagnoseAssetDockerBench.ps1`)
* User asks about running the Eliwana crusher test with Docker Bench
* User asks why a refuel assignment is cancelled or stuck after dispatch in Docker Bench
* User needs to understand the network topology when Docker Bench runs alongside FMS services
* User asks about DDS, CIC, RPK, or T264 Sim configuration in the Imperium context
* User wants to understand the relationship between `assets.json` and Docker Bench networking

## Adjusting Detail Level

Match the explanation depth to the user's request:

* **Non-technical**: What Docker Bench does, why it exists, what problem it solves for FMS development
* **Overview**: How the containers map to truck hardware, how they connect to FMS services
* **Technical**: Network topology, port mappings, environment variables, startup scripts
* **Deep technical**: NAT rules, DDS participant IDs, IP remapping, iptables verification, mode change orchestration

## How Docker Bench Fits into Imperium

### The Big Picture

Imperium's local development environment (in `Tools/local-environment/`) runs the entire FMS as Docker containers: SQL Server, Redis, RabbitMQ, 40+ FMS Core services, Office, and Field. Docker Bench adds a realistic simulation of the T264 autonomous haul truck's onboard computers to this environment, enabling end-to-end testing of the full autonomous haul cycle without physical hardware.

### Without Docker Bench

FMS developers typically use Robot Simulator (a lightweight .NET service) to simulate autonomous assets. Robot Simulator is fast and simple but does not run the real onboard software.

### With Docker Bench

Docker Bench runs the actual AMT (Autonomy Management Toolkit), CIC (Control IC), RPK (Robot Perception Kernel), and Motium software inside containers, providing production-like fidelity for testing FMS interaction with the truck's onboard systems. Currently supports up to four simultaneous assets (AHT001-AHT004).

## References

For detailed information, consult the following reference files:

* [Architecture and Networking](./references/architecture-and-networking.md) - Container topology, network layout, IP addressing, NAT and port forwarding
* [Configuration and Startup](./references/configuration-and-startup.md) - Environment files, assets.json, startup scripts, version selection
* [Diagnostics and Troubleshooting](./references/diagnostics-and-troubleshooting.md) - Diagnosing issues, mode changes, health checks, common problems
* [Testing Workflows](./references/testing-workflows.md) - Eliwana crusher test, load/dump circuits, multi-asset scenarios, refuelling test
* [testRefuelDockerBench.ps1](./references/testRefuelDockerBench.ps1) - Full source of the refuelling integration test script

## Refuel Stall Workflow (FX-8520)

For `testRefuelDockerBench.ps1`-style scenarios that stall in guided refuel
arrival waits, use this proven order:

1. Confirm area and goalpoint are open in TM state.
2. Confirm asset mode in Robot Control (Autonomy expected for travel).
3. Confirm assignment lifecycle in Assignment Aggregator.
4. Tail TM logs for dispatch handler messages.

### High-confidence cancellation signature

If you see both:

- `No MoveToArea instruction found for "LoadAreaId"` / `"DumpAreaId"`
- immediate `DispatchCancelledEvent`

then prioritise assignment payload/contract validation over repeated small spawn
yaw tweaks.

### Spawn pose best practice (Docker Bench assets)

When setting startup pose for refuel test assets, use the entry lane midpoint
centerpoint from Mine Model `PathSegment` data:

- lane id from TM `entryPathPoint.laneSegmentId`
- midpoint point (`count//2`) for `X`/`Y`
- tangent heading from adjacent midpoint points (`atan2`)

This avoids end-of-lane overhang and produces more repeatable dispatch behavior.
