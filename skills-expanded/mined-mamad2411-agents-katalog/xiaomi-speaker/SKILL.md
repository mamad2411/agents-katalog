---
name: xiaomi-speaker
description: 控制小米/米家智能音箱，支持播放/暂停、音量调节、切歌、TTS语音播报等功能。当用户需要控制小爱音箱、设置定时提醒、语音播报消息时使用此技能。支持设备名智能匹配（如"小爱"、"客厅音箱"），无需记忆复杂的设备ID。
---

# 小爱音箱控制器 🎵

> 优雅地控制你的小米智能音箱

## 功能特性

- 🎯 **智能设备名匹配** - 说"小爱"即可，自动识别音箱
- 🔊 **完整媒体控制** - 播放/暂停/切歌/音量调节
- 🗣️ **TTS 语音播报** - 让音箱说话，适合提醒和通知
- ⏰ **定时任务支持** - 自动提醒，无需人工值守
- 💾 **本地缓存** - 设备信息持久化，响应更快

## 设备要求

- 小米/米家智能音箱（如小爱音箱Pro）
- 设备需绑定到小米账号并联网

## 快速开始

### 1. 安装依赖

```bash
pip3 install mijiaAPI
```

### 2. 首次登录

```bash
python3 -m mijiaAPI --list_homes
```

扫描显示的二维码，用米家 APP 完成登录。

### 3. 查看设备

```bash
python3 scripts/xiaomi-speaker.py list
```

输出示例：
```
🎵 找到 1 个音箱设备:

  1. 小爱音箱Pro (xiaomi.wifispeaker.lx06)
     DID: 936030139...
```

---

## 命令参考

### 基础控制

```bash
# 播放/暂停
python3 scripts/xiaomi-speaker.py play 小爱
python3 scripts/xiaomi-speaker.py pause 小爱

# 切歌
python3 scripts/xiaomi-speaker.py next 小爱
python3 scripts/xiaomi-speaker.py prev 小爱

# 音量调节 (0-100)
python3 scripts/xiaomi-speaker.py volume 小爱 50

# 查看状态
python3 scripts/xiaomi-speaker.py status 小爱
```

### TTS 语音播报

```bash
python3 scripts/xiaomi-speaker.py say 小爱 "该起床啦"
python3 scripts/xiaomi-speaker.py say 小爱 "晚上八点开家庭会议"
```

### 刷新设备列表

当新增设备或修改设备名称后：

```bash
python3 scripts/xiaomi-speaker.py refresh
```

---

## 定时提醒（Cron 任务）

### 添加定时提醒

```bash
# 一次性提醒
openclaw cron add --at "2026-02-21T11:30:00+08:00" \
  --message "让小爱音箱播报：中午啦，全家人一起去吃涮羊肉吧！"

# 每日重复提醒
openclaw cron add --cron "30 21 * * *" \
  --message "让小爱音箱播报：九点半啦，哥哥和弟弟都要去刷牙睡觉啦！"
```

### 常用时间格式

| 需求 | Cron 表达式 |
|------|------------|
| 每天早上 8:30 | `30 8 * * *` |
| 每天下午 2:30 | `30 14 * * *` |
| 每天晚上 9:30 | `30 21 * * *` |
| 工作日早上 7:00 | `0 7 * * 1-5` |

---

## 自然语言使用

在 OpenClaw 中直接描述你的需求：

- *"把客厅音箱音量调到 50"*
- *"小爱播放音乐"*
- *"让小爱播报北京天气"*
- *"设置明天早上 8 点提醒哥哥上作文课"*

---

## 故障排除

### 登录失效

```bash
rm ~/.config/mijia-api/auth.json
python3 -m mijiaAPI --list_homes  # 重新登录
```

### 找不到设备

1. 确认设备在米家 APP 中在线
2. 运行 `python3 scripts/xiaomi-speaker.py refresh` 刷新列表
3. 检查设备名称是否包含 "音箱"、"小爱" 等关键词

### TTS 播报失败

部分音箱型号可能不支持 `play-text` 动作，可通过以下命令检查：

```bash
python3 -m mijiaAPI --get_device_info xiaomi.wifispeaker.lx06
```

查看 `actions` 列表中是否包含 `play-text`。

---

## 技术说明

- 基于 [mijiaAPI](https://github.com/Do1e/mijia-api) 调用小米云端 API
- 设备信息缓存在 `~/.config/xiaomi-speaker/devices.json`
- 登录状态保存在 `~/.config/mijia-api/auth.json`
- TTS 功能通过 `play-text` action（siid=5, aiid=1）实现

---

## 更新日志

### v1.0 (2026-02-21)

- ✅ 设备发现和智能名称匹配
- ✅ 播放/暂停/切歌/音量控制
- ✅ TTS 语音播报
- ✅ 本地设备缓存
- ✅ 定时提醒集成

---

## 路线图

- [ ] 支持更多音箱型号
- [ ] 音乐播放列表控制
- [ ] 智能家居场景联动
- [ ] 语音唤醒词设置

---

*优雅的不是技术，是体验。* 🦐
