---
name: browser-tab-manager
description: 管理当前浏览器标签页：智能分组、取消或关闭已有分组，以及关闭 Mearl 受控标签页。仅适用于 Mearl 扩展连接的 Chrome 浏览器。
install:
  description: 安装并注册浏览器标签管理 Skill、CLI 命令和工具箱页面
  command: npx @mearl/setup plugin "$SKILL_DIR"
version: "3.1.0"
metadata:
  argument-hint: 'mearl tabs <summary|smart-group|group|remove-group|close-group|close-mearl> [--payload JSON]'
---

# 浏览器标签管理

在 Mearl 插件工具箱打开「标签管理」，或通过 `mearl tabs` 使用命令。扩展模式提供分组能力；外部 CDP Provider 没有 Chrome 标签分组 API。

## 命令

```bash
mearl tabs summary
mearl tabs smart-group
mearl tabs --payload '{"command":"group","input":{"groups":[{"title":"项目文档","tabIds":[123,124]}]}}'
mearl tabs close-mearl
```

- `summary` 返回标签页计数、受控网页数和分组摘要；不展开网页正文或逐页元数据。
- `smart-group` 自动规划并执行分组，只依据标签标题和去掉查询参数的网址，不读取页面正文。已有分组、固定标签和扩展页面不参与；不足两个候选标签的窗口跳过。

- `group` 接收 `groups` 数组。每组包含 `title` 和同一窗口内至少两个未分组的 `tabIds`；执行前重新读取并核对目标，逐组返回结果和失败项。不会把普通标签标记为 Mearl 受控。
- `remove-group` 用 `summary` 返回的 `groupId`、`windowId`、`title`、`tabIds` 取消分组，保留组内标签页；`close-group` 关闭该分组的全部标签页。两者执行前都会重新核对分组，标题或成员变化时需刷新列表。
- `close-mearl` 重新读取当前标签页后，关闭当前受控登记中或 favicon 与 Mearl 注入图标精确匹配的 HTTP(S) 标签页，返回关闭数和失败项。扩展重载后仍可识别保留 Mearl favicon 的网页；已导航并更换 favicon 的旧页无法仅凭图标识别。

未注册时，从当前 Skill 实际目录执行 `npx @mearl/setup plugin "$SKILL_DIR"` 后重试。
