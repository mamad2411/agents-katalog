---
name: xjtu-doctor-scraper
description: 爬取西安交通大学第一附属医院官网医生列表的专用技能。触发条件：用户要求爬取该医院的医生信息、专家列表、科室医生等。This skill provides complete workflow for scraping doctor listings from XJTU First Affiliated Hospital website, including URL structure discovery, API analysis, batch crawling with CSV output.
agent_created: true
---

# 西安交通大学第一附属医院医生列表爬虫

## 概述

从官网 `http://www.dyyy.xjtu.edu.cn` 爬取医生列表和详情，输出CSV。

## 网站架构

- **主页面**：`/zjjs.htm`（静态HTML，约730个医生链接）
- **医生详情页**：`/zjjs/{大类}/{小类}/{缩写}.htm`（Vue.js动态渲染）
- **数据API**：`GET /services/industry/patient/static/userDoctor/detailByAccount/{account_id}`
- **account_id来源**：从详情页HTML中提取 `detailByAccount/(\d+)`

### URL路径深度区分

主页面链接包含两类，通过路径深度区分：

| 类型 | URL示例 | 路径深度 | 处理方式 |
|------|---------|----------|----------|
| 科室分类页面 | `zjjs/nkxt/e_k.htm` | 3级（`zjjs/大类/小类.htm`） | 跳过，无account_id |
| 医生详情页面 | `zjjs/nkxt/e_k/lxh.htm` | 4级（`zjjs/大类/小类/医生缩写.htm`） | 爬取详情 |

脚本已内置过滤逻辑，自动跳过3级路径的科室分类页面。

## 使用脚本

唯一脚本 `scripts/scrape.py`，支持三个子命令：

### ⚠️ Windows系统必读

Windows CMD默认使用GBK编码，无法显示脚本中的emoji字符（✅、⚠️）和部分中文特殊字符。**运行前必须设置UTF-8编码**：

```bash
# Windows CMD/PowerShell
export PYTHONIOENCODING=utf-8 && python scripts/scrape.py parse doctors_list.json

# 或使用chcp切换编码页
chcp 65001 && python scripts/scrape.py parse doctors_list.json
```

### 1. parse — 解析主页面
```bash
python scripts/scrape.py parse doctors_list.json
```
输出 `doctors_list.json`：`[[医生名, URL, 大类代码, 小类代码], ...]`

### 2. batch — 分批爬取详情
```bash
python scripts/scrape.py batch doctors_list.json output.csv 0 100
python scripts/scrape.py batch doctors_list.json output.csv 100 100
# ... 分8批直到完成
```
- 支持断点续爬（已存在的医生名自动跳过）
- 每条间隔0.2秒，避免请求过快

### 3. fix — 修复已有CSV字段
```bash
python scripts/scrape.py fix doctors_list.json input.csv output.csv
```

## ⚠️ 三大踩坑点

### 1. 图片URL — photoShortUrl
- ✅ `photoShortUrl` 是**UUID格式**：`85d0473b-5526-4617-ab8e-96ef69bc4727`
- ❌ 不要用 `doctorAccount`（数字如`000506`）作shortcode → 返回"文件不存在"
- 图片URL = `/services/industry/app-filesystem/file-show?appId=patient&shortcode={photoShortUrl}`
- 约76%医生有photoShortUrl，14%为空

### 2. 研究方向与专长 — acaTitle
- ✅ 用 `acaTitle`（可读文本，如"儿童生长发育及发育相关疾病..."）
- ❌ 不要用 `goodDirectionList`（只是UUID代码如`fea993f4d2914b908cd4fdfeec3eef39`）

### 3. 并发控制
- ❌ 高并发（20-40线程）容易中断
- ✅ 分批顺序执行，每批100条，0.2秒延迟

## 字段映射

| CSV字段 | API字段 | 说明 |
|---------|---------|------|
| 科室大类 | depTypeDicCodeName | 如"内科系统" |
| 科室小类 | parentDepTypeDicCodeName | 可能为空 |
| 科室名称 | departmentName | 如"儿科" |
| 医生名称 | name | |
| 医生职称 | docJobTitleDicCodeName | 如"主任医师" |
| 医生科室 | departmentName + " " + hospitalName | |
| 研究方向与专长 | **acaTitle** | ⚠️不用goodDirectionList |
| 专家介绍 | introduce | 富文本 |
| 医生图片URL | **photoShortUrl** | ⚠️UUID shortcode，不用doctorAccount |
