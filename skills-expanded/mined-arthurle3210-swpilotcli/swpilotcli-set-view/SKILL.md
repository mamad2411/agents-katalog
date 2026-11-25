---
name: swpilotcli-set-view
description: Set view orientation of the active SolidWorks document. Supported views: front, back, left, right, top, bottom, iso (default), dimetric, trimetric. Calls ShowNamedView2 + ViewZoomtofit2.
---

# swpilotcli-set-view

Set the view orientation of the active SolidWorks document.

## Usage

```bash
dotnet run --project ./sup_tools/swpilotcli-set-view/scripts/SetView/SetView.csproj -- <orientation>
```

## Arguments

| Argument | Description |
|----------|-------------|
| `front` | Front view |
| `back` | Back view |
| `left` | Left view |
| `right` | Right view |
| `top` | Top view |
| `bottom` | Bottom view |
| `iso` / `isometric` | Isometric view (default) |
| `dimetric` | Dimetric view |
| `trimetric` | Trimetric view |

If no argument is given, defaults to `iso`.

## Notes

- Calls `ShowNamedView2` + `ViewZoomtofit2` for a clean result.
- Viewport layout (single/two-horizontal/two-vertical/four) is **not yet implemented** — needs SolidWorks macro recording to discover the correct API.
