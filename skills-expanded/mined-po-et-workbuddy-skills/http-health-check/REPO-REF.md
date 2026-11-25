# Repo Ref
- source: https://github.com/po-et/workbuddy-skills (path: skills/http-health-check/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 服务健康巡检、批量检查一组 URL 的状态码与耗时、TLS 证书到期提醒、接口可用性检查、发布后冒烟检查、定时巡检脚本、响应里必须包含某个关键字。当用户说「帮我检查这些服务是不是都正常」「发布完了跑一遍冒烟」「哪些域名的证书快过期了」「写个巡检脚本每天跑」「这个接口现在能不能访问、多快」时使用。附纯标准库脚本 scripts/health_check.py：并发请求 URL 列表（命令行或清单文件
