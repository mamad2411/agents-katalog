---
name: macos-photos
description: Photos.app integration on macOS for AI agents via AppleScript/JXA
---

# macOS Photos Skill

Control and query Apple Photos.app on macOS using AppleScript (osascript) commands.

## Overview

Photos.app exposes an AppleScript dictionary that lets you read albums, media items, metadata, and perform limited write operations like creating albums and managing favorites. All commands use `osascript` from the terminal.

## Core Concepts

- **Media item** — a photo or video in the library
- **Album** — a user-created collection of media items
- **Folder** — a container that holds albums or other folders
- **Container** — generic term for album or folder
- **Keyword** — a tag attached to a media item

## Listing Albums

```bash
# List all album names
osascript -e 'tell application "Photos" to get name of every album'

# List albums with their item counts
osascript -e 'tell application "Photos"
  set albumList to every album
  set output to ""
  repeat with a in albumList
    set output to output & name of a & " (" & (count of media items of a) & ")" & linefeed
  end repeat
  return output
end tell'
```

## Listing Folders

```bash
# List all folder names
osascript -e 'tell application "Photos" to get name of every folder'
```

## Listing Media Items

```bash
# Count all media items in the library
osascript -e 'tell application "Photos" to count of every media item'

# List first 10 media item filenames
osascript -e 'tell application "Photos" to get filename of media items 1 thru 10'

# List media items in a specific album
osascript -e 'tell application "Photos" to get filename of every media item of album "Vacation"'
```

## Searching Photos

### By name/filename

```bash
osascript -e 'tell application "Photos"
  set results to every media item whose filename contains "IMG_2024"
  get filename of results
end tell'
```

### By date

```bash
# Photos taken on a specific date
osascript -e 'tell application "Photos"
  set targetDate to date "January 1, 2025"
  set nextDay to targetDate + (1 * days)
  set results to every media item whose date is greater than or equal to targetDate and date is less than nextDay
  get filename of results
end tell'
```

### By keyword

```bash
osascript -e 'tell application "Photos"
  set results to every media item whose keywords contains "travel"
  get filename of results
end tell'
```

### By favorite status

```bash
osascript -e 'tell application "Photos"
  set results to every media item whose favorite is true
  get filename of results
end tell'
```

## Getting Photo Metadata

```bash
# Full metadata for a single media item
osascript -e 'tell application "Photos"
  set img to media item 1
  set output to ""
  set output to output & "id: " & (id of img) & linefeed
  set output to output & "name: " & (name of img) & linefeed
  set output to output & "filename: " & (filename of img) & linefeed
  set output to output & "date: " & (date of img as string) & linefeed
  set output to output & "description: " & (description of img) & linefeed
  set output to output & "keywords: " & (keywords of img as string) & linefeed
  set output to output & "favorite: " & (favorite of img as string) & linefeed
  set output to output & "width: " & (width of img) & linefeed
  set output to output & "height: " & (height of img) & linefeed
  set output to output & "altitude: " & (altitude of img) & linefeed
  set output to output & "location: " & (location of img as string) & linefeed
  return output
end tell'
```

### Available metadata properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique persistent identifier |
| `name` | string | Display name of the media item |
| `filename` | string | Original filename on disk |
| `date` | date | Date the photo was taken |
| `description` | string | User-added description/caption |
| `keywords` | list of strings | Tags/keywords attached to the item |
| `favorite` | boolean | Whether the item is favorited |
| `width` | integer | Width in pixels |
| `height` | integer | Height in pixels |
| `altitude` | real | GPS altitude |
| `location` | list of reals | GPS coordinates {latitude, longitude} |

## Creating and Managing Albums

### Create an album

```bash
osascript -e 'tell application "Photos" to make new album named "My New Album"'
```

### Delete an album

```bash
osascript -e 'tell application "Photos" to delete album "My New Album"'
```

## Adding and Removing Photos from Albums

### Add photos to an album

```bash
# Add specific media items to an album by ID
osascript -e 'tell application "Photos"
  set targetAlbum to album "Vacation"
  set items to {media item id "ABC123", media item id "DEF456"}
  add items to targetAlbum
end tell'
```

### Remove photos from an album

Removing items from an album is not directly supported via AppleScript. Photos does not expose a `remove` command for media items in albums.

## Exporting Photos

```bash
# Export photos from an album to a folder
osascript -e 'tell application "Photos"
  set targetAlbum to album "Vacation"
  set items to every media item of targetAlbum
  set exportPath to POSIX file "/Users/Dmytro/Desktop/export" as alias
  export items to exportPath
end tell'

# Export with original quality (unmodified originals)
osascript -e 'tell application "Photos"
  set items to every media item of album "Vacation"
  set exportPath to POSIX file "/Users/Dmytro/Desktop/export" as alias
  export items to exportPath with using originals
end tell'
```

**Note**: The export destination folder must exist before running the command.

## Importing Photos

```bash
# Import files into the library
osascript -e 'tell application "Photos"
  import POSIX file "/Users/Dmytro/Desktop/photo.jpg"
end tell'

# Import into a specific album
osascript -e 'tell application "Photos"
  set targetAlbum to album "Imports"
  import POSIX file "/Users/Dmytro/Desktop/photo.jpg" into targetAlbum
end tell'

# Import multiple files
osascript -e 'tell application "Photos"
  set files to {POSIX file "/Users/Dmytro/Desktop/a.jpg", POSIX file "/Users/Dmytro/Desktop/b.jpg"}
  import files
end tell'
```

## Favoriting / Unfavoriting

```bash
# Favorite a photo
osascript -e 'tell application "Photos"
  set favorite of media item id "ABC123" to true
end tell'

# Unfavorite a photo
osascript -e 'tell application "Photos"
  set favorite of media item id "ABC123" to false
end tell'
```

## Other Useful Commands

```bash
# Open Photos.app
osascript -e 'tell application "Photos" to activate'

# Get the selection in the Photos UI (requires Photos to be open)
osascript -e 'tell application "Photos" to get selection'

# Spotlight search for photos (alternative to AppleScript)
mdfind "kMDItemContentType == 'public.image'" -onlyin ~/Pictures
```

## Limitations

- **Read-heavy API**: Photos AppleScript is much stronger at reading than writing. Many write operations (editing, moving between albums, deleting media items, setting metadata beyond favorites) are not supported or require workarounds.
- **No direct remove from album**: You cannot remove a media item from an album via AppleScript.
- **No metadata editing** (beyond favorites): You cannot set keywords, description, name, or date via AppleScript.
- **Performance on large libraries**: Queries over the entire library can be slow. Filter early and limit result sets where possible.
- **Photos must be running**: Most commands require Photos.app to be running. AppleScript will launch it if needed, but this adds delay.
- **No smart album access**: Smart albums are not exposed via AppleScript.
- **Export creates copies**: Exported files are copies; there is no way to get the original file path in the library.

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| "Photos got an error: Can't get album" | Album name does not exist or is misspelled | List all albums first to verify the exact name |
| Script hangs or is very slow | Querying too many media items at once | Limit with `media items 1 thru N` or filter by album |
| "Not authorized to send Apple events" | macOS privacy permissions not granted | Go to System Settings > Privacy & Security > Automation and enable Terminal/osascript for Photos |
| Export fails with "file not found" | Export destination folder does not exist | Create the folder first with `mkdir -p` |
| "Photos is not running" | Photos.app needs to be open | Add `tell application "Photos" to activate` before your command |
| Keywords search returns nothing | Keywords are case-sensitive in some contexts | Try different casing or list keywords first to verify values |
| Location returns `{missing value, missing value}` | Photo has no GPS data embedded | Check original photo EXIF data |
