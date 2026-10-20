# TeamSpeak Prometheus Exporter 架构指南

## 项目概述
一个基于 Python 的 TeamSpeak 3 服务器监控导出器，采用标准 `src` 布局。

## 目录结构
```
/opt/teamspeak-prometheus/
├── src/
│   └── ts3_exporter/        # 核心包
│       ├── __init__.py     # 包导出接口
│       ├── main.py         # 入口点，包含 TeamSpeakExporter 类
│       ├── config.py       # 配置加载逻辑
│       └── metrics.py      # Prometheus 指标定义
├── tests/                  # 测试目录
├── Dockerfile              # 容器化定义
├── pyproject.toml          # 项目元数据与依赖 (uv)
└── config.yaml.example     # 配置示例
```

## 核心组件
- **`ts3_exporter.main`**: 核心运行循环。使用 `ThreadPoolExecutor` 并行抓取多个 TS3 服务器。
- **`ts3_exporter.config`**: 处理 `config.yaml` 和环境变量。
- **`ts3_exporter.metrics`**: 统一管理所有 Prometheus Gauges。

## 开发规范
- **包管理**: 使用 `uv`。
- **导入**: 内部使用相对导入（如 `from . import metrics`）。
- **执行**: 
  - 本地开发：`export PYTHONPATH=$PYTHONPATH:$(pwd)/src && python -m ts3_exporter.main`
  - 安装后：`ts3-exporter`
- **测试**: 使用 `unittest`。运行命令：`export PYTHONPATH=$PYTHONPATH:$(pwd)/src && python -m unittest discover tests`

## 变更记录
- **2026-02-14**: 迁移到 `src` 布局，重构入口点为类结构，并更新了测试 mock 逻辑。
