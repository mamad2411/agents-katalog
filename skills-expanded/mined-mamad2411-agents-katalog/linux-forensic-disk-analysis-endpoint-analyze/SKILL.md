---
name: linux-forensic-disk-analysis-endpoint-analyze
description: "Linux Forensic Disk Analysis Endpoint Analyze."
domain: cybersecurity
---

--|
| **Order of Volatility** | Evidence collection priority from most volatile (RAM) to least volatile (backups) |
| **Chain of Custody** | Documented record of evidence handling from collection to presentation |
| **Write Blocker** | Hardware or software device that prevents modification of source evidence |
| **Super Timeline** | Consolidated chronological view of all artifact timestamps for incident reconstruction |
| **Prefetch** | Windows artifact recording program execution history |
| **ShimCache** | Application compatibility artifact tracking program existence on endpoint |

## Tools & Systems

- **Volatility 3**: Memory forensics framework for analyzing RAM dumps
- **KAPE (Kroll Artifact Parser and Extractor)**: Automated triage collection and parsing
- **Eric Zimmerman Tools**: Suite of Windows artifact parsers (PECmd, MFTECmd, RECmd, etc.)
- **Autopsy/Sleuth Kit**: Disk forensics platform for file system analysis
- **FTK Imager**: Forensic imaging and memory acquisition tool
- **Plaso/log2timeline**: Super timeline creation framework

## Common Pitfalls

- **Modifying evidence on live system**: Always image before analysis. Running tools on a live system alters timestamps and memory state.
- **Forgetting chain of custody**: Evidence without documented chain of custody is inadmissible in legal proceedings.
- **Analyzing only disk, ignoring memory**: In-memory-only malware (fileless attacks) leaves no disk artifacts. Always capture memory first.
- **Not hashing evidence**: All evidence must be cryptographically hashed at collection time to prove integrity.
- **Tunnel vision**: Focusing on one artifact when the timeline tells a broader story. Always build a comprehensive timeline.
