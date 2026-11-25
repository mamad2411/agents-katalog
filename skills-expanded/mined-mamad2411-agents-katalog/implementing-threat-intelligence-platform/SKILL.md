---
name: implementing-threat-intelligence-platform
description: >-
  构建以 MISP 为后端的威胁情报平台，从多个 Feed 摄入 IOC，通过 Galaxy 集群关联事件，并通过 VirusTotal 和 AbuseIPDB 富化指标。使用 PyMISP 创建事件、添加带 IDS 标志的属性、标记 MITRE ATT&CK 技术，并导出 STIX 2.1 Bundle 供下游 SIEM 消费。
domain: cybersecurity
subdomain: threat-intelligence
tags: [implementing, threat, intelligence, platform]
version: "1.0"
author: mahipal
license: Apache-2.0
---

## 操作说明

1. 安装依赖：`pip install pymisp requests stix2`
2. 部署 MISP 实例并从"管理 > 认证密钥"生成 API 密钥。
3. 使用 PyMISP 连接并创建威胁情报事件：
   - 创建包含威胁级别、分发和分析状态的事件
   - 添加带 to_ids 标志的属性（ip-dst、domain、sha256、url）
   - 用 MITRE ATT&CK 技术标识符标记事件
   - 跨组织关联事件
4. 从外部 Feed 摄入：URLhaus、Feodo Tracker、MalwareBazaar。
5. 通过 VirusTotal 和 AbuseIPDB API 富化 IOC。
6. 将关联事件导出为 STIX 2.1 Bundle。

```bash
python scripts/agent.py --misp-url https://misp.local --misp-key <api_key> --ingest-feeds --output misp_report.json
```

## 示例

### 创建带 IOC 的 MISP 事件
```python
from pymisp import PyMISP, MISPEvent, MISPAttribute
misp = PyMISP("https://misp.local", "api_key")
event = MISPEvent()
event.info = "网络钓鱼活动 - 2024-Q1"
event.threat_level_id = 2
event.add_attribute("ip-dst", "185.143.223.47", to_ids=True)
misp.add_event(event)
```
