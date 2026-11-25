---
name: syncfusion-winforms-navigation-view
description: Guide for implementing Syncfusion NavigationView control in Windows Forms for breadcrumb navigation and hierarchical path tracking. Use when building file explorers, folder browsers, or file browser-style interfaces with breadcrumb trails. Covers breadcrumb navigation, dropdown navigation, history tracking, and hierarchical bar structures for path-based location tracking with dropdown child selection.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Navigation Views in Windows Forms

## When to Use This Skill

Use the NavigationView control when you need:

- **Breadcrumb Navigation:** Display hierarchical location paths (e.g., `MyComputer > C: > Program Files > App`)
- **File Browser Interfaces:** Track and navigate folder hierarchies like Windows Explorer
- **Location Tracking:** Keep users aware of their current position in multi-level structures
- **Quick Navigation:** Allow users to jump back to parent locations or navigate via dropdown
- **Settings/Configuration Wizards:** Show user's progress through nested categories
- **Document Management:** Navigate document folders, categories, or organizational structures

**Key Feature:** Unlike traditional menus or tree views, NavigationView shows the current path with dropdown access to siblings at each level.

## Component Overview

The `NavigationView` control provides a breadcrumb-style navigation interface that displays a hierarchical path using **Bars** (nodes). Each Bar in the path shows a forward arrow that, when clicked, reveals a dropdown list of child Bars directly below it.

**Core Concepts:**
- **Bar:** A single node in the navigation hierarchy (e.g., "MyComputer", "C:", "Users")
- **Parent Bar:** A Bar that contains child Bars (root level or intermediate)
- **Child Bar:** A Bar nested within a parent Bar
- **Selected Bar:** The currently active Bar displayed in the path
- **History:** Tracks previously visited Bars for quick return navigation

**Visual Structure:**
```
[Icon] MyComputer > C: > Program Files > App   [History ▼]
       └─────┬─────┘
              └─ Click arrow to see child Bars dropdown
```

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

Read this reference when you need to:
- Install assemblies or NuGet packages for NavigationView
- Add the control to a form via designer or code
- Understand required namespaces (`Syncfusion.Windows.Forms.Tools`)
- Set up a basic NavigationView with minimal configuration
- See a complete minimal working example

**Key Topics:**
- Assembly deployment (6 required DLLs)
- Adding control via designer drag-and-drop
- Adding control manually using code
- Creating the first NavigationView instance
- Basic setup and initialization

---

### Bar Hierarchy and Structure
📄 **Read:** [references/bar-hierarchy.md](references/bar-hierarchy.md)

Read this reference when you need to:
- Create parent and child Bar relationships
- Build multi-level navigation hierarchies
- Add Bars to the NavigationView.Bars collection
- Add child Bars to a parent Bar's Bars collection
- Set the selected Bar to display a specific path
- Understand Bar properties (Text, ImageIndex)

**Key Topics:**
- Creating Bar instances
- Parent-child Bar relationships
- Adding root Bars to NavigationView
- Adding child Bars to parent Bars
- Setting SelectedBar property
- Navigating between Bars programmatically

---

### Dropdown Selection and History
📄 **Read:** [references/dropdown-and-history.md](references/dropdown-and-history.md)

Read this reference when you need to:
- Implement dropdown selection for child Bar navigation
- Enable/disable history button tracking
- Show previously visited locations in history dropdown
- Add custom buttons to the NavigationView
- Configure custom button appearance and images
- Handle BarPopup event for dropdown customization
- Control maximum items displayed in popups

**Key Topics:**
- Forward arrow dropdown mechanism
- ShowHistoryButtons property
- History tracking and dropdown
- Custom button collection
- Adding custom buttons (designer and code)
- BarPopup event handling
- Customizable popup item count

---

### Images and Visual Styling
📄 **Read:** [references/images-and-styling.md](references/images-and-styling.md)

Read this reference when you need to:
- Add icons to Bars using ImageList
- Set ImageIndex for parent and child Bars
- Apply visual styles (Office2007, Vista, Metro)
- Configure VisualStyle property
- Customize control appearance
- Match application theme or style

**Key Topics:**
- ImageList setup and assignment
- Setting Bar ImageIndex properties
- Visual styles overview
- Applying Office2007 style
- Applying Vista style
- Applying Metro style
- Appearance customization

---

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

Read this reference when you need to:
- Enable edit mode for direct path typing
- Allow users to type navigation paths
- Control popup behavior with BarPopup event
- Set maximum items to display in popups
- Cancel popup display conditionally
- Implement advanced navigation scenarios

**Key Topics:**
- Edit mode enabling and usage
- Typing paths directly into NavigationView
- BarPopup event advanced usage
- MaximumItemsToDisplay property
- Popup cancellation logic
- Quick navigation techniques

---

## Quick Start Example

Here's a minimal example of creating a NavigationView with a three-level hierarchy:

```csharp
using Syncfusion.Windows.Forms.Tools;
using Syncfusion.Windows.Forms.Tools.Navigation;

// Create NavigationView
NavigationView navigationView1 = new NavigationView();
navigationView1.Width = 400;
navigationView1.Height = 25;
navigationView1.Location = new System.Drawing.Point(20, 20);

// Create root Bar
Bar rootBar = new Bar();
rootBar.Text = "MyComputer";

// Create child Bars
Bar driveC = new Bar();
driveC.Text = "Local Disk (C:)";

Bar driveD = new Bar();
driveD.Text = "Local Disk (D:)";

Bar programFiles = new Bar();
programFiles.Text = "Program Files";

// Build hierarchy
rootBar.Bars.AddRange(new Bar[] { driveC, driveD });
driveC.Bars.Add(programFiles);

// Add root to NavigationView
navigationView1.Bars.Add(rootBar);

// Set initial selection
navigationView1.SelectedBar = rootBar;

// Add to form
this.Controls.Add(navigationView1);
```

**Result:** A breadcrumb navigation showing "MyComputer" with dropdown access to "C:" and "D:".

## Common Patterns

### File System Navigation Pattern

Mimic Windows Explorer folder navigation:

```csharp
// Root = Computer
Bar computer = new Bar { Text = "This PC" };

// Drives
Bar cDrive = new Bar { Text = "Local Disk (C:)" };
Bar dDrive = new Bar { Text = "Local Disk (D:)" };

// Common folders
Bar users = new Bar { Text = "Users" };
Bar documents = new Bar { Text = "Documents" };
Bar downloads = new Bar { Text = "Downloads" };

// Build hierarchy
computer.Bars.AddRange(new Bar[] { cDrive, dDrive });
cDrive.Bars.Add(users);
users.Bars.AddRange(new Bar[] { documents, downloads });

navigationView1.Bars.Add(computer);
navigationView1.SelectedBar = computer;
```

### Dynamic Bar Creation Based on Data

Populate NavigationView from data source:

```csharp
public void LoadFoldersFromPath(string rootPath, Bar parentBar)
{
    try
    {
        var directories = Directory.GetDirectories(rootPath);
        
        foreach (var dir in directories)
        {
            Bar childBar = new Bar();
            childBar.Text = Path.GetFileName(dir);
            childBar.Tag = dir; // Store full path
            
            parentBar.Bars.Add(childBar);
            
            // Optionally load sub-folders
            // LoadFoldersFromPath(dir, childBar);
        }
    }
    catch (UnauthorizedAccessException)
    {
        // Handle permission errors
    }
}

// Usage
Bar rootBar = new Bar { Text = "C:", Tag = @"C:\" };
LoadFoldersFromPath(@"C:\", rootBar);
navigationView1.Bars.Add(rootBar);
```

### Navigation with History Tracking

Enable users to track and return to previous locations:

```csharp
// Enable history button
navigationView1.ShowHistoryButtons = true;

// Handle BarSelected event to track navigation
navigationView1.BarSelected += (sender, e) =>
{
    string currentPath = GetFullPath(navigationView1.SelectedBar);
    Console.WriteLine($"Navigated to: {currentPath}");
    
    // Update UI based on selection
    LoadContent(currentPath);
};

// Helper to build full path
private string GetFullPath(Bar bar)
{
    List<string> path = new List<string>();
    Bar current = bar;
    
    while (current != null)
    {
        path.Insert(0, current.Text);
        current = current.Parent as Bar;
    }
    
    return string.Join(" > ", path);
}
```

### Custom Navigation Buttons

Add search or refresh buttons to NavigationView:

```csharp
// Create custom search button
CustomButton searchButton = new CustomButton();
searchButton.Name = "searchButton";
searchButton.Image = Properties.Resources.SearchIcon; // Your icon
searchButton.Appearance = ButtonAppearance.Office2007;

// Handle click
searchButton.Click += (sender, e) =>
{
    // Show search dialog or panel
    ShowSearchPanel();
};

// Add to NavigationView
navigationView1.Controls.Add(searchButton);
```

## Key Properties and Events

### Essential Properties

| Property | Type | Description |
|----------|------|-------------|
| `Bars` | `BarCollection` | Collection of root-level Bars |
| `SelectedBar` | `Bar` | Currently displayed Bar in the path |
| `ShowHistoryButtons` | `bool` | Show/hide history dropdown button |
| `VisualStyle` | `VisualStyles` | Apply Office2007, Vista, or Metro styling |
| `ImageList` | `ImageList` | Image collection for Bar icons |

### Bar Properties

| Property | Type | Description |
|----------|------|-------------|
| `Text` | `string` | Display text for the Bar |
| `ImageIndex` | `int` | Index in NavigationView.ImageList |
| `Bars` | `BarCollection` | Child Bars of this Bar |
| `Tag` | `object` | Store custom data (e.g., full path) |

### Important Events

| Event | Description | Common Use |
|-------|-------------|------------|
| `BarSelected` | Fires when user selects a Bar | Load content for selected location |
| `BarPopup` | Fires before dropdown shows | Customize popup items, set max items |
| `Click` | User clicks the control | Handle general interaction |

## Common Use Cases

### Use Case 1: File Explorer with Edit Mode

Allow users to navigate folders visually or type paths directly:

```csharp
// Enable edit mode
navigationView1.AllowEdit = true; // If property exists

// Handle path changes
navigationView1.BarSelected += (sender, e) =>
{
    if (navigationView1.SelectedBar.Tag is string path)
    {
        LoadDirectoryContents(path);
    }
};
```

### Use Case 2: Settings Navigation

Guide users through nested settings categories:

```csharp
Bar settings = new Bar { Text = "Settings" };
Bar appearance = new Bar { Text = "Appearance" };
Bar colors = new Bar { Text = "Colors" };
Bar fonts = new Bar { Text = "Fonts" };

settings.Bars.Add(appearance);
appearance.Bars.AddRange(new Bar[] { colors, fonts });

navigationView1.Bars.Add(settings);
navigationView1.SelectedBar = settings;
```

### Use Case 3: Document Management System

Navigate document categories with custom icons:

```csharp
// Setup ImageList
ImageList imgList = new ImageList();
imgList.Images.Add("folder", Properties.Resources.FolderIcon);
imgList.Images.Add("doc", Properties.Resources.DocumentIcon);
navigationView1.ImageList = imgList;

// Create hierarchy with images
Bar root = new Bar { Text = "Documents", ImageIndex = 0 };
Bar contracts = new Bar { Text = "Contracts", ImageIndex = 0 };
Bar invoices = new Bar { Text = "Invoices", ImageIndex = 0 };

root.Bars.AddRange(new Bar[] { contracts, invoices });
navigationView1.Bars.Add(root);
```

### Use Case 4: Limited Popup Items for Large Hierarchies

Control dropdown size for folders with many subfolders:

```csharp
navigationView1.BarPopup += (sender, e) =>
{
    // Limit items to 10 for better UX
    e.MaximumItemsToDisplay = 10;
    
    // Cancel popup for specific Bars
    if (e.CurrentBar.Text == "EmptyFolder")
    {
        e.Cancel = true;
    }
};
```

## Troubleshooting Tips

**Issue:** Bars not appearing in NavigationView
- **Solution:** Ensure Bars are added to `navigationView1.Bars` collection, not just created
- **Check:** Verify `SelectedBar` is set to make a Bar visible

**Issue:** Images not displaying
- **Solution:** Assign `ImageList` to NavigationView, then set `ImageIndex` on Bars
- **Check:** Ensure ImageIndex values are within ImageList bounds

**Issue:** Dropdown not showing child Bars
- **Solution:** Add child Bars to parent's `Bars` collection: `parentBar.Bars.Add(childBar)`
- **Check:** Verify parent Bar actually has children

**Issue:** History button not visible
- **Solution:** Set `navigationView1.ShowHistoryButtons = true`

**Issue:** Visual style not applied
- **Solution:** Set `VisualStyle` property after control initialization
- **Example:** `navigationView1.VisualStyle = VisualStyles.Office2007;`

## Next Steps

1. **Start with Getting Started:** Read [references/getting-started.md](references/getting-started.md) to set up the control
2. **Build Hierarchy:** Read [references/bar-hierarchy.md](references/bar-hierarchy.md) to create your Bar structure
3. **Add Features:** Read remaining references to add dropdown, history, images, and advanced capabilities
4. **Customize Appearance:** Apply visual styles to match your application theme
5. **Handle Events:** Wire up `BarSelected` and other events to respond to user navigation

For complete implementation details, proceed through the reference guides in the order listed above.
