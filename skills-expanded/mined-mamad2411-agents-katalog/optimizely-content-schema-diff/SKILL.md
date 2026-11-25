---
name: optimizely-content-schema-diff
version: 1.0.0
category: Migration/Validation
description: Compare old and new Optimizely content type inventories to catch missing types, missing properties, GUID mismatches, and type changes before running database migration. Run after building CMS 12 content models.
compatibility: Optimizely CMS 12 migration validation. Requires audit inventory JSON from optimizely-content-type-auditor.
---

# Optimizely Content Schema Diff

## Trigger On

- "compare content types old vs new"
- "validate content model migration"
- "check nothing was missed in migration"
- "diff schema before DB migration"
- "content type validation"

## Documentation

- [Content Types CMS 12](https://docs.developers.optimizely.com/content-management-system/docs/content-types)
- [Content Metadata Properties](https://docs.developers.optimizely.com/content-cloud/v12.0.0-content-cloud/docs/content-metadata-properties)

## What to Compare

### Critical Checks (DB migration will fail or corrupt without these)

| Check | Why Critical |
|---|---|
| `[ContentType(GUID = "...")]` matches exactly | CMS uses GUID to map DB records to classes — mismatch = data loss |
| All CMS 11 content types exist in CMS 12 | Missing type = orphaned content in DB |
| Property names match exactly (case-sensitive) | DB column names derived from property names |
| Property backing types compatible | Type change can corrupt stored values |

### Important Checks

| Check | Impact |
|---|---|
| `DisplayName` changed | Editor UI label changes — low risk |
| `Order` changed | Editor UI ordering changes — low risk |
| `GroupName` changed | Tab grouping changes in editor — low risk |
| `[AllowedTypes]` narrowed | Editors may lose ability to add existing content |
| `[Required]` added | Existing content without value fails validation |
| `[CultureSpecific]` added/removed | Language branch handling changes |

## Diff Report Format

```json
{
  "diffReport": {
    "missingContentTypes": [
      {
        "className": "LegacyPromoPage",
        "guid": "F1A2B3C4-...",
        "severity": "CRITICAL",
        "action": "Must be recreated in CMS 12 or content will be orphaned"
      }
    ],
    "guidMismatches": [
      {
        "className": "ArticlePage",
        "oldGuid": "A1B2C3D4-...",
        "newGuid": "X9Y8Z7W6-...",
        "severity": "CRITICAL",
        "action": "Fix GUID in new class to match old exactly"
      }
    ],
    "missingProperties": [
      {
        "contentType": "ArticlePage",
        "propertyName": "Subtitle",
        "oldType": "string",
        "severity": "HIGH",
        "action": "Add property to CMS 12 ArticlePage class"
      }
    ],
    "typeChanges": [
      {
        "contentType": "HeroBlock",
        "propertyName": "Link",
        "oldType": "UrlBuilder",
        "newType": "Url",
        "severity": "MEDIUM",
        "action": "Verify DB value format compatible — test on staging first"
      }
    ],
    "newProperties": [
      {
        "contentType": "ArticlePage",
        "propertyName": "MetaDescription",
        "newType": "string",
        "severity": "INFO",
        "action": "New property — editors must populate on publish"
      }
    ],
    "summary": {
      "criticalIssues": 2,
      "highIssues": 1,
      "mediumIssues": 3,
      "infoIssues": 5,
      "readyForDbMigration": false
    }
  }
}
```

## Pre-Migration Checklist

Before running `update-database` or deploying CMS 12:

- [ ] Zero `CRITICAL` issues in diff report
- [ ] All GUIDs verified against old codebase
- [ ] All property names verified (case-sensitive)
- [ ] Staging DB migration tested successfully
- [ ] Content spot-checked in CMS 12 editor
- [ ] `[Required]` changes reviewed against existing data
- [ ] `[AllowedTypes]` changes reviewed with editors

## GUID Verification Script Pattern

```csharp
// Quick runtime check — add to startup in dev only
public class ContentTypeGuidValidator : IStartupFilter
{
    private readonly IContentTypeRepository _contentTypeRepository;

    public ContentTypeGuidValidator(IContentTypeRepository contentTypeRepository)
    {
        _contentTypeRepository = contentTypeRepository;
    }

    public Action<IApplicationBuilder> Configure(Action<IApplicationBuilder> next)
    {
        return app =>
        {
            // Verify expected GUIDs are registered
            var articlePageType = _contentTypeRepository.Load("ArticlePage");
            Debug.Assert(articlePageType?.GUID == Guid.Parse("A1B2C3D4-..."),
                "ArticlePage GUID mismatch — check [ContentType] attribute");

            next(app);
        };
    }
}
```
