---
name: phishing-kit
trigger: 钓鱼 phishing 社工 仿冒 伪造页面 credential 凭证窃取
tools: tools in Tool/
x-alice-class: pentest
---# 钓鱼工具包

## Phase 1 — 页面克隆
```
python scripts/tool_launcher.py --clone {TARGET_URL} --output exports/phish/
```

## Phase 2 — 邮件模板
```
python scripts/tool_launcher.py --pretext {SCENARIO} --output exports/phish/email.txt
```

## Phase 3 — 凭证收集
```
构建收集页面 → 部署 → 测试 → 记录
```

输出 → exports/phish/
