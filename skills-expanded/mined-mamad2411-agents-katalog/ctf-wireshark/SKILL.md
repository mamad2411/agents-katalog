---
name: ctf-wireshark
description: Use when pi needs local Wireshark or TShark workflow for PCAP or PCAPNG traffic analysis, packet triage, stream following, endpoint or conversation summaries, HTTP or DNS or TLS extraction, or automated first-pass review of a capture. Trigger on mentions of Wireshark, tshark, pcap, pcapng, packet capture, traffic capture, 流量包, 抓包, follow stream, protocol analysis, or when a forensics task needs quick network evidence extraction.
---

# CTF Wireshark

## Overview

Use this skill to turn local Wireshark/TShark tooling into a repeatable packet-analysis workflow. Start with the bundled TShark automation to produce a quick evidence map, then pivot into focused filters or the Wireshark GUI only when the automated pass reveals something worth drilling into.

## Local Assets

- Preferred CLI binary: `tshark`. Not installed by default; per AGENTS.md 安装约定，下载/构建 tshark 到 `tools/bin/`（或装进 sage10.9 env），不要用 `apt install` 全局安装。
- Common GUI binary: `wireshark` (needs a display; on headless boxes skip the GUI)
- Automated first pass: [scripts/analyze_pcap.py](scripts/analyze_pcap.py)
- Protocol filter cheatsheet: [references/filters.md](references/filters.md)

## Environment Note

TShark is **not** installed by default. If `command -v tshark` returns nothing, tell the user and per AGENTS.md 包管理与工具安装约定 把它装进 `tools/bin/`（不要全局 `apt install`），或让用户在别处装好后用 `--tshark`/`TSHARK_PATH` 指定。Do not pretend the binary exists.

## Workflow

1. Preserve the original capture.
   Work on a copy if you plan to export objects or split streams.
2. Run the automated first pass.
   Use the bundled script to collect metadata, protocol hierarchy, endpoint stats, conversations, HTTP requests, DNS queries, TLS SNI values, and a deduplicated hostname list.
3. Form one short hypothesis.
   Decide whether the likely flag path is web traffic, beaconing, lateral movement, file transfer, cleartext credentials, or exfil.
4. Pivot to focused filters.
   Follow suspicious TCP streams, isolate one host pair, or filter to the protocol family that matters.
5. Keep exact proof.
   Save the packet numbers, display filter, and extracted object or transcript that proves the answer.

## Quick Start

Run the automated first pass with `python3` and the installed skill path:

```bash
python3 scripts/analyze_pcap.py ./capture.pcapng
```

Write the report to a file and increase the sample size when needed:

```bash
python3 scripts/analyze_pcap.py \
  ./Traffic.pcapng \
  --out ./traffic-report.md \
  --limit 40
```

If `tshark` is not on PATH, point at it explicitly:

```bash
python3 scripts/analyze_pcap.py ./Traffic.pcapng --tshark /usr/bin/tshark
```

## Good Fits

- The user hands over a `.pcap` or `.pcapng` file and wants a fast triage.
- The task mentions Wireshark or TShark directly.
- A forensics challenge likely hides the flag in HTTP, DNS, TLS, SMB, FTP, or raw TCP streams.
- You need a machine-generated starting point before opening the GUI.

## Notes

- Prefer `tshark` for repeatable summaries and bulk extraction.
- Open Wireshark GUI only when stream reassembly, packet-by-packet browsing, or follow-stream context matters more than automation (and a display is available).
- Keep captures read-only unless you explicitly need exported objects or filtered subsets.
