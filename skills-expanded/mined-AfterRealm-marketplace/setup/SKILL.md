---
name: setup
description: Set up the UE5 Blueprint plugin — enables Python remote execution in the Unreal Editor so Claude can export and analyze Blueprints.
---

# UE5 Blueprint Skills — Setup

Walk the user through enabling Python remote execution in their Unreal Engine 5 project. This is a one-time setup.

## Prerequisites Check

Run these checks first:

1. **Python 3 installed?**
   ```
   python --version
   ```

2. **upyrc installed?**
   ```
   pip show upyrc
   ```
   If not installed: `pip install upyrc`

3. **UE5 Editor running?** Ask the user if they have their project open.

## UE5 Editor Setup

Guide the user through these steps in the Unreal Editor:

### Step 1: Enable the Python Plugin
1. Open **Edit > Plugins**
2. Search for **"Python Editor Script Plugin"**
3. Enable it (check the box)
4. Restart the editor if prompted

### Step 2: Enable Remote Execution
1. Open **Edit > Project Settings**
2. Search for **"Python"** in the settings search bar
3. Under **Python > Remote Execution**:
   - Check **Enable Remote Execution**
   - Multicast Group Endpoint: `239.0.0.1:6766` (default)
   - Multicast Bind Address: `127.0.0.1` (default, leave as-is)

### Step 3: Test the Connection

Run the test script:
```
python "${CLAUDE_PLUGIN_ROOT}/scripts/test_connection.py"
```

If it prints "Connected to UE5 Editor" — setup is complete.

If it fails:
- Make sure the UE5 Editor is running
- Check that no firewall is blocking UDP port 6766 or TCP port 53320
- Try restarting the editor after enabling the Python plugin

## Known Gotchas

Tell the user about these before they start writing custom scripts:

- **`__file__` doesn't exist** in remote execution context. Scripts run inside UE5 can't use `__file__` or relative paths — use absolute paths or environment variables.
- **Asset path format** varies by project. Some projects use `/Game/MyProject/...`, others use short paths like `/MyMod/...`. If one format fails, try the other. The export scripts handle both.
- **Scripts time out at 120 seconds** by default. For very large Blueprints, increase the timeout with `--timeout 300`.
- **Only one remote connection at a time.** If VS Code or another tool is connected to UE5's Python bridge, disconnect it first or the connection will fail.

## Reference

The remote execution protocol is provided by [upyrc](https://github.com/cgtoolbox/UnrealRemoteControlWrapper) — a Python wrapper around UE5's built-in remote control API. The connection uses UDP multicast (239.0.0.1:6766) for discovery and TCP (127.0.0.1:53320) for command execution.

## Done

Tell the user:
- They can now use `/ue5-blueprints:blueprint-export` to export Blueprints
- They can use `/ue5-blueprints:blueprint-check` to analyze pasted Blueprint data
- They can use `/ue5-blueprints:blueprint-audit` for deep analysis of exported data
- Setup only needs to happen once per project
