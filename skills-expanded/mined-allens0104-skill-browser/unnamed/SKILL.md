---
name: 网站适配
description: `web-adapt` 的中文别名。适合先用通用方法适配陌生公开网站，再决定是否需要专用 site profile。
license: Proprietary session artifact for local Copilot use
---

# 网站适配 skill

这是下面这个能力族的中文短名：

- `adapt`
- `web-adapt`
- `universal-web-adaptation`

适合场景：

- 通用适配陌生网站
- 探测搜索框、按钮、弹窗和 opener
- 判断是否真的需要专用 site profile

## 核心做法

1. 先走通用适配
2. 页面重时优先调 runtime
3. 有新标签页或弹窗时要跟随
4. 只有通用路径不稳时才升级成专用 profile

## 调用示例

```text
请用 /网站适配 先通用适配这个网站，再告诉我是否真的需要专用 profile。
```

```text
请先通用适配这个陌生网站，并判断应该继续走 generic 还是升级成专用 profile。
```

## 指向

详细版请看：

- `skills/universal-web-adaptation/SKILL.md`
