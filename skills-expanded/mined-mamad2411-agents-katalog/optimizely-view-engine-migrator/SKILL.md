---
name: optimizely-view-engine-migrator
version: 1.0.0
category: Migration/Build
description: Migrate Optimizely CMS 11 MVC views, partial views, and display templates to CMS 12 ASP.NET Core patterns. Covers BlockComponent/ViewComponent patterns, tag helpers, and display channel conventions.
compatibility: Optimizely CMS 12, ASP.NET Core MVC, .NET 6+
---

# Optimizely View Engine Migrator

## Trigger On

- "migrate views to CMS 12"
- "convert display templates"
- "create block view component"
- "migrate partial controller"
- "update Razor views for CMS 12"

## Documentation

- [Content Templates CMS 12](https://docs.developers.optimizely.com/content-management-system/docs/content-templates)

## Controller Migration

### Page Controller

```csharp
// OLD (CMS 11) - ControllerBase or Controller
public class ArticlePageController : PageController<ArticlePage>
{
    public ActionResult Index(ArticlePage currentPage)
    {
        return View(new ArticlePageViewModel(currentPage));
    }
}

// NEW (CMS 12) - Same pattern, different base namespace
// EPiServer.Web.Mvc.PageController<T> still works in CMS 12
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

### Block — ViewComponent (preferred in CMS 12)

```csharp
// NEW (CMS 12) - BlockComponent (inherits ViewComponent)
public class TeaserBlockViewComponent : BlockComponent<TeaserBlock>
{
    private readonly IUrlResolver _urlResolver;

    public TeaserBlockViewComponent(IUrlResolver urlResolver)
    {
        _urlResolver = urlResolver;
    }

    protected override IViewComponentResult InvokeComponent(TeaserBlock currentBlock)
    {
        var model = new TeaserBlockViewModel
        {
            Heading = currentBlock.Heading,
            ImageUrl = _urlResolver.GetUrl(currentBlock.Image)
        };
        return View(model);
    }
}
```

### Block — PartialController (also valid)

```csharp
public class TeaserBlockController : ActionControllerBase
{
    public IActionResult Index(TeaserBlock currentBlock)
    {
        return PartialView(currentBlock);
    }
}
```

## View File Conventions

```
Views/
├── ArticlePage/
│   └── Index.cshtml           # Page controller view
├── Shared/
│   └── Components/
│       └── TeaserBlock/
│           └── Default.cshtml # BlockComponent view
├── TeaserBlock/
│   └── Index.cshtml           # PartialController view (alternative)
└── _Layout.cshtml
```

## Razor View Patterns

### Page View

```razor
@model ArticlePageViewModel

@Html.PropertyFor(m => m.CurrentPage.HeroImage)
<h1>@Html.PropertyFor(m => m.CurrentPage.Name)</h1>
<div>@Html.PropertyFor(m => m.CurrentPage.MainBody)</div>

@Html.PropertyFor(m => m.CurrentPage.RelatedContent)
```

### Block View (ViewComponent)

```razor
@model TeaserBlockViewModel

<div class="teaser">
    <h2>@Model.Heading</h2>
    @if (!string.IsNullOrEmpty(Model.ImageUrl))
    {
        <img src="@Model.ImageUrl" alt="@Model.AltText" />
    }
</div>
```

### ContentArea Rendering

```razor
@* Render a content area with default templates *@
@Html.PropertyFor(m => m.CurrentPage.MainContentArea)

@* Render with a display option hint *@
@Html.PropertyFor(m => m.CurrentPage.MainContentArea,
    new { CssClass = "row", Tag = ContentAreaTags.TwoThirdsWidth })
```

## Tag Helpers (CMS 12)

```razor
@* Register in _ViewImports.cshtml *@
@addTagHelper *, EPiServer.CMS.AspNetCore.TagHelpers

@* Usage *@
<epi-property-for name="Heading" />
<epi-content-area name="MainContentArea" />
```

## Display Channel Convention

```csharp
// Tag content type for specific display channels
[TemplateDescriptor(
    Inherited = true,
    TemplateTypeCategory = TemplateTypeCategories.MvcPartialView,
    Tags = new[] { RenderingTags.Mobile },
    AvailableWithoutTag = false)]
public class MobileTeaserBlockViewComponent : BlockComponent<TeaserBlock>
{
    protected override IViewComponentResult InvokeComponent(TeaserBlock currentBlock)
        => View("Mobile", currentBlock);
}
```

## Anti-Patterns

```csharp
// WRONG - WebForms style code-behind
public partial class ArticlePage : System.Web.UI.Page { }

// WRONG - HtmlHelper extensions from classic MVC
@Html.RenderAction("Index", "TeaserBlock") // not available in ASP.NET Core

// WRONG - ViewData instead of typed model
ViewData["Title"] = "..."; // prefer strongly typed ViewModels

// WRONG - Server controls
<asp:Repeater ...> // WebForms only, not CMS 12
```
