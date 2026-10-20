# Autodesk Vault Data Standard Extension

## Project Overview
This is a **deployed Vault 2027 extension** implementing the Autodesk Data Standard for PLM/PDM workflows. The codebase integrates with Autodesk Vault Professional, Inventor, and AutoCAD to enforce[...]

**Key Architecture:**
- **CAD/** - Inventor/AutoCAD client-side dialogs and PowerShell event handlers
- **Vault/** - Vault Explorer client dialogs and menu commands  
- **CAD.Custom/** & **Vault.Custom/** - Customer-specific overrides and extensions (ADSK.QS.* files)
- **Root DLLs** - .NET assemblies providing core extensibility framework (dataStandard4Vault.dll, CreateObject.dll, etc.)

## Technology Stack
- **Languages**: PowerShell 7.6.2 (UI logic, rules script), C# (.NET 10 compiled DLLs), XAML (WPF dialogs)
- **Framework**: Autodesk Vault API (Connectivity.Explorer.Extensibility, Connectivity.WebServices)
- **CAD Integration**: Inventor API, AutoCAD API via .NET interop
- **Configuration**: XML (.cfg, .xaml), JSON (CustomEntityDefinitions.json)

## Critical Patterns

### 1. PowerShell Event-Driven Dialog System
PowerShell scripts are invoked at specific lifecycle events. Function naming conventions trigger automatic execution:

```powershell
# CAD/addins/Default.ps1 or Vault/addinVault/Default.ps1
function InitializeWindow { }      # Called on dialog load
function AddinLoaded { }           # Called on add-in activation
function ActivateOkButton { }      # Returns bool for OK button state (Vault only)
function Validate { }              # Master validation orchestrator
function ValidateFile* { }         # Auto-discovered file validation functions
function ValidateFolder* { }       # Auto-discovered folder validation functions
```

**Customer extensions override base behavior** - `ADSK.QS.Default.ps1` in `.Custom` folders takes precedence over base `Default.ps1`.

### 2. Property System (`$Prop` global variable)
All dialog fields are accessed via `$Prop["PropertyName"]`:
- System properties: `_FileName`, `_FolderName`, `_CreateMode`, `_ReadOnly`, `_VaultVirtualPath`
- Custom properties: `DocNumber`, `Title`, `Description`, `Project`, `Revision`, etc.
- Setting values: `$Prop["Title"].Value = "New Value"`
- Property change events: `$Prop["Title"].add_PropertyChanged({ })`

### 3. Configuration Layering
- **Base**: `CAD/Configuration/` and `Vault/Configuration/` contain default XAML dialogs and .cfg files
- **Custom**: `.Custom` folders override base configurations (deployed customer implementations)
- **XML Definition Files**:
  - `Inventor.cfg` / `AutoCAD.cfg` - Path/filename definitions, property initialization
  - `File.xaml` / `Folder.xaml` - WPF dialog layouts with data bindings
  - `MenuDefinitions.xml` - Context menu commands mapped to PowerShell scripts

### 4. Localization
Multi-language support via `de-DE/` and `en-US/` folders:
- `UIStrings.xml` - UI labels (`$UIString["LBL1"]`, `$UIString["MNU5"]`)
- `PropertyTranslations.xml` - Property display name translations

### 5. Custom Entity (Custom Object) System
`CustomEntityDefinitions.json` defines custom Vault entities (Tasks, Projects, Organisations, etc.):
```json
{"dispNameField":"Task","idField":3,"nameField":"28ff95dd-0148-446a-8244-6936f6cea754"}
```
Each entity gets Create/Edit PowerShell scripts in `Vault.Custom/addinVault/Menus/`.

## Key Global Variables (PowerShell)
- `$dsWindow` - WPF window object (use `.FindName("ControlName")` to access XAML controls)
- `$Prop` - Property dictionary (read/write dialog fields)
- `$vaultConnection` - Active Vault connection object
- `$Document` - Inventor/AutoCAD document object (CAD context only)
- `$Application` - CAD application object
- `$UIString` / `$mPropTrans` - Localized string dictionaries

## Common Customization Points

### Extending File Dialogs
1. Edit `CAD.Custom/Configuration/Inventor.xaml` or `AutoCAD.xaml` for UI changes
2. Add validation functions in `CAD.Custom/addins/ADSK.QS.Default.ps1`:
   ```powershell
   function ValidateFileCustomRule {
       if (-not $Prop["DocNumber"].Value) { return $false }
       return $true
   }
   ```

### Adding Menu Commands (Vault)
1. Define command in `Vault.Custom/MenuDefinitions.xml`:
   ```xml
   <MyCommand Label="My Action" PSFile="MyAction.ps1" 
              NavigationTypes="File" Image="icon.ico"/>
   ```
2. Create `Vault.Custom/addinVault/Menus/MyAction.ps1` with command logic

### File Naming Rules
Modify `CAD/Configuration/Inventor.cfg`:
```xml
<FileNameDefinition>{Prop[DocNumber].Value}_{Prop[Revision].Value}</FileNameDefinition>
```

## Development Workflow

### Testing Changes
1. Restart Vault Explorer or CAD application to reload extensions
2. Check logs: `%TEMP%\` for PowerShell errors, `dataStandard4Vault.dll.log4net` for framework logs
3. Enable diagnostics in scripts: `$dsDiag.ShowLog()` and `$dsDiag.Inspect()`

### Debugging PowerShell
Use ISE or VSCode with PowerShell extension. Add breakpoints with:
```powershell
$dsDiag.ShowLog()  # Opens log viewer window
$dsDiag.Trace("Debug message: $($Prop["Title"].Value)")
```

### Deployment Notes
- **DO NOT modify base `CAD/` or `Vault/` folders** - changes will be overwritten on upgrades
- All customizations belong in `.Custom` folders
- MSI installers (`VDS-MFG-Installer.msi`, `VDS-PDMC-Installer.msi`) deploy pre-configured `.Custom` templates

## File Naming Convention
- `ADSK.QS.*` prefix = Autodesk QuickStart sample customizations (reference implementations)
- Base files (no prefix) = Core Data Standard framework (override with caution)

## Library Functions (ADSK.QS.*.Library.ps1)

### CAD Context (`ADSK.QS.CAD.Library.ps1`)
Reusable functions for Inventor/AutoCAD dialogs:

**Property & Folder Operations:**
- `mGetFolderPropValue($FldID, $DispName)` - Get single folder property value
- `mGetAllFolderProperties($FldID)` - Returns hashtable of all folder properties
- `mInheritProperties($Id, $MappingTable)` - Copy parent folder properties to file using mapping
- `mGetNewFileParentFldrByCat($Category)` - Find parent folder by category (e.g., "Project")

**Localization:**
- `mGetUIStrings()` - Load `UIStrings.xml` into hashtable
- `mGetPropTranslations()` - Load `PropertyTranslations.xml` for property name translations
- `mGetUIOverride()` / `mGetDBOverride()` - Check language override in `DSLanguages.xml`

**Usage Example:**
```powershell
# Inherit project properties from parent folder
$mSrc = mGetNewFileParentFldrByCat("CAT6") # Project category
$mMap = @{ "Project" = "Name"; "Project Number" = "Project Number" }
mInheritProperties $mSrc.Id $mMap
```

### Vault Context (`ADSK.QS.VLT.Library.ps1`)
Extended functions for Vault Explorer commands and dialogs:

**Entity Property Operations:**
- `mGetAllFileProperties($FileId)` - Get all file properties as hashtable
- `mGetAllFolderProperties($FolderId)` - Get all folder properties
- `mGetAllItemProperties($ItemId)` - Get all item properties
- `mGetAllChangeOrderProperties($ChangeOrderId)` - Get all ECO properties
- `mGetAllCustentProperties($CustentId)` - Get all custom object properties
- `mUpdateFldrProperties($FldId, $DispName, $Val)` - Update single folder property
- `mUpdateCustentProperties($CustentId, $DispName, $Val)` - Update custom object property

**Hierarchy & Navigation:**
- `mGetParentFldrByCat($Category)` - Walk up folder hierarchy to find category match
- `mGetFolderNumber($FileNumber, $nChar)` - Generate folder paths for sequential numbering (e.g., "$/xDMS/0/000/")

**Thin Client Link Generation:**
- `Adsk.CreateTcFileLink($FileFullVaultPath)` - Generate web link to file
- `Adsk.CreateTcFolderLink($FolderFullVaultPath)` - Generate web link to folder
- `Adsk.CreateTcItemLink($ItemMasterId)` - Generate web link to item
- `Adsk.CreateTcFileItemLink($FileFullVaultPath)` - Generate link to file's item
- `Adsk.CreateTcFileEcoLink($FileFullVaultPath)` - Generate link to file's ECO

**Security & Permissions:**
- `Adsk.GroupMemberOf($GroupName)` - Check if current user is in group
- `Adsk.CheckCfgAdminPermission()` - Check if user has Vault configuration permissions
- `mGetCUsPermissions()` - Get current user's permission IDs
- `mCopyEntACL($SourceEnt, $TargetEnt)` - Copy access control list between entities

**Advanced Operations:**
- `mSearchCustentOfCat($CatDispName)` - Search custom objects by category
- `mRecursivelyCreateFolders($sourceFolder, $targetFolder, $inclACL)` - Clone folder structure with properties/ACLs

**Usage Example:**
```powershell
# Get file properties and create web link
$fileProps = mGetAllFileProperties($fileId)
$webLink = Adsk.CreateTcFileLink($Prop["_FilePath"].Value)

# Check permissions before admin operation
if (Adsk.CheckCfgAdminPermission()) {
    # Perform administrative task
}
```

## External Dependencies
- `log4net.dll` - Logging framework
- `Newtonsoft.Json.dll` - JSON parsing
- `System.Management.Automation.dll` - PowerShell host
- Autodesk Vault SDK assemblies (31.0.0.0 = Vault 2026)

