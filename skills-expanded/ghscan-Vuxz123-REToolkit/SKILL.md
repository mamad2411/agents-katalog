# Install And Use GhidraMCP With REToolkit

This prompt is for an AI agent or human setting up REToolkit for MCP-first
Ghidra reverse engineering.

Example user request for an agent:

```text
cài đặt với prompts trên và chạy flows cho thằng apk này {path}
```

Before starting, load the repo-local skills from `skills/`. Use them directly
if the agent runtime supports repo-local skills; import or install them into
the agent's normal skill directory only if that runtime requires installed
skills:

```text
skills/retoolkit-install
skills/retoolkit-flow
skills/retoolkit-mcp-analysis
```

## Install REToolkit Skills

These REToolkit skills are plain Markdown instruction folders. Any agent can
use them by reading the repo-local `SKILL.md` files or importing the folders
into its own skill/instruction mechanism.

For non-Codex agents, do not use `$CODEX_HOME`; point the agent at these
folders, paste the relevant `SKILL.md` content into its instruction context, or
copy the folders into that agent's equivalent skill directory:

```text
skills/retoolkit-install
skills/retoolkit-flow
skills/retoolkit-mcp-analysis
```

For Codex, skip this step when the runtime can read repo-local skills directly.
If the runtime requires installed Codex skills, install the REToolkit skill
folders from the REToolkit root. Codex reads installed skills from
`$CODEX_HOME/skills` or `~/.codex/skills` when `CODEX_HOME` is not set:

```powershell
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$skillDest = Join-Path $codexHome "skills"
New-Item -ItemType Directory -Path $skillDest -Force | Out-Null

foreach ($name in @("retoolkit-install", "retoolkit-flow", "retoolkit-mcp-analysis")) {
    $src = Join-Path (Get-Location) "skills\$name"
    $dst = Join-Path $skillDest $name
    if (Test-Path -LiteralPath $dst) {
        Write-Host "Skill already installed: $dst"
    }
    else {
        Copy-Item -LiteralPath $src -Destination $dst -Recurse
        Write-Host "Installed skill: $dst"
    }
}
```

Restart Codex to pick up newly installed skills.

## Goal

Use `bethington/ghidra-mcp` as the analysis/query backend. REToolkit prepares
Unity IL2CPP projects and launches the MCP bridge with:

```powershell
.\re.ps1 mcp
```

The live Ghidra or PyGhidra GUI instance provides analysis capabilities through
the GhidraMCP plugin. Agent queries should go through MCP tools, not ghidra-cli
or a separate headless query bridge.

## Install

From the REToolkit root:

```powershell
.\install-re-toolkit.ps1 -All
```

`-All` runs the recommended full install order: runtime, .NET Runtime,
Ghidra, Il2CppDumper, GhidraMCP, then AssetRipper.

Use individual flags only when repairing or installing a specific component:

```powershell
.\install-re-toolkit.ps1 -InstallRuntime
.\install-re-toolkit.ps1 -InstallDotNetRuntime
.\install-re-toolkit.ps1 -InstallGhidra
.\install-re-toolkit.ps1 -InstallIl2CppDumper
.\install-re-toolkit.ps1 -InstallGhidraMcp
.\install-re-toolkit.ps1 -InstallAssetRipper
```

`-InstallRuntime` installs JDK 21 plus a toolkit-local Python 3.12 under
`runtime/python/python-3.12`. REToolkit/PyGhidra should use this local runtime
instead of any global Python 3.14 on the machine. It also prepares
`runtime/python/pyghidra-venv` for PyGhidra launches.

`-InstallDotNetRuntime` installs Microsoft .NET Runtime 8 for Il2CppDumper's
`net8.0` package. If Microsoft.NETCore.App 6.x is already installed,
`-InstallIl2CppDumper` can use Il2CppDumper's `net6.0` package instead.

`-InstallIl2CppDumper` replaces `tools\Il2CppDumper\ghidra.py` and
`tools\Il2CppDumper\ghidra_with_struct.py` with toolkit-maintained Python 3 /
PyGhidra-compatible templates. It also registers `tools\Il2CppDumper` as a
Ghidra Script Bundle. If Ghidra has never created its CodeBrowser tool config,
REToolkit seeds it from:

```text
templates/Ghidra/_code_browser.tcd
```

If Script Manager does not show `ghidra.py` or `ghidra_with_struct.py` after
the wrapper/installer runs, fully close all Ghidra/PyGhidra windows and reopen
the GUI so CodeBrowser reloads its Script Bundle config.

`-InstallGhidraMcp` downloads the latest release assets from:

```text
https://github.com/bethington/ghidra-mcp
```

It saves these files under `tools/ghidra-mcp`:

- `GhidraMCP-<version>.zip`
- `ghidra_mcp_bridge-<version>-py3-none-any.whl` (ships its own dependencies)

It also creates `tools/ghidra-mcp/.venv` and `pip install`s the wheel into
that local environment. The resulting `bridge-mcp-ghidra` console script is
the AI-client-side bridge, not the GUI plugin.

When a local Ghidra install is present, the installer extracts and installs the
extension under:

```text
%APPDATA%\ghidra\ghidra_<version>_PUBLIC\Extensions\GhidraMCP
```

## Ghidra GUI Setup

Start Ghidra/PyGhidra with a project name when possible:

```powershell
.\re.ps1 pyghidra-gui FoodHunt
# or
.\re.ps1 ghidra-gui FoodHunt
```

Passing `FoodHunt` updates Ghidra's recent/default project preferences before
launch. If Ghidra has never created its `preferences` file, REToolkit seeds it
from:

```text
templates/Ghidra/preferences
```

If the GhidraMCP extension is not visible, install the release extension ZIP:

```text
File > Install Extensions > Add
```

Select `tools/ghidra-mcp/GhidraMCP-<version>.zip`, then restart Ghidra.

Open the target project/program in a CodeBrowser, then enable the plugin:

```text
File > Configure > Configure All Plugins > GhidraMCP
```

Optional port settings:

```text
CodeBrowser > Edit > Tool Options > GhidraMCP HTTP Server
```

Start the server:

```text
Tools > GhidraMCP > Start MCP Server
```

## AI Client Config

Codex TOML fragment:

```toml
[mcp_servers.ghidra]
command = "powershell.exe"
args = [
  "-NoProfile",
  "-ExecutionPolicy", "Bypass",
  "-File", "C:\\Users\\DPC00176\\REToolkit\\re.ps1",
  "mcp"
]

[mcp_servers.ghidra.env]
RETOOLKIT_ROOT = "C:\\Users\\DPC00176\\REToolkit"
```

OpenCode JSON fragment:

```json
{
  "mcpServers": {
    "ghidra": {
      "command": "C:\\Users\\DPC00176\\REToolkit\\re.ps1",
      "args": ["mcp"],
      "type": "stdio",
      "env": {
        "RETOOLKIT_ROOT": "C:\\Users\\DPC00176\\REToolkit"
      }
    }
  }
}
```

## Agent Workflow

Prepare the project with REToolkit:

```powershell
.\re.ps1 flow FoodHunt "D:\Path\To\FoodHunt.apk"
```

`flow` scans/extracts the build, runs Il2CppDumper, imports the binary into
Ghidra without analysis, generates notes, sets the default Ghidra project, and
opens PyGhidra. It intentionally does not run long headless Auto Analysis and
does not auto-apply `ghidra.py`.

Important for agents: `flow`, `open`, and `pyghidra-gui` start PyGhidra
detached by default, so the wrapper returns after launch handoff while the GUI
keeps running. PyGhidra stdout/stderr logs are written under
`logs/pyghidra-gui-*`. Use `--console` only when foreground logs are
intentional.

Finish in the GUI:

1. Open the imported program.
2. Run Auto Analysis.
3. Run `ghidra.py` or `ghidra_with_struct.py` from the `tools\Il2CppDumper`
   Script Bundle if symbol import is needed.
4. When prompted, choose
   `workspaces\FoodHunt\02_Il2CppDumperOutput\script.json`.
5. Start `Tools > GhidraMCP > Start MCP Server`.

Then in the MCP client:

```text
list_instances
connect_instance FoodHunt
list_tool_groups
load_tool_group function
load_tool_group listing
```

Use MCP tools for function listing, decompilation, xrefs, strings, symbols,
comments, types, script execution, and batch operations.

## Workspace Archives

Use `.re` archives to move a prepared workspace between machines or toolkit
folders:

```powershell
.\re.ps1 export FoodHunt
.\re.ps1 import .\exports\FoodHunt.re
.\re.ps1 import .\exports\FoodHunt.re FoodHuntCopy
.\re.ps1 import .\exports\FoodHunt.re FoodHunt --force
```

The `.re` file is a ZIP archive with a REToolkit extension. Import restores the
workspace under `workspaces/` and rebases absolute paths in `project.re.json` to
the current toolkit folder.

## REToolkit Commands

Use these local commands to prepare and inspect workspace state:

```powershell
.\re.ps1 doctor
.\re.ps1 init <GameName>
.\re.ps1 add <GameName> <apk-or-xapk-or-aab-or-zip>
.\re.ps1 scan <GameName> <ExtractedPath>
.\re.ps1 dump <GameName>
.\re.ps1 import <GameName>
.\re.ps1 export <GameName> [OutFile.re]
.\re.ps1 import <Archive.re> [GameName] [--force]
.\re.ps1 flow <GameName> <apk-or-ExtractedPath>
.\re.ps1 open <GameName>
.\re.ps1 path <GameName>
.\re.ps1 status <GameName>
.\re.ps1 candidates <GameName>
.\re.ps1 context <GameName>
.\re.ps1 notes <GameName>
.\re.ps1 ghidra-gui [GameName]
.\re.ps1 pyghidra-gui [GameName]
.\re.ps1 assetripper
.\re.ps1 mcp
```

`import <GameName>` means Ghidra import. `import <Archive.re>` means workspace
archive import.

Legacy query aliases `summary`, `strings`, `functions`, and `stats` print MCP
guidance only. Do project queries through the connected GhidraMCP tools.

## Troubleshooting

- GhidraMCP menu is missing: install `tools/ghidra-mcp/GhidraMCP-<version>.zip`
  with `File > Install Extensions > Add`, restart Ghidra, then enable the
  plugin from `File > Configure > Configure All Plugins > GhidraMCP`.
- Script Manager does not show `ghidra.py`: fully close all Ghidra/PyGhidra
  windows and reopen the GUI.
- MCP cannot see the project: open the correct project/program in CodeBrowser
  and start `Tools > GhidraMCP > Start MCP Server`.
- Project lock error: close other Ghidra/headless processes for that project,
  or use MCP from the already-open GUI.
- Il2CppDumper cannot find .NET: run
  `.\install-re-toolkit.ps1 -InstallDotNetRuntime`; the installer prefers
  Il2CppDumper `net8.0` and falls back to `net6.0` only when
  Microsoft.NETCore.App 6.x already exists.

## Safety

- Do not run destructive write operations unless the user explicitly confirms
  the target project/program.
- Avoid running headless analysis while the same project is open in another
  Ghidra process.
- Prefer the already-open GUI plus GhidraMCP for interactive analysis.
