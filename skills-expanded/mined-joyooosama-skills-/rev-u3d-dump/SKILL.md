---
name: rev-u3d-dump
description: Dump Unity IL2CPP symbols from iOS/Android builds. Extract method names, addresses, and type info from IL2CPP binaries and global-metadata.dat, then generate IDA/Ghidra import scripts.
---

# rev u3d dump

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- Repo: `https://github.com/roytu/Il2CppDumper` (branch: `v39`)
- Supports metadata v24鈥搗39
- Outputs `script.json` with function addresses 鈥?ready for IDA/Ghidra import
- Repo: `https://github.com/SamboyCoding/Cpp2IL`
- Supports metadata v39, but dummy DLLs lack `[Address]` attributes
- Useful for C# source reconstruction, not ideal for IDA import
- `DOTNET_ROLL_FORWARD=LatestMajor` allows running on .NET 9/10 even though the project targets .NET 6/8
- Exit code 134 is normal in non-interactive mode (caused by `Console.ReadKey()` at the end)

## Available sections

- rev-u3d-dump - Unity IL2CPP Symbol Dumper
- Overview
- Key Files in Unity Build
- Tool Selection
- Il2CppDumper (recommended for metadata v39+)
- Cpp2IL (alternative)
- Step-by-Step Workflow
- Step 1: Locate IL2CPP Files
- Unzip IPA
- Binary
- Metadata
- Unzip APK

