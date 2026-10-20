---
name: optimizely-content-type-auditor
version: 1.0.0
category: Migration/Audit
description: Scan a legacy Optimizely CMS 11 or EPiServer codebase and produce a structured inventory of all content types, properties, and metadata. Run this first before any fresh-build migration to CMS 12.
compatibility: Targets EPiServer/Optimizely CMS 10/11 source. Output used to plan CMS 12 fresh build.
---

# Optimizely Content Type Auditor

## Trigger On

- "audit content types"
- "inventory my Optimizely content types"
- "what content types do I have"
- "scan EPiServer models"
- "start migration audit"
- any fresh-build migration kickoff task

## Documentation

- [CMS 12 Content Types](https://docs.developers.optimizely.com/content-management-system/docs/content-types)
- [Content Metadata Properties](https://docs.developers.optimizely.com/content-cloud/v12.0.0-content-cloud/docs/content-metadata-properties)
- [Breaking Changes CMS 11 → 12](https://docs.developers.optimizely.com/content-management-system/docs/breaking-changes-in-content-cloud-cms-12)

## Workflow

1. **Scan** all `.cs` files in the source project for classes decorated with `[ContentType]`
2. **Classify** each by base class: `PageData`, `BlockData`, `IContentMedia`, `MediaData`, `ImageData`, `VideoData`, or custom
3. **Extract** all public virtual properties, their types, and decorating attributes
4. **Record** `[ContentType(GUID=...)]` values — these must be preserved exactly in CMS 12
5. **Flag** deprecated or removed property types (e.g., `UrlBuilder`, `EPiServer.SpecializedProperties.*` without v12 equivalent)
6. **Output** structured inventory as JSON or Markdown table

## What to Scan For

### Class-Level Attributes
```csharp
[ContentType(DisplayName = "...", GUID = "...", GroupName = "...", Order = ...)]
[ImageUrl("...")]
[AvailableContentTypes(Include = new[] { typeof(...) })]
[Access(Scheme = AccessScheme.Everyone)]
```

### Property-Level Attributes
```csharp
[Display(Name = "...", GroupName = "...", Order = ..., Description = "...")]
[Required]
[AllowedTypes(new[] { typeof(BlockData) })]
[UIHint(UIHint.Image)]
[BackingType(typeof(PropertyLongString))]
[Ignore]
[ScaffoldColumn(false)]
[CultureSpecific]
```

### Base Class Mapping (CMS 11 → CMS 12)

| CMS 11 Base | CMS 12 Base | Notes |
|---|---|---|
| `PageData` | `PageData` | Unchanged |
| `BlockData` | `BlockData` | Unchanged |
| `ImageData` | `ImageData` | Unchanged |
| `VideoData` | `VideoData` | Unchanged |
| `MediaData` | `MediaData` | Unchanged |
| `IContentMedia` | `IContentMedia` | Interface unchanged |
| `SitePageData` (custom) | Rebuild as custom base | Carry forward |

### Property Types to Flag

| Old Type | CMS 12 Status | Action |
|---|---|---|
| `UrlBuilder` | Removed | Replace with `Url` (string) |
| `PropertyLongString` as BackingType | Still valid | Keep |
| `ContentArea` | Unchanged | Keep |
| `ContentReference` | Unchanged | Keep |
| `XhtmlString` | Unchanged | Keep |
| `LinkItemCollection` | Unchanged | Keep |
| `EPiServer.SpecializedProperties.PageType` | Removed | Replace with ContentReference |

## Output Format

Produce a structured inventory. Example:

```json
{
  "contentTypes": [
    {
      "className": "ArticlePage",
      "baseClass": "PageData",
      "guid": "A1B2C3D4-...",
      "displayName": "Article Page",
      "groupName": "Editorial",
      "order": 100,
      "properties": [
        {
          "name": "MainBody",
          "type": "XhtmlString",
          "attributes": ["Display", "CultureSpecific"],
          "flags": []
        },
        {
          "name": "HeroImage",
          "type": "ContentReference",
          "attributes": ["Display", "UIHint(UIHint.Image)"],
          "flags": []
        }
      ],
      "flags": []
    }
  ],
  "summary": {
    "totalContentTypes": 42,
    "pages": 18,
    "blocks": 20,
    "media": 4,
    "flaggedForReview": 3
  }
}
```

## Anti-Patterns to Flag

- Missing `GUID` on `[ContentType]` — must be added before CMS 12 migration or DB will lose mapping
- Properties not marked `virtual` — CMS 12 requires `public virtual` for all content properties
- Constructor logic in content type classes — not supported, move to factories
- Direct `DataFactory` usage — must be replaced with `IContentRepository`
- `HttpContext.Current` in content models — not available in ASP.NET Core
