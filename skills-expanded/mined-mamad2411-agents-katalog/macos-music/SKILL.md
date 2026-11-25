---
name: macos-music
description: Control Apple Music.app on macOS. Use for playback, library search, playlist management, volume, shuffle/repeat, and AirPlay output. Triggers on queries about playing music, songs, albums, artists, playlists, or controlling audio playback.
---

# macOS Music Integration

Control Music.app on macOS using AppleScript via `osascript`.

## Prerequisites

- macOS with Music.app (Catalina 10.15+)
- Automation permission granted to your terminal (System Settings > Privacy & Security > Automation)

## Playback Controls

### Play / Pause / Stop

```bash
# Play (resume)
osascript -e 'tell application "Music" to play'

# Pause
osascript -e 'tell application "Music" to pause'

# Toggle play/pause
osascript -e 'tell application "Music" to playpause'

# Stop
osascript -e 'tell application "Music" to stop'
```

### Next / Previous Track

```bash
# Next track
osascript -e 'tell application "Music" to next track'

# Previous track
osascript -e 'tell application "Music" to previous track'
```

### Play a Specific Track

```bash
# Play a track by name
osascript -e 'tell application "Music" to play (first track of playlist "Library" whose name is "Bohemian Rhapsody")'
```

## Current Track Info

### Get Now Playing

```bash
# Track name
osascript -e 'tell application "Music" to get name of current track'

# Artist
osascript -e 'tell application "Music" to get artist of current track'

# Album
osascript -e 'tell application "Music" to get album of current track'

# Duration (seconds)
osascript -e 'tell application "Music" to get duration of current track'

# Current position (seconds)
osascript -e 'tell application "Music" to get player position'

# Player state (playing, paused, stopped)
osascript -e 'tell application "Music" to get player state'
```

### Get All Track Info at Once

```bash
osascript -e '
tell application "Music"
    set t to current track
    set output to "Name: " & (name of t) & linefeed
    set output to output & "Artist: " & (artist of t) & linefeed
    set output to output & "Album: " & (album of t) & linefeed
    set output to output & "Duration: " & (duration of t) & "s" & linefeed
    set output to output & "Position: " & (player position) & "s"
    return output
end tell'
```

## Searching the Library

### Search by Name, Artist, or Album

```bash
# Search tracks by name
osascript -e '
tell application "Music"
    set results to (every track of playlist "Library" whose name contains "Yesterday")
    set output to ""
    repeat with t in results
        set output to output & (name of t) & " - " & (artist of t) & linefeed
    end repeat
    return output
end tell'

# Search tracks by artist
osascript -e '
tell application "Music"
    set results to (every track of playlist "Library" whose artist contains "Beatles")
    set output to ""
    repeat with t in results
        set output to output & (name of t) & " — " & (album of t) & linefeed
    end repeat
    return output
end tell'

# Search tracks by album
osascript -e '
tell application "Music"
    set results to (every track of playlist "Library" whose album contains "Abbey Road")
    set output to ""
    repeat with t in results
        set output to output & (name of t) & " - " & (artist of t) & linefeed
    end repeat
    return output
end tell'
```

## Playlist Management

### List All Playlists

```bash
osascript -e '
tell application "Music"
    set output to ""
    repeat with p in (every user playlist)
        set output to output & (name of p) & linefeed
    end repeat
    return output
end tell'
```

### Create a New Playlist

```bash
osascript -e 'tell application "Music" to make new playlist with properties {name:"My New Playlist"}'
```

### Add a Track to a Playlist

```bash
osascript -e '
tell application "Music"
    set t to (first track of playlist "Library" whose name is "Bohemian Rhapsody")
    duplicate t to playlist "My New Playlist"
end tell'
```

### Play a Playlist

```bash
osascript -e 'tell application "Music" to play playlist "My New Playlist"'
```

### Get Tracks in a Playlist

```bash
osascript -e '
tell application "Music"
    set output to ""
    repeat with t in (every track of playlist "My New Playlist")
        set output to output & (name of t) & " - " & (artist of t) & linefeed
    end repeat
    return output
end tell'
```

## Volume Control

```bash
# Get current volume (0-100)
osascript -e 'tell application "Music" to get sound volume'

# Set volume to 50
osascript -e 'tell application "Music" to set sound volume to 50'

# Mute (set to 0)
osascript -e 'tell application "Music" to set sound volume to 0'

# Max volume
osascript -e 'tell application "Music" to set sound volume to 100'
```

## Shuffle and Repeat

```bash
# Get shuffle state
osascript -e 'tell application "Music" to get shuffle enabled'

# Enable shuffle
osascript -e 'tell application "Music" to set shuffle enabled to true'

# Disable shuffle
osascript -e 'tell application "Music" to set shuffle enabled to false'

# Get repeat mode (off, one, all)
osascript -e 'tell application "Music" to get song repeat'

# Set repeat to all
osascript -e 'tell application "Music" to set song repeat to all'

# Set repeat to one
osascript -e 'tell application "Music" to set song repeat to one'

# Disable repeat
osascript -e 'tell application "Music" to set song repeat to off'
```

## AirPlay Output

### List AirPlay Devices

```bash
osascript -e '
tell application "Music"
    set output to ""
    repeat with d in (every AirPlay device)
        set output to output & (name of d) & " — active: " & (selected of d) & linefeed
    end repeat
    return output
end tell'
```

### Select an AirPlay Device

```bash
# Enable an AirPlay device
osascript -e '
tell application "Music"
    set targetDevice to (first AirPlay device whose name is "Living Room")
    set selected of targetDevice to true
end tell'

# Disable an AirPlay device
osascript -e '
tell application "Music"
    set targetDevice to (first AirPlay device whose name is "Living Room")
    set selected of targetDevice to false
end tell'
```

## Seek / Set Position

```bash
# Jump to 30 seconds into the current track
osascript -e 'tell application "Music" to set player position to 30'

# Fast-forward 10 seconds
osascript -e '
tell application "Music"
    set player position to (player position + 10)
end tell'
```

## Common Use Cases

### Play an Artist

```bash
osascript -e '
tell application "Music"
    play (first track of playlist "Library" whose artist is "Queen")
end tell'
```

### Show What Is Playing

```bash
osascript -e '
tell application "Music"
    if player state is playing then
        return (name of current track) & " by " & (artist of current track)
    else
        return "Nothing is playing"
    end if
end tell'
```

### Create a Playlist from Search Results

```bash
osascript -e '
tell application "Music"
    set newPL to (make new playlist with properties {name:"Jazz Picks"})
    set jazzTracks to (every track of playlist "Library" whose genre contains "Jazz")
    repeat with t in jazzTracks
        duplicate t to newPL
    end repeat
    return "Added " & (count of jazzTracks) & " tracks to Jazz Picks"
end tell'
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Not authorized to send Apple events" | Grant Automation permission to terminal |
| No tracks found | Ensure your library is synced / not empty |
| AirPlay device not listed | Check device is on the same network and available |
| Player state returns "stopped" unexpectedly | Open Music.app manually first, then retry |
| Commands hang or timeout | Music.app may be unresponsive; restart it |

## Technical Notes

- All commands use AppleScript via `osascript` (no private APIs).
- Music.app is the successor to iTunes on macOS Catalina and later.
- Apple Music subscription is not required for local library playback.
- AppleScript `tell application "Music"` launches the app if it is not running.
