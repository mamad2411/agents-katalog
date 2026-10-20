---
name: environment-check
description: Use when the user wants to know which evidence-handling tools are present on this host before running a pipeline — probes hashing, metadata, timestamping, packaging, and storage CLIs and reports what is missing with an install hint for each. Triggers - "check evidence tools", "what forensics tools are installed", "why did hashing fail".
allowed-tools: Bash(command *), Bash(sw_vers *), Bash(uname *), Read
---

# Environment Check

Probe the host for the CLIs this pipeline depends on and report exactly which stages
are currently blocked. Read-only — this skill installs nothing.

## When to use

- Before the first run on a new machine.
- When a command failed with "not found" and it is unclear which tool is missing.
- When handing a workflow to someone else and you need to state its prerequisites.

## Procedure

### 1. Identify the platform

```bash
uname -s                  # Darwin or Linux
sw_vers -productVersion   # macOS only; ignore a failure here
```

Platform decides which hashing binaries to expect. macOS ships `shasum` and `md5`;
GNU systems ship `sha256sum` and `md5sum`. Neither ships `b3sum`.

### 2. Probe each tool

Check presence with `command -v`, never by running the tool. A probe must not have
side effects.

| Tool | Stage it unblocks | Install hint |
| --- | --- | --- |
| `shasum` or `sha256sum` | hashing, verification | preinstalled on macOS and most Linux |
| `b3sum` | optional second hash | `brew install b3sum` / `cargo install b3sum` |
| `exiftool` | metadata inspection | `brew install exiftool` / `apt-get install libimage-exiftool-perl` |
| `mediainfo` | audio and video metadata | `brew install mediainfo` / `apt-get install mediainfo` |
| `file` | MIME typing during custody logging | preinstalled |
| `single-file` | web page capture | `npm install -g single-file-cli` |
| `ots` | OpenTimestamps anchoring | plugin virtual environment, see evidence-install-deps |
| `bagit.py` | BagIt packaging and validation | plugin virtual environment, see evidence-install-deps |
| `mat2` | metadata scrubbing on derived copies | plugin virtual environment, see evidence-install-deps |
| `rclone` | replication to remote storage | `brew install rclone` / `apt-get install rclone` |
| `aws` | S3 Object Lock and retention settings | `brew install awscli` / `pip install awscli` |
| `qpdf` | PDF structure work | `brew install qpdf` / `apt-get install qpdf` |

For each, record present or missing. For hashing, treat the pair as satisfied if
either member is present.

### 3. Check the plugin virtual environment

```bash
PLUGIN_DATA_DIR="${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/evidence-ops"
test -x "$PLUGIN_DATA_DIR/venv/bin/python" && echo "venv present" || echo "venv missing"
```

Python-based tools are looked for inside that virtual environment first and on `PATH`
second. Report which location satisfied each.

### 4. Report

Print one table of tool, status, and location. Then state, in plain terms, which
pipeline stages are blocked right now — for example "timestamping unavailable, `ots`
not installed". Do not offer to install anything here; name the evidence-install-deps skill and
stop.

## Output

- A table written to the conversation. No files are created or modified.

## Notes

- A missing optional tool is not an error. `b3sum` and `mat2` are optional; hashing,
  custody logging, and verification work without them.
- Do not infer a tool's absence from a failed run of a different tool.
