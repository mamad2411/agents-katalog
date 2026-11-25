---
name: skillhub
version: "1.0.0"
description: "Forge-skillHub integration gateway for discovering and managing reusable Forge skills"
triggers:
  - command: "skillhub"
  - auto: "when the user asks to discover, install, publish, update, or remove Forge skills"
route_level: [micro, standard, full]
inputs:
  - user_request
outputs:
  - selected Forge-skillHub workflow
next: none
token_budget: 1000
constraints:
  must:
    - "只通过 Forge-skillHub 的受支持能力管理技能"
---

# Forge SkillHub Gateway

Forge SkillHub 是 ForgeTeam 复用技能的发现和管理入口。

- 查找、安装或使用技能时，使用 `forge-skillhub` 工作流。
- 发布、更新或删除自有技能时，使用 `forge-skill-manage` 工作流。
- 私有技能必须保持仅拥有者可见，且不得被其他用户搜索。

本入口只负责路由到 `skillHub/` 下已有的子技能，不重复实现 Forge-skillHub 的上传、下载、更新或删除能力。
