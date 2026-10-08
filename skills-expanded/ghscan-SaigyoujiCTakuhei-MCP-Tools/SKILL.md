---
name: Netease Music
description: 网易云音乐控制模块，支持播放控制、音量调节、推荐漫游、歌单管理、搜索播放
---

# 网易云音乐操作手册

## 功能概览
网易云音乐模块通过全局快捷键（pyautogui）和 URL scheme（orpheus://）与 Windows 版网易云音乐客户端交互。

## 注册工具

### 配置工具 (2 个)

#### get_netease_config
- **描述**: 获取网易云音乐配置信息，验证路径是否有效
- **输入**: 无参数
- **输出**: `{success, config: {netease_music_path, path_status, chromedriver_path, chromedriver_status}, message}`
- **依赖**: 环境变量 `NETEASE_MUSIC_PATH` 和 `CHROMEDRIVER_PATH`

#### get_controller_info
- **描述**: 获取控制器信息和支持的功能列表
- **输入**: 无参数
- **输出**: `{success, data: {server_name, hotkey_available, supported_actions}, message}`

### 播放控制 (6 个)

#### launch_netease_music
- **描述**: 启动网易云音乐应用，支持自动最小化窗口
- **输入**: `{minimize_window: boolean}`
- **输出**: `{success, message, minimized}`

#### control_playback
- **描述**: 控制网易云音乐播放（通过全局快捷键）
- **输入**: `{action: "play_pause" | "previous" | "next"}`
- **输出**: `{success, message}` 或 `{success: false, error}`

#### control_volume
- **描述**: 控制网易云音乐音量（通过全局快捷键）
- **输入**: `{action: "volume_up" | "volume_down"}`
- **输出**: `{success, message}` 或 `{success: false, error}`

#### toggle_mini_mode
- **描述**: 切换网易云音乐迷你模式（通过全局快捷键）
- **输入**: 无参数
- **输出**: `{success, message}` 或 `{success: false, error}`

#### like_current_song
- **描述**: 喜欢当前播放的歌曲（通过全局快捷键）
- **输入**: 无参数
- **输出**: `{success, message}` 或 `{success: false, error}`

#### toggle_lyrics
- **描述**: 打开/关闭歌词显示（通过全局快捷键）
- **输入**: 无参数
- **输出**: `{success, message}` 或 `{success: false, error}`

### 推荐与漫游 (2 个)

#### play_daily_recommend
- **描述**: 播放网易云音乐每日推荐歌单（Selenium + ChromeDriver）
- **输入**: `{netease_path, chromedriver_path}`
- **输出**: `{success, message}` 或 `{success: false, error}`

#### play_roaming
- **描述**: 启动网易云音乐私人漫游功能（Selenium + ChromeDriver）
- **输入**: `{netease_path, chromedriver_path}`
- **输出**: `{success, message}` 或 `{success: false, error}`

### 歌单管理 (1 个)

#### manage_custom_playlists
- **描述**: 管理用户自定义歌单，支持 list/add/remove 操作
- **输入**: `{action: "list" | "add" | "remove", playlist_name, playlist_id, description}`
- **输出**: `{success, data/message, error}`
- **持久化**: playlists.json（项目根目录）

### 搜索播放 (2 个)

#### search_and_play_song
- **描述**: 搜索歌曲并直接播放
- **输入**: `{query, minimize_window}`
- **输出**: `{success, message, song, artist}` 或 `{success: false, error}`

#### search_and_play_playlist
- **描述**: 搜索歌单并直接播放
- **输入**: `{query, minimize_window}`
- **输出**: `{success, message, playlist}` 或 `{success: false, error}`

## 配置要求

### 环境变量
| 变量名 | 说明 | 必填 |
|--------|------|------|
| NETEASE_MUSIC_PATH | 网易云音乐客户端可执行文件路径 | 是（基础控制） |
| CHROMEDRIVER_PATH | ChromeDriver 路径 | 是（每日推荐/私人漫游） |

### 系统依赖
- **Python 包**: selenium, pyautogui, requests, psutil
- **Windows 特有**: pywin32（窗口控制）
- **外部依赖**: ChromeDriver（用于每日推荐/私人漫游）

## 快捷键映射

| 动作 | 快捷键 |
|------|--------|
| 播放/暂停 | Ctrl+Alt+P |
| 上一首 | Ctrl+Alt+Left |
| 下一首 | Ctrl+Alt+Right |
| 音量+ | Ctrl+Alt+Up |
| 音量- | Ctrl+Alt+Down |
| 迷你模式 | Ctrl+Alt+M |
| 喜欢歌曲 | Ctrl+Alt+L |
| 歌词显示 | Ctrl+Alt+D |

## URL Scheme

### 歌曲播放
```
orpheus://<base64>{"type":"song","id":"<song_id>","cmd":"play"}</base64>
```

### 歌单播放
```
orpheus://<base64>{"type":"playlist","id":"<playlist_id>","cmd":"play"}</base64>
```

## 错误处理

| 错误类型 | 返回格式 |
|----------|----------|
| pyautogui 未安装 | `{"success": false, "error": "pyautogui 未安装，无法使用快捷键控制"}` |
| Selenium 未安装 | `{"success": false, "error": "selenium 未安装"}` |
| 路径不存在 | `{"success": false, "error": "ChromeDriver 路径不存在"}` |
| 搜索无结果 | `{"success": false, "error": "未找到歌曲/歌单"}` |
| 网络异常 | `{"success": false, "error": "<具体错误信息>"}` |

## 注意事项

1. **全局快捷键依赖**: control_playback/control_volume/toggle_mini_mode/like_current_song/toggle_lyrics 需要 pyautogui 已安装且网易云音乐客户端已配置对应的全局快捷键
2. **Selenium 依赖**: play_daily_recommend/play_roaming 需要网易云音乐客户端已启动并启用远程调试（`--remote-debugging-port=9222`）
3. **URL Scheme**: search_and_play_song/search_and_play_playlist 通过 `orpheus://` URL scheme 直接触发网易云客户端播放
4. **歌单持久化**: playlists.json 存储于项目根目录，支持 list/add/remove 操作
5. **窗口控制**: launch_netease_music 的 minimize_window 功能依赖 pywin32，未安装时跳过最小化步骤
