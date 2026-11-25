---
name: nomad
version: 1.1.0
description: HashiCorp Nomad cluster orchestration. Query jobs, nodes, allocations, deployments, and services. Run, stop, and scale jobs. Monitor logs and troubleshoot workloads. Use for container orchestration, job scheduling, and cluster management.
homepage: https://github.com/danfedick/nomad-skill
metadata: {"clawdbot":{"emoji":"📦","requires":{"bins":["nomad"]}}}
---

# Nomad Skill

Orchestrate workloads with the HashiCorp Nomad CLI.

## Requirements

- `nomad` CLI installed
- `NOMAD_ADDR` environment variable (default: http://127.0.0.1:4646)
- `NOMAD_TOKEN` if ACLs are enabled

## Jobs

### List & Status
```bash
nomad job status                      # List all jobs
nomad job status <job-id>             # Job details
nomad job status -verbose <job-id>    # Detailed info
```

### Run & Stop
```bash
nomad job run job.nomad.hcl           # Deploy job
nomad job run -check-index=X job.hcl  # Deploy only if index matches
nomad job plan job.nomad.hcl          # Dry-run, show changes
nomad job stop <job-id>               # Stop job (leaves history)
nomad job stop -purge <job-id>        # Stop and remove completely
```

### Scale
```bash
nomad job scale <job-id> <group> 5    # Scale to 5 instances
nomad job scale -detach <job-id> <group> 3
```

### Dispatch (Parameterized Jobs)
```bash
nomad job dispatch <job-id>
nomad job dispatch -meta key=value <job-id>
nomad job dispatch -meta key=value <job-id> @payload.json
```

### History & Versions
```bash
nomad job history <job-id>
nomad job revert <job-id> <version>
nomad job deployments <job-id>
```

### Inspect
```bash
nomad job inspect <job-id>            # Full job spec JSON
nomad job validate job.nomad.hcl      # Validate syntax
```

## Allocations

```bash
nomad job allocs <job-id>             # List job allocations
nomad alloc status <alloc-id>         # Allocation details
nomad alloc status -short <alloc-id>  # Summary only
```

### Logs
```bash
nomad alloc logs <alloc-id>           # stdout
nomad alloc logs -stderr <alloc-id>   # stderr
nomad alloc logs -f <alloc-id>        # Follow
nomad alloc logs -tail -n 100 <alloc-id>
nomad alloc logs -job <job-id>        # Latest alloc logs
nomad alloc logs <alloc-id> <task>    # Specific task
```

### Exec
```bash
nomad alloc exec <alloc-id> /bin/sh
nomad alloc exec -task <task> <alloc-id> /bin/sh
nomad alloc exec -i -t <alloc-id> /bin/bash
```

### Files
```bash
nomad alloc fs <alloc-id>                    # List /
nomad alloc fs <alloc-id> /alloc/logs/       # List directory
nomad alloc fs -stat <alloc-id> /path        # File metadata
nomad alloc fs -tail -f <alloc-id> /alloc/logs/app.stdout.0
```

### Actions
```bash
nomad alloc stop <alloc-id>           # Stop allocation
nomad alloc restart <alloc-id>        # Restart all tasks
nomad alloc restart -task web <alloc-id>  # Restart specific task
nomad alloc signal -s SIGHUP <alloc-id>   # Send signal
```

## Nodes

```bash
nomad node status                     # List nodes
nomad node status <node-id>           # Node details
nomad node status -allocs <node-id>   # Show allocations
nomad node status -verbose <node-id>  # Full details
```

### Node Management
```bash
nomad node drain -enable <node-id>    # Drain for maintenance
nomad node drain -disable <node-id>   # Stop draining
nomad node eligibility -enable <node-id>   # Allow scheduling
nomad node eligibility -disable <node-id>  # Prevent scheduling
```

## Deployments

```bash
nomad deployment list
nomad deployment status <deployment-id>
nomad deployment promote <deployment-id>   # Promote canary
nomad deployment fail <deployment-id>      # Mark failed
nomad deployment pause <deployment-id>
nomad deployment resume <deployment-id>
```

## Evaluations

```bash
nomad eval list
nomad eval status <eval-id>
```

## Services

```bash
nomad service list
nomad service info <service-name>
nomad service delete <service-name>   # Force delete
```

## Namespaces

```bash
nomad namespace list
nomad namespace status <name>
nomad namespace apply -description "Prod" production
nomad namespace delete <name>
```

## Variables

```bash
nomad var list
nomad var get <path>
nomad var put <path> key=value key2=value2
nomad var put <path> @data.json
nomad var purge <path>
```

## ACLs

```bash
nomad acl policy list
nomad acl policy info <name>
nomad acl token list
nomad acl token self                  # Current token info
```

## Cluster

```bash
nomad server members                  # Raft cluster
nomad operator raft list-peers        # Raft peers
nomad agent-info                      # Local agent info
nomad operator snapshot save backup.snap
nomad operator snapshot restore backup.snap
```

## JSON Output

Add `-json` to most commands:
```bash
nomad job status -json
nomad node status -json
nomad alloc status -json <alloc-id>
```

## Filtering

Use `-filter` with expressions:
```bash
nomad job status -filter='Status == "running"'
nomad node status -filter='Status == "ready"'
nomad job allocs -filter='ClientStatus == "failed"' <job-id>
```

## Common Patterns

### Logs from latest allocation
```bash
nomad alloc logs $(nomad job allocs -json <job> | jq -r '.[0].ID')
```

### Find failed allocations
```bash
nomad job allocs <job-id> | grep -i failed
nomad eval list -filter='Status == "blocked"'
```

### Quick restart
```bash
nomad job stop <job-id> && nomad job run job.nomad.hcl
```

### Force new deployment
```bash
nomad job run -force job.nomad.hcl
```

### Exec into running container
```bash
ALLOC=$(nomad job allocs -json <job> | jq -r '.[0].ID')
nomad alloc exec -i -t $ALLOC /bin/sh
```

### Watch deployment
```bash
nomad deployment status -monitor <deployment-id>
```

### Scale to zero and back
```bash
nomad job scale <job-id> <group> 0
nomad job scale <job-id> <group> 3
```

## Environment Variables

- `NOMAD_ADDR` — API address (default: http://127.0.0.1:4646)
- `NOMAD_TOKEN` — ACL token
- `NOMAD_NAMESPACE` — Default namespace
- `NOMAD_REGION` — Default region
- `NOMAD_CACERT` / `NOMAD_CLIENT_CERT` / `NOMAD_CLIENT_KEY` — TLS config
- `NOMAD_TLS_SERVER_NAME` — TLS server name for verification

## Tips

- Use `nomad-tui` for interactive cluster management
- Use `-monitor` flag with deployments to watch progress
- Prefix alloc IDs work (e.g., `nomad alloc logs abc123` if unique)
- `-detach` returns immediately without waiting
- `-verbose` adds scheduling info and constraint details
