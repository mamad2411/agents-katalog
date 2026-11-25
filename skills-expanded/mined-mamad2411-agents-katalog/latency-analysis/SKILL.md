# Skill: Latency Analysis (ntsh_latency-analysis)

Diagnose network latency issues using hop-by-hop analysis, RTT baselines, jitter measurement, and TCP performance tuning.

---

## Hop-by-Hop Analysis with traceroute / mtr

### traceroute
Sends packets with incrementing TTL values to discover each hop in the path. Each hop decrements TTL by 1 and returns ICMP Time Exceeded when TTL reaches 0.

```bash
# Standard traceroute (ICMP on Windows, UDP on Linux)
traceroute 10.0.2.5          # Linux
tracert 10.0.2.5             # Windows

# TCP traceroute — bypasses ICMP-filtering firewalls
traceroute -T -p 443 10.0.2.5    # Linux — uses TCP SYN

# Set max hops and wait time
traceroute -m 20 -w 2 10.0.2.5

# Use specific source interface
traceroute -i eth0 10.0.2.5
```

### Interpreting traceroute Output
```
 1  10.0.1.1     0.5ms   0.4ms   0.5ms    # Local gateway
 2  10.100.0.1   1.2ms   1.1ms   1.3ms    # ISP edge
 3  * * *                                  # ICMP filtered (not necessarily a problem)
 4  72.14.233.1  15.2ms  15.1ms  15.3ms   # ISP backbone
 5  10.0.2.5     16.0ms  15.9ms  16.1ms   # Destination
```

- `* * *`: The hop is filtering ICMP — **not** necessarily packet loss. Check if subsequent hops respond normally.
- **Latency increase at a specific hop**: If latency jumps significantly (e.g., hop 4 is 15ms but hop 5 is 150ms), the link between those hops is the bottleneck.
- **Consistent latency across all hops**: Normal — each hop adds its processing time.
- **Asymmetric paths**: Forward and reverse paths may differ. traceroute only shows the forward path.

### mtr (My Traceroute)
Combines ping and traceroute for continuous monitoring, showing per-hop loss and latency statistics over time.

```bash
# Run 100-packet report
mtr --report -c 100 10.0.2.5

# Report with wide output (show hostnames and IPs)
mtr --report-wide -c 200 10.0.2.5

# TCP mode on port 443
mtr --report -T -P 443 -c 100 10.0.2.5

# No DNS resolution (faster)
mtr --report --no-dns -c 100 10.0.2.5
```

### Interpreting mtr Output
```
HOST                   Loss%   Snt   Last   Avg  Best  Wrst StDev
1. 10.0.1.1             0.0%   100    0.5   0.5   0.3   0.8   0.1
2. 10.100.0.1           0.0%   100    1.2   1.3   1.0   2.1   0.2
3. 72.14.233.1          5.0%   100   15.1  15.5  14.8  22.0   1.5
4. 10.0.2.5             0.0%   100   16.0  16.2  15.5  18.0   0.5
```

- **Loss at an intermediate hop but not at the destination**: The intermediate hop deprioritizes ICMP responses under load (ICMP rate limiting). Not a real problem.
- **Loss at the destination**: Real packet loss — investigate the last-mile link or destination host.
- **High StDev (jitter)**: Indicates inconsistent path quality — possible congestion, queuing, or path changes.

---

## RTT Baselines Per Cloud Environment

| Path Type | Expected RTT | Notes |
|-----------|-------------|-------|
| Intra-AZ (same zone) | < 1ms | Within the same data center |
| Intra-region (cross-AZ) | 1–2ms | Between availability zones in the same region |
| Cross-region (same continent) | 20–60ms | Depends on geographic distance |
| Cross-region (intercontinental) | 60–200ms | US to Europe ~80ms, US to Asia ~150ms |
| VPN over internet | 20–100ms+ | Adds encryption overhead + internet path variability |
| ExpressRoute / Direct Connect | 5–30ms | Lower and more consistent than internet-based VPN |
| On-premises to cloud (same metro) | 2–10ms | Via colocation meet-me facility |

**When to escalate**: If observed RTT exceeds baseline by > 50% consistently over 30+ minutes, investigate path quality (mtr), check for congestion (interface utilization), and consider cloud provider backbone issues.

---

## Jitter Measurement

Jitter is the variation in latency between packets. High jitter affects real-time applications (VoIP, video conferencing) even when average latency is acceptable.

```bash
# Measure jitter with mtr — look at StDev column
mtr --report -c 500 target.example.com

# Measure jitter with ping — calculate manually
ping -c 100 -i 0.1 target.example.com | tail -1
# "min/avg/max/mdev = 15.0/16.2/22.0/1.5 ms"
# mdev (mean deviation) ≈ jitter

# Acceptable jitter thresholds:
# VoIP: < 30ms jitter (ITU-T G.114)
# Video conferencing: < 30ms jitter
# Interactive applications: < 50ms jitter
# Batch/non-interactive: jitter not critical
```

---

## TCP Window Size Impact

TCP throughput is limited by the receive window size and RTT:
```
Max Throughput = Window Size / RTT
```

**Example**: 64 KB window, 50ms RTT:
```
Max Throughput = 65,536 bytes / 0.050s = 1,310,720 bytes/s ≈ 10 Mbps
```

This means a single TCP connection over a 50ms path cannot exceed ~10 Mbps with a 64 KB window, regardless of available bandwidth.

### Solutions
- **TCP Window Scaling** (RFC 7323): Enables windows up to 1 GB. Enabled by default on modern OS but may be disabled by middleboxes or legacy systems.
- **Increase receive buffer**: `sysctl -w net.core.rmem_max=16777216` (Linux).
- **Parallel connections**: Use multiple TCP connections to aggregate throughput (common in tools like azcopy, s3 cp --parallel).

```bash
# Check current TCP window scaling on Linux
sysctl net.ipv4.tcp_window_scaling
# Should be 1 (enabled)

# Check max receive buffer
sysctl net.core.rmem_max
# Increase if needed: sysctl -w net.core.rmem_max=16777216
```

---

## Nagle's Algorithm

Nagle's algorithm (RFC 896) coalesces small TCP segments to reduce overhead. It delays sending small packets until a previous packet is ACKed or enough data accumulates to fill a segment.

### When Nagle Causes Latency
- Interactive applications sending small messages (chat, gaming, real-time control).
- Combined with TCP Delayed ACK (receiver waits up to 200ms before sending ACK), Nagle can cause up to 200ms added latency per small message.

### Disabling Nagle (TCP_NODELAY)
```bash
# Application level — set TCP_NODELAY socket option
# Python: socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
# Node.js: socket.setNoDelay(true)
# Go: conn.SetNoDelay(true)

# Verify with packet capture — look for small packets sent immediately
# vs. coalesced larger packets with delay
```

**Analysis only — verify against vendor documentation before applying.**
