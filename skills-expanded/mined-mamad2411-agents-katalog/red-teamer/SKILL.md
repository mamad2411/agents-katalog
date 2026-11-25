---
name: red-teamer
description: '認可済 red team engagement の方法論: 偵察→初期 access→特権昇格→横展開→永続化→exfil の chain を MITRE ATT&CK Matrix に沿って計画 / 実行する。HTB Pro Labs / engagement で発火'
category: pentest
tags:
  - red-team
  - methodology
  - mitre-attack
  - lateral
  - persistence
  - chain
---

# Red Team Methodology

## When to Use

- 認可済 red team engagement を MITRE ATT&CK Matrix に沿って計画 / 実行
- HTB Pro Labs / boxes で full chain compromise が必要
- 評価対象が AD / cloud / endpoint を含む大規模 environment

**使わない場面**: 単発 CTF jeopardy (→ `web-pentester` / `cve-exploitation`)、blue team 視点 (→ `blue-teamer` / `dfir`)。

## Approach / Workflow

### Phase 1 — 偵察 (Reconnaissance / Resource Development)

```
- 対象 organization の OSINT (employee / tech stack / domain)
- 公開 asset 列挙 (subfinder / amass / Shodan / Censys)
- DNS / TLS cert / SOC2 / GitHub org / 公開 doc 探索
- C2 infrastructure 準備 (redirector / domain fronting / category)
```

### Phase 2 — 初期 access (Initial Access)

```
- phishing (custom payload / OAuth consent / Office 0day)
- 公開 RDP / VPN / Citrix の brute / valid credential
- 公開 web vuln (RCE / SSRF → metadata)
- supply chain (CI / 3rd party lib)
- 物理 access (USB drop / 入館)
```

### Phase 3 — Foothold / Execution

```
- C2 implant 設置 (Cobalt Strike / Sliver / Mythic / Brute Ratel / 自前)
- session 安定化 (UAC bypass / persistence trigger)
- LOLBAS (rundll32 / regsvr32 / mshta / wmic / certutil)
```

### Phase 4 — Privilege Escalation

```
Linux:    sudo -l, SUID, kernel exploit, capabilities, PATH 改竄, cron
Windows:  AlwaysInstallElevated, service misconfig, unquoted path,
          token impersonation (SeImpersonate / Juicy Potato),
          UAC bypass, Kernel exploit
Cloud:    metadata SSRF → role assume, IAM misconfig
```

### Phase 5 — Defense Evasion

```
- AMSI bypass (PowerShell)
- ETW patching
- DLL unhooking
- AV definition evasion (custom packer / encoder)
- log clearing (慎重に / detection 増えるので minimal)
```

### Phase 6 — Credential Access

```
- LSASS dump (procdump / direct read / lsassy)
- Mimikatz on memory dump (→ memory-analysis)
- DCSync (Replicating Directory Changes)
- Kerberoast (→ system)
- ASREProast
- Cached credentials / DPAPI
```

### Phase 7 — Discovery

```
Windows AD:   BloodHound (SharpHound), PowerView
Windows local: net / quser / whoami /groups, ipconfig /displaydns
Linux:        find SUID, /etc/passwd, ssh key
Cloud:        scout / pacu
```

### Phase 8 — Lateral Movement

```
- Pass-the-Hash (NTLM relay / impacket-psexec)
- Pass-the-Ticket (Rubeus / Kerberos kirbi)
- WMI / WinRM / RDP / SSH
- SQL trust (linked server)
- DCOM execution
- Cloud identity hop
```

### Phase 9 — Persistence

```
Windows:   service / scheduled task / WMI sub / run key / DLL hijack / golden ticket
Linux:     cron / systemd / .bashrc / authorized_keys / LD_PRELOAD
Cloud:     IAM new key / OAuth app / cross-account role / IdP federation
```

### Phase 10 — Exfiltration / Impact

```
- staged compress + encrypt + 3rd party cloud (Drive / Dropbox / S3)
- DNS exfil
- HTTPS POST chunked
- impact (encryption / wipe / sabotage) は engagement scope と要協議
```

### Phase 11 — レポート

```
- 全 chain (timeline + ATT&CK ID)
- 各段階の証跡 (screenshot / log / hash)
- detection 機能 (caught / missed の割合)
- 推奨対応 (rule / patch / segmentation / training)
- 残存リスク (cleanup 後の persistence)
```

### Phase 12 — Cleanup

```
- 設置 implant / persistence の確実な除去
- 取得 credential のリスト → engagement 後 rotation 依頼
- log を tamper した場合は元に戻すか明記
- screenshot / dump の sealed area への保管
```

## Tools

```
Cobalt Strike / Sliver / Mythic / Havoc / Brute Ratel
BloodHound / SharpHound / PowerView
Rubeus / Mimikatz / lsassy / procdump
impacket / NetExec (CrackMapExec)
nmap / masscan / amass / subfinder
Burp / curl
WebFetch
Bash (sandbox)
```

## Related Skills

- `hackthebox`, `reconnaissance`, `system`, `infrastructure`, `techstack-identification`
- `social-engineering`, `web-pentester`, `web-bounty`, `bug-bounter`, `hackerone`
- `cve-exploitation`, `source-code-scanning`
- `injection`, `server-side`, `testing-jwt-token-security`, `testing-oauth2-implementation-flaws`
- `system`, `memory-analysis`
- `cloud-pentester`, `kubernetes-security`, `cloud-pentester`
- `wifi-security`, `firmware-iot-security`, `subghz-sdr`
- `replay-attack`, `network-analyzer`
- `coordination`, `essential-tools`, `script-generator`, `patt-fetcher`

## Rules

1. **明示許可 + scope** — RoE (Rules of Engagement) 文書を engagement 前に確認
2. **non-destructive default** — encrypt / wipe / data manipulation は明示許可下
3. **detection 機能を意図的に上げる演習も検討** — 防御側の visibility 評価
4. **cleanup 完了報告**
