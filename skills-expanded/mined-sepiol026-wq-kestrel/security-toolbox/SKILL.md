---
name: security-toolbox
description: "Pick the right CLI tool for each hacking job."
version: 1.0.0
author: Kestrel Agent
license: AGPL-3.0
platforms: [linux, macos]
tags: [tooling, recon, web, credentials, ad, networking]
metadata:
  hermes:
    tags: [tooling, recon, web, credentials, ad, networking]
    related_skills: [node-hunting-at-scale, anonymous-service-to-root, web-app-penetration-testing]
---

# Security toolbox

Kestrel drives ordinary Unix tools through `terminal`. Nothing here depends on a
User-Agent header or a fake browser profile: a tool either does the job on the wire or
it does not. The stealth browser is for pages that decide by JavaScript; for everything
else use the right CLI.

## When to Use

Load at the start of any engagement to pick tools instead of improvising, and before
installing anything — half of this list is probably already on the box.

## 1. Inventory first

```bash
for t in nmap masscan naabu rustscan zmap curl wget jq ripgrep ffuf gobuster feroxbuster \
         nikto whatweb wpscan nuclei httpx subfinder amass dnsx katana gau waybackurls \
         sqlmap hydra medusa john hashcat sshpass proxychains4 netexec nxc impacket-smbserver \
         tcpdump tshark nc socat openssl python3 go cargo git docker; do
  command -v "$t" >/dev/null && echo "ok   $t" || echo "MISS $t"
done
```

Run it once per host and remember the result; installing a missing tool takes longer than
choosing a present one.

## 2. Ports and services

| job | tool | note |
| --- | --- | --- |
| whole IPv4, one port | `masscan` | 20-25 kpps without dropping frames; JSON out for pipelines |
| thousands of hosts, many ports | `nmap -iL -Pn --min-rate` | skip host discovery on the internet |
| quick live hosts | `naabu` | fast SYN connect scan, pipes into `httpx` |
| service versions, scripts | `nmap -sV -sC -p` | the only thing that names a product reliably |
| UDP that matters | `nmap -sU -p 53,123,161,500` | slow, scan selectively |

## 3. Web

| job | tool | note |
| --- | --- | --- |
| content discovery | `ffuf -w wordlist -u URL/FUZZ` | fastest with a good wordlist |
| directory brute | `feroxbuster` / `gobuster dir` | recursive, handles 403 vs 404 |
| fingerpбint | `whatweb`, `httpx -tech-detect -title -status-code` | titles catch panels faster than any probe |
| known issues | `nuclei -tags cve -severity critical,high` | templates lag new CVEs by days, not weeks |
| WordPress | `wpscan --enumerate vp,u` | plugins are the vulnerability |
| classic scanner | `nikto` | noisy, good for old Apache/IIS boxes |
| SQL injection | `sqlmap -u` with `--batch --level 3 --risk 2` | only after a parameter looks injectable |
| crawling | `katana -jc`, `gau`, `waybackurls` | historical URLs are where dead endpoints live |

## 4. Credentials

| job | tool | note |
| --- | --- | --- |
| SSH/FTP/HTTP form | `hydra -L users -P pass.txt` | one host at a time, `-t 4` to avoid lockouts |
| parallel batches | `medusa` | better than hydra for many hosts |
| hashes | `john`, `hashcat -m` | hashcat needs a GPU; john does not |
| password auth in scripts | `sshpass -p` | `-o NumberOfPasswordPrompts=1 -o PubkeyAuthentication=no` |
| spraying | manual loop over users with one password | lockout threshold is the constraint |

## 5. Network and pivoting

| job | tool | note |
| --- | --- | --- |
| tunnel anything | `ssh -D 1080`, `ssh -L/-R` | a SOCKS proxy from one owned host beats a proxy list |
| arbitrary tools over SOCKS | `proxychains4 cmd` | set `socks5 127.0.0.1 1080` in the config |
| raw relay | `socat TCP-LISTEN:...,fork TCP:...` | no SSH needed on the far side |
| packet capture | `tcpdump -i any -w x.pcap`, `tshark -r` | proves what actually crossed the wire |
| custom protocol | `python3 -c` with `socket` | faster than installing a client |

## 6. Active Directory and Windows

`netexec` (alias `nxc`) replaces the old crackmapexec: `nxc smb CIDR -u u -p p --shares`,
`nxc winrm`, `nxc ldap --bloodhound`. `impacket-*` covers `secretsdump.py`, `psexec.py`,
`smbclient.py`, `GetNPUsers.py`. `responder` for LLMNR poisoning in a LAN you control.

## 7. Container and orchestrator

`docker -H tcp://host:2375 ps`, `kubectl --server=http://host:10250` (or plain curl on the
API), `nomad job run`, `ctr -a /run/containerd/containerd.sock`, `crictl ps`. When an API
is open, the container runtime is the shell.

## 8. Install without a package manager

Static Go binaries land in `~/.local/bin` and need no root:

```bash
curl -sL https://github.com/projectdiscovery/nuclei/releases/latest/download/nuclei_$(uname -m)_linux.zip -o /tmp/n.zip
unzip -o /tmp/n.zip -d ~/.local/bin && chmod +x ~/.local/bin/nuclei
```

`pipx install` for Python tools, `go install github.com/...@latest` when Go is present,
`apt-get install -y` when it is not a scratch host.

## 9. Rules

- One tool per job. Two scanners on the same target is noise, not coverage.
- Save raw output to a file and parse it afterwards; re-running a scan because the output
  scrolled away is the most common waste.
- Respect the rate the target tolerates: a fast scan on a small box is a self-inflicted
  denial of service and burns the foothold.
- Prefer a tool that is already installed and understood over a shiny one that is not.
