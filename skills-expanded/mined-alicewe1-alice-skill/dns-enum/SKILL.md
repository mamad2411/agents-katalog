---
name: dns-enum
trigger: dns 子域名 域名 subfinder
tools: subfinder dns_enum.py
x-alice-class: pentest
---# 子域枚举

## Phase 1
`subfinder -d {TARGET} -o exports/dns_{TARGET}.txt`
或: `python Skills/dns-enum/scripts/dns_enum.py --target {TARGET} --subdomains --output exports/dns_{TARGET}.txt`

## Phase 2
`python Skills/dns-enum/scripts/dns_enum.py --target {TARGET} --records --output exports/dns_records_{TARGET}.txt`
