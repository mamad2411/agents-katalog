---
description: Route an attack vector to the appropriate specialist agent — usage: /project:attack <target> <vector>
allowed-tools: Bash, Read, Write
---

Execute an attack against target using the specified vector: $ARGUMENTS

Parse $ARGUMENTS: the first word is TARGET, remaining words are the VECTOR.

1. **Scope Check**: Verify TARGET is in scope.txt. Stop if not found.

2. **Route to Agent based on VECTOR keyword**:

   | Vector Keyword | Agent to Invoke |
   |----------------|-----------------|
   | `web`, `http`, `webapp`, `sqli`, `xss`, `ssrf`, `lfi`, `jwt` | `web-attacker` |
   | `api`, `rest`, `graphql`, `grpc`, `bola`, `idor`, `swagger` | `api-attacker` |
   | `ad`, `active-directory`, `kerberoast`, `asrep`, `dcsync`, `bloodhound` | `active-directory` |
   | `network`, `arp`, `mitm`, `snmp`, `smbrelay`, `responder` | `network-ops` |
   | `wireless`, `wifi`, `wpa`, `wps`, `eap`, `pmkid` | `wireless-attacker` |
   | `cloud`, `aws`, `azure`, `gcp`, `s3`, `iam`, `metadata` | `cloud-attacker` |
   | `container`, `docker`, `kubernetes`, `k8s`, `pod`, `kubelet` | `container-attacker` |
   | `exploit`, `cve-`, `rce`, `shell`, `metasploit`, `msfconsole` | `exploit` |
   | `mobile`, `android`, `ios`, `apk`, `frida`, `adb` | `mobile-attacker` |
   | `osint`, `passive`, `recon`, `crt.sh`, `shodan`, `theHarvester` | `osint` |
   | `reverse`, `binary`, `re`, `ghidra`, `r2`, `gdb`, `rop` | `reverse-engineer` |
   | `malware`, `sample`, `yara`, `ioc`, `sandbox` | `malware-analyst` |
   | `password`, `hash`, `crack`, `hashcat`, `john` | `password-attacks` |
   | `phishing`, `social`, `gophish`, `evilginx`, `vishing` | `social-engineer` |
   | `crypto`, `tls`, `ssl`, `jwt-crack`, `padding` | `crypto-attacker` |
   | `iot`, `firmware`, `uart`, `mqtt`, `binwalk` | `iot-attacker` |
   | `c2`, `sliver`, `havoc`, `meterpreter`, `beacon`, `implant` | `c2-operator` |
   | `evasion`, `amsi`, `av-bypass`, `obfuscate` | `evasion` |

3. **Invoke Selected Agent**: Delegate to the matched agent with:
   - Target: `TARGET`
   - Vector: `VECTOR`
   - Evidence dir: `evidence/$(date +%Y%m%d)/TARGET/`
   - Context from `evidence/$(date +%Y%m%d)/TARGET/recon_summary.md` if it exists

4. **Log Attack**: After agent completes, append to `evidence/$(date +%Y%m%d)/TARGET/attack_log.md`:
   ```markdown
   | $(date -u +%Y-%m-%dT%H:%M:%SZ) | VECTOR | [agent used] | [outcome summary] |
   ```

5. **Output Summary**: Print findings discovered with severity if available.

If VECTOR does not match any keyword, output:
```
Unknown attack vector. Available vectors: web, api, ad, network, wireless, cloud, container, exploit, mobile, osint, reverse, malware, password, phishing, crypto, iot, c2, evasion
```
