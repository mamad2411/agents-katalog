---
name: airs-embodied-bidding
description: >
  AIRS 具身智能 天眼查 招投标 数据查询工具。
  查询企业在天眼查平台的招投标/中标公示信息，导出结构化 CSV 报表，基于浏览器自动化技术实现。
  Keywords: AIRS, 具身智能, 天眼查, 招投标, embodied intelligence, bidding, tianyancha
version: 1.0.6
author: "airs"
tags: ["airs", "AIRS", "具身智能", "天眼查", "招投标", "tianyancha", "embodied", "china", "bidding", "company"]
---

## When to Use

当用户需要以下场景时触发此技能：

- 查询、导出企业在天眼查平台上的招投标/中标/投标公示信息
- 批量查询一批企业的招投标历史记录
- 按时间范围和金额筛选企业中标信息
- 基于企业名单文件进行招投标数据查询
- 交互式查询单个企业的招投标记录

**典型用户请求：**
- "查询宇树科技的招投标记录"
- "导出这些企业的中标信息"
- "采集 2026 年第一季度的招投标数据"
- "搜索乐聚机器人的中标项目"

## Requirements

### 系统要求
- **Node.js**: >= 18.0.0
- **操作系统**: macOS / Windows / Linux
- **Chrome 浏览器**: 已安装并可运行

### 前置准备

#### 1. 安装 Node.js
如未安装，请访问 https://nodejs.org/ 下载 LTS 版本。

验证安装：
```bash
node --version  # 应显示 v18 或更高版本
npm --version
```

#### 2. 启动 Chrome 远程调试

**⚠️ 必须先关闭所有 Chrome 窗口，然后运行以下命令：**

**macOS:**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome_debug_profile
```

**Windows:**
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" \
  --remote-debugging-port=9222 \
  --user-data-dir=%TEMP%\chrome_debug_profile
```

**Linux:**
```bash
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome_debug_profile
```

#### 3. 登录天眼查
Chrome 启动后，访问 https://www.tianyancha.com 并完成登录。

## Quick Start

```bash
# 进入脚本目录
cd scripts

# 安装依赖
npm install

# 检查环境状态
node cli.js status

# 搜索并确认企业信息
node cli.js search

# 下载招投标记录
node cli.js download --start-date 2026-01-01 --end-date 2026-03-31

# 交互式查询单个企业
node cli.js query "宇树科技"
```

## Commands

### `status` - 环境状态检查

检查 Node.js、Chrome 连接、npm 依赖等环境状态。

```bash
node cli.js status
```

### `search` - 企业搜索确认

从企业名单搜索天眼查信息，补全企业全称和链接。

**本地优先匹配：** 如果企业在 `assets/具身智能中游企业数据库.md` 中已有「天眼查企业全称」和「天眼查链接」，则直接使用本地数据，**不再访问天眼查搜索**。仅对缺少天眼查信息的企业才发起在线搜索。

```bash
# 使用默认企业名单
node cli.js search

# 使用自定义名单
node cli.js search --company-file /path/to/custom.md
```

**输出：** `data/company_list.csv`

### `download` - 批量下载招投标记录

基于已确认的企业列表，批量下载招投标记录。

```bash
# 使用默认参数（本季度）
node cli.js download

# 指定时间范围和金额门槛
node cli.js download \
  --start-date 2026-01-01 \
  --end-date 2026-03-31 \
  --min-amount 100
```

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--start-date` | string | 本季度第一天 | 开始日期 (YYYY-MM-DD) |
| `--end-date` | string | 今天 | 结束日期 (YYYY-MM-DD) |
| `--min-amount` | number | 0 | 最低金额门槛（万元） |

**输出：** `data/bidding_records.csv`

### `query` - 交互式单企业查询

交互式查询单个企业的招投标记录，支持模糊匹配。

```bash
# 交互式输入
node cli.js query

# 直接指定企业名称
node cli.js query "宇树科技"

# 指定查询参数
node cli.js query "宇树科技" --start-date 2026-01-01 --min-amount 50
```

**交互流程：**
1. 输入企业名称（支持简称/全称/模糊匹配）
2. 在本地企业数据库（`assets/具身智能中游企业数据库.md`）中匹配，**命中则直接使用已有的天眼查全称和链接，无需在线搜索**
3. 如有多个匹配，显示列表供选择
4. 输入时间范围和金额门槛
5. 自动采集并保存结果

## Data Format

### 输入：企业名单（Markdown 表格）

```markdown
| 索引 | 企业名称 | 所属领域 | 产品名称 | 城市 | 天眼查企业全称 | 天眼查链接 |
|------|----------|----------|----------|------|----------------|------------|
| 1 | 宇树科技 | 本体 | Unitree H1 | 杭州 | 宇树科技股份有限公司 | https://... |
```

### 输出 1：企业列表（CSV）

路径：`data/company_list.csv`

| 字段 | 说明 |
|------|------|
| 索引 | 企业编号 |
| 企业简称(MD) | 输入的简称 |
| 企业全称(天眼查) | 天眼查完整名称 |
| 公司ID | 天眼查公司ID |
| 天眼查链接 | 企业详情页 URL |
| 所属领域 | 行业领域 |
| 产品名称 | 主要产品 |
| 城市 | 所在城市 |
| 搜索状态 | 已确认/未找到/失败 |

### 输出 2：招投标记录（CSV）

路径：`data/bidding_records.csv`

| 字段 | 说明 |
|------|------|
| 企业名称 | 天眼查企业全称 |
| 项目名称 | 招投标项目标题 |
| 公告类型 | 中标公告/招标公告等 |
| 采购人 | 招采单位 |
| 中标金额 | 原始金额文本 |
| 发布日期 | YYYY-MM-DD |
| 天眼查详情页链接 | 项目详情 URL |

## Error Handling

| 错误场景 | 错误信息 | 解决方案 |
|----------|----------|----------|
| Chrome 未连接 | `未检测到 Chrome 远程调试服务` | 按前置准备步骤启动 Chrome |
| 需要安全验证 | `天眼查平台安全验证已触发` | 在 Chrome 窗口中手动完成验证码/滑块 |
| 企业未找到 | `未找到企业"XXX"的搜索结果` | 检查企业名称准确性，或尝试简称 |
| npm 依赖缺失 | `Cannot find package` | 运行 `npm install` |
| 天眼查信息缺失 | `该企业没有天眼查信息` | 先运行 `node cli.js search` |

## Performance Guidelines

- **单次查询建议**: 不超过 200 家企业
- **时间范围建议**: 不超过 1 年，可分季度采集
- **请求频率**: 自动 3-6 秒间隔，避免触发风控
- **安全验证**: 如遇频率过高（>5次/50家），建议暂停 30 分钟

## Expected Output

### 企业搜索确认报告
```
企业搜索完成：共 161 家国内企业
  已确认: 161 家
  未找到: 0 家
  海外跳过: 16 家
```

### 招投标记录摘要
```
招投标记录下载完成
  时间范围: 2026-01-01 至 2026-03-31
  金额门槛: 无门槛
  有记录企业: 28 / 161 家
  符合条件记录: 156 条
```
