# MEGA Manager Skill

> **QUICK REFERENCE**
> - **Downloads folder**: `output/mega-downloads/`
> - **Browse script**: `.venv\Scripts\python.exe scripts/mega/mega_browse.py`
> - **Commands**: `mega-ls`, `mega-get`, `mega-find`, `mega-du`, `mega-whoami`
> - **Login**: `mega-login user@email.com password` (must be done before any MEGA operations)
> - **Prerequisite**: MEGA CMD must be installed from https://mega.io/cmd
> - **Python**: ALWAYS use `.venv\Scripts\python.exe` (never bare `python`)

## Purpose
Browse, search, and download files from MEGA cloud storage using MEGA CMD.
**LOCAL/READ-ONLY by default** — no uploads unless user explicitly requests.

## Trigger Phrases
- "browse my MEGA", "list MEGA files", "download from MEGA"
- "find file in MEGA", "MEGA storage", "check MEGA space"
- `/mega browse`, `/mega download`, `/mega find`, `/mega info`

## Prerequisites
- MEGA CMD installed: https://mega.io/cmd
- User must be logged in via `mega-login` before use

---

## Installation & Setup (Windows)

### Step 1: Install MEGA CMD

**Option A: Direct Download (Recommended)**
```bash
# Download installer
curl -L -o "MEGAcmdSetup64.exe" "https://mega.nz/MEGAcmdSetup64.exe"

# Run installer (manual step)
start MEGAcmdSetup64.exe
```

**Option B: Manual**
1. Download from: https://mega.io/cmd
2. Run `MEGAcmdSetup64.exe`
3. Restart terminal after installation

### Step 2: MEGA CMD Location

After installation, MEGA CMD is at:
```
C:\Users\[USERNAME]\AppData\Local\MEGAcmd\
```

Contains:
- `MEGAclient.exe` - Main client executable
- `mega-*.bat` - Command batch files
- `MEGAcmdServer.exe` - Background server

### Step 3: Login to Account

```bash
# Using full path (recommended for Claude):
"C:\Users\[USERNAME]\AppData\Local\MEGAcmd\mega-login.bat" email@example.com "password"

# Or via PowerShell:
powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' login email@example.com password"
```

**IMPORTANT**: First login syncs account metadata. For large accounts (100GB+), this takes several minutes. Wait for completion.

### Step 4: Verify Login

```bash
powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' whoami"
```

---

## Running MEGA Commands from Claude

### Recommended Method (PowerShell)

Since MEGA CMD may not be in system PATH, use PowerShell with full paths:

```bash
# List files
powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' ls -l /"

# Check login
powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' whoami"

# Download file
powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' get '/remote/path' 'output/mega-downloads/'"
```

### Alternative Method (Batch files)

```bash
"C:\Users\[USERNAME]\AppData\Local\MEGAcmd\mega-ls.bat" /
"C:\Users\[USERNAME]\AppData\Local\MEGAcmd\mega-whoami.bat"
```

**Note**: Batch files may have path resolution issues with Git Bash. PowerShell method is more reliable.

---

## 3-Mode Workflow

### MODE 1: PLAN
1. Check MEGA CMD is installed:
   ```bash
   powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' version"
   ```
2. Check login status:
   ```bash
   powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' whoami"
   ```
3. If not installed → provide install instructions and stop
4. If not logged in → guide user through login process
5. Determine user intent: browse, search, download, or info

### MODE 2: CLARIFY
- Ask: What path to browse? (default: `/`)
- Ask: What file to search for? (if find)
- Ask: Where to download? (default: `output/mega-downloads/`)
- Confirm download before executing

### MODE 3: IMPLEMENT

**Browse files:**
```bash
powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' ls -l '/path'"
```

**Search files:**
```bash
powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' find '/' --pattern '*.mp4'"
```

**Download files:**
```bash
powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' get '/remote/path' 'output/mega-downloads/'"
```

**Storage info:**
```bash
powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' du /"
powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' whoami"
```

---

## Output Paths

- Downloaded files: `output/mega-downloads/`
- Transcripts: `output/transcripts/`
- File listings: displayed in console

---

## Safety Rules

1. **NEVER** upload files unless user explicitly says "upload"
2. **NEVER** delete remote files
3. **ALWAYS** confirm before downloading large files/folders
4. **SHOW** file sizes before download when possible
5. **WAIT** for login sync to complete before running commands

---

## Troubleshooting

### "Command not found"
Use full path to MEGAclient.exe via PowerShell.

### "Not logged in" error
Run login command and wait for sync to complete:
```bash
powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' login email password"
```

### "Invalid destiny" error
Path resolution issue with Git Bash. Use PowerShell method instead.

### Login takes too long
First login syncs all account metadata. Large accounts (100GB+) can take 5-10 minutes. This is normal.

### Server not running
Start server manually:
```bash
start "" "C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAcmdServer.exe"
```
