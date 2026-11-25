---
name: gomtm-task
description: Use when 执行 gomtm 系统下基于脚本的设备任务自动化, 需要通过 mtmai task 命令下发脚本、查询任务状态或排查任务执行结果.
---

# gomtm-task

## Overview

默认主线是使用 `mtmai task ...` 完成本地脚本读取、目标设备筛选、任务下发和结果查询。

`psql` 只作为诊断和核验手段保留, 不再作为默认工作流直接裸调数据库 RPC。

## Primary Workflow

1. 先用 `mtmai task list --target ...` 确认命中的设备。
2. 再用 `mtmai task push --target ... --file ...` 提交本地脚本。
3. 记录输出里的 `task_id` 或 `batch_id`。
4. 单任务用 `mtmai task get <task-id>` 或 `mtmai task wait <task-id>` 查看结果。
5. 批量任务用 `mtmai task wait --batch <batch-id>` 聚合查看结果。

## Script Types

- `python`
- `bash`
- 默认按文件后缀推断: `.py` -> `python`, `.sh` -> `bash`
- 需要时可用 `--type` 显式覆盖

## Examples

### 先查看目标设备

```bash
mtmai task list --target "platform=linux"
```

### 向单台或多台设备下发本地脚本

```bash
mtmai task push --target "id=DEVICE_UUID" --file ./mtmai/scripting/demo_task.py
mtmai task push --target "name~worker,platform=linux" --file ./mtmai/scripting/demo_task.py
```

说明:

- 单设备命中就是一条任务。
- 多设备命中会按设备 fan-out 成多条任务。
- 当前接受的命令面包含 `push`, `list`, `get`, `wait`。
- `mtmai task push --wait` 目前还未实现, 不要把它当作可用工作流。

### 查看单个任务结果

```bash
mtmai task get <task-id>
mtmai task wait <task-id>
```

重点关注输出中的:

- `Status`
- `Result summary`
- `Error summary`
- `Batch`
- `Source`

### 等待一批任务完成

```bash
mtmai task wait --batch <batch-id>
```

## Selector Notes

`--target` 支持轻量 selector:

- `key=value` 精确匹配
- `key~value` 子串匹配
- 当前支持键: `id`, `name`, `platform`, `tag`, `archived`

例子:

```bash
mtmai task list --target "platform=linux,name~worker"
mtmai task list --target "tag=testing,archived=false"
```

### 典型诊断查询

查看设备列表 RPC 返回:

```bash
psql "$SUPABASE_DATABASE_URL" -c "select * from public.device_list_cursor(p_platform := null, p_include_archived := true);"
```

查看单任务详情 RPC 返回:

```bash
psql "$SUPABASE_DATABASE_URL" -c "select * from public.device_task_get(p_id := 'TASK_ID');"
```

查看最近任务列表, 然后按 `metadata->>'batch_id'` 核对批次:

```bash
psql "$SUPABASE_DATABASE_URL" -c "select id, status, device_id, metadata from public.device_task_list_cursor(p_limit := 20);"
```


## 相关设备命令

```bash
# 远程设备接入当前主线
mtmai device install <DEVICE_ID>
mtmai device activate <DEVICE_ID>
mtmai device uninstall <DEVICE_ID>
mtmai device wait <DEVICE_ID>
```

历史说明: 旧 `mtmai onboarding ...` 与 `device_accesses` / `device_access_jobs` 已退役, 这里只保留名词提醒, 不能当作当前命令面使用.
