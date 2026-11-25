---
name: whats-new-in-csharp
description: Consult version-specific C# language and .NET runtime updates when writing or reviewing C# code or discussing new C# or .NET features.
metadata:
  homepage: "https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/"
  version: "C# 12, 13, 14"
  last-updated: "2026-09-20"
  generated-by: "gpt-6"
---

# What's New in C# and .NET

## How to load references

1. Before reading references, determine the project's effective C# language version and .NET target frameworks separately. Inspect `LangVersion`, `TargetFramework` or `TargetFrameworks`, inherited settings such as `Directory.Build.props`, and SDK selection in `global.json`. If `LangVersion` is absent, use the documented language default for the target framework. Do not equate the installed SDK with the project's runtime target. If the targets cannot be established, use the explicitly requested versions or ask.
2. Load references cumulatively and independently: read every listed C# reference at or below the language target, and every listed .NET reference at or below the runtime target, each in ascending version order. For upgrade discussions, use the proposed targets. For multi-targeted projects, account for each target and preserve compatibility when applying features.
3. Read each reference only once while its contents remain available in context. Reuse previously loaded content on subsequent invocations.
4. Check the language reference's runtime and SDK requirements before applying its features. Do not infer that matching C# and .NET version numbers belong together.

## C# language references

| C# version | Reference |
| --- | --- |
| 12 | [C# 12 summary](references/csharp-12-summary.md) |
| 13 | [C# 13 summary](references/csharp-13-summary.md) |
| 14 | [C# 14 summary](references/csharp-14-summary.md) |

## .NET runtime references

No runtime summaries are included yet. Future runtime summaries use `references/dotnet-<version>-summary.md` and remain separate from language summaries.

## Further reference

The [C# documentation](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/) and [.NET documentation](https://learn.microsoft.com/en-us/dotnet/core/whats-new/) cover uncommon restrictions, detailed version compatibility, and migration considerations intentionally omitted here. Consult them or linked feature specifications only when the task needs information absent from the loaded references. Do not fetch documentation for information already covered here or in those references.
