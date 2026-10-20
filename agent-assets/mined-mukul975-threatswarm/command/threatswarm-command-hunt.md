---
description: Run an ATT&CK-based threat hunt with a specific hypothesis
allowed-tools: Bash, Read, Write, Grep, Glob
---

Run threat hunt with hypothesis: $ARGUMENTS

Parse $ARGUMENTS for: hypothesis text, optional timeframe (e.g., "last 7 days"), affected systems.

1. **Hunt Setup**:
   ```
   ═══════════════════════════════════════════════
   THREAT HUNT START
   Hypothesis: $ARGUMENTS
   Timestamp:  $(date -u +%Y-%m-%dT%H:%M:%SZ)
   Log dir:    evidence/$(date +%Y%m%d)/hunt/
   ═══════════════════════════════════════════════
   ```
   Create: `mkdir -p evidence/$(date +%Y%m%d)/hunt/{hypotheses,queries,findings}`

2. **Map Hypothesis to ATT&CK**: Identify relevant TTPs from the hypothesis:
   - PowerShell / script execution → T1059.001, T1059.003
   - Lateral movement → T1021.001 (RDP), T1021.002 (SMB), T1021.006 (WinRM)
   - Credential dumping → T1003.001 (LSASS), T1003.003 (NTDS)
   - Persistence → T1547.001 (Run Keys), T1053.005 (Scheduled Task)
   - C2 beaconing → T1071.001 (HTTP/S), T1071.004 (DNS)
   - Data exfiltration → T1041 (exfil over C2), T1048 (exfil via protocol)

3. **Invoke `threat-hunter` Agent**: Delegate with:
   - Full hypothesis text from $ARGUMENTS
   - ATT&CK TTP mapping
   - Available log sources (auth.log, syslog, nginx access, Windows Event Logs, pcaps)
   - Timeframe context

4. **Query Execution**: The threat-hunter agent runs ATT&CK-aligned queries:
   - Linux auth log pattern matching
   - Web server log anomaly detection
   - Network traffic analysis (if pcaps available in evidence/)
   - Windows Event Log correlation (if accessible)

5. **Cross-Source Correlation**: Correlate findings across log sources:
   - Match IP addresses across auth, web, and network logs
   - Timeline reconstruction of suspicious activity
   - Confidence scoring per finding

6. **Write Hunt Report**: Output to `evidence/$(date +%Y%m%d)/hunt/hunt_report.md`:
   - Hypothesis tested
   - Queries run with results
   - Confirmed/likely/possible findings
   - IOCs extracted (IPs, domains, hashes)
   - Recommended follow-up hunts

7. **Print Summary**:
   ```
   ═══ HUNT RESULTS ═══════════════════
   Hypothesis: [text]
   ATT&CK TTPs: [T1234, T1235...]
   Findings Confirmed: X
   Findings Possible:  X
   IOCs Extracted:     X
   Report: evidence/$(date +%Y%m%d)/hunt/hunt_report.md
   ════════════════════════════════════
   ```

If no evidence/ files exist and no log access is configured, output:
```
⚠ No log sources found. Configure log paths or run recon first.
Available: /var/log/auth.log, /var/log/nginx/access.log, pcap files in evidence/
```
