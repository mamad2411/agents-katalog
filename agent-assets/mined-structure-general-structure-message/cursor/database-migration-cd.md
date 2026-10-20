---
description: |
triggers:
  - 数据库迁移
  - Flyway
  - 数据库变更
  - 数据库 CD
  - migration CD
  - 数据库持续部署
  - 数据库部署
role: devops
priority: medium
category: deployment
stack: _common
alwaysApply: false
---


# 数据库迁移 CD

> 在 CI/CD 流水线中安全执行数据库迁移。**生产迁移 MUST 用户确认 + 备份**。

## 核心原则

- ✅ **MUST** 迁移脚本与应用代码同 PR 提交（保持版本一致）
- ✅ **MUST** 迁移在应用部署**之前**执行（先 DB 后 App）
- ✅ **MUST** 迁移前备份生产数据库
- ✅ **MUST** 迁移失败时应用部署中止
- ❌ **MUST NOT** 在生产环境跳过备份直接迁移

## Flyway 迁移工作流

### 在 CI 流水线中的位置

```
代码提交 → 单测 → 打包 → 镜像构建
                              ↓
                       DB 迁移（测试）→ 应用部署（测试）
                              ↓
                       测试验证
                              ↓
                       生产审批（人工）
                              ↓
                       DB 备份（生产）
                              ↓
                       DB 迁移（生产）
                              ↓
                       应用部署（生产）
                              ↓
                       健康检查
```

### GitHub Actions 集成

```yaml
# .github/workflows/deploy.yml
jobs:
  migrate-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Flyway migrate (test)
        run: |
          mvn flyway:migrate \
            -Dflyway.url=jdbc:mysql://test-mysql:3306/mydb \
            -Dflyway.user=${{ secrets.DB_USER }} \
            -Dflyway.password=${{ secrets.DB_PASSWORD }}

  deploy-test:
    needs: migrate-test  # 迁移成功后才部署
    # ...

  migrate-prod:
    needs: approval  # 人工审批后
    runs-on: ubuntu-latest
    steps:
      - name: Backup production DB
        run: |
          mysqldump -h prod-mysql -u ${{ secrets.DB_USER }} -p${{ secrets.DB_PASSWORD }} mydb > backup-$(date +%Y%m%d-%H%M%S).sql

      - name: Run Flyway migrate (prod)
        run: |
          mvn flyway:migrate \
            -Dflyway.url=jdbc:mysql://prod-mysql:3306/mydb \
            -Dflyway.user=${{ secrets.DB_USER }} \
            -Dflyway.password=${{ secrets.DB_PASSWORD }}
```

## 迁移脚本规范

### 命名

```
V<version>__<description>.sql
```

示例：
- `V1_2_0__add_user_table.sql`
- `V1_2_1__add_user_index.sql`

### 位置

```
<module>-repository-mybatis/
└── src/main/resources/
    └── db/migration/
        ├── V1_0_0__init.sql
        ├── V1_1_0__add_user_table.sql
        └── V1_2_0__add_order_table.sql
```

### 关键约束

- ✅ **MUST** 版本号单调递增
- ✅ **MUST** 一个脚本一个目的
- ❌ **MUST NOT** 修改已发布的迁移脚本
- ❌ **MUST NOT** 在迁移脚本里使用数据库特定语法（除非必要）

## 回滚策略

### 向前回滚（推荐）

不写 `down` 迁移，而是写新的 `up` 迁移回退：

```sql
-- V1_2_1__rollback_user_email_index.sql
DROP INDEX idx_email ON user;
```

### 数据库备份 + 恢复（生产兜底）

```bash
# 迁移前备份
mysqldump -h host -u user -p mydb > backup-$(date +%Y%m%d-%H%M%S).sql

# 迁移失败恢复
mysql -h host -u user -p mydb < backup-20260815-103000.sql
```

## 验证

```bash
# 本地验证迁移
mvn flyway:migrate -Dflyway.url=jdbc:h2:mem:test

# 查看迁移历史
mvn flyway:info

# 校验迁移脚本
mvn flyway:validate
```

## 关键约束（MUST 遵守）

- ✅ **MUST** 生产迁移前备份
- ✅ **MUST** 迁移失败时应用部署中止
- ✅ **MUST** 迁移脚本与应用代码同 PR
- ❌ **MUST NOT** 跳过备份直接迁移生产
- ❌ **MUST NOT** 修改已发布的迁移脚本

## 关联

- 前置：`database-design`
- Wiki：`wiki/_common/database-design.md` `wiki/_common/ci-cd-pipeline.md`
- 相关：`ci-pipeline-design` / `deployment-verification`
