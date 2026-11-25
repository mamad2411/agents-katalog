---
name: csharp-security-patterns
description: Advanced .NET/C# security patterns. Viewstate, Azure AD Misconfig, Entity Framework Injection, Mass Assignment.
tools: Read, Grep, Glob
---

# C# (.NET) Security Patterns

## 1. Insecure Deserialization
- **BinaryFormatter**: `formatter.Deserialize(stream)`. (Mieroseys)
- **Json.NET**: `TypeNameHandling.All` allows instantiating arbitrary types.

## 2. VIEWSTATE MAC Validation
- **Pattern**: `enableViewStateMac="false"` in `web.config`.
- **Impact**: Deserialization RCE via VIEWSTATE parameter.

## 3. Entity Framework Injection
- **Pattern**: `context.Database.ExecuteSqlCommand("..." + input)`.
- **Correction**: Use parameters `{0}`.

## 4. Mass Assignment (Over-posting)
- **Pattern**: `UpdateModel(userModel)` where `userModel` binds directly to DB entity.
- **Impact**: User setting `IsAdmin = true`.
- **Fix**: Use ViewModels (DTOs).
