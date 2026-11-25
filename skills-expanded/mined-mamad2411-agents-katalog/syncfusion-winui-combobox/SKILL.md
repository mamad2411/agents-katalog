---
name: syncfusion-winui-combobox
description: Guide for implementing the Syncfusion WinUI ComboBox control (SfComboBox) for single and multiple selection with filtering and token display. Use this when working with searchable dropdowns, multi-select combo boxes, or editable combo boxes in WinUI applications. This skill covers selection modes, data binding, filtering, grouping, and custom item templates.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing ComboBoxes (Syncfusion WinUI)

## When to Use This Skill

Use this skill when the user needs to:
- Implement a dropdown selection control in WinUI applications
- Enable single or multiple item selection from a list
- Add filtering and searching capabilities to a dropdown
- Create an editable dropdown with auto-completion
- Display selected items as tokens or delimiter-separated values
- Group dropdown items by categories
- Customize dropdown appearance with templates
- Handle user input validation and invalid entries
- Implement keyboard navigation in dropdowns

## Component Overview

The **Syncfusion WinUI ComboBox** (`SfComboBox`) is a feature-rich dropdown selection control that supports:
- **Selection Modes:** Single and multiple selection with checkbox support
- **Filtering:** Built-in filtering with StartsWith or Contains modes
- **Editing:** Editable and non-editable modes with auto-completion
- **Display Modes:** Token display or delimiter-separated display for multiple selections
- **Searching:** Text search with highlighting
- **Grouping:** Organize items into categories
- **Customization:** Extensive template and styling options
- **Keyboard Support:** Full keyboard navigation and shortcuts
- **Accessibility:** WCAG compliant with screen reader support

**When to use ComboBox vs. other dropdowns:**
- **Use ComboBox when:** You need filtering, editing, or multiple selection with tokens
- **Use DropDownList when:** You need simple single-selection without editing
- **Use MultiSelect Dropdown when:** You need multiple selection without tokens (checkbox only)
- **Use AutoComplete when:** You need type-ahead suggestion without dropdown list persistence

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installing NuGet package (Syncfusion.Editors.WinUI)
 - Installing NuGet package (Syncfusion.Editors.WinUI)
 - Note: make sure to update the `Syncfusion.Editors.WinUI` NuGet package to the latest available version before release.
- Basic ComboBox implementation in XAML and C#
- Populating items with SfComboBoxItem
- Data binding with ItemsSource
- Setting DisplayMemberPath and TextMemberPath
- Customizing SelectionBox UI

### Selection Modes
📄 **Read:** [references/selection.md](references/selection.md)
- Single selection (UI and programmatic)
- SelectionChangeTrigger (Committed vs Always)
- Multiple selection with checkboxes
- Delimiter display mode for multiple selections
- Token display mode with removable tokens
- Hiding/showing checkboxes
- Auto-append UI types (TextWithSelection vs Text)
- SelectionChanged and SelectionChanging events

### Filtering and Searching
📄 **Read:** [references/filtering.md](references/filtering.md)
- Enabling filtering with IsFilteringEnabled
- Filter modes (StartsWith, Contains)
- TextSearchMode configuration
- Custom filtering with IComboBoxFilterBehavior
- Implementing GetMatchingIndexes for custom logic
- Filter examples and patterns

📄 **Read:** [references/searching.md](references/searching.md)
- Text search functionality
- IsTextSearchEnabled property
- Auto-complete behavior
- Highlighting search results
- Search customization options

### Editing Modes
📄 **Read:** [references/editing.md](references/editing.md)
- Editable vs non-editable modes (IsEditable property)
- Auto-completion and text appending
- Setting null values with AllowNull
- Opening dropdown programmatically (IsDropDownOpen)
- Handling invalid input with InputSubmitted event
- Input validation patterns

### Grouping and Organization
📄 **Read:** [references/grouping.md](references/grouping.md)
- Grouping items by category
- GroupMemberPath configuration
- Customizing group headers
- Group templates and styling
- Sorting within groups

### UI Customization
📄 **Read:** [references/ui-customization.md](references/ui-customization.md)
- ItemTemplate for dropdown items
- SelectionBoxItemTemplate for selected item display
- Header and footer templates
- Styling ComboBox elements
- Theme customization
- ComboBoxTokenItem styling for token mode
- Custom template examples

### Keyboard and Advanced Features
📄 **Read:** [references/keyboard-and-advanced.md](references/keyboard-and-advanced.md)
- Keyboard navigation shortcuts
- Leading and trailing views
- Watermark/placeholder text (PlaceholderText)
- Accessibility features
- Performance optimization for large datasets
- Troubleshooting common issues

## Quick Start Example

### Basic Single-Selection ComboBox

```xaml
<Window xmlns:editors="using:Syncfusion.UI.Xaml.Editors">
    <editors:SfComboBox x:Name="comboBox"
                        Width="250"
                        PlaceholderText="Select a social media"
                        ItemsSource="{Binding SocialMedias}"
                        DisplayMemberPath="Name"
                        TextMemberPath="Name" />
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
            new SocialMedia { Name = "Twitter", ID = 1 },
            new SocialMedia { Name = "Instagram", ID = 2 }
        };
    }
}

// Set DataContext
comboBox.DataContext = new SocialMediaViewModel();
```

### Editable ComboBox with Filtering

```xaml
<editors:SfComboBox x:Name="comboBox"
                    Width="250"
                    IsEditable="True"
                    IsFilteringEnabled="True"
                    TextSearchMode="StartsWith"
                    PlaceholderText="Type to filter..."
                    ItemsSource="{Binding Items}"
                    DisplayMemberPath="Name"
                    TextMemberPath="Name" />
```

### Multiple Selection with Tokens

```xaml
<editors:SfComboBox x:Name="comboBox"
                    Width="250"
                    SelectionMode="Multiple"
                    MultiSelectionDisplayMode="Token"
                    IsEditable="True"
                    ItemsSource="{Binding Items}"
                    DisplayMemberPath="Name"
                    TextMemberPath="Name" />
```

## Common Patterns

### Pattern 1: Editable Dropdown with Auto-Complete

When the user types, automatically filter and suggest matching items:

```xaml
<editors:SfComboBox IsEditable="True"
                    IsFilteringEnabled="True"
                    TextSearchMode="StartsWith"
                    IsTextSearchEnabled="True"
                    ItemsSource="{Binding Cities}"
                    DisplayMemberPath="CityName"
                    TextMemberPath="CityName" />
```

**Key Configuration:**
- `IsEditable="True"`: Enables text input
- `IsFilteringEnabled="True"`: Filters items as user types
- `TextSearchMode="StartsWith"`: Filters items starting with entered text
- `IsTextSearchEnabled="True"`: Auto-appends first match to typed text

### Pattern 2: Multiple Selection with Custom Delimiter

Display multiple selected items separated by a custom delimiter:

```xaml
<editors:SfComboBox SelectionMode="Multiple"
                    MultiSelectionDisplayMode="Delimiter"
                    DelimiterText=" | "
                    ItemsSource="{Binding Items}"
                    DisplayMemberPath="Name"
                    TextMemberPath="Name" />
```

```csharp
// Access selected items
var selectedItems = comboBox.SelectedItems;
foreach (var item in selectedItems)
{
    // Process each selected item
}
```

### Pattern 3: Token Mode with Custom Token Template

Display selected items as removable tokens with custom styling:

```xaml
<editors:SfComboBox SelectionMode="Multiple"
                    MultiSelectionDisplayMode="Token"
                    ItemsSource="{Binding Items}"
                    DisplayMemberPath="Name"
                    TextMemberPath="Name">
    <editors:SfComboBox.TokenItemTemplate>
        <DataTemplate>
            <Grid Background="LightBlue" 
                  Padding="8,4"
                  CornerRadius="4">
                <TextBlock Text="{Binding Name}" 
                          Foreground="DarkBlue" />
            </Grid>
        </DataTemplate>
    </editors:SfComboBox.TokenItemTemplate>
</editors:SfComboBox>
```

### Pattern 4: Handling Invalid Input

Validate and handle user input that doesn't match any items:

```xaml
<editors:SfComboBox x:Name="comboBox"
                    IsEditable="True"
                    InputSubmitted="OnInputSubmitted"
                    ItemsSource="{Binding Items}"
                    DisplayMemberPath="Name"
                    TextMemberPath="Name" />
```

```csharp
private async void OnInputSubmitted(object sender, ComboBoxInputSubmittedEventArgs e)
{
    // Option 1: Show error message
    var dialog = new ContentDialog
    {
        Content = $"'{e.Text}' is not a valid option. Please select from the list.",
        CloseButtonText = "Close"
    };
    dialog.XamlRoot = this.Content.XamlRoot;
    await dialog.ShowAsync();
    
    // Option 2: Add new item dynamically (for multiple selection)
    // e.Item = new YourModel { Name = e.Text, ID = comboBox.Items.Count };
    
    // Option 3: Prevent selection
    // e.Handled = true;
}
```

### Pattern 5: Custom Filtering Logic

Implement custom filtering for complex scenarios:

```csharp
public class CustomFilterBehavior : IComboBoxFilterBehavior
{
    public List<int> GetMatchingIndexes(SfComboBox source, ComboBoxFilterInfo filterInfo)
    {
        var filteredList = new List<int>();
        var items = source.Items.OfType<YourModel>().ToList();
        
        // Custom filtering logic - search in multiple properties
        filteredList.AddRange(
            from item in items
            where item.Name.Contains(filterInfo.Text, StringComparison.OrdinalIgnoreCase) ||
                  item.Category.Contains(filterInfo.Text, StringComparison.OrdinalIgnoreCase)
            select items.IndexOf(item)
        );
        
        return filteredList;
    }
}
```

```xaml
<editors:SfComboBox ItemsSource="{Binding Items}"
                    IsEditable="True"
                    IsFilteringEnabled="True"
                    DisplayMemberPath="Name"
                    TextMemberPath="Name">
    <editors:SfComboBox.FilterBehavior>
        <local:CustomFilterBehavior />
    </editors:SfComboBox.FilterBehavior>
</editors:SfComboBox>
```

### Pattern 6: Programmatic Selection Management

Control selection through code for dynamic scenarios:

```csharp
// Single selection
comboBox.SelectedIndex = 2;
comboBox.SelectedItem = specificItem;

// Multiple selection
comboBox.SelectedItems.Add(item1);
comboBox.SelectedItems.Add(item2);

// Clear selection
comboBox.SelectedItems.Clear();

// React to selection changes
comboBox.SelectionChanged += (sender, e) =>
{
    foreach (var added in e.AddedItems)
    {
        // Handle newly selected items
    }
    
    foreach (var removed in e.RemovedItems)
    {
        // Handle deselected items
    }
};
```

## Key Properties

### Data Binding
- **ItemsSource:** Collection of items to display (`IEnumerable`)
- **DisplayMemberPath:** Property name shown in dropdown list
- **TextMemberPath:** Property name shown in selection box
- **SelectedItem:** Currently selected item (single selection)
- **SelectedItems:** Collection of selected items (multiple selection)
- **SelectedIndex:** Index of selected item (single selection)

### Selection Configuration
- **SelectionMode:** `Single` or `Multiple` selection
- **MultiSelectionDisplayMode:** `Delimiter` or `Token` for multiple selection
- **DelimiterText:** Character(s) separating items in delimiter mode (default: ",")
- **IsMultiSelectCheckBoxEnabled:** Show/hide checkboxes in dropdown (default: true)
- **SelectionChangeTrigger:** When to update selection - `Committed` or `Always`

### Editing and Filtering
- **IsEditable:** Enable/disable text editing (default: false)
- **IsFilteringEnabled:** Enable/disable filtering (default: false)
- **TextSearchMode:** Filter mode - `StartsWith` or `Contains`
- **IsTextSearchEnabled:** Enable/disable auto-complete (default: true)
- **AllowNull:** Allow null selection when text is cleared (default: false)

### Display and UI
- **PlaceholderText:** Watermark text when no selection
- **IsDropDownOpen:** Programmatically open/close dropdown
- **SelectionBoxItemTemplate:** Template for selected item display
- **ItemTemplate:** Template for dropdown list items
- **HeaderTemplate:** Template for dropdown header
- **FooterTemplate:** Template for dropdown footer

### Grouping
- **GroupMemberPath:** Property name for grouping items

## Common Use Cases

### Use Case 1: Country/State Selection
Two-level dependent dropdowns:

```xaml
<editors:SfComboBox x:Name="countryComboBox"
                    PlaceholderText="Select Country"
                    ItemsSource="{Binding Countries}"
                    SelectionChanged="OnCountryChanged"
                    DisplayMemberPath="Name"
                    TextMemberPath="Name" />

<editors:SfComboBox x:Name="stateComboBox"
                    PlaceholderText="Select State"
                    ItemsSource="{Binding States}"
                    DisplayMemberPath="Name"
                    TextMemberPath="Name" />
```

```csharp
private void OnCountryChanged(object sender, ComboBoxSelectionChangedEventArgs e)
{
    if (e.AddedItems.Count > 0)
    {
        var country = e.AddedItems[0] as Country;
        // Update states collection based on selected country
        viewModel.LoadStates(country.ID);
    }
}
```

### Use Case 2: Tag Selection for Blog Posts
Multi-select with token display for selecting multiple tags:

```xaml
<editors:SfComboBox SelectionMode="Multiple"
                    MultiSelectionDisplayMode="Token"
                    IsEditable="True"
                    PlaceholderText="Add tags..."
                    ItemsSource="{Binding AvailableTags}"
                    InputSubmitted="OnTagInputSubmitted"
                    DisplayMemberPath="TagName"
                    TextMemberPath="TagName" />
```

### Use Case 3: Searchable Employee Directory
Editable dropdown with filtering for quick employee lookup:

```xaml
<editors:SfComboBox IsEditable="True"
                    IsFilteringEnabled="True"
                    TextSearchMode="Contains"
                    PlaceholderText="Search employee..."
                    ItemsSource="{Binding Employees}"
                    DisplayMemberPath="FullName"
                    TextMemberPath="FullName">
    <editors:SfComboBox.ItemTemplate>
        <DataTemplate>
            <Grid>
                <Grid.ColumnDefinitions>
                    <ColumnDefinition Width="Auto" />
                    <ColumnDefinition Width="*" />
                </Grid.ColumnDefinitions>
                <Ellipse Width="32" Height="32" Margin="8">
                    <Ellipse.Fill>
                        <ImageBrush ImageSource="{Binding PhotoUrl}" />
                    </Ellipse.Fill>
                </Ellipse>
                <StackPanel Grid.Column="1" VerticalAlignment="Center">
                    <TextBlock Text="{Binding FullName}" FontWeight="SemiBold" />
                    <TextBlock Text="{Binding Department}" 
                              FontSize="12" 
                              Foreground="Gray" />
                </StackPanel>
            </Grid>
        </DataTemplate>
    </editors:SfComboBox.ItemTemplate>
</editors:SfComboBox>
```

### Use Case 4: Settings Panel with Grouped Options
Group related configuration options:

```xaml
<editors:SfComboBox ItemsSource="{Binding Settings}"
                    GroupMemberPath="Category"
                    DisplayMemberPath="Name"
                    TextMemberPath="Name">
    <editors:SfComboBox.GroupStyle>
        <GroupStyle>
            <GroupStyle.HeaderTemplate>
                <DataTemplate>
                    <TextBlock Text="{Binding Key}" 
                              FontWeight="Bold"
                              Foreground="DarkBlue"
                              Margin="8,4" />
                </DataTemplate>
            </GroupStyle.HeaderTemplate>
        </GroupStyle>
    </editors:SfComboBox.GroupStyle>
</editors:SfComboBox>
```

## Best Practices

1. **Always set both DisplayMemberPath and TextMemberPath** when binding to complex objects
2. **Use IsEditable="True" with IsFilteringEnabled="True"** for better user experience with large lists
3. **Handle InputSubmitted event** when using editable mode to validate user input
4. **Choose appropriate TextSearchMode:** Use `StartsWith` for predictable lists, `Contains` for flexible searching
5. **Use Token mode for multiple selection** when space allows, Delimiter mode for compact display
6. **Implement custom FilterBehavior** for complex filtering scenarios (multiple properties, fuzzy matching)
7. **Set PlaceholderText** to guide users on what to select
8. **Use SelectionChangeTrigger="Always"** for real-time updates, `Committed` for better performance
9. **Enable AllowNull** in editable mode if null selection is valid for your use case
10. **Customize ItemTemplate** for rich visual representation with images, icons, or multiple text lines
