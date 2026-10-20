---
name: sqli-test
trigger: sql db 数据库 注入
tools: sqlmap sqli_tester.py
x-alice-class: pentest
---# 数据库测试

## Phase 1
`sqlmap -u "{TARGET}" --batch --level=2 --risk=2`
或: `python Skills/sqli-test/scripts/sqli_tester.py --target {TARGET} --detect`

## Phase 2
`sqlmap -u "{TARGET}" --batch --dbs`

输出 → exports/db_{TARGET}/
