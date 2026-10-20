# Copilot Instructions for TP05 Login & Registro

## Project Overview
**TP05** is an ASP.NET Core 9.0 MVC application focused on user authentication (registration and login). It's a simple 3-layer architecture with a single SQL Server database table.

- **Framework:** ASP.NET Core 9.0 with MVC pattern
- **Database:** SQL Server with Dapper ORM
- **Key Feature:** User registration and session-based login
- **Ports:** HTTP on 5021, HTTPS on 7164

## Architecture Pattern

### Data Flow
```
View (Razor .cshtml) → Controller (HomeController) → Model/BD (Dapper) → SQL Server
```

### Layer Responsibilities
- **Controllers** (`Controllers/HomeController.cs`): Handles HTTP requests, routes to views, manages ViewBag messages
- **Models** (`Models/Usuario.cs`, `Models/BD.cs`): Data models and database access layer combined
  - `Usuario`: Plain POCO with string properties for user data
  - `BD`: Singleton pattern instantiated per request; contains SQL queries and Dapper execution
- **Views** (`Views/Home/`): Razor templates with Bootstrap styling; use ASP.NET tag helpers for form binding

**Critical Pattern:** Database access is NOT separated into a repository/service layer—queries live directly in the `BD` class instantiated in controllers.

## Database Schema

Single table `Usuario` with columns:
```sql
id (int, PK), nombre (varchar 50), apellido (varchar 50), 
usuario (varchar 50), clave (varchar 50), tipo (varchar 50)
```

**Connection String Location:** Hardcoded in [Models/BD.cs](Models/BD.cs) line 7  
`Server=localhost;DataBase=TP05; Integrated Security=True; TrustServerCertificate=True;`

## Key Dependencies & Patterns

| Dependency | Version | Usage |
|-----------|---------|-------|
| Dapper | 2.1.79 | ORM for parameterized SQL queries |
| Microsoft.Data.SqlClient | 7.0.2 | SQL Server connectivity |
| Microsoft.AspNetCore.Session | 2.3.11 | Session state (configured in Program.cs) |

### Database Access Pattern (Dapper)
```csharp
string query = "SELECT ... WHERE usuario = @usuario AND clave = @clave";
using (SqlConnection connection = new SqlConnection(conexion))
{
    return connection.QueryFirstOrDefault<Usuario>(query, new { usuario, clave });
}
```
Always use parameterized queries via Dapper's anonymous object mappings.

## Common Developer Tasks

### Running the Application
```bash
dotnet run --launch-profile https
```
Launches at `https://localhost:7164` with hot reload enabled.

### Database Setup
1. Execute `script.sql` on local SQL Server to create `TP05` database and `Usuario` table
2. Ensure SQL Server is running and connection string in `BD.cs` points to correct instance

### Adding a New Action to HomeController
1. Add method to [HomeController.cs](Controllers/HomeController.cs)
2. Create matching `.cshtml` view in `Views/Home/[ActionName].cshtml`
3. Use ViewBag for passing messages: `ViewBag.Message = "Success";`
4. Views access BD via direct instantiation: `BD bd = new BD();`

### Error/Message Handling
- Success messages passed via `ViewBag.Message`
- Error messages passed via `ViewBag.Error`
- Views display with Bootstrap alert classes: `.alert-success`, `.alert-danger`

## Conventions & Anti-Patterns Found

**Conventions to Follow:**
- Views use ASP.NET tag helpers (`asp-action`, `asp-for`) for form binding
- Model properties are lowercase camelCase: `nombre`, `apellido`, `usuario`, `clave`
- File naming follows default MVC: `[ActionName].cshtml` in `Views/Home/`

**Issues to Avoid Perpetuating:**
- ⚠️ Passwords stored in plaintext (no hashing/salting)
- ⚠️ No input validation in views or models (no DataAnnotations)
- ⚠️ Connection string hardcoded (should be in `appsettings.json`)
- ⚠️ No HTTP POST handlers shown for Registro/InicioSesion (incomplete implementation)
- ⚠️ No error handling for database exceptions

## Files to Reference

| File | Purpose |
|------|---------|
| [Program.cs](Program.cs) | Startup config, middleware pipeline, session setup |
| [Controllers/HomeController.cs](Controllers/HomeController.cs) | All route handlers (incomplete) |
| [Models/BD.cs](Models/BD.cs) | SQL queries via Dapper |
| [Models/Usuario.cs](Models/Usuario.cs) | User data model |
| [Views/Home/Registro.cshtml](Views/Home/Registro.cshtml) | Registration form (bound to Usuario model) |
| [Views/Home/InicioSesion.cshtml](Views/Home/InicioSesion.cshtml) | Login form |
| [appsettings.json](appsettings.json) | Configuration (currently minimal) |
| [script.sql](script.sql) | Database schema creation |

## Important Implementation Notes

1. **View Model Binding:** Forms use `@model TP05.Models.Usuario` and ASP.NET automatically binds form data to model properties
2. **Session Usage:** Configured in [Program.cs](Program.cs) line 9 (`app.UseSession()`), but POST handlers not visible—you may need to implement session state management
3. **Validation:** Views show `<span asp-validation-for>` tags but no validators in model (add DataAnnotations if implementing validation)
4. **Database Queries:** Both SQL methods in [BD.cs](Models/BD.cs) expect exact matches (no LIKE searches or partial matches)
