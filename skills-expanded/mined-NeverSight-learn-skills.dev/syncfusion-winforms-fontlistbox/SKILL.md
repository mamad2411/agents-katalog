---
name: syncfusion-winforms-fontlistbox
description: Guide for implementing the Syncfusion WinForms FontListBox control in Windows Forms applications. Use this skill when the user needs to display a list of installed system fonts, configure selection modes for font selection, apply visual styles, enable font auto-complete, customize scrollbars, or handle font selection events. Covers UseAutoComplete, FontListBoxStyle, SelectionMode, and scrollbar behavior.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing the Syncfusion WinForms FontListBox Control

The Syncfusion `FontListBox` (`Syncfusion.Windows.Forms.Tools.FontListBox`) is a `ListBox`-derived control that automatically populates itself with all fonts installed on the user's system. It supports multiple selection modes, type-to-match auto-complete, horizontal scrollbars, item height control, and Office-style visual themes.

## When to Use This Skill

Use this skill when you need to:
- **Display a list of installed system fonts** — auto-populated on creation
- **Allow users to select a font** — apply the selected font to labels, text boxes, or other controls
- **Configure selection modes** — single, multi-simple, or multi-extended selection
- **Enable type-to-match auto-complete** — `UseAutoComplete`
- **Apply Office visual styles** — `VisualStyle` with `FontListBoxStyle` enum
- **Control scrollbar visibility** — `HorizontalScrollbar`, `ScrollAlwaysVisible`
- **Handle font selection events** — `SelectedIndexChanged`

## Component Overview

| Property | Type | Description |
|---|---|---|
| `SelectionMode` | `SelectionMode` | One, MultiSimple, or MultiExtended |
| `UseAutoComplete` | `bool` | Type-ahead matching within the list |
| `Sorted` | `bool` | Sort font names alphabetically |
| `ItemHeight` | `int` | Height in pixels of each list item |
| `HorizontalScrollbar` | `bool` | Show horizontal scrollbar when items overflow |
| `HorizontalExtent` | `int` | Width (px) of the scrollable area when horizontal scrollbar is on |
| `ScrollAlwaysVisible` | `bool` | Keep scrollbars visible regardless of item count |
| `VisualStyle` | `FontListBoxStyle` | Office/Metro visual theme |

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly references and NuGet package setup
- Adding FontListBox via designer or programmatically
- Auto-population with system fonts
- SelectionMode — None, One, MultiSimple, MultiExtended
- Handling SelectedIndexChanged to apply font to another control

### Customization and Behavior
📄 **Read:** [references/customization-and-behavior.md](references/customization-and-behavior.md)
- `ItemHeight` — row height per font entry
- `Sorted` — alphabetical sorting of font names
- `UseAutoComplete` — type-to-match as user types
- `HorizontalScrollbar` + `HorizontalExtent`
- `ScrollAlwaysVisible` — force scrollbars always visible

### Visual Styles
📄 **Read:** [references/visual-styles.md](references/visual-styles.md)
- `VisualStyle` property using `FontListBoxStyle` enum
- Available styles: Default, Metro, Office2016Colorful, Office2016White, Office2016Black, Office2016DarkGray

## Quick Start

**C#:**
```csharp
using Syncfusion.Windows.Forms.Tools;

FontListBox fontListBox1 = new FontListBox();
fontListBox1.Size = new System.Drawing.Size(160, 94);
fontListBox1.UseAutoComplete = true;
fontListBox1.SelectionMode = System.Windows.Forms.SelectionMode.One;
fontListBox1.SelectedIndexChanged += FontListBox1_SelectedIndexChanged;
this.Controls.Add(fontListBox1);

private void FontListBox1_SelectedIndexChanged(object sender, EventArgs e)
{
    label1.Font = new System.Drawing.Font(
        fontListBox1.SelectedItem.ToString(), 11, System.Drawing.FontStyle.Regular);
}
```

**VB.NET:**
```vb
Imports Syncfusion.Windows.Forms.Tools

Dim fontListBox1 As New FontListBox()
fontListBox1.Size = New System.Drawing.Size(160, 94)
fontListBox1.UseAutoComplete = True
fontListBox1.SelectionMode = System.Windows.Forms.SelectionMode.One
AddHandler fontListBox1.SelectedIndexChanged, AddressOf FontListBox1_SelectedIndexChanged
Me.Controls.Add(fontListBox1)

Private Sub FontListBox1_SelectedIndexChanged(ByVal sender As Object, ByVal e As EventArgs)
    label1.Font = New System.Drawing.Font(
        fontListBox1.SelectedItem.ToString(), 11, System.Drawing.FontStyle.Regular)
End Sub
```

## Common Use Cases

| Scenario | Properties to Set |
|---|---|
| Font picker for a text editor | `SelectionMode = One`, handle `SelectedIndexChanged` |
| Multi-font selection | `SelectionMode = MultiExtended` |
| Fast keyboard navigation | `UseAutoComplete = true` |
| Always show scrollbar | `ScrollAlwaysVisible = true` |
| Alphabetically sorted list | `Sorted = true` |
| Office-style appearance | `VisualStyle = FontListBoxStyle.Office2016Colorful` |
