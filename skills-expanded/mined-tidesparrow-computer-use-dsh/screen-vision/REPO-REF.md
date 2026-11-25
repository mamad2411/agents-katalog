# Repo Ref
- source: https://github.com/tidesparrow/computer-use-dsh (path: .dsh/skills/screen-vision/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 用千问（Qwen-VL 多模态模型）识别屏幕截图并驱动 computer_* 模拟操作。当主模型不支持图像输入（computer_screenshot 报 "requires an image-capable model"）时使用：截图 → 调 Qwen-VL 拿到屏幕描述与元素坐标 → 据此执行 computer_click / computer_move / computer_scroll 等
