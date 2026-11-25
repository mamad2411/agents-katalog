---
name: figma-ios-minimum-deployment-12
description: >-
  Generated Swift and Objective-C UI code must run on iOS 12.0+. Avoid APIs
  introduced in iOS 13+ unless wrapped in availability checks. Use when the user
  mentions iOS 12, minimum deployment, SF Symbols, darkContent status bar, or
  CALayerCornerCurve.
---

# 最低系统：iOS 12

本仓库产出、或按 Figma/MK 规范生成的 **Swift / Objective-C** 界面代码，**部署目标最低为 iOS 12.0**，除非用户显式提高版本。

## Swift：禁止或需封装的 API（常见）

| 类别 | iOS 13+ API | iOS 12 做法 |
|------|-------------|-------------|
| 图片 | `UIImage(systemName:)`（SF Symbols） | `#available(iOS 13, *)` 使用；否则 **矢量绘制**、`UIImage(named:)` 或项目内图标字体 |
| 状态栏 | `UIStatusBarStyle.darkContent` | iOS 12 用 **`.default`**（浅底深字）；13+ 再用 `.darkContent` |
| 圆角 | `CALayer.cornerCurve`、`.continuous` | **删除**；仅用 `cornerRadius`（iOS 12 无连续曲率） |
| 其它 | `UIColor(dynamicProvider:)`、`UIAction` 等 | 查文档，用 `#available` 分支或替代实现 |

## Objective-C

- 同样遵守：**不得**无条件调用仅 iOS 13+ 的类方法/枚举。
- 使用 `if (@available(iOS 13.0, *)) { ... } else { ... }`。

## 原则

- 新增界面代码前默认 **能编过 `IPHONEOS_DEPLOYMENT_TARGET = 12.0`**。
- 若必须使用高版本 API，必须 **显式** `@available` / `#available` 并提供 **else 分支**。

## 相关

- **总入口**（推荐流程、Skill 索引、新增 Skill 防重叠规则）：[figma-ios-playbook](../figma-ios-playbook/SKILL.md)
