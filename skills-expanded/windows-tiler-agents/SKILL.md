# Project conventions

- Use C# for the tiling engine and helper. Keep Explorer-only integration in the native bridge.
- Add inline documentation to every class, interface, record, struct, method, constructor, native hook, and script function. Explain non-obvious Win32 behavior near the relevant code.
- Keep window operations scoped to explicit taskbar-group handles. Do not select applications by process name.
- Run `scripts/test.ps1 -Windows` for desktop changes. The harness must manipulate only its own test windows.
- Native menu tests run outside Explorer. Do not describe them as live taskbar integration verification.
- Build MSI packages with `scripts/build-msi.ps1`; keep the installer UpgradeCode and component GUIDs stable across versions.
- Test installer lifecycle with `scripts/test-msi.ps1` only on an account without an existing Windows Tiler MSI installation. Do not suppress unrelated MSI validation failures.
