---
name: closed-loop-inspection
description: 执行监测-识别-分析-整改闭环单图巡检；调用论文神经符号内核，不修改合规真值。
when_to_use: 用户上传单张工地影像并需要完整 Agent 编排演示时
allowed_tools:
  - register_monitoring_event
  - run_inspection_kernel
  - assess_risks
  - record_rectification_ledger
---

# 闭环单图巡检

1. 监测：登记影像与场景
2. 识别：HTTP 调用 `KERNEL_BASE_URL` 论文内核
3. 分析：风险研判叙事
4. 整改：写入台账
