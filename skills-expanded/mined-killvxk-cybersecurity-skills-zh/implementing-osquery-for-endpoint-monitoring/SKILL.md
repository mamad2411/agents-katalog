---
name: implementing-osquery-for-endpoint-monitoring
description: >-
  部署 osquery 计划查询进行持续终端监控，涵盖进程清单、网络连接、文件完整性和持久化机制。
  生成包含查询包的 osquery.conf，配置差异结果日志记录，并分析查询结果以检测
  可疑进程、未授权监听端口和系统目录中的文件修改。
domain: cybersecurity
subdomain: security-operations
tags: [implementing, osquery, for, endpoint]
version: "1.0"
author: mahipal
license: Apache-2.0
---

## 说明

1. 安装依赖：`pip install requests`（osquery 需在终端上安装）
2. 生成包含以下安全监控查询包的 `osquery.conf`：
   - 进程监控：新进程、异常父子关系
   - 网络监听：意外的监听端口和出站连接
   - 文件完整性：/etc、/usr/bin、system32 中的修改
   - 持久化：cron 作业、启动项、计划任务、服务
3. 将配置部署到终端。
4. 分析 osquery 日志输出中的差异结果。
5. 生成安全发现报告。

```bash
python scripts/agent.py --results-dir /var/log/osquery/results/ --output osquery_report.json
```

## 示例

### Osquery 计划查询
```json
{"schedule": {"process_snapshot": {"query": "SELECT pid, name, path, cmdline, uid FROM processes WHERE on_disk = 0;", "interval": 300}}}
```
