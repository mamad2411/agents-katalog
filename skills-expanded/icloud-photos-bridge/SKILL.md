---
name: icloud-photos-bridge
description: "Read the Mac's iCloud Photos library from an agent. Catalog photos/videos with Apple's own quality scores, faces, labels and places, identify who is who by face cluster, build contact sheets, and download full-quality originals from iCloud. Use whenever a task needs the user's own photos or videos (selfie picking, b-roll, post images). Read-only; never edits or deletes the library."
---

# iCloud Photos bridge

The bridge is the local Photos database on the Mac, read through `osxphotos`. iCloud Photos syncs into it, so
everything in iCloud is visible here, including Apple's per-photo aesthetic scores, face clusters and scene labels.
Originals that only live in iCloud ("Optimize Mac Storage") are downloaded on demand through PhotoKit.

Other skills build on this one: `selfie-picker`, `broll-picker`.

## Rules

- Read-only. Never modify, delete, favorite or move anything in Photos.
- Photos stay on this Mac. Don't upload them anywhere unless the user asks for that exact destination.
- Never show or use other people's photos as the subject without asking. Identify people by face cluster
  (`owner.py`), never by guessing from the image.
- Download originals with `fetch.py` (PhotoKit). `osxphotos export --download-missing` silently skips
  iCloud-only files ("missing: 1") from a terminal, and asks y/N on an existing folder, which hangs an agent.

## Setup (once)

```bash
bash <this skill's folder>/scripts/setup.sh
```
Installs `osxphotos` (pipx or uv), checks library access, and saves where these scripts live to
`~/.config/icloud-photos/bridge_dir` so `selfie-picker` and `broll-picker` find them wherever the skill is installed. `BLOCKED` means the terminal app needs
**Full Disk Access** (System Settings > Privacy & Security > Full Disk Access), then restart the terminal.
The first iCloud download triggers a Photos permission prompt: choose **Full Access**.

All scripts run with the osxphotos Python:
```bash
PY=$(cat ~/.config/icloud-photos/python); B=$(cat ~/.config/icloud-photos/bridge_dir)
```

## 1. Who is the owner (once)

```bash
$PY $B/owner.py list --html people.html     # biggest face clusters with a sample photo
$PY $B/owner.py set <person-uuid>           # saved to ~/.config/icloud-photos/owner.json
```
The largest unnamed cluster is usually the library owner. Look at `people.html` (or read the keyphoto
thumbnails) and confirm with the user before saving.

## 2. Catalog

```bash
$PY $B/catalog.py --out catalog.jsonl --since 2026-09-01 [--until ...] [--kind photo|video|all]
```
One JSON line per item: `uuid, date, kind, selfie` (Photos' Selfies album), `front_camera, favorite, burst,
live, w, h, duration, local_original, thumb` (local preview path), `place` (city level), `labels`, `score`
(Apple's 0-1 aesthetics: overall, sharply_focused_subject, well_framed_subject, pleasant_lighting, failure,
noise, ...) and `faces` (person uuid, name, size, quality, eyes: 2 open / 1 closed / 0 unknown, smile).
Hidden, deleted and screenshots are left out. A few thousand items take under a minute.

## 3. Look at candidates

```bash
$PY $B/montage.py picks.json m.jpg --n 24 --title "Selfies"   # m.jpg for you to Read + m.html for the user
$PY $B/sheet.py final.json final.html --title "Selfies"        # HTML sheet alone, for a final set
```
The `.html` is one self-contained file (photos embedded, filename, date and caption under each) that opens
in any browser: hand that to the user. Always look at the JPG yourself first; scores miss what a glance catches.

## 4. Download originals

```bash
jq -r '.[].uuid' picks.json > uuids.txt
$PY $B/fetch.py ./originals --from uuids.txt
```
Full quality through PhotoKit, downloading from iCloud as needed: photos as the current (edited) version, videos
as the original movie, named `<uuid>.<ext>`. Re-running skips files already there.

- First run asks for Photos access: choose **Full Access**.
- `CloudPhotoLibraryErrorDomain 1005` means iCloud refused the download, almost always because the disk is
  nearly full. The script stops itself below 5 GB free (`MIN_FREE_GB=1` overrides it for a few small photos);
  free space, then re-run. Failed items print a hint for the PhotoKit error they hit.
- Fetch needs free disk space for originals; iCloud-only items download on demand.
