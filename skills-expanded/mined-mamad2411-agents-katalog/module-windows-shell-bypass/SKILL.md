# windows-shell-bypass

CVE-2026-21510: Windows Shell Security Feature Bypass

**Category:** exploitation — Exploitation Module

## Overview

CVE-2026-21510: Windows Shell Security Feature Bypass
CVSS: 8.8 (High)
Type: Security Feature Bypass (SmartScreen/MOTW)

This module creates malicious LNK files that bypass Windows SmartScreen
and Mark of the Web (MOTW) protections.

Technical Details:
- Exploits improper handling of URL zones in Windows Shell
- Bypasses "Mark of the Web" (MOTW) security warnings
- Allows silent execution of malicious payloads

Affected Systems:
- Windows 10 (21H2+)
- Windows 11 (bis 25H2)
- Windows Server 2012-

## Usage



## Agent Integration

- Agent persona: auto-selected from category 'exploitation'
- MCP:
- API:  with {"tool_name": "windows_shell_bypass", "target": "example.com"}
