---
name: pcap-analysis
description: "Adversarial analysis of PCAP files with two opposing views and diagnostic resolution. Designed for long-duration captures on quiet Linux systems. Supports host correlation and basic anomaly detection."
---

# PCAP Analysis

**Core Rule**: Same evidence. Two opposing views. Resolution based on diagnostic evidence and the overall pattern formed by multiple indicators over time.

## 1. Seal Evidence
Hash all input files immediately. Treat as read-only.

## 2. Extract Data Using Tools

### Quick Reference Table

| Purpose                        | Tool    | Command                                      | Notes |
|--------------------------------|---------|----------------------------------------------|-------|
| Traffic overview               | tshark  | `tshark -r file.pcap -q -z io,phs`          | Starting point |
| Volume & conversations         | tshark  | `tshark -r file.pcap -q -z conv,ip`         | Concentration signals |
| Inter-arrival timing           | tshark  | Extract `frame.time_delta` per destination  | Beaconing detection |
| Zeek analysis                  | Zeek    | `zeek -r file.pcap`                         | Strong for behavioral patterns |
| Host connections + processes   | ss      | `ss -tupn state established`                | Primary tool for process attribution |
| Encrypted DNS (DoH/DoT)        | tshark  | Filter known resolvers on 443 or 853        | Check for persistent connections |

**Note on `ss`**: `ss` (from the `iproute2` package) is the modern replacement for `netstat`. Use it as the primary tool. `netstat` is only a fallback.

## 3. Run Two Opposing Views

- **Hostile View**: Assume malicious activity. Focus on persistent low-volume patterns, regular timing, and combinations of indicators over long periods.
- **Benign View**: Assume legitimate activity (rare on a clean idle system).

## 4. Long Duration Quiet Capture Guidance

This skill is optimized for long-duration captures on quiet Linux systems with minimal running processes.

**Key Principles**:
- Low baseline noise makes persistent outbound activity significant.
- Focus on **regularity and persistence** across many hours rather than high volume.
- Account for natural Starlink burstiness — do not treat isolated bursts as malicious.
- Evaluate patterns across the full capture window.

## 5. Beaconing & Inter-Arrival Timing

Look for regular outbound connections to the same destination(s) with consistent timing and low jitter over long periods. Even low-frequency but regular patterns are meaningful in quiet, long-duration captures.

## 6. Host Correlation & Attribution (When Data Available)

When host data is available (e.g. from `ss`, process lists, or logs):

- Correlate persistent outbound connections to specific processes using `ss -tupn`.
- Identify processes maintaining long-lived or periodically repeating connections.
- Check `dmesg` and system logs for anomalies around the start of persistent activity.

**Useful `ss` Commands**:
```bash
ss -tupn state established
ss -tupn dst <destination-ip>
ss -tuln
```

## 7. Encrypted DNS (DoH / DoT)

**DoH** (port 443) hides queries. On quiet systems, sustained connections to known DoH resolvers are more notable.

**DoT** (port 853) is easier to detect due to the dedicated port.

Check for persistent connections to known resolvers and cross-reference with missing plaintext DNS activity when using Zeek.

## 8. Basic Anomaly Detection & Alerting

When running supporting scripts, implement lightweight alerting for:

- Persistent / long-lived connections
- Regular beaconing patterns (low jitter over time)
- AI/ML model files detected via YARA
- Correlated file activity + network connections

**Alert Output Format** (JSON Lines):
```json
{
  "timestamp": "...",
  "alert_type": "...",
  "severity": "medium",
  "description": "...",
  "details": {}
}
```

Write alerts to `/var/log/anomaly_alerts.jsonl` for easy review.

## 9. Indicator Combinations & Pattern Shapes

The overall pattern becomes more substantial when multiple indicators align over time (e.g., regular timing + consistent destination + persistence).

## 10. Output Structure

1. Evidence summary + hashes
2. Hostile View findings (include pattern shapes)
3. Benign View findings
4. Final Resolution
5. Limitations and environmental context

## Guidelines

- In quiet long-duration captures, prioritize **persistence, timing regularity, and combinations** of indicators.
- Use `ss` for process attribution when host data is available.
- Clearly note limitations from encryption (especially DoH).
- Default to describing observed patterns and their strength rather than forcing binary conclusions.
