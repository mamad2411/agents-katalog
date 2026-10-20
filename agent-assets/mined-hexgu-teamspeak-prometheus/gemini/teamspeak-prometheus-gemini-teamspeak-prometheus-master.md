# TeamSpeak Prometheus Exporter

本项目是一个用于监控 TeamSpeak 3 服务器的 Prometheus 导出器。它通过 TS3 Server Query 接口获取服务器状态和玩家在线信息，并以 Prometheus 格式暴露指标。

## 核心架构

- **`app.py`**: 项目入口。负责启动 Prometheus HTTP 服务，并根据配置的间隔（`read_interval`）多线程收集各 TS3 服务器的数据。
- **`metrics.py`**: 定义了所有导出的 Prometheus 指标。
    - `teamspeak_*`: 包含服务器带宽、丢包、在线人数等指标。
    - `teamspeak_player_online`: 详细记录每个在线玩家的属性（如 ID、昵称、IP、国家等）。
- **`config.py`**: 配置加载逻辑。支持从 `config.yaml` 映射或通过 `TEAMSPEAK_*` 环境变量进行单服务器快速配置。
- **`python-ts3`**: 核心依赖库，通过 git 直接引入（见 `pyproject.toml`）。

## 运行与开发

### 环境准备
项目使用 `uv` 进行包管理。本地开发建议安装 `uv`：
```bash
# 安装依赖
uv sync
```

### 运行 (推荐)
默认推荐使用 Docker Compose 运行，它会自动处理依赖并启动服务：
```bash
# 复制配置文件
cp config.yaml.example config.yaml

# 启动服务
docker compose up -d
```

### 本地开发运行
若需在本地直接运行：
```bash
# 设置 PYTHONPATH 并运行
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
uv run python -m ts3_exporter.main
```

### 测试
项目包含基于 `unittest` 的模拟测试，验证指标收集逻辑。
```bash
# 运行测试
uv run python -m unittest discover tests
```

## 配置说明 (`config.yaml`)

- `servers`: 服务器列表，每个服务器包含 `name`, `host`, `port`, `username`, `password`。
- `metrics_port`: 导出器监听端口（默认 8000）。
- `read_interval`: 抓取频率（单位：秒）。

## 开发规范
- **异步处理**: 采用 `ThreadPoolExecutor` 并行处理多个服务器的抓取，避免阻塞。
- **指标命名**: 统一使用 `teamspeak_` 前缀。
- **错误处理**: TS3 连接失败或抓取异常会被记录到日志，不会中断主循环。
- **依赖管理**: 新增依赖应通过 `uv add` 添加，并同步更新 `uv.lock`。
