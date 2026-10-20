---
name: hunting-for-webshells-in-web-servers
description: >-
  通过扫描高熵值文件、可疑的 PHP/JSP/ASP 模式（eval、base64_decode、system、passthru）、
  Web 根目录中近期修改的文件以及异常文件大小，检测植入 Web 服务器的 Webshell（网页后门）。
  使用香农熵（Shannon entropy）计算标记混淆载荷，并通过正则表达式模式匹配已知 Webshell 特征。
domain: cybersecurity
subdomain: security-operations
tags: [hunting, for, webshells, web]
version: "1.0"
author: mahipal
license: Apache-2.0
---

## 说明

1. 安装依赖：`pip install yara-python`
2. 确定需要扫描的 Web 服务器文档根目录（如 `/var/www/html`、`/opt/lampp/htdocs`）。
3. 运行 Agent 扫描 Webshell：
   - 香农熵分析标记熵值 > 5.5 的文件
   - 模式匹配检测 eval()、base64_decode()、system()、passthru()、shell_exec()
   - 文件修改时间分析发现近期变更的文件
   - 扩展名过滤针对 .php、.jsp、.asp、.aspx、.cgi、.py 文件

```bash
python scripts/agent.py --webroot /var/www/html --output webshell_report.json
```

## 示例

### 高熵 PHP Webshell 检测
```
File: /var/www/html/uploads/img_thumb.php
Entropy: 6.12 (threshold: 5.5)
Patterns matched: eval(), base64_decode(), str_rot13()
Last modified: 2025-12-01 03:42:00 (outside business hours)
Verdict: SUSPICIOUS - likely obfuscated webshell
```
