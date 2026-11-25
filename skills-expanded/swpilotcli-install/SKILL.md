# swpilotcli-install

Installs or uninstalls the SwpilotCLI SolidWorks add-in on the user's machine.

## What it does

**Install mode** (default):
1. Reads the Windows registry to find installed SolidWorks version(s)
2. Locates `SolidWorks.Interop.sldworks.dll` from the user's SolidWorks installation
3. Builds `SwpilotCLIAddin.dll` using the user's local Interop DLL
4. Prints instructions for the user to run `Manage.bat` as Administrator to register the DLL

**Uninstall mode**:
- Prints instructions to run `Manage.bat` as Administrator to unregister

## Usage

```bash
# Install
dotnet run --project SolidWorksConsole/swpilotcli-install/SwpilotInstall.csproj

# Uninstall
dotnet run --project SolidWorksConsole/swpilotcli-install/SwpilotInstall.csproj -- uninstall
```

## Notes

- SolidWorks must be **closed** when building, otherwise the DLL will be locked
- DLL registration requires Administrator privileges — the tool prints instructions for this step
- `src/` contains all source files needed to build `SwpilotCLIAddin.dll`
- `Manage.bat` handles register/unregister/reinstall via regasm
