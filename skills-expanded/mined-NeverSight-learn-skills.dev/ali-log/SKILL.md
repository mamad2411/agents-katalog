---
name: ali-log
description: 阿里云日志服务(SLS)查询工具，支持拉取原始日志、查询分析日志、日志下载任务、获取游标等操作。包含查询构建器、SQL模板、函数参考。支持大数据量日志异步下载（>5000条）。所有配置从环境变量读取。
---

# ali-log

## Overview

阿里云日志服务(SLS) Python SDK的封装，提供简单易用的日志查询功能。支持：
- 拉取原始日志 (pull_logs)
- 查询分析日志 (query_logs)
- **日志下载任务 (create_download_job)** - 支持大日志量异步下载
- 通过时间获取游标 (get_cursor)
- 通过游标获取时间 (get_cursor_time)
- **查询构建器** - 便捷的查询语句构建
- **SQL分析构建器** - SQL语句链式构建
- **查询模板** - 常用查询场景模板
- **性能优化建议** - 查询优化指导

## 数据量限制说明

| 查询方式 | 数据量限制 | 适用场景 |
|----------|-----------|----------|
| `query_logs` | 单次最多返回100条 | 小数据量实时查询 |
| `query_all_logs` | 建议最多5000条 | 中等数据量分页查询 |
| `create_download_job` | 仅查询无限制，SQL分析100万行/2GB | **大量日志下载（推荐）** |

**重要提示**：当需要查询/下载的日志数量超过5000条时，强烈建议使用 `create_download_job` 创建日志下载任务，因为：
1. `query_logs` 接口有分页限制（单次最多100条），大量数据查询效率低
2. 长时间分页查询可能导致超时
3. 下载任务支持异步执行，完成后从OSS下载，稳定可靠

## 文件结构

```
~/.claude/skills/ali-log/
├── SKILL.md              # 本文件
├── ali_log.py           # 核心客户端实现
├── query_builder.py     # 查询/SQL构建器
├── QUERY_REFERENCE.md   # 完整函数参考手册
└── requirements.txt     # 依赖
```

## 环境变量配置

在使用前需要配置以下环境变量：

```bash
# 阿里云访问密钥（必填）
export ALIBABA_CLOUD_ACCESS_KEY_ID="your-access-key-id"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="your-access-key-secret"

# 日志服务端点（必填）
export ALIBABA_CLOUD_LOG_ENDPOINT="cn-hangzhou.log.aliyuncs.com"

# 默认项目配置（可选）
export ALIBABA_CLOUD_LOG_PROJECT="your-project-name"
export ALIBABA_CLOUD_LOG_LOGSTORE="your-logstore-name"
```

## When to Use

- 查询阿里云SLS日志服务中的日志数据
- 分析日志内容，排查问题
- 获取特定时间范围的日志
- 实时拉取日志数据

## Quick Reference

### 基本用法

```python
from ali_log import AliLogClient

# 初始化客户端（自动从环境变量读取配置）
client = AliLogClient()

# 查询日志
logs = client.query_logs(
    from_time="2024-01-01 00:00:00",
    to_time="2024-01-01 23:59:59",
    query="* | SELECT * FROM log LIMIT 100"
)
```

### 方法说明

| 方法 | 用途 | 适用场景 |
|------|------|----------|
| `pull_logs` | 拉取原始日志 | 实时消费、数据同步 |
| `query_logs` | 查询分析日志 | 日志检索、统计分析（少量数据） |
| `get_cursor` | 获取时间游标 | 定位日志位置 |
| `list_shards` | 列出所有分区 | 了解Logstore结构 |
| `query_all_logs` | 查询所有日志 | 自动分页获取（建议≤5000条） |
| `create_download_job` | 创建日志下载任务 | 单时间段下载 |
| `batch_download_logs` | 批量并行下载 | **大时间范围下载（推荐）** |
| `get_download_job` | 获取下载任务状态 | 查询任务进度 |
| `wait_for_download_job` | 等待下载任务完成 | 同步等待任务 |

## 查询构建器

### QueryBuilder - 构建查询语句

```python
from query_builder import QueryBuilder, SQLBuilder, QueryTemplates

# 构建查询语句
qb = QueryBuilder()
query = (qb
    .field("level", "ERROR")
    .and_()
    .field("status", 500, ">=")
    .or_()
    .wildcard("uri", "/api/*")
    .build())
# 结果: level:ERROR and status>=500 or uri:/api/*
```

### SQLBuilder - 构建SQL分析语句

```python
from query_builder import SQLBuilder

# 构建SQL分析
sql = (SQLBuilder("*")
    .select_count("pv")
    .group_by_time("minute", format_str="%H:%i")
    .where_last_hours(1)
    .order_by("time")
    .limit(100)
    .build())
# 结果: * | SELECT count(*) as pv, date_format(...) ...
```

### QueryTemplates - 常用模板

```python
from query_builder import QueryTemplates

# 错误日志查询
query = QueryTemplates.error_logs()
# level:ERROR or level:FATAL or level:CRITICAL

# PV趋势SQL
sql = QueryTemplates.sql_pv_trend()

# 错误率统计
sql = QueryTemplates.sql_error_rate()

# Top URL统计
sql = QueryTemplates.sql_top_urls(top_n=10)
```

## Rules

1. **优先使用query_logs** - 大多数查询场景使用query_logs，pull_logs仅用于实时消费场景
2. **大数据量使用下载任务** - **当需要查询/下载超过5000条日志时，必须使用 `create_download_job` 创建日志下载任务**，避免超时和效率问题
3. **注意时间范围** - 查询时间范围不能超过24小时（部分接口限制）
4. **处理分页** - 大量日志需要分页获取，使用offset参数
5. **异常处理** - 所有方法可能抛出LogException，需要适当处理
6. **游标有效期** - 获取的游标有有效期，过期后需要重新获取
7. **GROUP BY优化** - 避免对字符串列进行分组，使用数值计算代替
8. **使用近似函数** - 大数据量时使用approx_distinct代替count(distinct)
9. **避免字符串生成** - 时间分组时使用date_trunc，避免date_format

## Example Usage

### 场景1：查询特定时间范围的ERROR日志

```python
from ali_log import AliLogClient

client = AliLogClient()
logs = client.query_logs(
    project="my-project",
    logstore="app-logs",
    from_time="2024-01-01 10:00:00",
    to_time="2024-01-01 11:00:00",
    query='level: ERROR | SELECT * FROM log LIMIT 100'
)
for log in logs:
    print(log)
```

### 场景2：实时拉取日志

```python
from ali_log import AliLogClient
import time

client = AliLogClient()

# 获取当前游标
cursor = client.get_cursor(
    logstore="app-logs",
    shard_id=0,
    timestamp=time.time()
)

# 轮询拉取新日志
while True:
    logs, next_cursor = client.pull_logs(
        logstore="app-logs",
        shard_id=0,
        cursor=cursor,
        count=100
    )
    for log in logs:
        print(log)
    cursor = next_cursor
    time.sleep(1)
```

### 场景3：统计分析日志

```python
from ali_log import AliLogClient

client = AliLogClient()

# 统计每分钟的错误数量
result = client.query_logs(
    from_time="2024-01-01 00:00:00",
    to_time="2024-01-01 23:59:59",
    query='''
        level: ERROR |
        SELECT date_trunc('minute', __time__) as time,
               count(*) as error_count
        FROM log
        GROUP BY time
        ORDER BY time
    '''
)
print(result)
```

### 场景4：使用查询构建器

```python
from ali_log import AliLogClient
from query_builder import QueryBuilder, SQLBuilder, QueryTemplates

client = AliLogClient()

# 方式1: 使用QueryBuilder构建查询
qb = QueryBuilder()
query = qb.field("level", "ERROR").and_().range_field("status", 500, 599).build()
logs = client.query_logs(
    from_time="2024-01-01 00:00:00",
    to_time="2024-01-01 23:59:59",
    query=f"{query} | SELECT * FROM log LIMIT 100"
)

# 方式2: 使用SQLBuilder构建分析语句
sql = (SQLBuilder("level:ERROR")
    .select_count("error_count")
    .group_by_time("hour")
    .where_last_hours(24)
    .build())
logs = client.query_logs(
    from_time="2024-01-01 00:00:00",
    to_time="2024-01-01 23:59:59",
    query=sql
)

# 方式3: 使用模板
sql = QueryTemplates.sql_pv_trend(unit="hour")
result = client.query_logs(
    from_time="2024-01-01 00:00:00",
    to_time="2024-01-01 23:59:59",
    query=sql
)
```

### 场景5：JSON日志分析

```python
from ali_log import AliLogClient

client = AliLogClient()

# 分析JSON格式的日志
result = client.query_logs(
    from_time="2024-01-01 00:00:00",
    to_time="2024-01-01 23:59:59",
    query='''
        * |
        SELECT
            json_extract_scalar(message, '$.level') as log_level,
            json_extract_scalar(message, '$.service') as service_name,
            count(*) as count
        GROUP BY log_level, service_name
        ORDER BY count DESC
    '''
)
```

### 场景6：性能分析

```python
from ali_log import AliLogClient

client = AliLogClient()

# 查询P50, P90, P99延迟
result = client.query_logs(
    from_time="2024-01-01 00:00:00",
    to_time="2024-01-01 23:59:59",
    query='''
        * |
        SELECT
            approx_percentile(request_time, 0.5) as p50,
            approx_percentile(request_time, 0.9) as p90,
            approx_percentile(request_time, 0.99) as p99,
            avg(request_time) as avg_time
        FROM log
    '''
)

# 查询慢请求Top 10
slow_logs = client.query_logs(
    from_time="2024-01-01 00:00:00",
    to_time="2024-01-01 23:59:59",
    query='''
        * |
        SELECT request_uri, request_time, remote_addr
        ORDER BY request_time DESC
        LIMIT 10
    '''
)
```

### 场景7：地理分布分析

```python
from ali_log import AliLogClient

client = AliLogClient()

# 按省份统计访问量
result = client.query_logs(
    from_time="2024-01-01 00:00:00",
    to_time="2024-01-01 23:59:59",
    query='''
        * |
        SELECT
            ip_to_province(remote_addr) as province,
            count(*) as pv
        GROUP BY province
        ORDER BY pv DESC
        LIMIT 20
    '''
)
```

### 场景8：下载大量日志（超过5000条）

```python
from ali_log import AliLogClient

client = AliLogClient()

# 方式1：简单下载（适合单个小时间段）
job_name = client.create_download_job(
    name="download-job-001",
    from_time="2024-01-01 00:00:00",
    to_time="2024-01-01 01:00:00",
    query="level: ERROR",
    oss_bucket="my-oss-bucket"
)

job_info = client.wait_for_download_job(job_name)
print(f"文件链接: {job_info['executionDetails']['filePath']}")

# 方式2：批量并行下载（推荐，适合大时间范围）
# 将2小时拆分为10分钟段并行下载，大幅提升效率
results = client.batch_download_logs(
    from_time="2024-01-01 00:00:00",
    to_time="2024-01-01 02:00:00",
    query="*",
    chunk_minutes=10,      # 每段10分钟
    max_workers=3,         # 最多3个并发（阿里云限制）
    oss_bucket="my-oss-bucket",
    oss_prefix="logs/2024-01-01/"
)

for r in results:
    print(f"日志数: {r['executionDetails']['logCount']}, "
          f"文件: {r['executionDetails']['filePath']}")
```

## 参考文档

## 参考文档

- **QUERY_REFERENCE.md** - 完整的SQL函数参考手册，包含：
  - 所有聚合函数
  - 字符串函数
  - JSON函数
  - 日期时间函数
  - IP函数
  - 条件表达式
  - 20+ 常用查询示例
  - 性能优化建议

## 常见问题与注意事项 (Troubleshooting)

### 1. 初始化客户端时必须传入 endpoint

**问题**: `ValueError: endpoint is required, set ALIBABA_CLOUD_LOG_ENDPOINT env var or pass endpoint parameter`

**解决**:
```python
# 方式1: 通过参数传入
client = AliLogClient(endpoint="cn-beijing.log.aliyuncs.com")

# 方式2: 设置环境变量
export ALIBABA_CLOUD_LOG_ENDPOINT="cn-beijing.log.aliyuncs.com"
client = AliLogClient()
```

### 2. 查询语法不支持某些 SPL 语法

**问题**: `LogException: invalid query: this spl is not supported translate to sql, column cannot be predicted`

**解决**: 阿里云 SLS 不支持 `* | LIMIT 5` 这种 SPL 语法，应直接使用：
```python
# ❌ 错误
logs = client.query_logs(query="* | LIMIT 5")

# ✅ 正确
logs = client.query_logs(query="*", limit=5)
```

### 3. query_logs 返回的是 QueriedLog 对象，不是字典

**问题**: `AttributeError: 'QueriedLog' object has no attribute 'get'`

**解决**: 需要通过 `get_contents()` 方法获取内容，内容为字典格式：
```python
logs = client.query_logs(query="*")

for log in logs:
    # log 是 QueriedLog 对象
    contents = log.get_contents()  # 返回 dict
    timestamp = log.get_time()     # 返回 Unix 时间戳
    source = log.get_source()      # 返回日志来源

    # 对于 JSON 格式的日志
    if 'content' in contents:
        import json
        data = json.loads(contents['content'])
```

### 4. 时间范围选择要适当

**问题**: 查询最近5分钟返回空结果

**解决**: 适当扩大时间范围，或检查日志是否正常产生：
```python
from datetime import datetime, timedelta

# 如果5分钟没有数据，尝试30分钟
to_time = datetime.now()
from_time = to_time - timedelta(minutes=30)  # 扩大到30分钟

logs = client.query_logs(
    from_time=from_time.strftime('%Y-%m-%d %H:%M:%S'),
    to_time=to_time.strftime('%Y-%m-%d %H:%M:%S'),
    query="*"
)
```

### 5. 项目/Logstore 必须显式指定

**问题**: `ValueError: project is required` 或 `ValueError: logstore is required`

**解决**: 每次查询都要指定 project 和 logstore，或在初始化时设置默认值：
```python
# 方式1: 查询时指定
logs = client.query_logs(
    project="your-project",
    logstore="your-logstore",
    query="*"
)

# 方式2: 初始化时设置默认值
client = AliLogClient(
    endpoint="cn-beijing.log.aliyuncs.com",
    project="your-project",      # 设置默认 project
    logstore="your-logstore"     # 设置默认 logstore
)
logs = client.query_logs(query="*")  # 不需要再传 project/logstore
```

## 查询优化技巧

### 1. 使用近似函数提高性能

```sql
-- 慢：精确去重
SELECT count(distinct user_id) as uv

-- 快：近似去重
SELECT approx_distinct(user_id) as uv
```

### 2. 避免字符串操作分组

```sql
-- 慢：字符串分组
SELECT date_format(__time__, '%Y-%m-%d %H') as hour, count(*)
GROUP BY hour

-- 快：数值计算分组
SELECT __time__ - __time__ % 3600 as hour, count(*)
GROUP BY hour
```

### 3. 使用GROUP BY优化

```sql
-- 快：字典大的字段放前面
SELECT user_id, status, count(*)
GROUP BY user_id, status
```
