# Repo Ref
- source: https://github.com/bighardperson/computer-science-skills-collection (path: skills/feishu-send-file/SKILL.md, branch: main)
- mined: 2026-09-20
- desc: 飞书发送文件技能。用于通过飞书向用户发送普通文件附件（HTML、ZIP、PDF、代码文件等）以及处理“本地图片路径被发成路径文本”的可靠补救场景。普通文件必须先上传获取 `file_key` 再发送；当本地图片用 `message`/`media` 发送后在飞书里只显示 `/root/...png` 路径而不显示图片时，改用本技能内的稳定图片上传脚本（`im/v1/images` -> `imag
