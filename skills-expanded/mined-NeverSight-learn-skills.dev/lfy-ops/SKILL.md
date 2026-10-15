---
name: lfy-ops
description: 运营数据查询技能。适用于获取企业财年时间范围、当前周数等运营数据。当用户需要：(1) 查询当前财年信息，(2) 获取当前属于第几周时使用此技能。
metadata:
  requires:
    bins: ["lfy-cli"]
  cliHelp: "lfy-cli ops --help"
---

# 运营数据查询技能

> `lfy-cli` 是陆份仪提供的命令行程序，所有操作通过执行 `lfy-cli` 命令完成。

通过 `lfy-cli ops <接口名> '{}'` 与运营系统交互。

## 注意事项

- 若 `errcode` 不为 `0` 或返回格式异常，需告知用户错误信息
- 财年信息由企业设定，日期按北京时间返回
- `week_no` 等技术字段默认不展示
- 当前版本不支持对运营数据进行任何修改操作

---

## 接口列表

### 获取当前财年信息 (get_fiscal_year)

```bash
lfy-cli ops get_fiscal_year '{}'
```

获取企业当前财年的时间范围，根据企业设定的财年开始日期计算。

参见 [API 详情](references/get_fiscal_year.md)。

### 获取当前周数 (get_current_week)

```bash
lfy-cli ops get_current_week '{}'
```

获取当前属于第几周，按财年起始日期开始计算。

参见 [API 详情](references/get_current_week.md)。

---

## 典型工作流

### 获取财年信息

**经典 query 示例：**
- "当前是第几个财年？"
- "财年什么时候开始？"
- "查一下今年的财年范围"

**流程：**
1. 调用 `get_fiscal_year` 命令获取财年信息
2. 展示财年开始和结束日期

**展示结果：**

📅 当前财年信息：

| 财年 | 开始日期 | 结束日期 |
|------|---------|---------|
| <current_fiscal_year>年 | <start_date> | <end_date> |

---

### 获取当前周数

**经典 query 示例：**
- "现在是第几周？"
- "本周是几号到几号？"
- "当前周信息"

**流程：**
1. 调用 `get_current_week` 命令获取当前周信息
2. 展示当前周数及日期范围

**展示结果：**

📆 当前周信息：

| 周名称 | 开始日期 | 结束日期 |
|--------|---------|---------|
| <week_name> | <start_date> | <end_date> |
