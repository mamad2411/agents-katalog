---
name: brute-force
trigger: brute 密码 登录 弱口令 credential auth
tools: brute_force.py
x-alice-class: pentest
---# 访问控制测试

## Phase 1
`python Skills/brute-force/scripts/brute_force.py --target {TARGET} --detect`

## Phase 2
`python Skills/brute-force/scripts/brute_force.py --target {TARGET} --service {SERVICE} --user {USER} --wordlist common --output exports/auth_{TARGET}.txt`
