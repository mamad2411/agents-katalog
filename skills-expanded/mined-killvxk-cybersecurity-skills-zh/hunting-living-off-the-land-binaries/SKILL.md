---
name: hunting-living-off-the-land-binaries
description: >
  检测 Windows 事件日志和 Sysmon 遥测数据中对离地攻击（Living Off The Land Binaries，LOLBAS）的滥用，
  包括 certutil、wmic、mshta、regsvr32 和 rundll32 等工具。
  通过将进程创建事件与 LOLBAS 项目数据库交叉比对来构建检测规则。
  适用于针对无文件攻击技术的威胁狩猎或构建 SIEM 检测规则的场景。
domain: cybersecurity
subdomain: security-operations
tags: [hunting, living, off, the]
version: "1.0"
author: mahipal
license: Apache-2.0
---

# 狩猎离地攻击二进制文件（LOLBAS）

## 说明

通过分析 Windows 进程创建事件（事件 ID 4688 / Sysmon 1）并将命令行与 LOLBAS 项目已知恶意模式进行匹配，检测 LOLBAS 滥用行为。

```python
import json
import requests

# 获取 LOLBAS 数据库
resp = requests.get("https://lolbas-project.github.io/api/lolbas.json")
lolbas_db = resp.json()

# 提取二进制文件名和可疑命令
for entry in lolbas_db:
    print(entry["Name"], [cmd["Command"] for cmd in entry.get("Commands", [])])
```

关键检测模式：
1. certutil -urlcache -split -f（下载）
2. mshta vbscript:Execute（脚本执行）
3. regsvr32 /s /n /u /i:http（squiblydoo 技术）
4. rundll32 javascript:（脚本执行）
5. wmic process call create（进程创建）
6. bitsadmin /transfer（下载）

## 示例

```python
# 将 Sysmon 事件 ID 1 与 LOLBAS 模式匹配
import Evtx.Evtx as evtx
with evtx.Evtx("Microsoft-Windows-Sysmon.evtx") as log:
    for record in log.records():
        xml = record.xml()
        if "certutil" in xml.lower() and "urlcache" in xml.lower():
            print(f"检测到 LOLBAS: {xml}")
```
