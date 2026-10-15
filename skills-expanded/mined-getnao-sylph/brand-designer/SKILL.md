# Create Brand Asset

Process for creating any branded visual asset (social graphics, one-pagers, banners, etc.).

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| Canva | Create and edit brand assets from templates |
| Claude Design | Generate presentations (fallback if Canva unavailable), videos, and motion graphics |

## Process

1. **Load brand guidelines** - read `brand/brand-guidelines.md` first
2. **Identify the asset type** - match to a template from the table below
3. **Use the template** - start from the existing template, don't design from scratch
4. **Apply brand rules** - colors, fonts, logo placement per guidelines
5. **Export** - save to the appropriate folder in `brand/assets/`
6. **Log** - note the asset in the channel's `_insights.md` if it's channel-specific

## Design tool templates

| Asset type | Tool | Template ID / location |
|------------|------|----------------------|
| Presentation deck | Canva | `[your-canva-template-id]` |
| LinkedIn carousel | Canva | Search "[your-company] carousel" in brand kit |
| Blog cover image | Canva | Search "[your-company] blog cover" in brand kit |
| Social media graphic | Canva | Search "[your-company] social" in brand kit |
| One-pager / PDF | Canva | Search "[your-company] one-pager" in brand kit |
| Email header | Canva | Search "[your-company] email" in brand kit |
| Event banner | Canva | Search "[your-company] event" in brand kit |

## Guardrails

- **Always start from a template** - never design from a blank canvas
- **Never modify the logo** - use it as-is from `brand/assets/logo/`
- **Stay within the color palette** - no off-brand colors
- **Get approval** before publishing any new asset type not in the table
- **Save source files** - keep editable versions alongside exports

## Self-improvement

After the CAO reviews a design asset:

1. If the CAO requests changes to colors, layout, or typography that deviate from the current guidelines, update `brand/brand-guidelines.md`
2. If a new asset type is created that isn't in the Design tool templates table, add it
3. Update `brand/_insights.md` with what worked and what the CAO adjusted
4. If a design approach works well for a specific channel or format, save it as a reference in `brand/_examples/`
