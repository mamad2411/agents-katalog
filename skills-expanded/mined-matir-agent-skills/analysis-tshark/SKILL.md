---
name: analysis-tshark
description: Network protocol analyzer (TShark/Wireshark) for traffic capture, packet analysis, and forensic examination.
metadata:
  version: 0.2.0
  category: offsec
---
# TShark Network Protocol Analyzer

## Quick Start
```bash
# Capture packets on interface
sudo tshark -i eth0

# Read and analyze capture file with filter
tshark -r capture.pcap -Y "http.request"

# Extract HTTP objects
tshark -r capture.pcap --export-objects http,extracted_files/
```

## Workflow
1. **Authorization**: Verify written permission for network monitoring and packet capture.
2. **Discovery**: Identify available network interfaces using `tshark -D`.
3. **Capture**: Capture traffic using `sudo tshark -i <iface> -w <file>` with BPF filters if needed.
4. **Analysis**: Use display filters (`-Y`) and field extraction (`-T fields`) to identify incidents.
5. **Extraction**: Export files, credentials, and artifacts for forensic examination.
6. **Statistics**: Generate protocol hierarchy and conversation stats using `-z` options.

## Rules & Constraints
- **RULE-1**: MUST obtain written authorization; comply with wiretapping and privacy laws.
- **RULE-2**: Encrypt capture files at rest and treat extracted credentials as highly sensitive.
- **RULE-3**: Use BPF capture filters (`-f`) for high-volume traffic to avoid packet drops.
- **RULE-4**: Maintain chain of custody for all capture files in forensic proceedings.

## When to Use
- Analyzing network traffic for security incidents and malware detection.
- Capturing packets for forensic analysis and credential extraction.
- Investigating network anomalies and attack patterns.

## When NOT to Use
- Systems without explicit written authorization.
- Real-time intrusion prevention (use IPS/FW).

## References
- [Skill Manual](references/analysis-tshark-manual.md)
- [Official Man Page](https://www.wireshark.org/docs/man-pages/tshark.html)
- [Wireshark Display Filters](https://wiki.wireshark.org/DisplayFilters)
