# Monitor Skill

## Overview
System health monitoring and alerting skill for services, resources, and infrastructure.

## Usage
```
/monitor                    # Full system health check
/monitor services           # Check running services
/monitor resources          # CPU, memory, disk usage
/monitor logs [service]     # Tail service logs
/monitor alert              # Configure alerts
/monitor report             # Generate health report
```

## Monitored Metrics
- **Services**: Backend, database, cache, web server
- **Resources**: CPU usage, RAM, disk space, network
- **Processes**: Zombie processes, high-memory processes
- **Logs**: Error patterns, crash detection

## Configuration
Edit `~/.qwen/skills/monitor/config.json` for custom monitoring.
