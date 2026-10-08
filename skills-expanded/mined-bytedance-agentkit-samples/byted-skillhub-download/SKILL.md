---
name: byted-skillhub-download
description: 从 SkillHub 下载私有或企业专属技能。当涉及下载内部、私有、企业专属或需授权的技能时使用。
---

# byted-skillhub-download

用途
- 从 SkillHub 精确按名称定位并下载**私有或企业专属**技能的最新版本 zip 包。
- **默认自动解压**：下载后会自动解压至以技能名称命名的目录中，并平铺顶层目录结构。
- 下载并解压完成后输出目录路径。

何时调用
- 当用户需求涉及下载**私有技能**或**企业专属技能**时触发。常见语义包括：
  1. 明确要求从 `byted-skillhub-download` 下载。
  2. 提到“下载企业专属技能”、“下载内部技能”或“下载私有 skill/技能”。
  3. 需要拉取存储在公司/企业 SkillHub 空间内的特定私有资源包。
- **注意**：对于普通的公开技能（Public Skills），请优先使用其他公开下载能力。

环境说明 (Agent 必读)
- **无需向用户索要环境变量**：当前环境已自动注入以下变量：
  - `ARK_SKILL_API_BASE`: SkillHub API 服务地址
  - `ARK_SKILL_API_KEY`: 企业 SkillHub 访问密钥
  - `SKILLHUB_SKILL_SPACE_ID`: 企业专属技能空间 ID
- **严禁向用户询问参数值**：Agent 在触发此技能时，应直接从环境中读取这些变量并执行脚本，不得中断流程向用户确认这些信息。

下载步骤
1. 执行脚本（路径相对于本 SKILL.md 所在目录）
   - `python ./scripts/download_from_skillhub.py --name "<精确名称>" --output /root/.openclaw/workspace/skills/`
   - 默认会将技能解压到 `/root/.openclaw/workspace/skills/<skill_name>/` 目录下
   - 若只想下载 zip 包而不解压，请添加 `--no-extract` 参数
2. 观察输出
   - 成功时，最后一行将打印解压后的目录路径（或 zip 文件路径）

安装提示
- 本技能仅下载并解压，不负责后续的安装逻辑。

示例
- 下载名为 "awesome-tool" 的技能至默认目录
  - `python ./scripts/download_from_skillhub.py --name "awesome-tool" --output /root/.openclaw/workspace/skills/`

故障排查
- 如提示缺少环境变量，请确认在环境中运行或联系管理员
- 未找到技能：确认名称为精确匹配，或检查 SkillSpaceId 是否正确
- 网络或鉴权错误：检查网络连通性与 API Key 是否有效
