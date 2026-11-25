---
name: optimizely-content-type-builder
version: 1.0.0
category: Migration/Build
description: Create correct Optimizely CMS 12 content type classes (PageData, BlockData, MediaData) with proper attributes, property types, and display metadata. Use during the fresh-build phase after running the auditor.
compatibility: Optimizely CMS 12, EPiServer.CMS.Core 12.x, .NET 6+
---

# Optimizely Content Type Builder

## Trigger On

- "create a content type"
- "add a page type"
- "create a block type"
- "build content model"
- "migrate content type to CMS 12"
- any task creating `PageData`, `BlockData`, or `MediaData` subclasses

## Documentation

- [Content Types](https://docs.developers.optimizely.com/content-management-system/docs/content-types)
- [Content Model and Views](https://docs.developers.optimizely.com/content-management-system/docs/content-model-and-views)
- [Restricting Content Types in Properties](https://docs.developers.optimizely.com/content-management-system/docs/restricting-content-types-in-properties)
- [Content Templates](https://docs.developers.optimizely.com/content-management-system/docs/content-templates)

## Rules

- ALL content properties MUST be `public virtual`
- ALWAYS include `GUID` on `[ContentType]` — copy from audit inventory exactly
- NEVER add constructor logic to content type classes
- Use `[Display]` for every editor-facing property
- Group properties with `GroupName` constants, not magic strings
- `BlockData` does NOT implement `IContent` directly — do not treat blocks like pages

## Page Type Pattern

```csharp
using EPiServer.Core;
using EPiServer.DataAbstraction;
using EPiServer.DataAnnotations;
using System.ComponentModel.DataAnnotations;

namespace MyProject.Models.Pages
{
    [ContentType(
        DisplayName = "Article Page",
        GUID = "A1B2C3D4-E5F6-7890-ABCD-EF1234567890",  // preserve from audit
        GroupName = GroupNames.Editorial,
        Order = 100)]
    [ImageUrl("~/icons/article.png")]
    public class ArticlePage : PageData
    {
        [Display(
            Name = "Hero Image",
            GroupName = SystemTabNames.Content,
            Order = 10)]
        [UIHint(UIHint.Image)]
        public virtual ContentReference HeroImage { get; set; }

        [Display(
            Name = "Introduction",
            GroupName = SystemTabNames.Content,
            Order = 20)]
        public virtual string Introduction { get; set; }

        [Display(
            Name = "Main Body",
            GroupName = SystemTabNames.Content,
            Order = 30)]
        [CultureSpecific]
        public virtual XhtmlString MainBody { get; set; }

        [Display(
            Name = "Related Content",
            GroupName = SystemTabNames.Content,
            Order = 40)]
        [AllowedTypes(new[] { typeof(BlockData) })]
        public virtual ContentArea RelatedContent { get; set; }
    }
}
```

## Block Type Pattern

```csharp
[ContentType(
    DisplayName = "Teaser Block",
    GUID = "B2C3D4E5-F6A7-8901-BCDE-F12345678901",
    GroupName = GroupNames.Content,
    Order = 10)]
public class TeaserBlock : BlockData
{
    [Display(Name = "Heading", GroupName = SystemTabNames.Content, Order = 10)]
    public virtual string Heading { get; set; }

    [Display(Name = "Body Text", GroupName = SystemTabNames.Content, Order = 20)]
    public virtual XhtmlString Body { get; set; }

    [Display(Name = "Image", GroupName = SystemTabNames.Content, Order = 30)]
    [UIHint(UIHint.Image)]
    public virtual ContentReference Image { get; set; }

    [Display(Name = "Link", GroupName = SystemTabNames.Content, Order = 40)]
    public virtual Url Link { get; set; }
}
```

## Media Type Pattern

```csharp
[ContentType(GUID = "C3D4E5F6-A7B8-9012-CDEF-123456789012")]
[MediaDescriptor(ExtensionString = "jpg,jpeg,png,gif,webp")]
public class ImageFile : ImageData
{
    [Display(Name = "Alt Text", GroupName = SystemTabNames.Content, Order = 10)]
    public virtual string AltText { get; set; }

    [Display(Name = "Caption", GroupName = SystemTabNames.Content, Order = 20)]
    public virtual string Caption { get; set; }
}
```

## AllowedTypes Patterns

```csharp
// Allow all blocks
[AllowedTypes(new[] { typeof(BlockData) })]
public virtual ContentArea ContentArea { get; set; }

// Allow specific types only
[AllowedTypes(new[] { typeof(TeaserBlock), typeof(CallToActionBlock) })]
public virtual ContentArea HeroArea { get; set; }

// Allow blocks but restrict specific ones
[AllowedTypes(
    AllowedTypes = new[] { typeof(BlockData) },
    RestrictedTypes = new[] { typeof(InternalOnlyBlock) })]
public virtual ContentArea PublicArea { get; set; }

// Restrict ContentReference to a specific page type
[AllowedTypes(typeof(ArticlePage))]
public virtual ContentReference RelatedArticle { get; set; }
```

## GroupName Constants Pattern

```csharp
public static class GroupNames
{
    public const string Editorial = "Editorial";
    public const string Content = "Content";
    public const string Metadata = "Metadata";
    public const string Settings = "Settings";
}
```

## Controller Pattern (Page)

```csharp
public class ArticlePageController : PageController<ArticlePage>
{
    private readonly IContentLoader _contentLoader;

    public ArticlePageController(IContentLoader contentLoader)
    {
        _contentLoader = contentLoader;
    }

    public IActionResult Index(ArticlePage currentPage)
    {
        var model = new ArticlePageViewModel(currentPage);
        return View(model);
    }
}
```

## Controller Pattern (Block)

```csharp
public class TeaserBlockViewComponent : BlockComponent<TeaserBlock>
{
    protected override IViewComponentResult InvokeComponent(TeaserBlock currentBlock)
    {
        return View(currentBlock);
    }
}
```

## Property Type Reference

| Property Type | Use For | Notes |
|---|---|---|
| `string` | Short text, URLs | Simple text fields |
| `XhtmlString` | Rich text editor | Requires TinyMCE setup |
| `ContentReference` | Single content link | Use `[UIHint(UIHint.Image)]` for images |
| `ContentArea` | Multiple content blocks | Use `[AllowedTypes]` to restrict |
| `Url` | External/internal links | Replaces old `UrlBuilder` |
| `LinkItemCollection` | List of links | Multi-link fields |
| `IList<ContentReference>` | Multi-select content | Combine with `[AllowedTypes]` |
| `bool` | Checkboxes | Simple flags |
| `int`, `double` | Numbers | Numeric input |
| `DateTime` | Date pickers | Use `[UIHint(UIHint.DateTime)]` |
| `SelectionFactory` | Dropdowns | Implement `ISelectionFactory` |

## Anti-Patterns

```csharp
// WRONG - not virtual
public string Title { get; set; }

// WRONG - no GUID
[ContentType(DisplayName = "My Page")]
public class MyPage : PageData { }

// WRONG - constructor logic
public ArticlePage()
{
    Title = "Default"; // throws at runtime
}

// WRONG - DataFactory (removed in CMS 12)
DataFactory.Instance.Get<PageData>(pageLink);

// WRONG - HttpContext.Current (not available in ASP.NET Core)
var request = HttpContext.Current.Request;
```
