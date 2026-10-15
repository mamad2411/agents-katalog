---
name: syncfusion-winui-autocomplete
description: Guide implementation of the Syncfusion WinUI AutoComplete control (SfAutoComplete)  for creating searchable dropdowns with single or multiple selection, filtering  suggestions, and customizable token display. Use this skill when implementing search-as-you-type functionality, autocomplete dropdowns with multi-select, tagging systems with token/chip display, or filtered suggestion boxes in WinUI applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing AutoComplete (SfAutoComplete)

The Syncfusion WinUI AutoComplete (`SfAutoComplete`) is a highly optimized control for providing filtered suggestions from large datasets as users type. It supports both single and multiple item selection, displaying selected items as tokens with images, text, and close buttons for easy removal.

## When to Use This Skill

Use this skill when the user needs to:
- **Implement autocomplete search functionality** in WinUI applications
- **Create searchable dropdowns** with filtered suggestions based on user input
- **Build tag or token input fields** with multi-select capability
- **Filter large datasets** based on characters entered by the user
- **Provide search-as-you-type experiences** with auto-suggestions
- **Implement multi-select dropdowns** with chip/token display
- **Add watermark text** to guide user input in search fields
- **Customize suggestion item display** with images and custom templates
- **Handle "no results found"** scenarios with custom messaging
- **Add leading/trailing icons or buttons** to autocomplete inputs

## Component Overview

**Package:** `Syncfusion.Editors.WinUI`  
**Namespace:** `Syncfusion.UI.Xaml.Editors`  
**Control:** `SfAutoComplete`

**Key Capabilities:**
- Single and multiple selection modes
- Real-time filtering (StartsWith or Contains)
- Custom filtering logic support
- Token/chip display for selected items
- Highlighting of matched text
- Grouping of suggestions
- Leading and trailing views
- Watermark/placeholder text
- Keyboard navigation
- Template customization

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

When the user needs to:
- Install the AutoComplete package
- Create and configure the control
- Set up data binding with ItemsSource
- Configure TextMemberPath and DisplayMemberPath
- Implement basic autocomplete functionality

### Selection
📄 **Read:** [references/selection.md](references/selection.md)

When the user needs to:
- Configure single vs multiple selection
- Handle selected items programmatically
- Display tokens/chips for multiple selections
- Listen to selection change events
- Work with SelectedItem or SelectedItems properties

### Searching and Filtering
📄 **Read:** [references/searching-filtering.md](references/searching-filtering.md)

When the user needs to:
- Configure filtering behavior (StartsWith or Contains)
- Implement custom filtering logic
- Search based on specific properties
- Handle auto-fill and auto-suggestions
- Select default items after filtering

### UI Customization
📄 **Read:** [references/ui-customization.md](references/ui-customization.md)

When the user needs to:
- Customize dropdown item templates
- Add leading icons or buttons
- Add trailing actions or clear buttons
- Style selected item tokens
- Handle "no results found" UI
- Set watermark/placeholder text

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

When the user needs to:
- Group suggestions by category
- Highlight matched text in suggestions
- Implement keyboard shortcuts
- Ensure accessibility compliance
- Handle advanced user interactions

## Quick Start Example

### Basic Single-Selection AutoComplete

```xaml
<Window xmlns:editors="using:Syncfusion.UI.Xaml.Editors">
    <Grid>
        <editors:SfAutoComplete x:Name="autoComplete"
                                Width="250"
                                PlaceholderText="Search social media..."
                                ItemsSource="{Binding SocialMedias}"
                                DisplayMemberPath="Name"
                                TextMemberPath="Name"
                                TextSearchMode="Contains" />
    </Grid>
</Window>
```

```csharp
// Model
public class SocialMedia
{
    public string Name { get; set; }
    public int ID { get; set; }
}

// ViewModel
public class SocialMediaViewModel
{
    public ObservableCollection<SocialMedia> SocialMedias { get; set; }
    
    public SocialMediaViewModel()
    {
        SocialMedias = new ObservableCollection<SocialMedia>
        {
            new SocialMedia { Name = "Facebook", ID = 0 },
            new SocialMedia { Name = "Instagram", ID = 1 },
            new SocialMedia { Name = "Twitter", ID = 2 },
            new SocialMedia { Name = "LinkedIn", ID = 3 }
        };
    }
}

// Set DataContext
autoComplete.DataContext = new SocialMediaViewModel();
```

### Multi-Selection with Tokens

```xaml
<editors:SfAutoComplete x:Name="autoComplete"
                        Width="300"
                        SelectionMode="Multiple"
                        PlaceholderText="Select multiple items..."
                        ItemsSource="{Binding SocialMedias}"
                        DisplayMemberPath="Name"
                        TextMemberPath="Name"
                        TextSearchMode="Contains" />
```

## Common Patterns

### Pattern 1: Search with Contains Filter

```xaml
<editors:SfAutoComplete ItemsSource="{Binding Countries}"
                        DisplayMemberPath="Name"
                        TextMemberPath="Name"
                        TextSearchMode="Contains"
                        PlaceholderText="Type to search..." />
```

Use when users need to find items by any part of the text, not just the beginning.

### Pattern 2: Multi-Select Tags with Custom Display

```xaml
<editors:SfAutoComplete SelectionMode="Multiple"
                        ItemsSource="{Binding Tags}"
                        DisplayMemberPath="Name"
                        TextMemberPath="Name">
    <editors:SfAutoComplete.ItemTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal" Padding="5">
                <TextBlock Text="{Binding Name}" 
                          FontWeight="SemiBold"/>
            </StackPanel>
        </DataTemplate>
    </editors:SfAutoComplete.ItemTemplate>
</editors:SfAutoComplete>
```

Use for tagging systems where users select multiple items displayed as tokens.

### Pattern 3: Autocomplete with Leading Icon

```xaml
<editors:SfAutoComplete ItemsSource="{Binding Items}"
                        DisplayMemberPath="Name"
                        TextMemberPath="Name">
    <editors:SfAutoComplete.LeadingView>
        <Grid Padding="8">
            <Path Data="M15.5 14h-.79l-.28-.27C15.41..." 
                  Fill="{ThemeResource SystemAccentColor}"/>
        </Grid>
    </editors:SfAutoComplete.LeadingView>
</editors:SfAutoComplete>
```

Use to provide visual context (e.g., search icon) for the autocomplete field.

### Pattern 4: Custom "No Results" Message

```xaml
<editors:SfAutoComplete ItemsSource="{Binding Products}"
                        DisplayMemberPath="Name"
                        TextMemberPath="Name"
                        NoResultsFoundContent="No products found. Try a different search." />
```

Use to provide helpful feedback when filtering returns no matches.

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `ItemsSource` | `object` | Collection of data items to display |
| `DisplayMemberPath` | `string` | Property path for dropdown item display |
| `TextMemberPath` | `string` | Property path for selection box text |
| `SelectionMode` | `AutoCompleteSelectionMode` | `Single` or `Multiple` selection |
| `TextSearchMode` | `AutoCompleteTextSearchMode` | `StartsWith` or `Contains` filtering |
| `PlaceholderText` | `string` | Watermark text when empty |
| `SelectedItem` | `object` | Currently selected item (single mode) |
| `SelectedItems` | `ObservableCollection` | Selected items collection (multiple mode) |
| `NoResultsFoundContent` | `object` | Content when no matches found |
| `LeadingView` | `object` | Content displayed before text input |
| `TrailingView` | `object` | Content displayed after text input |
| `GroupMemberPath` | `string` | Property path for grouping items |
| `HighlightedTextColor` | `Brush` | Color for highlighting matched text |
| `FilterBehavior` | `AutoCompleteFilterBehavior` | Custom filtering logic |

## Common Use Cases

### Email Recipient Selector
Multi-select autocomplete for selecting email recipients from a contact list, displaying selected contacts as removable tokens.

### Product Search
Single-select autocomplete for finding products in an e-commerce app, with contains-based filtering for flexible searching.

### Category Tagging
Multi-select autocomplete for assigning multiple categories or tags to items, with custom token display.

### Location Search
Single-select autocomplete with grouped suggestions (Countries > Cities), using StartsWith filtering for quick navigation.

### Skill Search
Multi-select autocomplete for selecting user skills from a predefined list, with "no results" message for unrecognized entries.

## Related Components

- **[ComboBox](../implementing-comboboxes/)** - For simple dropdown selection without autocomplete filtering
- **[TextBox](../../inputs/implementing-textboxes/)** - For basic text input without suggestions (if documented)

## Integration Tips

**With MVVM:**
- Bind `ItemsSource` to ViewModel's `ObservableCollection`
- Use `SelectedItem` or `SelectedItems` with two-way binding
- Handle selection changes in ViewModel via binding commands

**Performance:**
- Use virtualization for large datasets (>1000 items)
- Consider async loading for remote data sources
- Use `TextSearchMode.StartsWith` for better performance with very large lists

**Accessibility:**
- Always set `PlaceholderText` to guide users
- Use `AutomationProperties.Name` for screen readers
- Ensure keyboard navigation works (Tab, Enter, Esc)
- Test with high contrast themes

## Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| Suggestions not showing | Check `ItemsSource` is bound and contains data; verify `DisplayMemberPath` |
| Wrong text displayed | Set `TextMemberPath` to the correct property name |
| Filtering not working | Ensure `TextSearchMode` is set; verify property data types are strings |
| Multiple selection not working | Set `SelectionMode="Multiple"` |
| Custom template not applied | Check `ItemTemplate` DataContext binding matches data model |
| No results message not showing | Set `NoResultsFoundContent` property |

---

**Next Steps:** For detailed implementation, navigate to the specific reference file matching your needs using the documentation guide above.
