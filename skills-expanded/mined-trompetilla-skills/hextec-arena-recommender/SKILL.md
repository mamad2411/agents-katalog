---
name: hextec-arena-recommender
description: 海克斯大乱斗英雄推荐器。当用户使用 @海克斯 英雄名 查询海克斯大乱斗英雄推荐时自动触发。
allowed-tools: Bash
---

海克斯大乱斗推荐器

当用户使用 @海克斯 英雄名 时触发。

## 使用方式

**用户输入**: @海克斯 拉克丝

**执行**:
```bash
cd ~/.openclaw/skills/hextec-arena-recommender && python3 scripts/fetch_recommender.py "拉克丝"
```

## 输出格式

```
[英雄] 拉克丝 | 层级 T5
[装备] 卢登的回声, 法师之靴, 风暴狂涌...
[棱彩] 无限循环往复(51.52%) | 任务：沃格勒特的巫师(51.10%)
[黄金] 红包(55.00%) | 属性叠属性！(53.06%)
[白银] 火狐(54.49%) | 扇巴掌(50.24%)
[链接](https://hextech.dtodo.cn/zh-CN/champion-stats/99)
```

## 英雄名称映射

支持多种英雄名称：
- 中文名: 拉克丝、贾克斯、库奇
- 别名: 光辉、武器、飞机
- 拼音: lux、jax、corki

## 注意事项

- 必须使用 fetch_recommender.py 脚本
- 脚本会自动从网站获取数据
