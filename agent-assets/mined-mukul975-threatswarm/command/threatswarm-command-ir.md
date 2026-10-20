---
description: Incident response workflow — triage, evidence collection, timeline, and IOC extraction
allowed-tools: Bash, Read, Write, Glob
---

Run incident response workflow for: $ARGUMENTS

Parse $ARGUMENTS: incident type is one of [compromise, ransomware, data-exfil, insider, malware, unknown]
Optional second argument: affected system IP or hostname.

1. **IR Kickoff**:
   ```
   ═══════════════════════════════════════════════════
   INCIDENT RESPONSE START
   Type:      $ARGUMENTS
   Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)
   Operator:  $(whoami)
   ═══════════════════════════════════════════════════
   ```
   Create directories:
   ```bash
   mkdir -p evidence/$(date +%Y%m%d)/IR_$(date +%H%M%S)/{volatile,memory,logs,artifacts,iocs,timeline}
   IR_DIR=evidence/$(date +%Y%m%d)/IR_$(date +%H%M%S)
   ```

2. **Type-Specific Checklist**:

   **compromise**: Focus on initial access vector, persistence, lateral movement, credential theft
   **ransomware**: Focus on initial infection vector, encryption scope, shadow copy deletion, C2 communication
   **data-exfil**: Focus on data accessed, exfiltration method, destination IPs/domains
   **insider**: Focus on privileged access abuse, data downloads, account activity timeline
   **malware**: Focus on malware family identification, persistence, C2, affected hosts

3. **Invoke `dfir` Agent**: Delegate full triage with:
   - Incident type context
   - Volatile data capture first (processes, network, users)
   - Persistence mechanism hunting
   - Memory acquisition guidance (avml/LiME)
   - Log collection and analysis
   - Evidence directory: `$IR_DIR`

4. **System Snapshot**: Capture current state:
   ```bash
   # Snapshot current processes, network, users
   ps auxf > $IR_DIR/volatile/processes_$(date +%s).txt
   ss -tulnp > $IR_DIR/volatile/network_$(date +%s).txt
   who > $IR_DIR/volatile/users_$(date +%s).txt
   ```

5. **IOC Extraction**: Extract all IOCs to `$IR_DIR/iocs/`:
   - IP addresses from logs and network connections
   - Domain names from DNS and web logs
   - File hashes of suspicious executables
   - Registry keys (Windows), cron entries (Linux)
   - Malware indicators (mutex names, persistence paths)

6. **Threat Hunt Integration**: Invoke `threat-hunter` agent to find lateral movement:
   - Look for other systems the attacker may have reached
   - Correlate IOCs across available log sources

7. **Timeline Build**: Write UTC-ordered timeline to `$IR_DIR/timeline/timeline.md`:
   ```markdown
   | UTC Timestamp | Event | Source | ATT&CK TTP | Significance |
   |---------------|-------|--------|------------|--------------|
   ```

8. **Output Deliverables**:
   ```
   ═══ IR DELIVERABLES ════════════════════════════
   immediate_actions.md  — Containment steps
   timeline.md           — UTC event timeline
   iocs.txt              — Indicators of compromise
   evidence_manifest.txt — Chain of custody log
   ════════════════════════════════════════════════

   Next: Share IOCs with security team
   Next: Brief stakeholders using immediate_actions.md
   ```

9. **Write Evidence Manifest** to `$IR_DIR/evidence_manifest.txt`:
   ```
   Chain of Custody — $ARGUMENTS — $(date -u +%Y-%m-%dT%H:%M:%SZ)
   Operator: $(whoami)
   Files collected:
   [list all files with sha256 hashes]
   ```
