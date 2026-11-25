---
name: batch-flight-inspection
description: 架次批量巡检：文件夹多图编排、汇总报告、写入工地记忆。
when_to_use: 无人机航线多图或文件夹批处理演示
allowed_tools:
  - batch_flight_inspect
  - register_monitoring_event
---

# 架次批量巡检

对目录内影像逐张执行 `InspectionAgentOrchestrator.run_closed_loop`，输出 `data/agent_demo/batch_reports/*.json`。
