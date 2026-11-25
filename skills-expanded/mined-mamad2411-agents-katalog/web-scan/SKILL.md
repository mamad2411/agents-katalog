---
name: web-scan
trigger: web dir 目录 ffuf
tools: ffuf web_scanner.py
x-alice-class: pentest
---# 路径分析

## Phase 1
`python Skills/web-scan/scripts/web_scanner.py --target {TARGET} --whatweb`

## Phase 2
`ffuf -u {TARGET}/FUZZ -w Skills/web-scan/scripts/common.txt -mc 200,301,302,403 -o exports/dirs_{TARGET}.txt`
或: `python Skills/web-scan/scripts/web_scanner.py --target {TARGET} --dirs --output exports/dirs_{TARGET}.txt`
