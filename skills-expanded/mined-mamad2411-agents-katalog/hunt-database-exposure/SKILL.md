---
name: hunt-database-exposure
description: 数据库配置、备份、日志与管理面暴露专项：识别范围内公开 database metadata、backup/log/config artifact 和访问控制错误，不连接数据库或使用凭据。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-database-exposure

## 0. Engagement Gate

- 仅在授权、scope、host/身份 baseline 和主编排器路由齐备时执行；本 Skill 规划验证，不授予目标操作权限。
- 只使用自有账户、对象、域名、测试数据、回调和批准速率；WAF、超时、单次异常、扫描器命中均为 `INCONCLUSIVE`。
- 固定执行 `baseline → 单变量 probe → post-baseline → server/browser/monitor oracle → evidence`；出现第三方数据、共享基础设施或不可回滚副作用立即停止。

## 1. Trigger Signals

`database_backup`、`database_log`、`db_config_exposure`、`admin_console_hint`、`connection_string_hint`、`dump_file_url`。

## 2. Preconditions / Discovery

确认文件/console 当前可达、所属/范围、content type、访问控制和是否包含自有 canary；不得把文件名、搜索缓存或错误信息作为暴露证据。

## 3. Minimal Safe Validation

只读取批准的公开自有 canary backup/config/log 元数据，验证列表、ACL、目录索引或错误处理是否泄露不应公开的结构/配置；疑似凭据仅记录字段和 hash。

## 4. Oracle / False Positives

有效：当前范围内资源可重现公开并暴露本不应公开的自有 DB metadata/config/backup 内容，或自有低权身份访问管理面。错误消息、空文件、历史 archive 不成立。

## 5. Stop / Evidence / Routing

停止：数据库连接、凭据使用、数据导出、管理操作。保存 URL/hash/ACL、owner、最小脱敏摘录。SQL 参数问题转 `hunt-sqli`，source/config 转 `hunt-source-leak`。
