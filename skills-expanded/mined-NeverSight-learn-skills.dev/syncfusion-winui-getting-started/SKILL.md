---
name: syncfusion-winui-getting-started
description: Comprehensive guide for setting up Syncfusion WinUI components, including license registration, NuGet package installation, system requirements verification, and troubleshooting. Use this skill when users need help with Syncfusion licensing, installation, WinUI component configuration, theme setup, or resolving installation errors.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinUI Setup and Licensing

## When to Use This Skill

Use this skill when:
- Users need to install Syncfusion WinUI components
- License registration or validation is required
- System requirements must be verified
- Installation errors occur
- Configuration (themes, localization, RTL) is needed
- Troubleshooting setup or licensing issues
- Upgrading from trial to purchased license
- Setting up in CI/CD environments

## Setup Overview

Syncfusion WinUI components require three core setup phases:

1. **Prerequisites & System Check** - Verify OS, .NET version, and compatibility
2. **License Registration** - Register and validate Syncfusion license
3. **Package Installation & Configuration** - Install via NuGet and configure features

Each phase builds on the previous, and skipping any step can cause downstream issues.

---

## Documentation and Navigation Guide

### System Requirements & Prerequisites
📄 **Read:** [references/system-requirements.md](references/system-requirements.md)
- WinUI and Windows OS compatibility
- .NET version requirements
- Visual Studio prerequisites
- Hardware and browser requirements
- Target framework compatibility

### Licensing Overview
📄 **Read:** [references/licensing-overview.md](references/licensing-overview.md)
- License types and options
- Where to obtain license keys
- License registration process
- Community license eligibility
- Trial vs. purchased license differences

### Installation and Package Setup
📄 **Read:** [references/installation-setup.md](references/installation-setup.md)
- NuGet package installation steps
- Namespace registration
- Online installer configuration
- Offline installer download and setup
- Verifying successful installation

### License Validation and Activation
📄 **Read:** [references/license-validation.md](references/license-validation.md)
- License key registration in code
- Offline license validation
- Internet connection requirements
- Common license errors and solutions
- Trial to purchased upgrade process

### Theming
📄 **Read:** [references/theming.md](references/theming.md)
- Available themes (Fluent, Material, WinUI)
- Setting and switching themes
- System theme detection
- Custom theme creation
- Theme persistence

### Localization and Language Support
📄 **Read:** [references/localization.md](references/localization.md)
- Supported languages and culture codes
- Setting application language (WinUI-specific methods)
- Localizing with .resw files (resource-based approach)
- Localizing without .resw files (ILocalizationProvider and programmatic approach)
- Custom resource files and editing default strings
- RTL (Right-to-Left) language support
- Dynamic language switching

### Accessibility and Compact Sizing
📄 **Read:** [references/configuration-basics.md](references/configuration-basics.md)
- Screen reader support
- Automation properties and ARIA
- Keyboard navigation
- High contrast mode
- Compact sizing options

### Troubleshooting Installation
📄 **Read:** [references/troubleshooting-installation.md](references/troubleshooting-installation.md)
- Installation error solutions
- NuGet restore and package issues
- License validation troubleshooting
- Configuration problem fixes
- Getting support and debugging

### Upgrades and Patches
📄 **Read:** [references/upgrade-and-patches.md](references/upgrade-and-patches.md)
- Upgrading from trial to purchased license
- Applying service packs and patches
- Version upgrade considerations
- Maintaining existing installations
- Rollback procedures

---

## Quick Start Example

```csharp
// 1. Register License (in App.xaml.cs or MainWindow.xaml.cs)
using Syncfusion.Licensing;

public partial class App : Application
{
    public App()
    {
        // Register your license key before using any Syncfusion component
        SyncfusionLicenseProvider.RegisterLicense("YOUR_LICENSE_KEY");
        this.InitializeComponent();
    }
}

// 2. Add namespaces in XAML
xmlns:syncfusion="using:Syncfusion.UI.Xaml.Controls"

// 3. Use components
<syncfusion:SfButton Content="Click Me" />
```

---

## Common Setup Patterns

### Pattern 1: New Project Setup
1. Create WinUI project in Visual Studio
2. Install Syncfusion NuGet packages: `Install-Package Syncfusion.WinUI`
3. Register license in App.xaml.cs
4. Add namespace to XAML
5. Start using components

### Pattern 2: Trial to Production Upgrade
1. Verify current trial license in code
2. Obtain purchased license key
3. Update license registration with new key
4. Test all components work without trial limitations
5. Deploy to production

### Pattern 3: CI/CD Environment Setup
1. Set up offline license validation in build environment
2. Configure license in environment variables or secure vault
3. Reference license during build process
4. Ensure all dependencies are pre-cached
5. Test build in isolated environment

### Pattern 4: Feature Configuration
1. Install base Syncfusion package
2. Configure required theme (FluentLight, FluentDark, MaterialLight, etc.)
3. Add localization files (.resw approach) OR implement ILocalizationProvider (programmatic approach)
4. Enable RTL if targeting Arabic/Hebrew users
5. Enable accessibility features for compliance

### Pattern 5: Localization Setup
**Option A - .resw Files Approach:**
1. Download default resource files from Syncfusion GitHub
2. Create Resources/{language}/ folders in project
3. Copy .resw files for target languages
4. Set `ApplicationLanguages.PrimaryLanguageOverride` in code
5. Test with target language

**Option B - Provider Approach:**
1. Create class implementing `ILocalizationProvider` interface
2. Implement `GetLocalizedString(LocalizationInfo)` method
3. Set `LocalizationProvider.Provider` before InitializeComponent()
4. Return custom strings for specific resource keys
5. Use `ResourceAssemblyName` for assembly-specific localization

---

## Key Requirements Checklist

Before installing Syncfusion WinUI components, verify:

- [ ] **OS:** Windows 10 version 1809+ or Windows 11
- [ ] **.NET Version:** .NET 5 or higher (typically .NET 6+)
- [ ] **Visual Studio:** VS 2019 v16.9+ or VS 2022
- [ ] **WinUI 3:** Latest stable version installed
- [ ] **License:** Valid license key obtained or trial active
- [ ] **NuGet:** Updated to latest version
- [ ] **Admin Rights:** Required for some installation scenarios
- [ ] **Internet:** Available for online package restore (or offline packages cached)

---

## Quick Decision Tree

**User needs to...**

- **Install Syncfusion?** → [Installation and Package Setup](references/installation-setup.md)
- **Register license?** → [Licensing Overview](references/licensing-overview.md) then [License Validation](references/license-validation.md)
- **Fix installation error?** → [Troubleshooting Installation](references/troubleshooting-installation.md)
- **Check if system is compatible?** → [System Requirements](references/system-requirements.md)
- **Set up themes?** → [Theming](references/theming.md)
- **Configure language/RTL?** → [Localization and Language Support](references/localization.md)
- **Localize with .resw files?** → [Localization and Language Support](references/localization.md) (.resw Files section)
- **Localize programmatically?** → [Localization and Language Support](references/localization.md) (Provider Method section)
- **Set accessibility features?** → [Accessibility and Compact Sizing](references/configuration-basics.md)
- **Upgrade trial to paid?** → [Upgrades and Patches](references/upgrade-and-patches.md)
- **Validate license in CI/CD?** → [License Validation](references/license-validation.md)
