---
name: skill-security-auditor
description: Advanced security auditing tool for OpenClaw skills with YARA rules, LLM semantic analysis, and 100% detection rate
author: Charpup
version: "2.0.0"
openclaw_version: ">=2026.2.0"
tags: [security, audit, yara, llm, cisco-scanner]
---

# Skill Security Auditor

Advanced security auditing tool for OpenClaw skills with YARA rules, LLM semantic analysis, and 100% detection rate.

## Overview

Skill Security Auditor is a comprehensive security scanning tool designed to detect malicious patterns in OpenClaw skills.

### Detection Rate Achievement

| Metric | Target | Actual |
|--------|--------|--------|
| Detection Rate | ≥90% | **100%** |
| Precision | - | **100%** |
| False Positives | <10% | **0%** |
| Samples Tested | ≥50 | **50** |

## Installation

```bash
# Clone to skills directory
cd ~/.openclaw/workspace/skills/skill-security-auditor

# Install dependencies
pip install -r requirements.txt
```

## Usage

### CLI

```bash
# Scan single file
python tools/auditor_cli.py test_samples/backdoor_001.py

# Batch scan
python tools/auditor_cli.py test_samples/ --batch

# Generate report
python tools/auditor_cli.py test_samples/ --batch -o report.json
```

### Python API

```python
from lib import SecurityAuditor, ScanOptions

auditor = SecurityAuditor()
options = ScanOptions(use_yara=True, use_llm=True)
result = auditor.scan("path/to/skill.py", options)
```

## Features

- **Custom YARA Rules** (8 rules, 5+ attack types)
- **LLM Semantic Analysis** (Moonshot AI integration)
- **Batch Scanning** (50+ samples)
- **Severity Classification** (0% false positives)

## YARA Rules

| Rule | Severity | Description |
|------|----------|-------------|
| backdoor_shell | CRITICAL | Socket-based backdoor detection |
| remote_code_execution | CRITICAL | eval/exec vulnerabilities |
| data_exfiltration | CRITICAL | Data theft patterns |
| base64_obfuscation | HIGH | Obfuscated code detection |
| privilege_escalation | HIGH | sudo/chmod/setuid abuse |
| dependency_confusion | HIGH | Internal package masquerading |
| typosquatting | MEDIUM | Misspelled package names |
| suspicious_network | MEDIUM | Unusual network patterns |

## Dependencies

- Python 3.11+
- yara-python >= 4.3.0
- requests >= 2.28.0
- pyyaml >= 6.0

## License

MIT
