---
name: edt-add-project
description: Добавить 1С проект в EDT workspace на CT107. Три режима: project (готовый EDT проект), xml (из XML исходников), dt (из .dt файла с автоимпортом расширений). Используй когда нужно зарегистрировать проект в EDT для работы через edt-mcp.
argument-hint: [source-path] [project-name]
allowed-tools:
  - Bash
  - AskUserQuestion
---

# /edt-add-project — Add project to EDT workspace (CT107)

Script: `YOUR_KIT_ROOT\.claude\skills\1c-project-init\scripts\edt-import.ps1`

## Step 1 — Determine mode and collect params

Ask user (AskUserQuestion) if not provided in args:

1. **Mode**: `project` | `xml` | `dt`
2. **Source**: path to EDT project dir on CT107 | XML src dir on CT107 | .dt file (local or CT107)
3. **ProjectName** (xml/dt only): Latin name, no spaces/Cyrillic
4. **PlatformVersion** (default 8.3.24): `8.3.24` | `8.3.25`
5. **WithExtensions** (dt only): import extensions from IB? yes/no

## Step 2 — Pre-flight checks

### mode=project
```bash
ssh root@YOUR_EDT_SERVER "test -f '<Source>/.project' && cat '<Source>/.project' | grep '<name>'"
```
- Verify dir name matches `<name>` in `.project` (Latin only)
- If Cyrillic name: warn user, suggest renaming dir or fixing .project

### mode=xml
```bash
ssh root@YOUR_EDT_SERVER "ls '<Source>/' | head -5"
```
- Verify src dir exists and has 1C XML files

### mode=dt
```bash
ssh root@YOUR_EDT_SERVER "ls -lh '<Source>'"  # if on CT107
# OR check local path exists
```
- If local .dt: warn that scp will run (may take time for large files)
- Suggest DB name derived from ProjectName

## Step 3 — Run script

```powershell
powershell.exe -NoProfile -File "YOUR_KIT_ROOT\.claude\skills\1c-project-init\scripts\edt-import.ps1" `
  -Mode <mode> `
  -Source "<source>" `
  -ProjectName "<name>" `
  -PlatformVersion "<version>" `
  [-WithExtensions] `
  [-BaseProjectName "<base>"]
```

**Note:** EDT will be stopped during import (~30s downtime). edt-mcp will be unavailable until start completes.

## Step 4 — Verify

Wait 2-3 minutes after start, then:
```
edt-mcp list_projects
```
Expected: new project with state `ready`.

If state is `not_available` after 5 min → check:
```bash
ssh root@YOUR_EDT_SERVER "tail -30 /opt/edt-workspace/.metadata/.log | grep -i 'error\|exception\|PMF'"
```

## Step 5 — Report

Tell user:
- Project name and state in EDT
- List of imported extensions (if WithExtensions)
- Next step: connect to infobase in EDT Run configurations (for debugging)

## Mode reference

| Mode | Source | Creates |
|------|--------|---------|
| `project` | Existing EDT project dir on CT107 (has `.project`) | Registers in workspace metadata |
| `xml` | 1C XML src dir on CT107 | New EDT project from XML via `1cedtcli --configuration-files` |
| `dt` | `.dt` file | Restores IB → exports XML → imports config + extensions |

## Key facts

- EDT workspace: `/opt/edt-workspace`
- 1cedtcli: `/opt/edt-app/data/1cedtcli`
- Docker containers: `onec-server-24` (8.3.24, port 1641), `onec-server-25` (8.3.25, port 1541)
- ibcmd inside Docker: `/opt/1cv8/x86_64/8.3.24.XXXX/ibcmd`
- PG inside Docker: host=`onec-postgres`, user=`onec`, pwd=`YOUR_PG_PASSWORD`
- DT files on CT107: `/mnt/data/`
- Deploy dir: `/mnt/data/deploy/`

## Gotchas

- **Cyrillic dir name** → 1cedtcli arg-parse failure. Always use Latin dir names.
- **Missing DT-INF/PROJECT.PMF** → crashes ALL projects in workspace. Script creates it automatically.
- **1cedtcli needs EDT stopped** → script stops/starts EDT automatically.
- **Extension names from ibcmd** may be Cyrillic → script strips non-Latin chars for dir name.
- **`ibcmd extension list`** output format: one extension name per line (skip header lines).
- **Large configs**: indexing after import takes 3-10 min depending on config size.
