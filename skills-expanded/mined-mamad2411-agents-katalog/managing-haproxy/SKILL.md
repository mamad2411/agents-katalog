---
name: managing-haproxy
description: |
  Use when working with Haproxy — hAProxy load balancer management, backend
  health monitoring, frontend statistics, server status tracking, and ACL
  management. Covers session analysis, connection metrics, SSL termination
  status, and stick table inspection. Read this skill before any HAProxy
  operations — it enforces discovery-first patterns, anti-hallucination rules,
  and safety constraints.
connection_type: haproxy
preload: false
---

# HAProxy Management Skill

Monitor, analyze, and manage HAProxy load balancers safely.

## MANDATORY: Discovery-First Pattern

**Always query the stats socket or stats page before making changes. Never guess backend or frontend names.**

### Phase 1: Discovery

```bash
#!/bin/bash

HAPROXY_SOCKET="${HAPROXY_SOCKET:-/var/run/haproxy/admin.sock}"
HAPROXY_STATS_URL="${HAPROXY_STATS_URL:-http://127.0.0.1:8404/stats}"

ha_cmd() {
    echo "$@" | socat stdio "$HAPROXY_SOCKET" 2>/dev/null
}

echo "=== HAProxy Version ==="
ha_cmd "show info" | grep -E 'Name|Version|Uptime|Nbproc|Nbthread'

echo ""
echo "=== Process Info ==="
ha_cmd "show info" | grep -E 'CurrConns|MaxConn|CumConns|Idle_pct|Tasks'

echo ""
echo "=== Frontends ==="
ha_cmd "show stat" | awk -F, '$2=="FRONTEND" {printf "%-25s status=%-4s sessions=%s rate=%s/s\n", $1, $18, $5, $34}'

echo ""
echo "=== Backends ==="
ha_cmd "show stat" | awk -F, '$2=="BACKEND" {printf "%-25s status=%-4s sessions=%s\n", $1, $18, $5}'

echo ""
echo "=== Servers ==="
ha_cmd "show stat" | awk -F, '$2!="FRONTEND" && $2!="BACKEND" && NR>1 {printf "%-20s %-20s status=%-4s weight=%s checks=%s\n", $1, $2, $18, $19, $37}'
```

**Phase 1 outputs:** Frontend names, backend names, server list, health status, connection counts

### Phase 2: Analysis

Only inspect frontends, backends, and servers confirmed in Phase 1 output.

## Anti-Hallucination Rules

- **NEVER assume backend names** — always extract from `show stat` output
- **NEVER guess server addresses** — parse from running configuration
- **NEVER assume ACL names** — verify from config or `show acl`
- **NEVER assume stick table names** — list with `show table`
- **ALWAYS check stats socket availability** before issuing commands

## Safety Rules

- **READ-ONLY by default**: Use `show stat`, `show info`, `show servers state`
- **FORBIDDEN without explicit request**: `shutdown`, `disable server`, `set weight 0`
- **Drain before disable**: Use `set server BACKEND/SERVER state drain` before disabling
- **NEVER disable all servers**: Always keep at least one server active per backend
- **Config changes require reload**: Runtime changes via socket are temporary

## Core Helper Functions

```bash
#!/bin/bash

HAPROXY_SOCKET="${HAPROXY_SOCKET:-/var/run/haproxy/admin.sock}"

ha_cmd() {
    echo "$@" | socat stdio "$HAPROXY_SOCKET" 2>/dev/null
}

# Get CSV stats
ha_stats_csv() {
    ha_cmd "show stat" | grep -v '^#'
}

# Get server status for a backend
backend_servers() {
    local backend="$1"
    ha_cmd "show stat" | awk -F, -v be="$backend" \
        '$1==be && $2!="BACKEND" {printf "%-20s status=%s check=%s weight=%s\n", $2, $18, $37, $19}'
}

# Check if stats socket is accessible
check_socket() {
    if [ -S "$HAPROXY_SOCKET" ]; then
        echo "Socket OK: $HAPROXY_SOCKET"
    else
        echo "Socket not found: $HAPROXY_SOCKET"
        echo "Try: HAPROXY_SOCKET=/path/to/haproxy.sock"
    fi
}
```

## Common Operations

### Backend Health Dashboard

```bash
#!/bin/bash
echo "=== Backend Health Summary ==="
ha_cmd "show stat" | awk -F, '
    NR>1 && $2!="FRONTEND" && $2!="BACKEND" {
        backend=$1; server=$2; status=$18; check=$37
        if (status=="UP") up[backend]++
        else down[backend]=down[backend] " " server
        total[backend]++
    }
    END {
        for (b in total) {
            printf "%-25s UP=%d/%d", b, up[b]+0, total[b]
            if (down[b]) printf " DOWN:%s", down[b]
            printf "\n"
        }
    }
'

echo ""
echo "=== Last Health Check Details ==="
ha_cmd "show stat" | awk -F, '
    NR>1 && $2!="FRONTEND" && $2!="BACKEND" && $18!="UP" {
        printf "ALERT: %s/%s status=%s last_check=%s\n", $1, $2, $18, $37
    }
'
```

### Frontend Statistics

```bash
#!/bin/bash
echo "=== Frontend Connection Stats ==="
ha_cmd "show stat" | awk -F, '
    $2=="FRONTEND" {
        printf "%-25s curr_conn=%-6s cum_conn=%-10s rate=%s/s bytes_in=%s bytes_out=%s\n",
            $1, $5, $8, $34, $9, $10
    }
'

echo ""
echo "=== Request Rate (last 10 seconds) ==="
ha_cmd "show stat" | awk -F, '$2=="FRONTEND" {printf "%-25s req_rate=%s/s req_total=%s\n", $1, $34, $49}'

echo ""
echo "=== Error Rates ==="
ha_cmd "show stat" | awk -F, '
    $2=="FRONTEND" {
        ereq=$13+0; dreq=$11+0; total=$49+0
        rate=0; if(total>0) rate=ereq*100/total
        printf "%-25s errors=%d denied=%d error_rate=%.2f%%\n", $1, ereq, dreq, rate
    }
'
```

### Server Status Management

```bash
#!/bin/bash
echo "=== All Server States ==="
ha_cmd "show servers state" | awk 'NR>1 {
    printf "backend=%-20s server=%-20s addr=%-20s state=%s weight=%s\n", $4, $5, $6, $7, $8
}'

echo ""
echo "=== Session Distribution ==="
ha_cmd "show stat" | awk -F, '
    NR>1 && $2!="FRONTEND" && $2!="BACKEND" {
        printf "%-20s %-20s sessions=%-6s queued=%-4s weight=%s\n", $1, $2, $5, $3, $19
    }
'
```

### ACL and Stick Table Management

```bash
#!/bin/bash
echo "=== Configured ACLs ==="
ha_cmd "show acl" 2>/dev/null || echo "No runtime ACLs (check haproxy.cfg)"

echo ""
echo "=== Stick Tables ==="
ha_cmd "show table" | while read line; do
    table=$(echo "$line" | awk '{print $3}' | tr -d ',')
    echo "--- Table: $table ---"
    ha_cmd "show table $table" | head -20
    echo ""
done

echo ""
echo "=== Map Files ==="
ha_cmd "show map" 2>/dev/null || echo "No runtime maps configured"
```

### Connection and Session Analysis

```bash
#!/bin/bash
echo "=== Current Connections ==="
ha_cmd "show info" | grep -E 'CurrConns|MaxConn|CumConns|ConnRate|SessRate'

echo ""
echo "=== Connection Queue Status ==="
ha_cmd "show stat" | awk -F, '
    NR>1 && $2!="FRONTEND" {
        if ($3+0 > 0) printf "QUEUED: %s/%s queue=%s\n", $1, $2, $3
    }
'

echo ""
echo "=== Response Time Averages ==="
ha_cmd "show stat" | awk -F, '
    NR>1 && $2=="BACKEND" {
        printf "%-25s avg_resp=%sms last_resp=%sms\n", $1, $62, $63
    }
'
```

## Output Format

Present results as a structured report:
```
Managing Haproxy Report
═══════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Stats socket permissions**: HAProxy socket often requires root or haproxy group membership
- **Runtime vs config changes**: `set server` changes are lost on reload — always update haproxy.cfg too
- **`maxconn` per frontend vs global**: Frontend maxconn limits are independent of global maxconn
- **Health check intervals**: Short check intervals on many backends can cause CPU spikes
- **Stick table expiry**: Entries without expiry grow unbounded — always set `expire` parameter
- **SSL SNI routing**: Requires `tcp` mode on frontend — `http` mode terminates SSL before SNI is available
- **`option httpclose` vs `http-keep-alive`**: Wrong mode causes connection reuse issues or memory leaks
- **Zero-weight servers**: Setting weight to 0 drains but does not remove — new sessions may still arrive during health checks
