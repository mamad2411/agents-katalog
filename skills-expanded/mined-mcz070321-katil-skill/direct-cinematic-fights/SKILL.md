---
name: direct-cinematic-fights
description: "Use when 用户显式指定 KATIL 动作模块／direct-cinematic-fights 兼容入口，或旧流程指向本入口；普通 KATIL 打斗请求由主技能处理，本入口只转接。文戏不触发动作编排。"
metadata:
  integration-version: "3.10.5"
  integration-revision: "v3.10.5-impact-and-review-coverage"
  display-name: "KATIL-skill · 动作兼容入口"
---

# KATIL-skill V3.10.5 动作兼容入口

本模块只做路由转接，不维护第二套规则。先定位**本次选择的主技能根目录**：用户已明确候选／安装路径就用该路径；否则若本模块相邻的 `../katil-skill/SKILL.md` 存在就用同套包；若本入口位于主技能 `compatibility/direct-cinematic-fights/` 中则使用上两级的主技能；再否则从当前环境技能目录中的 `katil-skill` 条目取真实路径。核对主技能 `manifest.yaml` 的 `version` 为3.10.5，并确认下述专题存在，不跳到另一套旧版。本兼容入口隶属同一Core发布，不覆盖环境中独立安装的同名技能。

从已定位的根目录读取 `SKILL.md` 与 `references/action-and-shot-compiler.md`；视频交付按同根的 `references/prompt-delivery-and-language.md`。缺少主技能或专题时指出应完整安装同版主技能，不退回旧模板，也不复制一套新规则。

已经读过主入口与适用专题就直接继续，不重复加载。关键事件的镜头执行、已有战斗稿视觉精修、高速与多人、POV、一镜、原著和受创只按主入口条件选择。对外统一称 KATIL-skill；明确单语、范围、原文、时长、能力和终点优先，默认只输出文本提示词，不生成图片或视频文件。
