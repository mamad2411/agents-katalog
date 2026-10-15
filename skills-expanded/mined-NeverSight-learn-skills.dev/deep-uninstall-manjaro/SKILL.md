---
name: deep-uninstall-manjaro
description: Technical and comprehensive agent skill for complete software removal in Manjaro Linux systems
allowed-tools: AskUserQuestion, Bash, Read, Glob
argument-hint: [software-name]
---

# Deep Uninstall Manjaro

Advanced agent skill for complete and safe software removal in Manjaro Linux systems with multi-source package management support and deep cleanup capabilities.

## When to Use

Use this skill when the user requests to:
- "Uninstall software completely from Manjaro"
- "Remove program and all its traces"
- "Clean up after software removal"
- "Deep uninstall [software-name]"
- "Completely remove [software-name] from system"

## Prerequisites Validation

### Step 0: Input Safety Validation

```bash
# CRITICAL: Validate software name variable
if [ -z "$SOFTWARE_NAME" ] || [ ${#SOFTWARE_NAME} -lt 3 ]; then
    echo "ERROR: Software name too short or empty. Aborting for safety."
    exit 1
fi

# Validate against system paths
if [[ "$SOFTWARE_NAME" =~ ^(/|boot|dev|proc|sys|run|etc|usr|var|home|root)$ ]]; then
    echo "ERROR: Software name matches system path. Aborting for safety."
    exit 1
fi
```

### Step 1: System Verification

Before proceeding, verify the system meets all requirements:

```bash
# Check if running Manjaro
grep -i "manjaro" /etc/os-release && echo "Manjaro detected" || echo "Not Manjaro"

# Verify pamac availability
command -v pamac >/dev/null 2>&1 && echo "Pamac available" || echo "Pamac not found"

# Check pacman as fallback
command -v pacman >/dev/null 2>&1 && echo "Pacman available" || echo "Pacman not found"

# Verify Flatpak support
command -v flatpak >/dev/null 2>&1 && echo "Flatpak available" || echo "Flatpak not found"

# Check system permissions
[ "$(id -u)" = "0" ] && echo "Running as root" || echo "Running as user (sudo required)"
```

If any critical component fails, inform the user and suggest alternatives.

## Phase 1: Software Origin Identification

Execute these checks in hierarchical order to determine installation method:

### 1.1 Pamac/Pacman Native Packages

```bash
# Primary check with pamac (preferred)
pamac info "$SOFTWARE_NAME" 2>/dev/null && echo "Found in pamac"

# Fallback with pacman
pacman -Qi "$SOFTWARE_NAME" 2>/dev/null && echo "Found in pacman"

# Check if package is from AUR specifically
pamac info "$SOFTWARE_NAME" | grep -i "aur" && echo "AUR package detected"
```

### 1.2 Flatpak Applications

```bash
# Search Flatpak installations
flatpak list --app | grep -i "$SOFTWARE_NAME" && echo "Found Flatpak app"

# Search Flatpak runtimes
flatpak list --runtime | grep -i "$SOFTWARE_NAME" && echo "Found Flatpak runtime"

# Get Flatpak ID for removal
flatpak list --app | grep -i "$SOFTWARE_NAME" | cut -f1
```

### 1.3 Manual/External Installations

```bash
# Locate binary in system paths
which "$SOFTWARE_NAME" 2>/dev/null && echo "Binary found"

# Search common installation directories
find /usr/local/bin /opt /usr/local/lib -name "*$SOFTWARE_NAME*" 2>/dev/null

# Check user-local installations
find $HOME/.local/bin $HOME/.local/lib -name "*$SOFTWARE_NAME*" 2>/dev/null
```

### 1.5 Snap and AppImage Detection

```bash
# Check for Snap packages
if command -v snap >/dev/null 2>&1; then
    snap list | grep -i "$SOFTWARE_NAME" && echo "Found Snap package"
fi

# Check for AppImage integrations
find $HOME/.local/share/applications -name "*$SOFTWARE_NAME*.desktop" -exec grep -l "AppImage" {} + 2>/dev/null && echo "Found AppImage integration"

# Check for actual AppImage files
find $HOME/.local/bin /opt -name "*.AppImage" 2>/dev/null | grep -i "$SOFTWARE_NAME" && echo "Found AppImage file"
```

### 1.6 Fuzzy Name Matching

```bash
# Fuzzy search in pamac for similar names
pamac search "$SOFTWARE_NAME" | head -n 5

# Generate alternative name suggestions
echo "Similar packages found:"
pamac search "$SOFTWARE_NAME" | awk '{print $1}' | head -n 3
```

## Phase 2: Primary Uninstallation Execution

Based on Phase 1 results, execute appropriate removal method:

### 2.1 Native Package Removal (Official/AUR)

```bash
# Preferred: Use pamac for comprehensive removal
pamac remove --orphans "$SOFTWARE_NAME"

# Alternative: Use pacman with full dependency removal
pacman -Rns "$SOFTWARE_NAME"

# Verify removal
pamac info "$SOFTWARE_NAME" 2>/dev/null || echo "Package successfully removed"
```

### 2.2 Flatpak Removal

```bash
# Remove Flatpak application with data
flatpak uninstall --delete-data "$FLATPAK_ID"

# Remove unused runtimes
flatpak uninstall --unused

# Verify removal
flatpak list | grep -i "$SOFTWARE_NAME" || echo "Flatpak successfully removed"
```

### 2.3 Language Package Managers

```bash
# Python package removal
pip uninstall "$SOFTWARE_NAME"

# Node.js global package removal
npm uninstall -g "$SOFTWARE_NAME"

# Ruby gem removal
gem uninstall "$SOFTWARE_NAME"
```

### 2.4 Snap Package Removal

```bash
# Remove Snap package with data
snap remove "$SOFTWARE_NAME" --purge

# Verify removal
snap list | grep -i "$SOFTWARE_NAME" || echo "Snap successfully removed"
```

### 2.5 Manual Installation Removal

```bash
# Search for uninstall scripts
find /usr/local /opt -name "uninstall*" -path "*$SOFTWARE_NAME*" 2>/dev/null

# Search for cleanup scripts
find /usr/local /opt -name "cleanup*" -path "*$SOFTWARE_NAME*" 2>/dev/null

# Execute found uninstall scripts if safe
for script in $(find /usr/local /opt -name "uninstall*" -path "*$SOFTWARE_NAME*" 2>/dev/null); do
    echo "Found uninstall script: $script"
    # Ask user confirmation before execution
done
```

## Phase 3: Deep Residue Scanning

After primary removal, perform comprehensive system-wide residue search:

### 3.1 Optimized Configuration Files Search

```bash
# Define search hotspots (avoid global find)
SEARCH_HOTSPOTS=(
    "$HOME/.config"
    "$HOME/.local/share"
    "$HOME/.cache"
    "/etc"
    "/var/lib"
    "/opt"
    "/usr/local"
    "/usr/share"
)

# Search in hotspots only
for hotspot in "${SEARCH_HOTSPOTS[@]}"; do
    find "$hotspot" -maxdepth 3 -name "*$SOFTWARE_NAME*" -type d 2>/dev/null
    find "$hotspot" -maxdepth 4 -name "*$SOFTWARE_NAME*" -type f 2>/dev/null
done

# Alternative: Use faster tools if available
if command -v fd >/dev/null 2>&1; then
    fd --max-depth 4 "*$SOFTWARE_NAME*" /home 2>/dev/null
    fd --max-depth 3 "*$SOFTWARE_NAME*" /etc 2>/dev/null
fi

if command -v locate >/dev/null 2>&1; then
    locate -r "/$SOFTWARE_NAME" | grep -E "(config|cache|local)" 2>/dev/null
fi
```

### 3.2 System Configuration Search

```bash
# Global configuration
find /etc -maxdepth 2 -name "*$SOFTWARE_NAME*" 2>/dev/null

# System data directories
find /var/lib -maxdepth 2 -name "*$SOFTWARE_NAME*" 2>/dev/null

# Optional software directory
find /opt -maxdepth 2 -name "*$SOFTWARE_NAME*" 2>/dev/null

# Local installation directories
find /usr/local -maxdepth 2 -name "*$SOFTWARE_NAME*" 2>/dev/null
```

### 3.3 Hidden and System Files

```bash
# Search for hidden configuration files
find / -name ".*$SOFTWARE_NAME*" 2>/dev/null | grep -E "(config|cache|local)"

# Search for desktop entries
find /usr/share/applications -name "*$SOFTWARE_NAME*.desktop" 2>/dev/null
find $HOME/.local/share/applications -name "*$SOFTWARE_NAME*.desktop" 2>/dev/null

# Search for icon files
find /usr/share/icons -name "*$SOFTWARE_NAME*" 2>/dev/null
```

## Phase 4: User Project Protection Algorithm

CRITICAL: Protect user projects and documents from accidental deletion.

### 4.1 File Type Filtering

```bash
# Define protected file extensions
PROTECTED_EXTENSIONS=".jpg|.jpeg|.png|.gif|.pdf|.doc|.docx|.xls|.xlsx|.ppt|.pptx|.txt|.md|.sql|.sqlite|.db|.project|.workspace"

# Filter out user documents from deletion list
echo "$FOUND_FILES" | grep -vE "\.($PROTECTED_EXTENSIONS)$"
```

### 4.2 Directory Name Protection

```bash
# Define protected directory patterns
PROTECTED_DIRS="projects|work|documents|desktop|downloads|music|videos|pictures|backup"

# Exclude protected directories from deletion
echo "$FOUND_DIRECTORIES" | grep -vE "($PROTECTED_DIRS)"

# CRITICAL: Exclude system paths
PROTECTED_SYSTEM_PATHS="/boot|/dev|/proc|/sys|/run"
echo "$FOUND_FILES" | grep -vE "^($PROTECTED_SYSTEM_PATHS)"
```
```

### 4.3 Project Detection Algorithm

```bash
# Detect potential project directories by content analysis
for dir in $FOUND_DIRECTORIES; do
    # Check for project indicators
    if [ -f "$dir/Makefile" ] || [ -f "$dir/package.json" ] || [ -f "$dir/requirements.txt" ] || [ -f "$dir/.git/config" ]; then
        echo "[PROJECT DETECTED] $dir - Excluding from automatic deletion"
    fi
done
```

## Phase 5: Active Process Detection

Before proceeding with uninstallation, check if the software is currently running:

```bash
# Check for running processes
if pgrep -i "$SOFTWARE_NAME" >/dev/null 2>&1; then
    echo "[WARNING] Software is currently running. Consider closing it first."
    pgrep -i "$SOFTWARE_NAME"
fi

# Check for systemd services
systemctl list-units --type=service --state=running | grep -i "$SOFTWARE_NAME" && echo "[WARNING] System service detected"
```

## Phase 6: Dependency Impact Analysis

Check what other packages might be affected by the removal:

```bash
# Check reverse dependencies (requires pactree installation)
if command -v pactree >/dev/null 2>&1; then
    echo "[INFO] Checking reverse dependencies..."
    pactree -r "$SOFTWARE_NAME" 2>/dev/null || echo "pactree analysis completed"
else
    echo "[INFO] Install pactree for dependency analysis: sudo pacman -S pacman-contrib"
    echo "[INFO] pactree helps identify packages that depend on $SOFTWARE_NAME"
fi

# Alternative: Check with pamac
pamac info "$SOFTWARE_NAME" | grep -A 10 "Required By"
```

## Phase 7: User Confirmation and Report

Before any residue deletion, present detailed report to user:

### 5.1 Generate Residue Report

```
=== RESIDUE ANALYSIS REPORT ===

Software: $SOFTWARE_NAME
Primary Removal: SUCCESSFUL

Residues Found: $REsidue_COUNT

Configuration Files:
- $HOME/.config/$SOFTWARE_NAME/settings.conf (2.1KB)
- /etc/$SOFTWARE_NAME/config.yaml (1.5KB)

Data Files:
- $HOME/.local/share/$SOFTWARE_NAME/database.db (15.2MB)
- /var/lib/$SOFTWARE_NAME/logs/ (250MB)

[!] PROTECTED ITEMS (Not marked for deletion):
- $HOME/$SOFTWARE_NAME-projects/ (Detected as user project directory)
- $HOME/Documents/$SOFTWARE_NAME-notes.pdf (User document)

Items Marked for Deletion: $DELETION_COUNT
Total Size to be Freed: $SIZE_TO_FREE MB
```

### 5.2 User Confirmation Prompt

Use AskUserQuestion to present options:

**Choose action for residues:**
1. Delete all marked residues
2. Review each item individually
3. Backup residues before deletion
4. Skip residue cleanup
5. Show detailed file list

## Phase 6: Executed Cleanup

Based on user confirmation:

### 6.1 Safe Residue Removal

```bash
# Prefer trash-cli if available for safety
if command -v trash-put >/dev/null 2>&1; then
    echo "[INFO] Moving files to trash (safer option)"
    trash-put $HOME/.config/$SOFTWARE_NAME 2>/dev/null
    trash-put /etc/$SOFTWARE_NAME 2>/dev/null
    trash-put $HOME/.local/share/$SOFTWARE_NAME 2>/dev/null
    trash-put /var/lib/$SOFTWARE_NAME 2>/dev/null
    trash-put $HOME/.cache/$SOFTWARE_NAME 2>/dev/null
else
    echo "[WARNING] trash-cli not available, using permanent deletion"
    echo "[INFO] Install trash-cli for safer operations: sudo pacman -S trash-cli"

    # Remove configuration files
    rm -rf $HOME/.config/$SOFTWARE_NAME 2>/dev/null
    rm -rf /etc/$SOFTWARE_NAME 2>/dev/null

    # Remove data files
    rm -rf $HOME/.local/share/$SOFTWARE_NAME 2>/dev/null
    rm -rf /var/lib/$SOFTWARE_NAME 2>/dev/null

    # Remove cache files
    rm -rf $HOME/.cache/$SOFTWARE_NAME 2>/dev/null
fi
```

### 6.2 System File Cleanup

```bash
# Remove desktop entries
rm -f /usr/share/applications/*$SOFTWARE_NAME*.desktop
rm -f $HOME/.local/share/applications/*$SOFTWARE_NAME*.desktop

# Remove icon files
find /usr/share/icons -name "*$SOFTWARE_NAME*" -delete 2>/dev/null

# Remove manual pages
find /usr/share/man -name "*$SOFTWARE_NAME*" -delete 2>/dev/null
```

### 9.3 AUR Build Cleanup

```bash
# Clear AUR build cache for this specific software
find /var/tmp/pamac-build-* -maxdepth 1 -name "*$SOFTWARE_NAME*" -type d -exec rm -rf {} + 2>/dev/null

# Clear makepkg build directories
find /tmp/makepkg-* -maxdepth 1 -name "*$SOFTWARE_NAME*" -type d -exec rm -rf {} + 2>/dev/null
```

## Phase 10: Final Verification

### 10.1 Orphaned Dependencies Removal

```bash
# Remove orphaned packages
pamac remove --orphans

# Alternative with pacman
pacman -Rns $(pacman -Qtdq)

# Clear package cache
pamac clean --build-files
pacman -Scc
```

### 10.2 Final Verification

```bash
# Verify complete removal
echo "=== FINAL VERIFICATION ==="

# Check for any remaining references
if command -v "$SOFTWARE_NAME" >/dev/null 2>&1; then
    echo "[!] WARNING: Binary still found in system"
fi

# Check for remaining configuration
if [ -d "$HOME/.config/$SOFTWARE_NAME" ]; then
    echo "[!] WARNING: Configuration directory still exists"
fi

# System cleanup summary
echo "Cleanup completed successfully"
echo "Disk space freed: $FREED_SPACE MB"
```

## Error Handling and Edge Cases

### Common Issues and Solutions

1. **Package Not Found**: "Software not found in any package manager"
   - Solution: Proceed with manual binary search and file system cleanup

2. **Permission Denied**: "Cannot remove system files"
   - Solution: Prompt for sudo privileges or skip system-level files

3. **Dependencies in Use**: "Cannot remove, required by other packages"
   - Solution: Show dependent packages and ask for confirmation

4. **Large Data Directories**: "Data directory is >1GB"
   - Solution: Special confirmation for large deletions

### Safety Mechanisms

- Always verify system is Manjaro before proceeding
- Require explicit confirmation for system-level file deletions
- Protect user project directories with advanced detection
- Provide backup option before residue cleanup
- Log all actions for audit trail

## Workflow Summary

1. **System Verification** → Confirm Manjaro and required tools
2. **Origin Detection** → Identify installation method (pamac/pacman/flatpak/manual)
3. **Primary Removal** → Execute appropriate uninstall command
4. **Deep Scanning** → Search entire system for residues
5. **Protection Filtering** → Exclude user projects and documents
6. **User Confirmation** → Present detailed report and get approval
7. **Residue Cleanup** → Remove confirmed residues safely
8. **Final Cleanup** → Remove orphaned dependencies and verify completion

This skill ensures complete software removal while protecting user data and providing full transparency throughout the process.
