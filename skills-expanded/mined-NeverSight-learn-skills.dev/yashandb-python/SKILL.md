---
name: yashandb-python
name_for_command: yashandb-python
description: 指导用户完成 YashanDB Python 语言开发环境搭建。当用户提到 Python 开发、Python 驱动、yaspy、yasdb、PyYasdb 或需要使用 Python 连接 YashanDB 时，必须使用此技能。
---

# YashanDB Python 开发环境搭建

本技能指导用户完成 YashanDB Python 开发环境的完整搭建流程。

> **重要提示**：YashanDB 提供两个 Python 驱动包：**yaspy** 和 **yasdb**。推荐使用 **yaspy**，因为：
> - yaspy 在同等测试环境下有较大性能优势
> - 后续新增功能的演进优先级：yaspy > yasdb
> - 只有 yaspy 支持连接池

> **前置依赖**：Python 驱动依赖 YashanDB C 驱动。如未安装 C 驱动，请先执行 `/yashandb-c` 安装。

## 依赖关系

```
Python 驱动 (yaspy/yasdb)
    │
    └──► C 驱动 (libyascli) ← 执行 /yashandb-c 安装
```

## 步骤概览

1. 检查环境（Python、C 驱动）
2. 安装 Python 驱动
3. 测试连接

## 第一步：检查环境

### 检查 Python

```bash
python --version
pip --version
```

### 检查 C 驱动

```bash
ls ~/.yashandb/client/lib/libyascli.so 2>/dev/null && echo "已安装"
```

### Windows (PowerShell)

```powershell
Test-Path "$env:USERPROFILE\.yashandb\client\lib\yascli.dll"
```

如果 C 驱动未安装，执行 `/yashandb-c` 安装。

## 第二步：安装 Python 驱动

**yaspy 和 yasdb 不在 PyPI 上**，需要从 YashanDB 下载中心获取：
https://download.yashandb.com

根据平台选择对应的 whl 文件安装：

```bash
pip install yaspy-xx.xx-cp38-cp38-win_amd64.whl
```

### 驱动信息

| 属性 | 值 |
|------|-----|
| 推荐包名 | yaspy |
| Python 版本要求 | 3.6.0 及以上 |
| 默认端口 | 1688 |
| 连接池支持 | 仅 yaspy 支持 |

## 第三步：测试连接

### 基础连接方式

```python
import yasdb

# 方式一：使用参数
conn = yasdb.connect(
    host="192.168.1.2",
    port=1688,
    user="system",
    password="oracle"
)

# 执行查询
cursor = conn.cursor()
cursor.execute("SELECT 1 FROM dual")
result = cursor.fetchone()
print(f"YashanDB 连接成功! 查询结果: {result[0]}")

cursor.close()
conn.close()
```

### 连接池（仅 yaspy 支持）

```python
import yaspy

pool = yaspy.SessionPool(
    user="system",
    password="oracle",
    dsn="192.168.1.2:1688",
    min=2,
    max=10,
)

connection = pool.acquire()
cursor = connection.cursor()
cursor.execute("SELECT 1 FROM dual")
print(cursor.fetchone())

cursor.close()
pool.release(connection)
pool.close()
```

## 参考文档

- [installation](skills/yashandb-python/references/installation.md)
- [connection](skills/yashandb-python/references/connection.md)
- [troubleshooting](skills/yashandb-python/references/troubleshooting.md)

## 相关技能

- `/yashandb-c` - C 驱动安装（前置依赖）

## 相关资源

- Python 驱动下载：https://download.yashandb.com
- YashanDB 官方文档：https://doc.yashandb.com