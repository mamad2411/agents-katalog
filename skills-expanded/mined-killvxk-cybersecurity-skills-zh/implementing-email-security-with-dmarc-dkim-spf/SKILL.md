---
name: implementing-email-security-with-dmarc-dkim-spf
description: >-
  通过检查域名的 SPF、DKIM 和 DMARC DNS 记录，审计并验证电子邮件身份验证配置。
  使用 dnspython 查询 TXT 记录，验证 SPF 语法和查询次数，核查 DKIM 选择器记录，
  解析 DMARC 策略，识别可能导致电子邮件欺骗的错误配置。并生成修复建议。
domain: cybersecurity
subdomain: security-operations
tags: [implementing, email, security, with]
version: "1.0"
author: mahipal
license: Apache-2.0
---

## 说明

1. 安装依赖：`pip install dnspython checkdmarc`
2. 提供要审计的目标域名。
3. 运行 Agent 检查电子邮件安全：
   - 查询并验证 SPF 记录（语法、机制数量、include、redirect）
   - 检查常见选择器的 DKIM 记录（google、default、selector1、selector2）
   - 解析 DMARC 记录（策略、子域策略、报告 URI、对齐方式）
   - 识别可能导致邮件欺骗的错误配置
   - 生成修复建议

```bash
python scripts/agent.py --domain example.com --output email_security_report.json
```

## 示例

### 电子邮件安全审计结果
```
Domain: example.com
SPF: v=spf1 include:_spf.google.com ~all (WARN: softfail allows spoofing)
DKIM: selector1 OK, selector2 OK
DMARC: v=DMARC1; p=none; rua=mailto:dmarc@example.com (WARN: policy=none, no enforcement)
Risk: HIGH - p=none with ~all allows email spoofing
```
