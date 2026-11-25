---
name: apple-music-control
description: 通过 Apple Music 控制 macOS Apple Music 的完整方案。包括 applemusic-cli (推荐) 和 osascript 备选。
---

# Apple Music 控制指南

## applemusic-cli（推荐）

安装于 `/Users/minimx/applemusic-cli/`，通过 `am` 命令调用（`~/.local/bin/am`，基于 Bun/TypeScript 的 osascript 封装）。

### 常用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `am play` / `am pause` / `am stop` | 播放/暂停/停止 | `am play` |
| `am toggle` | 切换播放/暂停 | `am toggle` |
| `am next` / `am prev` | 切歌 | `am next` |
| `am now` | 当前播放信息 | `am now` |
| `am vol <0-100>` | 音量 | `am vol 50` |
| `am shuffle on/off` | 随机播放 | `am shuffle on` |
| `am repeat off/one/all` | 重复模式 | `am repeat all` |
| `am song "<name>"` | 搜索并播放歌曲 | `am song "最后派对"` |
| `am playlist "<name>"` | 播放列表 | `am playlist "MinimX"` |
| `am playlists` | 列出播放列表 | `am playlists` |
| `am tracks "<playlist>"` | 列出播放列表曲目 | `am tracks "MinimX" --limit 5` |
| `am songs` | 资料库所有歌曲 | `am songs --limit 10` |
| `am search "<query>"` | 搜索资料库 | `am search "陈奕迅"` |

支持 `--limit N --offset N` 分页。

### 用户偏好的播放模式（MinimX 歌单）

当前最稳定的方法——分两步走：

```bash
am song "最后派对 陈奕迅"
sleep 0.3
am playlist "MinimX"
sleep 0.3
am shuffle on
```

说明：`am song` 先独立播指定歌曲。`am playlist` + `am shuffle` 接管为 MinimX 随机播放队列。队列会被替换，这是 Apple Music API 的限制。

### 播放队列注意事项

**Apple Music AppleScript 不支持把整个 playlist 加入"待播"队列**。`play <playlist>` 和 `play <track>` 都会替换当前播放上下文。

### 已知方案

建立 playlist 上下文后跳到指定曲目：

```applescript
tell application "Music"
    set thePlaylist to playlist "MyPlaylist"
    set shuffle enabled to false
    play thePlaylist
    delay 2
    -- 尝试定位到目标曲目（仅对本地/已下载曲目有效）
    set targetTrack to first track of thePlaylist whose name contains "Song A"
    set current track to targetTrack
    play
    delay 1
    set shuffle mode to songs
    set shuffle enabled to true
end tell
```

**限制**：`set current track` 对 Apple Music 流媒体云曲目（非本地下载）无效，会报错 `-10006`。只对已下载到本地的歌曲有效。

---

## 基础播放控制（osascript 备选）

如果 `am` 不可用，回退到 osascript：

```applescript
tell application "Music" to play
tell application "Music" to pause
tell application "Music" to stop
tell application "Music" to playpause
tell application "Music" to next track
tell application "Music" to previous track
tell application "Music" to set player position to 60    -- 跳到 60 秒
```

### 音量
```applescript
tell application "Music" to set sound volume to 50
tell application "Music" to get sound volume
```

### Shuffle / Repeat
```applescript
tell application "Music" to set shuffle mode to songs    -- 开启
tell application "Music" to set shuffle enabled to false -- 关闭
tell application "Music" to set song repeat to off/one/all
```

获取状态：
```applescript
tell application "Music"
    set sm to shuffle mode
    set se to shuffle enabled
    set sr to song repeat
    return sm & ", " & se & ", " & sr
end tell
```

---

## 搜索曲目

```applescript
tell application "Music"
    set results to (search library playlist 1 for "周杰伦")
    if (count of results) > 0 then
        set t to item 1 of results
        play t
    end if
end tell
```

**注意**：`search` 只支持 `library playlist 1`（资料库主列表）。不能直接在用户自定义播放列表上 search。

---

## 播放列表管理

### 列出所有播放列表
```applescript
tell application "Music" to set plist to name of every user playlist
```

### 播整个播放列表
```applescript
tell application "Music"
    repeat with p in user playlists
        if name of p is "MinimX" then play p
    end repeat
end tell
```

### 获取播放列表中的曲目
```applescript
tell application "Music"
    repeat with p in user playlists
        if name of p is "MinimX" then
            set t to track 1 of p
            return name of t & " - " & artist of t
        end if
    end repeat
end tell
```

### 创建/删除播放列表
```applescript
-- 创建
tell application "Music"
    set newPl to make new playlist with properties {name:"新播放列表"}
    set results to (search library playlist 1 for "陈奕迅")
    if (count of results) > 0 then
        duplicate item 1 of results to newPl
    end if
end tell

-- 删除
tell application "Music"
    repeat with p in user playlists
        if name of p is "新播放列表" then delete p
    end repeat
end tell
```

### 资料库信息
```applescript
tell application "Music"
    return (count of tracks of library playlist 1) & " tracks, " & (count of user playlists) & " playlists"
end tell
```

---

## 曲目信息

```applescript
tell application "Music"
    set t to current track
    set info to "Name: " & name of t & linefeed
    set info to info & "Artist: " & artist of t & linefeed
    set info to info & "Album: " & album of t & linefeed
    set info to info & "Duration: " & duration of t
    return info
end tell
```

---

## 已知限制

1. **Apple Music 目录搜索** — AppleScript 不支持搜索 Apple Music 在线曲库。只能搜索已添加到资料库的曲目。
2. **`play <track>` 和 `play <playlist>` 都会替换当前队列** — AppleScript 没有"加入待播"API。播 playlist 会替换整个 Up Next。
3. **`play <track>` 后会重置 shuffle 为 off** — 必须单独再设 `am shuffle on` 或 `set shuffle enabled to true`。
4. **`set shuffle mode to off` 无效** — 只能用 `set shuffle enabled to false`。
5. **`search` 不支持用户播放列表** — 只能 `search library playlist 1`。
6. **云端/下载状态** — `cloud status` 属性可能因曲目类型而报类型错误。

---

## 调用方式（Hermes 环境）

优先用 `am` CLI（`terminal("am now")`），如果命令不满足需求再回退到 osascript。复杂多行 AppleScript 先用 `write_file` 写到 `/tmp/*.applescript` 再 `osascript /tmp/*.applescript`。
