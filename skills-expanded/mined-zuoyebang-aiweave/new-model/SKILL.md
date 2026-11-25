---
name: new-model
description: 根据 database_design.md 的 DDL 生成或更新 GORM Model 文件。自动选择正确的包、类型映射和 tag 格式。
disable-model-invocation: true
argument-hint: <表名> 例如 user 或 transaction 或 all
---

根据 `$ARGUMENTS` 从 DDL 文档生成 GORM Model 文件。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 特定内容如下。

## 第 0 步：拒绝规则与依赖前置

- ⛔ 拒绝（§A.1）：表名属于 `BUILD_STATUS.md` §0 的 🚫 模块时立即拒绝
- 状态检查（§A.2）：读 `BUILD_STATUS.md` §3 模型层明细
- 依赖（§A.3）：目标包目录（`models/db_xxx/`）不存在则先创建

## 第 1 步：读取 DDL（公共必读见 §B）

- 主文档：`docs/schema/database_design.md`
- 如参数为 `all`，提取所有表 DDL；否则定位到指定表
- 确认表所属库（§1 表清单 / §2 分库设计）

## 第 2 步：确定文件路径与类型映射

| 数据库 | Go 包 | 目录 |
|--------|-------|------|
| db_xxx_core | db_xxx_core | models/db_xxx_core/ |
| db_xxx_trade | db_xxx_trade | models/db_xxx_trade/ |
| db_xxx_log | db_xxx_log | models/db_xxx_log/ |
| db_xxx_call_log | db_xxx_call_log | models/db_xxx_call_log/ |

**类型映射**：
- bigint unsigned NOT NULL AUTO_INCREMENT → `uint64`
- varchar(N) NOT NULL → `string`；可空 → `*string`
- tinyint NOT NULL → `int8`；可空 → `*int8`
- int NOT NULL → `int`；bigint NOT NULL → `int64`
- decimal NOT NULL → `float64`
- datetime NOT NULL → `time.Time`
- date NOT NULL → `string`（YYYY-MM-DD）

## 第 3 步：生成 struct

```go
package {db_package}

import "time"

type {StructName} struct {
    ID        uint64    `gorm:"column:id;primaryKey" json:"id"`
    Field1    string    `gorm:"column:field_1;type:varchar(32);not null;default:''" json:"field_1"`
    Status    int8      `gorm:"column:status;not null;default:0" json:"status"`
    Deleted   int8      `gorm:"column:deleted;not null;default:0" json:"deleted"`
    CreatedAt time.Time `gorm:"column:created_at;not null" json:"created_at"`
    UpdatedAt time.Time `gorm:"column:updated_at;not null" json:"updated_at"`
}

func ({StructName}) TableName() string {
    return "{table_name}"
}
```

按月分片表需额外 `ShardTableName`：

```go
func ShardTableName(t time.Time) string {
    return fmt.Sprintf("{table}_%s", t.Format("200601"))
}
```

**GORM tag 规则**：必含 `column:{snake}`；主键 `primaryKey`；varchar/decimal/text 加 `type:{完整类型}`；NOT NULL → `not null`；DEFAULT → `default:{值}`；敏感字段（凡含密钥 / 哈希 / token 类——落地按业务字段名补充）`json:"-"`。

## 第 4 步：已有文件处理 + 文档同步（公共项见 §C）

- 文件已存在 → 逐字段对比 + 报告差异 → **不自动覆盖**，待用户确认
- 更新 `BUILD_STATUS.md` §3 对应行：⬜ → 🟢

## 第 5 步：测试同步（公共标准见 §D）

Model 层无独立业务逻辑，**不强制**单元测试。需校验 `test/fixtures/seed/*.sql` 与 struct 字段一致。

## 第 6 步：验证（公共格式见 §E）

```bash
go build ./models/{db_package}/...
go vet ./models/{db_package}/...
```


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
