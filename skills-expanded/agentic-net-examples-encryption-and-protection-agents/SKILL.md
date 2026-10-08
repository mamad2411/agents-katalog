---
name: Aspose.Cells Encryption and Protection Agent
category: encryption-and-protection
product: Aspose.Cells for .NET
language: C#
parent: ../AGENTS.md
version: 3.0
last_reviewed: 2026-08-21
primary_intent: Encrypt Excel files and protect workbooks, worksheets, cells, VBA projects, and signatures in C#
primary_apis: [Worksheet.Protect, Worksheet.Unprotect, ProtectionType, WorkbookSettings, EncryptionType, WriteProtection]
related_categories: [../open-workbook/, ../save-workbook/, ../macro-project/, ../document-properties/]
---

# Encryption and Protection Agent Instructions

## Mission and security boundary

Create secure, accurate Aspose.Cells for .NET examples that clearly distinguish access control, workbook/worksheet protection, write protection, file encryption, and digital signatures. Follow [`../AGENTS.md`](../AGENTS.md).

These features are not interchangeable:

| Security goal | Mechanism |
| --- | --- |
| Require a password to open a file | Workbook file encryption/load password |
| Restrict worksheet actions | `Worksheet.Protect` with `ProtectionType` and allowed operations |
| Protect workbook structure/windows | Workbook protection/settings APIs verified for the format |
| Mark or restrict modification | Write-protection/password-to-modify APIs |
| Verify origin/integrity | Digital signature APIs and certificates |
| Protect VBA project | VBA project protection/signing APIs |

Never claim worksheet protection encrypts workbook contents or provides strong confidentiality.

## Scope

In scope: protect/unprotect workflows, locked/unlocked cells, workbook structure, open passwords, encryption providers/types, password-to-modify, signatures, certificate handling, protection verification, and security audits.

Use `macro-project` for VBA editing, `open-workbook` for general loading, and `document-properties` for ordinary metadata.

## Hard rules

- Use placeholder passwords from environment/configuration in production-oriented examples; never hard-code real secrets.
- Keep demonstration passwords obviously synthetic and warn that they are not production credentials.
- Do not print passwords, private keys, certificate secrets, or decrypted content.
- Use a format that supports the requested protection/encryption feature.
- Validate by reopening with the correct password and, where safe, confirming failure with an incorrect password.
- Explain what attackers are and are not prevented from doing.
- Never weaken encryption silently to maximize compatibility.
- Do not use a password hint that reveals the password.

## Canonical worksheet pattern

```csharp
Workbook workbook = new Workbook();
Worksheet worksheet = workbook.Worksheets[0];
worksheet.Cells["A1"].PutValue("Protected content");

worksheet.Protect(ProtectionType.All, "ExampleOnly-Password", null);
workbook.Save("protected-worksheet.xlsx");
```

For file encryption, use the package-version-supported load/save encryption APIs rather than repurposing worksheet protection.

## Example contract

Each example must name the protected asset, threat/intent, mechanism, format, credential source, allowed operations, and verification. Use explicit types and synthetic data. Prefer filenames such as `encrypt-xlsx-with-open-password.cs` or `protect-excel-worksheet-in-csharp.cs`.

Signature examples must identify whether they add a visible signature line or a cryptographic signature. Certificate examples must use a test certificate and never assume access to a machine certificate store in CI.

## Enterprise validation

- Verify APIs and algorithms against the installed package and current product documentation.
- Build and run without exposing secrets.
- Reopen with valid credentials and verify protected flags/content.
- Test invalid credentials only when failure can be asserted safely.
- Confirm the saved format retains the intended control.
- For signatures, verify signature validity after save and detect post-sign modification.

Reject examples that confuse protection with encryption, contain real credentials, depend silently on Windows-only certificate state, or claim compliance/certification without evidence.

## SEO, GEO, and AEO

Target one direct question: "password protect Excel in C#," "encrypt XLSX without Excel," "lock cells," or "digitally sign an Excel file." The opening comment must identify the asset and mechanism. Use precise security language over marketing claims.

## Related knowledge

- [Category overview](README.md)
- [Open workbook](../open-workbook/)
- [Macro projects](../macro-project/)
- [Official protection and encryption documentation](https://docs.aspose.com/cells/net/protect-and-unprotect/)

## Definition of done

The example is done when the security objective, mechanism, limitation, credential handling, format support, and verification are explicit and correct.

