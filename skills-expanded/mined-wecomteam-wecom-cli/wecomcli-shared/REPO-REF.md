# Repo Ref
- source: https://github.com/wecomteam/wecom-cli (path: skills/wecomcli-shared/SKILL.md, branch: main)
- mined: 2026-09-20
- desc: wecom-cli 业务技能的公共前置检查、获取机器人及授权真人身份，以及通用输出约束。任何 wecomcli-* 技能首次准备执行 wecom-cli 命令前，都必须同时读取本技能，检查 CLI 是否安装、版本是否不低于 1.2.1，以及企业微信凭证是否已授权；仅在缺失、版本过低或未授权时执行安装或初始化。本技能还定义所有技能通用的 ID 类字段禁止外露约束。本技能不处理具体业务请求。
