---
name: syncfusion-angular-license
description: Use this skill when the user asks about Syncfusion Angular licensing, license keys, license registration, license validation errors, trial licenses, or license troubleshooting. This skill provides comprehensive guidance on generating, registering, and managing Syncfusion license keys for Angular applications, including edition-based and platform-based licensing models, registration methods, CI/CD integration, and resolving common licensing errors.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Licensing"
---

# Syncfusion Angular Licensing

This skill guides you through Syncfusion Angular licensing requirements, license key generation, registration methods, and troubleshooting validation errors.

## Table of Contents

- [Licensing Overview](#licensing-overview)
- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
- [Quick Start](#quick-start)
- [Common Registration Methods](#common-registration-methods)

## Licensing Overview

Syncfusion license key validation was introduced in the 2022 Volume 1 release (v20.1.0.47) for Essential JS2 platforms. All Angular applications referencing Syncfusion packages from npm, CDN, or build must register a valid license key to avoid validation warnings.

### Key Licensing Details

**License Key vs Unlock Key:**
- **License Key:** String registered in application code to validate Syncfusion package usage
- **Unlock Key:** Used only during Syncfusion installer process
- **⚠️ Important:** License key is NOT the same as installer unlock key

**Core Requirements:**
- License key validation introduced in v20.1.0.47+ (2022 Volume 1)
- License keys are **version and platform/edition specific**
- Validation occurs **offline** (no internet required during runtime)
- Required when using npm packages or trial installers
- Not required when using licensed installers

**License Types:**
- **Trial license:** 30-day evaluation period, full functionality, generates trial key, displays warning after expiration
- **Community license:** Free for qualifying individuals/organizations (<$1M USD revenue), same functionality as paid license, annual renewal required
- **Paid license:** Commercial license for enterprise use, perpetual or subscription-based, technical support included

**Edition-Based vs Platform-Based:**
- **v31.1.17+ (Edition-based):** UI Edition, Document SDK, PDF Viewer SDK, DOCX Editor SDK, Spreadsheet Editor SDK, Enterprise Edition (all editions combined)
- **v30.x.x and earlier (Platform-based):** Angular, React, Vue, JavaScript, Blazor, etc.

**Build Server Scenarios:**
- **Using npm packages:** License key required - register using `registerLicense()` or NPX command
- **Using trial installer:** License key required - trial warnings appear after 30 days
- **Using licensed installer:** License key NOT required - embedded license validation included

**Offline Validation:**
- No internet connection required during application runtime
- License validated locally against package metadata at startup
- Works in air-gapped environments and offline development
- No external API calls or performance impact

## Documentation and Navigation Guide

### Generating License Keys
📄 **Read:** [references/license-generation.md](references/license-generation.md)
- **Edition-based licensing (v31.1.17+):** UI Edition, Document SDK, PDF Viewer SDK, DOCX Editor SDK, Spreadsheet Editor SDK, Enterprise Edition
- **Platform-based licensing (v30.x.x and earlier):** Angular, JavaScript, React, etc.
- Generating keys from License & Downloads page
- Claim License Key page usage
- Version and platform specific license key

### Registering License Keys
📄 **Read:** [references/license-registration.md](references/license-registration.md)
- Direct registration in main.ts with `registerLicense()`
- NPX command registration: `npx syncfusion-license activate`
- License file method: `syncfusion-license.txt`
- Environment variable method: `SYNCFUSION_LICENSE`
- CI/CD integration: GitHub Actions, Azure Pipelines
- Active license, active trial, expired license scenarios

### Troubleshooting License Errors
📄 **Read:** [references/licensing-errors.md](references/licensing-errors.md)
- License key not registered error
- Invalid key error
- Trial expired error (30 days)
- Platform mismatch error
- Version mismatch error
- NPX command validation errors

## Quick Start

### 1. Generate License Key

Visit [License & Downloads](https://www.syncfusion.com/account/downloads) page:

**For v31.1.17+ (Edition-based):**
- Select version 31.x.x or higher
- Select required editions: UI Edition, Document SDK, PDF Viewer SDK, DOCX Editor SDK, Spreadsheet Editor SDK
- **Recommended:** Select all 5 editions for Enterprise Edition key
- Click "Get License Key"

**For v30.x.x and earlier (Platform-based):**
- Select version 30.x.x or earlier
- Select platforms: Angular, JavaScript, etc.
- Click "Get License Key"

### 2. Register License Key in Application

```typescript
// src/main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { registerLicense } from '@syncfusion/ej2-base';
import { AppComponent } from './app/app.component';

// Register Syncfusion license key
registerLicense('YOUR_LICENSE_KEY_HERE');

bootstrapApplication(AppComponent);
```

> **Note:** The `@syncfusion/ej2-base` package is a dependency for all Syncfusion components and will be automatically installed when you install any Syncfusion Angular package. You don't need to explicitly add it to your `package.json` file.

## Common Registration Methods

### Direct Registration (Recommended for Simple Apps)

```typescript
// src/main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { registerLicense } from '@syncfusion/ej2-base';
import { AppComponent } from './app/app.component';

registerLicense('Replace your generated license key here');

bootstrapApplication(AppComponent);
```

### Environment Variable Registration

```typescript
// src/main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { registerLicense } from '@syncfusion/ej2-base';
import { AppComponent } from './app/app.component';
import { environment } from './environments/environment';

// Use environment variable for license key
if (environment.syncfusionLicense) {
  registerLicense(environment.syncfusionLicense);
}

bootstrapApplication(AppComponent);
```

```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  syncfusionLicense: 'your_license_key_here'
};
```

### NPX Command Registration (Build Servers)

```bash
# Create syncfusion-license.txt in project root
echo "YOUR_LICENSE_KEY" > syncfusion-license.txt

# Activate license
npx syncfusion-license activate

# Clear cache after activation
rm -rf node_modules/.cache
```

### GitHub Actions CI/CD

```yaml
# .github/workflows/build.yml
steps:
  - name: Install dependencies
    run: npm install

  - name: Activate Syncfusion License
    run: npx syncfusion-license activate
    env:
      SYNCFUSION_LICENSE: ${{ secrets.SYNCFUSION_LICENSE }}
```

### Azure Pipelines CI/CD

```yaml
# azure-pipelines.yml
steps:
  - script: npm install
    displayName: 'Install dependencies'

  - script: npx syncfusion-license activate
    displayName: 'Activate Syncfusion License'
    env:
      SYNCFUSION_LICENSE: $(SYNCFUSION_LICENSE)
```

