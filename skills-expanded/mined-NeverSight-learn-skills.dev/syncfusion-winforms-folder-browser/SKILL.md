---
name: syncfusion-winforms-folder-browser
description: Implement Windows Forms FolderBrowser dialog for folder selection. Use this when implementing folder selection dialogs, directory browsing, or folder path selection in applications. Covers assembly setup, dialog initialization, location/style configuration, callback events, and common browsing patterns.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing FolderBrowser in Windows Forms

The Syncfusion FolderBrowser control provides a wrapper around the Win32 Shell Folder Browser API, enabling developers to display a folder selection dialog with .NET-centric properties, events, and methods.

## When to Use This Skill

Use this skill when you need to:
- Display a folder selection dialog to users
- Allow users to browse and select directory paths
- Customize dialog behavior (restrict to filesystem, show computers, etc.)
- Handle folder selection with callback validation
- Configure starting locations for browsing
- Add auto-complete file path functionality

## Component Overview

**FolderBrowser** is a dialog-based component that:
- Shows a native Windows folder selection dialog
- Abstracts complex Win32 Shell API interactions
- Supports various browsing styles and restrictions
- Provides callback events for validation
- Enables custom starting locations and path selection
- Works with both designer and code-based implementations

## Key Capabilities

| Feature | Purpose |
|---------|---------|
| **Location Settings** | Configure where browsing starts (MyComputer, CustomStartLocation, etc.) |
| **Style Options** | Control dialog behavior (RestrictToFilesystem, BrowseForComputer, ShowTextBox, etc.) |
| **Path Selection** | Automatically scroll and highlight specific folder paths |
| **Callback Events** | Validate folder selection in real-time during browsing |
| **Text Customization** | Set dialog descriptions and status messages |
| **Auto-Complete** | Enable textbox with folder path suggestions |

## Quick Start Example

```csharp
// Create and display a basic folder browser dialog
FolderBrowser folderBrowser = new FolderBrowser();

// Set starting location to My Computer
folderBrowser.StartLocation = Syncfusion.Windows.Forms.FolderBrowserFolder.MyComputer;

// Configure dialog styles
folderBrowser.Style = Syncfusion.Windows.Forms.FolderBrowserStyles.RestrictToFilesystem | 
                      Syncfusion.Windows.Forms.FolderBrowserStyles.NewDialogStyle;

// Show dialog and get selected path
if (folderBrowser.ShowDialog() == DialogResult.OK)
{
    string selectedFolder = folderBrowser.DirectoryPath;
    MessageBox.Show($"Selected: {selectedFolder}");
}
```

## Common Patterns

### Pattern 1: Basic Folder Selection
Show a simple dialog allowing users to browse and select any folder in the filesystem.

```csharp
var folderBrowser = new FolderBrowser();
folderBrowser.Style = FolderBrowserStyles.RestrictToFilesystem;
folderBrowser.ShowDialog();
```

### Pattern 2: Custom Starting Location
Start browsing from a specific path with pre-highlighted selection.

```csharp
folderBrowser.StartLocation = FolderBrowserFolder.CustomStartLocation;
folderBrowser.CustomStartLocation = "C:\\Program Files";
folderBrowser.SelectLocation = "C:\\Program Files\\Syncfusion";
folderBrowser.ShowDialog();
```

### Pattern 3: Multiple Style Flags
Combine multiple styles to enable text input and validation.

```csharp
folderBrowser.Style = FolderBrowserStyles.ShowTextBox | 
                      FolderBrowserStyles.Validate | 
                      FolderBrowserStyles.NewDialogStyle;
```

### Pattern 4: With Callback Validation
Handle folder selection validation through callback events.

```csharp
folderBrowser.FolderBrowserCallback += FolderBrowser_Callback;
folderBrowser.ShowDialog();

private void FolderBrowser_Callback(object sender, FolderBrowserCallbackEventArgs e)
{
    // Validate path or update status
    if (IsValidFolder(e.Path))
        e.BrowseCallbackText = $"Selected: {e.Path}";
    else
        e.Dismiss = true;
}
```

## Documentation Navigation

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly references and NuGet deployment
- Adding control via designer
- Adding control via code
- Basic dialog initialization and display
- Complete working example

### Location Settings
📄 **Read:** [references/location-settings.md](references/location-settings.md)
- StartLocation property with predefined locations
- CustomStartLocation for custom browsing paths
- SelectLocation for automatic path highlighting
- DirectoryPath property for retrieving selected path
- Practical code examples

### Style Options
📄 **Read:** [references/style-options.md](references/style-options.md)
- Style property overview and all available flags
- RestrictToFilesystem and domain restrictions
- BrowseForComputer and BrowseForEverything
- ShowTextBox and auto-complete functionality
- NewDialogStyle for resizable dialogs
- Combining multiple style flags

### Text Customization
📄 **Read:** [references/text-customization.md](references/text-customization.md)
- Description property for dialog titles
- Setting custom dialog text
- StatusText usage in callbacks
- Best practices for user-friendly messaging

### Callback Events
📄 **Read:** [references/callback-events.md](references/callback-events.md)
- FolderBrowserCallback event handling
- FolderBrowserCallbackEventArgs members
- Dismiss property for dialog control
- BrowseCallbackText and status updates
- FolderBrowserMessage types and meanings
- Real-time validation patterns

### Common Patterns
📄 **Read:** [references/common-patterns.md](references/common-patterns.md)
- Complete folder selection workflow
- Error handling and path validation
- Combining styles for specific scenarios
- Integration with file system operations
- Performance considerations

## Key Properties

| Property | Type | Purpose |
|----------|------|---------|
| `StartLocation` | FolderBrowserFolder | Sets the root folder for browsing |
| `CustomStartLocation` | string | Custom path when StartLocation is CustomStartLocation |
| `SelectLocation` | string | Path to auto-highlight during browsing |
| `DirectoryPath` | string | Gets the selected folder path |
| `Style` | FolderBrowserStyles | Flags controlling dialog appearance and behavior |
| `Description` | string | Sets the description text in the dialog |

## Assembly Requirements

Before using FolderBrowser, add the following assembly reference:
- **Syncfusion.Shared.Base.dll**

Or install via NuGet:
```
Install-Package Syncfusion.Shared.Base
```

---

**Next Steps:** Choose a reference document above based on your specific need, or start with Getting Started if you're new to this component.
