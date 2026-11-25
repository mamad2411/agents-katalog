---
name: repo2psm
description: Use when you know the current code repository or workspace and need to find the service PSM from repository files.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# Repo to PSM 查询

## 何时使用

当你已经知道当前代码仓库，想定位该仓库对应的服务 PSM 时使用。

典型场景：

- 用户给了 repo / workspace，让你找服务 PSM
- 后续要查 `psm-info`、`metrics`、`argos-query`，但当前只知道仓库，不知道 PSM

## 硬规则

1. 已知 repo，先用 `repo2psm`，不要默认手工 `grep` `bootstrap.sh` / `settings.py`。
2. 本 skill 只负责 `repo -> psm`，不负责猜 `vregion`。
3. 如果本 skill 返回空字符串，再回退到人工排查仓库文件。

## 规则

- **PSM 定义**: 服务唯一标识，格式为 `{PRODUCT}.{SUBSYSTEM}.{MODULE}` (如 `tiktok.devflow.api`)
- **工作区限制**: 仅在当前工作目录中查找

## 目标

在用户代码库中定位服务 PSM

## 查找策略

根目录下包含 PSM 定义的常见文件和字段名（概率从高到低）：

1. `script/bootstrap.sh` → `PSM` 变量
2. `script/settings.py` → `PRODUCT.SUBSYSTEM.MODULE`
3. `build.sh` → `RUN_NAME` 变量
4. `atum.yaml` → `PSM` 字段

## 输出后的下一步

- 已知 repo，先拿到 `psm`：用本 skill
- 已知 `psm` 后，要看 repo / scm / 部署 region 元信息：再用 `psm-info`
- 如果后续要查 metrics / logs，而用户没给 `vregion`：直接问用户，不要继续猜 region

## 输出

- 精确的 PSM 字符串 (如 `tiktok.devflow.api`)
- 如果无法定位服务 PSM，返回空字符串
