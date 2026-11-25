---
name: skills-toolkit
description: 打包/安装 Codex 技能。当用户要求「打包所有技能」「导出技能」「备份技能」「一键安装技能」「安装技能包」「从 zip 安装技能」「收集技能」等时使用。打包器会扫描 ~/.codex/skills（排除 .system）生成 zip + manifest；安装器从 zip/目录安装技能到 ~/.codex/skills 并自动备份旧文件。脚本位于 C:\Users\Administrator\Documents\skills-toolkit\。
metadata:
  short-description: 一键打包/安装 Codex 技能
x-alice-class: assist
---# Skills Toolkit（技能打包 + 一键安装）

收集本机全部 Codex 技能并打包成 zip，同时支持一键安装（终端菜单或图形界面）。

## 脚本位置
- 打包器: C:\Users\Administrator\Documents\skills-toolkit\package_skills.py
- 安装器: C:\Users\Administrator\Documents\skills-toolkit\install_skills.py

## 使用步骤

1. 打包全部技能（用户要求「打包/备份/收集所有技能」时），运行：

    python "C:\Users\Administrator\Documents\skills-toolkit\package_skills.py"

    产物在 ~/.codex/skills-packages/skills-package-<时间>.zip，内含 manifest.json + skills/。

2. 一键安装技能（用户要求「安装技能/安装技能包」时），运行：

    python "C:\Users\Administrator\Documents\skills-toolkit\install_skills.py"

    默认自动用最新的 zip 包，进入终端菜单；也可加参数：

    python "C:\Users\Administrator\Documents\skills-toolkit\install_skills.py" --package <zip> --all --force
    python "C:\Users\Administrator\Documents\skills-toolkit\install_skills.py" --list
    python "C:\Users\Administrator\Documents\skills-toolkit\install_skills.py" --gui

## 注意事项
- 打包会排除 .system（系统内置技能）。
- 安装前自动备份将被覆盖的旧文件到 ~/.codex/skills-backups/。
- 安装完提醒用户重启 Codex 桌面端，新技能才会出现在技能列表。
- 终端乱码时先执行 chcp 65001 或用 python -X utf8。
