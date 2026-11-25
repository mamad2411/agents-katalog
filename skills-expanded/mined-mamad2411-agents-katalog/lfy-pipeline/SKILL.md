---
name: lfy-pipeline
description: 商机查询技能。适用于通过关键字搜索商机列表。当用户需要按关键字搜索商机时使用此技能。
metadata:
  requires:
    bins: ["lfy-cli"]
  cliHelp: "lfy-cli pipeline --help"
---

# 商机查询技能

> `lfy-cli` 是陆份仪提供的命令行程序，所有操作通过执行 `lfy-cli` 命令完成。

通过 `lfy-cli pipeline <接口名> ' '` 与商机系统交互。

## 注意事项

- `keywords` 为空时可能返回错误或不完整结果
- 若 `errcode` 不为 `0` 或返回格式异常，需告知用户错误信息
- 若搜索结果为空，告知用户未找到对应商机
- `pipeline_id`、`stage_id` 等技术字段默认不展示
- 当前版本不支持对商机进行任何修改操作
---

## 接口列表

### 搜索商机 (search)

```bash
lfy-cli pipeline search '{"keywords": "<keywords>"}'
```

按关键字搜索商机，支持模糊匹配。

参见 [API 详情](references/search.md)。

### 获取商机阶段 (get_sales_stage)

```bash
lfy-cli pipeline get_sales_stage '{"gtm_id": <gtm_id>}'
```

根据 GTM ID 获取商机阶段列表，包括阶段名称、里程碑目标、价值主张等信息。

参见 [API 详情](references/get_sales_stage.md)。

---

## 典型工作流

### 搜索商机

**经典 query 示例：**
- "帮我搜索一下'科技'相关的商机"
- "找一下包含'未来'的商机"
- "搜索关键字为'成都'的商机有哪些？"

**流程：**
1. 提取用户提供的关键字
2. 调用 `search` 命令搜索商机
3. 在结果中筛选 `pipeline_name` 包含关键字的商机
4. 若找到唯一匹配，直接展示结果
5. 若找到多个匹配，最多展示前10个，并告知用户如果需要精准匹配请提供更具体的商机名称

**展示结果：**

📇 为您找到 1 个商机：<pipeline_name>

找不到时：

```
没有匹配到包含"<keywords>"的商机，请尝试更具体的方式问我，比如："帮我搜索一下'科技'相关的商机"。
```

### 获取商机阶段

**经典 query 示例：**
- "帮我查一下这个商机的阶段信息"
- "获取商机阶段"
- "这个商机进行到哪一步了"

**流程：**
1. 提取用户提供的 `gtm_id`
2. 调用 `get_sales_stage` 命令获取阶段信息
3. 展示阶段列表信息

**展示结果：**

📋 商机阶段信息：

| 阶段名称 | 里程碑目标 | 价值主张 | 建议天数 |
|----------|-----------|---------|---------|
| <stage_name> | <milestone_goal> | <value_proposition> | <suggested_stage_days>天 |
