---
name: "ali-weekly-report"
description: "阿里云销售周报：多维大盘汇总+当月Top10排行+周折线(仅Top10)+月柱状图(仅Top10)。触发词：阿里周报/阿里云周报/Ali周报/销售周报"
---

# 阿里云销售周报 Skill

## 执行顺序与全局架构说明

本 Skill 包含一个前置数据准备步骤和三个功能模块，必须严格按顺序串行完成：

- **Step 0**: [前置核心] 销售年度数据本地化（按月分批拉取，排除 CDN 客户，生成日大盘数据）
- **功能一**: 多维大盘汇总 + 当月 Top10 客户排行 + 大盘日用量趋势图（基于本地数据源输出）
- **功能二**: 当月 Top10 客户周用量折线图（基于本地数据源输出）
- **功能三**: 当月 Top10 客户月度用量柱状图（基于本地数据源输出与清理）

## 前置条件

依赖 `ali-billing-query` 技能的 DuckDB 配置（`~/.duckdbrc` 中的 `sales_bills_db` 连接）。

远程表：`sales_bills_db.sales_bills.v_bill_ali_detail`

## Step 0: 销售年度数据本地化

利用 DuckDB 按月分批拉取该销售在当年的所有明细数据，直接在 SQL 中清洗换行符并排除客户名称中包含 'CDN' 的数据。后续功能全部读取本地合并后的临时文件。

### 关键字段映射

- 远程表无 `cost_date` 字段，使用 `paymenttime`（DATE 类型）替代
- 远程表无 `cost_list_price_cost` 字段，使用 `pretaxgrossamount` 替代
- 月份匹配使用 `CAST(month AS INT) = $((10#$m))` 防止前导零问题

### 执行脚本

```bash
#!/bin/bash
set -euo pipefail

SALES_NAME="$1"
CURRENT_YEAR="$2"
LOCAL_CSV="ali_all_local_data_${SALES_NAME}.csv"

echo "=== Step 0: 初始化本地数据文件结构 ==="
duckdb -c "
COPY (
 SELECT paymenttime AS cost_date, year, month,
 TRIM(REGEXP_REPLACE(customer_name, '[\n\r]', '', 'g')) as customer_name,
 CAST(pretaxgrossamount AS DOUBLE) as pretaxgrossamount
 FROM sales_bills_db.sales_bills.v_bill_ali_detail LIMIT 0
) TO '${LOCAL_CSV}' WITH (HEADER, FORMAT CSV);"

get_last_day() {
  python3 -c "import calendar; print(calendar.monthrange($1, $2)[1])"
}

for m in 01 02 03 04 05 06 07 08 09 10 11 12; do
    last_day=$(get_last_day "${CURRENT_YEAR}" "$((10#$m))")
    echo "  拉取 ${CURRENT_YEAR}-${m} (1-${last_day})..."

    duckdb -c "
    COPY (
      SELECT paymenttime AS cost_date, year, month,
      TRIM(REGEXP_REPLACE(customer_name, '[\n\r]', '', 'g')) as customer_name,
      CAST(pretaxgrossamount AS DOUBLE) as pretaxgrossamount
      FROM sales_bills_db.sales_bills.v_bill_ali_detail
      WHERE paymenttime >= '${CURRENT_YEAR}-${m}-01' AND paymenttime <= '${CURRENT_YEAR}-${m}-${last_day}'
        AND sales_name = '${SALES_NAME}'
        AND CAST(month AS INT) = $((10#$m))
        AND LOWER(customer_name) NOT LIKE '%cdn%'
    ) TO '_tmp_${CURRENT_YEAR}_${m}_${SALES_NAME}.csv' WITH (HEADER, FORMAT CSV);" 2>&1 | tail -1

    if [ -s "_tmp_${CURRENT_YEAR}_${m}_${SALES_NAME}.csv" ]; then
      tail -n +2 "_tmp_${CURRENT_YEAR}_${m}_${SALES_NAME}.csv" >> "${LOCAL_CSV}"
    fi
    rm -f "_tmp_${CURRENT_YEAR}_${m}_${SALES_NAME}.csv"
  done

echo "Step 0 数据本地化完成。"
echo "总行数: $(wc -l < ${LOCAL_CSV})"
```

## 功能一：多维大盘汇总 + 当月 Top10 客户排行 + 大盘日用量趋势图

### 数据计算

基于本地 CSV 使用 Python 直接读取计算：

**大盘多维汇总**（上半部分表格）：
- 本季度累计：当年 Q_START~Q_END 月份的 pretaxgrossamount 总和
- 本月累计：当年 CUR_MONTH 月份的 pretaxgrossamount 总和
- 本周累计：当年 CUR_WEEK ISO 周数的 pretaxgrossamount 总和
- 当年累计：当年全部月份的 pretaxgrossamount 总和
- 月环比 (MoM)：`(本月 - 上月) / 上月 × 100%`，上月无数据则显示"新增"

**客户排行**（下半部分表格）：
- 按 **当月用量 (Current Month Cost)** 降序排列前 10 名客户
- 列：`# | 客户名称 | 本月 (USD) | 上月 (USD) | MoM`
- 金额前缀统一为 `$` (USD)

**大盘日用量趋势图**：当年按 cost_date 汇总所有客户的 pretaxgrossamount，折线图

### 输出要求

1. **表格图片**：使用 Python PIL 绘制图片表格
   - 蓝色表头（#4472C4），白字；斑马纹（#F2F7FB）；累计行浅蓝高亮（#D6E4F0）加粗
   - 字体：`/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc` index=2
   - 金额右对齐取整，带 `$` 和千分位逗号；环比保留 1 位小数（带 +/-），无数据标记"新增"
   - 运行结束时将 Top10 客户名写入 `top10_monthly_{sales_name}.txt`，供功能二/三读取

2. **大盘日趋势图**：紧跟在表格后发送
   - 尺寸：宽 1400px，高 500px
   - 横轴为日期（cost_date），竖轴为每日总消费金额
   - 深蓝色粗折线（#1F50B4），标注最高/最低日用量点（排除 0）
   - 大额续费触发 Y 轴截断标注，标签红色
   - 标题：`{sales_name} - 阿里云所有客户每日总用量趋势大盘 ({year} {quarter})`

### Python 脚本

附件 `func1_quarterly.py`

## 功能二：当月 Top10 客户周用量折线图

### 数据计算

基于本地 CSV，按 customer_name + ISO week number 汇总 pretaxgrossamount。

**关键过滤**：
- 只保留功能一计算出的 **当月 Top10 客户**（读取 `top10_monthly_{sales_name}.txt`）
- 其余长尾客户全部剔除，横轴和图例仅展示 10 个核心客户

### 图表绘制

- 画布：宽 1400px，高 700px，右侧预留 250px 图例区
- 全为 0 的客户不画线
- 长客户名使用智能折行（中文按字符数，英文按单词边界 textwrap.wrap）
- 每条折线标注最高点和最低点（排除 0），黑色字体；大额续费红色标注
- 附带简要文本统计表（周均、最高、最低用量）
- 金额前缀统一为 `$` (USD)

### Python 脚本

附件 `func2_weekly.py`

## 功能三：当月 Top10 客户月度用量柱状图

### 数据计算

基于本地 CSV，按 customer_name + month 汇总 pretaxgrossamount。

**关键过滤**：
- 只保留功能一计算出的 **当月 Top10 客户**（读取 `top10_monthly_{sales_name}.txt`）
- 若未找到 Top10 文件，则兜底为年累计 Top10，不扩大到全部客户

### 图表绘制

- 分组柱状图，横轴为客户名称（仅 10 个核心客户）
- Y 轴最大值 = 单月最大值 × 1.15
- 柱高 > 10px 时，柱顶上方黑色字体标注 `$`{cost:,.0f}
- 12 色方案，底部居中展示月份图例
- **横轴客户名顺时针倾斜 45 度**，防止英文名字重叠
- 字体：NotoSansCJK-Regular.ttc index=2
- 金额前缀统一为 `$` (USD)

### Python 脚本

附件 `func3_monthly.py`

## 自动化主控流与环境清理

```bash
#!/bin/bash
set -euo pipefail

SALES_NAME="$1"
CURRENT_YEAR="$2"
CURRENT_QUARTER="$3"

CLEANUP() {
 echo "=== 激活自动化安全清理规程 ==="
 rm -f ali_all_local_data_${SALES_NAME}.csv
 rm -f top10_monthly_${SALES_NAME}.txt
 rm -f gen_*_${SALES_NAME}.py
 rm -f step0_fetch_${SALES_NAME}.sh
 echo "临时缓冲区已全量物理粉碎。"
}
trap CLEANUP EXIT

# 串行驱动
bash step0_fetch_${SALES_NAME}.sh "$SALES_NAME" "$CURRENT_YEAR"
python3 func1_quarterly.py "$SALES_NAME" "$CURRENT_YEAR" "$CURRENT_QUARTER"
python3 func2_weekly.py "$SALES_NAME" "$CURRENT_YEAR"
python3 func3_monthly.py "$SALES_NAME" "$CURRENT_YEAR"
```

## 执行流程

1. 确认销售姓名（sales_name），默认当前年份和当前季度
2. 写入 Step 0 Shell 脚本 → 执行数据拉取
3. 写入功能一 Python 脚本 → 执行 → 生成表格图片 + 大盘日趋势图，并写入 Top10 客户列表文件
4. 写入功能二 Python 脚本 → 执行 → 生成仅当月 Top10 客户的折线图
5. 写入功能三 Python 脚本 → 执行 → 生成仅当月 Top10 客户的柱状图
6. 清理所有临时文件（CSV + Python 脚本 + Top10 列表）

## 大额续费截断规则（防死锁 & 防 Y 轴压扁）

适用于**功能一（大盘日趋势图）**和**功能二（客户周用量折线图）**。

### 核心逻辑：Y轴动态范围 + 均值倍数触发截断

不再使用固定阈值（如 ¥100,000），而是基于**当前图表要展现的数据集**动态计算：

1. 计算当前数据集（当前销售、当前季度内）的**非零日均值/周均值**
2. 判断最大值是否超过均值的 **3 倍**
3. 若超过 → 触发截断，Y 轴上限 = 均值 × 3 × 1.15（日常波动占 80% 画布）
4. 若未超过 → 正常范围，Y 轴上限 = 最大值 × 1.15

| 图表类型 | 截断触发条件 | Y轴上限 | 截断方式 |
|----------|-------------|---------|----------|
| 大盘日趋势图 | 日最大值 > 日均值 × 3 | 日均值 × 3 × 1.15 | 画线时将该点 Y 值 Cap 在均值×3 |
| 客户周用量折线图 | 周最大值 > 周均值 × 3 | 周均值 × 3 × 1.15 | 画线时将该点 Y 值 Cap 在均值×3 |

### 标注要求

- **截断点的文字标签必须写真实金额**，并追加 `(⚠️大额续费)` 标记
- 示例：`$628,014 (⚠️大额续费)`
- 标签颜色用红色（`fill=(220, 50, 50)`）以区分普通标注

### Y 轴设置

- 触发截断时：Y 轴上限 = 均值 × 3 × 1.15，80% 画布留给日常波动
- 未触发截断时：Y 轴上限 = 最大值 × 1.15，正常展示
- 代码绝不会因极端值导致计算死锁或渲染异常

### Python 实现要点

```python
import statistics

# 大盘日趋势图 - Y轴动态范围
non_zero_vals = [v for v in values if v > 0]
daily_avg = statistics.mean(non_zero_vals)
daily_max = max(non_zero_vals)

if daily_max > daily_avg * 3:
    DAILY_CAP = daily_avg * 3
    y_max = DAILY_CAP * 1.15
else:
    DAILY_CAP = daily_max  # 无需截断
    y_max = daily_max * 1.15

capped_y = min(actual_value, DAILY_CAP)  # 画线用截断值
if actual_value > DAILY_CAP:
    label = f"${actual_value:,.0f} (⚠️大额续费)"
    label_color = (220, 50, 50)
else:
    label = f"${actual_value:,.0f}"
    label_color = (0, 0, 0)

# 客户周用量折线图 - Y轴动态范围（同理）
non_zero_vals = [v for v in all_vals if v > 0]
weekly_avg = statistics.mean(non_zero_vals)
weekly_max = max(non_zero_vals)

if weekly_max > weekly_avg * 3:
    WEEKLY_CAP = weekly_avg * 3
    y_max = WEEKLY_CAP * 1.15
else:
    WEEKLY_CAP = weekly_max
    y_max = weekly_max * 1.15
```

### 不适用范围

- **功能三（月度柱状图）**不适用此规则，因为柱状图 Y 轴最大值 = 单月最大值 × 1.15，天然能容纳极端值
- 多维大盘汇总表格不适用，表格直接展示真实金额

---

## 注意事项

- 所有临时文件名带 `_${SALES_NAME}` 后缀，防止多用户并发冲突
- `paymenttime` 替代 `cost_date`，`pretaxgrossamount` 替代 `cost_list_price_cost`
- CDN 客户在 SQL 层面硬排除：`LOWER(customer_name) NOT LIKE '%cdn%'`
- 月份匹配使用 `CAST(month AS INT)` 防止前导零不匹配
- 金额前缀统一为 `$` (USD)，千分位逗号格式
- 功能一运行结束时写入 `top10_monthly_{sales_name}.txt`，功能二/三必须读取该文件过滤客户
- 图片通过 `message` 工具的 `filePath` 参数发送，必须使用绝对路径
