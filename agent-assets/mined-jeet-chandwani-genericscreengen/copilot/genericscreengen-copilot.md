# GitHub Copilot Instructions - c# solution and projects

## Solution Architecture

### Folder Structure
1. Root folder contains the solution file
2. Subfolders for each project:
3. Every structural folder created under solution root must also be added to the `.sln` as a Solution Folder so it is visible in .NET Explorer view

### Project Structure
1. Solution folder has all other projects as subfolders
2. Each project has its own folder named after the project
3. Each project has a clear responsibility and follows single responsibility principle
4. Each class library project follows naming convention {projectname}Lib
5. Each console application project follows naming convention {projectname}App
6. Each project has its own `README.md` file
7. Each solution has its own  `development-session-log.txt` file for tracking changes in 'Other' folder under solution 

### Solution structure
1. Each solution will have below folder structure 
   - 'Diagrams' - folder for architecture and class diagrams
   - 'Docs' - folder for additional documentation
   - 'Samples' - folder for sample JSON configuration files
   - 'Source' - folder for source code files if needed
   - '.github' - folder for GitHub related files
   - `{name}InterfacesLib` - contains all interfaces and enums
   - `{name}FactoryLib` - contains factory pattern implementation - has factory interface and default factory implementation
   - `{name}ImplementationsLib` - contains all implementation classes, base classes, and common utilities
   - `{name}UtilsLib` - contains common utilities and helper classes
   - `MyTestConsoleApp` - console application for testing and demonstration
2. Required structural folders (`Diagrams`, `Docs`, `Samples`, `Source`, `.github`, `Other`) must always be present both physically on disk and as Solution Folders in the `.sln`
3. Source code projects should be organized under the `Source` solution folder in .NET Explorer


## Coding Standards & Conventions
1. Each class, interface, and enum should be in its own file named after it.

### C# Code Style
1. **Target Framework**: .NET 8.0
2. **Nullable**: Enabled
3. **ImplicitUsings**: Enabled
4. **NO Top-Level Statements** in console applications - always use traditional Main method
5. Use traditional namespace declarations (not file-scoped)
6. Follow Hungarian notation with descriptive variable names where applicable
7. Use XML documentation comments for all public interfaces and classes
8. Use `readonly` for immutable properties
9. **ID values**: kebab-case format (e.g., "eg-001", "trf-002")

### Interface Design Patterns
1. **Interface Segregation**: Separate interfaces for different concerns, start with 1 class lib project dedicated to interfaces
2. **Inheritance Hierarchies**: Use base interfaces wherever possible for common features
3. **Factory Pattern**: Use factory pattern for creating instances dynamically based upon lib path and fully qualified class name
4. **Template Method Pattern**: Base classes provide virtual methods for derived class customization

### Performance Optimization Patterns
1. **Caching**: Parse JSON o config data once, cache results in protected variables
2. **Parameterized Methods**: Use generic parsing methods instead of specific ones
3. **Template Method**: Override `InitAfterLoad()` for post-load initialization

### Naming Conventions
1. **Class names**: UpperCamelCase (e.g., `CMyClass`) starts with C for classes, I for interfaces, E for enums, A for abstract classes
  - **Interfaces**: Start with `I` (e.g., `IMyInterface`)
  - **Abstract classes**: Start with `A` (e.g., `AMyAbstractClass`)
  - **Classes**: Start with `C` (e.g., `CMyClass`)
  - **Enums**: Start with `E` (e.g., `EMyEnum`)
2. **Method names**: UpperCamelCase (e.g., `MyMethod`)
3. **Variable names**: UpperCamelCase, with 3-5 lowercase letter prefixes base upon variable types
  - **Lists**: Use `lst` prefix for lists
  - **Strings**: Use `str` for strings
  - **Arrays**: Use `arr` for arrays
  - **Interfaces**: Use `itf` for interfaces
  - **Dictionaries**: Use `dict` for dictionaries
  - **Integers**: Use `i` for integers
  - **Booleans**: Use `f` for booleans
4. **Property names**: PascalCase (e.g., `MyProperty`)
5. **Constants**: UPPERCASE with underscores (e.g., `MY_CONSTANT`)
6. **Enums**: PascalCase starting with E for enums (e.g., `EMyEnum`)
7. **File names**: same as class or interface name


### Error Handling Standards
- Always use `out string strError` parameters for methods that can fail and return boolean success indicators, an d out varibale for return item 
- Use try-catch blocks for JSON parsing and file I/O operations
- Return boolean success indicators
- Provide detailed, contextual error messages
- Handle `JsonException` and general `Exception` separately

## JSON Configuration Standards

### JSON Schema
- Use a JSON schema to define the structure of your configuration files.
- Include examples in the schema for clarity.

## Development Session Tracking

### Log File Maintenance
- **File**: `development-session-log.txt`
- **Format**: Markdown with timestamps
- **Structure**: Branch-organized with prompt tracking
- **Update**: After every significant change

### Branch Organization

## Branch creation and tracking
- Always create a new branch for each new feature or change if on master, and update the session log with branch name, creation date, and status (ACTIVE/CLOSED)
- if already on a branch, update the session log with the new prompt and timestamp for each change made on that branch.

```markdown
# Branch: [branch-name]
**Branch Created**: [date]
**Branch Status**: ACTIVE/CLOSED
```

## Factory Pattern Implementation

### Interface Definition
1. Each interface should derive from 'ICanInit' interface
2. ICanInit interface will have only 1 method `bool Init(object objInputParam, out string strError)`


### Implementation Pattern
1. Each implementation class should derive from a base class that provides common functionality
2. Base classes should provide virtual methods for derived class customization

## Key Interfaces to Remember
1. ICanInit
2. I{solution}Factory

## When Adding New Features

1. **Check existing patterns** - Follow established conventions
2. **Update interfaces first** - Define contracts before implementation  
3. **Implement in base classes** - Make utilities available to derived classes
4. **Cache for performance** - Parse once, store in protected variables
5. **Update constants** - use constants instead of string literal except for error messages
6. **Document in session log** - Track all changes with timestamps
7. **Follow JSON standards** - Use established naming and structure patterns

**Remember**: These policies are designed to maintain consistency and adhere to best practices. They emphasizes clean architecture, performance optimization, and consistent coding standards. Always maintain the established patterns and update the session log for tracking purposes.
