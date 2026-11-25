---
name: syncfusion-angular-file-manager
description: "Implement the Syncfusion Angular File Manager component for file browsing, management, and operations. Use this skill whenever the user needs to create a file manager interface, handle file operations like upload/download/delete, manage folders, or customize file browsing experiences in Angular applications."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "File Manager"
---

# Implementing the Syncfusion Angular File Manager Component

The File Manager is a powerful graphical user interface component for managing file systems. It enables users to perform essential file operations—accessing, editing, sorting, uploading, downloading, and organizing files and folders—with an intuitive interface and comprehensive navigation functionality.

## When to Use This Skill

Use the File Manager component when you need to:
- **Browse and navigate** files and folders in a file system
- **Perform file operations** (create, delete, rename, upload, download)
- **Display files** in different view modes (details view, large icons view)
- **Implement drag-and-drop** file management
- **Handle large file sets** efficiently with virtualization
- **Customize** toolbar, context menu, and file display
- **Support** multi-selection, sorting, and localization

## Component Overview & Key Features

### Core Capabilities
- **File Operations**: Read, create, delete, rename, upload, download files
- **Navigation**: Breadcrumb navigation, navigation pane, folder hierarchy
- **View Options**: Details view (sorted list) and Large Icons view (thumbnail display)
- **User Interaction**: Multi-selection, drag-and-drop, right-click context menu
- **Performance**: UI virtualization for large file sets, state persistence
- **Customization**: Toolbar/context menu customization, CSS theming, custom icons
- **Accessibility**: RTL support, localization, ARIA attributes

### Architecture
- Server-based file operations via `ajaxSettings`
- Or client-side data binding with `fileSystemData` (flat or nested JSON)
- Feature modules: Navigation Pane, Toolbar, Details View, Virtualization
- Event-driven architecture for custom workflows

## Documentation and Navigation Guide

### API Reference (Start Here for API Details)
📄 **Read:** [references/api-reference-complete.md](references/api-reference-complete.md)
- Complete component properties with descriptions
- FileData interface for client-side binding
- Configuration models and best practices
- Service providers and utility functions

### Methods and Events Reference
📄 **Read:** [references/methods-and-events.md](references/methods-and-events.md)
- Complete list of all component methods with examples
- All component events with event arguments
- Event parameter interfaces and descriptions
- Practical examples for each method and event

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Prerequisites (Angular 4+, TypeScript 2.6+)
- Angular project setup and CLI commands
- Package installation (Ivy vs ngcc compatibility)
- CSS theme imports and styling
- Basic component initialization
- ajaxSettings configuration (file operations, download, upload, preview URLs)
- Initial view and component rendering

### File Operations
📄 **Read:** [references/file-operations.md](references/file-operations.md)
- Core operations: read, create, delete, rename, upload, download, copy, move
- File system provider configuration
- Server integration patterns
- Custom file providers (Google Drive, Amazon S3, Azure)
- Directory upload support
- Error handling and validation
- Request/response patterns

### Request and Response Parameters
📄 **Read:** [references/request-response-parameters-reference.md](references/request-response-parameters-reference.md)
- Complete response parameters for ALL 11 operations
- Request structure and parameters for each operation
- Response format and structure specifications
- FileManagerDirectoryContent interface definition
- DetailsObject and error response formats
- Request/response examples for every operation
- Error codes and error handling patterns
- Common data structures and interfaces
- Best practices for backend implementation

### Upload Customizations
📄 **Read:** [references/upload-customizations.md](references/upload-customizations.md)
- Directory upload configuration (directoryUpload property)
- Sequential upload setup (sequentialUpload property)
- Chunk upload for large files (chunkSize configuration)
- Auto-upload behavior control
- File size validation (minFileSize, maxFileSize)
- File type restrictions (allowedExtensions)
- Upload events (beforeSend, onSuccess, onFailure)
- Backend implementation examples (ASP.NET Core)
- 3 practical examples covering image-only, document, and complete upload configs

### File System Provider Reference
📄 **Read:** [references/file-system-provider-reference.md](references/file-system-provider-reference.md)
- Overview of 9 different file system providers
- Physical file system provider (on-premise local files)
- Azure cloud file system provider (Azure Blob Storage)
- Amazon S3 cloud file provider (AWS object storage)
- SharePoint file provider (Microsoft SharePoint integration)
- File Transfer Protocol provider (FTP server access)
- SQL database file system provider (database-backed storage)
- Node.js file system provider (lightweight Node.js runtime)
- Google Drive file system provider (Google Drive integration)
- Firebase Realtime Database provider (serverless cloud database)
- Setup instructions for each provider
- Configuration examples and best practices
- Provider comparison table
- Quick selection guide

### Views and Layout
📄 **Read:** [references/views-and-layout.md](references/views-and-layout.md)
- Details view (sorted file list with columns)
- Large Icons view (thumbnail display)
- Switching views dynamically or at initialization
- Initial view configuration
- CSS class customization for styling
- View-specific settings and configurations

### Navigation Features
📄 **Read:** [references/navigation-features.md](references/navigation-features.md)
- Breadcrumb navigation (folder hierarchy tracking)
- Navigation pane configuration (left sidebar with folder tree)
- Path specification and dynamic navigation
- Folder hierarchy traversal
- Showing/hiding navigation elements

### Data Structures
📄 **Read:** [references/data-structures.md](references/data-structures.md)
- Flat JSON data binding (no backend required)
- Nested items (folder hierarchies in local data)
- fileData interface and properties (name, size, date, isFile, hasChild, etc.)
- Parent-child relationships via parentId
- Flat vs nested approaches and trade-offs
- Server-based vs client-side data

### Nested Items Integration
📄 **Read:** [references/nested-items-integration.md](references/nested-items-integration.md)
- Dialog nesting with file selection pattern
- Tab nesting (multiple File Managers per tab)
- Splitter nesting (side-by-side layout)
- Accordion nesting (categorized file access)
- Managing multiple nested File Manager state
- Height calculation strategies
- Dimension management best practices
- 2 practical examples: file upload dialog, tabbed file management

### Drag and Drop
📄 **Read:** [references/drag-and-drop.md](references/drag-and-drop.md)
- Enabling drag-and-drop functionality
- Drop target configuration
- File move operations via dragging
- Drag event handling (fileDragStart, fileDragging, fileDragStop, fileDropped)
- Constraints and drop restrictions
- Visual feedback during drag operations

### Virtualization
📄 **Read:** [references/virtualization.md](references/virtualization.md)
- What is UI virtualization and performance benefits
- Module injection (VirtualizationService)
- Enabling virtualization (enableVirtualization property)
- Handling large file sets (100s-1000s of files)
- Memory optimization and scrolling performance
- Virtual scrolling in details and large icons views

### Sorting and Filtering
📄 **Read:** [references/sorting-and-filtering.md](references/sorting-and-filtering.md)
- Custom sorting via sortComparer function
- Natural sorting (like Windows Explorer)
- Sort orders (ascending/descending)
- Multi-column sorting in details view
- Column-specific sortComparer definitions
- Imported sortComparer utility or custom implementations

### Toolbar Customization
📄 **Read:** [references/toolbar-customization.md](references/toolbar-customization.md)
- Toolbar configuration and items
- Default toolbar items (NewFolder, Upload, View, Refresh, Cut, Copy, Paste, Delete, Download, Rename)
- Adding custom toolbar items with templates
- Modifying toolbar item properties
- Toolbar icons (Syncfusion, Font Awesome, custom SVG)
- Template-based toolbar items (checkboxes, dropdowns)
- Toolbar click events and event handling
- Conditional toolbar items based on selection

### Context Menu Customization
📄 **Read:** [references/context-menu-customization.md](references/context-menu-customization.md)
- Default context menu items (Open, Cut, Copy, Paste, Delete, Rename, Download)
- Adding custom context menu items
- Context menu configuration for files, folders, and layout
- Menu events (menuOpen, menuClose, menuClick)
- Dynamic menu modification and conditional items
- Adding icons to menu items
- Custom menu actions and implementations
- Submenu support

### Access Control and Permissions
📄 **Read:** [references/access-control-and-permissions.md](references/access-control-and-permissions.md)
- Permission model and FileData permission structure
- Implementing role-based access control (RBAC)
- File-level and folder-level permissions
- Backend permission rules configuration
- Access rules with Permission enumeration (Allow/Deny)
- Frontend permission handling and UI disabling
- Administrator, Editor, and Viewer role examples
- Audit logging and compliance

### Authentication and Custom Values
📄 **Read:** [references/authentication-and-custom-values.md](references/authentication-and-custom-values.md)
- beforeSend event for adding authentication headers
- JWT token authentication implementation
- Bearer token patterns
- Custom headers (API keys, request IDs, correlation IDs)
- Custom data passing with requests
- Query parameters and body data
- CORS configuration and cross-origin requests
- OAuth2 token refresh patterns
- Multi-tenant file manager setup
- Audit trail and request logging

### Custom File Providers
📄 **Read:** [references/custom-file-provider.md](references/custom-file-provider.md)
- Custom file provider architecture
- Required API endpoints (FileOperations, Upload, Download, GetImage)
- Request/response format specifications
- ASP.NET Core custom backend implementation
- Azure Blob Storage integration
- AWS S3 integration
- Database-backed file system (SQL)
- Google Drive and cloud storage patterns
- Implementing ICustomFileService interface

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Multi-selection of files and folders
- State persistence (enablePersistence property)
- Maintaining view, path, and selected items across page reload
- Ajax events (success, failure)
- Component lifecycle (created event)
- Refresh file operations programmatically
- Multiple file selection with bulk operations

### UI Customizations
📄 **Read:** [references/ui-customizations.md](references/ui-customizations.md)
- Large icon customization (size, layout, styling)
- Custom file type icons mapping
- showFileExtension property and dynamic control
- showHiddenItems configuration with server-side filtering
- Tooltip customization with file information
- allowMultiSelection control with single/multi toggle
- Multi-selection limitation patterns
- **showThumbnail**: Control thumbnail display (performance tuning for large collections)
- **showItemCheckBoxes**: Enable selection checkboxes (mobile-friendly & accessibility)
- **enableHtmlSanitizer**: Security property to prevent XSS attacks (CRITICAL: keep enabled)
- **popupTarget**: Specify popup/dialog container (required for nested File Managers)
- 15+ working code examples with CSS patterns and advanced configurations
- Complete UI customization examples

### Navigation Items Customization
📄 **Read:** [references/navigation-items-customization.md](references/navigation-items-customization.md)
- navigationPaneTemplate basic and advanced usage
- Custom item rendering with hierarchical styling
- Icon and badge integration patterns
- CSS styling approaches for navigation items
- Dynamic theme application (light/dark toggle)
- Path-based icon customization
- Professional navigation design patterns
- 1 comprehensive professional navigation example

### Customization and Styling
📄 **Read:** [references/customization-styling.md](references/customization-styling.md)
- CSS class customization (cssClass property)
- Theme customization and Theme Studio integration
- Custom thumbnails (showThumbnail property)
- Custom icon display for files and folders
- Responsive design and container sizing
- Advanced styling examples
- CSS variable overrides

### Localization and RTL
📄 **Read:** [references/localization-and-rtl.md](references/localization-and-rtl.md)
- Right-to-left (RTL) language support (enableRtl property)
- Localization library (l10) integration
- Language configuration and switching
- Custom text and message localization
- Regional date/time formatting

## Quick Start Example

### Basic File Manager Setup

```typescript
import { Component } from '@angular/core';
import { FileManagerModule, NavigationPaneService, ToolbarService, DetailsViewService } from '@syncfusion/ej2-angular-filemanager';

@Component({
  imports: [FileManagerModule],
  providers: [NavigationPaneService, ToolbarService, DetailsViewService],
  standalone: true,
  selector: 'app-root',
  template: `<ejs-filemanager 
    id='file-manager' 
    [ajaxSettings]='ajaxSettings' 
    height="500px">
  </ejs-filemanager>`
})
export class AppComponent {
  public ajaxSettings = {
    url: 'https://ej2-aspcore-service.azurewebsites.net/api/FileManager/FileOperations',
    getImageUrl: 'https://ej2-aspcore-service.azurewebsites.net/api/FileManager/GetImage',
    uploadUrl: 'https://ej2-aspcore-service.azurewebsites.net/api/FileManager/Upload',
    downloadUrl: 'https://ej2-aspcore-service.azurewebsites.net/api/FileManager/Download'
  };
}
```

### With Local JSON Data (No Backend)

```typescript
import { Component } from '@angular/core';
import { FileManagerModule } from '@syncfusion/ej2-angular-filemanager';
import { FileData } from '@syncfusion/ej2-filemanager';

@Component({
  imports: [FileManagerModule],
  standalone: true,
  selector: 'app-root',
  template: `<ejs-filemanager 
    id='file-manager' 
    [fileSystemData]='fileData' 
    height="500px">
  </ejs-filemanager>`
})
export class AppComponent {
  public fileData: FileData[] = [
    {
      id: '1',
      name: 'Documents',
      isFile: false,
      hasChild: true,
      parentId: null,
      dateModified: new Date('2024-01-15')
    },
    {
      id: '2',
      name: 'Resume.pdf',
      isFile: true,
      hasChild: false,
      parentId: '1',
      size: 204800,
      dateModified: new Date('2024-01-10')
    }
  ];
}
```

## Common Patterns

### Pattern 1: Server Integration with Full Configuration
**Use when:** Building a production file manager with backend services

```typescript
// app.component.ts
ajaxSettings = {
  url: '/api/FileManager/FileOperations',
  getImageUrl: '/api/FileManager/GetImage',
  uploadUrl: '/api/FileManager/Upload',
  downloadUrl: '/api/FileManager/Download'
};

toolbarSettings = {
  items: ['NewFolder', 'Upload', 'Download', 'Delete', 'Refresh', 'View', 'Details']
};
```

### Pattern 2: Local Data with Custom Formatting
**Use when:** Data comes from API but doesn't need backend file operations

Transform API response into fileData format:
```typescript
fileData = this.apiService.getFiles().map(file => ({
  id: file.id,
  name: file.fileName,
  isFile: file.type === 'file',
  parentId: file.parentId || null,
  size: file.fileSize,
  dateModified: new Date(file.modified)
}));
```

### Pattern 3: Virtualization for Large Datasets
**Use when:** Handling 1000+ files

```typescript
// Inject VirtualizationService, enable enableVirtualization
providers: [VirtualizationService]

// In template
<ejs-filemanager 
  [enableVirtualization]="true"
  [view]="'Details'"
  ...>
</ejs-filemanager>
```

### Pattern 4: Multi-Selection with Actions
**Use when:** Bulk file operations needed

```typescript
onDownloadSelected() {
  const selected = this.fileManager.selectedItems;
  // Download multiple files (server returns ZIP)
}
```

## Key Props and Settings

### Core Configuration
| Property | Type | Purpose |
|----------|------|---------|
| `ajaxSettings` | AjaxSettingsModel | Server endpoints for file operations (url, uploadUrl, downloadUrl, getImageUrl) |
| `fileSystemData` | FileData[] | Local JSON data (alternative to ajaxSettings) |
| `path` | string | Initial directory path to display |
| `view` | ViewType | Initial view mode: 'Details' or 'LargeIcons' |
| `height` | string \| number | Component height |
| `width` | string \| number | Component width |

### Selection & Multi-Selection
| Property | Type | Purpose |
|----------|------|---------|
| `allowMultiSelection` | boolean | Enable Ctrl+Click and Shift+Click selection |
| `enableRangeSelection` | boolean | Enable drag-based selection (Windows Explorer style) |

### File Operations
| Property | Type | Purpose |
|----------|------|---------|
| `allowDragAndDrop` | boolean | Enable drag-and-drop file movement |
| `uploadSettings` | UploadSettingsModel | Upload config (maxFileSize, minFileSize, autoUpload, allowedExtensions, directoryUpload) |
| `searchSettings` | SearchSettingsModel | Search config (filterType, allowSearchOnTyping, caseSensitive) |

### Display & Performance
| Property | Type | Purpose |
|----------|------|---------|
| `showThumbnail` | boolean | Display image thumbnails |
| `showHiddenItems` | boolean | Show/hide hidden files and folders (default: false) |
| `showFileExtension` | boolean | Display file extensions (default: true) |
| `enableVirtualization` | boolean | Virtualize large file sets (1000+ items) |
| `enablePersistence` | boolean | Persist view, path, and selected items |
| `enableRtl` | boolean | Right-to-left layout support |
| `enableHtmlSanitizer` | boolean | Sanitize HTML for security |

### UI Customization
| Property | Type | Purpose |
|----------|------|---------|
| `toolbarSettings` | ToolbarSettingsModel | Toolbar items and visibility |
| `navigationPaneSettings` | NavigationPaneSettingsModel | Left sidebar configuration |
| `contextMenuSettings` | ContextMenuSettingsModel | Right-click menu customization |
| `detailsViewSettings` | DetailsViewSettingsModel | Details view columns and sorting |
| `navigationPaneTemplate` | string \| object | Custom template for navigation nodes |
| `largeIconsTemplate` | string \| object | Custom template for large icons view |
| `cssClass` | string | CSS class for theming |
| `locale` | string | Localization culture (e.g., 'de-DE', 'ja-JP') |

### Sorting & Comparison
| Property | Type | Purpose |
|----------|------|---------|
| `sortComparer` | Function | Custom sort function (Windows Explorer-like sorting available) |

## Decision Tree: Choose Your Approach

```
Do you have a backend file service? 
  ├─ YES → Use ajaxSettings (see Getting Started)
  │        └─ Need to handle 1000+ files?
  │            ├─ YES → Enable enableVirtualization
  │            └─ NO → Standard setup
  │
  └─ NO → Use fileSystemData with local JSON
           └─ Need to organize hierarchically?
               ├─ YES → Use nested items with parentId
               └─ NO → Use flat data structure
```

---

**Next Steps:** Select the reference that matches your current task and dive into implementation details with code examples and best practices.
