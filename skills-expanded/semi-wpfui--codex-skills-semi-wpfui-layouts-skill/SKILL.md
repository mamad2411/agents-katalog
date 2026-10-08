---
name: semi-wpfui-layouts
description: Use Semi.WpfUi custom layout controls when building or migrating WPF demo pages and control examples in this repository. Apply when editing XAML under demo/Semi.WpfUi.Demo or composing layouts for Semi.WpfUi controls, especially where WPF Margin is being used only to create spacing between siblings.
---

# Semi.WpfUi layout controls

Use the controls from `Semi.WpfUi.Controls` in demo XAML:

```xml
xmlns:semi="clr-namespace:Semi.WpfUi.Controls;assembly=Semi.WpfUi"
```

## Choose the layout

- Use `semi:StackPanel` for a linear layout. Set `Spacing` for sibling gaps instead of per-child `Margin`.
- Use `semi:Grid` when rows or columns are required. Set `RowSpacing` and `ColumnSpacing` instead of spacer rows, columns, or sibling margins. Continue using normal WPF row and column definitions and attached placement properties.
- Use `semi:Panel` for children that should share the same available bounds and do not need row, column, or sequential layout.

## Demo-page rules

- Prefer a page-level `semi:StackPanel Spacing="..."` to separate headings and sections.
- Prefer nested `semi:StackPanel Spacing="..."` for fields, labels, and examples within a section.
- Use container `Padding` for a component's internal inset, such as `GroupBox Padding="16"`.
- Retain `Margin` only when it expresses an external layout requirement that the custom layouts cannot represent, such as page placement or an intentional one-off offset. Do not use it solely as a sibling gap.
- Keep the examples focused on the control being demonstrated; do not add unsupported Avalonia-only properties or class names when migrating an Avalonia demo.

## Example

```xml
<GroupBox Padding="16" Header="States">
    <semi:StackPanel Spacing="12">
        <semi:TextBox PlaceholderText="Default" />
        <semi:TextBox IsEnabled="False" PlaceholderText="Disabled" />
    </semi:StackPanel>
</GroupBox>
```
