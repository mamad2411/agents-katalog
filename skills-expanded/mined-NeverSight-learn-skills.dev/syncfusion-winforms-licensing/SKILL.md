---
name: syncfusion-winforms-licensing
description: Comprehensive guide for implementing and managing Syncfusion Windows Forms licensing. Use this when troubleshooting license validation errors, generating or registering license keys, or configuring CI/CD license validation. This skill covers license key management, trial vs licensed versions, NuGet package licensing, and build server scenarios.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Windows Forms Licensing

This skill provides comprehensive guidance for implementing and managing Syncfusion licensing in Windows Forms applications, including license key generation, registration, troubleshooting, and CI/CD integration.

## When to Use This Skill

Use this skill immediately when you need to:

- **Implement licensing** in a Windows Forms application using Syncfusion components
- **Resolve license validation errors** or trial expiration messages
- **Generate license keys** for specific versions and platforms
- **Register license keys** in C# or VB.NET Windows Forms applications
- **Troubleshoot licensing issues** such as invalid keys, platform mismatches, or version mismatches
- **Configure CI/CD pipelines** with license validation (Azure Pipelines, GitHub Actions, Jenkins)
- **Understand licensing requirements** for NuGet packages, trial installers, or licensed installers
- **Upgrade from trial to licensed version** after purchasing
- **Handle build server licensing** scenarios

## Overview of Syncfusion Licensing

Starting with version 16.2.0.x, Syncfusion introduced a new licensing system that requires license key registration for:
- Applications using evaluation installers
- Applications referencing Syncfusion NuGet packages from nuget.org

**Key Points:**
- License keys are **version and platform specific**
- License keys are different from installer unlock keys
- Validation happens **offline** during application execution (no internet required)
- Licensed installer users do not need to register license keys
- Trial license keys expire after 30 days

## Documentation and Navigation Guide

### Understanding Licensing

📄 **Read:** [references/licensing-overview.md](references/licensing-overview.md)

When to read this reference:
- Understanding the licensing system introduced in version 16.2.0.x
- Learning the difference between unlock keys and license keys
- Determining when license registration is required
- Understanding build server scenarios (NuGet vs Trial vs Licensed installers)
- Learning about version and platform specificity

### Generating License Keys

📄 **Read:** [references/license-generation.md](references/license-generation.md)

When to read this reference:
- Generating license keys from License & Downloads section
- Generating license keys from Trial & Downloads section
- Using the Claim License Key feature
- Handling active license scenarios
- Handling active trial scenarios
- Dealing with expired licenses
- Starting a trial when no license exists

### Registering License Keys

📄 **Read:** [references/license-registration.md](references/license-registration.md)

When to read this reference:
- Implementing the RegisterLicense method in C# or VB.NET
- Registering keys in Main() method for C# applications
- Registering keys in Application.Designer.vb for VB.NET
- Registering keys in Program.vb for VB.NET
- Understanding Syncfusion.Licensing.dll reference requirements
- Learning about offline validation capabilities

### Troubleshooting Licensing Errors

📄 **Read:** [references/licensing-errors.md](references/licensing-errors.md)

When to read this reference:
- Resolving "License key not registered" errors
- Fixing "Invalid key" errors
- Handling "Trial expired" messages
- Resolving platform mismatch errors
- Fixing version mismatch errors
- Troubleshooting "Could not load Syncfusion.Licensing.dll" errors
- Configuring Copy Local settings
- Understanding legacy errors (v16.2.0 - v20.3.0)

### Common Questions and CI/CD Integration

📄 **Read:** [references/licensing-faqs.md](references/licensing-faqs.md)

When to read this reference:
- Implementing CI/CD license validation (Azure Pipelines, GitHub Actions, Jenkins)
- Using LicenseKeyValidator utility in build pipelines
- Understanding where to get license keys
- Checking if internet connection is required for validation
- Upgrading from trial to licensed version
- Registering Syncfusion account for NuGet.org users
- Understanding license key specificity

## Quick Start Example

Here's a complete example of registering a Syncfusion license key in a Windows Forms application:

### C# Example

```csharp
using System;
using System.Windows.Forms;
using Syncfusion.Licensing;

namespace MyWindowsFormsApp
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            // Register Syncfusion license key BEFORE any Syncfusion control is initiated
            SyncfusionLicenseProvider.RegisterLicense("YOUR_LICENSE_KEY_HERE");
            
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());
        }
    }
}
```

### VB.NET Example (Application.Designer.vb)

```vb
Namespace My
    Partial Friend Class MyApplication
        Public Sub New()
            MyBase.New(Global.Microsoft.VisualBasic.ApplicationServices.AuthenticationMode.Windows)
            
            ' Register Syncfusion License
            Syncfusion.Licensing.SyncfusionLicenseProvider.RegisterLicense("YOUR_LICENSE_KEY_HERE")
            
            Me.IsSingleInstance = False
            Me.EnableVisualStyles = True
            Me.SaveMySettingsOnExit = True
            Me.ShutdownStyle = Global.Microsoft.VisualBasic.ApplicationServices.ShutdownMode.AfterMainFormCloses
        End Sub
    End Class
End Namespace
```

## Common Patterns

### Pattern 1: License Key Registration Workflow

When implementing Syncfusion licensing:

1. **Generate** license key from Syncfusion account
2. **Add reference** to Syncfusion.Licensing.dll
3. **Register** license key at application entry point (before any Syncfusion control initialization)
4. **Verify** no license validation errors appear

### Pattern 2: Troubleshooting License Errors

When encountering license validation errors:

1. **Identify** the specific error message
2. **Verify** license key is for correct version and platform
3. **Check** registration location (must be before control initialization)
4. **Ensure** Syncfusion.Licensing.dll is referenced and Copy Local = True
5. **Regenerate** license key if needed

### Pattern 3: CI/CD License Validation

When implementing license validation in CI pipelines:

1. **Download** LicenseKeyValidator utility
2. **Configure** PowerShell script with platform, version, and license key
3. **Integrate** script execution in CI pipeline (Azure, GitHub Actions, Jenkins)
4. **Validate** license before deployment
5. **Handle** validation failures appropriately

### Pattern 4: Upgrading from Trial to Licensed

When purchasing a license after trial:

1. **Option A:** Uninstall trial, install licensed version from License & Downloads
2. **Option B:** (For NuGet users) Replace trial license key with paid license key
3. **Verify** license registration in application
4. **Test** to ensure no trial messages appear

## Key Concepts

### License Key Characteristics

- **Version-specific:** License key must match Syncfusion assembly version
- **Platform-specific:** Windows Forms keys only work for Windows Forms platform
- **Offline validation:** No internet connection required during runtime
- **String format:** License key is a string registered via RegisterLicense()

### Registration Requirements

| Assembly Source | License Registration Required? | Where to Get Key |
|----------------|-------------------------------|------------------|
| NuGet packages from nuget.org | ✅ Yes | License & Downloads / Trial & Downloads |
| Trial installer | ✅ Yes | Trial & Downloads |
| Licensed installer | ❌ No | Not applicable |

### Critical Registration Rules

1. **Timing:** Register license key BEFORE initializing any Syncfusion control
2. **Location:** 
   - C#: In `Main()` method before `Application.Run()`
   - VB.NET: In `Application.Designer.vb` constructor or `Program.vb`
3. **Dependencies:** Ensure `Syncfusion.Licensing.dll` is referenced with Copy Local = True
4. **Format:** Place license key string between double quotes

## Common Use Cases

### Use Case 1: First-Time Syncfusion License Setup

**Scenario:** Developer setting up Syncfusion in a new Windows Forms project using NuGet packages.

**Approach:**
1. Read [references/licensing-overview.md](references/licensing-overview.md) to understand requirements
2. Read [references/license-generation.md](references/license-generation.md) to generate key
3. Read [references/license-registration.md](references/license-registration.md) to implement registration
4. Test application to verify no license errors

### Use Case 2: Resolving License Validation Error

**Scenario:** Application shows "License key not registered" or "Invalid key" error.

**Approach:**
1. Read [references/licensing-errors.md](references/licensing-errors.md) to identify specific error
2. Verify license key version and platform match
3. Check registration code location and timing
4. Regenerate license key if needed
5. Verify Syncfusion.Licensing.dll reference

### Use Case 3: Build Server Configuration

**Scenario:** Setting up Syncfusion licensing for automated builds or CI/CD.

**Approach:**
1. Read [references/licensing-overview.md](references/licensing-overview.md) build server section
2. Determine if license registration is required based on assembly source
3. Read [references/licensing-faqs.md](references/licensing-faqs.md) CI/CD section for pipeline setup
4. Implement license validation in CI pipeline
5. Test build process

### Use Case 4: Trial to Licensed Upgrade

**Scenario:** Developer purchased license after using trial version.

**Approach:**
1. Read [references/licensing-faqs.md](references/licensing-faqs.md) upgrade section
2. Choose upgrade approach (reinstall or key replacement)
3. Generate new paid license key
4. Update registration code with new key
5. Verify trial message is removed

### Use Case 5: Version Upgrade

**Scenario:** Upgrading Syncfusion components to a new version.

**Approach:**
1. Generate new license key for target version from License & Downloads
2. Update NuGet packages or installer to new version
3. Replace old license key with new version-specific key
4. Test application to ensure compatibility
5. If errors occur, read [references/licensing-errors.md](references/licensing-errors.md)

## Additional Resources

- **Syncfusion Account:** https://www.syncfusion.com/account/manage-trials/downloads
- **License & Downloads:** https://www.syncfusion.com/account/downloads
- **Support:** https://support.syncfusion.com/

## Summary

This skill covers the complete lifecycle of Syncfusion Windows Forms licensing:
- Understanding licensing requirements and scenarios
- Generating license keys for specific versions and platforms
- Registering license keys in C# and VB.NET applications
- Troubleshooting common licensing errors
- Implementing CI/CD license validation
- Handling trial and licensed version transitions

Always start by reading the appropriate reference file based on your specific need (overview, generation, registration, errors, or FAQs).
