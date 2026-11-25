---
name: cn-futures-terminal
description: 部署、启动、检查和排障基于 TqSdk + TQSim 的本地中文期货终端。适用于用户想在 OpenClaw 里安装中国期货可视化 UI、启动本地行情/模拟网关、检查健康状态、打开浏览器查看期货界面、或排查期货终端启动失败等场景。
---

# cn-futures-terminal

这个技能用于把中文期货终端部署到本机，并通过本地浏览器使用。

## 适用场景

当用户提出以下任一目标时使用本技能：
- 安装中国期货终端
- 启动或重启本地期货 UI
- 检查 TQ Gateway / TQSim 是否正常
- 排查期货终端打不开、无数据、账号未配置
- 检查推荐交易合约是否已从临近交割月切换到更活跃后月
- 想让 OpenClaw 直接协助运行和维护本地期货面板

## 默认运行目录

- 运行时目录默认使用：`$HOME/.openclaw/workspace/cn-futures-terminal-runtime`
- 如用户指定其他目录，优先使用用户目录

## 先决条件

1. 机器可访问天勤接口
2. 已注册信易账户：`https://account.shinnytech.com/`
3. 已准备环境变量：
   - `TQ_USER`
   - `TQ_PASSWORD`
   - 可选：`TQ_SYMBOLS`
   - 可选：`TQ_PORT`
4. 建议使用 `Python 3.12`
5. 如果用户要做量化研究，默认应包含同品种条带多个月份，例如：
   - `CZCE.PK604,CZCE.PK605,CZCE.PK610`

## 工作流

### 1. 首次部署

先执行：

```bash
bash scripts/bootstrap.sh
```

如果用户指定目录：

```bash
bash scripts/bootstrap.sh /custom/runtime/dir
```

作用：
- 把 `assets/tq_gateway/` 复制到运行时目录
- 创建 `.venv`
- 安装依赖
- 输出下一步命令

### 2. 启动网关和 UI

```bash
TQ_USER='xxx' TQ_PASSWORD='xxx' bash scripts/start_gateway.sh
```

可选：

```bash
TQ_USER='xxx' TQ_PASSWORD='xxx' TQ_SYMBOLS='SHFE.rb2605,DCE.i2605,CZCE.PK604,CZCE.PK605,CZCE.PK610' TQ_PORT=8787 bash scripts/start_gateway.sh
```

启动成功后，UI 地址通常是：
- `http://127.0.0.1:8787/`

### 3. 健康检查

```bash
bash scripts/status.sh
```

检查项：
- 端口是否监听
- `/health` 是否返回 `status=ok`
- 当前监听端口是多少
- `/contract_selector/CZCE.PK` 是否能返回推荐交易合约

### 4. 停止

```bash
bash scripts/stop_gateway.sh
```

## 排障规则

- 如果用户没有提供 `TQ_USER` / `TQ_PASSWORD`，不要伪造启动成功，直接说明缺少账号配置。
- 如果 `Python 3.12` 不存在，先尝试 `uv`，再退回 `python3`，但要明确提醒兼容性风险。
- 如果 `/health` 不通，先检查端口监听，再看进程是否退出。
- 如果用户反馈“15:00 后没有新数据”，优先判断是否是合约停盘，不要先判断为 UI 故障。
- 如果用户直接把前月当主力合约，不要机械接受；应优先检查 `/contract_selector/<交易所.品种>` 的 `tradable_leader`。该选择器对所有期货品种都有通用默认规则，并对部分品类使用覆盖阈值。
- 如果当前月已接近交割月或体量明显衰减，应明确提示用户系统推荐的后月合约。

## 交付标准

完成后至少要能给出这些事实：
- 运行时目录
- 启动命令
- 健康检查结果
- UI 地址
- 当前是否为模拟盘
- 当前品种的推荐交易合约（如用户涉及量化/研究）

## 脚本

- `scripts/bootstrap.sh`
- `scripts/start_gateway.sh`
- `scripts/status.sh`
- `scripts/stop_gateway.sh`

除非用户要求修改代码，否则优先使用这些脚本，不要重写一套部署流程。
