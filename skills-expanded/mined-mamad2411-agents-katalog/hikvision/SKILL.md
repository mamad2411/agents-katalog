---
name: hikvision
description: '通过 ISAPI 协议控制局域网内的海康威视录像机（如 DS-7804N-Z1）。支持：设备信息查询、摄像头通道管理、录像查询、实时预览流地址获取、PTZ云台控制、抓图、报警事件查询。当用户需要查看监控、回放录像、控制云台摄像头或获取监控截图时使用。不用于：云端海康服务（萤石云）、远程公网访问（需要额外配置）。'
homepage: https://www.hikvision.com/cn/support/tools/
metadata:
  {
    "openclaw":
      {
        "emoji": "📹",
        "requires":
          {
            "bins": ["python3"],
            "env": ["HIKVISION_HOST", "HIKVISION_USER", "HIKVISION_PASSWORD"],
          },
      },
  }
---

# 海康录像机控制

通过 ISAPI 协议控制局域网内的海康威视录像机（NVR）或网络摄像头。

## 何时使用

✅ **在以下情况使用此技能：**

- "查看录像机的设备信息"
- "列出所有摄像头通道"
- "查询今天下午2点到3点的录像"
- "获取摄像头的实时预览地址"
- "把摄像头往左转一点"
- "抓取通道1的截图"
- "查看最近的报警事件"

❌ **在以下情况不要使用此技能：**

- 萤石云相关操作 → 使用萤石云 API
- 公网远程访问 → 需要配置端口转发或 VPN
- 多设备集中管理平台 → 使用 iVMS 或其他平台软件

## 安装依赖

首次使用前，需要安装 Python 依赖：

```bash
pip install -r {baseDir}/scripts/requirements.txt
```

或者直接安装：

```bash
pip install requests>=2.28.0
```

## 环境变量配置

在使用前，需要设置以下环境变量：

```bash
# 录像机 IP 地址
export HIKVISION_HOST=192.168.1.64

# 登录用户名
export HIKVISION_USER=admin

# 登录密码
export HIKVISION_PASSWORD=your_password
```

可以将这些添加到 `~/.zshrc` 或 `~/.bashrc` 中持久化。

## 命令

### 设备信息

```bash
# 查询录像机基本信息（型号、序列号、固件版本等）
python {baseDir}/scripts/hikvision.py device-info

# 指定其他设备
python {baseDir}/scripts/hikvision.py device-info --host 192.168.1.100
```

### 通道管理

```bash
# 列出所有摄像头通道
python {baseDir}/scripts/hikvision.py channels

# 以 JSON 格式输出
python {baseDir}/scripts/hikvision.py channels --format json
```

### 录像查询

```bash
# 查询指定通道的录像（时间范围）
python {baseDir}/scripts/hikvision.py records --channel 1 --start "2026-03-04 14:00:00" --end "2026-03-04 15:00:00"

# 查询今天的录像
python {baseDir}/scripts/hikvision.py records --channel 1 --start "2026-03-04 00:00:00" --end "2026-03-04 23:59:59"
```

### 实时预览

```bash
# 获取通道1的RTSP流地址
python {baseDir}/scripts/hikvision.py stream-url --channel 1

# 获取所有通道的流地址
python {baseDir}/scripts/hikvision.py stream-url --all
```

### PTZ 云台控制

```bash
# 方向控制
python {baseDir}/scripts/hikvision.py ptz --channel 1 --action up
python {baseDir}/scripts/hikvision.py ptz --channel 1 --action down
python {baseDir}/scripts/hikvision.py ptz --channel 1 --action left
python {baseDir}/scripts/hikvision.py ptz --channel 1 --action right

# 变焦控制
python {baseDir}/scripts/hikvision.py ptz --channel 1 --action zoom_in
python {baseDir}/scripts/hikvision.py ptz --channel 1 --action zoom_out

# 停止移动
python {baseDir}/scripts/hikvision.py ptz --channel 1 --action stop

# 指定移动速度（0-100，默认50）
python {baseDir}/scripts/hikvision.py ptz --channel 1 --action up --speed 30
```

### 抓图

```bash
# 抓取通道1的截图，保存到临时文件
python {baseDir}/scripts/hikvision.py snapshot --channel 1

# 指定输出文件
python {baseDir}/scripts/hikvision.py snapshot --channel 1 --output /tmp/camera1.jpg
```

### 报警事件

```bash
# 查询最近的报警事件
python {baseDir}/scripts/hikvision.py events --limit 10

# 指定通道
python {baseDir}/scripts/hikvision.py events --channel 1 --limit 20
```

## 输出格式

默认输出为易读的文本格式，可以通过 `--format json` 获取 JSON 输出：

```bash
python {baseDir}/scripts/hikvision.py device-info --format json
python {baseDir}/scripts/hikvision.py channels --format json
```

## 常见问题

### 连接失败

1. 确认录像机 IP 地址正确
2. 确认电脑和录像机在同一局域网
3. 确认录像机的 HTTP 端口（默认 80）可访问

### 认证失败

1. 确认用户名和密码正确
2. 某些固件版本可能需要使用 Digest 认证

### HTTPS 证书错误

海康设备通常使用自签名证书，脚本已禁用 SSL 验证。在生产环境中应考虑导入设备证书。

## 注意事项

- PTZ 控制需要摄像头支持云台功能
- 录像查询时间范围不宜过大，可能影响设备性能
- 频繁调用可能导致设备负载过高
- 密码存储在环境变量中，注意 shell 历史记录

## 参考资料

- `references/isapi-endpoints.md` — ISAPI 端点详细说明
