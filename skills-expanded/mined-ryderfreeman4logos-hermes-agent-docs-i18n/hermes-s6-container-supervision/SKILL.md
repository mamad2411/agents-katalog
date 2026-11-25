---
name: hermes-s6-container-supervision
description: Modify or debug s6 services in the Hermes Docker image.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
environments: [s6]
metadata:
  hermes:
    tags: [docker, s6, supervision, gateway, profiles]
    related_skills: [hermes-agent]
---

# Hermes s6-overlay 容器监控功能

## 何时使用此功能

在以下场景中可加载此功能：
- 在 Hermes Docker 镜像中添加或删除静态服务（即那些需要在每个容器启动时都进行监控的服务，例如控制面板）
- 排查为何特定配置文件的网关无法启动、重启失败，或在执行 `docker restart` 后仍无法正常运行
- 了解为何容器的 CMD 命令为 `/opt/hermes/docker/main-wrapper.sh`，以及如何将前置参数传递给用户程序
- 修改 `cont-init.d` 启动脚本（用户 ID 重映射、卷初始化、配置文件同步）
- 更改特定配置文件网关的运行脚本内容（第 4 阶段）

如果您只是运行 Hermes Agent 并希望使用 Docker，建议参阅 `website/docs/user-guide/docker.md` 文档。

## 架构概览

```
/init                                  ← PID 1 (s6-overlay v3.2.3.0)
├── cont-init.d                        ← oneshot setup, runs as root
│   ├── 01-hermes-setup                ← docker/stage2-hook.sh
│   │   ├── UID/GID remap
│   │   ├── chown /opt/data
│   │   ├── chown /opt/data/profiles (every boot)
│   │   ├── seed .env / config.yaml / SOUL.md
│   │   └── skills_sync.py
│   └── 02-reconcile-profiles          ← hermes_cli.container_boot
│       ├── chown /run/service (hermes-writable for runtime register)
│       └── walk $HERMES_HOME/profiles/<name>/gateway_state.json
│           → recreate /run/service/gateway-<name>/
│           → auto-start only those with prior_state == "running"
│
├── s6-rc.d (static services, in /etc/s6-overlay/s6-rc.d/)
│   ├── main-hermes/run                ← exec sleep infinity (no-op slot)
│   └── dashboard/run                  ← if HERMES_DASHBOARD=1, runs `hermes dashboard`
│
├── /run/service (s6-svscan watches; tmpfs)
│   ├── gateway-coder/                 ← runtime-registered per-profile
│   │   ├── type        ("longrun")
│   │   ├── run         ("#!/command/with-contenv sh ... exec s6-setuidgid hermes hermes -p coder gateway run")
│   │   ├── down        (marker — present means "registered but don't auto-start")
│   │   └── log/run     (s6-log → $HERMES_HOME/logs/gateways/coder/current)
│   └── ...
│
└── CMD ("main program")               ← /opt/hermes/docker/main-wrapper.sh
    └── routes user args: bare exec | hermes subcommand | hermes (no args)
        — exec'd by /init with stdin/stdout/stderr inherited (TTY for --tui)
```

## 核心文件

| Path | Role |
|---|---|
| `Dockerfile` | s6-overlay install + cont-init.d wiring + `ENTRYPOINT ["/opt/hermes/docker/entrypoint-dispatch.sh"]` |
| `docker/entrypoint-dispatch.sh` | PID-1 dispatcher: exec's `/init` + main-wrapper when the image owns PID 1; on wrapped runtimes (Fly Machines, `docker run --init`) falls back to stage2-hook + main-wrapper directly, restoring the s6 helper PATH first (#38349). |
| `docker/stage2-hook.sh` | The "old entrypoint logic" — UID remap, chown, seed, skills sync. Runs as cont-init.d/01-hermes-setup. |
| `docker/cont-init.d/02-reconcile-profiles` | Calls `hermes_cli.container_boot` on every boot to restore profile gateway slots from the persistent volume. |
| `docker/main-wrapper.sh` | The container's CMD. Routes user args, drops to hermes via `s6-setuidgid`, exec's the chosen program. |
| `docker/s6-rc.d/main-hermes/run` | No-op `sleep infinity` — slot exists so the s6-rc user bundle is valid; main hermes runs as the CMD, not as a supervised service. |
| `docker/s6-rc.d/dashboard/run` | Conditional service — `exec sleep infinity` unless `HERMES_DASHBOARD` is truthy. |
| `docker/entrypoint.sh` | Back-compat shim that `exec`s the stage2 hook. External scripts that hard-coded the old entrypoint path still work. |
| `hermes_cli/service_manager.py` | `S6ServiceManager`: `register_profile_gateway`, `unregister_profile_gateway`, `start/stop/restart/is_running`, `list_profile_gateways`. |
| `hermes_cli/container_boot.py` | `reconcile_profile_gateways()` — walks persistent profiles, regenerates s6 slots, emits `container-boot.log`. |
| `hermes_cli/gateway.py::_dispatch_via_service_manager_if_s6` | Intercepts `hermes gateway start/stop/restart` and routes to s6 when running in a container. |

## 为何选择架构 B（以 CMD 作为主程序，而非由 s6 监控）

最初的计划（v1–v3）要求将 hermes 主进程作为受 s6-rc 监控的服务来运行。但两个真正的 s6-overlay v3 机制阻碍了这一方案的实现：

1. **cont-init.d 脚本无法接收 CMD 参数**——因此 stage2 钩子程序无法解析 `docker run <image> chat -q "hi"` 这样的命令，进而为相应的 `run` 脚本设置 `HERMES_ARGS`。
2. **`/run/s6/basedir/bin/halt` 不会传递写入到 `/run/s6-linux-init-container-results/exitcode` 中的退出码**。无论怎样，容器始终以 143（SIGTERM）码退出。这一情况已得到 s6 的创建者 skarnet 在 [问题 #477](https://github.com/just-containers/s6-overlay/issues/477) 中的确认：_“如果希望容器正常关闭，要么让 CMD 命令自身返回退出码，要么在没有 CMD 的情况下，手动设置所需的容器退出码后再调用 halt 命令”_。
因此，我们通过调度器采用 `s6-overlay-native CMD` 模式：设置 `ENTRYPOINT ["/opt/hermes/docker/entrypoint-dispatch.sh"]`，该调度器会在进程 ID 为 1 时执行 `/init /opt/hermes/docker/main-wrapper.sh "$@"`。该封装脚本会自动添加到用户参数的前面——这样一来，`docker run <image> --version` 命令就会变为 `/init main-wrapper.sh --version`，而 `--version` 参数便不会被 `/init` 所使用的 POSIX shell 拦截。封装脚本会通过 `s6-setuidgid` 将控制权移交给 hermes，随后再执行用户指定的程序。该程序的退出码即为容器的退出码，这与使用 tini 之前的行为完全一致。当入口点并非进程 ID 1 时（如 Fly Machines 或使用 `docker run --init` 的情况），调度器会完全跳过 `/init` 步骤（否则会因“只能以进程 ID 1 运行”而报错），恢复 s6 相关的路径设置，执行 `stage2-hook.sh`，并直接启动 `main-wrapper.sh`——此时该路径上不会有任何受监控的服务（参见 #38349）。

相应的权衡是：在 s6 环境下，主 hermes 进程处于无监控状态，这与它在 tini 环境下的行为一致（tini 是 s6 之前的镜像）。唯一的**新**保障在于控制台层面的监控功能——而位于 `/run/service/` 目录下的按配置文件划分的网关则享有完全的监控支持。

## 快速操作指南

### 验证运行中的容器中进程 ID 1 是否为 s6

```sh
docker exec <c> sh -c 'cat /proc/1/comm; readlink /proc/1/exe'
# Expect: s6-svscan or init / /package/admin/s6/.../s6-svscan
```

### 检查配置文件网关服务

```sh
# /command/ isn't on docker-exec PATH — use absolute path
docker exec <c> /command/s6-svstat /run/service/gateway-<name>
# "up (pid …) … seconds"            → running
# "down (exitcode N) … seconds, normally up, want up, …" → s6 wants it up but the process keeps exiting (crash loop)
# "down … normally up, ready …"     → user stopped it
```

### 手动启动/停止服务

```sh
docker exec <c> /command/s6-svc -u /run/service/gateway-<name>   # up
docker exec <c> /command/s6-svc -d /run/service/gateway-<name>   # down
docker exec <c> /command/s6-svc -t /run/service/gateway-<name>   # SIGTERM (restart)
```

### 查看 cont-init 一致性检查器日志

```sh
docker exec <c> tail -n 50 /opt/data/logs/container-boot.log
# 2026-05-21T06:18:05+0000 profile=coder prior_state=running action=started
# 2026-05-21T06:18:05+0000 profile=writer prior_state=stopped action=registered
```

### 添加新的静态服务

1. 创建 `docker/s6-rc.d/<名称>/type` 文件，内容为 `longrun\n`；同时创建 `docker/s6-rc.d/<名称>/run` 文件（内容应为 `#!/command/with-contenv sh` 加上 `# shellcheck shell=sh`）。
2. 在运行脚本的开头通过 `s6-setuidgid hermes` 命令将其权限设置为 hermes 用户（除非确实需要 root 权限）。
3. 创建空的 `docker/s6-rc.d/<名称>/dependencies.d/base` 文件，以便该服务能够等待基础资源包准备就绪。
4. 创建空的 `docker/s6-rc.d/user/contents.d/<名称>` 文件，以便该服务能够加入用户相关资源包。
5. Dockerfile 中的 `COPY docker/s6-rc.d/` 指令会自动加载这些文件——无需其他修改。

### 修改针对不同配置文件的网关运行命令

编辑 `hermes_cli/service_manager.py` 文件中的 `S6ServiceManager._render_run_script` 函数。在系统启动时进行服务同步时，`hermes_cli/container_boot.py::_register_service` 也会调用该函数，因此它是配置的唯一权威来源。请同时更新 `tests/hermes_cli/test_service_manager.py::test_s6_register_creates_service_dir_and_triggers_scan` 测试文件中的相应断言。

### 运行 Docker 测试套件

```sh
docker build -t hermes-agent-harness:latest .
HERMES_TEST_IMAGE=hermes-agent-harness:latest scripts/run_tests.sh tests/docker/ -v
# Expect 19 passed, 0 xfailed against the s6 image
```

该测试框架位于 `tests/docker/` 目录中，当无法使用 Docker 时将跳过相关测试。每个测试的超时时间已被延长至 180 秒（详见 `tests/docker/conftest.py`）。

## 常见问题

### 使用 `docker exec` 时出现“命令未找到”的错误

`s6-overlay` 会将其二进制文件放置在 `/command/` 目录中，但该路径仅对监控树中启动的进程有效——即服务、cont-init.d 脚本以及 main-wrapper.sh。执行 `docker exec <c> s6-svstat …` 时会因“命令未找到”而失败；应始终使用绝对路径 `/command/s6-svstat`。而 `hermes` 可以正常运行，是因为 Dockerfile 将 `/opt/hermes/.venv/bin` 添加到了运行时的 `ENV PATH` 环境变量中。

### 配置文件目录的所有权问题

cont-init 协调器是以 hermes 用户身份运行的（在 `02-reconcile-profiles` 脚本中使用了 `s6-setuidgid hermes` 命令）。如果某个配置文件目录最终由 root 用户拥有（例如因默认以 root 权限执行了 `docker exec <c> hermes profile create …` 命令），则协调器将无法读取 SOUL.md 文件，并引发 `PermissionError` 错误。解决方案：`stage2-hook.sh` 脚本会在**每次**系统启动时，以幂等方式将 `$HERMES_HOME/profiles` 目录的所有权移交给 hermes 用户。请勿删除该脚本中的相关代码。

### 通过 `docker exec` 创建的文件属于 root 所有

`docker exec` 命令默认以 root 权限执行。要么显式指定 `--user hermes` 参数，要么等待下一次启动时由 stage2 脚本处理权限变更。请勿手动以 root 权限在 `$HERMES_HOME/profiles/<name>/` 目录下创建文件——虽然下一次协调操作会处理这些文件，但正在进行的操作仍可能因权限问题而失败。

### 服务槽存在，但 s6-svstat 显示“s6-supervise 未运行”

服务目录存储在tmpfs上，因此在容器重启时会被清空。可能是cont-init协调器尚未运行（请在执行`docker restart`后稍等片刻），或者其运行失败了。可以查看`docker logs <c> | grep '02-reconcile'`来确认情况。

### 网关启动后立即退出（在svstat中显示为“down (exitcode 1)”）

很可能是该配置文件中没有设置模型或认证相关参数。服务槽位是正确的，问题出在网关本身未经过正确配置。请先运行`hermes -p <profile> setup`命令。s6监管进程会不断尝试重启它，这正是预期的行为——一旦配置问题得到解决，下一次重启就会成功并保持运行状态。

### 协调器跳过了某个配置文件

协调器以**是否存在`SOUL.md`文件**作为判断“真实配置文件”的依据。`hermes profile create`命令在创建配置时总会自动生成该文件。如果某个配置目录中不存在`SOUL.md`文件（可能是异常目录、恢复不完整或正在备份中），协调器会故意跳过该目录。如需重新处理该目录，可添加一个`SOUL.md`文件（即使内容为空也可）。

### “救命，容器以143号代码退出！”

请检查是否有程序调用了`s6-svscanctl -t`或 `/run/s6/basedir/bin/halt`命令——这两种命令都会触发/init进入第三阶段关闭流程，但会返回143（SIGTERM信号）而非预期的正常退出码。这是从架构版本A向版本B过渡时的现象。若希望容器以正常的退出码关闭，必须让CMD脚本（即main-wrapper.sh）正常执行结束；切勿试图通过结束脚本来强制控制退出。

## 相关技能

- `hermes-agent-dev`：用于浏览Hermes Agent的整个代码库。  
- `hermes-tool-quirks`：针对Hermes Tool的特定解决方案（如sed/grep等工具）——在调试s6堆栈与Hermes内置工具之间的交互时使用。
