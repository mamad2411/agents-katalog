---
name: visual-hazard-inspection
description: 调用论文 Web /detect，输出带隐患标注框的结果图与整改说明。
when_to_use: 用户上传工地图片并需要可视化隐患框（同 web_app_native 检测页）时
allowed_tools:
  - run_visual_inspection
---

# 隐患框图巡检

1. 调用内核 `POST /detect`（与 `web_app_native.py` 一致）
2. 返回 `result_image_url` 标注图 + 隐患列表与整改措施
3. 不修改论文编排与门控实现
