# PKCore Workspace Instructions

## Primary Project
- **PKCore (`d:\Appz\PKCore`) is the main project of this workspace.** All code changes, new files, builds, and fixes target PKCore unless the user explicitly says otherwise.
- The other workspace folders are **read-only references**:
  - `d:\Appz\Suisource\GSD1`, `GSD2`, `GSDShare` — decompiled game source, used only for grounding.
  - `d:\Appz\Suisource\Ideas` — notes/ideas, read for context only.
  - `...\Suikoden I and II HD Remaster\BepInEx` and `...\PKCore` — game install / runtime output (logs, configs, textures). Do not write project code there.
- Never edit decompiled source files; implement behavior changes as Harmony patches in PKCore instead.

## Environment & Build
- **Symlink Setup**: The build output directory is symlinked directly to the game's BepInEx plugins directory (`d:\SteamLibrary\steamapps\common\Suikoden I and II HD Remaster\BepInEx\plugins\`).
- **NEVER** run manual `Copy-Item` or file copy commands to the game folder. Running `dotnet build` is sufficient.

## Grounding
- Always ground game mechanics, methods, fields, and data in the local decompiled source code across the following workspaces:
  - **Suikoden I**: `d:\Appz\Suisource\GSD1` (`d:\Appz\Suisource\GSD1\GSD1`)
  - **Suikoden II**: `d:\Appz\Suisource\GSD2` (`d:\Appz\Suisource\GSD2\GSD2`)
  - **Shared / Engine Core**: `d:\Appz\Suisource\GSDShare` (`d:\Appz\Suisource\GSDShare\GSDShare`)

## Logging & Diagnostics
- **Game & BepInEx Logs**: The active log file is located at `d:\SteamLibrary\steamapps\common\Suikoden I and II HD Remaster\BepInEx\LogOutput.log`. Check this log directly for runtime diagnostics, text message IDs, character slot IDs, and errors.

## Map & Asset Patching Pattern (`MACHICON.EventInit`)
- **Standard Pattern for Map / `<map>.json` Asset Modifications**: Follow the proven pattern established in `SajahShopUnlockPatch.cs` (and `TenzanPassEncounterPatch.cs`).
  - Hook `[HarmonyPatch(typeof(MACHICON), "EventInit")]` as a `[HarmonyPostfix]`.
  - Upon map transition, `EVENTCON __result` holds `__result.mdat` (`MACHIDAT`), which is the deserialized object of the map asset (e.g., `vj17.json`, `va11.json`).
  - Modify `__result.mdat` directly in memory (e.g., `eventdata.mapeventdat`, `eventobj`, `eventdat.eventForm` script byte arrays, `battle_dat`, `monster_party`, etc.).
  - This acts as an in-memory **byte-patching** mechanism for map asset JSON files, eliminating the need for manual UABEA bundle extraction/repacking and making changes immune to official game updates.
