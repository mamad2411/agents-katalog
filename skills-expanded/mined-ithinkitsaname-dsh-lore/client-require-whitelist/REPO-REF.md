# Repo Ref
- source: https://github.com/ithinkitsaname/dsh-lore (path: skills/client-require-whitelist/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 检查 DSH 客户端插件的 require(...) 是否都落在宿主的 9 项浏览器模块表里。表外的名字在浏览器里解析不到而且不报错，所以这件事值得变成一条会红的命令。改 lib/client.js 或任何客户端半边时用得上。
