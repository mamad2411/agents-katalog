---
name: dns-network
description: Network debugging with DNS lookups, connectivity testing, and latency diagnosis. Use when user mentions "dns", "dig", "nslookup", "traceroute", "ping", "network debugging", "why is this slow", "connection timeout", "dns resolution", "curl timing", "network latency", "MTR", "netcat", or diagnosing network issues.
---

# DNS & Network Debugging

Practical workflows for diagnosing DNS, connectivity, and latency problems.

## DNS Lookups

### dig (preferred tool)

```bash
# A record (IPv4)
dig example.com

# Specific record types
dig example.com AAAA      # IPv6
dig example.com MX        # Mail servers
dig example.com CNAME     # Canonical name
dig example.com TXT       # TXT records (SPF, DKIM, verification)
dig example.com NS        # Nameservers
dig example.com SOA       # Start of authority

# Short output (just the answer)
dig +short example.com
dig +short example.com MX

# Query a specific DNS server
dig @8.8.8.8 example.com
dig @1.1.1.1 example.com

# Trace the full resolution path (root -> TLD -> authoritative)
dig +trace example.com

# Reverse lookup (IP to hostname)
dig -x 93.184.216.34

# Show all records you can get
dig example.com ANY +noall +answer

# Batch lookup from file (one domain per line)
dig -f domains.txt +short
```

### nslookup

```bash
nslookup example.com
nslookup example.com 8.8.8.8        # Use specific server
nslookup -type=MX example.com       # MX records
nslookup -type=TXT example.com      # TXT records
```

### host (quick and simple)

```bash
host example.com
host -t MX example.com
host 93.184.216.34                   # Reverse lookup
```

### Checking DNS Propagation

When you change DNS records, check multiple resolvers to see if the change has spread:

```bash
for dns in 8.8.8.8 1.1.1.1 208.67.222.222 9.9.9.9; do
  echo "--- $dns ---"
  dig @$dns example.com +short
done
```

Check the authoritative nameserver directly to confirm the record is correct at the source:

```bash
# Find authoritative NS
dig +short example.com NS
# Query it directly
dig @ns1.example.com example.com +short
```

## Connectivity Testing

### ping

```bash
ping example.com                     # Continuous (Ctrl+C to stop)
ping -c 5 example.com               # Send 5 packets
ping -c 5 -i 0.2 example.com       # 200ms interval between packets
ping -W 2 example.com               # 2-second timeout per packet (Linux)
ping -t 2 example.com               # 2-second timeout per packet (macOS)
```

What to look for: packet loss percentage and round-trip time variation. Consistent high latency is different from intermittent packet loss -- they point to different problems.

### traceroute / tracepath

```bash
traceroute example.com               # Show each hop to destination
traceroute -n example.com            # Skip reverse DNS (faster)
traceroute -T -p 443 example.com    # TCP traceroute on port 443
traceroute -I example.com            # Use ICMP instead of UDP
```

Read the output hop by hop. A sudden jump in latency at a specific hop identifies where the slowdown is. Stars (`* * *`) mean that hop is filtering probes -- not necessarily a problem.

### mtr (combines ping + traceroute)

```bash
mtr example.com                      # Interactive, live-updating
mtr -r -c 100 example.com           # Report mode, 100 cycles
mtr -rw -c 50 example.com           # Wide report (full hostnames)
mtr -T -P 443 example.com           # TCP mode on port 443
```

mtr is the best single tool for diagnosing path-level problems. The Loss% and Avg columns per hop tell you exactly where packets are being dropped or delayed.

## curl Timing Breakdown

This is the go-to for diagnosing "the site is slow" complaints:

```bash
curl -o /dev/null -s -w "\
    DNS lookup:  %{time_namelookup}s\n\
   TCP connect:  %{time_connect}s\n\
   TLS handshake: %{time_appconnect}s\n\
  First byte:   %{time_starttransfer}s\n\
  Total time:   %{time_total}s\n\
  HTTP code:    %{http_code}\n" \
  https://example.com
```

How to read the output:

- **time_namelookup** high (>100ms): DNS is slow. Check resolver, try 8.8.8.8.
- **time_connect - time_namelookup** high: Network path to server is slow.
- **time_appconnect - time_connect** high: TLS negotiation is slow (cert chain issues, slow server).
- **time_starttransfer - time_appconnect** high: Server is slow to generate the response (backend problem).
- **time_total - time_starttransfer** high: Large response body or slow transfer rate.

### curl verbose mode for HTTP debugging

```bash
# Full request/response headers and TLS details
curl -v https://example.com

# Even more detail (hex dump of traffic)
curl --trace - https://example.com

# Show only response headers
curl -I https://example.com

# Follow redirects and show each hop
curl -vL https://example.com 2>&1 | grep -E '< HTTP|< Location'
```

## Port Testing

### netcat (nc)

```bash
# Check if a port is open
nc -zv example.com 443
nc -zv example.com 80

# Scan a range of ports
nc -zv example.com 20-25

# With timeout
nc -zv -w 3 example.com 443

# Test UDP port
nc -zuv example.com 53
```

### Checking listening ports on local machine

```bash
# ss (modern replacement for netstat)
ss -tlnp                             # TCP listening ports with process names
ss -ulnp                             # UDP listening ports
ss -tlnp | grep :8080               # Check specific port
ss -s                                 # Summary statistics

# netstat (older but universal)
netstat -tlnp                        # TCP listening (Linux)
netstat -an | grep LISTEN            # All listening (macOS)

# lsof
lsof -i :8080                       # What process is on port 8080
lsof -i -P -n | grep LISTEN         # All listening ports
```

## tcpdump Basics

```bash
# Capture all traffic on an interface
sudo tcpdump -i eth0

# Filter by host
sudo tcpdump -i eth0 host example.com

# Filter by port
sudo tcpdump -i eth0 port 443
sudo tcpdump -i eth0 port 53        # DNS traffic

# Filter by protocol
sudo tcpdump -i eth0 tcp
sudo tcpdump -i eth0 udp and port 53

# Save to file for Wireshark analysis
sudo tcpdump -i eth0 -w capture.pcap port 443

# Read a capture file
sudo tcpdump -r capture.pcap

# Show packet contents in ASCII
sudo tcpdump -A -i eth0 port 80

# Limit capture to N packets
sudo tcpdump -c 100 -i eth0 port 443

# Common combo: DNS queries leaving this machine
sudo tcpdump -i any -n port 53
```

On macOS, use `en0` (Wi-Fi) or `en1` instead of `eth0`. Run `tcpdump -D` to list available interfaces.

## Local Configuration Files

### /etc/hosts

Static hostname-to-IP mappings. Checked before DNS.

```bash
# View current entries
cat /etc/hosts

# Add a temporary override (useful for testing before DNS changes)
echo "93.184.216.34 example.com" | sudo tee -a /etc/hosts

# Remove it when done
sudo sed -i '/example.com/d' /etc/hosts    # Linux
sudo sed -i '' '/example.com/d' /etc/hosts # macOS
```

### /etc/resolv.conf

DNS resolver configuration.

```bash
cat /etc/resolv.conf

# Typical contents:
# nameserver 8.8.8.8
# nameserver 8.8.4.4
# search mycompany.internal
```

On systems using systemd-resolved, the actual config may be managed elsewhere. Check with `resolvectl status`.

On macOS, DNS is managed by the system. Check with `scutil --dns`.

## Diagnostic Workflows

### "The site is slow"

1. Run the curl timing breakdown to isolate which phase is slow.
2. If DNS is slow: check `dig +short` time, try alternate resolvers.
3. If connect is slow: run `mtr -r -c 50` to find where latency spikes.
4. If TLS is slow: check `curl -v` for cert chain issues or protocol negotiation problems.
5. If first-byte is slow: the problem is server-side. Check application logs and server resources.
6. If transfer is slow: check response size, consider compression, test bandwidth.

### "I can't connect to the service"

1. Can you resolve the hostname? `dig +short hostname`
2. Can you reach the IP? `ping -c 3 <ip>`
3. Is the port open? `nc -zv hostname port`
4. Is something listening locally? `ss -tlnp | grep :port`
5. Is a firewall blocking? `sudo iptables -L -n` (Linux) or check security groups if cloud-hosted.
6. Is the route correct? `traceroute -n hostname`

### "DNS isn't resolving"

1. Check what resolver you are using: `cat /etc/resolv.conf` or `scutil --dns` (macOS).
2. Query the resolver directly: `dig @<resolver-ip> hostname`
3. Query a known-good public resolver: `dig @8.8.8.8 hostname`
4. If public works but local does not: local resolver or network is the problem.
5. If neither works: check if the domain actually has records: `dig +trace hostname`
6. Check for /etc/hosts overrides that might be interfering.

### "Works from my machine but not from the server"

1. Compare DNS results from both machines: `dig +short hostname`
2. Compare routes: `mtr -r -c 20 hostname` from both.
3. Check if the server has outbound firewall rules or proxy settings.
4. Check if the server uses a different resolver (corporate DNS, VPN split-tunnel).
5. Check environment variables: `env | grep -i proxy`

## Quick Reference

| Task | Command |
|---|---|
| Resolve hostname | `dig +short example.com` |
| Reverse lookup | `dig -x 1.2.3.4` |
| Check MX records | `dig +short example.com MX` |
| Trace DNS path | `dig +trace example.com` |
| Test port open | `nc -zv host 443` |
| Find what is on a port | `lsof -i :8080` |
| Listening ports | `ss -tlnp` |
| Path analysis | `mtr -r -c 50 host` |
| Capture DNS traffic | `sudo tcpdump -i any -n port 53` |
| Full curl timing | `curl -o /dev/null -s -w "dns:%{time_namelookup} connect:%{time_connect} tls:%{time_appconnect} firstbyte:%{time_starttransfer} total:%{time_total}\n" URL` |
