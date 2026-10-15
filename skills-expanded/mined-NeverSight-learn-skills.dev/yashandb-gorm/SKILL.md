---
name: yashandb-gorm
name_for_command: yashandb-gorm
description: 指导用户使用 GORM 连接 YashanDB。当用户提到 GORM、ORM、gorm-yasdb 或需要使用 GORM 操作 YashanDB 时，必须使用此技能。
---

# YashanDB GORM 使用指南

本技能指导用户使用 GORM ORM 框架连接和操作 YashanDB。

> **前置依赖**：GORM 依赖 Go 驱动和 C 驱动。请先完成 `/yashandb-go` 和 `/yashandb-c` 安装。

## 依赖关系

```
GORM (gorm-yasdb)
    │
    └──► Go 驱动 (yashandb-go)
              │
              └──► C 驱动 (libyascli) ← 执行 /yashandb-c 安装
```

## 步骤概览

1. 检查前置依赖
2. 安装 GORM 适配插件
3. 基础使用示例

## 第一步：检查前置依赖

### 检查 Go 驱动

```bash
go version
go list -m github.com/yashan-technologies/yashandb-go
```

### 如果未安装

执行 `/yashandb-go` 完成安装，然后继续。

## 第二步：安装 GORM 适配插件

```bash
go get -u github.com/yashan-technologies/yashandb-gorm
```

## 第三步：基础使用示例

### 连接数据库

```go
package main

import (
    "fmt"
    "log"

    yasdb "github.com/yashan-technologies/yashandb-gorm"
    "gorm.io/gorm"
)

func main() {
    dsn := "user/password@192.168.1.2:1688"
    db, err := gorm.Open(yasdb.Open(dsn), &gorm.Config{})
    if err != nil {
        log.Fatalf("连接失败: %v", err)
    }
    fmt.Println("YashanDB 连接成功!")
}
```

### 定义模型

```go
type User struct {
    ID    uint   `gorm:"primaryKey"`
    Name  string `gorm:"size:100"`
    Email string `gorm:"size:100"`
}

func (User) TableName() string {
    return "users"
}
```

### CRUD 操作

```go
// 创建
user := User{Name: "张三", Email: "zhangsan@example.com"}
db.Create(&user)

// 查询
var user User
db.First(&user, 1)
db.First(&user, "name = ?", "张三")

// 更新
db.Model(&user).Update("Email", "newemail@example.com")

// 删除
db.Delete(&user, 1)
```

## 参考文档

- [installation](skills/yashandb-gorm/references/installation.md)
- [basic-usage](skills/yashandb-gorm/references/basic-usage.md)
- [troubleshooting](skills/yashandb-gorm/references/troubleshooting.md)

## 相关技能

- `/yashandb-c` - C 驱动安装（底层依赖）
- `/yashandb-go` - Go 驱动安装（直接依赖）

## 相关资源

- GORM 官方文档：https://gorm.io/docs/
- gorm-yasdb 源码：https://github.com/yashan-technologies/yashandb-gorm
- YashanDB 官方文档：https://doc.yashandb.com