---
name: yashandb-go
name_for_command: yashandb-go
description: 指导用户完成 YashanDB Go 语言开发环境搭建。当用户提到 Go 开发、Go 驱动、yashandb-go 或需要使用 Go 连接 YashanDB 时，必须使用此技能。
---

# YashanDB Go 开发环境搭建

本技能指导用户完成 YashanDB Go 开发环境的完整搭建流程。

> **前置依赖**：Go 驱动依赖 YashanDB C 驱动。如未安装 C 驱动，请先执行 `/yashandb-c` 安装。

## 依赖关系

```
Go 驱动 (yashandb-go)
    │
    └──► C 驱动 (libyascli) ← 执行 /yashandb-c 安装
```

> **ORM 用户**：如需使用 GORM，请执行 `/yashandb-gorm` 技能。

## 步骤概览

1. 检查 C 驱动（前置依赖）
2. 安装 Go 驱动
3. 测试连接

## 第一步：检查 C 驱动

**Go 驱动依赖 C 驱动**（libyascli.so / yascli.dll）。

### 快速检查

```bash
ls ~/.yashandb/client/lib/libyascli.so 2>/dev/null && echo "已安装"
```

### Windows (PowerShell)

```powershell
Test-Path "$env:USERPROFILE\.yashandb\client\lib\yascli.dll"
```

### 如果未安装

执行 `/yashandb-c` 技能安装 C 驱动，然后继续下一步。

## 第二步：安装 Go 驱动

```bash
go get -u github.com/yashan-technologies/yashandb-go
```

或在项目中初始化 Go Modules 并添加依赖：

```bash
go mod init your-project-name
go mod tidy
go get github.com/yashan-technologies/yashandb-go
```

## 第三步：测试连接

连接信息由用户提供的 `{dsn}`，创建一个简单的测试程序：

```go
package main

import (
    "database/sql"
    "fmt"
    _ "github.com/yashan-technologies/yashandb-go"
)

func main() {
    dsn := "{dsn}"
    db, err := sql.Open("yasdb", dsn)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    var result int
    err = db.QueryRow("SELECT 1 FROM dual").Scan(&result)
    if err != nil {
        panic(err)
    }
    fmt.Println("YashanDB 连接成功! 查询结果:", result)
}
```

如果用户提供了 dsn，执行 `go run test.go`，输出 `YashanDB 连接成功! 查询结果: 1` 说明环境搭建完成。

## 参考文档

- [installation](skills/yashandb-go/references/installation.md)
- [connection](skills/yashandb-go/references/connection.md)
- [troubleshooting](skills/yashandb-go/references/troubleshooting.md)

## 相关技能

- `/yashandb-c` - C 驱动安装（前置依赖）
- `/yashandb-gorm` - GORM ORM 使用
- `/yashandb-python` - Python 驱动安装

## 相关资源

- Go 驱动源码：https://github.com/yashan-technologies/yashandb-go
- YashanDB 官方文档：https://doc.yashandb.com