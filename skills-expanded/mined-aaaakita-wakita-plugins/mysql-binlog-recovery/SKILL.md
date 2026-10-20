---
name: mysql-binlog-recovery
description: >
  MySQL 数据被误覆盖/误删/误更新后的 binlog 前行镜像恢复流程。当用户说"数据被覆盖了""恢复旧值""找回之前的内容""误删了""刚才的
  UPDATE 写错了""种子同步把用户数据冲了"时使用。覆盖 docker 化 MySQL（容器无
  mysqlbinlog）、ROW 格式 binlog 离线解析、mysqldump 备份兜底三条路径。
---

# MySQL binlog 数据恢复 Playbook

适用前提：`binlog_format=ROW` 且 `log_bin=ON`（MySQL 8 默认开启）。恢复的是**被覆盖前的行内容**（前行镜像），不是回滚事务。

## 第 0 步：先冻结现场，再动手

- 确认被覆盖的**表、行、时间窗**（问用户或查应用日志/审计）。时间窗越窄，解析越快。
- 告诉相关方先别再写这张表——后续写入会让 binlog 里的"前行镜像"被更新的覆盖冲掉。
- 全程**不碰在跑服务的正常流量**；恢复写回时优先走业务 API（见第 4 步）。

## 第 1 步：先找 mysqldump 备份（最便宜的路径）

每日定时备份里的旧值如果满足需求，直接用，不必碰 binlog。

本项目（YSYweb）备份在 `yuqing_backup` 容器 `/backups/YYYYMMDD_HHMMSS/mysql_all.sql.gz`（每日 01:29）：

```bash
docker exec yuqing_backup ls -lt /backups/
docker cp yuqing_backup:/backups/<dir> /tmp/yq_backup
zcat /tmp/yq_backup/mysql_all.sql.gz | grep -A5 "INSERT INTO \`<表名>\`"
```

备份不含目标版本（覆盖发生在备份之后）→ 走 binlog。

## 第 2 步：定位覆盖时刻所在的 binlog 文件

```bash
docker exec <mysql容器> sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e "SHOW BINARY LOGS; SHOW MASTER STATUS"'
docker exec <mysql容器> ls -l --time-style=full-iso /var/lib/mysql/binlog.*
```

按**文件 mtime** 选覆盖时刻所在的最新 binlog（ROW 事件顺序追加，目标通常就在当前活跃文件里）。

## 第 3 步：离线解析 binlog 取前行镜像

**坑（都踩过，别再趟）**：
- 应用 MySQL 容器里**没有 mysqlbinlog**；`mysql:8.0` 镜像里也没有（`/usr/bin`、`/usr/sbin` 都没有）。不要试图 `docker run --entrypoint mysqlbinlog mysql:8.0`。
- 宿主解析用 `pymysqlreplication`（Python 库），它**即使离线读文件也需要连一次真实库**拿 schema，且要求 `server_id` 和 `REPLICATION SLAVE` 权限。
- `binlog_row_metadata` 不是 FULL 时，解出的行 dict 键是 `UNKNOWN_COL0..N`（按列序），对着 `DESCRIBE 表` 数列位即可。

```bash
# 拷出 binlog（容器内路径不可直接读，volume 需要 root）
docker cp <mysql容器>:/var/lib/mysql/binlog.0000NN /tmp/binlog.target

# 装解析器（uv 建的 venv 没有 pip，用 uv pip）
uv pip install --python <venv>/bin/python -q mysql-replication

# 临时授权（用完必须收回，见第 5 步）
docker exec <mysql容器> sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e "GRANT REPLICATION SLAVE ON *.* TO \"<用户>\"@\"%\""'
```

```python
import datetime
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import UpdateRowsEvent, DeleteRowsEvent

stream = BinLogStreamReader(
    connection_settings={"host": "127.0.0.1", "port": 6212, "user": "<用户>", "passwd": "<密码>"},
    server_id=9999,                      # 必填，否则 TypeError
    log_file="/tmp/binlog.target",
    log_pos=4,
    resume_stream=False, blocking=False,  # 离线读文件模式
    only_events=[UpdateRowsEvent, DeleteRowsEvent],
    only_tables=["<表名>"], only_schemas=["<库名>"],
)
for ev in stream:
    ts = datetime.datetime.fromtimestamp(ev.timestamp)
    if not (开始 <= ts <= 结束):          # 按第 0 步的时间窗过滤
        continue
    for row in ev.rows:
        before = row.get("before_values")  # UPDATE/DELETE 的前行镜像=被覆盖前的值
        print(ts, before)
```

- `WriteRowsEvent` 没有 before（新增）；`DeleteRowsEvent` 的 `values` 即被删行。
- 同一行短时间被改多次时，**最后一次覆盖事件的 before_values = 用户最终版**，链式往前追可看完整编辑史。

## 第 4 步：恢复写回——走业务渠道，不直接改库

若该表有管理后台/公开 API（如本项目 prompt_fixed_blocks 有 PUT 端点），用 API 写回：触发正常的校验、缓存失效、审计日志。仅当无业务通道（纯数据表）时才直接 SQL 写回，并向用户说明绕过了业务层。

## 第 5 步：验证与清理（缺一不可）

1. 回读目标行，逐字段确认已是恢复值。
2. 收回临时授权：`REVOKE REPLICATION SLAVE ON *.* FROM "<用户>"@"%"; FLUSH PRIVILEGES;`
3. 删除拷出的 binlog、临时 token、备份副本（含敏感数据，不留痕）。
4. 向用户报告：恢复了什么、恢复到的版本时刻、数据来源（备份还是 binlog）。

## 预防（恢复成功后提醒用户）

这次能找回是靠 binlog/备份兜底。根源多是"把用户可在线编辑的数据当成陈旧种子/缓存直接覆盖"。同步或重置这类数据前必须先做新旧方向 diff——见 `config-sync-guard` skill。
