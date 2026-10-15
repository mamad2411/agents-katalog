---
name: syncfusion-winforms-common
description: Comprehensive guide for implementing Syncfusion Essential Studio Windows Forms (WinForms) controls in desktop applications. Use this skill when working with Syncfusion WinForms components or Essential Studio WinForms. Covers WinForms installation, localization, high DPI support, and .NET Core compatibility. Helps with adding controls, registering license keys, and troubleshooting WinForms component issues.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Windows Forms Components

Comprehensive guide for implementing Syncfusion® Essential Studio® Windows Forms (WinForms) controls in desktop applications. This skill covers everything from initial setup and installation to localization and .NET compatibility.

## When to Use This Skill

Use this skill when you need to:
- **Add Syncfusion WinForms controls** to a Windows Forms application
- **Register and manage license keys** for WinForms applications
- **Install or upgrade** Syncfusion WinForms via installer or NuGet
- **Set up .NET Core / .NET 5-9** projects with Syncfusion WinForms controls
- **Enable High DPI support** for Syncfusion WinForms controls
- **Localize** Syncfusion WinForms controls for different cultures
- **Troubleshoot** installation, licensing, or runtime errors

## Library Overview

Syncfusion® Essential Studio® for Windows Forms provides a comprehensive suite of UI controls for building rich Windows desktop applications, including grids, charts, schedulers, editors, navigation, layout, and input controls. All controls are designed for WinForms applications and support .NET Framework 4.6.2+ and .NET 6.0–9.0.

---

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Adding controls via Designer (Toolbox drag-drop)
- Adding controls via Code (C# / VB)
- Using Project Templates and Item Templates
- Assembly references required for controls
- Control dependency lookup (assembly and NuGet per control)

### Localization
📄 **Read:** [references/localization.md](references/localization.md)
- Using `ILocalizationProvider` interface
- Using Satellite Assemblies for multi-language support
- Localizing with `.resx` files
- Changing application culture at runtime
- Editing default culture strings

### High DPI Support
📄 **Read:** [references/high-dpi-support.md](references/high-dpi-support.md)
- DPI awareness overview (DPI-aware vs non-DPI-aware apps)
- DPI compatibility test matrix
- Enabling DPI awareness via `app.manifest`
- `AutoScaleDimensions` and `AutoScaleMode` setup
- Enabling `DpiAware` property for Grid controls
- Auto-switching images by DPI scaling with `ImageListAdv`

### System Requirements
📄 **Read:** [references/system-requirements.md](references/system-requirements.md)
- Supported Windows OS versions
- Hardware requirements (processor, RAM, disk)
- Supported Visual Studio versions
- Supported .NET Framework and .NET versions

### .NET Compatibility
📄 **Read:** [references/dotnet-compatibility.md](references/dotnet-compatibility.md)
- Creating WinForms apps with .NET Core / .NET 5-9
- Adding Syncfusion controls in .NET Core projects (assembly / NuGet)
- .NET Framework and .NET Core version compatibility matrix
- Version-specific .NET support per Syncfusion release

### Upgrading
📄 **Read:** [references/upgrading.md](references/upgrading.md)
- Upgrading via Control Panel / website installer
- Upgrading via Visual Studio Extensions
- Upgrading NuGet packages via Package Manager UI
- Upgrading NuGet packages via Package Manager Console
- Upgrading NuGet packages via .NET CLI
- Upgrading from trial to licensed version

### Installation
📄 **Read:** [references/installation.md](references/installation.md)
- Downloading the offline installer (trial and licensed)
- Installing with the UI wizard (step-by-step)
- Silent/command-line installation and uninstallation
- Installing NuGet packages via Package Manager UI
- Installing NuGet packages via .NET CLI
- Installing NuGet packages via Package Manager Console
- Common installation errors and solutions

---

## Quick Start

### 1. Install via NuGet

```powershell
# Package Manager Console
Install-Package Syncfusion.Shared.Base

# .NET CLI
dotnet add package Syncfusion.Shared.Base
```

### 2. Register License Key

Register the license before any Syncfusion control is initialized:

```csharp
// Program.cs — in static void Main(), before Application.Run()
static void Main()
{
    Syncfusion.Licensing.SyncfusionLicenseProvider.RegisterLicense("YOUR LICENSE KEY");

    Application.EnableVisualStyles();
    Application.SetCompatibleTextRenderingDefault(false);
    Application.Run(new Form1());
}
```

### 3. Add a Control via Code

```csharp
using Syncfusion.Windows.Forms.Tools;

// Create and configure the control
TextBoxExt textBox = new TextBoxExt();
textBox.Location = new System.Drawing.Point(100, 100);
textBox.Size = new System.Drawing.Size(200, 25);

// Add to form
this.Controls.Add(textBox);
```

---

## Common Patterns

### Enable High DPI

In `app.manifest`:
```xml
<application xmlns="urn:schemas-microsoft-com:asm.v3">
  <windowsSettings>
    <dpiAware xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true</dpiAware>
  </windowsSettings>
</application>
```

In code (for Grid controls):
```csharp
gridControl1.DpiAware = true;
```

### Localize Controls at Runtime

```csharp
// Set culture before InitializeComponent()
Thread.CurrentThread.CurrentCulture = new System.Globalization.CultureInfo("de-DE");
Thread.CurrentThread.CurrentUICulture = new System.Globalization.CultureInfo("de-DE");
```

---

## Key Assemblies

| Assembly | Controls Covered |
|---|---|
| `Syncfusion.Shared.Base` | ButtonAdv, most shared controls |
| `Syncfusion.Tools.Windows` | ComboBoxAdv, DockingManager, TabControlAdv, and most Tools controls |
| `Syncfusion.Grid.Windows` | GridControl, GridGroupingControl |
| `Syncfusion.Chart.Windows` | Chart control |
| `Syncfusion.SfDataGrid.WinForms` | SfDataGrid |

> For per-control dependency lookup, read [references/getting-started.md](references/getting-started.md).

---

## Common Use Cases

- **Business forms:** Add input controls, editors, and validation with Syncfusion WinForms tools
- **Data-heavy UIs:** Use GridControl or SfDataGrid with high DPI support
- **Multi-language apps:** Use `.resx` files or `ILocalizationProvider` for localization
- **CI/CD pipelines:** Validate license key automatically using `LicenseKeyValidator`
