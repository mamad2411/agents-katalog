---
name: nmap-triage
description: Use when running or interpreting nmap output during a pentest. Triggers on nmap commands, port scanning, service enumeration. Rate-aware — every command examples respects scan_limits.
---

# Nmap Triage (Pentest Mode)

## The standard pass (always rate-capped)

```bash
sudo nmap -sC -sV -p- \
  --max-rate <ROE.scan_limits.max_packet_rate_pps> \
  --max-parallelism <ROE.scan_limits.max_concurrent_hosts> \
  -oN engagements/current/recon/<host>-tcp.nmap <host>
```

UDP top-50 (UDP is slow; never `-pU-`):

```bash
sudo nmap -sU --top-ports 50 \
  --max-rate <ROE.scan_limits.max_packet_rate_pps> \
  -oN engagements/current/recon/<host>-udp.nmap <host>
```

## Flags that are usually banned

- `--min-rate` — pushes rate up; use `--max-rate` instead
- `-T5` — "insane" timing, ~300k pps capable
- `--script "(vuln|exploit|dos|brute)*"` — vuln/exploit scripts that probe
  destructively; `--script vuln` is a banned-by-default convention in many
  ROEs, check `roe.yaml`
- `--script "dos*"` — banned by `destructive_op_guard`

If the ROE explicitly allows `--script vuln`, fine — but capture evidence
for each script's finding into the manifest.

## Port → likely service → next move

| Port | Service | Next step |
|---|---|---|
| 21 | FTP | Anonymous login attempt; version-pin for vsftpd 2.3.4 |
| 22 | SSH | Banner grab; check for password auth |
| 23 | Telnet | Banner grab; always a finding (cleartext) |
| 25,465,587 | SMTP | `VRFY` / `EXPN` user enum; STARTTLS check |
| 53 | DNS | AXFR attempt; reverse PTR sweep of the in-scope CIDR |
| 80,443,8080,8443 | HTTP/S | feroxbuster + nuclei; vhost enum if HTTPS with SNI |
| 88 | Kerberos | Domain controller; AS-REP roast attempt for `--users-file` |
| 110,143,993,995 | POP/IMAP | Banner; cleartext-auth check |
| 111,2049 | RPC/NFS | `showmount -e`; check for no_root_squash |
| 135,139,445 | SMB | `enum4linux-ng -A`; signing check via `nxc smb` |
| 161 | SNMP | `snmpwalk -v2c -c public` then `private` then a small wordlist |
| 389,636,3268,3269 | LDAP | Anonymous bind; user/group enum |
| 1433 | MSSQL | `nxc mssql --local-auth` |
| 1521 | Oracle TNS | `tnscmd10g` for SID enum |
| 3306 | MySQL | Banner; check for `--initial-rcpt` style misconfigs |
| 3389 | RDP | NLA check; cert grab |
| 5432 | PostgreSQL | Banner; check default `postgres/postgres` |
| 5985,5986 | WinRM | `evil-winrm` test once we have a credential |
| 6379 | Redis | `redis-cli ping`; CONFIG SET for write-anywhere |
| 8000,8080,8443,8888 | Web (alt) | Same as 80/443 + check for management consoles |
| 9200 | Elasticsearch | `_cat/indices`; data exposure check |
| 27017 | MongoDB | Auth check |

## Reading service+version

The "interesting" decision comes from:

- Service age: anything > 5 years out of date is a candidate.
- Service genre: management consoles, file shares, auth services, anything
  with web UI for config.
- Reachability: if it's the *only* open port on a host, escalate priority.

## What to write into findings.json

For each port:

```json
{
  "port": 445,
  "proto": "tcp",
  "service": "smb",
  "product": "Windows SMB",
  "version": "Server 2019",
  "interesting": true,
  "notes": "SMBv1 disabled, signing not required (nxc smb signing check)",
  "tried": ["enum4linux", "nxc smb shares -u '' -p ''"]
}
```

## Pentest-specific gotchas

- `-Pn` can be helpful inside corporate networks where ICMP is blocked,
  but it doubles scan time on /24+. Per-host, not per-range.
- `--top-ports 1000` is acceptable as a fast first pass, but the
  authoritative scan is `-p-`.
- `-A` is fine but loud; honor `scan_limits` regardless.
- `--reason --packet-trace` is great for debugging filtered ports but
  generates a lot of evidence; capture once, don't leave it on.
