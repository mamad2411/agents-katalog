---
description: Post-exploitation workflow after getting shell access — privesc, credential harvest, lateral movement
allowed-tools: Bash, Read, Write
---

Run full post-exploitation workflow on: $ARGUMENTS

Parse $ARGUMENTS: first word is TARGET, second word (optional) is SESSION_ID or access level (user/www-data/root/SYSTEM).

1. **Scope Check**: Verify TARGET is in scope.txt. Stop if not found.

2. **Document Current Access**:
   ```
   ═══════════════════════════════════════════
   POST-EXPLOITATION START
   Target:       TARGET
   Session ID:   SESSION_ID (if provided)
   Timestamp:    $(date -u +%Y-%m-%dT%H:%M:%SZ)
   ═══════════════════════════════════════════
   ```

3. **Invoke `post-ex` Agent** for automated privilege escalation:
   - Detect OS type (Linux vs Windows)
   - Run LinPEAS/WinPEAS automated enumeration
   - Check SUID binaries, cron, sudo, capabilities (Linux)
   - Check SeImpersonatePrivilege, unquoted paths, AlwaysInstallElevated (Windows)
   - Document escalation path with ATT&CK TTPs
   - Target evidence dir: `evidence/$(date +%Y%m%d)/TARGET/post_ex/`

4. **Credential Harvesting**: After any privilege escalation:
   - Linux: read /etc/shadow if root, find config files with credentials
   - Windows: invoke `impacket-secretsdump` locally, or mimikatz via Meterpreter
   - Pass any discovered hashes to `password-attacks` agent for cracking
   - Store: location reference only (NOT plaintext passwords)

5. **Domain Check**: If target appears domain-joined:
   - Check for domain membership: `realm list` (Linux) or `systeminfo | findstr /i domain` (Windows)
   - If domain-joined: invoke `active-directory` agent for full domain compromise path
   - Run BloodHound collection from compromised host

6. **Lateral Movement Mapping**:
   ```bash
   # SMB sweep for reachable hosts (from compromised machine)
   crackmapexec smb $INTERNAL_SUBNET/24 \
     -u $COMPROMISED_USER -H $NTLM_HASH \
     --continue-on-success 2>&1 | \
     tee evidence/$(date +%Y%m%d)/$TARGET/lateral/smb_sweep.txt
   ```

7. **Update Findings**: Append to `evidence/$(date +%Y%m%d)/TARGET/findings.md`:
   ```markdown
   ## Post-Exploitation — $(date -u +%Y-%m-%dT%H:%M:%SZ)

   | Step | Method | ATT&CK | Result |
   |------|--------|--------|--------|
   | Privesc | [technique] | [TTP] | [user → root/SYSTEM] |
   | Lateral | [technique] | T1021 | [hosts reached] |
   ```

8. **Print Summary**:
   ```
   ═══ POST-EX RESULTS ════════════════
   Privilege Level: [user → root/SYSTEM]
   Hosts Reached:   X
   Credentials:     X hashes (see evidence/)
   Domain Admin:    [YES/NO]
   ════════════════════════════════════
   ```
