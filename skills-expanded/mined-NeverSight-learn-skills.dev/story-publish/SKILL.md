---
name: story-publish
version: 1.0.0
description: "把已经定稿并通过发布检查的小说章节交给项目已登记的平台发布适配器，支持只读预览/预检、登录、存草稿、修改、立即发布和排期发布。当用户说‘发到番茄’‘自动发布’‘存草稿’‘更新平台章节’时使用；不负责写正文或生成发布文案。"
metadata: {"openclaw":{"source":"https://github.com/qin1473692580-ux/oh-story-claudecode"}}
---

# Story Publish

把已批准的本地章节交给项目登记的发布适配器。发布材料由 story-release-package 准备；本 Skill 只负责平台交付，二者权限分离。

## 权限边界

- “继续写”“定稿”“准备发布”都不授权远程写入；只有用户明确要求登录、存草稿、修改、立即发布或排期发布时才执行对应动作。
- 预览只读本地；preflight、books 只读平台；draft 会写远程草稿；edit、publish、schedule 会修改正式平台状态。
- 不读取、不复制、不输出 Cookie、密码或浏览器存储。登录态只由项目登记的本地适配器管理。
- 不直接调用原始 GUI 或绕过项目级防重包装器。不得用 shell 拼接用户参数。
- 当前内置的是通用适配层，不是番茄 MCP；平台能力由项目本地适配器提供。

## 前置门禁

1. 目标章节必须已经定稿，且正文哈希仍与最新发布审查/清单一致；候选章不得发布。
2. 长篇项目的 tracking、revision 与 story doctor 门必须无未闭环阻断项。
3. 项目根存在 `.story-publish.json`，且 status 能确认适配器与解释器均存在。
4. 先 preview，再 preflight；任一目标章号或标题已存在时，新建发布必须中止。已有章节只能走明确的 edit。
5. 远程写入前向用户复述平台、作品、章节范围、动作、AI申报和排期；范围或动作改变后重新确认。

## 执行入口

从当前 Skill 目录定位 `scripts/publish_bridge.py`，按项目统一方式探测解释器：`for PYBIN in python3 python py; do "$PYBIN" -c "" 2>/dev/null && break; done`。没有可用解释器时停止，不猜命令；探测成功后把当前项目根传给 `--project-root`：

- 查看关联：`"$PYBIN" publish_bridge.py --project-root <项目根> status`
- 关联番茄适配器：`"$PYBIN" publish_bridge.py --project-root <项目根> configure fanqie --adapter <project_publish.py> --python <适配器虚拟环境Python>`
- 运行只读动作：`"$PYBIN" publish_bridge.py --project-root <项目根> run fanqie preview --chapters 109`
- 存草稿：在用户明确确认后增加 `--confirm-remote-draft`；该桥接确认参数不会传给下游。
- 正式修改/发布/排期：必须把下游要求的 `--confirm-live` 与 `--ai-declaration yes|no` 原样传入；不得代替用户猜测申报。

具体配置结构、动作分级和失败语义见 [references/adapter-contract.md](references/adapter-contract.md)。

## 结果回执

- 始终报告实际执行动作、适配器退出码和成功/失败章节；不能把“已启动”“已点击”写成“已发布”。
- 正式发布或修改后，调用适配器 preflight/平台回读能力确认目标状态；无法回读时报告 `REMOTE_STATE_UNVERIFIED`，不自动重试写入。
- 失败后不得自动重复 draft/edit/publish/schedule。先只读查询远端状态，再由用户决定是否重试。

## 禁止事项

- 不把本书 Book ID、书名、章节目录、账号路径或机器绝对路径写进本 Skill。
- 不把 `.story-publish.json`、Cookie、认证状态或平台响应原文打进发布包。
- 不因用户授权了一次发布而扩大到其他作品、其他章节或后续自动日更。
- 不在验证码、MFA、协议确认或平台风控页面自动代替用户操作。
