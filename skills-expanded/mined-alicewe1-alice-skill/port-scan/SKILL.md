---
name: port-scan
trigger: port 端口 nmap
tools: nuclei port_scanner.py
x-alice-class: pentest
---# 服务发现

## Phase 1
`nuclei -u {TARGET} 2>&1 > exports/scan_{TARGET}.txt`
或: `python scripts/port_scanner.py --target {TARGET} --top 1000 --output exports/scan_{TARGET}.txt`

## Phase 2
`python scripts/port_scanner.py --target {TARGET} --full --output exports/scan_full_{TARGET}.txt`
