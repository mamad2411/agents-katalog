---
name: portwind-wiki
description: Portwind 团队飞书 wiki 沉淀的结构、模板、路由规则。把零散的工具推荐、踩坑、设计文档、复盘、新人入门、技术分享沉淀到固定父节点下，agent 按路由自动归位、按模板填内容。当用户说「沉淀进 wiki」「沉淀进知识库」「记一个坑」「记一个 gotcha」「写复盘」「写 postmortem」「写技术分享」「写 design doc」「写选型对比」「记一个新工具」「加进工具雷达」「新人入门文档」「按 portwind 规范沉淀」时使用。依赖 lark-cli + lark-wiki / lark-doc skills（不重复造）。
---

# portwind-wiki — 团队 wiki 沉淀路由

把同事日常产生的内容（工具推荐 / 踩坑 / 设计文档 / 复盘 / 新人材料 / 技术分享）按既定规则归到飞书 wiki 7 个父节点下。

**这个 skill 是路由表 + 模板库，不是 CLI。** 实际写 wiki 走 `lark-wiki` / `lark-doc` skill。

## 怎么用

用户说一句话，你按下表路由：

| 用户说 | 去哪个父节点 | 用哪个 template |
|---|---|---|
| 「这个工具不错装一个」/「写一个 skill 给团队」 | **Skill 沉淀** | [tool-self](references/templates/tool-self.md) |
| 「我们做了个 SaaS / 部署型产品」 | **产品沉淀** | [product](references/templates/product.md) |
| 「这个改动需要 review」/「写个 design doc」/「比较一下 X 和 Y」 | **架构 & 调研** | [design-doc](references/templates/design-doc.md) |
| 「这个错我撞过」/「踩坑」/「gotcha」 | **踩坑 & 复盘** | [pitfall](references/templates/pitfall.md)（标题前缀 `[坑]`） |
| 「线上挂了」/「故障复盘」/「postmortem」 | **踩坑 & 复盘** | [postmortem](references/templates/postmortem.md)（标题前缀 `[复盘]`） |
| 「新人怎么上手」/「环境搭建」/「内部账号」 | **团队入门** | [onboarding](references/templates/onboarding.md) |
| 「群里有人安利了 X」/「我发现了个外部工具」 | **工具雷达** | [tool-radar](references/templates/tool-radar.md) |
| 「写个技术分享」/「talk 大纲」 | **技术分享** | [share-talk](references/templates/share-talk.md) |

## 路由的 3 个常见决策点

1. **自研 vs 外部** → 自研进 Skill 沉淀 / 产品沉淀；外部别人写的进工具雷达
2. **是什么 vs 为什么** → 使用层（怎么装、怎么用）属 Skill 沉淀；设计层（为什么选 X 不选 Y）属架构 & 调研
3. **轻 vs 重** → 个人撞过的小坑 = `[坑]` 模板；线上事故 = `[复盘]` 模板（同一父节点，不同模板）

## 5 条治理规则（agent 写时遵守）

1. **不删，只归档**：过时内容打 `[archived YYYY-MM]` 前缀，留搜索可见性
2. **模板必填段不能跳**：踩坑模板第 4 段「下次怎么避免」没填 → 不算完成
3. **外部工具用群体归因**：`来源：via <群名>，YYYY-MM`，不点 @人名
4. **外部工具带 review_at 字段**：默认 6 个月后，季度自清时检查
5. **cross-link**：设计文档链对应的工具页；分享归档链来料的设计文档

详见 [governance.md](references/governance.md)。

## 关键工作流

- **草稿不直接进团队空间**：先在「leo 的草稿箱」之类私人 wiki 空间写，定稿 `lark-cli wiki +move` 搬回 → 见 [drafts-workflow.md](references/drafts-workflow.md)
- **GitHub Releases 自动同步**：在自研项目里配 `.github/workflows/release-notes-to-wiki.yml`，发 release 自动建子文档 → 见 [release-automation.md](references/release-automation.md)
- **新团队首次搭 wiki**：跟着 [bootstrap.md](references/bootstrap.md) 一步步建 7 父节点

## 完整结构参考

7 父节点细节、子节点命名、索引页范式 → 见 [structure.md](references/structure.md)

## 前置依赖

- **lark-cli** ≥ 1.0.34（`auth check` 子命令）
- 已登录 `lark-cli auth login --recommend`
- 装了 `lark-wiki` / `lark-doc` skill（agent 实际写 wiki 时调用）

## 不要做的事

- ❌ 不要在本 skill 里实现 wiki API（用 `lark-wiki` skill）
- ❌ 不要把会议纪要 / 个人学习笔记沉淀进团队 wiki（飞书妙记已有 / 私人空间更合适）
- ❌ 不要因为「分类太严」拒绝沉淀 —— 实在不知道往哪放就先丢「踩坑 & 复盘」用 `[坑]` 兜底，比留白强
