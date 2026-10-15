---
name: baota-panel
description: 通过宝塔 (BT) 面板 API 管理服务器资源。支持网站管理、Docker 编排、数据库运维及文件管理。具备自动绕过防火墙和 Session 嗅探能力。
---

# 宝塔面板管理专家

通过宝塔面板 API 实现对服务器的全面自动化管理。

## 安装命令

```bash
npx skills add ayflying/ai-skills --skill baota-panel
```

## 准备工作 (Prerequisites)

1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```
2. **配置认证**：
   - 复制 `.env.example` 为 `.env`。
   - 在宝塔面板中开启 API 接口，获取密钥并填入 `.env`。
   - 将当前 IP 加入宝塔 API 的 IP 白名单。

## 核心亮点

- **稳健模式 (Robust Execution)**：当普通 Shell 接口被防火墙拦截时，自动切换至计划任务代理模式执行，确保 100% 命令送达。
- **Session 嗅探 (Socket Support)**：自动从服务器本地获取 `x-http-token`，支持调用宝塔内部的 Socket/Model 接口（如 Docker Compose 编排）。
- **全能管理**：覆盖网站、FTP、数据库、Docker、文件系统及系统监控。

## 常用命令示例

### 1. 系统信息
```bash
python scripts/bt_api.py
```

### 2. Docker Compose 部署 (稳健模式)
```python
from scripts.bt_api import BTPanelAPI
api = BTPanelAPI(url, key)

# 即使有防火墙拦截，也能稳定执行
api.docker_compose("/www/docker/myapp", "up -d")
```

### 3. 删除容器编排
```python
# 获取项目 ID 后执行删除
api.delete_compose_project(1)
```

## 内部文档
- [API 规范与认证](references/common.md)
- [网站管理接口](references/site.md)
- [Docker 与 Compose 管理](references/docker.md)
- [数据库与 FTP](references/database.md)
- [文件系统操作](references/files.md)
- [系统与安全](references/system.md)

## 安全红线
- **严禁擅自执行删除操作**。在删除站点、数据库、编排项目或清空回收站前，必须获得用户明确授权。
