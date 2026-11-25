---
name: cc-installer
description: Expert knowledge for creating CC:Tweaked installer scripts that download files from GitHub and handle path resolution correctly. Use when creating installers for turtle/computer script projects.
---

# CC:Tweaked Installer Script Skill

I am an expert in creating installer scripts for CC:Tweaked projects that download files from GitHub and properly configure paths so that `require()` works correctly.

## When to Use This Skill

- Creating an installer for a new CC:Tweaked project
- Setting up script distribution via GitHub raw content
- Fixing "module not found" errors in CC:Tweaked projects
- Creating modular script libraries with proper path resolution
- Helping users download and install scripts on turtles/computers

## Critical Knowledge: CC:Tweaked Path Resolution

### The Problem

CC:Tweaked's `require()` resolves module paths **relative to the running script's location**, NOT relative to the current working directory. This causes issues when:

1. Scripts are organized in subdirectories (e.g., `mining/smart_miner.lua`)
2. Those scripts need modules from sibling directories (e.g., `common/movement.lua`)

**Example of the problem:**

```
/myproject/
├── common/
│   └── movement.lua
└── mining/
    └── miner.lua      <- require("common.movement") FAILS here!
```

When `miner.lua` calls `require("common.movement")`, CC:Tweaked looks for `/myproject/mining/common/movement.lua` (relative to the script), not `/myproject/common/movement.lua`.

### The Solution: Absolute Paths

The fix is to compute the **absolute root directory** and add it to `package.path`:

```lua
-- PATH SETUP BOILERPLATE - Add to top of any script in a subdirectory
local function setupPaths()
    -- Get the absolute path to this script
    local scriptPath = shell.getRunningProgram()
    local absPath = "/" .. shell.resolve(scriptPath)

    -- Extract the directory containing this script
    -- e.g., "/mining/smart_miner.lua" -> "/mining/"
    local scriptDir = absPath:match("(.+/)") or "/"

    -- Go up one directory to find the root
    -- e.g., "/mining/" -> "/"
    -- e.g., "/myproject/mining/" -> "/myproject/"
    local rootDir
    if scriptDir == "/" then
        rootDir = "/"
    else
        local withoutTrailing = scriptDir:sub(1, -2)
        rootDir = withoutTrailing:match("(.*/)" ) or "/"
    end

    -- Add root to package path with ABSOLUTE paths
    package.path = rootDir .. "?.lua;" .. rootDir .. "?/init.lua;" .. package.path

    return rootDir
end

local ROOT_DIR = setupPaths()

-- Now require works correctly!
local movement = require("common.movement")
```

**Key points:**

- Use `shell.resolve()` to get absolute path
- Always prefix with `/` for absolute paths
- Add to `package.path` BEFORE any `require()` calls

---

## Installer Template

Here's a complete, customizable installer template:

```lua
--- Installer Script for CC:Tweaked Projects
-- Downloads all required files from GitHub to the turtle/computer
--
-- CUSTOMIZATION:
-- 1. Change GITHUB_USER, GITHUB_REPO, GITHUB_BRANCH
-- 2. Change PROJECT_FOLDER to your project name
-- 3. Update the 'files' table with your files
-- 4. Update the 'directories' table with your folders
--
-- Usage:
--   wget https://raw.githubusercontent.com/USER/REPO/BRANCH/path/to/installer.lua installer
--   installer
--
-- @script installer

-- ============================================
-- CONFIGURATION - CUSTOMIZE THESE VALUES
-- ============================================
local GITHUB_USER = "YOUR_USERNAME"       -- Your GitHub username
local GITHUB_REPO = "YOUR_REPO"           -- Your repository name
local GITHUB_BRANCH = "main"              -- Branch (main, master, etc.)
local PROJECT_FOLDER = "myproject"        -- Folder name in repo (path after /scripts/)

-- Base URL for raw GitHub content
local baseUrl = string.format(
    "https://raw.githubusercontent.com/%s/%s/%s/scripts/%s/",
    GITHUB_USER, GITHUB_REPO, GITHUB_BRANCH, PROJECT_FOLDER
)

-- ============================================
-- FILES TO DOWNLOAD - CUSTOMIZE THIS LIST
-- ============================================
local files = {
    -- Common libraries (shared modules)
    { path = "common/init.lua",      required = true },
    { path = "common/movement.lua",  required = true },
    { path = "common/utils.lua",     required = true },

    -- Configuration files
    { path = "config/settings.cfg",  required = true },

    -- Main scripts
    { path = "scripts/main.lua",     required = true },
    { path = "scripts/helper.lua",   required = false },  -- optional
}

-- Directories to create (must exist before downloading files into them)
local directories = {
    "common",
    "config",
    "scripts",
}

-- ============================================
-- INSTALLER LOGIC - Usually no changes needed below
-- ============================================

local function printHeader()
    term.clear()
    term.setCursorPos(1, 1)
    print("========================================")
    print("   " .. PROJECT_FOLDER .. " Installer")
    print("========================================")
    print("")
end

local function checkHttp()
    if not http then
        printError("HTTP API is not available!")
        printError("")
        printError("Ask your server admin to enable HTTP:")
        printError("  1. Edit config/computercraft-server.toml")
        printError("  2. Set http.enabled = true")
        printError("  3. Restart the server")
        return false
    end
    return true
end

local function createDirectories()
    print("Creating directories...")
    for _, dir in ipairs(directories) do
        if not fs.exists(dir) then
            fs.makeDir(dir)
            print("  Created: " .. dir .. "/")
        else
            print("  Exists:  " .. dir .. "/")
        end
    end
    print("")
end

local function downloadFile(remotePath, localPath)
    local url = baseUrl .. remotePath
    local response, err = http.get(url)

    if not response then
        return false, err or "Unknown error"
    end

    local content = response.readAll()
    response.close()

    local file = fs.open(localPath, "w")
    if not file then
        return false, "Could not write to " .. localPath
    end

    file.write(content)
    file.close()

    return true
end

local function downloadFiles()
    print("Downloading files...")
    local success = true
    local failed = {}

    for _, fileInfo in ipairs(files) do
        local path = fileInfo.path
        local isRequired = fileInfo.required

        write("  " .. path .. "... ")
        local ok, err = downloadFile(path, path)

        if ok then
            print("OK")
        else
            if isRequired then
                print("FAILED")
                table.insert(failed, {path = path, url = baseUrl .. path, error = err})
                success = false
            else
                print("skipped (optional)")
            end
        end
    end

    print("")

    -- Show detailed error info for failures
    if #failed > 0 then
        printError("========================================")
        printError("DOWNLOAD FAILURES:")
        printError("========================================")
        for _, f in ipairs(failed) do
            printError("")
            printError("File: " .. f.path)
            printError("URL:  " .. f.url)
            printError("Error: " .. tostring(f.error))
        end
        printError("========================================")
        print("")
    end

    return success
end

local function removeFiles()
    print("Removing installed files...")

    for _, fileInfo in ipairs(files) do
        if fs.exists(fileInfo.path) then
            fs.delete(fileInfo.path)
            print("  Deleted: " .. fileInfo.path)
        end
    end

    -- Remove directories (in reverse order, deepest first)
    for i = #directories, 1, -1 do
        local dir = directories[i]
        if fs.exists(dir) and fs.isDir(dir) then
            local contents = fs.list(dir)
            if #contents == 0 then
                fs.delete(dir)
                print("  Removed: " .. dir .. "/")
            else
                print("  Kept:    " .. dir .. "/ (not empty)")
            end
        end
    end

    print("")
    print("Uninstall complete!")
end

local function showUsage()
    print("Usage:")
    print("  installer          Install all files")
    print("  installer update   Re-download all files")
    print("  installer remove   Uninstall everything")
    print("")
end

local function main(args)
    printHeader()

    local command = args[1] or "install"

    if command == "help" or command == "-h" or command == "--help" then
        showUsage()
        return
    end

    if command == "remove" or command == "uninstall" then
        removeFiles()
        return
    end

    if not checkHttp() then
        return
    end

    if command == "update" then
        print("Updating " .. PROJECT_FOLDER .. "...")
        print("")
    else
        print("Installing " .. PROJECT_FOLDER .. "...")
        print("")
    end

    createDirectories()

    if downloadFiles() then
        print("========================================")
        print("Installation complete!")
        print("========================================")
        print("")
        print("Run your main script:")
        print("  scripts/main 50")
        print("")
    else
        printError("Installation failed!")
        printError("Check error messages above.")
    end
end

-- Capture args at file scope (required for Lua 5.2)
local tArgs = { ... }
main(tArgs)
```

---

## Creating a Path Init Module

For projects with multiple scripts in subdirectories, create a reusable path initialization module:

**common/init.lua:**

```lua
--- Path initialization module
-- Fixes package.path to allow require() to find common modules
-- from any subdirectory.
--
-- Usage: Add at top of any script in a subdirectory:
--   dofile(shell.resolve("common/init.lua"))
--   -- or if you can require it:
--   require("common.init")
--
-- @module init

local scriptPath = shell and shell.getRunningProgram() or ""
local absPath = ""
if shell and scriptPath ~= "" then
    absPath = "/" .. shell.resolve(scriptPath)
end

local scriptDir = absPath:match("(.+/)") or "/"

local rootDir = "/"
if scriptDir ~= "/" then
    local withoutTrailing = scriptDir:sub(1, -2)
    rootDir = withoutTrailing:match("(.*/)" ) or "/"
end

package.path = rootDir .. "?.lua;" .. rootDir .. "?/init.lua;" .. package.path

return {
    rootDir = rootDir,
    scriptDir = scriptDir,
    scriptPath = absPath
}
```

---

## Project Structure Best Practices

### Recommended Structure

```
/myproject/
├── installer.lua       <- Installer script (downloads everything)
├── common/             <- Shared libraries
│   ├── init.lua        <- Path initialization module
│   ├── movement.lua    <- Turtle movement utilities
│   └── utils.lua       <- General utilities
├── config/             <- Configuration files
│   └── settings.cfg    <- User-editable settings
├── scripts/            <- Main executable scripts
│   ├── main.lua        <- Primary script
│   └── helper.lua      <- Secondary script
└── docs/               <- Documentation (optional, not downloaded)
    └── README.md
```

### Key Design Principles

1. **All shared code in `common/`** - Modules that multiple scripts use
2. **Executable scripts in dedicated folder** - e.g., `scripts/`, `mining/`, `farming/`
3. **Config files separate** - Easy for users to edit without touching code
4. **Path setup at script top** - Every script in a subdirectory needs the boilerplate

---

## Customization Checklist

When creating a new installer, customize these items:

### 1. GitHub Configuration

```lua
local GITHUB_USER = "your_username"
local GITHUB_REPO = "your_repo"
local GITHUB_BRANCH = "main"
local PROJECT_FOLDER = "your_project_name"
```

### 2. Files List

Add all files your project needs:

```lua
local files = {
    { path = "common/init.lua",      required = true },
    { path = "common/yourmodule.lua", required = true },
    { path = "scripts/yourscript.lua", required = true },
    -- Add more files as needed
}
```

### 3. Directories List

List all directories that need to be created:

```lua
local directories = {
    "common",
    "config",
    "scripts",
}
```

### 4. Completion Message

Update the success message to show correct usage:

```lua
print("Run your main script:")
print("  scripts/yourscript <args>")
```

---

## Common Issues and Solutions

### "Module not found" Error

**Cause:** `require()` is resolving relative to script location, not root.
**Solution:** Add the path setup boilerplate to the top of your script.

### HTTP Not Available

**Cause:** Server has HTTP disabled.
**Solution:** Edit `config/computercraft-server.toml`:

```toml
[http]
    enabled = true

[[http.rules]]
    host = "*"
    action = "allow"
```

### Download Fails with "nil"

**Cause:** URL is incorrect or file doesn't exist on GitHub.
**Solution:**

1. Check the file exists in your repo
2. Verify branch name is correct
3. Test the URL in a browser

### "Cannot use '...' outside vararg function"

**Cause:** Trying to use `{ ... }` inside a function instead of at file scope.
**Solution:** Capture args at file scope:

```lua
-- At TOP of file, not inside a function:
local tArgs = { ... }

local function main(args)
    -- use args here
end

main(tArgs)
```

---

## Testing Installers

### Local Testing (CraftOS-PC)

1. Install CraftOS-PC emulator
2. Run the emulator
3. Test wget and installer commands

### Syntax Checking

Before pushing to GitHub, validate Lua syntax:

```powershell
# Windows with Lua installed
lua -c installer.lua

# Or use luac
luac -p installer.lua
```

### Test the Raw URL

Verify your GitHub raw URL works by opening in a browser:

```
https://raw.githubusercontent.com/USER/REPO/BRANCH/scripts/PROJECT/installer.lua
```

---

## Example: Complete Project Setup

Here's how to set up a new project from scratch:

### 1. Create Project Structure

```
/scripts/
└── mybot/
    ├── installer.lua
    ├── common/
    │   ├── init.lua
    │   └── movement.lua
    ├── config/
    │   └── settings.cfg
    └── mining/
        └── digger.lua
```

### 2. Create installer.lua

Use the template above with:

```lua
local GITHUB_USER = "yourname"
local GITHUB_REPO = "computercraft"
local PROJECT_FOLDER = "mybot"

local files = {
    { path = "common/init.lua",      required = true },
    { path = "common/movement.lua",  required = true },
    { path = "config/settings.cfg",  required = true },
    { path = "mining/digger.lua",    required = true },
}

local directories = {
    "common",
    "config",
    "mining",
}
```

### 3. Create common/init.lua

Use the path init module template above.

### 4. Add Path Setup to digger.lua

```lua
-- mining/digger.lua
local function setupPaths()
    local scriptPath = shell.getRunningProgram()
    local absPath = "/" .. shell.resolve(scriptPath)
    local scriptDir = absPath:match("(.+/)") or "/"
    local rootDir
    if scriptDir == "/" then
        rootDir = "/"
    else
        local withoutTrailing = scriptDir:sub(1, -2)
        rootDir = withoutTrailing:match("(.*/)" ) or "/"
    end
    package.path = rootDir .. "?.lua;" .. rootDir .. "?/init.lua;" .. package.path
    return rootDir
end

local ROOT_DIR = setupPaths()

-- Now require works!
local movement = require("common.movement")

-- Rest of your script...
```

### 5. Push to GitHub and Test

```bash
git add -A
git commit -m "Add mybot project"
git push
```

On turtle:

```
wget https://raw.githubusercontent.com/yourname/computercraft/main/scripts/mybot/installer.lua installer
installer
mining/digger
```
