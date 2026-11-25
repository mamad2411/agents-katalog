---
name: syncfusion-aspnetcore-file-manager
description: Implement the Syncfusion ASP.NET Core File Manager component for file browsing, management, and organization. Use this when building file browsers, implementing file operations (upload/download), customizing toolbars and context menus, enabling drag-and-drop, and configuring data binding for file systems. This skill covers file access, file events, search and filtering, and layout customization.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  components: "File Manager"
---

# Implementing the Syncfusion File Manager Component

The Syncfusion File Manager is a comprehensive, production-ready component for file browsing, management, and organization in web applications. It provides users with an explorer-like interface to navigate file systems, perform file operations (create, rename, delete, copy, move, upload, download), manage file organization, search and filter content, control access permissions, and handle large datasets efficiently through virtualization.

## When to Use This Skill

### File Browsing & Navigation
- **Create a file explorer interface**: Display folder hierarchies with large icons or detailed list views
- **Enable directory navigation**: Support breadcrumb navigation, path configuration, and backward navigation
- **Display file information**: Show file names, sizes, dates, types, and custom properties
- **Implement path tracking**: Maintain and display current directory path
- **Support file previews**: Enable image and file preview capabilities

### File Operations (CRUD)
- **Create folders**: Programmatically create new directories
- **Read & list files**: Display directory contents with filtering and sorting
- **Upload files**: Support single, multiple, and directory uploads with progress tracking
- **Download files**: Enable single and multi-file downloads (with ZIP support)
- **Rename files/folders**: Change names with validation and duplicate handling
- **Copy files/folders**: Duplicate files between locations
- **Move files/folders**: Cut and paste operations with conflict resolution
- **Delete files/folders**: Remove items with confirmation dialogs
- **Get file details**: Retrieve detailed metadata and properties

### File Organization & Search
- **Search files**: Find items by name with case sensitivity options
- **Filter content**: Apply custom filters and display only matching items
- **Sort files**: Order by name, size, date, or custom comparers
- **Multi-selection**: Select multiple items with Ctrl+Click, Shift+Click, and Ctrl+A
- **Range selection**: Drag to select multiple contiguous items
- **Select all/clear selection**: Programmatic selection control

### Upload & Drag-Drop
- **File upload**: Configure upload settings, allowed extensions, file size constraints
- **Batch upload**: Upload multiple files sequentially or in parallel
- **Chunk upload**: Handle large files with pause/resume capability
- **Directory upload**: Upload entire folder structures
- **Drag-and-drop**: Accept files from external sources or file manager items
- **Upload progress**: Track upload status and provide user feedback

### Display Customization
- **View switching**: Toggle between large icons view and details view
- **Column customization**: Configure columns in details view (name, size, date modified, etc.)
- **Template customization**: Create custom rendering for items and navigation pane
- **Thumbnail display**: Show image previews in large icons view
- **Navigation pane**: Configure sidebar with favorite folders and breadcrumb
- **Toolbar customization**: Add, remove, or customize toolbar items
- **Context menu**: Configure context menus for files, folders, and layout

### Advanced Features
- **Virtualization**: Render large file lists efficiently with virtual scrolling
- **Flat data structure**: Load data from arrays without server communication
- **State persistence**: Remember user preferences across sessions
- **RTL support**: Support right-to-left layouts for international applications
- **Localization**: Support multiple languages and locale-specific formatting
- **Security & permissions**: Control access to folders and files by role or user
- **Custom authentication**: Add headers, API keys, or tokens to requests

## Quick Start Example

### Controller Code (FileManagerController.cs)

```csharp
using Microsoft.AspNetCore.Mvc;
using Syncfusion.EJ2.FileManager;

public class FileManagerController : Controller
{
    public IActionResult Index()
    {
        return View();
    }
    
    [HttpPost]
    public IActionResult FileManager(string action, string path)
    {
        // Handle file operations based on action parameter
        if (action == "read")
        {
            // Return list of files and folders for the given path
            return Ok(new {
                cwd = new { name = "Root", hasChild = true, filterPath = "/" },
                files = new object[] { },
                error = (object)null,
                details = (object)null
            });
        }
        
        return Ok();
    }
}
```

### Razor View (Index.cshtml)

```html
<ejs-filemanager id="filemanager"
    path="/"
    width="100%"
    height="400px"
    allowDragAndDrop="true"
    allowMultiSelection="true"
    showThumbnail="true"
    enablePersistence="true">
    <e-filemanager-ajaxsettings url="/FileManager/FileManager"
        downloadUrl="/FileManager/Download"
        uploadUrl="/FileManager/Upload"
        getImageUrl="/FileManager/GetImage">
    </e-filemanager-ajaxsettings>
</ejs-filemanager>
```

## Navigation Guide

Navigate to the appropriate reference file based on your implementation needs:

### Getting Started & Setup
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Component installation and package setup
- Basic initialization and rendering
- AJAX endpoint configuration
- Width and height configuration
- View selection (LargeIcons vs Details)
- Initial path configuration
- Locale and RTL setup
- State persistence configuration

### File Operations (CRUD)
📄 **Read:** [references/file-operations.md](references/file-operations.md)
- Creating new folders programmatically
- Renaming files and folders
- Copying and pasting operations
- Cutting and moving operations
- Deleting files and folders
- Getting file/folder details
- Request and response formats
- Error handling and error codes
- Best practices and patterns

### File Upload & Drag-Drop
📄 **Read:** [references/file-upload.md](references/file-upload.md)
- Upload settings configuration
- File type filtering (allowedExtensions)
- File size constraints (minFileSize, maxFileSize)
- Auto-upload behavior and manual uploads
- Sequential vs parallel upload
- Chunk upload for large files with pause/resume
- Directory (folder) upload support
- Upload events and handlers
- Upload progress tracking

📄 **Read:** [references/drag-and-drop.md](references/drag-and-drop.md)
- Enabling drag-and-drop functionality
- Drop zone configuration
- Internal drag-and-drop (between file manager items)
- External drag-and-drop (from desktop or external sources)
- Drag event handlers (fileDragStart, fileDragging, fileDragStop, fileDropped)
- Preventing default browser behavior
- Multi-file drop support
- Custom drag-and-drop styling

### Display Views & Customization
📄 **Read:** [references/views-overview.md](references/views-overview.md)
- Large icons view (default)
- Details view with configurable columns
- Switching between views dynamically
- Custom large icons template
- Column configuration in details view
- Thumbnail display settings
- File extension display control

📄 **Read:** [references/layouts-customization.md](references/layouts-customization.md)
- Navigation pane settings and visibility
- Breadcrumb navigation and customization
- Toolbar configuration and visibility
- Layout responsive settings
- Template-based customization (navigation pane, large icons)
- Mobile view optimization
- Custom navigation items
- Show/hide hidden items
- Show/hide file extensions

### Selection, Search, Sort & Filter
📄 **Read:** [references/selection-modes.md](references/selection-modes.md)
- Multiple selection (enabled by default)
- Single selection mode
- Range selection with mouse drag
- Checkbox-based selection
- Keyboard shortcuts (Ctrl+A, Ctrl+Click, Shift+Click)
- Selection events (fileSelect, fileSelection)
- Programmatic selection methods
- Clear selection functionality

📄 **Read:** [references/search-sort-filter.md](references/search-sort-filter.md)
- Search functionality and settings
- Case-sensitive search options
- Real-time search as user types
- Sort by name, date modified, size
- Custom sort comparers
- Filter type (contains, startswith, endswith)
- Hidden items visibility
- File extension display

### Toolbar & Context Menu Customization
📄 **Read:** [references/toolbar-customization.md](references/toolbar-customization.md)
- Toolbar item configuration
- Default toolbar items list
- Custom toolbar items and actions
- Enable/disable toolbar items dynamically
- Toolbar visibility settings
- Toolbar layout and styling
- Toolbar click event handling

📄 **Read:** [references/context-menu.md](references/context-menu.md)
- Context menu settings for files, folders, and layout
- Default context menu items
- Enable/disable menu items dynamically
- Menu item event handling
- Custom menu items and actions
- Menu visibility configuration
- Menu events (menuOpen, menuClick, menuClose)

### Events & Methods
📄 **Read:** [references/file-events.md](references/file-events.md)
- **File Operation Events**: beforeDelete, delete, rename, folderCreate, beforeMove, move
- **Selection Events**: fileSelect, fileSelection
- **Navigation Events**: fileOpen, fileLoad
- **Upload Events**: uploadListCreate, success, failure
- **AJAX Events**: beforeSend, beforeDownload, beforeImageLoad
- **Popup Events**: popupOpen, beforePopupOpen, popupClose, beforePopupClose
- **Toolbar/Menu Events**: toolbarClick, toolbarCreate, menuClick, menuOpen, menuClose
- **Search Event**: search
- **Component Lifecycle**: created, destroyed
- Event handler patterns and best practices

📄 **Read:** [references/programmatic-methods.md](references/programmatic-methods.md)
- **Selection Methods**: selectAll(), clearSelection(), getSelectedFiles()
- **File Operation Methods**: createFolder(), deleteFiles(), renameFile(), downloadFiles()
- **Navigation Methods**: openFile(), traverseBackward(), refreshFiles(), refreshLayout()
- **Upload Methods**: uploadFiles()
- **Dialog Methods**: closeDialog()
- **Toolbar/Menu Methods**: disableToolbarItems(), enableToolbarItems(), disableMenuItems(), enableMenuItems()
- **Filter Methods**: filterFiles()
- **Advanced Methods**: getMenuItemIndex(), getToolbarItemIndex()
- Asynchronous operation handling

### Performance & Advanced Features
📄 **Read:** [references/virtualization.md](references/virtualization.md)
- Virtual scrolling for large file lists
- Virtualization configuration
- Virtualization limitations and workarounds
- Performance optimization for large datasets
- Memory management best practices
- Selecting files with virtualization

📄 **Read:** [references/flat-data-customization.md](references/flat-data-customization.md)
- Flat data structure and configuration
- Loading data without server communication
- Local file arrays and JSON data
- Flat data event handling (create, delete, rename, move)
- UI customization (extensions, hidden items, thumbnails)
- Custom file provider implementation
- Lazy loading patterns

### Security & Access Control
📄 **Read:** [references/security-basics.md](references/security-basics.md)
- HTML sanitization to prevent XSS attacks
- Input validation and error handling
- SQL injection prevention
- File type validation
- Common security vulnerabilities
- Safe file handling practices
- Permission-based access control

📄 **Read:** [references/authentication-headers.md](references/authentication-headers.md)
- Adding headers to AJAX requests
- Before Send event for custom headers
- Bearer token authentication
- API key authentication
- Basic authentication
- Before Download event handling
- Before Image Load event handling
- OAuth token refresh patterns
- Request header patterns and examples

### Server Integration
📄 **Read:** [references/server-integration.md](references/server-integration.md)
- ASP.NET Core backend implementation
- Node.js backend implementation
- Request/response patterns and formats
- Upload request with chunks
- Error handling strategies
- Resumable upload patterns
- File operation request/response structure

### Complete API Reference
📄 **Read:** [references/api-complete-reference.md](references/api-complete-reference.md)
- **All Properties**: ajaxSettings, path, view, width, height, and 40+ more
- **All Methods**: selectAll(), clearSelection(), createFolder(), deleteFiles(), renameFile(), downloadFiles(), and 15+ more
- **All Events**: beforeDelete, delete, fileSelect, beforeSend, beforeDownload, beforeImageLoad, and 20+ more
- **Type definitions**: FileData, AjaxSettingsModel, UploadSettingsModel, etc.
- **Complete working examples**: Full-featured implementations with all features

## Common Patterns

### Pattern 1: Basic Setup with Toolbar and Context Menu

**View Code (Index.cshtml)**:
```html
<ejs-filemanager id="filemanager"
    path="/"
    width="100%"
    height="400px">
    <e-filemanager-ajaxsettings url="/FileManager/FileManager"
        uploadUrl="/FileManager/Upload"
        downloadUrl="/FileManager/Download"
        getImageUrl="/FileManager/GetImage">
    </e-filemanager-ajaxsettings>
    <e-filemanager-toolbarsettings items="@new string[] {'NewFolder', 'Upload', 'Cut', 'Copy', 'Paste', 'Delete', 'Download', 'Rename', 'Refresh'}">
    </e-filemanager-toolbarsettings>
    <e-filemanager-contextmenusettings file="@new string[] {'Open', 'Delete', 'Rename', 'Download', 'Details'}"
        folder="@new string[] {'Open', 'Delete', 'Rename', 'Download', 'Details'}"
        layout="@new string[] {'SortBy', 'View', 'Refresh', 'NewFolder', 'Upload'}">
    </e-filemanager-contextmenusettings>
</ejs-filemanager>
```

### Pattern 2: Upload with Validation and Constraints

**View Code (Index.cshtml)**:
```html
<ejs-filemanager id="filemanager" path="/">
    <e-filemanager-ajaxsettings url="/FileManager/FileManager"
        uploadUrl="/FileManager/Upload">
    </e-filemanager-ajaxsettings>
    <e-filemanager-uploadsettings autoUpload="true"
        allowedExtensions=".jpg,.png,.pdf,.doc,.docx"
        minFileSize="1024"
        maxFileSize="5242880">
    </e-filemanager-uploadsettings>
</ejs-filemanager>
```

### Pattern 3: Details View with Custom Columns

**View Code (Index.cshtml)**:
```html
<ejs-filemanager id="filemanager" view="Details">
    <e-filemanager-ajaxsettings url="/FileManager/FileManager">
    </e-filemanager-ajaxsettings>
    <e-filemanager-detailsviewsettings>
        <e-filemanager-detailsviewsettings-columns>
            <e-detailsviewcolumn field="name" headerText="Name" minWidth="150" width="200"></e-detailsviewcolumn>
            <e-detailsviewcolumn field="_fm_modified" headerText="Date Modified" type="dateTime" minWidth="120" width="150"></e-detailsviewcolumn>
            <e-detailsviewcolumn field="size" headerText="Size" minWidth="90" width="120"></e-detailsviewcolumn>
        </e-filemanager-detailsviewsettings-columns>
    </e-filemanager-detailsviewsettings>
</ejs-filemanager>
```

### Pattern 4: Programmatic File Operations

**View Code (Index.cshtml)**:
```html
<button onclick="selectAllAndDelete()">Select All & Delete</button>

<ejs-filemanager id="filemanager">
    <e-filemanager-ajaxsettings url="/FileManager/FileManager">
    </e-filemanager-ajaxsettings>
</ejs-filemanager>

<script>
    function selectAllAndDelete() {
        var filemanager = document.getElementById('filemanager').ej2_instances[0];
        filemanager.selectAll();
        var selected = filemanager.getSelectedFiles();
        var names = selected.map(function(f) { return f.name; });
        filemanager.deleteFiles(names);
    }
</script>
```

### Pattern 5: Search with Real-Time Filtering

**View Code (Index.cshtml)**:
```html
<ejs-filemanager id="filemanager" search="onSearch">
    <e-filemanager-ajaxsettings url="/FileManager/FileManager">
    </e-filemanager-ajaxsettings>
    <e-filemanager-searchsettings allowSearchOnTyping="true"
        filterType="contains"
        ignoreCase="true">
    </e-filemanager-searchsettings>
</ejs-filemanager>

<script>
    function onSearch(args) {
        console.log('Search query:', args.searchString);
    }
</script>
```

### Pattern 6: Drag-Drop with Upload

**View Code (Index.cshtml)**:
```html
<ejs-filemanager id="filemanager"
    allowDragAndDrop="true"
    fileDragStart="onFileDragStart"
    fileDragStop="onFileDragStop"
    fileDropped="onFileDropped">
    <e-filemanager-ajaxsettings url="/FileManager/FileManager"
        uploadUrl="/FileManager/Upload">
    </e-filemanager-ajaxsettings>
    <e-filemanager-uploadsettings autoUpload="true"
        allowedExtensions=".jpg,.png,.pdf">
    </e-filemanager-uploadsettings>
</ejs-filemanager>

<script>
    function onFileDragStart(args) {
        console.log('Drag started:', args.fileDetails);
    }
    
    function onFileDragStop(args) {
        console.log('Drag stopped');
    }
    
    function onFileDropped(args) {
        console.log('File dropped:', args.fileDetails);
    }
</script>
```

### Pattern 7: Event-Driven File Operations

**View Code (Index.cshtml)**:
```html
<ejs-filemanager id="filemanager"
    beforeDelete="beforeDelete"
    delete="onDelete"
    beforeSend="beforeSend">
    <e-filemanager-ajaxsettings url="/FileManager/FileManager">
    </e-filemanager-ajaxsettings>
</ejs-filemanager>

<script>
    function beforeDelete(args) {
        console.log('Before delete:', args.fileDetails);
        // Validate or prevent deletion
        var isReadOnly = args.fileDetails.some(function(f) { return f.isReadOnly; });
        if (isReadOnly) {
            args.cancel = true;
        }
    }
    
    function onDelete(args) {
        console.log('File deleted:', args.fileDetails);
        // Update UI or log action
    }
    
    function beforeSend(args) {
        // Add custom headers
        args.ajaxSettings.headers = args.ajaxSettings.headers || {};
        args.ajaxSettings.headers['Authorization'] = 'Bearer ' + getToken();
    }
</script>
```

### Pattern 8: Virtual Scrolling for Large Datasets

**View Code (Index.cshtml)**:
```html
<ejs-filemanager id="filemanager"
    enableVirtualization="true"
    height="600px"
    width="100%">
    <e-filemanager-ajaxsettings url="/FileManager/FileManager">
    </e-filemanager-ajaxsettings>
</ejs-filemanager>
```

### Pattern 9: State Persistence

**View Code (Index.cshtml)**:
```html
<ejs-filemanager id="filemanager"
    enablePersistence="true">
    <e-filemanager-ajaxsettings url="/FileManager/FileManager">
    </e-filemanager-ajaxsettings>
</ejs-filemanager>
<!-- Persists: view type, current path, selected items -->
```

### Pattern 10: Localization and RTL

**View Code (Index.cshtml)**:
```html
<ejs-filemanager id="filemanager"
    locale="ar-AE"
    enableRtl="true">
    <e-filemanager-ajaxsettings url="/FileManager/FileManager">
    </e-filemanager-ajaxsettings>
</ejs-filemanager>
```

## Key Properties Summary

**Essential Configuration:**
- `ajaxSettings` - Server communication endpoints (url, uploadUrl, downloadUrl, getImageUrl)
- `path` - Current directory path
- `width` / `height` - Component dimensions
- `view` - Display mode (LargeIcons or Details)
- `allowDragAndDrop` - Enable drag-and-drop functionality
- `allowMultiSelection` - Enable multiple file selection
- `showThumbnail` - Display image thumbnails

**Upload Settings:**
- `uploadSettings.autoUpload` - Automatically upload files
- `uploadSettings.allowedExtensions` - Restrict file types
- `uploadSettings.maxFileSize` - Maximum file size limit
- `uploadSettings.directoryUpload` - Enable folder uploads
- `uploadSettings.sequentialUpload` - Upload files one by one

**Customization:**
- `toolbarSettings` - Configure toolbar items and visibility
- `contextMenuSettings` - Configure context menu for different contexts
- `navigationPaneSettings` - Configure left sidebar
- `detailsViewSettings` - Configure columns in details view
- `searchSettings` - Configure search behavior

**Advanced:**
- `enableVirtualization` - Optimize rendering for large lists
- `enablePersistence` - Remember user preferences
- `enableRtl` - Right-to-left layout support
- `cssClass` - Apply custom CSS styling
- `showFileExtension` - Display file extensions
- `showHiddenItems` - Show/hide hidden files
- `showItemCheckBoxes` - Display checkboxes for selection

## Common Use Cases

**Use Case 1: Document Management System**
- Users browse uploaded documents by folder
- Search and filter documents by metadata
- Download or preview documents
- Upload new documents with access control

**Use Case 2: Image Gallery Manager**
- Browse image folders with thumbnail previews
- Drag-and-drop images for organization
- Rename and organize image collections
- Download selected images as ZIP

**Use Case 3: Content Administration**
- Manage website content folders
- Create and organize folder hierarchies
- Rename and delete content items
- Control user access to specific folders

**Use Case 4: Cloud Storage Client**
- Full file management operations
- Multi-file upload with progress tracking
- Persistent user preferences across sessions
- Synchronized state

---


