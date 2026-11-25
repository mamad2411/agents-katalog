---
name: dfo-pvf
description: 分析DNF（Dungeon & Fighter）游戏的完整PVF文件集合。包括：角色动画(character/[job]/animation/*.ani)的帧结构和贴图引用、职业技能文件(skill/[job]/*.skl)的技能属性、怪物定义(monster/[type]/*.mob)的属性和AI、攻击判定(attackinfo/*.atk)等。**当你询问DNF的动画帧、攻击动作、技能数据、怪物属性、AI行为，或需要分析任何PVF文件时，必须使用此skill。**
license: mit
---

# DFO PVF 分析技能

## 项目结构

PVF 解压后目录结构大致如下：

```
character/      # 角色定义（swordman, mage, fighter 等）
skill/           # 技能文件
monster/         # 怪物定义
creature/        # 生物动画
aicharacter/     # AI 行为脚本
common/          # 公共资源
```

## 核心文件类型

| 类型 | 路径 | 说明 |
|------|------|------|
| 动画 | `character/[job]/animation/*.ani` | 角色动作帧序列 |
| 攻击判定 | `character/[job]/attackinfo/*.atk` | 攻击伤害区域 |
| 技能 | `skill/[job]/*.skl` | 技能属性定义 |
| 怪物 | `monster/[type]/*.mob` | 怪物属性和AI |

## 详细参考

- [ANI格式参考](references/ani_format.md) - 动画帧结构、贴图路径
- [ALS格式参考](references/als_format.md) - 动画列表组合、多层叠加
- [ATK格式参考](references/atk_format.md) - 攻击判定、击退效果、元素属性
- [SKL格式参考](references/skl_format.md) - 技能文件字段
- [MOB格式参考](references/mob_format.md) - 怪物定义字段

## 常用查询

**查找角色攻击动画的贴图帧：**
1. 读取 `character/[job]/animation/attack1.ani`
2. 查看 `[IMAGE]` 行获取 img 路径和帧索引

**查找技能定义：**
1. 在 `skill/[job]/` 目录搜索技能名
2. 读取对应的 `.skl` 文件
